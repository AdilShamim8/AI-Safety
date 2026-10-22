"""Tests for ai_safety_course.from_scratch.activations (track module 03).

Strategy: every claimed derivative is checked against a central finite
difference (the *numeric* ground truth), every claimed value against a
hand-computed constant, and the numerical-stability claims (sigmoid
branches, softmax max-subtraction, shift invariance) against inputs
that would overflow the naive forms.
"""

import math

import pytest

from ai_safety_course.from_scratch import activations as acts


def numeric_grad(f, x: float, h: float = 1e-6) -> float:
    """Central finite difference: the numeric derivative ground truth."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


# ---------------------------------------------------------------------------
# values
# ---------------------------------------------------------------------------


def test_relu_values() -> None:
    assert acts.relu(3.0) == 3.0
    assert acts.relu(-2.0) == 0.0
    assert acts.relu(0.0) == 0.0


def test_sigmoid_values() -> None:
    assert acts.sigmoid(0.0) == 0.5
    # sigmoid(1) = 1/(1+e^-1); sigmoid(-1) = 1/(1+e^1) = 1/(1+e)
    assert acts.sigmoid(1.0) == pytest.approx(1.0 / (1.0 + math.exp(-1.0)), rel=1e-12)
    assert acts.sigmoid(-1.0) == pytest.approx(1.0 / (1.0 + math.e), rel=1e-12)


def test_tanh_values() -> None:
    assert acts.tanh(0.0) == 0.0
    assert acts.tanh(1.0) == pytest.approx(math.tanh(1.0))
    assert acts.tanh(2.0) == pytest.approx(0.9640275800758169)


def test_silu_values() -> None:
    # silu(0) = 0 * 0.5 = 0; silu(1) = 1 * sigmoid(1)
    assert acts.silu(0.0) == 0.0
    assert acts.silu(1.0) == pytest.approx(1.0 / (1.0 + math.exp(-1.0)))
    assert acts.silu(-1.0) == pytest.approx(-1.0 * math.exp(-1.0) / (1.0 + math.exp(-1.0)))


def test_swiglu_value() -> None:
    # swiglu(v, g) = silu(g) * v; with g = 0: silu(0) = 0 -> output 0
    assert acts.swiglu(3.0, 0.0) == 0.0
    assert acts.swiglu(2.0, 1.0) == pytest.approx(2.0 * acts.silu(1.0))
    # with a large positive gate: silu(g) -> g, so ~ gate * value
    assert acts.swiglu(2.0, 100.0) == pytest.approx(2.0 * 100.0, rel=1e-6)


# ---------------------------------------------------------------------------
# derivatives against finite differences
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("z", [-3.0, -1.5, -0.7, -0.1, 0.0, 0.3, 1.2, 2.5, 4.0, 8.0])
def test_sigmoid_grad_numeric(z: float) -> None:
    assert acts.sigmoid_grad(z) == pytest.approx(numeric_grad(acts.sigmoid, z), abs=1e-6)


@pytest.mark.parametrize("z", [-3.0, -1.5, -0.4, 0.0, 0.9, 2.2, 5.0])
def test_tanh_grad_numeric(z: float) -> None:
    assert acts.tanh_grad(z) == pytest.approx(numeric_grad(acts.tanh, z), abs=1e-6)


@pytest.mark.parametrize("z", [-5.0, -2.0, -0.3, 0.0, 0.8, 1.7, 3.3, 6.0])
def test_silu_grad_numeric(z: float) -> None:
    assert acts.silu_grad(z) == pytest.approx(numeric_grad(acts.silu, z), abs=1e-6)


def test_relu_grad_matches_subgradient() -> None:
    assert acts.relu_grad(0.5) == 1.0
    assert acts.relu_grad(-0.5) == 0.0
    assert acts.relu_grad(0.0) == 0.0  # stated convention
    # away from the kink, numeric agreement is exact
    assert acts.relu_grad(1.0) == pytest.approx(numeric_grad(acts.relu, 1.0))
    assert acts.relu_grad(-1.0) == pytest.approx(numeric_grad(acts.relu, -1.0))


def test_sigmoid_grad_from_output_matches() -> None:
    for z in (-1.0, 0.0, 2.0):
        assert acts.sigmoid_grad_from_output(acts.sigmoid(z)) == pytest.approx(acts.sigmoid_grad(z))


def test_tanh_grad_from_output_matches() -> None:
    for z in (-1.0, 0.0, 2.0):
        assert acts.tanh_grad_from_output(acts.tanh(z)) == pytest.approx(acts.tanh_grad(z))


def test_swiglu_grads_numeric() -> None:
    v, g = 1.3, -0.6
    dv = (acts.swiglu(v + 1e-6, g) - acts.swiglu(v - 1e-6, g)) / 2e-6
    dg = (acts.swiglu(v, g + 1e-6) - acts.swiglu(v, g - 1e-6)) / 2e-6
    got_v, got_g = acts.swiglu_grads(v, g)
    assert got_v == pytest.approx(dv, abs=1e-6)
    assert got_g == pytest.approx(dg, abs=1e-6)


# ---------------------------------------------------------------------------
# numerical stability
# ---------------------------------------------------------------------------


def test_sigmoid_is_stable_for_large_magnitudes() -> None:
    # naive 1/(1+exp(-z)) overflows at exp(1000); ours must not
    assert acts.sigmoid(1000.0) == pytest.approx(1.0)
    assert acts.sigmoid(-1000.0) == pytest.approx(0.0)
    assert acts.sigmoid(-745.0) < 1e-300  # deep in the stable branch


def test_softmax_sums_to_one_and_positive() -> None:
    s = acts.softmax_list([1.0, 2.0, 3.0])
    assert math.fsum(s) == pytest.approx(1.0)
    assert all(v > 0 for v in s)
    assert s == pytest.approx([0.09003057, 0.24472847, 0.66524096], rel=1e-6)


def test_softmax_is_shift_invariant() -> None:
    base = acts.softmax_list([1.0, 2.0, 3.0])
    shifted = acts.softmax_list([1001.0, 1002.0, 1003.0])
    assert base == pytest.approx(shifted, rel=1e-12)


def test_softmax_survives_huge_logits() -> None:
    # exp(1000) is inf in float; the max-subtracted form must handle it
    s = acts.softmax_list([1000.0, 1000.1, 999.9])
    assert math.fsum(s) == pytest.approx(1.0)
    assert s[1] > s[0] > s[2]
    assert acts.softmax_list([5000.0, 5000.0]) == pytest.approx([0.5, 0.5])


def test_softmax_uniform_for_equal_logits() -> None:
    assert acts.softmax_list([7.0, 7.0, 7.0]) == pytest.approx([1 / 3] * 3)


def test_softmax_empty_raises() -> None:
    with pytest.raises(ValueError, match="nonempty"):
        acts.softmax_list([])


def test_softmax_tensor_rows_independently() -> None:
    from ai_safety_course.from_scratch.tensors import Tensor

    t = Tensor([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
    out = acts.softmax_tensor(t)
    assert out.shape == (2, 3)
    assert out.tolist()[0] == pytest.approx(acts.softmax_list([1.0, 2.0, 3.0]))
    assert out.tolist()[1] == pytest.approx(acts.softmax_list([3.0, 2.0, 1.0]))
    # a 1-D tensor softmaxes as a single row
    one = acts.softmax_tensor(Tensor([0.0, 0.0]))
    assert one.tolist() == pytest.approx([0.5, 0.5])
    with pytest.raises(ValueError, match="1-D/2-D"):
        acts.softmax_tensor(Tensor.ones(2, 2, 2))


# ---------------------------------------------------------------------------
# softmax Jacobian
# ---------------------------------------------------------------------------


def test_softmax_grad_matrix_form_numeric() -> None:
    z = [0.2, -1.0, 0.7]
    s = acts.softmax_list(z)
    J = acts.softmax_grad(s)
    h = 1e-7
    for j in range(3):
        zp = list(z)
        zm = list(z)
        zp[j] += h
        zm[j] -= h
        sp = acts.softmax_list(zp)
        sm = acts.softmax_list(zm)
        for i in range(3):
            numeric = (sp[i] - sm[i]) / (2 * h)
            assert J[i][j] == pytest.approx(numeric, abs=1e-5)


def test_softmax_list_grad_matches_matrix_form() -> None:
    s = acts.softmax_list([0.3, -0.8, 1.1])
    dL_ds = [0.5, -1.0, 0.25]
    via_collapse = acts.softmax_list_grad(s, dL_ds)
    J = acts.softmax_grad(s)
    via_matrix = [math.fsum(J[i][j] * dL_ds[i] for i in range(len(s))) for j in range(len(s))]
    assert via_collapse == pytest.approx(via_matrix, abs=1e-12)


def test_softmax_list_grad_numeric() -> None:
    z = [-0.4, 0.9, 1.8]
    s = acts.softmax_list(z)
    dL_ds = [1.0, 0.0, -2.0]

    def loss(zz: list[float]) -> float:
        ss = acts.softmax_list(zz)
        return math.fsum(a * b for a, b in zip(ss, dL_ds, strict=True))

    h = 1e-7
    for j in range(3):
        zp = list(z)
        zm = list(z)
        zp[j] += h
        zm[j] -= h
        numeric = (loss(zp) - loss(zm)) / (2 * h)
        assert acts.softmax_list_grad(s, dL_ds)[j] == pytest.approx(numeric, abs=1e-5)


def test_softmax_list_grad_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="equal lengths"):
        acts.softmax_list_grad([0.5, 0.5], [1.0])
