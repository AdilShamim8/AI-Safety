"""runner — config-driven, resumable, fail-closed P03 calibration runner.

Turns one YAML configuration into a complete, dated calibration and
selective-prediction record. Design contracts (mirroring the P01/P02
runner discipline, each test-enforced):

* **Config-driven**: one YAML file names the case set, the instruments
  to evaluate, the calibrators to fit, the split policy, the binning,
  and the abstention thresholds. The same config reproduces the same
  outputs byte-for-byte.
* **Deterministic**: the validation/evaluation split is round-robin by
  case order (even indices validation, odd indices evaluation — no
  seed, no shuffle, stated in every report); ties in rankings break by
  case index; no wall-clock value enters the serialized outputs.
* **Validation-only fits**: every calibrator is fit on the validation
  split and applied to the evaluation split — the fit-once state
  machine enforces it, and the report carries each map's parameters.
* **Fail-closed**: unknown config keys, unknown instruments or
  calibrators, schema mismatches, and non-positive splits abort with
  explicit errors.

For every (instrument, calibrator) pair the runner produces: the
evaluation-split reliability table with per-bin counts and Wilson
intervals, ECE with its binning stated, Brier, clipped log loss, the
mean gap, the full risk-coverage summary (AURC, oracle AURC, gap,
full-coverage risk), and threshold policies at the configured taus
with both sides of the abstention ledger. The report renders it all
with a provenance block (case-set checksum, config fingerprint, code
version, run date).

CLI: ``PYTHONPATH=src python -m ai_safety_course.calibration.runner
<config.yaml>`` (writes state.json, results.json, report.md under the
config's output_dir).
"""

import json
import platform
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from ai_safety_course import __version__ as CODE_VERSION
from ai_safety_course.calibration.calibrators import (
    _BaseCalibrator,
    calibrator_from_config,
)
from ai_safety_course.calibration.cases import (
    CalibrationCaseError,
    CalibrationCaseSet,
    load_case_set,
)
from ai_safety_course.calibration.metrics import (
    CalibrationError,
    brier_score,
    log_loss,
    mean_gap,
    reliability_table,
)
from ai_safety_course.calibration.selection import (
    aurc_gap,
    oracle_aurc,
    risk_coverage_curve,
    threshold_policy,
)

#: The results schema identifier (versioned; readers fail closed).
RESULTS_SCHEMA = "p03-results-v1"
STATE_SCHEMA = "p03-state-v1"

#: Keys accepted at the top level of a run configuration.
CONFIG_KEYS = frozenset(
    {
        "run_id",
        "project",
        "cases_path",
        "instruments",
        "calibrators",
        "num_bins",
        "thresholds",
        "run_date",
        "output_dir",
        "status_note",
    }
)


class RunnerError(ValueError):
    """Raised on any fail-closed runner condition."""


@dataclass(frozen=True)
class P03Config:
    """A validated P03 experiment configuration."""

    run_id: str
    project: str
    cases_path: str
    instruments: tuple[str, ...]
    calibrators: tuple[Mapping[str, Any], ...]
    num_bins: int
    thresholds: tuple[float, ...]
    run_date: str
    output_dir: str
    status_note: str

    def config_sha256(self) -> str:
        """A stable fingerprint of the semantic configuration."""
        import hashlib

        payload = json.dumps(
            {
                "run_id": self.run_id,
                "project": self.project,
                "cases_path": self.cases_path,
                "instruments": list(self.instruments),
                "calibrators": [dict(c) for c in self.calibrators],
                "num_bins": self.num_bins,
                "thresholds": list(self.thresholds),
                "run_date": self.run_date,
                "status_note": self.status_note,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_config(config: Mapping[str, Any]) -> P03Config:
    """Validate a raw mapping into a :class:`P03Config` (fail-closed)."""
    if not isinstance(config, Mapping):
        raise RunnerError(f"config must be a mapping, got {type(config).__name__}")
    unknown = set(config) - CONFIG_KEYS
    if unknown:
        raise RunnerError(f"unknown config keys: {sorted(unknown)}")

    def required(key: str) -> Any:
        if key not in config:
            raise RunnerError(f"config: missing required key {key!r}")
        return config[key]

    run_id = required("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise RunnerError(f"run_id must be a non-empty string, got {run_id!r}")
    project = required("project")
    if not isinstance(project, str) or not project.strip():
        raise RunnerError(f"project must be a non-empty string, got {project!r}")
    cases_path = required("cases_path")
    if not isinstance(cases_path, str) or not cases_path.strip():
        raise RunnerError("cases_path must be a non-empty string")
    instruments = required("instruments")
    if (
        not isinstance(instruments, Sequence)
        or isinstance(instruments, (str, bytes))
        or not instruments
    ):
        raise RunnerError("instruments must be a non-empty list of strings")
    instrument_list = []
    for name in instruments:
        if not isinstance(name, str) or not name.strip():
            raise RunnerError(f"instrument names must be strings, got {name!r}")
        instrument_list.append(name)
    if len(set(instrument_list)) != len(instrument_list):
        raise RunnerError("instruments must not repeat")
    calibrators = required("calibrators")
    if (
        not isinstance(calibrators, Sequence)
        or isinstance(calibrators, (str, bytes))
        or not calibrators
    ):
        raise RunnerError("calibrators must be a non-empty list")
    calibrator_list = []
    for entry in calibrators:
        if isinstance(entry, str):
            calibrator_list.append({"kind": entry})
        elif isinstance(entry, Mapping):
            calibrator_list.append(dict(entry))
        else:
            raise RunnerError(f"calibrator entries must be strings or mappings, got {entry!r}")
    num_bins = required("num_bins")
    if not isinstance(num_bins, int) or isinstance(num_bins, bool) or num_bins < 1:
        raise RunnerError(f"num_bins must be an int >= 1, got {num_bins!r}")
    thresholds = required("thresholds")
    if (
        not isinstance(thresholds, Sequence)
        or isinstance(thresholds, (str, bytes))
        or not thresholds
    ):
        raise RunnerError("thresholds must be a non-empty list of floats")
    threshold_list = []
    for tau in thresholds:
        if not isinstance(tau, (int, float)) or isinstance(tau, bool):
            raise RunnerError(f"thresholds must be numbers, got {tau!r}")
        if not 0.0 <= float(tau) <= 1.0:
            raise RunnerError(f"thresholds must be in [0, 1], got {tau!r}")
        threshold_list.append(float(tau))
    if sorted(set(threshold_list)) != sorted(threshold_list):
        raise RunnerError("thresholds must not repeat")
    run_date = required("run_date")
    try:
        parsed_date = date.fromisoformat(str(run_date))
    except ValueError as exc:
        raise RunnerError(f"run_date must be ISO format, got {run_date!r}") from exc
    output_dir = required("output_dir")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise RunnerError("output_dir must be a non-empty string")
    status_note = config.get("status_note", "")
    if not isinstance(status_note, str):
        raise RunnerError("status_note must be a string")
    return P03Config(
        run_id=run_id,
        project=project,
        cases_path=cases_path,
        instruments=tuple(instrument_list),
        calibrators=tuple(calibrator_list),
        num_bins=num_bins,
        thresholds=tuple(sorted(threshold_list)),
        run_date=parsed_date.isoformat(),
        output_dir=output_dir,
        status_note=status_note,
    )


@dataclass(frozen=True)
class InstrumentResult:
    """One (instrument, calibrator) evaluation on the evaluation split."""

    instrument: str
    calibrator_kind: str
    fit_report: str
    validation_count: int
    evaluation_count: int
    ece: float
    bin_counts: tuple[int, ...]
    reliability_rows: tuple[tuple[float, float, int, float, float, float, float], ...]
    brier: float
    log_loss_value: float
    mean_gap_value: float
    aurc: float
    oracle_aurc: float
    aurc_gap_value: float
    full_coverage_risk: float
    thresholds: tuple[dict[str, Any], ...]


def _evaluate_pair(
    case_set: CalibrationCaseSet,
    instrument: str,
    calibrator_config: Mapping[str, Any],
    *,
    num_bins: int,
    thresholds: Sequence[float],
    validation_indices: Sequence[int],
    evaluation_indices: Sequence[int],
) -> InstrumentResult:
    """Fit one calibrator on validation; evaluate on the evaluation split."""
    calibrator: _BaseCalibrator = calibrator_from_config(dict(calibrator_config))
    val_scores_all = case_set.instrument_scores(instrument)
    outcomes_all = case_set.outcomes()
    validation_scores = [val_scores_all[i] for i in validation_indices]
    validation_outcomes = [outcomes_all[i] for i in validation_indices]
    evaluation_scores = [val_scores_all[i] for i in evaluation_indices]
    evaluation_outcomes = [outcomes_all[i] for i in evaluation_indices]
    calibrator.fit(validation_scores, validation_outcomes)
    transformed = list(calibrator.transform(evaluation_scores))
    table = reliability_table(transformed, evaluation_outcomes, num_bins=num_bins)
    curve = risk_coverage_curve(transformed, evaluation_outcomes)
    threshold_rows = []
    for tau in thresholds:
        policy = threshold_policy(transformed, evaluation_outcomes, tau)
        threshold_rows.append(
            {
                "tau": tau,
                "answered": policy.answered,
                "coverage": policy.coverage,
                "errors": policy.errors,
                "selective_risk": policy.selective_risk if policy.answered else None,
                "false_abstentions": policy.false_abstentions,
                "false_abstention_rate": policy.false_abstention_rate,
            }
        )
    return InstrumentResult(
        instrument=instrument,
        calibrator_kind=str(calibrator_config.get("kind", calibrator_config)),
        fit_report=calibrator.fit_report(),
        validation_count=len(validation_indices),
        evaluation_count=len(evaluation_indices),
        ece=table.ece,
        bin_counts=table.bin_counts,
        reliability_rows=tuple(
            (
                bin_.lower,
                bin_.upper,
                bin_.count,
                bin_.mean_confidence,
                bin_.accuracy,
                bin_.accuracy_interval[0],
                bin_.accuracy_interval[1],
            )
            for bin_ in table.bins
        ),
        brier=brier_score(transformed, evaluation_outcomes),
        log_loss_value=log_loss(transformed, evaluation_outcomes),
        mean_gap_value=mean_gap(transformed, evaluation_outcomes),
        aurc=curve.aurc,
        oracle_aurc=oracle_aurc(evaluation_outcomes),
        aurc_gap_value=aurc_gap(transformed, evaluation_outcomes),
        full_coverage_risk=curve.full_coverage_risk,
        thresholds=tuple(threshold_rows),
    )


@dataclass
class RunResult:
    """The complete, deterministic record of one P03 run."""

    config: P03Config
    case_set: CalibrationCaseSet
    results: list[InstrumentResult]
    validation_indices: tuple[int, ...]
    evaluation_indices: tuple[int, ...]

    def provenance(self) -> dict[str, Any]:
        return {
            "schema": RESULTS_SCHEMA,
            "run_id": self.config.run_id,
            "project": self.config.project,
            "config_sha256": self.config.config_sha256(),
            "case_set": self.case_set.name,
            "case_set_version": self.case_set.version,
            "case_set_sha256": self.case_set.sha256,
            "num_bins": self.config.num_bins,
            "instruments": list(self.config.instruments),
            "split": "round-robin by case order (even validation, odd evaluation)",
            "code_version": CODE_VERSION,
            "python_version": platform.python_version(),
            "run_date": self.config.run_date,
            "status_note": self.config.status_note,
        }

    def to_json_dict(self) -> dict[str, Any]:
        """The full deterministic record (results.json payload)."""
        return {
            "provenance": self.provenance(),
            "validation_indices": list(self.validation_indices),
            "evaluation_indices": list(self.evaluation_indices),
            "results": [
                {
                    "instrument": r.instrument,
                    "calibrator": r.calibrator_kind,
                    "fit_report": r.fit_report,
                    "validation_count": r.validation_count,
                    "evaluation_count": r.evaluation_count,
                    "ece": r.ece,
                    "bin_counts": list(r.bin_counts),
                    "brier": r.brier,
                    "log_loss": r.log_loss_value,
                    "mean_gap": r.mean_gap_value,
                    "aurc": r.aurc,
                    "oracle_aurc": r.oracle_aurc,
                    "aurc_gap": r.aurc_gap_value,
                    "full_coverage_risk": r.full_coverage_risk,
                    "thresholds": [dict(t) for t in r.thresholds],
                }
                for r in self.results
            ],
        }


def run_experiment(config: P03Config, *, output_dir: Path | None = None) -> RunResult:
    """Execute the full calibration experiment (deterministic)."""
    cases_path = Path(config.cases_path)
    if not cases_path.exists():
        raise RunnerError(f"cases file not found: {cases_path}")
    try:
        case_set = load_case_set(cases_path)
    except CalibrationCaseError as exc:
        raise RunnerError(f"case set rejected: {exc}") from exc
    for instrument in config.instruments:
        if instrument not in case_set.instruments:
            raise RunnerError(
                f"instrument {instrument!r} not in case set "
                f"(available: {list(case_set.instruments)})"
            )
    total = len(case_set.cases)
    if total < 4:
        raise RunnerError("case set too small to split (need >= 4 cases)")
    validation_indices = tuple(range(0, total, 2))
    evaluation_indices = tuple(range(1, total, 2))
    if not validation_indices or not evaluation_indices:
        raise RunnerError("split produced an empty side; need >= 4 cases")
    directory = output_dir if output_dir is not None else Path(config.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    results: list[InstrumentResult] = []
    for instrument in config.instruments:
        for calibrator_config in config.calibrators:
            try:
                results.append(
                    _evaluate_pair(
                        case_set,
                        instrument,
                        calibrator_config,
                        num_bins=config.num_bins,
                        thresholds=config.thresholds,
                        validation_indices=validation_indices,
                        evaluation_indices=evaluation_indices,
                    )
                )
            except CalibrationError as exc:
                raise RunnerError(
                    f"pair ({instrument}, {calibrator_config}) rejected: {exc}"
                ) from exc
    return RunResult(
        config=config,
        case_set=case_set,
        results=results,
        validation_indices=validation_indices,
        evaluation_indices=evaluation_indices,
    )


def write_results(result: RunResult, output_dir: Path) -> Path:
    """Write results.json (deterministic serialization)."""
    path = output_dir / "results.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(result.to_json_dict(), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)
    return path


def load_config_file(path: Path) -> P03Config:
    """Load and validate a YAML configuration file."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RunnerError(f"invalid YAML in {path}: {exc}") from exc
    return parse_config(raw if raw is not None else {})


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: ``python -m ai_safety_course.calibration.runner``."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(
            "usage: python -m ai_safety_course.calibration.runner <config.yaml>",
            file=sys.stderr,
        )
        return 2
    from ai_safety_course.calibration.report import write_report

    try:
        config = load_config_file(Path(args[0]))
        output_dir = Path(config.output_dir)
        result = run_experiment(config, output_dir=output_dir)
        results_path = write_results(result, output_dir)
        report_path = write_report(result, output_dir)
    except (RunnerError, CalibrationError, CalibrationCaseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    pairs = ", ".join(f"{r.instrument}/{r.calibrator_kind}" for r in result.results)
    print(f"pairs: {len(result.results)} ({pairs})")
    print(f"results: {results_path}")
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
