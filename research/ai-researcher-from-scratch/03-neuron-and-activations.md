# Module 3 — The neuron and the activation functions

> Track: [AI Researcher From Scratch](README.md) · module 3 of 7.
> Video chapters: *Single Neuron Explained*, *Activation Functions*
> (SRC-VIDEO-001, page-inspected). Written companion: modules
> `04_neuron_from_scratch` (seven lessons, ending in *the concept of
> learning*) and `05_activation_functions` (six lessons: ReLU, sigmoid,
> tanh, SiLU, SwiGLU, softmax) of vukrosic/zero-to-ai-researcher
> (SRC-REPO-001, full-text-read). Code:
> [`activations.py`](../../src/ai_safety_course/from_scratch/activations.py)
> and [`neuron.py`](../../src/ai_safety_course/from_scratch/neuron.py) —
> every number below was produced by running them.

## 0. Why this module exists

Module 02 gave you the tensor toolbox; this module builds the smallest
thing worth calling a *model* out of it. One neuron is two operations —
a dot product and a nonlinearity — and the whole of deep learning is
those two operations repeated with learned contents. The video devotes a
chapter to the neuron and another to activations because the activation
is where the depth comes from: module 01 proved that a stack of linear
maps collapses into one linear map, so *something* nonlinear has to sit
between the layers or depth is decoration. The six activations here
(ReLU, sigmoid, tanh, SiLU, SwiGLU, softmax) are the ones the companion
repo teaches, and they are the right six: two classic (sigmoid, tanh),
the modern default (ReLU), the modern default's smooth successor
(SiLU), its gated form (SwiGLU — inside every current-generation
transformer FFN, module 05 will use it), and the distribution-maker
(softmax — the end of every classifier and the heart of attention).

And because a neuron is a *model*, it can *learn*: the module closes
with the companion's "concept of learning" lesson made exact — one
weight, one target, the chain rule applied factor by factor, one
update, and the loss visibly falling. That paragraph is the seed of
module 04's backpropagation; read it slowly.

## 1. The single neuron — two operations, precisely

A neuron maps an input vector to a number in two steps:

```text
z = w · x + b          (the linear step: module 01's dot product)
a = act(z)             (the activation: this module's nonlinearity)
```

The companion repo's framing is a pass/fail predictor: inputs are a
student's features, the weights are how much each feature matters, the
bias shifts the threshold, and the sigmoid turns the score into a
probability. Code:

```python
>>> from ai_safety_course.from_scratch.neuron import Neuron
>>> n = Neuron(weights=[-1.0, -0.5], bias=1.0, activation="sigmoid")
>>> n.pre_activation([1.0, 0.8])     # z = -1.0 - 0.4 + 1.0
-0.4
>>> n.forward([1.0, 0.8])            # a = sigmoid(-0.4)
0.401312339887548
```

`pre_activation` and `forward` are separate methods on purpose: the
*gradient* of the activation needs `z`, not `a`, so the API exposes the
boundary where the chain rule will later split. Everything else in the
neuron is bookkeeping — `Neuron` stores weights as a copied list (so
mutating the constructor argument after the fact does nothing, a small
honesty guarantee pinned by a test) and validates the activation name
against a four-entry registry (`relu`, `sigmoid`, `tanh`, `silu`) that
is literally the module's whole polymorphism.

The linear step is where module 01's "a layer computes dot products"
lives at its smallest: `linear_step([1, 2], [3, 4], -1) = 10` is one
row of the matrix example from module 01 section 5. One neuron is one
row; a layer of neurons is the whole matrix; that identification is
module 04's opening move.

## 2. The activation zoo — six nonlinearities, with derivatives

The table the module is built around (values verified by execution;
derivatives all pinned against central finite differences in
`test_fs_activations.py`):

| name | formula | f(-1) | f(0) | f(1) | derivative |
| --- | --- | --- | --- | --- | --- |
| ReLU | max(0, z) | 0.0 | 0.0 | 1.0 | 1 if z > 0 else 0 |
| sigmoid | 1/(1+e^-z) | 0.2689 | 0.5 | 0.7311 | s(1-s) |
| tanh | (e^z-e^-z)/(e^z+e^-z) | -0.7616 | 0.0 | 0.7616 | 1-t² |
| SiLU | z·sigmoid(z) | -0.2689 | 0.0 | 0.7311 | s(1+z(1-s)) |
| SwiGLU | silu(g)·v | — | 0.0 (g=0) | — | (silu(g), silu'(g)·v) |
| softmax | e^zi/Σe^zj | — | — | — | s_i(δ_ij - s_j) |

Four readings of this table, one per design lesson:

**Sigmoid and tanh are squashes.** Both map the whole line into a
bounded range — (0,1) and (-1,1) — and both *saturate*: far from zero,
their derivatives collapse toward 0 (sigmoid's s(1-s) is at most 0.25
and falls off both tails; tanh's 1-t² behaves the same way). That
saturation is the historical reason deep networks were hard to train
before ReLU: stacked sigmoids squashed their own gradients to nothing,
the vanishing-gradient problem in one column of arithmetic. Tanh at
least centers its output at zero, which keeps the *next* layer's dot
products from drifting all-positive — the zero-centered sibling, as the
companion lesson names it.

**ReLU is a hinge, and its derivative is a gate.** max(0, z) is
computationally nothing, nonsaturating on the positive side (derivative
exactly 1 for all z > 0 — gradients pass through unchanged, the property
that made depth trainable), and dead on the negative side (derivative
0 — inputs below the hinge send no gradient at all, the "dead ReLU"
failure mode). At exactly z = 0 the derivative does not exist; the
subgradient convention is 0, torch's `relu` backward takes the same
value, and both the code and the tests state the choice rather than
hiding it.

**SiLU and SwiGLU are gates.** SiLU(z) = z·sigmoid(z) — the input gates
itself, in the companion lesson's phrase: how much of z passes through
is decided by sigmoid(z), a function of z. The symmetry visible in the
table (silu(-1) = -0.2689 = -sigmoid(-1); silu(1) = +sigmoid(1)) is the
self-gating structure: negative inputs are mostly blocked but leak
slightly — smooth where ReLU is a kink, unbounded above where sigmoid
saturates. SwiGLU(v, g) = silu(g)·v generalizes the trick to *two*
arguments: one projection decides (the gate), the other is decided
about (the value). Modern transformer FFNs are exactly this — two
matmuls instead of one, with SwiGLU between — and module 05 wires it
into our GPT's feedforward block.

**Softmax is not an elementwise function.** It maps a vector to a
probability distribution: s_i = e^{z_i}/Σ_j e^{z_j}, positive, summing
to 1, order-preserving (bigger logit, bigger probability). It is the
last layer of every classifier and — scaled and masked — the *attention*
of module 05. Its Jacobian s_i(δ_ij − s_j) is a full matrix (the output
components interact through the normalization), and the module provides
both the matrix form and the collapsed one-pass chain-rule form
`dL/dz_j = s_j(dL/ds_j − Σ_i dL/ds_i·s_i)`; the tests check them
against each other and against finite differences.

**The numerical-stability lesson, once, properly.** Naive softmax on
[1000, 1000.1, 999.9] computes e^1000 = inf and dies (float64 overflows
near e^709). The fix is the max-subtraction trick: subtract max(z) from
every logit first. This is *exact*, not approximate — softmax is
shift-invariant because e^{max(z)} cancels from numerator and
denominator — and the test suite pins both the invariance
(softmax([1,2,3]) == softmax([1001,1002,1003]) to 12 digits) and the
survival of the huge-logit case. The same discipline appears in
sigmoid's two branches (z ≥ 0 uses 1/(1+e^-z); z < 0 uses e^z/(1+e^z) —
neither exponentiates a positive number larger than |z|). These two
tricks are the entry fee for writing any numerical ML code, and the
tests make them load-bearing.

## 3. The concept of loss — a number that says how wrong

Training needs a scalar that measures wrongness. The companion lesson
teaches two, both in `neuron.py`:

**Mean squared error** — per prediction, `(prediction - target)²`. Using
the lesson's own numbers (a pass/fail neuron predicting 0.19 for a
student who actually passed, target 1):

```python
>>> from ai_safety_course.from_scratch.neuron import mse, bce
>>> mse(0.19, 1.0)
0.6561000000000001
>>> bce(0.19, 1.0)
1.6607312068216509
```

Squaring keeps the error positive and punishes large misses
superlinearly (the lesson's two reasons). The gradient
`dL/d(prediction) = 2(prediction - target)` is the *outer* factor of
every chain rule in module 04.

**Binary cross-entropy** — `-[y log p + (1-y) log(1-p)]`, the right loss
for probabilistic yes/no outputs: it is (up to scaling) the negative
log-likelihood of the observed label under the predicted Bernoulli.
Where MSE charges 0.6561 for the 0.19-when-truth-1 miss, BCE charges
1.6607 = -log(0.19): it is *much* harder on confident wrongness — a 0.01
prediction against truth 1 costs -log(0.01) ≈ 4.6, and the curve blows
up toward infinity as p → 0, which is exactly the pressure that shapes
probability outputs. Two engineering details the code states and the
tests pin: probabilities are clipped to [ε, 1-ε] so p of exactly 0 or 1
gives a large-but-**finite** loss (the course-wide "log loss is
clipped, never silently infinite" contract, same as the evaluation
package's scorer), and targets must be exactly 0 or 1 — the loss raises
on anything else rather than computing garbage.

BCE has a famous property worth deriving once rather than trusting:
paired with a sigmoid output, the whole thing simplifies. With
`a = sigmoid(z)`, `y ∈ {0,1}`:

```text
dL/dz = dL/da · da/dz = [(a - y) / (a(1-a))] · [a(1-a)] = a - y
```

The sigmoid's derivative cancels BCE's denominator *exactly*, leaving
the error signal `a - y` — clean, bounded, and the reason
sigmoid+BCE became the standard pair. The unsimplified per-probability
form (`bce_grad_from_probability`) is kept in the code deliberately, so
the cancellation is something the *tests verify numerically*
(`test_bce_plus_sigmoid_cancellation`) rather than folklore the module
repeats.

## 4. The concept of learning — one weight, the full chain rule

The companion's final neuron lesson is "the concept of learning": if
you know how wrong you are, and you know which way each knob moves the
wrongness, you turn every knob a little against it. `learn_single_weight`
makes that exact for the smallest possible model — one weight, no
matrix, every factor inspectable:

```python
>>> from ai_safety_course.from_scratch.neuron import learn_single_weight
>>> new_w, before, after, grad = learn_single_weight(
...     w=0.4, x=1.0, bias=0.0, target=1.0, lr=0.5)
>>> before
0.16105159414601886
>>> grad
-0.1928392041133206
>>> new_w
0.4964196020566603
>>> after
0.14317327376518554
```

Read the arithmetic line by line — it is module 01's chain-rule
sentence with numbers in it:

```text
z = 0.4 · 1 + 0 = 0.4                the pre-activation
a = sigmoid(0.4) = 0.5987            the prediction
L = (a - 1)² = 0.1611                the loss
dL/dw = 2(a - target) · act'(z) · x  the three-factor chain rule
      = 2(0.5987 - 1) · 0.2403 · 1
      = -0.1928                       outer × middle × inner
w' = w - lr · dL/dw = 0.4 + 0.0964 = 0.4964    the update
L' = (sigmoid(0.4964) - 1)² = 0.1432  the loss after
```

The three factors are the whole story of backpropagation in miniature:
**outer** — how the loss moves with the prediction (2(a−y), from MSE);
**middle** — how the prediction moves with the pre-activation
(act'(z), this module's table); **inner** — how the pre-activation
moves with the weight (x, just the input). Module 04's backprop for a
full network is this product computed layer by layer *from the loss
backwards* — the name is "back" precisely because the outer factor is
computed first and the inner last. The test suite verifies the gradient
against a finite difference of the same model (`-0.19284` to 6 digits),
verifies the loss falls, and verifies the degenerate cases: a perfect
prediction gives gradient exactly 0 (no step), and a ReLU neuron sitting
exactly on its kink stays put by the stated convention.

One more observation that sets up module 07 (the source's
learning-rate *search* experiments): with `lr = 0.5` the step took the
loss from 0.1611 to 0.1432 — a 11% cut. The same function with a
different learning rate behaves differently (larger steps cut faster
until, past a threshold, they overshoot and the loss *rises*); the
learning rate is not a constant of nature but a per-architecture,
per-scale quantity. The companion repo's second experiment exists to
search it; the track's module 07 studies that protocol as research
training.

## 5. Where this connects

- **To the track**: module 04 stacks neurons into a layer and
  generalizes this module's three-factor gradient to a full backward
  pass; module 05's attention is softmax over scaled dot products —
  the Jacobian in section 2 is the exact object its gradients flow
  through.
- **To the safety curriculum**: refusal at the *model* level is shaped
  by the same saturation and gating behaviors studied here at the
  neuron level — a saturated sigmoid is the microscopic image of a
  confidently wrong model; the clipped-BCE discipline reappears in the
  P03 calibration package's log-loss scorer, verbatim.
- **To the sources**: the neuron's two-step structure, the pass/fail
  worked example, and the loss/learning lesson sequence follow the
  companion repo's `04_neuron_from_scratch` lessons (SRC-REPO-001);
  the six-activation set, the self-gating framing, and the
  advantages/disadvantages framing follow `05_activation_functions`.

## 6. Exercises

1. Compute by hand, then check against `activations.py`: sigmoid(2),
   tanh(0.5), silu(-2), relu(-3), and each one's derivative at the same
   point (for sigmoid use s(1-s) with your own s).
2. Verify numerically (finite differences, h = 1e-6) that
   silu'(z) = s(1 + z(1-s)) at z ∈ {-2, 0.5, 3}. Then explain in one
   sentence why SiLU's derivative does *not* vanish as z → +∞.
3. The pass/fail neuron of section 1 (w = [-1.0, -0.5], b = 1.0)
   predicts 0.4013 for x = [1.0, 0.8]. Compute the MSE and BCE losses
   against target 1, then run one `learn_single_weight`-style step on
   the bias b alone (derive dL/db — note the inner factor is now 1, not
   x) with lr = 0.5, and report the new prediction.
4. Prove softmax shift-invariance in one line (the e^c cancellation),
   then find a z-vector where the *naive* softmax implementation
   returns NaN but ours returns a valid distribution.
5. With `learn_single_weight(w=0.4, x=1.0, b=0.0, target=1.0)`:
   try lr ∈ {0.1, 0.5, 2.0, 8.0}. For each, report the loss after one
   step. Which lr overshoots (loss rises)? Bound the overshoot
   threshold by treating the single step as the quadratic-bowl
   contraction of module 01's exercise 3.

### Solutions

1. sigmoid(2) = 1/(1+e^-2) = 0.8808, derivative 0.8808·0.1192 =
   0.10499. tanh(0.5) = 0.4621, derivative 1 − 0.4621² = 0.7864.
   silu(-2) = -2·sigmoid(-2) = -2·0.1192 = -0.2384; s = 0.1192,
   silu' = 0.1192·(1 + (-2)(0.8808)) = 0.1192·(1 − 1.7616) = -0.0908.
   relu(-3) = 0, derivative 0. (Checks: `acts.sigmoid(2)`,
   `acts.tanh_grad(0.5)`, `acts.silu_grad(-2.0)`, ….)
2. Finite differences reproduce those numbers to ~1e-6. SiLU'(z) →
   sigmoid(z) → 1 as z → +∞ because the gate *opens*: the (1 + z(1−s))
   factor tends to 1 as s → 1, so the derivative tends to the ReLU-like
   pass-through 1 — smooth at the origin, nonsaturating in the tail,
   which is precisely the "ReLU's benefits without the kink" claim.
3. MSE = (0.4013 − 1)² = 0.3585; BCE = −log(0.4013) = 0.9130. The bias
   gradient: dL/db = 2(a − y)·act'(z)·1 = 2(−0.5987)·0.2403 = −0.2878;
   b' = 1.0 + 0.5·0.2878 = 1.1439; new z = −0.4 + 0.1439 = −0.2561;
   new prediction sigmoid(−0.2561) = 0.4363 — moved 0.035 toward the
   target, exactly as the gradient sign promised.
4. softmax(z + c) has numerator e^{z_i+c} = e^c·e^{z_i} and denominator
   e^c·Σe^{z_j} — the e^c cancels, so the distribution is unchanged for
   every c, in particular c = −max(z). Naive overflow: any vector with
   a logit above ~709.8 (float64's exp limit), e.g. [800, 799, 798] —
   naive gives inf/inf = NaN; ours subtracts 800 first and returns a
   valid distribution (pinned by `test_softmax_survives_huge_logits`
   at [1000, 1000.1, 999.9]).
5. One step from w = 0.4 (grad −0.19284, so w' = 0.4 + lr·0.19284):
   lr 0.1 → w' 0.4193, loss 0.1578 (small cut); lr 0.5 → 0.4964,
   0.1432; lr 2.0 → 0.7857, sigmoid = 0.6873, loss 0.0977 (best single
   step); lr 8.0 → w' 1.9427, sigmoid = 0.8747, loss 0.01566 — still
   falling, no overshoot *yet*. Overshoot threshold: near this
   operating point the update behaves like the quadratic bowl with
   curvature g = 2·act'(z)² ≈ 0.1154 (differentiating the gradient
   2(a−y)a'x once more at the current point, a≈y ignored), so
   contraction requires lr < 2/g ≈ 17.3 — lr 8 is inside, lr 32 would
   leap across and diverge. The honest general lesson: the safe lr is
   curvature-dependent, which is why the source's experiment 2 searches
   it per architecture instead of assuming it.

## 7. Readings and provenance

- SRC-VIDEO-001 — *Become AI Researcher From Scratch - Full Course*
  (video chapters: *Single Neuron Explained*; *Activation Functions*).
  Access: page-inspected 2026-10-22.
- SRC-REPO-001 — vukrosic/zero-to-ai-researcher: module
  `04_neuron_from_scratch` (lessons 01 what-is-a-neuron … 07
  the-concept-of-learning; the pass/fail predictor and the
  prediction-0.19/truth-1 loss example are its) and module
  `05_activation_functions` (six lessons, one per activation, each with
  advantages/disadvantages — the saturation and self-gating framings
  here follow them). Access: full-text-read 2026-10-22 (cloned).
- The sigmoid+BCE cancellation is standard and unattributed here; the
  max-subtraction softmax trick likewise. Both are *verified by the
  module's tests* rather than cited — that is the track's standing
  arrangement for elementary facts.
