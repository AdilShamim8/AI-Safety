"""The responsive contract: the dashboard must work on phones and desktops.

Session 5 opened with a measured defect: at a 390px viewport the
generated page carried 303px of horizontal overflow, because the
AWESOME id chips were appended with no break opportunities between
them — a bold title plus four nowrap chips formed one unbreakable
run. The fix and the phone layer that followed are pinned here rule
by rule, against the template (the single source the generator
copies) and, where the promise is about the shipped page, against
index.html itself.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = REPO_ROOT / "scripts" / "dashboard_template.html"
HTML = REPO_ROOT / "index.html"


def _tpl() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


def _html() -> str:
    return HTML.read_text(encoding="utf-8")


def test_viewport_meta_present() -> None:
    """A page shaped for phones starts by admitting how wide it is."""
    assert 'name="viewport" content="width=device-width, initial-scale=1"' in _html()


def test_phone_breakpoint_declared() -> None:
    """The max-width:640px layer exists beneath the 960px one."""
    assert "@media (max-width:640px)" in _tpl()


def test_wide_desktop_breakpoint_declared() -> None:
    """Large monitors get their own frame, not a floating narrow column."""
    assert "@media (min-width:1600px)" in _tpl()


def test_id_chips_carry_break_opportunities() -> None:
    """The measured defect stays dead: chips are preceded by break spaces."""
    pat = (
        'row.appendChild(document.createTextNode(" "));\n'
        '        row.appendChild(el("span","srcid", id));'
    )
    assert pat in _tpl(), "template lost the chip break-space insertion"
    assert pat in _html(), "generated page lost the chip break-space insertion"


def test_reduced_motion_gates_smooth_scrolling() -> None:
    """Visitors who asked for no motion get no animated jumps."""
    assert re.search(
        r"prefers-reduced-motion:reduce\)\{.*?html\{scroll-behavior:auto\}",
        _tpl(),
        re.S,
    )


def test_focus_visible_rule_present() -> None:
    """Keyboard focus is drawn, not suppressed."""
    assert ":focus-visible" in _tpl()


def test_table_scrollers_are_named_containers() -> None:
    """All three data tables scroll inside contained wrappers."""
    assert _tpl().count('<div class="tabwrap">') == 3
    assert ".tabwrap{overflow-x:auto;overscroll-behavior-x:contain" in _tpl()


def test_touch_targets_declared() -> None:
    """Coarse pointers get lifted hit areas."""
    assert "@media (pointer:coarse)" in _tpl()


def test_back_to_top_control_present() -> None:
    """The long page carries its own way up."""
    assert 'btn.id = "topBtn"' in _tpl()
    assert "#topBtn{" in _tpl()


def test_skip_link_present() -> None:
    """The first Tab press offers to jump the contents rail."""
    assert 'a.className = "skip"' in _tpl()
    assert ".skip:focus" in _tpl()


# ------------------------------------------------------------------
# session 6 — the phone table pass. Session 5 made the page FIT a
# 390px viewport; session 6 makes the register tables READ on one.
# A 626px five-column table was never a phone layout: names wrapped
# into jagged multi-line fragments and the sticky ID column spent
# prime width on "DS-002". The pins below hold the card restack,
# the field labels that name the restacked data, the scroll
# affordance for viewports that keep the columnar form, and the
# chrome ergonomics (thumb targets, facts grid).
# ------------------------------------------------------------------


def test_phone_table_cards_declared() -> None:
    """S6: at 640px the three register tables restack as cards."""
    tpl = _tpl()
    assert "S6 phone layer" in tpl, "the s6 phone layer banner is gone"
    assert tpl.count("@media (max-width:640px)") >= 2, "the s6 layer must be its own block"
    assert ".dtab thead{display:none}" in tpl
    assert ".dtab td.hide-m{display:block}" in tpl, "phones must re-show the 960px-hidden columns"
    assert (
        ".dtab td:not([data-label]):not(.idc):not(.ttl):not(.clm){display:none}" in tpl
    ), "unlabeled redundant link cells must not render as empty card rows"


def test_card_labels_stamp_every_field() -> None:
    """The row builders stamp data-label so a restacked card names its data."""
    tpl = _tpl()
    assert "function lbl(td, label)" in tpl
    pinned_calls = (
        'tr.appendChild(lbl(el("td", null, d.organization), "Organization"));',
        'tr.appendChild(lbl(el("td", null, d.risk_area), "Risk area"));',
        'tr.appendChild(lbl(el("td","hide-m mono", d.course_use), "Course use"));',
        'tr.appendChild(lbl(el("td","hide-m", s.org), "Organization"));',
        'tr.appendChild(lbl(el("td","hide-m mono", s.accessed_on), "Fetched"));',
        'tr.appendChild(lbl(el("td","hide-m", c.evidence_strength), "Strength"));',
        'tr.appendChild(lbl(el("td","hide-m mono", c.date), "Registered"));',
    )
    for call in pinned_calls:
        assert call in tpl, f"row builder lost its label stamp: {call}"
        assert call in _html(), f"generated page lost its label stamp: {call}"


def test_table_scroll_affordance_declared() -> None:
    """A sideways-scrolling wrapper wears a fade that says so."""
    tpl = _tpl()
    assert ".tabwrap.scrollable{" in tpl
    assert "mask-image:linear-gradient(90deg" in tpl
    assert "MutationObserver" in tpl, "the fade must re-check after every re-render"
    html = _html()
    assert ".tabwrap.scrollable{" in html
    assert "MutationObserver" in html


def test_phone_topbar_targets_and_facts_grid() -> None:
    """Thumb-sized topbar links; the facts line restacks as a 2-col grid."""
    tpl = _tpl()
    assert ".topbar .acts a{display:inline-flex" in tpl
    assert ".mast .facts{display:grid;grid-template-columns:1fr 1fr" in tpl
    assert ".mast .facts .m{display:none}" in tpl
    html = _html()
    assert ".mast .facts{display:grid;grid-template-columns:1fr 1fr" in html
