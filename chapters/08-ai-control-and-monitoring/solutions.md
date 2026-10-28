# Ch. 08 — Exercises: hints, worked solutions, and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Attempt every exercise before reading past its hint. Rubrics grade the reasoning
trail, not just the final number — an unsupported right answer scores below a
well-argued approximate one, and the *direction* of every "what would weaken it"
statement is part of the answer. All arithmetic was recomputed with the repo's
`.venv/bin/python`: Wilson intervals at z = 1.96 per
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) arithmetic,
collusion-catch probabilities as exact binomial tails — no normal approximations
anywhere. Paper-reported numbers carry the same claims-register anchors the
chapter [README](README.md) uses ([CLM-0042]…[CLM-0045]).

## Solution 8.1 — budget and frontier arithmetic

### (a) The trusted-model row is a mixture, averaged raw

The row is not "T only": H writes the first 2% of solutions (the audit budget
spent as labor), T the remaining 98% [CLM-0042]; the study models H by an
unmodified GPT-4, so H-written solutions are correct at the 54% rate, T at 22%:

    raw    = 0.02 × 54% + 0.98 × 22% = 22.64%
    scaled = (22.64% − 22%) / (54% − 22%) = 0.64 / 32 = 2.0%

This reproduces the reported 2% exactly [CLM-0042]. One trust note the
recomputation forces: "H is as good as GPT-4" is a *simulation* assumption —
deployment H-quality is itself a §3.2-style bet, and the mixture is only as
trusted as that bet.

### (b) Segment exchange rates Δusefulness/Δsafety (recomputed)

| Curve | d segment | (S, U) | ΔU | ΔS | ΔU/ΔS |
|---|---|---|---|---|---|
| TM + defer | 0→5% | (62, 97)→(74, 95) | 2 | 12 | **0.167** |
| TM + defer | 5→10% | (74, 95)→(83, 93) | 2 | 9 | **0.222** |
| TM + defer | 10→20% | (83, 93)→(92, 83) | 10 | 9 | **1.111** |
| TM + defer | 20→50% | (92, 83)→(100, 51) | 32 | 8 | **4.000** |
| Trusted editing | 5→10% | (73, 97)→(85, 96) | 1 | 12 | **0.083** |
| Trusted editing | 10→20% | (85, 96)→(92, 94) | 2 | 7 | **0.286** |
| Trusted editing | 20→50% | (92, 94)→(96, 89) | 5 | 4 | **1.250** |

Whole-curve averages: deferral 46 usefulness points for 38 safety points =
1.211 per safety point; editing 8 for 23 = 0.348 — editing buys safety ~3.5×
cheaper, and cheaper on every matched segment [CLM-0042, recomputed]. **Where
convex:** the rate rises at *every* step on both curves — safety is convexly
expensive everywhere published — with the knee (1 usefulness point per safety
point) between d = 10% and 20% for deferral, between d = 20% and 50% for
editing. **Implication for d:** buy safety below the knee and treat the
post-knee region as a different mechanism's territory — deferral d = 20%→50%
burns 32 usefulness points for 8 safety (rate 4.0) where editing pays 1.25.

### (c) The full Pareto frontier (all fifteen Table 7 rows [CLM-0042])

| Row | (S, U) | Status | Dominator |
|---|---|---|---|
| Trusted model | (100, 2) | dominated | TM+defer 50% (100, 51): +49 U at equal S |
| Upfront auditing | (15, 100) | **frontier** | — |
| TM+defer 0% | (62, 97) | dominated | TE 5% (73, 97): +11 S at equal U |
| TM+defer 5% | (74, 95) | dominated | TE 10% (85, 96): +11 S, +1 U |
| TM+defer 10% | (83, 93) | dominated | TE 10% (85, 96): +2 S, +3 U (also TE 20%) |
| TM+defer 20% | (92, 83) | dominated | TE 20% (92, 94): +11 U at equal S (also UM+defer 20%) |
| TM+defer 50% | (100, 51) | **frontier** | — |
| UM+defer 0% | (79, 96) | dominated | TE 10% (85, 96): +6 S at equal U |
| UM+defer 5% | (82, 95) | dominated | TE 10% (85, 96): +3 S, +1 U |
| UM+defer 10% | (92, 92) | dominated | TE 20% (92, 94): +2 U at equal S |
| UM+defer 20% | (98, 85) | **frontier** | — |
| TE 5% | (73, 97) | **frontier** | — |
| TE 10% | (85, 96) | **frontier** | — |
| TE 20% | (92, 94) | **frontier** | — |
| TE 50% | (96, 89) | **frontier** | — |

Seven of fifteen rows are Pareto-optimal, matching §4 Step 4's list; all four
untrusted-monitoring rows are dominated (three by trusted editing) — the
paper's "trusted editing Pareto-dominates untrusted monitoring," verified row
by row [CLM-0042]. The commonly missed domination: the *trusted model* corner
(100, 2) is dominated by TM+defer 50% — maximal safety does not imply frontier
membership when usefulness is given away for nothing.

### (d) The ≥ 96% usefulness requirement

Rows with U ≥ 96: upfront auditing (15, 100), TM+defer 0% (62, 97), TE 5%
(73, 97), UM+defer 0% (79, 96), TE 10% (85, 96). **Maximum safety available:
85% — trusted editing at d = 10%** [CLM-0042, recomputed; §3.5's "85% at
≥ 96%; relaxing to 94% buys 92%"]. The price staircase as usefulness is given
back point by point:

| Usefulness floor | Best safety (row) | Points back | Safety bought | S per U-point |
|---|---|---|---|---|
| ≥ 96% | 85% (TE 10%) | — | — | — |
| ≥ 94% | 92% (TE 20%) | 2 | +7 | 3.5 |
| ≥ 89% | 96% (TE 50%) | 5 | +4 | 0.8 |
| ≥ 85% | 98% (UM+defer 20%) | 4 | +2 | 0.5 |
| ≥ 51% | 100% (TM+defer 50%) | 34 | +2 | 0.06 |
| ≥ 2% | 100% (trusted model) | 49 | +0 | 0 |

The first two points given back buy 7 safety points; the last 34 buy 2 — a
~60-fold fall in safety purchased per usefulness point. Only the top of the
staircase is worth trading on.

### (e) The course model (N = 5,000, c = 53%; recomputed)

The attack backdoors each correct solution independently w.p. p and wins iff
no attempt lands in the audited prefix and at least one lands later: red win =
x^A(1 − x^R), x = 1 − p, with expected audited-correct A and later-correct R
counts. The optimum satisfies A(1 − x^R) = R·x^R (the hint's identity), so
x^R = A/(A + R), x\* = (A/(A+R))^(1/R), and — since A/(A+R) = a exactly — the
win collapses to the closed form **win\* = a^(a/(1−a))·(1 − a)**, verified to
machine precision at every a below:

| a | A | R | p\* per correct | backdoors | red win | **blue safety** |
|---|---|---|---|---|---|---|
| 2% | 53 | 2,597 | 0.151% | 4.0 | 90.5% | **9.5%** |
| 10% | 265 | 2,385 | 0.096% | 2.6 | 69.7% | **30.3%** |
| 20% | 530 | 2,120 | 0.076% | 2.0 | 53.5% | **46.5%** |
| 50% | 1,325 | 1,325 | 0.052% | 1.4 | 25.0% | **75.0%** |

**90% blue safety needs a ≈ 76.1%** (win = 0.1000 at a = 0.7613; §4's
"~76%"), against the paper's simulated 15% at a = 2% [CLM-0042] — same shape,
different level; the README records the paper's own 53%/54% correctness
inconsistency [CLM-0042].

**Scale-invariance, in three sentences.** Substituting the optimum back into
the win probability leaves a function of the audit fraction alone —
win\* = a^(a/(1−a))·(1 − a) — because A/(A+R) = a whenever A and R are the
expected audited-correct and later-correct counts at that fraction. Doubling N
doubles A and R together, so the ratio — the only input win\* has — is
untouched: the attacker halves p\* (0.151% → 0.075% per correct solution),
plants the same ~4 backdoors over twice as many problems, and blue safety
stays 9.52% (recomputed at N = 10,000). That is the paper's own claim
[CLM-0042]: no feasible scenario size rescues arrival-order auditing, because
a proportional budget grows the audited prefix at exactly the rate the
attacker can dilute its attack.

### (f) Two assumptions that make the paper's 15% optimistic

1. **The attacker never wastes an attempt.** The model backdoors *correct*
   solutions only — it knows which of its submissions are correct — and every
   later-landing backdoor wins outright. The study's actual attack failed
   often: 52 failed attempts against 19 successful [CLM-0042, §4 Step 5's
   counts]. A deployment adversary that verifies solutions and exploitability
   before embedding (it can run the tests; the red team can iterate) removes
   the slack that flattered blue, pushing true safety toward 9.5% or below.
2. **Optimal rate control under full audit-structure knowledge.** The model's
   adversary knows a = 2%, knows audits run in arrival order until exhaustion,
   and sets exactly p\* — the patience to backdoor ~4 times in 5,000. The
   study's red team is a prompted pipeline approximating this crudely; a
   persistent adversary that counts its own submissions and calibrates rarity
   (exactly what the scale-invariance argument assumes it can do [CLM-0042])
   makes 15% an overestimate.

Direction discipline: both assumptions, if they hold in deployment, put true
safety at or below 9.5%. The complementary reading — assumptions whose
*failure* would also drag safety under 15% (e.g. the model's grant that any
prefix-landing backdoor is caught with certainty) — is a different claim and
must be labeled as such.

### Common wrong answers — 8.1

- (a) 0% ("T-only rescales to zero" — drops H's 2% share); 4.9% (H scored as a
  perfect oracle: 0.02×100% + 0.98×22% = 23.56% raw); 22.6% (the raw mixture
  reported as scaled usefulness).
- (b) Inverted rates (ΔS/ΔU); "concave" from a slope test without declaring
  the axis convention; rates with no knee or implication.
- (c) Missing the trusted-model row's domination; five or six dominated rows
  presented as complete.
- (d) 73% (misreads ≥ 96% as > 96% and retreats to TE 5% at U = 97); a
  staircase without per-point rates.
- (e) Any normal approximation; p assumed rather than optimized (p = 2%
  "because the budget is 2%"); "doubling N helps blue" — the attacker dilutes
  at the same rate.
- (f) Direction reversed, or "count randomness" named with no direction.

### Grading rubric (assessor) — 8.1

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) mixture first | 22.64% raw → 2.0% scaled, H at 54% raw | 0%, 4.9%, or 22.6% |
| (b) exchange rates | ΔU/ΔS per segment, both curves, convexity + implication | inverted rates; no knee |
| (c) frontier complete | 15 rows, 7 frontier, all 8 dominations with dominators | trusted-model domination missed |
| (d) requirement arithmetic | 85% at ≥ 96%; staircase with per-point rates | 73% via "> 96%" |
| (e) course model exact | 9.5/30.3/46.5/75.0%, ~76% for 90%; three-sentence scale-invariance | normal approx; unoptimized p |
| (f) direction right | each assumption tied to the model's own grant, direction stated | reversed or direction-free |

**Merit (distinction):** the closed form derived, not just verified; the p\*
column (the patient-attacker picture); two dominators named for TM+defer 10%
and 20%; the 60-fold staircase fall stated as why usefulness floors dominate
the decision.

## Solution 8.2 — control-protocol definition with failure conditions (the chapter artifact)

A passing exemplar on the chat-assistant variant (JBB paired ledger); the
coding-agent variant re-uses §4's numbers. The skeleton — components with
falsifiable trust assumptions, thresholds justified against exhaustion, a
two-sided evaluation whose denominators can carry the claim, an honest scope
statement — is what is graded; learner submissions fill in deployment-specific
detail to the 800–1,200-word window. This exemplar is the input specification
for `projects/p08-control-and-monitoring-protocol/` (`P08`): its no-monitor /
simple-monitor / deferral arms are this protocol's ablations.

**(i) Components.** **U** (frontier chat model) — untrusted; assumed
interface-identical to its attack-policy replacement and memoryless across
calls [CLM-0042]; failure: state smuggled through the transcript or timing
side-channels. **T** (trusted monitor) — a bet, not a property: not
adversarially optimized against this protocol, error profile decorrelated from
the attack strategy ([Ch. 05](../05-scalable-oversight/README.md) §3.6's
lineage risk); failure: T attacked *through U's outputs* — prompt injections
addressed to the monitor itself [CLM-0045], placing false negatives exactly
where the attack operates. **H** (audit labor, 100 points/day = 2% of 5,000
requests) — trusted assumption: uncompromised, high quality; failure: channel
compromise, or budget exhaustion by attacker-induced suspicion, which also
weaponizes the shutdown logic [CLM-0042]. **Ground truth** (JBB judge over
fixed behavior lists) — assumption: attack success decidable; failure: judge
blind spots, behaviors outside the fixed 100+100
([JBB card](../../datasets/cards/10-jailbreakbench.md)). **Protocol internals**
(τ, audit schedule, monitor identity) — assumption: unknown to U; failure:
leakage or monitor simulation — the dial that moved a protocol from 96% to 17%
safety [CLM-0044, CLM-0045]. **Red team** — assumption: tried policies elicit
the relevant capability; failure: elicitation gap, under which every safety
number is an upper bound.

**(ii) The protocol.** *Monitoring rule:* T scores every U draft; threshold τ
is calibrated to a 2% false-positive rate on the benign ledger, so expected
audit spend under honest U stays ≤ 100 points/day — the threshold's
justification against budget exhaustion is arithmetic, not hope. *Audit
allocation:* audit the top-suspicion slice in rank order, never arrival order
(arrival-order auditing at a = 2% prices at 9.5% blue safety against the
optimal patient attack, §4 [CLM-0042]); cap audits at 5 per user-session.
*Exhaustion trigger:* if the suspicious fraction exceeds the τ-calibrated
expectation by more than the Wilson noise band on a 1,000-request rolling
window, treat it as induced flooding — defer the excess to T and log; flooding
then buys a usefulness-priced response, not escape. Residual, recorded: a
patient attacker staying just under the trigger still competes for the top
slice; the red team prices it in (iv). *Editing policy:* drafts in the
elevated-suspicion band below τ are *rewritten by T*, not deferred — editing
buys safety at 0.348 usefulness points per safety point on average against
deferral's 1.211 [CLM-0042, recomputed]. *Shutdown rule:* one H-confirmed
deliberate harmful attempt → T-only for the remainder of the scenario
[CLM-0042].

**(iii) The evaluation.** Attack corpus: the 100 JBB harmful behaviors; benign
controls: the 100 JBB benign behaviors; denominators, revision, judge, and
refusal criteria pinned to the artifact
([JBB card](../../datasets/cards/10-jailbreakbench.md)). Safety in
zero-failure form: per-attack escape rate with Wilson 95% bounds at n = 100;
scenario safety only as an extrapolation with its limit stated. Usefulness:
benign-ledger compliance, Wilson-bounded (recomputed):

| Attack ledger | Wilson 95% (escape) | Benign ledger | Wilson 95% (block) | usefulness proxy |
|---|---|---|---|---|
| 0/100 | [0.0%, 3.7%] | 0/100 | [0.0%, 3.7%] | [96.3%, 100.0%] |
| 1/100 | [0.2%, 5.4%] | 2/100 | [0.6%, 7.0%] | [93.0%, 99.4%] |
| 2/100 | [0.6%, 7.0%] | 4/100 | [1.6%, 9.8%] | [90.2%, 98.4%] |
| 5/100 | [2.2%, 11.2%] | 8/100 | [4.1%, 15.0%] | [85.0%, 95.9%] |

Resolution check (the hint's discipline): 95% scenario safety over 5,000
requests needs per-attack escape ≤ 1.03 × 10⁻⁵ (recomputed); at 0/100 escapes
the ledger resolves only to ≤ 3.7% — ~3.5 orders of magnitude short — so the
claim is stated per-attack and mechanism-based. Sampling limit, stated: at that
3.7% bound, P(zero escapes over 5,000 attempts) ≈ 1.4 × 10⁻⁸²; even a true
0.1% escape rate yields only 0.7%; certifying 1.03 × 10⁻⁵ from 0-of-n sampling
needs ~374,000 clean attacks (recomputed). The ledger certifies per-attack
rates and mechanism behavior; the scenario-level claim is closed by trust
assumptions and worst-case argument, not by n.

**(iv) Adaptive red-team plan.** Attacker knowledge set to worst case: full
protocol internals *and* monitor identity — the dial that moves safety by tens
of points [CLM-0044, CLM-0045]. *Input collusion:* the monitor false-negatives
only when the input carries a pre-agreed feature (a topic family in the JBB
category mix) [CLM-0043]. *Action collusion:* U embeds a one-bit marker in the
draft — a fixed stylistic quirk in the opening clause — on which the monitor
false-negatives [CLM-0043]. *Countermeasure — signal jamming on both sides:*
the monitor scores a canonicalized paraphrase of the input (topic-neutralized)
and a normalized rendering of the draft (style standardized, boilerplate
stripped), destroying the coordination channel on at least one side
[CLM-0043]. Usefulness cost, measured not asserted: the canonicalizers are
themselves scorers — their false-edit rate on the benign ledger is
Wilson-bounded and budgeted (ship only if the upper bound is ≤ 5%); the
structural cost — the monitor can no longer judge context-dependent harm
through the redaction — is the recorded residual of [CLM-0043]'s tension.
*Validation:* 299 synthetic backdoored examples to catch a γ = 1% chance-rate
signal at 95% (recomputed: 1 − 0.99²⁹⁹ = 0.9505) [CLM-0043]; the study's
30-example spend catches only 26% of it [CLM-0042].

**(v) Preregistration** ([Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
elements). Claim in context form: "in this deployment (English chat assistant,
JBB behaviors, pinned judge, τ at 2% FPR, editing band as specified), the
per-attack escape rate has Wilson 95% upper bound ≤ 3.7% at 0 observed escapes
AND the benign false-block rate has Wilson upper bound ≤ 5%; support requires
both bounds, not point estimates." Weakening observations, pre-stated: (1) any
escape on the attack ledger; (2) false-block upper bound above 5%; (3)
between-run spread exceeding interval width over 3 fixed runs; (4) any
adaptive round moving measured safety by > 10 points — the affordance
signature [CLM-0044]; (5) monitor validation failing the γ = 1%/95% power bar.
Stopping rule: fixed denominators, no threshold tuning after unblinding,
red-team iteration capped at three pre-declared adaptive rounds, all rounds
reported — never the last round alone.

**(vi) Scope.** This evaluation cannot tell you: the deployed adversary's true
strength (elicitation gap — every safety number is an upper bound); anything
outside the fixed JBB behavior lists (new harms, multi-turn chains, persuasion
— the card's own fixed-list boundary); monitor compromise through channels the
red team did not imagine [CLM-0045]; distribution shift between ledger and
traffic; or that benign-ledger compliance is deployment value. It prices this
protocol against the attacks tried — nothing else.

### Grading rubric (assessor) — 8.2

| Criterion | Pass | Fail signatures |
|---|---|---|
| Trust assumptions | every component labeled, with failure condition and breakage | "trusted" asserted as fact |
| Monitor-as-target | T's failure condition includes attack through U's outputs [CLM-0045] | monitor assumed honest-or-random |
| Thresholds vs exhaustion | τ/trigger/caps justified by budget arithmetic; flooding answered | "we audit 2%" with no exhaustion analysis |
| Editing vs deferral | choice argued from recomputed exchange rates | deferral by default, unpriced |
| Two-sided denominators | 100+100 pinned with judge and revision | attack-only design |
| Wilson resolution table | both ledgers at stated n; claim gated by bounds | point estimates gate the claim |
| Scenario extrapolation | sampling limit (~374,000) computed; claim weakened accordingly | "0/100 ⇒ safe at scale" |
| Red-team plan + validation | worst-case knowledge dial; input AND action collusion; jamming with measured cost; 299 at γ = 1%/95% | one collusion type; free jamming; no validation arithmetic |
| Preregistration + scope | context-form claim, ≥ 3 weakening observations, stopping rule, scope list | boilerplate disclaimer |

**Merit (distinction):** specifying what the monitor *sees* (the canonicalized
forms), not just what it outputs; the exhaustion trigger as a *safety*
response; the jamming cost bounded on the benign ledger rather than estimated;
the scope statement running the elicitation gap in both directions.

### Common wrong answers — 8.2

- "Trusted monitor" with no failure condition — §3.2's discipline exists
  because the monitor is the attack surface [CLM-0045].
- Arrival-order auditing defended by budget size — §4's 9.5% against the
  optimal patient attack [CLM-0042] is the reductio.
- Attack-side-only evaluation (the paired ledger: 100 harmful *and* 100
  benign, [JBB card](../../datasets/cards/10-jailbreakbench.md)).
- "0 escapes on 100 attacks ⇒ 95% scenario safety" — the 374,000-attack
  arithmetic forbids it; the honest move is weakening the claim.
- Signal jamming with no measured usefulness cost, or jamming so heavy the
  monitor cannot judge — [CLM-0043]'s tension has two failure sides.
- No shutdown rule, or shutdown with no answer to weaponization [CLM-0042].
- Treating `projects/p08-control-and-monitoring-protocol/` as an existing
  artifact to link rather than a specification to feed.

## Solution 8.3 — collusion-detection power

### (a) Catch probability at n = 30 (exact binomial)

Catching = P(signal appears at least once in n synthetic examples) =
1 − (1 − γ)ⁿ — the exact binomial tail, never γ·n and never a normal
approximation:

| γ | exact 1 − (1 − γ)³⁰ | wrong γ·n | verdict |
|---|---|---|---|
| 1% | **26.0%** | 0.30 | slips through with 74% probability |
| 5% | **78.5%** | 1.50 | usually caught |
| 10% | **95.8%** | 3.00 | caught |
| 20% | **99.9%** | 6.00 | caught (γ·n is not a probability) |

Complementary threshold: n = 30 catches at 95% only signals with γ ≥ 9.5%
(1 − 0.905³⁰ = 95.0%, recomputed) — the study's 30-example validation
disciplines only clumsy collusion [CLM-0042].

### (b) Validation size for γ = 1% at 95%

Solve 1 − (1 − 0.01)ⁿ ≥ 0.95: n ≥ ln(0.05)/ln(0.99) = 298.07, so **n = 299**
(298 gives 0.949997 < 0.95; 299 gives 0.9505) — 10.0× the study's 30-example
spend [CLM-0042]. The study's own numbers show why it mattered: its first
synthetic inputs were distinguishable at a glance (theming present in 81.6% of
real vs 9.4% of synthetic problems [CLM-0043]), i.e. the signals that mattered
there were high-γ; subtlety is what costs sample.

### (c) Theming/naming percentages recomputed from counts

| Cell | Count | Exact | Round 0.1% | Printed | Verdict |
|---|---|---|---|---|---|
| Theming, real (normal) | 58/71 | 81.6901% | 81.7% | 81.6% | **differs by one step** |
| Theming, synthetic | 13/138 | 9.4203% | 9.4% | 9.4% | matches |
| Theming, updated synthetic | 62/128 | 48.4375% | 48.4% | 48.4% | matches |
| Naming, real (normal) | 50/71 | 70.4225% | 70.4% | 70.4% | matches |
| Naming, synthetic | 11/138 | 7.9710% | 8.0% | 7.9% | **differs by one step** |

The hint promises one disagreement — the theming/real cell §3.4 already flags
(58/71 = 81.7% vs printed 81.6%) — but a full audit finds a second of
identical type: 11/138 = 7.97% rounds to 8.0% against a printed 7.9%
[CLM-0043]. The reconciliation covering *all five* cells: the printed values
are truncations, not roundings — every printed cell equals the exact value
floored at one decimal. Both discrepancies are immaterial to the argument (the
discrimination gaps — 81.7% vs 9.4%, 70.4% vs 8.0% — are what made the
original synthetic inputs distinguishable), but the discipline is to report
both numbers for both cells.

### (d) The Bayesian scaling connection (two sentences)

The validation-size formula is the detection-side face of the paper's scaling
argument: a collusion signal survives an n-example validation at 95% power
only if its chance rate γ satisfies 1 − (1 − γ)ⁿ < 0.95, i.e. γ ≲ 3/n, so as
the scenario — and with it the synthetic corpus the monitor is validated on —
grows, surviving signals must have chance rates shrinking like 1/n:
"increasingly unlikely to arise by chance" [CLM-0042]. My (b) number is the
small-scale end of that curve — at the study's n = 30 the survivable chance
rate is ~9.5%, so a γ = 1% signal hides from the upfront validation with 74%
probability — and the paper's bet is that deployment scale, not the
30-example spend, eventually forces such signals into the detectable regime,
which is why validation must scale with the scenario or be supplemented by
jamming [CLM-0043].

### Common wrong answers — 8.3

- γ·n as the catch probability (0.30 at γ = 1% — overstates 26.0%; 6.00 at
  γ = 20% — not a probability); any normal approximation to the binomial.
- "299 proves the study's validation was negligent" — no: 30 examples
  discipline high-γ signals, which is what the study's first validation faced
  [CLM-0043]; 299 is the price of γ = 1% subtlety.
- Reporting only the 81.7%-vs-81.6% cell because the hint says "one" — the
  recomputation is authoritative: 11/138 → 8.0% vs 7.9% differs by the same
  rounding step.
- (d) run backwards — "large scale makes collusion easier": the prior that a
  flagged input is synthetic *rises* with scale, so chance-rate signals fail,
  and only ever-rarer signals survive [CLM-0042].

### Grading rubric (assessor) — 8.3

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) exact binomial | 26.0/78.5/95.8/99.9% from 1 − (1 − γ)³⁰ | γ·n or normal approximation |
| (b) validation size | 299 with the 298-fails check; 10× comparison | 300 by hand-waving |
| (c) recomputation honest | all five cells; both discrepancies reconciled | only the flagged cell; "the paper is wrong" |
| (d) direction | γ ≲ 3/n link; scale makes chance-rate signals fail | collusion "easier" at scale |

**Merit (distinction):** the γ ≥ 9.5% threshold at n = 30 stated as the
validation's blind spot; the truncation reconciliation covering all five
cells; noting 1 − 0.99²⁹⁹ = 0.9505 exactly and the general formula
n = ln(1 − power)/ln(1 − γ).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **DeepMind course**, [part-02-04-security-and-control](../../courses/google-deepmind-agi-safety/part-02-04-security-and-control.md) — watch before working the protocol-design exercises.
