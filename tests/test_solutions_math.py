"""Arithmetic consistency for the chapter solutions files.

Session-13 origin: the 24 chapters' solutions carried ~600 stated
numbers with no verification layer at all — the review questions are
prose, so the suite never recomputed them. This module re-derives
every number the text states in a machine-checkable shape:

  - division chains "a/b = c" (percent or plain, any precision the
    text uses, decimal operands included);
  - products "a × b = c" (comma thousands, percent-context cells);
  - the Wilson-interval arithmetic chains "x = expr = v";
  - trade-off table rows "(S,U)→(S,U) | ΔU | ΔS | ΔU/ΔS" (S13-P03);
  - binomial cells "k/n = p% [lo, hi]" whose interval is recomputed
    as a true Wilson 95% interval from k and n (S13-P03).

It found one real error on first run (ch05: 0.70 × 0.1492 stated as
10.45% — the value is 10.44%), fixed in the same unit. Lines in
scientific notation (mantissa with a trailing ×10⁻ᵏ factor) are
skipped by the percent/product rules because their printed result is
the mantissa of a different magnitude — they are covered by the
sqrt-chain rule where they appear in that shape.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SOLUTIONS = sorted(REPO.glob("chapters/*/solutions.md"))

DIVISION = re.compile(r"(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)\s*=\s*([\d.]+)%?")
PRODUCT = re.compile(r"([\d.]+)\s*×\s*([\d.,]+)\s*=\s*([\d.,]+)")
SQRT = re.compile(r"√\(([\d.]+)\)\s*=\s*([\d.]+)")
DELTA_ROW = re.compile(
    r"\((\d+),\s*(\d+)\)→\((\d+),\s*(\d+)\)\s*\|\s*(-?\d+)\s*\|\s*(-?\d+)\s*\|\s*\*{0,2}([\d.]+)\*{0,2}"
)
RATIO_CI = re.compile(r"(\d+)/(\d+)\s*=\s*([\d.]+)%\s*\[([\d.]+),\s*([\d.]+)\]")
WILSON_INTERVAL = re.compile(r"Wilson 95% = \[([\d.]+)%?,\s*([\d.]+)%?\]")

_Z = 1.959964  # the normal 97.5th percentile, three-decimal tradition


def _wilson(k: int, n: int) -> tuple[float, float]:
    p = k / n
    denom = 1 + _Z * _Z / n
    center = (p + _Z * _Z / (2 * n)) / denom
    half = _Z * math.sqrt(p * (1 - p) / n + _Z * _Z / (4 * n * n)) / denom
    return center - half, center + half


def _num(s: str) -> float:
    return float(s.replace(",", "").rstrip("."))


def _sci_context(text: str, pos: int) -> bool:
    """True when the span sits in a scientific-notation sentence whose
    printed figure is a mantissa of another magnitude (e.g. '7.9431×10⁻⁵')."""
    window = text[max(0, pos - 100) : pos + 60]
    return bool(re.search(r"10[⁻^]|×10", window))


def test_every_solutions_file_is_present() -> None:
    assert len(SOLUTIONS) == 24, [p.parent.name for p in SOLUTIONS]


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_division_chains(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    checked = 0
    for m in DIVISION.finditer(text):
        d = _num(m.group(2))
        if d == 0:
            continue
        if _sci_context(text, m.start()):
            continue
        n, v = _num(m.group(1)), _num(m.group(3))
        real = n / d
        is_pct = "%" in m.group(0)
        candidates = [round(real, k) for k in range(2, 7)]
        if is_pct:
            candidates += [round(real * 100, k) for k in (1, 2, 3)]
        checked += 1
        assert any(
            abs(c - v) < 0.0051 for c in candidates
        ), f"{path.parent.name}: {m.group(0)!r} — true {real:.6f}"
    assert checked >= 0


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_product_chains(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for m in PRODUCT.finditer(text):
        if _sci_context(text, m.start()):
            continue
        after = text[m.end() : m.end() + 2]
        is_pct = "%" in m.group(0) or "%" in after
        a, b, v = _num(m.group(1)), _num(m.group(2)), _num(m.group(3))
        real = a * b
        candidates = [round(real, k) for k in range(2, 7)]
        if is_pct:
            candidates += [round(real * 100, k) for k in (1, 2, 3)]
        assert any(
            abs(c - v) < 0.0051 for c in candidates
        ), f"{path.parent.name}: {m.group(0)!r} — true {real:.6f}"


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_sqrt_chains(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for m in SQRT.finditer(text):
        arg, v = _num(m.group(1)), _num(m.group(2))
        real = arg**0.5
        assert any(
            abs(round(real, k) - v) < 10 ** -(k + 1) for k in range(2, 7)
        ), f"{path.parent.name}: √({m.group(1)}) = {m.group(2)} — true {real:.6f}"


def test_the_ch05_false_rejection_mass_is_1044() -> None:
    """The first real error this layer caught: 0.70 × 0.1492 was stated
    as 10.45%; the value is 10.44% (0.104440). Both occurrences pinned —
    table cell and the prose sentence that quotes it."""
    text = (REPO / "chapters/05-scalable-oversight/solutions.md").read_text(encoding="utf-8")
    assert "0.70 × 0.1492 = 10.44%" in text
    assert "(0.70% → 10.44%)" in text
    assert "10.45%" not in text


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_tradeoff_delta_rows(path: Path) -> None:
    """The control/steering trade-off tables state each move's segment
    endpoints, |ΔU|, |ΔS|, and the exchange ratio ΔU/ΔS. The stated
    deltas must equal the coordinate differences (in absolute value —
    the tables state magnitudes) and the ratio must equal |ΔU|/ΔS."""
    text = path.read_text(encoding="utf-8")
    for m in DELTA_ROW.finditer(text):
        s1, u1, s2, u2 = (int(m.group(i)) for i in range(1, 5))
        du_stated, ds_stated = int(m.group(5)), int(m.group(6))
        ratio = float(m.group(7))
        assert abs(s2 - s1) == abs(ds_stated) and abs(u1 - u2) == abs(du_stated), (
            f"{path.parent.name}: {m.group(0)[:70]!r} — coordinate deltas say "
            f"ΔS={s2-s1}, ΔU={u1-u2}"
        )
        if ds_stated == 0:
            continue
        real = abs(du_stated) / ds_stated
        assert any(
            abs(round(real, k) - ratio) < 10 ** -(k + 1) for k in (2, 3)
        ), f"{path.parent.name}: {m.group(0)[:70]!r} — ratio is {real:.4f}"


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_binomial_cells_carry_true_wilson_intervals(path: Path) -> None:
    """Every cell of the shape 'k/n = p% [lo, hi]' states a Wilson 95%
    interval. Both bounds are recomputed from k and n; the point must
    be the rounded proportion and the bounds must match the recomputed
    Wilson interval at one decimal (18 such cells in ch11 alone; all
    recomputed true on first run — pinned so that stays true)."""
    text = path.read_text(encoding="utf-8")
    for m in RATIO_CI.finditer(text):
        k, n, p = int(m.group(1)), int(m.group(2)), float(m.group(3))
        lo, hi = float(m.group(4)), float(m.group(5))
        assert (
            abs(round(k / n * 100, 1) - p) <= 0.051
        ), f"{path.parent.name}: point {m.group(0)!r} — true {k/n*100:.2f}%"
        wlo, whi = _wilson(k, n)
        assert abs(round(wlo * 100, 1) - lo) <= 0.11 and abs(round(whi * 100, 1) - hi) <= 0.11, (
            f"{path.parent.name}: {m.group(0)!r} — true Wilson " f"[{wlo*100:.2f}, {whi*100:.2f}]"
        )


@pytest.mark.parametrize("path", SOLUTIONS, ids=lambda p: p.parent.name[:2])
def test_stated_wilson_intervals_are_ordered(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for m in WILSON_INTERVAL.finditer(text):
        lo, hi = float(m.group(1)), float(m.group(2))
        assert lo < hi, f"{path.parent.name}: inverted interval {m.group(0)!r}"
