# 2.03 — Continuous monitoring

*Course companion note · [AI Security and Risk Management](README.md) ·
lesson 3 of chapter 2 (interactive exercise, 50 XP) · [course page](https://app.datacamp.com/learn/courses/ai-security-and-risk-management)*

## Where this lesson sits

The drill for the lifecycle half of the model-risks video: what to monitor after deployment, and why the watching never stops.

## The concepts this exercise tests

### 1. The monitorables and their signals

Post-deployment, the watch-list is: drift (the spam-filter pattern — accuracy decaying as the world moves), bias emergence (unfair outputs appearing as populations or usage patterns shift), and hallucination rates on live traffic. Each needs a baseline from deployment time, or the degradation cannot be measured — the repo's rule: a number without a pre-deployment referent has no meaning.

### 2. Monitoring is an early-warning system

The video's framing from the assessmentFrameworks lesson applies here: ongoing checks catch emerging risks and unexpected model behavior before they escalate — regular bias testing to identify unfair outputs, performance monitoring to catch degradation. In exercise terms: any answer that treats monitoring as a one-time check is wrong; the correct pattern is cadence plus thresholds plus a named owner.

## Worked example (beginner walk-through)

The monitoring contract in one paragraph. *Baseline:* at launch, record the model's accuracy, its refusal rate, and its error rate per subgroup — taken on day zero, because a number without a pre-deployment referent has no meaning. *Thresholds:* decide in advance what change triggers action — a two-point accuracy drop, a doubling of any subgroup's error rate, a new class of complaint in the support queue. *Owner:* a named person receives the alert, not a channel. *Cadence:* weekly drift checks, monthly bias re-tests, quarterly full re-assessment — the video's early-warning system, the checks set from the formal assessment's results. Any answer that treats monitoring as a one-time check or a dashboard purchase is the marked-wrong one; monitoring is a cadence with thresholds and a named owner, or it is retention without watching.

## Through-lines to this repository's chapters

- [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) — the monitoring chapter — dashboards, alerts, subgroup reliability.
- [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md) — monitoring as an assurance obligation.

## What only this course does

Drills the post-deployment watch — the habit the video courses never operationalize because they end when the model ships.

## Honesty note

Original study companion written to the lesson's announced scope. The lesson structure (titles, XP, order) was verified on the public catalog page 2026-11-03 (SRC-CURR-014); this interactive lesson's content is account-walled (SRC-CURR-015), so the note reconstructs the concepts it tests from the neighboring videos' announced scopes and the catalog page's stated chapter purposes. No video was streamed by this repository and no interactive exercise content is reproduced — the interactive lesson is account-walled; this note prepares the concepts it tests. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
