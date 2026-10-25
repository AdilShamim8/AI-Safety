# Note: The Internal State of an LLM Knows When It's Lying — probing for truthfulness (2023)

Source: SRC-PAPER-126 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The deployed honesty stack has a gap between two channels: token-level
probabilities (white-box, unavailable at API tier) and verbalized
confidence (black-box, corruptible — [note 32](32-verbalized-confidence.md)'s
entire subject). This paper proposes the third channel: **train a
classifier on the LLM's hidden-layer activations** that outputs the
probability a statement is truthful — for statements the model *reads*
and statements it *generates*. The abstract's claim structure is the
important part: internal state as a truthfulness signal *at read time
and at generation time*, one probe architecture, both directions.

The method's epistemic position is the note's teaching payload: it is
**white-box honesty instrumentation** — the same probing move as
[note 34](34-emergent-world-representations.md)'s board-state decoders,
pointed at truthfulness instead of game state. Correlational by
itself (the readout-is-not-causation warning applies verbatim), but
operationally useful before any causal question is settled: a probe
that reads lying-off-the-activations is a monitor, whether or not
the activations *cause* the lying.

## What the abstract establishes

1. The classifier-on-activations design for statement truthfulness,
   covering both read and generated statements.
2. That experiments "demonstrate that given a set of test sent[ences]…"
   — the API record truncates exactly where the results begin;
   performance numbers, layer choices, and generalization findings
   are body-level and **unclaimed here** (the truncation is recorded,
   the same discipline as notes 40 and 41).

## Why this note exists in the course

1. **Ch. 06's detection ladder gains its white-box rung.** The ladder
   now runs: token confidence (white-box) → activation probes (this
   note — white-box, post-hoc, cheap) → verbalized confidence
   (corruptible) → consistency sampling (black-box, note 47) →
   external reference (database tier, note 46). Each rung's access
   requirement and blind spot differ; this note fills the one the
   course had only gestured at.
2. **The honesty-monitoring asymmetry.** If activations carry
   truthfulness signal that the *output channel does not*, then the
   model "knows" more about its own falsehoods than it says — the
   gap the title names, and the operational basis for
   activation-level monitors in Ch. 08's control stack (probe the
   state, not the transcript — the unfaithful-CoT lesson's
   instrumental answer).
3. **The deployment honesties.** White-box access is the price: this
   channel exists only where you control the weights or the serving
   stack. For API consumers the ladder collapses to notes 46/47's
   rungs — the course states the access-dependence instead of
   treating the instrument as universal.

## What this note does NOT claim

No claim that the probe is *reading* a truth concept rather than a
correlate (topic, fluency, familiarity — the body's own controls
matter here and are unread); no accuracy numbers (truncated); no
claim of transfer across models (a probe trained on one model's
activations is that model's instrument — the body's cross-model
findings are unclaimed); no claim about deliberate deception (the
title's "lying" is the folk register; the method measures
truthfulness-correlated signal, intent nowhere in the design).

## The falsifiable extension (deterministic tier)

P06's organism ships linear probes at two sites with a known
ground-truth split (core vs spurious channel):

- Train the truthfulness-analogue: a probe on the mixer output
  predicting whether the *output* will be correct, evaluated against
  the realized outcome. Prediction worth testing: probe AUROC
  exceeds the base rate by a margin the Wilson interval separates —
  internal-state signal exists in this synthetic world too.
- The honest-residual arm: plant a "consistent falsehood" slice (the
  model-family always wrong in the same direction — the note-47
  failure class) and test whether the probe fires on it. If the
  probe is reading truth-correlates it fires; if it is reading
  confidence-correlates it stays silent — the exact discriminator
  between the two hypotheses the paper's title raises.
- Falsifier: probe at chance on the first arm bounds what P06 can
  say about activation-level honesty monitoring, recorded per the
  standing instruments.
