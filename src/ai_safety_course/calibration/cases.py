"""cases — versioned, checksummed calibration case sets.

A calibration case set is a YAML file holding items with known binary
outcomes and scripted confidence scores from named instruments. This
module loads and validates them with the same fail-closed policy as
the P01 case sets: any deviation from the declared schema version, any
missing or unknown field, any invalid outcome or score, or any
duplicate id raises :class:`CalibrationCaseError`. Instrument identity
is pinned by a SHA-256 checksum over the exact file bytes and an
explicit version field — an evaluation whose instrument silently
drifts between runs produces numbers that cannot be compared to
anything (the Chapter 02 rule, carried into Chapter 06's territory).

The committed fixture models calibration regimes at the metadata level
only (correct-answer frequencies by confidence band per instrument);
no dataset content is redistributed.
"""

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

#: The only case-set schema version this loader understands.
CASES_SCHEMA = "p03-calibration-cases/v1"

#: Fields every case must carry — no more, no fewer.
REQUIRED_CASE_FIELDS = ("id", "category", "expected_outcome", "instrument_scores")

#: Fields the file's top level must carry.
REQUIRED_TOP_LEVEL_FIELDS = ("schema", "version", "name", "cases")

#: Optional top-level fields.
OPTIONAL_TOP_LEVEL_FIELDS = ("description", "provenance")


class CalibrationCaseError(ValueError):
    """Raised when a calibration case-set file fails validation."""


@dataclass(frozen=True)
class CalibrationCase:
    """One calibration item: an outcome plus per-instrument confidence.

    Attributes:
        id: unique, stable item identifier.
        category: grouping label for per-category reporting.
        expected_outcome: 1 (correct/true) or 0 (wrong/false) — the
            ground truth the scores are calibrated against.
        instrument_scores: confidence in [0, 1] per instrument name.
    """

    id: str
    category: str
    expected_outcome: int
    instrument_scores: Mapping[str, float]

    def score(self, instrument: str) -> float:
        """This item's confidence under one instrument (fail-closed)."""
        try:
            return self.instrument_scores[instrument]
        except KeyError as exc:
            raise CalibrationCaseError(
                f"case {self.id!r} has no score for instrument {instrument!r}; "
                f"available: {sorted(self.instrument_scores)}"
            ) from exc


@dataclass(frozen=True)
class CalibrationCaseSet:
    """A validated, checksummed set of calibration items.

    Attributes:
        name: short name from the file.
        version: semantic version string from the file.
        description: human description from the file.
        provenance: provenance block from the file.
        cases: the items in file order.
        instruments: the instrument names any case carries (sorted,
            deduplicated).
        sha256: SHA-256 hex digest of the exact file bytes.
        path: filesystem path the set was loaded from.
    """

    name: str
    version: str
    description: str
    provenance: Mapping[str, Any]
    cases: tuple[CalibrationCase, ...]
    instruments: tuple[str, ...]
    sha256: str
    path: Path

    def instrument_scores(self, instrument: str) -> tuple[float, ...]:
        """All item scores for one instrument, in case order."""
        return tuple(case.score(instrument) for case in self.cases)

    def outcomes(self) -> tuple[int, ...]:
        """All outcomes, in case order."""
        return tuple(case.expected_outcome for case in self.cases)

    def categories(self) -> tuple[str, ...]:
        """Distinct categories, in first-appearance order."""
        seen: list[str] = []
        for case in self.cases:
            if case.category not in seen:
                seen.append(case.category)
        return tuple(seen)


def _validate_score(value: Any, context: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise CalibrationCaseError(f"{context}: score must be a number, got {value!r}")
    if not 0.0 <= float(value) <= 1.0:
        raise CalibrationCaseError(f"{context}: score must be in [0, 1], got {value!r}")
    return float(value)


def load_case_set(path: Path) -> CalibrationCaseSet:
    """Load and validate a calibration case set (fail-closed).

    Args:
        path: the YAML file to load.

    Raises:
        CalibrationCaseError: on any schema, field, or value violation.
    """
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CalibrationCaseError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, Mapping):
        raise CalibrationCaseError(f"{path}: top level must be a mapping")
    if raw.get("schema") != CASES_SCHEMA:
        raise CalibrationCaseError(f"{path}: schema {raw.get('schema')!r} != {CASES_SCHEMA!r}")
    missing = [f for f in REQUIRED_TOP_LEVEL_FIELDS if f not in raw]
    if missing:
        raise CalibrationCaseError(f"{path}: missing required fields: {missing}")
    unknown = set(raw) - set(REQUIRED_TOP_LEVEL_FIELDS) - set(OPTIONAL_TOP_LEVEL_FIELDS)
    if unknown:
        raise CalibrationCaseError(f"{path}: unknown top-level fields: {sorted(unknown)}")
    entries = raw["cases"]
    if not isinstance(entries, Sequence) or isinstance(entries, (str, bytes)):
        raise CalibrationCaseError(f"{path}: 'cases' must be a list")
    cases: list[CalibrationCase] = []
    instruments: set[str] = set()
    seen_ids: set[str] = set()
    for position, entry in enumerate(entries):
        context = f"{path}: case #{position}"
        if not isinstance(entry, Mapping):
            raise CalibrationCaseError(f"{context}: must be a mapping")
        case_fields = set(entry)
        if case_fields != set(REQUIRED_CASE_FIELDS):
            missing_case = set(REQUIRED_CASE_FIELDS) - case_fields
            extra_case = case_fields - set(REQUIRED_CASE_FIELDS)
            problems = []
            if missing_case:
                problems.append(f"missing {sorted(missing_case)}")
            if extra_case:
                problems.append(f"unknown {sorted(extra_case)}")
            raise CalibrationCaseError(f"{context}: {', '.join(problems)}")
        case_id = entry["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            raise CalibrationCaseError(f"{context}: id must be a non-empty string")
        if case_id in seen_ids:
            raise CalibrationCaseError(f"{context}: duplicate id {case_id!r}")
        seen_ids.add(case_id)
        category = entry["category"]
        if not isinstance(category, str) or not category.strip():
            raise CalibrationCaseError(f"{context}: category must be a non-empty string")
        outcome = entry["expected_outcome"]
        if outcome not in (0, 1) or isinstance(outcome, bool):
            raise CalibrationCaseError(
                f"{context}: expected_outcome must be 0 or 1, got {outcome!r}"
            )
        raw_scores = entry["instrument_scores"]
        if not isinstance(raw_scores, Mapping) or not raw_scores:
            raise CalibrationCaseError(f"{context}: instrument_scores must be a non-empty mapping")
        scores = {
            name: _validate_score(value, f"{context} instrument {name!r}")
            for name, value in raw_scores.items()
        }
        instruments.update(scores)
        cases.append(
            CalibrationCase(
                id=case_id,
                category=category,
                expected_outcome=int(outcome),
                instrument_scores=scores,
            )
        )
    if not cases:
        raise CalibrationCaseError(f"{path}: 'cases' must be non-empty")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return CalibrationCaseSet(
        name=str(raw["name"]),
        version=str(raw["version"]),
        description=str(raw.get("description", "")),
        provenance=dict(raw.get("provenance", {})),
        cases=tuple(cases),
        instruments=tuple(sorted(instruments)),
        sha256=digest,
        path=path,
    )


__all__ = [
    "CASES_SCHEMA",
    "CalibrationCase",
    "CalibrationCaseError",
    "CalibrationCaseSet",
    "load_case_set",
]
