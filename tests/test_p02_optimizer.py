"""P02 optimizer tests: determinism, honest saturation, and the pressure story.

Verified numbers pinned here (all computed by direct execution, seed=42,
warehouse = default parameters, judge = proxy-v1 unless stated):

* warehouse budgeted-search under the PROXY: alpha=8 -> J=1.000 with 5
  vase events (the clumsy untuned pool); alpha=4096 -> J=2.667 with 3
  events; alpha=65536 -> J=2.833 with 3 events; Goodhart gap pinned at
  2.000 from alpha=4096 up;
* warehouse budgeted-search under the INTENDED at alpha=65536: J=2.167
  with ZERO vase events and G=0.000 — the control arm discovers the
  vase-avoiding principle the proxy cannot price (the P02 headline);
* judge bon-width under the PROXY on tuning: width 4 -> J=0.820;
* local-search saturation: from the naive reference start on the
  warehouse, accepted-step climbing saturates at alpha=4 (J=2.333) and
  reports stopped_early honestly for every higher requested pressure.
"""

import pytest

from ai_safety_course.reward_spec.environments import (
    ARM_HELD_OUT,
    ARM_TUNING,
    REWARD_INTENDED,
    REWARD_PROXY,
    JudgeScoredAnswers,
    WarehouseGridworld,
)
from ai_safety_course.reward_spec.optimizer import (
    BonWidthOptimizer,
    BudgetedSearchOptimizer,
    LadderSweep,
    LocalSearchOptimizer,
    OptimizerError,
    TraceStep,
    optimizer_from_config,
    sweep_ladder,
)


class TestLocalSearchOptimizer:
    """Accepted-step pressure with honest saturation reporting."""

    def test_zero_pressure_returns_the_start_unchanged(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer(start="reference")
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=0, seed=42
        )
        assert result.achieved_pressure == 0
        assert result.stopped_early is False
        assert result.trace[0].accepted is False

    def test_saturation_is_reported_not_hidden(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer(start="reference")
        # From the naive start the climb saturates at 4 accepted steps.
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=8, seed=42
        )
        assert result.value == pytest.approx(2.333, abs=1e-3)
        assert result.achieved_pressure == 4
        assert result.stopped_early is True
        assert result.saturated is True
        # Requesting far more pressure changes nothing (same optimum).
        far = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=64, seed=42
        )
        assert far.value == pytest.approx(result.value)
        assert far.fingerprint == result.fingerprint

    def test_deterministic_same_seed_same_policy(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer(start="random")
        first = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=4, seed=7
        )
        second = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=4, seed=7
        )
        assert first.fingerprint == second.fingerprint
        assert first.value == second.value

    def test_monotone_value_along_the_trace(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer(start="random")
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=6, seed=11
        )
        values = [step.value for step in result.trace]
        assert values == sorted(values)  # hill climbing never regresses

    def test_configuration_validation(self) -> None:
        with pytest.raises(OptimizerError):
            LocalSearchOptimizer(start="middle")
        with pytest.raises(OptimizerError):
            LocalSearchOptimizer(max_neighbors_per_step=0)

    def test_bad_reward_and_pressure_fail_closed(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer()
        with pytest.raises(OptimizerError):
            optimizer.optimize(env, reward_name="vanilla", arm=ARM_TUNING, pressure=1, seed=1)
        with pytest.raises(OptimizerError):
            optimizer.optimize(env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=-1, seed=1)

    def test_neighbor_budget_is_a_safety_valve(self) -> None:
        env = WarehouseGridworld()
        optimizer = LocalSearchOptimizer(max_neighbors_per_step=10)
        with pytest.raises(OptimizerError, match="neighbors"):
            optimizer.optimize(env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=1, seed=1)


class TestBudgetedSearchOptimizer:
    """Evaluation-budget pressure: exact spend, monotone best, the P02 story."""

    @pytest.mark.parametrize(
        ("pressure", "proxy_value", "events"),
        [(8, 1.000, 5), (4096, 2.667, 3), (65536, 2.833, 3)],
    )
    def test_proxy_optimization_climbs_and_keeps_breaking_vases(
        self, pressure, proxy_value, events
    ) -> None:
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=pressure, seed=42
        )
        assert result.value == pytest.approx(proxy_value, abs=1e-3)
        assert env.side_effects(result.policy, ARM_TUNING, 0).event_count == events
        # The budget is spent exactly, never overspent.
        assert result.achieved_pressure == pressure
        assert result.stopped_early is False

    def test_intended_control_discovers_vase_avoidance(self) -> None:
        # The P02 headline: the same pressure under R instead of R_hat
        # converges to zero breakage and a zero Goodhart gap.
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_INTENDED, arm=ARM_TUNING, pressure=65536, seed=42
        )
        assert env.side_effects(result.policy, ARM_TUNING, 0).event_count == 0
        intended = env.evaluate(result.policy, REWARD_INTENDED, ARM_TUNING)
        proxy = env.evaluate(result.policy, REWARD_PROXY, ARM_TUNING)
        assert result.value == pytest.approx(2.167, abs=1e-3)
        assert proxy == pytest.approx(intended)  # G = 0 for the control

    def test_goodhart_gap_is_structurally_positive_for_proxy_policies(self) -> None:
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        proxy_result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=4096, seed=42
        )
        intended_of_proxy = env.evaluate(proxy_result.policy, REWARD_INTENDED, ARM_TUNING)
        assert proxy_result.value - intended_of_proxy == pytest.approx(2.000, abs=1e-3)

    def test_budget_of_one_evaluates_exactly_one_policy(self) -> None:
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=1, seed=3
        )
        assert result.achieved_pressure == 1
        assert len(result.trace) == 1

    def test_zero_pressure_fails_closed_with_guidance(self) -> None:
        optimizer = BudgetedSearchOptimizer()
        with pytest.raises(OptimizerError, match="reference policy"):
            optimizer.optimize(
                WarehouseGridworld(), reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=0, seed=1
            )

    def test_deterministic_across_calls(self) -> None:
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        first = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_HELD_OUT, pressure=600, seed=5
        )
        second = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_HELD_OUT, pressure=600, seed=5
        )
        assert first.fingerprint == second.fingerprint
        assert first.value == second.value
        assert first.trace == second.trace

    def test_best_so_far_is_monotone_along_restarts(self) -> None:
        env = WarehouseGridworld()
        optimizer = BudgetedSearchOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=3000, seed=42
        )
        best_values = [step.value for step in result.trace]
        assert best_values == sorted(best_values)

    def test_configuration_validation(self) -> None:
        with pytest.raises(OptimizerError):
            BudgetedSearchOptimizer(start="middle-of-nowhere")


class TestBonWidthOptimizer:
    """Selection-width pressure on the judge environment (closed form)."""

    def test_width_maps_to_pressure(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=4, seed=0
        )
        assert result.value == pytest.approx(0.820, abs=1e-3)
        assert result.optimizer_kind == "bon-width"
        assert result.stopped_early is False

    def test_pressure_zero_and_one_are_the_untuned_system(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        zero = optimizer.optimize(env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=0, seed=0)
        one = optimizer.optimize(env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=1, seed=0)
        assert zero.value == one.value == pytest.approx(0.470)

    def test_intended_selector_is_the_oracle_control(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        control = optimizer.optimize(
            env, reward_name=REWARD_INTENDED, arm=ARM_TUNING, pressure=8, seed=0
        )
        assert control.value == pytest.approx(0.954, abs=1e-3)

    def test_rejects_non_judge_environments(self) -> None:
        optimizer = BonWidthOptimizer()
        with pytest.raises(OptimizerError, match="judge-scored-answers"):
            optimizer.optimize(
                WarehouseGridworld(), reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=2, seed=0
            )

    def test_trace_has_start_and_final_rows(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        result = optimizer.optimize(
            env, reward_name=REWARD_PROXY, arm=ARM_TUNING, pressure=16, seed=0
        )
        assert len(result.trace) == 2
        assert result.trace[0].accepted is False
        assert result.trace[0].pressure == 0
        assert result.trace[1].pressure == 16


class TestSweepLadder:
    """The (arm x pressure) grid runner with fail-closed configuration."""

    def test_sweep_covers_every_cell(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        sweep = sweep_ladder(
            env,
            optimizer,
            reward_name=REWARD_PROXY,
            arms=(ARM_TUNING, ARM_HELD_OUT),
            pressures=(1, 4, 16),
            seed=42,
        )
        assert isinstance(sweep, LadderSweep)
        assert sweep.pressures == (1, 4, 16)
        assert sweep.arms == (ARM_TUNING, ARM_HELD_OUT)
        for arm in (ARM_TUNING, ARM_HELD_OUT):
            for pressure in (1, 4, 16):
                assert sweep.at(arm, pressure).requested_pressure == pressure

    def test_value_series_ordered_by_pressure(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        sweep = sweep_ladder(
            env,
            optimizer,
            reward_name=REWARD_PROXY,
            arms=(ARM_TUNING,),
            pressures=(1, 4, 16),
            seed=42,
        )
        series = sweep.value_series(ARM_TUNING)
        assert series[0] == pytest.approx(0.470)
        assert series[2] == pytest.approx(0.993, abs=1e-3)

    def test_missing_cell_fails_closed(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        sweep = sweep_ladder(
            env, optimizer, reward_name=REWARD_PROXY, arms=(ARM_TUNING,), pressures=(1, 4), seed=42
        )
        with pytest.raises(OptimizerError):
            sweep.at(ARM_TUNING, 16)

    def test_bad_arms_and_pressures_fail_closed(self) -> None:
        env = JudgeScoredAnswers()
        optimizer = BonWidthOptimizer()
        with pytest.raises(OptimizerError):
            sweep_ladder(
                env,
                optimizer,
                reward_name=REWARD_PROXY,
                arms=("deployment",),
                pressures=(1,),
                seed=42,
            )
        with pytest.raises(OptimizerError):
            sweep_ladder(
                env, optimizer, reward_name=REWARD_PROXY, arms=(ARM_TUNING,), pressures=(), seed=42
            )
        with pytest.raises(OptimizerError):
            sweep_ladder(env, optimizer, reward_name=REWARD_PROXY, arms=(), pressures=(1,), seed=42)
        with pytest.raises(OptimizerError):
            sweep_ladder(
                env,
                optimizer,
                reward_name=REWARD_PROXY,
                arms=(ARM_TUNING,),
                pressures=(4, 4),
                seed=42,
            )


class TestOptimizerFactory:
    """Config parsing: every regime reachable, unknowns rejected."""

    def test_local_search_from_config(self) -> None:
        optimizer = optimizer_from_config("local-search")
        assert isinstance(optimizer, LocalSearchOptimizer)
        assert optimizer.start == "reference"

    def test_budgeted_search_from_config(self) -> None:
        optimizer = optimizer_from_config({"kind": "budgeted-search", "start": "random"})
        assert isinstance(optimizer, BudgetedSearchOptimizer)
        assert optimizer.start == "random"

    def test_bon_width_from_config(self) -> None:
        optimizer = optimizer_from_config("bon-width")
        assert isinstance(optimizer, BonWidthOptimizer)

    @pytest.mark.parametrize(
        "bad",
        [
            "unknown-kind",
            {"kind": "local-search", "start": "middle"},
            {"kind": "budgeted-search", "nope": 1},
            {"kind": "bon-width", "extra": True},
            7,
            None,
        ],
    )
    def test_fail_closed_on_bad_configs(self, bad) -> None:
        with pytest.raises(OptimizerError):
            optimizer_from_config(bad)


class TestTraceStep:
    """Trace rows render deterministically."""

    def test_str_forms(self) -> None:
        start = TraceStep(pressure=0, fingerprint="seq:g11", value=1.0, accepted=False)
        step = TraceStep(pressure=3, fingerprint="seq:g11|g22", value=2.0)
        assert "start" in str(start)
        assert "step" in str(step)
        assert "alpha=3" in str(step)
