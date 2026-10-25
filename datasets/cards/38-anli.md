# Dataset card: Adversarial NLI (ANLI)

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a large-scale natural-language-inference benchmark
  collected by an **iterative, adversarial human-and-model-in-the-loop
  procedure** — non-expert annotators attacking model weaknesses
  round by round. The abstract's two-sided finding: training on it
  yields state-of-the-art performance on standard NLI benchmarks
  while its own test set "posing a more difficult challenge," and
  the analysis shows non-expert annotators "are successful at
  finding their weaknes[ses]" (truncation recorded).
- **Canonical home:** "Adversarial NLI: A New Benchmark for Natural
  Language Understanding" (Nie et al., arXiv:1910.14599,
  2019-10-31, API-verified 2026-10-25).

## 2. Composition (abstract-level)

- The adversarial-iteration design (rounds against a target model)
  and the two-sided result (transfer gains on standard sets; harder
  held-out challenge). Sizes and round counts: body-level,
  **unclaimed** — recorded as the limit.

## 3. Collection and labeling

- Non-expert annotators, adversarial instructions — the supply
  strategy [comparison 12](../../research/notes/comparison-12-evaluation-supply-strategies.md)
  files as adversarial-human (DynaHate's family, earlier and in
  NLI). The key transferable finding: adversarial selection does
  not require expert annotators to find model weaknesses.

## 4. Splits and leakage discipline

- Round-structured collection; standard contamination caveats
  apply for any modern use (the set is in training corpora by now —
  the honest note every old benchmark card carries).

## 5. Where the course uses it

- **Ch. 02:** the pre-LLM canonical case for human-and-model-in-the-
  loop evaluation — the design lineage that Dynabench and DynaHate
  industrialized ([note 60](../../research/notes/60-dynabench-dynamic-benchmarking.md)'s
  ancestors).
- **P01:** the harness's adversarial-case-generation rationale —
  annotators-as-attackers as the original template.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; sizes and rounds unclaimed;
  the SOTA claim is 2019-scoped (recorded with its date, not as a
  standing fact).
