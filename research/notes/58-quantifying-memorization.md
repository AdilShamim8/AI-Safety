# Note: Quantifying Memorization — the three log-linear laws (2022)

Source: SRC-PAPER-133 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Memorization was measured (note 56) and attacked (note 57); this
paper supplies the *engineering curves*. The framing: memorization
is undesirable for three distinct reasons — **privacy** (exposing
user data), **utility** (repeated easy-to-memorize text is often
low quality), and **fairness** (some texts are memorized over
others). The result: **three log-linear relationships** quantifying
how much LMs emit memorized training data. From the abstract's own
enumeration, memorization significantly grows as: (1) **model
capacity** increases, (2) **duplications of an example** increase
— the third axis (the API record truncates; the paper's wider
record at abstract level carries it as prompt length, i.e. longer
contexts memorize more, and the register records the truncation
honestly).

The trilogy closes with the shape the field needed: not "is there
memorization?" but "**how much, as a function of the knobs you
actually turn**" — capacity, duplication, and context — each a
governance lever with a law attached.

## What the abstract establishes

1. The three-fold undesirability (privacy, utility, fairness) — a
   framing the course adopts wholesale for Ch. 16.
2. Three log-linear relationships: memorization grows with capacity;
   with duplication count; [and with the third axis, truncated in
   the record — the note flags rather than invents it].
3. That appropriately-prompted LMs emit memorized data verbatim.

Unclaimed: the fitted slopes, the model families swept, the
deduplication-threshold findings, and the exact third-axis
statement (body-level; the truncation is recorded).

## Why this note exists in the course

1. **Ch. 16's governance curves.** Data governance decisions —
   dedup policies, capacity choices, retention rules — now have
   quantified consequences: the duplication law is the scientific
   basis of every dedup pipeline, and the capacity law is why
   "bigger model" is a privacy decision, not just a capability
   one (the [double descent](53-deep-double-descent.md) note's
   performance-side non-monotonicity, mirrored on the privacy side).
2. **The fairness axis, taken seriously.** "Some texts are
   memorized over others" is the privacy-fairness intersection:
   whose data gets remembered is not uniform, and Ch. 21's
   distributional lens picks this up — memorization risk is
   *jointly* distributed with data-source demographics.
3. **The utility framing's discipline.** Memorization is not only
   a privacy story — duplicated low-quality text degrades the
   model — which means dedup serves two masters with one pipeline:
   the rare case where the privacy fix and the quality fix are
   the same fix.
4. **Differential privacy's pricing.** The laws give DP's
   privacy-utility trade a concrete shape to price against
   (capacity × duplication × emission), which is how Ch. 16
   teaches DP-as-budget rather than DP-as-buzzword.

## What this note does NOT claim

No slopes or thresholds (body-level); no claim that the laws hold
for current frontier recipes unchanged (training data scale and
dedup norms moved — the honest drift caveat); no claim the third
axis is prompt length (the truncation is recorded as a truncation,
not filled from memory — the discipline this register exists to
enforce).

## The falsifiable extension (deterministic tier)

P02's canary apparatus (notes 56-57 extensions) extends to the
laws directly:

- Sweep learner capacity at fixed canary set; sweep duplication
  count at fixed capacity; sweep context length at both fixed.
  Measure emission lift per canary per condition; fit log-linear
  models per axis.
- Prediction worth testing: positive log-linear coefficients on
  at least two of three axes in this synthetic world — capacity
  and duplication being the two the API-complete abstract states.
- Falsifier: a flat or non-log-linear axis bounds the transfer of
  that law to this organism — and the two-instrument stack
  (exposure + extraction) already built reports the boundary
  result per the standing instruments.
