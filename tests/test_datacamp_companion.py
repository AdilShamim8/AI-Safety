"""The session-10 companion layer's own contract test.

The fifth course (DataCamp, added 2026-11-03) differs from the four
video courses: its lessons are interactive and graded, half of them
gamified, and its content is account-walled. This file pins what that
difference implies for the companion layer:

  1. the honesty basis — every exercise note states the account wall
     and reconstructs rather than reproduces; every video note names
     the owner-supplied synopsis as its scope basis;
  2. the coverage basis — 44 notes, one per verified lesson, every
     lesson carrying XP and a type, the three chapter purposes stated
     on the course page as the catalog page renders them;
  3. the glossary crosswalk — 20 terms, each with a one-line meaning,
     the teaching lesson, and the chapter mapping; every term must
     exist as a row in GLOSSARY.md.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DC = REPO_ROOT / "courses" / "datacamp-ai-security-risk"


def _read(name: str) -> str:
    return (DC / name).read_text(encoding="utf-8")


def test_every_note_states_the_honesty_basis() -> None:
    """All 44 notes carry the per-kind honesty paragraph; the exercise
    notes additionally state the account wall and the reconstruction."""
    notes = sorted(DC.glob("ch*.md"))
    assert len(notes) == 44
    for p in notes:
        text = p.read_text(encoding="utf-8")
        assert "## Honesty note" in text, p.name
        assert "SRC-CURR-014" in text, p.name
        assert "SRC-CURR-015" in text, p.name
        assert "No video was streamed" in text, p.name


def test_video_notes_name_the_synopsis_as_scope() -> None:
    """Video notes ground in the owner-supplied synopsis; exercise
    notes state the account wall and the reconstruction instead."""
    video = _read("ch01-01-security-risks-specific-to-ai.md")
    assert "the video synopsis was supplied by the owner" in video
    exercise = _read("ch01-02-ai-risk-awareness.md")
    assert "account-walled" in exercise
    assert "reconstructs the concepts" in exercise
    assert "the interactive lesson is account-walled" in exercise


def test_course_page_states_chapter_purposes_and_lesson_facts() -> None:
    """The catalog page's render is the basis: three chapter purposes,
    the 44-lesson count, the type split, the XP total, the level, the
    completion time, and the instructor credit — all as the page
    states them."""
    page = _read("README.md")
    for purpose in (
        "strategic understanding of AI security",
        "internal and external",
        "organizational goals",
    ):
        assert purpose in page, purpose
    assert "44 lessons" in page
    assert "12 videos" in page
    assert "21 interactive exercises" in page
    assert "11 gamified scenarios" in page
    assert "2750 XP" in page
    assert "beginner" in page
    assert "no prerequisites" in page
    assert "Angeline Corvaglia" in page


def test_glossary_crosswalk_terms_all_exist_in_glossary() -> None:
    """The crosswalk's 20 terms must each be a row in GLOSSARY.md —
    the crosswalk indexes the glossary, it does not extend it."""
    cw = _read("crosswalk-glossary.md")
    terms = re.findall(r"^\| \*\*(.+?)\*\* \|", cw, re.M)
    assert len(terms) == 20, len(terms)
    glossary = (REPO_ROOT / "GLOSSARY.md").read_text(encoding="utf-8")
    for term in terms:
        assert f"| **{term}** |" in glossary, f"crosswalk term missing from GLOSSARY.md: {term}"


def test_self_assessment_names_lesson_and_chapter_pointers() -> None:
    """Ten judgment questions, each pointing at its teaching lesson and
    deepening chapter."""
    sa = _read("self-assessment.md")
    questions = [ln for ln in sa.splitlines() if re.match(r"^\d+\. ", ln)]
    assert len(questions) == 10, f"expected 10 numbered questions, found {len(questions)}"
    assert sa.count("*(lesson") >= 10  # every question carries its pointers


def test_every_note_carries_a_worked_example() -> None:
    """The session-10 worked-example layer: all 44 notes carry the
    beginner walk-through section, each with a concrete scenario."""
    notes = sorted(DC.glob("ch*.md"))
    assert len(notes) == 44
    for p in notes:
        text = p.read_text(encoding="utf-8")
        assert "## Worked example (beginner walk-through)" in text, p.name
        assert len(text.split("## Worked example (beginner walk-through)")[1].split("## Through-lines")[0]) > 300, p.name
