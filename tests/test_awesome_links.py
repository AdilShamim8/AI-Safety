"""The link-layer instrument: AWESOME.md's live links vs. the register.

Rotation 3 (2026-10-25) opened the link layer — every entry in the
resource index carries a clickable link to its register URL, and every
link was verified live (liveness AND page identity) by
``scripts/verify_links.py`` before landing. The owner's directive
behind it: "you did not add the link and verify the link" — so the
repository now pins both halves of that promise.

What these tests keep true as the index grows:

  1. every bold-title entry adjacent to a register ID is a markdown
     link to exactly that entry's register URL — except the one
     expected-dead ID (the OpenAI Preparedness canonical 404, recorded
     in the register), which must stay UNlinked so no dead URL ships;
  2. every external link in the file points at a register URL or the
     bare origin of one (the AI Incident Database root is the host of
     SRC-REPORT-015) — the file's own admission rule: no unregistered
     links;
  3. the intro states the verified-link count in digits, recomputed
     from the file itself so growth fails loudly until the prose (and
     a fresh verify_links.py rotation) catches up.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

EXPECTED_DEAD = "SRC-REPORT-009"  # canonical 404 recorded in the register


def _read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def _register() -> dict[str, dict]:
    data = yaml.safe_load(_read("research/source-register.yaml"))
    return {s["id"]: s for s in data["sources"]}


def _clean(url: str) -> str:
    m = re.match(r"(https?://[^\s]+)", str(url).strip())
    return m.group(1) if m else str(url).strip()


def test_bold_entries_carry_their_register_link() -> None:
    """Rule 1: bold title + ID bracket => link to that ID's URL."""
    text = _read("AWESOME.md")
    reg = _register()
    checked = 0
    for m in re.finditer(r"\*\*([^*\n]+?)\*\*(?=\s*\[\s*(SRC-[A-Z]+-\d{3}))", text):
        title, sid = m.group(1).strip(), m.group(2)
        if sid == EXPECTED_DEAD:
            assert "](http" not in title, (
                f"{sid} is expected-dead (canonical 404 recorded); its" " title must stay unlinked"
            )
            continue
        assert (
            title.startswith("[") and f"]({_clean(reg[sid]['url'])})" in title
        ), f"{sid}: bold title {title!r} is not linked to its register URL"
        checked += 1
    assert checked >= 80, f"only {checked} bold entries carry links"


def test_every_external_link_is_registered() -> None:
    """Rule 2: external targets are register URLs or registered origins."""
    text = _read("AWESOME.md")
    reg_urls = {_clean(s["url"]) for s in _register().values() if s.get("url")}
    origins = {u.rsplit("/", 1)[0] if "/" in u[8:] else u for u in reg_urls}
    origins |= {f"{u.split('/')[0]}//{u.split('/')[2]}" for u in reg_urls if u.count("/") >= 3}
    allowed = reg_urls | origins
    bad = {t for t in re.findall(r"\]\((https?://[^)]+)\)", text) if t not in allowed}
    assert not bad, f"unregistered external links: {sorted(bad)[:5]}"


def test_intro_states_the_verified_count_in_digits() -> None:
    """Rule 3: the intro's link-layer claim matches the file's own ID set."""
    text = _squash(_read("AWESOME.md"))
    n_ids = len(set(re.findall(r"SRC-[A-Z]+-\d{3}", text)))
    assert f"fetched all {n_ids} URLs cited on this page" in text
    assert "scripts/verify_links.py" in text
    assert (REPO_ROOT / "scripts" / "verify_links.py").exists()


def test_link_instrument_is_runnable_and_documented() -> None:
    """The verifier exists, documents its channels, and the how-to-extend
    rule sends every new link through it."""
    doc = _read("scripts/verify_links.py")
    assert "arXiv API" in doc and "oEmbed" in doc
    assert EXPECTED_DEAD in doc
    awesome = _squash(_read("AWESOME.md"))
    assert "verify_links.py --ids" in awesome
