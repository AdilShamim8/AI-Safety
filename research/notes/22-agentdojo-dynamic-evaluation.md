# Note: AgentDojo — the dynamic environment that prices agent defenses (2024)

Source: SRC-PAPER-055 · Access: **abstract-read** (arXiv v3 page +
NeurIPS 2024 D&B poster page, 2026-10-22) · Note level:
**abstract-level**.

## The actual problem

Chapter 13's hardest evaluation question: how do you test a DEFENSE
against prompt injection without fooling yourself? Static attack
suites go stale; single-agent demos conflate task failure with
security failure; and a defense that "wins" by refusing everything
scores perfectly on attack metrics while being undeployable. The
paper's answer is infrastructure, not a benchmark: a *dynamic*
environment where attacks and defenses execute as code against a
simulated agent system with observable effects.

## Method (as the abstract establishes it)

An executable agent ecosystem — realistic tool sets and user tasks
plus an attack-injection mechanism — in which both attacks and
defenses can be deployed as arbitrary code. The environment facts
this course uses: 97 realistic tasks and 629 security test cases, with
agents evaluated on task success AND on security properties under
attack. Two headline findings from the abstract: state-of-the-art
LLMs fail many of the tasks even WITHOUT attacks (the competence
floor is lower than the deployment narrative assumes), and existing
prompt-injection attacks break some security properties but not all
(security is property-resolved, not binary).

## Results (abstract-level, honestly priced)

What the abstract does NOT give: per-model tables, the attack/defense
paradigm catalogue, and the environment's exact observability model —
all body-level and unread. What it does give is the structural lesson
the course's P07/P10 fixtures internalized: an agent-security
evaluation needs (a) tasks with executable ground truth, (b) attacks
whose success is a system event, not a string match, and (c) defenses
pluggable without rebuilding the world. The 97/629 counts are
environment facts — P07's 16 paired trials and P10's 9 held-out trials
are the course-scale miniature of exactly this shape.

## What this note does NOT claim

No reproduction, no body read, no per-model claims. The "fail many
tasks absent attacks" finding is quoted as an abstract statement about
the 2024 model set — dated, and the course prices it that way (the
competence floor moves with every model generation; the ENVIRONMENT
design is what transfers).

## Falsifiable extension

AgentDojo's missing instrument, from this course's perspective, is the
two-sided ledger as a first-class output: task-success and
security-success reported as a PAIR per configuration with intervals,
not as separate tables. Design: at course scale, extend the P10
harness with a third arm — a CaMeL-style flow-enforcing layer
(SRC-PAPER-054) over the same atlas-v2 matrix and held-out scenarios —
and report the full 2x2 (task x security) per arm with Wilson
intervals at n=9. Stopping rule: if the flow-layer arm's benign
completion falls below the monitor arm's 1/4 (P10's pinned floor
failure), the capability layer's utility price at THIS scale is worse
than the monitor's, and the "design beats training" ordering reverses
at small n — a real finding about scale, not about paradigms.

## My interpretation vs. their claims

Their claims: (1) dynamic environments beat static suites for
agent-security evaluation; (2) competence is the floor problem;
(3) security decomposes into properties. My reading: (1) is the
durable contribution — the environment IS the instrument, and its
97/629 shape is why this course's fixtures carry checksums, scripted
traces, and executable attack-success events rather than prose
scenarios; (2) is the most under-cited sentence in the agent-security
literature — every deployment debate assumes the competence floor is
handled, and the abstract says it is not; (3) "breaks some properties
but not all" is the vocabulary P07's R1-R4 policy rows implement
directly — per-rule fire counts instead of one ASR number.
