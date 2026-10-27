# Module 4 — Transparency and explainability: disclosure architecture and honest limits

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [Transparency and Explainability in AI systems](https://www.youtube.com/watch?v=eJ3wJEk9Fbs) (44:23) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The transparency module: the disclosure stack
(system cards, model cards, usage instructions, decision notices)
and the explainability toolbox (post-hoc explanation, interpretability)
with their honest limits.

## Core ideas, explained

### 1. Transparency is a stack, not a bit

The module organizes the disclosure obligations: transparency about
*the system* (documentation: what it does, limits, evaluation
results), transparency *in the interaction* (the user knows they face
an AI — the deepfake-disclosure class of duties), and transparency
*about the decision* (meaningful information about logic involved —
GDPR Article 22's lineage). Each layer has different legal force and
different failure modes.

### 2. Explainability's two channels and their limits

Post-hoc explanation (feature attribution, surrogate models) tells
you what correlated; mechanistic interpretability tells you what the
system computes. Both are partial — and the module's honest move is
to teach the limits as first-class content: explanations can be
unfaithful (the repo carries the unfaithful-explanations literature
in its notes), and disclosure can be gamed (the 500-page system card
as secrecy). The repo's
[Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md)
is the technical depth here.

### 3. Documentation as the deliverable

The practitioner's actual artifact: the model/system card with
intended use, out-of-scope uses, evaluation evidence, and known
limitations — the format the repo's dataset cards follow and its
templates make explicit. Writing one well is the fastest way to
discover how little you know about your own system.

## Through-line to this repository's chapters

- [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) —
  faithfulness and its limits.
- [Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md) —
  interpretability evaluation (when explanations are good enough).
- [research/notes/38-unfaithful-explanations.md](../../research/notes/38-unfaithful-explanations.md) —
  the limits, with evidence.

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
