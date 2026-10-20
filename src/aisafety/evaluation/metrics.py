"""Aggregation metrics for evaluation harnesses.

Design rule (from docs/risks/specification_gaming.md): never collapse a
safety evaluation into one number. Harnesses emit per-item booleans or
scores; this module summarizes them with explicit numerators,
denominators, and confidence intervals — Goodhart-resistant reporting.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class MetricSummary:
    name: str
    value: float
    numerator: int
    denominator: int

    @property
    def wilson95(self) -> tuple[float, float]:
        """Wilson score interval (95%) — appropriate for small n, unlike Wald."""
        return wilson_interval(self.value, self.denominator)

    def __str__(self) -> str:  # pragma: no cover - display helper
        lo, hi = self.wilson95
        return f"{self.name}={self.value:.4f} ({self.numerator}/{self.denominator}) [{lo:.3f}, {hi:.3f}]"


def safe_rate(name: str, numerator: int, denominator: int) -> MetricSummary:
    """Rate metric with explicit denominator; 0 when denominator is 0."""
    if denominator < 0:
        raise ValueError("denominator must be non-negative")
    value = (numerator / denominator) if denominator else 0.0
    return MetricSummary(name=name, value=value, numerator=numerator,
                         denominator=denominator)


def wilson_interval(p: float, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval bounds for a binomial proportion."""
    if n <= 0:
        return (0.0, 0.0)
    denom = 1 + z * z / n
    center = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (center - margin) / denom), min(1.0, (center + margin) / denom))


def mean_std(values: Sequence[float]) -> tuple[float, float]:
    """Mean and population standard deviation (0.0 for n <= 1)."""
    n = len(values)
    if n <= 0:
        raise ValueError("values must be non-empty")
    mean = sum(values) / n
    if n == 1:
        return mean, 0.0
    var = sum((v - mean) ** 2 for v in values) / n
    return mean, math.sqrt(var)


def summarize(name: str, flags: Iterable[bool]) -> MetricSummary:
    """Summarize an iterable of boolean outcomes as a rate."""
    bits = [1 if flag else 0 for flag in flags]
    return safe_rate(name, sum(bits), len(bits))


def parity_gap(name_a: str, rate_a: float, name_b: str, rate_b: float) -> float:
    """Difference between two rates, reported in the order given.

    Used for over-/under-refusal style comparisons (e.g., refusal-on-safe
    minus refusal-on-unsafe from XSTest — see benchmarks/xstest.py).
    """
    return rate_a - rate_b
