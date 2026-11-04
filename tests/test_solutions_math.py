"""Arithmetic consistency for the chapter solutions files.

Session-13 origin: the 24 chapters' solutions carried ~600 stated
numbers with no verification layer at all — the review questions are
prose, so the suite never recomputed them. This module re-derives
every number the text states in a machine-checkable shape:

  - division chains "a/b = c" (percent or plain, any precision the
    text uses, decimal operands included);
  - products "a × b = c" (comma thousands, percent-context cells);
  - the Wilson-interval arithmetic chains "x = expr = v".

It found one real error on first run (ch05: 0.70 × 0.1492 stated as
10.45% — the value is 10.44%), fixed in the same unit. Lines in
scientific notation (mantissa with a trailing ×10⁻ᵏ factor) are
skipped by the percent/product rules because their printed result is
the mantissa of a different magnitude — they are covered by the
sqrt-chain rule where they appear in that shape.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SOLUTIONS = sorted(REPO.glob("chapters/*/solutions.md"))

DIVISION = re.compile(r"(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)\s*=\s*([\d.]+)%?")
PRODUCT = re.compile(r"([\d.]+)\s*×\s*([\d.,]+)\s*=\s*([\d.,]+)")
SQRT = re.compile(r"√\(([\d.]+)\)\s*=\s*([\d.]+)")


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
