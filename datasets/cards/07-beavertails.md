# Dataset card: BeaverTails

**CC BY-NC 4.0 — NON-COMMERCIAL** (HF page license tag [R1]) · verification
date 2026-10-21 · prepared by the course build · status: composition verified
at `page-inspected` level

## 1. Identity and provenance

- **What it is:** a large corpus of **prompt–response pairs with
  human safety annotations**, built to improve safety alignment of LLM
  assistants — including a *preference* layer (safer vs less-safe response
  comparisons). It is the bridge dataset between safety classification and
  preference learning, which is why Ch.04 and P04 use it as label-quality
  audit material.
- **Canonical hosting inspected:** Hugging Face `PKU-Alignment/BeaverTails`
  [R1]. Paper: arXiv:2307.04657 [R1].
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed. The license makes this the catalog's clearest
  case study in **usage discipline** (see below).

## 2. Composition (page-verified [R1])

- **364k rows in the default subset**, organized in four configurations
  with row counts observed on the page [R1]:
  - `330k_train` — 301k rows
  - `330k_test` — 33.4k rows
  - `30k_train` — 27.2k rows
  - `30k_test` — 3.02k rows
- **Safety-annotation dimensions** observed on the page [R1] (at least
  eight groups, list as displayed, truncated in the fetch): animal abuse;
  child abuse; controversial topics / politics; discrimination /
  stereotype / injustice; drug abuse / weapons / banned substance; financial
  crime / property crime / theft; hate speech / offensive language;
  misinformation regarding ethics / laws (…).
- Task category on the page: **text classification** [R1] — i.e., the
  hosted artifact is the safety-annotation corpus; the preference-pair
  structure is part of the project's data story at paper level.

## 3. Collection and labeling

- The annotation protocol (annotator demographics, instructions, pay,
  agreement statistics): **not visible at page level**; recorded as not
  published at the achieved access level. The dimension taxonomy observed
  [R1] is the page-level anchor; how labels were adjudicated is pending the
  full-text read.
- Because the dimension set mixes *content categories* (hate speech) with
  *topic categories* (politics), label audits (P04) must first decide which
  axis a "positive" label is on — a real ambiguity the course teaches with
  this exact taxonomy.

## 4. Splits and leakage discipline

- Four explicit train/test configurations at two scales [R1]; the course's
  rule for projects: name *which* configuration a number refers to (330k vs
  30k scale changes CIs materially), and never mix rows across the paired
  split families. Prompt-level near-duplicate checks across train/test are
  mandatory before any classifier claim.

## 5. Uses and known misuse

- **Measures well:** multi-dimensional safety annotation of assistant-style
  prompt–response pairs at scale; base material for safety-reward
  model training and label-quality analysis.
- **Known misuse patterns:** (a) **any commercial use — barred by CC
  BY-NC 4.0** [R1]; (b) treating "controversial topics" as a hazard category
  rather than a topic flag; (c) fine-tuning on the annotations and reporting
  held-out accuracy without checking prompt overlap between the two split
  families; (d) quoting "364k safety labels" — the truthful phrasing is
  "364k *rows* each carrying multi-dimensional annotations" [R1].

## 6. What this dataset CANNOT support

- English-only safety claims about other languages or cultural contexts.
- Evidence that a model is *safe* — it is training/evaluation material
  about annotations, not a safety certificate.
- Detoxification research that requires per-token rationales (labels are
  row-level as hosted).
- Any downstream use that relicenses or commercializes the content
  (license bar [R1]).

## 7. Maintenance

- Upstream cadence not determined this round. Given the NC license, course
  policy is strict: P04 may *load and analyze under evaluation terms*; the
  repository itself never copies rows, and any derived statistics must be
  aggregate-only.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/PKU-Alignment/BeaverTails | license tag cc-by-nc-4.0; 364k default rows; four split configs with row counts (330k_train 301k; 330k_test 33.4k; 30k_train 27.2k; 30k_test 3.02k); safety-dimension taxonomy (8+ groups as displayed); task (text classification); arXiv 2307.04657 | page-inspected | 2026-10-21 |

Explicitly **not** claimed: annotator counts, agreement statistics,
preference-pair construction, PKU authorship details — pending the
full-text read of arXiv:2307.04657.
