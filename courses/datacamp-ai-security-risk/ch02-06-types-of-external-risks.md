# 2.06 — Types of external risks

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 6 of chapter 2 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the five external-risk groups: classify by the attack's target and phase — the exercise the taxonomy was built for.

## The concepts this exercise tests

### 1. Target-and-phase as the sorting key

The five groups sort cleanly on two axes: WHAT the attack targets (decisions, learning, training data, infrastructure, components) and WHEN it strikes (inference, training, data handling, hosting, development). A stem naming the target gives you the group: 'misclassify a stop sign' → adversarial input; 'fake reviews' → poisoning; 'reconstruct personal photos' → model inversion; 'flood the servers' → infrastructure; 'vulnerability in a library' → supply chain.

### 2. The two confusions the exercise plants

Poisoning versus adversarial input (both manipulate data; the phase differs), and inversion versus theft (inversion reconstructs the training data; theft copies the model — the exercise treats them as one group with two aims, exactly as the video does).

## Through-lines to this repository's chapters

- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — the inference-phase attack surface.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — the data-phase attacks and their defenses.

## What only this course does

Grades the two-axis classification — the sorting skill the video sets up and only an exercise can confirm.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
