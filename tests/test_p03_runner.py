"""P03 runner and report tests: determinism, fail-closed config, the split.

The fixture is the committed 60-item case set (checksum-pinned). Pinned
results (seed 20261022, round-robin split, K=10):

* the split is 30 validation / 30 evaluation (even/odd case order);
* well-calibrated/identity: Brier 0.1189, ECE 0.1127, AURC 0.1308 —
  below the full-coverage risk 0.4000 (the honest gate works);
* overconfident/identity: Brier 0.1637, ECE 0.1915 (the shift is
  visible), same AURC (a monotone map preserves ranking);
* inverted/identity: Brier 0.5609, ECE 0.5989, AURC 0.7178 — ABOVE
  the full-coverage risk 0.4000 (the inverted-signal signature: the
  gate is worse than answering everything);
* after Platt/histogram the inverted instrument's Brier falls to
  ~0.097/0.100 — the systematic inversion is correctable *on this
  distribution*, which the report's limitations section prices as
  same-distribution fit, not deployment robustness.
"""

import json
from pathlib import Path

import pytest
import yaml

from ai_safety_course.calibration.report import render_report, write_report
from ai_safety_course.calibration.runner import (
    RunnerError,
    load_config_file,
    parse_config,
    run_experiment,
    write_results,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES = (
    REPO_ROOT
    / "projects/p03-calibration-truthfulness-and-abstention/cases/calibration-cases-v1.yaml"
)

CONFIG = {
    "run_id": "test-run",
    "project": "P03",
    "cases_path": str(CASES),
    "instruments": ["well-calibrated-v1", "overconfident-v1", "inverted-v1"],
    "calibrators": ["identity", "platt", {"kind": "histogram", "num_bins": 5}],
    "num_bins": 10,
    "thresholds": [0.5, 0.9],
    "run_date": "2026-10-22",
    "output_dir": "runs/test-p03",
    "status_note": "test",
}


class TestConfigParsing:
    def test_valid_config(self) -> None:
        config = parse_config(CONFIG)
        assert config.num_bins == 10
        assert config.instruments == (
            "well-calibrated-v1",
            "overconfident-v1",
            "inverted-v1",
        )
        assert config.calibrators == (
            {"kind": "identity"},
            {"kind": "platt"},
            {"kind": "histogram", "num_bins": 5},
        )
        assert config.thresholds == (0.5, 0.9)
        assert len(config.config_sha256()) == 64

    @pytest.mark.parametrize(
        "mutation",
        [
            {"unknown": 1},
            {"run_id": ""},
            {"instruments": []},
            {"instruments": "all"},
            {"instruments": ["a", "a"]},
            {"calibrators": []},
            {"calibrators": 5},
            {"num_bins": 0},
            {"thresholds": [1.5]},
            {"thresholds": [0.5, 0.5]},
            {"run_date": "yesterday"},
            {"output_dir": ""},
        ],
    )
    def test_fail_closed(self, mutation: dict) -> None:
        with pytest.raises(RunnerError):
            parse_config({**CONFIG, **mutation})

    def test_missing_keys(self) -> None:
        for key in ("run_id", "cases_path", "instruments", "num_bins"):
            incomplete = {k: v for k, v in CONFIG.items() if k != key}
            with pytest.raises(RunnerError):
                parse_config(incomplete)

    def test_load_config_file(self, tmp_path: Path) -> None:
        path = tmp_path / "config.yaml"
        path.write_text(yaml.safe_dump(CONFIG), encoding="utf-8")
        assert load_config_file(path).run_id == "test-run"


class TestRunExperiment:
    def test_split_is_round_robin(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        assert result.validation_indices == tuple(range(0, 60, 2))
        assert result.evaluation_indices == tuple(range(1, 60, 2))
        assert len(result.validation_indices) == 30
        assert len(result.evaluation_indices) == 30

    def test_nine_pairs_in_order(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        pairs = [(r.instrument, r.calibrator_kind) for r in result.results]
        assert pairs == [
            ("well-calibrated-v1", "identity"),
            ("well-calibrated-v1", "platt"),
            ("well-calibrated-v1", "histogram"),
            ("overconfident-v1", "identity"),
            ("overconfident-v1", "platt"),
            ("overconfident-v1", "histogram"),
            ("inverted-v1", "identity"),
            ("inverted-v1", "platt"),
            ("inverted-v1", "histogram"),
        ]

    def test_pinned_identity_results(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        by_pair = {(r.instrument, r.calibrator_kind): r for r in result.results}
        honest = by_pair[("well-calibrated-v1", "identity")]
        assert honest.brier == pytest.approx(0.1189, abs=1e-3)
        assert honest.ece == pytest.approx(0.1127, abs=1e-3)
        assert honest.aurc == pytest.approx(0.1308, abs=1e-3)
        assert honest.full_coverage_risk == pytest.approx(0.4)
        over = by_pair[("overconfident-v1", "identity")]
        assert over.brier == pytest.approx(0.1637, abs=1e-3)
        assert over.ece == pytest.approx(0.1915, abs=1e-3)
        assert over.aurc == pytest.approx(honest.aurc)  # monotone map

    def test_inverted_signal_signature(self, tmp_path: Path) -> None:
        # The chapter's headline fact, pinned on the fixture: gating on
        # the inverted signal is WORSE than answering everything.
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        by_pair = {(r.instrument, r.calibrator_kind): r for r in result.results}
        inverted = by_pair[("inverted-v1", "identity")]
        assert inverted.aurc == pytest.approx(0.7178, abs=1e-3)
        assert inverted.aurc > inverted.full_coverage_risk
        assert inverted.brier == pytest.approx(0.5609, abs=1e-3)

    def test_calibration_corrects_on_distribution(self, tmp_path: Path) -> None:
        # Platt/histogram recover the systematic inversion — on this
        # distribution. The report's limitations price exactly this.
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        by_pair = {(r.instrument, r.calibrator_kind): r for r in result.results}
        corrected = by_pair[("inverted-v1", "platt")]
        assert corrected.brier < by_pair[("inverted-v1", "identity")].brier
        assert corrected.aurc == pytest.approx(by_pair[("well-calibrated-v1", "platt")].aurc)

    def test_deterministic_results(self, tmp_path: Path) -> None:
        first = run_experiment(
            parse_config({**CONFIG, "output_dir": str(tmp_path / "a")}),
            output_dir=tmp_path / "a",
        )
        second = run_experiment(
            parse_config({**CONFIG, "output_dir": str(tmp_path / "b")}),
            output_dir=tmp_path / "b",
        )
        assert first.to_json_dict() == second.to_json_dict()
        write_results(first, tmp_path / "a")
        write_results(second, tmp_path / "b")
        assert (tmp_path / "a" / "results.json").read_bytes() == (
            tmp_path / "b" / "results.json"
        ).read_bytes()

    def test_unknown_instrument_rejected(self, tmp_path: Path) -> None:
        config = parse_config(
            {**CONFIG, "instruments": ["nonexistent"], "output_dir": str(tmp_path)}
        )
        with pytest.raises(RunnerError, match="not in case set"):
            run_experiment(config, output_dir=tmp_path)

    def test_missing_cases_file_rejected(self, tmp_path: Path) -> None:
        config = parse_config(
            {**CONFIG, "cases_path": str(tmp_path / "nope.yaml"), "output_dir": str(tmp_path)}
        )
        with pytest.raises(RunnerError, match="not found"):
            run_experiment(config, output_dir=tmp_path)

    def test_results_json_schema(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        path = write_results(result, tmp_path)
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record["provenance"]["schema"] == "p03-results-v1"
        assert record["provenance"]["case_set"] == "calibration-cases-v1"
        assert len(record["results"]) == 9
        assert record["results"][0]["thresholds"][0]["tau"] == 0.5


class TestReport:
    def test_report_contains_all_sections(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        report = render_report(result)
        for section in (
            "# P03 experiment report",
            "### Reliability table",
            "ECE = ",
            "### Selective prediction",
            "### Proper scores",
            "## Cross-pair comparison",
            "## Honest limitations",
            "## Provenance",
        ):
            assert section in report, f"missing: {section}"
        assert "round-robin" in report
        assert "fit on validation only" in report or "validation only" in report

    def test_report_deterministic(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        assert render_report(result) == render_report(result)

    def test_write_report(self, tmp_path: Path) -> None:
        config = parse_config({**CONFIG, "output_dir": str(tmp_path)})
        result = run_experiment(config, output_dir=tmp_path)
        path = write_report(result, tmp_path)
        assert path == tmp_path / "report.md"
        assert path.read_text(encoding="utf-8") == render_report(result)


class TestCli:
    def test_end_to_end(self, tmp_path: Path, capsys) -> None:
        from ai_safety_course.calibration.runner import main

        config_path = tmp_path / "config.yaml"
        config_path.write_text(
            yaml.safe_dump({**CONFIG, "output_dir": str(tmp_path / "out")}),
            encoding="utf-8",
        )
        assert main([str(config_path)]) == 0
        out = tmp_path / "out"
        assert (out / "results.json").exists()
        assert (out / "report.md").exists()
        captured = capsys.readouterr().out
        assert "pairs: 9" in captured

    def test_usage_and_config_errors(self, capsys) -> None:
        from ai_safety_course.calibration.runner import main

        assert main([]) == 2
        assert main(["a", "b"]) == 2
