# Part 1.5 — Exercise 2: the alignment-failure classification quiz

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 1: 5. Exercise 2: Classification quiz for alignment failures](https://www.youtube.com/watch?v=h95RgGPs-ss) (2:25) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

Part 1's closing checkpoint (2 minutes): presented
with failure vignettes, the learner classifies each — specification
error, misgeneralization, feedback misspecification, instrumental
behavior — before Part 2 turns to solutions.

## Core ideas, explained

### 1. Classification as the examinable form of a taxonomy

A taxonomy that cannot be applied is decoration. The quiz format —
vignette in, class out — is the minimal examinable form, and it is
exactly what the repo's chapter exercises do with the same material
at case-study depth (see Ch. 03's exercises and the P02 project's
reward-misspecification cases).

### 2. The diagnostic payoff

Getting classification right matters operationally: response differs
by class. Specification failures argue for better objectives and
grader audits; misgeneralization argues for OOD stress tests and
interpretability; feedback misspecification argues for preference-data
audits; instrumental behavior argues for control protocols. A safety
team that cannot classify failures buys the wrong defense — which is
the practical reason this two-minute quiz sits at the hinge of the
whole course.

### 3. Where the drill deepens

The repo's [research/notes/comparison-02-behavioral-vs-mechanistic-evidence.md](../../research/notes/comparison-02-behavioral-vs-mechanistic-evidence.md)
extends the same skill one level up: not just *what* failure class,
but *what kind of evidence* establishes the classification — the
behavioral read versus the mechanistic read.

## Through-line to this repository's chapters

- [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) —
  the classification drill at full depth.
- [projects/p02-reward-misspecification-and-generalization/README.md](../../projects/p02-reward-misspecification-and-generalization/README.md) —
  the repo's own misclassification-mechanism experiment.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
