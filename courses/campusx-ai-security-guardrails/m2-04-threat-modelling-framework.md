# Threat Modelling Framework

*Course companion note · [AI Security & Guardrails](README.md) ·
module 2 lesson 4 (11:49) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

Module 2's capstone lesson (about 12 minutes as listed): the step-by-step framework the course repeats on any LLM application — the instrument both case studies run on.

## Core ideas, explained

### 1. The five-step framework

As the course applies it in both case studies: (1) map the application with Data Flow Diagrams — every component, and every entry and exit point; (2) draw the trust boundaries — where data crosses between levels of trust; (3) examine every component through the capability lens — what it can read, write, execute, or reach; (4) find every weak point from the diagram; (5) close each one with its own security layer. The course's phrase for the method: repeatable to secure any LLM-based application.

### 2. The capability lens

The course's signature instrument: for each component, ask what it can read, write, execute, or reach. The lens turns a diagram into a risk list — a component that can write is more dangerous than one that can only read, which is exactly how the course explains why an agent (with write and delete capabilities) is more dangerous than a RAG (whose worst case changes an answer).

### 3. Why a framework at all

The course's argument: security work without the framework is anecdote-driven — you fix the attack you happened to see. The framework makes the search systematic: every component visited, every capability priced, every weak point closed with a named layer. This repository's threat-model template and Ch. 13's discipline are the same argument at chapter depth.

## Through-lines to this repository's chapters

- [the threat-model template](../../templates/threat-model.md) — the repository's own form for the same discipline.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the chapter-length treatment.
- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — capability and exposure as quantities.

## What only this course does

The framework as a repeatable five-step procedure — the course's core deliverable, and the reason its two case studies are the same method twice.

## Honesty note

Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
