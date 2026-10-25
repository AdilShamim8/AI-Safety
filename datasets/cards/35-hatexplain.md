# Dataset card: HateXplain

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** the first benchmark hate-speech dataset "covering
  multiple aspects of the issue": every post annotated **from three
  perspectives** — the 3-class classification (hate / offensive /
  normal), **the target community** (who the hate/offense is aimed
  at), and the rationale spans (the abstract's truncated third
  perspective — explainability, per the paper's title and the
  dataset's name).
- **Canonical home:** "HateXplain: A Benchmark Dataset for
  Explainable Hate Speech Detection" (Mathew et al., arXiv:2012.10289,
  2020-12-18, API-verified 2026-10-25); data and code on GitHub and
  Hugging Face mirrors.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25;
  no content downloaded or redistributed.

## 2. Composition (abstract-stated)

- The three-perspective annotation scheme (3-class label + target
  community + rationales) — the abstract's own design statement.
- Sizes and the community list: body-level, **not established at
  this access level** — recorded as the honest limit.

## 3. Collection and labeling

- Abstract-level: posts collected from social media; the
  multi-perspective annotation is the dataset's distinguishing
  discipline. The annotator protocol and agreement statistics are
  body-level, unclaimed.
- Course-relevant design: the target-community field makes **who is
  harmed** a first-class label — the distributional question
  [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md)
  needs from a hate dataset, and the reason this card exists when
  RealToxicityPrompts (card 03)
  sets already do toxicity scoring.

## 4. Splits and leakage discipline

- Not established at abstract level; the standard grouped-split and
  contamination caveats apply (social-media text is in every large
  model's training data — memorization caveats from notes 56-58
  apply to any generation use).

## 5. Where the course uses it

- **Ch. 21:** hate-speech as a *targeted* harm — the target field
  drives the exposure analysis.
- **Ch. 10/11:** the rationale spans as interpretability ground
  truth — an explainability benchmark usable for evaluating
  rationale-faithfulness claims ([notes 38](../../research/notes/38-unfaithful-explanations.md)/[43](../../research/notes/43-measuring-cot-faithfulness.md)
  apply their caveats).
- **P09:** the subgroup-reliability audit's real-world candidate —
  target-community slices are exactly the subgroup axis.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; sizes, communities,
  agreement statistics unclaimed; the third annotation perspective
  confirmed only via the paper's title and the dataset's stated
  purpose (truncation recorded).
