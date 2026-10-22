"""attention — scaled dot-product attention, causal masking, multi-head (module 05).

Implements the video's attention block (SRC-VIDEO-001, page-inspected
chapters: *Attention Mechanism; Self-Attention Code; GPT Architecture
Overview; Positional Embeddings; Causal Self-Attention; Building the
GPT*) against the companion repository's module ``07_attention_mechanism``
(SRC-REPO-001, full-text-read — six lessons from what-is-attention to
attention-in-code). Note:
``research/ai_safety_course/from_scratch/05-attention-and-transformers.md``.

Scope decisions, stated
-----------------------
* **One sequence at a time.** Tensors are 2-D here: ``Q``, ``K``, ``V``
  are ``(T, d)`` per (batch item, head). Batching is a loop the caller
  writes in plain sight (module 02's no-silent-broadcast stance).
* **Backward is implemented.** :func:`scaled_dot_product_attention` and
  :class:`MultiHeadAttention` both propagate gradients — the softmax
  Jacobian of module 03, the matmul chain of module 04, applied to the
  attention graph. The tests verify every path against finite
  differences.
* **Heads are column blocks.** Head ``h`` of a projection reads columns
  ``[h*dh, (h+1)*dh)`` — mathematically identical to the
  reshape/permute formulation, and sliceable with module 02's toolbox.
* RoPE and DeepSeek's latent attention are *exposition* in the note
  (module 06), not code here; this module uses no positional encoding
  at all (the GPT adds learned position embeddings in
  ``transformer.py``).
"""

from __future__ import annotations

import math

from ai_safety_course.from_scratch import activations as acts
from ai_safety_course.from_scratch.tensors import Tensor, matmul

#: masked-logit fill value: exp(fill - max) underflows to exactly 0.0,
#: so masked positions get weight 0 and (automatically) gradient 0.
MASKED = -1e18


def causal_mask(T: int) -> Tensor:
    """The (T, T) causal mask: 1 where column j <= row i, else 0.

    Row i may attend to columns 0..i (itself included) — each position
    sees only the past and present, never the future. That single
    triangle is what makes a transformer *autoregressive*.
    """
    return Tensor([[1.0 if j <= i else 0.0 for j in range(T)] for i in range(T)])


def attention_scores(Q: Tensor, K: Tensor, mask: Tensor | None = None) -> Tensor:
    """Scaled pre-softmax scores: ``(Q @ K^T) / sqrt(dk)``, mask applied.

    The 1/sqrt(dk) scaling is the module's load-bearing constant: dot
    products of dk-dimensional random vectors have variance ~dk, so
    unscaled scores grow with dimension, softmax saturates (module 03's
    vanishing-gradient column), and gradients die. Dividing by sqrt(dk)
    keeps the softmax in its responsive region regardless of width.
    """
    if Q.ndim != 2 or K.ndim != 2 or Q.shape[0] != K.shape[0]:
        raise ValueError(f"Q, K must be (T, d) with matching T: {Q.shape}, {K.shape}")
    dk = Q.shape[1]
    if dk != K.shape[1]:
        raise ValueError(f"Q, K feature dims must match: {Q.shape} vs {K.shape}")
    scores = matmul(Q, K.T) * (1.0 / math.sqrt(dk))
    if mask is not None:
        if mask.shape != scores.shape:
            raise ValueError(f"mask must be {scores.shape} for scores: got {mask.shape}")
        scores = Tensor(
            [s if m == 1.0 else MASKED for s, m in zip(scores.data, mask.data, strict=True)]
        ).reshape(*scores.shape)
    return scores


def attention_weights(Q: Tensor, K: Tensor, mask: Tensor | None = None) -> Tensor:
    """The softmaxed attention pattern (T, T): row i is a distribution."""
    scores = attention_scores(Q, K, mask)
    return acts.softmax_tensor(scores)


def scaled_dot_product_attention(
    Q: Tensor, K: Tensor, V: Tensor, mask: Tensor | None = None
) -> tuple[Tensor, Tensor]:
    """Attention: ``(softmax(scores) @ V, weights)``.

    Returns the output (T, dv) *and* the weight matrix (T, T) — the
    pattern is the interpretable object (which token attends to which),
    so callers get it whether they asked or not; backward needs it too.
    """
    if V.ndim != 2 or V.shape[0] != K.shape[0]:
        raise ValueError(f"V must be (T, dv) with T matching K: {V.shape} vs {K.shape}")
    w = attention_weights(Q, K, mask)
    return matmul(w, V), w


def scaled_dot_product_attention_backward(
    d_out: Tensor, Q: Tensor, K: Tensor, V: Tensor, w: Tensor, mask: Tensor | None = None
) -> tuple[Tensor, Tensor, Tensor]:
    """Gradients of attention: ``(dQ, dK, dV)`` given the cached pattern.

    The chain, factor by factor (module 04's discipline, new graph):

    * ``out = W @ V`` so ``dV = W^T @ d_out`` and ``dW = d_out @ V^T``;
    * ``W = softmax(scores)`` row-wise, so each row's ``dScores`` is
      module 03's collapsed Jacobian ``W_row * (dW_row - dot(dW_row,
      W_row))`` — masked entries have weight 0 and stay 0;
    * ``scores = (Q @ K^T)/sqrt(dk)`` so ``dQ = dScores @ K /
      sqrt(dk)`` and ``dK = dScores^T @ Q / sqrt(dk)``.
    """
    if d_out.shape != (w.shape[0], V.shape[1]):
        raise ValueError(f"d_out must be {(w.shape[0], V.shape[1])}: got {d_out.shape}")
    dv = matmul(w.T, d_out)
    dw = matmul(d_out, V.T)
    # row-wise softmax Jacobian (collapsed form)
    t = w.shape[0]
    dscores = Tensor(
        [
            g
            for r in range(t)
            for g in acts.softmax_list_grad(
                w.data[r * t : (r + 1) * t], dw.data[r * t : (r + 1) * t]
            )
        ]
    ).reshape(t, t)
    if mask is not None:
        dscores = Tensor(
            [g if m == 1.0 else 0.0 for g, m in zip(dscores.data, mask.data, strict=True)]
        ).reshape(t, t)
    dk_dim = Q.shape[1]
    scale = 1.0 / math.sqrt(dk_dim)
    dq = matmul(dscores, K) * scale
    dk = matmul(dscores.T, Q) * scale
    return dq, dk, dv


def _xavier(in_dim: int, out_dim: int, seed: int) -> Tensor:
    """Variance-preserving init: randn * (1/sqrt(in_dim)).

    Without it, each matmul multiplies activation magnitude by
    ~sqrt(in_dim) and a deep stack's logits explode (the note's section
    on initialization shows the 10^4-scale logits this produces).
    """
    return Tensor.randn(in_dim, out_dim, seed=seed) * (1.0 / math.sqrt(in_dim))


class MultiHeadAttention:
    """Multi-head self-attention over one sequence: the GPT's mixer.

    ``W_q``, ``W_k``, ``W_v``, ``W_o`` are all ``(d_model, d_model)``;
    head ``h`` lives in columns ``[h*dh, (h+1)*dh)`` of the Q/K/V
    projections. ``backward`` propagates to the input and fills
    parameter gradients; ``sgd_step`` updates — the module 04 API.
    """

    def __init__(self, d_model: int, n_heads: int, seed: int = 0) -> None:
        if d_model <= 0 or n_heads <= 0 or d_model % n_heads != 0:
            raise ValueError(
                f"need d_model > 0 and n_heads | d_model: got d_model={d_model}, "
                f"n_heads={n_heads}"
            )
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        # Xavier-scaled: preserves activation scale through the stack
        self.w_q = _xavier(d_model, d_model, seed)
        self.w_k = _xavier(d_model, d_model, seed + 1)
        self.w_v = _xavier(d_model, d_model, seed + 2)
        self.w_o = _xavier(d_model, d_model, seed + 3)
        self.grad_w_q = Tensor.zeros(d_model, d_model)
        self.grad_w_k = Tensor.zeros(d_model, d_model)
        self.grad_w_v = Tensor.zeros(d_model, d_model)
        self.grad_w_o = Tensor.zeros(d_model, d_model)
        # caches for backward
        self._x: Tensor | None = None
        self._q: Tensor | None = None
        self._k: Tensor | None = None
        self._v: Tensor | None = None
        self._concat: Tensor | None = None
        self._weights: list[Tensor] = []

    def forward(self, x: Tensor, mask: Tensor | None = None) -> Tensor:
        """``softmax((XWq)(XWk)^T/sqrt(dh)) (XWv)`` per head, mixed by Wo."""
        if x.ndim != 2 or x.shape[1] != self.d_model:
            raise ValueError(f"x must be (T, {self.d_model}): got {x.shape}")
        self._x = x
        self._q = matmul(x, self.w_q)
        self._k = matmul(x, self.w_k)
        self._v = matmul(x, self.w_v)
        if mask is not None and (
            mask.ndim != 2 or mask.shape[0] != x.shape[0] or mask.shape[1] != x.shape[0]
        ):
            raise ValueError(f"mask must be ({x.shape[0]}, {x.shape[0]}): got {mask.shape}")
        outs: list[list[float]] = [[] for _ in range(x.shape[0])]
        self._weights = []
        for h in range(self.n_heads):
            lo, hi = h * self.d_head, (h + 1) * self.d_head
            q_h = self._q[:, lo:hi]
            k_h = self._k[:, lo:hi]
            v_h = self._v[:, lo:hi]
            out_h, w_h = scaled_dot_product_attention(q_h, k_h, v_h, mask)
            self._weights.append(w_h)
            for t in range(x.shape[0]):
                outs[t].extend(out_h.data[t * self.d_head : (t + 1) * self.d_head])
        self._concat = Tensor(outs)
        return matmul(self._concat, self.w_o)

    def backward(self, dl_dout: Tensor, mask: Tensor | None = None) -> Tensor:
        """Propagate ``dL/dOut)`` to ``dL/dX``, filling parameter grads."""
        if self._x is None or self._concat is None or self._q is None:
            raise RuntimeError("backward() called before forward()")
        if dl_dout.shape != (self._x.shape[0], self.d_model):
            raise ValueError(
                f"dL/dOut must be {(self._x.shape[0], self.d_model)}: got {dl_dout.shape}"
            )
        # output projection: out = concat @ Wo
        self.grad_w_o = matmul(self._concat.T, dl_dout)
        d_concat = matmul(dl_dout, self.w_o.T)
        # per head: slice d_concat, attention backward, reassemble
        t = self._x.shape[0]
        dq_full = [[0.0] * self.d_model for _ in range(t)]
        dk_full = [[0.0] * self.d_model for _ in range(t)]
        dv_full = [[0.0] * self.d_model for _ in range(t)]
        for h in range(self.n_heads):
            lo, hi = h * self.d_head, (h + 1) * self.d_head
            d_out_h = d_concat[:, lo:hi]
            q_h = self._q[:, lo:hi]
            k_h = self._k[:, lo:hi]
            v_h = self._v[:, lo:hi]
            dq_h, dk_h, dv_h = scaled_dot_product_attention_backward(
                d_out_h, q_h, k_h, v_h, self._weights[h], mask
            )
            for row in range(t):
                dq_full[row][lo:hi] = dq_h.data[row * self.d_head : (row + 1) * self.d_head]
                dk_full[row][lo:hi] = dk_h.data[row * self.d_head : (row + 1) * self.d_head]
                dv_full[row][lo:hi] = dv_h.data[row * self.d_head : (row + 1) * self.d_head]
        dq_t = Tensor(dq_full)
        dk_t = Tensor(dk_full)
        dv_t = Tensor(dv_full)
        # projection gradients and the input gradient
        self.grad_w_q = matmul(self._x.T, dq_t)
        self.grad_w_k = matmul(self._x.T, dk_t)
        self.grad_w_v = matmul(self._x.T, dv_t)
        dx = matmul(dq_t, self.w_q.T) + matmul(dk_t, self.w_k.T) + matmul(dv_t, self.w_v.T)
        return dx

    def sgd_step(self, lr: float) -> None:
        """Update all four projections (module 01's descent line)."""
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        for name in ("w_q", "w_k", "w_v", "w_o"):
            w = getattr(self, name)
            g = getattr(self, f"grad_{name}")
            updated = Tensor([a - lr * b for a, b in zip(w.data, g.data, strict=True)]).reshape(
                *w.shape
            )
            setattr(self, name, updated)


__all__ = [
    "MASKED",
    "MultiHeadAttention",
    "attention_scores",
    "attention_weights",
    "causal_mask",
    "scaled_dot_product_attention",
    "scaled_dot_product_attention_backward",
]
