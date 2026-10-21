"""Tests for the P01 case-set loader (schema validation, checksums).

Covers the committed 24-case synthetic fixture and the fail-closed
contract: unknown schema versions, missing/unknown fields, invalid
expected behaviors, duplicate ids, and missing files must all raise
:class:`CaseSetError` — never load silently.
"""

import hashlib
import re
from collections import Counter
from pathlib import Path

import pytest

from ai_safety_course.evaluation.cases import (
    CASES_SCHEMA,
    CaseSetError,
    load_case_set,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_PATH = REPO_ROOT / "projects" / "p01-evaluation-harness" / "cases" / "refusal-cases-v1.yaml"

VALID_MINIMAL = """\
schema: "p01-cases/v1"
version: "0.0.1-test"
name: "tiny"
cases:
  - id: "A-1"
    prompt: "safe prompt"
    expected_behavior: "comply"
    category: "cat-a"
    provenance: "synthetic"
  - id: "B-1"
    prompt: "unsafe prompt"
    expected_behavior: "refuse"
    category: "cat-a"
    provenance: "synthetic"
"""


def _write(tmp_path: Path, text: str, name: str = "cases.yaml") -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_committed_case_set_loads_with_expected_shape():
    case_set = load_case_set(CASES_PATH)
    assert len(case_set.cases) == 24
    assert case_set.version == "1.0.0"
    assert case_set.name == "refusal-cases-v1"
    behaviors = Counter(case.expected_behavior for case in case_set.cases)
    assert behaviors == {"comply": 12, "refuse": 12}
    categories = Counter(case.category for case in case_set.cases)
    assert set(categories.values()) == {4}
    assert len(categories) == 6
    # every category pairs two safe with two unsafe cases (XSTest-style pairing)
    for category in categories:
        side = Counter(
            case.expected_behavior for case in case_set.cases if case.category == category
        )
        assert side == {"comply": 2, "refuse": 2}, category


def test_committed_case_set_provenance_declares_synthetic():
    case_set = load_case_set(CASES_PATH)
    assert "synthetic" in case_set.provenance["authorship"]
    assert "metadata level" in case_set.provenance["design_model"]
    assert all(case.provenance for case in case_set.cases)


def test_checksum_matches_file_bytes_and_is_stable():
    case_set_a = load_case_set(CASES_PATH)
    case_set_b = load_case_set(CASES_PATH)
    digest = hashlib.sha256(CASES_PATH.read_bytes()).hexdigest()
    assert re.fullmatch(r"[0-9a-f]{64}", case_set_a.sha256)
    assert case_set_a.sha256 == case_set_b.sha256 == digest


def test_checksum_changes_when_content_changes(tmp_path):
    path = _write(tmp_path, VALID_MINIMAL)
    first = load_case_set(path)
    path.write_text(VALID_MINIMAL.replace("safe prompt", "other prompt"), encoding="utf-8")
    second = load_case_set(path)
    assert first.sha256 != second.sha256


def test_ids_unique_and_in_file_order():
    case_set = load_case_set(CASES_PATH)
    ids = case_set.ids()
    assert len(ids) == len(set(ids))
    assert ids[0] == case_set.cases[0].id
    assert case_set.by_id()["HC-SAFE-01"].category == "household-chemicals"
    assert case_set.categories()[0] == case_set.cases[0].category


def test_unknown_schema_version_is_rejected(tmp_path):
    path = _write(tmp_path, VALID_MINIMAL.replace(CASES_SCHEMA, "p01-cases/v2"))
    with pytest.raises(CaseSetError, match="unsupported schema"):
        load_case_set(path)


def test_missing_top_level_field_is_rejected(tmp_path):
    path = _write(tmp_path, VALID_MINIMAL.replace('name: "tiny"\n', ""))
    with pytest.raises(CaseSetError, match="missing top-level fields"):
        load_case_set(path)


def test_missing_case_field_is_rejected(tmp_path):
    text = VALID_MINIMAL.replace('    category: "cat-a"\n', "", 1)
    path = _write(tmp_path, text)
    with pytest.raises(CaseSetError, match="missing case fields"):
        load_case_set(path)


def test_unknown_case_field_is_rejected(tmp_path):
    text = VALID_MINIMAL.replace(
        '    provenance: "synthetic"',
        '    provenance: "synthetic"\n    difficulty: "hard"',
        1,
    )
    path = _write(tmp_path, text)
    with pytest.raises(CaseSetError, match="unknown case fields"):
        load_case_set(path)


def test_invalid_expected_behavior_is_rejected(tmp_path):
    text = VALID_MINIMAL.replace('expected_behavior: "refuse"', 'expected_behavior: "maybe"')
    path = _write(tmp_path, text)
    with pytest.raises(CaseSetError, match="expected_behavior"):
        load_case_set(path)


def test_duplicate_case_id_is_rejected(tmp_path):
    text = VALID_MINIMAL.replace('id: "B-1"', 'id: "A-1"')
    path = _write(tmp_path, text)
    with pytest.raises(CaseSetError, match="duplicate case id"):
        load_case_set(path)


def test_missing_file_is_rejected(tmp_path):
    with pytest.raises(CaseSetError, match="not found"):
        load_case_set(tmp_path / "nope.yaml")


def test_non_mapping_top_level_is_rejected(tmp_path):
    path = _write(tmp_path, "- just\n- a\n- list\n")
    with pytest.raises(CaseSetError, match="top level must be a mapping"):
        load_case_set(path)


def test_broken_yaml_is_rejected(tmp_path):
    path = _write(tmp_path, "schema: [unclosed\n")
    with pytest.raises(CaseSetError, match="YAML parse error"):
        load_case_set(path)
