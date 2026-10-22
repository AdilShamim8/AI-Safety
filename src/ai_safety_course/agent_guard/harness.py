"""harness — the paired evaluation engine for P07.

Each scenario runs under two arms that differ *only* in policy:

- **undefended** — :class:`AllowAllPolicy` (full delegation, the
  confused deputy deployed);
- **capability** — :class:`CapabilityPolicy` (R1-R4 over the
  privilege matrix).

Semantics, fixed by this module and shared by both arms:

- A step executes when the policy verdict is ALLOW.
- A CONSENT_REQUIRED verdict is resolved by the scenario's scripted
  user: ``grant`` records the consent (tool, and destination when the
  call has one) and re-checks; ``deny``/``none`` leaves the call
  unexecuted.
- A BLOCK (R2/R3) halts the flow: later steps do not run — the host
  interrupts the trace rather than continuing past a hard violation.
- An attack scenario *succeeds* under an arm when its target step
  executes under that arm; a benign scenario *completes* when every
  step executes.

The paired ledger across scenarios is the evidence: attack outcomes
(undefended success, capability success) and benign outcomes
(completion, completion) feed the sign-test and Wilson machinery in
:mod:`ai_safety_course.agent_guard.metrics`. Everything is
deterministic — no sampling, no model calls, no network.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai_safety_course.agent_guard.policy import (
    AllowAllPolicy,
    CapabilityPolicy,
    Decision,
    PolicyResult,
    Session,
)
from ai_safety_course.agent_guard.scenarios import Scenario, Step

#: Arm names, stable in reports.
ARM_UNDEFENDED = "undefended"
ARM_CAPABILITY = "capability-r1-r4"


@dataclass(frozen=True)
class StepOutcome:
    """What happened to one step under one arm."""

    step_index: int  # 1-based
    tool: str
    decision: Decision
    executed: bool
    rules_fired: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    consent_granted: bool = False


@dataclass(frozen=True)
class ScenarioResult:
    """The full outcome of one scenario under one arm."""

    scenario_id: str
    kind: str
    arm: str
    outcomes: tuple[StepOutcome, ...]
    attack_succeeded: bool
    benign_completed: bool
    halted_at: int | None  # 1-based step where the flow halted, if it did

    @property
    def success(self) -> bool:
        """Attack success or benign completion, per the scenario's kind."""
        return self.attack_succeeded if self.kind == "attack" else self.benign_completed


def _run_step(
    step: Step,
    index: int,
    policy: CapabilityPolicy | AllowAllPolicy,
    session: Session,
) -> tuple[StepOutcome, bool]:
    """Run one step; returns (outcome, should_continue)."""
    result: PolicyResult = policy.check(step.call, session)
    consent_granted = False

    if result.decision is Decision.CONSENT_REQUIRED and step.consent == "grant":
        destination = (
            policy.destination_of(step.call) if isinstance(policy, CapabilityPolicy) else None
        )
        session.consent_to(step.call.tool, destination)
        consent_granted = True
        result = policy.check(step.call, session)

    executed = result.decision is Decision.ALLOW
    outcome = StepOutcome(
        step_index=index,
        tool=step.call.tool,
        decision=result.decision,
        executed=executed,
        rules_fired=result.rules_fired,
        reasons=result.reasons,
        consent_granted=consent_granted,
    )
    continue_flow = executed
    return outcome, continue_flow


def run_scenario(
    scenario: Scenario,
    policy: CapabilityPolicy | AllowAllPolicy,
    arm: str,
) -> ScenarioResult:
    """Run one scenario under one policy arm (halt-on-block semantics)."""
    session = Session()
    outcomes: list[StepOutcome] = []
    halted_at: int | None = None

    for index, step in enumerate(scenario.steps, start=1):
        outcome, continue_flow = _run_step(step, index, policy, session)
        outcomes.append(outcome)
        if not continue_flow:
            halted_at = index
            break

    executed_steps = {o.step_index for o in outcomes if o.executed}
    attack_succeeded = scenario.kind == "attack" and scenario.target_step in executed_steps
    benign_completed = scenario.kind == "benign" and len(executed_steps) == len(scenario.steps)
    return ScenarioResult(
        scenario_id=scenario.id,
        kind=scenario.kind,
        arm=arm,
        outcomes=tuple(outcomes),
        attack_succeeded=attack_succeeded,
        benign_completed=benign_completed,
        halted_at=halted_at,
    )


@dataclass(frozen=True)
class PairedRun:
    """Every scenario under both arms, plus the per-arm rollups."""

    results: tuple[tuple[ScenarioResult, ScenarioResult], ...]  # (undefended, capability)
    undefended: tuple[ScenarioResult, ...]
    capability: tuple[ScenarioResult, ...]

    @property
    def attacks(self) -> tuple[tuple[ScenarioResult, ScenarioResult], ...]:
        return tuple(pair for pair in self.results if pair[0].kind == "attack")

    @property
    def benign(self) -> tuple[tuple[ScenarioResult, ScenarioResult], ...]:
        return tuple(pair for pair in self.results if pair[0].kind == "benign")


def run_paired(
    scenarios: tuple[Scenario, ...],
    capability_policy: CapabilityPolicy,
) -> PairedRun:
    """Run every scenario under both arms (undefended arm uses AllowAll)."""
    allow_all = AllowAllPolicy(capability_policy.matrix)
    pairs: list[tuple[ScenarioResult, ScenarioResult]] = []
    undefended: list[ScenarioResult] = []
    capability: list[ScenarioResult] = []
    for scenario in scenarios:
        u = run_scenario(scenario, allow_all, ARM_UNDEFENDED)
        c = run_scenario(scenario, capability_policy, ARM_CAPABILITY)
        pairs.append((u, c))
        undefended.append(u)
        capability.append(c)
    return PairedRun(
        results=tuple(pairs),
        undefended=tuple(undefended),
        capability=tuple(capability),
    )
