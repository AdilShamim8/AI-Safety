"""reward_spec — the P02 reward-misspecification project package.

This subpackage implements, as code, the Chapter 03 measurement
discipline
(``chapters/03-specification-reward-hacking-and-goal-misgeneralization/``):

* the Goodhart-gap, side-effect-ledger, held-out-divergence, paired-
  comparison, and preregistered-gate machinery with Wilson intervals at
  full-precision z (``metrics``);
* two small deterministic environments pairing an intended objective R
  with a misspecified proxy reward R_hat — the fragile-goods warehouse
  gridworld and the judge-scored-answers environment, both with tuning
  and held-out arms (``environments``);
* an optimization-pressure ladder over the policy space — deterministic
  local search whose *pressure* is the count of accepted improvement
  steps, sweeping from untuned to fully proxy-optimized (``optimizer``);
* a config-driven, resumable, fail-closed runner with seed control and a
  dated markdown report carrying full provenance (``runner``, ``report``).

Everything is CPU-only and stdlib-only; both environments are synthetic
model organisms authored for this course (no dataset content is
redistributed), and determinism is a design constraint: the same config
reproduces the same outputs byte-for-byte.
"""

from ai_safety_course.reward_spec.environments import (
    ARM_HELD_OUT,
    ARM_TUNING,
    REWARD_INTENDED,
    REWARD_PROXY,
    EnvironmentError,
    JudgeScoredAnswers,
    TaskEnvironment,
    WarehouseGridworld,
    environment_from_config,
)
from ai_safety_course.reward_spec.metrics import (
    Z_95,
    GateConfig,
    GateOutcome,
    GoodhartGap,
    HeldOutDivergence,
    MetricsError,
    MetricSummary,
    PairedComparison,
    SideEffectEvent,
    SideEffectLedger,
    WilsonInterval,
    evaluate_gates,
    goodhart_gap,
    rate_metric,
    summarize_rates,
    wilson_interval,
)

__all__ = [
    "ARM_HELD_OUT",
    "ARM_TUNING",
    "EnvironmentError",
    "GateConfig",
    "GateOutcome",
    "GoodhartGap",
    "HeldOutDivergence",
    "JudgeScoredAnswers",
    "MetricsError",
    "MetricSummary",
    "PairedComparison",
    "REWARD_INTENDED",
    "REWARD_PROXY",
    "SideEffectEvent",
    "SideEffectLedger",
    "TaskEnvironment",
    "WarehouseGridworld",
    "WilsonInterval",
    "Z_95",
    "environment_from_config",
    "evaluate_gates",
    "goodhart_gap",
    "rate_metric",
    "summarize_rates",
    "wilson_interval",
]
