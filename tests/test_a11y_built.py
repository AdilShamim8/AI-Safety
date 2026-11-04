"""Built-page accessibility structure, checked without a browser.

Session-13 origin (P16): the session opened with a live axe audit that
found the two real bugs P01 fixed (contrast, heading order). This
module pins the structural half of that audit against the built
index.html so it runs in CI on every push, no browser needed: the
renderers must still emit the h3 group headings (the heading-order
fix), every icon-only control must carry an aria-label (the ten search/
filter inputs do), the page must state its language, buttons must have
visible names, focus styles must exist for keyboard users, and images
(if ever added) must carry alt text — the corpus has none today, which
the sweep verifies so a future <img> without alt cannot land silently.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HTML = (REPO / "index.html").read_text(encoding="utf-8")
TPL = (REPO / "scripts" / "dashboard_template.html").read_text(encoding="utf-8")


def test_page_declares_language() -> None:
    m = re.search(r"<html[^>]*>", HTML)
    assert m and 'lang="' in m.group(0), m.group(0) if m else None


def test_group_headings_are_real_h3s() -> None:
    assert 'el("h3","eh")' in TPL
    assert 'el("h3", null, g.term)' in TPL
    # and the built page carries the paired selectors
    assert ".gl .ge h4, .gl .ge h3{" in HTML
    assert ".inc .ib h4, .inc .ib h3{" in HTML
    assert ".step .sb h4, .step .sb h3{" in HTML


def test_every_icon_only_control_has_aria_label() -> None:
    """Nine labels on the built page: three figure regions, the chapter
    route filter, and the five search inputs. All nine pinned by name."""
    labels = re.findall(r'aria-label="([^"]+)"', HTML)
    assert len(labels) >= 9, labels
    for needed in (
        "search notes",
        "search datasets",
        "search sources",
        "search claims",
        "search glossary",
        "filter chapters by route",
    ):
        assert needed in labels, f"missing aria-label: {needed}"


def test_buttons_have_visible_names() -> None:
    btns = re.findall(r"<button[^>]*>([^<]*)</button>", HTML)
    assert btns, "no buttons found in built page"
    for b in btns:
        assert b.strip(), f"empty-named button: {b!r}"


def test_focus_styles_exist() -> None:
    assert len(re.findall(r":focus", HTML)) >= 4


def test_images_must_carry_alt() -> None:
    imgs = re.findall(r"<img[^>]*>", HTML)
    for i in imgs:
        assert "alt=" in i, i
    # the corpus is image-free today; state it so a future <img>
    # without alt cannot land silently
    assert len(imgs) == 0, f"images appeared in the dashboard: {[i[:40] for i in imgs]}"
