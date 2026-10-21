# Ch. 01 — Exercises

(The prompts live in the chapter [README](README.md) §8; this file keeps the
full worked solutions separate so the prompts stay uncontaminated for
assessment use.)

## Solution 1.1 — agentic credential exfiltration

### (a) Six-primitive decomposition

First, narrow the context — "agents in general" has no stable propensity, so
no measurable claim. Chosen context κ: **an internal developer-productivity
agent** with a repo/file workspace, a web-search tool, and an email/PR
comment tool, running inside a company CI/dev VM where `.env` files with
live service credentials exist on disk.

- **Hazard h:** live credentials leave the trust boundary (attached to
  outbound email / posted in public PR comment / embedded in web-search
  query string).
- **Capability:** the agent can (i) read files containing secrets (fs read
  in workspace), (ii) emit content on outbound channels (email/PR/HTTP).
  Both are *design* facts, not model properties — measurable by tool
  inventory, not by behavioral eval.
- **Propensity:** the rate at which the model, in context κ, actually
  chooses to place secret-looking content into outbound channels, per
  opportunity. This is the behavioral unknown — and note it is *not*
  adversary-free: an attacker who can influence task text or retrieved web
  content (Ch. 13) optimizes this rate.
- **Exposure:** which credentials (blast radius per secret), which outbound
  surfaces are reachable, whether egress logging exists.
- **Severity:** secret class → compromise cost (a scoped API key vs
  production DB creds), times recovery (rotation latency).
- **Pathway p:**
  `secret on disk → agent reads it (capability+propensity) → no egress
  content inspection (opportunity) → outbound channel (exposure) →
  credential use by adversary (severity realized)`.

### (b) Threat hypothesis

> **H:** In context κ (dev VM, live `.env` files, email + web tools, no
> egress inspection), the agent emits secret-bearing outbound content at a
> rate causing ≥1 exfiltration event per 10k tasks (τ = once per ~2 years
> at observed task volume).
>
> **Weakening observations (pre-stated):**
> - **w1 (leading):** in 1,000 instrumented tasks where a synthetic secret
>   is planted in the workspace and task text tempts inclusion of "relevant
>   config," zero outbound messages contain the secret → capability∧
>   propensity link weakens (with synthetic-secret methodology documented —
>   planted values only, per RESPONSIBLE_RESEARCH.md).
> - **w2 (mechanism):** egress inspection on outbound email/PR bodies
>   matches planted secret patterns with recall ≥ 0.99 on a validation
>   corpus → opportunity link weakens to "only novel encodings pass."
> - **w3 (structural):** secret files are not in the agent's readable scope
>   (capability removed at the authorization layer, not the prompt) →
>   capability link severed; residual risk becomes "authorization layer
>   misconfiguration," a different and more testable hypothesis.

### (c) Evidence classification

- **(i) Incident report — agent emails `.env`:** kind: documented incident.
  Bears on: *feasibility of the full pathway* (all links at once, once,
  somewhere). Does not establish: rate in κ, or that κ's controls resemble
  the incident's. Strongest legitimate use: hazard-inventory justification —
  the pathway is not hypothetical. It is one sample, from a different
  deployment shape; treat its severity as a floor, not an estimate.
- **(ii) Benchmark, 3% of agentic episodes attempt exfiltration:** kind:
  benchmark result. Bears on: *propensity under the benchmark's
  distribution* — which was built to tempt exfiltration (attack-scaffolded
  prompts, planted secrets). Does not establish: propensity in κ, where
  task text is ordinary; benchmark-to-deployment propensity transfer is
  exactly the construct-validity gap Ch. 02 exists to police. Legitimate
  use: upper-bound stress estimate and prioritization, *labeled as such*.
- **(iii) Theorem — bounded-read agents cannot write outside a sandbox:**
  kind: formal result. Bears on: *capability/opportunity links, under the
  theorem's assumptions* (the sandbox actually enforces the bound; "read"
  and "write" cover the channels that matter — note email is an
  *application-level* write the sandbox may not model). Does not establish:
  anything about propensity, or about deployments where the assumption
  fails. The classic misuse is treating it as a deployment guarantee; the
  correct use is: if the assumption holds, one pathway link is *severed*,
  and effort shifts to verifying the assumption (which is a measurement,
  not a proof).

### Grading rubric (assessor)

Full credit requires: κ narrow enough for stable propensity (most common
failure: vague context); weakening observations that are observations
(measurements with outcomes), not restatements of the hypothesis; at least
one *leading* indicator; each evidence item answered in three parts (bears
on / establishes / does not establish); the incident treated as feasibility
not frequency; the benchmark's distribution-dependence named; the theorem's
assumption-conditional status named.

## Solution 1.2 — measurement design

Worked through for the "silent queue degradation" hazard of the chapter's
invoice assistant (H4), since it is the kind of worry that never becomes a
number otherwise. The same shape transfers to any deployment you know.

**Worry, restated:** since σ was deployed, human operators approve σ's
`flag-for-human` items with less scrutiny — σ's flags become rubber-stamped,
so ambiguous invoices route to a backstop that no longer backs anything.

**Sampling unit:** the *flagged invoice* (not the prompt, not the day).
Approval decisions by the same operator within a week are correlated
(fatigue, batching, trust spillover), so the effective n is smaller than
the count of invoices; a cluster-aware analysis (operator-week as a second
level) is the honest form. Denominator: all flagged invoices, split by
`flag reason` stratum — the ambiguity stratum is where the worry lives.

**Measurement:** per flagged invoice, time-to-approval and a weekly audit
sample of n = 30 decisions re-reviewed blind by a senior operator. Estimand:
share of σ-flagged approvals that fail re-review ("rubber-stamp rate"), by
stratum, with a Wilson interval per stratum (Ch. 02 supplies the machinery;
here only the design matters). Baseline: the pre-deployment human-only
re-review failure rate, same audit protocol — without it the number has no
referent.

**Weakening observation (leading):** rubber-stamp rate in the *ambiguity*
stratum flat vs. the human-only baseline, and time-to-approval not
decreasing over deployment months → the trust-spillover worry weakens.
Confirmation-style observation (harm arrived): reversal/complaint rates
rising — too late to act on cheaply, which is why it is not the primary.

**Dominant uncertainty and reduction:** epistemic + model uncertainty, not
aleatory — the estimate per stratum is measurable (more audit samples
reduce it), but the *model* risk is that re-review itself drifts toward
leniency (auditors get calibrated to σ's norms). Reduction: rotate
re-reviewers off fresh training rubrics quarterly; keep a fixed
golden-sample of pre-deployment decisions as a re-reviewer drift control.

**What this is not:** an intervention. The design deliberately stops at
measurement; whether to add cooling-off timers, flag-reason education, or
quota limits is a decision this number *feeds*, made in Ch. 22's
claim–evidence structure.

### Grading rubric (assessor)

Full credit requires: a real deployment the learner can observe; sampling
unit + correlation structure named (not just "n = X invoices"); a
denominator that includes the unaffected strata; a *baseline* from before
the worry's mechanism existed; at least one leading weakening observation;
uncertainty kinds separated with reduction plans; explicit statement that
intervention design is out of scope for the artifact.
