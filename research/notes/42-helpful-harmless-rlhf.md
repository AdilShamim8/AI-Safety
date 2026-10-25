# Note: Training a Helpful and Harmless Assistant — the RLHF baseline document (2022)

Source: SRC-PAPER-117 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Ch. 04 teaches preference learning and post-training as engineering; this
paper is the field's baseline engineering report — the document that
showed RLHF could produce a *helpful and harmless* assistant at scale
and what the knobs actually did. Four abstract-level findings the course
pins:

1. **Alignment training improved performance on almost all NLP
   evaluations** — the "alignment tax is negative" observation that
   shaped three years of deployment arguments. Preference training was
   not a capability sacrifice in this setting; it was measured as a
   gain.
2. **Compatibility with specialized skills**: RLHF "fully compatible
   with training for specialized skills such as python coding and
   summarization" — helpfulness and capability co-train.
3. **Iterated online training**: preference models and policies updated
   on a weekly cadence with fresh human feedback — the online loop that
   note 37's overoptimization curve warns about, here operated at a
   refresh rhythm.
4. **The KL–reward relation**: "a roughly linear relation between the
   RL reward and the square root of the KL divergence between the
   policy and its initialization" — the paper's most durable single
   formula. It prices *how far the policy has moved* in units of
   reward, which is why every later KL-budgeted alignment method (and
   P02's optimizer's KL ledger) cites it.

## Why the KL relation matters more than the rest

The √KL linearity gives post-training its most usable safety knob: the
KL divergence from initialization is a *measurable, pre-registrable
budget* for how much the policy may drift under reward optimization.
Ch. 04's post-training risk list and P02's optimizer design both run on
this: cap the drift, monitor the reward, and you have a two-axis
governance plot for any policy-training run — including runs whose
reward is itself learned (which is where note 37's curve re-enters: the
KL budget bounds the overoptimization axis). The relation is empirical
(this setting), not a theorem; the course teaches it as the observed
exchange rate, with the honest caveat that its linearity is a finding,
not a law.

## What the abstract establishes (and prices)

Established: all four findings above, in the abstract's own words. The
helpful/harmless *tradeoff structure* (when they conflict, how the
preference data encodes the priority), the data-collection pipeline
detail, the red-team co-training specifics, and the harmlessness-scale
methodology all live in the body — unread here, unclaimed. The note
carries the four load-bearing results and their engineering meaning;
numbers beyond the abstract's own statements are absent by design.

## Why this note exists in the course

Chapter 04's spine is: preference data → reward model → policy
optimization → the bills that come due. This paper is the primary
source for the whole first arc — the note that InstructGPT (note 26)
and DPO (note 25) both position against: InstructGPT as the pipeline's
founding demonstration, this paper as the scaled engineering
consolidation (the weekly-cadence online mode matters for Ch. 04's
"preference data is a living asset" teaching), DPO as the objective
simplification that skips the RM. Constitutional AI (note 30) then
replaces the human-feedback source. The four notes together are the
post-training decision tree the chapter's comparison section needs, and
this one is the root.

The harmlessness half also anchors Ch. 04's honesty about what
"harmless" means operationally: a property *of the preference data and
training process*, not a verified deployment property — the gap that
Ch. 22's release gates exist to police, and the reason this note pairs
with the overoptimization note rather than standing alone.

## What this note does NOT claim

No claim that RLHF is capability-positive universally (the paper's own
"almost all NLP evaluations" is setting-scoped); no claim about the
KL relation's exact coefficient or its transfer across objective
families (body-level); no claim that iterated online training is safe
at arbitrary cadence — that is note 37's caution, kept separate on
purpose.

## The falsifiable extension (deterministic tier)

P02's optimizer already ships a KL ledger; the extension tests the
√KL-linear-reward relation directly in the synthetic setting:

- Sweep the KL budget across at least five settings; for each, record
  terminal reward (proxy and gold) and cumulative √KL. Fit the
  reward-vs-√√... the prediction to test: reward is approximately
  linear in √KL *in the regime before the overoptimization peak*, with
  the relation flattening after it (peak = the exchange rate's
  breakdown point — the two papers' curves meeting).
- Falsifier: no linear segment at all (reward saturating immediately
  or super-linear throughout) would contradict the imported relation
  in this world — a recorded boundary on which knobs survive
  synthesis, which is exactly what the deterministic tier is for.
