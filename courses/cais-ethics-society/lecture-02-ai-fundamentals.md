# Lecture 2 — AI fundamentals: just enough machine to reason about

*Course companion note · [AI Safety, Ethics, & Society](README.md) ·
video: [Lecture 2 | AI Safety, Ethics, & Society: AI Fundamentals](https://www.youtube.com/watch?v=tWV3wdY2870) (52:04) · [playlist](https://www.youtube.com/playlist?list=PLXSn3Zz2ayT7ab7I12PBYVt0244369S1q) ·
[textbook](https://www.aisafetybook.com)*

## Where this lecture sits

The technical primer: how modern AI systems are
built and why their four signature properties — correlational,
opaque, brittle, unpredictable — generate the risk landscape the rest
of the course surveys.

## Core ideas, explained

### 1. The four properties as a risk-generating stack

The textbook's framing (correlational not causal; opaque;
brittle; unpredictable) is the cleanest non-technical account of why
ML behaves differently from software: the system's "program" is
statistical regularity mined from data, so it inherits the data's
correlations without its causes, cannot be read as code, fails
outside its distribution, and surprises even its builders. Every
later lecture's risks are these four properties meeting
deployment. The repo's prerequisites layer covers the same ground
with equations; this lecture is the no-equations version.

### 2. Why "just add more data" is a risk claim

Scaling as the field's default improvement mechanism means the
data's composition is the safety-critical substrate — provenance,
consent, and distributional coverage become safety properties, which
is why [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md)
treats data supply chains as a first-class chapter.

### 3. The transparency deficit, stated honestly

The opacity property sets up the course's later interpretability
needs without over-promising: current transparency tools explain
*some* decisions *approximately*, which is better than nothing and
not the same as understanding. The repo's interpretability arc
(Ch. 09–11) is the technical version of the same honesty.

## Through-line to this repository's chapters

- [prerequisites/](../../prerequisites/diagnostic.md) — the repo's
  own on-ramp with the math the course deliberately skips.
- [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md) —
  the interpretability answer at depth.

## Honesty note

This is an original study companion written to the lecture's announced
topic (verified in the playlist fetch, 2026-10-27, and corroborated by the
textbook's published chapter structure). The video itself was not
watched; no spoken content is transcribed or quoted, and no textbook
text is reproduced. Where an idea below is also carried by a source
this repository registers, the register ID appears and the source is
linked.
