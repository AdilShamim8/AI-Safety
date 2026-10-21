# Dataset card: TruthfulQA

apache-2.0 (as displayed on the Hugging Face page [R1]) · verification date
2026-10-21 · prepared by the course build · status: metadata verified at
`page-inspected` level; paper assigned as Ch.06 reading, not yet full-text-read

## 1. Identity and provenance

- **What it is:** an adversarial question-answering benchmark targeting
  *imitative falsehoods* — falsehoods that humans commonly believe or repeat,
  which a model pretrained on human text may reproduce because the wrong
  answer is *more statistically frequent*, not because the model is broken.
- **Canonical hosting:** Hugging Face `truthfulqa/truthful_qa` [R1]. The paper
  is arXiv:2109.07958 (linked from the HF page [R1]). The benchmark's original
  distribution point is the authors' repository (`sylinrl/TruthfulQA` on
  GitHub, referenced from the paper page); this card's facts come from the HF
  canonical page.
- **Who created it:** the paper is by Hilton, Evans, and Lin (author list per
  the paper's arXiv page, recorded at `metadata-only` level this round — the
  author names were **not** independently re-verified in this session and are
  pending the full-text read).
- **How WE obtained it:** metadata only, via direct inspection of the HF
  dataset page on 2026-10-21. No dataset content was downloaded or is
  redistributed here.

## 2. Composition

- **817 questions**, observed as the validation split's row count on the HF
  page [R1]. Single split (validation); size category displayed as 1K–10K [R1].
- **Task structure:** the HF page lists task categories multiple choice, text
  generation, and question answering [R1] — reflecting the benchmark's two
  evaluation regimes (generative answers and multiple-choice scoring).
- **Adversarial content domains** observed on the page [R1]: Misconceptions,
  Proverbs, Misquotations, Conspiracies, Superstitions (the page groups these
  under an "Adversarial" label). The paper's fuller 38-category taxonomy is
  paper-level knowledge **not verified this round** and is flagged as such.
- Sensitive content: questions deliberately embed common false beliefs;
  harmful-content density is low by design (the target is falsehood, not
  toxicity).

## 3. Collection and labeling

- Construction method (questions written adversarially by the authors, then
  filtered; multiple-choice options include true and false reference answers;
  human evaluators score generative answers against reference sets): this is
  **paper-level description, pending full-text verification**. The page-level
  facts are the counts above.
- Agreement measures (e.g., inter-annotator agreement for generative
  scoring): not visible at page level; recorded as **not published at the
  access level achieved**.

## 4. Splits and leakage discipline

- One 817-row validation split [R1] — the benchmark is an *evaluation-only*
  artifact. The course's discipline for it: it must never enter any training
  or few-shot tuning pipeline; contamination checks (n-gram overlap against
  pretraining corpora) are a Ch.02 discussion topic with TruthfulQA as the
  canonical example, because its questions are the kind of text that leaks
  into web crawls.

## 5. Uses and known misuse

- **Measures well:** a model's tendency to repeat common human falsehoods
  rather than give the literally true answer, under an adversarial question
  distribution.
- **Known misuse patterns** (course-position, not dataset defects): (a)
  quoting a TruthfulQA score as evidence of general honesty or safety — it is
  neither; (b) fine-tuning on TruthfulQA-style QA pairs to inflate the score
  (benchmark overfitting / adaptive contamination); (c) ignoring that
  "truthful" here means *not repeating common falsehoods*, which is a
  narrower construct than epistemic calibration.

## 6. What this dataset CANNOT support

- Claims about toxicity, bias, refusal quality, or harmful-capability
  levels — none of those constructs are targeted by the item distribution
  observed.
- Comparative claims like "model A is more honest than model B" without
  also reporting prompt format, decoding parameters, and the scoring regime
  (generative vs. multiple-choice produce different rankings).
- Long-horizon consistency or calibration claims: a fixed 817-question set
  cannot measure how truthfulness degrades over a multi-turn interaction.

## 7. Maintenance

- Upstream maintenance cadence: not determined this round (page did not show
  a changelog). The repo pins nothing; projects that use TruthfulQA (P01, P03)
  must record the HF revision they loaded.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/truthfulqa/truthful_qa | license tag (apache-2.0); validation split = 817 rows; size category 1K–10K; task tags (MC, text generation, QA); adversarial subcategory names (Misconceptions, Proverbs, Misquotations, Conspiracies, Superstitions); arXiv link 2109.07958 | page-inspected | 2026-10-21 |

Explicitly **not** claimed: paper author list, 38-category taxonomy, MC1/MC2
metric definitions, human-evaluation protocol — all pending the Ch.06
full-text reading of arXiv:2109.07958.
