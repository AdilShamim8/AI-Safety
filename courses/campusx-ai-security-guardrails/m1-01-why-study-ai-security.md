# Why Study AI Security?

*Course companion note · [AI Security & Guardrails](README.md) ·
module 1 lesson 1 (27:59) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The course's opening lesson (the longest in module 1, about 28 minutes as listed). It sets the thesis the whole course runs on: LLM applications built without security in mind are open to attack, and a partial understanding of RAG, agents, and multimodal agents leaves applications insecure — because every retriever, tool, and input channel you add without thinking about security becomes a new way in for an attacker.

## Core ideas, explained

### 1. Built without security in mind means open to attack

The course's first claim, stated as a default: an LLM application assembled for capability alone — a retriever added for knowledge, a tool added for action, a file channel added for convenience — ships every one of those additions as an attack surface. The security question is not asked after the architecture exists; the course's position is that it must be asked while the architecture is being chosen, which is what its threat-modelling framework (module 2) exists to enforce.

### 2. Partial understanding is the specific failure mode

The course targets a precise audience gap: practitioners who can build RAG, agents, and multimodal agents but have a partial understanding of what those systems are security-wise. Each pattern imports its own weak points — a RAG brings a vector database and a retriever; an agent brings tools and actions; a multimodal app brings non-text inputs. Knowing the pattern's capability without knowing its exposure is the partial understanding the course exists to correct.

### 3. Every component added is a new way in

The counting rule the course teaches: attack surface grows with every retriever, tool, and input channel. This repository's own risk-model chapter states the same rule as exposure — a hazard needs a pathway, and every new component is a new pathway. The course's version is the practitioner's statement of it, and its Data Flow Diagrams (module 2) are the instrument for counting.

### 4. The course's method: secure from the ground up

The closing move of the opening: security is designed in, not patched on. The course promises a repeatable step-by-step threat-modelling framework applied end to end to two production-grade case studies — a RAG application for a bank and a doctor-booking agent — each component getting its own security layer. That ground-up promise is what distinguishes this course from the four video courses in this repository's lecture library, which teach the concepts at research level without building the layers.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the application-security chapter this course works at production level.
- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — exposure and pathway as quantities — the disciplined version of every-component-is-a-way-in.
- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — the agent surface: tools, memory, MCP.

## What only this course does

The only course in the library that opens by counting attack surface per added component and promises to close every one of them with a named security layer in two worked case studies.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
