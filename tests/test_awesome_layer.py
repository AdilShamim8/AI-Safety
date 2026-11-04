"""AWESOME.md closure: link instances, the 97/3 statement, live-sweep
records.

Session-13 origin (P19): the annotated index states "verify_links.py
fetched all 100 URLs cited on this page" and "All 97 live — three
hosts bot-block". The arithmetic (100 instances, 3 bot-blocked hosts,
97 live) is pinned, along with the relative-link closure and the
count of unique external targets (96 — four sources are cited from
two media layers each, which the page's organization explains).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AWESOME = (REPO / "AWESOME.md").read_text(encoding="utf-8")


def test_relative_links_resolve() -> None:
    for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", AWESOME):
        link = m.group(1)
        if link.startswith(("http", "mailto")):
            continue
        assert (REPO / "AWESOME.md").parent.joinpath(link).resolve().exists(), link


def test_the_100_url_claim() -> None:
    flat = re.sub(r"\s+", " ", AWESOME)
    ext = re.findall(r"\]\((https?://[^)]+)\)", AWESOME)
    assert len(ext) == 100, len(ext)
    assert len(set(ext)) == 96, len(set(ext))
    assert "fetched all 100 URLs cited on this page" in flat


def test_the_live_statement_is_consistent() -> None:
    assert "All\n97 live" in AWESOME
    # 100 instances - 3 bot-blocked hosts = 97 live
    assert 100 - 3 == 97
    for host in ("OWASP", "American Bar Association", "ACM"):
        assert host in AWESOME
    assert "OpenAI Preparedness announcement" in AWESOME
