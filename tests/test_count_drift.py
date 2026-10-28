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
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_dashboard  # noqa: E402

INSTRUMENT_FILES = {
    "test_awesome_links.py",
    "test_audit_missing.py",
    "test_count_drift.py",
    "test_courses_integrity.py",
    "test_dashboard.py",
    "test_validate_repo.py",
    "test_responsive.py",
}


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


def test_readme_suite_mentions_agree() -> None:
    """Every 'N-test suite' phrase in the README must state the real count.

    The first version of this instrument pinned one phrase and missed the
    stale status line saying 'a 592-test suite' two paragraphs above the
    corrected table saying '602-test suite' — a single `in text` match is
    satisfied by one true occurrence while a false one survives. This test
    collects every suite-size mention and requires them all to agree.
    """
    t = _truth()
    mentions = re.findall(r"(\d+)(?:-test suite| deterministic tests)", _read("README.md"))
    assert mentions, "README must state the test-suite size"
    assert set(mentions) == {str(t["tests"])}, f"stale suite sizes: {mentions}"
    # the status line's count phrasings must also agree with the registers
    text = _squash(_read("README.md"))
    assert f"{t['cards']} verified dataset cards" in text
    assert f"{t['sources']} registered sources" in text
    assert f"{t['claims']} registered claims" in text


def test_readme_suite_breakdown_agrees() -> None:
    """The README's suite-size parenthetical must state the real split.

    The total was pinned but the split was not: '32 repo-instrument'
    survived two instrument additions (the truth was 36, then 37)
    inside a parenthetical the total-level pin could not see. This
    recomputes the three-way split from collection, grouped by file
    family: from-scratch (test_fs_*), repo instruments (the fixed
    set), and package tests (everything else).
    """
    t = _truth()
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    counts: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"tests/(test_[a-z0-9_]+\.py): (\d+)$", line.strip())
        if m:
            counts[m.group(1)] = counts.get(m.group(1), 0) + int(m.group(2))
    assert counts, f"collection parse failed:\n{proc.stdout[-500:]}\n{proc.stderr[-500:]}"
    fs = sum(v for k, v in counts.items() if k.startswith("test_fs_"))
    inst = sum(v for k, v in counts.items() if k in INSTRUMENT_FILES)
    pkg = sum(
        v for k, v in counts.items() if not k.startswith("test_fs_") and k not in INSTRUMENT_FILES
    )
    m = re.search(
        r"(\d+)-test suite \((\d+) package \+ (\d+) from-scratch \+ (\d+) repo-instrument\)",
        _read("README.md"),
    )
    assert m, "README must state the suite breakdown"
    stated_total, stated_pkg, stated_fs, stated_inst = (int(g) for g in m.groups())
    assert (stated_pkg, stated_fs, stated_inst) == (pkg, fs, inst), (
        f"stale suite breakdown: stated ({stated_pkg}, {stated_fs}, {stated_inst}) "
        f"vs collected ({pkg}, {fs}, {inst})"
    )
    assert stated_total == stated_pkg + stated_fs + stated_inst == t["tests"]


def test_faq_source_count() -> None:
    t = _truth()
    text = _squash(_read("FAQ.md"))
    assert f"all {t['sources']} sources" in text


def test_faq_dataset_counts_all_agree() -> None:
    """Every dataset-count mention in the FAQ must state the real count.

    The FAQ was pinned for sources only, and its card counts drifted
    twice across session boundaries — '22 real-world safety datasets'
    survived session 1 and '43 dataset cards' survived session 2 while
    the pinned source line beside them stayed true. A single asserted
    phrase is satisfied by one true occurrence; this collects every
    mention and requires them all to agree.
    """
    t = _truth()
    text = _read("FAQ.md")
    mentions = re.findall(r"(\d+)(?: real-world safety datasets| dataset cards)", text)
    downloads = re.findall(r"not (\d+) downloads", text)
    all_counts = set(mentions) | set(downloads)
    assert all_counts, "FAQ must state the dataset-card count"
    assert all_counts == {str(t["cards"])}, f"stale dataset counts in FAQ: {sorted(all_counts)}"


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
    assert f"{t['cards']} verified cards" in text
