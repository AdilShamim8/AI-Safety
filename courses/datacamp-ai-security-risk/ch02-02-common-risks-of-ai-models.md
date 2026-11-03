# 2.02 — Common risks of AI models

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 2 of chapter 2 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the seven model risks: discriminate them by symptom, since several present with the same complaint — 'the model performs badly'.

## The concepts this exercise tests

### 1. Symptom-to-risk mapping

The discriminations the exercise probes: great on training data, poor in the world → overfitting; poor everywhere, missing the pattern → underfitting; validation too good to be true, then production disappoints → leakage; accurate last quarter, degrading now → drift; right on average, skewed across groups → bias; confident falsehoods on specific prompts → hallucination; predictions fine but no one can say why → transparency/interpretability gap.

### 2. The overfit-versus-underfit boundary

The cleanest discriminator is WHERE the error lives: overfitting's error concentrates on unseen data, underfitting's on all data including the training set. An exercise stem that reports training-set performance versus held-out performance is handing you the answer.

### 3. Leakage's tell

Leakage almost always presents as an evaluation surprise, not a behavior surprise: metrics that cannot be reproduced by an independent evaluator. The repo's evaluation-science chapter builds its grouped splits and contamination checks on exactly this observation.

## Through-lines to this repository's chapters

- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) — the evaluation discipline that catches leakage and overfitting.
- [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) — drift detection as deployment engineering.

## What only this course does

Grades symptom diagnosis — the triage skill that turns the seven-item list into usable clinical judgment.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
