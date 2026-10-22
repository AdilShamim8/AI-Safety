"""calibrators — validation-only score calibration fits.

The Chapter 06 discipline this module enforces: a calibration map is
fit on a **validation split only** and applied untouched to the
**evaluation split** — fitting on the items you report is the
small-n overfitting Chapter 02 diagnosed wearing a calibration costume.
Every calibrator is a two-stage object: ``fit`` consumes the validation
(scores, outcomes) and freezes; ``transform`` maps new scores through
the frozen map. Fitting twice raises; transforming before fitting
raises.

Three maps, in increasing fit-capacity order:

* :class:`IdentityCalibrator` — no parameters; the raw score as-is
  (the baseline every other map must beat *on the evaluation split* to
  justify its existence).
* :class:`PlattCalibrator` — the two-parameter logistic map
  ``sigmoid(a*s + b)``, fit by deterministic Newton iterations (fixed
  initialization, fixed iteration count, no randomness). Parameters
  are bounded for finiteness under near-separable validation splits
  (the bound is stated in the report, not hidden).
* :class:`HistogramCalibrator` — the equal-width bin map: each bin's
  validation accuracy replaces the scores that fall in it. Empty
  validation bins fall back to the validation-split accuracy (the
  fallback is documented, never silent).

All three are stdlib-only and deterministic: the same validation split
produces byte-identical transforms.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass, field

from ai_safety_course.calibration.metrics import (
    CalibrationError,
    _validate_scores_outcomes,
)

#: Bound on |a| and |b| for the Platt map (near-separable validation
#: splits drive the MLE to infinity; the bound keeps every downstream
#: number finite and is reported with the fit).
PLATT_BOUND = 25.0

#: Newton iterations for the Platt fit (fixed; no early stop on
#: oscillation — determinism over micro-optimization).
PLATT_ITERATIONS = 100


def _sigmoid(x: float) -> float:
    """Numerically safe logistic function."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    exponent = math.exp(x)
    return exponent / (1.0 + exponent)


class _BaseCalibrator:
    """Shared fit/transform state machine (fit once, then frozen)."""

    _fitted: bool = False

    def fit(self, scores: Sequence[float], outcomes: Sequence[int]) -> "_BaseCalibrator":
        """Fit on the validation split (once)."""
        if self._fitted:
            raise CalibrationError(
                f"{type(self).__name__} is already fitted; a calibration map "
                "is fit once on its validation split and never refit"
            )
        clean_scores, clean_outcomes = _validate_scores_outcomes(scores, outcomes)
        self._fit_impl(clean_scores, clean_outcomes)
        self._fitted = True
        return self

    def transform(self, scores: Sequence[float]) -> tuple[float, ...]:
        """Map scores through the frozen calibration map."""
        if not self._fitted:
            raise CalibrationError(
                f"{type(self).__name__}.transform called before fit "
                "(fail-closed: no accidental identity fallback)"
            )
        clean: list[float] = []
        for score in scores:
            if not isinstance(score, (int, float)) or isinstance(score, bool):
                raise CalibrationError(f"score must be a number, got {score!r}")
            if not math.isfinite(float(score)) or not 0.0 <= float(score) <= 1.0:
                raise CalibrationError(f"score must be in [0, 1], got {score!r}")
            clean.append(float(score))
        return tuple(self._transform_impl(clean))

    def _fit_impl(self, scores: list[float], outcomes: list[int]) -> None:
        raise NotImplementedError

    def _transform_impl(self, scores: list[float]) -> list[float]:
        raise NotImplementedError

    def fit_report(self) -> str:
        """The frozen map's parameters, for the report's provenance."""
        if not self._fitted:
            raise CalibrationError("fit_report before fit")
        return self._fit_report_impl()

    def _fit_report_impl(self) -> str:
        raise NotImplementedError


class IdentityCalibrator(_BaseCalibrator):
    """The raw score, unchanged — the baseline map.

    Every other calibrator must beat this one *on the evaluation
    split* (Brier/log loss) to justify its parameters; a map that only
    helps on the split it was fit on is overfitting with extra steps.
    """

    _validation_accuracy: float = 0.0

    def _fit_impl(self, scores: list[float], outcomes: list[int]) -> None:
        self._validation_accuracy = sum(outcomes) / len(outcomes)

    def _transform_impl(self, scores: list[float]) -> list[float]:
        return list(scores)

    def _fit_report_impl(self) -> str:
        return f"identity (no parameters; validation accuracy " f"{self._validation_accuracy:.4f})"


@dataclass
class PlattCalibrator(_BaseCalibrator):
    """The two-parameter logistic map ``sigmoid(a*s + b)``.

    Fit by Newton's method on the validation split: fixed zero
    initialization, ``PLATT_ITERATIONS`` iterations, parameters bounded
    to ±``PLATT_BOUND`` (near-separable splits drive the MLE to
    infinity; the bound is the stated, finite stand-in).
    """

    a: float = 0.0
    b: float = 0.0

    def _fit_impl(self, scores: list[float], outcomes: list[int]) -> None:
        a, b = 0.0, 0.0
        for _ in range(PLATT_ITERATIONS):
            probabilities = [_sigmoid(a * s + b) for s in scores]
            # Gradient of the log-likelihood.
            ga = sum((y - p) * s for s, y, p in zip(scores, outcomes, probabilities, strict=True))
            gb = sum(y - p for y, p in zip(outcomes, probabilities, strict=True))
            # Hessian (negative-definite; Newton ascent with damping).
            haa = sum(p * (1 - p) * s * s for s, p in zip(scores, probabilities, strict=True))
            hab = sum(p * (1 - p) * s for s, p in zip(scores, probabilities, strict=True))
            hbb = sum(p * (1 - p) for p in probabilities)
            determinant = haa * hbb - hab * hab
            if determinant <= 1e-12:
                break  # degenerate geometry (e.g., all scores equal)
            # Newton step: theta += H^-1 g with H = [[haa, hab], [hab, hbb]].
            delta_a = (hbb * ga - hab * gb) / determinant
            delta_b = (haa * gb - hab * ga) / determinant
            step = max(1.0, abs(delta_a), abs(delta_b))
            a += delta_a / step
            b += delta_b / step
            a = max(-PLATT_BOUND, min(PLATT_BOUND, a))
            b = max(-PLATT_BOUND, min(PLATT_BOUND, b))
        self.a, self.b = a, b

    def _transform_impl(self, scores: list[float]) -> list[float]:
        return [_sigmoid(self.a * s + self.b) for s in scores]

    def _fit_report_impl(self) -> str:
        return (
            f"platt: sigmoid({self.a:.4f} * s + {self.b:.4f}) "
            f"(Newton, {PLATT_ITERATIONS} iterations, |params| <= {PLATT_BOUND})"
        )


@dataclass
class HistogramCalibrator(_BaseCalibrator):
    """The equal-width bin map: bin validation accuracy replaces score.

    Empty validation bins fall back to the validation-split accuracy
    (documented fallback — the map must be total, and inventing a bin
    center prior would be a silent prior injection).
    """

    num_bins: int = 10
    bin_accuracies: tuple[float, ...] = field(default_factory=tuple)
    fallback_accuracy: float = 0.5

    def _fit_impl(self, scores: list[float], outcomes: list[int]) -> None:
        if not isinstance(self.num_bins, int) or self.num_bins < 1:
            raise CalibrationError(f"num_bins must be an int >= 1, got {self.num_bins!r}")
        counts = [0] * self.num_bins
        correct = [0] * self.num_bins
        for score, outcome in zip(scores, outcomes, strict=True):
            index = min(int(score * self.num_bins), self.num_bins - 1)
            counts[index] += 1
            correct[index] += outcome
        self.fallback_accuracy = sum(outcomes) / len(outcomes)
        accuracies = [
            (correct[k] / counts[k]) if counts[k] > 0 else self.fallback_accuracy
            for k in range(self.num_bins)
        ]
        self.bin_accuracies = tuple(accuracies)

    def _transform_impl(self, scores: list[float]) -> list[float]:
        return [self.bin_accuracies[min(int(s * self.num_bins), self.num_bins - 1)] for s in scores]

    def _fit_report_impl(self) -> str:
        cells = ", ".join(f"{acc:.3f}" for acc in self.bin_accuracies)
        return (
            f"histogram: K={self.num_bins} bin accuracies ({cells}); "
            f"empty-bin fallback {self.fallback_accuracy:.4f}"
        )


def calibrator_from_config(config: object) -> _BaseCalibrator:
    """Build a calibrator from a config block (fail-closed on unknowns)."""
    if isinstance(config, str):
        kind, params = config, {}
    elif isinstance(config, dict):
        kind = config.get("kind")
        params = {k: v for k, v in config.items() if k != "kind"}
    else:
        raise CalibrationError(f"calibrator config must be a string or mapping, got {config!r}")
    if kind == "identity":
        if params:
            raise CalibrationError(f"identity takes no parameters, got {sorted(params)}")
        return IdentityCalibrator()
    if kind == "platt":
        if params:
            raise CalibrationError(f"platt takes no parameters, got {sorted(params)}")
        return PlattCalibrator()
    if kind == "histogram":
        unknown = set(params) - {"num_bins"}
        if unknown:
            raise CalibrationError(
                f"unknown histogram params: {sorted(unknown)}; supported: num_bins"
            )
        return HistogramCalibrator(num_bins=int(params.get("num_bins", 10)))
    raise CalibrationError(
        f"unknown calibrator kind {kind!r}; supported: identity, platt, histogram"
    )


__all__ = [
    "HistogramCalibrator",
    "IdentityCalibrator",
    "PLATT_BOUND",
    "PLATT_ITERATIONS",
    "PlattCalibrator",
    "calibrator_from_config",
]
