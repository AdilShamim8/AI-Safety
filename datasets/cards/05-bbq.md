# Dataset card: BBQ (Bias Benchmark for QA)

license: **CC-BY-4.0** — resolved 2026-10-23 by direct read of the canonical
repository LICENSE (full Creative Commons Attribution 4.0 International legal
code, 18,649 bytes, SPDX CC-BY-4.0) [R4]; the mirror placeholder is
superseded · verification date 2026-10-21 (updated 2026-10-23) ·
prepared by the course build · status: composition verified across three
hosted pages; canonical license closed

## 1. Identity and provenance

- **What it is:** a hand-built multiple-choice benchmark for *stereotype
  bias in question answering*. Items are built in **paired designs** — an
  *ambiguous* context where the correct answer is "unknown" (any specific
  answer reveals bias), and a *disambiguated* context where the answer is
  determined but the stereotyped entity is aligned or anti-aligned with the
  correct answer. This two-condition design is what elevates BBQ above a
  mere stereotype quiz: it separates *reliance on stereotypes* from
  *knowledge*.
- **Canonical home:** GitHub `nyu-mll/BBQ` (referenced from the inspected
  mirror pages [R1, R2]). Paper: "BBQ: A Hand-Built Bias Benchmark for
  Question Answering", Parrish et al., Findings of ACL 2022 [R3].
- **Authors (page-verified from the mirror card [R1]):** Alicia Parrish,
  Angelica Chen, Nikita Nangia, Vishakh Padmakumar, Jason Phang, Jana
  Thompson, Phu Mon Htut, Samuel R. Bowman.
- **How WE obtained it:** page inspection only, 2026-10-21, across three
  hosted pages (two HF mirrors + anthology citation block); no content
  downloaded or redistributed.

## 2. Composition (page-verified)

- **58,492 rows** on the inspected mirror [R1], and the same count on a
  second independent mirror [R2] — two-page agreement recorded, which is the
  strongest verification this round achieved for any dataset's size.
- **9 demographic categories** [R2]: age, disability status, gender
  identity, nationality, physical appearance, race/ethnicity, religion,
  SES, sexual orientation — attested social biases in U.S.
  English-speaking contexts (paper abstract, quoted on the mirror [R1]).
- **Two conditions per category** [R2]: `{category}_ambig` and
  `{category}_disambig` configurations.
- **Item structure** [R2]: context, question, three answer options
  (ans0/ans1/ans2), label, question_polarity (neg/nonneg),
  context_condition, example_id, answer metadata incl. group information.
- **Splits** [R2]: test split as main evaluation; small train splits exist
  only as 4-shot examples; **Religion has no train split** (no 4-shot
  examples were available) — a detail that bites anyone writing uniform
  few-shot loaders, and therefore worth card-level memory.

## 3. Collection and labeling

- Construction (templates hand-authored per bias phenomenon, subject
  attested stereotypes; names and entities filled per category): paper-level
  description, pending full-text read.
- Label provenance: correct answers are construct-determined (ambig →
  "unknown" is correct), not crowd-voted — so classic annotator-agreement
  questions apply to *item validity*, not to label noise. Item-validity
  audits are exactly the exercise Ch.02/P09 assigns with this dataset.

## 4. Splits and leakage discipline

- With the test split as the evaluation and train splits being 4-shot
  exemplars only [R2], the leakage risk is not internal splitting but
  *pretraining contamination* — BBQ items and analyses are widely quoted in
  web text. Course discipline: report BBQ results with the model's knowledge
  cutoff stated; treat near-ceiling disambig accuracy on strong models as a
  contamination signal worth checking, not as a victory.

## 5. Uses and known misuse

- **Measures well:** (a) reliance on stereotypes under ambiguity (accuracy
  on ambig items where the correct answer is "unknown"), and (b) whether
  bias overrides knowledge (accuracy gap on disambig items when the correct
  answer conflicts with the stereotype) — the paper abstract's own framing,
  including the finding that models average up to 3.4 percentage points
  higher accuracy when the correct answer aligns with a social bias, and
  over 5 points on gender [R1].
- **Known misuse patterns:** (a) reporting a single aggregate "BBQ score"
  collapsing ambig/disambig and neg/nonneg polarities — the construct lives
  in the condition contrasts; (b) comparing models evaluated with different
  answer-ordering or parsing conventions; (c) U.S.-English generalization:
  the categories are U.S.-context attested biases [R1], so cross-cultural
  claims are out of scope.

## 6. What this dataset CANNOT support

- Toxicity measurement (no toxicity construct), refusal quality, or
  open-ended generation bias (it is a fixed-option QA instrument — BOLD is
  the complementary open-ended instrument).
- Claims that low measured bias implies fairness of deployment decisions.
- Timeless bias claims: stereotype manifestations are culturally and
  temporally situated; the dataset is a dated snapshot of attested U.S.
  English biases.

## 7. Maintenance

- Canonical license: **resolved 2026-10-23** — CC-BY-4.0, read directly
  from the canonical repository LICENSE [R4] (full Creative Commons
  Attribution 4.0 International legal code, 18,649 bytes; the repository
  hosts the dataset files, so the license covers the data). Course projects
  (P09) may now cite the license; redistribution of item text should still
  follow CC-BY-4.0 attribution requirements.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/heegyu/bbq | 58,492 rows; 50.9 MB; full author list; GitHub nyu-mll/BBQ; paper abstract incl. the 3.4pp / >5pp gender findings; ACL 2022 Findings citation block (2022.findings-acl.165, pp. 2086–2105, DOI 10.18653/v1/2022.findings-acl.165) | page-inspected | 2026-10-21 |
| [R2] | https://huggingface.co/datasets/HiTZ/bbq | 9 categories with names; ambig/disambig config naming; ans0/1/2 + label field structure; test + 4-shot train split semantics; Religion no-train exception; license placeholder observed | page-inspected | 2026-10-21 |
| [R3] | https://huggingface.co/datasets/walledai/BBQ | independent second mirror showing the same 58,492-row count | page-inspected | 2026-10-21 |
| [R4] | https://github.com/nyu-mll/BBQ (LICENSE via GitHub license API) | CC-BY-4.0 (Creative Commons Attribution 4.0 International), full legal code, 18,649 bytes; SPDX CC-BY-4.0; the canonical repository hosts the dataset files themselves | page-inspected | 2026-10-23 |

Explicitly **not** claimed: arXiv identifier (2110.08193 recorded at
metadata-only level), per-category item counts, construction timeline —
pending the paper read. The canonical license is now verified [R4].
