"""scenarios — scripted agent traces with provenance-tagged arguments.

A scenario is a deterministic sequence of tool calls (each argument
carrying its provenance tag) plus, for attacks, the step whose
execution constitutes *attack success*. Scenarios are the paired
trials of the P07 harness: the same trace runs under the undefended
arm (full delegation) and the capability arm (R1-R4), and the paired
outcomes form the evidence ledger.

Fixture honesty (recorded in the project README and every report):
all scenario content is synthetic and authored for this course — no
real attack payloads, no dataset content, no product names beyond
generic tool names (``mail.send`` &c.). The scenarios model the
*mechanisms* of Chapter 14's attack classes at the metadata level:
which channel contributed which argument, and what the policy did
about it. Loading is fail-closed and checksum-pinned.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ai_safety_course.agent_guard.policy import Argument, Provenance, ToolCall

#: The only scenario-set schema version this loader understands.
SCENARIOS_SCHEMA = "p07-scenarios/v1"

#: Scripted user behaviors when the policy asks for consent.
CONSENT_GRANT = "grant"
CONSENT_DENY = "deny"
CONSENT_NONE = "none"
VALID_CONSENT = frozenset({CONSENT_GRANT, CONSENT_DENY, CONSENT_NONE})

#: Scenario kinds.
KIND_ATTACK = "attack"
KIND_BENIGN = "benign"
VALID_KINDS = frozenset({KIND_ATTACK, KIND_BENIGN})


class ScenarioError(ValueError):
    """Raised when a scenario set is structurally invalid."""


@dataclass(frozen=True)
class Step:
    """One step of a trace: the call, and the scripted user's consent behavior."""

    call: ToolCall
    consent: str = CONSENT_NONE


@dataclass(frozen=True)
class Scenario:
    """A scripted trace; attacks name the step whose execution = success."""

    id: str
    kind: str
    description: str
    steps: tuple[Step, ...]
    target_step: int | None = None

    def __post_init__(self) -> None:
        if self.kind not in VALID_KINDS:
            raise ScenarioError(f"scenario {self.id!r}: kind {self.kind!r} invalid")
        if not self.steps:
            raise ScenarioError(f"scenario {self.id!r}: must have at least one step")
        if self.kind == KIND_ATTACK:
            if self.target_step is None:
                raise ScenarioError(f"attack scenario {self.id!r}: target_step required")
            if not 1 <= self.target_step <= len(self.steps):
                raise ScenarioError(
                    f"attack scenario {self.id!r}: target_step "
                    f"{self.target_step} out of range 1..{len(self.steps)}"
                )
        if self.kind == KIND_BENIGN and self.target_step is not None:
            raise ScenarioError(f"benign scenario {self.id!r}: target_step must be absent")


@dataclass(frozen=True)
class ScenarioSet:
    """A checksum-pinned collection of scenarios."""

    scenarios: tuple[Scenario, ...]
    name: str = "<in-memory>"
    checksum: str = "<none>"
    schema_version: str = SCENARIOS_SCHEMA

    def __post_init__(self) -> None:
        ids = [s.id for s in self.scenarios]
        if len(set(ids)) != len(ids):
            dupes = sorted({i for i in ids if ids.count(i) > 1})
            raise ScenarioError(f"duplicate scenario ids: {dupes}")

    def attacks(self) -> tuple[Scenario, ...]:
        return tuple(s for s in self.scenarios if s.kind == KIND_ATTACK)

    def benign(self) -> tuple[Scenario, ...]:
        return tuple(s for s in self.scenarios if s.kind == KIND_BENIGN)


_PROVENANCE_BY_TAG = {p.value: p for p in Provenance}


def _parse_call(raw: Mapping[str, Any], scenario_id: str, step_no: int) -> ToolCall:
    if "tool" not in raw:
        raise ScenarioError(f"{scenario_id} step {step_no}: missing 'tool'")
    tool = str(raw["tool"])
    raw_args = raw.get("arguments", [])
    if not isinstance(raw_args, list):
        raise ScenarioError(f"{scenario_id} step {step_no}: 'arguments' must be a list")
    args: list[Argument] = []
    for ra in raw_args:
        if not isinstance(ra, Mapping):
            raise ScenarioError(f"{scenario_id} step {step_no}: argument must be a mapping")
        missing = [f for f in ("name", "value", "provenance") if f not in ra]
        if missing:
            raise ScenarioError(f"{scenario_id} step {step_no}: argument missing fields {missing}")
        tag = str(ra["provenance"])
        if tag not in _PROVENANCE_BY_TAG:
            raise ScenarioError(
                f"{scenario_id} step {step_no}: provenance {tag!r} must be one of "
                f"{sorted(_PROVENANCE_BY_TAG)}"
            )
        args.append(
            Argument(
                name=str(ra["name"]),
                value=str(ra["value"]),
                provenance=_PROVENANCE_BY_TAG[tag],
                is_capability_ref=bool(ra.get("is_capability_ref", False)),
            )
        )
    return ToolCall(tool=tool, arguments=tuple(args))


def parse_scenario_set(data: Mapping[str, Any]) -> ScenarioSet:
    """Validate and build a :class:`ScenarioSet` from a parsed mapping."""
    if data.get("schema_version") != SCENARIOS_SCHEMA:
        raise ScenarioError(
            f"schema_version {data.get('schema_version')!r} != {SCENARIOS_SCHEMA!r}"
        )
    raw = data.get("scenarios")
    if not isinstance(raw, list) or not raw:
        raise ScenarioError("scenario set must carry a non-empty 'scenarios' list")
    scenarios: list[Scenario] = []
    for entry in raw:
        if not isinstance(entry, Mapping):
            raise ScenarioError(f"scenario entry must be a mapping: {entry!r}")
        for f in ("id", "kind", "description", "steps"):
            if f not in entry:
                raise ScenarioError(f"scenario missing field {f!r}: {dict(entry)!r}")
        sid = str(entry["id"])
        raw_steps = entry["steps"]
        if not isinstance(raw_steps, list) or not raw_steps:
            raise ScenarioError(f"scenario {sid!r}: 'steps' must be a non-empty list")
        steps: list[Step] = []
        for i, rs in enumerate(raw_steps, start=1):
            if not isinstance(rs, Mapping) or "call" not in rs:
                raise ScenarioError(f"{sid} step {i}: missing 'call'")
            consent = str(rs.get("consent", CONSENT_NONE))
            if consent not in VALID_CONSENT:
                raise ScenarioError(
                    f"{sid} step {i}: consent {consent!r} must be one of {sorted(VALID_CONSENT)}"
                )
            steps.append(Step(call=_parse_call(rs["call"], sid, i), consent=consent))
        target = entry.get("target_step")
        scenarios.append(
            Scenario(
                id=sid,
                kind=str(entry["kind"]),
                description=str(entry["description"]),
                steps=tuple(steps),
                target_step=int(target) if target is not None else None,
            )
        )
    return ScenarioSet(scenarios=tuple(scenarios))


def load_scenario_set(path: Path) -> ScenarioSet:
    """Load and checksum-pin a scenario YAML file (fail-closed)."""
    raw = path.read_bytes()
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise ScenarioError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, Mapping):
        raise ScenarioError(f"{path}: top level must be a mapping")
    parsed = parse_scenario_set(data)
    return ScenarioSet(
        scenarios=parsed.scenarios,
        name=str(path),
        checksum=hashlib.sha256(raw).hexdigest(),
    )
