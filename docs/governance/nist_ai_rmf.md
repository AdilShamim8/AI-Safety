# NIST AI Risk Management Framework (AI RMF)

The **NIST AI RMF 1.0** (released January 26, 2023) is the de facto risk
management vocabulary for US AI governance — voluntary, but adopted by
agencies (it underpins the US federal AI guidance lineage), referenced by
state laws, and structurally copied worldwide. For engineers its value
is concrete: it tells you *what artifacts to produce* (maps, profiles,
measurement records) so "we manage AI risk" is an auditable claim.

## Structure: four core functions

| Function | Question | Typical artifacts |
|----------|----------|-------------------|
| **GOVERN** | Who is accountable, with what authority and culture? | AI policy, roles (AI risk officer), risk tolerance statement, incident process |
| **MAP** | What is this system, in what context, who is affected? | System card, context-of-use doc, stakeholder & impact inventory, risk register entries |
| **MEASURE** | What do the metrics actually show? | Eval results (bias, validity, robustness), telemetry plan, test records — *this repo's `benchmarks/` output feeds this directly* |
| **MANAGE** | What do we do about it? | Response plans, mitigation records, monitoring thresholds, change-management trail |

Plus **Profiles** (sector/application-specific overlays) and the
**Generative AI Profile (NIST AI 600-1, July 2024)** — the essential
companion for LLM work.

## The Generative AI Profile's 12 risk categories

NIST AI 600-1 names them explicitly; every LLM deployment should be able
to state its posture on each:

1. CBRN information accessibility
2. Confabulation (hallucination)
3. Dangerous, discriminatory, or illegal action
4. Data privacy & leakage
5. Environmental impacts
6. Harmful bias & homogenization
7. Human-AI configuration (over-/under-reliance)
8. Information integrity (disinformation, synthetic media)
9. Information security
10. Intellectual property
11. Obscenity, profanity, hate & toxicity
12. Value-chain risks (supplier, provenance, data consent)

For each, the profile lists specific controls and references the research
base — and notably it cross-references the measurement instruments
(benchmarks) a lab should run, which is precisely what this repository's
harness section operationalizes for the open ecosystem.

## How to actually use it (an engineering workflow)

1. **Adopt the vocabulary** in design docs: risks are *mapped*, functions
   are *govern/map/measure/manage*. This alone aligns you with every US
   procurement-style review that shows up in 2025+ state law.
2. **Write a mini-profile** for your system: 2–3 pages: context, affected
   users, the 12 GAI categories with your status on each ("measured via
   TruthfulQA harness v0.3 on YYYY-MM-DD; result: ...").
3. **Wire MEASURE to your CI**: eval harnesses that run on every model /
   prompt-template change and write structured results (the repo's
   `scripts/run_benchmark.py` emits exactly this record shape).
4. **Version everything**: AI RMF reviews are evidence audits; artifacts
   without versions don't count (see the repo's citation-first
   documentation policy).

## Related NIST instruments

- **AI RMF Playbook** — the operational companion (now community-updated).
- **NIST AI 100-1** (Risk classification); **AI 600-1** (GenAI profile).
- **NIST SP 800-218A?** — no: the correct neighbor is the **NIST AI Safety
  Institute** (est. Nov 2023; renamed Center for AI Standards and
  Innovation, 2025), which coordinates pre-deployment testing with labs.
- **US AI safety legislation trajectory**: EO 14110 (Oct 2023) → rescinded
  (Jan 2025) → state-level statutes (California SB 53, 2025) — see
  [frameworks_timeline.md](frameworks_timeline.md).

## Comparison with neighbors

| | NIST AI RMF | EU AI Act | ISO/IEC 42001 |
|--|-------------|-----------|----------------|
| Legal force | Voluntary | Binding regulation | Certifiable standard (voluntary) |
| Approach | Process framework | Product bans + duties by risk class | Management system (PDCA) |
| Best for | US-market readiness, engineering structure | EU market access | Demonstrable internal governance |
| Length | ~48pp + profiles | 140k+ words | ~40pp + audit |

Organizations serving multiple jurisdictions typically implement ISO
42001 *as* the management system, populate it with NIST-RMF-style
artifacts, and file EU-AI-Act conformity outputs from the same evidence
base — one measurement layer, three reporting surfaces. This repo's
benchmark output schema is designed to slot into that pattern.
