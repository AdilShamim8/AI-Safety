# Progress tracker — AI (safety) engineer (evaluations & assurance route)

**What this is:** the step-by-step milestone checklist for the
[evaluations & assurance route](../evaluations-and-assurance.md) —
artifact-gated progress for the engineer who ships systems with
safeguards, monitors, and release gates. Same discipline as the
[researcher](alignment-research.md) and
[security](ai-security-engineering.md) trackers: every checkbox
names its evidence, every milestone ends in self-audit, the fork's
commit history is the record. Compact version:
[careers index](../careers-index.md#progress-tracking--the-step-by-step-ladder).

**The engineer's special discipline:** your artifacts are *running
systems with stated price tags* — a guardrail without latency and
false-positive budgets is a screenshot, not a control. Every
milestone below demands the honest-cost half along with the
capability half.

## M0 — Orientation (shared, ~1 week)

- [ ] [START_HERE](../../START_HERE.md) read; [diagnostic](../../prerequisites/diagnostic.md) taken; R1–R5 gaps listed
- [ ] [Ch.01](../../chapters/01-risk-models-and-research-epistemics/README.md) completed; one risk hypothesis with weakening observations
- [ ] Repo runs green; schedule blocked
- [ ] The [judge's audit](../../planning/SESSION2_JUDGE_AUDIT.md) skimmed

**Self-audit:** What is a safety claim's context-relativity, and why
does re-using one across deployments void it? What are my three
biggest prerequisite gaps?

## M1 — The spine (shared, ~4 weeks)

- [ ] [Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md) completed; preregistered evaluation plan written
- [ ] P01 harness smoke tier green — I can run the evaluator end to end and read its reports
- [ ] First paper note published — suggestion: [note 41](../../research/notes/41-model-written-evaluations.md) (instrument circularity: your guard inherits your blindness) or [note 49](../../research/notes/49-helm.md) (the multi-metric grid as the anti-Goodhart instrument)
- [ ] One dataset card studied — suggestion: [Do-Not-Answer](../../datasets/cards/24-do-not-answer.md) (the refusal side of the pair) or [PKU-SafeRLHF](../../datasets/cards/25-pku-saferlhf.md) (decoupled axes for tuning trade-offs)

**Self-audit:** Why does a single-metric dashboard launder Goodhart
detachments? What did the model-written-evals note say agreement
numbers *cannot* detect?

## M2 — Calibration and selective prediction (the engineer's fork, ~5 weeks)

- [ ] [Ch.06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md) + [notes 46](../../research/notes/46-factscore.md)/[47](../../research/notes/47-selfcheckgpt.md)
- [ ] P03 completed: the calibration/selective-prediction audit — reliability tables, ECE with its binning, risk-coverage curves, abstention ledger with BOTH sides (selective risk + false-abstention rate)
- [ ] [note 32](../../research/notes/32-verbalized-confidence.md): the channel the model can be taught to fake — my monitor stack does not rely on it alone
- [ ] [Incident 04](../../research/notes/incidents/04-google-ai-overviews-eat-rocks.md) reviewed: the abstention gap at search scale; my writeup states what P03's threshold policies would have caught
- [ ] [Incident 06](../../research/notes/incidents/06-cursor-invented-policy.md) reviewed: confabulation on an authoritative channel; my design routes policy questions to pinned sources, not priors

**Self-audit:** What is ECE's binning dependence, and why does the
course pin it by test? What are the two sides of the abstention
ledger? Where does my stack's abstention signal come from?

## M3 — Control and monitoring (the differentiator, ~4 weeks)

- [ ] [Ch.08](../../chapters/08-ai-control-and-monitoring/README.md) + [note 01](../../research/notes/01-ai-control.md)
- [ ] P08 completed: the control-protocol study — trusted/deferred policy comparison, halt semantics, the safety-utility frontier at a stated budget
- [ ] [notes 38](../../research/notes/38-unfaithful-explanations.md)/[43](../../research/notes/43-measuring-cot-faithfulness.md): CoT monitoring's task-conditionality — my monitor validation includes the intervention check
- [ ] One monitor-hold design written: what trips it, what it holds, who releases, in four sentences
- [ ] The honesty ledger's not-executed tiers: I can name which parts of my own stack are untested at model tier, in writing

**Self-audit:** What does a safety-utility frontier price? Why is
"reads the CoT" a monitor with a documented blind spot? What would
trip my hold on a persona-drift failure ([incident 11](../../research/notes/incidents/11-bing-sydney-persona-collapse.md))?

## M4 — Reliability and release engineering (~4 weeks)

- [ ] [Ch.17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md) + [note 39](../../research/notes/39-lost-in-the-middle.md) (position subgroups) + [note 48](../../research/notes/48-inverse-scaling.md) (upgrade drift)
- [ ] [Ch.22](../../chapters/22-safety-engineering-and-assurance/README.md) completed
- [ ] P09 completed: the shift/subgroup reliability audit with Wilson intervals per slice
- [ ] One release-gate design written in safety-case grammar: claims, evidence, residuals, the behavior-changing-release trigger
- [ ] [Incident 02](../../research/notes/incidents/02-dpd-chatbot-update-regression.md) reviewed: behavior-changing releases need behavioral regression gates — my design has one

**Self-audit:** Which slice of my last audit would the position
subgroup have changed? What makes a release "behavior-changing" and
what does my gate do about it? Where is my inverse-scaling blind
spot (which capability might degrade in the next upgrade)?

## M5 — The dossier and the market step (~4 weeks)

- [ ] [Ch.23](../../chapters/23-governance-and-standards/README.md) completed
- [ ] P10 capstone dossier: harness → calibration → control → shift → release-gate, the full integration artifact
- [ ] [comparison 06](../../research/notes/comparison-06-safety-cases-vs-red-team-reports.md): assurance's two documents — I know which one I write
- [ ] The [MAINTENANCE](../../MAINTENANCE.md) operating discipline applied to my own stack: freshness checks, drift schedule, standing instruments
- [ ] [first-90-days.md](../first-90-days.md) engineer weeks completed with Friday artifacts

**Self-audit:** Can I hand a stranger the dossier and have them
audit my strongest claim in ten minutes? What is my residual
coverage field's honest content? Which gate would have caught
MyCity ([incident 05](../../research/notes/incidents/05-nyc-mycity-chatbot.md)), and can I say why?

## What this tracker does not promise

No "certified AI engineer" plaque: the artifact trail is the
portfolio. Latency and false-positive budgets are stated per
control or the control is not done. The market snapshot in the
[careers index](../careers-index.md) is dated — re-check before
quoting.
