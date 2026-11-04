"""Incident-file layer: template discipline and era coverage.

Session-13 origin (P23): the 14 incident reviews carry a strict
template (observable facts, attributed conclusions, named unknowns,
and a mandatory what-this-does-NOT-demonstrate section) and sit in
four eras whose ranges the incidents README states. Pinned here:
every incident file carries all four template sections, every
incident number 01-14 exists exactly once, and the README's era
ranges tile that span without gaps or overlaps.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INC = REPO / "research" / "notes" / "incidents"
FILES = sorted(f for f in INC.glob("*.md") if f.name != "README.md")


def test_fourteen_incidents_unique_numbers() -> None:
    nums = [int(f.name.split("-")[0]) for f in FILES]
    assert sorted(nums) == list(range(1, 15)), nums
    assert len(nums) == len(set(nums))


def test_every_incident_carries_the_template_sections() -> None:
    for f in FILES:
        t = f.read_text(encoding="utf-8").lower()
        assert "observable" in t, f"{f.name}: no observable-facts section"
        assert "established" in t, f"{f.name}: no established/attribution section"
        ok = any(w in t for w in ("limitation", "counterevidence", "assumption", "unrecorded"))
        assert ok, f"{f.name}: no limitations/assumptions section in any wording"
        assert (
            "does not demonstrate" in t or "does NOT demonstrate" in t
        ), f"{f.name}: no what-this-does-NOT-demonstrate section"


def test_eras_tile_the_span() -> None:
    t = (INC / "README.md").read_text(encoding="utf-8")
    ranges = re.findall(r"(\d{2})[–-](\d{2})", t)
    weeks = []
    for a, b in ranges:
        weeks += list(range(int(a), int(b) + 1))
    assert weeks, "no era ranges found in the incidents README"
    lo, hi = min(weeks), max(weeks)
    cover = [w for w in weeks if lo <= w <= hi]
    assert sorted(set(cover)) == list(range(lo, hi + 1)), "era ranges leave gaps"
