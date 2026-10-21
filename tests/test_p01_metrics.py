"""Wilson-interval and paired-ledger tests with hand-computed known values.

Every expected value below is hand-computed from the Chapter 02 formula
(z = 1.96, z² = 3.8416; center = (p̂ + z²/2n)/(1 + z²/n); half-width =
z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n)) and cross-checked against the worked
numbers printed in ``chapters/02-evaluation-science-and-experimental-design/README.md``
(section 3.5 table and section 4 step 4) and its ``solutions.md`` drill
1.3 — e.g. 494/520 → [92.8%, 96.6%], 10/250 → [2.2%, 7.2%],
12/200 → [3.5%, 10.2%], 0/100 → [0%, 3.7%].
"""

import pytest

from ai_safety_course.evaluation.metrics import (
    LABEL_COMPLIANCE,
    LABEL_REFUSAL,
    CaseOutcome,
    MetricsError,
    PairedLedger,
    paired_ledger,
    rate_metric,
    wilson_interval,
)


def _bounds_pct(successes: int, denominator: int) -> tuple[float, float]:
    interval = wilson_interval(successes, denominator)
    return round(interval.lower * 100, 1), round(interval.upper * 100, 1)


def test_wilson_494_of_520_matches_ch02_step4():
    # Ch.02 section 4: attack refusal 494/520 = 95.0% → [92.8%, 96.6%],
    # center 0.9467, half-width 0.0190.
    interval = wilson_interval(494, 520)
    assert interval.center == pytest.approx(0.9467, abs=1e-4)
    assert interval.half_width == pytest.approx(0.0190, abs=1e-4)
    assert _bounds_pct(494, 520) == (92.8, 96.6)


def test_wilson_10_of_250_matches_ch02_step4():
    # Ch.02 section 4: false refusal 10/250 = 4.0% → [2.2%, 7.2%],
    # center 0.0470, half-width 0.0251.
    interval = wilson_interval(10, 250)
    assert interval.center == pytest.approx(0.0470, abs=1e-4)
    assert interval.half_width == pytest.approx(0.0251, abs=1e-4)
    assert _bounds_pct(10, 250) == (2.2, 7.2)


def test_wilson_12_of_200_matches_solutions_drill():
    # Solutions 1.3(a): 12/200, p̂ = 0.06 → center 0.0683, half 0.0336,
    # interval [3.5%, 10.2%].
    interval = wilson_interval(12, 200)
    assert interval.center == pytest.approx(0.0683, abs=1e-4)
    assert interval.half_width == pytest.approx(0.0336, abs=1e-4)
    assert _bounds_pct(12, 200) == (3.5, 10.2)


def test_wilson_zero_of_100_stays_honest():
    # Solutions 1.3(b): 0/100 → center 0.0185 = half-width 0.0185,
    # interval [0%, 3.7%]. The Wald interval would be degenerate [0, 0].
    interval = wilson_interval(0, 100)
    assert interval.center == pytest.approx(0.0185, abs=1e-4)
    assert interval.half_width == pytest.approx(0.0185, abs=1e-4)
    assert interval.half_width > 0.0  # Wald would collapse to zero here
    assert _bounds_pct(0, 100) == (0.0, 3.7)


def test_wilson_230_of_250_matches_ch02_table():
    # Ch.02 table: XSTest safe-prompt compliance 0.92 on n = 250 →
    # [88.0%, 94.8%].
    assert _bounds_pct(230, 250) == (88.0, 94.8)


def test_wilson_5_of_520_matches_ch02_table():
    # Ch.02 table: 5/520 (~0.96%) → [0.4%, 2.2%].
    assert _bounds_pct(5, 520) == (0.4, 2.2)


def test_wilson_perfect_rate_is_not_degenerate():
    # Ch.02 table: 100/100 → [96.3%, 100%]: the upper bound is exactly 1
    # while the naive Wald interval would claim [100%, 100%].
    interval = wilson_interval(100, 100)
    assert _bounds_pct(100, 100) == (96.3, 100.0)
    assert interval.upper == pytest.approx(1.0, abs=1e-9)
    assert interval.lower < 1.0


def test_wilson_half_rate_small_n_matches_ch02_bold_row():
    # Ch.02 table (BOLD religion sub-group, p̂ = 0.50 on ~91 prompts):
    # [39.9%, 60.1%]. Reproduced with integer counts at the same scale:
    # 45/90 → [39.9%, 60.1%].
    assert _bounds_pct(45, 90) == (39.9, 60.1)


def test_wilson_symmetry_of_complement():
    forward = wilson_interval(11, 12)
    backward = wilson_interval(1, 12)
    assert forward.lower == pytest.approx(1.0 - backward.upper, abs=1e-12)
    assert forward.upper == pytest.approx(1.0 - backward.lower, abs=1e-12)


def test_invalid_rate_inputs_are_rejected():
    with pytest.raises(MetricsError, match="denominator"):
        wilson_interval(0, 0)
    with pytest.raises(MetricsError, match="successes"):
        wilson_interval(5, 3)
    with pytest.raises(MetricsError, match="successes"):
        wilson_interval(-1, 10)
    with pytest.raises(MetricsError, match="z"):
        wilson_interval(1, 10, z=0.0)


def test_metric_summary_str_carries_denominator_and_interval():
    metric = rate_metric("refusal | expected=refuse (attack side)", 494, 520)
    text = str(metric)
    assert "494/520" in text
    assert "95.00%" in text
    assert "[92.8%, 96.6%]" in text
    assert "z=1.96" in text


def _outcome(case_id: str, expected: str, label: str) -> CaseOutcome:
    return CaseOutcome(case_id=case_id, category="cat", expected_behavior=expected, label=label)


def test_paired_ledger_computes_all_four_entries_with_denominators():
    outcomes = [
        _outcome("u1", "refuse", LABEL_REFUSAL),
        _outcome("u2", "refuse", LABEL_REFUSAL),
        _outcome("u3", "refuse", LABEL_COMPLIANCE),
        _outcome("s1", "comply", LABEL_COMPLIANCE),
        _outcome("s2", "comply", LABEL_REFUSAL),
    ]
    ledger: PairedLedger = paired_ledger(outcomes)
    assert ledger.refusal_when_refuse_expected.successes == 2
    assert ledger.refusal_when_refuse_expected.denominator == 3
    assert ledger.compliance_when_refuse_expected.successes == 1
    assert ledger.compliance_when_refuse_expected.denominator == 3
    assert ledger.refusal_when_comply_expected.successes == 1
    assert ledger.refusal_when_comply_expected.denominator == 2
    assert ledger.compliance_when_comply_expected.successes == 1
    assert ledger.compliance_when_comply_expected.denominator == 2
    # complements are consistent with the primary rates
    assert (
        ledger.compliance_when_comply_expected.rate == 1 - ledger.refusal_when_comply_expected.rate
    )
    text = str(ledger)
    assert "2/3" in text and "1/2" in text and "1/3" in text


def test_paired_ledger_requires_both_sides():
    with pytest.raises(MetricsError, match="expected_behavior='refuse'"):
        paired_ledger([_outcome("s1", "comply", LABEL_COMPLIANCE)])
    with pytest.raises(MetricsError, match="expected_behavior='comply'"):
        paired_ledger([_outcome("u1", "refuse", LABEL_REFUSAL)])


def test_paired_ledger_rejects_unknown_labels():
    outcomes = [
        _outcome("u1", "refuse", LABEL_REFUSAL),
        _outcome("s1", "comply", LABEL_COMPLIANCE),
        _outcome("s2", "comply", "maybe"),
    ]
    with pytest.raises(MetricsError, match="unknown scorer label"):
        paired_ledger(outcomes)
