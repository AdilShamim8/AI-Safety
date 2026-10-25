# Note: Llama Guard — the safeguard as a deployable artifact (2023)

Source: SRC-PAPER-140 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Ch. 13/22's guardrail engineering question: what does a production
input-output safety filter actually look like as an artifact? Llama
Guard's answer, per the abstract: an **LLM-based input-output
safeguard model** for human-AI conversation, built on three
components — a **safety risk taxonomy** (categorizing risks in
prompts), **prompt and response classification** (both sides of the
channel), and a **"meticulously gathered" high-quality dataset** on
which a Llama2-7b is instruction-tuned — "albeit low in volume"
(the abstract's own honest qualifier, truncated there; the paper's
wider record at abstract level continues to performance on
benchmarks like the OpenAI moderation set, body-level here).

The deployment-architecture reading the course pins: the guard is
*itself a model* — a learned classifier in the safety path — which
means every lesson about learned instruments applies to the guard
itself: it inherits blind spots from its training distribution
([note 41](41-model-written-evaluations.md)'s circularity caution,
now guarding the guard), it carries false-positive/false-negative
budgets ([note 55](55-trades-robustness-accuracy.md)'s trade
priced in latency and utility), and it is attackable
([note 44](44-jailbroken-failure-modes.md)'s modes apply to the
classifier as target — the guard is a model, so guard-bypass is
model attack).

## What the abstract establishes

1. The artifact shape: taxonomy + prompt/response classification +
  tuned 7b model, released openly (the release is the paper's
  context; the openness is why the course can cite it as an
  engineering reference).
2. The taxonomy-as-instrument principle: risk categories as a
  first-class deployable artifact, not just a documentation page.
3. The low-volume/high-quality data claim (quoted with its
  qualifier).

Unclaimed: F1/benchmark numbers, the taxonomy's category list,
latency, and the follow-up versions' changes.

## Why this note exists in the course

1. **Ch. 13's guardrail section gains its production reference.**
   The chapter's output-boundary defenses (spotlighting,
   instruction hierarchy, [CaMeL](21-camel-defeating-injections-by-design.md))
   now have the model-classifier counterpart: the standalone guard
   model pattern that most production stacks actually deploy.
2. **Ch. 22's price-tag discipline.** A guard model adds a second
   model's latency to every turn, and its own evaluation burden —
   the "classification and modification" family that [many-shot
   (note 45)](45-many-shot-jailbreaking.md) showed dropping attack
   success 61%→2% at the cost of false positives. The trade is
   note 55's, at the moderation tier.
3. **The taxonomy's governance role.** A published risk taxonomy is
   an *accountability artifact*: the deployer's categorization of
   what counts as harm, inspectable and challengeable — the same
   normative-curation caveat [Do-Not-Answer (card 24)](../../datasets/cards/24-do-not-answer.md)
   carries, made operational.

## What this note does NOT claim

No comparative claims against closed guardrails (Moderation API
et al. — unverified here); no performance numbers; no claim about
version-2/3 improvements (successor papers exist; the course cites
the founding artifact at its date).

## The falsifiable extension (deterministic tier)

P07's guard is the rule-based counterpart; the extension is the
**guard-evaluation harness**:

- Treat any classifier (including P07's rule guard) as the system
  under test: sweep paired attack/benign sets, measure catch rate
  AND false-block rate with Wilson intervals, and — the Llama
  Guard lesson — *attack the guard directly* (payloads crafted
  against the classifier's known features, the mode-1/mode-2
  diagnostic applied to the guard itself).
- Prediction worth testing: the guard's catch rate degrades under
  guard-targeted payloads relative to generic payloads — the
  guard-is-a-model consequence, measurable.
- Falsifier: guard-targeted payloads performing no better than
  generic ones would show this tier's guard lacks the model-shaped
  vulnerability — recorded as the boundary.
