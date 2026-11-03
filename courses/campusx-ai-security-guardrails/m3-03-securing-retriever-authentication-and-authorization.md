# Securing Retriever - Authentication and Authorization

*Course companion note · [AI Security & Guardrails](README.md) ·
module 3 lesson 3 (35:58) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The second security layer (about 36 minutes as listed, the longest applied lesson in the case study): authentication and authorization at production level, with pre-retrieval metadata filtering that blocks restricted documents before the search runs.

## Core ideas, explained

### 1. Authentication before authorization

The layer's order: first prove who is asking (authentication), then enforce what that identity may retrieve (authorization). A RAG without authentication serves whoever asks — and in the bank's context, that is the first hole.

### 2. Pre-retrieval metadata filtering

The course's named instrument: restricted documents are blocked BEFORE the search runs — metadata filtering at the retrieval step, so the search itself never touches documents the requester may not see. The distinction that matters: filtering before retrieval versus filtering results after — post-filtering leaks through ranking signals and latency; pre-filtering never reads the document.

### 3. Production level means enforced, not advisory

The course's phrase is authentication and authorization AT PRODUCTION LEVEL — the rules attach to the retrieval path as code, not as a policy document. This repository's Ch. 14 carries the same rule for agents and tools; the case study applies it to the retriever.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — authorization on the retrieval path.
- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — the same rule for tools and actions.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — access rules as data protections.

## What only this course does

The pre-retrieval filtering layer — the only lesson in the library that draws the before-versus-after filtering distinction and builds the before.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
