# Part 2.4 — Security and control: assuming the model is adversarial

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 4. Security & control](https://www.youtube.com/watch?v=8wmZ0JK8kKM) (5:11) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The third mechanism (5 minutes): the control
paradigm — engineer the deployment environment so that even a
misaligned model cannot cause harm unmonitored: trusted/untrusted
separation, privilege boundaries, fallback modes, containment.

## Core ideas, explained

### 1. The paradigm shift: from alignment to containment

Control's move is to stop assuming alignment succeeds: design the
*system around the model* — which tools it can call, what a trusted
monitor sees, what happens when confidence drops — so that an
adversarially-capable model still cannot convert intent into harm.
The safety case becomes an engineering argument about the protocol,
auditable in a way inner objectives are not. The repo's
[Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) and
its control-protocol project are the full treatment.

### 2. Trusted/untrusted separation

The core pattern: trusted (weaker, safer) models supervise untrusted
(stronger) ones on the privileged path; untrusted output never
directly executes privileged actions unmonitored. The safety-case
sketches from the Harvard course's reading list (Korbak et al.) are
the worked versions; the repo's comparison note on alignment-vs-control
maps the philosophical difference.

### 3. Security as the substrate

Control inherits classic security engineering — least privilege,
defense in depth, fail-safe defaults — and the course's placement of
this *inside* the alignment program (not beside it) is itself a
position: the alignment problem is an extension of the security
problem, not a separate discipline. The Harvard course's robustness
lecture made the same move.

## Through-line to this repository's chapters

- [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) —
  the control chapter.
- [research/notes/comparison-03-alignment-vs-control.md](../../research/notes/comparison-03-alignment-vs-control.md) —
  the paradigm comparison.
- [projects/p08-control-and-monitoring-protocol/README.md](../../projects/p08-control-and-monitoring-protocol/README.md) —
  the repo's control experiment.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
