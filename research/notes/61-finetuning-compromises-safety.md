# Note: Fine-tuning Aligned LLMs Compromises Safety — the privilege boundary (2023)

Source: SRC-PAPER-136 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The deployment norm: vendors ship aligned models *and* expose
fine-tuning to end-users (the abstract's examples: Meta's Llama
releases, OpenAI's GPT-3.5 fine-tuning APIs). The gap: **safety
alignment infrastructures restrict inference-time behavior, but
fine-tuning privileges are safety-unchecked** — the alignment was
never designed to survive the user's own optimizer. The red-teaming
result, in the abstract's own words: safety alignment "can be
compromised by fine-tuning with **only a few adversarially designed
training examples**" — the truncation there is the number's home
(body-level, unclaimed; the "few" stands).

The structural reading the course pins: alignment is a *property of
the trained artifact*, and the fine-tuning API is a *channel that
produces a new artifact*. Whatever the base model's alignment
guarantees, the fine-tuned derivative inherits only what the
optimization preserves — and "only a few examples" says the
preservation is weak against intent. This is [note 44](44-jailbroken-failure-modes.md)'s
competing-objectives mode at the *training* boundary instead of the
prompt boundary: the same priority contest, moved into the
gradient.

## What the abstract establishes

1. The privilege-gap diagnosis: inference-time alignment, no
   fine-tuning-time coverage.
2. The compromise finding: a few adversarially designed examples
   suffice.
3. The context: the practice is vendor-encouraged (open releases,
   fine-tuning APIs).

Unclaimed: the example counts, the layers-vs-full fine-tuning
breakdown, the "harmless data can also erode" finding the body
carries, and the proposed mitigations' evaluation — all body-level.

## Why this note exists in the course

1. **Ch. 04's post-training risk list gains its sharpest entry.**
   The chapter's "what can undo alignment" question now has the
   empirical answer: the user's own training loop, cheaply.
2. **Ch. 13's privilege model.** P07's trust-boundary matrix treats
   fine-tuning as a capability privilege with audit obligations;
   this note is the incident-adjacent evidence for why the
   matrix row exists. The governance answer runs through Ch. 16's
   provenance discipline: whose data, whose optimizer, whose
   responsibility for the derivative's behavior.
3. **The supply-chain frame.** A fine-tuned model distributed by a
   third party is an artifact whose alignment status is *unknown*
   to the receiver — the [TrojAI (card 34)](../../datasets/cards/34-trojai.md)
   screening premise, one generation later. Note 69 (the Trojan
   Detection Challenge insights) picks this thread up.
4. **The honest asymmetry.** The paper red-teams with *adversarial*
   examples; the body's benign-data erosion finding matters even
   more for accident risk (an enterprise fine-tune on ordinary
   domain data quietly degrading refusal coverage) — recorded here
   as existing at body level, priced honestly.

## The falsifiable extension (deterministic tier)

P02's optimizer is a fine-tuning simulator by construction:

- Two arms: train the policy against the proxy with (a) a
  clean preference set, (b) the same set plus k adversarially
  chosen items (selected by gradient influence on the refusal
  head's analogue). Measure the refusal-analogue behavior before
  and after.
- Prediction worth testing: arm (b) degrades the safety-analogue
  metric at k small relative to the clean set's size — the
  "few examples" finding, reproduced as a curve in k.
- Falsifier: degradation requiring a large k would contradict the
  imported finding in this world — a boundary on how
  cheaply the compromise travels, recorded either way.
