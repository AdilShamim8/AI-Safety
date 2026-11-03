# CampusX — AI Security & Guardrails

**Navigate:** [← lecture library](../README.md) · [study plans](../study-plans.md) · [previous: DataCamp](../datacamp-ai-security-risk/README.md)

*The guardrails-engineering companion · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053) ·
[preview](https://learnwith.campusx.in/s/preview/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053-6ad0c6fb17f468ce3c894053) · 4 modules, 14 lessons (13 with published
durations totaling 330.47 minutes, 1 announced with duration
0), the outline marked TENTATIVE by the platform itself · verified
2026-11-03*

## What this course is

This is CampusX's practitioner course (Hinglish, paid — ₹1999 against
an MRP of ₹2499, 1095-day validity), and the sixth course in this
repository's lecture library. Where the five courses before it teach
the risk landscape and the concepts, this one builds the defenses:
two production-grade case studies secured layer by layer, end to end,
with the same repeatable five-step threat-modelling framework.

Its distinct evidential value in this library: it is the only course
that treats **guardrails engineering** as a construction discipline —
every component in a data flow examined through the capability lens
(what it can read, write, execute, or reach), every weak point closed
with its own named security layer, and the secured result red-teamed
with Promptfoo to grade which layers hold. The case studies are a
bank RAG (NovaBank — a RAG that works is not yet safe for a bank) and
a doctor-booking agent with tools, an MCP server, shared memory, and
no login (write and delete capabilities make an agent more dangerous
than a RAG: an attack no longer just changes an answer, it makes the
agent take real actions).

## The four-module arc

The structure runs from thesis to framework to two applications:

1. **Why Study AI Security?** — the thesis: applications built without
   security in mind are open to attack, and every added retriever,
   tool, and input channel is a new way in.
2. **AI Security & Challenges** — the structural differences from
   application security, the attack catalog, the toolbox, and the
   five-step threat-modelling framework.
3. **Threat Modelling our RAG Application** — the NovaBank case study:
   PII masking, pre-retrieval metadata filtering, input guardrails
   and delimiter defense, NeMo Guardrails output guardrails, and the
   Promptfoo red-team close.
4. **Threat Modelling our Agentic Application** — the doctor-booking
   agent: the jailbreak gate, the guard model on tool and MCP
   results, memory protection, and output guardrails.

## The complete lesson index

### Module 1 — Why Study AI Security?

| # | Lesson | Duration | Companion note |
|---|---|---|---|
| 1 | Why Study AI Security? | 27:59 | [m1-01-why-study-ai-security.md](m1-01-why-study-ai-security.md) |
| 2 | Why AI Security? | Practical Landscape | 22:58 | [m1-02-why-ai-security-practical-landscape.md](m1-02-why-ai-security-practical-landscape.md) |

### Module 2 — AI Security & Challenges

| # | Lesson | Duration | Companion note |
|---|---|---|---|
| 1 | AI Security & Challenges | 9:48 | [m2-01-ai-security-challenges.md](m2-01-ai-security-challenges.md) |
| 2 | Adversarial Attacks & Types | 8:46 | [m2-02-adversarial-attacks-and-types.md](m2-02-adversarial-attacks-and-types.md) |
| 3 | Tools Needed to Secure LLM Applications | 11:20 | [m2-03-tools-needed-to-secure-llm-applications.md](m2-03-tools-needed-to-secure-llm-applications.md) |
| 4 | Threat Modelling Framework | 11:49 | [m2-04-threat-modelling-framework.md](m2-04-threat-modelling-framework.md) |

### Module 3 — Threat Modelling our RAG Application

| # | Lesson | Duration | Companion note |
|---|---|---|---|
| 1 | Threat Modelling our RAG Application | 24:21 | [m3-01-threat-modelling-our-rag-application.md](m3-01-threat-modelling-our-rag-application.md) |
| 2 | Securing Vector Database - PII Leakage | 29:29 | [m3-02-securing-vector-database-pii-leakage.md](m3-02-securing-vector-database-pii-leakage.md) |
| 3 | Securing Retriever - Authentication and Authorization | 35:58 | [m3-03-securing-retriever-authentication-and-authorization.md](m3-03-securing-retriever-authentication-and-authorization.md) |
| 4 | Securing User Query and LLM - Jailbreak and Prompt Injection | 34:15 | [m3-04-securing-user-query-and-llm-jailbreak-and-prompt-injection.md](m3-04-securing-user-query-and-llm-jailbreak-and-prompt-injection.md) |
| 5 | Securing Output - Output Guardrails | 35:32 | [m3-05-securing-output-output-guardrails.md](m3-05-securing-output-output-guardrails.md) |
| 6 | Red Teaming our RAG Application | 44:04 | [m3-06-red-teaming-our-rag-application.md](m3-06-red-teaming-our-rag-application.md) |

### Module 4 — Threat Modelling our Agentic Application

| # | Lesson | Duration | Companion note |
|---|---|---|---|
| 1 | Threat Modelling our Agentic Application | announced | [m4-01-threat-modelling-our-agentic-application.md](m4-01-threat-modelling-our-agentic-application.md) |
| 2 | Securing from Jailbreak Attacks | 34:09 | [m4-02-securing-from-jailbreak-attacks.md](m4-02-securing-from-jailbreak-attacks.md) |

## How the course organizes knowledge

*The deep-dive version is [pedagogy.md](pedagogy.md).*

The course teaches in **built layers** (thesis → instrument → case
study → red-team grade), each layer named and assigned to a weak
point found in the diagram. Its signature instrument is the
**capability lens** — read, write, execute, reach — which prices
every component before any defense is chosen. Its evidence style is
**demos first**: every attack is shown working on the unsecured
application before the layer that closes it is built.

## Mapping to this repository's chapters

| Course module | Repository layers | Why |
|---|---|---|
| 1 — why study AI security | [Ch. 13](../../chapters/13-llm-application-security/README.md), [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) | exposure as a quantity; the application-security chapter |
| 2 — challenges, tools, framework | [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md), [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md), [templates/threat-model.md](../../templates/threat-model.md) | the attack catalog; the red-team discipline; the repository's own form |
| 3 — the RAG case study | [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md), [Ch. 13](../../chapters/13-llm-application-security/README.md), [P07](../../projects/p07-injection-defense/README.md) | the data protections; the injection defenses; the runnable project |
| 4 — the agent case study | [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md), [P08](../../projects/p08-control-and-monitoring-protocol/README.md) | tools, memory, MCP; the control-and-monitoring project |

The per-lesson mapping is tabulated in
[crosswalk-chapters.md](crosswalk-chapters.md); the 14 glossary terms
the course prompted are tabulated in
[crosswalk-glossary.md](crosswalk-glossary.md).

## Register entry and access level

- **[SRC-CURR-016]** — the [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053) (page-inspected
  2026-11-03: title, instructor, language, pricing with MRP, validity,
  sales count, the full published description, and the complete
  curriculum data with per-lesson durations — the outline itself
  marked TENTATIVE by the platform).

The course is paid and its lesson videos sit behind the paywall; no
video was watched and nothing behind the paywall is reproduced. The
companion notes are grounded in the page's own published description
and curriculum — the announced scope — and say so in every note's
honesty section.
