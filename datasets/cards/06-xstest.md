# Dataset card: XSTest

CC BY 4.0 for prompts (verbatim from the repository [R1]); model completions
remain under original Meta/Mistral/OpenAI licenses [R1] · verification date
2026-10-21 · prepared by the course build · status: fully verified at
`page-inspected` + `abstract-read` level

## 1. Identity and provenance

- **What it is:** a test suite for **exaggerated safety** — the failure
  mode where a model refuses *clearly safe* prompts because they resemble
  unsafe ones lexically or topically. It is the benign-control side of the
  red-teaming ledger: every safety evaluation needs its false-refusal
  denominator, and XSTest is the standard instrument for it.
- **Canonical home:** GitHub `paul-rottger/xstest` [R1]; canonical HF
  hosting `paul-rottger/xstest` (referenced as Paul/XSTest [R2]); mirrors
  inspected: `walledai/XSTest` [R3]. Paper: arXiv:2308.01263 [R4].
- **Authors (page-verified [R3, R4]):** Paul Röttger, Hannah Rose Kirk,
  Bertie Vidgen, Giuseppe Attanasio, Federico Bianchi, Dirk Hovy.
- **Venue (page-verified):** accepted at NAACL 2024 main conference [R1,
  R4], anthology 2024.naacl-long.301 [R1].
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified)

- **250 safe prompts across ten prompt types** that a well-calibrated model
  should not refuse, **plus 200 unsafe prompts as contrasts** that most
  applications should refuse [R3, R4]. The safe/unsafe pairing is the
  design feature: refusal quality is only meaningful against the
  complementary compliance measurement.
- Prompt data file: `xstest_prompts_v2` (referenced on the mirror page
  [R3]).
- Small by intent: a *test suite*, not a training corpus — statistical
  treatment must respect small-n (Wilson intervals over 250-item
  denominators are the Ch.02 exercise; the course's P01 harness uses XSTest
  as the canonical scorer-validation fixture).

## 3. Collection and labeling

- Construction method (ten prompt types manually authored to be superficially
  similar to unsafe requests — e.g., safe requests that mention sensitive
  topics or use imperative language — then checked so they are clearly
  safe): described at abstract level [R4]; the per-type rubric details are
  pending the full-text read.
- Labeling: the safe/unsafe classification is design-determined
  (construct-built), not crowd-annotated; disagreement measures are not
  published at the achieved access level.

## 4. Splits and leakage discipline

- A single fixed test set (no train split — it is not a training artifact).
  Contamination risk is asymmetric and worth naming: XSTest prompts and
  per-model results circulate publicly, so models post-NAACL-2024 may have
  seen the suite; refusal-rate comparisons across model generations should
  therefore state knowledge cutoffs (Ch.02 rule, exercised here).

## 5. Uses and known misuse

- **Measures well:** the *rate at which a model refuses clearly-safe
  prompts*, organized by superficial-similarity type — i.e., the false
  positive side of a safety filter, with the unsafe set supplying the false
  negative side on the same axis.
- **Known misuse patterns:** (a) reporting XSTest refusal rate without the
  unsafe-prompt compliance rate (half a confusion matrix); (b) averaging
  across the ten types when the interesting signal is per-type (models fail
  differently on, say, roleplay framing vs topic similarity — the type
  breakdown is the diagnostic); (c) using it to rank "safety" overall — it
  measures a calibration corner, not overall safety.

## 6. What this dataset CANNOT support

- Toxicity, bias, or hallucination claims — none of those constructs are
  targeted.
- Non-English over-refusal: English prompts as inspected.
- Claims about *appropriate* refusal judgment on genuinely borderline
  prompts: XSTest items are designed to be clearly safe (or clearly unsafe
  in the contrast set) — the hard middle is out of scope by design.

## 7. Maintenance

- Versioned prompt file (`xstest_prompts_v2` [R3]) shows active maintenance
  history (v1→v2). Course projects (P01, P07) pin the prompt-file version
  with their results.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://github.com/paul-rottger/xstest | license section verbatim (prompts CC-BY-4.0; completions under Meta/Mistral/OpenAI original licenses); authors; NAACL 2024 + anthology link 2024.naacl-long.301; repository stats (149 stars, CC-BY-4.0 badge) | page-inspected | 2026-10-21 |
| [R2] | https://huggingface.co/datasets/Paul/XSTest | canonical HF hosting; 250 safe prompts across 10 prompt types; false-refusal purpose | page-inspected | 2026-10-21 |
| [R3] | https://huggingface.co/datasets/walledai/XSTest | 250 safe + 200 unsafe composition; prompt file name xstest_prompts_v2; license split (prompts vs completions); downloads/context; arXiv paper link | page-inspected | 2026-10-21 |
| [R4] | https://arxiv.org/abs/2308.01263 | abstract (design intent, tension helpfulness/harmlessness); submission history (v1 2023-08-02, v2 2023-10-17, v3 2024-04-01); author list; NAACL 2024 acceptance note | abstract-read | 2026-10-21 |
