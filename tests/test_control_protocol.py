"""P08 tests — deterministic pins for the control-protocol frontier."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_safety_course.control_protocol import (  # noqa: E402
    TRUSTED_POLICY,
    UNTRUSTED_POLICY,
    Monitor,
    Task,
    frontier,
    wilson_interval,
)


def test_wilson_known() -> None:
    lo, hi = wilson_interval(46, 200)
    assert abs(lo - 0.1771) < 5e-4
    assert abs(hi - 0.2931) < 5e-4


def test_deterministic() -> None:
    f1 = frontier(seed=9)
    f2 = frontier(seed=9)
    assert [r.safety for r in f1] == [r.safety for r in f2]
    assert [r.completed for r in f1] == [r.completed for r in f2]


def test_policies_semantics() -> None:
    attack = Task(task_id=3, is_attack=True)
    assert UNTRUSTED_POLICY(attack)  # executes everything
    assert not TRUSTED_POLICY(attack)  # trusted catches ALL attacks
    # benign: 95% completed under trusted (id % 20 != 0)
    assert TRUSTED_POLICY(Task(task_id=7, is_attack=False))
    assert not TRUSTED_POLICY(Task(task_id=20, is_attack=False))


def test_monitor_rates() -> None:
    m = Monitor(recall=1.0, false_flag=0.0, seed=1)
    assert m.flags(Task(task_id=1, is_attack=True))
    assert not m.flags(Task(task_id=1, is_attack=False))
    m0 = Monitor(recall=0.0, false_flag=0.0, seed=1)
    assert not m0.flags(Task(task_id=1, is_attack=True))


def test_frontier_pinned() -> None:
    """Pinned 2026-10-23, seed=9 — the paired three-protocol frontier."""
    f = frontier(seed=9)
    no_mon, simple, defer = f
    # baseline: every attack executes, everything completes
    assert no_mon.safety == 0.0
    assert no_mon.usefulness == 1.0
    assert no_mon.trusted_executions == 0
    # simple monitor: safety = recall on this seed (17/60 violations)
    assert simple.violations == 17
    assert abs(simple.safety - 0.717) < 2e-3
    assert abs(simple.usefulness - 0.910) < 2e-3  # the false-flag cost
    # defer: SAME violations (paired flagging, trusted catches flagged)
    assert defer.violations == 17
    assert defer.safety == simple.safety
    # defer buys the usefulness back at the audit budget's cost
    assert defer.usefulness > simple.usefulness
    assert defer.trusted_executions == 61
    assert defer.trusted_executions > 0


def test_frontier_safety_intervals_overlap_honestly() -> None:
    """The monitor's recall is the safety ceiling for BOTH protocols:
    their intervals are identical (paired) — the residual 17 missed
    attacks are the named open hole neither protocol touches."""
    f = frontier(seed=9)
    simple, defer = f[1], f[2]
    assert simple.safety_ci == defer.safety_ci
    assert simple.safety_ci[0] < 0.70  # honestly below the nominal recall
