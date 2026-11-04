"""The lecture-library structure test: courses/ stays honest.

Opened with the lecture library (2026-10-27): four course
companions, 57 verified videos, 61 companion notes; extended
2026-11-03 with the fifth course (DataCamp, 44 verified
lessons — an interactive course, so its playlist promises adapt:
count-and-content agreement with the register, both URLs linked,
and no note outside the table). This test pins the structural
promises the library makes in its own index:

  1. every course page's note-table rows link to note files that
     exist (and every note file appears in exactly one table);
  2. every course page links its playlist, and that playlist URL is
     the one its register entries carry;
  3. the library index names all six courses.

If a note is removed or a table row is orphaned, this fails loudly.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
COURSES = REPO_ROOT / "courses"
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def _register() -> dict:
    data = yaml.safe_load((REPO_ROOT / "research" / "source-register.yaml").read_bytes())
    return {s["id"]: s for s in data["sources"]}


COURSE_DIRS = [
    "boaz-barak-cs2881",
    "google-deepmind-agi-safety",
    "cais-ethics-society",
    "safeshield-governance",
    "datacamp-ai-security-risk",
    "campusx-ai-security-guardrails",
]


def test_every_course_dir_exists_with_notes() -> None:
    for d in COURSE_DIRS:
        p = COURSES / d
        assert p.is_dir(), f"missing course dir: {d}"
        notes = list(p.glob("*.md"))
        assert len(notes) >= 8, f"{d}: expected a full note set, found {len(notes)}"


def test_note_rows_link_existing_files() -> None:
    for d in COURSE_DIRS:
        readme = (COURSES / d / "README.md").read_text(encoding="utf-8")
        for m in re.finditer(r"\[([\w-]+\.md)\]\(([\w-]+\.md)\)", readme):
            title, target = m.group(1), m.group(2)
            assert title == target, f"{d}: row text/target mismatch: {title} vs {target}"
            assert (COURSES / d / target).exists(), f"{d}: table links missing note {target}"


def test_playlist_urls_match_register() -> None:
    reg = _register()
    ids = {
        "boaz-barak-cs2881": "SRC-VIDEO-011",
        "google-deepmind-agi-safety": "SRC-VIDEO-013",
        "cais-ethics-society": "SRC-VIDEO-015",
        "safeshield-governance": "SRC-VIDEO-017",
    }
    for d, sid in ids.items():
        readme = (COURSES / d / "README.md").read_text(encoding="utf-8")
        url = reg[sid]["url"]
        assert f"]({url})" in readme, f"{d}: playlist URL not linked as registered"


def test_library_index_names_all_courses() -> None:
    t = (COURSES / "README.md").read_text(encoding="utf-8")
    for d in COURSE_DIRS:
        assert d in t, f"library index missing course dir: {d}"


def test_datacamp_lesson_count_matches_register() -> None:
    """The course page promises 44 lessons; the disk, the content
    modules, and the course page must agree on the same set."""
    from gen_datacamp_companion import ALL_LESSONS

    assert len(ALL_LESSONS) == 44
    assert sum(ls["xp"] for ls in ALL_LESSONS) == 2750
    notes = sorted(p.name for p in (COURSES / "datacamp-ai-security-risk").glob("ch*.md"))
    assert len(notes) == 44, f"note count drifted: {len(notes)}"
    # the worked-example layer: every note carries the beginner walk-through
    for n in notes:
        text = (COURSES / "datacamp-ai-security-risk" / n).read_text(encoding="utf-8")
        assert "## Worked example (beginner walk-through)" in text, n
    cx = sorted(p.name for p in (COURSES / "campusx-ai-security-guardrails").glob("m*-*.md"))
    for n in cx:
        text = (COURSES / "campusx-ai-security-guardrails" / n).read_text(encoding="utf-8")
        assert "## Worked example (practitioner walk-through)" in text, n
    slugs = {ls["slug"] + ".md" for ls in ALL_LESSONS}
    assert set(notes) == slugs, "note files and content modules disagree"


def test_datacamp_register_urls_linked_on_course_page() -> None:
    """Both registered URLs (the catalog page and the course page)
    are linked on the course page, exactly as the register carries
    them."""
    reg = _register()
    readme = (COURSES / "datacamp-ai-security-risk" / "README.md").read_text(encoding="utf-8")
    for sid in ("SRC-CURR-014", "SRC-CURR-015"):
        url = reg[sid]["url"]
        assert f"]({url})" in readme, f"datacamp: {sid} URL not linked as registered"


def test_datacamp_note_rows_cover_every_lesson() -> None:
    """Every lesson-table row links its note; every note is a row —
    the interactive course's version of the playlist promise."""
    readme = (COURSES / "datacamp-ai-security-risk" / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\((ch\d{2}-\d{2}-[\w-]+\.md)\)", readme))
    notes = {p.name for p in (COURSES / "datacamp-ai-security-risk").glob("ch*.md")}
    assert linked == notes, f"table/notes drift: {linked ^ notes}"


def test_campusx_lesson_count_and_durations_match_register() -> None:
    """The course page promises 14 lessons, 13 with published durations
    totaling 330.47 minutes and one announced (duration 0); the disk,
    the content modules, and the register must agree."""
    from gen_campusx_companion import ALL_LESSONS, PUBLISHED, TOTAL_MINUTES

    assert len(ALL_LESSONS) == 14
    assert len(PUBLISHED) == 13
    assert abs(TOTAL_MINUTES - 330.47) < 0.02
    notes = sorted(p.name for p in (COURSES / "campusx-ai-security-guardrails").glob("m*-*.md"))
    assert len(notes) == 14, f"note count drifted: {len(notes)}"
    slugs = {ls["slug"] + ".md" for ls in ALL_LESSONS}
    assert set(notes) == slugs


def test_campusx_register_url_linked_on_course_page() -> None:
    """The registered course URL is linked exactly as the register
    carries it."""
    reg = _register()
    readme = (COURSES / "campusx-ai-security-guardrails" / "README.md").read_text(encoding="utf-8")
    url = reg["SRC-CURR-016"]["url"]
    assert f"]({url})" in readme, "SRC-CURR-016 URL not linked as registered"


def test_campusx_note_rows_cover_every_lesson() -> None:
    """Every lesson-table row links its note; every note is a row."""
    readme = (COURSES / "campusx-ai-security-guardrails" / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\((m\d-\d{2}-[\w-]+\.md)\)", readme))
    notes = {p.name for p in (COURSES / "campusx-ai-security-guardrails").glob("m*-*.md")}
    assert linked == notes, f"table/notes drift: {linked ^ notes}"


def test_campusx_unpublished_lesson_carries_its_status() -> None:
    """The one duration-0 lesson must state its announced status in
    the note itself — the honesty rule the register records."""
    note = (
        COURSES
        / "campusx-ai-security-guardrails"
        / "m4-01-threat-modelling-our-agentic-application.md"
    ).read_text(encoding="utf-8")
    assert "not yet published" in note
    assert "duration 0" in note
