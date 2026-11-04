"""Research-notes ↔ register closure across all three citation families.

Session-13 origin (P11): 87 notes referenced their sources in four
physical forms nobody checked — single-line 'Source: ID · Access:',
two-line with a parenthetical, bolded access levels, and the
comparisons' collective 'Sources:' prose with an 'all X in the
register' claim. The sweep's one real error: SRC-PAPER-034's register
row said full-text-read while its own limitations text said "recorded
at abstract-read verification level for this build" and its note said
abstract-read — the field was wrong, the prose was right; the field is
now abstract-read. The comparisons split into two classes: the six
head-registered ones cite register ids collectively, and comparisons
07-12 are synthesis notes citing sibling paper-notes or incident notes
instead — each class is checked with its own rule.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SRCS = yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())["sources"]
BY_SRC = {s["id"]: s for s in SRCS}
NOTES = [p for p in (REPO / "research" / "notes").glob("*.md") if p.name != "README.md"]
NOTE_IDS = {p.name for p in NOTES}
INCIDENT_IDS = {
    p.name
    for p in (REPO / "research" / "notes" / "incidents").glob("*.md")
    if p.name != "README.md"
}
SRC = re.compile(r"SRC-[A-Z]+-\d+[a-z]?")
HEAD_REGISTERED = {f"0{i}" for i in range(1, 7)}


def test_note_count() -> None:
    assert len(NOTES) == 86, len(NOTES)


def test_single_source_notes_agree_with_register() -> None:
    checked = 0
    for n in sorted(NOTES):
        if n.name.startswith("comparison"):
            continue
        t = n.read_text(encoding="utf-8")
        m = re.search(
            r"^Source: (SRC-[A-Z]+-\d+[a-z]?) · Access: \*{0,2}([a-z-]+)\*{0,2}", t, re.M
        ) or re.search(
            r"^Source: (SRC-[A-Z]+-\d+[a-z]?) \(.*\)\n· Access: \*{0,2}([a-z-]+)\*{0,2}", t, re.M
        )
        assert m, f"{n.name}: no Source line in either form"
        sid, lvl = m.group(1), m.group(2)
        assert sid in BY_SRC, f"{n.name}: {sid} not in register"
        assert (
            BY_SRC[sid]["access_level"] == lvl
        ), f"{n.name}: note says {lvl}, register says {BY_SRC[sid]['access_level']} for {sid}"
        checked += 1
    assert checked == 74, checked


def test_head_registered_comparisons_cite_real_sources() -> None:
    for n in sorted(NOTES):
        if not n.name.startswith("comparison"):
            continue
        num = n.name.split("-")[1]
        t = n.read_text(encoding="utf-8")
        if num in HEAD_REGISTERED:
            found = set(SRC.findall(t[:600]))
            assert found, f"{n.name}: no register ids in head"
            for sid in found:
                assert sid in BY_SRC, f"{n.name}: {sid} not in register"
            mc = re.search(r"all \*\*([a-z-]+)\*\* in the register", t[:600])
            if mc:
                for sid in found:
                    real = BY_SRC[sid]["access_level"]
                    assert real == mc.group(
                        1
                    ), f"{n.name}: claims all {mc.group(1)}, but {sid} is {real}"


def test_synthesis_comparisons_cite_sibling_notes() -> None:
    """Comparisons 07-12 cite sibling paper-notes or incident notes; every
    citation must resolve to a file on disk."""
    for n in sorted(NOTES):
        if not n.name.startswith("comparison"):
            continue
        num = n.name.split("-")[1]
        if num in HEAD_REGISTERED:
            continue
        t = n.read_text(encoding="utf-8")
        cited = re.findall(r"notes/(\d+-[a-z-]+\.md)", t)
        incited = re.findall(r"incidents/([0-9]+[a-z-]*-[a-z-]+\.md)", t)
        by_number = re.findall(r"\(note (\d+)\)", t[:900])
        assert cited or incited, f"{n.name}: synthesis comparison cites no sibling note"
        for c in cited:
            assert c in NOTE_IDS, f"{n.name}: cites note {c!r} not on disk"
        for c in incited:
            assert c in INCIDENT_IDS, f"{n.name}: cites incident {c!r} not on disk"
        for b in by_number:
            assert any(
                x.startswith(b.zfill(2)) for x in NOTE_IDS
            ), f"{n.name}: cites note {b!r} not on disk"


def test_the_034_fix_stays() -> None:
    assert BY_SRC["SRC-PAPER-034"]["access_level"] == "abstract-read"
