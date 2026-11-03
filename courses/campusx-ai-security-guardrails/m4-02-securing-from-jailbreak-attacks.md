# Securing from Jailbreak Attacks

*Course companion note · [AI Security & Guardrails](README.md) ·
module 4 lesson 2 (34:09) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The course's closing applied lesson (about 34 minutes as listed): the jailbreak gate as the agent case study's first built layer — the defense the whole course has been building toward, at the input channel that matters most for an agent.

## Core ideas, explained

### 1. A separate guard model reads every message

The gate's architecture, from the published description: a separate guard model reading every message, along with recent turns, inside delimiters — blocking authority claims, requests for other people's data, and attempts to override the agent's rules. The design choices are the lesson: separate (its own model, not the agent's), contextual (recent turns, not the message alone), and delimited (the conversation arrives inside boundaries the guard treats as data).

### 2. What the gate blocks, named

The three block categories the description lists: authority claims (I am the administrator), requests for other people's data (patients' details), and attempts to override the agent's rules (ignore your instructions). Each is a jailbreak family the course named in module 2, now closed at the gate.

### 3. The method completes: every layer on both case studies

The lesson closes the course's arc: the same five-step framework, the same one-layer-per-weak-point method, now on the agent — gate on the conversation, guard on every tool and MCP result, judge on every memory write, guardrails on every answer, and (as the description promises) Promptfoo red-teaming at production level on both secured applications.

## Through-lines to this repository's chapters

- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — the gate in the agent's architecture.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — the jailbreak families at research depth.
- [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) — testing the gate systematically.

## What only this course does

The jailbreak gate built as its own model with recent-turn context and delimiters — the only lesson in the library that implements the conversation-level gate and names the three block categories it exists to catch.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
