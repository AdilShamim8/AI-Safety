# Note: Scaling Laws for Neural Language Models — the predictability that changed everything (2020)

Source: SRC-PAPER-145 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The empirical discovery: cross-entropy loss **scales as a power-law
with model size, dataset size, and training compute** — smooth
trends "spanning more than seven orders of magnitude," with
architectural details (width, depth) having **minimal effects
within a wide range**. The paper's simple equations govern
overfitting's dependence on model/data size and training speed's
dependence on model size (the abstract's own inventory; the
equations and the compute-optimal training recipe are body-level).

The safety course reads this paper as *infrastructure* — the
finding that made scaling an engineering discipline, and thereby
created every scale-related question the course asks: How big will
the next system be? (Predictably bigger, by budget.) What does
capability-vs-scale look like? (Smooth on loss; emergent and
non-monotone on behaviors — [the mirage](29-emergent-abilities-mirage.md),
[inverse scaling](48-inverse-scaling.md), [double descent](53-deep-double-descent.md)
are the behavior-side annotations to this loss-side law.) And what
does governance need? (Forecasting: power laws make "we will have
X compute in Y years" a usable input, which is Ch. 20/23's
eval-and-govern timeline logic.)

## What the abstract establishes

1. The power-law in model size, data, compute — over seven-plus
   orders of magnitude.
2. The architecture-insensitivity claim within wide ranges.
3. The existence of simple equations for overfitting and
   training-speed dependence.

## Why this note exists in the course

1. **The predictability baseline.** Every "surprise" note in the
   catalog is surprising *against* this law: smooth loss decline
   with lumpy behavior changes is the puzzle the mirage note
   resolves (metric choice), the phase-change note (50) explains
   mechanistically, and the inverse-scaling note documents. The
   course teaches them as one package with this note as the floor.
2. **Ch. 17/20's forecasting logic.** Release-eval scheduling and
   governance timelines assume scale is forecastable; this note is
   why that assumption is licensed — the honest version of
   "compute governance" starts from empirical predictability.
3. **The memorization tie.** [Note 58](58-quantifying-memorization.md)'s
   capacity law is the privacy-side member of the same family:
   scale laws are *governance-relevant across the board*, not just
   capability-relevant — bigger is a privacy decision, a
   robustness question (note 53), and an emergent-behavior
   lottery, all at once.

## What this note does NOT claim

No exponents (body-level); no claim that behavior-level properties
follow the loss's smoothness (the opposite — the companion notes
exist); no claim about post-2020 recipe changes (Chinchilla-style
data-optimality revisions are follow-up literature, cited in
readings at their own levels).

## The falsifiable extension (deterministic tier)

P02's sweep infra can verify a mini power law:

- Train learners across at least six sizes (two-plus orders of
  parameter magnitude in the synthetic scale); fit loss-vs-size on
  a log-log grid; report the fitted exponent with its interval.
- Prediction worth testing: a straight line on the log-log plot —
  the law's minimal form, holding in the small world where the
  course can check it.
- Falsifier: curvature beyond the interval would mark where this
  organism exits the regime — recorded, and the boundary itself is
  the pedagogical payload for what "empirical law" means.
