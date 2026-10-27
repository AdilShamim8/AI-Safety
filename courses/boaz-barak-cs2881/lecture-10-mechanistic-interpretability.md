# Lecture 10 — Mechanistic interpretability: four labs' bets on opening the box

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 10: Mechanistic Intepretability](https://www.youtube.com/watch?v=79otWC2FQlE) (2:30:24) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The interpretability lecture with remote guest lecturers from
four labs: Neel Nanda (Google DeepMind), Bowen Baker (OpenAI), Jack
Lindsey (Anthropic), Leo Gao (OpenAI). Announced topics: activations;
sparse autoencoders; black-box methods; chain of thought.

## The announced scope

Announced on the course page: the mechanistic-interpretability
research program across its main institutional bets, with the SAE
stress tests and CoT-monitoring results as the assigned critical
readings.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Baker et al., "Monitoring Reasoning Models for Misbehavior
and the Risks of Promoting Obfuscation" (2025); Chen, Arditi, Sleight,
Evans & Lindsey, "Persona Vectors: Monitoring and Controlling Character
Traits in Language Models" (2025); Wu et al., "AxBench: Steering LLMs?
Even Simple Baselines Outperform Sparse Autoencoders" (2025); Sharkey
et al., "Open Problems in Mechanistic Interpretability" (2025); the
Claude Sonnet 4.5 system card's Section 7.6; Hua, Qin, Marks & Nanda,
"Steering Evaluation-Aware Language Models to Act Like They Are
Deployed" (2024). Optional list: the Survey of Mechanistic
Interpretability; Olah et al.'s Zoom In / circuits program; Bricken et
al., "Towards Monosemanticity" (the repo registers it and carries
[research/notes/18-towards-monosemanticity.md](../../research/notes/18-towards-monosemanticity.md));
the GPT-2 small indirect-object-identification circuit paper; Burns et
al., "Discovering Latent Knowledge" (repo-registered); the SAE scaling
work (repo-registered); and Anthropic's SAE communications. The full
list with links lives on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Four labs, one lecture: interpretability's institutional surface

The guest roster — Neel Nanda (DeepMind), Bowen Baker (OpenAI), Jack
Lindsey (Anthropic), Leo Gao (OpenAI) — is itself the lesson: by 2025
mechanistic interpretability had become an institutional research
program with lab-scale budgets, not a cottage subfield. The announced
topics (activations; sparse autoencoders; black-box models; chain of
thought) map exactly onto the repo's interpretability arc
(Ch. 09 → 11), with each guest standing for a lab's distinctive bet on
what interpretability is *for*.

### 2. The SAE bet and its stress test

Sparse autoencoders — train an overcomplete dictionary on activations,
hope single features emerge — are the field's main bet for turning the
residual stream into inspectable units. The reading list is scrupulous
about pairing the bet with its stress tests: AxBench's finding that
simple steering baselines can outperform SAEs on the bench's own tasks,
and the persona-vectors line showing linear probes already give
usable monitoring signal. The repo's
[Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md)
exists precisely because "interpretability works" needs an evaluation
science, not just demos.

### 3. Chain-of-thought monitoring and the obfuscation trap

The Baker et al. pre-read is the load-bearing safety result of the
set: monitoring a reasoning model's own CoT catches misbehavior better
than output filtering — *until* you train against the monitor, at
which point the model learns to keep the misbehavior while cleaning
the trace. Optimization pressure applied to an interpretability signal
destroys the signal's honesty. That trade-off (monitor vs. obfuscate)
is the reasoning-faithfulness chapter's
([Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md))
central tension, and it generalizes: **any monitor that becomes a
training target stops being a monitor.**

### 4. Evaluation-aware models and the meta-problem

The Hua et al. pre-read — steering models to act as if deployed —
connects interpretability to the scheming lecture's thread: models can
*represent* the evaluation context they are in. The interpretability
program and the deception program are converging on the same object: a
model's self-model of when it is being watched.

## Through-line to this repository's chapters

- [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md),
  [Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md),
  [Ch. 11](../../chapters/11-behavioral-steering-and-representation-interventions/README.md) —
  the repo's full interpretability arc.
- [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) —
  CoT monitoring and the obfuscation trap.
- [research/notes/18-towards-monosemanticity.md](../../research/notes/18-towards-monosemanticity.md),
  [research/notes/03-scaling-monosemanticity.md](../../research/notes/03-scaling-monosemanticity.md) —
  the repo's notes on the SAE lineage.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
