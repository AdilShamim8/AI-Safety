# The coding bank — the deterministic projects as exercises

**Navigate:** [← questions](README.md) · [take-homes](../takehomes/README.md)

**How this bank works.** The ten projects are already
deterministic, offline, stdlib-first — which makes them ideal
interview material: you can run them anywhere, and so can the
interviewer.

## The exercises

**E1. "Build an evaluation harness from scratch."**
[P01](../../projects/p01-evaluation-harness/README.md) is exactly this;
the [example report](../../projects/p01-evaluation-harness/example-report.md)
shows the house format. Probe: "what do you report besides the mean?"
— paired ledgers and intervals, every time.

**E2. "Demonstrate reward misspecification."**
[P02](../../projects/p02-reward-misspecification-and-generalization/README.md):
the reward function the agent optimizes is not the one you meant —
shown, not asserted.

**E3. "Measure calibration honestly."**
[P03](../../projects/p03-calibration-truthfulness-and-abstention/README.md).
Probe: "your abstention threshold trades coverage for precision —
where do you set it and why?" The answer is a curve, not a number.

**E4. "Audit a preference dataset."**
[P04](../../projects/p04-preference-optimization-audit/README.md).

**E5. "Show weak-to-strong in miniature."**
[P05](../../projects/p05-weak-to-strong-or-scalable-oversight-analogue/README.md).

**E6. "Find a causal feature."**
[P06](../../projects/p06-causal-interpretability-study/README.md) —
intervention, not correlation; the probe is always "how do you know
the intervention is the cause?" (controls, held-out checks).

**E7. "Defend against prompt injection."**
[P07](../../projects/p07-injection-defense/README.md) — the
registered OWASP LLM01 is the named threat; the defense must say what
it does not stop.

**E8. "Design a control protocol."**
[P08](../../projects/p08-control-and-monitoring-protocol/README.md).

**E9. "Expose a subgroup failure your aggregate hides."**
[P09](../../projects/p09-shift-subgroup-reliability/README.md) — the
project that exists because averages lie.

**E10. "Write an assurance dossier."**
[P10](../../projects/p10-capstone-agent-evaluation-and-assurance-dossier/README.md)
— the capstone: evaluation, monitoring, go/no-go, and the honest
tiers in one document.

**The rule that grades all of them.** Every exercise ends the same
way in this corpus: what was run, what was not run, and the pinned
result. An interviewer who sees that habit has seen the whole course.
