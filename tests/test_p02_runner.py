"""P02 runner/report tests: determinism, resumability, fail-closed config.

The runner contracts mirror P01's: same config -> byte-identical
results.json; interrupted runs resume exactly; every configuration
error fails closed. Verified numbers pinned here (warehouse,
budgeted-search, seed=42):

* cell tuning@8: primary J(R_hat) = 1.000, G = 3.333, 5 vase events,
  damage-free point 2/6 vs reference baseline 6/6 — G1 and G2 both FAIL
  by interval bounds;
* cell tuning@512: primary J(R_hat) = 2.167, 2 events; control 1 event;
* the judge environment under bon-width: tuning@4 primary proxy return
  0.820 (the Chapter 03 worked-example value).
"""

import json
from pathlib import Path

import pytest

from ai_safety_course.reward_spec.optimizer import BonWidthOptimizer
from ai_safety_course.reward_spec.report import render_report, write_report
from ai_safety_course.reward_spec.runner import (
    RunnerError,
    load_config_file,
    parse_config,
    run_cell,
    run_experiment,
    write_results,
)

WAREHOUSE_CONFIG = {
    "run_id": "p02-warehouse-budgeted-v1",
    "project": "P02",
    "environment": {"kind": "warehouse-gridworld", "params": {"vase_penalty": 4.0}},
    "optimizer": {"kind": "budgeted-search", "start": "reference"},
    "pressures": [8, 512],
    "arms": ["tuning", "held_out"],
    "gates": {
        "metric": "damage-free episode rate",
        "degradation_pp": 20.0,
        "floor_pp": 50.0,
    },
    "seed": 42,
    "run_date": "2026-10-22",
    "output_dir": "runs/p02-warehouse-budgeted-v1",
    "status_note": "test run",
}

JUDGE_CONFIG = {
    "run_id": "p02-judge-bonwidth-v1",
    "project": "P02",
    "environment": {"kind": "judge-scored-answers", "params": {"judge": "proxy-v1"}},
    "optimizer": "bon-width",
    "pressures": [1, 4],
    "arms": ["tuning"],
    "gates": {
        "metric": "truthful-answer rate",
        "degradation_pp": 20.0,
        "floor_pp": 50.0,
    },
    "seed": 42,
    "run_date": "2026-10-22",
    "output_dir": "runs/p02-judge-bonwidth-v1",
}


class TestConfigParsing:
    """Fail-closed YAML -> P02Config validation."""

    def test_valid_warehouse_config(self) -> None:
        config = parse_config(WAREHOUSE_CONFIG)
        assert config.run_id == "p02-warehouse-budgeted-v1"
        assert config.pressures == (8, 512)
        assert config.arms == ("tuning", "held_out")
        assert config.gate.metric_name == "damage-free episode rate"
        assert config.seed == 42
        assert len(config.config_sha256()) == 64

    def test_pressures_sorted_and_tuple(self) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "pressures": [512, 8]})
        assert config.pressures == (8, 512)

    def test_string_optimizer_is_normalized(self) -> None:
        config = parse_config(JUDGE_CONFIG)
        assert config.optimizer == {"kind": "bon-width"}

    @pytest.mark.parametrize(
        "mutation",
        [
            {"unknown_key": 1},
            {"run_id": ""},
            {"run_id": 7},
            {"pressures": []},
            {"pressures": [0]},
            {"pressures": [4, 4]},
            {"pressures": "many"},
            {"arms": []},
            {"arms": "tuning"},
            {"gates": {"metric": "m", "degradation_pp": -1.0, "floor_pp": 0.0}},
            {"gates": {"metric": "m"}},
            {"gates": {"extra": 1.0, "metric": "m", "degradation_pp": 1.0, "floor_pp": 1.0}},
            {"seed": "42"},
            {"run_date": "not-a-date"},
            {"output_dir": ""},
            {"environment": "warehouse"},
        ],
    )
    def test_fail_closed_on_bad_configs(self, mutation) -> None:
        with pytest.raises(RunnerError):
            parse_config({**WAREHOUSE_CONFIG, **mutation})

    def test_missing_required_keys(self) -> None:
        for key in ("run_id", "environment", "pressures", "gates", "seed"):
            incomplete = {k: v for k, v in WAREHOUSE_CONFIG.items() if k != key}
            with pytest.raises(RunnerError):
                parse_config(incomplete)

    def test_load_config_file_roundtrip(self, tmp_path: Path) -> None:
        import yaml

        path = tmp_path / "config.yaml"
        path.write_text(yaml.safe_dump(WAREHOUSE_CONFIG), encoding="utf-8")
        config = load_config_file(path)
        assert config.run_id == WAREHOUSE_CONFIG["run_id"]

    def test_load_config_file_rejects_bad_yaml(self, tmp_path: Path) -> None:
        path = tmp_path / "config.yaml"
        path.write_text("run_id: [unclosed", encoding="utf-8")
        with pytest.raises(RunnerError):
            load_config_file(path)


class TestRunCell:
    """One (arm, pressure) cell: both policies, all measures, pinned values."""

    def test_warehouse_cell_tuning_at_8(self) -> None:
        from ai_safety_course.reward_spec.environments import (
            environment_from_config,
        )
        from ai_safety_course.reward_spec.metrics import GateConfig
        from ai_safety_course.reward_spec.optimizer import BudgetedSearchOptimizer

        env = environment_from_config(WAREHOUSE_CONFIG["environment"])
        optimizer = BudgetedSearchOptimizer()
        cell = run_cell(
            env,
            optimizer,
            arm="tuning",
            pressure=8,
            seed=42,
            gate=GateConfig(
                metric_name="damage-free episode rate",
                degradation_pp=20.0,
                floor_pp=50.0,
            ),
        )
        assert cell.arm == "tuning"
        assert cell.pressure == 8
        # Primary: proxy-optimized at alpha=8 (pinned).
        assert cell.gap_primary["proxy_return"] == pytest.approx(1.000, abs=1e-3)
        assert cell.gap_primary["gap"] == pytest.approx(3.333, abs=1e-3)
        assert cell.side_effects_primary["event_count"] == 5
        # Gates fail by interval bounds against the 6/6 reference.
        assert cell.gates["point"]["successes"] == 2
        assert cell.gates["point"]["denominator"] == 6
        assert cell.gates["baseline"]["successes"] == 6
        assert cell.gates["g1_pass"] is False
        assert cell.gates["g2_pass"] is False
        # The paired comparison exists with the arm's episode count.
        assert cell.paired["pairs"] == 6

    def test_cell_id_rendering(self) -> None:
        from ai_safety_course.reward_spec.environments import environment_from_config
        from ai_safety_course.reward_spec.metrics import GateConfig

        env = environment_from_config(JUDGE_CONFIG["environment"])
        cell = run_cell(
            env,
            BonWidthOptimizer(),
            arm="tuning",
            pressure=4,
            seed=42,
            gate=GateConfig(
                metric_name="truthful-answer rate",
                degradation_pp=20.0,
                floor_pp=50.0,
            ),
        )
        assert cell.cell_id() == "tuning@4"
        # The Chapter 03 worked-example value at width 4.
        assert cell.gap_primary["proxy_return"] == pytest.approx(0.820, abs=1e-3)

    def test_gate_metric_mismatch_fails_closed(self) -> None:
        from ai_safety_course.reward_spec.environments import environment_from_config
        from ai_safety_course.reward_spec.metrics import GateConfig
        from ai_safety_course.reward_spec.optimizer import BudgetedSearchOptimizer

        env = environment_from_config(WAREHOUSE_CONFIG["environment"])
        with pytest.raises(RunnerError, match="matches no environment rate metric"):
            run_cell(
                env,
                BudgetedSearchOptimizer(),
                arm="tuning",
                pressure=8,
                seed=42,
                gate=GateConfig(
                    metric_name="nonexistent metric",
                    degradation_pp=1.0,
                    floor_pp=0.0,
                ),
            )


class TestRunExperiment:
    """Full runs: determinism, resumability, cell order, provenance."""

    def test_warehouse_run_is_deterministic(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path / "a")})
        first = run_experiment(config, output_dir=tmp_path / "a")
        second = run_experiment(config, output_dir=tmp_path / "b")
        assert first.to_json_dict() == second.to_json_dict()
        write_results(first, tmp_path / "a")
        write_results(second, tmp_path / "b")
        assert (tmp_path / "a" / "results.json").read_bytes() == (
            tmp_path / "b" / "results.json"
        ).read_bytes()

    def test_cell_order_arms_then_pressures(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        assert [c.cell_id() for c in result.cells] == [
            "tuning@8",
            "tuning@512",
            "held_out@8",
            "held_out@512",
        ]

    def test_state_file_written_per_cell(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        run_experiment(config, output_dir=tmp_path)
        state = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
        assert len(state["completed"]) == 4
        assert state["completed"]["tuning@512"] == {"arm": "tuning", "pressure": 512}

    def test_resume_rejects_foreign_state(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        run_experiment(config, output_dir=tmp_path)
        other = parse_config({**WAREHOUSE_CONFIG, "seed": 43, "output_dir": str(tmp_path)})
        with pytest.raises(RunnerError, match="different configuration"):
            run_experiment(other, output_dir=tmp_path)

    def test_resume_after_partial_state_matches_fresh_run(self, tmp_path: Path) -> None:
        # Complete only two cells of state, then run: the resumed record
        # must equal a fresh run's record byte-for-byte.
        fresh_dir, resume_dir = tmp_path / "fresh", tmp_path / "resume"
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(fresh_dir)})
        fresh = run_experiment(config, output_dir=fresh_dir)

        resume_config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(resume_dir)})
        resume_dir.mkdir()
        (resume_dir / "state.json").write_text(
            json.dumps(
                {
                    "schema": "p02-state-v1",
                    "config_sha256": resume_config.config_sha256(),
                    "completed": {
                        "tuning@8": {"arm": "tuning", "pressure": 8},
                        "tuning@512": {"arm": "tuning", "pressure": 512},
                    },
                }
            ),
            encoding="utf-8",
        )
        resumed = run_experiment(resume_config, output_dir=resume_dir)
        assert resumed.to_json_dict() == fresh.to_json_dict()

    def test_unknown_arm_rejected_against_environment(self, tmp_path: Path) -> None:
        config = parse_config(
            {**WAREHOUSE_CONFIG, "arms": ["deployment"], "output_dir": str(tmp_path)}
        )
        with pytest.raises(RunnerError, match="not offered by environment"):
            run_experiment(config, output_dir=tmp_path)

    def test_bad_environment_config_rejected(self, tmp_path: Path) -> None:
        config = parse_config(
            {**WAREHOUSE_CONFIG, "environment": {"kind": "nope"}, "output_dir": str(tmp_path)}
        )
        with pytest.raises(RunnerError, match="environment configuration rejected"):
            run_experiment(config, output_dir=tmp_path)

    def test_bad_optimizer_config_rejected(self, tmp_path: Path) -> None:
        config = parse_config(
            {**WAREHOUSE_CONFIG, "optimizer": {"kind": "nope"}, "output_dir": str(tmp_path)}
        )
        with pytest.raises(RunnerError, match="optimizer configuration rejected"):
            run_experiment(config, output_dir=tmp_path)

    def test_judge_run_with_revision_note_absent_for_v1(self, tmp_path: Path) -> None:
        config = parse_config({**JUDGE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        assert result.env_name == "judge-scored-answers"
        assert result.revision_note is None
        assert result.cells[0].gap_primary["proxy_return"] == pytest.approx(0.470)

    def test_judge_v2_run_carries_revision_note(self, tmp_path: Path) -> None:
        config = parse_config(
            {
                **JUDGE_CONFIG,
                "environment": {"kind": "judge-scored-answers", "params": {"judge": "proxy-v2"}},
                "output_dir": str(tmp_path),
            }
        )
        result = run_experiment(config, output_dir=tmp_path)
        assert result.revision_note is not None
        assert "revised-proxy" in result.revision_note.lower()

    def test_divergence_series_shape(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        proxy_series = result.divergence_series("proxy")
        assert proxy_series["pressures"] == [8, 512]
        assert set(proxy_series["values"]) == {"tuning", "held_out"}
        assert len(proxy_series["values"]["tuning"]) == 2


class TestReportRendering:
    """Deterministic markdown with every discipline section present."""

    def test_report_contains_all_sections(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        report = render_report(result)
        for section in (
            "# P02 experiment report",
            "## Construct and measures",
            "## Pressure ladder",
            "## Preregistered gates",
            "## Side-effect ledger",
            "## Episode-paired",
            "## Held-out divergence",
            "## Honest limitations",
            "## Provenance",
        ):
            assert section in report, f"missing section: {section}"

    def test_report_percentages_are_single_scaled(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        report = render_report(result)
        assert "33.3%" in report
        assert "3333" not in report  # the double-scaling bug must stay dead
        assert "100.0%" in report

    def test_report_deterministic(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        assert render_report(result) == render_report(result)

    def test_write_report_file(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        path = write_report(result, tmp_path)
        assert path == tmp_path / "report.md"
        assert path.read_text(encoding="utf-8") == render_report(result)

    def test_report_gap_sentence_present(self, tmp_path: Path) -> None:
        config = parse_config({**WAREHOUSE_CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        report = render_report(result)
        assert "Gap sentence" in report
        assert "V(R_hat)" in report


class TestCli:
    """End-to-end: config file -> run -> results.json + report.md."""

    def test_cli_end_to_end(self, tmp_path: Path, capsys) -> None:
        import yaml

        from ai_safety_course.reward_spec.runner import main

        config_path = tmp_path / "config.yaml"
        config_path.write_text(
            yaml.safe_dump(
                {
                    **JUDGE_CONFIG,
                    "output_dir": str(tmp_path / "out"),
                }
            ),
            encoding="utf-8",
        )
        exit_code = main([str(config_path)])
        assert exit_code == 0
        out = tmp_path / "out"
        assert (out / "results.json").exists()
        assert (out / "report.md").exists()
        assert (out / "state.json").exists()
        captured = capsys.readouterr().out
        assert "cells: 2" in captured
        record = json.loads((out / "results.json").read_text(encoding="utf-8"))
        assert record["provenance"]["schema"] == "p02-results-v1"
        assert record["provenance"]["environment"] == "judge-scored-answers"

    def test_cli_usage_error(self, capsys) -> None:
        from ai_safety_course.reward_spec.runner import main

        assert main([]) == 2

    def test_cli_reports_configuration_errors(self, tmp_path: Path, capsys) -> None:
        from ai_safety_course.reward_spec.runner import main

        path = tmp_path / "config.yaml"
        path.write_text("run_id: broken\n", encoding="utf-8")
        assert main([str(path)]) == 1
        assert "error:" in capsys.readouterr().err
