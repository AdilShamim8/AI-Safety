# 2.09 — Secure development practices

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 9 of chapter 2 (video, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The secure-development video: regular security measures are castle walls repelling basic attacks; secure development practices are the additional defense layer BUILT by the teams that create and maintain the systems — data practices first, then coding, access, and infrastructure.

## Core ideas, explained

### 1. The four data practices

Data provenance and traceability: understanding the origin of data and tracking its journey through the AI system — provenance combats data poisoning by pinpointing and removing corrupted data. Data validation: checking and cleaning data before it is fed to the system, ensuring accuracy, relevance, and freedom from malicious tampering. Data minimization: limiting collection and processing to only what is absolutely necessary — significantly reducing the risk of privacy breaches and data theft. Encryption and anonymization: transforming sensitive data into a secure format only authorized parties can access; anonymization removes personally identifiable information, protecting against model inversion attacks aimed at extracting sensitive information from the system.

### 2. Secure coding, access management, secure infrastructure

Beyond data: secure coding practices (regular code reviews, vulnerability scanning, coding standards designed to prevent security flaws) shield against infrastructure attacks by keeping the underlying software robust against exploitation. Access controls limit who can interact with the system and its data — only trusted, verified individuals or entities may modify the model or its data, which is what reduces external attacks exploiting the system. Secure infrastructure safeguards the hardware and software environments: firewalls, intrusion detection systems, secure cloud services — the solid foundation against infrastructure-targeted threats.

### 3. Security is not for the tech team alone

The video's closing move: business leaders fund the security tools and training; legal experts check that practices respect user privacy; regulators define additional checks and balances. The teamwork is what makes the systems not only secure but trusted and reliable — the same four-pillar logic as chapter 1, now applied to the development lifecycle.

## Worked example (beginner walk-through)

A loan-approval model's data pipeline, walked through the four practices in order. *Provenance and traceability:* every field carries its origin — which bureau, which upload, which consent — so when poisoned or corrupt data is found, it can be pinpointed and removed. *Validation:* at ingestion, the data is checked and cleaned — accurate, relevant, untampered — before it ever reaches training. *Minimization:* the pipeline asks of every field "do we need this?" and drops what it does not — every uncollected datum is a breach that cannot happen. *Encryption and anonymization:* what remains is transformed for storage and stripped of identifiers where possible — the last line against model inversion. Then the non-data practices around it: secure coding (reviews, scanning, standards), access management (only trusted, verified parties may modify the model or its data), and secure infrastructure (firewalls, intrusion detection, secure cloud). The video's closing move is the beginner's headline: security is built by the teams that create the system, and it is not the tech team's job alone.

## Through-lines to this repository's chapters

- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — provenance, minimization, anonymization — the deep treatment.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — secure coding for the AI application layer.
- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — access control for agents with tools.
- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) — the engineering discipline behind the practices.

## What only this course does

The four data practices (provenance, validation, minimization, encryption/anonymization) named as a sequence — the beginner's data-protection ladder this repository taught only at expert depth.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); the video synopsis was supplied by the owner (2026-11-03) and is treated as the announced scope (SRC-CURR-015). No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
