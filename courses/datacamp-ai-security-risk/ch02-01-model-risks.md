# 2.01 — Model risks

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 1 of chapter 2 (video, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

Chapter 2 opens on the model lifecycle: watching risks during development reduces the harm of deploying a flawed system, but risks must ALSO be monitored after deployment — models drift over time as the real world and the data change, producing biased or inaccurate outputs if not monitored and addressed.

## Core ideas, explained

### 1. The seven common model risks

The video's list: lack of model transparency and interpretability, bias, hallucination, model drift, overfitting, underfitting, and data leakage. The first two are about the ability to understand the model: a non-transparent model's inner workings are not accessible and clear to those who use it; non-interpretable means people cannot understand WHY the model produces certain outputs from specific inputs. Both matter most in sensitive areas like healthcare or finance, where understanding the decision process is as important as the decision.

### 2. Bias and hallucination, where they enter

Bias: unfair preferences or prejudices arising at various stages — biased training data, algorithm choice and configuration, unrepresentative or flawed data, human assumptions during development. Hallucination: errors from insufficient training data, incorrect assumptions made by the model, and biases in the data. The repo's split for the same ground: bias is systematic across groups; hallucination is confident fabrication on outputs.

### 3. Drift: the model gets confused by the present

Model drift is previously accurate models losing relevance and accuracy because the data they see now does not follow the patterns they learned — the video's example is spam filters becoming less accurate as new deceptive tactics arrive. The repo's chapter on distribution shift is the formal treatment, and its glossary row is the discriminating version of this beat.

### 4. Overfitting, underfitting, and data leakage

The learning-quality triple: overfitting is learning the details and noise of the training data so much that future performance suffers; underfitting is a model too simple to learn the underlying patterns; leakage is outside data mistakenly included in the training set. Each damages the model's ability to make accurate predictions — and leakage is the quiet one, because it inflates validation scores before it ever shows up in production.

### 5. XAI as the management technique

The video's closing tool: Explainable AI (XAI), a set of methods that make models more understandable and transparent to humans by providing clear explanations of the reasoning behind outputs. It builds trust and aids identifying and correcting errors or biases within the model. Controlled across the lifecycle, these risks decide whether AI applications succeed; the repo's interpretability arc is the deep version.

## Through-lines to this repository's chapters

- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) — leakage and overfitting as evaluation-science subjects (grouped splits, contamination).
- [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) — drift and continuous monitoring at full depth.
- [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md) — transparency and interpretability as research programs.
- [Ch. 06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md) — hallucination as a measured behavioral quantity.

## What only this course does

The only lesson in the library that teaches the seven model risks as one lifecycle picture — underfitting and data leakage had no working definition anywhere in this repository before this companion.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); the video synopsis was supplied by the owner (2026-11-03) and is treated as the announced scope (SRC-CURR-015). No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
