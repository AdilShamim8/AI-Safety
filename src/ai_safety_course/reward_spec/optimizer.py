"""optimizer — deterministic optimization-pressure ladders over policies.

The P02 pressure knob, implemented three ways (all regimes deterministic
and CPU-only):

* :class:`LocalSearchOptimizer` — generic hill-climbing over the
  environment's policy space via ``policy_neighbors``. *Pressure* is the
  number of accepted improvement steps: alpha=0 is the untuned starting
  policy, alpha=k is the policy after k strictly-improving moves toward
  the chosen reward. Works on any :class:`~ai_safety_course.reward_spec.
  environments.TaskEnvironment`. If the search reaches a local optimum
  before the pressure is exhausted, it stops and *records that honestly*
  (``stopped_early=True``) — a saturated ladder point is a fact about the
  policy space, not an error.

* :class:`BudgetedSearchOptimizer` — local search with seeded restarts
  under a total *evaluation budget*: pressure alpha = the number of
  policy evaluations spent (the deployment-realistic "compute spent on
  optimizing" reading of pressure). Each restart samples a fresh start
  from the environment's reference sampler, climbs first-improvement
  until saturated, then restarts; the best policy ever seen is returned.
  This is the regime that finds the warehouse's vase-breaking routes:
  modest budgets clean the reachable dirt, larger budgets keep trading
  vases for vault dirt because the proxy cannot price the difference.

* :class:`BonWidthOptimizer` — the deployed best-of-n regime for the
  judge environment: pressure maps directly onto the selection width n
  (``JudgePolicy(base_mixture, width=n, selector=reward)``). This is the
  Chapter 03 section 4 story exactly: no search at all, just wider
  selection under the installed judge (or under the graded rubric, for
  the oracle control arm).

All optimizers return an :class:`OptimizationResult` carrying the final
policy, its fingerprint, the achieved value ``J(pi; reward, arm)``, the
trace of accepted steps, and the honest stop reason. Ties between
equally-improving neighbors are broken by first-encountered order in the
environment's fixed neighbor enumeration — never by wall-clock, never by
set iteration order.
"""

import random
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from ai_safety_course.reward_spec.environments import (
    REWARD_INTENDED,
    REWARD_PROXY,
    JudgeScoredAnswers,
    TaskEnvironment,
)


class OptimizerError(ValueError):
    """Raised on invalid optimizer configuration (fail-closed)."""


#: Starting points for local search.
START_KINDS = ("reference", "random")


@dataclass(frozen=True)
class TraceStep:
    """One accepted improvement step (or the alpha=0 start row).

    Attributes:
        pressure: the pressure level *after* this step (0 for the start).
        fingerprint: the policy's stable identifier after the step.
        value: ``J(pi; reward, arm)`` after the step.
        accepted: whether this row records an accepted move (False only
            for the alpha=0 start row).
    """

    pressure: int
    fingerprint: str
    value: float
    accepted: bool = True

    def __str__(self) -> str:
        marker = "start" if not self.accepted else "step"
        return f"alpha={self.pressure} [{marker}] {self.fingerprint}: {self.value:.4f}"


@dataclass(frozen=True)
class OptimizationResult:
    """The outcome of one (pressure, arm, reward) optimization run.

    Attributes:
        policy: the final policy object (opaque; environment-specific).
        fingerprint: stable identifier of the final policy.
        reward_name: the reward that was optimized.
        arm: the arm the optimization was measured on.
        requested_pressure: the pressure the caller asked for.
        achieved_pressure: the pressure actually reached (equal unless
            the search saturated at a local optimum early).
        value: ``J(pi; reward, arm)`` at the achieved pressure.
        trace: one row per accepted step, starting with the alpha=0 row.
        stopped_early: whether the search saturated before the requested
            pressure (recorded honestly, never silently rounded up).
        optimizer_kind: which regime produced this result.
    """

    policy: Any
    fingerprint: str
    reward_name: str
    arm: str
    requested_pressure: int
    achieved_pressure: int
    value: float
    trace: tuple[TraceStep, ...]
    stopped_early: bool
    optimizer_kind: str

    @property
    def saturated(self) -> bool:
        """Whether further pressure would change nothing (local optimum)."""
        return self.stopped_early

    def trace_lines(self) -> tuple[str, ...]:
        """The trace, one line per step (for reports and debugging)."""
        return tuple(str(step) for step in self.trace)


class PressureOptimizer(Protocol):
    """What both optimizer regimes expose to the runner."""

    kind: str

    def optimize(
        self,
        env: TaskEnvironment,
        *,
        reward_name: str,
        arm: str,
        pressure: int,
        seed: int,
    ) -> OptimizationResult: ...


def _check_reward_name(reward_name: str) -> None:
    if reward_name not in (REWARD_PROXY, REWARD_INTENDED):
        raise OptimizerError(
            f"reward_name must be {REWARD_PROXY!r} or {REWARD_INTENDED!r}, got {reward_name!r}"
        )


def _check_pressure(pressure: int) -> None:
    if not isinstance(pressure, int) or isinstance(pressure, bool) or pressure < 0:
        raise OptimizerError(f"pressure must be an int >= 0, got {pressure!r}")


@dataclass(frozen=True)
class LocalSearchOptimizer:
    """Hill-climbing under an explicit accepted-step budget.

    Args:
        start: ``"reference"`` starts from the environment's untuned
            reference policy (the deployment baseline being optimized);
            ``"random"`` starts from a seeded uniform sample of the
            unconstrained policy space (the search-from-scratch regime).
        max_neighbors_per_step: safety valve on per-step neighbor
            evaluation count (fail-closed if an environment offers more
            neighbors than the budget allows — the warehouse's 200
            neighbors at the default budget are fine).
    """

    start: str = "reference"
    max_neighbors_per_step: int = 512

    kind = "local-search"

    def __post_init__(self) -> None:
        if self.start not in START_KINDS:
            raise OptimizerError(f"start must be one of {START_KINDS}, got {self.start!r}")
        if not isinstance(self.max_neighbors_per_step, int) or self.max_neighbors_per_step < 1:
            raise OptimizerError(
                f"max_neighbors_per_step must be an int >= 1, got {self.max_neighbors_per_step!r}"
            )

    def optimize(
        self,
        env: TaskEnvironment,
        *,
        reward_name: str,
        arm: str,
        pressure: int,
        seed: int,
    ) -> OptimizationResult:
        """Climb for exactly ``pressure`` accepted steps (or to a local optimum).

        Deterministic: the RNG is seeded per run, neighbors are evaluated
        in the environment's fixed order, and ties go to the first
        strictly-better neighbor found.
        """
        _check_reward_name(reward_name)
        _check_pressure(pressure)
        rng = random.Random(seed)
        if self.start == "reference":
            policy = env.sample_reference(rng, arm)
        else:
            policy = env.sample_policy(rng)
        value = env.evaluate(policy, reward_name, arm)
        trace: list[TraceStep] = [
            TraceStep(
                pressure=0, fingerprint=env.policy_fingerprint(policy), value=value, accepted=False
            )
        ]
        accepted_steps = 0
        for _ in range(pressure):
            neighbors = env.policy_neighbors(policy)
            if len(neighbors) > self.max_neighbors_per_step:
                raise OptimizerError(
                    f"environment {env.name!r} offered {len(neighbors)} neighbors; "
                    f"budget is {self.max_neighbors_per_step} (raise the budget "
                    "or shrink the policy space)"
                )
            best_policy = None
            best_value = value
            for neighbor in neighbors:
                candidate = env.evaluate(neighbor, reward_name, arm)
                if candidate > best_value:
                    best_policy, best_value = neighbor, candidate
            if best_policy is None:
                break  # local optimum: pressure requested, saturation found
            policy = best_policy
            value = best_value
            accepted_steps += 1
            trace.append(
                TraceStep(
                    pressure=accepted_steps, fingerprint=env.policy_fingerprint(policy), value=value
                )
            )
        return OptimizationResult(
            policy=policy,
            fingerprint=env.policy_fingerprint(policy),
            reward_name=reward_name,
            arm=arm,
            requested_pressure=pressure,
            achieved_pressure=accepted_steps,
            value=value,
            trace=tuple(trace),
            stopped_early=accepted_steps < pressure,
            optimizer_kind=self.kind,
        )


@dataclass(frozen=True)
class BudgetedSearchOptimizer:
    """Restarted first-improvement search under a total evaluation budget.

    *Pressure* is the number of policy evaluations spent — the
    deployment-realistic reading ("how much compute went into
    optimizing this objective"). The loop: sample a start from the
    environment's reference sampler (1 evaluation), climb
    first-improvement through the fixed neighbor order until saturated,
    then restart with the next seeded sample; keep the best policy ever
    evaluated. The best-so-far after each restart forms the trace, so the
    report shows exactly when a better (possibly damage-route) policy was
    first found.

    Args:
        start: ``"reference"`` (the environment's naive/untuned sampler —
            the realistic candidate pool) or ``"random"`` (uniform over
            the unconstrained policy space).

    The budget is spent exactly (``achieved_pressure == requested`` for
    every non-zero pressure) — the final partial neighbor scan is
    truncated, never overspent.
    """

    start: str = "reference"

    kind = "budgeted-search"

    def __post_init__(self) -> None:
        if self.start not in START_KINDS:
            raise OptimizerError(f"start must be one of {START_KINDS}, got {self.start!r}")

    def _start_policy(self, env: TaskEnvironment, rng: random.Random, arm: str) -> Any:
        if self.start == "reference":
            return env.sample_reference(rng, arm)
        return env.sample_policy(rng)

    def optimize(
        self,
        env: TaskEnvironment,
        *,
        reward_name: str,
        arm: str,
        pressure: int,
        seed: int,
    ) -> OptimizationResult:
        """Spend exactly ``pressure`` evaluations; return the best policy seen."""
        _check_reward_name(reward_name)
        _check_pressure(pressure)
        if pressure < 1:
            raise OptimizerError(
                "budgeted-search needs pressure >= 1 (zero pressure has no "
                "candidate to evaluate; the untuned row comes from the "
                "environment's reference policy, not from the optimizer)"
            )
        rng = random.Random(seed)
        evals = 0
        best: Any = None
        best_value = float("-inf")
        best_fingerprint = ""
        trace: list[TraceStep] = []
        restarts = 0
        while evals < pressure:
            policy = self._start_policy(env, rng, arm)
            evals += 1
            value = env.evaluate(policy, reward_name, arm)
            if value > best_value:
                best, best_value = policy, value
                best_fingerprint = env.policy_fingerprint(policy)
            restarts += 1
            while evals < pressure:
                neighbors = env.policy_neighbors(policy)
                if not neighbors:
                    break
                moved = False
                for neighbor in neighbors:
                    if evals >= pressure:
                        break  # budget exhausted mid-scan: stop, never overspend
                    evals += 1
                    candidate = env.evaluate(neighbor, reward_name, arm)
                    if candidate > value:
                        policy, value = neighbor, candidate
                        moved = True
                        break  # first-improvement: move before finishing the scan
                if not moved:
                    break  # saturated from this start; restart
                if value > best_value:
                    best, best_value = policy, value
                    best_fingerprint = env.policy_fingerprint(policy)
            trace.append(TraceStep(pressure=evals, fingerprint=best_fingerprint, value=best_value))
        return OptimizationResult(
            policy=best,
            fingerprint=best_fingerprint,
            reward_name=reward_name,
            arm=arm,
            requested_pressure=pressure,
            achieved_pressure=evals,
            value=best_value,
            trace=tuple(trace),
            stopped_early=evals < pressure,
            optimizer_kind=self.kind,
        )


@dataclass(frozen=True)
class BonWidthOptimizer:
    """Best-of-n selection width as the pressure knob (judge environment).

    Pressure alpha maps to selection width n = max(1, alpha): alpha=0 and
    alpha=1 are both the untuned width-1 system (no selection), and each
    further unit of pressure widens the candidate pool the selector ranks.
    The selector objective is the optimized reward — the installed judge
    for ``proxy`` (deployment realism), the graded rubric for ``intended``
    (the oracle control of Chapter 03 section 4).
    """

    kind = "bon-width"

    def optimize(
        self,
        env: TaskEnvironment,
        *,
        reward_name: str,
        arm: str,
        pressure: int,
        seed: int,  # noqa: ARG002 — width is deterministic; seed unused by contract
    ) -> OptimizationResult:
        """Return the width-n BoN policy (closed form, no search)."""
        _check_reward_name(reward_name)
        _check_pressure(pressure)
        if not isinstance(env, JudgeScoredAnswers):
            raise OptimizerError(
                f"bon-width optimizer requires judge-scored-answers, got {env.name!r}"
            )
        width = max(1, pressure)
        policy = env.bon_width_policy(width, reward_name)
        value = env.evaluate(policy, reward_name, arm)
        start = env.bon_width_policy(1, reward_name)
        start_value = env.evaluate(start, reward_name, arm)
        trace = (
            TraceStep(
                pressure=0,
                fingerprint=env.policy_fingerprint(start),
                value=start_value,
                accepted=False,
            ),
            TraceStep(pressure=width, fingerprint=env.policy_fingerprint(policy), value=value),
        )
        return OptimizationResult(
            policy=policy,
            fingerprint=env.policy_fingerprint(policy),
            reward_name=reward_name,
            arm=arm,
            requested_pressure=pressure,
            achieved_pressure=width,
            value=value,
            trace=trace,
            stopped_early=False,
            optimizer_kind=self.kind,
        )


def optimizer_from_config(config: Any) -> PressureOptimizer:
    """Build an optimizer from a config block (fail-closed on unknowns)."""
    if isinstance(config, str):
        kind, params = config, {}
    elif isinstance(config, dict):
        kind = config.get("kind")
        params = {k: v for k, v in config.items() if k != "kind"}
    else:
        raise OptimizerError(f"optimizer config must be a string or mapping, got {config!r}")
    if kind == "local-search":
        unknown = set(params) - {"start", "max_neighbors_per_step"}
        if unknown:
            raise OptimizerError(
                f"unknown local-search params: {sorted(unknown)}; "
                f"supported: start, max_neighbors_per_step"
            )
        return LocalSearchOptimizer(
            start=params.get("start", "reference"),
            max_neighbors_per_step=params.get("max_neighbors_per_step", 512),
        )
    if kind == "budgeted-search":
        unknown = set(params) - {"start"}
        if unknown:
            raise OptimizerError(
                f"unknown budgeted-search params: {sorted(unknown)}; supported: start"
            )
        return BudgetedSearchOptimizer(start=params.get("start", "reference"))
    if kind == "bon-width":
        if params:
            raise OptimizerError(f"bon-width takes no parameters, got {sorted(params)}")
        return BonWidthOptimizer()
    raise OptimizerError(
        f"unknown optimizer kind {kind!r}; supported: local-search, " "budgeted-search, bon-width"
    )


@dataclass(frozen=True)
class LadderSweep:
    """A full (pressure x arm x reward) sweep over one environment.

    Built by :func:`sweep_ladder`; consumed by the runner and report.
    Every entry keeps the optimization result so nothing downstream sees
    a policy without its provenance (fingerprint, trace, stop reason).
    """

    env_name: str
    env_version: str
    optimizer_kind: str
    reward_name: str
    pressures: tuple[int, ...]
    arms: tuple[str, ...]
    results: dict[tuple[str, str, int], OptimizationResult] = field(default_factory=dict)

    def at(self, arm: str, pressure: int) -> OptimizationResult:
        """The result for (arm, pressure) under the sweep's reward."""
        try:
            return self.results[(arm, self.reward_name, pressure)]
        except KeyError as exc:
            raise OptimizerError(
                f"no result for arm={arm!r}, pressure={pressure!r} "
                f"(sweep covers pressures {self.pressures} on arms {self.arms})"
            ) from exc

    def value_series(self, arm: str) -> tuple[float, ...]:
        """The optimized value on one arm across the pressure ladder."""
        return tuple(self.at(arm, pressure).value for pressure in self.pressures)


def sweep_ladder(
    env: TaskEnvironment,
    optimizer: PressureOptimizer,
    *,
    reward_name: str,
    arms: Sequence[str],
    pressures: Sequence[int],
    seed: int,
) -> LadderSweep:
    """Run one optimizer across the full (arm x pressure) grid.

    The same seed is used for every cell, so the alpha=0 starting policy
    is identical across arms (any arm-dependence enters through
    ``sample_reference``'s arm argument, by design).
    """
    _check_reward_name(reward_name)
    if not arms:
        raise OptimizerError("arms must be non-empty")
    if not pressures:
        raise OptimizerError("pressures must be non-empty")
    for arm in arms:
        if arm not in env.arms:
            raise OptimizerError(
                f"arm {arm!r} not offered by environment {env.name!r} ({list(env.arms)})"
            )
    ladder = sorted(set(int(p) for p in pressures))
    if ladder != sorted(pressures):
        raise OptimizerError("pressures must not repeat")
    results: dict[tuple[str, str, int], OptimizationResult] = {}
    for arm in arms:
        for pressure in ladder:
            results[(arm, reward_name, pressure)] = optimizer.optimize(
                env, reward_name=reward_name, arm=arm, pressure=pressure, seed=seed
            )
    return LadderSweep(
        env_name=env.name,
        env_version=env.version,
        optimizer_kind=optimizer.kind,
        reward_name=reward_name,
        pressures=tuple(ladder),
        arms=tuple(arms),
        results=results,
    )


__all__ = [
    "BonWidthOptimizer",
    "LadderSweep",
    "LocalSearchOptimizer",
    "BudgetedSearchOptimizer",
    "OptimizationResult",
    "OptimizerError",
    "PressureOptimizer",
    "START_KINDS",
    "TraceStep",
    "optimizer_from_config",
    "sweep_ladder",
]
