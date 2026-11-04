"""Planning-layer integrity: STATUS unit table and content-matrix
values, recomputed from disk and git.

Session-13 origin (P17): the STATUS unit table (68 rows) had never
been verified against git, and the content-matrix notes section still
described the 2026-10-22 era — paper_notes 20/20 while the disk holds
74, comparison_notes_complete 2 while all twelve exist, dataset cards
13 while the catalog now holds 47. The matrix drives planning
decisions, so its numbers are resynced (history preserved in comments)
and pinned here. Also pinned: every STATUS row's commit exists, every
row marked pushed is on origin/main, and every chapter row's
project_ids and source_ids resolve against the registers.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
STATUS = (REPO / "planning" / "STATUS.md").read_text(encoding="utf-8")
MATRIX = yaml.safe_load((REPO / "planning" / "content-matrix.yaml").read_bytes())
SRC_IDS = {
    s["id"]
    for s in yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())["sources"]
}


def test_status_rows_reference_real_commits() -> None:
    rows = re.findall(
        r"^\| (S\d+-P\d+[^|]*)\| ([0-9a-f]{7,10})[^(]*\((\w+)\)[^|]*\| (.+?)\|$", STATUS, re.M
    )
    assert len(rows) >= 68, len(rows)
    for unit, sha, state, _files in rows:
        out = subprocess.run(
            ["git", "cat-file", "-t", sha], capture_output=True, text=True, cwd=REPO
        )
        assert out.stdout.strip() == "commit", f"{unit}: {sha} not a commit"
        if state == "pushed":
            r = subprocess.run(
                ["git", "branch", "-r", "--contains", sha], capture_output=True, text=True, cwd=REPO
            )
            assert "origin/main" in r.stdout, f"{unit}: {sha} marked pushed but not on origin/main"


def test_matrix_notes_values_match_disk() -> None:
    notes = MATRIX["notes"]
    papers = len([p for p in (REPO / "research" / "notes").glob("*.md") if re.match(r"\d", p.name)])
    comps = len(list((REPO / "research" / "notes").glob("comparison-*.md")))
    cards = len(list((REPO / "datasets" / "cards").glob("*.md")))
    assert notes["paper_notes_complete"] == papers, notes["paper_notes_complete"]
    assert notes["paper_notes_required"] == papers
    assert notes["comparison_notes_complete"] == comps, notes["comparison_notes_complete"]
    assert str(cards) in notes["dataset_catalog"], f"dataset_catalog count {cards} not stated"


def test_matrix_chapter_refs_resolve() -> None:
    for c in MATRIX["chapters"]:
        assert (REPO / str(c["path"]).rstrip("/")).exists(), f"ch{c['id']}: {c['path']}"
        for pid in c.get("project_ids") or []:
            assert re.fullmatch(r"P\d\d", pid), f"ch{c['id']}: {pid!r}"
        for sid in c.get("source_ids") or []:
            assert sid in SRC_IDS, f"ch{c['id']}: source {sid} not in register"


def test_matrix_project_paths_exist() -> None:
    for p in MATRIX.get("projects") or []:
        assert (
            REPO / str(p.get("path", "")).rstrip("/")
        ).exists(), f"{p.get('id')}: {p.get('path')}"
