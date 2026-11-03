# 1.10 — Balancing stakeholder interests

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 10 of chapter 1 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The harder stakeholder drill: given two interests in tension, produce the balance — the exercise tests whether you can hold both concerns in one decision.

## The concepts this exercise tests

### 1. Tension pairs the exercise uses

The recurring pairs from the video: precision versus privacy (data scientist versus legal), speed versus trustworthiness (executive growth agenda versus customer trust), innovation versus compliance cost (startup posture versus regulatory posture). Each pair maps to the stakeholder analysis method: whose interest, what concern, what impact on them — then the balanced decision.

### 2. The output format that scores

A balancing answer states both interests, the trade-off accepted, and the mitigation for the interest that lost ground ('we adopt the tool, and we add the audit that answers the legal concern'). Single-interest answers read as advocacy, not analysis — the exact failure mode the repo's governance chapter calls governance theater.

## Worked example (beginner walk-through)

The tension: the data science team wants to log every candidate interaction for training data; legal says retention itself is a privacy risk. The balanced answer follows a fixed shape. *State both interests:* richer training data improves the model; stored personal data creates exposure the company would have to answer for. *Name the trade-off accepted:* say the company keeps the data — then it must say what it now owes. *State the mitigation for the side that lost ground:* minimize what is stored (keep features, drop identifiers), bound the retention period, and log the decision. Single-interest answers read as advocacy, not analysis — which is exactly what this exercise marks wrong. The pattern is the everyday version of what [Ch. 23](../../chapters/23-governance-and-standards/README.md) institutionalizes as governance instruments.

## Through-lines to this repository's chapters

- [Ch. 23](../../chapters/23-governance-and-standards/README.md) — instruments that institutionalize the balancing.
- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) — why the balancing is systemic, not personal.

## What only this course does

Practices the balance-as-deliverable pattern — the governance skill the frameworks courses teach only at the document level.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
