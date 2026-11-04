"""The glossary's chapter-mapping column carries a small grammar:
chapter numbers and ranges (01–24), project ids and ranges (P01–P10),
from-scratch module ids (FS-01…), the keyword 'all', and two named
extras ('careers roadmap', 'incidents (all 14)'). Session-13 (P06):
353 rows carried 640 raw parts; the two prose cells that failed the
grammar were normalized into it. Every part of every cell is now
machine-checked: ranges must be ordered and in-tree, project ranges
within P01–P10, FS ids within the twelve modules.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GLOSSARY = (REPO / "GLOSSARY.md").read_text(encoding="utf-8")

CH = re.compile(r"^(\d{2})(?:–(\d{2}))?(?: \(.*\))?$")
PR = re.compile(r"^P(\d{2})(?:-P?(\d{2}))?$")
FS = re.compile(r"^FS-(\d{2})$")
NAMED = ("careers roadmap", "incidents (all 14)")


def _rows() -> list[tuple[str, str]]:
    return [
        (m.group(1), m.group(4).strip())
        for m in re.finditer(r"^\| \*\*(.+?)\*\* \|(.+)\| ([^|]+) \| (.+?) \|$", GLOSSARY, re.M)
    ]


def test_all_rows_parsed() -> None:
    assert len(_rows()) == 353


def test_chapter_mapping_parts_are_wellformed() -> None:
    for term, cell in _rows():
        if cell in ("all", "—"):
            continue
        for part in cell.split(","):
            part = part.strip()
            if part == "all" or part in NAMED:
                continue
            m = CH.match(part) or PR.match(part) or FS.match(part)
            assert m, f"{term!r}: unparsable part {part!r} in {cell!r}"
            if CH.match(part):
                a, b = int(m.group(1)), int(m.group(2) or m.group(1))
                assert a <= b, f"{term!r}: reversed range {part!r}"
                assert 1 <= a <= 24 and 1 <= b <= 24, f"{term!r}: {part!r} outside 01-24"
            elif PR.match(part):
                a, b = int(m.group(1)), int(m.group(2) or m.group(1))
                assert a <= b, f"{term!r}: reversed project range {part!r}"
                assert 1 <= a <= 10 and 1 <= b <= 10, f"{term!r}: {part!r} outside P01-P10"
            else:
                n = int(m.group(1))
                assert 1 <= n <= 12, f"{term!r}: FS-{n:02d} outside the twelve modules"


def test_the_two_normalized_cells_stay_normalized() -> None:
    text = GLOSSARY
    assert "| 23, careers roadmap |" in text
    assert "| 22, 21, incidents (all 14) |" in text
    assert "all incidents |" not in text.replace("incidents (all 14)", "")
