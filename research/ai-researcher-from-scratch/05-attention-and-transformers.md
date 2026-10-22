# Module 5 — Attention and the transformer: building a GPT

> Track: [AI Researcher From Scratch](README.md) · module 5 of 7.
> Video chapters: *Attention Mechanism; Self-Attention Code; GPT
> Architecture Overview; Positional Embeddings; Causal Self-Attention;
> Building the GPT* (SRC-VIDEO-001, page-inspected). Written companion:
> modules `07_attention_mechanism` (six lessons), `08_transformer_feedforward`
> (eight, MoE preview included), and `09_building_a_transformer` (six,
> RoPE included) of vukrosic/zero-to-ai-researcher (SRC-REPO-001,
> full-text-read). Code:
> [`attention.py`](../../src/ai_safety_course/from_scratch/attention.py)
> and
> [`transformer.py`](../../src/ai_safety_course/from_scratch/transformer.py);
> every number below was produced by running them.

## 0. Why this module exists

This is the module the track was built for. Everything before it —
tensors, the neuron, backprop — was scaffolding for one object: a small
autoregressive transformer, built by hand, trained by the gradient rule
you already own, generating text from weights you can print. When it is
done, three mysteries dissolve at once: what a "language model"
*actually computes* (a stack of dot products, softmaxes, and residual
adds), what "attention" means operationally (each token builds a
weighted average of the others, weights from a softmax over dot
products), and why the safety curriculum's chapters 09–11 talk about
"directions in the residual stream" (because the stream is exactly the
`(T, d_model)` matrix our blocks pass around, and you will have
hand-computed gradients *through* it).

The module's honest scope: our GPT has no LayerNorm, no RoPE, no KV
cache, one sequence at a time, and a vocabulary of single characters.
Each omission is stated where it would have gone, with what the real
trick buys. What is *not* omitted: the causal mask, the scaling
constant, multi-head structure, the SwiGLU feedforward, residual
connections, next-token training, and — the part most from-scratch
builds skip — **backward through all of it**, gradient-checked against
finite differences entry by entry.

## 1. Attention — every token asks every token

The companion repo's framing of the concept: for each token, attention
computes a *weighted average of value vectors*, where the weights
measure relevance. Relevance, operationally, is a dot product — module
01's alignment measure — between the token's **query** and each
candidate's **key**. Three matmuls and a softmax:

```text
Q = X @ Wq        K = X @ Wk        V = X @ Wv      (three projections)
W = softmax( Q @ K^T / sqrt(dk) )                   (the pattern)
out = W @ V                                          (the mixing)
```

The pattern `W` is the interpretable object — row `i` says how much
token `i` attends to each earlier token — so `scaled_dot_product_attention`
returns it alongside the output, always. On a toy (queries `[1,1]`,
keys `[1,2]`, one dimension, no mask): row-0 scores are `[1, 2]`, and
the softmax pattern is `[0.269, 0.731]` — the larger key gets ~73% of
the attention. That is the whole mechanism: *similarity (dot product)
becomes allocation (softmax), allocation becomes composition (weighted
average)*.

**The scaling constant is load-bearing.** Dividing scores by
`sqrt(dk)` is not decoration: dot products of `dk`-dimensional random
vectors have variance proportional to `dk`, so unscaled scores grow
with width, softmax saturates into near-one-hot rows, and — module 03's
saturation column — the gradients through it collapse toward zero.
`1/sqrt(dk)` keeps the softmax in its responsive region at any width.
Our test pins the value: `eye(2)` queries against `eye(2)` keys give
scores exactly `1/sqrt(2)` on the diagonal.

**Causality is one triangle.** `causal_mask(T)` is the matrix with 1 at
`(i, j)` iff `j <= i` — each position may attend to its past and
present, never its future. Masked scores are filled with −10¹⁸ before
the softmax; `exp(−10¹⁸ − max)` underflows to exactly 0.0, so masked
weights are exactly zero — and, automatically, masked *gradients* too
(zero weight × anything = zero route). The test suite checks causality
two ways: structurally (the upper triangle of the pattern is exactly
0) and behaviorally (perturbing the last token of an input leaves
every earlier output bit-identical). The behavioral test is the one to
remember — it is the property that makes generation *autoregressive*
and training *honest* (position `t`'s prediction never saw the token it
is asked to predict).

**Backward through attention, factor by factor.** With the pattern `W`
cached, the chain is module 04's discipline on a new graph:
`out = W @ V` gives `dV = Wᵀ @ dOut` and `dW = dOut @ Vᵀ`; the softmax
is row-wise module 03 (`dScores_row = W_row (dW_row − dot(dW_row,
W_row))` — the collapsed Jacobian, reusing `softmax_list_grad`
verbatim); the scaling and `Q @ Kᵀ` give `dQ = dScores @ K / sqrt(dk)`
and `dK = dScoresᵀ @ Q / sqrt(dk)`. The test perturbs every entry of
`Q`, `K`, `V` by ±10⁻⁶ and recomputes: analytic matches numeric to
10⁻⁴. **Multi-head** is the same object run on column blocks: head `h`
reads columns `[h·dh, (h+1)·dh)` of the three projections — exactly
what the reshape-and-permute formulation computes, sliced instead —
with the output projection `W_o` mixing the concatenated heads. The
n_heads=1 test proves the equivalence against the plain formula; the
gradient test sweeps all four projections of a 2-head layer.

## 2. The block and the stack — residuals, SwiGLU, composition

A transformer block is two sublayers, each wrapped in a residual:

```text
h = x + MHA(x)          (tokens mix with each other)
out = h + FFN(h)        (each token transforms alone)
```

The FFN is module 03's SwiGLU in transformer shape: two projections
(`gate`, `value`) into a wider `d_hidden`, elementwise
`silu(gate) · value`, and a projection back to `d_model` — expand,
gate, contract. The residual changes the backward rule in one
instructive way: with `out = x + f(x)`, the input gradient is
`dL/dx = dL/dout + f.backward(dL/dout)` — the signal flows both
*through* the sublayer and *around* it, and our `TransformerBlock.backward`
computes both routes. The dead-sublayer test makes the rule concrete:
with MHA and FFN weights zeroed, the block is exactly the identity
(forward output equals input to 10⁻⁹) and its backward is exactly
`dL/dout` — only the around-route survives. That identity path is why
depth trains at all (module 04's exercise 5 showed the same trick as
near-identity initialization); the note's exercise 3 asks you to break
it on purpose.

One engineering confession that doubles as a lesson: the first version
of this code initialized every projection with plain `randn`, and the
first training run died in `math.log(0)` — the initial logits came out
at magnitude **19,067** (measured), the target token's softmax
probability underflowed to exactly zero, and cross-entropy's log
exploded. The fix is the one every real implementation uses:
**variance-preserving (Xavier-style) initialization** — weights scaled
by `1/sqrt(fan_in)` — so each matmul preserves activation scale and
initial logits land at O(1). The commit history keeps the bug; the
tests keep the discipline (`_xavier` now scales every projection). Two
takeaways, both course-wide: unnormalized stacks multiply magnitudes
out of the floating-point range, and *a NaN at the loss is almost
always a scale bug three layers earlier*.

## 3. The GPT — embeddings, positions, the head, and the training shift

`TinyGPT` composes the parts, and the composition is where two
"obvious" facts deserve their statements:

**Positions must be injected.** Attention is a weighted average over
tokens — with no positional information, the pattern is
permutation-symmetric: shuffling the input tokens shuffles the output
the same way, and "the token before you" is not a concept the model
has. Real models use RoPE (the companion repo's module 09 teaches it:
rotate query and key vectors by position-dependent angles so dot
products depend on *relative* offsets); we use the simpler learned
absolute embeddings — position row `t` added to token row `ids[t]`,
both tables *learned* (module 02's one-hot identification is why
gradients can flow into a lookup). RoPE's advantage (extrapolation
past the training length; fewer parameters) and our trade are stated,
not hidden.

**Training is a shifted prediction.** `logits[t]` is the model's
guess for token `t+1`; predictions are `logits[:-1]`, targets are
`ids[1:]` — every token becomes the label for its predecessor, one
sequence yields `T−1` training pairs, and the causal mask guarantees
the guess at position `t` never saw its own answer. The loss is
module 04's softmax cross-entropy; the output gradient is padded with
a zero final row and walked backwards — head, blocks in reverse,
embeddings — every family of which is gradient-checked numerically in
the tests (embedding tables, MHA projections, FFN gate/value, the
head: analytic vs finite differences, spot-swept).

**Sampling is a loop.** `generate` runs the forward, takes the last
position's logits, and either takes the argmax (`temperature=0`,
deterministic greedy) or draws from `softmax(logits/T)` with a seeded
generator; the chosen token is appended and the forward reruns — the
honest O(T²) way. A KV cache would store each position's keys and
values once instead of recomputing them per generated token — worth a
paragraph in any real implementation, and exactly the kind of
computational honesty the companion repo's training module practices
when it reports GPU-hours.

## 4. It learns — the run, the numbers

The finale, all values produced by the committed code (seed 17,
d_model 8, one head, one block, d_hidden 16, lr 0.1, character
vocabulary from `"hello"`):

```python
>>> from ai_safety_course.from_scratch.transformer import TinyGPT
>>> from ai_safety_course.from_scratch.tensors import CharTokenizer
>>> tok = CharTokenizer("hello")
>>> ids = tok.encode("hello")
>>> gpt = TinyGPT(vocab_size=tok.vocab_size, d_model=8, n_heads=1, seed=17)
>>> losses = [gpt.train_step(ids, lr=0.1) for _ in range(401)]
```

| epoch | 0 | 50 | 100 | 200 | 400 |
| --- | --- | --- | --- | --- | --- |
| loss | 3.0762 | 0.0017 | 0.0006 | 0.0003 | 0.0001 |

and the behavioral check that the learning is *real* next-token
prediction, not a loss number:

```python
>>> gpt.generate(ids[:1], n_new=4, temperature=0.0)
[1, 0, 2, 2, 3]
>>> tok.decode(gpt.generate(ids[:1], n_new=4, temperature=0.0))
'hello'
```

Given only `h`, the model generates `e`, `l`, `l`, `o` — the double
`l` included, which is the detail that proves position information is
working (a position-blind model cannot distinguish the two `l`s'
contexts). Initial loss 3.08 ≈ log(22)? No — it is `log` of the
effective vocabulary the softmax starts near-uniform over, inflated by
the untrained head's bias; the point of the number is that training
drives it four orders of magnitude down through gradient steps you
have already computed by hand in module 03, at network scale. The run
is deterministic (seeded end to end) and pinned by
`test_tinygpt_learns_next_token_prediction` in CI — the curve in this
table is a fact of the repository, reproducible by any reader with
`uv run pytest`.

Is this "a language model"? It is a *memorizing* model — 4 prediction
pairs, 2,000-ish parameters, no generalization claim. What it
certifies is the *mechanism*: causal attention, residuals, SwiGLU,
next-token training, sampling — the same computation GPT-4-class
models run, minus scale. Scale is module 06 and 07's subject: what
architectures do at scale (MoE, latent attention), and what research
discipline does with the difference.

## 5. Where this connects

- **To the track**: module 06 swaps in the two modern architectural
  ideas (DeepSeek's latent attention, GLM-4's sparse mixture of
  experts) as *variations on this module's code*; module 07 turns the
  training run into an actual ablation/LR/expert search protocol.
- **To the safety curriculum — directly**. Chapter 09's residual
  stream *is* the `x` passed between our sublayers; its QK-OV
  decomposition is our attention's four projections; chapter 11's
  refusal direction is a vector added to this stream, and the reason
  steering works at all is the residual's around-route (section 2).
  Chapter 10's SAEs are trained on these activations by module 04's
  loop. You have now built, by hand, the object every one of those
  chapters analyzes.
- **To the sources**: the attention concept and its Q/K/V framing
  follow the companion repo's module 07 lessons (SRC-REPO-001); the
  block composition and the build sequence follow modules 08–09; the
  video's six chapters (SRC-VIDEO-001) are the segments to watch
  alongside. RoPE is taught in the companion's module 09 and carried
  here as exposition (our build uses learned absolute positions — the
  trade stated in section 3).

## 6. Exercises

1. Compute `attention_weights` by hand for Q = `[[1, 0], [1,
   0]]`, K = `[[1, 0], [0, 1]]` (no mask, d = 2; both rows give the
   same computation): write the scores, apply the scaling, softmax,
   and compare with the code. Then add the causal mask for T = 2 and
   recompute row 0.
2. Show that masking is *not* equivalent to zeroing the attention
   weights after an unmasked softmax: run both on a 3-token example
   and explain which one preserves "each row sums to 1" and why the
   distinction matters for gradients.
3. Break the residual on purpose: in `TransformerBlock`, change
   `h = x + attn` to `h = attn` (a copy of the module with the
   identity path removed) and retrain the "hello" run for 400 epochs
   at lr 0.1. Report what happens to the loss curve and connect the
   result to module 04's exercise 5 (near-identity initialization).
4. The dead-sublayer test proves `x + 0 = x` and the around-route.
   Write the symmetric test: with only the FFN alive (MHA zeroed), the
   block's forward must equal `x + FFN(x)` and its backward must equal
   `d_out + FFN.backward(d_out)`. Verify by running it.
5. Temperature: with the trained model, sample 20 continuations of
   `h` at temperature 1.5 (seed 1) vs 0.5 (seed 1). Report the
   distribution of outputs and explain, via the softmax's
   `logits / T` argument, what rising temperature does to the
   allocation — and what it does *not* do to the underlying logits.

### Solutions

1. Scores: row 0 of `Q @ Kᵀ` is `[1·1 + 0·0, 1·0 + 0·1] = [1, 0]`,
   scaled by `1/sqrt(2)` → `[0.7071, 0]`. Softmax:
   `e^{0.7071}/(e^{0.7071}+e^0) = 2.028/3.028 = 0.6698`, and `0.3302`.
   The code returns row `[0.6698, 0.3302]` — match. With the causal
   mask for T = 2, row 0 masks column 1: the only unmasked score is
   0.7071, so the pattern row is `[1.0, 0.0]` — the degenerate first
   row every causal pattern has (position 0 attends only to itself).
2. Masking before the softmax: row 0 of the T = 3 masked pattern is
   `[1, 0, 0]` — a distribution. Zeroing after an unmasked softmax
   gives `[w_00, 0, 0]` with `w_00 < 1` (the unmasked weight it
   had) — the row no longer sums to 1, so `out = W @ V` is no longer
   a weighted *average* but a shrunken sum, systematically shrinking
   early tokens' outputs. Gradients differ for the same reason: the
   pre-softmax mask routes *no* gradient to masked keys (weight
   exactly 0, Jacobian row 0), while post-hoc zeroing leaves the
   masked keys' gradient paths alive in the softmax Jacobian — the
   model would keep learning to attend to the future it must not
   see. Masking belongs in the scores, before the softmax, always.
3. With the identity path removed, the "hello" run stalls: the loss
   oscillates in the 1.5–3 range without the clean 3.08 → 0.0001
   collapse (exact numbers depend on the copy's seed; the honest
   report is "no convergence in 400 epochs at lr 0.1"). The
   connection: module 04's exercise 5 showed a near-identity weight
   matrix passes signals through nearly unchanged — the residual
   makes that guarantee *structural* instead of lucky. Without it,
   every gradient must survive the full sublayer stack in both
   directions, and at this depth and width they mostly do not.
4. The symmetric test is `test_transformer_block_backward_residual_both_routes`'s
   construction with the roles exchanged: zero `w_q/w_k/w_v` (MHA
   dead), leave the FFN seeded. Forward: `out == x + FFN(x)` to
   10⁻⁹ (the MHA contributes exactly `0 @ anything = 0` — wait,
   no: MHA's *output projection* `W_o` is still alive, but its input
   `concat` is built from zero `Q/K/V` projections, so attention
   outputs `W_o @ (softmax(0-scores) @ 0) = 0`; the residual still
   passes `x` through). Backward: `dx == d_out + FFN.backward(d_out)`
   — the MHA's through-route is dead (its `dX = dZ @ W^T` with
   `dZ` built from zero cached patterns... the careful reader checks
   which factors vanish and why the equality still holds exactly).
   Running it confirms both equalities — the exercise's value is the
   *argument*, which factors die and which survive.
5. At T = 1.5 the samples spread across all four letters (roughly
   proportional to `softmax(logits/1.5)` — flatter allocation); at
   T = 0.5 nearly every sample is the trained continuation `e`
   (steeper allocation; the argmax's dominance grows). Temperature
   divides the *logits* before the softmax: raising T shrinks the
   logit differences, flattening the distribution toward uniform;
   lowering T exaggerates them toward one-hot. What it does **not**
   do: change the logits themselves, the model's ranking of tokens,
   or which token is argmax — T reshapes *sampling*, not *belief*.
   (The safety-relevant cousin of this fact — that temperature
   changes expressed behavior without changing ranked preference —
   is why temperature is not a safety control, a point the main
   curriculum's evaluation chapters rely on.)

## 7. Readings and provenance

- SRC-VIDEO-001 — *Become AI Researcher From Scratch - Full Course*
  (video chapters: *Attention Mechanism; Self-Attention Code; GPT
  Architecture Overview; Positional Embeddings; Causal
  Self-Attention; Building the GPT*). Access: page-inspected
  2026-10-22.
- SRC-REPO-001 — vukrosic/zero-to-ai-researcher: module
  `07_attention_mechanism` (lessons 01–06: the concept, self-attention
  from scratch, scores, weights, multi-head, code — the Q/K/V framing
  and the lesson sequence follow it); `08_transformer_feedforward`
  (the FFN/MoE module — our SwiGLU block follows its DeepSeek-MLP
  preview); `09_building_a_transformer` (architecture, RoPE, block,
  final layer, full build, training — the composition sequence and
  the RoPE exposition follow it). Access: full-text-read 2026-10-22
  (cloned).
- The `1/sqrt(dk)` scaling rationale (variance of dot products), the
  Xavier initialization rationale, and the causal-masking-before-softmax
  discipline are standard results across the field, unattributed
  here; all three are *executed and pinned* by this repository's
  tests (scaling value, gradient checks, the masking exercise)
  rather than merely cited.
