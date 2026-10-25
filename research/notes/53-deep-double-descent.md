# Note: Deep Double Descent — where bigger models and more data hurt (2019)

Source: SRC-PAPER-128 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

The classical bias-variance picture says model complexity has one
sweet spot: past it, test error rises forever. This paper's finding
breaks the picture — **performance first gets worse and then gets
better as model size increases**, and the same non-monotonicity
appears **as a function of training epochs**. The unifier the paper
proposes: **effective model complexity** (EMC) — a regime-dependent
complexity measure — and a **generalized double descent conjecture**
with respect to it. The abstract's sharpest practical corollary:
regimes exist where **"increasing (even quadrupling) the number of
train samples actually hurts test performance."**

The safety reading is immediate and uncomfortable: *more compute,
more data, more training* — the field's default remediation for
every failure — has documented regions where it makes things worse.
Not marginally worse: the "hurts" regime is the descent's whole
point.

## What the abstract establishes

1. Double descent as a function of model size, across "a variety of
   modern deep learning tasks."
2. Double descent as a function of training epochs — the
   *within-run* version.
3. The EMC unification and the generalized conjecture.
4. The more-data-hurts regime, quadrupling included.

Unclaimed (body-level): the specific tasks and architectures, the
noise conditions that produce the effect, the label-noise
dependence the body's analysis centers on, and the transition-point
theory. The note claims the phenomenon and its shape, no curves.

## Why this note exists in the course

1. **Ch. 02's scale-axis teaching gets its mechanism paper.**
   [Inverse scaling (note 48)](48-inverse-scaling.md) documents
   *task-level* bigger-is-worse; this note supplies the *training-
   dynamics* version and — critically for the course's honesty —
   the two together kill the folk theorem "scale monotonically
   helps" from both ends. The learner who meets Ch. 17's
   upgrade-drift warnings now has both citations for why the next
   checkpoint is an empirical question, not a default.
2. **The interpolation regime reframes overfitting.** Past the
   interpolation threshold, the model fits the training set
   exactly and test error falls *again* — meaning "train loss
   zero" is not the failure signal classical theory promised, and
   the diagnostics that matter live on the held-out side
   (Ch. 02's preregistration logic, now with a theory-backed
   reason the training curve cannot be the audit).
3. **Checkpoint evaluation is mandatory, not cautious.** Epoch-wise
   double descent means a training run can pass through a *worse*
   valley and exit better — or be sampled at the valley. Ch. 20's
   dangerous-capability evals at checkpoints (not interpolated
   between them) inherit a second, independent justification
   ([note 50](50-induction-heads.md)'s phase change was the first).
4. **The more-data-hurts corollary for data governance.** Ch. 16's
   "more data is more surface" now has an accuracy-side analog:
   more data is *also* a documented test-error risk in specific
   regimes. Data acquisition decisions carry performance risk, not
   just privacy risk.

## What this note does NOT claim

No claim that current LLM training sits in any particular regime
(the paper is 2019, vision-and-NLP-classic scale — regime positions
move with scale and recipe, the honest scale-drift caveat); no
claim that EMC is settled theory (the paper's own word is
*conjecture*); no numbers (body-level).

## The falsifiable extension (deterministic tier)

P02's optimizer over a controlled synthetic task can sweep both
axes the paper names:

- Model-capacity sweep (learner width at fixed data) and epoch
  sweep (fixed capacity) with held-out error tracked at every
  point. Prediction worth testing: a non-monotonic held-out curve
  appears in at least one swept axis when label noise is planted
  (the body's condition, implemented as a planted-mislabel slice
  at known rate).
- The clean-control arm (no planted noise) prediction: monotone or
  flat — isolating noise's role in producing the descent.
- Falsifier: monotone curves under planted noise would contradict
  the imported phenomenon in this world — a boundary result
  recorded either way, per the standing instruments.
