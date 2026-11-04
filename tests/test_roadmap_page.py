"""ROADMAP page consistency: the route diagram vs the route pages.

Session-13 origin (P20): the ASCII route diagram's ALIGNMENT project
line said "P04,P05,P06" while the alignment route page schedules P02
in week 5 (it attaches to Ch.03, an alignment-route chapter) — the
diagram was written before P02 landed and never resynced. Fixed; the
pin now requires the diagram's project line for each route to be a
subset of the projects its route page actually schedules, and the
shared projects (P08 on two routes, P10 capstone on all) stay stated.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROADMAP = (REPO / "ROADMAP.md").read_text(encoding="utf-8")
ROUTES = {
    "alignment-research.md": "ALIGNMENT",
    "ai-security-engineering.md": "AI SECURITY",
    "evaluations-and-assurance.md": "EVALUATIONS &",
}


def _diagram() -> str:
    i = ROADMAP.find("COMMON SPINE")
    j = ROADMAP.find("```", i + 10)
    assert i > 0 and j > i
    return ROADMAP[i:j]


def test_alignment_diagram_lists_p02() -> None:
    assert "P02,P04,P05,P06 P07 (+P08 shared)" in _diagram()


def test_diagram_projects_subset_of_route_pages() -> None:
    """The project line is the diagram row that starts with a P-list;
    split it into the three route columns by their known contents."""
    d = _diagram()
    line = None
    for row in d.split("\n"):
        if re.match(r" P\d\d", row) and "P10" not in row:
            line = row
            break
    assert line, "project line not found in diagram"
    # column split by the three known anchors: alignment first, the
    # '(+P08 shared)' marker ends the security column
    m = re.match(r" ([A-Z0-9,]+)\s+(P\d+ \(\+P\d+ shared\))\s+(P[\d,]+)", line)
    assert m, f"project line not parsed: {line!r}"
    cols = {
        "alignment-research.md": m.group(1),
        "ai-security-engineering.md": m.group(2),
        "evaluations-and-assurance.md": m.group(3),
    }
    for page, col in cols.items():
        page_text = (REPO / "roadmaps" / page).read_text(encoding="utf-8")
        for pid in re.findall(r"P\d\d", col):
            assert pid in page_text, f"{page}: diagram lists {pid} but route page never mentions it"


def test_shared_projects_stay_stated() -> None:
    d = _diagram()
    assert "+P08 shared" in d
    assert "P10 CAPSTONE" in d


def test_roadmap_relative_links_resolve() -> None:
    for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", ROADMAP):
        link = m.group(1)
        if link.startswith(("http", "mailto")):
            continue
        assert (REPO / "ROADMAP.md").parent.joinpath(link).resolve().exists(), link
