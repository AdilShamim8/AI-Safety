# Securing Vector Database - PII Leakage

*Course companion note · [AI Security & Guardrails](README.md) ·
module 3 lesson 2 (29:29) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The first security layer (about 29 minutes as listed): PII detection and masking, so customers' personal data never reaches the vector database.

## Core ideas, explained

### 1. Why the vector database is the weak point

The RAG's store holds whatever was indexed — and if customer personal data is embedded into the store, every retrieval is a potential disclosure: the store does not enforce access rules, and an attacker who can query can fish. The case study's answer is structural: the data never reaches the store at all.

### 2. PII detection and masking

As the description states: PII detection and masking, so customers' personal data never reaches the vector database. Detection finds the identifiers in the ingestion path; masking transforms them (redaction or tokenization) before embedding. The layer is a pre-storage gate — the same data-minimization logic as this repository's Ch. 16, applied at the vector store.

### 3. The layer's scope

Masking closes the PII-leakage path; it does not close unauthorized retrieval of restricted documents (the next lesson's layer) or injection (the one after). The case study's method is one layer per weak point, and the lesson ends by naming what remains open.

## Through-lines to this repository's chapters

- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — PII, masking, minimization — the chapter depth.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the store as an application component.

## What only this course does

The vector-store masking layer — the only lesson in the library that treats the embedding store as the PII boundary and masks at ingestion.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
