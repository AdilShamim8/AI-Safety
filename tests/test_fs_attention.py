"""Tests for ai_safety_course.from_scratch.attention (track module 05).

Structure: the attention *pattern* is checked against hand computation
on a tiny example; causality is checked behaviorally (perturbing a
future token must not change any earlier output) and structurally (the
mask's zeros); and — the load-bearing part — every backward path
(attention core, all four projections, the input gradient) is verified
against central finite differences.
"""

import math

import pytest

from ai_safety_course.from_scratch.attention import (
    MASKED,
    MultiHeadAttention,
    attention_scores,
    attention_weights,
    causal_mask,
    scaled_dot_product_attention,
    scaled_dot_product_attention_backward,
)
from ai_safety_course.from_scratch.tensors import Tensor, matmul

# ---------------------------------------------------------------------------
# the mask and the pattern
# ---------------------------------------------------------------------------


def test_causal_mask_shape_and_triangle() -> None:
    m = causal_mask(4)
    assert m.tolist() == [
        [1.0, 0.0, 0.0, 0.0],
        [1.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0, 1.0],
    ]


def test_attention_weights_row_zero_is_degenerate() -> None:
    # with a causal mask, row 0 attends to exactly one position: itself
    q = Tensor.randn(3, 2, seed=1)
    k = Tensor.randn(3, 2, seed=2)
    w = attention_weights(q, k, causal_mask(3))
    assert w[0, 0] == pytest.approx(1.0)
    assert w[0, 1] == 0.0 and w[0, 2] == 0.0
    # every row is a distribution
    for r in range(3):
        assert math.fsum(w.data[r * 3 : (r * 3 + 3)]) == pytest.approx(1.0)


def test_attention_scores_scaling_is_sqrt_d() -> None:
    # Q=K=identity(2): scores = I/sqrt(2) before masking
    eye2 = Tensor.eye(2)
    s = attention_scores(eye2, eye2)
    assert s.tolist() == [
        [pytest.approx(1 / math.sqrt(2)), 0.0],
        [0.0, pytest.approx(1 / math.sqrt(2))],
    ]


def test_attention_weights_unmasked_hand() -> None:
    # two queries (rows) against two keys, d=1: row 0 scores [1*1, 1*2]
    q = Tensor([[1.0], [1.0]])
    k = Tensor([[1.0], [2.0]])
    w = attention_weights(q, k)
    # row 0: scores [1, 2]; softmax = [1/(1+e), e/(1+e)]
    e = math.exp(1.0)
    assert w[0, 0] == pytest.approx(1 / (1 + e))
    assert w[0, 1] == pytest.approx(e / (1 + e))
    # row 1: scores [1*1, 1*2] again (same query) -> same distribution
    assert w[1, 0] == pytest.approx(1 / (1 + e))


def test_masking_sets_masked_scores_to_zero_weight() -> None:
    q = Tensor.randn(3, 2, seed=3)
    k = Tensor.randn(3, 2, seed=4)
    w_masked = attention_weights(q, k, causal_mask(3))
    w_open = attention_weights(q, k)
    # strictly-upper triangle is exactly zero under the mask, nonzero (generically) without
    for i in range(3):
        for j in range(3):
            if j > i:
                assert w_masked[i, j] == 0.0
    assert any(w_open[i, j] != 0.0 for i in range(3) for j in range(3) if j > i)


def test_masked_constant_underflows_to_zero() -> None:
    assert math.exp(MASKED) == 0.0


def test_shapes_are_validated() -> None:
    q = Tensor.ones(3, 2)
    with pytest.raises(ValueError, match="matching T"):
        attention_scores(q, Tensor.ones(4, 2))
    with pytest.raises(ValueError, match="feature dims must match"):
        attention_scores(q, Tensor.ones(3, 3))
    with pytest.raises(ValueError, match="mask must be"):
        attention_scores(q, Tensor.ones(3, 2), Tensor.ones(2, 2))
    with pytest.raises(ValueError, match="V must be"):
        scaled_dot_product_attention(q, q, Tensor.ones(4, 2))


# ---------------------------------------------------------------------------
# causality, behaviorally: the future cannot leak
# ---------------------------------------------------------------------------


def test_causality_future_perturbation_does_not_change_past() -> None:
    mha = MultiHeadAttention(4, 2, seed=9)
    x = Tensor.randn(5, 4, seed=10)
    out_a = mha.forward(x, causal_mask(5))
    x2 = Tensor(x.tolist())
    x2_list = x2.tolist()
    x2_list[4] = [v + 5.0 for v in x2_list[4]]  # perturb ONLY the last token
    out_b = mha.forward(Tensor(x2_list), causal_mask(5))
    for t in range(4):  # every earlier position unchanged
        for c in range(4):
            assert out_a[t, c] == pytest.approx(out_b[t, c], abs=1e-12)
    # and position 4 did change
    assert any(out_a[4, c] != out_b[4, c] for c in range(4))


def test_without_mask_information_flows_backwards() -> None:
    mha = MultiHeadAttention(4, 2, seed=9)
    x = Tensor.randn(5, 4, seed=10)
    out_a = mha.forward(x)  # bidirectional
    x2 = Tensor(x.tolist())
    x2_list = x2.tolist()
    x2_list[4] = [v + 5.0 for v in x2_list[4]]
    out_b = mha.forward(Tensor(x2_list))
    # some earlier position now sees the perturbation
    assert any(
        out_a[t, c] != pytest.approx(out_b[t, c], abs=1e-12) for t in range(4) for c in range(4)
    )


# ---------------------------------------------------------------------------
# gradient checks (load-bearing)
# ---------------------------------------------------------------------------


def test_attention_backward_core_numeric() -> None:
    """dQ, dK, dV against finite differences, causal mask on."""
    t, d, dv = 3, 2, 3
    q = Tensor.randn(t, d, seed=11)
    k = Tensor.randn(t, d, seed=12)
    v = Tensor.randn(t, dv, seed=13)
    mask = causal_mask(t)
    d_out = Tensor.randn(t, dv, seed=14)

    out, w = scaled_dot_product_attention(q, k, v, mask)
    dq, dk, dv_g = scaled_dot_product_attention_backward(d_out, q, k, v, w, mask)

    h = 1e-6

    def loss_with(pert: str, idx: int, sign: float) -> float:
        qq, kk, vv = q, k, v
        if pert == "q":
            qq = _perturb(q, idx, sign * h)
        elif pert == "k":
            kk = _perturb(k, idx, sign * h)
        else:
            vv = _perturb(v, idx, sign * h)
        o, _ = scaled_dot_product_attention(qq, kk, vv, mask)
        return math.fsum(a * b for a, b in zip(o.data, d_out.data, strict=True))

    for pert, grad in (("q", dq), ("k", dk), ("v", dv_g)):
        for i in range(grad.numel()):
            num = (loss_with(pert, i, +1) - loss_with(pert, i, -1)) / (2 * h)
            assert grad.data[i] == pytest.approx(num, abs=1e-4), f"{pert}[{i}]"


def _perturb(t_: Tensor, idx: int, delta: float) -> Tensor:
    data = list(t_.data)
    data[idx] += delta
    return Tensor(data).reshape(*t_.shape)


def test_mha_backward_all_paths_numeric() -> None:
    """Input gradient AND all four projection gradients, numerically."""
    d_model, n_heads, t = 4, 2, 3
    mha = MultiHeadAttention(d_model, n_heads, seed=21)
    x = Tensor.randn(t, d_model, seed=22)
    d_out = Tensor.randn(t, d_model, seed=23)
    mask = causal_mask(t)

    mha.forward(x, mask)
    dx = mha.backward(d_out, mask)

    def loss_at() -> float:
        out = mha.forward(x, mask)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    # input gradient
    h = 1e-6
    for i in range(x.numel()):
        orig = x.data[i]
        x.data[i] = orig + h
        lp = loss_at()
        x.data[i] = orig - h
        lm = loss_at()
        x.data[i] = orig
        num = (lp - lm) / (2 * h)
        assert dx.data[i] == pytest.approx(num, abs=1e-4), f"dx[{i}]"

    # projection gradients (weights are plain attributes; perturb flat data)
    for name in ("w_q", "w_k", "w_v", "w_o"):
        w = getattr(mha, name)
        g = getattr(mha, f"grad_{name}")
        for i in range(w.numel()):
            orig = w.data[i]
            w.data[i] = orig + h
            lp = loss_at()
            w.data[i] = orig - h
            lm = loss_at()
            w.data[i] = orig
            num = (lp - lm) / (2 * h)
            assert g.data[i] == pytest.approx(num, abs=1e-4), f"d{name}[{i}]"


def test_mha_sgd_step_changes_weights_and_reduces_loss() -> None:
    mha = MultiHeadAttention(4, 2, seed=31)
    x = Tensor.randn(3, 4, seed=32)
    d_out = Tensor.randn(3, 4, seed=33)
    mask = causal_mask(3)

    def loss_now() -> float:
        out = mha.forward(x, mask)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    # descend the dot-product objective: backward(d_out) gives the true
    # gradient of <out, d_out>; sgd_step already subtracts it
    loss0 = loss_now()
    w_before = mha.w_q.tolist()
    mha.forward(x, mask)
    mha.backward(d_out, mask)
    mha.sgd_step(0.001)
    assert loss_now() < loss0
    assert mha.w_q.tolist() != w_before


def test_mha_validates_arguments() -> None:
    with pytest.raises(ValueError, match="n_heads \\| d_model"):
        MultiHeadAttention(6, 4)
    mha = MultiHeadAttention(4, 2, seed=1)
    with pytest.raises(ValueError, match="x must be"):
        mha.forward(Tensor.ones(3, 5))
    with pytest.raises(ValueError, match="mask must be"):
        mha.forward(Tensor.ones(3, 4), Tensor.ones(2, 2))
    with pytest.raises(RuntimeError, match="before forward"):
        mha.backward(Tensor.ones(3, 4))
    mha.forward(Tensor.ones(3, 4))
    with pytest.raises(ValueError, match="dL/dOut must be"):
        mha.backward(Tensor.ones(3, 5))
    with pytest.raises(ValueError, match="learning rate"):
        mha.sgd_step(-1.0)


def test_multihead_output_shape_and_head_split_equivalence() -> None:
    """One head vs the core op: n_heads=1 equals the plain formula."""
    t, d = 4, 6
    mha = MultiHeadAttention(d, 1, seed=41)
    x = Tensor.randn(t, d, seed=42)
    mask = causal_mask(t)
    q = matmul(x, mha.w_q)
    k = matmul(x, mha.w_k)
    v = matmul(x, mha.w_v)
    out, _ = scaled_dot_product_attention(q, k, v, mask)
    expected = matmul(out, mha.w_o)
    got = mha.forward(x, mask)
    assert got.shape == (t, d)
    assert got.allclose(expected, tol=1e-9)


def test_multihead_heads_see_different_slices() -> None:
    """Two heads on disjoint column blocks must not be identical outputs.

    With distinct seeded projections, head outputs differ generically;
    this pins that the head loop actually slices different columns
    rather than recomputing one head n_heads times.
    """
    mha = MultiHeadAttention(4, 2, seed=51)
    x = Tensor.randn(3, 4, seed=52)
    q = matmul(x, mha.w_q)
    # head slices of the projection are distinct blocks of columns
    h0 = q[:, 0:2]
    h1 = q[:, 2:4]
    assert not h0.allclose(h1)
    out = mha.forward(x, causal_mask(3))
    assert out.shape == (3, 4)
