"""P06 tests — deterministic pins for the activation-patching audit."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_safety_course.patch_audit import (  # noqa: E402
    corrupt,
    exact_binom_one_sided,
    fit_readout,
    forward,
    holm,
    make_slice,
    mcnemar_exact_one_sided,
    probe_accuracy,
    run_patch_audit,
    wilson_interval,
)


def test_wilson_matches_known_values() -> None:
    lo, hi = wilson_interval(46, 200)
    assert abs(lo - 0.1771) < 5e-4
    assert abs(hi - 0.2931) < 5e-4


def test_exact_binomial_and_holm() -> None:
    # P[X >= 8] under Binomial(8, 0.5) = 1/256
    assert abs(exact_binom_one_sided(8, 8) - 0.00390625) < 1e-12
    # Holm: smallest p scaled by m, running max, capped at 1
    adj = holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert abs(adj["a"] - 0.03) < 1e-12
    assert abs(adj["c"] - 0.06) < 1e-12  # 2 * 0.03, lifted above b by the max
    assert abs(adj["b"] - 0.06) < 1e-12
    assert all(v <= 1.0 for v in adj.values())


def test_mcnemar_exact_one_sided() -> None:
    # b=102, c=15: the pinned audit value must be tiny and one-sided
    p = mcnemar_exact_one_sided(102, 15)
    assert p < 1e-15


def test_data_and_contrasts_deterministic() -> None:
    d1 = make_slice(123, 50, 0.9)
    d2 = make_slice(123, 50, 0.9)
    assert [ex.a_obs for ex in d1] == [ex.a_obs for ex in d2]
    assert [ex.b for ex in d1] == [ex.b for ex in d2]
    ex = d1[0]
    c1 = corrupt(ex, "label_flip", 7)
    c1b = corrupt(ex, "label_flip", 7)
    assert c1.a_obs == c1b.a_obs and c1.b == c1b.b
    assert c1.t == ex.t  # matched-topic control baked into both contrasts
    c2 = corrupt(ex, "b_flip", 7)
    assert c2.a_obs == ex.a_obs and c2.b == -ex.b and c2.t == ex.t


def test_readout_learns_the_shortcut() -> None:
    """The organism's headline: the fitted readout leans on the CLEAN
    spurious channel (b) more than the noisy core channel (a)."""
    train = make_slice(11 * 31 + 1, 400, 0.9)
    r = fit_readout(train)
    assert abs(r.w[0] - 2.247) < 2e-2
    assert abs(r.w[1] - 2.661) < 2e-2
    assert abs(r.w[1]) > abs(r.w[0])  # |w_b| > |w_a|: shortcut learned
    assert abs(r.w[2]) < 0.5  # topic slots stay near-useless
    assert abs(r.w[3]) < 0.5


def test_probe_favors_the_spurious_site() -> None:
    """Ch. 11's cautionary instrument: the probe reads the label BETTER at
    the spurious site than at the core site — readout is not causation."""
    heldout = make_slice(11 * 31 + 2, 200, 0.9)
    p1 = probe_accuracy("s1", heldout)
    p2 = probe_accuracy("s2", heldout)
    assert abs(p1 - 0.825) < 2e-2
    assert abs(p2 - 0.915) < 2e-2
    assert p2 > p1


def test_patching_is_trivial_at_the_band_ends() -> None:
    """Ch. 09's first lesson: s0 (the embedding) and s3 (the mixer output)
    restore everything precisely because they sit at the ends of the
    information flow — restoration there localizes nothing."""
    r = run_patch_audit(seed=11)
    for site in ("s0", "s3"):
        assert r.c1[site].rate == 1.000
        assert r.c2[site].rate == 1.000


def test_c1_grid_pinned() -> None:
    """The label-flip contrast grid. Restoring the TRUE channel (s1)
    restores ZERO decisions because the readout leans on b; restoring the
    spurious channel (s2) restores every decision — the vendor's cherry,
    reproduced honestly."""
    r = run_patch_audit(seed=11)
    s1, s2 = r.c1["s1"], r.c1["s2"]
    assert (s1.k, s1.n) == (0, 166)
    assert abs(s1.gap_R - 0.194) < 2e-2  # the logit moves, no decision returns
    assert s1.p_holm > 0.99  # no evidence of restoration at the core site
    assert (s2.k, s2.n) == (166, 166)
    assert abs(s2.rate - 1.000) < 1e-9
    assert abs(s2.gap_R - 0.806) < 2e-2  # gap-form and decision-form differ
    assert s2.p_holm < 1e-40


def test_c2_grid_locality() -> None:
    """The b-isolate contrast: the causal window sits exactly at s2 and
    nowhere else (s1's window is the 3% leak, ~0)."""
    r = run_patch_audit(seed=11)
    s1, s2 = r.c2["s1"], r.c2["s2"]
    assert (s1.k, s1.n) == (0, 200)
    assert abs(s1.gap_R - 0.009) < 5e-3
    assert (s2.k, s2.n) == (200, 200)
    assert abs(s2.gap_R - 0.991) < 2e-2


def test_controls_do_not_restore() -> None:
    """Random-patch and matched-magnitude controls at the informative
    sites: the clean-donor patch at s2 (166/166) beats its random control
    by a mile; at s1 nothing restores anything, clean donor included."""
    r = run_patch_audit(seed=11)
    assert (r.random_controls_c1["s1"].k, r.random_controls_c1["s1"].n) == (0, 166)
    assert r.matched_controls_c1["s1"].k <= 1
    assert (r.random_controls_c1["s2"].k, r.random_controls_c1["s2"].n) == (53, 166)
    assert (r.matched_controls_c1["s2"].k, r.matched_controls_c1["s2"].n) == (20, 166)
    # the s2 clean-donor effect (166/166) is far outside its control band
    assert r.c1["s2"].rate > r.random_controls_c1["s2"].ci[1]


def test_flip_slice_collapse_and_ablation_recovery() -> None:
    """The intervention that settles it: on the deployment-flip slice the
    b-reliant model collapses to 0.335; neutral b-ablation recovers to
    0.770 with disjoint Wilson intervals and an exact McNemar."""
    r = run_patch_audit(seed=11)
    assert abs(r.flip_acc - 0.335) < 2e-2
    assert abs(r.flip_ablated_acc - 0.770) < 2e-2
    assert r.flip_ablated_ci[0] > r.flip_ci[1]  # disjoint: recovery is real
    assert (r.flip_recovery_b, r.flip_recovery_c) == (102, 15)
    assert r.flip_mcnemar_p < 1e-15


def test_heldout_two_sided_ledger() -> None:
    """The ablation price, honestly priced: in-distribution the b channel
    HELPS (0.915 with vs 0.805 without) — the same circuit is a benefit
    in-distribution and a liability under flip. Both sides are pinned."""
    r = run_patch_audit(seed=11)
    assert abs(r.heldout_acc - 0.915) < 2e-2
    assert abs(r.heldout_ablated_acc - 0.805) < 2e-2
    assert r.heldout_acc > r.heldout_ablated_acc


def test_full_audit_deterministic() -> None:
    r1 = run_patch_audit(seed=11)
    r2 = run_patch_audit(seed=11)
    assert r1.readout.w == r2.readout.w
    assert r1.c1["s2"].k == r2.c1["s2"].k
    assert r1.flip_recovery_b == r2.flip_recovery_b
    assert [s.k for s in r1.c2.values()] == [s.k for s in r2.c2.values()]


def test_forward_patch_and_ablate_semantics() -> None:
    """Mechanics: a patch replaces exactly the target site's activations;
    b-ablation neutralizes only the b input channel."""
    x = (1.3, 1.0, 0.4)
    _, base = forward(x)
    _, ablated = forward(x, ablate_b=True)
    assert base.s0[0] == ablated.s0[0]  # a untouched
    assert ablated.s0[1] == 0.0  # b neutralized at the embedding
    assert base.s0[2] == ablated.s0[2]  # topic untouched
    donor = [0.5, -0.5, 0.25, 0.1]
    _, patched = forward(x, patch=("s2", donor))
    assert patched.s2 == donor  # the patch landed
    assert patched.s0 == base.s0  # upstream untouched
    assert patched.s1 == base.s1
