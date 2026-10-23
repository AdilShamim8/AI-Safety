"""P05 tests — deterministic pins for the weak-to-strong analogue."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_safety_course.w2s_audit import (  # noqa: E402
    WeakSupervisor,
    run_w2s,
    true_label,
    wilson_interval,
)


def test_wilson_known() -> None:
    lo, hi = wilson_interval(46, 200)
    assert abs(lo - 0.1771) < 5e-4
    assert abs(hi - 0.2931) < 5e-4


def test_deterministic() -> None:
    r1 = run_w2s(seed=5)
    r2 = run_w2s(seed=5)
    assert r1.strong_acc_id == r2.strong_acc_id
    assert r1.weak_acc_id == r2.weak_acc_id


def test_true_label_invariant_structure() -> None:
    # the boundary is deterministic and mildly nonlinear
    # boundary value = x1 + 0.7*x2 + 0.3*sin(x1), label 1 iff > 0.1
    assert true_label(1.0, 1.0) == 1  # 1.0 + 0.7 + 0.252 = 1.952 > 0.1
    assert true_label(-1.0, -1.0) == 0  # -1.0 - 0.7 - 0.252 < 0.1
    assert true_label(0.5, -0.5) == 1  # 0.5 - 0.35 + 0.144 = 0.294 > 0.1
    assert true_label(0.0, 0.0) == 0  # 0.0 + 0.0 + 0.0 = 0.0 < 0.1


def test_weak_supervisor_flip_rate() -> None:
    weak = WeakSupervisor(flip_prob=0.0, seed=1)
    assert weak.label(1.0, 1.0) == true_label(1.0, 1.0)
    # with flip_prob=1.0 the supervisor is always wrong
    weak1 = WeakSupervisor(flip_prob=1.0, seed=1)
    assert weak1.label(1.0, 1.0) == 1 - true_label(1.0, 1.0)


def test_w2s_effect_pinned() -> None:
    """Pinned 2026-10-23, seed=5: the weak-to-strong effect emerges."""
    r = run_w2s(seed=5)
    # weak supervisor ~ 1 - flip_prob
    assert abs(r.weak_acc_id - 0.708) < 2e-3
    # strong learner trained ONLY on weak labels far exceeds the supervisor
    assert abs(r.strong_acc_id - 0.963) < 3e-3
    assert r.exceeds_supervisor
    # the intervals are disjoint: the effect is not noise
    assert r.strong_ci_id[0] > r.weak_ci_id[1]
    # oversight gap recovered, pinned
    assert abs(r.oversight_gap_recovered - 0.255) < 5e-3


def test_recovery_persists_under_covariate_shift() -> None:
    """The recovery is shift-robust: the learner approximated the
    invariant boundary, not the supervisor's noise."""
    r = run_w2s(seed=5)
    assert abs(r.strong_acc_ood - 0.975) < 3e-3
    assert abs(r.weak_acc_ood - 0.677) < 3e-3
    assert r.strong_ci_ood[0] > r.weak_ci_ood[1]
    # OOD strength within a few points of ID strength
    assert r.strong_acc_ood > r.strong_acc_id - 0.03


def test_upper_reference_reachable() -> None:
    """The ground-truth upper reference: the learner approaches (but
    honestly does not reach) the Bayes rate of a linear learner on
    the nonlinear boundary."""
    r = run_w2s(seed=5)
    assert 0.90 <= r.strong_acc_id <= 0.99  # real ceiling below 1.0
