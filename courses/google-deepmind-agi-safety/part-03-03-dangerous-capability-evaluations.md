# Part 3.3 — Dangerous capability evaluations: the course's closing instrument

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 3: 3. Dangerous capability evaluations](https://www.youtube.com/watch?v=00h9yaN5un4) (6:26) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The course's final video (6 minutes): how
dangerous-capability evaluations are actually built and used —
cyber-offense uplift, CBRN knowledge, autonomous reproduction,
persuasion — and what an evaluation can and cannot establish.

## Core ideas, explained

### 1. The uplift measurement frame

The modern dangerous-capability eval measures *uplift*: how much
better does a competent adversary become with the model than without
it? The frame is honest about the base rate (capabilities exist
outside the model) and focuses the safety question on marginal
contribution — the construct validity discussion the repo's
[Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md)
centers.

### 2. Autonomy as the compounding axis

Among the capability clusters, autonomy (can the model operate
independently for long horizons; can it acquire resources; can it
improve itself) is the one that compounds all the others — the
recursive-self-improvement lecture in the Harvard course (this
library) is the growth-model version of the same worry. METR's
task-horizon measurement (registered) is the leading indicator.

### 3. What an eval can establish

The closing honesty: evaluations establish *capability under the
tested conditions* — not intent, not deployment behavior, not what a
motivated adversary will find six months later with the same weights.
The gap between "passed the eval" and "safe" is the entire reason
Parts 2 and 3 exist as a stack. The course ends where the repo
begins: safety is a claim about evidence, never a property.

## Through-line to this repository's chapters

- [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) —
  the dangerous-capability chapter.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  what evaluations can establish, methodologically.
- [courses/boaz-barak-cs2881/lecture-07-lab-vs-field.md](../boaz-barak-cs2881/lecture-07-lab-vs-field.md) —
  the externalist view of the same instrument.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
