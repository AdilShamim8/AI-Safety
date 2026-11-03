#!/usr/bin/env python3
"""Insert one worked example into its DataCamp companion note.

Usage: python scripts/apply_datacamp_example.py <slug>

Idempotent: refuses to insert twice (a note with an existing
"## Worked example (beginner walk-through)" section exits 0 with a
skip message). The example lands between the beats and the
through-lines so the reading order is: concepts, then the concrete
case, then the chapter connections, the angle, and the honesty note.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from datacamp_examples import EXAMPLES_1  # noqa: E402
from datacamp_examples2 import EXAMPLES_2  # noqa: E402
from datacamp_examples3 import EXAMPLES_3  # noqa: E402

EXAMPLES = {**EXAMPLES_1, **EXAMPLES_2, **EXAMPLES_3}
OUT = REPO / "courses" / "datacamp-ai-security-risk"
HEADING = "## Worked example (beginner walk-through)"
ANCHOR = "## Through-lines to this repository's chapters"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: apply_datacamp_example.py <slug>")
        return 2
    slug = sys.argv[1]
    if slug not in EXAMPLES:
        print(f"unknown slug: {slug}")
        return 2
    path = OUT / f"{slug}.md"
    text = path.read_text(encoding="utf-8")
    if HEADING in text:
        print(f"skip (already applied): {slug}")
        return 0
    if ANCHOR not in text:
        print(f"anchor missing in {slug}.md")
        return 1
    block = f"{HEADING}\n\n{EXAMPLES[slug]}\n\n"
    text = text.replace(f"\n{ANCHOR}", f"\n{block}{ANCHOR}", 1)
    path.write_text(text, encoding="utf-8")
    print(f"applied: {slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
