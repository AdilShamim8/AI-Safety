"""Tests for ai_safety_course.from_scratch.network (track module 04).

The load-bearing tests here are the **gradient checks**: for a one-layer
and a two-layer network, every analytic weight/bias gradient produced by
``backward`` is compared against a central finite difference of the
*same* loss — the numeric ground truth. Everything else (shapes, XOR
convergence, determinism) is scaffolding around that guarantee.
"""

import math

import pytest

from ai_safety_course.from_scratch.network import (
    LAYER_ACTIVATIONS,
    MLP,
    DenseLayer,
    mse_loss,
    one_hot_targets,
    softmax_cross_entropy,
    train_loop,
    train_step_mse,
)
from ai_safety_course.from_scratch.tensors import Tensor

# ---------------------------------------------------------------------------
# forward, by hand
# ---------------------------------------------------------------------------


def test_dense_layer_forward_identity_hand_computed() -> None:
    # X (2x2) @ W (2x2) + b -> every entry a dot product + bias
    layer = DenseLayer(
        weights=Tensor([[1.0, 2.0], [3.0, 4.0]]),
        bias=Tensor([10.0, 20.0]),
        activation="identity",
    )
    x = Tensor([[1.0, 1.0], [0.0, 1.0]])
    out = layer.forward(x)
    assert out.shape == (2, 2)
    # row 0: [1*1+1*3+10, 1*2+1*4+20] = [14, 26]; row 1: [13, 24]
    assert out.tolist() == [[14.0, 26.0], [13.0, 24.0]]


def test_dense_layer_forward_sigmoid_matches_module03() -> None:
    # single input, single output: the layer IS module 03's neuron
    layer = DenseLayer(weights=Tensor([[0.5], [0.5]]), bias=Tensor([-1.0]), activation="sigmoid")
    assert layer.forward(Tensor([[1.0, 0.8]])).tolist() == [[pytest.approx(0.47502081252106)]]


def test_dense_layer_validates_shapes_and_names() -> None:
    with pytest.raises(ValueError, match="2-D"):
        DenseLayer(Tensor.ones(3), Tensor.zeros(1))
    with pytest.raises(ValueError, match="bias must be"):
        DenseLayer(Tensor.ones(2, 2), Tensor.zeros(3))
    with pytest.raises(ValueError, match="unknown activation"):
        DenseLayer(Tensor.ones(2, 2), Tensor.zeros(2), activation="gelu")
    layer = DenseLayer(Tensor.ones(2, 2), Tensor.zeros(2))
    with pytest.raises(ValueError, match="X of shape"):
        layer.forward(Tensor.ones(3, 3))


def test_from_seed_is_deterministic() -> None:
    a = DenseLayer.from_seed(3, 2, activation="tanh", seed=11)
    b = DenseLayer.from_seed(3, 2, activation="tanh", seed=11)
    c = DenseLayer.from_seed(3, 2, activation="tanh", seed=12)
    assert a.weights.allclose(b.weights)
    assert not a.weights.allclose(c.weights)
    assert a.bias.tolist() == [0.0, 0.0]


def test_backward_before_forward_raises() -> None:
    layer = DenseLayer(Tensor.ones(2, 2), Tensor.zeros(2))
    with pytest.raises(RuntimeError, match="before forward"):
        layer.backward(Tensor.ones(1, 2))


# ---------------------------------------------------------------------------
# gradient checks: analytic backprop vs finite differences
# ---------------------------------------------------------------------------


def _numeric_mlp_gradient(
    mlp: MLP, x: Tensor, y: Tensor, layer_idx: int, kind: str, h: float = 1e-6
) -> Tensor:
    """Central finite differences of the MSE loss w.r.t. one parameter block."""
    param = mlp.layers[layer_idx].weights if kind == "w" else mlp.layers[layer_idx].bias
    grads = []
    for i in range(param.numel()):
        orig = param.data[i]

        def loss_at() -> float:
            pred = mlp.forward(x)
            loss, _ = mse_loss(pred, y)
            return loss

        param.data[i] = orig + h
        lp = loss_at()
        param.data[i] = orig - h
        lm = loss_at()
        param.data[i] = orig
        grads.append((lp - lm) / (2 * h))
    return Tensor(grads).reshape(*param.shape)


def test_one_layer_sigmoid_mse_gradients_numeric() -> None:
    mlp = MLP([DenseLayer.from_seed(2, 3, activation="sigmoid", seed=5)])
    x = Tensor([[0.5, -1.0], [1.5, 0.25]])
    y = Tensor([[0.1, 0.9, 0.4], [0.8, 0.2, 0.6]])
    pred = mlp.forward(x)
    _, grad = mse_loss(pred, y)
    mlp.backward(grad)
    num_w = _numeric_mlp_gradient(mlp, x, y, 0, "w")
    num_b = _numeric_mlp_gradient(mlp, x, y, 0, "b")
    assert mlp.layers[0].grad_weights.allclose(num_w, tol=1e-5)
    assert mlp.layers[0].grad_bias.allclose(num_b, tol=1e-5)


def test_two_layer_tanh_identity_gradients_numeric() -> None:
    mlp = MLP(
        [
            DenseLayer.from_seed(2, 4, activation="tanh", seed=7),
            DenseLayer.from_seed(4, 1, activation="identity", seed=8),
        ]
    )
    x = Tensor([[0.3, -0.7], [-1.1, 0.9], [0.0, 0.0]])
    y = Tensor([[0.5], [-0.2], [0.1]])
    pred = mlp.forward(x)
    _, grad = mse_loss(pred, y)
    mlp.backward(grad)
    for idx in (0, 1):
        num_w = _numeric_mlp_gradient(mlp, x, y, idx, "w")
        num_b = _numeric_mlp_gradient(mlp, x, y, idx, "b")
        assert mlp.layers[idx].grad_weights.allclose(num_w, tol=1e-5), f"layer {idx} dW"
        assert mlp.layers[idx].grad_bias.allclose(num_b, tol=1e-5), f"layer {idx} db"


def test_three_layer_relu_middle_gradients_numeric() -> None:
    """A relu in the middle of the stack, off its kink, still checks out."""
    mlp = MLP(
        [
            DenseLayer.from_seed(3, 5, activation="tanh", seed=21),
            DenseLayer.from_seed(5, 5, activation="relu", seed=22),
            DenseLayer.from_seed(5, 2, activation="identity", seed=23),
        ]
    )
    x = Tensor.randn(6, 3, seed=9)
    y = Tensor.randn(6, 2, seed=10)
    pred = mlp.forward(x)
    _, grad = mse_loss(pred, y)
    mlp.backward(grad)
    for idx in (0, 1, 2):
        num_w = _numeric_mlp_gradient(mlp, x, y, idx, "w")
        assert mlp.layers[idx].grad_weights.allclose(num_w, tol=1e-4), f"layer {idx} dW"


def test_softmax_cross_entropy_gradient_numeric() -> None:
    logits = Tensor([[0.2, -0.5, 1.1], [0.9, 0.0, -0.3], [-1.2, 0.4, 0.05]])
    target_ids = [0, 2, 1]
    loss, grad = softmax_cross_entropy(logits, target_ids)
    assert loss > 0.0

    h = 1e-6
    for r in range(logits.shape[0]):
        for c in range(logits.shape[1]):
            orig = logits.data[r * 3 + c]
            logits.data[r * 3 + c] = orig + h
            lp, _ = softmax_cross_entropy(logits, target_ids)
            logits.data[r * 3 + c] = orig - h
            lm, _ = softmax_cross_entropy(logits, target_ids)
            logits.data[r * 3 + c] = orig
            numeric = (lp - lm) / (2 * h)
            assert grad.data[r * 3 + c] == pytest.approx(numeric, abs=1e-5)


def test_softmax_cross_entropy_loss_value_hand() -> None:
    # two rows, same logits but swapped targets -> same loss; plus a
    # hand value: uniform logits over 3 classes -> loss = log(3)
    uniform = Tensor.zeros(2, 3)
    loss, _ = softmax_cross_entropy(uniform, [0, 2])
    assert loss == pytest.approx(math.log(3.0))
    # confident correct prediction -> tiny loss
    good = Tensor([[100.0, 0.0, -100.0]])
    loss_g, grad_g = softmax_cross_entropy(good, [0])
    assert loss_g == pytest.approx(0.0, abs=1e-9)
    # grad is (p - y)/B ~ 0 for the correct class, ~0 for the others
    assert max(abs(v) for v in grad_g.data) < 1e-8


def test_softmax_cross_entropy_validates() -> None:
    with pytest.raises(ValueError, match="one target id per row"):
        softmax_cross_entropy(Tensor.zeros(2, 3), [0])
    with pytest.raises(ValueError, match="outside 3 classes"):
        softmax_cross_entropy(Tensor.zeros(2, 3), [0, 3])


# ---------------------------------------------------------------------------
# losses and one-hot
# ---------------------------------------------------------------------------


def test_mse_loss_value_and_grad() -> None:
    pred = Tensor([[0.19, 0.5], [0.81, 0.5]])
    target = Tensor([[1.0, 0.0], [1.0, 1.0]])
    loss, grad = mse_loss(pred, target)
    # ((0.81)^2 + (0.5)^2 + (0.19)^2 + (0.5)^2) / 4
    assert loss == pytest.approx((0.6561 + 0.25 + 0.0361 + 0.25) / 4)
    # grad = 2 (pred - target) / numel
    assert grad.data[0] == pytest.approx(2 * (0.19 - 1.0) / 4)
    assert grad.data[1] == pytest.approx(2 * 0.5 / 4)
    with pytest.raises(ValueError, match="equal shapes"):
        mse_loss(Tensor.ones(2, 2), Tensor.ones(2))


def test_one_hot_targets() -> None:
    oh = one_hot_targets([1, 0], 3)
    assert oh.tolist() == [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]


def test_identity_activation_passes_gradient_through() -> None:
    layer = DenseLayer(Tensor.eye(2), Tensor.zeros(2), activation="identity")
    layer.forward(Tensor([[1.0, 2.0]]))
    out = layer.backward(Tensor([[5.0, -5.0]]))
    # identity grad 1: dX = dA @ W^T = dA @ I = dA
    assert out.allclose(Tensor([[5.0, -5.0]]))


def test_layer_activations_registry_has_five() -> None:
    assert set(LAYER_ACTIVATIONS) == {"identity", "relu", "sigmoid", "tanh", "silu"}


# ---------------------------------------------------------------------------
# training: the update works, the loop converges, and it is deterministic
# ---------------------------------------------------------------------------


def test_sgd_step_reduces_loss() -> None:
    mlp = MLP([DenseLayer.from_seed(2, 1, activation="sigmoid", seed=3)])
    x = Tensor([[0.0, 1.0]])
    y = Tensor([[1.0]])
    loss0, _ = mse_loss(mlp.forward(x), y)
    step_loss = train_step_mse(mlp, x, y, lr=0.5)
    # the step returns the pre-update loss (the batch it trained on)...
    assert step_loss == pytest.approx(loss0)
    # ...and the update itself then lowers the loss on the same batch
    loss1, _ = mse_loss(mlp.forward(x), y)
    assert loss1 < loss0


def test_sgd_step_rejects_negative_lr() -> None:
    layer = DenseLayer(Tensor.eye(2), Tensor.zeros(2))
    with pytest.raises(ValueError, match="learning rate"):
        layer.sgd_step(-0.1)


def test_xor_converges_with_hidden_layer() -> None:
    """XOR: the classic demonstration that depth is not decoration.

    A 2 -> 4 -> 1 tanh/sigmoid network trained by plain SGD reaches
    all four truth rows; a linear model provably cannot (the note's
    section 4 works the impossibility argument).
    """
    x = Tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = Tensor([[0.0], [1.0], [1.0], [0.0]])
    mlp = MLP(
        [
            DenseLayer.from_seed(2, 4, activation="tanh", seed=42),
            DenseLayer.from_seed(4, 1, activation="sigmoid", seed=43),
        ]
    )
    curve = train_loop(mlp, x, lr=0.5, epochs=4000, y=y)
    assert curve[-1] < 0.02
    assert curve[-1] < curve[0]
    preds = mlp.forward(x).tolist()
    for p, row in zip(preds, y.tolist(), strict=True):
        assert abs(p[0] - row[0]) < 0.1
    # and the four rows classify correctly at the 0.5 threshold
    bits = [1 if p[0] > 0.5 else 0 for p in preds]
    assert bits == [0, 1, 1, 0]


def test_training_curve_is_deterministic() -> None:
    def run() -> list[float]:
        mlp = MLP(
            [
                DenseLayer.from_seed(2, 3, activation="tanh", seed=100),
                DenseLayer.from_seed(3, 1, activation="identity", seed=101),
            ]
        )
        x = Tensor([[1.0, -1.0], [0.5, 0.5]])
        y = Tensor([[0.3], [-0.2]])
        return train_loop(mlp, x, lr=0.1, epochs=50, y=y)

    assert run() == run()


def test_train_loop_validates_arguments() -> None:
    mlp = MLP([DenseLayer.from_seed(2, 1, seed=1)])
    x = Tensor.ones(2, 2)
    with pytest.raises(ValueError, match="needs y"):
        train_loop(mlp, x, lr=0.1, epochs=1, loss="mse")
    with pytest.raises(ValueError, match="needs target_ids"):
        train_loop(mlp, x, lr=0.1, epochs=1, loss="ce")
    with pytest.raises(ValueError, match="unknown loss"):
        train_loop(mlp, x, lr=0.1, epochs=1, y=Tensor.ones(2, 1), loss="huber")


def test_mlp_widths_must_chain() -> None:
    with pytest.raises(ValueError, match="widths must chain"):
        MLP([DenseLayer.from_seed(2, 3, seed=1), DenseLayer.from_seed(4, 1, seed=2)])


def test_classification_train_step_softmax_ce_converges() -> None:
    """Three separable clusters in 2-D, 3-way softmax output."""
    x = Tensor(
        [
            [0.0, 0.0],
            [0.1, 0.0],
            [0.0, 0.1],
            [1.0, 1.0],
            [0.9, 1.0],
            [1.0, 0.9],
            [1.0, 0.0],
            [0.9, 0.1],
            [1.0, 0.1],
        ]
    )
    target_ids = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    mlp = MLP(
        [
            DenseLayer.from_seed(2, 8, activation="tanh", seed=55),
            DenseLayer.from_seed(8, 3, activation="identity", seed=56),
        ]
    )
    curve = train_loop(mlp, x, lr=0.5, epochs=300, loss="ce", target_ids=target_ids)
    assert curve[-1] < 0.05
    # argmax per row recovers the classes
    preds = mlp.forward(x).tolist()
    got = [row.index(max(row)) for row in preds]
    assert got == target_ids
