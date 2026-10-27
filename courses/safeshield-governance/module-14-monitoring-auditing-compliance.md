# Module 14 — AI monitoring, auditing, and compliance: the evidence loop that never closes

*Course companion note · [Safeshield AI Governance series](README.md) ·
video: [AI Monitoring, Auditing, and Compliance](https://www.youtube.com/watch?v=ZxxQg1Lcf_w) (50:33) · [playlist](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)*

## Where this module sits

The series closer: runtime monitoring, audit types
(first-party, second-party, third-party), compliance program
operation, and the continuous loop that keeps every prior module
honest over time.

## Core ideas, explained

### 1. Monitoring as governance's runtime

Static compliance decays: models drift, usage shifts, adversaries
adapt. The monitoring stack — behavioral metrics, drift alarms,
incident intake, override tracking — is what keeps the risk register
true after the audit leaves. The repo's
[Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md)
supplies the model-side monitoring mechanics; this module supplies
the organizational wrapper (who reads the dashboards, with what
authority to act).

### 2. Audit as a discipline with types

First-party (self-assessment — cheapest, weakest), second-party
(customer or partner audit — contractual teeth), third-party
(certification or independent audit — strongest, slowest). The
module's key content: what makes an audit *meaningful* — independence,
stated criteria, evidence sampling, findings with severities, and
follow-up. The AI-audit literature's open problem (auditing systems
whose behavior is statistical and whose internals are opaque) is
presented honestly, with the evaluation-science frontier as the
boundary of current practice.

### 3. Compliance as the loop that funds itself

The series ends where enterprise governance always ends: compliance
is not a state but a cycle — monitor, audit, correct, re-document —
and the organizational test is whether the cycle survives its first
budget cut. The repo's maintenance file
([MAINTENANCE.md](../../MAINTENANCE.md)) makes the identical bet at
repository scale: truth that is not re-verified on a schedule is
not truth.

## Through-line to this repository's chapters

- [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) —
  runtime monitoring mechanics.
- [MAINTENANCE.md](../../MAINTENANCE.md) — the repo's own
  re-verification loop.
- [Ch. 23](../../chapters/23-governance-and-standards/README.md) —
  the compliance layer's full map.

## Honesty note

This is an original study companion written to the module's announced
topic (verified in the playlist fetch, 2026-10-27). The video itself was
not watched; no spoken content is transcribed or quoted. Where the
module's subject is a published standard or law, the companion
explains it from the published instrument — which is the primary
source this repository prefers anyway.
