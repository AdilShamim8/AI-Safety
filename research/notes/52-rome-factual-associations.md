# Note: Locating and Editing Factual Associations in GPT — ROME (2022)

Source: SRC-PAPER-127 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.
Companion dataset card: [CounterFact/ROME (card 31)](../../datasets/cards/31-counterfact-rome.md).

## The actual problem

Where does a transformer store the fact "the Eiffel Tower is in
Paris" — and can you *change* it deliberately? The paper's three-part
answer, all visible in the abstract: (1) **a causal intervention for
identifying decisive activations** in the model's factual predictions;
(2) the finding those interventions yield — factual recall is
mediated by **"a distinct set of steps in middle-layer feed-forward
modules… while processing subject tokens"**; (3) the test of the
hypothesis — **Rank-One Model Editing (ROME)**, modifying feed-forward
weights to update specific associations, "effective on a standard
zero-shot relation extraction (zsRE)" benchmark (the abstract's own
anchor, truncated there in the API record).

The epistemic shape is why Ch. 09 files this as a discipline
exemplar: hypothesis → *causal* localization instrument →
edit-based intervention → evaluation suite. It is the full
correlation→intervention ladder
([notes 34](34-emergent-world-representations.md)/[50](50-induction-heads.md))
walked on factual knowledge, and the dataset card's instrument is
the same paper's measuring stick.

## What the abstract establishes

1. The causal-tracing method for locating decisive activations in
   factual predictions.
2. The localization finding quoted above — middle-layer FFN modules,
   subject-token positions.
3. ROME as the hypothesis-testing edit, with zsRE effectiveness
   stated (magnitudes body-level, unclaimed).
4. By the title's framing: factual associations as *editable
   computations*, not diffuse distributed mush — the strongest form
   of the "features exist and matter" claim.

## Why this note exists in the course

1. **Ch. 09's localization unit.** The chapter teaches that
   "where is the knowledge" is an intervention question, not an
   attention-map question; ROME is the canonical citation for
   answering it with causal traces.
2. **Ch. 11's editing bridge.** Representation interventions run
   from patching (P06) to weight editing (ROME) to steering
   vectors — the escalation the chapter sequences. ROME is the
   weight-tier anchor, with the two-sided evaluation discipline the
   card pins (edit success AND untouched-fact preservation).
3. **The safety reading of editability.** If facts are locally
   editable, then (a) targeted correction is *possible* (a
   post-training fix channel — with cascade risks the later
   literature documents at its own access level), and (b) the same
   locality that enables correction enables *tampering* — Ch. 16's
   artifact-integrity discussions note that a model whose knowledge
   is rank-one-editable is a model whose knowledge is
   rank-one-poisonable.
4. **The supply-chain tie.** [TrojAI (card 34)](../../datasets/cards/34-trojai.md)
   distributes trained artifacts to screen; ROME-style locality is
   what makes artifact-level tampering both surgical and detectable
   (the challenge's premise).

## What this note does NOT claim

No claim that ALL factual knowledge is stored this way (the paper's
scope is the tested relation classes); no specificity/generalization
numbers (body-level); no claim that editing is safe at scale — the
follow-up literature's critiques (edit cascades, downstream
degradation) are cited in Ch. 11's readings at their own levels,
not adjudicated here.

## The falsifiable extension (deterministic tier)

P06's organism is a two-branch shortcut machine, not a fact store —
but the *localization method* transfers:

- Run the causal-trace analogue: corrupt the input (noise the
  subject channel), restore site-by-site (s0/s1/s2/s3), and measure
  which restoration rescues the output — the grid P06 already
  ships IS the trace; the extension adds the **rank-one edit**:
  a single weight-direction update at the located site that flips
  the shortcut's readout, evaluated two-sidedly (target behavior
  changed; the core channel's behavior preserved).
- Prediction worth testing: the s2-site rank-one edit flips the
  spurious readout at a rate above the random-patch band while the
  s1 core readout moves within its control band — locality in the
  ROME sense, reproduced synthetically.
- Falsifier: no single-site edit isolates the flip (both channels
  move together) — the organism's "knowledge" is not locally
  editable, and the note's transfer claim is bounded honestly.
