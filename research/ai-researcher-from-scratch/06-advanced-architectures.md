# Module 6 — Advanced architectures: latent attention and the mixture of experts

> Track: [AI Researcher From Scratch](README.md) · module 6 of 7.
> Written companion: modules `10_deepseek_latent_attention` (three
> lessons) and `11_glm4_moe` (three lessons) of
> vukrosic/zero-to-ai-researcher (SRC-REPO-001, full-text-read), plus
> the companion paper's abstract-level findings (claim `CLM-0073`).
> Code:
> [`moe.py`](../../src/ai_safety_course/from_scratch/moe.py); the
> numbers below were produced by running it or read directly from the
> cited sources.

## 0. Why this module exists

Module 05 built the transformer in its classical shape. This module
changes two of its parts — the *mixer* and the *feedforward* — in the
two directions production models actually scale: attention that costs
less per token, and feedforward layers that add capacity without
adding per-token compute. Both ideas come from the companion
repository's advanced modules, and both are variations on module 05's
code rather than new machinery: latent attention is three
cross-attentions chained through a bottleneck, and the mixture of
experts is the SwiGLU block behind a learned router. Building them
once at toy scale is what makes the architecture names in papers —
"MLA", "MoE", "sparse activation" — parse as *engineering decisions
with costs and trades* instead of vocabulary.

The module is also where the track's honesty discipline meets
impressive-sounding numbers head-on: the companion paper's headline
results (an 8.7× ablation gap, a 3e-3 optimal learning rate, 4 experts
beating 8) are carried at exactly their evidence strength —
self-reported, single-setup, abstract-level — and the note's closing
section shows how to *read* such numbers rather than repeat them.

## 1. Latent attention — the bottleneck trick, as the companion teaches it

The companion's module 10 poses the problem in one paragraph:
self-attention is all-to-all, so its cost grows with the square of the
sequence — 100 tokens → 10,000 attention pairs; 10,000 tokens →
100,000,000. The *latent* solution it teaches inserts a small set of
**M learnable "summary tokens"** between input and output, and routes
all information through them in three steps:

```text
1. gather      h = attn(Q = L, K = X, V = X)   latents read every input
2. confer      z = attn(Q = h, K = h, V = h)   latents mix among themselves
3. broadcast   y = attn(Q = X, K = z, V = z)   inputs read the summaries
               out = X + y                     (residual, as in module 05)
```

`L` is a parameter matrix (M × d_model), learned like any weight; the
companion's device is "reporters" — each latent gathers a summary of
some slice of the sequence, the reporters confer, then every token
reads back the pooled summary instead of every other token. The
arithmetic, from our `attention_pairs` (a function, not a slogan):

| N tokens | dense pairs | latent pairs (M = 64) | reduction |
| --- | --- | --- | --- |
| 1,000 | 1,000,000 | 132,096 | 7.6× |
| 10,000 | 100,000,000 | 1,296,409+... → 2·10⁴·64 + 64² = 1,296,409 | 77× |

Honest pricing, two notes on it. First, the companion lesson's headline
"16×" for N = 1000, M = 64 counts *only the gather step* (N·M = 64,000
vs N² = 1,000,000); counting all three steps the reduction is 7.6×,
and it grows with N (the M² confer term fades). Second, the reduction
buys a *bottleneck*: information that does not survive the M-token
compression is gone — the same trade as any summary, and the reason
latent counts and placement are research variables (module 07's
search discipline applies to them exactly as it applies to learning
rates and expert counts).

**The other latent trick, stated so the names don't blur.** What
DeepSeek's production models call MLA (multi-head latent attention)
is a *different* mechanism with the same marketing word: low-rank
projections — the companion paper's head lists "LoRA-style Q/K/V
projections" among DeepSeek's components — where Q and K are computed
through a small rank-r bottleneck (`X @ W_down @ W_up`), shrinking
parameters and the KV cache rather than attention pairs. Our
`LatentAttention` implements the companion's *latent-token* version,
because that is what its module 10 actually teaches; the low-rank
version is one exercise away (exercise 4) and its trade is stated
there. Confusing the two is common and worth one deliberate
un-confusion: **latent tokens change what attention *computes over*;
latent (low-rank) projections change how the *projections are
parameterized*.**

The code reuses module 05 unchanged where it can: `cross_attention`
is the core op with the shape rule relaxed (Q may have Tq rows, K/V
Tk — "latents attend to inputs" and "inputs attend to latents" both
need exactly that), and `cross_attention_backward` is the same factor
list (`dV = Wᵀ dOut`, `dW = dOut Vᵀ`, collapsed softmax Jacobian,
scaled `dQ`/`dK`). The full backward — three chained
cross-attentions, two projections, the residual, *and the learnable
latents themselves* — is gradient-checked against finite differences
for every parameter family, the same discipline as modules 04–05.

## 2. The sparse mixture of experts — capacity without per-token cost

The companion's module 11 recap: a standard FFN gives every token the
same capacity; a mixture of experts (MoE) replaces it with E parallel
FFNs and a **router** that picks, per token, which few actually run.
GLM-4-class models scale this hard — the companion's architecture
lesson cites 64–128 experts with top-2/top-4 routing, each expert a
substantial FFN, for total parameters in the hundreds of billions
while per-token compute stays flat (summary-level statements from the
lesson text; the production configurations live in the papers it
points to).

Our `SparseMoE` is the mechanism at inspectable scale:

```text
logits = X @ W_router                    (T, E) — the router scores
s      = softmax(logits)                 per-token distribution over experts
top-k  = the k largest s_i               (k = top_k, e.g. 2 of 4)
out_t  = Σ_{i ∈ top-k} s_i · E_i(x_t)    only the selected experts run
```

Three properties, each pinned by a test, are what make this an
*architecture* and not just an ensemble:

**Selection is learned, not assigned.** The router is a plain matmul
whose rows compete through a softmax; which experts a token picks
depends on the token (our routing test shows different tokens picking
different expert sets from the same seeded router), and the *router's
own weights* are trained by gradient through the selection — the
collapsed softmax Jacobian of module 03, with `dL/ds_i = 0` on
non-selected experts, flows into `dW_router = Xᵀ @ dL/dlogits` exactly
as in any dense layer. The gradient-check test perturbs router
entries by ±10⁻⁶ and the analytic gradient matches.

**Sparsity is real in both directions.** A non-selected expert
computes nothing in the forward (it is not even *called* on that
token's batch) and receives *exactly zero gradient* in the backward —
the unselected-experts test asserts all-zero gradient tensors, and the
frozen-experts test asserts their weights do not move under
`sgd_step`. This double sparsity is the entire economics of MoE: you
pay compute proportional to k, not E, and the training signal
concentrates on the experts that actually ran. The catch has a name —
**load imbalance**: if the router collapses onto a few favorites,
most parameters sit idle and the effective model is small; production
training adds auxiliary balance losses, which is the note's exercise
5 and the honest "what we did NOT implement" line.

**The weights are the softmax scores, not renormalized.** Our mix uses
the selected experts' raw softmax scores `s_i` (which sum to less than
1 over the selection); renormalizing to sum to 1 (a common variant)
changes the gradient structure slightly. The choice is stated in the
docstring; the exercise 3 asks you to derive the difference.

The backward's one subtle factor — worth a sentence because the
gradient check caught a real bug here during development: with
`out = s_i · E_i(x)`, the routing weight enters the expert's upstream
*once* (`dL/dE_i = s_i · dOut`), and the expert's returned `dX`
contribution needs no further scaling; the first implementation
multiplied by `s_i` twice, the finite-difference check disagreed by
exactly the `s_i` factor, and the fix is in the commit history with
the bug preserved — the gradient-check discipline earning its keep on
day one.

## 3. Reading the paper's numbers — the module's honesty lesson

The companion repository's paper (`ai_research_paper.md`, read at head
level; SRC-REPO-001) reports, at abstract strength: an **8.7×**
validation-performance gap between the best and worst of five
ablation configurations; **3e-3** as the identified optimal learning
rate for its DeepSeek-attention+MLP setup (0.015 validation loss,
99.7% accuracy as stated); and **4 experts with top-2 routing** as the
best DeepSeek-attention+GLM-4-MoE configuration (0.061 validation
loss, 98.7% accuracy as stated) — all positioned under a
"train-an-LLM-for-a-dollar" consumer-GPU framing (claim `CLM-0073`).

How this course carries those numbers is the lesson:

- **Self-reported, single setup**: no independent replication exists;
  the numbers describe *their* configurations on *their* data at
  *their* scale. They are evidence that the authors' searches found
  these optima — not that 3e-3 transfers to your architecture (module
  03's exercise 5 already showed the safe learning rate is
  curvature-dependent, and module 07's LR-search protocol exists
  because of exactly this).
- **Abstract-level**: the paper's experiment sections and figures were
  not read; per-run variance, seeds, and the ablation table's actual
  contents are outside our evidence. The honest phrasing is
  "reported", never "shown" or "demonstrated".
- **The framing is a framing**: "under one dollar" is a hardware-cost
  narrative, not an audited cost accounting — the course's own P02
  project exists because cost claims deserve ledgers, not adjectives.

None of this diminishes the work — it *prices* it. The same discipline
applies to the GLM-4 lesson's 64–128-expert figures (summary-level
statements from the lesson, pointing at papers we did not fetch) and
to the companion's 16× headline (true for the gather step, 7.6× for
the whole pipeline — both stated in section 1). A researcher who
reads numbers this way — evidence class first, transferability second,
narrative last — is strictly harder to fool, which is the point of a
track that sits inside an AI-safety curriculum.

## 4. Where this connects

- **To the track**: module 07 turns the architecture choices this
  module exposed (expert counts, top-k, latent counts, learning
  rates) into the *research methodology* the companion repo teaches —
  ablation, LR search, expert search — as preregistered protocols.
- **To the safety curriculum**: sparse routing is a *safety-relevant*
  architecture choice — chapter 03's specification gaming and P02's
  reward misspecification both become subtler when only k-of-E
  pathways receive gradient (dead experts, router collapse, and
  expert-specialization-on-unsafe-behavior are the failure families);
  the main curriculum's chapter on model organisms of misalignment
  (07) analyzes deceptive behaviors that live *in specific
  pathways*, and pathway-level sparsity is what makes "which
  pathway" a well-posed question.
- **To the sources**: latent attention's three-step structure, the
  N² cost framing, and the reporters device follow companion module
  10 (SRC-REPO-001); the router/top-k/GLM-4 figures follow module 11;
  the paper numbers follow the paper's head at abstract level.

## 5. Exercises

1. Compute, by hand or with `attention_pairs`: the dense and latent
   pair counts for N = 500, M = 32, and the reduction factor. Then
   find the N at which the latent route breaks even for M = 64 (the
   N where 2NM + M² = N²), and explain why *small* sequences should
   not use latent attention.
2. Our `LatentAttention` confers with plain cross-attention over the
   gathered latents. Replace step 2 with an *identity* (z_raw = h) in
   a copy of the class and re-run the gradient-check logic mentally:
   which cached patterns become unused, and which gradients (dQ of
   step 1? dK/dV of step 2?) change or vanish?
3. Derive the gradient difference between our raw-score mix
   (`out = Σ s_i E_i`) and the renormalized variant
   (`out = Σ (s_i / Σ_selected s_j) E_i`): in the renormalized case,
   what extra term appears in `dL/ds_j` for *non-selected* j, and
   what does that imply about gradient flow to the router?
4. The low-rank variant: write (on paper or in a copy) a
   `LowRankAttention` whose Q and K go through `X @ W_down @ W_up`
   with rank r = d/4, V full-rank. Count parameters for d_model = 64
   versus module 05's `MultiHeadAttention`, and state what the KV
   cache stores in each design at generation time.
5. Load balance: instrument `SparseMoE.forward` to record, per expert,
   the number of tokens routed to it across a batch of 50 random
   tokens with a seeded router. Report the distribution. Then write
   one paragraph on what an auxiliary load-balance loss would have
   to add to the backward (which gradients, which sign) to flatten
   it — and one honest sentence on what your instrumented run can
   and cannot conclude.

### Solutions

1. Dense: 500² = 250,000. Latent: 2·500·32 + 32² = 32,000 + 1,024 =
   33,024 — a 7.57× reduction. Break-even for M = 64: 2N·64 + 64² =
   N² → N² − 128N − 4,096 = 0 → N = (128 + √(16,384 + 16,384))/2 =
   (128 + √32,768)/2 ≈ (128 + 181.0)/2 ≈ 154.5. Below N ≈ 155, the
   latent route costs *more* pairs than dense attention — the
   bottleneck is overhead, not savings, on short sequences (and the
   fixed M·d latent parameters and projections add their own constant
   cost, pushing the practical break-even higher).
2. With z_raw = h: the step-2 cross-attention and its pattern cache
   `_w2` disappear; backward loses the `dh_q + dh_k + dh_v` split
   (step 2's backward was what produced it — with the identity, the
   broadcast's `dz` flows directly into the `w_up` projection's
   backward). The step-1 gradients (dQ → latents; dK/dV → inputs)
   survive unchanged in *form* but change in *value* because the
   forward values of `z` changed (no confer step means different
   keys/values for the broadcast). The gradient checks would still
   pass after the edit — they verify whatever forward you actually
   run — which is itself the lesson: checks pin consistency, not
   architecture choice.
3. In the renormalized case, out = Σ (s_i / S) E_i with S =
   Σ_selected s_j. The weight on E_i is w_i = s_i/S, whose derivative
   w.r.t. s_j for *non-selected* j is −(s_i/S²)·(∂S/∂s_j) = 0 — wait,
   carefully: S sums only selected scores, so ∂S/∂s_j = 0 for
   non-selected j, and ∂w_i/∂s_j = 0 as well. The surprise: *no*
   extra term appears for non-selected j — renormalization still
   routes them zero gradient. The difference is elsewhere: for
   selected j, ∂w_i/∂s_j = (δ_ij S − s_i)/S² — the router's gradient
   for a selected logit now includes the −s_i/S² cross-terms from
   every selected expert's weight, making the router's landscape
   steeper (weights sum to 1 over the selection, so raising one
   selected score must lower the others' normalized weights). The
   honest correction to the naive expectation: renormalization
   changes the *selected* experts' gradient coupling, not the
   unselected ones' zeros.
4. Parameters (d = 64): module 05's MHA uses 4 matrices of d² = 4,096
   → 16,384. Low-rank Q and K with r = 16: W_down (64×16) + W_up
   (16×64) = 2·1,024 = 2,048 each → 4,096 for both, plus full-rank V
   and W_o (4,096 + 4,096) → 12,288 total, a 25% parameter cut. The
   KV cache: dense stores K and V rows per token (2·d per token per
   head-scale); low-rank can cache the *latent* `X @ W_down` (r = 16
   dims) and recompute K's up-projection at use time — a 4× smaller
   K-side cache at the cost of one extra matmul per attended
   position. That cache/compute trade is the actual production
   argument for MLA-style designs.
5. Instrumented run (our code, router seed 70, tokens seed 71, 50
   tokens, 4 experts, top-1): per-expert counts {0: 20, 1: 4, 2: 8,
   3: 18} — max/min ratio 5× (your seeds will differ; the *shape* —
   favorites plus a starving tail — is the robust observation). An
   auxiliary loss would add a term penalizing deviation of the
   per-expert token shares from uniform (e.g. E·Σ_i (f_i − 1/E)² on
   the batch's routing frequencies f_i), whose gradient flows into
   the router logits with the sign that raises *starving* experts'
   scores on tokens they currently lose — at the cost of fighting the
   task loss (the balance/performance tension every production MoE
   paper negotiates). What the run cannot conclude: anything about
   training dynamics — a single forward's routing distribution under
   a random-init router says nothing about the equilibrium the joint
   loss will reach, which is exactly why the companion repo's
   experiment 3 searches expert *configurations* rather than
   asserting one.

## 6. Readings and provenance

- SRC-REPO-001 — vukrosic/zero-to-ai-researcher: module
  `10_deepseek_latent_attention` (lessons 01–03: the latent-token
  bottleneck with the N² cost framing and the reporters device, the
  three-stage DeepSeek framing, the implementation outline — our
  `LatentAttention` follows them) and module `11_glm4_moe` (lessons
  01–03: MoE recap, the GLM-4 architecture lesson whose 64–128-expert
  and top-2/top-4 figures are cited here at summary level, the
  implementation outline). Access: full-text-read 2026-10-22 (cloned).
- The companion paper's abstract-level findings (8.7×; 3e-3; 4
  experts, top-2) are carried under claim `CLM-0073` at
  abstract-read strength with the pricing of section 3 —
  self-reported, single-setup, unreplicated, sections unread.
- The renormalization gradient analysis (exercise 3) and the
  break-even arithmetic (exercise 1) are elementary derivations done
  for this note, unattributed; both are small enough to check by
  hand, and the repository's tests pin the pieces the code executes.
