# 2.12 — Fortified Code Forge

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 12 of chapter 2 (gamified scenario, 100 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The secure-development capstone game: build a system's defenses under constraints — choosing which practices to deploy with limited resources, the chapter's engineering trade-off scenario.

## The concepts this exercise tests

### 1. Constrained choice is the real skill

The game presents a budget and a threat profile; the winning play covers the highest-probability attack groups first with the cheapest effective practice — provenance against poisoning, input validation against adversarial, minimization where the data is sensitive, access control where modification is possible. This is the course's preview of chapter 3's threat prioritization: severity times likelihood under budget.

### 2. The forge's lesson

The title's claim: security is built, not bought — the practices are the blacksmith's anvil, and the game grades whether you can forge the right four bars for the door that is actually under attack, not the door you wish were under attack.

## Worked example (beginner walk-through)

The forge hands you a budget and a threat profile. Say the profile is: a recommender fed by user-generated content (poisoning risk high), a public API (adversarial inputs possible), and a small trust team (insider risk low, fatigue risk high). The winning allocation: provenance on the content feed first (cheapest effective counter to the highest-probability group), input validation at the API second, minimization on the profile store third (the data is sensitive), and access control on the training pipeline fourth. What the game grades is the *sequencing under constraint* — severity times likelihood under budget — which is chapter 3's threat prioritization arriving early as play. The forge's lesson: security is built, not bought, and the right four bars go on the door that is actually under attack.

## Through-lines to this repository's chapters

- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) — the engineering trade-offs at full depth.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — the practice menu in detail.

## What only this course does

A graded resource-allocation game — the trade-off judgment chapter 3 will formalize, previewed here as play.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
