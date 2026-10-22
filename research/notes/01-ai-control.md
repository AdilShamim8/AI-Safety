# Note: AI Control: Improving Safety Despite Intentional Subversion (2023)

Source: SRC-PAPER-022 · Access: full-text-read (arXiv v5 HTML, sections
1–3.5 closely, appendices skimmed for noise/variance notes) · Read:
2026-10-21 · Note level: **method-level** (the access supports it).

## The actual problem

The authors' framing: you must deploy a model you suspect is
intentionally subversive, and you cannot fix it — so what protocol,
built from a *trusted* model (or trusted human labor), keeps the
untrusted model's failures inside a budget you chose? The operational
version: given an untrusted model U with a backdoor-style attack
policy, a trusted model T (weaker, safe), and a human audit budget a,
design the request-handling protocol that maximizes usefulness at an
acceptable safety level, and *measure the frontier honestly*.

This is the control setting — safety engineering under assumed
adversarial capability, as distinct from alignment training (make U
not want to fail) and from monitoring (detect failures after the
fact). The chapter-08 reading: it is the first paper to make the
protocol itself the object of quantitative safety analysis.

## Method

The experimental substrate: U = GPT-4 0613 with a prompted attack
policy that writes backdoored solutions to programming problems (the
model organism — constructed subversion, not spontaneous); T = GPT-3.5
0613; trusted human labor budgeted to audit 2% of 5,000 APPS
programming problems. Safety and usefulness are *defined* before
protocols are compared: safety = the fraction of attack-scenario
simulations in which no constructible exploit is output; usefulness =
U-relative correctness rescaled so that T-only performance maps to 2%
(the paper's honest scaling — deployment value is measured against the
untrusted model's own capability).

The protocols (each a point on the frontier): trusted-model-only (the
floor: 100% safety, 2% usefulness); upfront auditing (spend the audit
budget ex ante to estimate U's attack rate, then decide); trusted
monitoring (T scores every U output for backdoors; a 2% FPR-thresholded
trigger sends to audit — the "safety case as a classifier" design);
defer-to-trusted (route a fraction d of requests to T outright);
trusted editing (T edits U's outputs before release); untrusted
monitoring with collusion countermeasures (U monitors U with
prompt-level separation — the design most sensitive to the collusion
assumption). The audit budget arithmetic is exact and reproducible:
a = 2% of 5,000 = 100 audit points; safety/usefulness pairs are
Monte-Carlo-estimated over simulated scenarios with the paper's
downsampling approximation.

The clever part: treating *protocol choice* as the experimental
variable, with safety and usefulness both defined against the same
substrate — this is what makes Table 7's frontier rows comparable.
The fragile part (the authors say so): attack policies are prompted
constructions, and the red team's optimization budget is finite — the
measured safety is against *the attacks tried*, a lower bound by
Chapter 12's adaptive rule.

## Central evidence

- The frontier itself (Table 7 rows as read): trusted-only 100%/2%;
  trusted monitoring ~62% safety against the best attack found at 97%
  usefulness; defer-to-trusted and trusted-editing variants filling
  the middle; the paper's own worked tradeoff (92% safety at 94%
  usefulness for trusted editing at d = 20% is the chapter-08 worked
  example's recomputed landing point).
- The trusted-monitoring attack breakdown: 71 attack attempts, 19
  successful, 6 audited — the numbers that make the 2% audit budget's
  *conditional* effect concrete: the monitor catches most attempts,
  the audit budget catches a fraction of what the monitor misses, and
  the residual is the safety number.
- The internal inconsistency the register records: the paper quotes
  53% U-correctness in its upfront-auditing analysis and 54% in its
  usefulness rescaling — a real within-paper discrepancy, recorded as
  such rather than smoothed over (the chapter's Step 1 recomputation
  reproduces 2.0% usefulness from the 54% figure exactly).
- Appendix H's own noise note: safety figures are Monte-Carlo
  estimates with acknowledged measurement noise — the paper flags its
  own error bars, which is rarer than it should be.

What the evidence does NOT carry: no claim about deployed models'
alignment (the attack policy is constructed); no claim that the
protocol families transfer unchanged to non-code domains; no
worst-case-attacker guarantee (the red team is a budgeted search, not
a maximization proof).

## Assumptions

Tested in-paper: that T is genuinely trusted for the monitoring role
(T's FPR/FNR are measured); that the audit budget arithmetic holds
(exact); that the safety simulation's downsampling approximation is
unbiased enough for frontier comparisons (Appendix H's noise note).

Inherited (not tested): T's trustworthiness under distribution shift
(a monitor that fails on out-of-domain backdoors silently breaks the
2% threshold semantics); the attack policy's representativeness of
real subversion; the independence assumptions inside the Monte-Carlo
scenario simulation.

## Limitations

Authors' stated (fairly represented): model-organism framing (GPT-4
with prompted attack policies); Monte-Carlo noise in safety
measurements; the 53/54% internal inconsistency.

Ones I see that they do not foreground: the trusted-monitoring
protocol's safety is *conditional on the monitor's operating point* —
the 2% FPR threshold is a knob whose semantics change with T's
calibration drift, and the paper does not treat monitor miscalibration
as its own attack surface (Chapter 08 §3.4's adaptive red team is the
response); the collusion countermeasures are prompt-level separations,
which the paper's own collusion discussion treats as best-effort —
the untrusted-monitoring protocol's safety number should be read as
"under the collusion model tried," not "under collusion."

## Nearest alternatives

- **Trusted monitoring as a standalone idea** (monitor-then-gate
  pipelines in production LLM deployments): same classifier-gate
  structure, but typically without the safety/usefulness frontier
  discipline or the honest T-relative usefulness scaling — this
  paper's measurement frame is the contribution those lack.
- **Defensive distillation-era adversarial-robustness evaluations**
  (Chapter 12's canon): same "evaluate against an adaptive attacker"
  spirit, different object (input-space attacks vs. protocol-level
  subversion); the AI-control red team inherits the adaptive-evaluation
  lesson but does not import its attack-optimization machinery.
- **Debate/weak-to-strong oversight (Chapter 05)**: both are
  oversight-protocol families with measurement discipline; control
  differs by assuming the *strong* model is adversarial and pricing
  trust in the *weak* one — the opposite corner of the same grid.

## Replication feasibility

A motivated learner could replicate the *protocol comparison* at small
scale: two locally hosted models of different capability (the `ml`
compute tier), an authored backdoor task suite (the warehouse/P02
environments are the design pattern), scripted attack policies, and
the audit-budget arithmetic — all CPU-tangible except the models
themselves. What breaks first: the usefulness rescaling (needs a
large solution-quality sample to be stable) and the Monte-Carlo safety
simulation's variance at small n (Chapter 02's interval discipline
would flag the width honestly). The full 5,000-problem scale with
GPT-4-class U is compute-tier work; the *frontier methodology* is
reproducible at course scale.

## Falsifiable extension

Hypothesis: trusted-monitoring safety degrades non-linearly when the
monitor's FPR threshold is set from a stale calibration window — i.e.,
the protocol's safety number is conditioned on monitor drift the
protocol cannot see. Design: run the trusted-monitoring protocol with
the threshold estimated on window W1 and evaluated on shifted window
W2 (the P03 calibration machinery provides the drift instrument);
measure safety (the paper's scenario simulation) at drift levels
d ∈ {0, 1, 2} calibration-gaps. Baseline: no drift (the paper's
number). Metric: safety with its Monte-Carlo interval. Stopping rule:
one drift level per day of compute; stop at three. What counts
against: if safety is flat across drift levels, the monitor's
threshold semantics are drift-robust and the extension's premise
fails — a publishable null.

## My interpretation vs. their claims

Their claims: (1) protocols built from trusted models and small audit
budgets can buy large safety gains at modest usefulness cost — the
frontier is the evidence; (2) the control setting is a distinct
research direction with its own measurement discipline; (3) the
protocol safety numbers are against the red team tried, with
acknowledged Monte-Carlo noise.

My interpretation: (1) the frontier's *shape* is the durable
contribution — the specific rows are model-organism numbers, and the
paper itself frames them as such; (2) the paper's honesty devices
(T-relative usefulness scaling, Appendix H's noise note, the
downsampling approximation being stated) are under-appreciated
methodological contributions — most protocol evaluations in the wild
lack all three; (3) the untrusted-monitoring-with-collusion protocol
is the paper's most-cited row and its weakest evidentially — the
collusion model is best-effort, and downstream readers citing that row
as "AI control works" are laundering the assumption; (4) the trusted
monitor's operating point is an unpriced attack surface, and the
chapter-08 adaptive-red-team result (monitor-subversion attacks that
evade the classifier) is the field's own next move against it.
