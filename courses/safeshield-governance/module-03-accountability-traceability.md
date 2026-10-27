# Module 3 — Accountability and traceability: who answers, and how we reconstruct why

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [Accountability and Traceability in AI Systems](https://www.youtube.com/watch?v=sgRDWssuPz0) (51:53) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The accountability module: responsibility allocation
across the AI supply chain, and the traceability infrastructure
(logging, provenance, audit trails) that makes responsibility
answerable in fact rather than in principle.

## Core ideas, explained

### 1. Responsibility gaps and how law closes them

The classic problem: harm occurs, and every party points at another
— the provider at the deployer's misuse, the deployer at the
provider's opacity, the data source at both. The closures in current
law: duty allocations (the EU AI Act's provider/deployer split),
product liability's presumptions, and sectoral duties of care. The
module teaches the map because an auditor's first question is always
"whose duty was this?"

### 2. Traceability as reconstruction capability

Accountability is only as good as the evidence: versioned model and
data lineage, decision logs, evaluation records, human-override
records. The engineering requirement is a time-travel query — given
a decision last March, reconstruct the model, prompt, data, and
policy versions that produced it. That is exactly the provenance
discipline the repo's
[Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md)
teaches technically, and the incident notes exercise repeatedly.

### 3. The audit trail as the unit of governance

An unlogged decision is an ungoverned decision. The module's
practical output: the log schema (who, what, when, which version,
what evidence, what override) that turns organizational memory into
audit evidence — and the retention policy that keeps it alive long
enough to matter.

## Through-line to this repository's chapters

- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) —
  provenance and supply-chain discipline.
- [research/notes/incidents/README.md](../../research/notes/incidents/README.md) —
  incident reconstruction as the practiced skill.

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
