# Lecture 9 — Economic impacts of foundation models: labor, growth, and the measurement layer

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 9: Economic Impacts of AI](https://www.youtube.com/watch?v=4vQSMijp_M8) (2:32:33) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The economics lecture, with guest lecturers Ronnie Chatterji
(then chief economist at OpenAI) and Bharat Chandar (Stanford Digital
Economy Lab). Announced topics: labor substitution and productivity
effects; inequality and policy responses.

## The announced scope

Announced on the course page: the employment-effects evidence
base, the growth-vs-risk formalization, and how usage data bridges
lab capability and macro outcomes.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Jones, "Artificial Intelligence in Research and Development"
(2025); Chatterji et al., "How People Use ChatGPT" (NBER, 2025);
Brynjolfsson, Chandar & Chen, "Canaries in the Coal Mine? Six Facts about
the Recent Employment Effects of Artificial Intelligence" (2025); Jones,
"The A.I. Dilemma: Growth versus Existential Risk" (2024). Optional list:
Goldman Sachs on long-run AI impact on GDP and jobs; Brynjolfsson et al.,
"Generative AI at Work"; Acemoglu & Restrepo on AI, automation, and work;
Eloundou et al., "GPTs are GPTs"; and Roodman's modeling of transformative
AI's economic impact. The full list with links lives on the
[course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Labor economics as the first measurable safety-adjacent impact

The lecture's guest pair (Ronnie Chatterji, then OpenAI's chief
economist, and Bharat Chandar of the Stanford Digital Economy Lab)
frames employment effects as the earliest place AI's societal impact
becomes *measurable at scale* — which makes it the natural test bed for
the course's measurement axis applied to social outcomes. The Canaries
paper's six facts are the anchor: occupation-level exposure is visible
in online job postings before it is visible in aggregate employment;
writing-heavy and entry-level task clusters show the earliest
displacement signals; and the aggregate statistics lag the micro
signals by construction. The safety connection is direct: uneven,
rapid labor reallocation is itself a social risk factor, and the
governance layer (Ch. 23) increasingly cites exactly these employment
indicators.

### 2. The growth-versus-risk dilemma, formalized

Chad Jones's "The A.I. Dilemma" puts the lecture's title question into
a growth model: if AI dramatically expands effective labor and research
capacity, growth can explode (the transformational case); the same
mechanism raises the stakes of misalignment. Growth economics gives
the field its cleanest statement of why capability and risk are one
variable viewed from two sides — and why "pause" arguments and
"accelerate" arguments are both claims about a shared quantity neither
side can yet measure well.

### 3. How-people-actually-use-it data as the missing measurement layer

The NBER "How People Use ChatGPT" line of work matters because usage
data — what tasks people actually bring to these systems, at what
frequency, with what substitution — is the bridge between lab
capability curves and macro outcomes. It is also the dataset class
this repository's dataset catalog treats with care: proprietary panel
data with strong access restrictions, priced honestly in the register
as vendor-self-reported when it is.

### 4. The Fall 2026 continuation

The Fall 2026 iteration brought the same material forward a year with
Chad Jones and Erik Brynjolfsson as guests and a refreshed list (the
Turing Trap, centaur evaluations, the transformative-AI research
agenda) — its companion note lands later in this library under
`f26-lecture-05-economic-impact.md`.

## Through-line to this repository's chapters

- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) —
  labor displacement as sociotechnical risk, not just economics.
- [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md) —
  the measurement discipline applied to social outcomes.
- [datasets/README.md](../../datasets/README.md) — the catalog's
  treatment of employment and usage datasets.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
