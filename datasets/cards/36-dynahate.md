# Dataset card: DynaHate

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a hate-detection dataset built by a
  **human-and-model-in-the-loop process over four rounds of dynamic
  data creation** — trained annotators generating entries designed
  to challenge the models, Dynabench-style
  rounds applied to hate speech (the card's structural kin: dynamic
  generation against a moving model target).
- **Canonical home:** "Learning from the Worst: Dynamically
  Generated Datasets to Improve Online Hate Detection" (Vidgen et
  al., arXiv:2012.15761, 2020-12-31, API-verified 2026-10-25).

## 2. Composition (abstract-stated)

- **~40,000 entries**, generated and labelled by trained annotators
  across the four rounds.
- **~15,000 challenging perturbations** — the adversarial half.
- **Fine-grained labels for type and target of hate** on every
  hateful entry; **hateful entries are 54% of the dataset**,
  "substantially higher than comparable datasets" (the abstract's
  own comparison).
- The abstract's headline finding: "model performance is su[bject
  to substantial degradation under adversarial conditions]" —
  truncation recorded; the point stands at its level.

## 3. Collection and labeling

- Trained annotators (not crowd volunteers) with fine-grained
  labeling — [comparison 12](../../research/notes/comparison-12-evaluation-supply-strategies.md)'s
  adversarial-human extreme of the supply spectrum, applied to a
  harm domain.
- The 54% balance is a design choice against class-imbalance
  pathologies — recorded as the dataset's stated property, not a
  universal standard.

## 4. Splits and leakage discipline

- Round structure *is* the split discipline (train on earlier
  rounds, evaluate on later adversarial rounds). Standard
  contamination caveats apply.

## 5. Where the course uses it

- **Ch. 21:** dynamic hate evaluation — perturbation robustness in
  the harm domain, with target labels feeding the exposure analysis.
- **Ch. 15:** the Dynabench-lineage citation for dynamic generation
  in a safety-critical domain.
- **P07/P09:** adversarial-perturbation and subgroup audit
  candidate with fine-grained slices.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; the degradation finding
  truncates in the API record (recorded); annotator-training detail
  and per-round dynamics body-level.
