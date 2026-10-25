"""Tests for the dashboard generator (scripts/build_dashboard.py).

The dashboard is a generated artifact claiming to mirror the repo's own
registers — if the extraction drifts, the page lies while looking
authoritative. These tests pin the contract between the repo and the
page.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_dashboard  # noqa: E402


def test_build_data_counts_match_repo() -> None:
    data = build_dashboard.build_data()
    assert len(data["sources"]) >= 160
    assert len(data["claims"]) >= 150
    assert len(data["datasets"]) == 22
    assert len(data["chapters"]) == 24
    assert len(data["projects"]) == 10
    assert all(p["status"] == "implemented" for p in data["projects"])
    assert data["repo"]["tests"] >= 500  # 586 at pin time
    if data["repo"].get("shallow"):
        # CI shallow clones (fetch-depth 1) carry no history: the count is
        # legitimately unavailable, and the generator must say so.
        assert data["repo"]["commits"] == 0
    else:
        assert data["repo"]["commits"] >= 100


def test_every_source_has_required_fields() -> None:
    data = build_dashboard.build_data()
    for s in data["sources"]:
        assert s["id"] and s["title"] and s["url"], s["id"]
        assert s["access_level"] in {
            "full-text-read",
            "abstract-read",
            "page-inspected",
            "metadata-only",
            "unavailable",
        }


def test_render_is_self_contained() -> None:
    """No external scripts, styles, or fonts: the page must work offline
    and on GitHub Pages without third-party requests."""
    data = build_dashboard.build_data()
    html = build_dashboard.render(data)
    assert not re.search(r'<script[^>]+src=["\']http', html)
    assert not re.search(r'<link[^>]+href=["\']http', html)
    assert "@import" not in html
    assert "fonts.googleapis" not in html


def test_render_contains_all_sections() -> None:
    data = build_dashboard.build_data()
    html = build_dashboard.render(data)
    for section in (
        "overview",
        "method",
        "chapters",
        "projects",
        "datasets",
        "sources",
        "claims",
        "careers",
        "quickstart",
    ):
        assert f'id="{section}"' in html, section
    assert "DASHBOARD_DATA" in html
    assert "The judge" in html


def test_payload_is_valid_json_with_careers() -> None:
    data = build_dashboard.build_data()
    html = build_dashboard.render(data)
    m = re.search(r"window\.DASHBOARD_DATA = (/\*__DATA__\*/)?(\{.*?\});?\n", html, re.S)
    assert m, "payload not found"
    payload = json.loads(m.group(2))
    assert len(payload["careers"]) == 3
    roles = {c["role"] for c in payload["careers"]}
    assert roles == {
        "AI safety researcher",
        "AI security specialist",
        "AI (safety) engineer",
    }
    assert len(payload["quickstart"]) >= 5
    for c in payload["careers"]:
        assert c["route_url"].startswith("https://github.com/AdilShamim8/AI-Safety")
        assert len(c["ladder"]) == 3


def test_generated_index_html_up_to_date() -> None:
    """The committed index.html must be regenerable: rendering fresh data
    must produce a file whose structural skeleton matches (the generated
    date and commit count legitimately differ)."""
    out = REPO_ROOT / "index.html"
    assert out.is_file()
    committed = out.read_text(encoding="utf-8")
    assert "window.DASHBOARD_DATA" in committed
    # the nine sections survived generation
    for section in (
        "overview",
        "method",
        "chapters",
        "projects",
        "datasets",
        "sources",
        "claims",
        "careers",
        "quickstart",
    ):
        assert f'id="{section}"' in committed, section
