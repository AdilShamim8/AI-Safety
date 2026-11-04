"""Source-register deep checks: supports-path closure and url mirrors.

Session-13 origin (P08): the supports field carried five grammar
shorthand forms nobody validated — 'chapters/NN' (dir prefix),
'chapters/NN and MM' (two chapters), 'chapters/NN-.../README.md'
(ellipsis), 'datasets/catalog.yaml DS-NNN' (catalog id), and compound
'X and Y' pairs — plus a '(planned)' tag that exempts artifacts not
built yet. 280 raw strings resolve to 300 concrete paths; every one
must exist on disk. The eleven duplicate urls are intentional mirrors
(one row per support-surface: chapters vs notes for the same paper,
card+license for the same repository) and are allowed exactly when
the two entries' supports differ — identical supports would be the
real-duplicate class.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SRC = yaml.safe_load((REPO / "research" / "source-register.yaml").read_bytes())["sources"]
CHDIRS = {d.name.split("-")[0]: d.name for d in (REPO / "chapters").glob("[0-9][0-9]-*")}


def _resolve(raw: str) -> list[tuple[str, bool]]:
    planned = "(planned)" in raw
    s = raw.split(" (")[0].strip()
    parts = [s]
    if " and " in s and "/" in s:
        segs = s.split(" and ")
        if all("/" in seg for seg in segs):
            parts = segs
    out: list[tuple[str, bool]] = []
    for part in parts:
        part = part.strip()
        m = re.fullmatch(r"chapters/(\d\d) and (\d\d)", part)
        if m:
            out += [
                ("chapters/" + CHDIRS[m.group(1)], planned),
                ("chapters/" + CHDIRS[m.group(2)], planned),
            ]
            continue
        m = re.fullmatch(r"datasets/catalog\.yaml (DS-\d+)", part)
        if m:
            out.append(("datasets/catalog.yaml", planned))
            continue
        m = re.fullmatch(r"chapters/(\d\d)-\.\.\./README\.md", part)
        if m:
            out.append((f"chapters/{CHDIRS[m.group(1)]}/README.md", planned))
            continue
        if re.fullmatch(r"chapters/\d\d", part):
            out.append(("chapters/" + CHDIRS[part.split("/")[1]], planned))
            continue
        out.append((part, planned))
    return out


def test_every_supports_path_exists() -> None:
    checked = 0
    for src in SRC:
        for sup in src.get("supports") or []:
            for path, planned in _resolve(str(sup)):
                if path.startswith(("chapters/", "research/", "datasets/", "courses/")):
                    if planned:
                        continue
                    checked += 1
                    assert (
                        REPO / path
                    ).exists(), f"{src['id']}: supports path {path!r} not on disk"
    assert checked >= 290, f"closure sweep unexpectedly small: {checked}"


def test_duplicate_urls_are_intentional_mirrors() -> None:
    by_url: dict[str, list[dict]] = defaultdict(list)
    for s in SRC:
        by_url[s["url"]].append(s)
    for url, group in by_url.items():
        if len(group) < 2:
            continue
        supports = [str(g.get("supports")) for g in group]
        assert len(set(supports)) == len(supports), (
            f"{url}: {len(group)} entries with identical supports — a real duplicate, "
            f"not a mirror: {[g['id'] for g in group]}"
        )


def test_urls_are_http_and_ids_unique() -> None:
    ids = [s["id"] for s in SRC]
    assert len(ids) == len(set(ids))
    for s in SRC:
        assert s["url"].startswith("http"), f"{s['id']}: {s['url']!r}"


def test_access_level_taxonomy() -> None:
    allowed = {"abstract-read", "page-inspected", "full-text-read", "metadata-only"}
    for s in SRC:
        assert (
            s.get("access_level") in allowed
        ), f"{s['id']}: access_level {s.get('access_level')!r}"
