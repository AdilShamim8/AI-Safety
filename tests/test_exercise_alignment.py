"""Exercises-to-solutions alignment across all 24 chapters.

Session-13 origin (P09): the pairing was never machine-checked, and
the numbering is non-uniform by design — early chapters answer with
'## Solution N.N', later ones with '## Exercise N.N', chapter 06
splits Exercise 6.1 into three lettered sub-solutions 6.1(a)(b)(c),
and chapters 09/10/11 open with a '.0' prelude section that sets up
notation before answering anything. This module normalizes all four
forms and requires: every stated exercise has a solution header, no
orphan solutions exist (the .0 preludes are the only allowed extras),
and a repeated solution number is legal only as the (a)(b)(c) triple.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAPTERS = sorted((REPO / "chapters").glob("[0-9][0-9]-*"))


def _pair(d: Path) -> tuple[list[str], list[tuple[str, str]]]:
    readme = (d / "README.md").read_text(encoding="utf-8")
    sol = (d / "solutions.md").read_text(encoding="utf-8")
    exercises = re.findall(r"\*\*Exercise (\d+\.\d+)", readme)
    solutions = re.findall(r"^## (?:Solution|Exercise) (\d+\.\d+)(\(?[a-c]\)?)?", sol, re.M)
    return exercises, solutions


def test_twenty_four_chapters_present() -> None:
    assert len(CHAPTERS) == 24


def test_every_exercise_has_a_solution() -> None:
    total = 0
    for d in CHAPTERS:
        exercises, solutions = _pair(d)
        total += len(exercises)
        sol_nums = [s[0] for s in solutions]
        # a repeated number is legal only as the lettered (a)(b)(c) triple
        for num, count in Counter(sol_nums).items():
            if count > 1:
                letters = [s[1] for s in solutions if s[0] == num]
                assert sorted(letters) == ["(a)", "(b)", "(c)"], (
                    f"{d.name[:2]}: solution {num} repeated {count}x without "
                    f"(a)(b)(c) structure: {letters}"
                )
                sol_nums = [n for n in sol_nums if n != num] + [num]
        missing = set(exercises) - set(sol_nums)
        assert not missing, f"{d.name[:2]}: exercises without solutions: {sorted(missing)}"
    assert total == 72, total


def test_no_orphan_solutions() -> None:
    for d in CHAPTERS:
        exercises, solutions = _pair(d)
        extras = set(s[0] for s in solutions) - set(exercises)
        non_prelude = [p for p in extras if not p.endswith(".0")]
        assert not non_prelude, f"{d.name[:2]}: solutions answering nothing: {sorted(non_prelude)}"


def test_exercise_numbers_match_chapter_prefix() -> None:
    for d in CHAPTERS:
        prefix = d.name.split("-")[0]
        exercises, _ = _pair(d)
        for num in exercises:
            assert int(num.split(".")[0]) == int(
                prefix
            ), f"{d.name[:2]}: {num} not chapter-prefixed"
