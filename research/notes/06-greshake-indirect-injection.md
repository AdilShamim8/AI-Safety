# Note: Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection (2023)

Source: SRC-PAPER-050 · Access: abstract-read · Read: 2026-10-22 ·
Note level: **abstract-level** (the register's access governs; no
numeric success rates appear in the abstract and none are cited).

## The actual problem

The authors' framing: LLM-integrated applications — chat with web
browsing, code assistants, email summarizers — retrieve and ingest
untrusted data, and an adversary who controls *that data* controls
part of the instruction stream. The operational version: demonstrate
remote exploitation of real-world LLM applications by planting prompts
in data the application will retrieve, and organize the impact
taxonomy (what an indirect injection actually buys the attacker).

## Method

(What the abstract carries:) strategic injection of prompts into data
likely to be retrieved — demonstrations against real-world systems
including Bing's GPT-4-powered Chat and code-completion engines —
with the attacker never sending a message to the application at all.

The design logic: the attack surface is not the model but the
*application's data flow* — a web page is a published instruction, an
email is a delayed instruction, a repository file is a targeted
instruction. The method is the threat model: who can write what the
application will read.

## Central evidence

- Real-world demonstrations: Bing's GPT-4-powered Chat and
  code-completion engines compromised through retrieved data (the
  systems of the day, named).
- The impact taxonomy (the abstract's organizing contribution): data
  theft, worming (self-propagating injection through the application's
  own outputs), and information-ecosystem contamination — indirect
  injection is not one vulnerability but a class with an ecosystem
  footprint.
- The mechanism claims: processing retrieved prompts as arbitrary
  instructions, manipulating application functionality, controlling
  whether and how other APIs are called — the LLM becomes the
  confused deputy that hands the attacker the application's
  capabilities.

What the evidence does NOT carry: per-application success rates and
attack specifics live in the unread full text; the demonstrations date
to the 2023 application generation (specific integrations have
changed); nothing about defenses (the paper is the threat-model
anchor, not the mitigation source).

## Assumptions

Tested in-paper: that the demonstrated systems ingest attacker-
controllable data (the retrieval premise — the applications' own
features); that instruction-following transfers from the user's
channel to the retrieved channel (the demonstrated compromises).

Inherited: that the 2023-generation behavior generalizes across
application designs (the channel problem is structural — chapter 13's
argument — but *rates* are application-specific); that no implicit
privilege separation existed in the demonstrated systems (true then,
still mostly true).

## Limitations

Authors' (abstract-level): none stated beyond the demonstrations.
Mine: the paper predates the retrieval-marking and hierarchy defenses
(chapter 13's families), so its systems were undefended by design —
the right modern reading is "the attack class exists and its impact
taxonomy is rich," not "current systems fall at these rates"; and the
worming class, while logical, needs persistence conditions (stored +
retrieved + forwarded) that specific deployments may not provide.

## Nearest alternatives

- **Perez & Ribeiro (SRC-PAPER-051)**: the direct-injection twin —
  the user's own text as the attack channel; together the two papers
  cover the channel problem's two halves.
- **OWASP LLM Top 10 (SRC-REPORT-004)**: the deployment vocabulary
  that grew around this threat class — LLM01 is this paper's finding
  in list form.
- **Spotlighting (SRC-PAPER-053) and the instruction hierarchy
  (SRC-PAPER-052)**: the defense families that answer it — read the
  attack first, or the defenses' measured effects (50%→2%) have no
  threat model to be effects against.

## Replication feasibility

The *threat-model artifact* is fully replicable at course scale: pick
a RAG deployment pattern (chapter 13's worked example is exactly
this), enumerate the adversary-writable bytes that reach context, and
price each channel's reach — no attack execution needed for the
audit-form deliverable. What is NOT course-scale: executing attacks
against third-party systems (out of scope by the course's own rules —
the chapter-13 boundary). A self-owned toy RAG stack with an authored
"poisoned corpus" reproduces the mechanism honestly (P07's design).

## Falsifiable extension

Hypothesis: the worming class requires all three persistence
conditions (stored, later-retrieved, forwarded-by-the-application),
and deployments missing any one are structurally non-wormable even
while remaining injection-vulnerable — so "injection risk" and
"worming risk" are separable audit findings. Design: model the three
conditions as a 2³ grid over deployment patterns; for each cell,
evaluate an authored injection's propagation on a toy RAG stack
(store-yes/no × retrieve-yes/no × forward-yes/no). Metric: injected
instruction propagation rate with explicit denominators. Baseline:
the full-conditions cell. What counts against: if propagation occurs
in cells missing conditions (e.g., forwarding alone suffices), the
taxonomy's separability premise fails and worming is harder to scope
than the conditions suggest.

## My interpretation vs. their claims

Their claims: (1) indirect prompt injection enables remote
exploitation of LLM-integrated applications; (2) the impact taxonomy
spans data theft, worming, and ecosystem contamination; (3) real
systems of the day were demonstrably compromised.

My interpretation: (1) is the founding structural claim of the
application-security chapter and has aged perfectly — the channel
problem (chapter 13 §1) is an architecture fact, not a bug report;
(2) the taxonomy's most under-used entry is ecosystem contamination —
injection as a *publishing* strategy (poison the corpus every chatbot
reads) scales with the number of LLM applications that touch the web,
which makes it a public-goods problem dressed as a security problem;
(3) the demonstrations were undefended systems, and the paper's
citation life as "injection works" should be read as "injection
worked, undefended, then" — the modern question is the defense
families' measured effects under adaptive pressure, which is
chapter 13 §3.2's exact discipline.
