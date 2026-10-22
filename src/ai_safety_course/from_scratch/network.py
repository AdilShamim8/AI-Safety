"""network — a dense layer, an MLP, and backpropagation by hand (module 04).

Implements the companion repository's module
``06_neural_network_from_scratch`` (SRC-REPO-001, full-text-read —
seven lessons from the architecture of a network to implementing
backpropagation) and the video's *Neural Network Layers* / *How Networks
Learn* chapters (SRC-VIDEO-001, page-inspected). Note:
``research/ai_safety_course/from_scratch/04-neural-network-and-backprop.md``.

Design contract
---------------
* A :class:`DenseLayer` is exactly module 03's neuron, vectorized over
  rows: ``Z = X @ W + b`` (one matmul — every output unit's dot product
  computed at once), then an elementwise activation. ``identity`` is an
  activation here (gradient 1) so logit layers compose too.
* **Backpropagation is written out, not imported.** :meth:`DenseLayer.backward`
  is the three-factor chain rule of module 03 with the factors now
  matrices: ``dZ = dA * act'(Z)`` (outer), ``dW = X^T @ dZ``,
  ``db = colsum(dZ)`` (middle), ``dX = dZ @ W^T`` (inner). Every shape
  is asserted against the parameter it updates.
* The softmax output layer is deliberately *outside* the layer: softmax
  is not elementwise (module 03's Jacobian), so
  :func:`softmax_cross_entropy` computes logits-level gradients in one
  place, using the (p - y) cancellation derived in module 03.
* Determinism: construct layers from :meth:`DenseLayer.from_seed` (or
  pass explicit tensors) — same seed, same network, same training
  curve, reproducible in CI.
"""

from __future__ import annotations

import math

from ai_safety_course.from_scratch import activations as acts
from ai_safety_course.from_scratch.tensors import Tensor, matmul

#: elementwise activations usable inside a DenseLayer (name -> (fn, grad)).
#: identity is included for logit/output layers.
LAYER_ACTIVATIONS: dict[str, tuple[object, object]] = {
    "identity": (lambda z: z, lambda z: 1.0),
    "relu": (acts.relu, acts.relu_grad),
    "sigmoid": (acts.sigmoid, acts.sigmoid_grad),
    "tanh": (acts.tanh, acts.tanh_grad),
    "silu": (acts.silu, acts.silu_grad),
}


def _add_row(matrix: Tensor, row: Tensor) -> Tensor:
    """Add ``row`` (shape (n,)) to every row of ``matrix`` (shape (b, n)).

    This is the toolbox's *explicit* broadcast: no silent shape
    coercion (module 02's stance), the loop is in plain sight.
    """
    if matrix.ndim != 2 or row.ndim != 1:
        raise ValueError(f"_add_row needs (b, n) and (n,): got {matrix.shape}, {row.shape}")
    if matrix.shape[1] != row.shape[0]:
        raise ValueError(f"_add_row width mismatch: matrix {matrix.shape} vs row {row.shape}")
    b, n = matrix.shape
    out = [matrix.data[i * n + j] + row.data[j] for i in range(b) for j in range(n)]
    return Tensor(out).reshape(b, n)


class DenseLayer:
    """One fully-connected layer: ``A = act(X @ W + b)``.

    ``W`` has shape ``(in_features, out_features)`` (so ``X @ W`` works
    directly), ``b`` has shape ``(out_features,)``. ``forward`` caches
    ``x``, ``z``, ``a`` — backprop needs all three; the cache is the
    price of not having autograd, paid in memory you can inspect.
    """

    def __init__(self, weights: Tensor, bias: Tensor, activation: str = "identity") -> None:
        if weights.ndim != 2:
            raise ValueError(f"weights must be 2-D (in, out): got {weights.shape}")
        if bias.ndim != 1 or bias.shape[0] != weights.shape[1]:
            raise ValueError(
                f"bias must be (out_features,): got {bias.shape} for weights {weights.shape}"
            )
        if activation not in LAYER_ACTIVATIONS:
            known = ", ".join(sorted(LAYER_ACTIVATIONS))
            raise ValueError(f"unknown activation {activation!r}; known: {known}")
        self.weights = weights
        self.bias = bias
        self.activation = activation
        # gradients, filled by backward(); zeroed before each pass
        self.grad_weights: Tensor = Tensor.zeros(*weights.shape)
        self.grad_bias: Tensor = Tensor.zeros(bias.shape[0])
        # cache
        self._x: Tensor | None = None
        self._z: Tensor | None = None
        self._a: Tensor | None = None

    @classmethod
    def from_seed(
        cls, in_features: int, out_features: int, activation: str = "tanh", seed: int = 0
    ) -> DenseLayer:
        """Deterministic construction: seeded-normal weights, zero bias."""
        w = Tensor.randn(in_features, out_features, seed=seed)
        b = Tensor.zeros(out_features)
        return cls(w, b, activation)

    def forward(self, x: Tensor) -> Tensor:
        """``A = act(X @ W + b)`` for a batch ``X`` of shape (b, in)."""
        if x.ndim != 2 or x.shape[1] != self.weights.shape[0]:
            raise ValueError(
                f"forward needs X of shape (b, {self.weights.shape[0]}): got {x.shape}"
            )
        fn, _ = LAYER_ACTIVATIONS[self.activation]
        self._x = x
        self._z = _add_row(matmul(x, self.weights), self.bias)
        self._a = self._z.map(fn)  # type: ignore[call-arg]
        return self._a

    def backward(self, dl_da: Tensor) -> Tensor:
        """Propagate ``dL/dA`` to ``dL/dX``, storing ``dW`` and ``db``.

        The three factors, stated once more (module 03's sentence):

        * outer: ``dZ = dA * act'(Z)`` — elementwise;
        * middle: ``dW = X^T @ dZ`` and ``db = colsum(dZ)`` — how each
          parameter moved the pre-activation;
        * inner: ``dX = dZ @ W^T`` — how the input moved it; this is
          what the *previous* layer receives as its dL/dA.
        """
        if self._x is None or self._z is None or self._a is None:
            raise RuntimeError("backward() called before forward()")
        if dl_da.shape != self._a.shape:
            raise ValueError(f"backward needs dL/dA of shape {self._a.shape}: got {dl_da.shape}")
        _, grad_fn = LAYER_ACTIVATIONS[self.activation]
        # outer factor: dZ = dA * act'(Z), evaluated at the cached z
        dz = Tensor(
            [g * grad_fn(z) for g, z in zip(dl_da.data, self._z.data, strict=True)]
        ).reshape(
            *self._z.shape
        )  # type: ignore[call-arg]
        # middle factors: how each parameter moved the pre-activation
        self.grad_weights = matmul(self._x.T, dz)
        self.grad_bias = dz.sum(axis=0)
        # inner factor: what the previous layer receives as its dL/dA
        return matmul(dz, self.weights.T)

    def sgd_step(self, lr: float) -> None:
        """One gradient-descent update: ``w <- w - lr * dW`` (module 01)."""
        if lr < 0:
            raise ValueError(f"learning rate must be >= 0, got {lr}")
        self.weights = Tensor(
            [w - lr * g for w, g in zip(self.weights.data, self.grad_weights.data, strict=True)]
        ).reshape(*self.weights.shape)
        self.bias = Tensor(
            [b - lr * g for b, g in zip(self.bias.data, self.grad_bias.data, strict=True)]
        )


class MLP:
    """A stack of :class:`DenseLayer` objects trained by plain SGD.

    The whole of "how networks learn" in this module: forward through
    the stack, compute dL/d(output) with a loss, walk the stack
    *backwards* handing each layer the previous layer's dX, then update.
    """

    def __init__(self, layers: list[DenseLayer]) -> None:
        for a, b in zip(layers, layers[1:], strict=False):
            if a.weights.shape[1] != b.weights.shape[0]:
                raise ValueError(
                    f"layer widths must chain: {a.weights.shape} then {b.weights.shape}"
                )
        self.layers = layers

    def forward(self, x: Tensor) -> Tensor:
        a = x
        for layer in self.layers:
            a = layer.forward(a)
        return a

    def backward(self, dl_dout: Tensor) -> None:
        grad = dl_dout
        for layer in reversed(self.layers):
            grad = layer.backward(grad)

    def sgd_step(self, lr: float) -> None:
        for layer in self.layers:
            layer.sgd_step(lr)


# ---------------------------------------------------------------------------
# losses with their output-gradients (batch-mean forms)
# ---------------------------------------------------------------------------


def mse_loss(prediction: Tensor, target: Tensor) -> tuple[float, Tensor]:
    """Batch-mean MSE and dL/d(prediction).

    Mean over *all* elements (batch and features), with the explicit
    denominator in the gradient — module 02's rule. Returns
    ``(loss, grad)`` so callers cannot take one without the other.
    """
    if prediction.shape != target.shape:
        raise ValueError(f"mse_loss needs equal shapes: {prediction.shape} vs {target.shape}")
    diff = prediction - target
    loss = math.fsum(v * v for v in diff.data) / diff.numel()
    grad = diff * (2.0 / diff.numel())
    return loss, grad


def one_hot_targets(target_ids: list[int], n_classes: int) -> Tensor:
    """One-hot class targets as a (len(ids), n_classes) tensor."""
    rows = [[1.0 if j == i else 0.0 for j in range(n_classes)] for i in target_ids]
    return Tensor(rows)


def softmax_cross_entropy(logits: Tensor, target_ids: list[int]) -> tuple[float, Tensor]:
    """Batch-mean softmax cross-entropy and dL/d(logits).

    The gradient uses module 03's cancellation at network scale:
    with ``p = softmax(logits)`` and one-hot ``y``,
    ``dL/dlogits = (p - y) / B`` — no Jacobian matrix, one subtraction.
    The tests verify this against finite differences rather than
    trusting the algebra.
    """
    if logits.ndim != 2:
        raise ValueError(f"softmax_cross_entropy needs (B, C) logits: got {logits.shape}")
    if len(target_ids) != logits.shape[0]:
        raise ValueError(f"need one target id per row: {len(target_ids)} ids for {logits.shape}")
    for i in target_ids:
        if not 0 <= i < logits.shape[1]:
            raise ValueError(f"target id {i} outside {logits.shape[1]} classes")
    p = acts.softmax_tensor(logits)
    y = one_hot_targets(target_ids, logits.shape[1])
    b = logits.shape[0]
    loss = (
        -math.fsum(math.log(p.data[r * logits.shape[1] + t]) for r, t in enumerate(target_ids)) / b
    )
    grad = (p - y) * (1.0 / b)
    return loss, grad


# ---------------------------------------------------------------------------
# one training step / a training loop
# ---------------------------------------------------------------------------


def train_step_mse(mlp: MLP, x: Tensor, y: Tensor, lr: float) -> float:
    """Forward, MSE backward, SGD update; returns the batch loss."""
    pred = mlp.forward(x)
    loss, grad = mse_loss(pred, y)
    mlp.backward(grad)
    mlp.sgd_step(lr)
    return loss


def train_step_softmax_ce(mlp: MLP, x: Tensor, target_ids: list[int], lr: float) -> float:
    """Forward (logits), softmax-CE backward, SGD update; returns the loss."""
    logits = mlp.forward(x)
    loss, grad = softmax_cross_entropy(logits, target_ids)
    mlp.backward(grad)
    mlp.sgd_step(lr)
    return loss


def train_loop(
    mlp: MLP,
    x: Tensor,
    lr: float,
    epochs: int,
    *,
    loss: str = "mse",
    y: Tensor | None = None,
    target_ids: list[int] | None = None,
) -> list[float]:
    """Repeat :func:`train_step_*` and return the per-epoch loss curve.

    Deterministic by construction (no shuffling, no decay): the curve a
    test pins is the curve a reader reproduces. Use ``loss="mse"`` with
    ``y`` (a Tensor of targets) or ``loss="ce"`` with ``target_ids``.
    """
    curve: list[float] = []
    for _ in range(epochs):
        if loss == "mse":
            if y is None:
                raise ValueError("loss='mse' needs y")
            curve.append(train_step_mse(mlp, x, y, lr))
        elif loss == "ce":
            if target_ids is None:
                raise ValueError("loss='ce' needs target_ids")
            curve.append(train_step_softmax_ce(mlp, x, target_ids, lr))
        else:
            raise ValueError(f"unknown loss {loss!r} (mse | ce)")
    return curve


__all__ = [
    "DenseLayer",
    "LAYER_ACTIVATIONS",
    "MLP",
    "mse_loss",
    "one_hot_targets",
    "softmax_cross_entropy",
    "train_loop",
    "train_step_mse",
    "train_step_softmax_ce",
]
