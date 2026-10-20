"""Tests for evaluation metrics (Wilson intervals, rates, parity)."""

from __future__ import annotations

import pytest

from src.aisafety.evaluation.metrics import (
    MetricSummary,
    mean_std,
    parity_gap,
    safe_rate,
    summarize,
    wilson_interval,
)


class TestSafeRate:
    def test_basic(self):
        m = safe_rate("r", 3, 4)
        assert m.value == 0.75
        assert (m.numerator, m.denominator) == (3, 4)

    def test_zero_denominator(self):
        m = safe_rate("r", 0, 0)
        assert m.value == 0.0

    def test_negative_denominator_rejected(self):
        with pytest.raises(ValueError):
            safe_rate("r", 1, -1)


class TestWilsonInterval:
    def test_degenerate(self):
        assert wilson_interval(0.5, 0) == (0.0, 0.0)

    def test_bounds_contain_point(self):
        p, n = 0.4, 50
        lo, hi = wilson_interval(p, n)
        assert lo <= p <= hi

    def test_extremes(self):
        lo, hi = wilson_interval(1.0, 10)
        assert hi == 1.0 and lo > 0.5
        lo, hi = wilson_interval(0.0, 10)
        assert lo == 0.0 and hi < 0.5

    def test_summary_carries_interval(self):
        m = MetricSummary("x", 0.5, 10)
        lo, hi = m.wilson95
        assert lo < 0.5 < hi


class TestMeanStd:
    def test_basic(self):
        mean, std = mean_std([2.0, 4.0])
        assert mean == 3.0
        assert std == 1.0

    def test_single_value(self):
        mean, std = mean_std([7.5])
        assert (mean, std) == (7.5, 0.0)

    def test_empty_rejected(self):
        with pytest.raises(ValueError):
            mean_std([])


class TestSummarize:
    def test_bools(self):
        m = summarize("t", [True, True, False])
        assert m.numerator == 2
        assert m.denominator == 3
        assert m.value == pytest.approx(2 / 3)

    def test_empty(self):
        assert summarize("t", []).denominator == 0


class TestParityGap:
    def test_order_preserved(self):
        assert parity_gap("a", 0.8, "b", 0.3) == pytest.approx(0.5)
        assert parity_gap("a", 0.3, "b", 0.8) == pytest.approx(-0.5)
