# Note: Cooperative Inverse Reinforcement Learning — assistance games' founding formalism (2016)

Source: SRC-PAPER-137 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The standard RL frame treats the human as environment: a reward
signal to be optimized. CIRL replaces the frame — **a two-player
game of assistance**: the human knows the reward function (or parts
of it); the robot does not; both are players in a shared Markov game
where the robot's job is to *learn* the reward by observing the
human, and the human's job (implicitly) is to behave so the robot
can learn. The profound consequence the course pins: **in a CIRL
frame, uncertainty about the objective is built into the agent's
situation** — the optimal policy under reward uncertainty is not
"guess the reward and optimize hard" but "act so that you keep
learning what the human wants, and defer where the uncertainty is
load-bearing."

That single property is why Ch. 05 (scalable oversight) and Ch. 03
(specification) both route through this formalism: it is the
mathematical home of the idea that *the objective is the unknown*,
which is the exact inversion of the standard frame that produced
[the overoptimization problem](37-reward-overoptimization.md).

## What the abstract establishes

1. The CIRL formalism: the two-player cooperative game with
   asymmetric reward knowledge, generalizing IRL into the game
   setting.
2. The framework-level results the paper develops (equilibrium
   behavior, the learning-of-reward structure) — announced at
   framework level; specific theorems are body-level, unclaimed
   here.

## Why this note exists in the course

1. **Ch. 05's theoretical spine.** The chapter's oversight protocols
   (feedback solicitation, delegation, deference) are operational
   answers to the CIRL situation; [note 10](10-weak-to-strong.md)'s
   oversight-generality question is asked *inside* this frame.
   Off-switch-style deference (note 63, the sequel) is CIRL's
   most-cited corollary.
2. **Ch. 03's specification connection.** A misspecified reward is
   a certainty-assumption failure; CIRL makes the uncertainty
   first-class, which is the formal version of "preregister what
   you do not know" ([Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md)'s
   discipline, formalized).
3. **The corrigibility lineage.** The course's honesty about this
   literature: CIRL is a *theoretical framework* whose practical
   transfer to LLM training is an open research program, not a
   deployed mechanism — the notes pair it with the empirical
   overoptimization curve (note 37) as the theory-practice gap
   made visible, which is itself a Ch. 24 lesson in theorist
   humility.

## What this note does NOT claim

No claim that current LLM training instantiates CIRL (RLHF is not
CIRL — the reward model replaces the human-player structure with a
learned proxy, precisely the substitution note 37's curve
measures); no theorems; no claim about convergence or
learnability results (body-level).

## The falsifiable extension (deterministic tier)

P05's oversight analogue can implement the frame's minimal
comparison:

- Arm A (certainty frame): grader trains once on the feedback
  signal and applies it without further inquiry. Arm B (assistance
  frame): grader *allocates budget between acting and querying*,
  with query cost and reward-uncertainty both modeled.
- Prediction worth testing: under a reward distribution with high
  early uncertainty, arm B's total return exceeds arm A's — the
  value of inquiry, reproduced as a curve in query cost.
- Falsifier: arm A dominating at all query costs would show this
  synthetic world has no value-of-inquiry regime — bounding the
  frame's demo value honestly.
