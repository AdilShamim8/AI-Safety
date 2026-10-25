# Note: Certified Adversarial Robustness via Randomized Smoothing (2019)

Source: SRC-PAPER-129 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Note 35's story ends with an epistemic wound: empirical defense
claims kept falling to adaptive attacks, so *attack-based* evidence
could not certify anything. This paper is the field's other answer —
**certification instead of attack-resistance**: a *provable*
guarantee, independent of any attacker's cleverness. The mechanism,
**randomized smoothing**: take any classifier that classifies well
under Gaussian noise and construct a new classifier — the most
probable class under noise — for which one can *prove* an ℓ₂-norm
robustness radius. The abstract's contributions: the technique
existed, but with loose guarantees; this paper proves a **tight**
ℓ₂ guarantee for Gaussian smoothing, and demonstrates it at scale —
an **ImageNet classifier with 49% certified top-1 accuracy under
perturbations with ℓ₂ norm less than 0.5 (=127/255)**, with the
closing note that no certified defense had previously reached that
bar (the abstract's own claim, truncated there).

## Why certification matters more than the numbers

The epistemic asymmetry is the note's whole teaching: an empirical
robustness number is a claim about *attacks tried*
([note 35](35-obfuscated-gradients.md): possibly obfuscated);
a certified number is a claim about *all attacks within the ball* —
the difference between "we survived the red team" and "the geometry
survives everything." Ch. 12's defense taxonomy runs exactly on
this split: **certified defenses** (sound but narrow — ℓ₂-only,
radius-limited, accuracy-priced) versus **empirical defenses**
(broad but unfalsifiable-until-adaptive-attack). The deployer's
question the course drills: *which kind of claim is on the label?*
A vendor robustness number without its claim type is unlabeled
merchandise.

The price side is equally load-bearing: certified accuracy is
*lower* than clean accuracy (49% certified where the base model
scores far higher) — the robustness-accuracy trade
(note 55, the paired TRADES note, which follows)
purchased with a *proof* attached. The course's honest-cost
discipline: the certificate's price is part of the certificate.

## What the abstract establishes

1. The smoothing construction (any noise-robust classifier → a
   certifiable smoothed classifier).
2. The tight ℓ₂ guarantee for Gaussian smoothing.
3. The ImageNet demonstration with the 49%-at-ℓ₂≤0.5 number.
4. The no-prior-certified-defense-reached-this framing.

Unclaimed: the proof's machinery (body-level), radii under other
norms (ℓ∞ certification is a different, harder literature the
course notes but does not import), and the later critiques of
smoothing's ℓ∞ limits (cited in Ch. 12 readings at their own level).

## Why this note exists in the course

1. **Ch. 12's certified-defense unit.** The chapter's
   threat-model grid asks what a defense claim *is*; this note is
   the canonical sound-claim citation, paired against the
   obfuscated-gradients story as the field's two roads.
2. **The assurance grammar connection.** A certificate is a
   safety-case-shaped artifact: a stated scope (the ℓ₂ ball), a
   stated guarantee (certified accuracy within it), stated
   exclusions (everything outside the norm). Ch. 22's
   safety-case template teaches exactly this grammar — this note
   is its mathematical instance.
3. **P09's audit logic.** Reliability claims with *scopes* beat
   claims without them; the shift-audit's per-slice Wilson
   intervals are the certification habit at behavioral tier.

## The falsifiable extension (deterministic tier)

The smoothing construction is runnable on P02's synthetic task:

- Wrap the base classifier in Gaussian smoothing (sample-and-vote
  at k noise draws); certify per-input via the majority margin;
  measure certified accuracy at planted radii against (a) random
  perturbations, (b) *worst-case-in-ball* perturbations found by
  grid search on the 2-D synthetic input.
- Prediction worth testing: the certified set's empirical accuracy
  holds at the claimed radius (no in-ball counterexample found),
  while the *uncertified remainder* fails — the certificate's
  selectivity reproduced, with the abstention-shaped consequence
  (smoothing as selective prediction: certify-or-abstain) visible
  in the same table.
- Falsifier: an in-ball counterexample on a certified input would
  mean the implementation's margin calculus is wrong — a bug worth
  finding before any claim, which is the deterministic tier's
  entire purpose.
