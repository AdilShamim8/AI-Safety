"""SYLLABUS internal consistency: the per-chapter Projects column must
agree with the 'Where the projects attach' section.

Session-13 origin (P05): the table and the attach section drifted —
the table had empty cells for chapters 10/11 (P06 spans 09–11 there)
and a spurious P10 in chapter 15 (P10's README mentions ch15, but its
attachment is 22+24; the mention is material, not attachment). A link
mention in a project README is not the same thing as an attachment,
so the check runs against the attach section, which is the syllabus's
own authoritative statement.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SYL = (REPO / "SYLLABUS.md").read_text(encoding="utf-8")


def _attach_section() -> str:
    i = SYL.find("## Where the projects attach")
    j = SYL.find("## Scope boundaries")
    assert i > 0 and j > i
    return SYL[i:j]


def _attach_map() -> dict[str, list[str]]:
    attach: dict[str, list[str]] = {}
    pat = re.compile(r"(P\d\d)[^(]+\((?:Ch\.)?(\d{2})(?:[–-](\d{2}))?(?:\+(\d{2}))?\)")
    for m in pat.finditer(_attach_section()):
        pid, a, b, c = m.group(1), m.group(2), m.group(3), m.group(4)
        chs = [a]
        if b:
            chs += [f"{int(a) + k:02d}" for k in range(1, int(b) - int(a) + 1)]
        if c:
            chs.append(c)
        for ch in chs:
            attach.setdefault(ch, []).append(pid)
    return attach


def test_attach_section_covers_all_ten_projects() -> None:
    ids = {p for ps in _attach_map().values() for p in ps}
    assert ids == {f"P{i:02d}" for i in range(1, 11)}, sorted(ids)


def test_projects_column_matches_attach_section() -> None:
    attach = _attach_map()
    rows = re.findall(r"^\| (\d\d) \| .+? \| .+? \| .+? \| (.+?) \|$", SYL, re.M)
    assert len(rows) == 24
    for num, projects in rows:
        stated = sorted(x.strip() for x in projects.split(",") if x.strip() != "—")
        disk = sorted(attach.get(num, []))
        assert stated == disk, f"chapter {num}: table says {stated}, attach section says {disk}"


def test_prereq_column_ids_exist() -> None:
    rows = re.findall(r"^\| (\d\d) \| .+? \| (.+?) \| .+? \| .+? \|$", SYL, re.M)
    for num, prereq in rows:
        ids = [x.strip() for x in prereq.split(",") if x.strip() != "—"]
        for pid in ids:
            assert re.fullmatch(r"\d{2}", pid), f"chapter {num}: prereq {pid!r}"
            assert int(pid) < int(num), f"chapter {num}: prereq {pid} not earlier"
