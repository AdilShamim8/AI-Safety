# 1.02 — AI risk awareness

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 2 of chapter 1 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The first interactive exercise. It drills the five AI-specific risks the opening video introduced, testing whether the learner can tell them apart by their mechanism rather than by their outcome.

## The concepts this exercise tests

### 1. The discriminating feature is the phase, not the harm

All five risks end in some kind of harm, so outcome language ('it gave a wrong answer') cannot tell them apart. The discriminating feature is where in the pipeline the fault enters: poisoned or biased training data (data poisoning, bias) faults the learning; misleading inputs at run time (adversarial attacks) fault the decisions; a confident fabrication with no input trigger (hallucination) faults the generation; and a disclosure of protected information (sensitive data exposure) faults the handling of the data itself.

### 2. The confusions the exercise is designed to catch

The two confusions the exercise probes: data poisoning versus adversarial attacks (training-time versus inference-time manipulation — the repo's chapters 12 and 16 draw the same line), and bias versus hallucination (systematic skew across groups versus confident fabrication on individual outputs). A third, subtler one: hallucination versus a wrong-but-honest prediction, which turns on whether the system presents the output as truth.

### 3. How to prepare in five minutes

Re-state each risk in one sentence naming the phase: 'bias — the training data skews the learned behavior across groups'; 'poisoning — an attacker corrupts the training data'; 'adversarial — an attacker crafts run-time inputs'; 'hallucination — the model fabricates and asserts'; 'data exposure — the system leaks protected information'. If your sentence cannot name the phase, the exercise will find you.

## Through-lines to this repository's chapters

- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — the threat-hypothesis form forces the same mechanism-first discipline.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — the poisoning-versus-adversarial boundary at full depth.

## What only this course does

Turns the video's definitions into a discrimination skill — the active-recall step this repository's flashcard method assumes but this course actually grades.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
