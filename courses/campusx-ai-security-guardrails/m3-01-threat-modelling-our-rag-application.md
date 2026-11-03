# Threat Modelling our RAG Application

*Course companion note · [AI Security & Guardrails](README.md) ·
module 3 lesson 1 (24:21) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The case study opens (about 24 minutes as listed): the NovaBank RAG application, and why a RAG that works is not yet safe for a bank. The five-step framework runs here for the first time, end to end.

## Core ideas, explained

### 1. A RAG that works is not yet safe for a bank

The case study's thesis, from the published description: functional correctness and safety are different properties. The RAG answers correctly on the demo queries; the bank context adds restricted documents, customer personal data, and regulatory exposure — and the same architecture that answers well leaks and misretrieves under an adversary.

### 2. The framework applied: maps, boundaries, capability

As the description states: using Data Flow Diagrams, entry and exit points, trust boundaries, and the capability table, you find every weak point in the pipeline — then close each one with its own security layer. The lesson is the framework made concrete: the diagram of the RAG (query channel, retriever, vector database, LLM, output channel), the boundaries where data crosses trust levels, and the capability table that prices each component.

### 3. The weak points the case study names

From the description's own list, the layers that follow one per lesson: the vector database (PII leakage), the retriever (authentication and authorization), the user query and LLM (jailbreak and prompt injection), and the output (guardrails) — each mapped as a weak point before it is closed.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the RAG surface at chapter depth.
- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — works-versus-safe as the hazard/exposure distinction.
- [the threat-model template](../../templates/threat-model.md) — the repository's form for this exact exercise.

## What only this course does

The only lesson in the library that runs the full framework on a production-grade RAG with the bank's constraints — and states the works-is-not-safe thesis as its opening move.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
