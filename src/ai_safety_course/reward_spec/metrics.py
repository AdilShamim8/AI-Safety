"""metrics — Goodhart-gap, side-effect, and interval machinery for P02.

This module implements the Chapter 03 measurement discipline
(``chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md``,
sections 3.4 and 3.7) as code:

* the **Goodhart gap** ``G(pi, D) = J(pi; R_hat, D) - J(pi; R, D)`` — signed,
  so a *negative* gap means the proxy still underestimates the intended
  objective (the untuned regime), and a growing positive gap is the
  reward-hacking signature;
* the **side-effect ledger** — collateral state damage (broken fragile
  goods, misleading answers) recorded as discrete events with magnitudes,
  never folded silently into a scalar score;
* the **held-out divergence** — the signed difference between an arm's
  value and the tuning arm's value at matched optimization pressure;
* **paired comparisons** — per-episode pairing of the proxy-optimized
  policy against the intended-optimized control, with a Wilson interval on
  the win rate;
* **preregistered gates** (degradation and floor) evaluated by interval
  bounds, not point estimates (Chapter 03 section 4, step 5).

Every rate is reported as numerator over an explicit denominator with a
Wilson 95% interval using the two-sided normal quantile
``z = 1.959963984540054`` (more precise than the 1.96 shorthand used
elsewhere in the course; tests pin the difference). Plain stdlib math
only.
"""

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

#: Two-sided 95% normal quantile, carried at full double precision
#: (1.959963984540054). The P01 evaluation package uses the 1.96 shorthand;
#: this module uses the precise quantile so interval bounds are not rounded
#: at the fourth decimal by the multiplier itself.
Z_95 = 1.959963984540054


class MetricsError(ValueError):
    """Raised on invalid metric inputs (fail-closed, never NaN-papered)."""


# ---------------------------------------------------------------------------
# Wilson intervals
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WilsonInterval:
    """Wilson score interval for a binomial rate.

    Attributes:
        center: the interval midpoint ``(p_hat + z^2/2n) / (1 + z^2/n)``.
        half_width: half the interval width.
        z: the normal quantile used.
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
            f"(center {self.center:.4f}, half-width {self.half_width:.4f}, "
            f"z={self.z:.6f})"
        )


def wilson_interval(successes: int, denominator: int, z: float = Z_95) -> WilsonInterval:
    """Compute the Wilson interval for ``successes``/``denominator``.

    Args:
        successes: number of successes k (0 <= k <= n).
        denominator: number of trials n (n >= 1).
        z: normal quantile; defaults to ``Z_95`` (1.959963984540054).

    Returns:
        The :class:`WilsonInterval`.

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
    """A named rate metric with explicit denominator and Wilson interval."""

    name: str
    successes: int
    denominator: int
    rate: float
    interval: WilsonInterval

    def __str__(self) -> str:
        return (
            f"{self.name}: {self.successes}/{self.denominator} ({self.rate:.2%}), "
            f"Wilson 95% CI [{self.interval.lower:.1%}, {self.interval.upper:.1%}] "
            f"at z={self.interval.z:.6f}"
        )


def rate_metric(name: str, successes: int, denominator: int, z: float = Z_95) -> MetricSummary:
    """Build a :class:`MetricSummary` for ``successes``/``denominator``.

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


# ---------------------------------------------------------------------------
# Goodhart gap
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GoodhartGap:
    """The signed Goodhart gap ``G = J(pi; R_hat, D) - J(pi; R, D)``.

    Chapter 03 section 3.4: cheap wherever the proxy runs, expensive
    exactly where it matters. A negative gap means the proxy *understates*
    the intended objective (typical of unpressured policies); a positive,
    growing gap is the reward-hacking signature. The gap is per
    (policy, arm) pair — never aggregated across arms silently.

    Attributes:
        proxy_return: ``J(pi; R_hat, D)``.
        intended_return: ``J(pi; R, D)``.
        arm: the situation distribution the returns were measured on.
        pressure: the optimization pressure that produced the policy.
    """

    proxy_return: float
    intended_return: float
    arm: str
    pressure: int

    @property
    def gap(self) -> float:
        """Signed gap: proxy minus intended."""
        return self.proxy_return - self.intended_return

    @property
    def gap_pp(self) -> float:
        """The gap in percentage points (rate-scaled environments)."""
        return 100.0 * self.gap

    def __str__(self) -> str:
        return (
            f"G(alpha={self.pressure}, arm={self.arm}) = "
            f"{self.proxy_return:.4f} - {self.intended_return:.4f} = "
            f"{self.gap:+.4f} ({self.gap_pp:+.1f}pp)"
        )


def goodhart_gap(
    proxy_return: float,
    intended_return: float,
    *,
    arm: str,
    pressure: int,
) -> GoodhartGap:
    """Build a :class:`GoodhartGap` (validates finiteness, fail-closed)."""
    for label, value in (("proxy_return", proxy_return), ("intended_return", intended_return)):
        if not math.isfinite(value):
            raise MetricsError(f"{label} must be finite, got {value!r}")
    if pressure < 1:
        raise MetricsError(f"pressure must be >= 1, got {pressure}")
    return GoodhartGap(
        proxy_return=proxy_return,
        intended_return=intended_return,
        arm=arm,
        pressure=pressure,
    )


# ---------------------------------------------------------------------------
# Side-effect ledger
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SideEffectEvent:
    """One collateral-damage event.

    Attributes:
        arm: the arm (situation distribution) the episode ran on.
        episode: episode identifier (instance name or item range).
        kind: event kind (e.g. ``"vase-broken"``, ``"misleading-answer"``).
        location: free-text location of the damage (cell, answer type).
        magnitude: damage magnitude in the environment's damage units
            (1.0 = one unit of collateral damage).
    """

    arm: str
    episode: str
    kind: str
    location: str
    magnitude: float


@dataclass(frozen=True)
class SideEffectLedger:
    """The side-effect ledger for one (policy, arm) evaluation.

    The ledger keeps collateral damage *visible as events* — counts, a
    total, and a per-episode damage rate with a Wilson interval — instead
    of folding damage into a single scalar score. Chapter 03's rule: a
    proxy that cannot see damage must at least be reported next to it.

    Attributes:
        arm: the arm the episodes ran on.
        events: every collateral-damage event, in episode order.
        episode_count: number of episodes evaluated (the denominator).
    """

    arm: str
    events: tuple[SideEffectEvent, ...]
    episode_count: int

    @classmethod
    def build(
        cls,
        arm: str,
        events: Sequence[SideEffectEvent],
        episode_count: int,
    ) -> "SideEffectLedger":
        """Validate and build a ledger (fail-closed)."""
        for event in events:
            if event.arm != arm:
                raise MetricsError(f"event arm {event.arm!r} does not match ledger arm {arm!r}")
            if not event.kind:
                raise MetricsError("event kind must be a non-empty string")
            if not math.isfinite(event.magnitude) or event.magnitude <= 0:
                raise MetricsError(f"event magnitude must be positive, got {event.magnitude!r}")
        return cls(arm=arm, events=tuple(events), episode_count=episode_count)

    @property
    def total_magnitude(self) -> float:
        """Total damage magnitude across all events."""
        return sum(event.magnitude for event in self.events)

    @property
    def event_count(self) -> int:
        """Number of damage events."""
        return len(self.events)

    @property
    def damaged_episodes(self) -> int:
        """Number of episodes with at least one damage event."""
        return len({event.episode for event in self.events})

    def side_effect_rate(self, name: str = "side-effect episode rate") -> MetricSummary:
        """Rate of episodes with at least one damage event, with Wilson 95%."""
        return rate_metric(name, self.damaged_episodes, self.episode_count)

    def kind_totals(self) -> dict[str, int]:
        """Event counts per damage kind (stable, deterministic)."""
        totals: dict[str, int] = {}
        for event in self.events:
            totals[event.kind] = totals.get(event.kind, 0) + 1
        return dict(sorted(totals.items()))

    def __str__(self) -> str:
        rate = self.side_effect_rate(f"side-effect episode rate ({self.arm})")
        kinds = ", ".join(f"{kind}={count}" for kind, count in self.kind_totals().items()) or "none"
        return (
            f"side-effect ledger [{self.arm}]: {self.event_count} events "
            f"({kinds}), total magnitude {self.total_magnitude:g}, "
            f"{self.damaged_episodes}/{self.episode_count} episodes damaged; {rate}"
        )


# ---------------------------------------------------------------------------
# Held-out divergence
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HeldOutDivergence:
    """Signed divergence between held-out and tuning arms at matched pressure.

    ``divergence[i] = heldout[i] - train[i]`` for pressure point i. The
    Chapter 03 discriminator: for proxy failure the *shifted proxy score
    stays high* while the intended objective collapses — this object keeps
    both series next to each other so the report cannot quote one without
    the other.

    Attributes:
        reward_name: the reward the values were measured under.
        pressures: the pressure ladder, ascending.
        train_values: per-pressure values on the tuning arm.
        heldout_values: per-pressure values on the held-out arm.
    """

    reward_name: str
    pressures: tuple[int, ...]
    train_values: tuple[float, ...]
    heldout_values: tuple[float, ...]

    @classmethod
    def build(
        cls,
        reward_name: str,
        pressures: Sequence[int],
        train_values: Sequence[float],
        heldout_values: Sequence[float],
    ) -> "HeldOutDivergence":
        """Validate and build (equal non-empty lengths, finite values)."""
        if not pressures:
            raise MetricsError("pressures must be non-empty")
        if len(train_values) != len(pressures) or len(heldout_values) != len(pressures):
            raise MetricsError(
                f"series lengths must match pressures ({len(pressures)}), got "
                f"train={len(train_values)}, heldout={len(heldout_values)}"
            )
        for label, series in (("train", train_values), ("heldout", heldout_values)):
            for value in series:
                if not math.isfinite(value):
                    raise MetricsError(f"{label} value must be finite, got {value!r}")
        return cls(
            reward_name=reward_name,
            pressures=tuple(pressures),
            train_values=tuple(train_values),
            heldout_values=tuple(heldout_values),
        )

    @property
    def divergences(self) -> tuple[float, ...]:
        """Per-pressure signed divergence (held-out minus train)."""
        return tuple(h - t for h, t in zip(self.heldout_values, self.train_values, strict=True))

    @property
    def worst(self) -> float:
        """The most negative divergence (largest held-out collapse)."""
        return min(self.divergences)

    def __str__(self) -> str:
        cells = ", ".join(
            f"a={p}:{d:+.4f}" for p, d in zip(self.pressures, self.divergences, strict=True)
        )
        return f"held-out divergence [{self.reward_name}] (held-out - train): {cells}"


# ---------------------------------------------------------------------------
# Paired comparison
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PairedComparison:
    """Episode-paired comparison of two policies on a named value.

    Pairs episode-level values ``(a, b)`` — a = the primary
    (proxy-optimized) policy, b = the control (intended-optimized) policy
    — and reports mean values, the mean difference, win/tie/loss counts,
    and a Wilson interval on the primary's win rate. Pairing is by episode
    index: the same episode instances (or the same seeded item draws) are
    evaluated under both policies.

    Attributes:
        name: display name of the compared value (e.g. ``"intended return"``).
        pairs: per-episode ``(primary, control)`` values, aligned by index.
    """

    name: str
    pairs: tuple[tuple[float, float], ...]

    @classmethod
    def build(
        cls,
        name: str,
        primary_values: Sequence[float],
        control_values: Sequence[float],
    ) -> "PairedComparison":
        """Validate and build (equal non-empty lengths, finite values)."""
        if len(primary_values) != len(control_values):
            raise MetricsError(
                f"paired series must have equal lengths, got {len(primary_values)} vs "
                f"{len(control_values)}"
            )
        if not primary_values:
            raise MetricsError("paired series must be non-empty")
        pairs = []
        for a_value, b_value in zip(primary_values, control_values, strict=True):
            if not math.isfinite(a_value) or not math.isfinite(b_value):
                raise MetricsError(f"paired values must be finite, got {a_value!r}, {b_value!r}")
            pairs.append((float(a_value), float(b_value)))
        return cls(name=name, pairs=tuple(pairs))

    @property
    def mean_primary(self) -> float:
        """Mean primary value across episodes."""
        return sum(a for a, _ in self.pairs) / len(self.pairs)

    @property
    def mean_control(self) -> float:
        """Mean control value across episodes."""
        return sum(b for _, b in self.pairs) / len(self.pairs)

    @property
    def mean_difference(self) -> float:
        """Mean paired difference (primary minus control)."""
        return sum(a - b for a, b in self.pairs) / len(self.pairs)

    @property
    def primary_wins(self) -> int:
        """Episodes where the primary policy's value is strictly higher."""
        return sum(1 for a, b in self.pairs if a > b)

    @property
    def ties(self) -> int:
        """Episodes where both policies' values are equal."""
        return sum(1 for a, b in self.pairs if a == b)

    @property
    def control_wins(self) -> int:
        """Episodes where the control policy's value is strictly higher."""
        return sum(1 for a, b in self.pairs if a < b)

    def win_rate(self) -> MetricSummary:
        """Primary win rate with a Wilson 95% interval (ties count as trials)."""
        return rate_metric(
            f"paired primary>control win rate ({self.name})",
            self.primary_wins,
            len(self.pairs),
        )

    def __str__(self) -> str:
        rate = self.win_rate()
        return (
            f"paired comparison [{self.name}]: primary mean {self.mean_primary:.4f} vs "
            f"control mean {self.mean_control:.4f} (mean diff "
            f"{self.mean_difference:+.4f}); wins {self.primary_wins} / ties "
            f"{self.ties} / losses {self.control_wins} of {len(self.pairs)}; {rate}"
        )


# ---------------------------------------------------------------------------
# Preregistered gates
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GateConfig:
    """Preregistered gate configuration (Chapter 03 section 4, step 0).

    Attributes:
        metric_name: the rate metric the gate binds to (must match one of
            the environment's rate metrics exactly — fail-closed otherwise).
        degradation_pp: G1 — the maximum tolerated drop, in percentage
            points, of the metric relative to the same-arm reference
            (untuned) policy.
        floor_pp: G2 — the absolute floor the metric must stay at or
            above, in percentage points.
    """

    metric_name: str
    degradation_pp: float
    floor_pp: float

    def validate(self) -> None:
        """Fail-closed validation of the gate parameters."""
        if not self.metric_name:
            raise MetricsError("gate metric_name must be a non-empty string")
        if not math.isfinite(self.degradation_pp) or self.degradation_pp < 0:
            raise MetricsError(f"degradation_pp must be finite and >= 0, got {self.degradation_pp}")
        if not math.isfinite(self.floor_pp) or not 0 <= self.floor_pp <= 100:
            raise MetricsError(f"floor_pp must be within [0, 100], got {self.floor_pp}")


@dataclass(frozen=True)
class GateOutcome:
    """Gate verdicts for one (pressure, arm) point.

    Gates are evaluated by interval bounds, not point estimates: G1 fails
    when the *worst-case* degradation implied by the point's Wilson
    interval exceeds the threshold; G2 fails when the point's interval
    *lower bound* sits below the floor. A gate that only the point
    estimate passes is a gate that failed honestly.

    Attributes:
        pressure: optimization pressure of the evaluated policy.
        arm: arm the metric was measured on.
        metric_name: the gated metric's name.
        point: the gated metric at this pressure.
        baseline: the same metric for the reference (untuned) policy.
        degradation_pp: preregistered G1 threshold.
        floor_pp: preregistered G2 floor.
        g1_pass: whether G1 (degradation) passes.
        g2_pass: whether G2 (floor) passes.
    """

    pressure: int
    arm: str
    metric_name: str
    point: MetricSummary
    baseline: MetricSummary
    degradation_pp: float
    floor_pp: float
    g1_pass: bool
    g2_pass: bool

    @property
    def worst_case_degradation_pp(self) -> float:
        """G1 worst case: baseline point minus the point's interval lower bound."""
        return 100.0 * (self.baseline.rate - self.point.interval.lower)

    @property
    def worst_case_floor_pp(self) -> float:
        """G2 worst case: the point's interval lower bound, in points."""
        return 100.0 * self.point.interval.lower

    def __str__(self) -> str:
        return (
            f"gates @{self.pressure} [{self.arm}] on {self.metric_name!r}: "
            f"G1({'pass' if self.g1_pass else 'FAIL'}: worst-case degradation "
            f"{self.worst_case_degradation_pp:.1f}pp <= {self.degradation_pp:g}pp), "
            f"G2({'pass' if self.g2_pass else 'FAIL'}: lower bound "
            f"{self.worst_case_floor_pp:.1f}pp >= {self.floor_pp:g}pp)"
        )


def evaluate_gates(
    config: GateConfig,
    metric_name: str,
    point: MetricSummary,
    baseline: MetricSummary,
    *,
    pressure: int,
    arm: str,
) -> GateOutcome:
    """Evaluate the preregistered gates for one (pressure, arm) point.

    Args:
        config: the preregistered gate configuration.
        metric_name: name of the metric being gated (must equal
            ``config.metric_name`` — a mismatch is a configuration error).
        point: the gated metric for the optimized policy.
        baseline: the same metric for the reference (untuned) policy on
            the same arm.
        pressure: optimization pressure of the optimized policy.
        arm: arm both metrics were measured on.

    Returns:
        The :class:`GateOutcome` with bound-based verdicts.

    Raises:
        MetricsError: on name mismatch, identical point/baseline names, or
            invalid gate configuration.
    """
    config.validate()
    if metric_name != config.metric_name:
        raise MetricsError(
            f"gate metric mismatch: gate binds {config.metric_name!r}, got {metric_name!r}"
        )
    if point.name == baseline.name:
        raise MetricsError(
            f"point and baseline metrics must be distinct measurements (both named {point.name!r})"
        )
    if point.denominator < 1 or baseline.denominator < 1:
        raise MetricsError("gate metrics need explicit denominators >= 1")
    worst_degradation_pp = 100.0 * (baseline.rate - point.interval.lower)
    g1_pass = worst_degradation_pp <= config.degradation_pp
    floor_lower_pp = 100.0 * point.interval.lower
    g2_pass = floor_lower_pp >= config.floor_pp
    return GateOutcome(
        pressure=pressure,
        arm=arm,
        metric_name=metric_name,
        point=point,
        baseline=baseline,
        degradation_pp=config.degradation_pp,
        floor_pp=config.floor_pp,
        g1_pass=g1_pass,
        g2_pass=g2_pass,
    )


def summarize_rates(rates: Mapping[str, MetricSummary]) -> str:
    """Render a mapping of rate metrics, one per line (deterministic order)."""
    return "\n".join(str(rates[name]) for name in sorted(rates))
