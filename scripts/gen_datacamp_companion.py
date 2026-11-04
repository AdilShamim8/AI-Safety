#!/usr/bin/env python3
"""Generate the DataCamp companion layer under
courses/datacamp-ai-security-risk/ (course page, 44 companion notes,
reading map, pedagogy, self-assessment, two crosswalks).

Content source: scripts/datacamp_content.py (chapter 1),
datacamp_content2.py (chapter 2), datacamp_content3.py (chapter 3) —
see those modules for the honesty basis.

Run from the repository root:  uv run python scripts/gen_datacamp_companion.py
Idempotent: regenerates every file it owns; never touches files it
does not own.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from datacamp_content import CH1  # noqa: E402
from datacamp_content2 import CH2  # noqa: E402
from datacamp_content3 import CH3  # noqa: E402

OUT = REPO / "courses" / "datacamp-ai-security-risk"
CATALOG_URL = "https://www.datacamp.com/courses/ai-security-and-risk-management"
APP_URL = "https://app.datacamp.com/learn/courses/ai-security-and-risk-management"
CHAPTERS = [CH1, CH2, CH3]
ALL_LESSONS = [ls for ch in CHAPTERS for ls in ch["lessons"]]

TYPE_LABEL = {"video": "video", "exercise": "interactive exercise", "gamified": "gamified scenario"}
KIND_WORD = {"video": "video", "exercise": "exercise", "gamified": "gamified exercise"}


def honesty_note(kind: str) -> str:
    tail = (
        "No video was streamed by this repository and no interactive "
        "exercise content is reproduced — the interactive lesson is "
        "account-walled; this note prepares the concepts it tests. "
        "Where an idea is also carried by a source this repository "
        "registers, the register ID appears and the source is linked."
    )
    if kind == "video":
        head = (
            "Original study companion written to the lesson's announced "
            "scope. The lesson structure (titles, XP, order) was verified "
            "on the public catalog page 2026-11-03 (SRC-CURR-014); the "
            "video synopsis was supplied by the owner (2026-11-03) and is "
            "treated as the announced scope (SRC-CURR-015). "
        )
    else:
        head = (
            "Original study companion written to the lesson's announced "
            "scope. The lesson structure (titles, XP, order) was verified "
            "on the public catalog page 2026-11-03 (SRC-CURR-014); this "
            "interactive lesson's content is account-walled "
            "(SRC-CURR-015), so the note reconstructs the concepts it "
            "tests from the neighboring videos' announced scopes and the "
            "catalog page's stated chapter purposes. "
        )
    return head + tail


def note_markdown(ch: dict, ls: dict) -> str:
    ideas = (
        "## Core ideas, explained\n"
        if ls["kind"] == "video"
        else "## The concepts this exercise tests\n"
    )
    body = [f"# {ch['number']}.{ls['n']:02d} — {ls['title']}", ""]
    body.append(
        f"*Course companion note · [AI Security and Risk Management](README.md) ·\n"
        f"lesson {ls['n']} of chapter {ch['number']} ({TYPE_LABEL[ls['kind']]}, "
        f"{ls['xp']} XP) · [course page]({APP_URL})*"
    )
    body += ["", "## Where this lesson sits", "", ls["situation"], ""]
    body.append(ideas)
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
    body.append(honesty_note(ls["kind"]))
    return "\n".join(body) + "\n"


def course_page() -> str:
    total_xp = sum(ls["xp"] for ls in ALL_LESSONS)
    videos = sum(1 for ls in ALL_LESSONS if ls["kind"] == "video")
    interactive = sum(1 for ls in ALL_LESSONS if ls["kind"] == "exercise")
    games = sum(1 for ls in ALL_LESSONS if ls["kind"] == "gamified")
    rows = []
    for ch in CHAPTERS:
        rows.append(f"### Chapter {ch['number']} — {ch['title']}")
        rows.append("")
        rows.append(f"*{ch['purpose']}*")
        rows.append("")
        rows.append("| # | Lesson | Type | XP | Companion note |")
        rows.append("|---|---|---|---|---|")
        for ls in ch["lessons"]:
            rows.append(
                f"| {ls['n']} | {ls['title']} | {TYPE_LABEL[ls['kind']]} | "
                f"{ls['xp']} | [{ls['slug']}.md]({ls['slug']}.md) |"
            )
        rows.append("")
    lessons_block = "\n".join(rows)
    return f"""# DataCamp — AI Security and Risk Management

**Navigate:** [← lecture library](../README.md) · [study plans](../study-plans.md) · [previous: Safeshield governance](../safeshield-governance/README.md)

*The interactive-course companion · [catalog page]({CATALOG_URL}) ·
[course page]({APP_URL}) · 3 chapters, 44 lessons ({videos} videos,
{interactive} interactive exercises, {games} gamified scenarios),
{total_xp} XP, about 1 hour median completion, beginner level with no
prerequisites · structure verified on the public catalog page 2026-11-03*

## What this course is

This is Angeline Corvaglia's course for DataCamp (with collaborators
Joe Franklin and Jordan Beecher) — the fifth course in this repository's
lecture library, and the one that differs from the other four in kind:
not a lecture series but an **interactive-exercise course**, where every
concept is introduced in a short video and then immediately graded —
recall drills, discriminations, and gamified scenario games (Riskland
Junction, Security Catalyst Station, Model Risk Abyss, Perimeter Peril
Point, Fortified Code Forge, Assessment Framework Enclave, General
Landora Implementor, Alignment Avenue, Culture Citadel, Throne of
Stagnation). It is also the library's only **beginner,
no-prerequisites** course: no mathematics, no programming, no ML
background assumed — the register the other four courses skip entirely.

Its distinct evidential value in this library is therefore twofold.
First, it teaches the **operational and strategic layers** the video
courses gesture at but never grade: the security-operations tool
families (anomaly detection/UEBA, TIPs, SOAR, SIEM), the seven model
risks over the lifecycle, the five external-attack groups, the four
data-protection practices, the EU AI Act's risk tiers, threat
prioritization and risk appetite, the security-aware culture's role
map, and the forward-looking set (regulation, synthetic data, AGI).
Second, it teaches all of it in the **judgment format** — every
exercise scores a decision, not a recital — which is the pedagogy this
repository's own exercises adopt at greater depth.

## The three-chapter arc

The structure moves from landscape to operations to strategy — each
chapter turning outward one more layer:

1. **AI's Security Landscape** — the five AI-specific risks, AI as a
   change agent FOR security, and the four-pillar ecosystem (people,
   legal, technology, processes).
2. **Risk Management Fundamentals** — the seven model risks, the five
   external-attack groups, the secure-development practices, and the
   formal-plus-continuous assessment posture anchored in the EU AI
   Act's risk tiers.
3. **Strategic Integration of AI Security** — threat prioritization,
   risk appetite, the innovation–security spectrum, the
   start-up-versus-bank alignment contrast, the security-aware
   culture's role map, and the forward-looking set.

## The complete lesson index

{lessons_block}
## How the course organizes knowledge

*The deep-dive version is [pedagogy.md](pedagogy.md).*

The course teaches in **graded layers** (video claim → drill → game),
each layer at a fixed XP price, and it is the only course in this
library whose claims about your learning are backed by a score it
actually assigns. Its signature move is the **gamified scenario**: ten
named games, each the capstone of its chapter-half, where the graded
unit is judgment under constraints. Its risk teaching runs on the
**phase discriminator** (training-time versus inference-time versus
data-handling), the same boundary this repository's chapters 12 and 16
draw — stated here at the level a first-week beginner can hold.

## Mapping to this repository's chapters

| Course chapter | Repository chapters | Why |
|---|---|---|
| 1 — landscape (five risks, AI-for-security, ecosystem) | [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md), [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md), [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md), [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) | the five-risk taxonomy with full epistemic care; the attack surfaces; the data layer; the systemic frame |
| 2 — fundamentals (model risks, external risks, practices, assessment) | [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md), [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md), [Ch. 13](../../chapters/13-llm-application-security/README.md), [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md), [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md), [Ch. 23](../../chapters/23-governance-and-standards/README.md) | evaluation science; interpretability; the application surface; drift and monitoring; assurance; the EU AI Act in full |
| 3 — strategy (prioritization, appetite, culture, future) | [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md), [Ch. 22](../../chapters/22-safety-engineering-and-assurance/README.md), [Ch. 23](../../chapters/23-governance-and-standards/README.md), [Ch. 24](../../chapters/24-research-practice-and-capstone-execution/README.md) | the sociotechnical layer; safety culture; governance instruments; where the survey courses send you next |

The per-lesson mapping (every one of the 44 notes carries its own
through-lines) is tabulated in [crosswalk-chapters.md](crosswalk-chapters.md);
the glossary terms the course prompted are tabulated in
[crosswalk-glossary.md](crosswalk-glossary.md).

## Register entries and access levels

- **[SRC-CURR-014]** — the [public catalog page]({CATALOG_URL})
  (page-inspected 2026-11-03: title, instructor and collaborators,
  beginner level, no prerequisites, 3 chapters / 44 lessons with XP,
  schema durations, rating, enrollment count, publication date, and
  track placements, all as rendered).
- **[SRC-CURR-015]** — the [course page]({APP_URL}) (metadata-only:
  unauthenticated fetch redirects to sign-in, recorded 2026-11-03; the
  lesson-level structure was supplied by the owner from account access
  and corroborated by the catalog page's schema positions).

No interactive exercise was opened by this repository; no exercise
content is reproduced anywhere. The companion notes are original
explanations of each lesson's announced scope: the video synopses were
supplied by the owner (2026-11-03) and are treated as the announced
scope; exercise notes reconstruct the concepts the exercise tests from
the neighboring videos' scopes. No video was streamed.

## The companion set (complete)

All 44 lessons are covered — every video, every exercise, every game —
plus the pedagogy analysis, the reading map, the self-assessment, and
two crosswalks. The course's own stated follow-ons (AI Ethics, AI
Strategy, XAI Concepts, Introduction to Data Security) are recorded in
the [wrap-up note](ch03-17-wrap-up-ai-security-and-risk-management.md);
the deeper ladder each of them points toward is this repository's
chapter spine.
"""


def reading_map() -> str:
    return """# The DataCamp course × this repository's spine

**Navigate:** [← the DataCamp companion](README.md) · [pedagogy](pedagogy.md) · [self-assessment](self-assessment.md)

*Part of the [DataCamp companion](README.md) · 2026-11-03*

| Course chapter | The repo's depth layer |
|---|---|
| 1 — the five risks, AI-for-security, the ecosystem | Ch. 01 (the taxonomy with full epistemic care), Ch. 12 (the attack surfaces), Ch. 21 (the systemic frame) |
| 2 — model risks, external risks, practices, assessment | Ch. 02 (evaluation science: leakage, overfitting), Ch. 17 (drift and monitoring), Ch. 16 (the data-protection practices), Ch. 23 (the EU AI Act in full) |
| 3 — strategy, culture, the future set | Ch. 22 (safety culture, prioritization under budget), Ch. 23 (risk appetite as an instrument), Ch. 21 (the sociotechnical layer) |

The course (registered SRC-CURR-014/015) is the graded beginner
on-ramp; this repository is the working complement — the same arc with
exercises that execute and evidence the register can audit. The
per-lesson mapping is [crosswalk-chapters.md](crosswalk-chapters.md).
"""


def pedagogy() -> str:
    return """# How the DataCamp course organizes knowledge

**Navigate:** [← the DataCamp companion](README.md) · [reading map](reading-map.md) · [self-assessment](self-assessment.md)

*A pedagogy analysis · part of the [DataCamp companion](README.md) ·
written 2026-11-03 from the verified course structure*

## The question this note answers

The lecture library's index asks of every course: how does it gather,
organize, and manage information? This course's answer is unique in the
library, so it earns its own analysis.

## The exercise-graded architecture

| Axis | The DataCamp course |
|---|---|
| Unit of instruction | the single graded item (video claim → drill → game) |
| Core artifact | short videos plus an XP-priced exercise bank, half of it gamified scenarios |
| Evidence discipline | every claim about your learning is backed by a score the platform assigns |
| Time cost | about 1 hour median completion (2 hours by schema) |
| Who it is for | absolute beginners — no prerequisites, the register every other course skips |
| What only it does | grades judgment at beginner level: ten scenario games where the scored unit is a decision |

## What the architecture chooses to believe

**The course bets on the graded loop.** Concepts arrive in short
videos, then every concept is immediately scored — first as
discrimination drills (which risk is this? which practice fits that?),
then as scenario games where the score is a decision's outcome
(Riskland Junction, Model Risk Abyss, Throne of Stagnation). The bet
is that judgment, not recall, is the transferable unit — and the
course spends its whole budget on it.

**The phase discriminator is the load-bearing idea.** Across chapters,
the same boundary does the sorting work: training-time versus
inference-time versus data-handling (poisoning versus adversarial
input; validation versus encryption; drift versus hallucination). The
course states it in plain words where this repository's chapters 12
and 16 draw it in full depth — the two registers agree, which is why
the mapping tables pair them.

**The strategy chapter is the course's own bet.** Chapter 3 —
prioritization under budget, risk appetite, the
start-up-versus-bank contrast, the culture role map — is material no
other course in the library teaches at all, and it is where the
course most clearly earns its place: the layer where security becomes
an instrument of the organization's strategy rather than its cost.

## What this repository took from it

The graded-loop discipline for its own exercises; the phase
discriminator as the beginner's first sorting key (now stated in the
glossary rows the crosswalk records); the strategic layer as a
teachable subject with its own glossary; and the ten scenario games as
the pattern its capstone exercises approximate at greater depth.
"""


def self_assessment() -> str:
    return """# Self-assessment — the DataCamp course

**Navigate:** [← the DataCamp companion](README.md) · [reading map](reading-map.md) · [pedagogy](pedagogy.md)

Ten judgment questions. Answer from the course and its companion
notes; every question names the lesson that teaches it and the
repository chapter that deepens it.

1. An AI hiring system trained on ten years of historical decisions
   reproduces the biases of those decisions. Which of the five
   AI-specific risks is this, what phase does the fault enter
   through, and which chapter of this repository owns the deep
   treatment? *(lesson 1.01; Ch. 01, Ch. 21)*
2. A recommender misleads users after attackers seeded fake profiles.
   Data poisoning or adversarial input — and what distinguishes the
   two families? *(lessons 1.01–1.03, 2.05–2.06; Ch. 12, Ch. 16)*
3. Your security operations center drowns in event data. Which of the
   four tool families (anomaly detection/UEBA, TIP, SOAR, SIEM) do you
   reach for, and what does each family analyze? *(lesson 1.04–1.05;
   Ch. 08)*
4. A model scores brilliantly on held-out data and disappoints in
   production three months later. Name the two candidate risks and the
   observation that separates them. *(lessons 2.01–2.04; Ch. 02,
   Ch. 17)*
5. Validation accuracy looks too good to be true and cannot be
   reproduced independently. What happened, and which evaluation
   discipline prevents it? *(lessons 2.01–2.02; Ch. 02)*
6. Attackers reconstruct training images from a facial-recognition
   model's outputs. Which external-attack group is this, and which two
   practices counter it? *(lessons 2.05, 2.09; Ch. 16)*
7. A system screens job applicants. Under the EU AI Act's four tiers,
   how do you classify it, and what obligation follows? *(lessons
   2.13–2.14; Ch. 23)*
8. A startup and a bank adopt the same AI security tooling. Explain
   the different postures, naming the determinants of risk appetite.
   *(lessons 3.01–3.05, 3.07; Ch. 23)*
9. Who in an organization catches model drift — and who catches a
   compliance gap, an insider threat, and a trust complaint? *(lesson
   3.09–3.10; Ch. 21, Ch. 22)*
10. Regulation shifts, synthetic data arrives, AGI is debated. Which
    posture keeps security effective through all three, and what is
    its cost? *(lessons 3.13–3.16; Ch. 22, Ch. 23)*

Scoring: eight or more with the phase or determinant named — you
carried the course's judgment layer. Fewer — re-run the chapter's
games; the notes are the map back.
"""


def crosswalk_chapters() -> str:
    lines = [
        "# The DataCamp lessons × this repository's chapters",
        "",
        "**Navigate:** [← the DataCamp companion](README.md) · [crosswalk: glossary](crosswalk-glossary.md)",
        "",
        "*Part of the [DataCamp companion](README.md) · 2026-11-03 · every",
        "through-line stated in a companion note, tabulated here for",
        "either-direction lookup.*",
        "",
    ]
    for ch in CHAPTERS:
        lines.append(f"## Chapter {ch['number']} — {ch['title']}")
        lines.append("")
        lines.append("| Lesson | Repository chapters |")
        lines.append("|---|---|")
        for ls in ch["lessons"]:
            refs = ", ".join(f"[{label}]({relpath})" for relpath, label, _ in ls["throughlines"])
            lines.append(f"| {ls['n']}. {ls['title']} | {refs} |")
        lines.append("")
    return "\n".join(lines)


def crosswalk_glossary() -> str:
    rows = [
        (
            "SIEM",
            "Security information and event management — real-time event data analyzed to identify anomalies, find patterns, flag incidents; AI adds detection speed and prediction.",
            "1.04",
            "12, 14",
        ),
        (
            "SOAR",
            "Security orchestration, automation, and response — AI streamlines and synchronizes security tasks across systems so experts focus on sophisticated threats.",
            "1.04",
            "12, 14",
        ),
        (
            "UEBA",
            "User and entity behavior analytics — AI studies patterns of user behavior to find irregularities: compromised accounts, insider risks.",
            "1.04",
            "12, 14",
        ),
        (
            "Threat intelligence platform (TIP)",
            "AI-powered analysis of threat intelligence data — the who, why, how, and what-next of potential threats.",
            "1.04",
            "12, 14",
        ),
        (
            "Underfitting",
            "A model too simple to learn the underlying patterns of the data — poor everywhere, including the training set.",
            "2.01",
            "02, 12",
        ),
        (
            "Data leakage",
            "Outside data mistakenly included in the training set — inflates validation scores, disappoints in production.",
            "2.01",
            "02, 12",
        ),
        (
            "Model transparency",
            "The inner workings of a model being accessible and clear to those who use it.",
            "2.01",
            "09, 02",
        ),
        (
            "Model interpretability",
            "People being able to understand why a model produces certain outputs from specific inputs.",
            "2.01",
            "09, 02",
        ),
        (
            "Explainable AI (XAI)",
            "Methods that make models more understandable and transparent to humans — clear explanations of the reasoning behind outputs.",
            "2.01",
            "09, 22",
        ),
        (
            "Continuous monitoring (lifecycle)",
            "Post-deployment watching for drift, bias emergence, and unexpected behavior — the early-warning system.",
            "2.01, 2.03",
            "17, 22",
        ),
        (
            "Data validation",
            "Checking and cleaning data before it is fed to an AI system — accurate, relevant, free from malicious tampering.",
            "2.09",
            "12, 16",
        ),
        (
            "Data minimization",
            "Limiting collection and processing to only what is absolutely necessary — significantly reduces privacy-breach and data-theft risk.",
            "2.09",
            "16",
        ),
        (
            "Anonymization",
            "Removing personally identifiable information from datasets — protecting against model inversion attacks.",
            "2.09",
            "16",
        ),
        (
            "Data provenance and traceability",
            "Understanding the origin of data and tracking its journey through the AI system — the anti-poisoning practice.",
            "2.09",
            "16, 22",
        ),
        (
            "Model inversion attack",
            "Exploiting a model to access or reconstruct its confidential training data.",
            "2.05, 2.09",
            "16, 12",
        ),
        (
            "Supply chain attack (AI)",
            "A vulnerability injected into a widely used AI library or component — present in every system built on it.",
            "2.05",
            "16, 14",
        ),
        (
            "Threat prioritization",
            "Ranking risks by potential severity and probability — the risk matrix's format for resource allocation.",
            "3.01",
            "22, 01",
        ),
        (
            "Low-hanging fruit (mitigation)",
            "Actions implementable quickly that significantly reduce risk — the first wave that shows progress and boosts morale.",
            "3.01",
            "22",
        ),
        (
            "Security-aware culture",
            "An environment where employees recognize the importance of protecting data and understand their role in safeguarding digital assets.",
            "3.09",
            "22, 23",
        ),
        (
            "Synthetic data",
            "Artificial data sets that resemble real-world information without personal details or others' intellectual property — new integrity challenges.",
            "3.13",
            "16, 23",
        ),
    ]
    lines = [
        "# The DataCamp course × the glossary",
        "",
        "**Navigate:** [← the DataCamp companion](README.md) · [crosswalk: chapters](crosswalk-chapters.md)",
        "",
        "*Part of the [DataCamp companion](README.md) · 2026-11-03 · the 20",
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
    # self-check: unique slugs, resolvable through-line targets
    slugs = [ls["slug"] for ls in ALL_LESSONS]
    assert len(slugs) == len(set(slugs)) == 44, "slug set is wrong"
    assert sum(ls["xp"] for ls in ALL_LESSONS) == 2750, "XP total drifted"
    for ls in ALL_LESSONS:
        for relpath, _label, _why in ls["throughlines"]:
            # through-lines are written from the notes' location (the course
            # directory), and verified there
            assert (OUT / relpath).exists(), f"{ls['slug']}: bad through-line {relpath}"
    written = []
    (OUT / "README.md").write_text(course_page(), encoding="utf-8")
    written.append("README.md")
    for ch in CHAPTERS:
        for ls in ch["lessons"]:
            p = OUT / f"{ls['slug']}.md"
            p.write_text(note_markdown(ch, ls), encoding="utf-8")
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
    print(f"datacamp companion: {len(written)} files written to {OUT}")


if __name__ == "__main__":
    main()
