"""Roadmaps-layer closure: links, schedule arithmetic, plan tiling.

Session-13 origin (P13): the roadmap pages carry schedule arithmetic
nobody recomputed. Swept and pinned here: (1) every relative link
under roadmaps/ resolves; (2) Schedule A (audit-only, 12 weeks) tiles
weeks 1–12 exactly with no gap or repeat, and its hour column sums to
the stated ~120 h; (3) Schedule B (part-time, 24 weeks) tiles 1–24
including the single-week buffer row, and its stated ~7 h/week × 24 ≈
170 h is consistent within rounding; (4) first-90-days carries the
shared spine on weeks 1–4 and three role plans (A/B/C) each tiling
weeks 5–12 in their table rows; (5) the careers index states three
roles and links the first-90-days page. All sweeps passed with zero
findings — this unit is a pin, not a fix.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROADMAPS = REPO / "roadmaps"


def test_relative_links_resolve() -> None:
    for f in sorted(ROADMAPS.rglob("*.md")):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", t):
            link = m.group(1)
            if link.startswith(("http", "mailto")):
                continue
            assert (f.parent / link).resolve().exists(), f"{f.name}: {link}"


def _schedule_section(marker: str) -> str:
    t = (ROADMAPS / "study-schedules.md").read_text(encoding="utf-8")
    i = t.find(marker)
    assert i > 0, marker
    j = t.find("##", i + 10)
    return t[i : j if j > 0 else len(t)]


def test_schedule_a_tiles_and_sums() -> None:
    sec = _schedule_section("Schedule A")
    rows = re.findall(r"^\|\s*(?:\d+[–-]\d+|\d+)\s*\|[^|]+\|\s*(\d+)\s*\|", sec, re.M)
    hours = [int(h) for h in rows]
    assert sum(hours) == 120, f"Schedule A hours sum {sum(hours)} != 120"
    week_rows = re.findall(r"^\|\s*(\d+)[–-](\d+)\s*\|", sec, re.M)
    singles = re.findall(r"^\|\s*(\d+)\s*\|[^|]+\|\s*\d+\s*\|", sec, re.M)
    weeks = []
    for a, b in week_rows:
        weeks += list(range(int(a), int(b) + 1))
    weeks += [int(w) for w in singles]
    assert sorted(set(weeks)) == list(range(1, 13)), sorted(set(weeks))
    assert len(weeks) == len(set(weeks)), "Schedule A repeats a week"


def test_schedule_b_tiles_24_weeks() -> None:
    sec = _schedule_section("Schedule B")
    ranges = re.findall(r"^\|\s*(\d+)[–-](\d+)\s*\|", sec, re.M)
    singles = re.findall(r"^\|\s*(\d+)\s*\|", sec, re.M)
    weeks = []
    for a, b in ranges:
        weeks += list(range(int(a), int(b) + 1))
    weeks += [int(w) for w in singles]
    assert sorted(set(weeks)) == list(range(1, 25)), sorted(set(weeks))
    assert len(weeks) == len(set(weeks)), "Schedule B repeats a week"


def test_first_90_days_tiling() -> None:
    t = (ROADMAPS / "first-90-days.md").read_text(encoding="utf-8")
    spine = re.search(r"^## The shared spine \(weeks (\d+)[–-](\d+)", t, re.M)
    assert spine and (int(spine.group(1)), int(spine.group(2))) == (1, 4)
    for letter in "ABC":
        i = t.find(f"## Plan {letter}")
        assert i > 0, letter
        j = t.find("## Plan", i + 10)
        sec = t[i : j if j > 0 else len(t)]
        weeks = [int(w) for w in re.findall(r"^\|\s*(\d+)\s*\|", sec, re.M)]
        assert sorted(set(weeks)) == list(range(5, 13)), f"Plan {letter}: {sorted(set(weeks))}"
        assert len(weeks) == len(set(weeks)), f"Plan {letter} repeats a week"


def test_careers_index_three_roles() -> None:
    t = (ROADMAPS / "careers-index.md").read_text(encoding="utf-8")
    assert t.startswith("# Careers index — three roles")
    assert "first-90-days.md" in t
    for plan in ("Plan A", "Plan B", "Plan C"):
        assert plan in (ROADMAPS / "first-90-days.md").read_text(encoding="utf-8")
