# Dataset card: StereoSet

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a benchmark for **measuring stereotypical bias in
  pretrained language models** — the abstract's framing: stereotypes
  are "over-generalized beliefs about a particular group," such
  beliefs "are known to hurt target groups," and since LMs train on
  real-world data they capture these biases; StereoSet exists to
  *quantify* what was captured, where existing bias work evaluated
  on "a small set of artificially constructed" probes (the
  abstract's diagnosis, truncating there).
- **Canonical home:** "StereoSet: Measuring stereotypical bias in
  pretrained language models" (Nadeem et al., arXiv:2004.09456,
  2020-04-20, API-verified 2026-10-25).

## 2. Composition (abstract-level)

- The design (from the paper's own wider record at abstract level,
  with the API truncation recorded): intrasentence and intersentence
  **crowdsourced** association tests — a context, a stereotypical
  continuation, an anti-stereotypical continuation, and a
  meaningless control; bias measured as preference for the
  stereotypical option, alongside a language-modeling score to
  separate bias from degradation. The abstract's truncation leaves
  sizes and category counts body-level, **unclaimed here**.

## 3. Collection and labeling

- Crowdsourced construction (the paper's stated method family) —
  the supply side sits in [comparison 12](../../research/notes/comparison-12-evaluation-supply-strategies.md)'s
  human-curated middle. The annotator and validation protocol are
  body-level.

## 4. Splits and leakage discipline

- A diagnostic probe set, not a training set; the course's use is
  measurement-only, with the contamination caveat inverted: the
  *point* is to measure what training data already embedded.

## 5. Where the course uses it

- **Ch. 02/21:** the bias-measurement unit's canonical citation —
  pairing with BBQ (card 05) as the two bias
  instrument generations (association-based vs question-based),
  and with CrowS-Pairs (card 19) as the
  paired-perturbation family.
- **P09:** the slice template — per-category bias reporting with
  intervals, never a single bias number.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; sizes and categories
  unclaimed (truncation); the intrasentence-vs-CrowS-Pairs
  methodology debates are body/literature-level and cited only as
  existing.
