"""metrics — rate metrics with Wilson intervals and the paired ledger.

This module implements the Chapter 02 statistical discipline exactly
(``chapters/02-evaluation-science-and-experimental-design/README.md``,
section 3.5): every rate metric is reported as numerator over an explicit
denominator with a Wilson 95% interval, computed as

.. code-block:: text

               p̂ + z²/2n                z · sqrt(p̂(1−p̂)/n + z²/4n²)
    center  =  -----------     half  =  ---------------------------
               1 + z²/n                   1 + z²/n

with z = 1.96. The Wilson interval is used instead of the naive (Wald)
interval because it behaves near p̂ = 0 and p̂ = 1, where the Wald standard
error collapses to a false claim of zero uncertainty (the Chapter 02
counterexample). All arithmetic here is plain stdlib float math — the
known-value tests pin it against hand-computed Chapter 02 examples.

The paired ledger enforces the "both sides of the confusion matrix" rule:
a refusal rate on unsafe prompts is only reported together with the
false-refusal rate on safe prompts, each with its own denominator.
"""

import math
from collections.abc import Sequence
from dataclasses import dataclass

#: Two-sided 95% normal quantile, the Chapter 02 convention (z² = 3.8416).
Z_95 = 1.96


class MetricsError(ValueError):
    """Raised on invalid rate inputs or an unbalanceable ledger (fail-closed)."""


@dataclass(frozen=True)
class WilsonInterval:
    """Wilson score interval for a binomial rate.

    Attributes:
        center: the interval's midpoint (p̂ + z²/2n)/(1 + z²/n).
        half_width: half the interval width — the honest +/- attached to
            the observed rate.
        z: the normal quantile used (1.96 for 95%).
        successes: numerator k.
        denominator: denominator n (the explicit ledger denominator).
    """

    center: float
    half_width: float
    z: float
    successes: int
    denominator: int

    @property
    def lower(self) -> float:
        """Lower bound of the interval."""
        return self.center - self.half_width

    @property
    def upper(self) -> float:
        """Upper bound of the interval."""
        return self.center + self.half_width

    def __str__(self) -> str:
        return (
            f"[{self.lower:.4f}, {self.upper:.4f}] "
            f"(center {self.center:.4f}, half-width {self.half_width:.4f}, z={self.z:g})"
        )


def wilson_interval(successes: int, denominator: int, z: float = Z_95) -> WilsonInterval:
    """Compute the Wilson interval for ``successes``/``denominator``.

    Args:
        successes: number of successes k (0 <= k <= n).
        denominator: number of trials n (n >= 1) — the explicit
            denominator that Chapter 02 requires next to every rate.
        z: normal quantile; defaults to 1.96 (95%).

    Returns:
        The :class:`WilsonInterval` (center, half-width, bounds).

    Raises:
        MetricsError: if n < 1, k outside [0, n], or z <= 0.
    """
    if denominator < 1:
        raise MetricsError(f"denominator must be >= 1, got {denominator}")
    if not 0 <= successes <= denominator:
        raise MetricsError(f"successes must be within [0, {denominator}], got {successes}")
    if z <= 0:
        raise MetricsError(f"z must be positive, got {z}")

    p_hat = successes / denominator
    z_squared = z * z
    denom_factor = 1.0 + z_squared / denominator
    center = (p_hat + z_squared / (2.0 * denominator)) / denom_factor
    variance = p_hat * (1.0 - p_hat) / denominator + z_squared / (4.0 * denominator**2)
    half_width = z * math.sqrt(variance) / denom_factor
    return WilsonInterval(
        center=center, half_width=half_width, z=z, successes=successes, denominator=denominator
    )


@dataclass(frozen=True)
class MetricSummary:
    """A named rate metric with explicit denominator and Wilson interval.

    ``__str__`` renders the Chapter 02 reporting style: numerator,
    denominator, rate, and the interval — never a bare percentage.
    """

    name: str
    successes: int
    denominator: int
    rate: float
    interval: WilsonInterval

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.successes}/{self.denominator} ({self.rate:.2%}), "
            f"Wilson CI [{self.interval.lower:.1%}, {self.interval.upper:.1%}] "
            f"at z={self.interval.z:g}"
        )


def rate_metric(name: str, successes: int, denominator: int, z: float = Z_95) -> MetricSummary:
    """Build a :class:`MetricSummary` for ``successes``/``denominator``.

    Args:
        name: metric display name (e.g. ``"refusal | expected=refuse"``).
        successes: numerator.
        denominator: explicit denominator (n >= 1).
        z: normal quantile, default 1.96.

    Returns:
        The summarized metric.

    Raises:
        MetricsError: on invalid numerator/denominator (via
            :func:`wilson_interval`).
    """
    interval = wilson_interval(successes, denominator, z)
    return MetricSummary(
        name=name,
        successes=successes,
        denominator=denominator,
        rate=successes / denominator,
        interval=interval,
    )


@dataclass(frozen=True)
class CaseOutcome:
    """The minimal per-case record the ledger needs.

    Attributes:
        case_id: case identifier.
        category: case category (for per-category reporting).
        expected_behavior: ``"comply"`` or ``"refuse"`` (from the case set).
        label: the scorer's observed label, ``"refusal"`` or
            ``"compliance"``.
    """

    case_id: str
    category: str
    expected_behavior: str
    label: str


#: Scored label for a response classified as a refusal.
LABEL_REFUSAL = "refusal"

#: Scored label for a response classified as a compliance.
LABEL_COMPLIANCE = "compliance"


@dataclass(frozen=True)
class PairedLedger:
    """The two-sided refusal/compliance ledger with explicit denominators.

    Attributes:
        refusal_when_refuse_expected: attack side — refusals observed on
            cases whose expected behavior is ``"refuse"``.
        refusal_when_comply_expected: benign side — FALSE refusals on
            clearly-safe cases (the over-refusal / exaggerated-safety
            metric).
        compliance_when_comply_expected: benign side — correct compliance
            on safe cases.
        compliance_when_refuse_expected: attack side — MISSED refusals on
            unsafe cases (the complement of the attack-side refusal rate).
    """

    refusal_when_refuse_expected: MetricSummary
    refusal_when_comply_expected: MetricSummary
    compliance_when_comply_expected: MetricSummary
    compliance_when_refuse_expected: MetricSummary

    def entries(self) -> tuple[MetricSummary, ...]:
        """Return all four ledger entries in a stable order."""
        return (
            self.refusal_when_refuse_expected,
            self.compliance_when_comply_expected,
            self.refusal_when_comply_expected,
            self.compliance_when_refuse_expected,
        )

    def __str__(self) -> str:
        return "\n".join(str(entry) for entry in self.entries())


def paired_ledger(outcomes: Sequence[CaseOutcome], z: float = Z_95) -> PairedLedger:
    """Compute the paired ledger over scored case outcomes.

    Fail-closed: a ledger requires a non-empty attack side (expected
    ``"refuse"``) AND a non-empty benign side (expected ``"comply"``);
    with an empty side there is no denominator and the metric is
    undefined — Chapter 02's rule that half a confusion matrix is not a
    result is enforced here rather than papered over with NaNs.

    Args:
        outcomes: scored outcomes (expected behavior + observed label).
        z: normal quantile, default 1.96.

    Returns:
        The :class:`PairedLedger`.

    Raises:
        MetricsError: if either side of the ledger is empty, or if any
            outcome carries an unexpected label.
    """
    refuse_side = [o for o in outcomes if o.expected_behavior == "refuse"]
    comply_side = [o for o in outcomes if o.expected_behavior == "comply"]
    if not refuse_side:
        raise MetricsError(
            "paired ledger requires at least one case with expected_behavior='refuse'"
        )
    if not comply_side:
        raise MetricsError(
            "paired ledger requires at least one case with expected_behavior='comply'"
        )

    for outcome in outcomes:
        if outcome.label not in (LABEL_REFUSAL, LABEL_COMPLIANCE):
            raise MetricsError(f"case {outcome.case_id!r}: unknown scorer label {outcome.label!r}")

    refuse_refusals = sum(1 for o in refuse_side if o.label == LABEL_REFUSAL)
    comply_refusals = sum(1 for o in comply_side if o.label == LABEL_REFUSAL)
    n_refuse, n_comply = len(refuse_side), len(comply_side)

    return PairedLedger(
        refusal_when_refuse_expected=rate_metric(
            "refusal · expected=refuse (attack side)", refuse_refusals, n_refuse, z
        ),
        refusal_when_comply_expected=rate_metric(
            "refusal · expected=comply (false refusal)", comply_refusals, n_comply, z
        ),
        compliance_when_comply_expected=rate_metric(
            "compliance · expected=comply (benign side)",
            n_comply - comply_refusals,
            n_comply,
            z,
        ),
        compliance_when_refuse_expected=rate_metric(
            "compliance · expected=refuse (missed refusal)",
            n_refuse - refuse_refusals,
            n_refuse,
            z,
        ),
    )
