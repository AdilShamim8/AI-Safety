"""CITATION, prerequisites, and the glossary payload parity.

Session-13 origin (P22): three small closures never checked together —
CITATION.cff must carry its required fields (title, message, version,
date-released, repository-code, license), the prerequisites/ pages
must have no broken relative links, and the dashboard's glossary
payload must hold exactly as many term objects as GLOSSARY.md has
rows (363 = 363 today), so the page can never silently ship fewer
terms than the source file carries. All three passed on this corpus;
pinned.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_citation_fields() -> None:
    t = (REPO / "CITATION.cff").read_text(encoding="utf-8")
    for k in ("title:", "message:", "version:", "date-released:", "repository-code:", "license:"):
        assert re.search(rf"^{k}", t, re.M), f"CITATION.cff missing {k}"


def test_prerequisites_links_resolve() -> None:
    for f in (REPO / "prerequisites").rglob("*.md"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", t):
            link = m.group(1)
            if link.startswith(("http", "mailto")):
                continue
            assert f.parent.joinpath(link).resolve().exists(), f"{f.name}: {link}"


def test_glossary_payload_parity() -> None:
    page = (REPO / "index.html").read_text(encoding="utf-8")
    rows = len(re.findall(r"^\| \*\*", (REPO / "GLOSSARY.md").read_text(encoding="utf-8"), re.M))
    terms = len(re.findall(r'"term":', page))
    assert rows == 363, rows
    assert terms == rows, f"dashboard glossary holds {terms} terms; GLOSSARY.md has {rows} rows"
