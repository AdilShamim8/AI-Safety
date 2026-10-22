# AI Researcher From Scratch — an owner-directed research track

> Status: **building** — 3 / 7 module notes complete (counters in
> [`planning/STATUS.md`](../../planning/STATUS.md) are the truthful record;
> this page updates as each module lands).
>
> Source: the owner selected the video
> [Become AI Researcher From Scratch - Full Course - LLM, Math, Pytorch, Neural Networks, Transformers](https://www.youtube.com/watch?v=44l-xL7OKLo)
> (Vuk Rosić, published 2025-11-18, ~3 hours, CC-BY) and its written
> companion, the MIT-licensed repository
> [vukrosic/zero-to-ai-researcher](https://github.com/vukrosic/zero-to-ai-researcher).
> This track distills their curriculum into module notes **plus runnable
> code in this repository** — the owner's requirement: "make sure with code".

## What this track is, and what it is not

This is the **mechanics track** of the course. The main curriculum
([`chapters/`](../../chapters/)) teaches how to *evaluate and steer* models
as a safety researcher; this track teaches what the evaluated object *is*,
built by hand: tensors, a neuron, a network trained by backpropagation,
attention, a small autoregressive transformer you can generate text from,
and the two architectural ideas (latent attention, sparse mixture-of-experts)
behind modern efficient LLMs. A safety researcher who has built a GPT once
asks better questions of one — the track exists to make the "black box"
claim die of exposure.

It is **not** a transcript or a mirror of the source material. The video's
spoken transcript could not be retrieved at access time (page-inspected
only: title, channel, date, license, and the chapter list — see
`SRC-VIDEO-001` in the
[source register](../source-register.yaml)); nothing spoken is quoted here.
The notes are an original synthesis anchored to (a) the video's published
chapter list and (b) the companion repository's written modules, which were
cloned and read in full (`SRC-REPO-001`, full-text-read). Every borrowed
structural element (module names, experiment designs) is attributed; the
prose and all code in `src/ai_safety_course/from_scratch/` are written for
this repository.

## The two-source spine

| Element | Source | Access level | License |
| --- | --- | --- | --- |
| 24-chapter video spine: Course Introduction; AI Math Roadmap; PyTorch Module Overview; Neural Networks Overview; Transformers Overview; Math for AI; PyTorch Introduction; Tensor Operations; Creating Tensors; Matrix Multiplication; Transposing & Permuting; Indexing & Slicing; Concatenating Tensors; Special Tensors; Single Neuron Explained; Activation Functions; Neural Network Layers; How Networks Learn; Attention Mechanism; Self-Attention Code; GPT Architecture Overview; Positional Embeddings; Causal Self-Attention; Building the GPT | `SRC-VIDEO-001` | page-inspected (2026-10-22) | CC-BY (as displayed) |
| 12-module written curriculum: start here → Python (9 lessons) → math (functions, derivatives, gradients, vectors, matrices) → PyTorch (9 lessons incl. tokenization/embeddings) → neuron from scratch (7) → activations (ReLU, sigmoid, tanh, SiLU, SwiGLU, softmax) → network + backprop (7) → attention (6) → feedforward + MoE (8) → building a transformer with RoPE (6) → DeepSeek latent attention (3) → GLM-4 MoE (3) | `SRC-REPO-001` | full-text-read (2026-10-22) | MIT (© 2025 Vuk Rosić) |
| Research methodology: three experiments — 5-variant ablation at 512 hidden dims with HellaSwag; learning-rate search; expert-configuration search | `SRC-REPO-001` | full-text-read | MIT |
| Blueberry-LLM paper findings (8.7× ablation gap; 3e-3 optimal LR; 4 experts + top-2 routing) | `SRC-REPO-001` (paper head) | abstract-level | MIT |

Honesty notes that travel with these numbers: the paper's findings are
self-reported single-setup results, not independently replicated (claim
`CLM-0073`); "train an LLM for 1 dollar" is a hardware-cost framing, not an
audited cost. The track prices them accordingly wherever they appear.

## Module map (7 modules)

Each module = one note in this folder + one stdlib-only code module +
tests. Code lives in
[`src/ai_safety_course/from_scratch/`](../../src/ai_safety_course/from_scratch/)
with tests in [`tests/`](../../tests/) (`test_fs_*.py`).

| # | Module (note) | Video chapters covered | Code |
| --- | --- | --- | --- |
| 1 | [`01-math-foundations.md`](01-math-foundations.md) — functions, derivatives, gradients, vectors, matrices | Math for AI; AI Math Roadmap | `tensors.py` |
| 2 | [`02-python-and-pytorch-fundamentals.md`](02-python-and-pytorch-fundamentals.md) — the tensor toolbox by hand | PyTorch Introduction → Special Tensors; tokenization & embeddings | `tensors.py` |
| 3 | [`03-neuron-and-activations.md`](03-neuron-and-activations.md) — one neuron, six activations | Single Neuron Explained; Activation Functions | `neuron.py`, `activations.py` |
| 4 | `04-neural-network-and-backprop.md` — layers, chain rule, learning | Neural Network Layers; How Networks Learn | `network.py` |
| 5 | `05-attention-and-transformers.md` — self-attention, causal masking, positional encoding, a small GPT | Attention Mechanism → Building the GPT | `attention.py`, `transformer.py` |
| 6 | `06-advanced-architectures.md` — DeepSeek latent attention, GLM-4 MoE | (companion-repo modules 10–11) | `moe.py` |
| 7 | `07-research-methodology.md` — the three experiments as research training | (companion-repo methodology layer) | — (protocol module) |

(Module rows become links as each note lands — the absence of a link is
the honest signal that the note is not written yet.)

## Why the code is stdlib-only (and what that buys you)

The repository's engineering baseline (ADR-0002) keeps the core dependency
floor at pytest + PyYAML; the `ml` group (torch et al.) exists only as a
planned dependency group for the compute-tier projects. This track leans
into that constraint deliberately: **a from-scratch implementation that
imports a deep-learning framework is not from scratch.** Every module here
is pure Python 3.12 standard library — tensors are nested lists, matrix
multiplication is loops you can read, backpropagation is explicit gradient
plumbing, attention is arithmetic you can step through with `print`. The
tests run in CI on every push, so the implementations stay honest.

The trade is stated plainly: this code is for *understanding* (hundreds of
parameters, seconds of runtime), not for *training* (the source's own
experiments — 512-dimension ablations, HellaSwag evaluation, RTX-class
budgets — are GPU work; their designs are studied in modules 6–7 and their
executions remain unexecuted protocols in this repo, honestly marked).
When you reach for production work, you graduate to PyTorch — the video's
own tool — and the mapping is 1:1: `tensors.py` ↔ `torch.Tensor`, the
manual backward pass ↔ `autograd`, `transformer.py` ↔
`torch.nn.MultiheadAttention` and friends.

## Running the code

```bash
# from the repository root (uv sync first if needed; stdlib + pytest only)
uv run pytest tests/ -q            # whole suite incl. from-scratch modules
uv run pytest tests/test_fs_tensors.py -q   # one module
```

Each code module carries a docstring that cites the note and sources it
implements; each note ends with a "where it connects" section tying the
mechanics back to the safety curriculum (e.g. why a researcher evaluating
refusal directions on chapter 11's terms wants to have built the thing that
has them).

## Reading order and prerequisites

- **If you have never trained anything:** modules 1 → 7 in order; do the
  exercises in each note before moving on (solutions included).
- **If you know PyTorch but not the internals:** skim 1–2, slow down at
  4 (backprop by hand) and 5 (the GPT build), then 6.
- **If you are here from the safety curriculum:** module 5 is the one that
  pays directly into chapters 09–11 (interpretability); module 7 pays into
  chapter 02 (evaluation science) — the source's ablation/LR/expert
  searches are miniature versions of the course's controlled-experiment
  discipline.

The track's completion record, per module, lives in
[`planning/content-matrix.yaml`](../../planning/content-matrix.yaml)
(`from_scratch:` section) — check there, not here, for what is done.
