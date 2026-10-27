# Part 2.3 — Robust training and monitoring: safety that survives distribution shift

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 3. Robust training & monitoring](https://www.youtube.com/watch?v=xhXYgIWFGkc) (6:07) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The second mechanism (6 minutes): training-time
robustness (generalization beyond the training distribution) plus
deployment-time monitoring (watching behavior in production) — the
two halves of the reliability story.

## Core ideas, explained

### 1. Why robustness is a safety property

A safety behavior that holds on the training distribution and fails
under shift is not a safety behavior — it is a hope. The robustness
program (adversarial training, distribution-shift stress testing,
generalization measurement) exists because every deployment moves the
distribution: new users, new tools, new adversaries. The repo's
[Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md)
and [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md)
are the full treatments.

### 2. Monitoring as runtime evidence

Deployment monitoring — anomaly detection, drift alarms, behavioral
telemetry, CoT inspection where available — is the runtime half of
the safety case: the claim "risks stay below stated limits" needs
*ongoing* evidence, not just pre-deployment evals. The repo's
[Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md)
carries the CoT-monitoring mechanics and its known trap (training
against the monitor promotes obfuscation — the Baker et al. result on
the Harvard course's reading list too).

### 3. The honest gap

Robustness research has a famously honest gap: no defense certifies
against adaptive attack (the repo's comparison note on static
benchmarks vs. adaptive evaluation exists for this reason). The
course prices monitoring and robustness as necessary layers, never as
sufficient ones — the stack framing again.

## Through-line to this repository's chapters

- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) —
  adversarial robustness.
- [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) —
  shift reliability.
- [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) —
  runtime monitoring and its traps.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
