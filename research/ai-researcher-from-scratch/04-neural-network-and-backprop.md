# Module 4 — The neural network and backpropagation

> Track: [AI Researcher From Scratch](README.md) · module 4 of 7.
> Video chapters: *Neural Network Layers*, *How Networks Learn*
> (SRC-VIDEO-001, page-inspected). Written companion: module
> `06_neural_network_from_scratch` of vukrosic/zero-to-ai-researcher
> (SRC-REPO-001, full-text-read — seven lessons from the architecture of
> a network through the chain rule to implementing backpropagation).
> Code: [`network.py`](../../src/ai_safety_course/from_scratch/network.py);
> every number below was produced by running it.

## 0. Why this module exists

Module 03 ended with one weight learning by the three-factor chain
rule. This module does the only two things that remain to make that a
*neural network*: **stack** neurons into layers and layers into a
network, and **generalize** the three factors from scalars to matrices
so every weight in the stack learns *at once*. That generalization has
a famous name — backpropagation — and a reputation for difficulty that
it does not deserve: it is module 03's outer/middle/inner sentence,
with matrix products in place of scalar multiplications, walked from
the loss backwards. The module's proof that you now hold the real
thing is the last section: a network with a hidden layer learns XOR —
a function no amount of linear machinery can represent — in a few
thousand plain-SGD steps, while the same network *without* the
nonlinearity sits pinned at the data's mean, exactly as the algebra
predicts. When that contrast makes sense, you understand what depth is
*for*, which is the conceptual hinge the whole rest of the track
(transformers included) swings on.

## 1. The dense layer — the neuron, vectorized

A dense layer is the module-03 neuron copied across output units and
run on a batch at once. For a batch `X` of shape `(B, in)`, weights
`W` of shape `(in, out)`, bias `b` of shape `(out,)`:

```text
Z = X @ W + b          every output unit's dot product, one matmul
A = act(Z)             the activation, elementwise
```

The key identification from module 01 realized: *column j of W is
neuron j's weight vector*, and `X @ W` computes all B·out dot products
in one product. The worked example from the tests, hand-checkable:

```python
>>> from ai_safety_course.from_scratch.network import DenseLayer
>>> from ai_safety_course.from_scratch.tensors import Tensor
>>> layer = DenseLayer(Tensor([[1.0, 2.0], [3.0, 4.0]]), Tensor([10.0, 20.0]))
>>> layer.forward(Tensor([[1.0, 1.0], [0.0, 1.0]])).tolist()
[[14.0, 26.0], [13.0, 24.0]]
```

Row `[1, 1]`: first output = 1·1 + 1·3 + 10 = 14, second = 1·2 + 1·4 +
20 = 26. Row `[0, 1]` shifts only through column 2 of `W`: 13 and 24.
Two design details worth their words. The bias add is an explicit
loop (`_add_row`) rather than silent broadcasting — module 02's
stance, kept honest in plain sight. And the layer caches `x`, `z`,
`a` on every forward: backprop needs all three, and the cache is the
visible price of not having autograd — memory you can *inspect*, which
is exactly what module 05's attention will ask you to do when a
gradient looks wrong.

`identity` is in the activation registry (gradient identically 1)
because logit layers — the output of a classifier before softmax — are
dense layers too; the note's network examples use it for exactly that.

## 2. Backpropagation — the three factors, as matrices

Module 03's learning step was `dL/dw = 2(a−y) · act'(z) · x` — outer
(loss→prediction), middle (prediction→pre-activation), inner
(pre-activation→weight). A layer's backward pass is the same sentence
with the factors promoted:

| factor | scalar form (module 03) | matrix form (here) |
| --- | --- | --- |
| outer | `2(a−y)` | `dZ = dA ⊙ act'(Z)` — elementwise |
| middle | `act'(z)` | `dW = Xᵀ @ dZ`, `db = colsum(dZ)` |
| inner | `x` | `dX = dZ @ Wᵀ` |

Three remarks make this derivation complete rather than magical.

**Every shape is forced.** `dA` arrives shaped `(B, out)` — the
previous factor's `dX`. `dZ` matches it (elementwise product with the
cached activation derivative). Then `dW = Xᵀ @ dZ` is `(in, B) @ (B,
out) = (in, out)` — *the shape of W itself*, which is the point: a
gradient must live where its parameter lives. `db` is the column-sum
of `dZ` because the bias enters every row of `Z` identically (sum the
routes). And `dX = dZ @ Wᵀ` is `(B, out) @ (out, in) = (B, in)` — the
shape of the input, handed to the previous layer as *its* `dA`. If you
can reconstruct this table from the shape rule alone, you own
backpropagation; the note's exercise 1 asks you to prove it to
yourself exactly that way.

**The walk is backwards because the outer factor is computed first.**
`MLP.backward` iterates `reversed(self.layers)`, each layer consuming
the `dX` of the one after it. That ordering is not an implementation
choice — it is the chain rule's structure: to know how an early weight
moved the loss, you must first know how the loss moved with the final
output, then pass that signal down through every intermediate
computation. "Back"-propagation is the direction the *question*
travels; the answer (the update) then travels forward through
`sgd_step` as `w ← w − lr·dW`, module 01's descent line, unchanged.

**The tests do not trust the algebra.** For one-, two-, and three-layer
stacks (sigmoid, tanh, and a relu in the middle), every analytic
`dW`/`db` is compared against a central finite difference of the same
loss — perturb one weight by `h`, recompute the loss, take the slope.
Analytic backprop that matches numeric differentiation on every
parameter of every layer is *correct* backprop; anything else is a
sign error waiting for a training run to expose it. This
gradient-check discipline is the single most transferable skill in the
module: it is how you debug any autograd system too, including
PyTorch's (torch has `gradcheck` because everyone needs it).

## 3. The loss layer — softmax cross-entropy at network scale

The network's output gradient comes from a loss. Two are provided,
both batch-mean forms with the denominator written out (`mse_loss`
returns `(loss, grad)` as a pair so no caller can take one without the
other). The interesting one is `softmax_cross_entropy` for
classification: given logits `(B, C)` and integer targets, it applies
module 03's cancellation at the network scale —

```text
p = softmax(logits),  y = one-hot targets
L = -(1/B) Σ log p[r, t_r]
dL/dlogits = (p - y) / B
```

— the sigmoid+BCE cancellation's multi-class sibling: softmax's
Jacobian and cross-entropy's logarithm cancel wholesale, and the
output-layer gradient is *the error signal itself*, `(p − y)/B`, no
matrix in sight. The code computes the loss from `p` directly and the
gradient from the subtraction; the test suite verifies the gradient
entry-by-entry against finite differences of the loss, so the
cancellation is load-bearing, not decorative. The convenience wrapper
`train_step_softmax_ce` wires forward → loss → backward → update in
four lines, which is the entire learning loop of a modern classifier
minus the framework.

## 4. Learning, end to end — XOR, and why depth is not decoration

XOR — the exclusive-or of two bits — is the canonical function that
*no* linear model can represent: its four points `[[0,0]→0, [0,1]→1,
[1,0]→1, [1,1]→0]` are not separable by any single line (the
impossibility argument: a linear model's output is `w·x + b`; XOR
requires `f(0,0)=f(1,1)` but `f(0,1)=f(1,0)` with a *different*
value — forcing `w₁ = w₂` and `w₁ = −w₂` simultaneously, hence
`w = 0`, hence constant output). It is the smallest function that
*needs* a hidden layer, which makes it the right final exam for this
module. Run with our code — 2→4→1, tanh hidden, sigmoid output, plain
SGD at lr 0.5, 4000 epochs, seeded init:

```python
>>> from ai_safety_course.from_scratch.network import MLP, DenseLayer, train_loop
>>> from ai_safety_course.from_scratch.tensors import Tensor
>>> x = Tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
>>> y = Tensor([[0.0], [1.0], [1.0], [0.0]])
>>> mlp = MLP([DenseLayer.from_seed(2, 4, "tanh", seed=42),
...            DenseLayer.from_seed(4, 1, "sigmoid", seed=43)])
>>> curve = train_loop(mlp, x, lr=0.5, epochs=4000, y=y)
```

| epoch | 0 | 100 | 500 | 1000 | 2000 | 4000 |
| --- | --- | --- | --- | --- | --- | --- |
| loss | 0.2824 | 0.0461 | 0.0036 | 0.0015 | 0.0007 | 0.0003 |

Final predictions: `[0.008, 0.981, 0.981, 0.023]` — the network has
carved the two diagonal classes apart, and all four rows classify
correctly at the 0.5 threshold. The control experiment is the same
architecture with the hidden activation set to `identity`: after 2000
epochs it sits at loss **0.2500** with predictions `[0.5, 0.5, 0.5,
0.5]` — the constant-mean function, which is provably the best any
linear stack can do on XOR (loss 0.25 = predicting the label mean).
Same code, same optimizer, same learning rate; only the nonlinearity
differs. *That* is what "activation functions are where the depth
comes from" (module 03) means operationally, and it is why module 05's
attention blocks are dense layers with a softmax bolted in rather than
more linear maps.

The determinism guarantee matters as much as the convergence: the run
above is reproducible bit-for-bit (seeded init, no shuffling, no
decay), and `test_training_curve_is_deterministic` pins it by training
the same network twice and comparing curves. A training curve a reader
cannot reproduce is an anecdote; this one is a fact of the repository.

## 5. Where this connects

- **To the track**: module 05's transformer is this module's machinery
  plus two additions — attention (a softmax over scaled dot products
  inserted between the dense layers) and residual connections (the
  identity path made architectural). Its training loop, if you build
  one, is `train_loop` with a different forward.
- **To the safety curriculum**: backprop is the mechanism that *makes*
  steering vectors trainable and features learnable — chapter 10's
  SAEs train by exactly this loop, and chapter 09's patching analyses
  manipulate the caches (`x`, `z`, `a`) that our layers expose on
  purpose. A safety researcher who can read a backward pass can read
  an interpretability paper's methods section.
- **To the sources**: the layer→network→chain-rule→backprop sequence
  follows the companion repo's module 06 (SRC-REPO-001); XOR as the
  depth demonstration and the gradient-check discipline are the
  track's additions, both standard in the wider literature and both
  *verified by this repository's tests* rather than cited.

## 6. Exercises

1. Reconstruct the backward table of section 2 from shapes alone: given
   `dA (B, out)`, cached `X (B, in)` and `Z (B, out)`, and `W (in,
   out)`, argue the only matmuls that produce `(in, out)` for `dW`,
   `(out,)` for `db`, and `(B, in)` for `dX`. Then confirm each against
   `DenseLayer.backward`.
2. Hand-compute one backward pass: `X = [[1, 2]]`, `W = [[0.5],
   [-0.5]]`, `b = [0.25]`, activation sigmoid, and `dA = [[0.4]]`.
   Compute `Z`, `A`, `dZ`, `dW`, `db`, `dX`. Check against the code.
3. Verify the loss-returned-before-update semantics: run
   `train_step_mse` once and show the returned loss equals the
   pre-update loss, then that the *next* forward's loss is lower.
   Explain in one sentence why returning the pre-update loss is the
   honest choice for a loss curve.
4. The linear control of section 4 predicts `[0.5, 0.5, 0.5, 0.5]` at
   loss 0.25. Show this is *the* optimum for any linear model on XOR
   with MSE (not just ours): with predictions `pᵢ = w·xᵢ + b`, set
   `∂L/∂w = 0` and `∂L/∂b = 0` and solve.
5. Modify the XOR run: hidden width 4 → 2. Does it still converge at
   lr 0.5 within 4000 epochs? Try seeds 42/43 vs 7/8. Report what you
   find and connect it to module 07's *architecture search* framing
   (initialization and capacity are search variables, not constants).

### Solutions

1. `dW` must be `(in, out)`; the only cached tensors with the needed
   dimensions are `Xᵀ (in, B)` and `dZ (B, out)` — their product is
   forced, and its `(i, j)` entry is `Σ_batch x_b,i · dz_b,j`: the
   gradient of a dot-product weight accumulates over the batch, which
   is also why `dW` is a *sum* of per-example outer products. `db`:
   bias enters `Z` additively per column, so each `dz_b,j` routes to
   it with coefficient 1 — the column-sum. `dX`: the only product
   giving `(B, in)` is `dZ @ Wᵀ`; entry `(b, i)` is `Σ_out dz_b,j ·
   W_ij`, the sensitivity of the loss to input feature `i` through
   *every* output unit it feeds. All three are what
   `DenseLayer.backward` computes.
2. `Z = 1·0.5 + 2·(−0.5) + 0.25 = −0.25`; `A = sigmoid(−0.25) =
   0.4378`. `act'(Z) = 0.4378·0.5622 = 0.2461`. `dZ = 0.4·0.2461 =
   0.09846`. `dW = Xᵀ @ dZ = [[0.0985], [0.1969]]` (the second weight
   gets twice the gradient — it sees twice the input). `db =
   [0.0985]`. `dX = dZ @ Wᵀ = [[0.0492, −0.0492]]`. (The code
   produces exactly these values — pinned by the same arithmetic in
   the gradient-check tests at tolerance 1e-5.)
3. `train_step_mse` computes `loss` from the forward pass *before*
   `sgd_step` mutates the weights, so the returned value describes the
   batch the step trained on — the honest curve, because a curve of
   post-update losses would report each batch's loss under *different*
   weights than the ones that produced it, mixing two runs into one
   series. The test `test_sgd_step_reduces_loss` pins both facts.
4. With `L = (1/4)Σᵢ(pᵢ − yᵢ)²` and `pᵢ = w₁x₁ + w₂x₂ + b`:
   `∂L/∂b = (1/2)Σ(pᵢ − yᵢ) = 0` gives `Σpᵢ = Σyᵢ = 2`. `∂L/∂w₁ =
   (1/2)Σ(pᵢ−yᵢ)x₁ᵢ = 0`: summing over rows with `x₁ = 1` (rows 3, 4)
   gives `p₃ + p₄ = y₃ + y₄ = 1`; similarly `p₁ + p₂ = 1` (rows with
   `x₂ = 1`: `p₂ + p₄ = 1`). Solving: `p₁ = p₄`, `p₂ = p₃`, and with
   `Σp = 2` all four equations are satisfied by `p₁ = p₄ = a`, `p₂ =
   p₃ = 1 − a` for *any* a — a one-parameter family of stationary
   points. But linearity forces `p₄ − p₂ = w₁·(1−0) + w₂·(1−1)... `:
   in fact `p₄ − p₂ = w₁` while the XOR labels want `p₄ − p₂ = −1` and
   `p₂ − p₁ = +1` with `p₄ − p₁ = w₁ + w₂` needing to be 0, so `w₁ =
   −w₂` and `w₁ = w₂` → `w = 0` → every `pᵢ = b = 0.5`, loss
   `((0.5)²·4)/4 = 0.25`. The family collapses to the mean — the
   gradient's only reachable stationary point is the useless one, at
   exactly the loss our control run reports.
5. With width 2, both seed pairs tried converge within 4000 epochs at
   lr 0.5 — seeds 42/43: loss 0.4062 → 0.0005 with final predictions
   [0.019, 0.976, 0.976, 0.017]; seeds 7/8: 0.2509 → 0.0005 with
   [0.025, 0.981, 0.981, 0.026]. Two hidden units suffice for XOR's
   two-line carve (the classic minimum capacity), and neither pair
   stalls permanently. The honest observations that remain: the
   *initial* loss differs by seed (0.41 vs 0.25 — the seeded init
   places the carve differently), the epoch at which loss crosses
   0.01 varies, and width-4 reached 0.0003 where width-2 reaches
   0.0005 — capacity and initialization are variables that change
   outcomes, which is precisely why the companion repo's experiment 3
   searches expert counts and module 07 treats search as a
   first-class research skill.

## 7. Readings and provenance

- SRC-VIDEO-001 — *Become AI Researcher From Scratch - Full Course*
  (video chapters: *Neural Network Layers*; *How Networks Learn*).
  Access: page-inspected 2026-10-22.
- SRC-REPO-001 — vukrosic/zero-to-ai-researcher, module
  `06_neural_network_from_scratch` (lessons 01 architecture … 07
  implementing backpropagation; the chain-rule-first sequencing and
  the build-a-layer/build-a-network progression follow it). Access:
  full-text-read 2026-10-22 (cloned).
- XOR as the depth demonstration and finite-difference gradient
  checking are standard practice across the field, unattributed here;
  both are *executed and pinned* by this repository's tests rather
  than cited — the track's arrangement for elementary facts.
