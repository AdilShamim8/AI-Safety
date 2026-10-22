"""Tests for ai_safety_course.from_scratch.moe (track module 06).

Load-bearing: finite-difference gradient checks through the latent
attention's three chained cross-attentions (including the learnable
latents themselves) and through the sparse MoE's top-k routing (the
router gradient through the collapsed Jacobian, expert gradients
through the selected paths only). Plus the companion lesson's
complexity arithmetic, routing determinism, and the sparsity contract:
non-selected experts receive exactly zero gradient.
"""

import math

import pytest

from ai_safety_course.from_scratch.moe import (
    LatentAttention,
    SparseMoE,
    attention_pairs,
    cross_attention,
    cross_attention_backward,
    top_k_indices,
)
from ai_safety_course.from_scratch.tensors import Tensor

# ---------------------------------------------------------------------------
# the complexity arithmetic (companion module 10's lesson)
# ---------------------------------------------------------------------------


def test_attention_pairs_arithmetic() -> None:
    assert attention_pairs(1000) == 1_000_000
    assert attention_pairs(1000, 64) == 2 * 64_000 + 4_096  # 132,096
    # the honest reduction factor, including confer and broadcast
    ratio = attention_pairs(1000) / attention_pairs(1000, 64)
    assert ratio == pytest.approx(7.57, rel=1e-3)


# ---------------------------------------------------------------------------
# cross-attention
# ---------------------------------------------------------------------------


def test_cross_attention_shapes_and_rows() -> None:
    q = Tensor.randn(3, 4, seed=1)  # 3 queries
    k = Tensor.randn(5, 4, seed=2)  # 5 keys
    v = Tensor.randn(5, 4, seed=3)
    out, w = cross_attention(q, k, v)
    assert out.shape == (3, 4)
    assert w.shape == (3, 5)
    for r in range(3):
        assert math.fsum(w.data[r * 5 : (r * 5 + 5)]) == pytest.approx(1.0)


def test_cross_attention_backward_numeric() -> None:
    q = Tensor.randn(3, 2, seed=4)
    k = Tensor.randn(4, 2, seed=5)
    v = Tensor.randn(4, 3, seed=6)
    d_out = Tensor.randn(3, 3, seed=7)
    out, w = cross_attention(q, k, v)
    dq, dk, dv = cross_attention_backward(d_out, q, k, v, w)

    def loss_of(pert: str, idx: int, sign: float) -> float:
        h = 1e-6
        qq, kk, vv = q, k, v
        if pert == "q":
            qq = _pert(q, idx, sign * h)
        elif pert == "k":
            kk = _pert(k, idx, sign * h)
        else:
            vv = _pert(v, idx, sign * h)
        o, _ = cross_attention(qq, kk, vv)
        return math.fsum(a * b for a, b in zip(o.data, d_out.data, strict=True))

    for pert, grad in (("q", dq), ("k", dk), ("v", dv)):
        for i in range(grad.numel()):
            num = (loss_of(pert, i, +1) - loss_of(pert, i, -1)) / 2e-6
            assert grad.data[i] == pytest.approx(num, abs=1e-4), f"{pert}[{i}]"


def _pert(t_: Tensor, idx: int, delta: float) -> Tensor:
    data = list(t_.data)
    data[idx] += delta
    return Tensor(data).reshape(*t_.shape)


def test_cross_attention_validates() -> None:
    with pytest.raises(ValueError, match="feature dims must match"):
        cross_attention(Tensor.ones(3, 2), Tensor.ones(4, 3), Tensor.ones(4, 3))
    with pytest.raises(ValueError, match="V rows must match"):
        cross_attention(Tensor.ones(3, 2), Tensor.ones(4, 2), Tensor.ones(3, 2))


# ---------------------------------------------------------------------------
# latent attention
# ---------------------------------------------------------------------------


def test_latent_attention_forward_shape_and_residual() -> None:
    lat = LatentAttention(4, 3, seed=8)
    x = Tensor.randn(6, 4, seed=9)
    out = lat.forward(x)
    assert out.shape == (6, 4)
    # residual present: zeroing latents' effect is hard, but shape holds and
    # output differs from input (the block computes something)
    assert not out.allclose(x)


def test_latent_attention_backward_numeric_all_parameters() -> None:
    """dX, latents, w_up, w_down — all against finite differences."""
    lat = LatentAttention(4, 3, seed=12)
    x = Tensor.randn(5, 4, seed=13)
    d_out = Tensor.randn(5, 4, seed=14)
    lat.forward(x)
    dx = lat.backward(d_out)
    g_latents = Tensor(list(lat.grad_latents.data)).reshape(*lat.grad_latents.shape)
    g_up = Tensor(list(lat.grad_w_up.data)).reshape(*lat.grad_w_up.shape)
    g_down = Tensor(list(lat.grad_w_down.data)).reshape(*lat.grad_w_down.shape)

    def loss_now() -> float:
        out = lat.forward(x)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    h = 1e-6
    for i in range(x.numel()):
        orig = x.data[i]
        x.data[i] = orig + h
        lp = loss_now()
        x.data[i] = orig - h
        lm = loss_now()
        x.data[i] = orig
        assert dx.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"dx[{i}]"
    for name, grad in (("latents", g_latents), ("w_up", g_up), ("w_down", g_down)):
        param = getattr(lat, name)
        for i in range(param.numel()):
            orig = param.data[i]
            param.data[i] = orig + h
            lp = loss_now()
            param.data[i] = orig - h
            lm = loss_now()
            param.data[i] = orig
            assert grad.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"d{name}[{i}]"


def test_latent_attention_sgd_reduces_loss() -> None:
    lat = LatentAttention(4, 2, seed=20)
    x = Tensor.randn(4, 4, seed=21)
    d_out = Tensor.randn(4, 4, seed=22)

    def loss_now() -> float:
        out = lat.forward(x)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    loss0 = loss_now()
    lat.forward(x)
    lat.backward(d_out)
    lat.sgd_step(0.001)
    assert loss_now() < loss0


def test_latent_attention_validates() -> None:
    with pytest.raises(ValueError, match="positive"):
        LatentAttention(0, 3)
    lat = LatentAttention(4, 2, seed=1)
    with pytest.raises(ValueError, match="x must be"):
        lat.forward(Tensor.ones(3, 5))
    with pytest.raises(RuntimeError, match="before forward"):
        lat.backward(Tensor.ones(3, 4))


# ---------------------------------------------------------------------------
# sparse MoE
# ---------------------------------------------------------------------------


def test_top_k_indices_deterministic() -> None:
    assert top_k_indices([0.1, 0.5, 0.3, 0.4], 2) == [1, 3]
    # ties broken by index
    assert top_k_indices([0.5, 0.5, 0.2], 2) == [0, 1]
    with pytest.raises(ValueError, match="k must be in"):
        top_k_indices([0.1, 0.2], 0)
    with pytest.raises(ValueError, match="k must be in"):
        top_k_indices([0.1, 0.2], 3)


def test_moe_forward_mixes_selected_experts() -> None:
    moe = SparseMoE(d_model=4, d_hidden=6, n_experts=3, top_k=2, seed=30)
    x = Tensor.randn(5, 4, seed=31)
    out = moe.forward(x)
    assert out.shape == (5, 4)
    # every token routed to exactly top_k experts
    assert all(len(route) == 2 for route in moe._routing)


def test_moe_routing_varies_across_tokens() -> None:
    """Different tokens (generically) pick different expert sets."""
    moe = SparseMoE(d_model=4, d_hidden=6, n_experts=4, top_k=2, seed=32)
    x = Tensor.randn(8, 4, seed=33)
    moe.forward(x)
    sets = {tuple(i for i, _ in route) for route in moe._routing}
    assert len(sets) > 1


def test_moe_backward_numeric_router_and_experts() -> None:
    """dX, router, and one expert's weights — all numeric-checked."""
    moe = SparseMoE(d_model=3, d_hidden=4, n_experts=3, top_k=2, seed=40)
    x = Tensor.randn(4, 3, seed=41)
    d_out = Tensor.randn(4, 3, seed=42)
    moe.forward(x)
    dx = moe.backward(d_out)
    g_router = Tensor(list(moe.grad_router.data)).reshape(*moe.grad_router.shape)
    # an expert that is selected by at least one token:
    selected_expert = next(iter(moe._groups))
    expert_w = moe.experts[selected_expert].w_gate
    g_expert_w = Tensor(list(moe.experts[selected_expert].grad_w_gate.data)).reshape(
        *moe.experts[selected_expert].grad_w_gate.shape
    )

    def loss_now() -> float:
        out = moe.forward(x)
        return math.fsum(a * b for a, b in zip(out.data, d_out.data, strict=True))

    h = 1e-6
    for i in range(x.numel()):
        orig = x.data[i]
        x.data[i] = orig + h
        lp = loss_now()
        x.data[i] = orig - h
        lm = loss_now()
        x.data[i] = orig
        assert dx.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"dx[{i}]"
    for i in range(moe.router.numel()):
        orig = moe.router.data[i]
        moe.router.data[i] = orig + h
        lp = loss_now()
        moe.router.data[i] = orig - h
        lm = loss_now()
        moe.router.data[i] = orig
        assert g_router.data[i] == pytest.approx((lp - lm) / (2 * h), abs=1e-4), f"drouter[{i}]"
    for i in range(0, expert_w.numel(), 3):  # spot-sweep the expert's weights
        orig = expert_w.data[i]
        expert_w.data[i] = orig + h
        lp = loss_now()
        expert_w.data[i] = orig - h
        lm = loss_now()
        expert_w.data[i] = orig
        assert g_expert_w.data[i] == pytest.approx(
            (lp - lm) / (2 * h), abs=1e-4
        ), f"dexpert_w_gate[{i}]"


def test_moe_unselected_experts_get_zero_gradient() -> None:
    """The sparsity contract: non-selected experts see exactly zero grad."""
    moe = SparseMoE(d_model=3, d_hidden=4, n_experts=4, top_k=1, seed=50)
    x = Tensor.randn(3, 3, seed=51)
    d_out = Tensor.randn(3, 3, seed=52)
    moe.forward(x)
    moe.backward(d_out)
    selected = set(moe._groups)
    for i, expert in enumerate(moe.experts):
        if i in selected:
            continue
        assert all(v == 0.0 for v in expert.grad_w_gate.data)
        assert all(v == 0.0 for v in expert.grad_w_value.data)
        assert all(v == 0.0 for v in expert.grad_w_out.data)


def test_moe_sgd_step_changes_only_selected() -> None:
    moe = SparseMoE(d_model=3, d_hidden=4, n_experts=4, top_k=1, seed=60)
    x = Tensor.randn(3, 3, seed=61)
    d_out = Tensor.randn(3, 3, seed=62)
    moe.forward(x)
    moe.backward(d_out)
    before = [Tensor(list(e.w_gate.data)).reshape(*e.w_gate.shape) for e in moe.experts]
    moe.sgd_step(0.01)
    selected = set(moe._groups)
    for i, expert in enumerate(moe.experts):
        after = Tensor(list(expert.w_gate.data)).reshape(*expert.w_gate.shape)
        if i in selected:
            assert not after.allclose(before[i])  # selected experts moved
        else:
            assert after.allclose(before[i])  # unselected frozen


def test_moe_validates() -> None:
    with pytest.raises(ValueError, match="top_k"):
        SparseMoE(4, 6, 3, 0)
    with pytest.raises(ValueError, match="top_k"):
        SparseMoE(4, 6, 3, 4)
    moe = SparseMoE(4, 6, 3, 2, seed=1)
    with pytest.raises(ValueError, match="x must be"):
        moe.forward(Tensor.ones(3, 5))
    with pytest.raises(RuntimeError, match="before forward"):
        moe.backward(Tensor.ones(3, 4))
