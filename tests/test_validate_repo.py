"""Tests for the repository pre-commit validator.

The validator enforces the honesty infrastructure (register schemas, local
link integrity, artifact hygiene), so it gets its own regression tests: if
the validator silently stops catching violations, every downstream guarantee
weakens.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_repo  # noqa: E402

FULL_SOURCE_ENTRY = """\
sources:
  - id: SRC-TEST-001
    title: "t"
    authors_or_organization: "t"
    url: "https://example.com"
    source_type: commentary
    publication_date: null
    version: null
    accessed_on: 2026-10-21
    access_level: page-inspected
    evidence_class: synthesis
    peer_review_status: unknown
    supports: ["x"]
    limitations: "t"
    license: unknown
"""


def _make_git_repo(tmp_path: Path) -> Path:
    (tmp_path / ".git").mkdir()
    return tmp_path


def test_repo_itself_passes_validation():
    errors = (
        validate_repo.check_yaml(REPO_ROOT)
        + validate_repo.check_links(REPO_ROOT)
        + validate_repo.check_sizes(REPO_ROOT)
    )
    assert errors == [], errors


def test_broken_local_link_is_caught(tmp_path):
    _make_git_repo(tmp_path)
    (tmp_path / "page.md").write_text("[missing](nope.md)\n", encoding="utf-8")
    errors = validate_repo.check_links(tmp_path)
    assert any("nope.md" in e for e in errors), errors


def test_external_and_anchor_links_are_ignored(tmp_path):
    _make_git_repo(tmp_path)
    (tmp_path / "page.md").write_text(
        "[ok](https://example.com) [anchor](#section) [mail](mailto:a@b.c)\n",
        encoding="utf-8",
    )
    assert validate_repo.check_links(tmp_path) == []


def test_missing_register_fields_are_caught(tmp_path):
    _make_git_repo(tmp_path)
    research = tmp_path / "research"
    research.mkdir()
    (research / "source-register.yaml").write_text(
        "sources:\n  - id: SRC-X\n    title: x\n", encoding="utf-8"
    )
    errors = validate_repo.check_yaml(tmp_path)
    assert any("SRC-X" in e and "missing fields" in e for e in errors), errors


def test_invalid_access_level_is_caught(tmp_path):
    _make_git_repo(tmp_path)
    research = tmp_path / "research"
    research.mkdir()
    bad = FULL_SOURCE_ENTRY.replace("page-inspected", "skimmed")
    (research / "source-register.yaml").write_text(bad, encoding="utf-8")
    errors = validate_repo.check_yaml(tmp_path)
    assert any("invalid access_level" in e for e in errors), errors


def test_valid_register_entry_passes(tmp_path):
    _make_git_repo(tmp_path)
    research = tmp_path / "research"
    research.mkdir()
    (research / "source-register.yaml").write_text(FULL_SOURCE_ENTRY, encoding="utf-8")
    assert validate_repo.check_yaml(tmp_path) == []


def test_oversize_file_is_caught(tmp_path):
    _make_git_repo(tmp_path)
    big = tmp_path / "big.bin"
    big.write_bytes(b"x" * (validate_repo.MAX_FILE_BYTES + 1))
    errors = validate_repo.check_sizes(tmp_path)
    assert any("big.bin" in e for e in errors), errors
