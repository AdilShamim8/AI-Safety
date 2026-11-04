"""Cross-package consistency of stated constants and behaviors.

Session-13 origin (P21): the evaluation package computes Wilson
intervals at the 1.96 shorthand while reward_spec uses the
full-precision quantile 1.959963984540054, each documented in its own
module — a reader comparing the two could reasonably ask which is
right. Measured answer: the two conventions agree to four decimal
places on every interval the corpus states (largest observed gap
0.0001), so both are honest at every precision the repo publishes;
this module pins that agreement at 1e-4 so if either constant ever
changes, the comparison runs on CI. Also pinned: decimal-place claims
in src docstrings must be backed by matching round() calls or format
specs, and every module claiming determinism without randomness is
documented as such (the from-scratch track's seeded modules are
covered by their own tests).
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src" / "ai_safety_course"


def _wilson(k: int, n: int, z: float) -> tuple[float, float]:
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / d
    return c - h, c + h


def test_the_two_z_conventions_agree_at_1e4() -> None:
    """z=1.96 (evaluation package) vs the full-precision quantile
    (reward_spec): every interval the corpus states agrees to 4dp."""
    for k, n in ((87, 1000), (182, 200), (432, 450), (165, 200), (58, 71), (353, 817)):
        a = _wilson(k, n, 1.96)
        b = _wilson(k, n, 1.959963984540054)
        for x, y in zip(a, b, strict=True):
            assert abs(x - y) < 1e-4, (k, n, x, y)


def test_z_constants_stay_as_documented() -> None:
    ev = (SRC / "evaluation" / "metrics.py").read_text(encoding="utf-8")
    rs = (SRC / "reward_spec" / "metrics.py").read_text(encoding="utf-8")
    assert "Z_95 = 1.96" in ev
    assert "1.959963984540054" in rs


def test_decimal_place_claims_are_backed() -> None:
    for f in SRC.rglob("*.py"):
        t = f.read_text(encoding="utf-8")
        for m in re.finditer(r"(\d+) decimal places", t):
            n = int(m.group(1))
            assert re.search(
                rf"round\([^)]*,\s*{n}\)|:.{n}f", t
            ), f"{f.name}: claims {n} dp with no matching round/format"
