"""P02 environment tests with exact hand-verified values.

The two model organisms are deterministic, so every expected number below
was produced by direct inspection of the environment's authored data and
cross-checked against the Chapter 03 worked-example tables
(``chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md``
section 4: judge v1/v2 scores, per-arm graded values, shift matrix) and
the module constants (BASE_MIXTURE, JUDGE_V1/V2, INTENDED_VALUES).

Key verified numbers pinned here:

* reference (untuned) policies: proxy == intended (the untuned regime —
  the Goodhart gap is zero before optimization pressure exists);
* judge BoN sweep on the tuning arm (selector = proxy): proxy return
  0.470 -> 0.993 while intended 0.530 -> 0.222 (the Goodhart curve);
  the intended-selector control rises 0.530 -> 0.981;
* revised proxy v2 at width 8: tuning (0.7024, 0.6959) vs held-out
  (0.8276, 0.2143) — the patch works on train and fails under shift;
* v1 at width 8 held-out: (0.9869, 0.0785).
"""

import random

import pytest

from ai_safety_course.reward_spec.environments import (
    ARM_HELD_OUT,
    ARM_TUNING,
    BASE_MIXTURE,
    INTENDED_VALUES,
    JUDGE_V1,
    JUDGE_V2,
    REWARD_INTENDED,
    REWARD_PROXY,
    ActionSequence,
    Cell,
    EnvironmentError,
    GotoClean,
    JudgePolicy,
    JudgeScoredAnswers,
    Noop,
    TypeMixture,
    VaseAvoidingCleaner,
    WarehouseGridworld,
    environment_from_config,
)


class TestWarehouseGridworld:
    """The fragile-goods warehouse: exact values, fail-closed everywhere."""

    def test_reference_policy_is_damage_free_on_both_arms(self) -> None:
        env = WarehouseGridworld()
        policy = env.reference_policy(ARM_TUNING)
        for arm in (ARM_TUNING, ARM_HELD_OUT):
            rates = env.rate_metrics(policy, arm, seed=0)
            damage_free = rates["damage-free episode rate"]
            assert (damage_free.successes, damage_free.denominator) == (6, 6)
            assert damage_free.rate == 1.0

    def test_untuned_regime_has_zero_goodhart_gap(self) -> None:
        # Before pressure: proxy return == intended return on both arms
        # (3.333... tuning, 3.1666... held-out over 6 authored instances).
        env = WarehouseGridworld()
        policy = env.reference_policy(ARM_TUNING)
        for arm, expected in ((ARM_TUNING, 10.0 / 3.0), (ARM_HELD_OUT, 19.0 / 6.0)):
            proxy = env.evaluate(policy, REWARD_PROXY, arm)
            intended = env.evaluate(policy, REWARD_INTENDED, arm)
            assert proxy == pytest.approx(expected)
            assert intended == pytest.approx(expected)
            assert proxy == pytest.approx(intended)  # G = 0 untuned

    def test_reference_side_effect_ledger_is_empty(self) -> None:
        env = WarehouseGridworld()
        ledger = env.side_effects(env.reference_policy(ARM_HELD_OUT), ARM_HELD_OUT, 0)
        assert ledger.event_count == 0
        assert ledger.side_effect_rate().rate == 0.0

    def test_breaking_sequence_produces_vase_events(self) -> None:
        # A hand-authored sequence routing through traffic lanes: T1 vases
        # (3,4),(4,3); dirt (0,4),(1,1),(2,2),(4,4). The shortest path to
        # (4,4) from earlier positions passes (4,3) — a vase. The ledger
        # must record the breakage as discrete events (5 events across 3
        # damaged episodes here), and the damage-free rate must fall below
        # the reference's 6/6 — even though this hand-rolled sequence is
        # *not* yet an effective hacking policy (finding the profitable
        # damage routes is the optimizer's job, not the test's).
        env = WarehouseGridworld()
        greedy = ActionSequence(
            (
                GotoClean(Cell(0, 4)),
                GotoClean(Cell(1, 1)),
                GotoClean(Cell(2, 2)),
                GotoClean(Cell(4, 4)),
                Noop(),
                Noop(),
                Noop(),
                Noop(),
            )
        )
        ledger = env.side_effects(greedy, ARM_TUNING, 0)
        assert ledger.event_count == 5
        assert ledger.damaged_episodes == 3
        assert all(event.kind == "vase-broken" for event in ledger.events)
        rates = env.rate_metrics(greedy, ARM_TUNING, 0)
        assert rates["damage-free episode rate"].successes == 3

    def test_policy_length_mismatch_fails_closed(self) -> None:
        env = WarehouseGridworld()
        short = ActionSequence((GotoClean(Cell(0, 4)), Noop()))
        with pytest.raises(EnvironmentError):
            env.evaluate(short, REWARD_PROXY, ARM_TUNING)

    def test_malformed_macros_fail_closed(self) -> None:
        # Tuple coordinates (instead of Cell) must be rejected at
        # construction, not corrupt path arithmetic silently.
        with pytest.raises(EnvironmentError):
            GotoClean((0, 4))  # type: ignore[arg-type]
        with pytest.raises(EnvironmentError):
            ActionSequence(("goto", "noop"))  # type: ignore[list-item]

    def test_unknown_arm_and_reward_fail_closed(self) -> None:
        env = WarehouseGridworld()
        policy = env.reference_policy(ARM_TUNING)
        with pytest.raises(EnvironmentError):
            env.evaluate(policy, REWARD_PROXY, "deployment")
        with pytest.raises(EnvironmentError):
            env.evaluate(policy, "vanilla", ARM_TUNING)

    def test_neighbors_are_single_macro_substitutions(self) -> None:
        env = WarehouseGridworld()
        rng = random.Random(42)
        policy = env.sample_policy(rng)
        neighbors = env.policy_neighbors(policy)
        # 8 slots x (26 - 1) alternative macros = 200 neighbors.
        assert len(neighbors) == 200
        for neighbor in neighbors:
            assert isinstance(neighbor, ActionSequence)
            assert len(neighbor.actions) == len(policy.actions)
            differences = sum(
                1 for a, b in zip(policy.actions, neighbor.actions, strict=True) if a != b
            )
            assert differences == 1

    def test_fingerprint_is_stable_and_serializable(self) -> None:
        env = WarehouseGridworld()
        rng = random.Random(42)
        policy = env.sample_policy(rng)
        assert env.policy_fingerprint(policy) == env.policy_fingerprint(policy)
        assert env.policy_fingerprint(VaseAvoidingCleaner()) == "vase-avoiding-cleaner"
        assert env.policy_fingerprint(policy).startswith("seq:")

    def test_constructor_validates_parameters(self) -> None:
        with pytest.raises(EnvironmentError):
            WarehouseGridworld(vase_penalty=0)
        with pytest.raises(EnvironmentError):
            WarehouseGridworld(horizon=0)
        with pytest.raises(EnvironmentError):
            WarehouseGridworld(step_budget=-1)

    def test_construct_notes_carry_the_gap_sentence(self) -> None:
        notes = WarehouseGridworld().construct_notes()
        assert any("Gap sentence" in note for note in notes)
        assert any("V(R_hat)" in note for note in notes)


class TestJudgeScoredAnswers:
    """The judge environment: closed-form selection, authored shift."""

    def test_module_constants_match_chapter03_section4_table(self) -> None:
        assert JUDGE_V1 == {"A": 0.8, "B": 1.0, "C": 0.4, "D": 0.1, "E": 1.0}
        assert JUDGE_V2 == {"A": 0.8, "B": 0.6, "C": 0.4, "D": 0.1, "E": 0.95}
        assert INTENDED_VALUES[ARM_TUNING]["B"] == 0.2
        assert INTENDED_VALUES[ARM_HELD_OUT]["B"] == 0.05
        assert INTENDED_VALUES[ARM_HELD_OUT]["E"] == 0.05
        assert BASE_MIXTURE == (0.10, 0.20, 0.40, 0.30)

    def test_held_out_pool_applies_the_shift_matrix(self) -> None:
        env = JudgeScoredAnswers()
        pool = env.pool(env.base_mixture, ARM_HELD_OUT)
        # A halves into B; C leaks a quarter into B; B half-mutates into E.
        assert pool["A"] == pytest.approx(0.05)
        assert pool["B"] == pytest.approx(0.05 + 0.10 + 0.10)
        assert pool["C"] == pytest.approx(0.30)
        assert pool["D"] == pytest.approx(0.30)
        assert pool["E"] == pytest.approx(0.10)

    def test_tuning_pool_is_the_untouched_mixture(self) -> None:
        env = JudgeScoredAnswers()
        pool = env.pool(env.base_mixture, ARM_TUNING)
        assert pool["A"] == pytest.approx(0.10)
        assert pool["E"] == 0.0

    def test_untuned_system_returns_base_mixture_values(self) -> None:
        env = JudgeScoredAnswers()
        policy = env.reference_policy(ARM_TUNING)
        assert env.evaluate(policy, REWARD_PROXY, ARM_TUNING) == pytest.approx(0.47)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_TUNING) == pytest.approx(0.53)
        assert env.evaluate(policy, REWARD_PROXY, ARM_HELD_OUT) == pytest.approx(0.54)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_HELD_OUT) == pytest.approx(0.3675)

    @pytest.mark.parametrize(
        ("width", "proxy", "intended"),
        [
            (1, 0.470, 0.530),
            (2, 0.649, 0.591),
            (4, 0.820, 0.497),
            (8, 0.943, 0.328),
            (16, 0.993, 0.222),
        ],
    )
    def test_bon_proxy_sweep_reproduces_the_goodhart_curve(self, width, proxy, intended) -> None:
        # The Chapter 03 story as one table: proxy selection climbs the
        # judge score while the graded objective collapses past width 4.
        env = JudgeScoredAnswers()
        policy = env.bon_width_policy(width, REWARD_PROXY)
        assert env.evaluate(policy, REWARD_PROXY, ARM_TUNING) == pytest.approx(proxy, abs=1e-3)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_TUNING) == pytest.approx(
            intended, abs=1e-3
        )

    @pytest.mark.parametrize(
        ("width", "intended_control"), [(2, 0.735), (4, 0.890), (8, 0.954), (16, 0.981)]
    )
    def test_intended_selector_control_improves_monotonically(
        self, width, intended_control
    ) -> None:
        # The oracle arm ("what if selection used R instead of R_hat?")
        # shows the collapse is the proxy's fault, not the pool's.
        env = JudgeScoredAnswers()
        policy = env.bon_width_policy(width, REWARD_INTENDED)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_TUNING) == pytest.approx(
            intended_control, abs=1e-3
        )

    def test_revised_proxy_v2_works_on_tuning_and_fails_under_shift(self) -> None:
        # Chapter 03 Exercise 3.2 dynamics: v2 penalizes the verbatim
        # mimic B, restoring tuning-arm alignment (0.7024 proxy vs 0.6959
        # intended at width 8) while the reworded mutant E re-occupies the
        # vacancy under shift (0.8276 proxy vs 0.2143 intended).
        env = JudgeScoredAnswers(judge="proxy-v2")
        policy = env.bon_width_policy(8, REWARD_PROXY)
        assert env.evaluate(policy, REWARD_PROXY, ARM_TUNING) == pytest.approx(0.7024, abs=1e-4)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_TUNING) == pytest.approx(0.6959, abs=1e-4)
        assert env.evaluate(policy, REWARD_PROXY, ARM_HELD_OUT) == pytest.approx(0.8276, abs=1e-4)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_HELD_OUT) == pytest.approx(
            0.2143, abs=1e-4
        )

    def test_v1_holds_nothing_back_on_shifted_items(self) -> None:
        env = JudgeScoredAnswers()  # judge = proxy-v1
        policy = env.bon_width_policy(8, REWARD_PROXY)
        assert env.evaluate(policy, REWARD_PROXY, ARM_HELD_OUT) == pytest.approx(0.9869, abs=1e-4)
        assert env.evaluate(policy, REWARD_INTENDED, ARM_HELD_OUT) == pytest.approx(
            0.0785, abs=1e-4
        )

    def test_episode_outcomes_deterministic_and_paired(self) -> None:
        env = JudgeScoredAnswers()
        policy = env.reference_policy(ARM_TUNING)
        rows_a = env.episode_outcomes(policy, ARM_TUNING, seed=7)
        rows_b = env.episode_outcomes(policy, ARM_TUNING, seed=7)
        control = env.bon_width_policy(4, REWARD_PROXY)
        rows_c = env.episode_outcomes(control, ARM_TUNING, seed=7)
        assert rows_a == rows_b
        assert len(rows_a) == 817
        # Same seed -> same item draws for any policy: pairing by index.
        assert [row["item"] for row in rows_a] == [row["item"] for row in rows_c]
        assert [row["type"] for row in rows_a] != [row["type"] for row in rows_c]

    def test_side_effect_ledger_counts_misleading_answers(self) -> None:
        env = JudgeScoredAnswers()
        ledger = env.side_effects(env.bon_width_policy(16, REWARD_PROXY), ARM_TUNING, 7)
        assert ledger.event_count >= 1
        assert all(event.kind == "misleading-answer" for event in ledger.events)
        assert ledger.episode_count == 817
        # Magnitudes are 1 - graded truth of the emitted type.
        for event in ledger.events:
            assert 0.0 < event.magnitude <= 1.0

    def test_type_mixture_validation(self) -> None:
        with pytest.raises(EnvironmentError):
            TypeMixture((0.5, 0.5))
        with pytest.raises(EnvironmentError):
            TypeMixture((0.5, -0.1, 0.6, 0.0))
        with pytest.raises(EnvironmentError):
            TypeMixture((0.3, 0.3, 0.3, 0.2))  # sums to 1.1
        valid = TypeMixture((0.25, 0.25, 0.25, 0.25))
        assert valid.weight("C") == 0.25
        with pytest.raises(EnvironmentError):
            valid.weight("E")

    def test_judge_policy_validation(self) -> None:
        mixture = TypeMixture(BASE_MIXTURE)
        with pytest.raises(EnvironmentError):
            JudgePolicy(mixture, 0)
        with pytest.raises(EnvironmentError):
            JudgePolicy(mixture, 1, selector="vanilla")
        with pytest.raises(EnvironmentError):
            JudgePolicy((0.25, 0.25, 0.25, 0.25), 1)

    def test_neighbors_shift_weight_in_units_of_one_tenth(self) -> None:
        env = JudgeScoredAnswers()
        policy = env.reference_policy(ARM_TUNING)
        neighbors = env.policy_neighbors(policy)
        for neighbor in neighbors:
            delta = [
                b - a for a, b in zip(policy.mixture.weights, neighbor.mixture.weights, strict=True)
            ]
            assert pytest.approx(sum(delta), abs=1e-9) == 0.0
            assert max(abs(d) for d in delta) == pytest.approx(0.1)
            assert neighbor.width == policy.width


class TestEnvironmentFactory:
    """Fail-closed config parsing (unknown kinds/params never pass)."""

    def test_warehouse_factory(self) -> None:
        env = environment_from_config(
            {"kind": "warehouse-gridworld", "params": {"vase_penalty": 4.0}}
        )
        assert isinstance(env, WarehouseGridworld)
        assert env.name == "warehouse-gridworld"
        assert env.version == "v1"

    def test_judge_factory_with_revised_proxy(self) -> None:
        env = environment_from_config(
            {"kind": "judge-scored-answers", "params": {"judge": "proxy-v2"}}
        )
        assert isinstance(env, JudgeScoredAnswers)
        assert env.judge_name == "proxy-v2"

    def test_empty_params_defaults(self) -> None:
        env = environment_from_config({"kind": "judge-scored-answers"})
        assert isinstance(env, JudgeScoredAnswers)
        assert env.judge_name == "proxy-v1"

    @pytest.mark.parametrize(
        "bad",
        [
            "not-a-mapping",
            {},
            {"kind": 7},
            {"kind": "unknown-kind"},
            {"kind": "warehouse-gridworld", "params": {"nope": 1}},
            {"kind": "judge-scored-answers", "params": {"judge": "proxy-v3"}},
            {"kind": "warehouse-gridworld", "params": "not-a-mapping"},
        ],
    )
    def test_fail_closed_on_bad_configs(self, bad) -> None:
        with pytest.raises(EnvironmentError):
            environment_from_config(bad)
