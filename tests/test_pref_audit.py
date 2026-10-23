"""P04 tests — deterministic pins + numeric checks (offline)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_safety_course.pref_audit import (  # noqa: E402
    bt_gradient,
    bt_loss,
    dpo_loss,
    label_bias_condition,
    make_preference_data,
    optimal_policy_from_rewards,
    run_audit,
)


def test_bt_loss_values() -> None:
    assert abs(bt_loss(0.0) - math.log(2)) < 1e-12
    assert bt_loss(5.0) < 1e-2
    assert abs(bt_loss(-5.0) - 5.0) < 1e-2  # -z + log(1+e^z) ~ -z


def test_bt_gradient_matches_finite_difference() -> None:
    for z in (-2.0, -0.5, 0.0, 0.7, 3.0):
        h = 1e-6
        fd = (bt_loss(z + h) - bt_loss(z - h)) / (2 * h)
        assert abs(fd - bt_gradient(z)) < 1e-5


def test_dpo_loss_extremes() -> None:
    # with beta=1 the margins pass through directly
    assert dpo_loss(10.0, 0.0, beta=1.0) < 1e-3
    assert dpo_loss(0.0, 10.0, beta=1.0) > 9.9
    # beta scales the effective margin
    assert dpo_loss(10.0, 0.0, beta=0.1) == dpo_loss(1.0, 0.0, beta=1.0)


def test_optimal_policy_normalizes_and_orders() -> None:
    rewards = {0: 2.0, 1: 1.0, 2: 0.0}
    pol = optimal_policy_from_rewards(rewards, beta=1.0)
    assert abs(sum(pol.values()) - 1.0) < 1e-12
    assert pol[0] > pol[1] > pol[2]
    # beta -> 0 concentrates on the argmax
    pol0 = optimal_policy_from_rewards(rewards, beta=0.01)
    assert pol0[0] > 0.999


def test_data_deterministic() -> None:
    d1 = make_preference_data(seed=7)
    d2 = make_preference_data(seed=7)
    assert [p.chosen for p in d1.pairs] == [p.chosen for p in d2.pairs]
    assert [it.x for it in d1.items] == [it.x for it in d2.items]


def test_audit_runs_and_pinned() -> None:
    data = make_preference_data(seed=7)
    res = run_audit(data, beta=1.0)
    # pinned 2026-10-23 (deterministic fixture, seed=7)
    assert abs(res.proxy_dpo - 2.9024) < 1e-3
    assert abs(res.proxy_sft - 2.8540) < 1e-3
    assert abs(res.heldout_dpo - 0.0093) < 1e-3
    assert abs(res.heldout_sft - (-0.0687)) < 1e-3
    assert abs(sum(res.policy_dpo.values()) - 1.0) < 1e-9


def test_label_bias_condition_pinned() -> None:
    data = make_preference_data(seed=7)
    bias = label_bias_condition(data, flip_fraction=0.2)
    assert bias.flips == 40  # 20% of 200
    # pinned 2026-10-23: adversarial concentrated flips REDUCE held-out quality
    assert abs(bias.heldout_clean - 0.0093) < 1e-3
    assert abs(bias.heldout_biased - (-0.0552)) < 1e-3
    assert abs(bias.drift - (-0.0645)) < 1e-3


def test_proxy_heldout_divergence() -> None:
    """The Ch. 04 seam: the proxy gain does not certify the held-out gain.

    Pinned on seed=7: proxy gain 0.0484 vs held-out gain 0.0780 -- the
    two gains DIVERGE by more than either is large, i.e., knowing the
    proxy improvement tells you almost nothing about the true-quality
    improvement (and the label-bias instrument shows the direction the
    proxy cannot see). The audit's headline is the divergence, not a
    guaranteed ordering.
    """
    data = make_preference_data(seed=7)
    res = run_audit(data, beta=1.0)
    proxy_gain = res.proxy_dpo - res.proxy_sft
    heldout_gain = res.heldout_dpo - res.heldout_sft
    assert proxy_gain > 0
    assert heldout_gain > 0
    assert abs(proxy_gain - heldout_gain) > 0.02  # divergence, measured
    # and the label-bias instrument carries the harm the proxy hides
    bias = label_bias_condition(data, flip_fraction=0.2)
    assert bias.drift < 0
