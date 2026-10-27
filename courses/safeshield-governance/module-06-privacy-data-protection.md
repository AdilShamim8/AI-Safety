# Module 6 — Privacy and data protection: from data minimization to machine unlearning

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [Privacy and Data Protection in AI Systems](https://www.youtube.com/watch?v=3vgHshL9m94) (49:32) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The privacy module: the GDPR-class principles
(lawful basis, purpose limitation, minimization), AI-specific
frictions (training vs. erasure), and the technical toolbox
(de-identification, differential privacy, federated learning,
unlearning).

## Core ideas, explained

### 1. The principles meet the technology

Data protection's principles assume record-oriented systems; LLM
training does not fit: purposes are discovered post-hoc, data is
mixed at scale, and "erasure" of one person's contribution from a
trained weight matrix is not a database delete. The module maps each
principle to its AI-era friction — the map regulators themselves are
working through.

### 2. The extraction problem

The repo's own spine carries the canonical evidence (the
Scalable-Extraction paper on the Harvard course's reading list):
aligned deployment does not prevent training-data extraction —
memorization is a measurable property with a known attack surface.
Privacy compliance for ML therefore needs memorization measurement,
not just data-processing paperwork. The repo's
[Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md)
carries the full treatment.

### 3. The toolbox, priced honestly

Differential privacy (calibrated noise; utility cost), federated
learning (movement of data stops, model updates still leak),
de-identification (always reversible at scale), unlearning (an
active research field, not a service you can buy). The module's
practical lesson: privacy claims should state the technique, the
budget, and the residual risk — which is precisely how the repo
requires dataset cards to speak.

## Through-line to this repository's chapters

- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) —
  the privacy chapter, including extraction.
- [research/notes/14-model-extraction.md](../../research/notes/14-model-extraction.md)
  and [research/notes/57-extracting-training-data.md](../../research/notes/57-extracting-training-data.md) —
  the extraction evidence base.

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
