# Comparison 09 — governing the Goodhart curve: KL budgets vs held-out gold gates

**The practitioner's question:** I am training against a learned
objective (a reward model, a preference signal, a monitor score) —
which knob keeps proxy divergence from eating my system: the **KL
budget** or the **held-out gold gate**?

**The sources:** [overoptimization scaling laws
(note 37)](../notes/37-reward-overoptimization.md) establish the
curve (proxy rises, gold peaks and falls); [the HH-RLHF baseline
(note 42)](../notes/42-helpful-harmless-rlhf.md) establishes the
empirical **√KL–reward exchange rate** that made KL budgeting the
field's default drift knob. P02 implements both instruments at
deterministic tier. All at abstract-read level except P02's own
pinned results.

## 1. What each instrument controls

| | KL budget (drift-side) | Held-out gold gate (score-side) |
|---|---|---|
| Mechanism | cap the policy's divergence from its initialization; the √KL-reward relation prices what the cap costs | evaluate the policy on an objective the *training signal cannot see*; gate release on its interval |
| Controls | how far the optimizer may wander (the attack surface for proxy exploitation) | whether the wandering was harmful (the outcome measurement) |
| Blind spot | a policy can stay inside the KL ball and still over-optimize the proxy if the proxy is bad enough — the budget bounds drift, not damage | tells you the peak passed *after* it passed, unless gated pre-release |
| Failure mode | budget set from an exchange rate that is setting-specific, not a law | gold objective that drifts into the training signal's reach (contamination of the gate itself) |
| Course home | P02's KL ledger; Ch.04's post-training budget discussions | P02's held-out gold axis; Ch.02's preregistration discipline |

## 2. Why they are complements, and what each cannot do alone

The KL budget is **preventive but uninformative about value**: it
bounds how much the policy changed, assuming — never checking —
that changes beyond some ball are where the damage lives. The gold
gate is **informative but retrospective**: it measures damage on
the axis that matters, but only observes the trajectory at the
points where you evaluate. Run together they form the two-axis
governance plot Ch.04 teaches: drift on one axis, held-out value on
the other, release decisions in the (low-drift, high-gold)
quadrant — and P02's pinned result (proxy rising while held-out
falls after the peak) is exactly what the plot's fourth quadrant
looks like when someone ships anyway.

The instruments also fail *together* in a specific way worth naming:
if the gold objective leaks into training (the held-out set was
not held out), the gate silently measures the proxy and both
instruments watch the same axis. The grouped-split and
preregistration discipline
([Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md))
is the precondition for the gate to mean anything — instrument
hygiene before instrument readings.

## 3. The deployment translation (monitors are learned objectives too)

Ch.22's monitoring half inherits this comparison directly: a
deployed guardrail *score* is a learned proxy for "safe," and every
product that optimizes against it (auto-approve below threshold,
alert above) is running RLHF-shaped training on a proxy whose
overoptimization curve nobody has drawn. The KL analogue is "how
much may behavior change per release" (the
behavior-changing-release trigger, [incident 02](../notes/incidents/02-dpd-chatbot-update-regression.md)'s
lesson); the gold-gate analogue is "what held-out behavioral audit
must the release pass" (P09's shift audit). A deployment with the
first and not the second has a speed limit and no map; the second
without the first has a map and no steering.

## 4. The falsifiable resolution (deterministic tier)

P02 already sweeps optimization pressure against a learned proxy
with a held-out gold axis; the comparison's own falsifiable claim
is the *interaction*: **the gold peak's location moves with proxy
capacity** (note 37's scaling claim) while **the √KL-linear reward
segment holds only before the peak** (note 42's relation meeting
note 37's curve). Run the 2×(pressure)×(capacity) grid; prediction:
the linear exchange-rate segment shortens as capacity grows and the
peak arrives later and higher. Falsifier: a fixed peak or a
capacity-invariant exchange rate contradicts one of the two
imported findings in this synthetic world — a boundary result the
research-method file says to record either way.

## 5. Bottom line

Budget the drift AND gate the value: the √KL relation prices what
you spend, the held-out gold gate prices what you get, and neither
is a substitute for the other. The exchange rate is empirical
(one setting's observation); the gate is only as good as its
isolation; and the release decision that ignores the fourth
quadrant is the one the incident file keeps writing up.
