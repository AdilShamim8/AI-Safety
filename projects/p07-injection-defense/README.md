# P07 — Injection defense as a capability audit

**Project status: `implemented`** (code + 41 dedicated tests, full
repository suite green; deterministic CPU-only paired runs over
synthetic scripted scenarios; no model calls, no network, no live
clients — the compute tier that would exercise a real agent runtime
is scoped below and honestly marked as not executed) · 2026-10-22 ·
chapter links: [Ch. 13 — LLM application
security](../../chapters/13-llm-application-security/README.md) and
[Ch. 14 — agents, tools, memory, and MCP
security](../../chapters/14-agent-tool-memory-mcp-security/README.md)


**Session-2 companion materials:** [jailbroken's two modes](../../research/notes/44-jailbroken-failure-modes.md) (classify your residual by mode), [many-shot](../../research/notes/45-many-shot-jailbreaking.md) (the compute-free family), [Llama Guard](../../research/notes/65-llama-guard-safeguard-model.md) (guard-is-a-model), [HotFlip](../../research/notes/73-hotflip.md) (the flip family), [InjecAgent](../../datasets/cards/27-injecagent.md)/[BIPIA](../../datasets/cards/28-bipia.md)/[AgentDojo](../../datasets/cards/30-agentdojo.md), [incident 07](../../research/notes/incidents/07-slack-ai-exfiltration.md) (your exfiltration pairs' real-world case), [C08](../../research/notes/comparison-08-jailbreak-modes-defense-families.md).
## The question this project answers

Can the audit discipline of Chapters 13-14 be *code* — and when it
is, what does a capability policy actually buy, measured honestly?

Concretely: build the privilege and trust-boundary matrix for a
realistic tool-bearing assistant; implement the R1-R4 capability
policy over provenance-tagged arguments (R1 exfiltration consent,
R2 argument integrity — W-tagged values may never fill capability
references, R3 provenance-at-write for store writes, R4 first-use
consent for irreversible tools); run paired arms — the same scripted
traces under full delegation (the confused deputy, deployed) and
under the policy — and price the difference with Wilson intervals,
discordant-pair ledgers, and exact one-sided sign tests.

And the sharper question the fixture is built to answer: *what does
the policy NOT stop?* Two residual attack classes are scripted on
purpose — the authored-policy gap (an undeclared
capability-reference argument walked straight through) and consent
decay (a socially-engineered human satisfying R1/R4 legitimately). A
defense whose fixture shows no residuals would be testing the wrong
thing.

## What landed in this repository

```text
projects/p07-injection-defense/
├── README.md                        (this file: protocol + usage)
├── cases/atlas-v2-matrix.yaml       15-tool privilege matrix (Ch. 14's
│                                    Atlas + exercise 14.1's CRM server),
│                                    checksum-pinned
├── cases/atlas-v2-scenarios.yaml    16 paired trials (8 attack, 8 benign),
│                                    checksum-pinned
├── configs/atlas-v2-paired-v1.yaml  the preregistered run (pinned
│                                    expectations below)
├── example-report.md                genuine output of that run (committed)
└── runs/                            local outputs (gitignored per policy)
src/ai_safety_course/agent_guard/
├── matrix.py     ToolSpec / PrivilegeMatrix: exfiltration pairs,
│                 authority gradient, store writers, fail-closed
│                 checksum-pinned loader, red-flag audit
├── policy.py     provenance tags (U/W/A), Argument/ToolCall,
│                 CapabilityPolicy with R1-R4 (R2/R3 hard-block;
│                 R1/R4 consent-gated), AllowAllPolicy (the arm that
│                 differs only in trusting the model)
├── scenarios.py  scripted traces with per-argument provenance,
│                 fail-closed loader
├── harness.py    paired arms, halt-on-block semantics, consent
│                 resolution by the scripted user
├── metrics.py    rates with Wilson intervals, discordant-pair
│                 ledgers, exact one-sided sign tests, rule fires
├── report.py     dated markdown reports, full provenance block,
│                 per-scenario trace appendix
└── runner.py     config-driven deterministic runner + CLI
tests/test_p07_agent_guard.py         41 deterministic tests (offline)
```

Repository data policy: `runs/` stays local and gitignored; the
committed `example-report.md` is the genuine output of the
preregistered run. All scenario content is synthetic and authored
for this course — no real attack payloads, no dataset content, no
product names beyond generic tool names.

## Usage

```bash
PYTHONPATH=src python -m ai_safety_course.agent_guard.runner \
    --config projects/p07-injection-defense/configs/atlas-v2-paired-v1.yaml
```

Outputs are byte-stable for a fixed configuration (verified:
regeneration is byte-identical). The runner is fail-closed: matrix
or scenario checksum drift aborts before any result is produced.

## The preregistered protocol

**H1 (defense effect).** The capability arm blocks the six
designed-blockable attack classes that all succeed under full
delegation. Pinned expectation: attack success 8/8 undefended → 2/8
capability; paired one-sided sign test p = 0.015625 (6 discordant
pairs, 0 regressions).

**H2 (utility cost).** The benign cost is exactly the unattended
automation flow: 8/8 → 7/8, with `benign-automated-report`
incomplete because no user answers the consent screen. The cost is
an interaction-timeout, not a capability failure.

**H3 (residuals are the documented policy limits, not surprises).**
The two attacks that succeed under the capability arm are
`attack-policy-gap-crm` (Ch. 14 §6's authored-policy gap: the
`value` argument of `crm.update` is a capability reference in
disguise, undeclared in the policy's table) and
`attack-consent-decay` (the human half: the user typed the planted
address themselves and approved the destination — R1/R4 satisfied by
social engineering). Both are scripted on purpose; a run in which
they *stop* succeeding means the fixture drifted, not that the
policy improved.

**Stopping and disconfirmation.** Any disagreement between a run and
the pinned expectations is a finding about the fixture or the code,
never a reason to re-run until the numbers look better. If the
`example-report.md` in the repository ever disagrees with a fresh
run over the same checksums, that is a bug report.

**Non-claims.** Nothing here measures deployed-agent attack
prevalence; the numbers are mechanism results over 16 synthetic
paired trials with wide Wilson intervals by design. R2 as authored
also blocks W-tagged link-following (a real utility cost of strict
argument integrity that this fixture does not exercise — recorded,
not hidden). R3 as authored covers `memory.write` only; the matrix
audit flags three store writers (`files.write`, `memory.write`,
`crm.update`) and the policy covers one — the uncovered two are
exactly where the residual CRM attack walks through.

## Compute tiers (honest scoping)

- **Tier 0 (this implementation):** deterministic offline paired runs
  over synthetic scripted scenarios — executed, committed, test-pinned.
- **Tier 1 (not executed):** a live agent runtime over the same matrix
  and policy, with a real model emitting real calls (AgentDojo-style
  harness integration), measuring attack success under adaptive attack
  construction rather than scripted payloads. Requires model access
  and a runtime; scoped, not built here.
- **Tier 2 (not executed):** human-in-the-loop consent-decay
  measurement (how often do users approve socially-engineered
  destinations?) — a behavioral experiment with IRB-level ethics
  review, far outside this repository's scope; the fixture models the
  mechanism, not the rate.
