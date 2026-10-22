"""Tests for ai_safety_course.from_scratch.neuron (track module 03).

Hand-computed values for the linear step and forward pass; loss values
against arithmetic done in the note; the learning step's gradient
against a finite difference of the same model; and the famous
BCE-with-sigmoid cancellation checked numerically rather than trusted.
"""

import math

import pytest

from ai_safety_course.from_scratch import activations as acts
from ai_safety_course.from_scratch.neuron import (
    Neuron,
    bce,
    bce_grad_from_probability,
    learn_single_weight,
    linear_step,
    mse,
    mse_grad,
)

# ---------------------------------------------------------------------------
# linear step
# ---------------------------------------------------------------------------


def test_linear_step_hand_computed() -> None:
    # z = 1*3 + 2*4 - 1 = 10
    assert linear_step([1.0, 2.0], [3.0, 4.0], -1.0) == pytest.approx(10.0)
    assert linear_step([0.5, 0.5], [1.0, 0.8], -1.0) == pytest.approx(-0.1)


def test_linear_step_default_bias_zero() -> None:
    assert linear_step([2.0, 3.0], [1.0, 1.0]) == pytest.approx(5.0)


def test_linear_step_length_mismatch_raises() -> None:
    with pytest.raises(ValueError, match="len\\(weights\\) == len\\(x\\)"):
        linear_step([1.0, 2.0], [1.0])


# ---------------------------------------------------------------------------
# neuron forward
# ---------------------------------------------------------------------------


def test_neuron_forward_sigmoid_hand_computed() -> None:
    n = Neuron(weights=[0.5, 0.5], bias=-1.0, activation="sigmoid")
    assert n.pre_activation([1.0, 0.8]) == pytest.approx(-0.1)
    assert n.forward([1.0, 0.8]) == pytest.approx(acts.sigmoid(-0.1))
    assert n.forward([1.0, 0.8]) == pytest.approx(0.47502081252106, rel=1e-10)


def test_neuron_forward_relu_and_tanh() -> None:
    r = Neuron(weights=[1.0, -2.0], bias=0.5, activation="relu")
    # z = 1 - 2 + 0.5 = -0.5 -> relu clamps it to 0
    assert r.forward([1.0, 1.0]) == 0.0
    # and a positive z passes through unchanged
    assert r.forward([2.0, 0.5]) == pytest.approx(1.5)
    t = Neuron(weights=[1.0, 1.0], bias=0.0, activation="tanh")
    assert t.forward([0.5, 0.5]) == pytest.approx(math.tanh(1.0))


def test_neuron_rejects_empty_weights_and_unknown_activation() -> None:
    with pytest.raises(ValueError, match="at least one weight"):
        Neuron(weights=[])
    with pytest.raises(ValueError, match="unknown activation"):
        Neuron(weights=[1.0], activation="gelu")


def test_neuron_weights_are_copies() -> None:
    src = [1.0, 2.0]
    n = Neuron(src)
    src[0] = 99.0
    assert n.weights[0] == 1.0


# ---------------------------------------------------------------------------
# losses
# ---------------------------------------------------------------------------


def test_mse_and_grad_hand_computed() -> None:
    # the companion lesson's own numbers: prediction 0.19, truth 1
    assert mse(0.19, 1.0) == pytest.approx(0.6561)
    assert mse_grad(0.19, 1.0) == pytest.approx(-1.62)
    assert mse(0.5, 0.5) == 0.0
    assert mse_grad(0.5, 0.5) == 0.0
    # symmetry of the error and antisymmetry of the gradient
    assert mse(1.3, 0.7) == mse(0.7, 1.3)
    assert mse_grad(1.3, 0.7) == -mse_grad(0.7, 1.3)


def test_bce_hand_computed() -> None:
    assert bce(0.19, 1.0) == pytest.approx(-math.log(0.19), rel=1e-12)
    assert bce(0.5, 1.0) == pytest.approx(math.log(2.0))
    assert bce(0.5, 0.0) == pytest.approx(math.log(2.0))
    # correct predictions -> ~0 loss (clipped, finite)
    assert bce(1.0, 1.0) == pytest.approx(0.0, abs=1e-9)
    assert bce(0.0, 0.0) == pytest.approx(0.0, abs=1e-9)
    # the finite-huge case: confidently wrong (predict 0, truth 1)
    assert bce(0.0, 1.0) == pytest.approx(-math.log(1e-12), rel=1e-9)
    with pytest.raises(ValueError, match="y must be 0 or 1"):
        bce(0.5, 0.3)


def test_bce_grad_from_probability_numeric() -> None:
    for p in (0.2, 0.5, 0.81):
        for y in (0.0, 1.0):
            h = 1e-8
            pc = min(max(p, 1e-12), 1 - 1e-12)
            numeric = (bce(pc + h, y) - bce(pc - h, y)) / (2 * h)
            assert bce_grad_from_probability(p, y) == pytest.approx(numeric, rel=1e-5)


def test_bce_plus_sigmoid_cancellation() -> None:
    """The famous cancellation: d/dz BCE(sigmoid(z), y) = sigmoid(z) - y.

    Checked numerically — the note derives it; the test pins it.
    """
    for z in (-1.5, 0.0, 0.9, 2.3):
        for y in (0.0, 1.0):
            h = 1e-7
            a = acts.sigmoid(z)
            numeric = (bce(acts.sigmoid(z + h), y) - bce(acts.sigmoid(z - h), y)) / (2 * h)
            analytic = a - y
            assert numeric == pytest.approx(analytic, abs=1e-6)


# ---------------------------------------------------------------------------
# the learning step
# ---------------------------------------------------------------------------


def test_learn_single_weight_grad_matches_finite_difference() -> None:
    w, x, b, target = 0.4, 1.5, -0.2, 1.0

    def loss_of(wv: float) -> float:
        return (acts.sigmoid(wv * x + b) - target) ** 2

    h = 1e-7
    numeric = (loss_of(w + h) - loss_of(w - h)) / (2 * h)
    _, _, _, grad = learn_single_weight(w, x, b, target, lr=0.5)
    assert grad == pytest.approx(numeric, abs=1e-6)


def test_learn_single_weight_reduces_loss() -> None:
    new_w, before, after, grad = learn_single_weight(w=0.4, x=1.5, bias=-0.2, target=1.0, lr=0.5)
    assert before > 0.0
    assert after < before
    assert new_w > 0.4  # target 1, prediction below target -> weight rises


def test_learn_single_weight_hand_check() -> None:
    # z = 0.4*1 + 0 = 0.4; a = sigmoid(0.4); L = (a-1)^2
    a = acts.sigmoid(0.4)
    expected_grad = 2.0 * (a - 1.0) * acts.sigmoid_grad(0.4) * 1.0
    new_w, before, after, grad = learn_single_weight(w=0.4, x=1.0, bias=0.0, target=1.0, lr=0.5)
    assert before == pytest.approx((a - 1.0) ** 2)
    assert grad == pytest.approx(expected_grad)
    assert new_w == pytest.approx(0.4 - 0.5 * expected_grad)
    assert after == pytest.approx((acts.sigmoid(new_w) - 1.0) ** 2)


def test_learn_single_weight_zero_grad_at_perfect_prediction() -> None:
    # a == target -> grad 0 -> no movement
    new_w, before, after, grad = learn_single_weight(w=0.0, x=1.0, bias=0.0, target=0.5, lr=10.0)
    assert grad == pytest.approx(0.0)
    assert new_w == 0.0
    assert before == 0.0 == after


def test_learn_single_weight_relu_kink() -> None:
    # at z = 0 exactly, relu grad is 0 by the stated convention
    _, _, _, grad = learn_single_weight(
        w=0.0, x=1.0, bias=0.0, target=-1.0, lr=0.1, activation="relu"
    )
    assert grad == 0.0
    # just past the kink, the gradient is alive
    _, _, _, grad_pos = learn_single_weight(
        w=0.01, x=1.0, bias=0.0, target=-1.0, lr=0.1, activation="relu"
    )
    assert grad_pos != 0.0


def test_learn_single_weight_unknown_activation_raises() -> None:
    with pytest.raises(ValueError, match="unknown activation"):
        learn_single_weight(0.1, 1.0, 0.0, 1.0, activation="swish")


def test_repeated_steps_converge_on_easy_target() -> None:
    """Many small steps converge: 250 steps at lr=2 reach the 0.9 target.

    The fixed point is w* = log(9) ~ 2.197 (sigmoid(w*) = 0.9); near it
    the per-step contraction is (1 - lr * 2 * a'(w*)^2) ~ 0.968, so 250
    steps leave ~1e-3 of the initial gap — the tolerances below carry
    an order of magnitude of margin.
    """
    w = 0.1
    x, b, target, lr = 1.0, 0.0, 0.9, 2.0
    for _ in range(250):
        w, _, after, _ = learn_single_weight(w, x, b, target, lr=lr)
    assert after < 1e-6
    assert acts.sigmoid(w * x + b) == pytest.approx(0.9, abs=1e-3)
