# 2.05 — External risks in AI

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 5 of chapter 2 (video, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The external-threats video: internal risks live within a model's design or data; external risks are attacks from outside actors trying to manipulate the model. Threats are diverse and target different aspects of AI systems, so the video organizes them into five groups.

## Core ideas, explained

### 1. Adversarial input attacks (inference phase)

Attackers influence the deployed model's decision-making by manipulating input data: an image altered slightly makes a computer-vision system misclassify — not recognizing a stop sign. The target is the decision, the phase is inference.

### 2. Data corruption and poisoning (training phase)

Attackers insert false or malicious data into the training dataset so the AI learns incorrectly. Like adversarial input attacks, this manipulates data — but the target is the integrity of the model's LEARNING, not its decisions. Example: fake product reviews steering an e-commerce recommender. The poisoning-versus-adversarial boundary is the phase boundary: training versus inference.

### 3. Model theft and inversion

Attacks aimed at stealing sensitive information FROM the model: exploiting it to access or reconstruct its confidential training data — manipulated inputs uncovering private data used in training, like personal photos from a facial-recognition system. The target is neither the outputs nor the learning; it is the training data itself.

### 4. Infrastructure attacks

Targets the physical and virtual environments hosting AI systems — the supporting infrastructure rather than the models. The common example: flooding AI servers with overwhelming requests from many sources to overload them and make them inaccessible (the denial-of-service family).

### 5. Supply chain attacks and the best-practice set

Attacks on the components and libraries used in development — a vulnerability injected into a widely used AI library is present in every system built on that library. The defense set the video names: regular security audits; data validation and sanitization to guard the integrity of training and inference data; strong access controls restricting system access; encryption of sensitive information and anonymization where possible; continuous monitoring for immediate response; a more secure supply chain via trusted development tools, updated regularly; and ongoing education and training for staff. Risks evolve quickly — new threats emerge as AI advances, so continuous learning, proactive risk management, and vigilance are a must.

## Worked example (beginner walk-through)

One company, five attack surfaces. *Adversarial input:* a driver-assistance camera sees a modified stop sign and misclassifies it — the decision was manipulated at inference time. *Corruption and poisoning:* fake five-star reviews steer a recommender — the learning itself was corrupted at training time. *Theft and inversion:* researchers reconstruct training images from a facial-recognition model's outputs — the target is the training data, not the outputs and not the learning. *Infrastructure:* a flood of requests from many sources makes the service unavailable — the target is the hosting. *Supply chain:* a vulnerability planted in a widely used library ships inside every system built on it — the target is the development dependency. The taxonomy sorts by target and phase; learn the five targets and you can place any attack you read about, which is precisely how [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) and [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) organize their chapters.

## Through-lines to this repository's chapters

- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) — adversarial inputs and robustness at full depth.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the application-security surface (inference-time attacks).
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) — model inversion, supply chain, and the data-protection practices.
- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — infrastructure attacks on agentic systems.

## What only this course does

The five-group external-risk taxonomy organized by attack target (decision, learning, data, infrastructure, supply chain) — the cleanest beginner statement of the outside-actor surface in this library.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); the video synopsis was supplied by the owner (2026-11-03) and is treated as the announced scope (SRC-CURR-015). No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
