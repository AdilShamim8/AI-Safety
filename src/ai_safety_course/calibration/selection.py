"""selection — selective prediction, risk–coverage, and the abstention ledger.

This module implements the Chapter 06 selective-prediction discipline
(``chapters/06-honesty-uncertainty-and-selective-prediction/README.md``
section 3.3) as code:

* **rank-based selective prediction** — items sorted by score descending,
  answered top-m; the risk–coverage curve is selective risk R(m) as a
  function of coverage C = m/n;
* **AURC** — the mean of R(m) over m = 1..n (the average selective
  risk if every coverage level were equally likely);
* **the oracle curve** — ranking by outcome itself (all correct items
  first); the best achievable curve for this (scores, outcomes) set,
  whose gap to the instrument's AURC measures the ranking information
  the score fails to extract;
* **threshold policies** — answer iff s >= tau, reported at operating
  points with explicit answered-count denominators and Wilson
  intervals (selective risk is a *conditional* rate whose denominator
  moves with tau);
* **the false-abstention side** — the clearly-answerable items the
  policy declined: an abstention report without a false-abstention
  rate is half a confusion matrix (the chapter's XSTest-side lesson).

Fail-closed throughout; deterministic ordering (ties broken by item
index, never by sort instability); plain stdlib only.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass

from ai_safety_course.calibration.metrics import (
    Z_95,
    CalibrationError,
    _validate_scores_outcomes,
)
from ai_safety_course.evaluation.metrics import wilson_interval


@dataclass(frozen=True)
class RiskCoveragePoint:
    """One operating point on the risk–coverage curve.

    Attributes:
        rank: m, the number of items answered (top-m by score).
        coverage: m/n.
        answered: the answered count (selective risk's denominator).
        errors: errors among the answered items.
        selective_risk: errors/answered (conditional rate).
        risk_interval: Wilson 95% on the selective risk.
    """

    rank: int
    coverage: float
    answered: int
    errors: int
    selective_risk: float
    risk_interval: tuple[float, float]

    def __str__(self) -> str:
        return (
            f"m={self.rank}: coverage={self.coverage:.3f} "
            f"risk={self.selective_risk:.3f} "
            f"[{self.risk_interval[0]:.3f}, {self.risk_interval[1]:.3f}] "
            f"({self.errors}/{self.answered})"
        )


@dataclass(frozen=True)
class RiskCoverageCurve:
    """The full rank-based risk–coverage curve for one instrument.

    Attributes:
        points: operating points m = 1..n, ascending.
        total: n, the full item count.
        aurc: the mean of R(m) over m = 1..n.
        oracle_aurc: the AURC of the oracle ranking (correct items
            first) — the best achievable for this set.
        aurc_gap: instrument AURC minus oracle AURC, the ranking
            information the score failed to extract.
    """

    points: tuple[RiskCoveragePoint, ...]
    total: int

    @property
    def aurc(self) -> float:
        """Mean selective risk over all coverage levels (m = 1..n)."""
        if not self.points:
            raise CalibrationError("risk-coverage curve is empty")
        return sum(point.selective_risk for point in self.points) / len(self.points)

    @property
    def full_coverage_risk(self) -> float:
        """R(n): the error rate of answering everything."""
        return self.points[-1].selective_risk

    def at_coverage(self, coverage: float) -> RiskCoveragePoint:
        """The operating point nearest a target coverage (fail-closed)."""
        if not 0.0 < coverage <= 1.0:
            raise CalibrationError(f"coverage must be in (0, 1], got {coverage!r}")
        target = max(1, min(round(coverage * self.total), self.total))
        return self.points[target - 1]

    def curve_lines(self) -> tuple[str, ...]:
        """One line per operating point (deterministic, for reports)."""
        return tuple(str(point) for point in self.points)


def risk_coverage_curve(scores: Sequence[float], outcomes: Sequence[int]) -> RiskCoverageCurve:
    """Build the rank-based risk–coverage curve (ties by item index).

    Items are sorted by score descending; the point at rank m answers
    the top m and reports selective risk with its Wilson interval.
    """
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    order = sorted(range(len(clean_scores)), key=lambda i: (-clean_scores[i], i))
    points: list[RiskCoveragePoint] = []
    errors_so_far = 0
    for rank in range(1, len(order) + 1):
        outcome = clean_outcomes[order[rank - 1]]
        if outcome == 0:
            errors_so_far += 1
        interval = wilson_interval(errors_so_far, rank, z=Z_95)
        points.append(
            RiskCoveragePoint(
                rank=rank,
                coverage=rank / len(clean_scores),
                answered=rank,
                errors=errors_so_far,
                selective_risk=errors_so_far / rank,
                risk_interval=(interval.lower, interval.upper),
            )
        )
    return RiskCoverageCurve(points=tuple(points), total=len(clean_scores))


def oracle_aurc(outcomes: Sequence[int]) -> float:
    """AURC of the oracle ranking: all correct items answered first.

    The best achievable curve for any score on this outcome set — the
    ceiling the instrument's AURC gap is measured against.
    """
    if not outcomes:
        raise CalibrationError("oracle needs at least one outcome")
    for outcome in outcomes:
        if outcome not in (0, 1) or isinstance(outcome, bool):
            raise CalibrationError(f"outcome must be 0 or 1, got {outcome!r}")
    correct = sum(outcomes)
    total = len(outcomes)
    risks: list[float] = []
    errors = 0
    for rank in range(1, total + 1):
        if rank > correct:
            errors += 1
        risks.append(errors / rank)
    return sum(risks) / total


@dataclass(frozen=True)
class ThresholdPolicy:
    """A fixed confidence threshold: answer iff s >= tau.

    Attributes:
        tau: the threshold in [0, 1] (tau = 0 answers everything).
        answered: items with s >= tau (the answered-count denominator).
        errors: errors among the answered.
        false_abstentions: clearly-answerable items declined (s < tau
            with outcome 1) — the over-refusal side of the ledger.
    """

    tau: float
    answered: int
    errors: int
    false_abstentions: int
    total: int

    @property
    def coverage(self) -> float:
        return self.answered / self.total if self.total else 0.0

    @property
    def selective_risk(self) -> float:
        """Conditional error rate among answered (denominator explicit)."""
        if self.answered == 0:
            raise CalibrationError(
                "selective risk is undefined when nothing is answered "
                "(tau above every score); report coverage 0 instead"
            )
        return self.errors / self.answered

    @property
    def false_abstention_rate(self) -> float:
        """Answerable-but-declined rate (the half-confusion-matrix side)."""
        if self.total == 0:
            raise CalibrationError("threshold policy over an empty set")
        return self.false_abstentions / self.total


def threshold_policy(
    scores: Sequence[float], outcomes: Sequence[int], tau: float
) -> ThresholdPolicy:
    """Evaluate answer-iff-s>=tau with both sides of the ledger."""
    if not isinstance(tau, (int, float)) or isinstance(tau, bool):
        raise CalibrationError(f"tau must be a number, got {tau!r}")
    if not math.isfinite(float(tau)) or not 0.0 <= float(tau) <= 1.0:
        raise CalibrationError(f"tau must be in [0, 1], got {tau!r}")
    clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
    answered = 0
    errors = 0
    false_abstentions = 0
    for score, outcome in zip(clean_scores, clean_outcomes, strict=True):
        if score >= float(tau):
            answered += 1
            if outcome == 0:
                errors += 1
        else:
            if outcome == 1:
                false_abstentions += 1
    return ThresholdPolicy(
        tau=float(tau),
        answered=answered,
        errors=errors,
        false_abstentions=false_abstentions,
        total=len(clean_scores),
    )


def aurc_gap(scores: Sequence[float], outcomes: Sequence[int]) -> float:
    """Instrument AURC minus oracle AURC (the ranking-information gap)."""
    curve = risk_coverage_curve(scores, outcomes)
    return curve.aurc - oracle_aurc(outcomes)


__all__ = [
    "RiskCoverageCurve",
    "RiskCoveragePoint",
    "ThresholdPolicy",
    "aurc_gap",
    "oracle_aurc",
    "risk_coverage_curve",
    "threshold_policy",
]
