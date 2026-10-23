# Dataset card: Winogender Schemas

MIT (canonical repository LICENSE, read directly) · verification date
2026-10-23 · prepared by the course build · status: paper verified at
`abstract-read` level; canonical README read directly with the
composition arithmetic stated

## 1. Identity and provenance

- **What it is:** a diagnostic set of **Winograd-schema-style minimal
  pair sentences that differ only by the gender of one pronoun**,
  designed to test for gender bias in automated coreference resolution.
  The bias probe is structural: if a system resolves the pronoun
  differently as the gender changes, the occupational-stereotype
  association is doing work.
- **Canonical home:** `github.com/rudinger/winogender-schemas` (master
  branch, LICENSE read directly 2026-10-23: MIT, copyright (c) 2018
  Rachel Rudinger) [R2]; Hugging Face hosting `oskarvanderwal/
  winogender` (MIT tag, 1,489 downloads at inspection) [R3]. Paper: the
  arXiv record under 1804.09301, 2018-04-25 [R1].
- **Authors (abstract-verified [R1]):** Rachel Rudinger, Jason
  Naradowsky, Brian Leonard, Benjamin Van Durme (Johns Hopkins).
- **How WE obtained it:** abstract read + repository README/LICENSE
  reads + HF API page inspection on 2026-10-23; no sentence content
  downloaded or redistributed.

## 2. Composition (README-verified)

- **120 templates — 60 occupations, two templates per occupation**
  [R2]; each template has three mentions: an OCCUPATION, a
  PARTICIPANT, and a PRONOUN coreferent with either the occupation or
  the participant [R2].
- Fully instantiated: **720 sentences** = 120 templates x {female,
  male, neutral} x {participant, "someone"} [R2]; files
  `data/templates.tsv` and `data/all_sentences.tsv` [R2]. The
  arithmetic is stated in the README itself and cross-checks
  (120 x 3 x 2 = 720).

## 3. Collection and labeling

- Templates were authored by the paper's authors (schema-style
  construction, not crowdsourced at scale); the abstract reports the
  paper **evaluated and confirmed systematic gender bias in three
  publicly-available coreference resolution systems** and **correlated
  this bias with real-world and textual gender statistics** [R1].
- The README carries the paper's own interpretation rule, quoted for
  the course's construct-validity drill: the schemas have **high
  positive predictive value and low negative predictive value** — they
  may demonstrate the *presence* of gender bias, not prove its
  *absence* [R2].

## 4. Splits and leakage discipline

- A single fixed diagnostic set (no train split). Contamination: tiny,
  public, and famous since 2018 — assume exposure for post-2018
  systems; use as a probe, not a leaderboard.

## 5. Uses and known misuse

- **Measures well:** the pronoun-gender sensitivity of coreference (or
  of any system consuming the sentences) with a clean control (the
  "someone" bleached-referent arm).
- **Does not measure:** overall fairness of a deployed system;
  bias beyond gender/occupation associations; harms of downstream
  decisions.
- Known misuse: treating a pass on Winogender as proof of no gender
  bias — directly contradicted by the authors' PPV statement [R2].

## 6. What this dataset cannot support

- Population-level claims about occupations (the 60-occupation list is
  a curated instrument, not a sample).
- Modern-LLM chat-assistant claims without re-instrumentation (the
  original probe targets coreference systems).
- Statistical power claims — at 120 templates, per-occupation analysis
  is n=2 by construction.

## 7. Maintenance

- License: MIT (canonical LICENSE [R2]; HF hosting tag agrees [R3]).

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/1804.09301 (via arXiv API) | authors (Rudinger, Naradowsky, Leonard, Van Durme); 2018-04-25; abstract (Winograd schema-style minimal pairs differing by pronoun gender; systematic gender bias confirmed in three public coreference systems; correlation with real-world and textual gender statistics) | abstract-read | 2026-10-23 |
| [R2] | https://github.com/rudinger/winogender-schemas (README.md + LICENSE, master branch) | 120 templates (60 occupations x 2); 720 sentences arithmetic (x {female, male, neutral} x {participant, someone}); data file names; the PPV/NPV interpretation quote; MIT license text (c) 2018 Rachel Rudinger | page-inspected (direct read) | 2026-10-23 |
| [R3] | https://huggingface.co/api/datasets/oskarvanderwal/winogender | license tag mit; 1,489 downloads; last modified 2024-03-07 | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the three evaluated systems' identities and
scores, the real-world statistics used for correlation, and the
authoring protocol details — all pending the full-text read.
