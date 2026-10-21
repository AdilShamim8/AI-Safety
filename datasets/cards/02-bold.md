# Dataset card: BOLD (Bias in Open-Ended Language Generation)

CC BY-SA 4.0 (license sentence displayed on the HF page [R1]) · verification
date 2026-10-21 · prepared by the course build · status: composition verified
at `page-inspected` level

## 1. Identity and provenance

- **What it is:** a prompt set for measuring *bias and toxicity in open-ended
  generation*: each prompt seeds a generation with identity-linked content
  (a profession, a gendered or racialized person reference, a religion, a
  political ideology) so that differences in model continuations across
  sub-groups can be measured with sentiment and toxicity/regard scorers.
- **Canonical hosting inspected:** Hugging Face `AmazonScience/bold` [R1].
  Paper: "BOLD: Dataset and Metrics for Measuring Biases in Open-Ended
  Language Generation", arXiv:2101.11718, with an ACM publication listed on
  the page [R1].
- **Authorship note (important for provenance literacy):** the paper authors
  are Salesforce researchers (Dhamala et al.) — this is **paper-level
  knowledge not re-verified this round**; what is *page-verified* is that the
  dataset is hosted under the `AmazonScience` HF organization. Hosting org ≠
  author org: a real provenance trap that this card teaches by example.
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified numbers [R1])

- **23,679 text-generation prompts** in total, across five domains:
  - Profession — 18 sub-groups, 10,195 prompts
  - Gender — 2 sub-groups, 3,204 prompts
  - Race — 4 sub-groups, 7,657 prompts
  - Religious ideologies — 7 sub-groups, 639 prompts
  - Political ideologies — 12 sub-groups, 1,984 prompts
- The sub-group structure is the pedagogically valuable part: bias metrics
  are computed **within domain across sub-groups**, and the sub-group sizes
  are wildly imbalanced (639 religious prompts vs 10,195 profession prompts),
  which directly affects the statistical power of any disparity claim — a
  Ch.02 worked example.

## 3. Collection and labeling

- Collection method (prompts sampled from Wikipedia text at sub-group-linked
  positions): **paper-level description, pending full-text verification**;
  not claimed as verified here.
- No human labeling of outputs is part of the dataset itself; labels/scores
  are produced by downstream scorers applied to generations.

## 4. Splits and leakage discipline

- The inspected page presented the prompt set without train/test split
  semantics [R1]; the course treats every BOLD evaluation as a *fresh
  generation task* (no fitting on prompts), making classic label leakage less
  of a concern than scorer leakage: any toxicity or sentiment scorer used on
  continuations must itself be validated and versioned (Ch.02, P01).

## 5. Uses and known misuse

- **Measures well:** relative differences in generation quality across
  identity sub-groups within a domain, under a controlled prompt form.
- **Known misuse patterns:** (a) averaging disparity across domains with
  different sub-group counts and prompt forms; (b) reporting sentiment gaps
  without the confidence intervals the imbalanced sub-group sizes demand
  (religion has 639 prompts total); (c) treating BOLD prompts as
  representative of user traffic — they are Wikipedia-seeded, not
  user-derived.

## 6. What this dataset CANNOT support

- Claims about *chat* behavior or instruction-following bias: prompts are
  completion-style, pre-chat-era.
- Causal claims that a model "is biased against group X" from generation
  disparities alone — the construct measured is *conditional generation
  statistics*, not intent or downstream harm.
- Non-English bias: English-only as inspected.
- Toxicity *propensity* claims without a fixed scorer, decoding parameters,
  and seed control — the dataset provides prompts, not toxicity labels
  (contrast RealToxicityPrompts, which ships scored prompts).

## 7. Maintenance

- Upstream cadence not determined this round. Course projects (P09) must pin
  the HF revision and record scorer versions with their results.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/AmazonScience/bold | license sentence (Creative Commons Attribution Share Alike 4.0 International); 23,679 prompts; per-domain sub-group counts and prompt counts (Profession 18/10,195; Gender 2/3,204; Race 4/7,657; Religious 7/639; Political 12/1,984); task (text generation); arXiv 2101.11718 + ACM publication link | page-inspected | 2026-10-21 |

Explicitly **not** claimed: Wikipedia sourcing method, author names,
sentiment/regard metric definitions, FAccT venue — pending full-text read of
arXiv:2101.11718.
