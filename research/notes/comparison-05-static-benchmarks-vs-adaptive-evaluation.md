# Comparison note C05 — Static benchmarks vs adaptive evaluation: what each evidence kind is for

> Comparison notes: 5 of 5 planned — the planned comparison-note set
> is complete with this note. Sources: SRC-PAPER-045 (Madry et al.,
> abstract-read), SRC-PAPER-046 (Goodfellow et al., abstract-read),
> SRC-PAPER-047 (Carlini & Wagner, abstract-read — the 100% vs 0.5%
> case), SRC-PAPER-048 (Croce & Hein, abstract-read — the 50+-defense
> audit), SRC-PAPER-004 (GCG, abstract-read), SRC-PAPER-055
> (AgentDojo, abstract-read), SRC-PAPER-056 (ToolEmu, abstract-read),
> SRC-PAPER-061 (XSTest, abstract-read), SRC-PAPER-058 (Ganguli red
> teaming, abstract-read), SRC-PAPER-059 (Perez LM-vs-LM,
> abstract-read). Companion chapters: 02 (construct validity,
> contamination, adaptive overfitting), 12 (the two canonical
> evaluation failures), 15 (the engagement that composes both).

## The question a comparison exists to answer

Every safety number in this course came from one of two instruments,
and confusing them is the field's most reliable way to publish a
wrong claim. **Static benchmarks** are fixed case sets with fixed
labels — XSTest's 250 safe / 200 unsafe prompts [SRC-PAPER-061],
ToolEmu's 36 tools and 144 cases [SRC-PAPER-056], AgentDojo's 97
tasks and 629 security cases [SRC-PAPER-055]. **Adaptive
evaluation** is an adversary who iterates against the *system or
defense being evaluated* — optimized suffixes [SRC-PAPER-004], the
red-team engagement of Chapter 15, the attack-the-defense phase.
The two instruments answer different questions, degrade
differently, and compose into the only evaluation stack this course
certifies.

## What static benchmarks are for — and how they rot

A static benchmark's virtue is exactly its fixity: comparability
across systems and time, cheap repeated runs, and construct control
(the ten XSTest prompt types isolate *which* exaggerated-safety
failure mode fires [SRC-PAPER-061]). Its rot is the same fixity:
once a benchmark is public and aspirational, systems train against
it — contamination and adaptive overfitting in Chapter 02's sense —
and the number measures benchmark-specific competence, not the
construct. The red-teaming literature adds the coverage ceiling:
static suites enumerate an attack space that has no closure, so a
clean run bounds only the attempted family (Ch. 15's discipline;
AgentDojo's own framing as a *dynamic, extensible* environment is
the field's acknowledgment that static alone is insufficient
[SRC-PAPER-055]).

## What adaptive evaluation is for — and how it dies

Adaptive evaluation prices what benchmarks cannot: robustness under
an adversary who *reads the defense*. Its record is the graveyard
Chapter 12 walks through: distillation's claimed 0.5% attack
success against 100% under Carlini-Wagner's adaptive attack
[SRC-PAPER-047]; Croce-Hein's audit of 50+ defended models finding
nearly every robustness claim overestimated, often by more than 10
points [SRC-PAPER-048]. Its failure modes are cost and authority:
adaptive work is expensive (human red teamers [SRC-PAPER-058],
attack models [SRC-PAPER-059], optimization runs [SRC-PAPER-004]),
and its results are only as strong as the attacker's authorization
and the oracle's validity — an adaptive attack that is weak, or a
judge that is gameable, manufactures false confidence with more
machinery than a static run ever assembles.

## The comparison, fixed

| Dimension | Static benchmarks | Adaptive evaluation |
|---|---|---|
| Question answered | "does the system meet a fixed, comparable bar?" | "does it survive an adversary who knows the defense?" |
| Comparability | high — same cases, same labels, across time | low — each engagement is bespoke; only the *protocol* transfers |
| Cost | low, repeatable | high, per-target |
| Rot mode | contamination and tuning-to-the-suite | attacker-budget and oracle-validity limits |
| Signature failure | a high score that tracks the suite, not the construct | a clean report whose attacker was underpowered |
| Canonical evidence | XSTest failure modes [SRC-PAPER-061]; ToolEmu rates [SRC-PAPER-056] | the 0.5%-vs-100% collapse [SRC-PAPER-047]; the 50+-model audit [SRC-PAPER-048]; transferable suffixes [SRC-PAPER-004] |
| What it can never give | absence of novel failure | comparability across systems |
| This course's worked form | P01/P03 case sets; P07's paired fixtures | P07's residual-class scenarios; Ch. 15's Meridian engagement |

## The composition rule

The instruments compose in a fixed order, and the order is the
finding: **static first, adaptive second, claims partitioned.** A
static suite establishes the floor and the failure-mode vocabulary;
the adaptive phase attacks whatever the defense claims; the report
scopes every number to its instrument — "meets the fixed bar" and
"survived the declared adversary" are different sentences, and
neither licenses the other. The Madry framing of evaluating against
a *first-order adversary* [SRC-PAPER-045] and the linear-explanation
account of why adversarial examples exist at all [SRC-PAPER-046]
supply the theory; the two Chapter 12 failures supply the cautionary
tales; Chapter 02 supplies the construct-validity grammar that keeps
either instrument honest about what it measures.

## Non-claims

This note does not claim static benchmarks are obsolete — they are
the only comparability instrument the field has — nor that adaptive
evaluation is automatically more truthful: an underpowered adaptive
phase launders more confidence than any benchmark. All numbers
remain at their register access levels. With C05, the planned
five-note comparison set (C01–C05) is complete; the register's
comparison coverage now spans preference learning (C01), evidence
kinds (C02), safety paradigms (C03), defense families (C04), and
evaluation instruments (C05).
