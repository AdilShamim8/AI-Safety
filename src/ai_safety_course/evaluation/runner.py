"""runner — config-driven, resumable, fail-closed evaluation runner.

The runner turns a small YAML configuration into a complete, dated
evaluation record. Design contracts (each is test-enforced):

* **Config-driven**: one YAML file names the case set, the adapter
  configuration, the output directory, the seed, and the run date. The
  same config reproduces the same outputs byte-for-byte.
* **Deterministic**: the seed is threaded into every adapter call, no
  wall-clock value enters the serialized outputs (the run *date* comes
  from the config), and iteration follows case-file order.
* **Resumable**: after every completed case, ``<output_dir>/state.json``
  is rewritten with the completed records. An interrupted run (crash,
  adapter error) resumes from that file and produces results identical to
  an uninterrupted run — "resumes exactly", not "resumes approximately".
* **Fail-closed**: unknown config schema, unknown case-set schema,
  unknown adapter kind, stale/mismatched resume state, and any adapter
  exception abort the run with an explicit error. The runner never
  silently skips a case, never substitutes a default response, and never
  mixes state across different case sets or adapter configurations.

Outputs (written under ``output_dir``):

* ``state.json`` — resumability state (schema, run identity, completed
  case records).
* ``results.json`` — the full, deterministic run record (provenance +
  per-case rows). This is the artifact the report generator consumes.
* ``report.md`` — written by the command-line entry point
  (``python -m ai_safety_course.evaluation.runner <config.yaml>``).
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
from ai_safety_course.evaluation.adapters import (
    AdapterError,
    ModelAdapter,
    adapter_from_config,
    config_sha256,
)
from ai_safety_course.evaluation.cases import Case, CaseSet, CaseSetError, load_case_set
from ai_safety_course.evaluation.metrics import (
    LABEL_COMPLIANCE,
    LABEL_REFUSAL,
    CaseOutcome,
    PairedLedger,
    paired_ledger,
)
from ai_safety_course.evaluation.scorer import (
    RuleBasedRefusalScorer,
    Scorer,
    ScorerValidation,
    validate_scorer,
)

#: The only run-config schema version this runner understands.
RUN_CONFIG_SCHEMA = "p01-run/v1"

#: Schema of the resumability state file.
STATE_SCHEMA = "p01-state/v1"

#: Schema of the results file.
RESULTS_SCHEMA = "p01-results/v1"

#: The only scorer selectable from configuration (fail-closed otherwise).
CONFIGURABLE_SCORERS = frozenset({"rule-based-v1"})

#: Keys every serialized case record carries.
RECORD_FIELDS = (
    "case_id",
    "category",
    "expected_behavior",
    "prompt",
    "response",
    "label",
    "matched",
)


class RunError(RuntimeError):
    """Raised on any fail-closed runner condition (config, state, execution)."""


@dataclass(frozen=True)
class RunConfig:
    """A fully resolved run configuration.

    Attributes:
        run_id: short identifier for the run (recorded in all outputs).
        cases_path: path to the YAML case set.
        output_dir: directory for ``state.json`` / ``results.json`` /
            ``report.md``.
        adapter_config: the adapter block (``kind`` plus kind-specific
            keys) — fingerprinted into provenance.
        seed: integer seed threaded to every adapter call.
        run_date: ISO date string for the report; ``None`` means "use
            today at run start" (explicit dates keep outputs
            byte-reproducible).
        report_title: title line for the generated report.
        scorer_name: scorer selector, currently only ``"rule-based-v1"``.
    """

    run_id: str
    cases_path: Path
    output_dir: Path
    adapter_config: Mapping[str, Any]
    seed: int
    run_date: str | None
    report_title: str
    scorer_name: str


@dataclass(frozen=True)
class CaseRecord(CaseOutcome):
    """One executed case: the scored outcome plus the full evidence.

    Extends :class:`~ai_safety_course.evaluation.metrics.CaseOutcome`
    (the ledger input) with the prompt, the response text, and the
    matched refusal-pattern ids, so error analysis is reproducible from
    the results file alone.
    """

    prompt: str
    response: str
    matched: tuple[str, ...]

    @property
    def is_match(self) -> bool:
        """Whether the scored label agrees with the expected behavior."""
        expected_label = LABEL_REFUSAL if self.expected_behavior == "refuse" else LABEL_COMPLIANCE
        return self.label == expected_label


@dataclass(frozen=True)
class RunResult:
    """The complete record of one evaluation run.

    Everything a report needs, including the provenance block required by
    the repository's experiment-report template: case-set checksum and
    version, adapter configuration fingerprint, seed, code version,
    environment, and the scorer's validation status.
    """

    run_id: str
    run_date: str
    report_title: str
    case_set: CaseSet
    adapter_kind: str
    adapter_config_sha256: str
    seed: int
    code_version: str
    python_version: str
    pyyaml_version: str
    scorer_name: str
    scorer_validation: ScorerValidation
    records: tuple[CaseRecord, ...]
    resumed_cases: int

    def ledger(self) -> PairedLedger:
        """The paired refusal/compliance ledger for this run."""
        return paired_ledger(list(self.records))

    def mismatches(self) -> tuple[CaseRecord, ...]:
        """Records whose scored label disagrees with the expected behavior."""
        return tuple(record for record in self.records if not record.is_match)


def _require(config: Mapping[str, Any], key: str, where: str) -> Any:
    """Fail-closed required-field lookup."""
    if key not in config:
        raise RunError(f"{where}: missing required field {key!r}")
    return config[key]


def _is_plain_int(value: Any) -> bool:
    """Whether ``value`` is an int (excluding bool, which is an int subclass)."""
    return isinstance(value, int) and not isinstance(value, bool)


def load_run_config(path: Path | str) -> RunConfig:
    """Load and validate a run config from a YAML file.

    Paths inside the config are resolved relative to the current working
    directory (the documented invocation point is the repository root).

    Raises:
        RunError: on missing file, YAML errors, wrong schema, missing or
            mistyped fields, or an invalid adapter/scorer selector.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise RunError(f"run config not found or not a file: {config_path}")
    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as exc:
        raise RunError(f"{config_path}: YAML parse error: {exc}") from exc

    if not isinstance(data, Mapping):
        raise RunError(f"{config_path}: top level must be a mapping, got {type(data)!r}")
    schema = data.get("schema")
    if schema != RUN_CONFIG_SCHEMA:
        raise RunError(
            f"{config_path}: unsupported schema {schema!r}; this runner only accepts "
            f"{RUN_CONFIG_SCHEMA!r} (fail-closed)"
        )

    run_id = _require(data, "run_id", str(config_path))
    if not isinstance(run_id, str) or not run_id.strip():
        raise RunError(f"{config_path}: run_id must be a non-empty string")
    cases_path = _require(data, "cases_path", str(config_path))
    output_dir = _require(data, "output_dir", str(config_path))
    if not isinstance(cases_path, str) or not cases_path.strip():
        raise RunError(f"{config_path}: cases_path must be a non-empty string")
    if not isinstance(output_dir, str) or not output_dir.strip():
        raise RunError(f"{config_path}: output_dir must be a non-empty string")

    adapter_config = _require(data, "adapter", str(config_path))
    try:
        adapter_from_config(adapter_config)  # fail fast on bad adapter config
    except AdapterError as exc:
        raise RunError(f"{config_path}: invalid adapter config: {exc}") from exc

    seed = _require(data, "seed", str(config_path))
    if not _is_plain_int(seed):
        raise RunError(f"{config_path}: seed must be an integer, got {seed!r}")

    run_date = data.get("run_date")
    if run_date is not None:
        if not isinstance(run_date, str) or len(run_date) != 10 or run_date[4] != "-":
            raise RunError(f"{config_path}: run_date must be an ISO 'YYYY-MM-DD' string")

    report_title = data.get("report_title", "P01 evaluation run")
    if not isinstance(report_title, str) or not report_title.strip():
        raise RunError(f"{config_path}: report_title must be a non-empty string")

    scorer_name = data.get("scorer", "rule-based-v1")
    if scorer_name not in CONFIGURABLE_SCORERS:
        raise RunError(
            f"{config_path}: unknown scorer {scorer_name!r}; supported: "
            f"{sorted(CONFIGURABLE_SCORERS)}"
        )

    return RunConfig(
        run_id=run_id,
        cases_path=Path(cases_path),
        output_dir=Path(output_dir),
        adapter_config=dict(adapter_config),
        seed=seed,
        run_date=run_date,
        report_title=report_title,
        scorer_name=scorer_name,
    )


def _make_scorer(scorer_name: str) -> Scorer:
    """Map a config scorer selector to a scorer instance (fail-closed)."""
    if scorer_name == "rule-based-v1":
        return RuleBasedRefusalScorer()
    raise RunError(f"unknown scorer {scorer_name!r}; supported: {sorted(CONFIGURABLE_SCORERS)}")


def _dump_json(payload: Mapping[str, Any]) -> str:
    """Deterministic JSON rendering (sorted keys, 2-space indent)."""
    return json.dumps(dict(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _record_to_dict(record: CaseRecord) -> dict[str, Any]:
    """Serialize one case record (stable key set)."""
    return {
        "case_id": record.case_id,
        "category": record.category,
        "expected_behavior": record.expected_behavior,
        "prompt": record.prompt,
        "response": record.response,
        "label": record.label,
        "matched": list(record.matched),
    }


def _record_from_dict(data: Mapping[str, Any], where: str) -> CaseRecord:
    """Deserialize one case record (fail-closed on malformed rows)."""
    missing = [field for field in RECORD_FIELDS if field not in data]
    if missing:
        raise RunError(f"{where}: record missing fields {missing}")
    label = data["label"]
    if label not in (LABEL_REFUSAL, LABEL_COMPLIANCE):
        raise RunError(f"{where}: invalid label {label!r}")
    matched = data["matched"]
    if not isinstance(matched, list) or not all(isinstance(item, str) for item in matched):
        raise RunError(f"{where}: 'matched' must be a list of pattern ids")
    str_fields = ("case_id", "category", "expected_behavior", "prompt", "response")
    values = {field: data[field] for field in str_fields}
    for field, value in values.items():
        if not isinstance(value, str):
            raise RunError(f"{where}: field {field!r} must be a string")
    return CaseRecord(label=label, matched=tuple(matched), **values)


def _load_state(state_path: Path, config: RunConfig, case_set: CaseSet) -> dict[str, CaseRecord]:
    """Load resume state; fail-closed on mismatch with the current run.

    A state file is only reusable when it was produced by the same run
    identity: same case-set checksum, same adapter configuration
    fingerprint, same seed, and same run id. Anything else aborts —
    resuming a different run's state would silently mix instruments
    (Chapter 02's provenance rule, enforced in code).
    """
    if not state_path.is_file():
        return {}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RunError(f"{state_path}: unreadable resume state: {exc}") from exc
    if not isinstance(data, Mapping):
        raise RunError(f"{state_path}: state must be a JSON object")
    if data.get("schema") != STATE_SCHEMA:
        raise RunError(
            f"{state_path}: unsupported state schema {data.get('schema')!r}; "
            f"expected {STATE_SCHEMA!r}"
        )

    expected = {
        "run_id": config.run_id,
        "cases_sha256": case_set.sha256,
        "adapter_config_sha256": config_sha256(config.adapter_config),
        "seed": config.seed,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise RunError(
                f"{state_path}: state does not match this run ({key}: state has "
                f"{data.get(key)!r}, config requires {value!r}); refusing to resume — "
                "delete the output directory to start fresh"
            )

    completed = data.get("completed")
    if not isinstance(completed, list):
        raise RunError(f"{state_path}: 'completed' must be a list of records")
    restored: dict[str, CaseRecord] = {}
    for index, entry in enumerate(completed):
        record = _record_from_dict(entry, f"{state_path}: completed[{index}]")
        if record.case_id not in case_set.by_id():
            raise RunError(
                f"{state_path}: completed case {record.case_id!r} is not in the case set "
                f"({case_set.name} @ {case_set.sha256[:12]}); refusing stale state"
            )
        restored[record.case_id] = record
    return restored


def _write_state(
    state_path: Path,
    config: RunConfig,
    case_set: CaseSet,
    records: Sequence[CaseRecord],
) -> None:
    """Persist the resumability state (called after every completed case)."""
    payload = {
        "schema": STATE_SCHEMA,
        "run_id": config.run_id,
        "cases_sha256": case_set.sha256,
        "adapter_config_sha256": config_sha256(config.adapter_config),
        "seed": config.seed,
        "completed": [_record_to_dict(record) for record in records],
    }
    state_path.write_text(_dump_json(payload), encoding="utf-8")


def run_evaluation(
    config: RunConfig,
    *,
    adapter: ModelAdapter | None = None,
    scorer: Scorer | None = None,
) -> RunResult:
    """Execute (or resume) the evaluation described by ``config``.

    Args:
        config: the resolved run configuration.
        adapter: optional pre-built adapter (programmatic use, e.g.
            :class:`~ai_safety_course.evaluation.adapters.CallableAdapter`);
            defaults to building one from ``config.adapter_config``.
        scorer: optional scorer override; defaults to the scorer named in
            the config.

    Returns:
        The complete :class:`RunResult` (also serialized to
        ``<output_dir>/results.json``).

    Raises:
        RunError: on any fail-closed condition — invalid config, invalid
            case set, mismatched resume state, or an adapter failure
            mid-run (the state written so far remains resumable).
    """
    try:
        case_set = load_case_set(config.cases_path)
    except CaseSetError as exc:
        raise RunError(f"cannot load case set: {exc}") from exc

    if adapter is None:
        try:
            adapter = adapter_from_config(config.adapter_config)
        except AdapterError as exc:
            raise RunError(f"cannot build adapter: {exc}") from exc
    if scorer is None:
        scorer = _make_scorer(config.scorer_name)

    validation = validate_scorer(scorer)

    output_dir = config.output_dir
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise RunError(f"cannot create output directory {output_dir}: {exc}") from exc
    state_path = output_dir / "state.json"

    resumed = _load_state(state_path, config, case_set)
    records_by_id: dict[str, CaseRecord] = dict(resumed)

    for case in case_set.cases:
        if case.id in records_by_id:
            continue
        record = _execute_case(case, adapter, scorer, config.seed)
        records_by_id[case.id] = record
        ordered = [records_by_id[cid] for cid in case_set.ids() if cid in records_by_id]
        _write_state(state_path, config, case_set, ordered)

    records = tuple(records_by_id[cid] for cid in case_set.ids())
    run_date = config.run_date or date.today().isoformat()

    result = RunResult(
        run_id=config.run_id,
        run_date=run_date,
        report_title=config.report_title,
        case_set=case_set,
        adapter_kind=adapter.name,
        adapter_config_sha256=config_sha256(config.adapter_config),
        seed=config.seed,
        code_version=f"ai-safety-course {CODE_VERSION} (P01 harness)",
        python_version=platform.python_version(),
        pyyaml_version=yaml.__version__,
        scorer_name=scorer.name,
        scorer_validation=validation,
        records=records,
        resumed_cases=len(resumed),
    )

    results_payload = {
        "schema": RESULTS_SCHEMA,
        "run_id": result.run_id,
        "run_date": result.run_date,
        "report_title": result.report_title,
        "case_set": {
            "name": case_set.name,
            "version": case_set.version,
            "path": case_set.path,
            "sha256": case_set.sha256,
        },
        "adapter": {"kind": result.adapter_kind, "config_sha256": result.adapter_config_sha256},
        "seed": result.seed,
        "code_version": result.code_version,
        "python_version": result.python_version,
        "pyyaml_version": result.pyyaml_version,
        "scorer": {
            "name": result.scorer_name,
            "validation": str(result.scorer_validation),
        },
        "resumed_cases": result.resumed_cases,
        "records": [_record_to_dict(record) for record in records],
    }
    try:
        (output_dir / "results.json").write_text(_dump_json(results_payload), encoding="utf-8")
    except OSError as exc:
        raise RunError(f"cannot write results.json: {exc}") from exc
    return result


def _execute_case(case: Case, adapter: ModelAdapter, scorer: Scorer, seed: int) -> CaseRecord:
    """Run one case end-to-end (adapter call + scoring), fail-closed."""
    try:
        response = adapter.generate(case.prompt, case_id=case.id, seed=seed)
    except Exception as exc:  # noqa: BLE001 — deliberate fail-closed boundary
        raise RunError(
            f"adapter {adapter.name!r} failed on case {case.id!r}: {exc!r}; "
            "run aborted (fail-closed) — the state file keeps completed cases"
        ) from exc
    if not isinstance(response, str) or not response.strip():
        raise RunError(
            f"adapter {adapter.name!r} returned an empty/non-string response for case "
            f"{case.id!r}; run aborted (fail-closed)"
        )
    scored = scorer.score(prompt=case.prompt, response=response)
    return CaseRecord(
        case_id=case.id,
        category=case.category,
        expected_behavior=case.expected_behavior,
        prompt=case.prompt,
        response=response,
        label=scored.label,
        matched=scored.matched,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point: ``python -m ...runner <config.yaml>``.

    Writes ``state.json``, ``results.json``, and ``report.md`` under the
    configured output directory, then prints the paired ledger.

    Returns:
        0 on success, 1 on any fail-closed error, 2 on usage errors.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1 or args[0] in {"-h", "--help"}:
        print(
            "usage: python -m ai_safety_course.evaluation.runner <run-config.yaml>", file=sys.stderr
        )
        return 2
    try:
        config = load_run_config(args[0])
        result = run_evaluation(config)
    except RunError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    from ai_safety_course.evaluation import report as report_module  # local: avoid cycle

    report_path = config.output_dir / "report.md"
    try:
        report_module.write_report(result, report_path)
    except OSError as exc:
        print(f"error: cannot write report: {exc}", file=sys.stderr)
        return 1
    print(f"run {result.run_id!r} complete: {len(result.records)} cases")
    print(str(result.ledger()))
    print(f"results: {config.output_dir / 'results.json'}")
    print(f"report:  {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
