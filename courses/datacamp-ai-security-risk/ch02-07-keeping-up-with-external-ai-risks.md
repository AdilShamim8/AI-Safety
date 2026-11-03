# 2.07 — Keeping up with external AI risks

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 7 of chapter 2 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the defense half of the external-risks video: map each best practice to the risk group it counters — the exercise where the toolbox becomes a matching skill.

## The concepts this exercise tests

### 1. The practice-to-group mapping

Audits → surface vulnerabilities across groups; validation and sanitization → guard training and inference data integrity (poisoning, adversarial inputs); access controls → prevent unauthorized use (theft, breaches); encryption and anonymization → protect sensitive information (inversion, exposure); continuous monitoring → catch emerging threats (drift plus attacks); trusted, regularly updated development tools → secure the supply chain; ongoing staff education → the human layer every group exploits first.

### 2. The rule the exercise encodes

Defense is layered because attacks are phased: no single practice covers two groups, and every answer that claims one practice closes the whole surface is the distractor. The repo's control chapter states the same as 'defense in depth against a phased adversary'.

## Worked example (beginner walk-through)

Map each practice to the group it counters. *Regular security audits* → surface vulnerabilities across groups. *Data validation and sanitization* → guard the integrity of training and inference data against poisoning and crafted inputs. *Strong access controls* → prevent unauthorized use: model theft, breaches. *Encryption and anonymization* → protect sensitive information even if it leaks: inversion, exposure. *Continuous monitoring* → catch emerging threats as they develop. *Trusted, regularly updated development tools* → secure the supply chain at the dependency level. *Ongoing education and training* → the human layer every group exploits first. The rule the exercise encodes: defense is layered because attacks are phased — no single practice covers two groups, and any answer claiming one practice closes the whole surface is the distractor.

## Through-lines to this repository's chapters

- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — the data-protection practices in depth.
- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) — layered defense as an engineering discipline.

## What only this course does

Turns the defense list into a matching skill graded per-answer — practice the lecture format cannot give.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
