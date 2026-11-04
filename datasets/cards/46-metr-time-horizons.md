# Dataset card: METR time-horizon measurements (task-length data)

unknown (blog-published analysis; see license section) · verification
date 2026-10-27 · prepared by the course build · status: blog page inspected
in full (finding, doubling time); analysis code and raw data linked
from the page; no data downloaded or redistributed

## 1. Identity and provenance

- **What it is:** METR's measurement of the length of software tasks
  AI agents can complete with given reliability — the field's
  cleanest capability-trajectory instrument: the task-horizon
  doubling curve.
- **Canonical home:** [Measuring AI Ability to Complete Long
  Software Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
  [R1] (METR blog, 2025-03-19; page inspected 2026-10-27).
- **The load-bearing finding:** the length of tasks AI agents can
  complete with 50% reliability has been doubling roughly every **7
  months** over the ~6 years measured [R1].
- **Data availability:** the post links analysis code, raw data, and
  a dedicated time-horizons page [R1] — linked, not downloaded.
- **How WE obtained it:** page inspection on 2026-10-27; no data
  redistributed.

## 2. Composition (page-verified)

- Task-horizon measurements across agent vintages, with
  reliability-conditioned horizon lengths; the doubling-time trend is
  the headline construct [R1].

## 3. License

- Not stated on the inspected page; treated as unknown. Analysis
  code and data remain under METR's terms at their canonical home.

## 4. Course use

- **Chapters:** 02 (evaluation design: reliability-conditioned
  capability measurement), 01 (trajectory evidence as priced claims),
  20 (autonomy as the compounding capability axis).
- **Lecture library:** the CS 2881 Lecture 1 notes (the METR
  pre-reading) and the DeepMind Part 1.1 note (the
  capability-trajectory claim).

## 5. Verification record

- [R1] metr.org blog page (full render: title, finding, doubling
  time, links; 2026-10-27).

## 6. What this dataset CANNOT support

- No extrapolation beyond the measured range: the doubling-time figure
  is the paper's page-level statement over their model set; the card
  does not project it to unmeasured models or future releases.
- No per-task breakdown: the card records the finding and the doubling
  time; task-level composition and scoring live in the unread body.
- No hiring or capability decision: a time-horizon number is not a
  deployment decision input by itself, and the card does not treat it
  as one.
- No redistribution: page-verified only; no files downloaded.
