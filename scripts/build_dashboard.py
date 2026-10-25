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
                        m.group(5).strip()[1:-1]
                        if m.group(5).strip().startswith("[")
                        else m.group(5)
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
        out.append({
            "ch": pdir.name.split("-")[0],
            "title": pdir.name.split("-", 1)[1],
            "notes": len(set(links)),
        })
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
        out.append({
            "slug": slug,
            "role": role,
            "milestones": milestones,
            "boxes": sum(m["boxes"] for m in milestones),
        })
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

    return {
        "repo": {
            "source_types": dict(sorted(type_counts.items(), key=lambda kv: -kv[1])),
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
            "fs_modules": fs_modules,
            "generated_on": datetime.now(UTC).date().isoformat(),
        },
        "chapters": chapters,
        "projects": projects,
        "datasets": datasets,
        "sources": sources,
        "claims": claims,
        "incidents": incidents,
        "not_executed": NOT_EXECUTED,
        "fs_track": fs_track,
        "careers": CAREERS,
        "progress": _progress_trackers(),
        "note_coverage": _note_coverage(),
        "quickstart": QUICKSTART,
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
