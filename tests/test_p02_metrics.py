"""P02 metric tests: every expected value hand-computed from the formulas.

The Wilson interval uses the full-precision quantile
``z = 1.959963984540054`` (not the 1.96 shorthand of the P01 package);
expected bounds below are computed by carrying the formula
center = (p̂ + z²/2n)/(1 + z²/n),
half = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n)
at double precision and rounding at the fourth decimal.

Goodhart-gap, side-effect, held-out-divergence, paired-comparison, and
gate semantics are pinned against the Chapter 03 definitions
(``chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md``
sections 3.4, 3.7, and 4).
"""

import math

import pytest

from ai_safety_course.reward_spec.metrics import (
    Z_95,
    GateConfig,
    GateOutcome,
    HeldOutDivergence,
    MetricsError,
    PairedComparison,
    SideEffectEvent,
    SideEffectLedger,
    evaluate_gates,
    goodhart_gap,
    rate_metric,
    summarize_rates,
    wilson_interval,
)


def _bounds(successes: int, denominator: int) -> tuple[float, float]:
    interval = wilson_interval(successes, denominator)
    return round(interval.lower, 4), round(interval.upper, 4)


class TestWilsonInterval:
    """Bounds pinned by carrying the formula at double precision."""

    def test_z_constant_is_the_precise_quantile(self) -> None:
        # 1.959963984540054, not the 1.96 shorthand (module contract).
        assert Z_95 == pytest.approx(1.959963984540054, rel=0, abs=1e-15)
        assert Z_95 != 1.96

    def test_half_half_split(self) -> None:
        # 250/500: bounds [0.4563, 0.5437] (hand-carried at full-precision z).
        assert _bounds(250, 500) == (0.4563, 0.5437)

    def test_zero_successes(self) -> None:
        # 0/40: upper bound 0.0876 (z²-only upper limit form).
        assert _bounds(0, 40) == (0.0, 0.0876)

    def test_all_successes(self) -> None:
        # 40/40: lower bound 0.9124 (mirror of the zero case).
        assert _bounds(40, 40) == (0.9124, 1.0)

    def test_small_denominator(self) -> None:
        # 6/6: [0.6097, 1.0].
        assert _bounds(6, 6) == (0.6097, 1.0)

    def test_extremes_fail_closed(self) -> None:
        with pytest.raises(MetricsError):
            wilson_interval(1, 0)
        with pytest.raises(MetricsError):
            wilson_interval(-1, 10)
        with pytest.raises(MetricsError):
            wilson_interval(11, 10)

    def test_rate_metric_carries_name_and_denominator(self) -> None:
        summary = rate_metric("damage-free episode rate (tuning)", 5, 6)
        assert summary.name == "damage-free episode rate (tuning)"
        assert summary.successes == 5
        assert summary.denominator == 6
        assert summary.rate == pytest.approx(5 / 6)
        assert "(83.33%)" in str(summary)  # explicit rate with n=6 denominator

    def test_summarize_rates_sorted_deterministically(self) -> None:
        rates = {
            "b-metric": rate_metric("b-metric", 1, 4),
            "a-metric": rate_metric("a-metric", 2, 4),
        }
        rendered = summarize_rates(rates)
        assert rendered.splitlines()[0].startswith("a-metric")


class TestGoodhartGap:
    """Signed gap semantics: negative = untuned regime, positive = hacking."""

    def test_positive_gap_is_the_hacking_signature(self) -> None:
        gap = goodhart_gap(0.92, 0.31, arm="tuning", pressure=64)
        assert gap.gap == pytest.approx(0.61)
        assert gap.gap_pp == pytest.approx(61.0)
        assert "G(alpha=64" in str(gap)

    def test_negative_gap_is_the_untuned_regime(self) -> None:
        gap = goodhart_gap(0.41, 0.55, arm="tuning", pressure=1)
        assert gap.gap == pytest.approx(-0.14)
        assert gap.gap_pp < 0

    def test_per_arm_not_silently_aggregated(self) -> None:
        # The dataclass carries the arm so reports cannot average arms.
        gap = goodhart_gap(0.5, 0.4, arm="held_out", pressure=4)
        assert gap.arm == "held_out"
        assert gap.pressure == 4

    def test_fail_closed_on_nonfinite_and_bad_pressure(self) -> None:
        with pytest.raises(MetricsError):
            goodhart_gap(math.inf, 0.5, arm="tuning", pressure=1)
        with pytest.raises(MetricsError):
            goodhart_gap(0.5, math.nan, arm="tuning", pressure=1)
        with pytest.raises(MetricsError):
            goodhart_gap(0.5, 0.4, arm="tuning", pressure=0)


class TestSideEffectLedger:
    """Discrete events with magnitudes, never folded into a scalar."""

    def test_build_and_counts(self) -> None:
        events = (
            SideEffectEvent(
                arm="tuning", episode="T1", kind="vase-broken", location=(2, 2), magnitude=1.0
            ),
            SideEffectEvent(
                arm="tuning", episode="T2", kind="vase-broken", location=(1, 0), magnitude=1.0
            ),
            SideEffectEvent(
                arm="tuning", episode="T2", kind="vase-broken", location=(1, 1), magnitude=1.0
            ),
        )
        ledger = SideEffectLedger.build("tuning", events, episode_count=6)
        assert ledger.arm == "tuning"
        assert ledger.episode_count == 6
        assert ledger.event_count == 3
        assert ledger.total_magnitude == pytest.approx(3.0)
        assert ledger.damaged_episodes == 2
        rate = ledger.side_effect_rate()
        assert rate.successes == 2
        assert rate.denominator == 6
        assert ledger.kind_totals() == {"vase-broken": 3}

    def test_zero_event_ledger_is_valid(self) -> None:
        ledger = SideEffectLedger.build("held_out", (), episode_count=5)
        assert ledger.event_count == 0
        assert ledger.side_effect_rate().rate == 0.0

    def test_fail_closed_on_event_arm_mismatch(self) -> None:
        with pytest.raises(MetricsError):
            SideEffectLedger.build(
                "tuning",
                (
                    SideEffectEvent(
                        arm="held_out",
                        episode="H1",
                        kind="vase-broken",
                        location=(0, 0),
                        magnitude=1.0,
                    ),
                ),
                episode_count=6,
            )

    def test_fail_closed_on_nonpositive_magnitude(self) -> None:
        with pytest.raises(MetricsError):
            SideEffectLedger.build(
                "tuning",
                (
                    SideEffectEvent(
                        arm="tuning",
                        episode="T1",
                        kind="vase-broken",
                        location=(0, 0),
                        magnitude=-1.0,
                    ),
                ),
                episode_count=6,
            )


class TestHeldOutDivergence:
    """held-out minus tuning at matched pressure, worst = most negative."""

    def test_divergences_and_worst(self) -> None:
        series = HeldOutDivergence.build(
            "intended",
            pressures=(1, 4, 16),
            train_values=(0.60, 0.55, 0.50),
            heldout_values=(0.59, 0.44, 0.20),
        )
        assert series.divergences == (
            pytest.approx(-0.01),
            pytest.approx(-0.11),
            pytest.approx(-0.30),
        )
        assert series.worst == pytest.approx(-0.30)
        assert "held-out divergence [intended]" in str(series)

    def test_fail_closed_on_length_mismatch(self) -> None:
        with pytest.raises(MetricsError):
            HeldOutDivergence.build(
                "proxy", pressures=(1, 4), train_values=(0.5,), heldout_values=(0.5, 0.4)
            )

    def test_fail_closed_on_empty(self) -> None:
        with pytest.raises(MetricsError):
            HeldOutDivergence.build("proxy", pressures=(), train_values=(), heldout_values=())

    def test_fail_closed_on_nonfinite(self) -> None:
        with pytest.raises(MetricsError):
            HeldOutDivergence.build(
                "proxy", pressures=(1,), train_values=(math.inf,), heldout_values=(0.5,)
            )


class TestPairedComparison:
    """Episode-paired primary-vs-control with a Wilson win rate."""

    def test_means_counts_and_win_rate(self) -> None:
        comparison = PairedComparison.build(
            name="proxy-vs-intended @ alpha=16 [tuning]",
            primary_values=(0.8, 0.4, 0.6, 0.2),
            control_values=(0.6, 0.4, 0.9, 0.2),
        )
        assert comparison.mean_primary == pytest.approx(0.5)
        assert comparison.mean_control == pytest.approx(0.525)
        assert comparison.mean_difference == pytest.approx(-0.025)
        assert comparison.primary_wins == 1
        assert comparison.ties == 2
        assert comparison.control_wins == 1
        win = comparison.win_rate()
        assert win.successes == 1
        assert win.denominator == 4

    def test_paired_lengths_must_match(self) -> None:
        with pytest.raises(MetricsError):
            PairedComparison.build(name="x", primary_values=(0.5, 0.5), control_values=(0.5,))

    def test_fail_closed_on_empty_series(self) -> None:
        with pytest.raises(MetricsError):
            PairedComparison.build(name="x", primary_values=(), control_values=())

    def test_fail_closed_on_nonfinite_pair(self) -> None:
        with pytest.raises(MetricsError):
            PairedComparison.build(name="x", primary_values=(math.nan,), control_values=(0.5,))


class TestGates:
    """G1 degradation and G2 floor judged by interval bounds, not points."""

    def _point_and_baseline(self) -> tuple:
        # point 12/20 = 0.60 [0.3866, 0.7822]; baseline 18/20 = 0.90
        # [0.6993, 0.9722] (hand-carried at z = 1.959963984540054).
        point = rate_metric("truthful-answer rate (tuning)", 12, 20)
        baseline = rate_metric("truthful-answer rate (tuning) [reference]", 18, 20)
        return point, baseline

    def test_g1_fails_when_worst_case_degradation_exceeds_threshold(self) -> None:
        point, baseline = self._point_and_baseline()
        config = GateConfig(
            metric_name="truthful-answer rate (tuning)", degradation_pp=20.0, floor_pp=0.0
        )
        outcome = evaluate_gates(
            config, "truthful-answer rate (tuning)", point, baseline, pressure=16, arm="tuning"
        )
        # worst-case degradation = 100*(0.90 - 0.3866) = 51.3pp > 20pp -> fail
        assert outcome.g1_pass is False
        assert outcome.worst_case_degradation_pp == pytest.approx(51.34, abs=0.05)
        # floor 0: lower bound 38.66pp >= 0 -> G2 passes
        assert outcome.g2_pass is True
        assert "G1(FAIL" in str(outcome)

    def test_g2_fails_when_lower_bound_below_floor(self) -> None:
        point, baseline = self._point_and_baseline()
        config = GateConfig(
            metric_name="truthful-answer rate (tuning)", degradation_pp=100.0, floor_pp=50.0
        )
        outcome = evaluate_gates(
            config, "truthful-answer rate (tuning)", point, baseline, pressure=16, arm="tuning"
        )
        assert outcome.g1_pass is True  # 100pp tolerance
        assert outcome.g2_pass is False  # lower bound 38.66pp < 50pp floor
        assert outcome.worst_case_floor_pp == pytest.approx(38.66, abs=0.05)

    def test_metric_name_mismatch_is_a_configuration_error(self) -> None:
        point, baseline = self._point_and_baseline()
        config = GateConfig(metric_name="other metric", degradation_pp=20.0, floor_pp=0.0)
        with pytest.raises(MetricsError):
            evaluate_gates(
                config, "truthful-answer rate (tuning)", point, baseline, pressure=1, arm="tuning"
            )

    def test_gate_config_validation(self) -> None:
        with pytest.raises(MetricsError):
            GateConfig(metric_name="", degradation_pp=1.0, floor_pp=0.0).validate()
        with pytest.raises(MetricsError):
            GateConfig(metric_name="m", degradation_pp=-1.0, floor_pp=0.0).validate()
        with pytest.raises(MetricsError):
            GateConfig(metric_name="m", degradation_pp=1.0, floor_pp=101.0).validate()

    def test_gate_outcome_type_is_frozen_and_carries_pressure(self) -> None:
        point, baseline = self._point_and_baseline()
        config = GateConfig(
            metric_name="truthful-answer rate (tuning)", degradation_pp=20.0, floor_pp=0.0
        )
        outcome = evaluate_gates(
            config, "truthful-answer rate (tuning)", point, baseline, pressure=64, arm="held_out"
        )
        assert isinstance(outcome, GateOutcome)
        assert outcome.pressure == 64
        assert outcome.arm == "held_out"
