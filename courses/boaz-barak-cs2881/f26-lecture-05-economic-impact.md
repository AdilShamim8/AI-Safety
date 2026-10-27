# Fall 2026 Lecture 5 — Economic impact of AI: the Turing Trap and the centaur standard

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Fall 2026 Lecture 5: Economic Impact of AI](https://www.youtube.com/watch?v=iezRKFkyjVY) (2:25:27) · Fall 2026 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The October 1 economics lecture with guests Chad
Jones and Erik Brynjolfsson — the 2026 refresh of the labor-and-growth
material, now anchored on the imitation-vs-complement design choice
and the freshest employment evidence.

## The announced scope

Announced on the course page: the Turing Trap, centaur
evaluations, the 2026-updated Canaries evidence, the transformative-AI
research agenda, and the growth-vs-bottleneck growth models. The
student experiment: LLM market mechanisms.

## The published reading list (Fall 2026 Lecture 5, Oct 1, as listed on the course page)

Guest lecturers: Chad Jones and Erik Brynjolfsson. Required
pre-reading: Brynjolfsson, "The Turing Trap: The Promise & Peril of
Human-Like Artificial Intelligence" (Daedalus, 2022); Brynjolfsson,
Chandar & Chen, "Canaries in the Coal Mine: Six Facts about the
Recent Employment Effects of Artificial Intelligence" (August 2026
update); Haupt & Brynjolfsson, "AI Should Not Be an Imitation Game:
Centaur Evaluations" (ICML 2025); "A Research Agenda for the
Economics of Transformative AI" (skim, focusing on the nine research
challenges including safety); Jones, "AI and Our Economic Future"
(Journal of Economic Perspectives, Summer 2026); Jones & Tonetti,
"Past Automation and Future A.I.: How Weak Links Tame the Growth
Explosion" (May 2026). Optional: "AI's Use of Knowledge in Society."
The full list with links lives on the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. The Turing Trap: imitation as the wrong objective

Brynjolfsson's Daedalus essay is the conceptual anchor of the 2026
economics lecture: building machines to imitate humans captures only
the tasks humans already do — and competes with them — while building
machines to *complement* humans (different capability profile, human
in the loop where judgment lives) grows the pie. The safety course
teaches it because objective-choice at the system level is a safety
decision: an economy optimizing human-imitation is an economy
building replacements rather than colleagues, with the distributional
and stability consequences that follow.

### 2. Centaur evaluations: measuring complementarity, not similarity

The Haupt–Brynjolfsson ICML paper operationalizes the Turing Trap's
moral for evaluators: benchmark designs that score AI-alone against
humans-alone systematically miss the human+AI condition where most
value may live. For the repo's evaluation chapters this is a
construct-validity lesson with economic stakes — what your benchmark
measures determines what your economy builds. The paired-design
methodology (same tasks, human-only, AI-only, and paired arms) is the
exportable experimental template.

### 3. The 2026 state of the employment evidence

The Canaries paper's August 2026 update is the reading list's
freshest evidence: exposure measurable in postings and task clusters,
early-career and writing-heavy occupations showing the sharpest
signals, and — the paper's own caution — aggregate employment still
inside noise. Teaching *the update itself* models the discipline this
repository demands everywhere: perishable numbers, dated fetches, the
register pricing them as they deserve.

### 4. Weak links and why growth may not explode

Jones & Tonetti's "weak links" framing is the growth-theory
counterweight to the explosion models of the RSI lecture: in
production networks, the slowest necessary input caps output, so
AI-driven productivity in some tasks does not automatically compound
through the economy. Alongside Jones's JEP piece on "AI and Our
Economic Future," it gives the 2026 economics lecture both horns —
transformative upside conditional on complements, and drag from every
remaining bottleneck — which is exactly the priced-scenario posture
the course opened with.

## Through-line to this repository's chapters

- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) —
  economic transformation as systemic risk and benefit.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  benchmark design as an economic instrument (the centaur lesson).
- [datasets/README.md](../../datasets/README.md) — the employment-evidence
  dataset cluster (Canaries and usage panels).

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
