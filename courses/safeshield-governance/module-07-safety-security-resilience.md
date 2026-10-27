# Module 7 — Safety, security, and resilience: the S-word triad in governance terms

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [Safety, Security, and Resilience in AI Systems](https://www.youtube.com/watch?v=EEdL-HSvHkk) (40:49) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The triad module: safety (the system behaves within
limits), security (adversaries cannot bend it), resilience (it
absorbs shocks and recovers) — as governance obligations with
engineering counterparts.

## Core ideas, explained

### 1. Three properties, three disciplines

The module's definitional work: safety is about the system's own
behavior (the failure-mode discipline the repo's whole middle arc
teaches); security is about intelligent adversaries (the red-team
and adversarial-ML chapters); resilience is about the system-of-
systems surviving what the first two miss (cascades, recovery,
graceful degradation). Conflating them produces compliance programs
that audit one and ship the others.

### 2. Resilience as the governance layer's favorite word — earned

Resilience earns its place only with specifics: redundancy in the
dependency graph, circuit breakers, rollback paths, incident
response with rehearsed roles, and degradation modes that fail
loudly instead of confidently. The NIST AI RMF's "Manage" function
(see the module on it in this series) is largely this content
reorganized; aviation's safety culture is the historical template
(the CAIS course's safety-engineering lecture, in this library,
teaches the same lineage accessibly).

### 3. Security's supply-chain turn

Modern AI security includes the pipeline: weights, data, and
dependencies as stealable/poisonable assets. The repo's Ch. 12–14
arc is the technical depth; the governance question the module adds
is who owns which supply-chain risk — the answer the ISO 42001
management system (next modules) formalizes.

## Through-line to this repository's chapters

- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) —
  the security/robustness technical layer.
- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) —
  the assurance discipline.
- [courses/cais-ethics-society/lecture-04-safety-engineering.md](../cais-ethics-society/lecture-04-safety-engineering.md) —
  the accessible lineage of the same ideas.

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
