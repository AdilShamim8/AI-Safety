# Note: CheckList — behavioral testing comes to NLP (2020)

Source: SRC-PAPER-134 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Held-out accuracy "often overestimates the performance of NLP
models" — the abstract's diagnosis, and the evaluation era's open
secret. The paper's move: import **behavioral testing from software
engineering**. CheckList is a task-agnostic methodology built from
two structures: a **matrix of general linguistic capabilities ×
test types** (the ideation grid — what to test, organized) and a
software tool to generate large, diverse test cases from it
(template-driven, largely model-free generation).

The SE analogy is the course's favorite part: software does not
ship on "the test suite passes at 94%"; it ships on unit, edge, and
behavioral coverage of *named* behaviors. CheckList brings that
grammar to models: capability (sentiment, negation, temporal
reasoning…) × test type (minimum functionality, invariance,
directional expectation) = a coverage claim with named cells, not
a single accuracy number.

## What the abstract establishes

1. The overestimation diagnosis for held-out accuracy.
2. The methodology: capability × test-type matrix + generation
   tool, task-agnostic.
3. That commercial and research models "failed on many important
   behaviors" when tested this way (the abstract's empirical
   payload — magnitudes body-level, unclaimed).

Unclaimed: per-model failure rates, the specific capability
breakdowns, and the tool's generation mechanics.

## Why this note exists in the course

1. **Ch. 02's testing grammar.** The chapter's evaluation design
   unit now has its SE-bridge citation: the course's
   capability-slice reporting and P01's case-family structure are
   CheckList-shaped (named behaviors, per-cell ledgers, paired
   invariance arms — P09's perturbation audits are invariance
   tests with Wilson intervals).
2. **The invariance test as the fairness instrument.** Directional
   expectations and invariance tests are exactly how
   [CrowS-Pairs (card 19)](../../datasets/cards/19-crows-pairs.md)-style
   perturbation audits work; CheckList is the general grammar the
   fairness datasets instantiate.
3. **The overestimation lineage.** Note 41 (model-written evals),
   note 49 (HELM), and this note form Ch. 02's evaluation-adequacy
   trio: generation for breadth, coverage with named holes, and
   behavioral testing for capability-level claims. Each answers a
   different failure of the single-number era.

## What this note does NOT claim

No claim that CheckList cells transfer unmodified to LLM-era chat
behaviors (the paper predates them; the grammar transfers, the
capability lists need rebuilding — the course says so); no numbers.

## The falsifiable extension (deterministic tier)

P01's harness can implement the matrix directly:

- Define three capability cells (e.g., numeric-currency conversion,
  negation handling, temporal ordering) × two test types (minimum
  functionality — does the behavior hold on minimal cases;
  invariance — does the score survive meaning-preserving
  perturbation).
- Generate cases per cell (the harness's template machinery);
  evaluate the scorer per cell with Wilson intervals; report the
  matrix, not a mean.
- Prediction worth testing: at least one cell fails while the
  aggregate accuracy stays high — the overestimation phenomenon,
  reproduced as a table the learner can hold.
- Falsifier: a uniformly-passing matrix at this tier bounds the
  demonstration (the organism's capabilities were too easy), which
  itself instructs cell design — recorded either way.
