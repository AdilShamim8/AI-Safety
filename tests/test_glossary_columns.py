"""Glossary columns: the five-cell row shape.

Session-13 origin (P27): each of the 353 standard rows must carry all
five cells — term, definition, alias (may be the em-dash when a term
has none, but the cell must exist), common confusion, and the chapter
mapping. The confusion column is what makes the glossary a
misconception guard rather than a dictionary; empty cells fail.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
G = (REPO / "GLOSSARY.md").read_text(encoding="utf-8")


def _rows() -> list[tuple[str, str, str, str, str]]:
    out = []
    for m in re.finditer(r"^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", G, re.M):
        out.append(tuple(x.strip() for x in m.groups()))
    return out


def test_all_rows_parse_five_cells() -> None:
    rows = _rows()
    assert len(rows) == 353, len(rows)


def test_definition_and_confusion_cells_nonempty() -> None:
    for term, definition, _alias, confusion, chapters in _rows():
        assert definition and len(definition) > 20, f"{term!r}: thin definition"
        assert confusion and len(confusion) > 10, f"{term!r}: no confusion note"
        assert chapters, f"{term!r}: no chapter mapping"
