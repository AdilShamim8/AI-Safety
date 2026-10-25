# Dataset card: Civil Comments (toxicity benchmark)

LICENSE not observed this session — the underlying dataset's terms
were not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a **highly skewed multi-label hate-speech
  dataset** from the Civil Comments platform, studied in the
  anchor paper's wide model comparison with **inference time and
  bias metrics** alongside performance. The paper's own findings
  include: all BERT variants show **similar performance regardless
  of size, optimizations, or pre-training language**, while RNNs
  are much faster at inference (the abstract's comparison, quoted
  at its level).
- **Canonical home:** "A benchmark for toxic comment classification
  on Civil Comments" (Nyzhnyi et al., arXiv:2301.11125,
  2023-01-26, API-verified 2026-10-25); the underlying data is the
  Jigsaw/Perspective-lineage Civil Comments corpus distributed via
  Kaggle channels (the card's honest note: dataset-as-distributed
  was not inspected this session — the paper is the verified
  anchor).

## 2. Composition (abstract-level)

- Highly skewed multi-label toxicity classes; the paper's
  performance/bias/speed comparison design. Sizes and label
  inventory: body-level, **unclaimed** here.

## 3. Collection and labeling

- Platform-native moderation data (real-world distribution — the
  property that distinguishes it from constructed sets like
  DynaHate (card 36): here the skew IS the
  phenomenon, not a design flaw to balance away).
- The paper's bias-metric integration is the card's teaching
  payload: performance, bias, and latency reported together —
  [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md)'s
  price-tag discipline applied to a content-moderation stack.

## 4. Splits and leakage discipline

- Standard contamination caveats; class-skew reporting demands
  per-class intervals (Wilson, per class — the paired-ledger rule
  for skewed distributions).

## 5. Where the course uses it

- **Ch. 21:** real-distribution toxicity — the naturally-skewed
  counterpart to the curated sets, feeding the exposure analysis.
- **P03/P09:** skewed-class calibration and per-class subgroup
  audits — the reliability instruments' stress case.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; sizes and labels unclaimed;
  the underlying corpus's distribution page uninspected (the
  anchor paper carries the card).
