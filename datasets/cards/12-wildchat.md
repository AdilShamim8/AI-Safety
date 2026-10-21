# Dataset card: WildChat

ODC-BY for the WildChat-1M release (license change effective 2024-06-26,
retroactive [R2]); other releases under Ai2 Impact License terms referenced
by the nontoxic variant [R3] · verification date 2026-10-21 · prepared by
the course build · status: three release pages verified at
`page-inspected` level

## 1. Identity and provenance

- **What it is:** **real, in-the-wild user–ChatGPT conversations**,
  collected by offering free assistant access in exchange for research
  consent — the closest public analogue to production traffic. For a safety
  curriculum it is simultaneously (a) the realest distribution shift test
  there is, (b) a privacy and consent case study, and (c) a license
  archaeology exercise.
- **Canonical hosting inspected (three releases):**
  - `allenai/WildChat` — 650K conversations [R1]
  - `allenai/WildChat-1M` — 1 million conversations [R2]
  - `allenai/WildChat-4.8M` — 3,199,860 conversations, non-toxic user
    inputs only, release dated Aug 11 2025 [R3]
- **Collection mechanism (page-verified sentence [R1]):** "We collected
  WildChat by offering online users free access to OpenAI's GPT-3.5" —
  the consent-for-access exchange is the provenance fact to remember.
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified)

- Three releases at three scales: **650K → 1M → 3,199,860 conversations**
  [R1, R2, R3] — the 4.8M-branded release contains 3.2M conversations
  (branding vs count discrepancy recorded verbatim [R3]).
- **The 4.8M release is filtered to non-toxic user inputs** [R3] — meaning
  the largest release is *not* the full distribution; safety analyses that
  need the toxic tail must use the earlier releases and their license
  terms.
- **License history (the worked example this catalog exists to teach):**
  the 1M release's license was **changed to ODC-BY on 2024-06-26,
  retroactively** [R2] (observed both on the dataset page and in the README
  commit trail, commit `7d6490e` [R2]); the nontoxic variant references the
  **Ai2 Impact License** (`impact-lr`) [R3]. Same project, multiple
  licenses, changing over time — any derived work must state which release
  under which license.

## 3. Collection and labeling

- Collection window and demographics: not visible at page level; pending
  the paper read (the project has a NeurIPS-stage paper — recorded at
  metadata-only level, not cited as fact).
- There is no human annotation layer at page level; the toxic/non-toxic
  split of releases implies an upstream filtering classifier whose method
  and threshold are pending verification — a scorer- provenance question,
  not a dataset defect.

## 4. Splits and leakage discipline

- Real traffic has *time* as its natural split axis; any course use (P09)
  must split temporally, never randomly, or train-test contamination is
  guaranteed (same users, same sessions, near-duplicate prompts).
- PII: real-user data may contain identifying content by construction;
  the course's rule is no re-identification attempts, aggregates only, and
  Ch.16 uses this dataset as its de-identification-limits case.

## 5. Uses and known misuse

- **Measures well (as material):** the actual distribution of user intents,
  styles, languages, and difficult cases that laboratory benchmarks miss.
- **Known misuse patterns:** (a) treating the 4.8M release as unfiltered
  truth (it is the non-toxic-filtered view [R3]); (b) quoting "1M
  conversations" without the license and date qualifiers; (c) any use that
  deanonymizes users — barred by the Impact-license tradition and by basic
  research ethics; (d) using conversations as *training* data without
  checking which release's license permits it.

## 6. What this dataset CANNOT support

- Model-vs-model preference claims (it is single-assistant traffic —
  contrast LMSYS Arena-style preference data).
- Toxicity-rate claims about "all real traffic" from the filtered release
  [R3].
- Any claim that lab benchmarks are *wrong* — WildChat shows they are
  *different distributions*, which is a shift argument, not a validity
  refutation (Ch.17's core distinction).

## 7. Maintenance

- Active multi-release project (2024-2025 releases observed [R1, R2, R3]);
  license changes are dated and public [R2]. Course projects pin release +
  license + date triple with every statistic.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/allenai/WildChat | 650K conversations; collection-method sentence (free GPT-3.5 access for online users) | page-inspected | 2026-10-21 |
| [R2] | https://huggingface.co/datasets/allenai/WildChat-1M | 1M conversations; license change to ODC-BY dated 2024-06-26, described as retroactive; README commit reference (7d6490e) | page-inspected | 2026-10-21 |
| [R3] | https://huggingface.co/datasets/allenai/WildChat-4.8M and https://huggingface.co/datasets/allenai/WildChat-nontoxic | 3,199,860 conversations in the 4.8M-branded release; non-toxic-only filter; release date Aug 11 2025; Ai2 Impact License reference on the nontoxic variant | page-inspected | 2026-10-21 |

Explicitly **not** claimed: paper venue, PII policy details, toxic-filter
classifier method, demographic composition — pending further verification.
