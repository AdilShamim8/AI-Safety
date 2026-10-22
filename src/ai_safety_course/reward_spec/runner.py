"""runner — config-driven, resumable, fail-closed P02 experiment runner.

Turns one YAML configuration into a complete, dated optimization-pressure
experiment record. Design contracts (each test-enforced, mirroring the
P01 runner discipline):

* **Config-driven**: one YAML file names the environment, the optimizer,
  the pressure ladder, the arms, the preregistered gate, the seed, and
  the run date. The same config reproduces the same outputs
  byte-for-byte.
* **Deterministic**: every optimizer call is seeded from the config
  seed; no wall-clock value enters the serialized outputs; iteration
  order is (arm, pressure) with pressures ascending.
* **Resumable**: after every completed (arm, pressure) cell,
  ``<output_dir>/state.json`` is rewritten. An interrupted run resumes
  from that file and produces results identical to an uninterrupted run.
* **Fail-closed**: unknown config keys, unknown environment/optimizer
  kinds, gate metrics that match no environment rate metric, and
  mismatched resume state abort with explicit errors. The runner never
  silently skips a cell, never substitutes a default policy, and never
  mixes state across different configurations.

The experiment design (preregistered in the project README): at every
(arm, pressure) cell the runner optimizes **two** policies under
**matched** pressure — the *primary* under the proxy reward R_hat
(deployment realism) and the *control* under the intended objective R
(the Chapter 03 oracle arm) — then measures both on both rewards, the
side-effect ledger, the rate metrics with gates against the environment's
untuned reference policy, and an episode-paired primary-vs-control
comparison. The proxy/intended value series across the ladder form the
held-out divergence.

Outputs (written under ``output_dir``):

* ``state.json`` — resumability state (run identity + completed cells).
* ``results.json`` — the full, deterministic run record.
* ``report.md`` — written by the CLI entry point
  (``python -m ai_safety_course.reward_spec.runner <config.yaml>``).
"""

import json
import platform
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

from ai_safety_course import __version__ as CODE_VERSION
from ai_safety_course.reward_spec.environments import (
    REWARD_INTENDED,
    REWARD_PROXY,
    EnvironmentError,
    TaskEnvironment,
    environment_from_config,
)
from ai_safety_course.reward_spec.metrics import (
    GateConfig,
    GateOutcome,
    GoodhartGap,
    MetricsError,
    MetricSummary,
    PairedComparison,
    SideEffectLedger,
    evaluate_gates,
    goodhart_gap,
    rate_metric,
)
from ai_safety_course.reward_spec.optimizer import (
    OptimizationResult,
    OptimizerError,
    PressureOptimizer,
    optimizer_from_config,
)

#: The results/state schema identifier (versioned; readers fail closed
#: on unknown schemas).
RESULTS_SCHEMA = "p02-results-v1"
STATE_SCHEMA = "p02-state-v1"

#: Keys accepted at the top level of a run configuration.
CONFIG_KEYS = frozenset(
    {
        "run_id",
        "project",
        "environment",
        "optimizer",
        "pressures",
        "arms",
        "gates",
        "seed",
        "run_date",
        "output_dir",
        "status_note",
    }
)

#: Keys accepted inside a ``gates`` block.
GATE_KEYS = frozenset({"metric", "degradation_pp", "floor_pp"})


class RunnerError(ValueError):
    """Raised on any fail-closed runner condition (never papered over)."""


@dataclass(frozen=True)
class P02Config:
    """A validated P02 experiment configuration.

    Attributes:
        run_id: short identifier for the run (report header, filenames).
        project: project label (``"P02"``).
        environment: the environment config block (kind + params).
        optimizer: the optimizer config block (kind + params).
        pressures: the optimization-pressure ladder, ascending, >= 1.
        arms: the arms to sweep (subset of the environment's arms).
        gate: the preregistered gate (metric prefix, degradation, floor).
        seed: the master seed threaded into every optimizer call.
        run_date: the run date (from config; never wall-clock).
        output_dir: where state/results/report are written.
        status_note: honest one-line status qualifier for the report.
    """

    run_id: str
    project: str
    environment: Mapping[str, Any]
    optimizer: Mapping[str, Any]
    pressures: tuple[int, ...]
    arms: tuple[str, ...]
    gate: GateConfig
    seed: int
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
                "environment": dict(self.environment),
                "optimizer": dict(self.optimizer),
                "pressures": list(self.pressures),
                "arms": list(self.arms),
                "gates": {
                    "metric": self.gate.metric_name,
                    "degradation_pp": self.gate.degradation_pp,
                    "floor_pp": self.gate.floor_pp,
                },
                "seed": self.seed,
                "run_date": self.run_date,
                "status_note": self.status_note,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _require(config: Mapping[str, Any], key: str, context: str) -> Any:
    if key not in config:
        raise RunnerError(f"{context}: missing required key {key!r}")
    return config[key]


def parse_config(config: Mapping[str, Any]) -> P02Config:
    """Validate a raw mapping into a :class:`P02Config` (fail-closed)."""
    if not isinstance(config, Mapping):
        raise RunnerError(f"config must be a mapping, got {type(config).__name__}")
    unknown = set(config) - CONFIG_KEYS
    if unknown:
        raise RunnerError(f"unknown config keys: {sorted(unknown)}")
    run_id = _require(config, "run_id", "config")
    if not isinstance(run_id, str) or not run_id.strip():
        raise RunnerError(f"run_id must be a non-empty string, got {run_id!r}")
    project = _require(config, "project", "config")
    if not isinstance(project, str) or not project.strip():
        raise RunnerError(f"project must be a non-empty string, got {project!r}")
    environment = _require(config, "environment", "config")
    if not isinstance(environment, Mapping):
        raise RunnerError("environment config must be a mapping")
    optimizer = _require(config, "optimizer", "config")
    if isinstance(optimizer, str):
        optimizer = {"kind": optimizer}
    if not isinstance(optimizer, Mapping):
        raise RunnerError("optimizer config must be a string or mapping")
    pressures = _require(config, "pressures", "config")
    if not isinstance(pressures, Sequence) or isinstance(pressures, (str, bytes)):
        raise RunnerError("pressures must be a list of ints")
    ladder: list[int] = []
    for entry in pressures:
        if not isinstance(entry, int) or isinstance(entry, bool) or entry < 1:
            raise RunnerError(f"pressures must be ints >= 1, got {entry!r}")
        ladder.append(entry)
    if not ladder:
        raise RunnerError("pressures must be non-empty")
    if sorted(set(ladder)) != sorted(ladder):
        raise RunnerError("pressures must not repeat")
    ladder.sort()
    arms = _require(config, "arms", "config")
    if not isinstance(arms, Sequence) or isinstance(arms, (str, bytes)):
        raise RunnerError("arms must be a list of strings")
    arm_list = [arm for arm in arms if isinstance(arm, str)]
    if len(arm_list) != len(list(arms)):
        raise RunnerError("arms must be strings")
    if not arm_list:
        raise RunnerError("arms must be non-empty")
    gates_block = _require(config, "gates", "config")
    if not isinstance(gates_block, Mapping):
        raise RunnerError("gates config must be a mapping")
    unknown_gate = set(gates_block) - GATE_KEYS
    if unknown_gate:
        raise RunnerError(f"unknown gate keys: {sorted(unknown_gate)}")
    try:
        gate = GateConfig(
            metric_name=str(_require(gates_block, "metric", "gates")),
            degradation_pp=float(_require(gates_block, "degradation_pp", "gates")),
            floor_pp=float(_require(gates_block, "floor_pp", "gates")),
        )
        gate.validate()
    except (TypeError, ValueError) as exc:
        raise RunnerError(f"invalid gates block: {exc}") from exc
    seed = _require(config, "seed", "config")
    if not isinstance(seed, int) or isinstance(seed, bool):
        raise RunnerError(f"seed must be an int, got {seed!r}")
    run_date = _require(config, "run_date", "config")
    try:
        parsed_date = date.fromisoformat(str(run_date))
    except ValueError as exc:
        raise RunnerError(f"run_date must be ISO format, got {run_date!r}") from exc
    output_dir = _require(config, "output_dir", "config")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise RunnerError(f"output_dir must be a non-empty string, got {output_dir!r}")
    status_note = config.get("status_note", "")
    if not isinstance(status_note, str):
        raise RunnerError(f"status_note must be a string, got {status_note!r}")
    return P02Config(
        run_id=run_id,
        project=project,
        environment=dict(environment),
        optimizer=dict(optimizer),
        pressures=tuple(ladder),
        arms=tuple(arm_list),
        gate=gate,
        seed=seed,
        run_date=parsed_date.isoformat(),
        output_dir=output_dir,
        status_note=status_note,
    )


@dataclass(frozen=True)
class CellRecord:
    """One (arm, pressure) cell of the experiment.

    Everything downstream (report, gates, divergence) reads from this
    record; nothing is recomputed after the cell completes.
    """

    arm: str
    pressure: int
    primary: dict[str, Any]
    control: dict[str, Any]
    gap_primary: dict[str, float]
    gap_control: dict[str, float]
    gates: dict[str, Any]
    side_effects_primary: dict[str, Any]
    side_effects_control: dict[str, Any]
    paired: dict[str, Any]
    reference: dict[str, Any]

    def cell_id(self) -> str:
        return f"{self.arm}@{self.pressure}"


def _optimization_dict(result: OptimizationResult) -> dict[str, Any]:
    return {
        "fingerprint": result.fingerprint,
        "reward_name": result.reward_name,
        "arm": result.arm,
        "requested_pressure": result.requested_pressure,
        "achieved_pressure": result.achieved_pressure,
        "value": result.value,
        "stopped_early": result.stopped_early,
        "optimizer_kind": result.optimizer_kind,
        "trace_steps": len(result.trace),
    }


def _gap_dict(gap: GoodhartGap) -> dict[str, float]:
    return {
        "proxy_return": gap.proxy_return,
        "intended_return": gap.intended_return,
        "gap": gap.gap,
        "gap_pp": gap.gap_pp,
        "pressure": gap.pressure,
    }


def _ledger_dict(ledger: SideEffectLedger) -> dict[str, Any]:
    rate = ledger.side_effect_rate(f"side-effect episode rate ({ledger.arm})")
    return {
        "arm": ledger.arm,
        "event_count": ledger.event_count,
        "episode_count": ledger.episode_count,
        "damaged_episodes": ledger.damaged_episodes,
        "total_magnitude": ledger.total_magnitude,
        "kind_totals": ledger.kind_totals(),
        "rate": {
            "successes": rate.successes,
            "denominator": rate.denominator,
            "lower": rate.interval.lower,
            "upper": rate.interval.upper,
        },
    }


def _metric_dict(metric: MetricSummary) -> dict[str, Any]:
    return {
        "name": metric.name,
        "successes": metric.successes,
        "denominator": metric.denominator,
        "rate": metric.rate,
        "lower": metric.interval.lower,
        "upper": metric.interval.upper,
    }


def _gate_dict(outcome: GateOutcome) -> dict[str, Any]:
    return {
        "pressure": outcome.pressure,
        "arm": outcome.arm,
        "metric_name": outcome.metric_name,
        "point": _metric_dict(outcome.point),
        "baseline": _metric_dict(outcome.baseline),
        "degradation_pp": outcome.degradation_pp,
        "floor_pp": outcome.floor_pp,
        "g1_pass": outcome.g1_pass,
        "g2_pass": outcome.g2_pass,
        "worst_case_degradation_pp": outcome.worst_case_degradation_pp,
        "worst_case_floor_pp": outcome.worst_case_floor_pp,
    }


def _paired_dict(comparison: PairedComparison) -> dict[str, Any]:
    win_rate = comparison.win_rate()
    return {
        "name": comparison.name,
        "pairs": len(comparison.pairs),
        "mean_primary": comparison.mean_primary,
        "mean_control": comparison.mean_control,
        "mean_difference": comparison.mean_difference,
        "primary_wins": comparison.primary_wins,
        "ties": comparison.ties,
        "control_wins": comparison.control_wins,
        "win_rate": {
            "successes": win_rate.successes,
            "denominator": win_rate.denominator,
            "lower": win_rate.interval.lower,
            "upper": win_rate.interval.upper,
        },
    }


def _match_rate_metric(
    metrics: Mapping[str, MetricSummary], gate_metric: str, arm: str
) -> tuple[str, MetricSummary]:
    """Bind the gate's metric name to the environment's arm-specific metric.

    Environments key their rate metrics by construct name (e.g. ``"damage-free
    episode rate"``) while the metric's display name carries the arm suffix
    (``"damage-free episode rate (tuning)"``). Both forms are accepted; any
    other mismatch is a configuration error.
    """
    if gate_metric in metrics and arm in metrics[gate_metric].name:
        return gate_metric, metrics[gate_metric]
    suffixed = f"{gate_metric} ({arm})"
    if suffixed in metrics:
        return suffixed, metrics[suffixed]
    for name, metric in sorted(metrics.items()):
        if name.startswith(gate_metric) and arm in metric.name:
            return name, metric
    raise RunnerError(
        f"gate metric {gate_metric!r} matches no environment rate metric on arm "
        f"{arm!r}; available: {sorted(metrics)}"
    )


def run_cell(
    env: TaskEnvironment,
    optimizer: PressureOptimizer,
    *,
    arm: str,
    pressure: int,
    seed: int,
    gate: GateConfig,
) -> CellRecord:
    """Execute one (arm, pressure) cell: primary + control + all measures."""
    primary = optimizer.optimize(
        env, reward_name=REWARD_PROXY, arm=arm, pressure=pressure, seed=seed
    )
    control = optimizer.optimize(
        env, reward_name=REWARD_INTENDED, arm=arm, pressure=pressure, seed=seed
    )
    primary_intended = env.evaluate(primary.policy, REWARD_INTENDED, arm)
    control_proxy = env.evaluate(control.policy, REWARD_PROXY, arm)
    gap_primary = goodhart_gap(primary.value, primary_intended, arm=arm, pressure=pressure)
    gap_control = goodhart_gap(control_proxy, control.value, arm=arm, pressure=pressure)
    # Gates: the optimized (primary) policy's rate metrics against the
    # environment's untuned reference policy on the same arm.
    primary_metrics = env.rate_metrics(primary.policy, arm, seed)
    reference_policy = env.reference_policy(arm)
    reference_metrics = env.rate_metrics(reference_policy, arm, seed)
    metric_name, point = _match_rate_metric(primary_metrics, gate.metric_name, arm)
    _, baseline = _match_rate_metric(reference_metrics, gate.metric_name, arm)
    # Gates require distinct measurement names: tag the reference baseline
    # (same construct, untuned policy) so the point/baseline pair reads
    # unambiguously in tables and verdict strings.
    baseline = rate_metric(f"{baseline.name} [reference]", baseline.successes, baseline.denominator)
    gate_outcome = evaluate_gates(gate, metric_name, point, baseline, pressure=pressure, arm=arm)
    ledger_primary = env.side_effects(primary.policy, arm, seed)
    ledger_control = env.side_effects(control.policy, arm, seed)
    primary_values = env.intended_episode_values(primary.policy, arm, seed)
    control_values = env.intended_episode_values(control.policy, arm, seed)
    comparison = PairedComparison.build(
        name=f"primary-vs-control intended @ alpha={pressure} [{arm}]",
        primary_values=primary_values,
        control_values=control_values,
    )
    return CellRecord(
        arm=arm,
        pressure=pressure,
        primary=_optimization_dict(primary),
        control=_optimization_dict(control),
        gap_primary=_gap_dict(gap_primary),
        gap_control=_gap_dict(gap_control),
        gates=_gate_dict(gate_outcome),
        side_effects_primary=_ledger_dict(ledger_primary),
        side_effects_control=_ledger_dict(ledger_control),
        paired=_paired_dict(comparison),
        reference={
            "fingerprint": env.policy_fingerprint(reference_policy),
            "metrics": {
                name: _metric_dict(metric) for name, metric in sorted(reference_metrics.items())
            },
        },
    )


@dataclass
class RunResult:
    """The complete, deterministic record of one P02 experiment run."""

    config: P02Config
    env_name: str
    env_version: str
    optimizer_kind: str
    construct_notes: tuple[str, ...]
    revision_note: str | None
    cells: list[CellRecord] = field(default_factory=list)

    def cells_for_arm(self, arm: str) -> list[CellRecord]:
        return [cell for cell in self.cells if cell.arm == arm]

    def divergence_series(self, series: str) -> dict[str, Any]:
        """Proxy- or intended-value series per arm across the ladder."""
        values: dict[str, list[float]] = {}
        for arm in self.config.arms:
            arm_values = []
            for cell in self.cells_for_arm(arm):
                if series == "proxy":
                    arm_values.append(cell.gap_primary["proxy_return"])
                else:
                    arm_values.append(cell.gap_primary["intended_return"])
            values[arm] = arm_values
        return {
            "series": series,
            "pressures": list(self.config.pressures),
            "values": values,
        }

    def provenance(self) -> dict[str, Any]:
        return {
            "schema": RESULTS_SCHEMA,
            "run_id": self.config.run_id,
            "project": self.config.project,
            "config_sha256": self.config.config_sha256(),
            "environment": self.env_name,
            "environment_version": self.env_version,
            "optimizer_kind": self.optimizer_kind,
            "pressures": list(self.config.pressures),
            "arms": list(self.config.arms),
            "seed": self.config.seed,
            "run_date": self.config.run_date,
            "code_version": CODE_VERSION,
            "python_version": platform.python_version(),
            "status_note": self.config.status_note,
        }

    def to_json_dict(self) -> dict[str, Any]:
        """The full deterministic record (results.json payload)."""
        return {
            "provenance": self.provenance(),
            "construct_notes": list(self.construct_notes),
            "revision_note": self.revision_note,
            "cells": [
                {
                    "arm": cell.arm,
                    "pressure": cell.pressure,
                    "primary": cell.primary,
                    "control": cell.control,
                    "gap_primary": cell.gap_primary,
                    "gap_control": cell.gap_control,
                    "gates": cell.gates,
                    "side_effects_primary": cell.side_effects_primary,
                    "side_effects_control": cell.side_effects_control,
                    "paired": cell.paired,
                    "reference": cell.reference,
                }
                for cell in self.cells
            ],
            "divergence": {
                "proxy": self.divergence_series("proxy"),
                "intended": self.divergence_series("intended"),
            },
        }


def _cell_order(config: P02Config) -> list[tuple[str, int]]:
    """Deterministic iteration order: arms as configured, pressures ascending."""
    return [(arm, pressure) for arm in config.arms for pressure in config.pressures]


def _state_path(output_dir: Path) -> Path:
    return output_dir / "state.json"


def _load_state(output_dir: Path, config: P02Config) -> dict[str, Any]:
    """Load resumable state; fail-closed on schema/identity mismatch."""
    path = _state_path(output_dir)
    if not path.exists():
        return {"schema": STATE_SCHEMA, "config_sha256": config.config_sha256(), "completed": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RunnerError(f"corrupt state file {path}: {exc}") from exc
    if state.get("schema") != STATE_SCHEMA:
        raise RunnerError(f"state schema {state.get('schema')!r} != {STATE_SCHEMA!r}; refusing")
    if state.get("config_sha256") != config.config_sha256():
        raise RunnerError(
            "state belongs to a different configuration (config_sha256 mismatch); "
            "use a fresh output_dir or remove the stale state"
        )
    return state


def _write_state(output_dir: Path, state: Mapping[str, Any]) -> None:
    path = _state_path(output_dir)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(dict(state), sort_keys=True, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def run_experiment(config: P02Config, *, output_dir: Path | None = None) -> RunResult:
    """Execute the full experiment (resumable across interruptions).

    Args:
        config: the validated configuration.
        output_dir: where resumability state is written (defaults to the
            config's ``output_dir`` relative to the current directory).

    Returns:
        The complete :class:`RunResult` (identical whether the run was
        fresh or resumed — cells are deterministic given the config).
    """
    try:
        env = environment_from_config(config.environment)
    except EnvironmentError as exc:
        raise RunnerError(f"environment configuration rejected: {exc}") from exc
    for arm in config.arms:
        if arm not in env.arms:
            raise RunnerError(
                f"config arm {arm!r} not offered by environment {env.name!r} " f"({list(env.arms)})"
            )
    try:
        optimizer = optimizer_from_config(dict(config.optimizer))
    except OptimizerError as exc:
        raise RunnerError(f"optimizer configuration rejected: {exc}") from exc
    if config.seed < 0:
        raise RunnerError("seed must be >= 0")
    directory = output_dir if output_dir is not None else Path(config.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    state = _load_state(directory, config)
    completed: dict[str, dict[str, Any]] = dict(state.get("completed", {}))
    revision_note = getattr(env, "revision_note", None)
    revision_note = revision_note() if callable(revision_note) else None
    result = RunResult(
        config=config,
        env_name=env.name,
        env_version=env.version,
        optimizer_kind=optimizer.kind,
        construct_notes=env.construct_notes(),
        revision_note=revision_note,
        cells=[],
    )
    for arm, pressure in _cell_order(config):
        cell_id = f"{arm}@{pressure}"
        if cell_id in completed:
            # Deterministic replay: recompute the cell (cheap, exact) so the
            # in-memory record matches a fresh run byte-for-byte.
            cell = run_cell(
                env,
                optimizer,
                arm=arm,
                pressure=pressure,
                seed=config.seed,
                gate=config.gate,
            )
        else:
            cell = run_cell(
                env,
                optimizer,
                arm=arm,
                pressure=pressure,
                seed=config.seed,
                gate=config.gate,
            )
            completed[cell_id] = {"arm": arm, "pressure": pressure}
            state = {
                "schema": STATE_SCHEMA,
                "config_sha256": config.config_sha256(),
                "completed": completed,
            }
            _write_state(directory, state)
        result.cells.append(cell)
    return result


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


def load_config_file(path: Path) -> P02Config:
    """Load and validate a YAML configuration file."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise RunnerError(f"invalid YAML in {path}: {exc}") from exc
    return parse_config(raw if raw is not None else {})


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point: ``python -m ai_safety_course.reward_spec.runner``."""
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("usage: python -m ai_safety_course.reward_spec.runner <config.yaml>", file=sys.stderr)
        return 2
    from ai_safety_course.reward_spec.report import write_report

    try:
        config = load_config_file(Path(args[0]))
        output_dir = Path(config.output_dir)
        result = run_experiment(config, output_dir=output_dir)
        results_path = write_results(result, output_dir)
        report_path = write_report(result, output_dir)
    except (RunnerError, MetricsError, OptimizerError, EnvironmentError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(
        f"cells: {len(result.cells)} ({', '.join(f'{c.arm}@{c.pressure}' for c in result.cells)})"
    )
    print(f"results: {results_path}")
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
