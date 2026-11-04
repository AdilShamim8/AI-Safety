"""Projects-layer count surface: status-line and quickstart numbers
recomputed from collection.

Session-13 origin (P15): the ten project READMEs carry three count
styles — per-file inline claims ("8 tests, pinned numbers"), status-
line family totals (p02 "157 tests green", p03 "98 tests green"), and
p01's user-facing quickstart ("78 tests (7 repo + 71 P01)"). The
inline claims were all true; the family totals had drifted (p02 157 →
150, p03 98 → 87) because later sessions edited shared tests without
resyncing the status lines they were written into, and p01's
quickstart described the suite as it stood at write time (78 = 7 repo
+ 71 P01) while `uv run pytest` now collects 873. This module
recomputes every claim from collection on each run: per-file claims
must equal that file's collected count, family totals must equal the
family sum, and p01's quickstart must equal the current total with the
repo-side split stated as the remainder.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _counts() -> dict[str, int]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    return {k: int(v) for k, v in re.findall(r"(tests/test_[a-z0-9_]+\.py): (\d+)", proc.stdout)}


INLINE_CLAIMS = {
    "projects/p06-causal-interpretability-study/README.md": (
        r"test_patch_audit\.py`\s*\((\d+) tests",
        "tests/test_patch_audit.py",
    ),
    "projects/p04-preference-optimization-audit/README.md": (
        r"test_pref_audit\.py`\s*\((\d+) tests",
        "tests/test_pref_audit.py",
    ),
    "projects/p05-weak-to-strong-or-scalable-oversight-analogue/README.md": (
        r"test_w2s_audit\.py`\s*\((\d+) tests",
        "tests/test_w2s_audit.py",
    ),
    "projects/p08-control-and-monitoring-protocol/README.md": (
        r"test_control_protocol\.py`\s*\((\d+) tests",
        "tests/test_control_protocol.py",
    ),
    "projects/p09-shift-subgroup-reliability/README.md": (
        r"test_shift_audit\.py`\s*\((\d+) tests",
        "tests/test_shift_audit.py",
    ),
    "projects/p10-capstone-agent-evaluation-and-assurance-dossier/README.md": (
        r"test_assurance\.py`\s*\((\d+) tests",
        "tests/test_assurance.py",
    ),
}


def test_inline_per_file_claims() -> None:
    counts = _counts()
    for readme, (pat, testfile) in INLINE_CLAIMS.items():
        t = (REPO / readme).read_text(encoding="utf-8")
        m = re.search(pat, t)
        assert m, f"{readme}: claim pattern {pat!r} not found"
        assert (
            int(m.group(1)) == counts[testfile]
        ), f"{readme}: states {m.group(1)}, collection says {counts[testfile]} for {testfile}"


def test_family_status_lines() -> None:
    counts = _counts()
    p02 = sum(v for k, v in counts.items() if k.startswith("tests/test_p02_"))
    p03 = sum(v for k, v in counts.items() if k.startswith("tests/test_p03_"))
    t2 = (REPO / "projects/p02-reward-misspecification-and-generalization/README.md").read_text(
        encoding="utf-8"
    )
    assert f"code + {p02} tests green" in t2, f"p02 status line should state {p02}"
    t3 = (REPO / "projects/p03-calibration-truthfulness-and-abstention/README.md").read_text(
        encoding="utf-8"
    )
    assert f"code + {p03} tests green" in t3, f"p03 status line should state {p03}"


def test_p01_quickstart_formula() -> None:
    counts = _counts()
    total = sum(counts.values())
    p01 = sum(v for k, v in counts.items() if k.startswith("tests/test_p01_"))
    t = (REPO / "projects/p01-evaluation-harness/README.md").read_text(encoding="utf-8")
    m = re.search(r"# (\d+) tests \((\d+) repo \+ (\d+) P01\)", t)
    assert m, "p01 quickstart formula line not found"
    assert int(m.group(1)) == total, f"quickstart total {m.group(1)} != {total}"
    assert int(m.group(2)) == total - p01, f"repo side {m.group(2)} != {total - p01}"
    assert int(m.group(3)) == p01
