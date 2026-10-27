# Part 2.7 — Alignment stress tests: red-teaming the alignment program itself

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 7. Alignment stress tests](https://www.youtube.com/watch?v=vswXc-_Chtg) (3:44) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

Part 2's closer (3 minutes): adversarially testing
whether the alignment measures actually hold — stress tests, red
teaming, and the model-organisms program that deliberately builds
misaligned examples to study detection and containment.

## Core ideas, explained

### 1. Testing the defenses, not just the model

The reflexive move: every mechanism in Parts 2.1–2.6 is itself a
claim that can be stress-tested. Red teams attack the oversight
structure, the control protocol, the monitor — not only the model.
The repo's [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md)
teaches exactly this discipline, and its evaluation-supply-strategy
comparison note prices the "who builds the evals" problem.

### 2. Model organisms of misalignment

The research program that builds deliberately misaligned systems at
small scale — sleeper agents, reward tampering, goal misgeneralization
demos — to develop detection and control under ground truth. The
repo registers the sleeper-agents paper and carries its note; the
Harvard course's scheming lecture works the same lineage.

### 3. The compounding caveat

Stress tests establish *this attack, this defense, this budget* —
never safety in general. The course closes Part 2 with the honest
frame it opened with: a stack of partial measures, each stress-tested
within its scope, is the actual deliverable. The repo's
[Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md)
supplies the methodology that keeps that claim honest.

## Through-line to this repository's chapters

- [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) —
  the red-teaming chapter.
- [research/notes/04-sleeper-agents.md](../../research/notes/04-sleeper-agents.md) —
  the model-organisms flagship.
- [research/notes/comparison-12-evaluation-supply-strategies.md](../../research/notes/comparison-12-evaluation-supply-strategies.md) —
  who builds the evals.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
