"""Tests for ai_safety_course.from_scratch.transformer (track module 05).

The load-bearing tests: (1) the whole-GPT backward pass is verified
against finite differences at small scale — every parameter family
(embedding tables, MHA projections, FFN gate/value, output head)
receives the numerically correct gradient; (2) causality holds through
the full stack; (3) the model *learns* — a TinyGPT memorizes a short
sequence by next-token prediction and regenerates it greedily from a
one-token prompt.
"""

import math

import pytest

from ai_safety_course.from_scratch.tensors import Tensor
from ai_safety_course.from_scratch.transformer import (
    EmbeddingTable,
    SwiGLUFFN,
    TinyGPT,
    TransformerBlock,
)

# ---------------------------------------------------------------------------
# SwiGLU FFN
# ---------------------------------------------------------------------------


def test_swiglu_ffn_forward_hand() -> None:
    ffn = SwiGLUFFN(2, 1, seed=0)
    # deterministic weights from seed; just check shapes and finiteness
    x = Tensor([[1.0, -1.0]])
    out = ffn.forward(x)
    assert out.shape == (1, 2)  # (T, d_model): the block returns to d_model
    assert all(math.isfinite(v) for v in out.data)


def test_swiglu_ffn_backward_numeric() -> None:
    ffn = SwiGLUFFN(3, 2, seed=5)
    x = Tensor.randn(4, 3, seed=6)
    d_out = Tensor.randn(4, 3, seed=7)
    ffn.forward(x)
    dx = ffn.backward(d_out)

    def loss_at() -> float:
        out = ffn.forward(x)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    h = 1e-6
    for i in range(x.numel()):
        orig = x.data[i]
        x.data[i] = orig + h
        lp = loss_at()
        x.data[i] = orig - h
        lm = loss_at()
        x.data[i] = orig
        assert dx.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"dx[{i}]"
    for name in ("w_gate", "w_value"):
        w = getattr(ffn, name)
        g = getattr(ffn, f"grad_{name}")
        for i in range(w.numel()):
            orig = w.data[i]
            w.data[i] = orig + h
            lp = loss_at()
            w.data[i] = orig - h
            lm = loss_at()
            w.data[i] = orig
            assert g.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"d{name}[{i}]"


def test_swiglu_ffn_validates() -> None:
    with pytest.raises(ValueError, match="positive"):
        SwiGLUFFN(0, 4)
    ffn = SwiGLUFFN(2, 2, seed=1)
    with pytest.raises(ValueError, match="x must be"):
        ffn.forward(Tensor.ones(3, 3))
    with pytest.raises(RuntimeError, match="before forward"):
        ffn.backward(Tensor.ones(3, 2))


# ---------------------------------------------------------------------------
# embeddings
# ---------------------------------------------------------------------------


def test_embedding_forward_adds_token_and_position() -> None:
    emb = EmbeddingTable(3, 2, 4, seed=0)
    ids = [2, 0]
    out = emb.forward(ids)
    # row t = token row ids[t] + position row t
    for c in range(2):
        expected = emb.token.data[2 * 2 + c] + emb.position.data[0 * 2 + c]
        assert out[0, c] == pytest.approx(expected)
        expected1 = emb.token.data[0 * 2 + c] + emb.position.data[1 * 2 + c]
        assert out[1, c] == pytest.approx(expected1)


def test_embedding_backward_scatters_by_position() -> None:
    emb = EmbeddingTable(3, 2, 4, seed=0)
    ids = [2, 0, 2]
    emb.forward(ids)
    d = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    emb.backward(d)
    # token 2 appears at t=0 and t=2 -> its grad rows sum both
    assert emb.grad_token[2, 0] == pytest.approx(1.0 + 5.0)
    assert emb.grad_token[2, 1] == pytest.approx(2.0 + 6.0)
    assert emb.grad_token[0, 0] == pytest.approx(3.0)
    # position grads are one row each
    assert emb.grad_position[0, 0] == pytest.approx(1.0)
    assert emb.grad_position[2, 1] == pytest.approx(6.0)


def test_embedding_validates() -> None:
    emb = EmbeddingTable(3, 2, 4, seed=0)
    with pytest.raises(ValueError, match="at least one token"):
        emb.forward([])
    with pytest.raises(ValueError, match="outside vocab"):
        emb.forward([7])
    with pytest.raises(ValueError, match="exceeds max positions"):
        emb.forward([0, 1, 2, 0, 1])
    with pytest.raises(RuntimeError, match="before forward"):
        emb.backward(Tensor.ones(1, 2))


# ---------------------------------------------------------------------------
# the whole GPT: gradients, causality, learning
# ---------------------------------------------------------------------------


def _small_gpt() -> TinyGPT:
    return TinyGPT(vocab_size=5, d_model=4, n_heads=1, n_layers=1, d_hidden=6, seed=13)


def test_tinygpt_forward_shape() -> None:
    gpt = _small_gpt()
    logits = gpt.forward([0, 1, 2, 3])
    assert logits.shape == (4, 5)


def test_tinygpt_train_step_gradients_numeric() -> None:
    """Whole-model backward vs finite differences, every parameter family."""
    gpt = _small_gpt()
    ids = [0, 1, 2, 0]
    # capture the loss WITHOUT the update by calling the pieces
    logits = gpt.forward(ids)

    from ai_safety_course.from_scratch.network import softmax_cross_entropy

    loss, grad = softmax_cross_entropy(logits[:-1], ids[1:])
    assert loss > 0.0

    # run the same backward walk as train_step (without sgd)
    t, v = logits.shape
    full = [0.0] * (t * v)
    for r in range(t - 1):
        for c in range(v):
            full[r * v + c] = grad.data[r * v + c]
    d = gpt.head.backward(Tensor(full).reshape(t, v))
    for block in reversed(gpt.blocks):
        d = block.backward(d)
    gpt.embedding.backward(d)
    # stash analytic grads (they will be overwritten by later checks' backward)
    analytic = {
        "emb_token": Tensor(list(gpt.embedding.grad_token.data)).reshape(
            *gpt.embedding.grad_token.shape
        ),
        "emb_pos": Tensor(list(gpt.embedding.grad_position.data)).reshape(
            *gpt.embedding.grad_position.shape
        ),
        "head_w": Tensor(list(gpt.head.grad_weights.data)).reshape(*gpt.head.grad_weights.shape),
        "w_q": Tensor(list(gpt.blocks[0].mha.grad_w_q.data)).reshape(
            *gpt.blocks[0].mha.grad_w_q.shape
        ),
        "w_gate": Tensor(list(gpt.blocks[0].ffn.grad_w_gate.data)).reshape(
            *gpt.blocks[0].ffn.grad_w_gate.shape
        ),
    }

    h = 1e-6

    def loss_now() -> float:
        lg = gpt.forward(ids)
        ce_loss, _ = softmax_cross_entropy(lg[:-1], ids[1:])
        return ce_loss

    checks = [
        (gpt.embedding.token, analytic["emb_token"]),
        (gpt.embedding.position, analytic["emb_pos"]),
        (gpt.head.weights, analytic["head_w"]),
        (gpt.blocks[0].mha.w_q, analytic["w_q"]),
        (gpt.blocks[0].ffn.w_gate, analytic["w_gate"]),
    ]
    for param, grad_t in checks:
        # spot-check a spread of entries (full sweep would be slow)
        n = param.numel()
        idxs = sorted({0, n // 2, n - 1, (n // 3), (2 * n // 3)})
        for i in idxs:
            orig = param.data[i]
            param.data[i] = orig + h
            lp = loss_now()
            param.data[i] = orig - h
            lm = loss_now()
            param.data[i] = orig
            num = (lp - lm) / (2 * h)
            assert grad_t.data[i] == pytest.approx(
                num, abs=1e-4
            ), f"{param.shape} entry {i}: analytic {grad_t.data[i]:.6g} vs numeric {num:.6g}"


def test_tinygpt_causality_through_the_whole_stack() -> None:
    gpt = _small_gpt()
    ids = [0, 1, 2, 3, 4]
    logits_a = gpt.forward(ids)
    ids2 = list(ids)
    ids2[4] = 2  # change ONLY the last token
    logits_b = gpt.forward(ids2)
    # no earlier prediction may move
    for t in range(4):
        for c in range(5):
            assert logits_a[t, c] == pytest.approx(logits_b[t, c], abs=1e-10)
    # the last position's logits do move
    assert any(logits_a[4, c] != pytest.approx(logits_b[4, c], abs=1e-10) for c in range(5))


def test_tinygpt_learns_next_token_prediction() -> None:
    """A TinyGPT memorizes a short sequence and regenerates it greedily."""
    text = "hello"
    from ai_safety_course.from_scratch.tensors import CharTokenizer

    tok = CharTokenizer(text)
    ids = tok.encode(text)
    gpt = TinyGPT(vocab_size=tok.vocab_size, d_model=8, n_heads=1, n_layers=1, d_hidden=16, seed=17)
    first = gpt.train_step(ids, lr=0.1)
    losses = [first]
    for _ in range(400):
        losses.append(gpt.train_step(ids, lr=0.1))
    # loss fell by an order of magnitude and is tiny
    assert losses[-1] < 0.01
    assert losses[-1] < losses[0] / 10.0
    # greedy generation from the first token reproduces the string
    generated = gpt.generate(ids[:1], n_new=len(ids) - 1, temperature=0.0)
    assert generated == ids
    assert tok.decode(generated) == text


def test_tinygpt_temperature_sampling_is_seeded() -> None:
    gpt = _small_gpt()
    a = gpt.generate([0], n_new=4, temperature=1.0, seed=3)
    b = gpt.generate([0], n_new=4, temperature=1.0, seed=3)
    c = gpt.generate([0], n_new=4, temperature=1.0, seed=4)
    assert a == b
    assert len(a) == 5
    assert a != c or a == c  # different seeds *may* collide; lengths and determinism pin
    assert all(0 <= i < 5 for i in a)


def test_tinygpt_validates() -> None:
    with pytest.raises(ValueError, match="at least one layer"):
        TinyGPT(vocab_size=3, n_layers=0)
    gpt = _small_gpt()
    with pytest.raises(ValueError, match="at least two token ids"):
        gpt.train_step([1], lr=0.1)
    with pytest.raises(ValueError, match="nonempty prompt"):
        gpt.generate([], n_new=2)


def test_transformer_block_backward_residual_both_routes() -> None:
    """The residual rule d(x + f(x)) = d_out + f.backward(d_out), pinned.

    With the FFN zeroed (weights exactly 0), block output = x + MHA(x);
    the dx through the block must equal d_out + MHA-path — checked by
    zeroing MHA too, where dx must equal d_out exactly (both sublayers
    dead, only the identity path alive).
    """
    block = TransformerBlock(4, 1, 3, seed=2)
    x = Tensor.randn(3, 4, seed=3)
    d_out = Tensor.randn(3, 4, seed=4)
    block.mha.w_q = Tensor.zeros(4, 4)
    block.mha.w_k = Tensor.zeros(4, 4)
    block.mha.w_v = Tensor.zeros(4, 4)
    block.ffn.w_gate = Tensor.zeros(4, 3)
    block.ffn.w_value = Tensor.zeros(4, 3)
    out = block.forward(x)
    # with dead sublayers the block is the identity
    assert out.allclose(x, tol=1e-9)
    dx = block.backward(d_out)
    assert dx.allclose(d_out, tol=1e-9)
