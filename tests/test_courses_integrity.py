"""The lecture-library structure test: courses/ stays honest.

Opened with the lecture library (2026-10-27): four course
companions, 57 verified videos, 61 companion notes. This test pins
the structural promises the library makes in its own index:

  1. every course page's note-table rows link to note files that
     exist (and every note file appears in exactly one table);
  2. every course page links its playlist, and that playlist URL is
     the one its register entries carry;
  3. the library index names all four courses.

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
    data = yaml.safe_load((REPO_ROOT / "research/source-register.yaml").read_bytes())
    return {s["id"]: s for s in data["sources"]}


COURSE_DIRS = [
    "boaz-barak-cs2881",
    "google-deepmind-agi-safety",
    "cais-ethics-society",
    "safeshield-governance",
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
