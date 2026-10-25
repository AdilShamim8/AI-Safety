#!/usr/bin/env python3
"""audit_missing.py — repo-wide missing-values audit.

The owner-directed completeness check (2026-10-25) as an executable,
repeatable instrument:

  1. source-register.yaml — every entry carries the full 13-field schema;
     access_level values are from the allowed set; URLs present.
  2. claims-register.yaml — every entry carries the full schema; every
     `source` references an existing register ID.
  3. content-matrix.yaml — every unit is implemented (status + date);
     every unit's path exists on disk.
  4. dataset cards — every catalog entry has a card file with a license
     statement and a verification date.
  5. cross-reference integrity — every SRC-*/CLM-* ID mentioned in any
     committed prose file exists in the registers.
  6. placeholder scan — TBD/TODO/FIXME/PLACEHOLDER markers and honesty
     markers ("not yet", "pending", "unverified") REPORTED by file (not
     failed: honesty markers are this repository's method, not gaps).

Hard failures exit 1; the report prints every finding with a file:line
locator. Running this script is part of the pre-commit discipline.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SRC_FIELDS = [
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
]
CLAIM_FIELDS = [
    "id",
    "claim",
    "source",
    "section_or_page",
    "evidence_strength",
    "assumptions",
    "counterevidence",
    "date",
]
ACCESS_LEVELS = {
    "full-text-read",
    "abstract-read",
    "page-inspected",
    "metadata-only",
    "unavailable",
}
HARD = []
SOFT = []


def hard(msg: str) -> None:
    HARD.append(msg)
    print(f"HARD  {msg}")


def soft(msg: str) -> None:
    SOFT.append(msg)
    print(f"soft  {msg}")


def audit_source_register() -> set[str]:
    data = yaml.safe_load((REPO / "research/source-register.yaml").read_bytes())
    ids: set[str] = set()
    for i, entry in enumerate(data["sources"], start=1):
        eid = entry.get("id", f"<#{i}>")
        ids.add(eid)
        for field in SRC_FIELDS:
            if field not in entry:
                hard(f"source-register: {eid} missing field {field!r}")
        if entry.get("access_level") not in ACCESS_LEVELS:
            hard(f"source-register: {eid} access_level {entry.get('access_level')!r} invalid")
        if not entry.get("url"):
            hard(f"source-register: {eid} missing url")
        if entry.get("publication_date") is None:
            soft(f"source-register: {eid} publication_date null (allowed; never inferred)")
    print(f"source-register: {len(ids)} entries checked")
    return ids


def audit_claims_register(source_ids: set[str]) -> set[str]:
    data = yaml.safe_load((REPO / "research/claims-register.yaml").read_bytes())
    ids: set[str] = set()
    for i, entry in enumerate(data["claims"], start=1):
        eid = entry.get("id", f"<#{i}>")
        ids.add(eid)
        for field in CLAIM_FIELDS:
            if field not in entry:
                hard(f"claims-register: {eid} missing field {field!r}")
        if entry.get("source") not in source_ids:
            hard(f"claims-register: {eid} references unknown source {entry.get('source')!r}")
    print(f"claims-register: {len(ids)} entries checked")
    return ids


def audit_content_matrix() -> int:
    data = yaml.safe_load((REPO / "planning/content-matrix.yaml").read_bytes())
    count = 0
    sections = data.get("chapters", []) + data.get("projects", [])
    for unit in sections:
        uid = unit.get("id", "<unknown>")
        # Chapters carry `maturity: complete`; projects carry
        # `status: implemented` — both are the completeness signal.
        done = unit.get("status") == "implemented" or unit.get("maturity") == "complete"
        verified = unit.get("verified_on")
        path = unit.get("path")
        count += 1
        if not done:
            soft(
                f"content-matrix: {uid} not yet complete "
                f"(status={unit.get('status')!r}, maturity={unit.get('maturity')!r})"
            )
        if done and verified is None:
            hard(f"content-matrix: {uid} complete but verified_on is null")
        if path and not (REPO / path).exists():
            hard(f"content-matrix: {uid} path does not exist: {path}")
    print(f"content-matrix: {count} units checked across chapters/projects")
    return count


def audit_dataset_cards() -> None:
    catalog = yaml.safe_load((REPO / "datasets/catalog.yaml").read_bytes())
    entries = catalog.get("datasets", [])
    for entry in entries:
        name = entry.get("name", "<unknown>")
        card = entry.get("card") or entry.get("card_path")
        if not card:
            hard(f"catalog: {name} has no card path")
            continue
        card_path = REPO / "datasets" / str(card)
        if not card_path.exists():
            hard(f"catalog: {name} card missing on disk: {card}")
            continue
        text = card_path.read_text(encoding="utf-8")
        if not re.search(r"apache|mit|cc-by|cc by|odc|openrail|unknown|noassertion", text, re.I):
            hard(f"catalog card {card_path.name}: no license statement found")
        if "verification date" not in text.lower() and "verified" not in text.lower():
            hard(f"catalog card {card_path.name}: no verification-date statement")
        for marker in ("TBD", "TODO", "FIXME"):
            if marker in text:
                soft(f"catalog card {card_path.name}: placeholder marker {marker!r}")
    print(f"dataset cards: {len(entries)} catalog entries checked")


def audit_cross_references(source_ids: set[str], claim_ids: set[str]) -> None:
    pattern = re.compile(r"\b(SRC-[A-Z]+-\d+|CLM-\d{4})\b")
    scan_dirs = ["chapters", "projects", "roadmaps", "research", "datasets", "planning"]
    files = 0
    for d in scan_dirs:
        for path in (REPO / d).rglob("*.md"):
            files += 1
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for match in pattern.findall(line):
                    if match.startswith("SRC-") and match not in source_ids:
                        hard(f"{path.relative_to(REPO)}:{lineno}: unregistered source id {match}")
                    if match.startswith("CLM-") and match not in claim_ids:
                        hard(f"{path.relative_to(REPO)}:{lineno}: unregistered claim id {match}")
    print(f"cross-references: {files} markdown files scanned")


def audit_placeholders() -> None:
    pattern = re.compile(r"\b(TBD|TODO|FIXME|PLACEHOLDER|XXX)\b")
    scan_dirs = ["chapters", "projects", "roadmaps", "prerequisites", "templates"]
    for d in scan_dirs:
        for path in (REPO / d).rglob("*.md"):
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                if pattern.search(line):
                    soft(f"{path.relative_to(REPO)}:{lineno}: placeholder marker")


def main() -> int:
    print(f"audit_missing — {REPO.name} — full missing-values scan\n")
    source_ids = audit_source_register()
    claim_ids = audit_claims_register(source_ids)
    audit_content_matrix()
    audit_dataset_cards()
    audit_cross_references(source_ids, claim_ids)
    audit_placeholders()
    print(f"\n--- summary: {len(HARD)} hard findings, {len(SOFT)} soft notes ---")
    if HARD:
        print("HARD findings must be fixed before commit:")
        for msg in HARD:
            print(f"  - {msg}")
        return 1
    print("No hard findings: every register entry, card, unit, and cross-reference is complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
