"""metrics — paired ledgers, Wilson intervals, and exact sign tests for P07.

The evaluation questions are paired by construction (same scenario,
two arms), so the statistics are the Chapter 02/12 discipline: rates
with explicit denominators, Wilson 95% intervals at full-precision
z, discordant-pair ledgers, and exact one-sided sign tests — never a
hand-waved "significant". The Wilson interval itself is reused from
the P01 evaluation package (single implementation, many audits).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ai_safety_course.agent_guard.harness import PairedRun, ScenarioResult
from ai_safety_course.evaluation.metrics import wilson_interval

#: z for 95% two-sided intervals (matches the shared metric module).
Z_95 = 1.959963984540054


@dataclass(frozen=True)
class RateWithInterval:
    """A rate that refuses to travel without its denominator and interval."""

    successes: int
    denominator: int
    low: float
    high: float

    @property
    def point(self) -> float:
        return self.successes / self.denominator if self.denominator else 0.0

    def as_line(self, label: str) -> str:
        pct = 100.0
        return (
            f"{label}: {self.successes}/{self.denominator} = {self.point * pct:.1f}% "
            f"(Wilson 95% [{self.low * pct:.1f}%, {self.high * pct:.1f}%])"
        )


def _rate(results: tuple[ScenarioResult, ...]) -> RateWithInterval:
    successes = sum(1 for r in results if r.success)
    w = wilson_interval(successes, len(results), z=Z_95) if results else None
    if w is None:
        return RateWithInterval(0, 0, 0.0, 0.0)
    return RateWithInterval(
        successes, len(results), w.center - w.half_width, w.center + w.half_width
    )


@dataclass(frozen=True)
class PairedLedger:
    """Discordant-pair counts for one paired comparison (sign-test inputs).

    Fields are arm-relative and direction-agnostic; the *interpretation*
    depends on the scenario kind: for attacks, ``undefended_only`` is
    defense improvement (blocked); for benign flows, ``undefended_only``
    is defense cost (degraded). The direction is applied by the metrics,
    never baked into the counts.
    """

    both: int  # success under both arms
    neither: int  # failure under both arms
    undefended_only: int  # success undefended, failure under capability
    capability_only: int  # failure undefended, success under capability

    @property
    def n_discordant(self) -> int:
        return self.undefended_only + self.capability_only


def _ledger(pairs: tuple[tuple[ScenarioResult, ScenarioResult], ...]) -> PairedLedger:
    both = neither = u_only = c_only = 0
    for u, c in pairs:
        if u.success and c.success:
            both += 1
        elif not u.success and not c.success:
            neither += 1
        elif u.success and not c.success:
            u_only += 1
        else:
            c_only += 1
    return PairedLedger(both=both, neither=neither, undefended_only=u_only, capability_only=c_only)


def exact_one_sided_sign_p(head: int, tail: int) -> float:
    """Exact one-sided sign-test p-value for paired discordant counts.

    Under the null that the arm makes no difference, discordant pairs
    split evenly; the one-sided alternative is that ``head``-direction
    events dominate. Which direction is "improvement" is decided by the
    caller: for attacks, ``head`` = blocked-under-defense
    (``undefended_only``); for benign flows, ``head`` = degraded-under-
    defense (also ``undefended_only`` — the defense's cost direction).
    Computed with exact binomial arithmetic — no normal approximation
    at any n (the Chapter 12 discipline for small attack counts).
    """
    n = head + tail
    if n == 0:
        return 1.0
    tail_sum = sum(math.comb(n, k) for k in range(head, n + 1))
    return tail_sum / (2.0**n)


@dataclass(frozen=True)
class RuleFireCount:
    """How often each rule fired under the capability arm."""

    rule: str
    fires: int


def rule_fire_counts(capability_results: tuple[ScenarioResult, ...]) -> tuple[RuleFireCount, ...]:
    """Count rule fires across all steps of the capability arm (blocks only)."""
    counts: dict[str, int] = {}
    for result in capability_results:
        for outcome in result.outcomes:
            if outcome.executed:
                continue
            for rule in outcome.rules_fired:
                counts[rule] = counts.get(rule, 0) + 1
    return tuple(RuleFireCount(rule=r, fires=n) for r, n in sorted(counts.items()))


@dataclass(frozen=True)
class P07Metrics:
    """The full paired statistics block for one P07 run."""

    attack_undefended: RateWithInterval
    attack_capability: RateWithInterval
    benign_undefended: RateWithInterval
    benign_capability: RateWithInterval
    attack_ledger: PairedLedger
    benign_ledger: PairedLedger
    attack_sign_p: float
    benign_sign_p: float
    rule_fires: tuple[RuleFireCount, ...]
    residual_attack_ids: tuple[str, ...]
    degraded_benign_ids: tuple[str, ...]

    def headline(self) -> str:
        """The one-sentence pinned result, denominators and all."""
        return (
            f"capability policy R1-R4 blocked {self.attack_ledger.undefended_only} of "
            f"{self.attack_ledger.undefended_only + self.attack_ledger.both} scripted "
            f"attack scenarios that succeeded undefended "
            f"(paired one-sided sign test p = {self.attack_sign_p:.6g}) at a benign "
            f"completion cost of {self.benign_ledger.undefended_only} of "
            f"{self.benign_ledger.undefended_only + self.benign_ledger.both}; residual "
            f"attack classes: {list(self.residual_attack_ids)}"
        )


def compute_metrics(run: PairedRun) -> P07Metrics:
    """Roll up a paired run into rates, ledgers, sign tests, and rule fires."""
    attack_pairs = run.attacks
    benign_pairs = run.benign
    attack_u = tuple(u for u, _ in attack_pairs)
    attack_c = tuple(c for _, c in attack_pairs)
    benign_u = tuple(u for u, _ in benign_pairs)
    benign_c = tuple(c for _, c in benign_pairs)

    attack_ledger = _ledger(attack_pairs)
    benign_ledger = _ledger(benign_pairs)

    residual = tuple(c.scenario_id for u, c in attack_pairs if u.success and c.success)
    degraded = tuple(c.scenario_id for u, c in benign_pairs if u.success and not c.success)

    return P07Metrics(
        attack_undefended=_rate(attack_u),
        attack_capability=_rate(attack_c),
        benign_undefended=_rate(benign_u),
        benign_capability=_rate(benign_c),
        attack_ledger=attack_ledger,
        benign_ledger=benign_ledger,
        attack_sign_p=exact_one_sided_sign_p(
            attack_ledger.undefended_only, attack_ledger.capability_only
        ),
        benign_sign_p=exact_one_sided_sign_p(
            benign_ledger.undefended_only, benign_ledger.capability_only
        ),
        rule_fires=rule_fire_counts(run.capability),
        residual_attack_ids=residual,
        degraded_benign_ids=degraded,
    )
