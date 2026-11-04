"""The honesty ledger vs the claims register.

Session-13 origin (P25): courses/honesty-ledger.md justifies the
lecture library's access discipline by naming the claims that pin it
(1 distinct CLM ids today). Every id it names must
exist in the claims register (the S13-P07 renumbering fixed the
collisions this sweep would have caught), and every SRC-CURR row it
cites must exist in the source register.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
LEDGER = (REPO / "courses/honesty-ledger.md").read_text(encoding="utf-8")
CLAIMS = {
    c["id"] for c in yaml.safe_load((REPO / "research/claims-register.yaml").read_bytes())["claims"]
}
SOURCES = {
    s["id"]
    for s in yaml.safe_load((REPO / "research/source-register.yaml").read_bytes())["sources"]
}


def test_every_cited_claim_exists() -> None:
    cited = set(re.findall(r"CLM-\d{4}", LEDGER))
    assert cited, "no claims cited in the ledger"
    for cid in cited:
        assert cid in CLAIMS, f"ledger cites {cid} not in register"


def test_every_cited_source_exists() -> None:
    for sid in set(re.findall(r"SRC-[A-Z]+-\d+[a-z]?", LEDGER)):
        assert sid in SOURCES, f"ledger cites {sid} not in register"


def test_ledger_states_the_two_account_walled_courses() -> None:
    flat = re.sub(r"\s+", " ", LEDGER)
    assert "No DataCamp exercise was opened" in flat
    assert "No CampusX video was watched" in flat
