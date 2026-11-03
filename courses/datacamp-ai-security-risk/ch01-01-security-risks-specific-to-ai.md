# 1.01 — Security risks specific to AI

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 1 of chapter 1 (video, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The course's opening video. It sets the contract for the whole course: AI offers significant potential, but only effective risk management lets you harness the benefits safely — and adopting AI means rethinking security, because traditional security strategies are not sufficient when AI is in the loop.

## Core ideas, explained

### 1. A coin: benefits on one side, security risks on the other

The course's framing device: integrating AI is a coin whose two sides are its benefits and its security risks. The point of the metaphor is that you cannot accept one side without the other — every AI adoption decision is simultaneously a security decision. This repository states the same thing operationally in its risk-model chapter: a hazard without an exposure and a pathway is not yet a risk, and an adopted system always creates exposure.

### 2. The five risks that are specific to AI

The video names the five: bias, hallucination, data poisoning, adversarial attacks, and sensitive data exposure. What makes them AI-specific is that they all arise from the system learning from data — none of them is a traditional software bug you can patch. The course then works two of them as full examples: an AI hiring system trained on historical company data that reflects past bias learns and magnifies that bias (harm to candidates and to the company — trust declines), and attackers running a shopping platform's recommender through fake user profiles and interactions — data poisoning — misleading it into recommending unpopular or harmful products to genuine users (customer deception, reputational damage, lost trust).

### 3. Speed is what makes AI bias different from human bias

A key difference the video draws: AI makes lightning-fast decisions, often amplifying the impact before anyone can notice. Bias at machine speed unfairly favors or harms groups and creates uneven outcomes at an alarming rate — the same reason this repository treats propensity (a rate with a denominator) as its own risk-model quantity.

### 4. Hallucination, poisoning, adversarial input, data exposure

The remaining definitions, compressed: hallucination is the AI generating incorrect or misleading information and presenting it as truth (flawed decisions, misinformation spread, lost trust); data poisoning is someone intentionally tampering with training data so the system veers off course — weeds planted in a well-tended garden; adversarial attacks present misleading inputs during operation (not training) and are hard to detect, compromising the system's integrity; sensitive data exposure is a poorly secured AI system disclosing sensitive or protected information it relies on for training and operation.

### 5. Understanding is the first step; proactivity is the posture

The video closes its argument: recognizing these risks is the first crucial step toward managing them, and it is what lets you avoid the damages — financial losses, reputational damage, wrong AI-powered decisions, regulatory penalties. Because the AI risk landscape constantly changes, proactive risk management is essential: knowledge of the AI security ecosystem, foresight to future-proof the approach, and the wisdom to build a security-aware culture — the three things the rest of the course teaches.

## Worked example (beginner walk-through)

A small retailer launches an AI support chatbot. Walk the five risks past it, one by one, by asking where the fault would enter. **Bias**: the bot was trained on two years of resolved tickets; if past agents escalated certain customer names slowly, the bot learns that pattern — the fault entered through the training data. **Hallucination**: it confidently cites a return policy clause that does not exist — the fault is in generation, with no attacker and no bad data. **Data poisoning**: a competitor files fake tickets praising a rival product until the bot recommends it — the fault entered through training data an attacker controlled. **Adversarial input**: a user crafts a message that makes the bot override its guidelines — the fault entered at run time. **Sensitive data exposure**: the bot repeats a customer's card details back into a shared transcript — the fault is in data handling. The retailer's first lesson is the one this repository's [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) formalizes: name the phase before naming the risk, because each phase implies a different fix.

## Through-lines to this repository's chapters

- [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) — the repo's own risk vocabulary (hazard, exposure, pathway, propensity) is the disciplined version of this video's five-risk list.
- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — adversarial input attacks at full technical depth.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — sensitive data exposure, provenance, and the data-protection practices that reduce it.
- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) — bias and trust as sociotechnical, not merely technical, failures.

## What only this course does

The only lesson in the library that introduces the five AI-specific risks through two worked business stories — a hiring system and a shopping platform — before any technical machinery: the complete beginner on-ramp this repository lacked.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); the video synopsis was supplied by the owner (2026-11-03) and is treated as the announced scope (SRC-CURR-015). No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
