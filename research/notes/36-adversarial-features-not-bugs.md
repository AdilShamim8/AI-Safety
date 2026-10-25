# Note: Adversarial Examples Are Not Bugs — the non-robust features thesis (2019)

Source: SRC-PAPER-111 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The folk explanation of adversarial examples — "the model is brittle, a
bug of high-dimensional curve-fitting" — predicts they are noise-level
artifacts of a mis-trained model. This paper's thesis inverts that:
adversarial examples exist *because the training distribution genuinely
supports them*. Non-robust features — "features derived from patterns in
the data distribution that are highly predictive, yet brittle and
incomprehensible to humans" — are real signal the model is *correctly*
learning from the data it was given. The adversarial perturbation is not
random noise that breaks a fragile model; it is a legible (to the model)
instance of predictive structure that humans do not perceive.

That inversion matters for every downstream claim in the course. If
adversarial vulnerability comes from genuinely predictive brittle
features, then: (a) "just train more / regularize harder" does not remove
it without changing what the data rewards; (b) robustness is a statement
about *which features you want the model to use*, which is a
specification choice — Ch. 03's territory, reached from Ch. 12; and (c)
the human-specified notion of robustness can be *misaligned with the
inherent geometry of the data* — the abstract's closing framing, and the
paper's deepest sentence.

## What the abstract establishes

1. The non-robust-features thesis as a direct attribution: adversarial
   examples "can be directly attributed to the presence of non-robust
   features" — not to optimization pathology.
2. A theoretical framework capturing these features, and their
   "widespread existence in standard datasets" established empirically.
3. The misalignment framing: a rigorous setting tying practice to "a
   misalignment between the (human-specified) notion of robustness and
   the inherent geometry of the data."

The famous experiments the body carries — training on adversarially
perturbed data with corrected labels yielding *robust* models, and
restricted-IMGnet transfer experiments showing non-robust features are
learnable and predictive — are behind the abstract's "we establish their
widespread existence" and are NOT claimed numerically here. The note
prices them as body-level results the abstract announces.

## Why this note exists in the course

Chapter 12 asks "when is an attack on a learned model *security* rather
than accuracy loss?" This paper supplies the answer's theoretical half:
evasion attacks live in the gap between the features the data rewards and
the features the operator intended. That is the same gap Ch. 03 names as
specification failure (the proxy's blindness), which is why Ch. 12's
failure-pathway section routes adversarial ML *through* specification
rather than through "models are fragile." The paper is the bridge citation
for that routing.

It also grounds Ch. 10's interpretability motivation from the adversarial
side: if predictive features can be human-incomprehensible, then
"understand what the model uses" is not a display preference but a
robustness decision — the features you cannot see are the ones an
adversary optimizes against. Note 36 and notes 03/18 (the monosemanticity
line) are the two ends of that argument.

## The honest counterweights

The thesis is contested literature: alternative accounts (label-noise
effects, boundary-thickness accounts) exist, and the note's abstract-level
access cannot adjudicate them. The course carries the thesis for its
*clarifying* value — it forces the specification question — while Ch. 12's
readings keep the controversy visible (the honest-residuals discipline;
the "contested claim" glossary term). No claim here that non-robust
features are the *sole* cause; the abstract itself says "directly
attributed to the presence of," not "exhaustively explained by."

## The falsifiable extension (deterministic tier)

The thesis has a synthetic test that P02 and P06's organisms can run:

- Build a two-channel dataset where channel A is robust-generative
  (signal survives small perturbations) and channel B is
  non-robust-predictive (tiny perturbations flip labels, high marginal
  predictiveness). P06's fixture is already close: its spurious channel
  is the non-robust analog.
- Prediction from the thesis: a standard-trained learner weights channel
  B by its predictiveness regardless of brittleness; a learner trained
  on B-perturbed-but-relabeled data shifts weight to A. Weight shift is
  measurable as the readout's coefficient ratio (P06 ships these
  numbers: w_a 2.247 vs w_b 2.661 in the standard arm).
- Falsifier: if training on perturbed-relabeled data leaves the weight
  ratio unchanged, the synthetic world contradicts the thesis's minimum
  claim — a recorded negative result, which the research-method file
  says is a publishable-tier outcome at this tier.
