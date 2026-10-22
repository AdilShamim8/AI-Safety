# Module 1 — Math foundations: functions, derivatives, gradients, vectors, matrices

> Track: [AI Researcher From Scratch](README.md) · module 1 of 7.
> Video chapters: *Math for AI*, *AI Math Roadmap* (SRC-VIDEO-001,
> page-inspected). Written companion: the `02_math_not_scary` module of
> vukrosic/zero-to-ai-researcher (SRC-REPO-001, full-text-read — five
> lessons: functions, derivatives, gradients, vectors, matrices).
> Code: `tensors.py` (module 2's commit, alongside its own note) carries
> this module's vectors and matrices as runnable code; this note's
> arithmetic is all hand-checkable.

## 0. Why this module exists

Everything in the rest of the track — the neuron, the trained network, the
GPT — is five mathematical objects used together: a **function** (the
model is one), a **derivative** (how the loss moves when a weight moves),
a **gradient** (all those derivatives stacked into a vector), **vectors**
(how data and parameters are stored), and **matrices** (how a layer
actually computes). The companion repo calls this module "math not scary",
and the name is the right attitude: none of this needs a calculus course
first. What it needs is the *rate-of-change* reading of each symbol,
because that reading is the one training uses. When module 4 makes a
network learn, the entire learning step is: compute a gradient, take a
small step against it, repeat. If you can compute one derivative and one
matrix product by hand, you can follow every line.

A note on honesty about the sources: the video's spoken explanations were
not retrievable (page-inspected only), so the intuition-first style below
(the machine, the car, the mountain) follows the *written* companion
lessons, which use exactly those devices. Nothing here quotes the video's
words; the chapter titles anchor which segments of the video this module
pairs with when you watch it.

## 1. Functions — the model is one

A function is a mapping from inputs to outputs with the property that the
same input always produces the same output. The companion lesson's device
is the machine: something goes in, one thing comes out, and the machine is
deterministic. Notation: `f(x) = y`, where `x` is the input (independent
variable) and `y` the output (dependent variable). Formally `f: A → B`
maps every element of set `A` to exactly one element of set `B`.

**Hand calculation** (do these yourself; they take seconds). For the
linear function `f(x) = 2x + 3`:

- `f(1) = 2(1) + 3 = 5`
- `f(0) = 3`
- `f(-1) = 2(-1) + 3 = 1`

For the quadratic `g(x) = x² + 2x + 1`:

- `g(2) = 4 + 4 + 1 = 9`
- `g(0) = 1`
- `g(-1) = 1 - 2 + 1 = 0`

Two vocabulary moves matter for the rest of the track. First,
**composition**: if `h(x) = f(g(x))`, then `h` is *g into f* — and a
neural network is nothing but composed functions
(`activation(linear(activation(linear(x))))`), which is why the chain rule
(module 4) is the engine of all learning. Second, the two families you
will meet as named objects: **activation functions** (module 3's ReLU,
sigmoid, tanh, SiLU, SwiGLU, softmax — the nonlinear *kinks* that let
stacked layers express more than one big linear map) and **loss
functions** (the scalar score of how wrong a prediction was). The model
is a function; the loss is a function *of the model's output*; training
is adjusting the first to shrink the second.

The one conceptual trap to disarm now: `f(1)` is not `f * 1`. The
parentheses are application, not multiplication. The companion lesson
flags this explicitly because it is the single most common notation slip
when people start substituting numbers into formulas by hand.

## 2. Derivatives — how the loss moves when a weight moves

The derivative measures instantaneous rate of change: how much the output
nudges when the input nudges. The companion lesson's device is the car:
position is a function of time, speed is its derivative — speed *is* the
"position change per unit time" reading, taken to the limit. Definition:

```text
f'(x) = lim(h→0) [f(x + h) − f(x)] / h
```

Read it as a *question and an answer*: the question is "over a tiny
interval `h`, what is the average slope?", and the derivative is the
answer when `h` shrinks to nothing. Two worked examples, one of which the
whole track reuses:

**Example A — `f(x) = x²` has `f'(x) = 2x`.** By the definition:
`[f(x+h) − f(x)]/h = [(x+h)² − x²]/h = [2xh + h²]/h = 2x + h`, which goes
to `2x` as `h` vanishes. At `x = 3`, the slope is `6`: a 0.01 nudge to
the input moves the output by about `0.06`. (Check: `3.01² = 9.0601`,
versus `9 + 0.06 = 9.06` — the definition's approximation is good to
`0.0001` here, which is the `h²` term showing through.)

**Example B — `f(x) = 2x + 3` has `f'(x) = 2`, everywhere.** Linear
functions have constant slope; that constant is the coefficient. A layer
without activations would be a stack of these, and its whole derivative
structure would be the product of the coefficients — this is exactly why
linear-only stacks collapse: their expressiveness cannot grow with depth.

Rules you will actually use (each derivable from the definition in one
line): the power rule `d/dx xⁿ = n·xⁿ⁻¹`; the constant multiple; the sum
rule; and the **chain rule** for composition — if `h(x) = f(g(x))` then
`h'(x) = f'(g(x)) · g'(x)`. The chain rule deserves one slow sentence:
*"the outer machine's sensitivity, evaluated at the inner machine's
output, times the inner machine's sensitivity."* Backpropagation
(module 4) is this sentence applied recursively to every layer.

**Partial derivatives** extend the idea to functions of several inputs:
`∂f/∂x₁` is the ordinary derivative *holding the other inputs fixed*.
For `f(x₁, x₂) = x₁² + 3·x₁·x₂`: `∂f/∂x₁ = 2x₁ + 3x₂` and
`∂f/∂x₂ = 3x₁`. Each partial answers "which way does the loss move if I
move *only this one* knob?" — and the next section is what happens when
you refuse to choose just one.

## 3. Gradients — all the knobs at once

The gradient is the vector of all partial derivatives. For
`f(x₁, …, xₙ)`:

```text
∇f = [∂f/∂x₁, ∂f/∂x₂, …, ∂f/∂xₙ]
```

The companion lesson's device is the mountain: stand somewhere, and the
gradient points in the direction of steepest *ascent*; its magnitude is
how steep; the *negative* gradient is the direction of steepest descent.
**Gradient descent** is therefore one line of pseudo-code:

```text
repeat:  w ← w − η · ∇f(w)
```

where `η` (eta) is the learning rate — the step size. The mountain device
also explains why the learning rate matters (module 7 studies it as a
real experiment): too large a step in steep terrain and you leap across
the valley to higher ground than you left; too small and the descent
takes forever. The source's own learning-rate search (companion repo,
experiment 2) exists because the right `η` is architecture- and
scale-dependent, not a constant of nature.

**Worked example** (hand-checkable, and exactly the shape of a training
step). Take `f(w₁, w₂) = w₁² + w₂²` (a parabolic bowl), start at
`(3, 4)`, learning rate `η = 0.1`:

- Gradient: `∇f = (2w₁, 2w₂) = (6, 8)` at the start.
- Step: `w ← (3, 4) − 0.1 · (6, 8) = (2.4, 3.2)`.
- Loss before: `9 + 16 = 25`. Loss after: `5.76 + 10.24 = 16`. One step
  cut the loss by 36%; the distance to the minimum shrank from `5` to
  `4` — exactly factor `1 − 2η = 0.8` per step for this bowl (see the
  exercise).

This is *the* computation of machine learning, at its smallest. Module
4's network training loop is this paragraph with a few hundred more
partials, computed by the chain rule instead of by hand.

## 4. Vectors — how data and parameters live

A vector is an ordered list of numbers. The companion lesson's device is
directions: "walk 4 blocks east, 3 blocks north" is the vector `[4, 3]` —
a package of distance and direction. In this track vectors are less about
geometry and more about *storage with arithmetic*: a data point's
features, a token's embedding (module 2), a layer's weights (module 4) —
all vectors.

Two properties and three operations carry the whole track:

- **Magnitude** (length): `‖v‖ = √(Σvᵢ²)`. For `[4, 3]`:
  `√(16+9) = √25 = 5`. This is the Pythagorean theorem by another name,
  and it is why module 3's softmax and module 5's scaled attention divide
  by square roots — to keep magnitudes (and therefore gradients) sane.
- **Direction**: the way the arrow points; normalize by dividing by the
  magnitude.
- **Addition** (element-wise) and **scalar multiplication**: the two
  operations that make vectors a *vector space*. `[4,3] + [0,2] = [4,5]`;
  `0.5 · [4,3] = [2,1.5]`.
- **Dot product** `a · b = Σ aᵢbᵢ`: one number measuring *alignment*.
  `[4,3]·[4,3] = 25` (a vector with itself: the squared magnitude);
  `[4,3]·[3,-4] = 12−12 = 0` (perpendicular); `[1,0]·[-2,0] = -2`
  (opposed). Attention (module 5) is a dot product at its core — "how
  aligned is this query with that key?" — so the sign and size of dot
  products is worth internalizing now.

The cosine-similarity reading `cos(θ) = (a·b)/(‖a‖‖b‖)` turns the dot
product into a normalized alignment score in `[-1, 1]`; it is how the
safety literature measures embedding-space direction (chapter 11's
refusal direction is exactly such a direction), and it appears again in
module 2's tokenization discussion.

## 5. Matrices — how a layer actually computes

A matrix is a rectangular grid of numbers — the companion lesson's
device is the spreadsheet: one row per student, one column per exam. A
matrix is also *a stack of vectors* (rows or columns), and — the reading
that matters here — *a function*: a matrix maps an input vector to an
output vector by a fixed rule.

Three operations, one of which is the track's heartbeat:

- **Shape**: a `m×n` matrix has `m` rows, `n` columns.
- **Transpose** `Aᵀ`: rows become columns; `(Aᵀ)ᵢⱼ = Aⱼᵢ`. Module 5's
  attention uses transposes constantly (queries against keys).
- **Matrix multiplication** `C = A·B`: `Cᵢⱼ` is the dot product of row `i`
  of `A` with column `j` of `B`. Shape rule: `(m×n)·(n×p) = (m×p)` — the
  inner dimensions must agree, and the inner agreement is *where the dot
  products come from*.

**Worked example** — a one-layer "network" on a toy dataset. Let

```text
      [ 1  2 ]        [1]         [ 1·1 + 2·2 ]   [ 5 ]
W  =  [ 3  4 ]    x = [2]    Wx = [ 3·1 + 4·2 ] = [11]
      [ 5  6 ]                     [ 5·1 + 6·2 ]   [17]
```

Each output is a dot product of one row of weights with the input: the
layer computes all its dot products at once. A batch of inputs is a
matrix `X` whose rows are examples, and the whole forward pass of a
linear layer is the single product `X·Wᵀ`. When the video's *Matrix
Multiplication* chapter says this is "the core operation of neural
networks", this paragraph — with the multiplication actually written out
— is the whole content of the claim.

Non-negotiable properties, each one line of checking: multiplication is
**not commutative** in general (try `A·B` vs `B·A` on the 2×2 case
above), it **is** associative, `(A·B)ᵀ = Bᵀ·Aᵀ`, and shapes must match or
the product is undefined. Every from-scratch bug you will write in this
track is a shape bug; `tensors.py` (next commit) exists partly so the
shape error messages are yours and readable.

## 6. Where this connects

- **To the track**: module 2 builds the tensor container (vectors and
  matrices as nested lists with the operations above); module 3 adds the
  activation kinks; module 4 is the gradient paragraph at scale; module
  5 is dot products deciding attention.
- **To the safety curriculum**: chapter 09's residual stream and
  chapter 11's refusal direction are *vectors in the model*; the
  steering vector arithmetic (add/ablate a direction) is vector addition
  and scalar multiplication, exactly as written in section 4. Chapter
  10's feature-absorption analysis is a statement about matrix rank and
  feature directions. You cannot read those chapters critically without
  this module's fluency.
- **To the sources**: functions/derivatives/gradients/vectors/matrices
  lesson sequence is the companion repo's `02_math_not_scary` module
  (SRC-REPO-001); the "Math for AI" and "AI Math Roadmap" video chapters
  (SRC-VIDEO-001) are the segments this note pairs with.

## 7. Exercises

1. Compute `f(-2)` and `f'(-2)` for `f(x) = 3x² − 2x + 1`. Then verify
   `f'` numerically: evaluate `[f(-2+0.001) − f(-2)]/0.001` and compare.
2. For `f(x₁, x₂, x₃) = x₁x₂ + x₂x₃ + x₃x₁`, write the gradient and
   evaluate it at `(1, 2, 3)`.
3. Run two more gradient-descent steps on the bowl
   `f = w₁² + w₂²` from section 3 (start `(3,4)`, `η = 0.1`; you already
   have step 1). What is the distance to the origin after each step?
   Conjecture the pattern; prove it for this bowl.
4. Compute `A·B` and `B·A` for `A = [[1,2],[3,4]]`,
   `B = [[0,1],[1,0]]`. Which entries differ?
5. Show that for the 2×2 identity-like case `W = [[1,0],[0,1]]`, `Wx = x`
   for any 2-vector `x` — and explain what that says about
   initialization (a weight matrix near identity passes signals through
   nearly unchanged; chapter 09's residual stream does this by design).

### Solutions

1. `f(-2) = 3(4) − 2(−2) + 1 = 12 + 4 + 1 = 17`. `f'(x) = 6x − 2`, so
   `f'(-2) = −14`. Numerical: `f(−1.999) = 3(3.996001) + 3.998 + 1 =
   11.988003 + 3.998 + 1 = 16.986003`; difference quotient
   `[16.986003 − 17]/0.001 = −13.997` — within 0.003% of the exact
   `−14`, and the gap is the `O(h)` truncation of the finite
   difference.
2. `∇f = (x₂+x₃, x₁+x₃, x₁+x₂)`; at `(1,2,3)` this is `(5, 4, 3)`.
   Check the middle partial against the definition: hold `x₁=1, x₃=3`,
   vary `x₂`: `f(1,x₂,3) = x₂ + 3x₂ + 3 = 4x₂ + 3`, slope `4`. ✓
3. Step 1: `(3,4) → (2.4, 3.2)`, distance `5 → 4`. Step 2: gradient at
   `(2.4,3.2)` is `(4.8, 6.4)`; new point `(2.4−0.48, 3.2−0.64) =
   (1.92, 2.56)`, distance `3.2`. Step 3: gradient `(3.84, 5.12)`; new
   point `(1.536, 2.048)`, distance `2.56`. Pattern: distance shrinks by
   exactly `1 − 2η = 0.8` per step. Proof: the update is
   `w ← w − η·2w = (1−2η)w`, a scalar contraction of the vector; for
   `η ∈ (0, 1)` the iterates spiral straight into the origin — and for
   `η > 1` they would blow up, which is the learning-rate lesson in
   miniature.
4. `A·B = [[2,1],[4,3]]`, `B·A = [[3,4],[1,2]]`. Both products are
   defined (square), but every off-diagonal entry differs: row/column
   order in the dot products differs. `B` here is a permutation matrix;
   left-multiplying by it swaps rows of `A`, right-multiplying swaps
   columns — a clean way to *see* non-commutativity as "row action vs
   column action".
5. `Wx` computes dot products of rows `[1,0]` and `[0,1]` with `x`,
   which select `x₁` and `x₂` respectively — the identity map. Near
   identity, `W = I + ε` gives `Wx = x + εx`: the signal passes with a
   small perturbation. Residual streams (chapter 09) add the identity as
   an explicit skip path (`x + f(x)`), which is the same trick made
   architectural: it guarantees the pass-through while letting the
   learned part be small.

## 8. Readings and provenance

- SRC-VIDEO-001 — *Become AI Researcher From Scratch - Full Course*
  (video chapters: *Math for AI*, *AI Math Roadmap*). Access:
  page-inspected 2026-10-22; watch these segments alongside this note.
- SRC-REPO-001 — vukrosic/zero-to-ai-researcher, module
  `02_math_not_scary` (five lessons: 01 functions, 02 derivatives, 03
  gradients, 04 vectors, 05 matrices). Access: full-text-read
  2026-10-22 (cloned). The intuition devices (machine, car, mountain,
  directions, spreadsheet) and the hand-calculation style follow these
  written lessons.
- The gradient-descent contraction analysis (exercise 3) is elementary
  and unattributed; the general discipline of pricing learning rates as
  architecture-dependent is the companion repo's experiment 2 design,
  covered in module 07.
