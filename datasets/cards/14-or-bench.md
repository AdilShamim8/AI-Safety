# Dataset card: OR-Bench

CC-BY-4.0 (both Hugging Face hostings carry the tag) · verification date
2026-10-23 · prepared by the course build · status: paper verified at
`abstract-read` level; hosting pages inspected via the HF API; composition
numbers from the verified abstract

## 1. Identity and provenance

- **What it is:** the first large-scale **over-refusal benchmark** — a
  corpus of prompts that are innocuous but crafted to trigger refusals,
  giving the over-refusal side of the safety ledger a systematic instrument.
  Where XSTest hand-authors 250 safe prompts, OR-Bench automatically
  generates 80,000, trading curation depth for scale.
- **Canonical home:** the paper names `https://huggingface.co/bench-llms`
  and the code repository `github.com/justincui03/or-bench` [R1]. Two HF
  orgs exist and both carry CC-BY-4.0: `bench-llms/or-bench` (the org named
  in the abstract's URL; 937 downloads at inspection) and `bench-llm/or-bench`
  (higher traffic: 9,801 downloads; last modified 2024-12-19) [R2, R3]. The
  org-name discrepancy (`bench-llms` vs `bench-llm`) is recorded honestly;
  both hostings agree on the license tag and the paper description.
- **Paper:** *OR-Bench: An Over-Refusal Benchmark for Large Language
  Models* — arXiv:2405.20947, v1 2024-05-31, v5 2025-06-15 [R1].
- **Authors (abstract-verified [R1]):** Justin Cui, Wei-Lin Chiang, Ion
  Stoica, Cho-Jui Hsieh.
- **How WE obtained it:** abstract read + HF API page inspection on
  2026-10-23; no prompt content downloaded or redistributed.

## 2. Composition (abstract-verified)

- **80,000 over-refusal prompts across 10 common rejection categories**,
  a subset of **around 1,000 hard prompts** that challenge even
  state-of-the-art LLMs, and an additional **600 toxic prompts** included
  to prevent indiscriminate compliance from models optimized to never
  refuse [R1].
- The toxic-prompt contrast set is the design feature worth teaching: an
  over-refusal score is only interpretable next to a compliance score —
  the same paired-ledger discipline as XSTest's 250/200 split (Ch.02).
- The paper reports a measurement study of **32 popular LLMs across 8
  model families** [R1].

## 3. Collection and labeling

- Prompts are **automatically generated** by a novel method the paper
  introduces for large-scale over-refusal dataset construction [R1]; the
  generation pipeline details live in the unread body. Automatic
  generation is the load-bearing caveat: category labels are assigned by
  construction, not by independent human adjudication at the achieved
  access level.

## 4. Splits and leakage discipline

- Hard-prompt subset and toxic contrast are the published splits [R1].
  Contamination consideration: automatically generated prompts are less
  likely to be memorized verbatim than hand-authored suites, but the
  benchmark's public release (2024) means post-2024 models may have
  adapted to its distribution; over-refusal comparisons across model
  generations should state knowledge cutoffs (Ch.02 rule).

## 5. Uses and known misuse

- **Measures well:** the scale side of over-refusal measurement;
  monitoring drift in refusal thresholds after safety-tuning changes
  (Ch.06 selective prediction; C04's authorization-boundary framing).
- **Does not measure:** why a model refuses (no rationale annotations);
  calibrated abstention quality (a refusal of an unanswerable question is
  correct behavior, and OR-Bench's category structure does not separate
  it from over-refusal — the construct question Ch.02 drills).
- Known misuse: quoting a single OR-Bench rate without the paired toxic
  compliance rate — a model can trivially lower over-refusal by complying
  with everything.

## 6. What this dataset cannot support

- Claims about refusal quality in languages other than the generated
  distribution (English at abstract level).
- Causal claims about which alignment stage created the over-refusal —
  the benchmark measures the behavior, not the mechanism.
- Per-category refusal rates (category-level results live in the unread
  body).

## 7. Maintenance

- License: CC-BY-4.0 on both hostings [R2, R3]. The dual-org situation is
  a provenance question for downstream users: cite the paper, pin the
  exact hosting and revision used.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2405.20947 (via arXiv API) | title; authors (Cui, Chiang, Stoica, Hsieh); v1 2024-05-31 / v5 2025-06-15; abstract (80,000 prompts, 10 categories, ~1,000 hard, 600 toxic; 32 LLMs / 8 families; automatic generation method; HF org bench-llms; github justincui03/or-bench) | abstract-read | 2026-10-23 |
| [R2] | https://huggingface.co/api/datasets/bench-llms/or-bench | org named in the paper's URL; license tag cc-by-4.0; 937 downloads; last modified 2024-06-23 | page-inspected (API) | 2026-10-23 |
| [R3] | https://huggingface.co/api/datasets/bench-llm/or-bench | license tag cc-by-4.0; 9,801 downloads; 22 likes; last modified 2024-12-19; org-name discrepancy vs the paper's URL recorded | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the prompt-generation pipeline details,
per-category composition counts, per-model results, and any statement
about which hosting is "official" beyond what the paper's URL names —
all pending the full-text read and a repository inspection.
