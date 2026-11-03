#!/usr/bin/env python3
"""Insert one worked example into its CampusX companion note.

Usage: python scripts/apply_campusx_example.py <slug>

Idempotent: refuses to insert twice (a note with an existing
"## Worked example (practitioner walk-through)" section exits 0 with
a skip message). The example lands between the beats and the
through-lines.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from campusx_examples import EXAMPLES_12  # noqa: E402
from campusx_examples3 import EXAMPLES_3  # noqa: E402
from campusx_examples4 import EXAMPLES_4  # noqa: E402

EXAMPLES = {**EXAMPLES_12, **EXAMPLES_3, **EXAMPLES_4}
OUT = REPO / "courses" / "campusx-ai-security-guardrails"
HEADING = "## Worked example (practitioner walk-through)"
ANCHOR = "## Through-lines to this repository's chapters"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: apply_campusx_example.py <slug>")
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
