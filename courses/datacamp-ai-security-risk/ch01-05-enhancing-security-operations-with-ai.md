# 1.05 — Enhancing security operations with AI

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 5 of chapter 1 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the change-agent video: given a security-ops need, pick the right tool family — the exercise tests function-matching, not vendor knowledge.

## The concepts this exercise tests

### 1. Match by function, not by brand

The reliable mapping: continuous streams of behavioral and log data needing irregular-pattern detection → anomaly detection / UEBA; intelligence about attackers (motivations, tactics, techniques, what-next) needing aggregation and analysis → TIPs; repetitive cross-system tasks needing orchestration so experts focus on sophisticated threats → SOAR; real-time event correlation across systems to flag incidents → SIEM, with AI adding detection speed and prediction.

### 2. The trap: overlapping vocabulary

All four families say 'analyze' and 'alert', so the exercise discriminates on the object of the analysis: behavior (UEBA), adversary intelligence (TIP), workflows (SOAR), events (SIEM). If a stem describes what is analyzed rather than which product category it belongs to, you have your answer.

### 3. Why the bank example generalizes

The wire-transfer case in the video is the pattern to re-use: a real-time event stream, a learned model of past attempts, and a human investigation triggered the moment the model flags. Every correct answer in this exercise is some rotation of that pattern with the object swapped.

## Worked example (beginner walk-through)

Three needs, three families. *Need 1:* "alert me when an employee's account starts behaving like someone else's" — the object is behavior over time: **UEBA**. *Need 2:* "tell me which tactics the group targeting our sector is using next" — the object is adversary intelligence: a **TIP**. *Need 3:* "when an alert fires, automatically open a ticket, isolate the host, and page the on-call analyst" — the object is the workflow itself: **SOAR**. The distractor answers all sound plausible because every family says "analyze" and "alert." The tie-breaker is the *object of the analysis*: behavior, adversary, or workflow. If a stem describes what is being studied rather than which product category it belongs to, you already have your answer.

## Through-lines to this repository's chapters

- [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) — monitoring design under adversary pressure.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — what adversarial robustness means for detectors.

## What only this course does

Grades the function-matching judgment the video could only assert — the four tool families as a decision, not a list.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
