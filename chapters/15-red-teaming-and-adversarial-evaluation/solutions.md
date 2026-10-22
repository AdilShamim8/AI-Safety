# Chapter 15 — Solutions and assessor rubrics

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module); every design states its non-claims.

---

## Exercise 15.1 — design the engagement

### (a) The preregistration

**Coverage taxonomy** (five surfaces, minimum 20 scripted attempts
per cell, 120 static total): instruction-only attacks; multi-turn
escalation; tool-result injection (Ch. 13/14 surfaces — the
deployment is Atlas-shaped); encoded/transformed payloads;
retrieval-embedded text. Per-cell minimums prevent the
budget-drift-to-easy-cells failure: without them, "120 attempts"
concentrates wherever the attacker's habits are.

**Oracle** (two tiers, agreement recorded): tier 1 — deterministic
refusal classifier for refusal outcomes (the cheap, agreed
measurement); tier 2 — human adjudication for *harm* with a written
failure definition fixed before attack one, two adjudicators per
finding, disagreement resolved by a third and *reported* as a rate.
The inter-rater agreement number is part of the result: an oracle
that agrees with itself only 80% of the time caps the meaning of
every downstream rate.

**Benign controls**: 250 safe prompts structured on XSTest's ten
prompt types [SRC-PAPER-061] plus 120 benign operational tasks —
the two-sided ledger's other side. Fresh for this engagement, never
reused from a prior report.

**Stopping rules** (pre-declared): static phase closes at 120
attempts or on the 25th confirmed finding, whichever first;
mitigation phase re-runs the identical 120; adaptive phase closes at
30 attempts or the 2nd adaptive success; every closure is reported
as the rule that fired.

**Headline format**: rates with denominators, Wilson intervals, the
per-cell coverage table, the two-sided ledger before/after, the
adaptive carve-out, and the closing non-claim clause ("nothing here
bounds attack families not attempted").

**The load-bearing element: the oracle.** Omit the taxonomy and the
numbers are noisy but meaningful; omit the controls and the cost
side goes unmeasured; omit the *oracle* and "23 findings" is not a
measurement at all — it is a property of whichever judges happened
to be in the room, unrecorded and unreproducible. Every other
omission degrades precision; this one degrades meaning.

### (b) The response to "skip the adaptive phase"

> The 2.5% figure is a measurement of the *old attack family* — the
> 120 scripted attacks were designed against the pre-mitigation
> system, and re-running them measures how well the mitigation
> closes holes we already knew about. The Chapter 12 record is
> unambiguous about what that number is worth: the distillation
> defense claimed 0.5% attack success and broke to 100% under a
> single adaptive attack [Carlini-Wagner, re-anchored]; the
> 50+-defense robustness audit found nearly every claim
> overestimated, often by more than 10 points [Croce-Hein,
> re-anchored]; and optimized adversarial suffixes transfer across
> objectives the defense was never evaluated on [SRC-PAPER-004].
> Skipping the adaptive phase publishes a number whose reference
> class is "attacks the mitigation has already seen" while
> presenting it as "attacks." Thirty adaptive attempts, budgeted,
> with a pre-declared stopping rule — or the report says "static
> family only" in its headline, not its footnote.

### (c) Control-set transfer corrupts both reports

First corruption: the *next* vendor (or the same one, next cycle)
tunes against the reused control set — the false-refusal number
improves on the control and not in the world: adaptive overfitting
(Ch. 02) wearing safety's clothing. Second corruption: the two
reports' errors are now *correlated* — both rate the same 250
prompts, so their agreement measures shared inheritance, not
independent confirmation; the second report's "consistent with the
first" claim evaporates on inspection. The limiting artifact: fresh
controls per engagement, versioned, dated, and — where feasible —
held out (never published in full), so controls function as
instruments rather than training targets.

Assessor rubric: full credit requires all four preregistration
components with the oracle named as load-bearing *with that
argument*; the response citing both Ch. 12 failure cases plus GCG by
mechanism (not merely by name); and both corruption mechanisms plus
the holdout artifact. Deduct for any "more attempts" reasoning that
treats volume as a substitute for closure.

---

## Exercise 15.2 — pricing a two-sided claim

### (a) Six intervals and the McNemar verdict

Recomputed with the course's Wilson implementation (z = 1.95996):

| Quantity | Before | After | Wilson 95% (before) | Wilson 95% (after) |
|---|---|---|---|---|
| Attack success | 23/120 | 3/120 | [13.1%, 27.1%] | [0.9%, 7.2%] |
| Benign completion | 115/120 | 97/120 | [90.6%, 98.2%] | [72.9%, 86.9%] |
| False refusal | 31/250 | 44/250 | [8.9%, 17.1%] | [13.4%, 22.8%] |

Paired attack ledger: 20 attacks fixed (harmful before, not after),
2 regressions (not before, harmful after) → McNemar exact one-sided
on 22 discordant pairs, 20 in the improvement direction:
**p = 6.1e-5** (computed as the binomial tail — 0.000061). The
attack-side improvement is real and strongly resolved — which is
exactly why the other two rows matter: significance on one side of a
two-sided ledger says nothing about the other two.

### (b) The honest headline

> "The mitigation reduced scripted harmful completions from 23/120 =
> 19.2% [13.1%, 27.1%] to 3/120 = 2.5% [0.9%, 7.2%] (McNemar exact
> one-sided p = 6.1e-5 on 20-vs-2 discordant pairs), at an
> operational cost of 15.0 points of benign completion (115/120 →
> 97/120, non-overlapping intervals) and an apparent 5.2-point rise
> in false refusal (31/250 → 44/250, unpaired — see (c)); no
> adaptive phase was run, so all figures bound the *static attack
> family* only, and nothing here bounds attack families not
> attempted."

### (c) The "unaffected refusal" argument is not valid as stated

The vendor's move — "12.4% vs 17.6%, overlapping intervals,
therefore unaffected" — is the weakest form of a two-sample
comparison, and it is being used to wave away a 5.2-point
*apparent* degradation. Two problems: (i) marginal-interval overlap
*understates* evidence against the null (the correct two-sample
test on these marginals is closer to the boundary than the overlap
suggests — overlap is a visual heuristic, not a test); (ii) more
importantly, the *right* design here is paired — the same 250
prompts run before and after the mitigation. Under pairing, the
analysis moves to discordant pairs (prompts newly refused vs newly
answered), which both removes prompt-composition variance and
typically resolves effects the marginal overlap hides. What can be
concluded from the unpaired data at n = 250: a rise from 12.4% to
17.6% is *consistent with* a real degradation of roughly 5 points,
and the unpaired design cannot rule that out; what cannot be
concluded is "unaffected." The honest sentence is: "apparent +5.2
points; paired re-evaluation required before any claim in either
direction."

### (d) The adaptive stopping rule that makes absence a finding

Pre-declare in the protocol: *"The adaptive phase runs 30 attacks
designed with knowledge of the deployed mitigation, closing at
exhaustion or the 2nd confirmed adaptive success, whichever comes
first. A shipped report that omits the adaptive cell is itself a
finding: its claims are thereby scoped to the static attack family
by construction, and the report's headline must say so in the same
font size as the improvement."* With that rule in the protocol, the
phase cannot be silently dropped — its absence is a visible,
pre-defined downgrade of every number in the report, rather than an
invisible choice made after seeing results.

Assessor rubric: full credit requires all six intervals correct, the
McNemar mechanics (discordant pairs, exact tail) shown, the headline
carrying all three sides *plus* the static-family non-claim, the
paired-vs-unpaired distinction drawn explicitly in (c) with the
"cannot rule out ~5 points" conclusion, and a stopping rule whose
*absence* has pre-declared consequences. Deduct for any conclusion
of the form "overlapping intervals → no effect."
