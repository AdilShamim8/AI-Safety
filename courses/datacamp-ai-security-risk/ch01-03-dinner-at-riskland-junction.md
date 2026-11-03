# 1.03 — Dinner at Riskland Junction

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 3 of chapter 1 (gamified scenario, 100 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

A gamified scenario exercise: the learner classifies risk examples into the five families while a story unfolds — the course's signature move of grading judgment, not recall.

## The concepts this exercise tests

### 1. Scenario classification is a two-step procedure

For each story beat the exercise serves, the reliable procedure is: first name the phase the fault entered through (training data, run-time input, generation, data handling), then match the phase to the family. Stories are written to tempt you toward the harm word ('customers were deceived') instead of the mechanism word — the same trap as classifying a risk by its consequence instead of its causal pathway, which the repo's risk-model chapter treats as the primary classification error.

### 2. Why the game grades judgment

Every wrong classification in this game would, in a real organization, buy the wrong defense: calling poisoning 'bias' sends you scrubbing labels instead of auditing the data supply chain; calling an adversarial attack 'hallucination' sends you retraining instead of hardening inputs. The game makes that cost felt — the repo's phrase for the same lesson is 'each family implies different interventions, and misclassifying a risk buys the wrong defense'.

## Through-lines to this repository's chapters

- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — the risk taxonomy with the full classification discipline.
- [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) — misuse framing when the adversary is the point.

## What only this course does

The only graded scenario trainer for risk classification in the library — judgment practice the video courses cannot give.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
