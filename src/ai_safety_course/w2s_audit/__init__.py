"""P05 — Weak-to-strong / scalable-oversight analogue (stdlib-only, deterministic).

A small, fully-inspectable analogue of the weak-to-strong
generalization setting (Ch. 05's scalable-oversight question):
a *weak supervisor* labels training data with i.i.d. label noise
(the simplest error structure a higher-capacity learner can average
out); a *strong learner* with the richer view (raw features, linear
boundary) trains on the weak labels; a *ground-truth upper reference*
(the true labeling function) scores everything.

The quantity of interest is the **oversight gap recovered**: can the
strong learner exceed its supervisor — recover signal the supervisor
never reliably provided — and does the recovery persist under pure
covariate shift (the boundary is invariant; the input distribution
moves)?

Analogue-scope honesty: real supervisors make *systematic* errors
that resist noise-averaging; this minimal analogue models the
mechanism (i.i.d. noise + capacity) in its cleanest form — the
small-analogue scope statement the project brief requires.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

__all__ = [
    "Point",
    "make_task",
    "true_label",
    "WeakSupervisor",
    "fit_strong_learner",
    "strong_predict",
    "W2SResult",
    "run_w2s",
    "wilson_interval",
]


@dataclass(frozen=True)
class Point:
    x1: float
    x2: float
    y: int  # ground truth


def true_label(x1: float, x2: float) -> int:
    """The invariant true boundary (mildly nonlinear so a linear
    learner has a real ceiling below 100%)."""
    return 1 if (x1 + 0.7 * x2 + 0.3 * math.sin(x1)) > 0.1 else 0


class WeakSupervisor:
    """Labels with the true function corrupted by i.i.d. flips.

    ``flip_prob`` is the supervisor's limitation rate; the flips are
    seeded and per-point (deterministic given the seed).
    """

    def __init__(self, flip_prob: float = 0.30, seed: int = 3) -> None:
        self.flip_prob = flip_prob
        self._rng = Random(seed)

    def label(self, x1: float, x2: float) -> int:
        y = true_label(x1, x2)
        if self._rng.random() < self.flip_prob:
            return 1 - y
        return y


def make_task(seed: int = 5, n_train: int = 1500, n_test: int = 400) -> dict[str, list[Point]]:
    rng = Random(seed)

    def draw(n: int, shift: float) -> list[Point]:
        pts = []
        for _ in range(n):
            x1 = rng.gauss(0.0, 1.0) + shift
            x2 = rng.gauss(0.0, 1.0) + 0.5 * shift
            pts.append(Point(x1=round(x1, 6), x2=round(x2, 6), y=true_label(x1, x2)))
        return pts

    return {
        "train": draw(n_train, 0.0),
        "test_id": draw(n_test, 0.0),
        "test_ood": draw(n_test, 1.2),  # pure covariate shift
    }


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    return math.exp(z) / (1.0 + math.exp(z))


def fit_strong_learner(
    train: list[Point], weak: WeakSupervisor, epochs: int = 600, lr: float = 0.3
) -> tuple[float, float, float]:
    """Linear logistic learner on raw features, trained on WEAK labels."""
    w1 = w2 = b = 0.0
    rows = [(p.x1, p.x2, weak.label(p.x1, p.x2)) for p in train]
    for _ in range(epochs):
        g1 = g2 = gb = 0.0
        for x1, x2, yl in rows:
            p = _sigmoid(w1 * x1 + w2 * x2 + b)
            e = p - yl
            g1 += e * x1
            g2 += e * x2
            gb += e
        n = len(rows)
        w1 -= lr * g1 / n
        w2 -= lr * g2 / n
        b -= lr * gb / n
    return w1, w2, b


def strong_predict(model: tuple[float, float, float], x1: float, x2: float) -> int:
    w1, w2, b = model
    return 1 if _sigmoid(w1 * x1 + w2 * x2 + b) >= 0.5 else 0


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def _acc(preds: list[int], truths: list[int]) -> tuple[float, tuple[float, float]]:
    k = sum(1 for p, t in zip(preds, truths, strict=True) if p == t)
    n = len(truths)
    lo, hi = wilson_interval(k, n)
    return k / n, (lo, hi)


@dataclass
class W2SResult:
    weak_acc_id: float
    weak_ci_id: tuple[float, float]
    strong_acc_id: float
    strong_ci_id: tuple[float, float]
    strong_acc_ood: float
    strong_ci_ood: tuple[float, float]
    weak_acc_ood: float
    weak_ci_ood: tuple[float, float]
    oversight_gap_recovered: float

    @property
    def exceeds_supervisor(self) -> bool:
        """The weak-to-strong effect: learner beats its supervisor."""
        return self.strong_acc_id > self.weak_acc_id


def run_w2s(seed: int = 5, flip_prob: float = 0.30) -> W2SResult:
    task = make_task(seed=seed)
    weak = WeakSupervisor(flip_prob=flip_prob, seed=seed + 100)
    model = fit_strong_learner(task["train"], weak)

    weak_preds_id = [weak.label(p.x1, p.x2) for p in task["test_id"]]
    weak_preds_ood = [weak.label(p.x1, p.x2) for p in task["test_ood"]]
    strong_preds_id = [strong_predict(model, p.x1, p.x2) for p in task["test_id"]]
    strong_preds_ood = [strong_predict(model, p.x1, p.x2) for p in task["test_ood"]]

    truths_id = [p.y for p in task["test_id"]]
    truths_ood = [p.y for p in task["test_ood"]]

    weak_acc, weak_ci = _acc(weak_preds_id, truths_id)
    strong_acc, strong_ci = _acc(strong_preds_id, truths_id)
    strong_ood, strong_ood_ci = _acc(strong_preds_ood, truths_ood)
    weak_ood, weak_ood_ci = _acc(weak_preds_ood, truths_ood)

    return W2SResult(
        weak_acc_id=weak_acc,
        weak_ci_id=weak_ci,
        strong_acc_id=strong_acc,
        strong_ci_id=strong_ci,
        strong_acc_ood=strong_ood,
        strong_ci_ood=strong_ood_ci,
        weak_acc_ood=weak_ood,
        weak_ci_ood=weak_ood_ci,
        oversight_gap_recovered=strong_acc - weak_acc,
    )
