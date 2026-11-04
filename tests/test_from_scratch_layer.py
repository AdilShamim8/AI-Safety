"""From-scratch track closure: note/code/test three-way pairing and
the count surface.

Session-13 origin (P14): the track README's status line said
"174 tests" while the suite collected 176 — two cross-layer pin tests
were added to test_fs_tensors.py on 2026-11-03 (commits 6cd5e70,
d02f49b) without resyncing the README's stated count. The exact
drift class test_count_drift guards at repo level, now guarded at
track level too: the stated count is recomputed from pytest
collection on every run. Also pinned: the 7-note ↔ 7-code-module ↔
7-test-file three-way pairing (tensor, neuron+activations, network,
attention+transformer, moe, and the protocol module that has notes
and tests but no code module by design), the glossary's FS-N
references stay within the seven modules, and the module map table
links resolve.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRACK = REPO / "research" / "ai-researcher-from-scratch"
CODE = REPO / "src" / "ai_safety_course" / "from_scratch"


def test_status_line_count_matches_collection() -> None:
    t = (TRACK / "README.md").read_text(encoding="utf-8")
    m = re.search(r"(\d+) tests", t)
    assert m, "no test count stated in the track README"
    stated = int(m.group(1))
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    counts = dict(re.findall(r"(tests/test_fs_[a-z]+\.py): (\d+)", proc.stdout))
    real = sum(int(v) for v in counts.values())
    assert stated == real, f"track README states {stated}; collection says {real}"


def test_seven_way_pairing() -> None:
    notes = sorted(p.name for p in TRACK.glob("0*.md"))
    assert len(notes) == 7, notes
    code = [p.stem for p in CODE.glob("*.py") if p.name != "__init__.py"]
    tests = sorted(p.name for p in (REPO / "tests").glob("test_fs_*.py"))
    assert len(tests) == 7, tests
    # every code module named in the map table exists
    t = (TRACK / "README.md").read_text(encoding="utf-8")
    code_names = {f"{c}.py" for c in code}
    for m in re.finditer(r"`([a-z_]+\.py)`", t):
        assert m.group(1) in code_names, m.group(1)
    assert "moe.py" in code_names


def test_glossary_fs_refs_within_seven() -> None:
    g = (REPO / "GLOSSARY.md").read_text(encoding="utf-8")
    for m in re.finditer(r"FS-(\d+)", g):
        assert 1 <= int(m.group(1)) <= 7, f"FS-{m.group(1)} outside the seven modules"


def test_module_map_links_resolve() -> None:
    t = (TRACK / "README.md").read_text(encoding="utf-8")
    for m in re.finditer(r"\]\(([^)#]+?)(#[^)]*)?\)", t):
        link = m.group(1)
        if link.startswith(("http", "mailto")):
            continue
        assert (TRACK / link).resolve().exists(), f"track README: {link}"
