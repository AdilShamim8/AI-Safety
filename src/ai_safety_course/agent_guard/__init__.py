"""agent_guard — P07: injection defense as a capability audit (Ch. 13-14 as code).

The privilege and trust-boundary matrix (the audit artifact), the
R1-R4 capability policy with provenance tags (the defense), the
paired scenario harness (the evaluation), and Wilson/sign-test
metrics (the pricing). Stdlib-only, deterministic, offline.
"""

from ai_safety_course.agent_guard.harness import (
    ARM_CAPABILITY,
    ARM_UNDEFENDED,
    PairedRun,
    ScenarioResult,
    StepOutcome,
    run_paired,
    run_scenario,
)
from ai_safety_course.agent_guard.matrix import (
    AUTHORITY_LEVELS,
    MatrixAudit,
    MatrixError,
    PrivilegeMatrix,
    ToolSpec,
    audit_matrix,
    load_matrix,
    parse_matrix,
)
from ai_safety_course.agent_guard.metrics import (
    P07Metrics,
    PairedLedger,
    RateWithInterval,
    compute_metrics,
    exact_one_sided_sign_p,
)
from ai_safety_course.agent_guard.policy import (
    R1,
    R2,
    R3,
    R4,
    AllowAllPolicy,
    Argument,
    CapabilityPolicy,
    Decision,
    PolicyResult,
    Provenance,
    Session,
    ToolCall,
)
from ai_safety_course.agent_guard.scenarios import (
    Scenario,
    ScenarioError,
    ScenarioSet,
    Step,
    load_scenario_set,
    parse_scenario_set,
)

__all__ = [
    "ARM_CAPABILITY",
    "ARM_UNDEFENDED",
    "AUTHORITY_LEVELS",
    "R1",
    "R2",
    "R3",
    "R4",
    "AllowAllPolicy",
    "Argument",
    "MatrixAudit",
    "MatrixError",
    "PairedLedger",
    "PairedRun",
    "P07Metrics",
    "PolicyResult",
    "PrivilegeMatrix",
    "Provenance",
    "RateWithInterval",
    "Scenario",
    "ScenarioError",
    "ScenarioResult",
    "ScenarioSet",
    "Session",
    "Step",
    "StepOutcome",
    "ToolCall",
    "ToolSpec",
    "audit_matrix",
    "compute_metrics",
    "Decision",
    "CapabilityPolicy",
    "exact_one_sided_sign_p",
    "load_matrix",
    "load_scenario_set",
    "parse_matrix",
    "parse_scenario_set",
    "run_paired",
    "run_scenario",
]
