# Comparison note C04 — Prompt defenses vs authorization boundaries: two answers to the same attack

> Comparison notes: 4 of 5 planned. Sources: SRC-PAPER-004
> (Universal and Transferable Adversarial Attacks, abstract-read),
> SRC-PAPER-050 (Greshake indirect injection, abstract-read),
> SRC-PAPER-052 (Instruction Hierarchy, abstract-read), SRC-PAPER-053
> (Spotlighting, abstract-read), SRC-REPORT-004 (OWASP LLM Top 10
> 2025, abstract-read), SRC-REPORT-005 (MCP specification 2025-06-18,
> page-inspected), SRC-REPORT-006 (Invariant Labs tool poisoning,
> page-inspected), SRC-REPORT-007 (Willison CaMeL commentary,
> page-inspected), SRC-PAPER-054 (CaMeL, abstract-read). Companion
> chapters: 13 (the attack), 14 (the boundary), 15 (the red team
> that prices both); companion project: P07 (the boundary family,
> implemented and measured).

## The question a comparison exists to answer

Indirect prompt injection is the same attack whichever defense you
pick: untrusted text lands in a context the model reads as
instructions [SRC-PAPER-050]. The field offers two fundamentally
different answers, and products routinely ship one while claiming
the other. **Prompt defenses** work *inside the model's channel*:
marking, delimiting, instruction-priority training — making the
model itself distinguish trusted from untrusted text.
**Authorization boundaries** work *outside the model*: capabilities,
provenance tags, argument policies, consent gates — making the
system safe regardless of what the model believes. The comparison
fixes what each family can and cannot promise, because the most
common deployment error is paying for one and relying on the other.

## What prompt defenses claim — and their measured shape

The instruction-hierarchy family trains priority separation into
the model, with reported robustness gains including on unseen
attacks [SRC-PAPER-052]. The spotlighting family transforms
untrusted input to carry a provenance signal, with the celebrated
>50% → <2% attack-success reduction on evaluated GPT-family models
[SRC-PAPER-053]. Both are real effects with real numbers — and both
are **behavioral**: they are properties of a training run or a
prompting convention, priced on an evaluated attack set, and
carried with exactly the qualifiers Chapter 13 taught: version
fragility (fine-tunes and updates move trained priorities silently),
adaptive pressure (optimized suffixes are designed to defeat
instructions [SRC-PAPER-004]), and the interval discipline
("under 2%" at 2/100 is [0.6%, 7.0%], a point estimate's costume).
The deepest limit is structural, not empirical: there is "no known
reliable way to have an LLM follow instructions in one category of
text while safely applying those instructions to another category of
text" [SRC-REPORT-007] — the prompt-defense family is a search for
the best approximate exception to that sentence, and every measured
number is bounded by it.

## What authorization boundaries claim — and their measured shape

The boundary family changes the question from *will the model
misbehave?* to *what can a misbehaving model actually reach?* The
MCP specification states the boundary condition in its own security
principles: tool descriptions are untrusted, enforcement lives in
the host, not the protocol [SRC-REPORT-005]. CaMeL demonstrates the
strongest form — untrusted data cannot influence unauthorized flows
*by construction* — at a measured utility price (77% of AgentDojo
tasks with provable security vs 84% undefended [SRC-PAPER-054]).
The tool-poisoning demonstration shows where boundaries must sit:
the attack ships as *untrusted text in the capability channel*
itself [SRC-REPORT-006]. This course's P07 implements the family at
fixture scale and prices it honestly: 6 of 8 scripted attack classes
blocked (paired sign test p = 0.0156) at a benign cost of 1 of 8,
with two residual classes that are *properties of the approach, not
implementation accidents* — the authored-policy gap and consent
decay. That honesty is the family's signature: boundaries fail
legibly (a blocked call, a consent screen) and their failures have
names.

## The comparison, fixed

| Dimension | Prompt defenses | Authorization boundaries |
|---|---|---|
| Where they live | in the model (training or prompting) | in the host (architecture and policy) |
| Trust assumption | the model can learn to privilege trusted text, approximately | the model may be fully compromised; the system holds anyway |
| Evidence genre | behavioral rates on attack sets, version-dated | architectural properties + measured utility/cost ledgers |
| Best measured effect | >50% → <2% ASR for spotlighting [SRC-PAPER-053]; unseen-attack gains for hierarchy [SRC-PAPER-052] | provable security at 77%-vs-84% utility [SRC-PAPER-054]; P07's 6/8 at p=0.0156 |
| Adaptive pressure | direct — the defense *is* model behavior; optimization targets it [SRC-PAPER-004] | indirect — attacks aim at policy gaps and consent decay (P07's residuals) |
| Failure mode when it fails | silent: the injection succeeds and the call fires | legible: a block, a consent prompt, a named residual class |
| Cost profile | cheap to deploy, expensive to verify (must re-evaluate per version/attack set) | expensive to build and author policies, cheap to verify (the matrix is the coverage claim) |
| What it cannot promise | immunity (the no-known-reliable-way sentence) | correct goals (proofs cover flows, not intent; humans rubber-stamp consent) |
| OWASP mapping | LLM01 mitigations within the model channel | LLM01/LLM05/LLM06 containment at the system edge [SRC-REPORT-004] |

## When the comparison decides something

1. **"We have prompt-injection mitigations" as a launch gate.** The
   comparison's answer: a launch gate needs a *boundary* claim —
   what can a successful injection reach? A prompt defense can
   lower the rate; it cannot bound the blast radius, and a launch
   decision is a blast-radius decision. Ch. 13's verdict ("prompts-
   as-defense fails as a category") is about *gates*, not about
   *layers*.
2. **Defense-in-depth ordering.** The families compose, but the
   order matters: boundaries outside, prompt defenses inside. A
   boundary without behavior defenses pays a consent/monitoring tax
   on every ambiguous call (P07's cost row); a prompt defense
   without boundaries has no floor when the behavior fails — and
   behavior fails silently, which is the property that makes it the
   wrong innermost-or-outermost choice.
3. **Red-team scoping.** Ch. 15's engagement design differs per
   family: prompt defenses are evaluated as rates on attack
   batteries with version pinning and adaptive phases; boundaries
   are audited as coverage (does the matrix name every tool? is
   every capability-reference argument declared?) plus targeted
   attempts at the named residual classes. A vendor report that
   evaluates one family's claims with the other family's method is
   mismatched — rate-testing a proof, or coverage-auditing a
   behavior — and the mismatch is detectable in the report's
   methodology section.

## Non-claims

This note does not claim boundaries are strictly superior: the
utility price of capability layers is real and measured
[SRC-PAPER-054], the policy-authoring burden is real (P07's gap
scenario is the worked case), and prompt defenses demonstrably
reduce attack success on their evaluated sets. Nor does it claim
the two families are the whole space: isolation/sandboxing and
monitoring (Ch. 08) are adjacent answers with their own ledgers.
All cited numbers remain at their register access levels; nothing
here re-executes a cited system. The final comparison note (C05,
planned) prices static benchmarks against adaptive evaluation —
the evidence-side counterpart of this defenses-side comparison.
