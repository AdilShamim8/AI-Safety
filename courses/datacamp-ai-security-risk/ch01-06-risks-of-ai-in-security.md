# 1.06 — Risks of AI in security

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 6 of chapter 1 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The second drill for the change-agent material: the risks of using AI in security — accountability and the ethical dilemmas — tested as discriminations.

## The concepts this exercise tests

### 1. Accountability is hard when the reasoning is opaque

The video's claim to master for this exercise: because it is difficult to understand how some systems make decisions, it is hard to know who is responsible for them. The exercise probes this with ownership questions — vendor or deployer? operator or auditor? — and the honest answer pattern is: whoever could foresee and mitigate, which requires the decision path to be inspectable. The repo's translation: no monitorability, no accountability (its control and reasoning-faithfulness chapters).

### 2. The ethical dilemmas as a weighing, not a verdict

Facial recognition in surveillance producing unfair results for specific groups and raising privacy concerns is the video's example. The exercise tests whether you can state BOTH sides of the weighing — the security benefit and the fairness/privacy cost — before concluding. Answers that carry only one side are the ones marked wrong.

### 3. The adoption rule

The closing principle the exercise wants applied to every stem: AI must be adopted carefully — know and mitigate the related risks BEFORE introducing AI into security operations. In exercise terms: any answer that deploys first and assesses later is wrong, which is the EU AI Act's own logic two chapters later.

## Worked example (beginner walk-through)

The model flags a transaction as fraudulent but cannot say why, and the analyst asks who owns the decision. The honest answer has two halves. *Accountability half:* responsibility follows the inspectable path — since it is difficult to understand how the system decided, it is hard to know who is responsible; that is the video's exact warning, and it is why the answer pattern is "whoever could foresee and mitigate," which requires the decision path to be reviewable. *Ethics half:* suppose the same bank adds face recognition to branch cameras. The security benefit is real, and so are the fairness and privacy costs the video names — unfair results for specific groups, privacy concerns. The answer that scores states BOTH sides before concluding; the answer that carries only one side is the marked-wrong one.

## Through-lines to this repository's chapters

- [Ch. 19](../../chapters/19-multimodal-and-embodied-safety/README.md) — facial-recognition fairness at full depth.
- [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) — why monitorability is the precondition for accountability.
- [Ch. 23](../../chapters/23-governance-and-standards/README.md) — who answers when the reasoning is opaque.

## What only this course does

Turns 'adopt carefully' from a slogan into graded weighings — the accountability drill this repository preaches but never quizzes.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
