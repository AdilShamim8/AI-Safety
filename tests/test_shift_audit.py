"""P09 tests — deterministic pins for the shift/subgroup audit."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_safety_course.shift_audit import (  # noqa: E402
    accuracy_by_slice,
    binned_ece,
    fit_logistic,
    make_deployment,
    run_shift_audit,
    wilson_interval,
)


def test_wilson_matches_known_values() -> None:
    lo, hi = wilson_interval(46, 200)
    assert abs(lo - 0.1771) < 5e-4
    assert abs(hi - 0.2931) < 5e-4
    lo, hi = wilson_interval(0, 150)
    assert lo == 0.0
    assert abs(hi - 0.0250) < 5e-4  # zero-numerator bound


def test_data_deterministic() -> None:
    d1 = make_deployment(seed=11)
    d2 = make_deployment(seed=11)
    assert [e.x1 for e in d1["id"].examples] == [e.x1 for e in d2["id"].examples]
    assert [e.y for e in d1["ood"].examples] == [e.y for e in d2["ood"].examples]


def test_audit_pinned_numbers() -> None:
    """Pinned 2026-10-23, seed=11 — the whole audit in one test."""
    r = run_shift_audit(seed=11)
    # ID vs OOD with intervals
    assert abs(r.id_acc - 0.899) < 2e-3
    assert abs(r.ood_acc - 0.674) < 2e-3
    assert r.ood_ci[1] < r.id_ci[0]  # disjoint: the shift drop is real
    # group structure in ID (the aggregate hides the group)
    assert abs(r.average_group - 0.674) < 2e-3
    assert r.worst_group < r.average_group
    # calibration degrades under shift (Ch. 17's station 4)
    assert r.ece_ood > 2 * r.ece_id


def test_id_group_gap_exists() -> None:
    d = make_deployment(seed=11)
    m = fit_logistic(d["id"])
    a0, ci0, _ = accuracy_by_slice(m, d["id_g0"])
    a1, ci1, _ = accuracy_by_slice(m, d["id_g1"])
    # pinned: 0.840 vs 0.958 — the ID aggregate (0.899) hides both tails
    assert abs(a0 - 0.840) < 3e-3
    assert abs(a1 - 0.958) < 3e-3
    assert ci0[1] < ci1[0]  # disjoint group intervals


def test_half_recipe_mitigation_fails_honestly() -> None:
    """The GroupDRO coupling caveat, reproduced: reweighting alone does
    not transfer across the shift — the mitigated worst-group is no
    better than the unmitigated one (pinned: 0.608 vs 0.612)."""
    r = run_shift_audit(seed=11)
    assert abs(r.mitigated_worst - 0.608) < 4e-3
    assert r.mitigated_worst <= r.worst_group + 2e-3  # no real improvement
    assert r.mitigated_average < r.average_group  # and it costs the average


def test_ece_pinned() -> None:
    d = make_deployment(seed=11)
    m = fit_logistic(d["id"])
    assert abs(binned_ece(m, d["id"]) - 0.039) < 5e-3
    assert abs(binned_ece(m, d["ood"]) - 0.115) < 8e-3
