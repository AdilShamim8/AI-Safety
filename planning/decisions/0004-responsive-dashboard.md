# ADR-0004 — The dashboard is a responsive artifact

Date: 2026-10-28 · status: accepted · scope: `index.html`,
`scripts/dashboard_template.html` (the template),
`scripts/build_dashboard.py`

## Context

The dashboard shipped as a designed page for one implicit width: the
1220px editorial frame. It carried a 960px collapse for tablets, but
nothing beneath it for phones and nothing above ~1300px for large
desktops. The session opened with a measurement rather than an
opinion: at a 390px viewport the page demanded 303px of horizontal
scroll, and the element demanding it was not a data table (those were
already wrapped in scrollers) but the AWESOME id chips — appended by
the rendering script with no break opportunities between them, so a
bold title plus four nowrap chips formed a single unbreakable run.

## Decision

1. **Measure, then fix.** The opening audit is a script
   (`scripts/visual_audit.py`), not a screenshot album: it loads the
   generated page at four widths (360, 390, 1440, 1920) and fails if
   the document carries horizontal overflow. It runs on demand (its
   dependency is optional) and any responsive change is expected to
   run it before and after.
2. **Breakpoints are a contract.** 640px (phone), 960px (existing
   collapse), 1600px (large desktop), plus two capability queries —
   `pointer:coarse` for touch targets and `prefers-reduced-motion`
   for motion gating. `tests/test_responsive.py` pins each declared
   promise against the template, which is the single source the
   generator copies.
3. **The template is the only hand-edited surface.** No responsive
   rule is written into the generated `index.html`; every rule lands
   in the template and the page is regenerated in the same commit,
   exactly as the freshness test has always demanded.
4. **One concern per unit.** The phone layer arrived as seventeen
   commits (frame, topbar, tap targets, masthead, chain, ledger,
   cards, rungs, tables, search, steps, trackers, FAQ, type,
   safe-areas), each regenerating and re-verifying the page, so any
   regression has a one-line bisect target.
5. **Desktop is not an afterthought.** The large-screen breakpoint,
   keyboard focus visibility, a skip link, and a back-to-top control
   are part of the same decision: "better on a phone and a desktop"
   is one contract, not two.
6. **Navigation is part of responsive reading.** Every markdown
   surface carries a uniform nav line under its H1 (chapters also
   close with a pointer to their successor), because the narrowest
   screen is where a dead-end page hurts most. Pinned by
   `tests/test_site_navigation.py`.

## Consequences

The page no longer horizontally scrolls at any audited width; the
data tables still scroll sideways by design (with their ID column
pinned), which the audit treats as contained, not overflowing. The
responsive contract tests run in CI with the rest of the suite, so a
future edit that deletes a breakpoint or re-welds the chips fails a
build instead of quietly regressing the phone. Print remains a
first-class target (the print block was extended in the same
session). The visual audit remains optional-dependency tooling for
humans, not a CI gate — its failure mode (playwright missing) is a
skip, never a false red.
