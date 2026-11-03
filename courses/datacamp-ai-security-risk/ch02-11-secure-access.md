# 2.11 — Secure access

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 11 of chapter 2 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the access-management half of the video: who may interact with the AI system and its data, and under what verification.

## The concepts this exercise tests

### 1. The access question has two sides

The video's rule: limit who can interact with the system, and allow only trusted, verified individuals or entities to MODIFY the model or its data. The exercise probes both sides: read-access decisions (who sees data) and write-access decisions (who may change the model) — and the second is the security-critical one, because every external attack group that targets learning or data is looking for a write path.

### 2. The principle to apply in every stem

Access is granted by role and verification, not by convenience: any stem where access is granted because someone asked, is in a hurry, or is senior is the wrong answer. The repo's phrase: authorization follows verification; the course's phrase: trusted and verified — same rule, different register.

## Worked example (beginner walk-through)

One question, two sides. *Who may read?* — analysts, auditors, the monitoring system: read access follows role. *Who may modify?* — the model, its weights, its training data: write access follows verification, and this is the security-critical side, because every external attack group that targets learning or data is looking for a write path. The exercise's stems grant access because someone asked, is in a hurry, or is senior — each is the marked-wrong answer. The principle in one line, the video's own: only trusted, verified individuals or entities may modify the model or its data; authorization follows verification, never convenience. [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) is where the same rule meets AI agents that hold tools.

## Through-lines to this repository's chapters

- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — access control for AI systems with tools.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the application layer's access surface.

## What only this course does

Grades the modify-versus-read distinction — the access decision the security courses state and this exercise scores.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
