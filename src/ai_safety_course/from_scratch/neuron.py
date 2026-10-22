"""neuron — one neuron, its losses, and one explicit learning step (module 03).

Implements the companion repository's module ``04_neuron_from_scratch``
(SRC-REPO-001, full-text-read — seven lessons: what is a neuron, the
linear step, the activation function, building a neuron in Python,
making a prediction, the concept of loss, the concept of learning) and
the video's *Single Neuron Explained* chapter (SRC-VIDEO-001,
page-inspected). Note:
``research/ai-safety_course/from_scratch/03-neuron-and-activations.md``.

The module is deliberately minimal and scalar: weights are a list, the
forward pass is one dot product plus one activation, and the learning
step (:func:`learn_single_weight`) is the *concept of learning* made
exact — one weight, one target, one gradient computed in full by the
chain rule, one update, and the loss before/after so the step's effect
is visible. Module 04 generalizes exactly this arithmetic to layers.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

from ai_safety_course.from_scratch import activations as acts

#: Clipping bound for binary cross-entropy (p of exactly 0/1 gives inf).
BCE_EPS = 1e-12

#: Registry: name -> (activation, derivative w.r.t. pre-activation z).
#: The neuron's whole polymorphism, in one table.
ACTIVATIONS: Mapping[str, tuple[object, object]] = {
    "relu": (acts.relu, acts.relu_grad),
    "sigmoid": (acts.sigmoid, acts.sigmoid_grad),
    "tanh": (acts.tanh, acts.tanh_grad),
    "silu": (acts.silu, acts.silu_grad),
}


def linear_step(weights: Sequence[float], x: Sequence[float], bias: float = 0.0) -> float:
    """The neuron's linear step: z = w . x + b.

    One dot product — module 01's "layer computes dot products" at its
    smallest, and the exact operation ``matmul`` performs a whole
    matrix of at once.
    """
    if len(weights) != len(x):
        raise ValueError(f"linear_step needs len(weights) == len(x): {len(weights)} vs {len(x)}")
    return math.fsum(w * xi for w, xi in zip(weights, x, strict=True)) + bias


class Neuron:
    """A single neuron: linear step followed by an activation.

    >>> n = Neuron(weights=[0.5, 0.5], bias=-1.0, activation="sigmoid")
    >>> n.forward([1.0, 0.8])   # z = 0.5 + 0.4 - 1.0 = -0.1
    0.47502081252106
    """

    def __init__(
        self, weights: Sequence[float], bias: float = 0.0, activation: str = "sigmoid"
    ) -> None:
        if not weights:
            raise ValueError("a neuron needs at least one weight")
        if activation not in ACTIVATIONS:
            known = ", ".join(sorted(ACTIVATIONS))
            raise ValueError(f"unknown activation {activation!r}; known: {known}")
        self.weights: list[float] = [float(w) for w in weights]
        self.bias: float = float(bias)
        self.activation: str = activation

    def forward(self, x: Sequence[float]) -> float:
        """The prediction: activation(linear(x))."""
        z = linear_step(self.weights, x, self.bias)
        fn, _ = ACTIVATIONS[self.activation]
        return fn(z)  # type: ignore[call-arg]

    def pre_activation(self, x: Sequence[float]) -> float:
        """The linear step alone (exposed for gradient computations)."""
        return linear_step(self.weights, x, self.bias)


# ---------------------------------------------------------------------------
# losses (the companion's lesson 06: the concept of loss)
# ---------------------------------------------------------------------------


def mse(prediction: float, target: float) -> float:
    """Squared error for one prediction: (prediction - target)^2.

    Squaring keeps the error positive and punishes large misses
    superlinearly — the companion lesson's two reasons, verbatim in
    spirit. The mean of MSE over a batch is what training minimizes;
    per-example is the atom.
    """
    return (prediction - target) ** 2


def mse_grad(prediction: float, target: float) -> float:
    """dL/d(prediction) = 2 (prediction - target)."""
    return 2.0 * (prediction - target)


def bce(p: float, y: float, eps: float = BCE_EPS) -> float:
    """Binary cross-entropy for one prediction: -[y log p + (1-y) log(1-p)].

    ``p`` is clipped to ``[eps, 1-eps]`` so probabilities of exactly 0
    or 1 give a large-but-finite loss, never inf (the course-wide rule:
    log loss is clipped, never silently infinite — same contract as the
    evaluation package's scorer).
    """
    if y not in (0.0, 1.0):
        raise ValueError(f"bce target y must be 0 or 1, got {y}")
    pc = min(max(float(p), eps), 1.0 - eps)
    return -(y * math.log(pc) + (1.0 - y) * math.log(1.0 - pc))


def bce_grad_from_probability(p: float, y: float, eps: float = BCE_EPS) -> float:
    """dL/dp of BCE: (p - y) / (p (1 - p)), evaluated at the clipped p.

    Note the famous cancellation this *almost* has: paired with a
    sigmoid output, dL/dz simplifies to (a - y) — the note's section 6
    derives it; this function is the unsimplified per-probability form
    so the cancellation can be *tested* rather than trusted.
    """
    if y not in (0.0, 1.0):
        raise ValueError(f"bce target y must be 0 or 1, got {y}")
    pc = min(max(float(p), eps), 1.0 - eps)
    return (pc - y) / (pc * (1.0 - pc))


# ---------------------------------------------------------------------------
# the concept of learning, made exact (companion lesson 07)
# ---------------------------------------------------------------------------


def learn_single_weight(
    w: float,
    x: float,
    bias: float,
    target: float,
    lr: float = 0.5,
    activation: str = "sigmoid",
) -> tuple[float, float, float, float]:
    """One full gradient-descent step on a one-weight neuron.

    Model: ``a = act(w * x + bias)``, loss ``L = (a - target)^2``.
    The chain rule gives

        dL/dw = 2 (a - target) * act'(z) * x

    — outer sensitivity (loss to prediction), middle (prediction to
    pre-activation), inner (pre-activation to weight): the module-01
    chain-rule sentence, applied once.

    Returns ``(new_w, loss_before, loss_after, grad)`` so the caller
    (and the tests, and the note's worked example) can see the whole
    step: gradient, update, and effect.
    """
    if activation not in ACTIVATIONS:
        known = ", ".join(sorted(ACTIVATIONS))
        raise ValueError(f"unknown activation {activation!r}; known: {known}")
    fn, grad_fn = ACTIVATIONS[activation]
    z = w * x + bias
    a = fn(z)  # type: ignore[call-arg]
    loss_before = (a - target) ** 2
    grad = 2.0 * (a - target) * grad_fn(z) * x  # type: ignore[call-arg]
    new_w = w - lr * grad
    a_after = fn(new_w * x + bias)  # type: ignore[call-arg]
    loss_after = (a_after - target) ** 2
    return new_w, loss_before, loss_after, grad


__all__ = [
    "ACTIVATIONS",
    "BCE_EPS",
    "Neuron",
    "bce",
    "bce_grad_from_probability",
    "learn_single_weight",
    "linear_step",
    "mse",
    "mse_grad",
]
