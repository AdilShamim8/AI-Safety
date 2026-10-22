# Module 2 — Python and PyTorch fundamentals: the tensor toolbox by hand

> Track: [AI Researcher From Scratch](README.md) · module 2 of 7.
> Video chapters: *PyTorch Introduction; Tensor Operations; Creating
> Tensors; Matrix Multiplication; Transposing & Permuting; Indexing &
> Slicing; Concatenating Tensors; Special Tensors* (SRC-VIDEO-001,
> page-inspected). Written companion: `03_pytorch_fundamentals` of
> vukrosic/zero-to-ai-researcher (SRC-REPO-001, full-text-read — nine
> lessons; the ninth, tokenization and embeddings, closes this note).
> Code: this note is written against
> [`src/ai_safety_course/from_scratch/tensors.py`](../../src/ai_safety_course/from_scratch/tensors.py)
> — every snippet below runs against it unchanged.

## 0. Why this module exists

The video spends eight chapters inside one library — PyTorch — because
one data structure carries the entire rest of the track: the **tensor**.
The neuron is tensor arithmetic; the network is a stack of matrix
products; attention is a batch of dot products; the GPT is all of it
looped. This module rebuilds that toolbox in pure standard-library
Python so that nothing about it stays magic: you will *write* the
creation functions, the matmul, the transposes, the slicing — and then,
when you open PyTorch later, the API feels like an old friend with a
faster engine, not a foreign language.

The mapping is 1:1 by design. Our `Tensor` mirrors `torch.Tensor`'s
core surface (shape, ndim, indexing semantics, `T`, `permute`,
`reshape`); our free functions mirror `torch.cat` and `@`. What we
deliberately do **not** implement: autograd (module 4 does gradients by
hand), GPU dispatch, and broadcasting beyond scalars — each omission is
a module of its own later, which is exactly why omitting it here is
pedagogically honest.

How to read the rest of this note: each section names the video
chapter, states the concept in one paragraph, shows the toolbox call,
and shows the torch line it translates to. Run the snippets — they are
the module's exercises zero.

## 1. PyTorch Introduction — the toolbox you are holding

```python
>>> from ai_safety_course.from_scratch.tensors import Tensor, matmul, concat
>>> t = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
>>> t.shape, t.ndim, t.numel()
((3, 2), 2, 6)
```

The construction contract is the module's first lesson: data must be
**rectangular** — every row the same length all the way down — or
construction fails immediately with a `ShapeError` that prints both
shapes involved. Ragged data is the number-one from-scratch bug class,
and the toolbox refuses to carry it silently. (Try it:
`Tensor([[1.0, 2.0], [3.0]])` names the offending element index in the
error message.)

In torch: `torch.tensor([[1., 2.], [3., 4.], [5., 6.]])` — same nesting,
same row-major meaning. The mental model to keep: a tensor is *a shape
plus `shape`-many floats in a fixed traversal order*. Every operation
below is a rule for reading and rewriting that flat list through the
shape.

## 2. Creating tensors and special tensors — the constructors

The video's *Creating Tensors* and *Special Tensors* chapters map to
seven constructors on our class, each with a torch twin:

| ours | torch | what it makes |
| --- | --- | --- |
| `Tensor(data)` | `torch.tensor(data)` | from nested lists (validated) |
| `Tensor.zeros(2, 3)` | `torch.zeros(2, 3)` | all `0.0`, shape `(2, 3)` |
| `Tensor.ones(2)` | `torch.ones(2)` | all `1.0` |
| `Tensor.full(7.0, 3, 1)` | `torch.full((3, 1), 7.0)` | a constant |
| `Tensor.arange(5)` / `Tensor.arange(1, 5, 2)` | `torch.arange(...)` | a ramp |
| `Tensor.eye(3)` | `torch.eye(3)` | the identity matrix |
| `Tensor.rand(4, 5, seed=7)` / `Tensor.randn(..., seed=...)` | `torch.rand` / `torch.randn` | seeded uniform / normal |

Two design decisions deserve words because they are course-wide rules,
not conveniences. First, **`arange` follows torch's argument order**:
`arange(start, stop, step)` with `arange(5)` meaning `0..4` — the
single-argument form counts from zero, exactly like the framework, so
your fingers learn one convention. Second, **randomness is seeded and
therefore reproducible**: `Tensor.rand(4, 5, seed=7)` returns the same
tensor on every run of every test in CI. PyTorch's equivalent is
`torch.manual_seed(7)` + `torch.rand(4, 5)`; the difference is that our
seed is a constructor argument, which makes the dependency of a result
on a particular random draw *visible at the call site* — a small
discipline that scales all the way up to the course's
reproducibility rules for real experiments (chapter 02).

`randn` is worth one extra sentence because it is how weights get
initialized in every later module: it draws standard-normal values via
the Box–Muller transform from a seeded generator, so
`Tensor.randn(3, 2, seed=1)` is the "small random matrix" you will
hand to `neuron.py` and `network.py`.

## 3. Tensor operations — elementwise, with the scalar exception

The *Tensor Operations* chapter is arithmetic that respects shape:

```python
>>> a = Tensor([[1.0, 2.0], [3.0, 4.0]])
>>> b = Tensor([[10.0, 20.0], [30.0, 40.0]])
>>> (a + b).tolist()
[[11.0, 22.0], [33.0, 44.0]]
>>> (b - a).tolist(), (a * 2.0).tolist(), (10.0 - a).tolist()
([[9.0, 18.0], [27.0, 36.0]], [[2.0, 4.0], [6.0, 8.0]], [[9.0, 8.0], [7.0, 6.0]])
```

Elementwise tensor–tensor arithmetic requires **equal shapes** and says
so loudly on mismatch. Scalars broadcast — `a * 2.0`, `10.0 - a` —
which is the entire broadcasting story we need: real broadcasting rules
(torch's "size-1 axes expand") buy expressiveness at the cost of silent
shape coercion, and this toolbox refuses the cost. When module 4 needs
a column-wise operation, it *writes the loop*, on purpose.

The companion lesson makes the point that this is "identical to NumPy"
— true here too: our `+` on two same-shape tensors does what
`np.array` addition does, element by element, no more, no less.
Reductions round out the set: `t.sum()`, `t.mean()`, `t.sum(axis=0)`,
`t.mean(axis=1)`, with the axis convention matching torch (axis 0 runs
down rows, axis 1 runs along columns) and the mean always carrying its
explicit denominator — a course habit from the metrics modules that
will save you from more than one "average of an average" bug.

## 4. Matrix multiplication — the heartbeat

Module 01 wrote the 3×2 worked example out by hand; the toolbox runs
it:

```python
>>> from ai_safety_course.from_scratch.tensors import matmul
>>> w = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
>>> x = Tensor([1.0, 2.0])
>>> matmul(w, x).tolist()          # (3,2) @ (2,) -> (3,)
[5.0, 11.0, 17.0]
>>> matmul(w, w.T).tolist()        # (3,2) @ (2,3) -> (3,3)
[[5.0, 11.0, 17.0], [11.0, 25.0, 39.0], [17.0, 39.0, 61.0]]
```

Every entry is a dot product — row of the left, column of the right —
and the shape rule `(m, n) @ (n, p) = (m, p)` is enforced with the
inner dimensions printed on failure. The vector cases follow torch's
conventions: a 1-D right operand is a column (result 1-D), a 1-D left
operand is a row. In torch the same calls are `w @ x` and `w @ w.T`;
the `@` operator is the one symbol you will type most in this track.

One caution the module wants planted now: **`matmul` is the only place
in the toolbox where shape rules are nontrivial**, so it is the only
place where "it ran without error" is weak evidence. When a from-scratch
model misbehaves, print the shapes at every matmul first — the
discipline pays for itself the first time an attention head silently
computes over the wrong axis (module 5's exercises include exactly that
failure, planted on purpose).

## 5. Transposing and permuting — reordering axes

```python
>>> t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
>>> t.T.tolist()                    # 2-D transpose
[[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
>>> t3 = Tensor([[[1.0], [2.0]], [[3.0], [4.0]]])   # shape (2, 2, 1)
>>> t3.permute(2, 0, 1).shape
(1, 2, 2)
```

`t.T` reverses all axes; `transpose(0, 1)` swaps two named axes;
`permute(*axes)` is the general reorder requiring each axis exactly
once — all three match their torch namesakes exactly, because attention
code (module 5) permutes constantly and the vocabulary transfer is the
point. The permute implementation is the nicest thing in the toolbox to
read slowly: it computes flat strides for the old shape, then walks the
new shape's indices and re-derives each old flat position. Shape
manipulation as *index arithmetic* — which is all it ever is.

`reshape` and `flatten` complete the family: `t.reshape(3, 2)`
reinterprets the same row-major data under a new shape (element count
preserved, error message otherwise), `-1` infers one axis from the
count, `flatten()` collapses to 1-D. The torch twins share names and
semantics; note our `reshape` takes var-args or a tuple, a small
ergonomic license.

## 6. Indexing and slicing — reading parts of tensors

```python
>>> t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0], [6.0, 7.0, 8.0]])  # ragged: fails
>>> t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
>>> t[1, 0]            # full-int index -> plain float
4.0
>>> t[0].tolist()      # partial-int index -> the row, as a Tensor
[1.0, 2.0, 3.0]
>>> t[0:2].tolist()    # slice both rows
[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
>>> t[:, 1].tolist()   # a column
[2.0, 5.0, 8.0]
>>> t[1:3, 0:2].tolist()
[[4.0, 5.0], [7.0, 8.0]]
>>> t[::2].tolist()    # step slicing
[[1.0, 2.0, 3.0], [7.0, 8.0, 9.0]]
```

The rules, inherited whole from NumPy/torch: one index per axis; an
int selects and *drops* the axis; a slice keeps it; negatives count
from the end; an all-int tuple long enough to cover every axis returns
a plain `float`. Two safety rails differ from torch on purpose: too
*many* indices raise (instead of arcane KeyError paths), and there is
no advanced indexing (boolean masks, index arrays) — when module 5
needs "the top-k positions", it calls a helper that loops, in plain
sight.

Slicing is where the from-scratch advantage bites: `t[:, 1]` above
executes an explicit loop over row indices computing flat offsets, and
once you have read that loop once, `x[:, 1]` in torch stops looking
like incantation and starts looking like the loop it secretly is.

## 7. Concatenating tensors — joining along an axis

```python
>>> from ai_safety_course.from_scratch.tensors import concat
>>> a = Tensor([[1.0, 2.0], [3.0, 4.0]])
>>> concat([a, Tensor([[5.0, 6.0]])], axis=0).tolist()
[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
>>> concat([a, Tensor([[5.0], [6.0]])], axis=1).tolist()
[[1.0, 2.0, 5.0], [3.0, 4.0, 6.0]]
```

`concat(tensors, axis)` is `torch.cat(tensors, dim=...)`: the axis
dimension sums, every *other* dimension must match exactly, and both
facts appear in the error message when violated. The module's
non-obvious learning is the **block structure of memory**: along axis
0, concatenation is literally list-splicing of flat arrays; along axis
1, it interleaves blocks per row. The implementation walks
prefix-blocks and copies per-tensor runs — reading it once explains why
torch prefers you concatenate along axis 0 when you have a choice
(contiguous copies, no per-row bookkeeping), a fact that matters at
production scale and is invisible at toy scale.

## 8. Tokenization and embeddings — text becomes a vector

The companion's ninth lesson is the bridge from this module to module
5, and its two ideas deserve their exact framing. **Tokenization**
turns text into integers: word-based (huge vocabulary, no fallback for
unseen words), character-based (tiny vocabulary, long sequences),
subword/BPE (the modern standard — common words whole, rare words in
meaningful pieces). **Embeddings** turn integers into vectors via a
lookup table: a `(vocab_size, d_model)` matrix where token id `i` maps
to row `i` — and that matrix is *learned*, initialized random and
nudged by gradients until words used in similar ways sit near each
other in the space.

Our toolbox implements the character level end-to-end:

```python
>>> from ai_safety_course.from_scratch.tensors import CharTokenizer, embed, one_hot, Tensor
>>> tok = CharTokenizer("hello")
>>> ids = tok.encode("hello")
>>> ids, tok.decode(ids), tok.vocab_size
([1, 0, 2, 2, 3], 'hello', 4)
>>> table = Tensor.randn(tok.vocab_size, 2, seed=5)   # the learnable embedding, at birth
>>> vecs = embed(ids, table)        # shape (5, 2): rows 1, 0, 2, 2, 3 of the table
>>> product = matmul(one_hot(ids, tok.vocab_size), table)
>>> vecs.allclose(product)
True
```

That last check is the module's centerpiece claim, pinned by a test in
the suite: **an embedding lookup is a matrix product with a one-hot
matrix.** Row selection and one-hot multiplication are the same linear
operation, which is why `torch.nn.Embedding` can be a learnable layer
at all — it *is* linear, and gradients can flow into it. The lookup
form is what everyone runs (one-hot would blow memory by a factor of
`vocab_size`); the one-hot form is the proof of linearity. When module
5's GPT embeds tokens and when chapter 11 of the safety curriculum
talks about "directions in embedding space", this is the machinery
under both.

One honest scope note: BPE and friends are not implemented here —
they are vocabulary-learning algorithms, not tensor operations, and
the track's GPT (module 5) is character-level on purpose: a tokenizer
you can read in one screen cannot hide anything from you.

## 9. Where this connects

- **To the track**: module 3's neuron is `matmul(w, x)` plus one
  activation; module 4's network is a stack of those with gradients
  computed through these same ops; module 5's attention is three
  matmuls and a softmax over shapes you can now slice and permute with
  intent.
- **To the safety curriculum**: every "vector in the model" claim
  (chapter 09's residual stream, chapter 10's feature directions,
  chapter 11's refusal direction) lives in a tensor of exactly this
  kind; the reason steering vectors can be added and ablated is the
  vector-space structure of module 01, stored in the containers of
  this module.
- **To the sources**: the chapter list is SRC-VIDEO-001's PyTorch
  block (chapters *PyTorch Introduction* through *Special Tensors*);
  the lesson sequence and the tokenization/embeddings framing follow
  the companion repo's `03_pytorch_fundamentals` lessons 01–09
  (SRC-REPO-001).

## 10. Exercises

1. Construct `t = Tensor.arange(1, 13).reshape(3, 4)`. Predict, then
   check: `t[:, 2]`, `t[1]`, `t[1:3, 0:2]`, `t.T.shape`, and
   `matmul(t, t.T).shape`.
2. Using only `Tensor.eye`, `matmul`, and `reshape`: build a
   `(2, 3)` matrix `x` and an operator that swaps its two rows
   (hint: a permutation matrix is rows of the identity, reordered).
3. Prove by experiment (not by proof) that `concat` along axis 1 of
   `a` and `b` equals `concat([a.T, b.T], axis=0).T` for compatible
   `a`, `b`. Then explain *why* in one sentence using the block
   structure of section 7.
4. With `tok = CharTokenizer("the quick brown fox")`: encode
   "the fox"; build `E = Tensor.randn(tok.vocab_size, 3, seed=2)`;
   embed; and verify by direct indexing (`E[ids[0]]` etc. — you may
   need `Tensor(E.tolist()[i])` or `embed([i], E)`) that each output
   row is the table row of its id.
5. The module claims elementwise `+` requires equal shapes while `*`
   with a scalar does not. Find the torch behavior for
   `(3, 1) + (1, 4)` (read the docs or run torch if available —
   otherwise reason it out from the broadcasting rule) and write two
   sentences on *why this toolbox refuses it*.

### Solutions

1. `t.tolist()` is `[[1..4], [5..8], [9..12]]`. `t[:, 2]` →
   `[3.0, 7.0, 11.0]` (third column). `t[1]` → `[5.0, 6.0, 7.0, 8.0]`
   (partial-int index returns the row). `t[1:3, 0:2]` →
   `[[5.0, 6.0], [9.0, 10.0]]`. `t.T.shape` → `(4, 3)`.
   `matmul(t, t.T)` is `(3, 4) @ (4, 3)` → `(3, 3)` (a Gram matrix;
   entry `(i, j)` is the dot of row `i` and row `j` — every diagonal
   entry positive).
2. Let `x` be `(2, 3)`; then `P = Tensor([[0.0, 1.0], [1.0, 0.0]])`
   (the 2×2 identity with rows swapped) gives `matmul(P, x)` with row
   0 = old row 1 and row 1 = old row 0 — left-multiplication acts on
   rows, module 01's exercise 4 general. No reshape is even needed;
   the exercise's point is that "swap rows" is *multiplication by a
   permuted identity*, a fact module 05 reuses when it talks about
   attention permuting token axes.
3. `concat([a, b], axis=1).T` has rows = columns of the join;
   `concat([a.T, b.T], axis=0)` stacks exactly those transposed
   blocks in the same order, so equality holds (test it with
   `.allclose`). Why: axis-1 concatenation interleaves per-row blocks
   of `a` and `b`; transposing first turns those into whole rows of
   `a.T`/`b.T`, and axis-0 concatenation is contiguous block-splicing
   — the transpose converts the interleaved layout into the spliced
   one. Same data, different traversal.
4. `"the fox"` encodes to 7 ids (6 letters + one space); `embed(ids, E)`
   is `(7, 3)`, and output row `k` equals `embed([ids[k]], E)` (or
   row `ids[k]` of `E`) — the lookup contract, checked one row at a
   time. `one_hot(ids, tok.vocab_size) @ E` matches (section 8's
   identification, now verified by hand).
5. Torch broadcasts size-1 axes: `(3, 1) + (1, 4)` yields `(3, 4)`
   with each operand expanded. This toolbox refuses it because
   silent expansion converts shape mistakes into wrong-but-running
   code — the failure mode from-scratch code is designed to expose.
   The trade is explicitness over brevity, and at the scale of the
   track (and its tests), explicitness is the cheaper currency.

## 11. Readings and provenance

- SRC-VIDEO-001 — *Become AI Researcher From Scratch - Full Course*
  (video chapters: *PyTorch Introduction; Tensor Operations; Creating
  Tensors; Matrix Multiplication; Transposing & Permuting; Indexing &
  Slicing; Concatenating Tensors; Special Tensors*). Access:
  page-inspected 2026-10-22; watch alongside, then run the snippets.
- SRC-REPO-001 — vukrosic/zero-to-ai-researcher, module
  `03_pytorch_fundamentals` (nine lessons, 01 creating tensors … 09
  tokenization and embeddings; the lesson texts cover each operation
  in NumPy and PyTorch forms). Access: full-text-read 2026-10-22
  (cloned). The tokenization taxonomy (word / character / subword)
  and the "embedding = learnable lookup table" framing follow lesson
  09's written text.
- The one-hot identification is elementary linear algebra, unattributed
  here; the implementation choice of *lookup over one-hot for memory*
  is the standard engineering fact stated in the companion lesson.
