"""Chapter-layer closure: links, register refs, note refs, structure.

Session-13 origin (P18): the 24 chapter READMEs and solutions files
reference datasets, sources, and paper notes inline; all three sweeps
ran clean on this corpus (no broken relative link, no SRC id outside
the register, no note or incident path missing, all 24 carry the
'## 7. Readings' and '## 8. Exercises' sections) — pinned here so a
future edit cannot break them silently.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((REPO / "chapters").glob("[0-9][0-9]-*"))
SRC_IDS = {
    s["id"]
    for s in yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())["sources"]
}


def test_relative_links_resolve() -> None:
    for d in CHAPTERS:
        for f in (d / "README.md", d / "solutions.md"):
            t = f.read_text(encoding="utf-8")
            for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", t):
                link = m.group(1)
                if link.startswith(("http", "mailto")):
                    continue
                assert (d / link).resolve().exists(), f"{d.name[:2]}: {link}"


def test_src_refs_in_register() -> None:
    for d in CHAPTERS:
        for f in (d / "README.md", d / "solutions.md"):
            t = f.read_text(encoding="utf-8")
            for m in re.finditer(r"\bSRC-[A-Z]+-\d+[a-z]?\b", t):
                assert m.group(0) in SRC_IDS, f"{d.name[:2]}: {m.group(0)} not in register"


def test_note_refs_resolve() -> None:
    for d in CHAPTERS:
        for f in (d / "README.md", d / "solutions.md"):
            t = f.read_text(encoding="utf-8")
            for m in re.finditer(r"notes/(\d+-[a-z-]+)\.md", t):
                assert (
                    REPO / "research" / "notes" / f"{m.group(1)}.md"
                ).exists(), f"{d.name[:2]}: notes/{m.group(1)}.md missing"
            for m in re.finditer(r"notes/incidents/([0-9a-z-]+)\.md", t):
                assert (
                    REPO / "research" / "notes" / "incidents" / f"{m.group(1)}.md"
                ).exists(), f"{d.name[:2]}: incidents/{m.group(1)}.md missing"


def test_every_chapter_carries_the_standard_sections() -> None:
    for d in CHAPTERS:
        t = (d / "README.md").read_text(encoding="utf-8")
        assert re.search(r"^## 7\. Readings", t, re.M), f"{d.name[:2]}: no readings section"
        assert re.search(r"^## 8\. Exercises", t, re.M), f"{d.name[:2]}: no exercises section"
        assert "ompletion" in t, f"{d.name[:2]}: no completion block"
