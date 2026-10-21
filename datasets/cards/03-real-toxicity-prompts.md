# Dataset card: RealToxicityPrompts

apache-2.0 (HF page license tag [R1]) · verification date 2026-10-21 ·
prepared by the course build · status: composition verified at
`page-inspected` level

## 1. Identity and provenance

- **What it is:** a corpus of sentence-level *prompts with toxicity scores*,
  built so that the toxicity of model continuations can be attributed to the
  prompt's own toxicity region — the canonical dataset for asking "does a
  toxic-seeded prompt elicit toxic continuation?"
- **Canonical hosting inspected:** Hugging Face `allenai/real-toxicity-prompts`
  [R1]. Paper: arXiv:2009.11462, linked from the page [R1]. The scoring
  backend used by the original authors (the Perspective API) is
  **paper-level knowledge, not re-verified this round**.
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified [R1])

- **99.4k rows in the default subset** [R1].
- **Fields include toxicity scores across eight subcategories** observed on
  the page: threat, insult, severe_toxicity, toxicity, profanity,
  sexually_explicit, identity_attack, flirtation [R1]. This
  multi-dimensional score structure is what makes the dataset more useful
  than a binary "toxic / not" label: different subcategories support
  different constructs (Ch.02 uses identity_attack vs insult as the example
  of construct drift).
- Content: real web-text-derived prompts, a fraction of which contain toxic
  language by construction. Not redistributed here.

## 3. Collection and labeling

- Original construction (prompts sampled from web text corpora spanning
  four domains, split by the toxicity score of the prompt's continuation
  region): **paper-level, pending full-text verification**.
- Score provenance: the eight scores on the page [R1] are attributes of the
  shipped dataset; *who/what produced them* (automated toxicity classifier
  API) is paper-level knowledge — treat "labels are machine scores, not human
  judgments" as the working assumption until the paper is read, and note
  that this matters: classifier-labeled benchmarks inherit the classifier's
  biases (Ch.02 case study).

## 4. Splits and leakage discipline

- The inspected page showed a default subset without split semantics [R1];
  the original paper's toxic/non-toxic prompt-continuation design is
  paper-level. Course discipline: treat as evaluation-only; any scorer
  trained on top of these scores must be fit on a documented, disjoint
  sample.

## 5. Uses and known misuse

- **Measures well:** conditional toxicity of continuations across prompt
  toxicity regions, at scale (~99.4k rows).
- **Known misuse patterns:** (a) reporting a single "toxicity" aggregate and
  ignoring the eight subcategory scores; (b) treating the machine scores as
  ground truth for human-perceived toxicity; (c) using free-form generated
  continuations scored by a *different* classifier version than the
  dataset's — version skew makes cross-paper numbers incomparable (Ch.15
  red-teaming metric discussion).

## 6. What this dataset CANNOT support

- Claims about *causal* harm of toxic outputs; it measures propensity under
  continuation, not downstream impact on readers.
- Chat-assistant refusal behavior: prompts are completion-style.
- Multilingual toxicity claims: inspected page shows English data.
- Any claim that "non-toxic prompts produce non-toxic continuations" — the
  dataset's own purpose was to show the propensity structure is more
  complicated than that.

## 7. Maintenance

- Upstream cadence not determined this round. P09 usage must pin the HF
  revision; any project scorer must be versioned alongside.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/allenai/real-toxicity-prompts | license tag (apache-2.0); 99.4k rows (default subset); the eight toxicity subcategory field names; arXiv 2009.11462 | page-inspected | 2026-10-21 |

Explicitly **not** claimed: Perspective API scoring method, four-source
corpus composition, original split design — pending the full-text read of
arXiv:2009.11462.
