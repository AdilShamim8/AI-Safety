"""metrics — calibration measurement with bin counts and intervals.

This module implements the Chapter 06 measurement discipline
(``chapters/06-honesty-uncertainty-and-selective-prediction/README.md``
sections 3.2–3.3) as code:

* the **reliability table** — equal-width bins with per-bin count, mean
  confidence, realized accuracy, and a Wilson 95% interval on each
  bin accuracy (the chapter's rule: report bin counts with every ECE,
  because a 6-item bin reading 0.000 accuracy carries a Wilson upper
  bound near 0.39);
* **ECE** — the bin-weighted |accuracy − confidence| sum, always
  reported *next to* its bin populations (ECE is a binning artifact:
  it depends on K and on bin populations);
* **Brier** and **log loss** — proper scoring rules that punish
  miscalibration and reward discrimination (log loss clipped to a
  stated epsilon, never infinite);
* the **mean gap** — mean confidence minus accuracy, reported as the
  one-number marginal it is, never confused with ECE (off-middle bins
  cancel in the average; the shape survives only in ECE).

Binary outcomes throughout: ``outcome`` is 1 (correct/true) or 0
(wrong/false), ``score`` in [0, 1]. Every aggregate carries its
explicit denominator; every rate carries its interval. Plain stdlib
math only; the Wilson z is the full-precision quantile.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from ai_safety_course.evaluation.metrics import wilson_interval

#: Two-sided 95% normal quantile at full precision (module contract:
#: the P02/P03 packages never round the multiplier).
Z_95 = 1.959963984540054

#: Clipping bound for log loss (scores of exactly 0/1 would give
#: infinite loss; the clip is stated, never silent).
LOG_EPS = 1e-15


class CalibrationError(ValueError):
    """Raised on invalid calibration inputs (fail-closed, never NaN)."""


@dataclass(frozen=True)
class ReliabilityBin:
    """One equal-width reliability bin.

    Attributes:
        index: bin number (0-based; bin k covers [k/K, (k+1)/K)).
        lower: bin lower edge (inclusive).
        upper: bin upper edge (inclusive for the last bin).
        count: number of items in the bin (the denominator).
        mean_confidence: mean score of the bin's items.
        accuracy: realized accuracy (mean outcome) of the bin's items.
        accuracy_interval: Wilson 95% interval on the bin accuracy.
    """

    index: int
    lower: float
    upper: float
    count: int
    mean_confidence: float
    accuracy: float
    accuracy_interval: tuple[float, float]

    @property
    def gap(self) -> float:
        """Signed accuracy minus confidence (the bin's miscalibration)."""
        return self.accuracy - self.mean_confidence

    @property
    def abs_gap(self) -> float:
        """|accuracy − confidence| (the ECE contribution's numerator)."""
        return abs(self.accuracy - self.mean_confidence)

    def __str__(self) -> str:
        return (
            f"bin[{self.lower:.1f}, {self.upper:.1f}): n={self.count} "
            f"conf={self.mean_confidence:.3f} acc={self.accuracy:.3f} "
            f"({self.accuracy_interval[0]:.3f}, {self.accuracy_interval[1]:.3f}) "
            f"gap={self.gap:+.3f}"
        )


@dataclass(frozen=True)
class ReliabilityTable:
    """The binned reliability table for one (scores, outcomes) set.

    Attributes:
        num_bins: the binning width K (ECE's hidden parameter).
        bins: the non-empty bins, ascending.
        total: the total item count (the ECE denominator).
    """

    num_bins: int
    bins: tuple[ReliabilityBin, ...]
    total: int

    @property
    def ece(self) -> float:
        """Expected calibration error: Σ (n_k/n)·|acc_k − conf_k|."""
        if self.total == 0:
            raise CalibrationError("reliability table is empty")
        return sum((bin_.count / self.total) * bin_.abs_gap for bin_ in self.bins)

    @property
    def bin_counts(self) -> tuple[int, ...]:
        """Per-bin counts, ascending by bin index (report with every ECE)."""
        return tuple(bin_.count for bin_ in self.bins)

    def ece_statement(self) -> str:
        """ECE rendered with its binning and populations (the discipline)."""
        counts = ", ".join(str(c) for c in self.bin_counts)
        return f"ECE = {self.ece:.4f} at K = {self.num_bins} (bin counts: {counts})"

    def table_lines(self) -> tuple[str, ...]:
        """One line per bin (deterministic order, for reports)."""
        return tuple(str(bin_) for bin_ in self.bins)


def _validate_scores_outcomes(
    scores: Sequence[float], outcomes: Sequence[int]
) -> tuple[list[float], list[int]]:
    """Fail-closed validation of the paired inputs."""
    if len(scores) != len(outcomes):
        raise CalibrationError(
            f"scores and outcomes must have equal length, got " f"{len(scores)} vs {len(outcomes)}"
        )
    if not scores:
        raise CalibrationError("calibration needs at least one item")
    clean_scores: list[float] = []
    clean_outcomes: list[int] = []
    for score, outcome in zip(scores, outcomes, strict=True):
        if not isinstance(score, (int, float)) or isinstance(score, bool):
            raise CalibrationError(f"score must be a number, got {score!r}")
        if not math.isfinite(float(score)) or not 0.0 <= float(score) <= 1.0:
            raise CalibrationError(f"score must be in [0, 1], got {score!r}")
        if outcome not in (0, 1) or isinstance(outcome, bool):
            raise CalibrationError(f"outcome must be 0 or 1, got {outcome!r}")
        clean_scores.append(float(score))
        clean_outcomes.append(int(outcome))
    return clean_scores, clean_outcomes


def reliability_table(
    scores: Sequence[float], outcomes: Sequence[int], num_bins: int = 10
) -> ReliabilityTable:
    """Build the equal-width reliability table (fail-closed).

    Args:
        scores: confidence scores in [0, 1].
        outcomes: binary outcomes (1 = correct/true).
        num_bins: binning width K (must be >= 1; the ECE parameter).
    """
    if not isinstance(num_bins, int) or isinstance(num_bins, bool) or num_bins < 1:
        raise CalibrationError(f"num_bins must be an int >= 1, got {num_bins!r}")
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    buckets: dict[int, list[float]] = {}
    bucket_outcomes: dict[int, list[int]] = {}
    for score, outcome in zip(clean_scores, clean_outcomes, strict=True):
        index = min(int(score * num_bins), num_bins - 1)
        buckets.setdefault(index, []).append(score)
        bucket_outcomes.setdefault(index, []).append(outcome)
    bins = []
    for index in sorted(buckets):
        members = buckets[index]
        member_outcomes = bucket_outcomes[index]
        count = len(members)
        mean_conf = sum(members) / count
        accuracy = sum(member_outcomes) / count
        interval = wilson_interval(sum(member_outcomes), count, z=Z_95)
        bins.append(
            ReliabilityBin(
                index=index,
                lower=index / num_bins,
                upper=(index + 1) / num_bins,
                count=count,
                mean_confidence=mean_conf,
                accuracy=accuracy,
                accuracy_interval=(interval.lower, interval.upper),
            )
        )
    return ReliabilityTable(num_bins=num_bins, bins=tuple(bins), total=len(clean_scores))


def brier_score(scores: Sequence[float], outcomes: Sequence[int]) -> float:
    """Mean squared score versus outcome (the proper scoring rule).

    ``(1/n) Σ (s_i − y_i)^2`` — minimized in expectation only by true
    probabilities; punishes miscalibration and rewards discrimination.
    """
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    return sum((s - y) ** 2 for s, y in zip(clean_scores, clean_outcomes, strict=True)) / len(
        clean_scores
    )


def log_loss(scores: Sequence[float], outcomes: Sequence[int]) -> float:
    """Clipped negative log-likelihood (proper scoring rule).

    ``−(1/n) Σ [y·ln s + (1−y)·ln(1−s)]`` with s clipped to
    [LOG_EPS, 1−LOG_EPS] — the clip is stated in the report, never
    silent, and the epsilon is part of the metric's identity.
    """
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    total = 0.0
    for s, y in zip(clean_scores, clean_outcomes, strict=True):
        clipped = min(max(s, LOG_EPS), 1.0 - LOG_EPS)
        total += y * math.log(clipped) + (1 - y) * math.log(1.0 - clipped)
    return -total / len(clean_scores)


def mean_gap(scores: Sequence[float], outcomes: Sequence[int]) -> float:
    """Mean confidence minus accuracy — the one-number marginal.

    Reported as itself, never as a calibration measure: off-middle bins
    cancel in the average (the chapter's instrument-V example: mean gap
    −0.6 points with ECE 0.187).
    """
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    mean_conf = sum(clean_scores) / len(clean_scores)
    accuracy = sum(clean_outcomes) / len(clean_outcomes)
    return mean_conf - accuracy


def accuracy_rate(outcomes: Sequence[int]) -> float:
    """Full-coverage accuracy with its explicit denominator available."""
    if not outcomes:
        raise CalibrationError("accuracy needs at least one outcome")
    for outcome in outcomes:
        if outcome not in (0, 1) or isinstance(outcome, bool):
            raise CalibrationError(f"outcome must be 0 or 1, got {outcome!r}")
    return sum(outcomes) / len(outcomes)


__all__ = [
    "CalibrationError",
    "LOG_EPS",
    "ReliabilityBin",
    "ReliabilityTable",
    "Z_95",
    "accuracy_rate",
    "brier_score",
    "log_loss",
    "mean_gap",
    "reliability_table",
]
