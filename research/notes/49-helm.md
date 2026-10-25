# Note: HELM — evaluation as a coverage discipline, not a leaderboard (2022)

Source: SRC-PAPER-124 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The 2022 status quo the abstract opens with: LMs becoming "the
foundation for almost all major language technologies" while their
"capabilities, limitations, and risks are not well understood" — and
the leaderboard ecosystem making it worse by collapsing that
multi-dimensional unknown into one accuracy number on one benchmark.
HELM's answer is a *coverage discipline*:

1. **Taxonomize first** — the space of scenarios (use cases) and
   metrics (desiderata) — then select a subset *based on coverage and
   feasibility*, while **noting what is missing or underrepresented**
   (the abstract's own examples: QA for neglected English dialects,
   trustworthiness metrics). The omissions list is part of the method,
   not an apology.
2. **Multi-metric measurement** — 7 metrics per scenario (the abstract
   lists accuracy, calibration, robustness before truncating; the
   course's glossary carries the rest of the family as HELM's seven).
3. The same model measured across the scenario × metric grid —
   transparency through *breadth with stated holes*, not a single
   crowning score.

## Why the course cares more about the method than the numbers

HELM's tables (body-level, unclaimed here) age like benchmarks; its
*method* is durable and the course imports it wholesale:

1. **Coverage-over-rank is Ch. 02's first commandment.** A safety-relevant
   eval names its scenario axis, its metric axis, and — the HELM move
   most copied into this course — **its own underrepresented omissions
   in writing**. The audit's missing-values discipline and the
   dashboard's honesty ledger are this move at repo scale.
2. **The multi-metric grid is the anti-Goodhart instrument.** Note 37's
   proxy-divergence logic applies to evaluations themselves: any single
   metric optimized hard detaches from the desideratum it proxied.
   HELM's grid makes the detachment *visible* (accuracy up, calibration
   down, robustness sideways) — the pattern the P01 harness reproduces
   with its paired metric ledgers.
3. **Calibration as a first-class metric** — the abstract's truncated
   list already includes it — is why P03's instruments (reliability
   tables, ECE-with-binning, risk-coverage) have a field-standard
   citation rather than a folklore one. A deployment that reports only
   accuracy is running a pre-HELM evaluation stack.

## What the abstract establishes

1. The taxonomize→select→note-gaps methodology (quoted above).
2. The multi-metric commitment with the 7-metric count and the first
   three named.
3. The transparency framing — HELM's stated purpose — which is why the
   course files it under *evaluation science* rather than *benchmark*.

Unclaimed: the scenario list, per-model results, the leaderboard
infrastructure, and the four metrics the truncation cut (the course's
readings name them — fairness, bias, toxicity, efficiency — via the
body at its own access level; this note flags the boundary honestly).

## Why this note exists in the course

Chapter 02 needed the canonical bridge from "benchmarks exist" to
"evaluation is a designed instrument with declared coverage." HELM is
that bridge, and three later chapters inherit it directly:

- **Ch. 17** (deployment reliability): the scenario axis is where
  *deployment distributions* enter evaluation design — HELM's
  taxonomy is the vocabulary P09's shift-audit uses for its slices.
- **Ch. 20** (dangerous capabilities and release): the release-eval
  question "what did we *not* measure?" is the HELM omissions-list
  discipline promoted to a gate artifact — the safety-case template's
  residual-coverage field.
- **Ch. 22** (safety engineering): the multi-metric grid is the shape
  of the deployment dashboard — no single green number, ever; a grid
  with named holes, which is also this repo's dashboard design rule
  (the honesty ledger at the front door).

The note closes a trio with notes 41 and 48: model-written evals
(breadth, with generator blind spots), inverse scaling (scale-axis
honesty), HELM (coverage-axis honesty). Together they are Ch. 02's
"what a modern evaluation owes you" — and all three are 2022–2023
documents the field is still catching up to.

## The falsifiable extension (deterministic tier)

The HELM grid is a *report format*, runnable on anything:

- Take P01's existing results and re-render them as a HELM-style
  scenario × metric grid (scenarios = the harness's case families;
  metrics = accuracy, calibration-ish discrimination (the harness's
  score separation), robustness (perturbation arm), abstention
  quality (P03-style selective metrics) — at least four axes).
- Prediction worth testing: at least one model/case-family pair
  *reorders* between metric axes (better accuracy, worse selective
  risk) — the anti-Goodhart pattern made visible in the course's own
  numbers, not just the literature's.
- Falsifier: perfectly correlated axes across all families would make
  the multi-metric discipline redundant *at this tier* — worth knowing
  before anyone spends model-tier compute expanding the grid.
