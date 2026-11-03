# Securing Output - Output Guardrails

*Course companion note · [AI Security & Guardrails](README.md) ·
module 3 lesson 5 (35:32) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The fourth security layer (about 36 minutes as listed): output guardrails built with NVIDIA NeMo Guardrails, checking every answer for private data, wrong facts, or a manipulated response before it reaches the user.

## Core ideas, explained

### 1. The output channel is a real channel

The layer's premise: the answer the model produces is not yet the answer the user gets — there is an output channel, and it can be guarded like any channel. The guardrail sits between the LLM's generation and the user, which is why non-deterministic outputs (module 1's first structural difference) get checked per answer, not per release.

### 2. Built with NVIDIA NeMo Guardrails

The course's open-source anchor for this layer: output guardrails built with NVIDIA NeMo Guardrails, checking every answer for private data, wrong facts, or a manipulated response before it reaches the user. The three checks are three closures: private data (the PII path that survived the earlier layers), wrong facts (grounding against the retrieved documents), and manipulated responses (the injection that survived the delimiter defense).

### 3. Defense in depth, stated as the case study's logic

The course stacks the layers deliberately: masking at ingestion, filtering at retrieval, guardrails at input, delimiters in the prompt, guardrails at output. No single layer is trusted to catch everything; the output guardrail is the last check on the answer, and the red-team pass (the next lesson) tests whether the stack holds.

## Worked example (practitioner walk-through)

Stand at the answer box and list what can still be wrong. The four earlier layers are in; the model generates. *Private data:* an answer quoting a customer's records — the PII path that survived (or bypassed) masking. *Wrong facts:* an answer contradicting the retrieved documents — the grounding failure. *A manipulated response:* an answer shaped by an injection the delimiter defense missed. The output guardrail checks all three on the answer channel, per answer — because outputs are non-deterministic, the check cannot be per-release. Built with NVIDIA NeMo Guardrails in the course, the layer is the last check, and the course is honest about what it is not: it is not a substitute for the earlier layers, it is the reason the stack is called defense in depth — each layer exists because the one before it can be beaten.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the output channel as an application surface.
- [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) — checking every result as the control pattern.
- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) — layered defense as an assurance discipline.

## What only this course does

The NeMo Guardrails output layer — the only lesson in the library that builds the last-check guardrail on the answer channel and states the three closures it exists for.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
