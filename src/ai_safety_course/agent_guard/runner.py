"""runner — config-driven, deterministic P07 runs (CLI entry point).

Loads a privilege matrix, a scenario set, and a run configuration
(all YAML, all checksum-pinned), executes the paired arms, computes
the full metrics block, and writes a dated markdown report. The
runner is fail-closed: any schema, path, or coverage error aborts
before any result is produced. Determinism is total — no clocks in
the numbers (the run date comes from the config), no sampling, no
network, no model calls.

CLI::

    python -m ai_safety_course.agent_guard.runner --config <config.yaml>

The config names its matrix and scenario files relative to its own
directory, pins their expected checksums, and carries the
preregistered headline the report must match.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import yaml

from ai_safety_course import __version__ as CODE_VERSION
from ai_safety_course.agent_guard.harness import PairedRun, run_paired
from ai_safety_course.agent_guard.matrix import load_matrix
from ai_safety_course.agent_guard.metrics import P07Metrics, compute_metrics
from ai_safety_course.agent_guard.policy import CapabilityPolicy
from ai_safety_course.agent_guard.report import write_report
from ai_safety_course.agent_guard.scenarios import load_scenario_set

#: The only run-config schema version this runner understands.
RUN_CONFIG_SCHEMA = "p07-run-config/v1"


class RunnerError(ValueError):
    """Raised when a run configuration is invalid."""


@dataclass(frozen=True)
class RunConfig:
    """A validated P07 run configuration."""

    run_id: str
    project: str
    run_date: str
    matrix_path: Path
    scenarios_path: Path
    expected_matrix_checksum: str
    expected_scenarios_checksum: str
    status_note: str
    scenario_notes: dict[str, str]


@dataclass(frozen=True)
class RunResult:
    """Everything a report needs, nothing it does not."""

    config: RunConfig
    run: PairedRun
    metrics: P07Metrics
    matrix_name: str
    matrix_checksum: str
    scenarios_name: str
    scenarios_checksum: str
    config_fingerprint: str
    code_version: str
    scenario_notes: dict[str, str]


def _checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_run_config(path: Path) -> RunConfig:
    """Load and validate a run config (fail-closed, checksums pinned)."""
    data = yaml.safe_load(path.read_bytes())
    if not isinstance(data, Mapping):
        raise RunnerError(f"{path}: top level must be a mapping")
    if data.get("schema_version") != RUN_CONFIG_SCHEMA:
        raise RunnerError(f"schema_version {data.get('schema_version')!r} != {RUN_CONFIG_SCHEMA!r}")
    for f in (
        "run_id",
        "project",
        "run_date",
        "matrix",
        "scenarios",
        "expected_matrix_checksum",
        "expected_scenarios_checksum",
    ):
        if f not in data:
            raise RunnerError(f"{path}: missing field {f!r}")
    base = path.parent
    matrix_path = (base / str(data["matrix"])).resolve()
    scenarios_path = (base / str(data["scenarios"])).resolve()
    for p in (matrix_path, scenarios_path):
        if not p.is_file():
            raise RunnerError(f"{path}: referenced file does not exist: {p}")
    notes = {str(k): str(v) for k, v in (data.get("scenario_notes") or {}).items()}
    return RunConfig(
        run_id=str(data["run_id"]),
        project=str(data["project"]),
        run_date=str(data["run_date"]),
        matrix_path=matrix_path,
        scenarios_path=scenarios_path,
        expected_matrix_checksum=str(data["expected_matrix_checksum"]),
        expected_scenarios_checksum=str(data["expected_scenarios_checksum"]),
        status_note=str(data.get("status_note", "implemented")),
        scenario_notes=notes,
    )


def execute_run(config: RunConfig, report_dir: Path) -> RunResult:
    """Execute the paired run and write the report; returns the full result."""
    matrix_checksum = _checksum(config.matrix_path)
    scenarios_checksum = _checksum(config.scenarios_path)
    if matrix_checksum != config.expected_matrix_checksum:
        raise RunnerError(
            f"matrix checksum drift: expected {config.expected_matrix_checksum}, "
            f"got {matrix_checksum} ({config.matrix_path})"
        )
    if scenarios_checksum != config.expected_scenarios_checksum:
        raise RunnerError(
            f"scenario checksum drift: expected {config.expected_scenarios_checksum}, "
            f"got {scenarios_checksum} ({config.scenarios_path})"
        )

    matrix = load_matrix(config.matrix_path)
    scenario_set = load_scenario_set(config.scenarios_path)
    policy = CapabilityPolicy(matrix=matrix)
    run = run_paired(scenario_set.scenarios, policy)
    metrics = compute_metrics(run)

    config_fingerprint = hashlib.sha256(
        f"{config.run_id}|{matrix_checksum}|{scenarios_checksum}".encode()
    ).hexdigest()[:16]

    result = RunResult(
        config=config,
        run=run,
        metrics=metrics,
        matrix_name=config.matrix_path.name,
        matrix_checksum=matrix_checksum,
        scenarios_name=config.scenarios_path.name,
        scenarios_checksum=scenarios_checksum,
        config_fingerprint=config_fingerprint,
        code_version=CODE_VERSION,
        scenario_notes=config.scenario_notes,
    )
    report_dir.mkdir(parents=True, exist_ok=True)
    out_path = report_dir / f"{config.run_id}-report.md"
    write_report(result, out_path)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: ``--config <path>`` executes one preregistered run."""
    parser = argparse.ArgumentParser(prog="agent-guard-runner")
    parser.add_argument("--config", required=True, help="path to a P07 run config YAML")
    parser.add_argument(
        "--report-dir", default=None, help="output directory (default: alongside config)"
    )
    args = parser.parse_args(argv)

    config_path = Path(args.config).resolve()
    try:
        config = load_run_config(config_path)
        report_dir = (
            Path(args.report_dir).resolve()
            if args.report_dir
            else config_path.parent.parent / "runs"
        )
        result = execute_run(config, report_dir)
    except (RunnerError, ValueError) as exc:
        print(f"RUN FAILED: {exc}", file=sys.stderr)
        return 1
    print(result.metrics.headline())
    print(f"report: {report_dir / (config.run_id + '-report.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
