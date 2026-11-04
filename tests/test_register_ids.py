"""Register id uniqueness and the no-collision rule.

Session-13 origin (P07): the 2026-11-03 course claims were given
CLM-0207..0218 — a block already occupied by the 2026-10-25 paper
claims, so twelve ids carried two entries each. The audit that found
it ran on the raw yaml with a Counter; the fix renumbered the course
block to CLM-0224..0235 (after the then-max 223). These tests make
id collisions impossible to ship: uniqueness, prefix format, and —
the rule that would have caught this case — no two claims may share
an id, with a message naming both sources so the next collision is
diagnosed in seconds.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent


def _claims() -> list[dict]:
    return yaml.safe_load((REPO / "research" / "claims-register.yaml").read_bytes())["claims"]


def _sources() -> list[dict]:
    return yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())["sources"]


def test_claim_ids_are_unique() -> None:
    claims = _claims()
    counts = Counter(c["id"] for c in claims)
    dups = {k: v for k, v in counts.items() if v > 1}
    assert not dups, "duplicate claim ids (the S13-P07 collision class): " + "; ".join(
        f"{cid} -> {[c['source'] for c in claims if c['id'] == cid]}" for cid in dups
    )


def test_claim_id_prefix_and_width() -> None:
    for c in _claims():
        assert c["id"].startswith("CLM-") and len(c["id"]) == 8 and c["id"][4:].isdigit(), c["id"]


def test_claim_sources_all_exist() -> None:
    src_ids = {s["id"] for s in _sources()}
    for c in _claims():
        assert c["source"] in src_ids, f"{c['id']}: source {c['source']} not in register"


def test_course_block_is_the_renumbered_one() -> None:
    """The 12 course claims carry CLM-0224..0235 and course sources; the
    paper twins keep their original ids with paper sources. If a future
    edit swaps these back, this fails with both sides named."""
    claims = _claims()
    course = {c["id"]: c for c in claims if c["id"] >= "CLM-0224" and c["id"] <= "CLM-0235"}
    assert len(course) == 12, sorted(course)
    for cid, c in course.items():
        assert str(c["source"]).startswith("SRC-CURR-01"), (cid, c["source"])
    for old in ("CLM-0207", "CLM-0213"):
        twin = [c for c in claims if c["id"] == old]
        assert len(twin) == 1 and str(twin[0]["source"]).startswith("SRC-"), (old, twin)


def test_evidence_strength_is_stated_for_every_claim() -> None:
    for c in _claims():
        es = c.get("evidence_strength", "")
        assert (
            es and len(es) >= 20
        ), f"{c['id']}: evidence_strength missing or too thin to be honest"
