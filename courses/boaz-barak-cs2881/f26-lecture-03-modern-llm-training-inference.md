# Fall 2026 Lecture 3 — Modern LLM training and inference: the systems layer joins the stack

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Fall 2026 Lecture 3: Modern LLM Training and Inference](https://www.youtube.com/watch?v=Lp_e8Ts5-nE) (1:16:37) · Fall 2026 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The September 17 substrate lecture: the training
pipeline of 2025 plus the inference-systems half — serving math,
KV-caches, quantization, reasoning-model training, and on-policy
distillation as the transfer vehicle.

## The announced scope

Announced on the course page: a nine-item ordered
reading list with per-item section guidance, from Horace He's
compute-first essay through SmolLM3, plus the experiment on false
statements as filler tokens for LLM reasoning (Andrew Wu and Andrea
Chen).

## The published reading list (Fall 2026 Lecture 3, Sep 17, as listed on the course page)

Required, in order, with the course page's own section guidance:
Horace He, "Making Deep Learning Go Brrrr From First Principles"
(read whole); Austin et al., "All the Transformer Math You Need to
Know" (through gradient checkpointing and KV-cache); Austin et al.,
"All About Transformer Inference" (basics through memory, then GQA
and quantization); Lambert, "Instruction Fine-Tuning" (opening, chat
templates, best practices, implementation); Lambert et al.,
"Illustrating Reinforcement Learning from Human Feedback" (the
three-stage pipeline and limitations); OpenAI Spinning Up Part 3
(policy-gradient derivations, interpreting actions as tokens and
returns as verifier scores); Lambert, "Reasoning and Inference-Time
Scaling" (RLVR's role, RL training vs. inference-time scaling,
reasoning-model practices); Lu & Thinking Machines Lab, "On-Policy
Distillation" (through implementation, plus the reasoning section);
and the SmolLM3 report (pretraining, mid-training, post-training
through model merging). Optional: the vLLM/PagedAttention paper and
Stanford CS336's scaling-laws lecture. The full list with links lives
on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. From "how models are trained" to "how models are served"

The Fall 2025 substrate lecture covered the training pipeline; the
2026 revision adds the **inference-side** half — the systems view
(KV-cache, attention math, memory bandwidth, quantization, serving
engines) that determines what deployment actually costs and what
latency budgets safety mechanisms get. The systems reading list
(Horace He's compute-first essay, the transformer-math pair) teaches
safety students what every infrastructure engineer knows: constraints
live in bandwidth and memory, and any monitor, refusal layer, or
control wrapper you design must fit inside them.

### 2. The reasoning-model stack, end to end

Lambert's Reasoning chapter plus the on-policy distillation post give
the current shape of the reasoning era: RL against verifiable rewards
to build long chains of thought, then *distillation* of those chains
into cheaper students — with the safety-relevant twist that a
distilled model inherits the teacher's reasoning behavior without the
RL process that produced it. Every safety property that lived in the
process (verification, monitoring hooks) must survive the compression
or it is gone. This is the substrate version of the "does alignment
survive transfer" question the Fall 2025 opening experiment asked.

### 3. On-policy distillation as the new transfer vehicle

The TML post on the reading list matters beyond efficiency: on-policy
distillation (student generates, teacher's logits supervise) has
become the default way capability — and behavior — moves between
models. For safety that makes distillation a first-class research
object: it is the mechanism by which refusals, personas, quirks, and
failure modes propagate across the ecosystem, bypassing both
pretraining and explicit post-training. The repo's
[Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md)
carries the post-training side; this lecture is where the transfer
mechanics live.

### 4. A real open-model spec as a worked example

SmolLM3 closes the list because it is a fully documented open-model
build — pretraining, mid-training, and post-training decisions in the
open. Reading a complete model card as a *safety document* (what
choices were made, what was measured, what was skipped) is the
companion skill to Lecture 4's spec-drafting, and it previews the
open-weights lecture later in the term.

## Through-line to this repository's chapters

- [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) —
  the post-training and transfer layer this lecture grounds.
- [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) —
  the deployment/systems constraints safety mechanisms must respect.
- [research/ai-researcher-from-scratch/](../../research/ai-researcher-from-scratch/README.md) —
  the repo's own build-the-mechanics track for the same substrate.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
