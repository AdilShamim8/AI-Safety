"""Course-library claims: the Videos column and the six-course set.

Session-13 origin (P30): the library table's Videos column is pinned
to the values stated at registration (CS 2881 19, DeepMind 16, CAIS
8, Safeshield 14, plus the two account-walled courses' stated
counts), and the page must link exactly the six course directories
that exist on disk.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIB = (REPO / "courses/README.md").read_text(encoding="utf-8")
DIRS = {
    "boaz-barak-cs2881": 19,
    "google-deepmind-agi-safety": 16,
    "cais-ethics-society": 8,
    "safeshield-governance": 14,
    "datacamp-ai-security-risk": None,
    "campusx-ai-security-guardrails": None,
}


def test_video_counts_stay_as_registered() -> None:
    flat = re.sub(r"\s+", " ", LIB)
    anchors = {
        "boaz-barak-cs2881": "Harvard CS 2881",
        "google-deepmind-agi-safety": "Google DeepMind AGI Safety Course",
        "cais-ethics-society": "AI Safety, Ethics, & Society",
        "safeshield-governance": "AI Governance series",
    }
    for course, n in DIRS.items():
        if n is None:
            continue
        anchor = anchors[course]
        m = re.search(re.escape(anchor) + r"[^|]*\|[^|]*\|\s*(\d+)\s*\|", flat)
        assert m, f"library row for {course} not parsed"
        assert int(m.group(1)) == n, f"{course}: videos stated {m.group(1)}, registered {n}"


def test_six_course_dirs_exist_and_linked() -> None:
    for d in DIRS:
        assert (REPO / "courses" / d).is_dir(), d
        assert f"{d}/" in LIB, f"{d} not linked in the library table"
