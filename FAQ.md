# FAQ — the questions beginners actually ask

Answered with links into the repository, not generic advice. If your
question is not here, the [START_HERE](START_HERE.md) map or the
[dashboard](index.html) is the next stop.

## Getting started

**Do I need a GPU, an API key, or paid anything?**
No. The core path is free and CPU-only: every project runs
deterministically on a laptop (`uv sync && uv run pytest` is the whole
setup). The optional compute tiers (local small models for P03/P04/P06
model paths) use open models; the course never requires a paid API —
where a commercial model would be interesting, the evaluation is
designed so a small local model demonstrates the same methodology.

**How long does this take?**
The honest arithmetic lives in [ROADMAP.md](ROADMAP.md) and
[roadmaps/study-schedules.md](roadmaps/study-schedules.md): ~120 h
focused (a selection), ~170 h part-time (one specialization),
~400+ h the full curriculum. If you want the first steps concrete
instead of arithmetic: [roadmaps/first-90-days.md](roadmaps/first-90-days.md),
an artifact every Friday.

**Which route should I pick?**
Take the [diagnostic](prerequisites/diagnostic.md) first — it maps
your gaps to chapters. Then pick by the work you want to do, not the
title you want to hold: [alignment research](roadmaps/alignment-research.md)
(investigate failures), [AI security engineering](roadmaps/ai-security-engineering.md)
(bound them), [evaluations and assurance](roadmaps/evaluations-and-assurance.md)
(test and argue them), or [audit-only](roadmaps/audit-only.md) (read
and judge, no PyTorch). The job-market mapping is in
[roadmaps/careers-index.md](roadmaps/careers-index.md).

**I'm not "experienced" — is this for me?**
The advanced chapters assume Python, linear algebra, probability,
gradient basics, and transformer/RL familiarity (the diagnostic's
R1–R5). If some are shaky, [targeted refreshers](prerequisites/targeted-refreshers.md)
tell you exactly what to study and which chapters will hurt without
it. Total beginners to Python should build that base elsewhere first —
this is deliberately not a first programming course.

## Using the course

**What does "verified reading" actually mean?**
Every external fact traces to a register entry with one of five access
levels — full-text-read, abstract-read, page-inspected, metadata-only,
unavailable — and a date. The method is the course's spine; the
learner version (with a five-minute drill you can do right now) is
[prerequisites/verifying-sources.md](prerequisites/verifying-sources.md),
and the live state of all 261 sources is the
[evidence ladder](index.html).

**Can I cite the numbers in the chapters?**
Cite the primary sources (every number's register ID is in the prose),
and cite this repository for the curriculum itself
([CITATION.cff](CITATION.cff)). Market numbers (job counts, salaries)
are dated snapshots: re-verify before you rely on them — that is not a
disclaimer, it is the method.

**Where do the datasets come from? Are they included?**
22 real-world safety datasets, each with a deep card
([datasets/catalog.yaml](datasets/catalog.yaml)): composition facts
traced to the URLs they were collected from, licenses as observed,
contamination status. The repository **never redistributes dataset
content** — you download from the canonical sources under their terms.

**What are the "incident reviews"?**
Production failures (Air Canada's chatbot liability, DPD's post-update
regression, the Chevy dealership's $1 Tahoe), reviewed under a strict
template: observable facts, attributed conclusions, named unknowns,
and a mandatory "what this does NOT demonstrate" section.
[Read them](research/notes/incidents/README.md) — they are the fastest
way to see the course's discipline applied to events you may already
know from the news.

**What is index.html?**
The whole build as one generated web page: counters, the evidence
ladder, chapter map, project cards, dataset/source/claims explorers
with live search, the career tracks, and the beginner quickstart. It
is generated from the repository's own data
(`scripts/build_dashboard.py`), works offline, and is regenerated in
the same commit as any data change — the page cannot silently drift
from the repo (CI checks).

## Going deeper

**Can I contribute?**
Yes — start at [CONTRIBUTING.md](CONTRIBUTING.md); the three rules
that matter most are there, and [MAINTENANCE.md](MAINTENANCE.md) is
the operating manual for the living parts (registers, catalog,
dashboard). The bar for prose is the honesty infrastructure: no claim
without a source at a stated access level.

**What do I do if a number or link looks wrong?**
Open an issue — a wrong number that traces to no register entry is a
bug, and the repo's own audit exists to catch exactly that. If you can
fetch the primary source yourself, you already know the method: record
what you actually saw, at what access level, on what date.

**Is there a certificate?**
No. The exit criteria are artifacts — a falsified hypothesis, a threat
model, a safety case, a deployability dossier — because that is what
interviewers at every organization in the
[careers index](roadmaps/careers-index.md) actually probe.

**Why do some notes say the abstract "truncates"?**
Because the arXiv API record for that paper cuts off mid-sentence,
and the note refuses to fill the gap from memory. The session-2
note set (33-70) was verified against the API title-by-title —
five of the eighteen planned IDs were wrong in the register's own
draft, caught before a single note cited them. "Truncation
recorded" is the discipline: the honest limit is printed where the
invented number would have gone.

**Why do the incidents include failures that were fixed quickly?**
Because the response half is the lesson. Cursor corrected in three
hours; MyCity kept the bot up; Air Canada fought to a tribunal.
[Comparison 10](research/notes/comparison-10-incident-response-postures.md)
extracts the pattern: time-to-honest-characterization sorts the
outcomes more than the failures themselves did. Fast fixes that
never happened would be noise; fast fixes that did are the
curriculum.

**What's the difference between the four progress trackers?**
The discipline: each route's checkboxes name artifacts a stranger
can audit — the researcher's falsifiable extensions, the security
specialist's paired ledgers, the engineer's price-tagged controls,
the auditor's written challenges. Fork the repo, tick in your fork,
and your commit history is the progress record. The trackers live
in [roadmaps/progress/](roadmaps/progress/README.md).

**Why does the dashboard show a bar chart of notes per chapter?**
Because coverage is a claim, and the chart is the claim's audit:
nine chapters silently had zero note companions until the widget
surfaced it (fixed the same day). If a bar drops to zero again,
that is a regression — which is the point of rendering it.

**Why 43 dataset cards and not 43 downloads?**
Because the catalog is a *verification* instrument, not a mirror:
every card records where each fact was collected, at what access
level, on what date — and the redistribution policy is "never."
Downloading the data is the learner's own step, taken after the
five-minute drill (in the [dataset README](datasets/README.md))
confirms the card's chain holds.

**What did the LLM-as-judge actually decide?**
The [session-2 audit](planning/SESSION2_JUDGE_AUDIT.md) judged seven
gaps — notes, datasets, incidents, trackers, dashboard, glossary,
re-checks — priced each with named collection points, and closed all
seven with the evidence table in its section 6. The judge's own four
mistakes (wrong IDs, masked gate, silent sweep, crossed message) are
recorded there too: an audit that cannot audit itself is marketing.

**Is the dashboard the same as the repo?**
No, and the test suite enforces the difference: the dashboard is
*generated* from the repo's registers and catalogs, and the
freshness test fails if the committed index.html drifts from a fresh
build. Regenerate with `uv run python scripts/build_dashboard.py`
after touching any register — or let the gate teach you (it taught
this session twice).

## The lecture library (the video-course companions)

**What is `courses/`?** The four external courses the owner selected —
Harvard CS 2881, the Google DeepMind AGI Safety Course, the CAIS
Ethics & Society course, and the Safeshield governance series —
turned into companion notes: a course page with the complete verified
video index per course, one note per lecture, per-course pedagogy
analyses, and study plans that schedule the watching against the 24
chapters.

**Are the notes transcripts?** No. The playlist structures were
verified (via YouTube's playlist API), the Harvard course pages were
read in full, and the notes are original explanations of each
lecture's announced topics and published readings. No video was
watched; no spoken content is transcribed or quoted anywhere in this
repository — the same rule the video library has always held. See
[courses/README.md](courses/README.md) for the full note discipline.

**Where do I start?** The [watch guide](courses/README.md#how-to-watch-the-guide):
90 minutes (the DeepMind course) before Chapter 01; the alongside
pass (~4–6 hours across the whole program) paired by chapter; the
operator pass (12.5 hours, Safeshield) for audit and governance
routes.

**Can I contribute a lecture note?** Yes — follow
[CONTRIBUTING.md](CONTRIBUTING.md)'s lecture-library section: register
the source first, verify its URL through the link instrument, write
an original companion to the announced scope, and link the course
README's row in the same commit that adds the note. Never transcribe
or quote spoken content; never reproduce textbook text.

**Why do some counts in the README keep changing?** Because
the repository recomputes them from its own data — the registers, the
catalog, the test suite — and fails loudly (via the count-drift
tests) whenever a pinned surface drifts. If you see numbers move
after a pull, the instruments are working; the CHANGELOG records
what moved and why.
