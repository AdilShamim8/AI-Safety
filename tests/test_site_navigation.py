"""The navigation contract: every reading surface carries its way out.

Session 5 gave every markdown surface one uniform nav line under its
H1 (chapters also got a closing pointer to their successor), because
on a phone GitHub's own prev/next affordances are weakest and a
reader entering from search could land on a solutions file with no
way back. These tests pin the promise: the line exists, and every
link on it resolves to a real file.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIRS = sorted(
    d.name for d in (REPO_ROOT / "chapters").iterdir() if d.is_dir() and d.name[0].isdigit()
)

HUBS = [
    "courses/README.md",
    "courses/boaz-barak-cs2881/README.md",
    "courses/google-deepmind-agi-safety/README.md",
    "courses/cais-ethics-society/README.md",
    "courses/safeshield-governance/README.md",
    "courses/study-plans.md",
    "courses/how-courses-organize.md",
    "roadmaps/alignment-research.md",
    "roadmaps/ai-security-engineering.md",
    "roadmaps/evaluations-and-assurance.md",
    "roadmaps/audit-only.md",
    "roadmaps/careers-index.md",
    "roadmaps/first-90-days.md",
    "roadmaps/study-schedules.md",
    "roadmaps/progress/README.md",
    "prerequisites/diagnostic.md",
    "prerequisites/targeted-refreshers.md",
    "prerequisites/verifying-sources.md",
    "datasets/README.md",
    "research/notes/README.md",
]


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _links(line: str) -> list[str]:
    return re.findall(r"\]\(([^)#]+?)(?:#[^)]*)?\)", line)


def test_every_chapter_carries_nav_and_next() -> None:
    for d in CHAPTER_DIRS:
        rel = f"chapters/{d}/README.md"
        text = _read(rel)
        nav = [ln for ln in text.splitlines() if ln.startswith("**Chapter nav:**")]
        assert nav, f"{rel}: no chapter-nav line"
        for target in _links(nav[0]):
            assert (REPO_ROOT / "chapters" / d / target).exists(), (rel, target)
        tail = [
            ln
            for ln in text.splitlines()
            if ln.startswith("**Next:**") or ln.startswith("**Course complete.**")
        ]
        assert tail, f"{rel}: no closing next pointer"
        for target in _links(tail[0]):
            assert (REPO_ROOT / "chapters" / d / target).exists(), (rel, target)


def test_every_solutions_file_carries_back_nav() -> None:
    for d in CHAPTER_DIRS:
        rel = f"chapters/{d}/solutions.md"
        text = _read(rel)
        nav = [ln for ln in text.splitlines() if ln.startswith("**Navigate:**")]
        assert nav, f"{rel}: no navigate line"
        for target in _links(nav[0]):
            assert (REPO_ROOT / "chapters" / d / target).exists(), (rel, target)


def test_hub_pages_carry_navigate_lines() -> None:
    for h in HUBS:
        assert "**Navigate:**" in _read(h), f"{h}: no navigate line"


def test_hub_nav_links_resolve() -> None:
    for h in HUBS:
        text = _read(h)
        nav = [ln for ln in text.splitlines() if ln.startswith("**Navigate:**")]
        assert nav, h
        base = (REPO_ROOT / h).parent
        for target in _links(nav[0]):
            assert (base / target).exists(), (h, target)
