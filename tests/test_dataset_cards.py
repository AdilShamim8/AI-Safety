"""Dataset catalog ↔ card closure and the boundary-section rule.

Session-13 origin (P10): the catalog's 47 rows and the cards directory
were closed one-to-one (no missing card files, no orphan cards, no
shared rows) and every size fact number appears in its card's text —
all verified here so that stays true. The sweep's one real finding:
the four newest cards (GDPval, METR RE-bench, METR time-horizons,
Canaries) shipped with the five-section schema, missing the
"What this dataset CANNOT support" boundary section that cards 01-43
carry and that the register's access-level promises rest on; section
six was added to each, grounded in each card's own recorded access
level. Also pinned: the verified_on field mixes yaml dates and
strings (normalized here), course_use chapter/project refs must be
in-tree, and every R-id used by a size fact must exist in that row's
references.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CAT = yaml.safe_load((REPO / "datasets" / "catalog.yaml").read_bytes())["datasets"]
CHDIRS = {d.name.split("-")[0] for d in (REPO / "chapters").glob("[0-9][0-9]-*")}


def test_catalog_and_cards_are_one_to_one() -> None:
    for row in CAT:
        card = REPO / "datasets" / row["card"]
        assert card.exists(), f"{row['id']}: card file {row['card']} missing"
    by_card = Counter(row["card"] for row in CAT)
    assert all(v == 1 for v in by_card.values())
    disk = {f"cards/{c.name}" for c in (REPO / "datasets" / "cards").glob("*.md")}
    stated = {row["card"] for row in CAT}
    assert disk == stated, f"orphan cards: {sorted(disk - stated)}"


def test_every_card_carries_a_boundary_section() -> None:
    """Three boundary wordings exist across card generations ('What this
    dataset CANNOT support', the lowercase variant, 'Honest limitations
    (this card)'); any one of the three satisfies the rule."""
    for c in sorted((REPO / "datasets" / "cards").glob("*.md")):
        t = c.read_text(encoding="utf-8")
        ok = (
            "CANNOT support" in t
            or "cannot support" in t.lower()
            or "Honest limitations (this card)" in t
        )
        assert ok, f"{c.name}: no honest-boundary section in any wording"


def test_size_facts_appear_in_card_text() -> None:
    for row in CAT:
        t = (REPO / "datasets" / row["card"]).read_text(encoding="utf-8").replace(",", "")
        for fact in row.get("size_facts") or []:
            s = str(fact.get("fact", ""))
            for n in re.findall(r"[\d,]+(?:\.\d+)?", s):
                v = n.replace(",", "")
                if v.isdigit() and len(v) >= 3:
                    assert v in t, f"{row['id']}: size {n!r} not on card ({s[:50]!r})"


def test_course_use_refs_are_in_tree() -> None:
    for row in CAT:
        cu = row.get("course_use") or {}
        for ch in cu.get("chapters") or []:
            assert ch in CHDIRS, f"{row['id']}: chapter {ch}"
        for pr in cu.get("projects") or []:
            assert re.fullmatch(r"P\d\d", pr), f"{row['id']}: project {pr!r}"


def test_size_fact_ref_ids_exist() -> None:
    for row in CAT:
        ref_ids = {r["id"] for r in (row.get("references") or [])}
        for fact in row.get("size_facts") or []:
            r = str(fact.get("ref", ""))
            if r:
                assert r in ref_ids, f"{row['id']}: size fact cites {r!r}, not in references"


def test_verified_on_is_stated_for_every_row() -> None:
    for row in CAT:
        v = str(row.get("verified_on", ""))
        assert re.match(r"^2026-\d\d-\d\d", v), f"{row['id']}: verified_on {v!r}"
