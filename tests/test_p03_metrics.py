"""P03 calibration metric tests with hand-computed known values.

The worked set: scores (0.9, 0.8, 0.6, 0.3), outcomes (1, 0, 1, 0).
Every expected value below is carried by hand from the Chapter 06
formulas and cross-checked against the chapter's discipline:

* ECE (K=10) = 0.4 (all four bins singleton; |gap| weighted by 1/4);
* Brier = 0.225; clipped log loss = 0.6456 (natural log);
* mean gap = +0.15 (mean confidence 0.65, accuracy 0.5);
* AURC = 0.3333 (R(m) = 0, 0.5, 1/3, 0.5); full-coverage risk 0.5;
* oracle AURC = 0.2083 (correct-first ranking: R(m) = 0, 0, 1/3, 1/2);
* AURC gap = 0.125.
"""

import math

import pytest

from ai_safety_course.calibration.metrics import (
    LOG_EPS,
    Z_95,
    CalibrationError,
    brier_score,
    log_loss,
    mean_gap,
    reliability_table,
)
from ai_safety_course.calibration.selection import (
    RiskCoverageCurve,
    ThresholdPolicy,
    aurc_gap,
    oracle_aurc,
    risk_coverage_curve,
    threshold_policy,
)

SCORES = (0.9, 0.8, 0.6, 0.3)
OUTCOMES = (1, 0, 1, 0)


class TestReliabilityTable:
    """Binning, ECE, and the report-your-bin-counts discipline."""

    def test_worked_set_ece(self) -> None:
        table = reliability_table(SCORES, OUTCOMES, num_bins=10)
        assert table.total == 4
        assert table.bin_counts == (1, 1, 1, 1)
        assert table.ece == pytest.approx(0.4)

    def test_singleton_bins_carry_wide_intervals(self) -> None:
        # The chapter's rule: a 1-item bin at accuracy 0.0 has a Wilson
        # upper bound near 0.79 — the reason bin counts ride along.
        table = reliability_table(SCORES, OUTCOMES, num_bins=10)
        for bin_ in table.bins:
            assert bin_.count == 1
            assert bin_.accuracy_interval[1] > 0.7

    def test_ece_statement_names_the_binning(self) -> None:
        table = reliability_table(SCORES, OUTCOMES, num_bins=10)
        statement = table.ece_statement()
        assert "K = 10" in statement
        assert "bin counts: 1, 1, 1, 1" in statement

    def test_all_identical_scores_single_bin(self) -> None:
        table = reliability_table([0.5, 0.5, 0.5], [1, 0, 1], num_bins=10)
        assert table.bin_counts == (3,)
        assert table.ece == pytest.approx(2 / 3 - 0.5)  # |2/3 - 0.5|

    def test_ece_depends_on_k(self) -> None:
        # The binning artifact, demonstrated: K=1 collapses ECE to the
        # mean gap's absolute value; K=10 sees the shape.
        table_k1 = reliability_table(SCORES, OUTCOMES, num_bins=1)
        assert table_k1.ece == pytest.approx(abs(mean_gap(SCORES, OUTCOMES)))
        table_k10 = reliability_table(SCORES, OUTCOMES, num_bins=10)
        assert table_k10.ece == pytest.approx(0.4)
        assert table_k1.ece != pytest.approx(table_k10.ece)

    def test_mean_gap_differs_from_ece(self) -> None:
        # The chapter's point: the marginal cancels what ECE sees.
        assert mean_gap(SCORES, OUTCOMES) == pytest.approx(0.15)
        assert reliability_table(SCORES, OUTCOMES, 10).ece == pytest.approx(0.4)

    def test_score_one_lands_in_last_bin(self) -> None:
        table = reliability_table([1.0, 0.05], [1, 0], num_bins=10)
        assert table.bins[-1].index == 9
        assert table.bins[-1].count == 1

    def test_fail_closed_on_inputs(self) -> None:
        with pytest.raises(CalibrationError):
            reliability_table([0.5], [1, 0])
        with pytest.raises(CalibrationError):
            reliability_table([], [])
        with pytest.raises(CalibrationError):
            reliability_table([1.5], [1])
        with pytest.raises(CalibrationError):
            reliability_table([0.5], [2])
        with pytest.raises(CalibrationError):
            reliability_table([0.5], [1], num_bins=0)
        with pytest.raises(CalibrationError):
            reliability_table([float("nan")], [1])


class TestProperScoringRules:
    """Brier and clipped log loss on the worked set."""

    def test_brier_worked(self) -> None:
        # (0.01 + 0.64 + 0.16 + 0.09) / 4 = 0.225
        assert brier_score(SCORES, OUTCOMES) == pytest.approx(0.225)

    def test_brier_perfect_scores(self) -> None:
        assert brier_score([1.0, 0.0], [1, 0]) == pytest.approx(0.0)

    def test_brier_worst_case(self) -> None:
        assert brier_score([1.0, 0.0], [0, 1]) == pytest.approx(1.0)

    def test_log_loss_worked(self) -> None:
        # -(ln 0.9 + ln 0.2 + ln 0.6 + ln 0.7)/4 = 0.6456
        assert log_loss(SCORES, OUTCOMES) == pytest.approx(0.6456, abs=1e-4)

    def test_log_loss_clips_extremes_finitely(self) -> None:
        value = log_loss([0.0, 1.0], [1, 0])
        assert math.isfinite(value)
        # Both items clip to the epsilon band; the float rounding of
        # 1 - (1 - eps) makes the value epsilon-close to -ln(eps).
        assert value == pytest.approx(-math.log(LOG_EPS), rel=1e-4)

    def test_log_loss_perfect(self) -> None:
        assert log_loss([1.0, 0.0], [1, 0]) == pytest.approx(0.0, abs=1e-12)


class TestRiskCoverage:
    """Rank-based curves, AURC, oracle ceiling, threshold ledger."""

    def test_worked_set_curve(self) -> None:
        curve = risk_coverage_curve(SCORES, OUTCOMES)
        assert isinstance(curve, RiskCoverageCurve)
        risks = [point.selective_risk for point in curve.points]
        assert risks == [pytest.approx(r) for r in (0.0, 0.5, 1 / 3, 0.5)]
        assert curve.full_coverage_risk == pytest.approx(0.5)

    def test_worked_set_aurc_and_oracle(self) -> None:
        curve = risk_coverage_curve(SCORES, OUTCOMES)
        assert curve.aurc == pytest.approx(1 / 3)
        assert oracle_aurc(OUTCOMES) == pytest.approx(0.5 / 4 + (1 / 3) / 4)
        # (0 + 0 + 1/3 + 1/2)/4 = 0.2083
        assert oracle_aurc(OUTCOMES) == pytest.approx(0.2083, abs=1e-4)
        assert aurc_gap(SCORES, OUTCOMES) == pytest.approx(0.125)

    def test_perfect_score_zero_gap(self) -> None:
        scores = (0.9, 0.8)
        outcomes = (1, 0)
        assert aurc_gap(scores, outcomes) == pytest.approx(0.0)
        assert risk_coverage_curve(scores, outcomes).aurc == pytest.approx(oracle_aurc(outcomes))

    def test_inverted_signal_is_worse_than_answering_everything(self) -> None:
        # The chapter's poisoned-instrument fact: an inverted signal
        # makes the gate WORSE than full coverage on average (AURC
        # above the full-coverage risk).
        inverted = (0.1, 0.2, 0.4, 0.7)  # ranks the wrong items first
        curve = risk_coverage_curve(inverted, OUTCOMES)
        assert curve.aurc > curve.full_coverage_risk

    def test_ties_broken_by_item_index(self) -> None:
        curve = risk_coverage_curve([0.5, 0.5], [1, 0])
        # Item 0 (correct) answers before item 1 (wrong): R(1) = 0.
        assert curve.points[0].selective_risk == pytest.approx(0.0)

    def test_every_point_carries_its_interval_and_denominator(self) -> None:
        curve = risk_coverage_curve(SCORES, OUTCOMES)
        for point in curve.points:
            assert point.answered == point.rank
            assert 0.0 <= point.risk_interval[0] <= point.selective_risk
            assert point.selective_risk <= point.risk_interval[1] <= 1.0

    def test_at_coverage_rounds_to_nearest_rank(self) -> None:
        curve = risk_coverage_curve(SCORES, OUTCOMES)
        point = curve.at_coverage(0.5)
        assert point.rank == 2
        assert point.selective_risk == pytest.approx(0.5)

    def test_at_coverage_fail_closed(self) -> None:
        curve = risk_coverage_curve(SCORES, OUTCOMES)
        with pytest.raises(CalibrationError):
            curve.at_coverage(0.0)
        with pytest.raises(CalibrationError):
            curve.at_coverage(1.5)

    def test_z_precision_is_the_module_contract(self) -> None:
        assert Z_95 == pytest.approx(1.959963984540054, abs=1e-15)


class TestThresholdPolicy:
    """Both sides of the abstention ledger."""

    def test_worked_policy(self) -> None:
        policy = threshold_policy(SCORES, OUTCOMES, 0.5)
        assert isinstance(policy, ThresholdPolicy)
        assert policy.answered == 3  # 0.9, 0.8, 0.6
        assert policy.errors == 1  # the 0.8 was wrong
        assert policy.coverage == pytest.approx(0.75)
        assert policy.selective_risk == pytest.approx(1 / 3)
        assert policy.false_abstentions == 0  # the declined 0.3 was wrong

    def test_false_abstention_side_is_counted(self) -> None:
        # Declining correct items is the over-refusal side.
        policy = threshold_policy(SCORES, OUTCOMES, 0.7)
        assert policy.answered == 2  # 0.9, 0.8
        assert policy.false_abstentions == 1  # 0.6 was correct, declined
        assert policy.false_abstention_rate == pytest.approx(0.25)

    def test_tau_zero_answers_everything(self) -> None:
        policy = threshold_policy(SCORES, OUTCOMES, 0.0)
        assert policy.answered == 4
        assert policy.selective_risk == pytest.approx(0.5)

    def test_unanswered_policy_fails_closed_with_guidance(self) -> None:
        policy = threshold_policy(SCORES, OUTCOMES, 1.0)  # no score >= 1.0
        assert policy.answered == 0
        with pytest.raises(CalibrationError, match="coverage 0"):
            _ = policy.selective_risk

    def test_fail_closed_on_tau(self) -> None:
        with pytest.raises(CalibrationError):
            threshold_policy(SCORES, OUTCOMES, 1.5)
        with pytest.raises(CalibrationError):
            threshold_policy(SCORES, OUTCOMES, -0.1)
        with pytest.raises(CalibrationError):
            threshold_policy(SCORES, OUTCOMES, float("nan"))
