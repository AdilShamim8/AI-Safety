# Lecture 7 — Lab vs field: capabilities, safety, and the measurement gap (Joel Becker, METR)

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 7: Lab vs Field: Guest lecture by Joel Becker](https://www.youtube.com/watch?v=fuRmxFZ-umE) (2:01:36) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The measurement lecture, delivered by METR's Joel Becker under
the course's "Capabilities vs. Safety" title. Announced topics: growth
in capabilities (METR task doubling, developer productivity, GDPval);
what it means for large-scale job displacement and automating AI R&D;
the OpenAI Preparedness framework and the RSP family.

## The announced scope

Announced on the course page: the METR measurement program,
the responsible-scaling policy family, and the lab-vs-field evaluation
distinction that ties them together.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Becker, Rush, Barnes & Rein, "Measuring the Impact of
Early-2025 AI on Experienced Open-Source Developer Productivity" (2025);
the METR GPT-5 report; Anthropic's Responsible Scaling Policy (the repo
registers the announcement page); OpenAI's Preparedness Framework v2
(the repo registers the beta structure). Optional list: "Canaries in
the Coal Mine" (Brynjolfsson, Chandar & Chen); METR's long-task
measurement, "Common Elements of Frontier AI Safety Policies," and
HCAST; Davidson's AGI transition scenarios; the four labs' scaling
policy announcements; Shevlane et al., "Evaluating Frontier Models for
Extreme Risks"; the UK frontier AI policy paper, the EU AI Act code of
practice, the US AI executive order, NIST AI RMF (repo-registered),
Sastry et al. on compute governance, and ISO/IEC 42001. The full list
with links lives on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. The lecture's title contrast: lab vs field

Guest lecturer Joel Becker (METR) brings the evaluation community's
central lesson: **lab evaluations and field performance are different
objects**. A capability measured in a controlled harness establishes a
ceiling, not a deployment outcome; conversely, field productivity gains
measured on real developers establish a floor for economic impact, not
a capability claim. METR's randomized developer-productivity study —
which found experienced open-source developers were actually *slowed*
by early-2025 AI on their own repos while believing they had been
sped up — is the canonical demonstration that self-reported uplift is
not evidence, and that the lab/field distinction is not pedantry.

### 2. The RSP family: capability thresholds as governance triggers

The responsible-scaling policies (Anthropic's RSP, OpenAI's
Preparedness Framework, DeepMind's Frontier Safety Framework) are the
labs' answer to "when does a model become too dangerous to ship
unchanged": define capability thresholds (uplift on CBRN, cyber,
autonomy), evaluate against them, and attach required safeguards per
tier. The lecture's skeptical angle is exactly this repo's
[Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md)
angle: thresholds inherit every evaluation-science limitation
(construct validity, contamination, adaptive overfitting) plus the
incentive problem — the lab grading its own homework.

### 3. METR's measurement program as the connective tissue

Task-length horizons, HCAST, developer-productivity RCTs, the common
elements analysis — METR's output is the closest thing the field has
to a measurement institution, and the lecture uses it to teach the
difference between *capability forecasting* (doubling curves) and
*safety evidence* (what a given model cannot yet do, measured how?).
The repo's [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md)
is the methods layer under all of it.

## Through-line to this repository's chapters

- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  evaluation science: the chapter this lecture assumes.
- [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) —
  dangerous-capability evaluation and release decisions.
- [Ch. 23](../../chapters/23-governance-and-standards/README.md) — the
  RSP/Preparedness family as private governance instruments.
- [research/notes/comparison-05-static-benchmarks-vs-adaptive-evaluation.md](../../research/notes/comparison-05-static-benchmarks-vs-adaptive-evaluation.md)
  — the repo's own comparison note on exactly the lab/field tension.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
