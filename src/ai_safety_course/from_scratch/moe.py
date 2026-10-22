"""moe — latent-token attention and a sparse mixture-of-experts FFN (module 06).

Implements the companion repository's advanced-architecture modules
(SRC-REPO-001, full-text-read): ``10_deepseek_latent_attention`` (three
lessons — the latent-token bottleneck, the DeepSeek framing, an
implementation) and ``11_glm4_moe`` (three lessons — MoE recap, the
GLM-4 architecture, an implementation), both of which the video's
companion paper also exercises (CLM-0073, abstract-strength numbers).
Note: ``research/ai-researcher-from-scratch/06-advanced-architectures.md``.

The two ideas, stated plainly
------------------------------
* **Latent attention (as the companion teaches it)**: M learnable
  "summary tokens" sit between the input and the output. Tokens
  compress into latents, latents confer among themselves, tokens read
  back — attention pairs drop from O(N^2) to O(N*M + M^2) for M << N.
  (DeepSeek's production MLA — low-rank Q/K/V projections, per the
  companion paper head's "LoRA-style" description — is the *other*
  latent trick, carried in the note at exposition level.)
* **Sparse mixture-of-experts**: a router picks top-k experts per
  token; only those experts compute, and only those paths get
  gradient. GLM-4-class models scale expert *count* (the companion
  cites 64-128 experts, top-2/top-4 routing, at summary level) while
  keeping per-token compute flat.

Both classes carry full ``backward`` (gradient-checked against finite
differences in the tests) and the module-04 ``sgd_step`` API.
"""

from __future__ import annotations

import math

from ai_safety_course.from_scratch import activations as acts
from ai_safety_course.from_scratch.attention import _xavier
from ai_safety_course.from_scratch.tensors import Tensor, matmul
from ai_safety_course.from_scratch.transformer import SwiGLUFFN


def attention_pairs(n_tokens: int, n_latents: int | None = None) -> int:
    """Attention pair count: N^2 dense, or 2*N*M + M^2 latent.

    The companion lesson's arithmetic as a function: for N = 1000 and
    M = 64, dense attention costs 1,000,000 pairs and the latent route
    2*64,000 + 4,096 = 132,096 — a 7.6x reduction. The lesson's
    headline "16x" counts only the gather step (N*M vs N^2); the note
    prices both honestly.
    """
    if n_latents is None:
        return n_tokens * n_tokens
    return 2 * n_tokens * n_latents + n_latents * n_latents


# ---------------------------------------------------------------------------
# cross-attention (Q and K/V from different sources) — the latent machinery
# ---------------------------------------------------------------------------


def cross_attention(Q: Tensor, K: Tensor, V: Tensor) -> tuple[Tensor, Tensor]:
    """``softmax(Q @ K^T / sqrt(d)) @ V`` with Q and K of different lengths.

    Same formula as module 05's core op; the relaxation is that ``Q``
    may have ``Tq`` rows while ``K``/``V`` have ``Tk`` — which is what
    "latents attend to inputs" and "inputs attend to latents" both
    need. No mask: cross-attention sees everything it is given.
    """
    if Q.ndim != 2 or K.ndim != 2 or V.ndim != 2:
        raise ValueError(f"Q, K, V must be 2-D: {Q.shape}, {K.shape}, {V.shape}")
    if Q.shape[1] != K.shape[1]:
        raise ValueError(f"Q, K feature dims must match: {Q.shape} vs {K.shape}")
    if V.shape[0] != K.shape[0]:
        raise ValueError(f"V rows must match K rows: {V.shape} vs {K.shape}")
    scores = matmul(Q, K.T) * (1.0 / math.sqrt(Q.shape[1]))
    w = acts.softmax_tensor(scores)
    return matmul(w, V), w


def cross_attention_backward(
    d_out: Tensor, Q: Tensor, K: Tensor, V: Tensor, w: Tensor
) -> tuple[Tensor, Tensor, Tensor]:
    """Gradients of :func:`cross_attention`: ``(dQ, dK, dV)``.

    Module 05's factor list, unchanged by the shape relaxation:
    ``dV = W^T dOut``, ``dW = dOut V^T``, row-wise collapsed softmax
    Jacobian, ``dQ = dScores K / sqrt(d)``, ``dK = dScores^T Q / sqrt(d)``.
    """
    if d_out.shape != (w.shape[0], V.shape[1]):
        raise ValueError(f"d_out must be {(w.shape[0], V.shape[1])}: got {d_out.shape}")
    dv = matmul(w.T, d_out)
    dw = matmul(d_out, V.T)
    tq, tk = w.shape
    dscores = Tensor(
        [
            g
            for r in range(tq)
            for g in acts.softmax_list_grad(
                w.data[r * tk : (r * tk + tk)], dw.data[r * tk : (r * tk + tk)]
            )
        ]
    ).reshape(tq, tk)
    scale = 1.0 / math.sqrt(Q.shape[1])
    dq = matmul(dscores, K) * scale
    dk = matmul(dscores.T, Q) * scale
    return dq, dk, dv


class LatentAttention:
    """The latent-token bottleneck, three steps (companion module 10).

    ``latents`` are M learnable vectors (parameters, seeded). The
    forward, with per-step output projections so each step can
    specialize:

    1. *gather* — ``h = attn(Q=L, K=X, V=X) @ w_up`` (latents read inputs)
    2. *confer* — ``z = attn(Q=h, K=h, V=h) @ w_down`` (latents mix)
    3. *broadcast* — ``y = attn(Q=X, K=z, V=z)`` (inputs read latents)

    and the residual ``out = X + Y`` so the block composes like module
    05's. Backward chains all three steps plus the residual, and hands
    the latents their gradient through step 1's dQ.
    """

    def __init__(self, d_model: int, n_latents: int, seed: int = 0) -> None:
        if d_model <= 0 or n_latents <= 0:
            raise ValueError("d_model and n_latents must be positive")
        self.d_model = d_model
        self.n_latents = n_latents
        self.latents = Tensor.randn(n_latents, d_model, seed=seed)
        self.w_up = _xavier(d_model, d_model, seed + 1)
        self.w_down = _xavier(d_model, d_model, seed + 2)
        self.grad_latents = Tensor.zeros(n_latents, d_model)
        self.grad_w_up = Tensor.zeros(d_model, d_model)
        self.grad_w_down = Tensor.zeros(d_model, d_model)
        # caches for backward
        self._x: Tensor | None = None
        self._h_raw: Tensor | None = None
        self._h: Tensor | None = None
        self._z_raw: Tensor | None = None
        self._z: Tensor | None = None
        self._w1: Tensor | None = None
        self._w2: Tensor | None = None
        self._w3: Tensor | None = None

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 2 or x.shape[1] != self.d_model:
            raise ValueError(f"x must be (T, {self.d_model}): got {x.shape}")
        self._x = x
        h_raw, self._w1 = cross_attention(self.latents, x, x)
        self._h_raw = h_raw
        self._h = matmul(h_raw, self.w_up)
        z_raw, self._w2 = cross_attention(self._h, self._h, self._h)
        self._z_raw = z_raw
        self._z = matmul(z_raw, self.w_down)
        y, self._w3 = cross_attention(x, self._z, self._z)
        return x + y

    def backward(self, dl_dout: Tensor) -> Tensor:
        if self._x is None or self._h_raw is None or self._z_raw is None:
            raise RuntimeError("backward() called before forward()")
        if dl_dout.shape != self._x.shape:
            raise ValueError(f"dL/dOut must be {self._x.shape}: got {dl_dout.shape}")
        assert self._w1 is not None and self._w2 is not None and self._w3 is not None
        assert self._h is not None and self._z is not None
        # residual split: out = x + y
        dy = dl_dout
        # broadcast: y = attn(Q=x, K=z, V=z); z serves as both key and value
        dx_q, dz_k, dz_v = cross_attention_backward(dy, self._x, self._z, self._z, self._w3)
        dz = dz_k + dz_v
        # z = z_raw @ w_down
        self.grad_w_down = matmul(self._z_raw.T, dz)
        dz_raw = matmul(dz, self.w_down.T)
        # confer: z_raw = attn(h, h, h); h serves as query, key, and value
        dh_q, dh_k, dh_v = cross_attention_backward(dz_raw, self._h, self._h, self._h, self._w2)
        dh = dh_q + dh_k + dh_v
        # h = h_raw @ w_up
        self.grad_w_up = matmul(self._h_raw.T, dh)
        dh_raw = matmul(dh, self.w_up.T)
        # gather: h_raw = attn(Q=latents, K=x, V=x)
        dl_q, dx_k, dx_v = cross_attention_backward(
            dh_raw, self.latents, self._x, self._x, self._w1
        )
        self.grad_latents = dl_q
        return dl_dout + dx_q + dx_k + dx_v

    def sgd_step(self, lr: float) -> None:
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        self.latents = Tensor(
            [a - lr * b for a, b in zip(self.latents.data, self.grad_latents.data, strict=True)]
        ).reshape(*self.latents.shape)
        for name in ("w_up", "w_down"):
            w = getattr(self, name)
            g = getattr(self, f"grad_{name}")
            setattr(
                self,
                name,
                Tensor([a - lr * b for a, b in zip(w.data, g.data, strict=True)]).reshape(*w.shape),
            )


# ---------------------------------------------------------------------------
# sparse mixture-of-experts
# ---------------------------------------------------------------------------


def top_k_indices(scores: list[float], k: int) -> list[int]:
    """Indices of the k largest scores (ties broken by index — deterministic)."""
    if k <= 0 or k > len(scores):
        raise ValueError(f"k must be in 1..{len(scores)}: got {k}")
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    return sorted(order[:k])


class SparseMoE:
    """Top-k routed mixture of expert FFNs (companion module 11, GLM-4 style).

    ``router`` maps each token to softmax scores over ``n_experts``;
    the top-k experts are selected (weights = their softmax scores),
    each selected expert (a :class:`SwiGLUFFN`) processes the tokens
    that chose it, and outputs mix by weight. Only selected experts
    compute and only selected paths receive gradient — the sparsity is
    real in both directions. GLM-4-class scale (the companion's 64-128
    experts, top-2/top-4 routing) is the same mechanism with more of
    everything; the load-balance question scale raises is the note's.
    """

    def __init__(
        self, d_model: int, d_hidden: int, n_experts: int, top_k: int, seed: int = 0
    ) -> None:
        if n_experts <= 0 or top_k <= 0 or top_k > n_experts:
            raise ValueError(
                f"need 1 <= top_k <= n_experts: got top_k={top_k}, n_experts={n_experts}"
            )
        self.d_model = d_model
        self.n_experts = n_experts
        self.top_k = top_k
        self.router = _xavier(d_model, n_experts, seed)
        self.experts = [
            SwiGLUFFN(d_model, d_hidden, seed=seed + 100 * (i + 1)) for i in range(n_experts)
        ]
        self.grad_router = Tensor.zeros(d_model, n_experts)
        # caches for backward
        self._x: Tensor | None = None
        self._routing: list[list[tuple[int, float]]] = []
        self._groups: dict[int, list[int]] = {}
        self._token_out: list[dict[int, list[float]]] = []

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 2 or x.shape[1] != self.d_model:
            raise ValueError(f"x must be (T, {self.d_model}): got {x.shape}")
        self._x = x
        t_len = x.shape[0]
        logits = matmul(x, self.router)
        probs = acts.softmax_tensor(logits)
        n = self.n_experts
        # routing decisions (deterministic given weights and inputs)
        self._routing = []
        self._groups = {}
        for t in range(t_len):
            row = probs.data[t * n : (t * n + n)]
            selected = top_k_indices(row, self.top_k)
            self._routing.append([(i, row[i]) for i in selected])
            for i in selected:
                self._groups.setdefault(i, []).append(t)
        # each selected expert runs once, batched over the tokens that chose it
        self._token_out = [dict() for _ in range(t_len)]
        for i, tokens in self._groups.items():
            batch = Tensor([x.data[t * self.d_model : (t + 1) * self.d_model] for t in tokens])
            out_batch = self.experts[i].forward(batch)
            for p, t in enumerate(tokens):
                self._token_out[t][i] = out_batch.data[p * self.d_model : (p + 1) * self.d_model]
        # weighted mix per token
        rows: list[list[float]] = []
        for t in range(t_len):
            out_row = [0.0] * self.d_model
            for i, w in self._routing[t]:
                expert_row = self._token_out[t][i]
                for c in range(self.d_model):
                    out_row[c] += w * expert_row[c]
            rows.append(out_row)
        return Tensor(rows)

    def backward(self, dl_dout: Tensor) -> Tensor:
        if self._x is None:
            raise RuntimeError("backward() called before forward()")
        if dl_dout.shape != self._x.shape:
            raise ValueError(f"dL/dOut must be {self._x.shape}: got {dl_dout.shape}")
        t_len, d = self._x.shape
        n = self.n_experts
        # 1) expert paths: each expert's backward on its own token batch.
        #    out = w * E_i(x), so the upstream into expert i is w * dOut
        #    (the weight is applied ONCE, here) and the expert's returned
        #    dX contribution needs no further scaling.
        dx = [[0.0] * d for _ in range(t_len)]
        expert_dx: dict[int, tuple[list[int], Tensor]] = {}
        for i, tokens in self._groups.items():
            d_rows = []
            for t in tokens:
                w = next(w for j, w in self._routing[t] if j == i)
                d_rows.append([w * v for v in dl_dout.data[t * d : (t + 1) * d]])
            expert_dx[i] = (tokens, self.experts[i].backward(Tensor(d_rows)))
        for _i, (tokens, dx_i) in expert_dx.items():
            for p, t in enumerate(tokens):
                for c in range(d):
                    dx[t][c] += dx_i.data[p * d + c]
        # 2) router path: dL/ds_i = <dOut_t, E_i(x_t)> on selected experts,
        #    0 elsewhere; then the collapsed softmax Jacobian per token
        dlogits = [[0.0] * n for _ in range(t_len)]
        for t in range(t_len):
            d_row = dl_dout.data[t * d : (t + 1) * d]
            for i, _w in self._routing[t]:
                dlogits[t][i] = math.fsum(
                    a * b for a, b in zip(d_row, self._token_out[t][i], strict=True)
                )
        logits = matmul(self._x, self.router)
        probs = acts.softmax_tensor(logits)
        dl_logits = Tensor(
            [
                g
                for t in range(t_len)
                for g in acts.softmax_list_grad(probs.data[t * n : (t * n + n)], dlogits[t])
            ]
        ).reshape(t_len, n)
        self.grad_router = matmul(self._x.T, dl_logits)
        return Tensor(dx) + matmul(dl_logits, self.router.T)

    def sgd_step(self, lr: float) -> None:
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        self.router = Tensor(
            [a - lr * b for a, b in zip(self.router.data, self.grad_router.data, strict=True)]
        ).reshape(*self.router.shape)
        for expert in self.experts:
            expert.sgd_step(lr)


__all__ = [
    "LatentAttention",
    "SparseMoE",
    "attention_pairs",
    "cross_attention",
    "cross_attention_backward",
    "top_k_indices",
]
