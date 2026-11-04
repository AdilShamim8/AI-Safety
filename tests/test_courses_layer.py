"""Course-layer closure: study-plan lesson refs, companion counts,
watching-companion links, and the honesty ledger.

Session-13 origin (P12): the six-course library had three unchecked
claim surfaces. (1) study-plans.md schedules lessons by abbreviation
('CS 2881 Lecture 8', 'DeepMind P2.2', 'Safeshield M6') — every
reference must resolve to a companion file on disk. (2) Each course
directory carries a companion count (17/8/14/44/16/14 across the six)
and each course page states its own — both are pinned to the disk
classification (companions = lecture-*, f26-lecture-*, m?-??, ch??-??,
part-??-??, module-?? files; crosswalks and pedagogy pages excluded).
(3) Every chapter README's watching-companions block links course
pages that must exist. All three sweeps passed with zero findings, so
this unit is a pin, not a fix.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COURSES = REPO / "courses"
COMPANION_PAT = {
    "boaz-barak-cs2881": r"(lecture-\d|f\d\d-lecture-\d)",
    "cais-ethics-society": r"lecture-\d\d-",
    "campusx-ai-security-guardrails": r"m\d-\d\d",
    "datacamp-ai-security-risk": r"ch\d\d-\d\d",
    "google-deepmind-agi-safety": r"part-\d\d-",
    "safeshield-governance": r"module-\d\d",
}
EXPECTED_COUNTS = {
    "boaz-barak-cs2881": 17,
    "cais-ethics-society": 8,
    "campusx-ai-security-guardrails": 14,
    "datacamp-ai-security-risk": 44,
    "google-deepmind-agi-safety": 16,
    "safeshield-governance": 14,
}


def _companions(course: str) -> list[str]:
    pat = re.compile(COMPANION_PAT[course])
    return [p.name for p in (COURSES / course).glob("*.md") if pat.match(p.name)]


def test_companion_counts_match_disk() -> None:
    for course, expected in EXPECTED_COUNTS.items():
        assert (
            len(_companions(course)) == expected
        ), f"{course}: {len(_companions(course))} companions, expected {expected}"


def test_study_plan_refs_resolve() -> None:
    t = (COURSES / "study-plans.md").read_text(encoding="utf-8")
    boaz = {
        int(re.search(r"lecture-(\d+)", n).group(1))
        for n in _companions("boaz-barak-cs2881")
        if re.match(r"lecture-\d", n)
    }
    for m in re.finditer(r"CS 2881 (?:F26 )?Lecture (\d+)", t):
        assert int(m.group(1)) in boaz, f"study-plans: CS 2881 Lecture {m.group(1)} not on disk"
    dm = {
        mm.group(1)
        for n in _companions("google-deepmind-agi-safety")
        if (mm := re.match(r"part-(\d\d-\d\d)", n))
    }
    for m in re.finditer(r"DeepMind P(\d)\.(\d+)", t):
        key = f"0{m.group(1)}-{int(m.group(2)):02d}"
        assert (
            key in dm
        ), f"study-plans: DeepMind P{m.group(1)}.{m.group(2)} -> part-{key} not on disk"
    ss = {
        mm.group(1)
        for n in _companions("safeshield-governance")
        if (mm := re.match(r"module-(\d\d)", n))
    }
    for m in re.finditer(r"Safeshield M(\d+)", t):
        assert m.group(1).zfill(2) in ss, f"study-plans: Safeshield M{m.group(1)} not on disk"


def test_watching_companion_links_resolve() -> None:
    for d in sorted((REPO / "chapters").glob("[0-9][0-9]-*")):
        t = (d / "README.md").read_text(encoding="utf-8")
        m = re.search(r"[Ww]atching companions?\n(.{0,900})", t, re.S)
        if not m:
            continue
        for mm in re.finditer(r"\]\((\.\./\.\./courses/[^)]+)\)", m.group(1)):
            p = (REPO / mm.group(1).replace("../../", "")).resolve()
            assert p.exists(), f"{d.name[:2]}: broken course link {mm.group(1)}"


def test_course_relative_links_resolve() -> None:
    for f in COURSES.rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", t):
            link = m.group(1)
            if link.startswith(("http", "mailto")):
                continue
            assert (f.parent / link).resolve().exists(), f"{f.relative_to(REPO)}: {link}"


def test_six_courses_each_have_the_four_fixed_pages() -> None:
    for course in EXPECTED_COUNTS:
        for page in ("README.md", "pedagogy.md", "reading-map.md", "self-assessment.md"):
            assert (COURSES / course / page).exists(), f"{course}: missing {page}"
