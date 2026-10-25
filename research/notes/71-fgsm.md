# Note: Explaining and Harnessing Adversarial Examples — FGSM (2014)

Source: SRC-PAPER-146 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The founding paper of the linear-explanation program: adversarial
examples exist because **linear behavior in high dimensions suffices**
— a small perturbation, applied in the right direction, accumulates
enough activation change across many dimensions to flip the output,
no exotic nonlinearity required. The paper's instrument, **Fast
Gradient Sign Method (FGSM)**: perturb by the sign of the loss
gradient times a small epsilon — one backward pass, one attack. The
paper also introduced **adversarial training** on
gradient-sign-perturbed examples as the harnessing half.

## What the abstract establishes

1. The linear explanation for adversarial examples.
2. FGSM as the one-step attack (cheapness is the point).
3. Adversarial training (training on the perturbed examples) as the
   accompanying defense direction.

## Why this note exists in the course

1. **Ch. 12's origin station.** The lineage's first paper — before
   [C&W (05)](05-carlini-wagner-robustness.md) refined attacks,
   [Madry (20)](20-madry-adversarial-training.md) matured training,
   and [smoothing (54)](54-randomized-smoothing.md) certified: FGSM
   is where "attack and defend with the same gradient" begins.
2. **The single-step caveat the course keeps visible.** FGSM's
   cheapness is also its evaluation danger: defenses evaluated only
   against one-step attacks inherit the
   [obfuscated-gradients](35-obfuscated-gradients.md) trap — the
   lineage's later papers exist because one-step evaluation
   certified nothing.
3. **The linear hypothesis as a teaching model.** Whether it fully
   explains modern-model adversarial vulnerability (later literature
   says partially) matters less than its discipline: a mechanism
   hypothesis that yields a constructible attack — Ch. 12's
   "mechanism-then-instrument" pattern, first instance.

## What this note does NOT claim

No claim the linear explanation is complete for current architectures
(contested, honestly noted); no numbers; no claim about FGSM's
attack strength against modern defenses (weak by design of its
budget).

## The falsifiable extension (deterministic tier)

P02 already implements gradient-sign perturbations: the extension is
the paired-evaluation discipline — measure a defense against FGSM
AND against the multi-step attack the harness ships, and tabulate
the gap. Prediction: single-step-only evaluation overstates
robustness by a margin the intervals separate — the founding trap,
reproduced as a two-column table.
