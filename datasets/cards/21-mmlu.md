# Dataset card: MMLU (Measuring Massive Multitask Language Understanding)

MIT (Hugging Face license tag, `cais/mmlu`) · verification date
2026-10-23 · prepared by the course build · status: paper verified at
`abstract-read` level; split sizes verified via the HF datasets-server
API

## 1. Identity and provenance

- **What it is:** a multitask accuracy test for text models — 57 tasks
  spanning elementary mathematics, US history, computer science, law,
  and more; the general-capability anchor the course uses as the
  retained-capability control in unlearning and safety-training
  discussions (Ch.17 shift; Ch.20 hazardous-knowledge evaluations).
- **Canonical home:** `cais/mmlu` on Hugging Face [R2] (541,018
  downloads, 881 likes at inspection; last modified 2024-03-08). Paper:
  *Measuring Massive Multitask Language Understanding*, arXiv:2009.03300,
  2020-09-07 [R1].
- **Authors (abstract-verified [R1]):** Dan Hendrycks, Collin Burns,
  Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and 1 further
  author (7 total).
- **How WE obtained it:** abstract read + HF API page inspection +
  datasets-server split query on 2026-10-23; no question content
  downloaded or redistributed.

## 2. Composition (abstract + split-verified)

- **57 tasks** including elementary mathematics, US history, computer
  science, law, and more [R1].
- Split sizes under the `all` configuration (HF datasets-server [R3]):
  **test 14,042; validation 1,531; dev 285; auxiliary_train 99,842**.
  Per-subject splits also exist (e.g., abstract_algebra test 100,
  anatomy test 135, astronomy test 152 [R3]).
- Baseline finding at publication: most recent models had **near
  random-chance accuracy**, while the very largest GPT-3 model
  improved over random chance by **almost 20 percentage points on
  average** [R1].

## 3. Collection and labeling

- The collection methodology (sources of questions, exam provenance,
  filtering) lives in the unread body; the auxiliary_train split's
  provenance (ARC/MC_TEST/OBQA/RACE per the wider literature) is NOT
  verified at this access level and is not relied upon by the course.

## 4. Splits and leakage discipline

- Fixed public test set since 2020 — heavily contaminated territory
  for current models; MMLU is a *retained-knowledge* instrument in
  this course, never a frontier-capability claim. The dev/validation
  splits support few-shot prompts; cross-generation comparisons should
  state cutoffs and few-shot protocol (Ch.02 rule).

## 5. Uses and known misuse

- **Measures well:** broad multitask knowledge retention — exactly the
  control variable needed when evaluating safety interventions
  (unlearning, safety tuning) for collateral capability damage.
- **Does not measure:** safety, honesty, or calibration (separate
  instruments in this catalog); frontier reasoning (post-2020
  contamination makes headline accuracy uninterpretable for current
  models).
- Known misuse: quoting MMLU as an alignment or safety metric; the
  catalog's role here is the *paired-control* discipline (Ch.16's
  utility ledger; Ch.20's retained-capability checks).

## 6. What this dataset cannot support

- Claims about current frontier models' knowledge state.
- Per-subject curriculum claims (per-subject composition beyond the
  spot-checked splits lives in the unread body/repo).
- Any evaluation of *safety* constructs.

## 7. Maintenance

- License: MIT per the HF tag [R2]. Subject taxonomy and answer-key
  maintenance history live in the repository, unread this round.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2009.03300 (via arXiv API) | title; 7 authors (Hendrycks, Burns, Basart, Zou, Mazeika, Song, +1); 2020-09-07; abstract (57 tasks; near random-chance for most models; largest GPT-3 ~20pp over random) | abstract-read | 2026-10-23 |
| [R2] | https://huggingface.co/api/datasets/cais/mmlu | license tag mit; arXiv tags (2009.03300 + three related); 881 likes; 541,018 downloads; last modified 2024-03-08 | page-inspected (API) | 2026-10-23 |
| [R3] | https://datasets-server.huggingface.co/size?dataset=cais/mmlu | all/test 14,042; all/validation 1,531; all/dev 285; all/auxiliary_train 99,842; spot-checked per-subject splits (abstract_algebra 100, anatomy 135, astronomy 152) | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the collection methodology, auxiliary_train
provenance, per-subject full listing, and the paper's per-model
results — pending the full-text read.
