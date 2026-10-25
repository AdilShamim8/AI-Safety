# Dataset card: MM-SafetyBench

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a benchmark for **safety evaluation of multimodal
  LLMs**, built on the abstract's core observation: MLLMs "can be
  easily compromised by **query-relevant images, as if the text
  query itself were malicious**" — the image channel carries the
  attack while the text stays benign. A comprehensive framework for
  safety-critical scenarios follows (the API record truncates into
  the taxonomy; recorded).
- **Canonical home:** "MM-SafetyBench: A Benchmark for Safety
  Evaluation of Multimodal Large Language Models" (Liu et al.,
  arXiv:2311.17600, 2023-11-29, API-verified 2026-10-25).

## 2. Composition (abstract-level)

- The query-relevant-image attack design and the
  safety-critical-scenario framework. Scenario counts and taxonomy
  detail: body-level, **unclaimed**.

## 3. Collection and labeling

- Constructed attack-image pairing — the same design grammar as
  FigStep (card 29) (typographic payloads) but
  generalized to **query-relevant imagery**: the image is not a
  text container but a semantic accomplice. The two cards together
  give Ch. 19 both multimodal attack families.

## 4. Splits and leakage discipline

- Standard discipline: constructed payloads are enumerable attack
  families; defenses evaluated against them need designed
  follow-ups before robustness claims (the standing
  adaptive-evaluation caveat).

## 5. Where the course uses it

- **Ch. 19:** the multimodal safety benchmark citation — pairing
  with FigStep as the two attack instruments, and with
  BIPIA (card 28) as the content-channel bridge.
- **P10:** the dossier's multimodal risk section gains its
  evaluation-tier candidate.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; scenario counts and taxonomy
  unclaimed (truncation recorded); no attack-success numbers
  claimed.
