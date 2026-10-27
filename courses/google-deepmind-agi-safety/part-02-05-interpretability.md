# Part 2.5 — Interpretability: opening the box before trusting the output

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 5. Interpretability](https://www.youtube.com/watch?v=G2AenEl9A4Y) (4:35) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The fourth mechanism (4 minutes): interpretability
as evidence about the model's internals — features, circuits,
representation-level signals — complementing behavioral evaluation
with mechanistic reads.

## Core ideas, explained

### 1. Two evidentiary channels

Behavioral evaluation answers "what does the model do";
interpretability answers "what is the model computing and why."
For safety claims — especially *absence* claims ("it is not
scheming") — the internal channel is in principle stronger: a
capability could be latent and unexercised. In practice both
channels are partial, and the honest posture is triangulation
(the repo's comparison note on behavioral vs. mechanistic evidence).

### 2. The SAE program and its evaluation problem

Sparse autoencoders dominate current mech-interp practice (the
Harvard interpretability lecture's guests are the program's leads);
the field's own stress tests — AxBench's baseline comparison,
steering-vs-monitoring gaps — define what "interpretable enough for
safety" would have to mean. The repo's
[Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md)
is that evaluation layer.

### 3. The monitoring connection

Representation-level signals (persona vectors, internal-state
truthfulness probes — both registered in the repo's spine) give
monitoring a channel that the model's *output* cannot fully fake:
useful precisely because output-channel monitors become training
targets and degrade (the obfuscation trap). Internal channels have
the same exposure in principle — the arms race just moves.

## Through-line to this repository's chapters

- [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md)
  and [Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md) —
  the interpretability arc.
- [research/notes/51-internal-state-truthfulness.md](../../research/notes/51-internal-state-truthfulness.md) —
  the internal-signal monitoring line.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
