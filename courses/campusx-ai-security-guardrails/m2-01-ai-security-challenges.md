# AI Security & Challenges

*Course companion note · [AI Security & Guardrails](README.md) ·
module 2 lesson 1 (9:48) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

Module 2's opening lesson (about 10 minutes as listed), the shortest of the four. It states what AI security means in this course and why it is harder than traditional application security, preparing the ground for the adversarial attacks lesson that follows.

## Core ideas, explained

### 1. What AI security means here

The working definition the course builds on: securing the application around the model — the RAG pipeline, the tools, the memory, the channels — not only the model itself. The course's scope is the practitioner's: every component in the data flow, each getting its own security layer by the end of the case studies.

### 2. Why harder than application security

The three structural reasons restated as the challenge list: outputs are non-deterministic, inputs are natural language, and applications are connected to tools and data. Traditional defenses assume deterministic outputs, validated inputs, and a bounded system boundary — none of which an LLM application provides.

### 3. The bridge to the framework

The lesson's closing job: naming the challenges precisely enough that the next lesson (adversarial attacks and types) and the one after (the threat-modelling framework) have something to organize. This repository's Ch. 13 is the chapter-length version of the same ground.

## Through-lines to this repository's chapters

- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the application-security chapter at full depth.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — the adversarial side the next lesson details.

## What only this course does

The compact statement of scope — the whole course's meaning of AI security in ten minutes, the layer the survey courses spend chapters approaching.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
