#!/usr/bin/env python3
"""Generate the CampusX companion layer under
courses/campusx-ai-security-guardrails/ (course page, 14 companion
notes, reading map, pedagogy, self-assessment, two crosswalks).

Content source: scripts/campusx_content.py (module 1),
campusx_content2.py (module 2), campusx_content3.py (module 3 — the
NovaBank case study), campusx_content4.py (module 4 — the agent case
study). See those modules for the honesty basis (published course
description and outline, both public; no video watched; nothing
behind the paywall reproduced).

Run from the repository root:
  uv run python scripts/gen_campusx_companion.py
Idempotent: regenerates every file it owns.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from campusx_content import CM1  # noqa: E402
from campusx_content2 import CM2  # noqa: E402
from campusx_content3 import CM3  # noqa: E402
from campusx_content4 import CM4  # noqa: E402

OUT = REPO / "courses" / "campusx-ai-security-guardrails"
COURSE_URL = "https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053"
PREVIEW_URL = "https://learnwith.campusx.in/s/preview/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053-6ad0c6fb17f468ce3c894053"
MODULES = [CM1, CM2, CM3, CM4]
ALL_LESSONS = [ls for m in MODULES for ls in m["lessons"]]
TOTAL_MINUTES = round(sum(ls["minutes"] for ls in ALL_LESSONS), 2)
PUBLISHED = [ls for ls in ALL_LESSONS if ls["minutes"] > 0]


def honesty_note(ls: dict) -> str:
    unpublished = (
        "This lesson is listed with duration 0 on the course page — "
        "announced in the outline, not yet published at verification "
        "time. The note is written to the case study's announced scope, "
        "which the course's published description states in full; the "
        "recording was not available to check against. "
        if ls["minutes"] == 0
        else ""
    )
    return (
        f"{unpublished}"
        "Original study companion written to the lesson's announced "
        "scope. The course page (public, no login; its outline is marked "
        "TENTATIVE by the platform itself) was fetched and read in full on "
        "2026-11-03 and is registered as SRC-CURR-016; the lesson titles, "
        "order, and durations are taken from its published curriculum "
        "data, and the teaching beats are grounded in the page's own "
        "published description. No video was watched by this repository, "
        "nothing behind the paywall is reproduced, and no lesson content "
        "beyond the page is transcribed. Where an idea is also carried by "
        "a source this repository registers, the register ID appears and "
        "the source is linked."
    )


def fmt_minutes(m: float) -> str:
    if m == 0:
        return "announced"
    whole = int(m)
    sec = int(round((m - whole) * 60))
    return f"{whole}:{sec:02d}"


def note_markdown(ls: dict) -> str:
    body = [f"# {ls['title']}", ""]
    dur = fmt_minutes(ls["minutes"])
    body.append(
        f"*Course companion note · [AI Security & Guardrails](README.md) ·\n"
        f"module {ls['module']} lesson {ls['n']} ({dur}) · "
        f"[course page]({COURSE_URL})*"
    )
    body += ["", "## Where this lesson sits", "", ls["situation"], ""]
    body.append("## Core ideas, explained")
    body.append("")
    for i, (heading, text) in enumerate(ls["beats"], 1):
        body.append(f"### {i}. {heading}")
        body.append("")
        body.append(text)
        body.append("")
    body.append("## Through-lines to this repository's chapters")
    body.append("")
    for relpath, label, why in ls["throughlines"]:
        body.append(f"- [{label}]({relpath}) — {why}")
    body.append("")
    body.append("## What only this course does")
    body.append("")
    body.append(ls["angle"])
    body.append("")
    body.append("## Honesty note")
    body.append("")
    body.append(honesty_note(ls))
    return "\n".join(body) + "\n"


def course_page() -> str:
    rows = []
    for m in MODULES:
        rows.append(f"### Module {m['number']} — {m['title']}")
        rows.append("")
        rows.append("| # | Lesson | Duration | Companion note |")
        rows.append("|---|---|---|---|")
        for ls in m["lessons"]:
            rows.append(
                f"| {ls['n']} | {ls['title']} | {fmt_minutes(ls['minutes'])} | "
                f"[{ls['slug']}.md]({ls['slug']}.md) |"
            )
        rows.append("")
    lessons_block = "\n".join(rows)
    published_min = round(sum(ls["minutes"] for ls in PUBLISHED), 2)
    return f"""# CampusX — AI Security & Guardrails

**Navigate:** [← lecture library](../README.md) · [study plans](../study-plans.md) · [previous: DataCamp](../datacamp-ai-security-risk/README.md)

*The guardrails-engineering companion · [course page]({COURSE_URL}) ·
[preview]({PREVIEW_URL}) · 4 modules, 14 lessons (13 with published
durations totaling {published_min} minutes, 1 announced with duration
0), the outline marked TENTATIVE by the platform itself · verified
2026-11-03*

## What this course is

This is CampusX's practitioner course (Hinglish, paid — ₹1999 against
an MRP of ₹2499, 1095-day validity), and the sixth course in this
repository's lecture library. Where the five courses before it teach
the risk landscape and the concepts, this one builds the defenses:
two production-grade case studies secured layer by layer, end to end,
with the same repeatable five-step threat-modelling framework.

Its distinct evidential value in this library: it is the only course
that treats **guardrails engineering** as a construction discipline —
every component in a data flow examined through the capability lens
(what it can read, write, execute, or reach), every weak point closed
with its own named security layer, and the secured result red-teamed
with Promptfoo to grade which layers hold. The case studies are a
bank RAG (NovaBank — a RAG that works is not yet safe for a bank) and
a doctor-booking agent with tools, an MCP server, shared memory, and
no login (write and delete capabilities make an agent more dangerous
than a RAG: an attack no longer just changes an answer, it makes the
agent take real actions).

## The four-module arc

The structure runs from thesis to framework to two applications:

1. **Why Study AI Security?** — the thesis: applications built without
   security in mind are open to attack, and every added retriever,
   tool, and input channel is a new way in.
2. **AI Security & Challenges** — the structural differences from
   application security, the attack catalog, the toolbox, and the
   five-step threat-modelling framework.
3. **Threat Modelling our RAG Application** — the NovaBank case study:
   PII masking, pre-retrieval metadata filtering, input guardrails
   and delimiter defense, NeMo Guardrails output guardrails, and the
   Promptfoo red-team close.
4. **Threat Modelling our Agentic Application** — the doctor-booking
   agent: the jailbreak gate, the guard model on tool and MCP
   results, memory protection, and output guardrails.

## The complete lesson index

{lessons_block}
## How the course organizes knowledge

*The deep-dive version is [pedagogy.md](pedagogy.md).*

The course teaches in **built layers** (thesis → instrument → case
study → red-team grade), each layer named and assigned to a weak
point found in the diagram. Its signature instrument is the
**capability lens** — read, write, execute, reach — which prices
every component before any defense is chosen. Its evidence style is
**demos first**: every attack is shown working on the unsecured
application before the layer that closes it is built.

## Mapping to this repository's chapters

| Course module | Repository layers | Why |
|---|---|---|
| 1 — why study AI security | [Ch. 13](../../chapters/13-llm-application-security/README.md), [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) | exposure as a quantity; the application-security chapter |
| 2 — challenges, tools, framework | [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md), [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md), [templates/threat-model.md](../../templates/threat-model.md) | the attack catalog; the red-team discipline; the repository's own form |
| 3 — the RAG case study | [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md), [Ch. 13](../../chapters/13-llm-application-security/README.md), [P07](../../projects/p07-injection-defense/README.md) | the data protections; the injection defenses; the runnable project |
| 4 — the agent case study | [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md), [P08](../../projects/p08-control-and-monitoring-protocol/README.md) | tools, memory, MCP; the control-and-monitoring project |

The per-lesson mapping is tabulated in
[crosswalk-chapters.md](crosswalk-chapters.md); the 14 glossary terms
the course prompted are tabulated in
[crosswalk-glossary.md](crosswalk-glossary.md).

## Register entry and access level

- **[SRC-CURR-016]** — the [course page]({COURSE_URL}) (page-inspected
  2026-11-03: title, instructor, language, pricing with MRP, validity,
  sales count, the full published description, and the complete
  curriculum data with per-lesson durations — the outline itself
  marked TENTATIVE by the platform).

The course is paid and its lesson videos sit behind the paywall; no
video was watched and nothing behind the paywall is reproduced. The
companion notes are grounded in the page's own published description
and curriculum — the announced scope — and say so in every note's
honesty section.
"""


def reading_map() -> str:
    return """# The CampusX course × this repository's spine

**Navigate:** [← the CampusX companion](README.md) · [pedagogy](pedagogy.md) · [self-assessment](self-assessment.md)

*Part of the [CampusX companion](README.md) · 2026-11-03*

| Course module | The repo's depth layer |
|---|---|
| 1 — why study AI security | Ch. 01 (exposure and pathway), Ch. 13 (the application surface) |
| 2 — attacks, tools, framework | Ch. 12 (the attack families), Ch. 15 (red teaming), the threat-model template |
| 3 — the RAG case study | Ch. 16 (PII, masking, access rules), Ch. 13 (injection defenses), the P07 project |
| 4 — the agent case study | Ch. 14 (tools, memory, MCP), the P08 project |

The course (registered SRC-CURR-016) is the build layer — the same
arc with every defense implemented and red-teamed; this repository is
the depth complement. The per-lesson mapping is
[crosswalk-chapters.md](crosswalk-chapters.md).
"""


def pedagogy() -> str:
    return """# How the CampusX course organizes knowledge

**Navigate:** [← the CampusX companion](README.md) · [reading map](reading-map.md)

*A pedagogy analysis · part of the [CampusX companion](README.md) ·
written 2026-11-03 from the verified course page*

## The question this note answers

How does the course gather, organize, and manage information — the
question the lecture library's index asks of every course. This one's
answer is unique in the library: it teaches security as construction.

## The capability-lens architecture

| Axis | The CampusX course |
|---|---|
| Unit of instruction | one component of a data flow, priced and closed |
| Core artifact | Data Flow Diagrams + the capability table + one named layer per weak point |
| Evidence discipline | demos first: every attack shown working before its defense is built |
| Case studies | two production-grade systems (a bank RAG; a doctor-booking agent) |
| The grade | a Promptfoo red-team pass on the secured stack, per layer |
| Who it is for | practitioners who can build RAG and agents and need the security half |
| What only it does | guardrails engineering as a construction discipline, layer by layer |

## What the architecture chooses to believe

**The course bets on the framework over the anecdote.** Security work
without the five-step method fixes the attack you happened to see;
with it, every component is visited, every capability priced, every
weak point closed. The bet is that methodical beats clever — and the
red-team grade at the end is there to prove the method held.

**The capability lens is the load-bearing idea.** Read, write,
execute, reach: the four verbs that turn a diagram into a risk list.
The lens explains the course's central claim — why an agent (write
and delete) is more dangerous than a RAG (read and answer) — and it
is the same instrument this repository's threat-model template asks
for, which is why the pairing works.

**Demos first is an honesty device.** Every attack is shown working on
the unsecured application before the layer that closes it is built.
The course never asserts a defense works; it runs the attack, builds
the layer, and red-teams the result. That is the same evidence
discipline this repository's evaluation chapters enforce.

## What this repository took from it

The per-component capability framing (now in the glossary as its own
row); the pre-retrieval versus post-retrieval filtering distinction;
the conversation-level jailbreak gate as a design pattern; the
per-layer red-team report as the output of a security review; and the
two case studies as the working exemplars the chapters and projects
point to.
"""


def self_assessment() -> str:
    return """# Self-assessment — the CampusX course

**Navigate:** [← the CampusX companion](README.md) · [reading map](reading-map.md) · [pedagogy](pedagogy.md)

Ten judgment questions. Answer from the course and its companion
notes; every question names the lesson that teaches it and the
repository layer that deepens it.

1. Your RAG answers every demo query correctly. Name the thesis that
   says it is not yet safe for a bank, and the instrument that finds
   out. *(module 1 and 3.01; Ch. 01, Ch. 13)*
2. State the three structural differences from application security,
   and say which defense in the toolbox answers each one. *(module
   1.02 and 2.03; Ch. 13)*
3. Walk the five-step framework on any LLM application you have built
   — diagram, boundaries, capability table, weak points, layers.
   *(module 2.04; templates/threat-model.md)*
4. Why does the vector database leak PII, and what is the layer that
   closes it — and where in the pipeline does that layer sit? *(module
   3.02; Ch. 16)*
5. Pre-retrieval metadata filtering versus post-retrieval filtering:
   which does the course build, and why does the other leak? *(module
   3.03; Ch. 13, Ch. 14)*
6. The user query and the retrieved documents are two different
   channels. Name the defense for each, and the attack each one
   closes. *(module 3.04; Ch. 12, Ch. 13)*
7. What three things does the output guardrail check every answer
   for, and why is the check per-answer rather than per-release?
   *(module 3.05; Ch. 08, Ch. 22)*
8. Why is an agent with write and delete more dangerous than a RAG?
   Give the lens answer and the case-study examples. *(module 4.01;
   Ch. 14)*
9. The jailbreak gate reads every message with recent turns inside
   delimiters. Name the three block categories and why the gate is a
   separate model. *(module 4.02; Ch. 14, Ch. 15)*
10. What does the Promptfoo red-team pass actually grade, and why is
    the per-layer report the finding rather than a pass/fail?
    *(module 3.06; Ch. 02, Ch. 15, P07)*

Scoring: eight or more with the lens or the layer named — you carried
the method. Fewer — re-run the case studies' lessons; the notes are
the map back.
"""


def crosswalk_chapters() -> str:
    lines = [
        "# The CampusX lessons × this repository's layers",
        "",
        "**Navigate:** [← the CampusX companion](README.md) · [crosswalk: glossary](crosswalk-glossary.md)",
        "",
        "*Part of the [CampusX companion](README.md) · 2026-11-03 · every",
        "through-line stated in a companion note, tabulated here for",
        "either-direction lookup.*",
        "",
    ]
    for m in MODULES:
        lines.append(f"## Module {m['number']} — {m['title']}")
        lines.append("")
        lines.append("| Lesson | Repository layers |")
        lines.append("|---|---|")
        for ls in m["lessons"]:
            refs = ", ".join(f"[{label}]({relpath})" for relpath, label, _ in ls["throughlines"])
            lines.append(f"| {ls['n']}. {ls['title']} | {refs} |")
        lines.append("")
    return "\n".join(lines)


def crosswalk_glossary() -> str:
    rows = [
        (
            "Guardrails (LLM applications)",
            "The engineering layers placed around an LLM application's channels — input, retrieval, prompt, tool, memory, output — each closing a named attack; the construction discipline of securing component by component.",
            "all modules",
            "13, 14, 22",
        ),
        (
            "Input guardrails",
            "The gate on the user-query channel that stops jailbreaks before the query reaches the retriever or the LLM.",
            "3.04",
            "13, 12",
        ),
        (
            "Output guardrails",
            "The last-check layer on the answer channel — every answer checked for private data, wrong facts, or a manipulated response before it reaches the user; built with NVIDIA NeMo Guardrails in the course.",
            "3.05",
            "13, 08",
        ),
        (
            "Guard model",
            "A separate model that reads traffic and blocks by rule — on the conversation (the jailbreak gate) or on every tool and MCP result — so the defense does not share the protected model's context.",
            "4.01, 4.02",
            "14, 08",
        ),
        (
            "PII masking",
            "Detection and redaction/tokenization of personal identifiers in the ingestion path, so customers' personal data never reaches the vector database.",
            "3.02",
            "16",
        ),
        (
            "Pre-retrieval metadata filtering",
            "Authorization enforced as metadata filtering that blocks restricted documents BEFORE the search runs — the search never touches what the requester may not see.",
            "3.03",
            "13, 14",
        ),
        (
            "Delimiter defense",
            "Retrieved documents delivered inside explicit boundaries with a system prompt that treats them as data, never instructions — the defense against injection from retrieved content.",
            "3.04",
            "13, 14",
        ),
        (
            "Data Flow Diagram (DFD)",
            "The map of an LLM application's components and flows — every entry and exit point and trust boundary — the first step of the threat-modelling framework.",
            "2.04, 3.01",
            "13, 01",
        ),
        (
            "Capability table",
            "The instrument that prices every component by what it can read, write, execute, or reach — turning a diagram into a risk list.",
            "2.04, 3.01",
            "14, 01",
        ),
        (
            "Jailbreak gate",
            "The conversation-level guard: a separate model reading every message with recent turns inside delimiters, blocking authority claims, other people's data, and rule-override attempts.",
            "4.02",
            "14, 12",
        ),
        (
            "Trust boundary",
            "A line in the diagram where data crosses between levels of trust — the boundaries the framework draws before any weak point is named.",
            "2.04, 3.01",
            "13, 16",
        ),
        (
            "Shared memory (agent)",
            "The agent's cross-session store of past conversations — a write surface: personal data and poisoned lessons must never reach it, which is why a judge checks every write.",
            "4.01",
            "14",
        ),
        (
            "Promptfoo",
            "The open-source red-team harness the course uses to grade the secured stack — attack prompts as cases, the security layers as the code under test, results as a per-layer report.",
            "3.06",
            "15, 02",
        ),
        (
            "Multimodal attack surface",
            "Images, files, and other non-text inputs as attack paths that text-only defenses miss — every input channel added is a new way in.",
            "1.01, 1.02",
            "19, 13",
        ),
    ]
    lines = [
        "# The CampusX course × the glossary",
        "",
        "**Navigate:** [← the CampusX companion](README.md) · [crosswalk: chapters](crosswalk-chapters.md)",
        "",
        "*Part of the [CampusX companion](README.md) · 2026-11-03 · the 14",
        "terms the course prompted, each now carried as a row in",
        "[GLOSSARY.md](../../GLOSSARY.md) with the chapters that use it.*",
        "",
        "| Term | One-line meaning | Taught in lesson | Glossary chapters |",
        "|---|---|---|---|",
    ]
    for term, meaning, lesson, chapters in rows:
        lines.append(f"| **{term}** | {meaning} | {lesson} | {chapters} |")
    lines += [
        "",
        "The glossary rows carry the full definitions with aliases,",
        "common confusions, and chapter mappings; this table is the",
        "course-to-glossary index.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    slugs = [ls["slug"] for ls in ALL_LESSONS]
    assert len(slugs) == len(set(slugs)) == 14, "slug set is wrong"
    assert len(PUBLISHED) == 13, "published-lesson count drifted"
    assert abs(TOTAL_MINUTES - 330.47) < 0.02, f"total minutes drifted: {TOTAL_MINUTES}"
    for ls in ALL_LESSONS:
        for relpath, _label, _why in ls["throughlines"]:
            assert (OUT / relpath).exists(), f"{ls['slug']}: bad through-line {relpath}"
    written = []
    (OUT / "README.md").write_text(course_page(), encoding="utf-8")
    written.append("README.md")
    for ls in ALL_LESSONS:
        p = OUT / f"{ls['slug']}.md"
        p.write_text(note_markdown(ls), encoding="utf-8")
        written.append(p.name)
    for name, text in (
        ("reading-map.md", reading_map()),
        ("pedagogy.md", pedagogy()),
        ("self-assessment.md", self_assessment()),
        ("crosswalk-chapters.md", crosswalk_chapters()),
        ("crosswalk-glossary.md", crosswalk_glossary()),
    ):
        (OUT / name).write_text(text, encoding="utf-8")
        written.append(name)
    print(f"campusx companion: {len(written)} files written to {OUT}")


if __name__ == "__main__":
    main()
