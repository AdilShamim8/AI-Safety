# Tools Needed to Secure LLM Applications

*Course companion note · [AI Security & Guardrails](README.md) ·
module 2 lesson 3 (11:20) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The tools lesson (about 11 minutes as listed): the toolbox the course deploys across both case studies — named here before the framework lesson assigns each tool to a layer.

## Core ideas, explained

### 1. The toolbox as the course names it in practice

From the published description and outline: PII detection and masking (so customers' personal data never reaches the vector database); authentication and authorization at production level (pre-retrieval metadata filtering that blocks restricted documents before the search runs); input guardrails (stopping jailbreaks in the user query); delimiters and a system prompt that treats retrieved documents as data (the prompt-injection defense); output guardrails built with NVIDIA NeMo Guardrails (checking every answer for private data, wrong facts, or a manipulated response before it reaches the user); a separate guard model (reading every message and every tool and MCP result); and Promptfoo for the red-team pass at the close.

### 2. Each tool answers a named attack

The organizing rule: no tool without an attack it closes. Masking answers PII leakage; pre-retrieval filtering answers unauthorized retrieval; input guardrails answer jailbreaks; delimiters answer injection from retrieved documents; output guardrails answer manipulated responses; the guard model on tool results answers indirect injection hidden in external content.

### 3. The open-source anchor

The course builds its output guardrails with NVIDIA NeMo Guardrails and red-teams with Promptfoo — the two open-source anchors of the practitioner layer, both now carried as glossary rows in this repository.

## Worked example (practitioner walk-through)

Assign every tool to its attack, and notice what has no tool. Masking → PII leakage at ingestion. Pre-retrieval filtering → unauthorized retrieval. Input guardrails → jailbreaks on the query. Delimiters and the data-not-instructions prompt → injection from retrieved documents. A guard model on tool results → injection hidden in external content. Output guardrails → manipulated or leaking answers. Promptfoo → the whole stack, tested. What has no tool: a user who is legitimately authorized and legitimately malicious, and a model that is wrong without being attacked. The honest toolbox answer names those two residuals and routes them to policy and to evaluation — which is why the course closes with red-teaming rather than with the toolbox.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the defense layer at chapter depth.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — PII, masking, and the data protections.
- [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) — monitoring every result as the control pattern.

## What only this course does

The only lesson in the library that names the practitioner toolbox — masking, filtering, guardrails, delimiters, guard models, red-team harness — as one assignable set.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
