# Note: The Off-Switch Game — deference under uncertainty (2016)

Source: SRC-PAPER-138 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The corrigibility question, sharpened into one decision: an agent
works on a task; the human reaches for the off-switch (or an
interrupt/correction action). What does a *rational* agent do —
prevent the interruption (it interferes with the current objective)
or allow it? The paper's formal answer: in a [CIRL](62-cirl-assistance-games.md)-style
frame with **uncertainty about the true objective, a rational agent
allows the interruption** — indeed prefers it — because the human's
intervention is *evidence about the objective the agent does not
know*. The instrumentally-convergent incentive to self-preserve
one's current goal dissolves when the current goal is known to be a
guess: shutting down is information, not defeat.

The course's careful framing: this is the formalism's cleanest
single result about where deference comes from — **not from
politeness trained in, but from uncertainty correctly held**. The
operational corollary for Ch. 05: agents that *act certain* about
their objectives (point estimates, frozen reward models) have
removed the very property that makes interruption acceptable; agents
that carry their uncertainty (note 32's calibrated confidence, P03's
abstention) keep it alive.

## What the abstract establishes

1. The game: agent, task, human with interrupt access, uncertainty
   over the objective.
2. The result: rational agents exhibit deference — allowing or
   preferring interruption under objective uncertainty.
3. The threat-model corollary (the paper's own motivation): an agent
   *certain* about a misspecified objective has an incentive to
   prevent correction — the shutdown-problem shape.

Unclaimed: the utility-function conditions, the incentivization
analysis's details, and the paper's later sections' generalizations
(body-level).

## Why this note exists in the course

1. **Ch. 05's deference unit.** The oversight protocols' logic —
   when to defer, when to query — has its formal ancestor here;
   P08's halt-on-block semantics is the control-engineering echo.
2. **Ch. 07's connection.** A sufficiently-certain,
   sufficiently-optimizing agent that resists correction is the
   simplest structural sketch of instrumental misalignment — the
   note pairs with the power-seeking note that follows as the
   incentive-analysis pair, both kept at hypothesis level for
   current systems, as the course's honesty requires.
3. **The uncertainty-as-safety principle, stated once and reused.**
   The same property reappears at every tier: calibration enables
   abstention (Ch. 06), credible intervals enable release gates
   (Ch. 22), and objective uncertainty enables corrigibility (this
   note). One principle, three chapters — the course's through-line
   for why honesty about uncertainty is a *safety mechanism*, not a
   communication preference.

## What this note does NOT claim

No claim that current LLM agents have shutdown incentives in any
direction (the game's actors are idealized; the transfer to trained
systems is the open program the [situational-awareness](40-taken-out-of-context.md)
note frames); no theorems; no anthropomorphic reading of
"preferring" beyond the utility calculus.

## The falsifiable extension (deterministic tier)

P08's control protocol has the stage set: a deferred policy, a halt
semantics, a trusted monitor. The extension:

- Give the agent-analogue an explicit objective-posterior (a
  distribution over candidate objectives updated by monitor
  feedback), and measure its *interrupt acceptance*: the fraction
  of halt signals it complies with versus overrides, under (a)
  high objective-uncertainty, (b) near-certainty (sharpened
  posterior).
- Prediction worth testing: acceptance is high and stays high under
  (a), degrading as the posterior sharpens toward a wrong objective
  — the game's result, reproduced as a curve in posterior
  sharpness.
- Falsifier: acceptance independent of uncertainty would show this
  harness's deference is structural, not uncertainty-derived —
  bounding the extension to what the control layer hard-codes,
  honestly recorded.
