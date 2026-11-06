# The system-design bank — eval-and-safety pipelines under constraints

**Navigate:** [← questions](README.md) · [safety engineer](../roles/safety-engineer.md)

**What this round is.** The senior round: design a system that
evaluates, monitors, and decides — with the constraints stated, not
hidden. This corpus trains it directly: the P01→P10 arc is a
harness-to-dossier pipeline, and the capstone
([P10](../../projects/p10-capstone-agent-evaluation-and-assurance-dossier/README.md))
is the round in project form.

## The three canonical prompts

**Prompt A — "Design an evaluation pipeline for a model being
deployed to customers."**
The house skeleton, in order:
1. **Threat/scope model first** (what is this system trusted with —
   the OWASP/ATLAS surfaces if it is an app; the capability families
   if it is a model).
2. **The harness** ([P01](../../projects/p01-evaluation-harness/README.md)):
   cases, baselines, paired ledgers, intervals. Name the determinism
   requirement.
3. **The decision layer**: go/no-go criteria fixed in advance — the
   preregistration habit applied to deployment.
4. **Monitoring**: what is watched post-launch, what triggers
   rollback ([P08](../../projects/p08-control-and-monitoring-protocol/README.md)
   is the pattern).
5. **The honest tiers**: what this design does not cover, stated on
   the diagram itself.

**Prompt B — "Add a monitoring system that catches what the evals
missed."**
The P09 lesson as a design principle: aggregate dashboards hide
subgroup failures — design the decomposition in. Answer includes
drift detection and the escalation path, with an explicit
"what monitoring cannot see" section.

**Prompt C — "We need this in production next month with half the
eval coverage you asked for."**
The round's real test: the honest tier negotiation. State what
coverage buys what confidence, which slices are non-negotiable (name
them — injection, subgroup reliability), and what the reduced plan
monitors more heavily instead. The [honesty round](honesty-round.md)
answers live here; the engineers who pass this prompt are the ones
who refuse to let the date edit the evidence.

## The grading shape

Every system-design answer in this bank ends with the diagram's own
boundary: what the design covers, what it does not, and what would
have to be true to change it. That closing move is why this corpus's
graduates draw the boundary before being asked.
