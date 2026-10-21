"""cases — versioned, checksummed evaluation case sets.

A case set is a YAML file holding synthetic evaluation prompts with their
expected behaviors. This module loads and validates them with a fail-closed
policy: any deviation from the declared schema version, any missing or
unknown field, any invalid expected-behavior value, or any duplicate id
raises :class:`CaseSetError` instead of being silently tolerated. The
Chapter 02 rule this enforces: an evaluation whose instrument
(case set) silently drifts between runs produces numbers that cannot be
compared to anything, so instrument identity is pinned by a SHA-256
checksum over the exact file bytes and an explicit version field.

The committed fixture ``projects/p01-evaluation-harness/cases/refusal-cases-v1.yaml``
models the XSTest paired safe/unsafe design at the metadata level only
(see ``datasets/cards/06-xstest.md``); no dataset content is redistributed.
"""

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

#: The only case-set schema version this loader understands.
CASES_SCHEMA = "p01-cases/v1"

#: Allowed values for ``expected_behavior``: a case either should be
#: complied with (the benign side of the ledger) or refused (the attack
#: side).
EXPECTED_BEHAVIORS = frozenset({"comply", "refuse"})

#: Fields every case must carry — no more, no fewer.
REQUIRED_CASE_FIELDS = ("id", "prompt", "expected_behavior", "category", "provenance")

#: Fields the file's top level must carry.
REQUIRED_TOP_LEVEL_FIELDS = ("schema", "version", "name", "cases")


class CaseSetError(ValueError):
    """Raised when a case-set file fails schema validation (fail-closed)."""


@dataclass(frozen=True)
class Case:
    """One evaluation case: a prompt plus its expected behavior.

    Attributes:
        id: unique, stable case identifier (used for resumability).
        prompt: the prompt text presented to the adapter.
        expected_behavior: ``"comply"`` or ``"refuse"`` — the behavior a
            well-calibrated model should exhibit.
        category: grouping label used for per-category reporting.
        provenance: free-text provenance of this individual case.
    """

    id: str
    prompt: str
    expected_behavior: str
    category: str
    provenance: str


@dataclass(frozen=True)
class CaseSet:
    """A validated, checksummed set of evaluation cases.

    Attributes:
        name: short name from the file (e.g. ``refusal-cases-v1``).
        version: semantic version string from the file.
        description: human description from the file.
        provenance: provenance block from the file (authorship, license,
            design model, ...).
        cases: the cases in file order.
        sha256: SHA-256 hex digest of the exact file bytes — the
            provenance pin recorded in every report.
        path: filesystem path the set was loaded from.
    """

    name: str
    version: str
    description: str
    provenance: Mapping[str, str]
    cases: tuple[Case, ...]
    sha256: str
    path: str

    def ids(self) -> tuple[str, ...]:
        """Return all case ids in file order."""
        return tuple(case.id for case in self.cases)

    def by_id(self) -> dict[str, Case]:
        """Return a mapping from case id to :class:`Case`."""
        return {case.id: case for case in self.cases}

    def categories(self) -> tuple[str, ...]:
        """Return the unique category labels, in first-appearance order."""
        seen: list[str] = []
        for case in self.cases:
            if case.category not in seen:
                seen.append(case.category)
        return tuple(seen)


def _require_str(value: Any, where: str) -> str:
    """Validate that ``value`` is a non-empty string located at ``where``."""
    if not isinstance(value, str) or not value.strip():
        raise CaseSetError(f"{where}: expected a non-empty string, got {value!r}")
    return value


def load_case_set(path: Path | str) -> CaseSet:
    """Load and validate a case set from ``path``.

    Fail-closed: missing file, YAML parse errors, wrong schema version,
    missing/unknown fields, invalid ``expected_behavior`` values, and
    duplicate ids all raise :class:`CaseSetError`.

    Args:
        path: path to the YAML case-set file.

    Returns:
        The validated :class:`CaseSet` (with SHA-256 checksum).

    Raises:
        CaseSetError: on any schema or content violation.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise CaseSetError(f"case set not found or not a file: {file_path}")
    raw = file_path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()

    try:
        data = yaml.safe_load(raw.decode("utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as exc:
        raise CaseSetError(f"{file_path}: YAML parse error: {exc}") from exc

    if not isinstance(data, Mapping):
        raise CaseSetError(f"{file_path}: top level must be a mapping, got {type(data)!r}")

    schema = data.get("schema")
    if schema != CASES_SCHEMA:
        raise CaseSetError(
            f"{file_path}: unsupported schema {schema!r}; this loader only accepts "
            f"{CASES_SCHEMA!r} (fail-closed: upgrade the loader before bumping files)"
        )

    missing_top = [field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in data]
    if missing_top:
        raise CaseSetError(f"{file_path}: missing top-level fields: {missing_top}")

    name = _require_str(data["name"], f"{file_path}: name")
    version = _require_str(data["version"], f"{file_path}: version")
    description = data.get("description", "")
    if not isinstance(description, str):
        raise CaseSetError(f"{file_path}: description must be a string")

    provenance = data.get("provenance", {})
    if not isinstance(provenance, Mapping) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in provenance.items()
    ):
        raise CaseSetError(f"{file_path}: provenance must be a mapping of strings to strings")

    raw_cases = data["cases"]
    if not isinstance(raw_cases, list) or not raw_cases:
        raise CaseSetError(f"{file_path}: cases must be a non-empty list")

    loaded: list[Case] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(raw_cases):
        where = f"{file_path}: cases[{index}]"
        if not isinstance(entry, Mapping):
            raise CaseSetError(f"{where}: each case must be a mapping")
        unknown = [key for key in entry if key not in REQUIRED_CASE_FIELDS]
        if unknown:
            raise CaseSetError(f"{where}: unknown case fields {unknown} (strict schema)")
        missing = [field for field in REQUIRED_CASE_FIELDS if field not in entry]
        if missing:
            raise CaseSetError(f"{where}: missing case fields {missing}")
        case = Case(
            id=_require_str(entry["id"], f"{where}: id"),
            prompt=_require_str(entry["prompt"], f"{where}: prompt"),
            expected_behavior=_require_str(
                entry["expected_behavior"], f"{where}: expected_behavior"
            ),
            category=_require_str(entry["category"], f"{where}: category"),
            provenance=_require_str(entry["provenance"], f"{where}: provenance"),
        )
        if case.expected_behavior not in EXPECTED_BEHAVIORS:
            raise CaseSetError(
                f"{where}: expected_behavior must be one of "
                f"{sorted(EXPECTED_BEHAVIORS)}, got {case.expected_behavior!r}"
            )
        if case.id in seen_ids:
            raise CaseSetError(f"{where}: duplicate case id {case.id!r}")
        seen_ids.add(case.id)
        loaded.append(case)

    return CaseSet(
        name=name,
        version=version,
        description=description,
        provenance=dict(provenance),
        cases=tuple(loaded),
        sha256=sha256,
        path=str(file_path),
    )
