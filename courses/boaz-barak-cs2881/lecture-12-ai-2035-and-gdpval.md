# Lecture 12 — AI in 2035 and GDPval: measuring the economy a model could touch

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 12: AI in 2035 and GDPval](https://www.youtube.com/watch?v=BNSHJLLpsGM) (1:47:41) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The closing lecture of the Fall 2025 course, with guest
lecturers Tejal Patwardhan and Kevin Liu (OpenAI). Announced focus:
future directions in AI safety research, with GDPval — OpenAI's
GDP-weighted occupational-task benchmark — as the measurement
artifact at the center.

## The announced scope

Announced on the course page: discussion of future directions
in AI safety research; the archived resources block was still marked
as to-be-determined at freeze.

## The published reading list (Fall 2025, as listed on the course page)

Guest lecturers: Tejal Patwardhan and Kevin Liu (OpenAI). The course
page lists the lecture as "AI 2035" with discussion of future
directions in AI safety research; its resources section was still
marked "to be determined" at the archive's freeze. The lecture's
worked material — GDPval, the economics-of-AI measurement program —
is introduced in this course's Fall 2026 continuation and in OpenAI's
published GDPval documentation. See the
[course page](https://boazbk.github.io/mltheoryseminar) for the record as archived.

## Core ideas, explained

### 1. GDPval: benchmarking the economy instead of the model

GDPval is the lecture's load-bearing artifact (and the reason the
playlist titles this "AI in 2035 and GDPval"): a benchmark built from
real occupational tasks sampled proportionally to US GDP components,
so that model performance on the task set estimates the fraction of
economic activity the system could, in principle, automate. The
methodological move is worth staring at: instead of asking "how smart
is the model," it asks "how much of the measured economy does this
capability touch" — measurement aligned to the variable the growth
debate is actually about.

### 2. What a labor-share estimate is and is not

A GDPval-style estimate prices *task-level capability*, not
deployment: the gap between "can do the core task" and "is doing the
job" contains adoption friction, integration cost, regulation,
trust, and the parts of occupations that are not their task lists.
The honest use of these numbers is as a leading indicator with a
stated construct (see Ch. 02's construct-validity discipline), never
as a layoff forecast. The repo's dataset catalog treats GDPval as a
real-world economics-of-AI dataset exactly with that caveat.

### 3. AI in 2035: scenario discipline, again

The "2035" framing returns the course to its opening move: with
timelines this uncertain, the responsible output is not a point
prediction but a set of priced scenarios with stated dependencies and
leading indicators to watch. The course closes where it opened —
measurement and scale — now with a semester of machinery for both.

## Through-line to this repository's chapters

- [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) —
  economic-capability benchmarks as release-relevant evaluation.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  construct validity for economic capability claims.
- [datasets/README.md](../../datasets/README.md) — GDPval as a
  real-world dataset in the catalog's economics cluster.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
