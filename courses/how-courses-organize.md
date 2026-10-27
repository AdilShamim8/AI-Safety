# How the four courses organize knowledge

*A cross-course analysis · part of the [lecture library](README.md) ·
written 2026-10-27 from the verified course structures*

## The question this note answers

The owner's directive for this library was specific: understand not just
what these courses teach, but **how they gather, organize, and manage
information** — the pedagogy itself — because that is the layer a
repository can actually learn from. This note compares the four courses
as *knowledge-organizing systems*, then states what this repository took
from each.

## Four architectures, side by side

| Axis | Harvard CS 2881 | DeepMind AGI Safety | CAIS Ethics & Society | Safeshield Governance |
|---|---|---|---|---|
| Unit of instruction | the weekly research seminar | the single compressed claim | the textbook chapter | the framework module |
| Core artifact | primary-source reading list + student experiment | 3–9 minute mechanism videos + exercises | published textbook, 8 chapters | standards and law as curriculum |
| Evidence discipline | read papers as a researcher reads: assumptions, gaps, strength | a lab's self-statement, priced as such | accessible synthesis of the published literature | compliance-grade: the standard is the source |
| Time cost | graduate semester (13 × 2.5h lectures + project) | ~85 minutes | ~7 hours | ~12.5 hours |
| Who it is for | ML-ready graduate students | practitioners in a hurry | everyone | GRC professionals |
| What only it does | live student experiments every lecture; guest practitioners per topic | a frontier lab's own risk model, stated publicly | collective-action and society-scale framing | implementation and audit practice |

## What each architecture chooses to believe

**CS 2881 bets on evidence discipline.** Its organizing claim — visible in
every lecture's design — is that safety knowledge is built the way other
empirical knowledge is built: read the primary sources, run the small
experiment, present the result including its failures. The student
experiments are the load-bearing structure: every week, a group runs a
bounded empirical study and defends it live. The course even teaches the
meta-lesson — its Fall 2025 experiments on policy compliance and on coding
agents under impossible tasks are themselves small studies of *when honest
work becomes evaluation gaming*.

**The DeepMind course bets on compression.** Eighty-five minutes, sixteen
named mechanisms, two checkpoint exercises. The bet is that a working
professional will give the problem one commute's worth of attention, so
every minute must carry one load-bearing idea. The exercises are placed
exactly where a misconception would compound — after instrumental
subgoals, after the failure taxonomy — which is curriculum design as error
correction.

**The CAIS course bets on layering.** It moves outward in circles of scope
(single agent → engineering → complex systems → society) because its
audience cannot yet distinguish an alignment failure from a market failure
from a governance failure; the layering *is* the content. It is also the
only course that teaches collective action — racing dynamics, coordination
among humans — as a first-class unit, which is precisely the gap a
technically-focused curriculum leaves.

**The Safeshield series bets on operability.** Principles → risk process →
named frameworks → lifecycle operations. Its "knowledge" is law and
standards: ISO/IEC 42001's management-system clauses, the NIST AI RMF's
govern-map-measure-manage cycle, the EU AI Act's risk tiers. The bet is
that the governance layer is learnable the way accounting or aviation
regulation is learnable — as documented, auditable practice.

## What this repository took from each

1. **From CS 2881: the reading-list-as-spine.** The repo's paper spine and
   note companions follow the same logic the Harvard course does — the
   primary source is the unit of truth, and every claim lands with its
   register entry. The companion notes in this library reproduce the
   course's published reading lists precisely so learners can do what the
   course does: read the sources, not summaries of them.
2. **From the DeepMind course: the compressed on-ramp.** The repo's
   START_HERE and the lecture library's primer pass exist because the
   lab's course proves the format: one honest 90-minute orientation beats
   a week of unstructured reading for a newcomer.
3. **From CAIS: the scope layers.** The repo's late chapters
   (sociotechnical risk, governance) mirror the CAIS arc's outer circles,
   and its collective-action material fills the gap the technical courses
   leave.
4. **From Safeshield: the operator's Monday.** The repo's assurance and
   audit chapters teach the same frameworks conceptually; the governance
   series is indexed here as the practice layer that turns those concepts
   into documentable, auditable process.

## The honest limitation of this analysis

This note is written from the courses' **published structures** —
schedules, reading lists, syllabi, video titles — not from watching them
end to end. It analyzes the architecture, which is fully visible in those
artifacts; it does not claim to review the lecture delivery itself. The
per-lecture companion notes carry the same honesty marker individually.
