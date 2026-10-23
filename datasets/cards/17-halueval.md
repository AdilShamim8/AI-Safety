# Dataset card: HaluEval

apache-2.0 (Hugging Face mirror `pminervini/HaluEval` license tag) ·
verification date 2026-10-23 · prepared by the course build · status:
paper verified at `abstract-read` level; canonical GitHub README read
directly; hosting pages inspected

## 1. Identity and provenance

- **What it is:** a large-scale **hallucination evaluation benchmark** —
  generated and human-annotated hallucinated samples for evaluating
  whether LLMs can *recognize* hallucinated content, across general,
  QA, dialogue, and summarization settings.
- **Canonical home:** `github.com/RUCAIBox/HaluEval` [R2] (the paper's
  stated access point [R1]); Hugging Face hosting `pminervini/HaluEval`
  [R3] (8,996 downloads, 34 likes at inspection; last modified
  2023-12-07). Paper: *HaluEval: A Large-Scale Hallucination Evaluation
  Benchmark for Large Language Models*, arXiv:2305.11747,
  v1 2023-05-19, updated 2023-10-23 [R1].
- **Authors (abstract-verified [R1]):** Junyi Li, Xiaoxue Cheng, Wayne
  Xin Zhao, Jian-Yun Nie, Ji-Rong Wen (RUC AI Box group).
- **How WE obtained it:** abstract read + canonical README fetch + HF
  API page inspection on 2026-10-23; no sample content downloaded or
  redistributed.

## 2. Composition (README-verified)

- **35K generated and human-annotated hallucinated samples** used in the
  paper's experiments [R2], composed as:
  - **5K general** — human-annotated samples for ChatGPT responses to
    general user queries drawn from the Alpaca 52K instruction-tuning
    set [R2];
  - **10K QA** — hallucinated samples with HotpotQA as seed data
    (fields: knowledge from Wikipedia, question, right_answer,
    hallucinated_answer) [R2];
  - **10K dialogue** — OpenDialKG as seed (knowledge, dialogue_history,
    right_response, hallucinated_response) [R2];
  - **10K summarization** — CNN/Daily Mail as seed (document,
    right_summary, hallucinated_summary) [R2].
- Each task pairs a *right* and a *hallucinated* target — the
  forced-choice design that makes recognition measurable.

## 3. Collection and labeling

- Two-step ChatGPT-based framework: **sampling-then-filtering** [R1],
  plus hired human labelers annotating hallucinations in ChatGPT
  responses [R1]. The empirical headline at abstract level: ChatGPT is
  likely to generate hallucinated content in specific topics by
  fabricating unverifiable information — **about 19.5% of responses**
  [R1] (on the paper's topic distribution; a construct statement, not a
  universal rate).
- Providing external knowledge or adding reasoning steps helps LLMs
  recognize hallucinations [R1] — the finding that connects this
  benchmark to Ch.06's calibration-without-honesty discussion.

## 4. Splits and leakage discipline

- Fixed evaluation sets per task [R2]; the seeds are public corpora
  (HotpotQA, OpenDialKG, CNN/DM, Alpaca), so contamination risk is the
  standard one: post-2023 models may have seen both seeds and the
  benchmark; recognition scores across model generations should state
  knowledge cutoffs (Ch.02 rule).

## 5. Uses and known misuse

- **Measures well:** hallucination *recognition* (the forced-choice
  task), topic-dependent generation tendencies at 2023-era model
  quality.
- **Does not measure:** free-form factual accuracy (SimpleQA is the
  instrument for that — this catalog's card 18); calibration of
  confidence (Ch.06 separates knowing from knowing-that-you-know).
- Known misuse: quoting 19.5% as "ChatGPT hallucinates 19.5% of the
  time" without the topic-distribution qualifier.

## 6. What this dataset cannot support

- Claims about current-generation models (2023 benchmark).
- Aggregate "hallucination rate" claims across deployments — the
  construct is topic-specific fabrication of unverifiable information.
- Cross-task comparability claims beyond the paper's own experiments.

## 7. Maintenance

- License: apache-2.0 per the HF mirror tag [R3]; the canonical GitHub
  repository does not display a license file in the fetched listing and
  the README carries no license statement — the mirror's tag is the
  only license signal at the achieved access level, recorded honestly.
  Downstream users should verify before redistribution.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2305.11747 (via arXiv API) | title; 5 authors (Li, Cheng, Zhao, Nie, Wen); v1 2023-05-19 / updated 2023-10-23; abstract (sampling-then-filtering; human labelers; ~19.5% hallucinated responses in specific topics; external-knowledge/reasoning findings; github RUCAIBox/HaluEval) | abstract-read | 2026-10-23 |
| [R2] | https://github.com/RUCAIBox/HaluEval (README.md fetched raw) | 35K total composition; 5K general (Alpaca-sourced) + 10K each QA (HotpotQA), dialogue (OpenDialKG), summarization (CNN/Daily Mail); per-task field schemas | page-inspected (direct read) | 2026-10-23 |
| [R3] | https://huggingface.co/api/datasets/pminervini/HaluEval | id; license tag apache-2.0; 34 likes; 8,996 downloads; last modified 2023-12-07; no arXiv tag on the page | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the filtering-instruction details, the
human-annotation protocol and agreement statistics, the paper's
per-model recognition results, and the license of the canonical
repository — all pending the full-text read.
