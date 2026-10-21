# Dataset card: Anthropic HH-RLHF

MIT (HF page license tag [R1]) · verification date 2026-10-21 · prepared by
the course build · status: composition verified at `page-inspected` level

## 1. Identity and provenance

- **What it is:** the preference corpus behind a production assistant's
  safety training: crowdsourced workers compared two model responses and
  chose the more helpful / less harmful one. It is the canonical real-world
  artifact for studying what human preference data actually looks like —
  including its red-teaming portion, where workers were asked to find ways
  to elicit harmful behavior.
- **Canonical hosting inspected:** Hugging Face `Anthropic/hh-rlhf` [R1].
  Paper: arXiv:2204.05862 [R1] (the "Helpful and Harmless" RLHF paper —
  title recorded at metadata-only level this round).
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified [R1])

- **169k total rows** — train 161k, test 8.55k [R1].
- **MIT license** [R1] — the most permissive license in this catalog; still
  not a redistribution invitation for a course repository (the content is
  assistant dialogue, some of it deliberately harmful in the red-team
  portion).
- Subset structure (helpful-base / harmless-base / red-team splits that the
  project is known for): the fetched page presented only a "default"
  aggregate view [R1] — the **subset names were not visible** in this
  session's fetch and are therefore recorded as pending, not as fact. This
  is exactly the kind of gap the card discipline exists to expose.

## 3. Collection and labeling

- Collection story (US-based crowdworkers, per-conversation preferences,
  red-team attempts kept as standalone data): paper-level knowledge,
  pending full-text read. Page-level facts: row counts and license only
  [R1].
- Preference labeling means each row encodes a *pairwise human judgment*
  under the workers' interpretation of helpful/harmless — the label-quality
  questions Ch.04/P04 assign (rater drift, ambiguity, coarse binary
  preference vs graded harm) all live here.

## 4. Splits and leakage discipline

- Single train/test split observed (161k/8.55k) [R1]. Leakage concern is
  conversational, not lexical: workers produce multi-turn sessions; if
  sessions can straddle the split, train-test contamination is structural.
  The course rule: verify session-level disjointness before any claim —
  and record that we have **not** verified it at this access level.

## 5. Uses and known misuse

- **Measures well (as material):** real preference data for training and
  auditing safety-tuning; red-team attempt structure for studying attack
  surface as it existed circa 2021-2022.
- **Known misuse patterns:** (a) treating "preferred by a crowdworker in
  2022" as ground-truth helpfulness/harmlessness — preference is a dated
  human judgment, not an oracle; (b) training on the red-team portion
  without its safety framing; (c) citing the corpus as evidence about
  current frontier-model behavior (it reflects the assistant generation it
  was collected against).

## 6. What this dataset CANNOT support

- Claims about *modern* model safety (its judgments target long-past model
  versions).
- Demographic representativeness of preferences (worker population
  details pending paper read; page level shows nothing).
- Toxicity or bias benchmarks: it is preference/red-team data, not scored
  evaluation items.
- License laundering of dialogue content: MIT covers the *data files*;
  generated content rights are a separate legal question the course flags
  rather than resolves.

## 7. Maintenance

- Page last-updated marker observed (May 2023) [R1] — treat as a stable
  historical corpus, not a living benchmark. P04 pins the HF revision.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/Anthropic/hh-rlhf | license tag (mit); 169k total rows; train 161k / test 8.55k; arXiv 2204.05862; "default" subset view (subset names not displayed); page update marker May 2023 | page-inspected | 2026-10-21 |

Explicitly **not** claimed: subset names (helpful-base, harmless-base,
red-team), worker protocol, paper title/authorship — pending the full-text
read of arXiv:2204.05862.
