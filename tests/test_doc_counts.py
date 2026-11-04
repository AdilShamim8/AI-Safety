"""Document-count consistency: every stated count vs the disk.

Session-13 origin (P04): the stated-count surfaces were pinned one by
one across sessions (README suite size, library notes, CITATION
glossary), but the check was always written after a human noticed a
stale figure — MAINTENANCE carried 261 sources against the register's
264 until this sweep. The rule here is the same as
test_companion_note_counts_computed_from_disk: derive from the tree,
compare against every doc that states the figure, and require dated
snapshots to carry the word 'snapshot' so a historical number is never
mistaken for a stale one.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent


def _truth() -> dict[str, int]:
    sources = yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())
    claims = yaml.safe_load((REPO / "research" / "claims-register.yaml").read_bytes())
    notes = [p for p in (REPO / "research" / "notes").glob("*.md")]
    papers = [p for p in notes if re.match(r"\d", p.name)]
    return {
        "chapters": len(list((REPO / "chapters").glob("[0-9][0-9]-*"))),
        "projects": len([p for p in (REPO / "projects").iterdir() if p.is_dir()]),
        "courses": len([c for c in (REPO / "courses").iterdir() if c.is_dir()]),
        "sources": len(sources["sources"]),
        "claims": len(claims["claims"]),
        "glossary": len(
            re.findall(r"^\| \*\*", (REPO / "GLOSSARY.md").read_text(encoding="utf-8"), re.M)
        ),
        "paper notes": len(papers),
    }


DOCS = ("README.md", "SYLLABUS.md", "FAQ.md", "CITATION.cff", "courses/README.md")


def test_current_counts_agree_across_docs() -> None:
    """Every doc that states a current figure must state the disk's."""
    truth = _truth()
    for doc in DOCS:
        text = (REPO / doc).read_text(encoding="utf-8")
        for figure, real in truth.items():
            for m in re.finditer(rf"(\d+)\s+{re.escape(figure)}", text):
                stated = int(m.group(1))
                assert stated == real, f"{doc}: states {stated} {figure}; the tree holds {real}"


def test_dated_snapshots_are_labeled() -> None:
    """A doc may carry an old figure only as a dated snapshot; those
    must say so next to the number (MAINTENANCE's run records)."""
    for doc in ("MAINTENANCE.md",):
        text = (REPO / doc).read_text(encoding="utf-8")
        truth = _truth()
        for figure, real in truth.items():
            for m in re.finditer(rf"(\d+)\s+{re.escape(figure)}", text):
                stated = int(m.group(1))
                if stated == real:
                    continue
                window = text[max(0, m.start() - 260) : m.end() + 260]
                assert "snapshot" in window or "run time" in window, (
                    f"{doc}: {stated} {figure} (tree holds {real}) with no "
                    "snapshot label — a stale figure, not a dated record"
                )
