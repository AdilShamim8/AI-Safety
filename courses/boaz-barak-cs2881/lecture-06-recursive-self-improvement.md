# Lecture 6 — Recursive self-improvement: takeoff models and their speed limits

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 6: Recursive Self Improvement](https://www.youtube.com/watch?v=wzep3Rnv6iw) (2:29:33) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The takeoff lecture: what happens when AI starts accelerating AI
R&D itself. Announced framing question: "Is AI R&D an 'AI-complete'
task?" — with the growth economics literature (Davidson, Epoch,
Aghion–Jones–Jones) as the quantitative spine and the skeptics' file
as the assigned counterweight.

## The announced scope

Announced on the course page: takeoff models, intelligence
explosion typologies, GATE-style automation trajectory modeling, and
the experiment on whether narrow-task success requires broad general
skills.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Tom Davidson, "Takeoff Speeds" (the Anthropic talk);
Davidson, Hadshar & MacAskill, "Three Types of Intelligence Explosion"
(2025); Epoch AI, "GATE: Modeling the Trajectory of AI and Automation"
(2025); Epoch AI, "AI in 2030" (2025). Optional list: Aghion, Jones &
Jones on AI and economic growth; Davidson & Houlden on software
intelligence explosions; the ETH–Davidson question on whether AI R&D
automation causes one; Erdil & Besiroglu's idea-production survey and
explosive-growth review; Schrittwieser's "The Case Against the
Singularity" and "Failing to Understand the Exponential, Again";
AlphaZero; and Davidson's takeoff simulation playground. The full list
with links lives on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. The question behind the lecture: is AI R&D AI-complete?

The announced framing question — "Is AI R&D an 'AI-complete' task?" —
is the crux of every takeoff model. If automating AI research requires
solving general intelligence (AI-complete), self-improvement stalls at
tool-assisted human speed. If it decomposes into ordinary research
tasks (literature synthesis, experiment scaffolding, hyperparameter
search, code), then AI systems can meaningfully accelerate the research
that improves them, and growth dynamics — not alignment intentions —
set the timeline. Everything else in the lecture is machinery for
pricing that one conditional.

### 2. Three types of intelligence explosion

The Davidson–Hadshar–MacAskill typology is the reading list's spine:
a *software-only* explosion (better algorithms alone, compute fixed),
a *compute-driven* explosion (recursive software gains plus rapidly
expanding hardware), and an *overhang-driven* explosion (compute is
already there; only software lags). Each has different signatures,
different speed limits, and different safety implications — most
crucially for control: the faster the software-only variant, the less
wall-clock time any monitoring or pause mechanism gets to act.

### 3. Takeoff speeds as the safety-relevant variable

Davidson's takeoff-models work parameterizes exactly the quantity
safety arguments quietly assume: how long is the interval between
"AI meaningfully accelerates AI R&D" and "AI does AI R&D better than
the human frontier"? Long intervals leave room for evaluation,
governance, and correction; short ones leave room only for
pre-commitment. The lecture's job is to show this is an *empirical*
quantity with measurable intermediate markers (METR's task-length
trend from Lecture 1 is one such marker), not a philosophical mood.

### 4. The skeptics' file is on the list too

Schrittwieser's two essays and the Erdil–Besiroglu line are the
assigned counterweight: exponentials in compute do not automatically
become exponentials in useful capability; idea production may face
diminishing returns; deployment friction eats lab gains. The course's
method — strongest version of each side, then price — applies with
special force here because the disagreement is about growth rates,
where a small parameter difference compounds into opposite worlds.

## Through-line to this repository's chapters

- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) —
  the systemic-risk chapter carries the growth-and-cascade material.
- [Ch. 24](../../chapters/24-research-practice-and-capstone-execution/README.md) —
  the capstone's scenario-and-evidence discipline is the learner-scale
  version of pricing takeoff claims.
- The [DeepMind course](../google-deepmind-agi-safety/README.md)'s
  Part 1 videos are the compressed version of the same risk-model
  terrain.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
