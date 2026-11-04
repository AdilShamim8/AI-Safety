"""Comparison-note layer: the twelve-note set and the fixed header.

Session-13 origin (P24): comparison-01's header still said '1 of 5
planned (the others: ...)' — written when only one comparison existed,
stale for weeks while the set grew to twelve. The header now states
the twelve-note reality; this module pins it and sweeps the set:
twelve files exist, each cites material that resolves (register ids,
sibling notes, or incident notes), and each states the practitioner
question that the reading-map promises comparisons carry.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
NOTES = REPO / "research" / "notes"
COMPS = sorted(NOTES.glob("comparison-*.md"))
SRC_IDS = {
    s["id"]
    for s in yaml.safe_load((REPO / "research/source-register.yaml").read_bytes())["sources"]
}


def test_twelve_comparisons_exist() -> None:
    assert len(COMPS) == 12, len(COMPS)


def test_the_fixed_header_stays() -> None:
    t = (NOTES / "comparison-01-rlhf-vs-dpo-vs-rlaif.md").read_text(encoding="utf-8")
    assert "twelve-note set" in t
    assert "1 of 5 planned" not in t


def test_every_comparison_carries_the_practitioner_question() -> None:
    for c in COMPS:
        t = c.read_text(encoding="utf-8")
        ok = "ractitioner" in t or "uestion" in t
        assert ok, f"{c.name}: no question posed"


def test_comparison_citations_resolve() -> None:
    note_ids = {p.name for p in NOTES.glob("*.md")}
    inc_ids = {p.name for p in (NOTES / "incidents").glob("*.md") if p.name != "README.md"}
    for c in COMPS:
        t = c.read_text(encoding="utf-8")
        for m in re.finditer(r"\bSRC-[A-Z]+-\d+[a-z]?\b", t):
            assert m.group(0) in SRC_IDS, f"{c.name}: {m.group(0)} not in register"
        for m in re.finditer(r"notes/(\d+-[a-z-]+\.md)", t):
            assert m.group(1) in note_ids, f"{c.name}: notes/{m.group(1)} missing"
        for m in re.finditer(r"incidents/([0-9a-z-]+\.md)", t):
            assert m.group(1) in inc_ids, f"{c.name}: incidents/{m.group(1)} missing"
