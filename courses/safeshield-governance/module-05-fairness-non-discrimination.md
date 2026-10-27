# Module 5 — Fairness and non-discrimination: metrics, law, and the impossibility results

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [Fairness and Non-Discrimination in AI Systems](https://www.youtube.com/watch?v=w3P6mTI8SkU) (46:19) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The fairness module: how discrimination enters ML
(data, labels, proxies, feedback), the fairness-metric zoo and its
impossibility results, and the legal doctrines (disparate treatment,
disparate impact) that make fairness a compliance object.

## Core ideas, explained

### 1. Where bias actually enters

The module's pipeline view: historical data encodes past
discrimination; labels carry annotator priors; features proxy for
protected attributes (zip code ≈ race in US data); objective
functions optimize whatever the proxy rewards; deployment feedback
loops compound it. Each entry point has a different remedy — and
remedies applied to the wrong entry point do nothing, the fairness
version of the genesis-taxonomy lesson from the DeepMind course in
this library.

### 2. The metric zoo and the impossibility theorems

Demographic parity, equalized odds, calibration, counterfactual
fairness — the module teaches the main metrics and the honest
theorem at the field's center: several desirable fairness criteria
are mutually unsatisfiable except in degenerate cases. Choosing a
metric is therefore a *policy* choice to be documented and defended,
not a technical default. The repo's dataset cards carry fairness
metrics for exactly this reason.

### 3. The legal floor

Anti-discrimination law's two doctrines — intentional
(disparate treatment) and effects-based (disparate impact, the
four-fifths rule in US employment) — predate ML and apply to it
through the outcomes they inspect. The module maps metrics to
doctrines: which metric a regulator will accept is a question of
which statute you live under — the practical reason fairness work
is jurisdictional.

## Through-line to this repository's chapters

- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) —
  fairness in deployed sociotechnical context.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  the measurement discipline fairness metrics need.
- [datasets/README.md](../../datasets/README.md) — the fairness
  dataset cluster (BBQ, BOLD, StereoSet, and the rest).

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
