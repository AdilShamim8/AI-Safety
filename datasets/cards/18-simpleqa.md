# Dataset card: SimpleQA

simple-evals repository MIT (LICENSE read directly); canonical data file
served from `openaipublic.blob.core.windows.net` [R2, R3] · verification
date 2026-10-23 · prepared by the course build · status: paper verified
at `abstract-read` level; canonical CSV fetched and parsed row-by-row
(structure and counts only — no answer content redistributed)

## 1. Identity and provenance

- **What it is:** a short-form **factuality** benchmark — questions with
  a single, indisputable answer, adversarially collected against GPT-4
  responses, graded correct / incorrect / not attempted. It is the
  instrument for "do models know what they know" (Ch.06's selective
  prediction, P10's capstone factuality gate).
- **Canonical home:** the paper's stated location is
  `github.com/openai/simple-evals` [R1] (repository LICENSE read
  directly 2026-10-23: MIT [R2]); the eval script pins the canonical
  data URL `openaipublic.blob.core.windows.net/simple-evals/
  simple_qa_test_set.csv` [R3]. Paper: *Measuring short-form factuality
  in large language models*, arXiv:2411.04368, submitted 2024-11-07
  [R1] (the repository header renders the title as "SimpleQA: Measuring
  short-form factuality in large language models" [R3] — the arXiv
  listing omits the "SimpleQA:" prefix; both titles recorded).
- **Authors (abstract-verified [R1]):** Jason Wei, Nguyen Karina, Hyung
  Won Chung, Yunxin Joy Jiao, Spencer Papay, and 3 further authors
  (8 total, OpenAI).
- **How WE obtained it:** abstract read + repository/license inspection
  + canonical CSV parse on 2026-10-23; topic counts extracted
  programmatically; question/answer text is not reproduced in this
  course.

## 2. Composition (direct CSV read)

- **4,326 questions** (parsed with a CSV reader 2026-10-23; the naive
  line count is 4,333 because some quoted fields span lines — the
  row-accurate count is 4,326) [R3].
- Columns: `metadata` (topic, answer_type, source urls), `problem`,
  `answer` [R3].
- **Topic distribution (parsed [R3]):** Science and technology 858,
  Politics 709, Art 550, Other 475, Geography 424, Sports 368, Music
  341, TV shows 293, History 173, Video games 135 (sum 4,326 —
  cross-checked).

## 3. Collection and labeling

- Adversarially collected against GPT-4 responses: question writers
  were steered toward questions GPT-4 answers incorrectly, making the
  set *challenging by construction* [R1]. Single-indisputable-answer
  design makes grading easy — each answer graded correct, incorrect,
  or not attempted [R1].

## 4. Splits and leakage discipline

- A single public test set [R3]. Because "not attempted" is a graded
  outcome, the *intended* measurement couples accuracy with selective
  prediction: a model with ideal behavior gets as many correct as
  possible while not attempting questions it is not confident about
  [R1] — the same risk-coverage trade the course's Ch.06 formalizes.
  Contamination: fixed public set, post-2024 cutoffs should be stated.

## 5. Uses and known misuse

- **Measures well:** short-form factuality with unambiguous grading;
  the accuracy-attempt trade across confidence thresholds (when run
  with abstention instrumentation).
- **Does not measure:** long-form truthfulness (TruthfulQA's
  misconception construct), calibration quality absent abstention
  instrumentation, multilingual factuality.
- Known misuse: reporting accuracy without the not-attempted rate —
  the paper's own grading design makes that number half the story.

## 6. What this dataset cannot support

- Claims about hallucination *rates* in free-form generation (different
  construct — HaluEval, card 17).
- Agentic or tool-augmented factuality (closed-book construct).
- Comparisons across models without stating each model's option to
  abstain (the grading contract must be uniform).

## 7. Maintenance

- License: the `openai/simple-evals` repository is MIT [R2]; the data
  file is served from OpenAI's public blob storage with no separate
  license statement observed at the file location [R3] — recorded
  honestly; downstream redistribution should verify terms at the data
  URL directly.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2411.04368 (via arXiv API) | title (Measuring short-form factuality in large language models); 8 authors (Wei, Nguyen, Chung, Jiao, Papay, ...); submitted 2024-11-07; abstract (adversarial collection against GPT-4; single indisputable answers; correct/incorrect/not-attempted grading; know-what-you-know framing; github.com/openai/simple-evals) | abstract-read | 2026-10-23 |
| [R2] | https://github.com/openai/simple-evals (LICENSE via GitHub license API) | MIT license; repository file listing (simpleqa_eval.py present) | page-inspected | 2026-10-23 |
| [R3] | https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv (URL from simpleqa_eval.py, fetched and parsed) | 4,326 rows; columns metadata/problem/answer; topic distribution (858/709/550/475/424/368/341/293/173/135); multi-line quoted fields explaining the 4,333 naive line count | page-inspected (direct CSV read) | 2026-10-23 |

Explicitly **not** claimed: the paper's per-model results, the
collection protocol's writer instructions, answer-type distribution,
and any statement about the data file's license beyond what was
observable — pending the full-text read.
