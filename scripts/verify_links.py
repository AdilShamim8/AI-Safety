#!/usr/bin/env python3
"""verify_links.py — liveness and identity check for register URLs.

The link-layer instrument (opened 2026-10-25, rotation 3): every
external URL this repository turns into a clickable link is fetched
server-side and checked for BOTH liveness (HTTP status) and identity
(the page title matches the register entry's title). Liveness alone
is not verification — a redirect to a parking page is live.

Three verification channels, priced by what each can honestly show:

  1. arXiv URLs — verified against the arXiv API (export.arxiv.org):
     the API returns the canonical title for the paper ID, which is
     matched against the register entry's title. This is the
     authoritative channel for the paper spine.
  2. YouTube watch URLs — verified via YouTube's oEmbed endpoint,
     which returns the canonical video title without authentication.
  3. Everything else (channels, playlists, blogs, reports, wikis) —
     a direct GET with a browser user agent; status, final URL after
     redirects, and the page's <title>/og:title are recorded.

Verdicts:
  LIVE              2xx/3xx and (where a title was extractable) the
                    title corroborates the register entry.
  LIVE-BOT-BLOCKED 401/403/405: the host refuses bots but the page is
                    not known to be gone (EEOC and Reuters have shown
                    this pattern since rotation 1). Reported, not
                    failed — the register's limitations field carries
                    the corroborating search evidence.
  EXPECTED-DEAD    404/410 on a URL whose death is already recorded in
                    the register (the OpenAI Preparedness canonical
                    page). Reported as a pass with its record cited.
  DEAD             404/410/connection failure with no death record.
                    Exit 1 — the link must not be added or must be
                    removed and the register entry corrected.

Usage:
  python scripts/verify_links.py              # every ID cited in AWESOME.md
  python scripts/verify_links.py --all        # every register source
  python scripts/verify_links.py --ids SRC-VIDEO-002,SRC-BLOG-003
  python scripts/verify_links.py --md NOTES.md  # IDs cited in one file

Part of the pre-link discipline: no URL becomes a markdown link in
AWESOME.md (or anywhere else) without passing through this script,
and each run is recorded in MAINTENANCE.md as a re-check rotation.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import yaml

REPO = Path(__file__).resolve().parents[1]
REGISTER = REPO / "research" / "source-register.yaml"

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TIMEOUT = 25
# URLs whose death is already recorded in the register itself.
EXPECTED_DEAD = {
    "SRC-REPORT-009": "canonical page 404 recorded in the register entry",
}
ARXIV_API = "https://export.arxiv.org/api/query"
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(v\d+)?")
WATCH_RE = re.compile(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})")


def _norm(text: str) -> str:
    """Comparison form: lowercase, alphanumeric only, single-spaced."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


STOP = {
    "the",
    "a",
    "an",
    "of",
    "and",
    "or",
    "for",
    "to",
    "in",
    "on",
    "is",
    "are",
    "with",
    "from",
    "by",
    "how",
    "your",
    "you",
    "what",
    "that",
    "this",
    "s",
    "it",
    "its",
    "at",
    "as",
    "be",
}


def _tokens(text: str) -> set[str]:
    """Significant tokens: the identity key for title comparison."""
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 1 and t not in STOP}


def _identity(rtitle: str, ptitle: str) -> tuple[bool | None, str]:
    """Token-overlap identity: is this page the page the register means?

    Register titles carry house annotations — parentheticals like
    "(YouTube channel)" and colon-subtitles — so the comparison strips
    parentheticals and compares significant-token overlap in both
    directions. A 60% overlap on either side passes: page titles
    reorder words ("Curriculum | AI Safety — ARENA" vs "ARENA
    curriculum"), append hosts ("| Substack"), or reword a verb
    ("reduce" to "mitigate") without being a different page.
    """
    if not ptitle:
        return None, "no page title extractable"
    reg = _tokens(re.sub(r"\([^)]*\)", "", rtitle))
    pag = _tokens(ptitle)
    if not pag:
        return None, "page title is generic/stopwords only"
    inter = reg & pag
    r_ratio = len(inter) / len(reg) if reg else 0.0
    p_ratio = len(inter) / len(pag)
    if r_ratio >= 0.6 or p_ratio >= 0.6:
        if 0 < len(inter) < min(len(reg), len(pag)):
            return True, f"title wording drifts: page says {ptitle[:60]!r}"
        return True, ""
    return False, f"TITLE MISMATCH page={ptitle[:70]}"


# Hosts where the domain alone can NEVER carry identity (shared
# repositories: any paper/repo/channel lives there). On these, only the
# title match counts. Everywhere else, an exact-domain page with a
# generic or reworded title is still the subject's own site.
SHARED_HOSTS = {"arxiv.org", "youtube.com", "youtu.be", "github.com"}


def _domain(url: str) -> str:
    return urlparse(url).netloc.removeprefix("www.")


def _domain_identity(url: str, final: str, ptitle: str) -> tuple[bool | None, str]:
    """Exact-domain fallback for self-hosted sites with opaque titles."""
    if not url or not final:
        return None, ""
    d, fd = _domain(url), _domain(final)
    if not d or d != fd or d in SHARED_HOSTS:
        return None, ""
    return True, f"domain match ({d}); page title {ptitle[:40]!r} not identity-bearing"


def _clean_url(raw: str) -> str:
    """Register urls must be bare; strip any trailing annotation."""
    m = re.match(r"(https?://[^\s]+)", str(raw).strip())
    return m.group(1) if m else str(raw).strip()


def fetch(url: str) -> dict:
    """GET with redirects followed; return status/final-url/title."""
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        with urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(300_000).decode("utf-8", errors="replace")
            title = ""
            for pat in (
                r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)',
                r"<title[^>]*>(.*?)</title>",
            ):
                m = re.search(pat, body, re.IGNORECASE | re.DOTALL)
                if m:
                    title = re.sub(r"\s+", " ", html.unescape(m.group(1))).strip()
                    break
            return {"status": resp.status, "final": resp.geturl(), "title": title}
    except HTTPError as e:
        return {"status": e.code, "final": url, "title": ""}
    except (URLError, TimeoutError, OSError) as e:
        return {"status": None, "final": url, "title": "", "error": str(e)[:80]}


def arxiv_batch(entries: list[dict]) -> dict[str, str]:
    """Canonical titles from the arXiv API for all arXiv-URL entries."""
    ids: list[str] = []
    key_of: dict[str, str] = {}
    for e in entries:
        m = ARXIV_RE.search(e["url"])
        if not m:
            continue
        aid = m.group(1)
        ids.append(aid)
        key_of[aid] = e["id"]
    titles: dict[str, str] = {}
    for i in range(0, len(ids), 40):
        chunk = ids[i : i + 40]
        q = urlencode({"id_list": ",".join(chunk), "max_results": len(chunk)})
        try:
            with urlopen(
                Request(f"{ARXIV_API}?{q}", headers={"User-Agent": UA}),
                timeout=TIMEOUT,
            ) as resp:
                root = ET.fromstring(resp.read().decode("utf-8", errors="replace"))
            ns = {"a": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("a:entry", ns):
                aid = entry.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1]
                aid = re.sub(r"v\d+$", "", aid)
                t = re.sub(r"\s+", " ", entry.findtext("a:title", "", ns)).strip()
                titles[key_of.get(aid, aid)] = t
        except (HTTPError, URLError, ET.ParseError, TimeoutError, OSError) as e:
            print(f"  arXiv API batch failed: {e}", file=sys.stderr)
    return titles


def verify_one(entry: dict, arxiv_titles: dict[str, str]) -> dict:
    """Full verdict for one register entry."""
    eid, url, rtitle = entry["id"], entry["url"], entry["title"]
    verdict = {
        "id": eid,
        "url": url,
        "register_title": rtitle,
        "status": None,
        "channel": "",
        "title": "",
        "note": "",
    }
    # Channel 1: arXiv API — authoritative for the paper spine.
    if eid in arxiv_titles:
        api = arxiv_titles[eid]
        ok, note = _identity(rtitle, api)
        verdict.update(status=200, channel="arxiv-api", title=api, note=note)
        verdict["live"] = True
        verdict["identity"] = ok
        return verdict
    # Channel 2: YouTube oEmbed — authoritative for watch URLs.
    m = WATCH_RE.search(url)
    if m:
        try:
            q = urlencode(
                {"url": f"https://www.youtube.com/watch?v={m.group(1)}", "format": "json"}
            )
            with urlopen(
                Request(f"https://www.youtube.com/oembed?{q}", headers={"User-Agent": UA}),
                timeout=TIMEOUT,
            ) as resp:
                meta = json.loads(resp.read().decode("utf-8"))
            ok, note = _identity(rtitle, meta.get("title", ""))
            verdict.update(
                status=resp.status, channel="oembed", title=meta.get("title", ""), note=note
            )
            verdict["live"] = True
            verdict["identity"] = ok
            return verdict
        except (HTTPError, URLError, json.JSONDecodeError, TimeoutError, OSError):
            pass  # fall through to the direct fetch
    # Channel 3: direct GET.
    r = fetch(url)
    verdict.update(status=r["status"], channel="get", title=r.get("title", ""))
    verdict["final"] = r["final"]
    if "error" in r:
        verdict["note"] = r["error"]
    if r["status"] and 200 <= r["status"] < 400:
        verdict["live"] = True
        if r.get("title"):
            ok, note = _identity(rtitle, r["title"])
            if ok is False:
                ok, dom_note = _domain_identity(url, r.get("final", ""), r["title"])
                note = dom_note or note
            verdict["identity"] = ok
            if note:
                verdict["note"] = note
        else:
            ok, note = _domain_identity(url, r.get("final", ""), "")
            verdict["identity"] = ok if ok is not None else None
            verdict["note"] = note or "alive; no title extractable (JS-rendered?)"
    elif r["status"] in (401, 403, 405):
        verdict["live"] = True  # bot-blocked, not known-dead
        verdict["identity"] = None
        verdict["note"] = "bot-blocked (register carries search corroboration)"
    else:
        verdict["live"] = False
        verdict["identity"] = False
    return verdict


def collect_ids(md_path: Path | None, do_all: bool, id_arg: str) -> list[str]:
    """Which register IDs to verify, and from where."""
    if id_arg:
        return [x.strip() for x in id_arg.split(",") if x.strip()]
    if do_all:
        reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
        return [s["id"] for s in reg["sources"]]
    target = md_path or (REPO / "AWESOME.md")
    text = target.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"SRC-[A-Z]+-\d{3}", text)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--all", action="store_true", help="verify the whole register")
    ap.add_argument("--md", type=Path, help="verify IDs cited in this markdown file")
    ap.add_argument("--ids", help="comma-separated register IDs")
    args = ap.parse_args()

    reg = yaml.safe_load(REGISTER.read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in reg["sources"]}
    ids = collect_ids(args.md, args.all, args.ids or "")
    entries = [
        {"id": i, "url": _clean_url(by_id[i]["url"]), "title": by_id[i]["title"]}
        for i in ids
        if i in by_id and by_id[i].get("url")
    ]
    skipped = [i for i in ids if i not in by_id]
    if skipped:
        print(f"NOT IN REGISTER (audit must catch these): {skipped}")
        return 2

    n_arxiv = sum(1 for e in entries if ARXIV_RE.search(e["url"]))
    print(f"verifying {len(entries)} register URLs ({n_arxiv} via arXiv API)")
    arxiv_titles = arxiv_batch(entries)
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda e: verify_one(e, arxiv_titles), entries))

    failures = []
    print(f"\n{'ID':<17}{'VERDICT':<22}{'CHANNEL':<11}PAGE TITLE")
    print("-" * 110)
    for v in results:
        if not v["live"] and v["id"] in EXPECTED_DEAD:
            state = "EXPECTED-DEAD"
        elif not v["live"]:
            state = "DEAD"
            failures.append(v)
        elif v["identity"] is False:
            state = "LIVE-WRONG-PAGE"
            failures.append(v)
        elif v["identity"] is None:
            state = "LIVE-BOT-BLOCKED" if "bot-blocked" in v["note"] else "LIVE-NO-TITLE"
        else:
            state = "LIVE"
        print(f"{v['id']:<17}{state:<22}{v['channel']:<11}{v['title'][:58]}")
        if v["note"]:
            print(f"{'':<17}note: {v['note']}")
        if v.get("final") and v["final"] != v["url"]:
            print(f"{'':<17}redirected to: {v['final'][:90]}")
    print("-" * 110)
    n_live = sum(1 for v in results if v["live"])
    print(f"{n_live}/{len(results)} live; {len(failures)} hard failures")
    for v in failures:
        print(f"  FAIL {v['id']}: {v['note'] or 'unreachable'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
