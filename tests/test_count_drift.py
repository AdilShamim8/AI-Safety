"""The count-drift instrument: prose surfaces vs. the registers they describe.

Session 2's closing sweep found six files whose hand-written counts had
survived six phases of corpus growth: the README structure table said
20 notes / 160 sources while the registers held 74 / 231; the FAQ said
164 sources; CITATION.cff carried the 150-commit abstract; and two
front doors counted the incidents at 11 and 3. Every drifted number
describes something machine-countable — the registers, the notebook
directories, the catalog, the glossary table, the test suite.

These tests recompute the truth from the repo's own data (the same
``build_dashboard.build_data()`` extraction the pinned dashboard tests
already cover) and require each count-bearing surface to carry it.
When the corpus grows, these tests fail until the prose catches up —
that failure is the instrument working, not a false alarm.

Scope discipline: only *current-state* surfaces are pinned. Dated
records — planning/STATUS.md, CHANGELOG.md, the session judge audit —
legitimately describe past states and are never asserted here. Counts
are written in digits on pinned surfaces for the same reason: a
number spelled out in words evades every check this file can make.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_dashboard  # noqa: E402


def _squash(text: str) -> str:
    """Collapse all whitespace so phrase checks survive line wrapping."""
    return re.sub(r"\s+", " ", text)


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _truth() -> dict[str, int]:
    """The corpus counts, recomputed from the repo's own data."""
    data = build_dashboard.build_data()
    repo = data["repo"]
    incident_files = list((REPO_ROOT / "research" / "notes" / "incidents").glob("[0-9][0-9]-*.md"))
    glossary_terms = len(re.findall(r"^\| \*\*", _read("GLOSSARY.md"), re.M))
    return {
        "sources": len(data["sources"]),
        "claims": len(data["claims"]),
        "cards": len(data["datasets"]),
        "paper_notes": int(repo["paper_notes"]),
        "comparison_notes": int(repo["comparison_notes"]),
        "incidents": len(incident_files),
        "glossary": glossary_terms,
        "tests": int(repo["tests"]),
    }


def test_truth_is_the_expected_corpus() -> None:
    """Guard the extraction itself: the corpus must be at least this deep."""
    t = _truth()
    assert t["sources"] >= 231
    assert t["claims"] >= 206
    assert t["cards"] >= 43
    assert t["paper_notes"] >= 74
    assert t["comparison_notes"] >= 12
    assert t["incidents"] >= 14
    assert t["glossary"] >= 296
    assert t["tests"] >= 594


def test_readme_structure_table_counts() -> None:
    t = _truth()
    text = _squash(_read("README.md"))
    assert (
        f"{t['paper_notes']} paper + {t['comparison_notes']} comparison "
        f"+ {t['incidents']} incident reviews"
    ) in text
    assert f"{t['sources']} sources / {t['claims']} claims" in text
    assert f"{t['cards']} verified real-world dataset cards" in text
    assert f"{t['tests']}-test suite" in text


def test_faq_source_count() -> None:
    t = _truth()
    text = _squash(_read("FAQ.md"))
    assert f"all {t['sources']} sources" in text


def test_start_here_counts() -> None:
    t = _truth()
    text = _squash(_read("START_HERE.md"))
    assert f"{t['cards']} verified dataset cards" in text
    assert (
        f"{t['paper_notes']} paper notes + {t['comparison_notes']} comparisons "
        f"+ {t['incidents']} incident reviews"
    ) in text


def test_citation_cff_states_version_and_counts() -> None:
    """A released corpus must state its version and describe what it ships."""
    t = _truth()
    text = _read("CITATION.cff")
    assert re.search(r'^version: "\d+\.\d+\.\d+"$', text, re.M)
    assert re.search(r'^date-released: "\d{4}-\d{2}-\d{2}"$', text, re.M)
    squashed = _squash(text)
    assert (
        f"{t['paper_notes']} paper notes + {t['comparison_notes']} comparison notes "
        f"+ {t['incidents']} incident reviews"
    ) in squashed
    assert f"{t['cards']} verified dataset cards" in squashed
    assert f"{t['glossary']}-term glossary" in squashed
    assert f"({t['sources']} sources, {t['claims']} claims)" in squashed


def test_notes_readme_front_door_counts() -> None:
    t = _truth()
    text = _squash(_read("research/notes/README.md"))
    assert f"**{t['paper_notes']} paper notes**" in text
    assert f"**{t['comparison_notes']} comparison notes**" in text
    assert f"**{t['incidents']} incident reviews**" in text


def test_incidents_readme_counts_and_register_range() -> None:
    t = _truth()
    text = _read("research/notes/incidents/README.md")
    rows = re.findall(r"^\| (\d{2}) \|", text, re.M)
    assert len(rows) == t["incidents"], "index table rows must match incident files"
    squashed = _squash(text)
    assert f"{t['incidents']} incidents, four eras" in squashed
    assert f"all {t['incidents']} incidents" in squashed.lower()
    assert "accountability era" in squashed  # the fourth era is named, not just counted
    # the stated register range must match what the incident notes actually cite
    cited: set[int] = set()
    incidents_dir = REPO_ROOT / "research" / "notes" / "incidents"
    for note in incidents_dir.glob("[0-9][0-9]-*.md"):
        body = note.read_text(encoding="utf-8")
        cited.update(int(m) for m in re.findall(r"SRC-REPORT-(\d{3})", body))
    assert cited, "incident notes must cite SRC-REPORT sources"
    lo, hi = min(cited), max(cited)
    assert f"[SRC-REPORT-{lo:03d}..{hi:03d}]" in squashed


def test_awesome_counts() -> None:
    t = _truth()
    text = _squash(_read("AWESOME.md"))
    assert (f"{t['paper_notes']} paper notes and {t['comparison_notes']} comparison notes") in text
    assert f"{t['incidents']} incidents reviewed" in text
