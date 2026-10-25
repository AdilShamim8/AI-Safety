"""P10 — the capstone: bounded-agent evaluation and assurance dossier.

Integration of the course's project stack into one assurance artifact:
P07's R1-R4 capability guard + Ch. 08's monitor/audit-budget discipline
+ resource limits, evaluated as a three-arm paired comparison
(undefended / guard / bounded) over a held-out scenario set, and
reported through Ch. 22's claim/evidence/caveat grammar with the
deployability verdict that the numbers dictate — including the verdict
NOT DEPLOYABLE at the pinned configuration.
"""

from ai_safety_course.assurance.dossier import (
    DOSSIER_CONFIG_SCHEMA,
    Dossier,
    DossierConfig,
    DossierError,
    execute_dossier,
    load_dossier_config,
    run_dossier,
    wilson_interval,
    write_dossier_markdown,
)
from ai_safety_course.assurance.monitor import (
    ACTION_HOLD,
    ACTION_UNCOVERED,
    FlaggingMonitor,
    MonitorEvent,
)
from ai_safety_course.assurance.system import (
    ARM_BOUNDED,
    BoundedScenarioResult,
    ResourceLimits,
    ThreeArmRun,
    run_bounded_scenario,
    run_three_arms,
)

__all__ = [
    "ACTION_HOLD",
    "ACTION_UNCOVERED",
    "ARM_BOUNDED",
    "DOSSIER_CONFIG_SCHEMA",
    "Dossier",
    "DossierConfig",
    "DossierError",
    "FlaggingMonitor",
    "MonitorEvent",
    "ResourceLimits",
    "ThreeArmRun",
    "BoundedScenarioResult",
    "execute_dossier",
    "load_dossier_config",
    "run_bounded_scenario",
    "run_three_arms",
    "run_dossier",
    "wilson_interval",
    "write_dossier_markdown",
]
