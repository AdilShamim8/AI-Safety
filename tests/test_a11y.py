"""Accessibility invariants for the dashboard template and build.

Session-13 origin: an axe audit of the deployed page found 15
color-contrast nodes (ink-3 at 2.8-3.3:1 against the paper tones) and
3 heading-order skips (h2 section -> h4 items, the group level was a
styled div, not a heading). Both are pinned here so a regression is
caught by the suite, not by a user's screenshot.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TPL = REPO / "scripts" / "dashboard_template.html"
HTML = REPO / "index.html"


def _tpl() -> str:
    return TPL.read_text(encoding="utf-8")


def _lum(hexstr: str) -> float:
    def f(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (int(hexstr[i : i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _ratio(fg: str, bg: str) -> float:
    a, b = sorted((_lum(fg), _lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def _var(name: str, text: str) -> str:
    m = re.search(rf"--{re.escape(name)}:(#[0-9a-fA-F]{{6}})", text)
    assert m, f"--{name} not defined"
    return m.group(1)


def test_ink3_meets_aa_on_every_paper_tone() -> None:
    """ink-3 (the small-label tone) must clear 4.5:1 on paper, paper-2,
    and paper-3 — the three backgrounds it actually sits on. Was
    #8f8674 at 2.8-3.3:1 (15 axe nodes); #6b6350 clears all three."""
    t = _tpl()
    ink3 = _var("ink-3", t)
    for bg_name in ("paper", "paper-2", "paper-3"):
        bg = _var(bg_name, t)
        r = _ratio(ink3, bg)
        assert r >= 4.5, f"ink-3 {ink3} on {bg_name} {bg}: {r:.2f} < 4.5"


def test_ink2_still_clears_every_paper_tone() -> None:
    """The body-text secondary tone stays above the bar too (5.7+ as of
    the audit) — checked so the ink-3 fix cannot be 'fixed' later by
    someone darkening the wrong variable."""
    t = _tpl()
    ink2 = _var("ink-2", t)
    for bg_name in ("paper", "paper-2", "paper-3"):
        assert _ratio(ink2, _var(bg_name, t)) >= 4.5


def test_no_heading_level_skips_in_template_headings() -> None:
    """The static template must not jump heading levels: the era header
    is an h3 now (was a styled div between the section h2 and item h4s
    — the skip axe flagged). The JS renderers build h3s at the group
    level; their selectors are pinned here too."""
    t = _tpl()
    assert 'el("h3","eh")' in t, "era headers must be real h3 headings"
    assert 'el("h3", null, g.term)' in t, "glossary group rows must be h3"
    html = HTML.read_text(encoding="utf-8")
    assert ".gl .ge h4, .gl .ge h3{" in html
    assert ".inc .ib h4, .inc .ib h3{" in html
    assert ".step .sb h4, .step .sb h3{" in html
    # and the UA-default resets that keep the h3s pixel-identical
    assert "h3.eh{margin:0" in t
