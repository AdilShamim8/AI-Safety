# Note: Universal Adversarial Perturbations — one vector, every image (2016)

Source: SRC-PAPER-147 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The property that made adversarial vulnerability look structural
rather than input-specific: there exists a **universal,
image-agnostic, very small perturbation vector** that misclassifies
natural images **with high probability** — one fixed noise pattern,
many victims. The paper proposes the systematic algorithm for
computing these universal perturbations and shows
state-of-the-art networks are highly vulnerable to them, with the
perturbation "quasi-imperceptible" (the API record truncates there).

## What the abstract establishes

1. Existence and generality: one perturbation, high-probability
   misclassification across natural images.
2. The computation algorithm (systematic, iterative — body-level
   detail).
3. Smallness (quasi-imperceptible scale).

## Why this note exists in the course

1. **The transfer-and-structure evidence.** Universality is evidence
   that adversarial vulnerability is a property of the *model's
   decision geometry* (a shared fragile direction), not of
   individual inputs — the structural reading that
   [note 36](36-adversarial-features-not-bugs.md) deepens and that
   justifies treating robustness as a first-class training concern.
2. **Ch. 12's attack-surface arithmetic.** A universal perturbation
   is an *economy of attack*: compute once, apply everywhere — the
   property that turns adversarial noise from a per-input curiosity
   into deployable sabotage material (printed, per
   [note 64](64-physical-world-adversarial.md)).
3. **The GCG parallel on the language side.** [Note 31](31-gcg-universal-suffixes.md)'s
   transferable suffixes are UAP's language-model analog — one
   suffix, many models and prompts. The course teaches the two as
   one phenomenon at two modalities.

## What this note does NOT claim

No success-rate numbers (truncated); no claim of universality across
architectures (per-model within the paper's scope); no claim about
certified defenses' resistance to UAP-shaped attacks.

## The falsifiable extension (deterministic tier)

P02 can compute a universal perturbation for its synthetic
classifier: accumulate per-example sign-gradients, normalize,
iterate; then evaluate on held-out inputs. Prediction: a single
direction achieves misclassification above chance at imperceptible
magnitude, and its effectiveness concentrates where the decision
boundary is thinnest — universality reproduced, with the thickness
map as the bonus instrument. Falsifier: no shared direction (each
input needing its own) would mark this organism as lacking the
structural property — recorded either way.
