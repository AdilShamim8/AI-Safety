# Note: HotFlip — gradient attacks arrive in text (2017)

Source: SRC-PAPER-148 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Vision had gradient attacks; text had a discrete problem — you
cannot add 0.001 to a word. HotFlip's move: treat the one-hot input
as if it were continuous, compute the gradient, and derive the best
**atomic flip** — swap one token for another in the direction the
loss most wants — then search greedily over sequences of flips. The
abstract's findings: only **a few manipulations** greatly decrease
character-level classifier accuracy, and the method's efficiency
makes **adversarial training tractable** for text (the harnessing
half, arriving with the attack).

## What the abstract establishes

1. The atomic-flip operation (gradient-based token swap on one-hot
   inputs).
2. The few-flips-suffice finding.
3. Efficiency enabling adversarial training in the text setting.

## Why this note exists in the course

1. **The language-attack lineage's bridge.** [FGSM (71)](71-fgsm.md)
   was continuous; [GCG (31)](31-gcg-universal-suffixes.md) is
   token-level discrete optimization; HotFlip is the bridge that
   brought the gradient program across the modality line — the
   course's Ch. 12→13 wiring uses it as the hinge citation.
2. **Discrete search discipline.** HotFlip's greedy flips are a
   reminder that language attacks inherit combinatorial structure
   (which token, which replacement) — the reason
   [jailbreak taxonomies](44-jailbroken-failure-modes.md) classify
   by *mode* rather than enumerating strings.
3. **Spellcheck is not a defense.** The few-flips finding is the
   original evidence that small lexical changes carry large
   behavioral changes — [spotlighting (08)](08-spotlighting.md)'s
   canonicalization exists because the flip family exists.

## What this note does NOT claim

No accuracy-drop numbers; no claim character-level classifiers are
the current threat surface (they are not — the method's transfer
principle is the claim); no claim HotFlip-style attacks defeat
modern instruction-tuned refusal (different objective, different
era — honestly separated).

## The falsifiable extension (deterministic tier)

P07's guard can host the flip family: craft single-token swaps that
change classification (tool-intent labels in the synthetic harness),
measure the guard's catch rate on flipped versus original payloads.
Prediction: a measurable fraction of flips evade a token-matching
defense while the intent is unchanged — lexical brittleness,
tabulated. Falsifier: full catch under all flips would show this
guard's feature space is flip-robust — recorded either way.
