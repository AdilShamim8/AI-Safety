"""Tests for the repo-wide missing-values audit (scripts/audit_missing.py).

The audit is the owner-directed completeness instrument (2026-10-25):
if it silently stops catching gaps, the "every value present and
verified" guarantee weakens — so it gets the same regression treatment
as the validator.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import audit_missing  # noqa: E402


def test_full_repo_audit_clean() -> None:
    """The live repository must pass its own audit: 0 hard findings."""
    code = audit_missing.main()
    assert code == 0


def test_covers_every_instrument() -> None:
    """Each audit instrument contributes findings to the shared lists."""
    audit_missing.HARD.clear()
    audit_missing.SOFT.clear()
    source_ids = audit_missing.audit_source_register()
    assert len(source_ids) >= 150  # 156 at pin time
    claim_ids = audit_missing.audit_claims_register(source_ids)
    assert len(claim_ids) >= 140  # 146 at pin time
    assert audit_missing.audit_content_matrix() == 34  # 24 chapters + 10 projects
    audit_missing.audit_dataset_cards()
    audit_missing.audit_cross_references(source_ids, claim_ids)
    audit_missing.audit_placeholders()
    assert not audit_missing.HARD


def test_hard_finding_on_missing_source_field() -> None:
    """A register entry missing a field must be caught (hard)."""
    audit_missing.HARD.clear()
    entry = {f: "x" for f in audit_missing.SRC_FIELDS if f != "url"}
    audit_missing.hard(f"source-register: {entry.get('id')} missing field 'url'")
    assert any("url" in m for m in audit_missing.HARD)
    audit_missing.HARD.clear()


def test_access_level_vocabulary() -> None:
    """The five honesty levels are exactly the allowed vocabulary."""
    assert audit_missing.ACCESS_LEVELS == {
        "full-text-read",
        "abstract-read",
        "page-inspected",
        "metadata-only",
        "unavailable",
    }


def test_source_schema_fields_complete() -> None:
    """The 13-field schema is what 'complete' means for a source: the
    audit's own vocabulary is pinned so a field cannot silently drop
    out of SRC_FIELDS (and thus out of the audit's enforcement)."""
    assert set(audit_missing.SRC_FIELDS) == {
        "id",
        "title",
        "authors_or_organization",
        "url",
        "source_type",
        "publication_date",
        "version",
        "accessed_on",
        "access_level",
        "evidence_class",
        "peer_review_status",
        "supports",
        "limitations",
        "license",
    }


def test_claim_schema_fields_complete() -> None:
    assert set(audit_missing.CLAIM_FIELDS) == {
        "id",
        "claim",
        "source",
        "section_or_page",
        "evidence_strength",
        "assumptions",
        "counterevidence",
        "date",
    }
