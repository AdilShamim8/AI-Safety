# Note: Measuring Faithfulness in Chain-of-Thought — from suspicion to instrument (2023)

Source: SRC-PAPER-118 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Note 38 established that CoT explanations can rationalize — the
*existence* of unfaithfulness. This paper is the methodological sequel:
turn "is this CoT faithful?" into a **measurement design**. The move is
interventionist, and it is the same epistemic upgrade as Ch. 09→Ch. 11's
probing-to-patching ladder, applied to the CoT channel: do not ask
whether the explanation *sounds* right (that is correlational reading);
**intervene on the CoT** — add mistakes, paraphrase it — and measure how
strongly the model's *answer* conditions on the intervention. A model
whose answer tracks its own stated reasoning is using the CoT; a model
whose answer ignores corrupted or reworded CoT is generating text that
merely accompanies its computation.

The abstract's headline finding: **large variation across tasks** —
models "sometimes relying heavily on the CoT and other times primarily
ignoring it." Faithfulness is not a model property; it is a
task-conditional property. For monitoring (Ch. 18) that is the worse
news: you cannot certify "CoT is faithful for this deployment" from a
model-level eval; you need the task family's own conditioning profile.

The abstract also kills two comfortable hypotheses in passing: the CoT
performance boost does not come from *added test-time compute alone*
(nor from phrasing-encoded information) — the reasoning text is doing
something the compute story cannot explain, which sharpens why the
channel matters enough to audit.

## What the abstract establishes

1. The interventionist measurement design (mistakes, paraphrase) as the
   faithfulness instrument.
2. Task-conditional conditioning: large cross-task variation in how
   strongly answers depend on their CoT.
3. The negative results on compute-alone and phrasing-alone
   explanations of CoT's benefit.
4. The abstract's final clause — "as models become larger and m[ore
   capable]..." — truncates in the API record; the body's
   scale-faithfulness finding is recorded as existing but unclaimed
   here (the honest truncation discipline, same as note 41's).

## Why this note exists in the course

Chapter 18 pairs this note with note 38 as the field's two-step:
**document the failure, then build the detector.** The course's own
monitoring methods descend from the second step:

1. **Truncation/paraphrase audits become monitor-validation items.**
   Ch. 22's release-gate template now has a concrete, cheap test to
   list: does the deployed task family show answer-conditioning on CoT
   interventions? A gate that cannot answer this has not validated its
   CoT-reading monitor — the exact gap the safety-case template's
   "monitor validated against failure mode" field exists to expose.
2. **P01's harness gains the design pattern.** The extension below
   implements mistake-injection and paraphrase arms at deterministic
   tier.
3. **The task-conditionality result disciplines evals.** A faithfulness
   number measured on one task family is not evidence about another —
   the same subgroup logic Ch. 17 applies to distribution shift,
   applied to the explanation channel.

## What this note does NOT claim

No per-task conditioning numbers (body-level); no claim that
intervention-passing CoT is *fully* faithful — the design measures
answer-conditioning, a necessary-not-sufficient property the body
itself is careful about, and the note inherits that care; no claim
about scale trends (the truncated clause is left as the body's).

## The falsifiable extension (deterministic tier)

P01's runner can implement both intervention arms on its synthetic
case sets:

- **Mistake arm**: corrupt a stated premise in the CoT (swap a value)
  and measure answer flip-rate versus uncorrupted controls. Prediction
  worth testing: flip-rate varies by case family (the task-conditioned
  conditioning effect) even at fixed difficulty.
- **Paraphrase arm**: meaning-preserving rewording of the CoT with
  answers held to a stable band — meaning-invariance is the cheap
  necessary condition for the channel carrying content rather than
  token-level cues.
- Falsifier: uniform flip-rate across families (no
  task-conditionality) would contradict the imported finding in this
  synthetic world — recorded either way in P01's paired-ledger format,
  which is the report shape Ch. 18's exercises drill.
