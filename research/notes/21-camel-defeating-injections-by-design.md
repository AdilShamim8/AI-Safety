# Note: Defeating Prompt Injections by Design (CaMeL) (2025)

Source: SRC-PAPER-054 · Access: **abstract-read** (arXiv v2 page,
2026-10-22) · Note level: **abstract-level** (the access supports
exactly this and no more).

## The actual problem

Prompt injection's structural pessimism: every same-channel defense
(instruction hierarchy, spotlighting, system-prompt discipline) tries to
make the MODEL distinguish trusted instructions from untrusted data
inside one token stream — and Chapter 13's claim is that this cannot
be a boundary, only a prior. CaMeL's move is to stop trying: keep the
model, but move the trust boundary OUT of the model and into a
deterministic system layer around it. The question the paper asks:
how much agent usefulness survives when control flow and data flow are
enforced by code the model cannot rewrite?

## Method (as the abstract establishes it)

Two mechanisms, both inherited from classical software security rather
than from ML: (1) the system extracts CONTROL FLOW and DATA FLOW
explicitly from the trusted user query, so untrusted content the model
later retrieves can inform values but can never alter the program's
shape — the data cannot promote itself into an instruction position
because no such promotion path exists; (2) a CAPABILITY system
governs tool calls, enforcing security policies over data flows so
private data cannot exfiltrate over unauthorized paths — the
principle Dennis and Van Horn named in 1966 [SRC-PAPER-057],
resurrected for LLM agents. The claim class is "provable security" —
the defense argument is about the system's structure, not about the
model's robustness.

## Results (abstract-level, with the honest caveats)

77% of AgentDojo tasks solved WITH the CaMeL layer, versus 84%
undefended [SRC-PAPER-054, v2 abstract; the v1 figure was 67%, and
the chapter 14 register entry already prices the version drift]. The
7-point usefulness gap IS the result a careful reader should keep:
security bought at a measured utility price, stated up front — the
same two-sided discipline P07 and P10 enforce on their own defenses.
What the abstract does not give: per-task breakdowns (which tasks the
layer loses), the security-policy formalism, and what "provable"
precisely scopes over (the model can still be socially engineered
into producing wrong VALUES; the guarantee is about FLOWS). The
register's limitations field carries all of this.

## What this note does NOT claim

The body was not read: the 77/84 numbers are abstract statements with
assumed denominators (97 AgentDojo tasks, from SRC-PAPER-055), the
theorem statement is unread, and no reproduction exists here. Chapter
13's original pointer to CaMeL as "design-direction" was correct at
its access level — this note upgrades the pointer to an abstract-level
claim with its price attached, nothing more.

## Falsifiable extension

The usefulness gap is where the course can extend: CaMeL's own
framework implies a frontier — how much of the 7-point loss is the
capability policies (recoverable by policy tuning, as P10's IA-1..IA-3
recover benign flows) versus the control-flow discipline itself
(structural)? Design: instrument a CaMeL-style layer over the P07
fixture stack with per-task hold-out; ablate R1–R4-style policies one
at a time; report each configuration's attack-stop and
benign-completion rates with Wilson intervals at the fixture's n.
Stopping rule: if no single policy's removal recovers >2 benign
points at zero attack cost, the loss is structural, and the
"capability-layer" pricing of the 7-point gap fails. This is runnable
at the course's deterministic tier — no model downloads.

## My interpretation vs. their claims

Their claims: (1) a protective system layer can secure LLM agents
even when the model is fully susceptible; (2) capabilities + explicit
flows are the right primitives; (3) 77% at provable security versus
84% undefended. My reading: (1) is the field's strongest answer yet
to injection's structural pessimism, and its ancestry (CFI, CFL,
capabilities) is exactly the software-security lineage Chapter 14
teaches — the paper is evidence that the 1960s vocabulary still
works; (2) the durable contribution is the FLOW/VALUE distinction
itself, which survives any model change; (3) the number to cite is
always the PAIR with its gap and version — a bare "77%" (or the v1
"67%") is how a structured result degrades into a slogan, and the
comparison note C04's prompt-defenses-versus-boundaries frame is the
course's device for keeping the pair together.
