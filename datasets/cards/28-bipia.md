# Dataset card: BIPIA

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open

## 1. Identity and provenance

- **What it is:** the abstract's firstness claim — "the first benchmark
  for indirect prompt injection attacks" — for the Copilot-shaped
  threat: LLMs integrated with external content "have enabled
  applications such as Microsoft Copilot but also introduced
  vulnerabilities," where embedded malicious instructions "manipulate
  LLM outputs, causing deviations from user expectations."
- **Canonical home:** "Benchmarking and Defending Against Indirect
  Prompt Injection Attacks on Large Language Models" (Jiao et al.,
  arXiv:2312.14197, 2023-12-21, API-verified 2026-10-25); code and
  data released publicly.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes the benchmark's scope and the headline
  evaluation result: existing LLMs evaluated with BIPIA are
  "universally vulnerable" — the paper's own word, recorded here as
  its finding, with per-model magnitudes body-level and unclaimed.
- The paper also carries defenses (the title's "Defending Against"
  half); their evaluation against adaptive attacks is exactly where
  the course applies the note-35 discipline (defense claims need
  adaptive evaluation) — the card flags this pairing rather than
  treating the defense numbers as settled.

## 3. Collection and labeling

- Abstract-level: constructed injection scenarios across external
  content types (the Copilot integration class). The scenario
  taxonomy and labeling are body-level, unclaimed.
- The "universally vulnerable" finding's honesty condition: universal
  *susceptibility to the benchmark's scenario set*, not a bound on
  all possible injections — the same enumeration-vs-elimination
  distinction note 44's taxonomy enforces.

## 4. Splits and leakage discipline

- Not established at abstract level; course discipline identical to
  InjecAgent (card 27): shipped payloads are the floor, not the
  ceiling, of the attack space.

## 5. Where the course uses it

- **Ch. 14:** the integration-era IPI benchmark — paired with
  InjecAgent for scenario breadth and with note 06 (Greshake) for
  the founding threat model.
- **Ch. 19** (multimodal and embodied safety): the external-content
  framing extends naturally to multimodal content streams — the
  bridge citation for injection *beyond text*.
- **P07:** the second real-world candidate for the guard's evaluation
  tier, with the adaptive caveat shared across all injection
  benchmarks.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; composition counts and
  defense results unclaimed (abstract truncates mid-analysis —
  recorded). Firstness claims are dated (2023-12): later benchmarks
  exist; the card records the claim as the paper's, at its date.
