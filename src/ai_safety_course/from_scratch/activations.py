"""activations — the six nonlinearities the video teaches (track module 03).

Implements the companion repository's module ``05_activation_functions``
(SRC-REPO-001, full-text-read: ReLU, sigmoid, tanh, SiLU, SwiGLU, softmax)
and the video's *Activation Functions* chapter (SRC-VIDEO-001,
page-inspected), in plain stdlib math. Note:
``research/ai-researcher-from-scratch/03-neuron-and-activations.md``.

Every function comes with its **exact derivative** — not because the
toolbox will differentiate for you (module 04 does that by hand), but
because an activation without its derivative is half an object: the
derivative is the part training actually uses. Each ``*_grad`` returns
the derivative with respect to the *pre-activation input* ``z``, given
whatever it needs (for most, ``z`` itself; for softmax, the whole
output distribution).

Conventions
-----------
* ``z`` is the pre-activation scalar; tensor-free on purpose — module
  03's neuron is scalar arithmetic you can check by hand.
* ReLU at exactly 0 returns derivative 0 (the subgradient convention
  torch's ``relu`` backward also takes; stated so nobody rediscovers it).
* Softmax is computed with the max-subtraction trick for numerical
  stability — the trick is *the* lesson of numerical softmax and is
  commented inline.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from ai_safety_course.from_scratch.tensors import Tensor

# ---------------------------------------------------------------------------
# rectified linear unit
# ---------------------------------------------------------------------------


def relu(z: float) -> float:
    """max(0, z) — the modern default nonlinearity."""
    return z if z > 0.0 else 0.0


def relu_grad(z: float) -> float:
    """1 for positive z, 0 otherwise (0 at exactly 0, by convention)."""
    return 1.0 if z > 0.0 else 0.0


# ---------------------------------------------------------------------------
# sigmoid
# ---------------------------------------------------------------------------


def sigmoid(z: float) -> float:
    """The logistic function 1 / (1 + e^{-z}); range (0, 1).

    Numerically stable by branch: for negative z the naive
    ``1/(1+exp(-z))`` computes ``exp(-z)`` with a huge exponent and
    overflows; the ``e/(1+e)`` form with ``e = exp(z)`` cannot.
    """
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def sigmoid_grad_from_output(s: float) -> float:
    """sigmoid'(z) given s = sigmoid(z): s (1 - s)."""
    return s * (1.0 - s)


def sigmoid_grad(z: float) -> float:
    """sigmoid'(z) = sigma(z) (1 - sigma(z))."""
    return sigmoid_grad_from_output(sigmoid(z))


# ---------------------------------------------------------------------------
# hyperbolic tangent
# ---------------------------------------------------------------------------


def tanh(z: float) -> float:
    """tanh(z); range (-1, 1) — the zero-centered sibling of sigmoid."""
    return math.tanh(z)


def tanh_grad_from_output(t: float) -> float:
    """tanh'(z) given t = tanh(z): 1 - t^2."""
    return 1.0 - t * t


def tanh_grad(z: float) -> float:
    """tanh'(z) = 1 - tanh(z)^2."""
    return tanh_grad_from_output(math.tanh(z))


# ---------------------------------------------------------------------------
# SiLU (swish)
# ---------------------------------------------------------------------------


def silu(z: float) -> float:
    """SiLU / swish: z * sigmoid(z) — self-gated, smooth, unbounded above.

    The companion lesson's framing: the input *gates itself* — how much
    of z passes through is decided by sigmoid(z), a function of z.
    """
    return z * sigmoid(z)


def silu_grad(z: float) -> float:
    """SiLU'(z) = sigma(z) (1 + z (1 - sigma(z)))."""
    s = sigmoid(z)
    return s * (1.0 + z * (1.0 - s))


# ---------------------------------------------------------------------------
# SwiGLU (elementwise gate form)
# ---------------------------------------------------------------------------


def swiglu(value: float, gate: float) -> float:
    """SwiGLU in its elementwise form: silu(gate) * value.

    In a transformer FFN the two arguments are two different linear
    projections of the same input (module 05 wires this up); here the
    gate/value split is exposed so the activation itself is testable.
    """
    return silu(gate) * value


def swiglu_grads(value: float, gate: float) -> tuple[float, float]:
    """(d/dvalue, d/dgate) of SwiGLU: (silu(gate), silu'(gate) * value)."""
    return silu(gate), silu_grad(gate) * value


# ---------------------------------------------------------------------------
# softmax
# ---------------------------------------------------------------------------


def softmax_list(logits: Sequence[float]) -> list[float]:
    """Softmax over a 1-D sequence, computed stably.

    max(z) is subtracted from every logit before exponentiation.
    softmax(z - max(z)) is *identical* to softmax(z) — both the exp
    numerator and the normalization denominator scale by the same
    e^{max(z)} and cancel — but the subtracted form cannot overflow:
    exp(1000) is inf, exp(1000 - 1000) is 1. Shift invariance is the
    one-line proof, and it is pinned by a test.
    """
    if not logits:
        raise ValueError("softmax needs a nonempty logit sequence")
    m = max(float(v) for v in logits)
    exps = [math.exp(float(v) - m) for v in logits]
    total = math.fsum(exps)
    return [e / total for e in exps]


def softmax_tensor(logits: Tensor) -> Tensor:
    """Softmax over the last axis of a 1-D or 2-D Tensor (rows independently)."""
    if logits.ndim == 1:
        return Tensor(softmax_list(logits.data))
    if logits.ndim == 2:
        n = logits.shape[1]
        rows = [softmax_list(logits.data[r * n : (r + 1) * n]) for r in range(logits.shape[0])]
        return Tensor(rows)
    raise ValueError(f"softmax_tensor supports 1-D/2-D, got shape {logits.shape}")


def softmax_grad(s: Sequence[float]) -> list[list[float]]:
    """The Jacobian of softmax given its own output s.

    J[i][j] = s_i * (delta_ij - s_j). Used by module 04's backprop when
    a softmax sits at the end of the network without cross-entropy's
    convenient cancellation.
    """
    n = len(s)
    return [[s[i] * ((1.0 if i == j else 0.0) - s[j]) for j in range(n)] for i in range(n)]


def softmax_list_grad(s: Sequence[float], dL_ds: Sequence[float]) -> list[float]:
    """Chain-rule helper: dL/dz given s = softmax(z) and dL/ds.

    dL/dz_j = s_j (dL/ds_j - sum_i dL/ds_i * s_i) — the standard
    collapsed form of the softmax Jacobian, one pass, no matrix.
    """
    if len(s) != len(dL_ds):
        raise ValueError(
            f"softmax_list_grad needs equal lengths: s has {len(s)}, dL/ds has {len(dL_ds)}"
        )
    dot = math.fsum(a * b for a, b in zip(dL_ds, s, strict=True))
    return [s[j] * (dL_ds[j] - dot) for j in range(len(s))]


__all__ = [
    "relu",
    "relu_grad",
    "sigmoid",
    "sigmoid_grad",
    "sigmoid_grad_from_output",
    "silu",
    "silu_grad",
    "softmax_grad",
    "softmax_list",
    "softmax_list_grad",
    "softmax_tensor",
    "swiglu",
    "swiglu_grads",
    "tanh",
    "tanh_grad",
    "tanh_grad_from_output",
]
