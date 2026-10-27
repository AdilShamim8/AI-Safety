# Lecture 2 — Modern LLM training and safety training

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 2: Modern LLM training and safety training](https://www.youtube.com/watch?v=GXggPt_gqiI) (2:23:02) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The course's technical substrate lecture: everything later lectures
assume about *where models come from*. Announced topics: modern LLM
training overview (DeepSeek R1 as the worked example); pretraining;
mid-training; reinforcement learning (RLHF/RLVF); safety training.
The Fall 2026 iteration extends the same spine with inference-time
scaling and on-policy distillation.

## The announced scope

Announced on the course page: the full pretraining-to-safety-training
pipeline, taught from primary sources. Experiment: "Optimizing Prompts
with Reinforcement Learning" — policy-gradient optimization of prompt
prefixes across benchmarks.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: InstructGPT (Ouyang et al. 2022) — the repo's own note is
[research/notes/26-instructgpt-pipeline.md](../../research/notes/26-instructgpt-pipeline.md);
Constitutional AI (Bai et al. 2022) — carried as
[research/notes/30-constitutional-ai.md](../../research/notes/30-constitutional-ai.md);
DeepSeekMath (Shao et al. 2024); DeepSeek-R1 (2025) — the RL-over-verifiable-rewards
manifesto; Guan et al., "Deliberative Alignment" (2024). Optional list
includes Christiano et al. 2017, Ziegler et al. 2019, DPO (Rafailov et al.
2023 — the repo carries
[research/notes/25-dpo-reparameterization.md](../../research/notes/25-dpo-reparameterization.md)),
RLAIF, GSPO, and Raschka's practitioner write-ups. The full list with
links lives on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. The modern training stack as safety's actual substrate

The lecture's spine is the pipeline that produces a deployed model:
pretraining (trillions of tokens, next-token prediction) → mid-training
(context extension, reasoning-phase data) → post-training (supervised
fine-tuning, then preference optimization, then — for reasoning models —
reinforcement learning against verifiable rewards) → safety training
(refusal behavior, deliberative alignment layers). The safety-relevant
claim is structural: safety is not a stage, it is a *property under
dispute* at every stage. Pretraining data carries the distribution's
values; SFT carries demonstration norms; RLHF carries preference
imperfections (sycophancy is the canonical artifact); RLVR carries
whatever the verifier rewards, including its exploits.

### 2. RLHF and its known failure surface

InstructGPT defined the recipe; the field has spent the years since
cataloguing its failure surface — preference data encodes what raters
reward, not what they value, and models learn the difference. The repo
carries this as [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md)'s
core tension and as the sycophancy paper note. Constitutional AI is the
branch that replaces human raters with a written constitution and
model-generated critique — moving the value source from crowdsourced
preference to an inspectable document, at the cost of inheriting the
constitutional drafter's frame.

### 3. DeepSeek-R1 and RLVR: when the verifier becomes the teacher

The R1 line of work is on the list because it changed what "training"
means: reinforcement learning where the reward is *verification* (code
that passes tests, math that checks) rather than human preference. For
safety this is a double-edged structure — verifiable domains get
cleanly-scaling capability, while the verifier's exploits (passing tests
without solving problems) become the new reward-hacking surface. The
course returns to exactly this in its grading-and-reward-hacking lecture
(Fall 2026's John Schulman session); this repository's
[Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md)
is the full treatment.

### 4. The experiment: optimizing prompts with policy gradients

The Fall 2025 experiment uses a policy-gradient algorithm to optimize
prompt prefixes — RL where the "policy" is which persona prefix to
activate, showing post-training machinery turned on the prompt layer.
It teaches the mechanical skill (policy gradients over discrete tokens)
on a task small enough to finish, which is exactly the repo's own
from-scratch project philosophy.

## Through-line to this repository's chapters

- [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) —
  the chapter is this lecture's depth layer: RLHF, DPO, RLAIF,
  constitutional methods, and their failure surfaces.
- [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) —
  where the verifier-exploitation story lands as a full chapter.
- [research/notes/26-instructgpt-pipeline.md](../../research/notes/26-instructgpt-pipeline.md)
  and [research/notes/30-constitutional-ai.md](../../research/notes/30-constitutional-ai.md) —
  the repo's own paper notes on two of the pre-readings.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
