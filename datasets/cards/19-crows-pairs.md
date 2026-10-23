# Dataset card: CrowS-Pairs

CC BY-SA 4.0 (canonical repository README statement; HF tag agrees) ·
verification date 2026-10-23 · prepared by the course build · status:
paper verified at `abstract-read` level; canonical README and HF page
inspected

## 1. Identity and provenance

- **What it is:** a challenge benchmark of **crowdsourced stereotype
  pairs** — minimal sentence pairs where one sentence is more
  stereotyping and the other less, for measuring social bias in masked
  language models against protected demographic groups in the US.
- **Canonical home:** `github.com/nyu-mll/crows-pairs` (master branch,
  read 2026-10-23) [R2]; Hugging Face hosting `nyu-mll/crows_pairs`
  [R3] (943 downloads, 15 likes at inspection). Paper: *CrowS-Pairs: A
  Challenge Dataset for Measuring Social Biases in Masked Language
  Models*, arXiv:2010.00133, 2020-09-30 [R1].
- **Authors (abstract-verified [R1]):** Nikita Nangia, Clara Vania,
  Rasika Bhalerao, Samuel R. Bowman (NYU).
- **How WE obtained it:** abstract read + repository README read + HF
  API page inspection on 2026-10-23; no pair content downloaded or
  redistributed.

## 2. Composition (abstract-verified)

- **1,508 examples covering stereotypes dealing with nine types of
  bias**, including race, religion, and age [R1].
- The minimal-pair design: a model is presented with two sentences —
  one more stereotyping, one less — and the measured quantity is which
  the model prefers [R1]. The data focuses on stereotypes about
  historically disadvantaged groups, contrasted with advantaged groups
  [R1].
- Headline finding: **all three widely-used MLMs evaluated
  substantially favor sentences that express stereotypes in every
  category** [R1].

## 3. Collection and labeling

- Crowdsourced construction [R1]; the annotator protocol, per-bias-type
  counts, and validation procedure live in the unread body. The
  repository's provenance statement (README [R2]): the data is created
  using prompts taken from the ROCStories corpora and the fiction part
  of MNLI — downstream users inherit those corpora's terms.

## 4. Splits and leakage discipline

- A single fixed evaluation set; no train split (it is not a training
  artifact). Contamination: public since 2020, so post-2020 models may
  have seen the pairs; stereotype-preference comparisons across model
  generations should state knowledge cutoffs (Ch.02 rule).

## 5. Uses and known misuse

- **Measures well:** stereotype preference in masked-LM
  pseudo-log-likelihood scoring — the paradigm it was built for.
- **Does not measure:** generative toxicity (different construct —
  RealToxicityPrompts, card 03); bias beyond the nine covered types;
  non-US cultural contexts (the abstract scopes to protected
  demographic groups in the US).
- Known misuse: reporting a single aggregate score without the
  per-type breakdown; quoting the MLM finding as a claim about
  decoder-only chat models (different scoring paradigm).

## 6. What this dataset cannot support

- Claims about real-world harm rates (it measures model preference,
  not deployment effects).
- Comparative claims across bias benchmarks without stating each
  one's construct (BBQ's QA framing vs CrowS-Pairs' MLM scoring —
  Ch.02's construct-validity exercise).
- Per-type bias magnitude rankings (per-type counts live in the
  unread body).

## 7. Maintenance

- License: **CC BY-SA 4.0** — stated in the canonical repository's
  README [R2] and matching the HF tag [R3]; the repository carries no
  LICENSE file (recorded honestly). ShareAlike obligations apply to
  adaptations; seed-corpus provenance (ROCStories, MNLI fiction)
  should be cited downstream [R2].

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2010.00133 (via arXiv API) | title; 4 authors (Nangia, Vania, Bhalerao, Bowman); 2020-09-30; abstract (1,508 examples; nine bias types incl. race/religion/age; minimal-pair design; disadvantaged-vs-advantaged contrast; all three MLMs favor stereotypes in every category) | abstract-read | 2026-10-23 |
| [R2] | https://github.com/nyu-mll/crows-pairs (README.md, master branch) | license statement (CC BY-SA 4.0); seed provenance (ROCStories corpora + fiction part of MNLI) | page-inspected (direct read) | 2026-10-23 |
| [R3] | https://huggingface.co/api/datasets/nyu-mll/crows_pairs | license tag cc-by-sa-4.0; 943 downloads; 15 likes; last modified 2024-01-18 | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the crowdsourcing protocol, per-type
example counts, annotator demographics, and the three evaluated MLMs'
specific scores — all pending the full-text read.
