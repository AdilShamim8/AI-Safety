# The lecture library — four courses, one method

*Part of [AI Safety](../README.md) · opened 2026-10-27 · the video-course
companions layer of the [resource index](../AWESOME.md)*

## What this layer is

The repository's spine is its own 24-chapter course. This directory adds
the four external courses the owner selected on 2026-10-27, each
transmitted as a YouTube playlist, each turned into the same three
artifacts: a **course page** (identity, structure, and the complete video
index with verified links), **companion notes** for every lecture (one
file per video), and — where the course publishes one — a **reading map**
that connects the course's own reading list to this repository's paper
spine, chapters, and register entries.

The four courses were not chosen to agree with each other, and they do
not. One is a graduate research seminar taught by a theoretical computer
scientist who also works at a frontier lab. One is a frontier lab's own
compressed statement of what it thinks the alignment problem is. One is
a non-technical textbook course written by an academic research org.
One is a practitioner training series on governance frameworks and
audit practice. Read together, they are four defensible answers to
"what does a safety education actually need to contain?" — and this
repository's answer, the 24 chapters, is a fifth. The differences are
the point: where the courses overlap, the idea is probably load-bearing;
where only one course teaches something, that is a bet, and it is
priced as one in the notes.

## The four courses

| Course | What it is | Videos | Companion |
|---|---|---|---|
| [Harvard CS 2881 — AI Safety](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W) (Boaz Barak) | Graduate research seminar; measurement and scale as the two organizing axes; student experiments presented in every lecture | 19 | [boaz-barak-cs2881/](boaz-barak-cs2881/) |
| [Google DeepMind AGI Safety Course](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW) | The frontier lab's own ~90-minute statement of the alignment problem and its candidate answers, in three parts with exercises | 16 | [google-deepmind-agi-safety/](google-deepmind-agi-safety/) |
| [AI Safety, Ethics, & Society](https://www.youtube.com/playlist?list=PLXSn3Zz2ayT7ab7I12PBYVt0244369S1q) (Center for AI Safety) | The non-technical university course: risks, fundamentals, single-agent safety, safety engineering, complex systems, ethics, collective action, governance | 8 | [cais-ethics-society/](cais-ethics-society/) |
| [AI Governance series](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW) (Safeshield Training) | Practitioner training in the governance layer: principles, risk management, ISO/IEC 42001, NIST AI RMF, the EU AI Act, audit practice | 14 | [safeshield-governance/](safeshield-governance/) |

(Companion directories land one course at a time this session; each
row's link is added by the unit that completes it — the live record is
[planning/STATUS.md](../planning/STATUS.md).)

Every external link in the table was resolved on 2026-10-27: the
four playlists through YouTube's playlist API (title, channel, video
count, and the full per-video list with durations), and the Harvard
course's own schedule page was read in full, both the Fall 2026 page and
the Fall 2025 archive (that page is itself registered — see its course
companion). Their register entries are
[SRC-VIDEO-011..018](../research/source-register.yaml) and
[SRC-CURR-012..013](../research/source-register.yaml), added by the
units that build each course page.

## How to watch (the guide)

The library is not a fifth course to complete; it is a set of lenses over
the course you are already taking. Three sane patterns, in order of
escalation:

1. **The primer pass (about 90 minutes).** Before starting the repo's
   common methodological spine (Chapters 01–02), watch the Google DeepMind
   AGI Safety Course straight through. It is the field's own compressed
   statement of the problem, it requires no mathematics, and it will make
   every chapter's first section land faster.
2. **The alongside pass (about 7 hours, spread over the whole course).**
   Pair each chapter cluster with its matching lectures from the
   [Harvard CS 2881 playlist](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W)
   and the [CAIS course](https://www.youtube.com/playlist?list=PLXSn3Zz2ayT7ab7I12PBYVt0244369S1q)
   — the mapping table in each course page and the "watching companions"
   block in each chapter README state exactly which lectures pair with
   which chapters, and why. Watch the lecture *before* the chapter when a
   topic is new to you; after it, when you want the researcher's vantage.
3. **The operator pass (about 12.5 hours).** If your target is audit,
   assurance, or governance work rather than research, run the
   [Safeshield governance series](https://www.youtube.com/playlist?list=PL70MHvytmJU8zwamiQnweHV0Vj-h0zlOW)
   alongside Chapters 22–23 and the [audit-only route](../roadmaps/audit-only.md).
   It is the only layer here that teaches the frameworks as Monday-morning
   practice rather than as concepts.

One rule holds across all three patterns: **the lectures are primary
sources, not summaries of this repository**. When a lecturer and a chapter
disagree, the disagreement is the finding — write it down, price both
sides, and carry it into the chapter's critique exercise.

## The note discipline (read this before reading any note)

These companion notes are **original explanations, not transcripts**.
The playlist and course-page structure was verified at fetch, but no
video was watched and no spoken content is transcribed or quoted
anywhere in this repository — the same rule the video library has held
since it opened. Each note is anchored to what CAN be verified: the
lecture's announced title and topic, the course page's published
schedule, required-reading list, and experiment description, and the
field's own literature where the repo already registers it. Where a
note explains an idea, it explains it from the literature — the
lecture link is the pointer to the source, never the paraphrased
content of it.

This means the notes are honest about their strength: they are study
companions written to the lecture's announced scope. If a lecture
surprised its audience with material outside that scope, the note
cannot know. The reading lists are reproduced where the course page
publishes them — as link lists attributed to the course, not as this
repository's endorsements — and where a reading already sits in the
repo's [paper spine](../AWESOME.md), the note says so and cites the
register ID.

## How the library maps onto the chapters

- **Chapters 01–08** (risk models through control) pair with the
  DeepMind course's Parts 1–2 and Barak's scheming lecture cluster.
- **Chapters 09–11** (interpretability) pair with Barak's
  interpretability lecture and its four guest researchers.
- **Chapters 12–15** (adversarial ML, application security, agents,
  red teaming) pair with Barak's robustness lecture and the DeepMind
  design-patterns material.
- **Chapters 16–18** (privacy, reliability, reasoning) pair with the
  Safeshield privacy module and the monitoring material.
- **Chapters 19–24** (misuse, systemic risk, assurance, governance,
  research practice) pair with the CAIS course as a whole, the
  Safeshield governance series, and Barak's economics and regulation
  lectures.

The per-chapter mapping, lecture by lecture, is stated in each
chapter's README (the "watching companions" block) and in each course
page's own mapping table — both written so that either direction of
lookup works.

## Building status

This layer is being built unit by unit in session 3 (see
[planning/STATUS.md](../planning/STATUS.md) for the live record): the
four course pages land first, then the companion notes course by
course, then the chapter integrations. The honesty rule from the
repository's method applies here too: a note that does not exist yet
is listed as not existing yet — nothing in this directory will ever
claim completeness it does not have.

## The complete library (2026-10-27 state)

Four courses · 57 verified videos · 61 companion notes (18 Harvard +
16 DeepMind + 8 CAIS + 14 Safeshield + 5 pedagogy/study-plan pages)
· 4 self-assessments · 3 framework crosswalks · 3 cross-course
comparisons · 10 register entries · 4 verified dataset cards added to
the catalog (GDPval, RE-Bench, METR time-horizons, Canaries) ·
watching companions in all 24 chapters and watching pointers in all
24 solutions files. Every external URL in this layer passed
`verify_links.py` before it landed; the runs are recorded as
rotation 4 in MAINTENANCE.md. The structure is pinned by
`tests/test_courses_integrity.py`.

See also: [honesty-ledger.md](honesty-ledger.md) — what this library did NOT do.
