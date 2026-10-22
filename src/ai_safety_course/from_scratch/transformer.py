"""transformer — a small autoregressive GPT, built from the track's parts.

Implements the video's build (SRC-VIDEO-001, page-inspected chapters:
*GPT Architecture Overview; Positional Embeddings; Causal
Self-Attention; Building the GPT*) against the companion repository's
modules ``08_transformer_feedforward`` and ``09_building_a_transformer``
(SRC-REPO-001, full-text-read — the feedforward layer, MoE preview, the
transformer block, the final linear layer, full transformer, training).
Note: ``research/ai-safety-course/from_scratch/05-attention-and-transformers.md``.

Composition (every part is a previous module, stated)
----------------------------------------------------
* token + position embeddings — module 02's lookup table, learned
  (gradients flow into the table; the one-hot identification is why
  they can);
* causal multi-head attention — module 05's ``attention.py``, verbatim;
* the feedforward block — SwiGLU (module 03's gate/value activation as
  two projections), the design the companion repo's DeepSeek-MLP lesson
  previews and current transformers use;
* residual connections — module 04's identity-pass observation made
  architectural (``x + f(x)``), with the backward rule (``d_in =
  d_out + d_sub``) written out;
* the output head — a module 04 ``DenseLayer`` with identity
  activation, projecting back to vocabulary logits.

Scope decisions, stated plainly: no LayerNorm/RMSNorm (the block is
residual-only; training works at toy scale), learned absolute position
embeddings instead of RoPE (RoPE is exposition in the note and code in
module 06's companion lesson), one sequence at a time (no batching).
Each omission is a deliberate trade of modern stability tricks for
readability — the note says which trick buys what.
"""

from __future__ import annotations

import random
from collections.abc import Sequence

from ai_safety_course.from_scratch import activations as acts
from ai_safety_course.from_scratch.attention import (
    MultiHeadAttention,
    _xavier,
    causal_mask,
)
from ai_safety_course.from_scratch.network import (
    DenseLayer,
    _add_row,
    softmax_cross_entropy,
)
from ai_safety_course.from_scratch.tensors import Tensor, matmul


class SwiGLUFFN:
    """The position-wise feedforward block, transformer-shaped.

    ``h = silu(X @ Wg + bg) * (X @ Wv + bv)`` (gate and value, module
    03's SwiGLU as two projections) followed by the output projection
    ``out = h @ Wout + bout`` back to ``d_model`` — the expanding-then-
    contracting shape a transformer block needs so the residual
    ``y + FFN(y)`` composes. ``backward`` propagates to the input and
    fills all three projections' gradients — the ``DenseLayer`` API.
    """

    def __init__(self, d_model: int, d_hidden: int, seed: int = 0) -> None:
        if d_model <= 0 or d_hidden <= 0:
            raise ValueError("d_model and d_hidden must be positive")
        self.d_model = d_model
        self.d_hidden = d_hidden
        # Xavier-scaled per fan-in: gate/value read d_model, out reads d_hidden
        self.w_gate = _xavier(d_model, d_hidden, seed)
        self.b_gate = Tensor.zeros(d_hidden)
        self.w_value = _xavier(d_model, d_hidden, seed + 1)
        self.b_value = Tensor.zeros(d_hidden)
        self.w_out = _xavier(d_hidden, d_model, seed + 2)
        self.b_out = Tensor.zeros(d_model)
        self.grad_w_gate = Tensor.zeros(d_model, d_hidden)
        self.grad_b_gate = Tensor.zeros(d_hidden)
        self.grad_w_value = Tensor.zeros(d_model, d_hidden)
        self.grad_b_value = Tensor.zeros(d_hidden)
        self.grad_w_out = Tensor.zeros(d_hidden, d_model)
        self.grad_b_out = Tensor.zeros(d_model)
        self._x: Tensor | None = None
        self._g: Tensor | None = None
        self._v: Tensor | None = None
        self._h: Tensor | None = None

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 2 or x.shape[1] != self.d_model:
            raise ValueError(f"x must be (T, {self.d_model}): got {x.shape}")
        self._x = x
        self._g = _add_row(matmul(x, self.w_gate), self.b_gate)
        self._v = _add_row(matmul(x, self.w_value), self.b_value)
        prod = [acts.swiglu(v, g) for g, v in zip(self._g.data, self._v.data, strict=True)]
        self._h = Tensor(prod).reshape(x.shape[0], self.d_hidden)
        return _add_row(matmul(self._h, self.w_out), self.b_out)

    def backward(self, dl_dout: Tensor) -> Tensor:
        if self._x is None or self._g is None or self._v is None or self._h is None:
            raise RuntimeError("backward() called before forward()")
        if dl_dout.shape != (self._x.shape[0], self.d_model):
            raise ValueError(
                f"dL/dOut must be {(self._x.shape[0], self.d_model)}: got {dl_dout.shape}"
            )
        # output projection: out = h @ Wout + bout
        self.grad_w_out = matmul(self._h.T, dl_dout)
        self.grad_b_out = dl_dout.sum(axis=0)
        dh = matmul(dl_dout, self.w_out.T)
        # swiglu(v, g) = silu(g) * v: two partials (module 03)
        da = [d * v for d, v in zip(dh.data, self._v.data, strict=True)]
        dv = [d * acts.silu(g) for d, g in zip(dh.data, self._g.data, strict=True)]
        dg = [d * acts.silu_grad(g) for d, g in zip(da, self._g.data, strict=True)]
        dg_t = Tensor(dg).reshape(self._x.shape[0], self.d_hidden)
        dv_t = Tensor(dv).reshape(self._x.shape[0], self.d_hidden)
        self.grad_w_gate = matmul(self._x.T, dg_t)
        self.grad_b_gate = dg_t.sum(axis=0)
        self.grad_w_value = matmul(self._x.T, dv_t)
        self.grad_b_value = dv_t.sum(axis=0)
        return matmul(dg_t, self.w_gate.T) + matmul(dv_t, self.w_value.T)

    def sgd_step(self, lr: float) -> None:
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        for name in ("w_gate", "w_value", "w_out"):
            w = getattr(self, name)
            g = getattr(self, f"grad_{name}")
            setattr(
                self,
                name,
                Tensor([a - lr * b for a, b in zip(w.data, g.data, strict=True)]).reshape(*w.shape),
            )
        for name in ("b_gate", "b_value", "b_out"):
            b = getattr(self, name)
            g = getattr(self, f"grad_{name}")
            setattr(
                self,
                name,
                Tensor([a - lr * bb for a, bb in zip(b.data, g.data, strict=True)]),
            )


class TransformerBlock:
    """``x + MHA(x)`` then ``y + FFN(y)``, causal mask applied inside.

    The residual backward rule, written once: with ``out = x + f(x)``,
    ``dL/dx = dL/dout + f.backward(dL/dout)`` — the gradient flows both
    *through* the sublayer and *around* it. Both routes are computed.
    """

    def __init__(self, d_model: int, n_heads: int, d_hidden: int, seed: int = 0) -> None:
        self.mha = MultiHeadAttention(d_model, n_heads, seed=seed)
        self.ffn = SwiGLUFFN(d_model, d_hidden, seed=seed + 10)
        self._mask: Tensor | None = None
        self._x: Tensor | None = None

    def forward(self, x: Tensor) -> Tensor:
        if x.ndim != 2:
            raise ValueError(f"x must be (T, d): got {x.shape}")
        self._x = x
        self._mask = causal_mask(x.shape[0])
        attn = self.mha.forward(x, self._mask)
        h = x + attn
        ffn_out = self.ffn.forward(h)
        return h + ffn_out

    def backward(self, dl_dout: Tensor) -> Tensor:
        if self._x is None or self._mask is None:
            raise RuntimeError("backward() called before forward()")
        dh = self.ffn.backward(dl_dout) + dl_dout  # residual 2 (around + through)
        dx = self.mha.backward(dh, self._mask) + dh  # residual 1 (around + through)
        return dx

    def sgd_step(self, lr: float) -> None:
        self.mha.sgd_step(lr)
        self.ffn.sgd_step(lr)


class EmbeddingTable:
    """Learned token and position embeddings, added.

    ``forward(ids)`` looks up token row ``ids[t]`` and position row
    ``t`` and adds them — module 02's two lookups, both *learned*
    (which the one-hot identification licenses). ``backward`` scatters
    the input gradient into both tables; ``sgd_step`` updates them.
    """

    def __init__(self, vocab_size: int, d_model: int, max_positions: int, seed: int = 0) -> None:
        if vocab_size <= 0 or d_model <= 0 or max_positions <= 0:
            raise ValueError("vocab_size, d_model, max_positions must be positive")
        self.token = Tensor.randn(vocab_size, d_model, seed=seed)
        self.position = Tensor.randn(max_positions, d_model, seed=seed + 1)
        self.grad_token = Tensor.zeros(vocab_size, d_model)
        self.grad_position = Tensor.zeros(max_positions, d_model)
        self._ids: list[int] | None = None

    def forward(self, ids: Sequence[int]) -> Tensor:
        if not ids:
            raise ValueError("need at least one token id")
        if len(ids) > self.position.shape[0]:
            raise ValueError(
                f"sequence of {len(ids)} exceeds max positions {self.position.shape[0]}"
            )
        d = self.token.shape[1]
        rows = []
        for t, i in enumerate(ids):
            if not 0 <= i < self.token.shape[0]:
                raise ValueError(f"token id {i} outside vocab {self.token.shape[0]}")
            rows.append(
                [
                    tok + pos
                    for tok, pos in zip(
                        self.token.data[i * d : (i + 1) * d],
                        self.position.data[t * d : (t + 1) * d],
                        strict=True,
                    )
                ]
            )
        # cache only after full validation: a failed forward leaves no cache
        self._ids = list(ids)
        return Tensor(rows)

    def backward(self, dl_dout: Tensor) -> None:
        if self._ids is None:
            raise RuntimeError("backward() called before forward()")
        if dl_dout.shape != (len(self._ids), self.token.shape[1]):
            raise ValueError(
                f"dL/dOut must be {(len(self._ids), self.token.shape[1])}: got {dl_dout.shape}"
            )
        v, d = self.token.shape
        grad_t = [0.0] * (v * d)
        grad_p = [0.0] * (self.position.shape[0] * d)
        for t, i in enumerate(self._ids):
            for c in range(d):
                g = dl_dout.data[t * d + c]
                grad_t[i * d + c] += g
                grad_p[t * d + c] += g
        self.grad_token = Tensor(grad_t).reshape(v, d)
        self.grad_position = Tensor(grad_p).reshape(*self.position.shape)

    def sgd_step(self, lr: float) -> None:
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        self.token = Tensor(
            [a - lr * b for a, b in zip(self.token.data, self.grad_token.data, strict=True)]
        ).reshape(*self.token.shape)
        self.position = Tensor(
            [a - lr * b for a, b in zip(self.position.data, self.grad_position.data, strict=True)]
        ).reshape(*self.position.shape)


class TinyGPT:
    """Embeddings -> transformer blocks -> vocabulary logits, autoregressive.

    Trained on next-token prediction: ``logits[t]`` predicts
    ``ids[t+1]`` (the causal mask enforces that position ``t`` never
    sees beyond itself). One sequence at a time; deterministic given
    seeds.
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 8,
        n_heads: int = 1,
        n_layers: int = 1,
        d_hidden: int = 16,
        max_positions: int = 64,
        seed: int = 0,
    ) -> None:
        if n_layers <= 0:
            raise ValueError("need at least one layer")
        self.embedding = EmbeddingTable(vocab_size, d_model, max_positions, seed=seed)
        self.blocks = [
            TransformerBlock(d_model, n_heads, d_hidden, seed=seed + 100 * (i + 1))
            for i in range(n_layers)
        ]
        self.head = DenseLayer(_xavier(d_model, vocab_size, seed + 999), Tensor.zeros(vocab_size))
        self.vocab_size = vocab_size

    def forward(self, ids: Sequence[int]) -> Tensor:
        x = self.embedding.forward(ids)
        for block in self.blocks:
            x = block.forward(x)
        return self.head.forward(x)

    def train_step(self, ids: Sequence[int], lr: float) -> float:
        """One next-token prediction step; returns the mean CE loss.

        The shift, stated: predictions are ``logits[:-1]`` (positions
        0..T-2), targets are ``ids[1:]`` (tokens 1..T-1) — every token
        is a label for its predecessor. The output gradient is padded
        with a zero row at the end so shapes align with the forward,
        then walked backwards: head, blocks in reverse, embeddings.
        """
        if len(ids) < 2:
            raise ValueError("need at least two token ids to train on")
        logits = self.forward(ids)
        loss, grad = softmax_cross_entropy(logits[:-1], list(ids[1:]))
        t, v = logits.shape
        # scatter (T-1, V) grad back into (T, V) with a zero final row
        full = [0.0] * (t * v)
        for r in range(t - 1):
            for c in range(v):
                full[r * v + c] = grad.data[r * v + c]
        d = self.head.backward(Tensor(full).reshape(t, v))
        for block in reversed(self.blocks):
            d = block.backward(d)
        self.embedding.backward(d)
        self._sgd_all(lr)
        return loss

    def _sgd_all(self, lr: float) -> None:
        for block in self.blocks:
            block.sgd_step(lr)
        self.embedding.sgd_step(lr)
        self.head.sgd_step(lr)

    def generate(
        self, prompt_ids: Sequence[int], n_new: int, temperature: float = 1.0, seed: int = 0
    ) -> list[int]:
        """Autoregressive sampling: ``n_new`` tokens after the prompt.

        temperature 0.0 means greedy argmax (deterministic); otherwise
        tokens are drawn from softmax(logits / temperature) with a
        seeded generator. Each new token is appended and the forward
        reruns — the honest O(T^2) way, no KV cache (the note explains
        what a KV cache would buy).
        """
        if not prompt_ids:
            raise ValueError("need a nonempty prompt")
        ids = list(prompt_ids)
        rng = random.Random(seed)
        for _ in range(n_new):
            logits = self.forward(ids)
            last = logits.data[-self.vocab_size :]
            if temperature <= 0.0:
                ids.append(max(range(self.vocab_size), key=lambda j: last[j]))
            else:
                probs = acts.softmax_list([v / temperature for v in last])
                ids.append(rng.choices(range(self.vocab_size), weights=probs, k=1)[0])
        return ids
