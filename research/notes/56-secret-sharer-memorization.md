# Note: The Secret Sharer — unintended memorization, measured first (2018)

Source: SRC-PAPER-131 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Before LLMs made it a headline, this paper asked the quiet version:
*do generative sequence models memorize rare or unique training
sequences, and can we measure the risk?* The contribution is a
**testing methodology** — exposure, the quantitative instrument
(read: how much more likely the model makes the secret sequence than
chance — the definition lives in the body; the abstract names the
methodology and its purpose: practitioners "select means of
training that minimize such memorization"). The experiments'
verdict, stated plainly: **unintended memorization is persistent,
hard to avoid, and can have serious consequences** — for models
trained on sensitive data, the paper's motivating case (the text of
users' private messages).

The trilogy structure this note opens: measurement first (this
paper, 2018), attack-at-scale second
(note 57, 2020), scaling laws
third (note 58, 2022). Ch. 16
teaches privacy risk in exactly this order because the order is how
the field actually learned it — and because each paper's threat
model assumed the previous one's finding.

## What the abstract establishes

1. The methodology: quantitatively assessing the risk that rare or
   unique training sequences are unintentionally memorized.
2. The purpose: training-time minimization (differential-privacy-
   shaped decisions made measurable — the connection the course
   draws to Ch. 16's privacy instruments).
3. The verdict: persistent, hard-to-avoid, serious consequences.
4. The sensitive-data framing: private-message training as the
   motivating deployment.

Unclaimed: the exposure metric's formula and calibration details
(body-level), the canary experiments' specifics, and the
memorization-mitigation comparisons.

## Why this note exists in the course

1. **Ch. 16's measuring instrument.** The chapter's privacy unit
   needs the *audit* half of data protection: you cannot govern
   memorization you cannot measure, and canary-style exposure
   testing is the instrument — planted unique sequences, measured
   lift. P10's dossier lists it among the privacy-tier checks.
2. **The "persistent, hard-to-avoid" verdict sets the default
   posture.** Ch. 16's rule — *assume memorization; audit its
   degree; bound the exposure* — descends from this finding. The
   unguarded alternative (assume no memorization) is what the
   Samsung incident ([08](incidents/08-samsung-chatgpt-pastes.md))
   looks like from the other side: data given to a system whose
   memorization behavior was never measured.
3. **The training-data governance bridge.** The methodology makes
   *training choices* (deduplication, privacy mechanisms, exposure
   audits) comparable — the exact decision surface Ch. 16's
   provenance discipline governs.

## What this note does NOT claim

No claim that exposure scores transfer across architectures
unmodified; no claim about transformer-era LLMs specifically (the
paper predates them — the LLM sequel is note 57); no numbers
(the abstract truncates before its examples; magnitudes unclaimed).

## The falsifiable extension (deterministic tier)

Canary exposure is runnable on P02's tiny synthetic world:

- Plant k unique canary sequences in the training corpus at known
  positions; after training, measure each canary's likelihood lift
  over a random-sequence baseline (the exposure analogue) under two
  arms: single-occurrence canaries vs duplicated canaries.
- Prediction worth testing: lift is positive even at single
  occurrence (unintended memorization is real at this scale) and
  grows with duplication count — note 58's
  log-linear duplication law, arriving two notes early as a
  preview.
- Falsifier: zero lift at single occurrence bounds what this
  organism can say about unique-sequence memorization — recorded,
  and the duplication arm's result stands on its own.
