# Lecture 1 — Introduction: AI 2027, normal technology, and the measurement-and-scale frame

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 1](https://www.youtube.com/watch?v=-NCiWaRS6So) (2:25:51) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The opening lecture of Harvard's first AI safety course. Its job is
to set the epistemic terms: the field's disagreement is real and
quantitative (timelines, takeoff, controllability), the course will
not resolve it by fiat, and the tools for making progress are
measurement and scale analysis rather than argument. The Fall 2026
iteration reopens the same questions with a fresh, incident-heavy
reading list.

## The announced scope

Topics announced on the course page: introduction to the course's
method; the risk landscape; the experiment — "Emerging alignment":
fine-tune a model on outputs from a model with a 'good persona' and
evaluate transfer to other datasets, including a 'subtle alignment'
variant with random inputs.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: *AI 2027* (the scenario document); Narayanan & Kapoor,
"AI as Normal Technology"; METR, "Measuring AI Ability to Complete Long
Tasks." Optional resources listed: Bostrom's Vulnerable World Hypothesis
(and Nielsen's detailed notes), the AI X-risk Persuasion Tournament, the
Cotra–Narayanan speed-limit debate and the Erdil–Cotra–Kokotajlo timelines
debate, Carlsmith's "Is Power-Seeking AI an Existential Risk?", Open
Philanthropy's AI 2023 Review & Forecast, the Alignment Forum glossary,
and Epoch AI's compute-trends work. The full list with links lives on the
[course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. The course's opening move: take every position seriously, then price them

An introduction to AI safety that begins with *AI 2027* and "AI as Normal
Technology" — the field's most-cited acceleration scenario and its most
cited anti-alarm frame, assigned in the same week — is making a
methodological promise: no position gets dismissed, every position gets
priced. That promise is the whole shape of the field's real disagreement.
The optimist case (transformative capabilities, mostly fine outcomes) and
the pessimist case (loss of control, catastrophic outcomes) are not
different facts but different priors over the same facts — over how fast
capability compounds, how much measurement lags deployment, and how much
of the risk is already locked in by economics rather than by research.
A learner who cannot state the strongest version of the position they
disagree with is not ready to do safety work.

### 2. The two organizing axes: measurement and scale

The course's own framing (from its introduction) is that safety work
differs from capability work along two axes. **Measurement**: safety
claims resist the "improve what you measure" loop because the quantities
that matter — worst-case behavior, deceptive compliance, real-world harm —
are defined over contexts the evaluator does not control. **Scale**: every
hazard and every intervention must be asked the compound question — does
this get better or worse as models, data, compute, and deployment surface
grow? An intervention that works at toy scale and decays at frontier
scale is not a solution; it is a schedule for a failure.

### 3. METR's long-task finding: the one number to carry

"Measuring AI Ability to Complete Long Tasks" is on the pre-reading list
because it is the cleanest empirical anchor the field has for capability
trajectory: the length of software tasks AI agents can complete with
reliability has been doubling roughly every seven months, against a
background of human professional task horizons measured in hours to
months. The finding matters less as a forecast than as a *measurement
discipline* — it replaces vibes about "rapid progress" with a calibrated
horizon metric, exactly the move Chapter 01's evidence rules demand. (The
repo's Chapter 02 carries the evaluation-method side of this.)

### 4. The experiment: emerging alignment

The Fall 2025 opening experiment fine-tunes a model on the outputs of a
model with a "good persona" and evaluates transfer — asking whether
alignment-adjacent behavior propagates through distillation or stays a
surface persona. That question — does safety training survive transfer
into a new model, or was it decoration? — recurs through the whole field,
and this repository treats it as such in [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md)'s
distillation discussion and in the preference-audit project.

## Through-line to this repository's chapters

- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) —
  the risk-model discipline: converting "might be unsafe" into priced,
  checkable claims; this lecture is the motivational version of that
  chapter's entire first half.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  the METR-style horizon measurement as a worked example of evaluation
  design.
- [Ch. 24](../../chapters/24-research-practice-and-capstone-execution/README.md) —
  the course's own research-seminar practice is the model for the
  capstone's evidence discipline.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
