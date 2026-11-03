# Why AI Security? | Practical Landscape

*Course companion note · [AI Security & Guardrails](README.md) ·
module 1 lesson 2 (22:58) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

Module 1's second lesson (about 23 minutes as listed). It draws the line the course considers load-bearing: AI security is harder than traditional application security, for three structural reasons — outputs are non-deterministic, inputs are natural language, and applications are connected to tools and data — and it surveys the practical landscape with the live demos the course runs.

## Core ideas, explained

### 1. Three structural differences from application security

The course's own list, stated as the reason traditional defenses do not transfer wholesale: outputs are non-deterministic (the same input does not guarantee the same output, so output checking cannot be a string match); inputs are natural language (the attack surface is every phrasing a human can produce, not a typed field with a validator); and applications are connected to tools and data (the model is not the whole system — the retriever, the tools, the stores, and the channels around it are half the surface).

### 2. The live demos the course runs

As the published description states: live demos show how a RAG pipeline can be manipulated, how an attacker can turn an agent's tools and actions against you, and how images, files, and other non-text inputs open attack paths that text-only defenses miss. The demos are the course's evidence style: each attack is shown working before the defense for it is built.

### 3. The practical landscape: what is actually deployed

The lesson positions the course against the landscape of shipped LLM applications — RAG pipelines, agents with tools and shared memory, multimodal assistants — and the gap between what works and what is safe. Its emblem, delivered in module 3: a RAG that works is not yet safe for a bank.

### 4. Where this sits in the library

The four video courses teach the risk landscape at survey level; this course is the practitioner layer — the same landscape with the defenses built. This repository's chapters 12 and 13 are the deep treatments of the two sides the lesson names: adversarial manipulation, and the application surface built around the model.

## Worked example (practitioner walk-through)

Run the three structural differences against a concrete feature request. The request: "add file upload so users can ask about their PDFs." *Non-deterministic outputs:* you cannot write a test that asserts the answer for a given file, so the output check must be per-answer, not per-release — a guard on the answer channel. *Natural-language inputs:* the file's text becomes instructions your model may obey, so the upload is not an input field with a validator; it is an attack surface with a parser you do not control. *Connectedness:* the moment the upload exists, your app touches the filesystem, the parser, and the vector store — three components you now defend or accept. The feature is two lines of code and six surfaces; that arithmetic is the lesson, and the demos the course runs (a RAG manipulated, an agent's tools turned against it, images opening paths text defenses miss) are the same arithmetic at full scale.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the three structural differences at chapter depth.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — the manipulation demos at research depth.
- [Ch. 19](../../chapters/19-multimodal-and-embodied-safety/README.md) — non-text inputs as an attack surface.

## What only this course does

The only lesson in the library that states the non-determinism / natural-language / connectedness triple as the reason application security does not transfer — and then builds the defenses that answer each part.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
