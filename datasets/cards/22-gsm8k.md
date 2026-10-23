# Dataset card: GSM8K (Grade School Math 8K)

MIT (canonical repository LICENSE read directly; HF tag agrees) ·
verification date 2026-10-23 · prepared by the course build · status:
paper verified at `abstract-read` level; split sizes verified via the
HF datasets-server API; the 8.5K-vs-8,792 discrepancy recorded

## 1. Identity and provenance

- **What it is:** a dataset of **high quality linguistically diverse
  grade school math word problems** for diagnosing multi-step
  mathematical reasoning; the reasoning-capability anchor the course
  pairs with safety instruments when utility ledgers are needed
  (Ch.16's DP re-train ledger; Ch.17's capability-retention checks).
- **Canonical home:** `github.com/openai/grade-school-math` (master
  branch, LICENSE read directly 2026-10-23: MIT, copyright (c) 2021
  OpenAI) [R2]; Hugging Face hosting `openai/gsm8k` [R3] (986,952
  downloads, 2,000 likes at inspection). Paper: *Training Verifiers to
  Solve Math Word Problems*, arXiv:2110.14168, 2021-10-27 [R1].
- **Authors (abstract-verified [R1]):** Karl Cobbe, Vineet Kosaraju,
  Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, and 6
  further authors (12 total, OpenAI).
- **How WE obtained it:** abstract read + repository LICENSE read +
  HF API inspection + datasets-server split query on 2026-10-23; no
  problem content downloaded or redistributed.

## 2. Composition (abstract + split-verified)

- The abstract states **8.5K** problems [R1]; the released splits sum
  to **8,792** (train 7,473 + test 1,319 [R3]) — a **documented
  discrepancy** between the paper's headline figure and the released
  artifact, recorded the same way the AdvBench 520-vs-500 mirror
  discrepancy is (card 09). Both numbers are true at their own level:
  abstract-stated vs artifact-realized.
- Two configurations on HF: `main` and `socratic` (same counts in
  each: 7,473 / 1,319 [R3]) — the socratic variant carries
  step-hinted solutions.
- Baseline finding at publication: even the largest transformer
  models failed to achieve high test performance despite the
  conceptual simplicity of the distribution [R1]; the paper's remedy
  is **training verifiers** — the dataset's role in the
  verify-then-generate paradigm [R1].

## 3. Collection and labeling

- Problems were authored by human contractors (per the wider
  literature — NOT verified at this access level and not relied
  upon); what is abstract-verified is the *characterization*: high
  quality, linguistically diverse, grade-school level, requiring
  multi-step reasoning [R1]. Solution-verification protocol details
  live in the unread body.

## 4. Splits and leakage discipline

- Fixed public train/test split since 2021; heavily practiced-on
  territory for current models — GSM8K in this course is a
  *retained-reasoning control*, not a frontier claim. The test set's
  1,319 problems are the utility-ledger denominator when quoted.

## 5. Uses and known misuse

- **Measures well:** multi-step word-problem reasoning at
  grade-school difficulty; the utility side of paired
  safety-vs-capability ledgers.
- **Does not measure:** advanced mathematics, symbolic rigor, or
  agentic tool use; safety constructs of any kind.
- Known misuse: quoting GSM8K accuracy as general intelligence;
  quoting the 8.5K figure as the dataset size without noting the
  released-artifact count differs (the discrepancy cut both ways in
  the literature).

## 6. What this dataset cannot support

- Claims about mathematical *soundness* of current models
  (contamination plus answer-key leakage risk).
- Cross-benchmark reasoning rankings without identical few-shot and
  stopping protocols.
- The contractor-protocol claims sometimes attached to it (unverified
  here).

## 7. Maintenance

- License: MIT (canonical LICENSE [R2]; HF tag agrees [R3]).

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2110.14168 (via arXiv API) | title; 12 authors (Cobbe, Kosaraju, Bavarian, Chen, Jun, Kaiser, +6); 2021-10-27; abstract (8.5K high-quality diverse grade-school problems; largest transformers fail; training verifiers to solve math word problems) | abstract-read | 2026-10-23 |
| [R2] | https://github.com/openai/grade-school-math (LICENSE, master branch) | MIT License, copyright (c) 2021 OpenAI | page-inspected (direct read) | 2026-10-23 |
| [R3] | https://huggingface.co/api/datasets/openai/gsm8k + https://datasets-server.huggingface.co/size?dataset=openai/gsm8k | license tag mit; arXiv tag 2110.14168; 2,000 likes; 986,952 downloads; main train 7,473 / test 1,319; socratic train 7,473 / test 1,319 | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the solution-verification protocol, the
contractor authorship claims, per-difficulty breakdowns, and the
paper's verifier-model results — pending the full-text read.
