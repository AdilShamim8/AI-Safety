# Part 2.2 — Amplified oversight: supervision that scales with the system

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 2. Amplified oversight](https://www.youtube.com/watch?v=E9nBGNi6jQA) (6:18) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The first mechanism video (6 minutes): how do you
supervise a system on tasks you cannot do yourself? Amplified
oversight — decompose, delegate, debate, use the model to check the
model — as the scalable-oversight research program's compressed
statement.

## Core ideas, explained

### 1. The core problem: supervision's capability ceiling

If a model exceeds its supervisor on the task domain, ordinary
oversight fails — the supervisor cannot tell correct from confident.
Every amplified-oversight technique is a bet on structure rescuing
the asymmetry: *decomposition* (the supervisor can check pieces it
cannot check whole), *debate* (adversarial models expose each other's
errors to a weaker judge), *consultancy* (one-sided advocacy under
scrutiny). Each has a formal literature the repo's
[Ch. 05](../../chapters/05-scalable-oversight/README.md) walks in
depth, including the debate-optimality line in the notes.

### 2. Debate as the emblem

The debate proposal (two models argue opposing answers; a human
judges) remains the field's most-cited scalable-oversight bet because
it converts a capability gap into an adversarial structure — the
models' mutual incentive to expose flaws does the supervision work.
Its open question, honest in every treatment: does optimizing to win
debates optimize for truth, or for persuasiveness? The repo carries
both sides.

### 3. Weak-to-strong as the modern empirical anchor

The weak-to-strong generalization program (registered in the repo's
spine) gave amplified oversight its measurable form: strong student,
weak supervisor, and the question of how far elicitation and
structure recover the supervision gap. The repo's P05 project is the
learner-scale version of exactly that experiment.

## Through-line to this repository's chapters

- [Ch. 05](../../chapters/05-scalable-oversight/README.md) —
  the full scalable-oversight chapter.
- [research/notes/27-debate-optimality.md](../../research/notes/27-debate-optimality.md)
  and [research/notes/10-weak-to-strong.md](../../research/notes/10-weak-to-strong.md) —
  the two load-bearing papers.
- [projects/p05-weak-to-strong-or-scalable-oversight-analogue/README.md](../../projects/p05-weak-to-strong-or-scalable-oversight-analogue/README.md) —
  the repo's own experiment.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
