# Red Teaming our RAG Application

*Course companion note · [AI Security & Guardrails](README.md) ·
module 3 lesson 6 (44:04) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The case study's closing lesson (about 44 minutes as listed, the longest in the module): red-teaming the secured RAG with Promptfoo, checking which security layers hold up at production level.

## Core ideas, explained

### 1. Red team the secured application, not the demo

The lesson's object: the application AFTER the four layers are in — because the question that matters is which layers hold, not whether an unsecured app can be attacked. The course's promise from the description: by the end, you can red team both secured applications with Promptfoo and check which security layers hold up at production level.

### 2. Promptfoo as the harness

The open-source anchor for the red-team pass: systematized adversarial testing — attack prompts as cases, the security layers as the code under test, results as pass/fail per layer. The lesson is where the course's evidence style completes: every attack from module 2 is run against every layer from module 3.

### 3. The finding is the grade

The lesson's output: a per-layer report — which attacks each layer stopped, and which slipped through to be caught (or missed) by the next. That per-layer report is the practitioner's version of this repository's evaluation discipline (Ch. 02 and Ch. 15): the layers are the system under test, and the attack set is the measurement instrument.

## Through-lines to this repository's chapters

- [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) — red-teaming methodology at chapter depth.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) — the measurement discipline behind the per-layer report.
- [the P07 project](../../projects/p07-injection-defense/README.md) — the repository's own runnable injection-defense exercise, the same method in code.

## What only this course does

The red-team pass on the secured stack — the only lesson in the library that grades the defense layers themselves, per layer, with a named harness.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
