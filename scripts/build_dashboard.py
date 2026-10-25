#!/usr/bin/env python3
"""build_dashboard.py — generate the single-file index.html dashboard.

Reads the repository's own registers and catalogs (never hand-maintained
numbers), assembles one JSON payload, and injects it into
scripts/dashboard_template.html to emit a self-contained index.html at
the repository root: no external CSS/JS/fonts, works offline, and is
GitHub-Pages-ready.

Data extracted:
  - research/source-register.yaml     -> sources (160)
  - research/claims-register.yaml     -> claims (150)
  - datasets/catalog.yaml             -> datasets (22)
  - planning/content-matrix.yaml      -> chapters (24), projects (10)
  - git rev-list --count HEAD         -> commit count
  - pytest --collect-only -q          -> test count
  - paper/comparison note indexes     -> note counts

The generator is itself tested (tests/test_dashboard.py) and is part of
the pre-commit discipline: if a register changes, regenerate.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "scripts/dashboard_template.html"
OUT = REPO / "index.html"

#: What the build honestly did NOT execute — mirrors each project
#: README's not-executed tiers and STATUS's counters. The dashboard
#: shows the wins AND the gaps; hiding the gaps here would betray the
#: method the page is selling.
NOT_EXECUTED = [
    {
        "id": "P03",
        "tier": "ml compute tier",
        "what": (
            "TruthfulQA / XSTest runs against a local small model " "with the real scorer pipeline"
        ),
    },
    {
        "id": "P04",
        "tier": "real-model tier",
        "what": (
            "the preference-optimization audit on an actual tuned policy "
            "(the deterministic organism carries the seam)"
        ),
    },
    {
        "id": "P06",
        "tier": "compute tier",
        "what": (
            "activation patching on a real open model "
            "(TransformerLens-style hooking per the Ch.09 exercise protocol)"
        ),
    },
    {
        "id": "P07",
        "tier": "tier 1 + tier 2",
        "what": (
            "the live agent runtime, and human consent-decay rates "
            "(tier-2 evidence: out of scope for an offline build)"
        ),
    },
    {
        "id": "P10",
        "tier": "live + adaptive",
        "what": (
            "a live agent system and the adaptive red-team phase "
            "against the deployed configuration"
        ),
    },
    {
        "id": "course-wide",
        "tier": "real local-model experiments",
        "what": (
            "0 of the 3 required compute-tier executions "
            "(recorded honestly in planning/STATUS.md)"
        ),
    },
]

CAREERS = [
    {
        "role": "AI safety researcher",
        "question": "why does the system fail — and what does that teach about alignment?",
        "summary": (
            "Papers, evaluation reports, falsified hypotheses. The route runs the "
            "alignment spine (Ch.03–05, 07, 09–11, 18) with P02/P04/P05/P06, and "
            "enters through fellowships (MATS: 12 weeks, 631 alumni since 2021) and "
            "research-artifact portfolios."
        ),
        "route_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/alignment-research.md",
        "page_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/careers-index.md",
        "ladder": [
            [
                "Rung 2",
                "Ch.03-05 chain + P02 + P04: one Goodhart-style result with honest intervals",
            ],
            ["Rung 3", "P06 causal-claims study + the Ch.24 research proposal"],
            ["Rung 4", "MATS application with this fork's commit history as evidence"],
        ],
    },
    {
        "role": "AI security specialist",
        "question": "how does an adversary break it — and what boundary stops them?",
        "summary": (
            "Threat models, red-team reports with denominators, regression suites. "
            "The route runs the security spine (Ch.12–16, 19) with P07/P08/P10, and "
            "hires today under four titles per the SANS 10,643-posting analysis: "
            "AI/ML Security Engineer, AI Red Team Engineer, AI Governance and "
            "Security Risk Lead, AI Security Architect."
        ),
        "route_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/ai-security-engineering.md",
        "page_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/careers-index.md",
        "ladder": [
            [
                "Rung 2",
                "Ch.12-14 chain + P07: one threat model + one isolated attack/defense evaluation",
            ],
            ["Rung 3", "Ch.15 red-team report with denominators + Ch.16 provenance audit"],
            ["Rung 4", "Search the four titles directly; the P10 dossier is the portfolio"],
        ],
    },
    {
        "role": "AI (safety) engineer",
        "question": "what do we ship — with which safeguards, at what utility price?",
        "summary": (
            "Guardrails, monitors, harnesses, release gates, runbooks. The route runs "
            "the evaluations spine (Ch.05, 08, 17, 22–23) with P01/P03/P08/P09/P10 — "
            "the harness-to-dossier miniature of the day job — and hires under "
            "Safeguards/Trust/MTS titles at labs and platforms."
        ),
        "route_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/evaluations-and-assurance.md",
        "page_url": "https://github.com/AdilShamim8/AI-Safety"
        "/tree/main/roadmaps/careers-index.md",
        "ladder": [
            ["Rung 2", "P03 calibration audit + Ch.08 + P08 control protocol at a stated budget"],
            ["Rung 3", "P09 shift/subgroup audit + release-gate design in safety-case grammar"],
            ["Rung 4", "The P10 dossier: send the integration artifact, not a resume bullet"],
        ],
    },
]

QUICKSTART = [
    {
        "title": "Take the diagnostic (30 min)",
        "body": (
            "Read <code>START_HERE.md</code> (and <code>FAQ.md</code> for the questions "
            "everyone asks next), then <code>prerequisites/diagnostic.md</code> — five "
            "tasks (R1–R5) that place your math, ML, and security baseline. Worked "
            "answers are included; grade yourself honestly."
        ),
    },
    {
        "title": "Learn the verification habit (5 min, once)",
        "body": (
            "<code>prerequisites/verifying-sources.md</code> — where each kind of "
            "information actually lives, what an access level is, and how to write a "
            "falsifiable claim. The whole course runs on this; the evidence ladder "
            "above is what it looks like at scale."
        ),
    },
    {
        "title": "Set up the repository (10 min)",
        "body": (
            "Clone, then <code>uv sync</code>, then <code>uv run pytest</code> — "
            "the full deterministic suite must pass before anything else. "
            "Every project runs offline on a laptop: no GPUs, no API keys."
        ),
    },
    {
        "title": "Read Chapter 01 and write one threat hypothesis (8 h)",
        "body": (
            "The first artifact of the whole course: a hazard claim with observations "
            "that would weaken it. This single exercise sets the epistemic tone — "
            "claims you can imagine failing, not vibes."
        ),
    },
    {
        "title": "Preregister your first evaluation (Ch.02, 12 h)",
        "body": (
            "Construct validity, dependence-aware splits, Wilson intervals, power. "
            "Then run P01's harness smoke tier and validate the scorer against "
            "hand-verified labels."
        ),
    },
    {
        "title": "Fork the discipline, not just the repo",
        "body": (
            "From here the route pages own the sequence (alignment / security / "
            "evaluations), and <code>roadmaps/careers-index.md</code> owns the "
            "progress ladder: artifacts, not hours."
        ),
    },
]


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_bytes())


def _commit_count() -> tuple[int, bool]:
    """Commit count and a shallow-clone flag. CI checkouts clone with
    fetch-depth 1, where rev-list counts 1; the dashboard must never
    embed that as the repository's commit count."""
    shallow = (
        subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        == "true"
    )
    out = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True
    )
    count = int(out.stdout.strip())
    if shallow and count <= 1:
        return 0, True
    return count, False


def _test_count() -> int:
    """Sum the per-file counts from pytest -q --collect-only output
    (this pytest version emits `tests/test_x.py: N` lines, no total)."""
    out = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    )
    m = re.search(r"(\d+) tests collected", out.stdout)
    if m:
        return int(m.group(1))
    counts = re.findall(r"tests/[^:]+: (\d+)", out.stdout)
    if counts:
        return sum(int(c) for c in counts)
    raise SystemExit("could not count tests from pytest --collect-only output")


def _note_counts() -> tuple[int, int]:
    notes_dir = REPO / "research/notes"
    papers = [p for p in notes_dir.glob("*.md") if re.match(r"\d{2}-", p.name)]
    comparisons = list(notes_dir.glob("comparison-*.md"))
    return len(papers), len(comparisons)


def _note_titles() -> list[dict[str, str]]:
    """Title lines of the paper notes, for the notes widget."""
    out = []
    for p in sorted((REPO / "research/notes").glob("*.md")):
        if not re.match(r"\d{2}-", p.name):
            continue
        first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        out.append({"file": p.name, "title": first})
    return out


def _incidents() -> list[dict[str, str]]:
    """Parse the incident index README table into cards."""
    import re as _re

    table = (REPO / "research/notes/incidents/README.md").read_text(encoding="utf-8")
    rows = []
    for line in table.splitlines():
        m = _re.match(r"\| (\d\d) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|", line)
        if m:
            row = {
                "no": m.group(1),
                "name": m.group(2),
                "class": m.group(3),
                "lesson": m.group(4),
                "note": (
                    m.group(5).strip()[1:-1] if m.group(5).strip().startswith("[") else m.group(5)
                ),
            }
            no = int(m.group(1))
            if no <= 3:
                row["era"] = "liability & authority (2023-24)"
                row["year"] = "2023-24"
            elif no <= 8:
                row["era"] = "rollout & channel (2023-25)"
                row["year"] = "2023-25"
            elif no <= 11:
                row["era"] = "history (2016-23)"
                row["year"] = "2016-23"
            else:
                row["era"] = "accountability (2018-23)"
                row["year"] = "2018-23"
            rows.append(row)
    return rows


def _fs_track() -> list[dict[str, str]]:
    """The from-scratch researcher track modules."""
    out = []
    for p in sorted((REPO / "research/ai-researcher-from-scratch").glob("*.md")):
        if p.name == "README.md":
            continue
        first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        out.append({"file": p.name, "title": first})
    return out


def _note_coverage() -> list[dict]:
    """Count note-companion links per chapter README for the coverage widget."""
    out = []
    for pdir in sorted((REPO / "chapters").glob("[0-9][0-9]-*")):
        readme = pdir / "README.md"
        if not readme.is_file():
            continue
        text = readme.read_text(encoding="utf-8")
        links = re.findall(r"\]\(\.\./\.\./research/notes/([\w-]+\.md)\)", text)
        out.append(
            {
                "ch": pdir.name.split("-")[0],
                "title": pdir.name.split("-", 1)[1],
                "notes": len(set(links)),
            }
        )
    return out


def _progress_trackers() -> list[dict]:
    """Parse the per-route progress trackers into milestone summaries."""
    routes = [
        ("alignment-research", "AI safety researcher"),
        ("ai-security-engineering", "AI security specialist"),
        ("evaluations-and-assurance", "AI (safety) engineer"),
        ("audit-only", "The reader/judge (audit route)"),
    ]
    out = []
    for slug, role in routes:
        f = REPO / "roadmaps" / "progress" / f"{slug}.md"
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        milestones = []
        cur = None
        for line in text.splitlines():
            m = re.match(r"^## (M\d+) — (.+?)(?: \(.*\))?$", line)
            if m:
                cur = {"id": m.group(1), "name": m.group(2), "boxes": 0}
                milestones.append(cur)
                continue
            if cur is not None and line.startswith("- [ ]"):
                cur["boxes"] += 1
        out.append(
            {
                "slug": slug,
                "role": role,
                "milestones": milestones,
                "boxes": sum(m["boxes"] for m in milestones),
            }
        )
    return out


def _project_headlines() -> dict[str, str]:
    """One-line honest headline per project, read from each README's
    'Pinned results' or opening — sourced from the repo itself."""
    headlines: dict[str, str] = {}
    for pdir in sorted((REPO / "projects").iterdir()):
        readme = pdir / "README.md"
        if not readme.is_file():
            continue
        pid = pdir.name.split("-")[0].upper()
        text = readme.read_text(encoding="utf-8")
        m = re.search(r"\*\*The headline:\*\*(.+?)(?:\n\n|\Z)", text, re.S)
        if not m:
            m = re.search(r"\*\*The verdict:.*?\*\*(.+?)(?:\n\n|\Z)", text, re.S)
        if not m:
            m = re.search(r"^## Pinned results.*?^\|.*\n(\|.*\n)", text, re.M | re.S)
        headlines[pid] = (
            re.sub(r"\s+", " ", m.group(1)).strip()[:180]
            if m
            else ("see the project README for pinned results")
        )
    return headlines


GH_BASE = "https://github.com/AdilShamim8/AI-Safety"

#: The four routes and the synthesis block, as the dependency map draws
#: them (planning/dependency-map.md) — prose structure, not counts.
ROUTES = [
    {
        "slug": "alignment-research",
        "name": "Alignment research",
        "verb": "investigate failures",
        "purpose": "Investigate alignment interventions and their failure modes.",
        "evidence": ("Replication, ablation, critical research memo, falsifiable extension"),
        "sequence": (
            "03 specification → 04 preference learning → 05 oversight → "
            "07 deception → 09–11 interpretability → 18 faithfulness"
        ),
        "url": f"{GH_BASE}/tree/main/roadmaps/alignment-research.md",
    },
    {
        "slug": "ai-security-engineering",
        "name": "AI security engineering",
        "verb": "bound them",
        "purpose": "Secure AI applications and agent workflows.",
        "evidence": (
            "Threat model, isolated attack/defense evaluation, regression "
            "suite, remediation report"
        ),
        "sequence": (
            "12 adversarial ML → 13 LLM app security → 14 agent/MCP "
            "security → 15 red teaming → 16 privacy & supply chains → 19 multimodal"
        ),
        "url": f"{GH_BASE}/tree/main/roadmaps/ai-security-engineering.md",
    },
    {
        "slug": "evaluations-and-assurance",
        "name": "Evaluations and assurance",
        "verb": "test and argue them",
        "purpose": "Design credible tests and contextual safety arguments.",
        "evidence": (
            "Dataset card, validated scorers, uncertainty analysis, "
            "monitoring study, evidence-backed safety case"
        ),
        "sequence": (
            "05 oversight → 08 control → 17 shift & reliability → "
            "22 safety engineering → 23 governance"
        ),
        "url": f"{GH_BASE}/tree/main/roadmaps/evaluations-and-assurance.md",
    },
    {
        "slug": "audit-only",
        "name": "Audit-only",
        "verb": "read and judge",
        "purpose": "Read and judge the build without PyTorch — the verification route.",
        "evidence": "Critical audits, register cross-checks, honest-tier reviews",
        "sequence": "01–02 spine → the registers → chapter critiques → the audit checklist",
        "url": f"{GH_BASE}/tree/main/roadmaps/audit-only.md",
    },
]

#: Chapter blocks as the dependency map and route pages group them: display
#: name, short key (used by the page's route filter), and member chapter ids.
#: Chapter 05 appears in both the alignment and evaluations lines (the route
#: pages both claim it); the catalog shows it once, tagged for both. Chapter
#: 06 is the evaluations route's honesty/calibration unit per that route
#: page's own sequence (week 4: "Ch.06 honesty, uncertainty, selective
#: prediction").
CHAPTER_BLOCKS = [
    ("The common methodological spine", "spine", ["01", "02"]),
    ("The alignment-research line", "alignment", ["03", "04", "05", "07", "09", "10", "11", "18"]),
    ("The security-engineering line", "security", ["12", "13", "14", "15", "16", "19"]),
    ("The evaluations-and-assurance line", "evaluations", ["06", "08", "17", "22", "23"]),
    ("The synthesis", "synthesis", ["20", "21", "24"]),
]

#: Incident-era descriptions, from research/notes/incidents/README.md.
INCIDENT_ERAS = [
    {
        "era": "liability & authority (2023-24)",
        "range": "01-03",
        "desc": (
            "The classic era: the generation channel meets contract law. "
            "Air Canada's tribunal, DPD's regression, Chevy's $1 Tahoe."
        ),
    },
    {
        "era": "rollout & channel (2023-25)",
        "range": "04-08",
        "desc": (
            "AI Overviews' satire laundering, MyCity's unlawful answers, "
            "Cursor's invented policy, Slack's injection exfiltration, Samsung's pastes."
        ),
    },
    {
        "era": "history (2016-23)",
        "range": "09-11",
        "desc": (
            "The incidents the modern conversation grew from — Bing's spilled "
            "prompt, Tay's sixteen hours, Sydney's two hours — reviewed under "
            "the same template."
        ),
    },
    {
        "era": "accountability (2018-23)",
        "range": "12-14",
        "desc": (
            "The harm arrived through the training data and the audit was the "
            "instrument that worked: Galactica's three-day withdrawal, the "
            "EEOC's first AI-bias settlement, Amazon's scrapped recruiting engine."
        ),
    },
]

#: The three schedules, parsed from roadmaps/study-schedules.md.


def _md_inline(text: str) -> str:
    """Minimal inline-markdown renderer for prose pulled out of the repo's
    own documents: bold, code spans, and links (relative targets are
    absolutized to the GitHub blob URL so the single-file page stays
    navigable). Text is HTML-escaped first; everything else is additive."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _link(m: re.Match[str]) -> str:
        label, target = m.group(1), m.group(2)
        if target.startswith(("http", "#", "mailto:")):
            href = target
        else:
            href = f"{GH_BASE}/blob/main/{target}"
        return f'<a href="{href}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w&;])`([^`\n]+)`", r"<code>\1</code>", text)
    return text


def _paragraphs(lines: list[str]) -> list[str]:
    """Split a run of lines into blank-line-separated paragraphs."""
    out: list[str] = []
    cur: list[str] = []
    for line in lines:
        if line.strip():
            cur.append(line.strip())
        elif cur:
            out.append(" ".join(cur))
            cur = []
    if cur:
        out.append(" ".join(cur))
    return out


def _syllabus_rows() -> list[dict[str, str]]:
    """The 24-row course catalog from SYLLABUS.md: description, hard
    prerequisites, core artifact, and attached projects per chapter."""
    text = (REPO / "SYLLABUS.md").read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        m = re.match(r"\| (\d{2}) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", line)
        if not m:
            continue
        chapter = m.group(2)
        if " — " in chapter:
            title, desc = chapter.split(" — ", 1)
        else:
            title, desc = chapter, ""
        prereq = m.group(3).strip()
        rows.append(
            {
                "id": m.group(1),
                "title": title.strip(),
                "desc": desc.strip(),
                "prereq": "" if prereq == "—" else prereq,
                "artifact": m.group(4).strip(),
                "projects": m.group(5).strip(),
            }
        )
    return rows


def _glossary() -> list[dict[str, str]]:
    """Glossary terms from GLOSSARY.md's table: term, definition, common
    confusion, and the chapters that use it."""
    text = (REPO / "GLOSSARY.md").read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| **"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6:
            continue
        rows.append(
            {
                "term": parts[1].strip("*"),
                "def": parts[2],
                "aliases": parts[3],
                "confusion": parts[4],
                "chapters": parts[5],
            }
        )
    return rows


def _faq() -> list[dict]:
    """FAQ.md into sectioned question cards; answers keep their links as
    GitHub-absolutized anchors."""
    text = (REPO / "FAQ.md").read_text(encoding="utf-8")
    sections: list[dict] = []
    cur_section: dict | None = None
    cur_q: dict | None = None
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and "FAQ" not in line:
            cur_section = {"section": line[3:].strip(), "items": []}
            sections.append(cur_section)
            cur_q = None
            buf = []
            continue
        if line.startswith("**") and line.rstrip().endswith("**") and "?" in line:
            if cur_q is not None:
                cur_q["a"] = _md_inline(" ".join(buf)).strip()
            elif cur_section is not None and buf:
                cur_section["intro"] = _md_inline(" ".join(buf))
            buf = []
            if cur_section is not None:
                cur_q = {"q": _md_inline(line.strip("*")), "a": ""}
                cur_section["items"].append(cur_q)
            continue
        buf.append(line)
    if cur_q is not None:
        cur_q["a"] = _md_inline(" ".join(buf)).strip()
    for s in sections:
        for item in s["items"]:
            item["a"] = item["a"].strip()
    return sections


def _awesome() -> list[dict]:
    """AWESOME.md into themed sections of annotated entries. Sections
    without `- **bold**` entries (e.g. pointers to other repo surfaces)
    keep their paragraph as the section note — nothing is dropped."""
    text = (REPO / "AWESOME.md").read_text(encoding="utf-8")
    sections: list[dict] = []
    cur_section: dict | None = None
    cur_entry: dict | None = None
    para: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and "AWESOME" not in line:
            cur_section = {"section": line[3:].strip(), "entries": [], "paras": []}
            sections.append(cur_section)
            cur_entry = None
            para = []
            continue
        if line.startswith("- **") and cur_section is not None:
            m = re.match(r"- \*\*(.+?)\*\*(.*)$", line)
            cur_entry = {"name": m.group(1), "rest": [m.group(2).strip()]}
            cur_section["entries"].append(cur_entry)
            continue
        if cur_entry is not None and line.startswith("  "):
            cur_entry["rest"].append(line.strip())
            continue
        if cur_section is not None and line.startswith("- "):
            # non-bold list line: belongs to the section paragraph flow
            para.append(line[2:].strip())
            continue
        if cur_section is not None:
            if line.strip():
                para.append(line.strip())
            elif para:
                cur_section["paras"].append(" ".join(para))
                para = []
    if cur_section is not None and para:
        cur_section["paras"].append(" ".join(para))
    out: list[dict] = []
    for s in sections:
        entries = []
        for e in s["entries"]:
            rest = " ".join(r for r in e["rest"] if r)
            ids = re.findall(r"(?:SRC|DS)-[A-Z]+-\d+", rest)
            note = rest
            # strip the leading id bracket(s) and dash separator
            note = re.sub(r"^(\s*\[[^\]]*\]\s*)+", "", note)
            note = note.lstrip("—- ").strip()
            entries.append(
                {
                    # titles carry live markdown links since the link
                    # layer opened (rotation 3); render them as anchors
                    "name": _md_inline(e["name"]),
                    "ids": ids,
                    "note": _md_inline(note),
                }
            )
        # trim parenthetical stale-count risk from the display title
        title = re.sub(r"\s*\(\d+[^)]*\)$", "", s["section"])
        out.append(
            {
                "section": title,
                "full_title": s["section"],
                "entries": entries,
                "note": _md_inline(" ".join(s["paras"])).strip(),
            }
        )
    return out


def _schedules() -> list[dict]:
    """Study-schedule headlines from roadmaps/study-schedules.md."""
    text = (REPO / "roadmaps" / "study-schedules.md").read_text(encoding="utf-8")
    schedules: list[dict] = []
    cur: dict | None = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"## Schedule ([A-Z]) — (.+)$", line)
        if m:
            if cur is not None:
                cur["note"] = _md_inline(" ".join(buf[:2])).strip()
            cur = {"letter": m.group(1), "tagline": m.group(2).strip(), "note": ""}
            schedules.append(cur)
            buf = []
            continue
        if cur is not None:
            buf.append(line)
    if cur is not None:
        cur["note"] = _md_inline(" ".join(buf[:2])).strip()
    return schedules


def _notes_index() -> dict:
    """The research-notebook index: paper notes with their register source
    and honest method level, plus the comparison-note titles."""
    table = (REPO / "research" / "notes" / "README.md").read_text(encoding="utf-8")
    papers: list[dict] = []
    for line in table.splitlines():
        m = re.match(
            r"\| (\d{2}) \| \[(.+?)\]\(([\w-]+\.md)\) \| (SRC-[A-Z]+-\d+) \| (.+?) \|", line
        )
        if m:
            papers.append(
                {
                    "no": m.group(1),
                    "title": m.group(2),
                    "file": m.group(3),
                    "source": m.group(4),
                    "level": m.group(5),
                }
            )
    comparisons = []
    for p in sorted((REPO / "research" / "notes").glob("comparison-*.md")):
        first = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ")
        comparisons.append({"file": p.name, "title": first})
    return {"papers": papers, "comparisons": comparisons}


def _dir_names(directory: str, prefix: str) -> dict[str, str]:
    """Actual on-disk directory names keyed by chapter/project number, so
    generated links never depend on slugifying a display title."""
    out: dict[str, str] = {}
    for d in sorted((REPO / directory).iterdir()):
        if d.is_dir() and d.name.startswith(prefix):
            num = d.name.split("-", 1)[0]
            out[num.upper() if prefix.startswith("p") else num] = d.name
    return out


def _access_counts(sources_raw: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for s in sources_raw:
        lvl = str(s.get("access_level", "unknown"))
        counts[lvl] = counts.get(lvl, 0) + 1
    order = [
        "full-text-read",
        "abstract-read",
        "page-inspected",
        "metadata-only",
        "unavailable",
    ]
    return {lvl: counts.get(lvl, 0) for lvl in order if counts.get(lvl, 0)}


def build_data() -> dict:
    sources_raw = _load(REPO / "research/source-register.yaml")["sources"]
    claims_raw = _load(REPO / "research/claims-register.yaml")["claims"]
    catalog = _load(REPO / "datasets/catalog.yaml")
    matrix = _load(REPO / "planning/content-matrix.yaml")

    sources = [
        {
            "id": s["id"],
            "title": s["title"],
            "org": s.get("authors_or_organization", ""),
            "type": s.get("source_type", ""),
            "url": s.get("url", ""),
            "access_level": s.get("access_level", ""),
            "accessed_on": str(s.get("accessed_on", "")),
        }
        for s in sources_raw
    ]
    claims = [
        {
            "id": c["id"],
            "claim": re.sub(r"\s+", " ", str(c["claim"])).strip(),
            "source": c.get("source", ""),
            "evidence_strength": c.get("evidence_strength", ""),
            "date": str(c.get("date", "")),
        }
        for c in claims_raw
    ]
    datasets = []
    for d in catalog["datasets"]:
        lic = d.get("license") or {}
        datasets.append(
            {
                "id": d["id"],
                "name": d["name"],
                "organization": d.get("organization", ""),
                "risk_area": d.get("risk_area", ""),
                "license": lic.get("as_observed", "unknown") if isinstance(lic, dict) else str(lic),
                "course_use": ", ".join(
                    [f"ch{c}" for c in (d.get("course_use") or {}).get("chapters", [])]
                    + [p for p in (d.get("course_use") or {}).get("projects", [])]
                ),
                "verified_on": str(d.get("verified_on", "")),
                "card_url": (
                    f"https://github.com/AdilShamim8/AI-Safety"
                    f"/tree/main/datasets/{d.get('card', '')}"
                ),
            }
        )
    chapters = [
        {
            "id": ch["id"],
            "title": ch["title"],
            "phase": ch.get("phase", ""),
            "maturity": ch.get("maturity", ""),
        }
        for ch in matrix["chapters"]
    ]
    headlines = _project_headlines()
    projects = [
        {
            "id": p["id"],
            "title": p["title"],
            "status": p.get("status", ""),
            "package": (
                "src/ai_safety_course/" + p["id"].lower().replace("p", "", 1) + "/"
                if p.get("status") == "implemented"
                and p["id"] in {"P01", "P02", "P03", "P04", "P05", "P07", "P08", "P09"}
                else ""
            ),
            "headline": headlines.get(p["id"], ""),
        }
        for p in matrix["projects"]
    ]
    # Fix package paths for the two that differ from the pXX convention
    pkg_map = {
        "P01": "evaluation",
        "P02": "reward_spec",
        "P03": "calibration",
        "P04": "pref_audit",
        "P05": "w2s_audit",
        "P06": "patch_audit",
        "P07": "agent_guard",
        "P08": "control_protocol",
        "P09": "shift_audit",
        "P10": "assurance",
    }
    for pr in projects:
        pr["package"] = (
            f"src/ai_safety_course/{pkg_map[pr['id']]}/" if pkg_map.get(pr["id"]) else ""
        )

    commits_count, commits_shallow = _commit_count()
    papers, comparisons = _note_counts()
    note_titles = _note_titles()
    incidents = _incidents()
    fs_track = _fs_track()
    # the from-scratch researcher track: tensors, neuron/activations,
    # network, attention, transformer, moe (7 modules)
    fs_modules = 7

    # Source-type distribution for the register widget
    type_counts: dict[str, int] = {}
    for s in sources_raw:
        t = str(s.get("source_type", "other"))
        type_counts[t] = type_counts.get(t, 0) + 1

    # The catalog surfaces parsed from the repo's own documents
    syllabus_rows = _syllabus_rows()
    glossary = _glossary()
    faq = _faq()
    awesome = _awesome()
    schedules = _schedules()
    notes_index = _notes_index()
    chapter_dirs = _dir_names("chapters", "")
    project_dirs = _dir_names("projects", "p")

    # attach the real directory name to each catalog row, so generated
    # links never depend on slugifying a display title
    for row in syllabus_rows:
        row["dir"] = chapter_dirs.get(row["id"], "")
    for pr in projects:
        pr["dir"] = project_dirs.get(pr["id"], "")

    return {
        "repo": {
            "source_types": dict(sorted(type_counts.items(), key=lambda kv: -kv[1])),
            "access_counts": _access_counts(sources_raw),
            "commits": commits_count,
            "shallow": commits_shallow,
            "tests": _test_count(),
            "sources": len(sources),
            "claims": len(claims),
            "datasets": len(datasets),
            "notes": papers + comparisons,
            "paper_notes": papers,
            "comparison_notes": comparisons,
            "note_titles": note_titles,
            "glossary_terms": len(glossary),
            "fs_modules": fs_modules,
            "generated_on": datetime.now(UTC).date().isoformat(),
        },
        "chapters": chapters,
        "chapter_catalog": syllabus_rows,
        "chapter_blocks": [{"block": b, "short": s, "ids": ids} for b, s, ids in CHAPTER_BLOCKS],
        "projects": projects,
        "datasets": datasets,
        "sources": sources,
        "claims": claims,
        "incidents": incidents,
        "incident_eras": INCIDENT_ERAS,
        "not_executed": NOT_EXECUTED,
        "fs_track": fs_track,
        "careers": CAREERS,
        "routes": ROUTES,
        "progress": _progress_trackers(),
        "note_coverage": _note_coverage(),
        "quickstart": QUICKSTART,
        "notes_index": notes_index,
        "glossary": glossary,
        "faq": faq,
        "awesome": awesome,
        "schedules": schedules,
    }


def render(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = template.replace("/*__DATA__*/null", payload)
    if "__DATA__" in html:
        raise SystemExit("template placeholder not replaced correctly")
    return html


def main() -> int:
    data = build_data()
    OUT.write_text(render(data), encoding="utf-8")
    size = OUT.stat().st_size
    print(
        f"index.html written: {size/1024:.0f} KB · "
        f"{data['repo']['sources']} sources, {data['repo']['claims']} claims, "
        f"{data['repo']['datasets']} datasets, {len(data['chapters'])} chapters, "
        f"{len(data['projects'])} projects, {data['repo']['tests']} tests, "
        f"{data['repo']['commits']} commits"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
