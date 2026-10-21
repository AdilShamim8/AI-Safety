"""evaluation — the P01 evaluation harness and scorer validation.

This subpackage implements, as code, the Chapter 02 evaluation-science
discipline (``chapters/02-evaluation-science-and-experimental-design/``):

* versioned, checksummed case sets with fail-closed schema validation
  (``cases``);
* deterministic, offline model adapters — no network, no model downloads
  (``adapters``);
* rate metrics reported with Wilson 95% intervals and explicit
  denominators, plus the paired refusal/compliance ledger (``metrics``);
* a config-driven, resumable, fail-closed runner with seed control
  (``runner``);
* a dated markdown report generator with a provenance block (``report``);
* a rule-based refusal scorer validated against hand-verified examples
  (``scorer``).

Everything here is CPU-only and stdlib+PyYAML; determinism is a design
constraint, not an afterthought (seeds are threaded through, and outputs
for a fixed configuration are byte-stable).
"""

from ai_safety_course.evaluation.adapters import (
    AdapterError,
    CallableAdapter,
    EchoAdapter,
    ModelAdapter,
    ScriptedAdapter,
)
from ai_safety_course.evaluation.cases import Case, CaseSet, CaseSetError
from ai_safety_course.evaluation.metrics import (
    MetricSummary,
    PairedLedger,
    WilsonInterval,
    paired_ledger,
    rate_metric,
    wilson_interval,
)
from ai_safety_course.evaluation.runner import (
    RunConfig,
    RunError,
    RunResult,
    load_run_config,
    run_evaluation,
)
from ai_safety_course.evaluation.scorer import (
    RuleBasedRefusalScorer,
    Scorer,
    ScoreResult,
    hand_verified_examples,
    validate_scorer,
)

__all__ = [
    "AdapterError",
    "CallableAdapter",
    "Case",
    "CaseSet",
    "CaseSetError",
    "EchoAdapter",
    "MetricSummary",
    "ModelAdapter",
    "PairedLedger",
    "RuleBasedRefusalScorer",
    "RunConfig",
    "RunError",
    "RunResult",
    "ScoreResult",
    "ScriptedAdapter",
    "Scorer",
    "WilsonInterval",
    "hand_verified_examples",
    "load_run_config",
    "paired_ledger",
    "rate_metric",
    "run_evaluation",
    "validate_scorer",
    "wilson_interval",
]
