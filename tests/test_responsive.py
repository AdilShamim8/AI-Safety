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


# ------------------------------------------------------------------
# session 6 (part 2) — the viewport guard. A real complaint screenshot
# showed the page laid out at a ~980px desktop canvas on a phone: the
# browser had ignored the viewport meta (desktop-mode request or an
# in-app WebView), so every media query missed and the phone showed a
# sliced desktop page — giant clipped headings, text cut at the right
# edge, a sideways scrollbar. Media queries cannot fire in that state,
# so the phone layout is ALSO driven by a class the head script sets
# from the real constraints (coarse pointer, small physical screen,
# clientWidth too wide for it), and the guard stylesheet is derived
# mechanically from the template's own media blocks at build time.
# ------------------------------------------------------------------


def test_viewport_guard_script_present() -> None:
    """The head script detects the meta-ignored state and marks <html>."""
    tpl = _tpl()
    assert 'classList.toggle("vw-guard"' in tpl
    assert 'matchMedia("(pointer:coarse)")' in tpl
    assert "screen.width" in tpl
    assert "cw > 640" in tpl
    html = _html()
    assert 'classList.toggle("vw-guard"' in html


def test_viewport_guard_reaches_540_and_600px_screens() -> None:
    """s7: the first guard gated at screen.width <= 500 and missed the
    540/600px CSS-width budget phones entirely — a meta-ignoring browser
    on those screens still showed the sliced desktop page. The gate now
    reaches 620; a real tablet still never passes, because with the meta
    honored its clientWidth equals its screen.width under the 640 bar."""
    tpl = _tpl()
    assert "sw <= 620" in tpl
    assert "sw <= 500" not in tpl
    html = _html()
    assert "sw <= 620" in html


def test_viewport_guard_font_scale_compensation() -> None:
    """s8: the s7 zoom compensation is gone — zoom shrank the layout
    viewport itself, so the 520px body cap and px paddings written for
    the oversized canvas overflowed it and the page rendered magnified
    past the right edge (the owner's second complaint, reproduced at
    427px in DevTools). The guard now scales type instead: the head
    script publishes --vfs (canvas over screen, clamped 1.05..3) and
    every font-size in the derived layer is wrapped in
    calc(*var(--vfs,2.2)) — font sizes cannot change clientWidth, so
    no freeze is needed and no oscillation is possible."""
    tpl = _tpl()
    assert 'setProperty("--vfs"' in tpl
    assert "Math.max(1.05, Math.min(3" in tpl
    assert "--vgz" not in tpl
    assert "hit === null" not in tpl
    html = _html()
    assert "--vgz" not in html
    assert "zoom:var(" not in html
    assert "max-width:520px" not in html
    assert "html.vw-guard{overflow-x:clip}" in html
    # the base tier is derived too, so body type reads at physical size
    assert "html.vw-guard body{font-size:calc(16px*var(--vfs,2.2))}" in html


def test_viewport_guard_remeasures_not_frozen() -> None:
    """s8: the s7 verdict froze on first-run geometry, so a transiently
    wrong first measurement stayed wrong for the page's life. The guard
    now re-detects on every event (apply() calls detect() directly),
    listens on pageshow for bfcache restores, and re-checks once more
    800ms after load for late viewport changes — a false verdict
    self-corrects instead of persisting."""
    tpl = _tpl()
    assert "var hit = detect();" in tpl  # re-detected on every apply()
    assert 'classList.toggle("vw-guard", hit)' in tpl
    assert 'addEventListener("pageshow"' in tpl
    assert "setTimeout(apply, 800)" in tpl
    html = _html()
    assert "var hit = detect();" in html


def test_guard_layer_scales_every_font_size() -> None:
    """s8: the derivation must scale every font-size it emits — the
    base tier included, so type the media blocks never re-set still
    reads at physical size on the downscaled canvas — and must never
    leave an unscaled one behind."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import build_dashboard  # noqa: E402

    layer = build_dashboard._guard_layer(_tpl())
    total = layer.count("font-size:")
    wrapped = layer.count("font-size:calc(")
    assert total > 100  # the base tier alone carries ~114 font rules
    assert total == wrapped, "a guard font-size escaped the --vfs scaling"


def test_phone_layer_breaks_slash_joined_tokens() -> None:
    """s7: chapter descriptions carry slash-joined vocabulary runs that
    the line breaker treats as one word; at 320px the first chapter's
    run ("hazard/capability/propensity/exposure/severity", ~269px at
    13px sans) alone pushed the layout viewport 15px past the screen.
    The phone layer now wraps such tokens anywhere — in the media block
    and in the guard layer derived from it."""
    tpl = _tpl()
    assert ".chap .cb .cd{overflow-wrap:anywhere}" in tpl
    assert ".dtab td.clm{overflow-wrap:anywhere}" in tpl
    assert ".awe{overflow-wrap:anywhere}" in tpl
    assert ".note{overflow-wrap:anywhere}" in tpl
    html = _html()
    assert ".chap .cb .cd{overflow-wrap:anywhere}" in html
    assert "html.vw-guard .chap .cb .cd{overflow-wrap:anywhere}" in html


def test_guard_layer_derived_into_page() -> None:
    """The generated page carries the re-scoped phone layer."""
    html = _html()
    assert "s6/s8 viewport-guard layer — DERIVED" in html
    assert "html.vw-guard body{overflow-wrap:anywhere}" in html
    assert "html.vw-guard{overflow-x:clip}" in html
    assert (
        "html.vw-guard #topBtn{width:calc(48px*var(--vfs,2.2));"
        "height:calc(48px*var(--vfs,2.2))}" in html
    )
    assert "html.vw-guard .toc-toggle{display:flex" in html
    assert "html.vw-guard .dtab td.hide-m{display:block}" in html
    assert "@media (orientation:landscape){html.vw-guard .toc{max-height:56vh}}" in html


def test_guard_layer_matches_derivation_exactly() -> None:
    """No drift: the emitted layer is character-for-character the derivation."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import build_dashboard  # noqa: E402

    layer = build_dashboard._guard_layer(_tpl())
    assert layer in _html(), "guard layer drifted from the media blocks"


def test_guard_layer_excludes_print_and_stray_blocks() -> None:
    """The single-line sticky-th stray must not swallow the print rules."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import build_dashboard  # noqa: E402

    layer = build_dashboard._guard_layer(_tpl())
    assert "@page" not in layer
    assert "page-break" not in layer
    assert "top:41px" not in layer
