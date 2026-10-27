# Progress tracker — AI safety researcher (alignment research route)

**What this is:** the step-by-step milestone checklist for the
[alignment research route](../alignment-research.md) — the owner's
ask: a way to *track progress as you gain expertise*, artifact by
artifact, not hour by hour. Every checkbox names its evidence; when
you can show a stranger the artifact, the box is done. The compact
ladder lives in the [careers index](../careers-index.md#progress-tracking--the-step-by-step-ladder);
this file is the expanded, route-specific version. Copy it into your
fork and tick as you go — your commit history IS the progress record.

**How to self-audit each milestone:** after ticking every box in a
milestone, answer the three questions at its end out loud (or in
writing in your fork). If you cannot, you have read without doing —
the first honest failure mode — and the milestone is not done.

## M0 — Orientation (shared with all routes, ~1 week)

- [ ] [START_HERE](../../START_HERE.md) read; [diagnostic](../../prerequisites/diagnostic.md) taken; my R1–R5 gap list written down
- [ ] [Ch.01](../../chapters/01-risk-models-and-research-epistemics/README.md) completed; one threat hypothesis written with pre-stated weakening observations
- [ ] Repo runs: `uv sync && uv run pytest` green on my machine
- [ ] Schedule chosen ([study-schedules.md](../study-schedules.md)) and calendar blocked
- [ ] The [judge's audit](../../planning/SESSION2_JUDGE_AUDIT.md) skimmed — I know what this repo has verified and what it has honestly not

**Self-audit:** Can I state my threat hypothesis's *weakening
observations* without looking? Can I say what the honesty ledger is
for? What is my biggest prerequisite gap, in one sentence?

## M1 — The methodological spine (all roles, ~4 weeks)

- [ ] [Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md) completed; one preregistered evaluation plan written (construct, gap sentence, splits, interval plan)
- [ ] P01 harness smoke tier green: runner + scorer validation reproduced
- [ ] First paper note published in my fork with its falsifiable extension — suggestion: [note 33](../../research/notes/33-concrete-problems.md) (the founding taxonomy) or [note 49](../../research/notes/49-helm.md) (evaluation as coverage)
- [ ] One [dataset card](../../datasets/README.md) studied end-to-end — suggestion: [FEVER](../../datasets/cards/33-fever.md) (evidence-anchored labels, 185,445 claims, the NotEnoughInfo class)
- [ ] The Wilson-interval habit: every rate I have reported this month carries its interval and denominator

**Self-audit:** Can I write a gap sentence for a score I computed?
Can I say why grouped splits matter for agent evals? Which of my
numbers this month had no denominator?

## M2 — Specification and preference (the researcher's fork, ~5 weeks)

- [ ] [Ch.03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) + [note 37](../../research/notes/37-reward-overoptimization.md) (Goodhart's curve, measured)
- [ ] [Ch.04](../../chapters/04-preference-learning-and-post-training/README.md) + [note 42](../../research/notes/42-helpful-harmless-rlhf.md) (the RLHF baseline and the √KL price)
- [ ] P02 completed: proxy-vs-gold sweep with the peak-and-fall pinned and honestly interval'd
- [ ] P04 completed: preference-optimization audit with paired metrics (helpfulness AND harmlessness, never one alone)
- [ ] [PKU-SafeRLHF card](../../datasets/cards/25-pku-saferlhf.md) studied: the decoupled-axes design and why it matters for the audit
- [ ] One Goodhart-style result written up with honest intervals and the falsifier stated

**Self-audit:** Can I draw the overoptimization curve and say what
moves its peak? What does the √KL relation price, and what kind of
claim is it (empirical, not theorem)? Where did my P02 result
honestly not execute?

## M3 — Oversight and honesty (the researcher's differentiators, ~4 weeks)

- [ ] [Ch.05](../../chapters/05-scalable-oversight/README.md) + [note 10](../../research/notes/10-weak-to-strong.md)
- [ ] [Ch.06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md) + [notes 46](../../research/notes/46-factscore.md)/[47](../../research/notes/47-selfcheckgpt.md) (the factuality instrument cabinet)
- [ ] P03 completed: calibration/selective-prediction audit with the abstention ledger's both sides
- [ ] [Incident 04](../../research/notes/incidents/04-google-ai-overviews-eat-rocks.md) reviewed: the abstention gap at search scale — I can say what P03 would have caught
- [ ] Two more paper notes on the route's list, each with its falsifiable extension run at deterministic tier

**Self-audit:** Can I explain why FActScore measures agreement with
a named source, not truth? What passes a SelfCheck-style consistency
filter that a reference check would catch? Which incident-teaching
maps to which instrument?

## M4 — Interpretability (the researcher's depth, ~4 weeks)

- [ ] [Ch.09](../../chapters/09-mechanistic-interpretability-foundations/README.md) + [notes 34](../../research/notes/34-emergent-world-representations.md)/[50](../../research/notes/50-induction-heads.md) (probe-plus-intervention; the six-argument ladder)
- [ ] [Ch.10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md) + [Ch.11](../../chapters/11-behavioral-steering-and-representation-interventions/README.md)
- [ ] P06 completed: the causal-interpretability study with the instrument battery (probes, patching grid, controls, deployment-flip)
- [ ] [CounterFact/ROME card](../../datasets/cards/31-counterfact-rome.md) studied: causal editing's evaluation design
- [ ] The readout-is-not-causation warning: I can name the probe accuracy P06 pins on the spurious channel (0.915) and what settled the question instead

**Self-audit:** Can I walk the evidence ladder
(correlation→perturbation→ablation→mechanism) with one example from
each rung? What is a latent-move intervention, and why is it
stronger than ablation? What did the phase change teach about
checkpoint evals?

## M5 — Deception and evaluation-awareness (the frontier literacy, ~3 weeks)

- [ ] [Ch.07](../../chapters/07-deception-scheming-and-evaluation-awareness/README.md) + [note 40](../../research/notes/40-taken-out-of-context.md) (capability + incentive, no malice needed)
- [ ] [notes 12](../../research/notes/12-alignment-faking.md)/[23](../../research/notes/23-ai-sandbagging.md) (the behavioral evidence)
- [ ] The causal chain written in my own words: capability (out-of-context reasoning) + incentive (testing gates deployment) + expression (sandbagging/alignment-faking)
- [ ] [Incident 11](../../research/notes/incidents/11-bing-sydney-persona-collapse.md) reviewed: persona drift as context pressure — related but distinct from deception

**Self-audit:** Can I say what situational awareness is *without*
anthropomorphism? Why does eval leakage become a safety concern at
the gate level? What is the honest access level of my knowledge
here (abstract-level for which notes)?

## M6 — Research practice and the market step (~4 weeks)

- [ ] [Ch.24](../../chapters/24-research-practice-and-capstone-execution/README.md) completed; research proposal drafted per its template
- [ ] P06 or P02 chosen as the capstone companion; the dossier assembled
- [ ] Ten+ paper notes published in my fork (the public trail — quality over count, but count is the floor)
- [ ] P10 capstone dossier: the integration artifact — assurance case, evidence, honest residuals
- [ ] [first-90-days.md](../first-90-days.md) week-13 checkpoint met: things I can hand a stranger

**Self-audit:** If an interviewer asks "show me a result you
falsified," do I have one? Can I defend my dossier's weakest claim
in one honest sentence? What is my not-executed tier, stated
plainly?

## What this tracker does not promise

No certification, no completion certificate, no employment
guarantee. The market-signal sources
([careers index](../careers-index.md)) are dated snapshots; the
tracker's promise is narrower and real: **every ticked box is an
artifact a stranger can audit**, which is the only progress that
counts in this field.

### Watching checkpoints (alignment route)

- [ ] Primer: DeepMind course end-to-end (85 min) — before Ch. 01
- [ ] Alongside: CS 2881 L1 (both iterations) with Ch. 01–02
- [ ] Alongside: CS 2881 L2/L4 + DeepMind P2.1 with Ch. 03–04
- [ ] Alongside: CS 2881 L8 + Under Pressure with Ch. 07–08
- [ ] Alongside: CS 2881 L10 with Ch. 09–11
- [ ] Self-check: the CS 2881 and DeepMind self-assessments
