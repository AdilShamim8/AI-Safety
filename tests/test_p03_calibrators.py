"""P03 calibrator and case-set tests: the validation-only discipline.

Pinned behaviors (deterministic, hand-verified):

* Platt on the 8-item validation split (scores .95..0.25, outcomes
  1,1,0,1,0,1,0,0) converges to a=5.9408, b=-3.5645 — and makes the
  *evaluation* Brier worse (0.2382 vs identity 0.2300): the honest
  small-n overfitting the discipline exists to expose;
* Histogram (K=5) on the same split maps to bin accuracies
  (0.5, 0.0, 0.5, 0.5, 1.0) with the documented empty-bin fallback,
  and is worse still (0.375);
* fit-once-then-frozen state machine: refit raises, transform-before-
  fit raises;
* case sets: schema, checksum, duplicate-id, and field validation all
  fail closed.
"""

from pathlib import Path

import pytest
import yaml

from ai_safety_course.calibration.calibrators import (
    HistogramCalibrator,
    IdentityCalibrator,
    PlattCalibrator,
    calibrator_from_config,
)
from ai_safety_course.calibration.cases import (
    CASES_SCHEMA,
    CalibrationCaseError,
    CalibrationCaseSet,
    load_case_set,
)
from ai_safety_course.calibration.metrics import CalibrationError, brier_score

VAL_SCORES = [0.95, 0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25]
VAL_OUTCOMES = [1, 1, 0, 1, 0, 1, 0, 0]
EVAL_SCORES = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
EVAL_OUTCOMES = [1, 0, 1, 1, 0, 0, 1, 0]


class TestIdentityCalibrator:
    def test_identity_is_the_baseline(self) -> None:
        calibrator = IdentityCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        assert calibrator.transform(EVAL_SCORES) == tuple(EVAL_SCORES)
        assert brier_score(EVAL_SCORES, EVAL_OUTCOMES) == pytest.approx(0.23)
        assert "identity" in calibrator.fit_report()


class TestPlattCalibrator:
    def test_newton_converges_to_pinned_parameters(self) -> None:
        calibrator = PlattCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        assert calibrator.a == pytest.approx(5.9408, abs=1e-3)
        assert calibrator.b == pytest.approx(-3.5645, abs=1e-3)

    def test_platt_can_make_things_worse_and_that_is_reported(self) -> None:
        # The honest small-n outcome: the fitted map beats nothing here.
        calibrator = PlattCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        transformed = calibrator.transform(EVAL_SCORES)
        assert brier_score(transformed, EVAL_OUTCOMES) == pytest.approx(0.2382, abs=1e-3)
        assert brier_score(transformed, EVAL_OUTCOMES) > brier_score(EVAL_SCORES, EVAL_OUTCOMES)

    def test_transform_is_deterministic_and_monotone(self) -> None:
        calibrator = PlattCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        first = calibrator.transform(EVAL_SCORES)
        second = calibrator.transform(EVAL_SCORES)
        assert first == second
        assert list(first) == sorted(first, reverse=True)  # a > 0: order preserved

    def test_fit_report_names_the_map(self) -> None:
        calibrator = PlattCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        report = calibrator.fit_report()
        assert "platt" in report
        assert "Newton" in report


class TestHistogramCalibrator:
    def test_bin_accuracies_and_fallback(self) -> None:
        calibrator = HistogramCalibrator(num_bins=5).fit(VAL_SCORES, VAL_OUTCOMES)
        # bin0 empty -> fallback 0.5; bins 1..4 as computed by hand.
        assert calibrator.bin_accuracies == (
            pytest.approx(0.5),
            pytest.approx(0.0),
            pytest.approx(0.5),
            pytest.approx(0.5),
            pytest.approx(1.0),
        )
        assert calibrator.fallback_accuracy == pytest.approx(0.5)

    def test_transform_maps_to_bin_accuracies(self) -> None:
        calibrator = HistogramCalibrator(num_bins=5).fit(VAL_SCORES, VAL_OUTCOMES)
        assert calibrator.transform(EVAL_SCORES) == (
            pytest.approx(1.0),
            pytest.approx(1.0),
            pytest.approx(0.5),
            pytest.approx(0.5),
            pytest.approx(0.5),
            pytest.approx(0.5),
            pytest.approx(0.0),
            pytest.approx(0.0),
        )

    def test_worst_brier_of_the_three_maps(self) -> None:
        calibrator = HistogramCalibrator(num_bins=5).fit(VAL_SCORES, VAL_OUTCOMES)
        transformed = calibrator.transform(EVAL_SCORES)
        assert brier_score(transformed, EVAL_OUTCOMES) == pytest.approx(0.375, abs=1e-3)


class TestFitOnceStateMachine:
    """The validation-only discipline enforced by the object itself."""

    def test_refit_raises(self) -> None:
        calibrator = PlattCalibrator().fit(VAL_SCORES, VAL_OUTCOMES)
        with pytest.raises(CalibrationError, match="never refit"):
            calibrator.fit(VAL_SCORES, VAL_OUTCOMES)

    def test_transform_before_fit_raises(self) -> None:
        with pytest.raises(CalibrationError, match="before fit"):
            PlattCalibrator().transform([0.5])

    def test_fit_report_before_fit_raises(self) -> None:
        with pytest.raises(CalibrationError):
            IdentityCalibrator().fit_report()

    def test_invalid_inputs_fail_closed(self) -> None:
        with pytest.raises(CalibrationError):
            PlattCalibrator().fit([0.5], [2])
        with pytest.raises(CalibrationError):
            PlattCalibrator().fit([1.5], [1])
        with pytest.raises(CalibrationError):
            IdentityCalibrator().fit([0.5], [1, 0])


class TestCalibratorFactory:
    def test_factory_kinds(self) -> None:
        assert isinstance(calibrator_from_config("identity"), IdentityCalibrator)
        assert isinstance(calibrator_from_config("platt"), PlattCalibrator)
        assert isinstance(
            calibrator_from_config({"kind": "histogram", "num_bins": 5}),
            HistogramCalibrator,
        )

    @pytest.mark.parametrize(
        "bad", ["nope", {"kind": "identity", "extra": 1}, {"kind": "platt", "x": 2}, 7]
    )
    def test_factory_fail_closed(self, bad: object) -> None:
        with pytest.raises(CalibrationError):
            calibrator_from_config(bad)


def _write_case_set(path: Path, cases: list[dict], **top: object) -> Path:
    payload = {
        "schema": CASES_SCHEMA,
        "version": "1.0.0",
        "name": "test-cases",
        "cases": cases,
        **top,
    }
    path.write_text(yaml.safe_dump(payload), encoding="utf-8")
    return path


VALID_CASE = {
    "id": "C-001",
    "category": "science",
    "expected_outcome": 1,
    "instrument_scores": {"instrument-a": 0.9, "instrument-b": 0.4},
}


class TestCaseSet:
    def test_valid_load_with_checksum(self, tmp_path: Path) -> None:
        path = _write_case_set(
            tmp_path / "cases.yaml",
            [VALID_CASE, {**VALID_CASE, "id": "C-002", "expected_outcome": 0}],
        )
        case_set = load_case_set(path)
        assert isinstance(case_set, CalibrationCaseSet)
        assert len(case_set.cases) == 2
        assert case_set.instruments == ("instrument-a", "instrument-b")
        assert len(case_set.sha256) == 64
        assert case_set.outcomes() == (1, 0)
        assert case_set.instrument_scores("instrument-a") == (0.9, 0.9)

    def test_case_score_fail_closed_on_unknown_instrument(self, tmp_path: Path) -> None:
        path = _write_case_set(tmp_path / "cases.yaml", [VALID_CASE])
        case_set = load_case_set(path)
        with pytest.raises(CalibrationCaseError, match="no score for instrument"):
            case_set.instrument_scores("instrument-c")

    @pytest.mark.parametrize(
        "mutation",
        [
            {"id": "C-001"},  # duplicate id
            {"expected_outcome": 2},
            {"expected_outcome": "1"},
            {"instrument_scores": {}},
            {"instrument_scores": {"a": 1.5}},
            {"instrument_scores": {"a": "high"}},
            {"category": ""},
            {"extra_field": 1},
        ],
    )
    def test_case_validation_fails_closed(self, tmp_path: Path, mutation: dict) -> None:
        broken = {**VALID_CASE, **mutation}
        if "extra_field" in mutation and "id" not in mutation:
            broken.pop("id", None)
            broken["id"] = "C-003"
        path = _write_case_set(tmp_path / "cases.yaml", [VALID_CASE, broken])
        with pytest.raises(CalibrationCaseError):
            load_case_set(path)

    def test_schema_version_fail_closed(self, tmp_path: Path) -> None:
        path = tmp_path / "cases.yaml"
        path.write_text(
            yaml.safe_dump(
                {"schema": "wrong/v1", "version": "1.0.0", "name": "x", "cases": [VALID_CASE]}
            ),
            encoding="utf-8",
        )
        with pytest.raises(CalibrationCaseError, match="schema"):
            load_case_set(path)

    def test_empty_cases_fail_closed(self, tmp_path: Path) -> None:
        path = _write_case_set(tmp_path / "cases.yaml", [])
        with pytest.raises(CalibrationCaseError):
            load_case_set(path)

    def test_missing_case_field_fail_closed(self, tmp_path: Path) -> None:
        incomplete = {k: v for k, v in VALID_CASE.items() if k != "category"}
        path = _write_case_set(tmp_path / "cases.yaml", [incomplete])
        with pytest.raises(CalibrationCaseError, match="missing"):
            load_case_set(path)
