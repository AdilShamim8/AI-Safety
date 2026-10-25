# Comparison 12 — evaluation supply: model-written breadth vs human-curated depth

**The practitioner's question:** I need eval coverage faster than
my annotation budget — do I generate evaluation items with models
or keep paying humans?

**The sources:** [model-written evaluations
(note 41)](../notes/41-model-written-evaluations.md) (the generation
method, its 90–100% agreement validation, and the blind-spot
caution), [HELM (note 49)](../notes/49-helm.md) (coverage-with-
named-holes as the reporting standard), and the catalog's own cards
as instances of each supply strategy — model-written suites
(AgentDojo's generated tasks, Do-Not-Answer's curated set)
alongside human-curated anchors (TruthfulQA, FEVER). Mixed access
levels as usual; the comparison is priced accordingly.

## 1. What each supply strategy actually buys

| | Model-written supply | Human-curated supply |
|---|---|---|
| Cost curve | marginal cost near zero; breadth scales with generation | linear in annotator hours |
| Coverage shape | inherits the generator's imagination — broad where the prior is rich, empty where it is blind | broad where the funders' attention is; slow into novel territory |
| Label quality | agreement can match or beat human-written (the note's 90–100%) | agreement is what it is — but *disagreement is informative* (annotator conflicts surface genuine ambiguity) |
| The blind spot | **omitted question classes are invisible to every label metric** — agreement measures given-exists, not exists | omissions are visible to funders' hindsight (and to auditors asking "who decided this scope?") |
| Provenance | the instrument is made of the measured system class — circularity risk is structural | the instrument is made of humans with known incentives (also circular, differently) |
| Register instances | AgentDojo's extensible tasks; StrongREJECT's rubric generation | FEVER's blinded three-way labels; TruthfulQA's adversarial categories |

## 2. The real trade is *where the blind spot lives*

Human curation's blind spot is **fundable**: evaluation exists
where someone paid attention — the bias is socio-economic and
*auditable* (ask who funded the dataset, read the five-provenance
questions, see the gap). Model-written supply's blind spot is
**distributional**: evaluation exists where the generator's prior
is dense — the bias is statistical and *invisible to the method's
own quality metrics*, because label agreement cannot detect an
example that was never generated. The note-41 extension's
coverage-vs-agreement ledger is the instrument that makes the
second blind spot measurable at all.

The trap in both directions: model-written evals quoted with
crowdworker agreement as though agreement certified coverage
(it certifies labels-given-existence); human-curated evals quoted
as "gold standard" as though funding attention were coverage (it
is attention). HELM's discipline — name the omissions in writing —
is the reporting standard that covers both, and the course's
registers apply it uniformly: every catalog card's "what this
dataset cannot support" section is the omissions list in miniature.

## 3. The hybrid the field actually runs

Production evaluation stacks are layered by supply: a
**human-curated core** for the constructs where label ambiguity
itself is the signal (factuality's three-way labels, refusal
quality's judgment calls); **model-written breadth** for coverage
sweeps where the failure mode is sparse and the label is cheap
(injection payloads, jailbreak augmentation families — AgentHarm's
440 = 110×augmentation shape); and **dynamic environments**
([AgentDojo, card 30](../../datasets/cards/30-agentdojo.md)) where
the supply question dissolves into "can you generate *and* defend*
faster than the adversary iterates." The layering rule: the more
the construct depends on human judgment ambiguity, the more the
core stays human; the more it depends on enumeration breadth, the
more it goes to generation — and the coverage ledger runs on every
layer either way.

## 4. The falsifiable resolution (deterministic tier)

The coverage-inheritance experiment (note 41's extension) is this
comparison's instrument: generator A produces a class-distributed
case set; generator B (trained on A's output) extends it; measure
B's class coverage against A's frequency distribution. Prediction:
coverage concentrates on A's frequent classes while B's *label*
agreement stays flat — supply bias inherited, quality metrics
silent. The human-curated arm's parallel: have a "funding"
manipulation (drop one class from A entirely) and observe B never
discovers it — the invisible-omission property, demonstrated.
Falsifier: uniform B coverage, or B discovering the dropped class,
would show inheritance is weaker than the note claims in this
synthetic world.

## 5. Bottom line

Generate for breadth, curate for judgment, run the coverage ledger
on both, and publish the omissions list with whatever supply you
chose — the honest eval names what it did not generate *and* what
nobody paid to ask. Agreement numbers certify labels; only the
ledger certifies coverage; only the omissions list certifies
honesty.
