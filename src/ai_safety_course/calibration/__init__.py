"""calibration — the P03 calibration and selective-prediction project package.

This subpackage implements, as code, the Chapter 06 measurement
discipline
(``chapters/06-honesty-uncertainty-and-selective-prediction/``):

* reliability tables with per-bin counts, Wilson intervals, ECE with
  its binning stated, Brier and clipped log loss, and the mean gap as
  a marginal — never as a calibration measure (``metrics``);
* rank-based risk–coverage curves with AURC, the oracle ceiling and
  gap, threshold policies with both sides of the abstention ledger
  (``selection``).

Everything is CPU-only and stdlib-only. Determinism is a design
constraint: tie-breaking is by item index, never sort instability.
"""

from ai_safety_course.calibration.metrics import (
    LOG_EPS,
    Z_95,
    CalibrationError,
    ReliabilityBin,
    ReliabilityTable,
    accuracy_rate,
    brier_score,
    log_loss,
    mean_gap,
    reliability_table,
)
from ai_safety_course.calibration.selection import (
    RiskCoverageCurve,
    RiskCoveragePoint,
    ThresholdPolicy,
    aurc_gap,
    oracle_aurc,
    risk_coverage_curve,
    threshold_policy,
)

__all__ = [
    "LOG_EPS",
    "Z_95",
    "CalibrationError",
    "ReliabilityBin",
    "ReliabilityTable",
    "RiskCoverageCurve",
    "RiskCoveragePoint",
    "ThresholdPolicy",
    "accuracy_rate",
    "aurc_gap",
    "brier_score",
    "log_loss",
    "mean_gap",
    "oracle_aurc",
    "reliability_table",
    "risk_coverage_curve",
    "threshold_policy",
]
