"""P09 — Distribution shift and subgroup reliability (stdlib-only, deterministic).

Implements Chapter 17's discipline as code on a seeded synthetic
deployment: a classifier trained in-distribution is evaluated on an
OOD slice with a group structure, measuring:

- ID vs OOD accuracy (with Wilson intervals);
- worst-group vs average-group accuracy (the aggregate that hides
  the group);
- calibration degradation under shift (binned reliability, ECE);
- one mitigation (group-aware cost reweighting) with the coupling
  caveat Ch. 17 prices.

The data model is the classic spurious-correlation setup: the label
depends on a core feature x1; a spurious feature x2 correlates with
the label *only in the ID distribution*; under the OOD shift the
spurious correlation flips/weakens, and the ID-trained classifier
(which leaned on x2) degrades exactly where it trusted x2 most.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from random import Random

__all__ = [
    "Example",
    "Dataset",
    "make_deployment",
    "fit_logistic",
    "predict",
    "wilson_interval",
    "accuracy_by_slice",
    "worst_group_gap",
    "binned_ece",
    "ShiftAuditResult",
    "run_shift_audit",
    "mitigate_group_weights",
]


@dataclass(frozen=True)
class Example:
    x1: float  # core feature: P(y=1) depends on it everywhere
    x2: float  # spurious feature: correlates with y only in ID
    y: int
    group: int


@dataclass
class Dataset:
    examples: list[Example]
    name: str


def make_deployment(seed: int = 11) -> dict[str, Dataset]:
    """Deterministic ID / OOD / groups.

    Groups differ in base rate (P(y=1) via an intercept offset), and
    in ID the spurious feature x2 = y + noise; in OOD x2 = (1 - y) +
    noise — the correlation *flips*, breaking any classifier that
    leaned on it.
    """
    rng = Random(seed)

    def _draw(
        n: int,
        group: int,
        y_rate: float,
        spurious_flip: bool,
        name: str,
        x1_noise: float = 0.8,
    ) -> Dataset:
        ex: list[Example] = []
        for _ in range(n):
            y = 1 if rng.random() < y_rate else 0
            x1 = (y - 0.5) * 2.0 + rng.gauss(0.0, x1_noise)  # core signal (noise varies by group)
            raw = y if not spurious_flip else (1 - y)
            x2 = raw + rng.gauss(0.0, 0.7)
            ex.append(Example(x1=round(x1, 6), x2=round(x2, 6), y=y, group=group))
        return Dataset(examples=ex, name=name)

    # ID: groups 0/1 with different base rates AND different core-signal noise
    # (group 0's core signal is weaker, so ID training leans harder on the
    # spurious x2 for group 0 -- the worst-group setup)
    id_g0 = _draw(500, 0, 0.35, False, "ID-g0", x1_noise=1.4)
    id_g1 = _draw(500, 1, 0.65, False, "ID-g1", x1_noise=0.5)
    # OOD: same base rates, spurious flipped, per-group noise preserved
    ood_g0 = _draw(250, 0, 0.35, True, "OOD-g0", x1_noise=1.4)
    ood_g1 = _draw(250, 1, 0.65, True, "OOD-g1", x1_noise=0.5)
    return {
        "id": Dataset(examples=id_g0.examples + id_g1.examples, name="ID"),
        "ood": Dataset(examples=ood_g0.examples + ood_g1.examples, name="OOD"),
        "id_g0": id_g0,
        "id_g1": id_g1,
        "ood_g0": ood_g0,
        "ood_g1": ood_g1,
    }


def _sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    return math.exp(z) / (1.0 + math.exp(z))


def fit_logistic(
    data: Dataset, epochs: int = 300, lr: float = 0.1, weights: dict[int, float] | None = None
) -> tuple[float, float, float, float]:
    """2-feature logistic + intercept by plain SGD; group weights optional."""
    w1, w2, b = 0.0, 0.0, 0.0
    rows = [(e.x1, e.x2, e.y, (weights or {}).get(e.group, 1.0)) for e in data.examples]
    for _ in range(epochs):
        g1 = g2 = gb = 0.0
        for x1, x2, y, w in rows:
            p = _sigmoid(w1 * x1 + w2 * x2 + b)
            e = w * (p - y)
            g1 += e * x1
            g2 += e * x2
            gb += e
        n = len(rows)
        w1 -= lr * g1 / n
        w2 -= lr * g2 / n
        b -= lr * gb / n
    return w1, w2, b, 0.0


def predict(model: tuple[float, float, float, float], e: Example) -> float:
    w1, w2, b, _ = model
    return _sigmoid(w1 * e.x1 + w2 * e.x2 + b)


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def accuracy_by_slice(
    model: tuple[float, float, float, float], data: Dataset
) -> tuple[float, tuple[float, float], int]:
    k = sum(1 for e in data.examples if (predict(model, e) >= 0.5) == bool(e.y))
    n = len(data.examples)
    lo, hi = wilson_interval(k, n)
    return k / n, (lo, hi), n


def worst_group_gap(
    model: tuple[float, float, float, float], groups: list[Dataset]
) -> dict[str, float]:
    accs = {}
    for g in groups:
        acc, _, _ = accuracy_by_slice(model, g)
        accs[g.name] = acc
    worst = min(accs.values())
    avg = sum(accs.values()) / len(accs)
    return {"worst": worst, "average": avg, "gap": avg - worst}


def binned_ece(model: tuple[float, float, float, float], data: Dataset, bins: int = 10) -> float:
    """Binned expected calibration error."""
    n = len(data.examples)
    total = 0.0
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        members = []
        for e in data.examples:
            p = predict(model, e)
            if lo <= p < hi or (i == bins - 1 and p == 1.0):
                members.append((p, e.y))
        if members:
            conf = sum(p for p, _ in members) / len(members)
            freq = sum(y for _, y in members) / len(members)
            total += (len(members) / n) * abs(conf - freq)
    return total


@dataclass
class ShiftAuditResult:
    id_acc: float
    id_ci: tuple[float, float]
    ood_acc: float
    ood_ci: tuple[float, float]
    worst_group: float
    average_group: float
    group_gap: float
    ece_id: float
    ece_ood: float
    mitigated_worst: float
    mitigated_average: float


def mitigate_group_weights(data: Dataset, groups: list[Dataset]) -> dict[int, float]:
    """One mitigation: upweight the group with lower ID accuracy.

    The Ch. 17 caveat: this is DRO-lite *without* the regularization
    coupling the GroupDRO paper requires — the project prices the
    half-recipe honestly.
    """
    base = fit_logistic(data)
    accs = {}
    for g in groups:
        acc, _, _ = accuracy_by_slice(base, g)
        accs[g.name] = acc
    worst_name = min(accs, key=accs.get)
    gmap = {}
    for g in groups:
        gmap[g.name] = g
    worst = gmap[worst_name]
    weight = 1.0 + 2.0 * (accs[max(accs, key=accs.get)] - accs[worst_name])
    worst_groups = {e.group for e in worst.examples}
    return {e.group: (weight if e.group in worst_groups else 1.0) for e in data.examples}


def run_shift_audit(seed: int = 11) -> ShiftAuditResult:
    d = make_deployment(seed=seed)
    model = fit_logistic(d["id"])
    id_acc, id_ci, _ = accuracy_by_slice(model, d["id"])
    ood_acc, ood_ci, _ = accuracy_by_slice(model, d["ood"])
    # worst-group measured on the OOD slice (the deployment's reality),
    # with the ID slice's groups as the in-distribution reference
    wg = worst_group_gap(model, [d["ood_g0"], d["ood_g1"]])
    ece_id = binned_ece(model, d["id"])
    ece_ood = binned_ece(model, d["ood"])
    # mitigation: group weights fit on ID groups (the honest limitation --
    # the deployment cannot see OOD labels), then re-evaluated OOD
    wts = mitigate_group_weights(d["id"], [d["id_g0"], d["id_g1"]])
    model_mit = fit_logistic(d["id"], weights=wts)
    wg_mit = worst_group_gap(model_mit, [d["ood_g0"], d["ood_g1"]])
    return ShiftAuditResult(
        id_acc=id_acc,
        id_ci=id_ci,
        ood_acc=ood_acc,
        ood_ci=ood_ci,
        worst_group=wg["worst"],
        average_group=wg["average"],
        group_gap=wg["gap"],
        ece_id=ece_id,
        ece_ood=ece_ood,
        mitigated_worst=wg_mit["worst"],
        mitigated_average=wg_mit["average"],
    )
