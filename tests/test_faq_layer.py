"""FAQ layer: link closure and the standing claims.

Session-13 origin (P28): the FAQ's links and its dated-snapshot
warnings (market numbers) are pinned; every relative link resolves
and the page keeps its re-verify instruction for market figures.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAQ = (REPO / "FAQ.md").read_text(encoding="utf-8")


def test_relative_links_resolve() -> None:
    for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", FAQ):
        link = m.group(1)
        if link.startswith(("http", "mailto")):
            continue
        assert (REPO / "FAQ.md").parent.joinpath(link).resolve().exists(), link


def test_market_numbers_carry_the_reverify_warning() -> None:
    flat = re.sub(r"\s+", " ", FAQ)
    assert "dated snapshots" in flat or "re-verify" in flat
