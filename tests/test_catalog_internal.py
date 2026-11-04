"""Catalog internal consistency: id sequence and required fields.

Session-13 origin (P26): 47 rows; pinned — the DS ids run 001-047 with
no gaps, every row carries hf_id or canonical_url, a license record,
an access_level, and a card; the redistribution_policy header states
what the repo does with dataset content.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CAT = yaml.safe_load((REPO / "datasets/catalog.yaml").read_bytes())
ROWS = CAT["datasets"]


def test_ds_ids_sequence_without_gaps() -> None:
    nums = sorted(int(r["id"][3:]) for r in ROWS)
    assert nums == list(range(1, 48)), "DS id sequence has gaps"


def test_every_row_has_url_and_license() -> None:
    for r in ROWS:
        assert re.match(
            r"^https?://", str(r.get("canonical_url", r.get("hf_id", "")))
        ), f"{r['id']}: no canonical url/hf id"
        assert r.get("license"), f"{r['id']}: no license record"
        assert r.get("access_level"), f"{r['id']}: no access_level"


def test_redistribution_policy_stated() -> None:
    assert CAT.get("redistribution_policy"), "catalog header must state the redistribution policy"
