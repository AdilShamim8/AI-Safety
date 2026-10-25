# Dataset card: PKU-SafeRLHF

LICENSE not observed this session — the canonical Hugging Face page's
license tag was not inspected; **unknown (pending page-inspect)** ·
verification date 2026-10-25 (arXiv abstract verified via API;
title/authors/date checked) · prepared by the course build · status: card
at abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a safety human-preference dataset designed for safety
  alignment research — and, critically, **separating the annotations of
  helpfulness and harmlessness** for the same question-answer pairs,
  "providing distinct perspectives on these coupled attributes." The
  abstract's own framing: a sibling project to SafeRLHF and BeaverTails
  (the latter already carded as DS-007).
- **Canonical home:** "PKU-SafeRLHF: Towards Multi-Level Safety
  Alignment for LLMs and Agents" (Ji et al., arXiv:2406.15513,
  2024-06-20, API-verified 2026-10-25); dataset hosted under the
  PKU-Alignment organization on Hugging Face.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-stated)

- **44.6k refined prompts** and **265k question-answer pairs** with
  safety meta-labels — the abstract's own counts, quoted verbatim.
- **19 harm categories** and **three severity levels** ranging from
  minor to severe — the multi-level taxonomy of the title, with
  answers generated [by models named in the body — unclaimed here].
- The separation design is the composition's load-bearing choice: the
  same response carries *two independent* labels (helpful? harmless?),
  so preference training on this data can trade the axes explicitly
  instead of learning a confounded "goodness."

## 3. Collection and labeling

- Abstract-level: refined prompts (curation applied), paired QA
  generation, and safety meta-labels at the stated granularity. The
  annotation protocol (annotator counts, agreement, training) is
  body-level and unclaimed.
- Course-relevant: the 19-category × 3-severity structure encodes a
  *graduated* harm model — harm as severity levels rather than a
  binary — which is the exact move Ch. 04's harm-preference training
  and Ch. 21's severity-tail analysis both need from a dataset.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline: preference
  data is training data — any safety evaluation on it must use
  held-out prompts with grouped splits by prompt family (Ch. 02's
  rule for preference corpora).

## 5. Where the course uses it

- **Ch. 04:** the decoupled-axes citation — preference training that
  can optimize helpfulness and harmlessness separately, the design
  response to the coupled-objective problem the HH-RLHF line
  (card 08) trained jointly.
- **P04** (preference-optimization audit): the natural real-world
  candidate for the audit's data tier, cited alongside BeaverTails
  with the same paired-metric discipline (helpfulness change +
  harmlessness change, never one alone).
- **Ch. 21:** severity-level labels as the dataset-side anchor for
  severity distribution analysis.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; annotation protocol,
  model-generated-answer specifics, and split structure unclaimed.
  The abstract truncates mid-sentence ("answers gen[erated…]") —
  recorded here as the API record's honest limit.
