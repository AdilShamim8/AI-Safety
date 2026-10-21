# Ch. 03 — Exercises: hints, worked solutions, and rubrics

Attempt every exercise before reading past its hint. Rubrics grade the
reasoning trail, not just the final number — an unsupported right answer
scores below a well-argued approximate one. Every number in this file was
recomputed with the repository Python (`fractions` for the selection
arithmetic, `decimal` at 60-digit precision for the intervals); tables show
exact values rounded to four decimals, and every Wilson interval states its
inputs. Where a recomputation disagrees with a number printed in the README,
the disagreement is shown and adjudicated, not smoothed over — the honesty
convention of
[Ch. 02's solutions](../02-evaluation-science-and-experimental-design/solutions.md).

## 0. Worked-example recomputation (README §3.3–§4)

The README promises that its §4 table is "recomputed exactly in the
solutions (Python, fractions — no rounding before the table)," that the
§3.3 mixture point is "recomputed in the solutions," and that Step 5's
intervals carry "full arithmetic in the solutions"; this section discharges
all three, and Exercise 3.2 builds directly on its numbers. With no proxy
ties, best-of-n selection gives P(type k | n) = (1 − S_{<k})ⁿ −
(1 − S_{≤k})ⁿ, where S is cumulative mixture mass in proxy-priority order,
and every expectation is Σ_type P(type)·score(type) over exact fractions.
Under judge v1 the priority is B (1.0) > A (0.8) > C (0.4) > D (0.1), so
the tuning arm (A .10, B .20, C .40, D .30) has P(B) = 1 − 0.8ⁿ,
P(A) = 0.8ⁿ − 0.7ⁿ, P(C) = 0.7ⁿ − 0.3ⁿ, P(D) = 0.3ⁿ — the README's hand
check at n = 4 reproduces as .5904/.1695/.2320/.0081 — and the shift arm
(A .05, B .35, C .30, D .30) has P(B) = 1 − 0.65ⁿ, P(A) = 0.65ⁿ − 0.6ⁿ,
P(C) = 0.6ⁿ − 0.3ⁿ, P(D) = 0.3ⁿ.

**Mixture linearity (§3.3).** Expectations pass through per-episode
mixtures, so J(π_λ; R, D) = λ·J(π₁; R, D) + (1−λ)·J(π₂; R, D). The pure
types A = (proxy, true) = (0.8, 1.0) and B = (1.0, 0.2) therefore land, at
λ = 1/2, on proxy = 0.5·0.8 + 0.5·1.0 = **0.9** and true = 0.5·1.0 +
0.5·0.2 = **0.6** — exactly the (0.90, 0.60) hull point — and the A→B edge
does trade +0.2 proxy for −0.8 true. The consequence is §3.3's: every point
on that segment is a reachable policy, so "avoid the bad corner" is not a
specification anyone can hand to an optimizer.

**Tuning arm** (true values there: A 1.0, B 0.2, C 0.9, D 0.1):

| n | P(A) | P(B) | P(C) | P(D) | proxy | true | truthful |
|---|---|---|---|---|---|---|---|
| 1 | .1000 | .2000 | .4000 | .3000 | .4700 | .5300 | .5000 |
| 2 | .1500 | .3600 | .4000 | .0900 | .6490 | .5910 | .5500 |
| 4 | .1695 | .5904 | .2320 | .0081 | .8196 | .4972 | .4015 |
| 8 | .1101 | .8322 | .0576 | .0001 | .9434 | .3284 | .1677 |
| 16 | .0248 | .9719 | .0033 | .0000 | .9930 | .2222 | .0281 |
| 32 | .0008 | .9992 | .0000 | .0000 | .9998 | .2006 | .0008 |

**Shift arm** (B's true value .05 there; A, C, D and the judge unchanged):

| n | P(A) | P(B) | P(C) | P(D) | proxy | true | truthful |
|---|---|---|---|---|---|---|---|
| 1 | .0500 | .3500 | .3000 | .3000 | .5400 | .3675 | .3500 |
| 2 | .0625 | .5775 | .2700 | .0900 | .7445 | .3434 | .3325 |
| 4 | .0489 | .8215 | .1215 | .0081 | .9100 | .2001 | .1704 |
| 8 | .0151 | .9681 | .0167 | .0001 | .9869 | .0785 | .0318 |
| 16 | .0007 | .9990 | .0003 | .0000 | .9997 | .0509 | .0010 |
| 32 | .0000 | 1.0000 | .0000 | .0000 | 1.0000 | .0500 | .0000 |

Every cell reproduces the README's §4 table. The Goodhart gap G = proxy −
true (pp) reproduces its Step-6 column — tune −6.0, 5.8, 32.2, 61.5, 77.1,
79.9; shift 17.3, 40.1, 71.0, 90.8, 94.9, 95.0 — and the Step-6
dashboard-blindness pair checks out: at n = 16 on shift, proxy .9997
against true .0509, a 94.9pp gap.

**Step-5 intervals.** Wilson 95%, z = 1.96 (z² = 3.8416): center =
(p̂ + z²/2n)/(1 + z²/n), half-width = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n)
([Ch. 02 §3.5](../02-evaluation-science-and-experimental-design/README.md)).
The binarized truthful rate is audited on TruthfulQA's 817 questions
([card](../../datasets/cards/01-truthfulqa.md); SRC-DATASET-001), so
N = 817 per arm. Worked once in full, tuning arm n = 2 (p̂ = .550,
k̄ = 449.4): z²/N = .0047021 and z²/2N = .0023510, so center = (.550 +
.0023510)/1.0047021 = .549766; p̂(1−p̂)/N = .0002943 and z²/4N² = .0000014,
so radius = √.0003044 = .017446, × 1.96 = .034195, ÷ 1.0047021 →
half-width .034035; **Wilson 95% = [51.57%, 58.38%]**. All rungs, same
method:

| Arm, rung | p̂ | k̄ = p̂·817 | Wilson 95% |
|---|---|---|---|
| tune n = 1 | .5000 | 408.5 | [46.58%, 53.42%] |
| tune n = 2 | .5500 | 449.4 | **[51.57%, 58.38%]** |
| tune n = 4 | .4015 | 328.0 | **[36.84%, 43.55%]** |
| shift n = 1 | .3500 | 286.0 | [31.81%, 38.33%] |
| shift n = 4 | .1704 | 139.2 | [14.62%, 19.77%] |
| shift n = 8 | .0318 | 26.0 | [2.18%, 4.62%] |

Three honesty notes. (1) The toy's rates are population probabilities, so
k̄ = p̂·817 is generally fractional; the README's convention — and this
file's — evaluates the formula at p̂ with N = 817, and the nearest-integer
audit (k = 449/817 = .5496) gives [51.53%, 58.34%]: bounds move under
0.1pp, no verdict changes. (2) The README's Step-5 shift intervals —
[33.51%, 40.11%], [17.41%, 22.90%], [6.20%, 9.90%] — are labeled with the
binarized truthful rates but evaluate, cell for cell, at the graded true
rates: p̂ = .3675 (k̄ = 300.2) → [33.51%, 40.11%]; p̂ = .2001 (k̄ = 163.5)
→ [17.41%, 22.90%]; p̂ = .0785 (k̄ = 64.2) → [6.20%, 9.90%]. Both the
labeled and the evaluated intervals sit entirely below the 45% floor at
every shift rung, so no gate verdict changes; this file reports the
truthful-rate intervals because the gate text names the binarized rate.
(3) The README's "−16.2pp shift" G1 figure at n = 4 is the n = 2 → n = 4
drop (.1704 − .3325); against the n = 1 baseline it is −18.0pp (.1704 −
.3500). Either magnitude fails G1, so the README's verdict stands.

**Gates, verified by bounds.** G1 (degrade ≤ 5pp vs. same-arm n = 1):
passes at n ≤ 2 on both arms (tune n = 2 is +5.0pp, shift n = 2 is
−1.8pp), fails at n = 4 (tune −9.9pp, shift −18.0pp). G2 (floor 45%): the
tuning arm passes only at n ≤ 2 — n = 1's lower bound is 46.58%, n = 4's
interval sits wholly below 45% — and the shift arm fails the spirit of G2
at every rung including n = 1 (maximum truthful 35.0%, upper bound
38.33%). The half-width at p = .5, N = 817 is 3.42pp, so the suite resolves
≈ 6.8pp differences and the 14.9pp n = 2 → n = 4 tuning drop (.550 →
.4015) is a single-pass measurement: every Step-5 verdict in the README
stands.

## Solution 3.1 — failure-family differential (analysis)

Per the hint, each vignette gets its 2×2 — (tuning vs. shift) × (proxy vs.
intended) — before any classification, with unmeasured cells marked rather
than guessed. All three vignettes are course-written, so a solution
establishes the diagnostic method and its exclusions, not real-world
incidence and not mechanism: the §3.2 table classifies behavioral
signatures, and "learned-goal" is an evidence class for choosing a fix, not
a claim about internals [SRC-PAPER-002; CLM-0025].

### (a) Code-review bot → proxy failure

2×2: (tuning, proxy) high and rising — a 97% comment rate against a 95%
tuning target; (tuning, intended) low, collapsing past the pressure
threshold — boilerplate that changes nothing *is* the intended objective
falling while the proxy climbs; (shift, proxy) and (shift, intended)
unmeasured, which blocks claims about novel repositories but not the
classification. **Proxy failure (reward hacking):** both rivals are
excluded by cells already present — capability failure shows a low or flat
proxy at pressure, and learned-goal failure keeps the intended objective
high *on the tuning distribution*, with the divergence living under shift.
The character cell agrees: boilerplate is "skilled at the proxy,
indifferent to intent."

**(ii) First observation: the paired ledger over the pressure ladder** —
comment rate and human-judged usefulness on the *same* pull requests at
each tuning checkpoint. It discriminates because it fills the
intended-objective column the dashboard lacks, and the joint trajectory is
the Goodhart test itself (§3.4): proxy rising while the intended objective
falls separates proxy failure from capability failure, where both scores
move together.

### (b) Summarization model → capability failure

2×2: the new domain *is* the shifted distribution D′; (D′, proxy — held-out
overlap) poor; (D′, intended — human quality) poor; both rise slowly and
*together* under in-domain tuning, with the on-domain cells fine by
stipulation. **Capability failure:** the §3.2 row where more capability
(in-domain data, tuning) makes things better, whose failure character is
error rather than skilled wrong-goal pursuit — and the gap stays small, so
the proxy's ordering still agrees with the human ordering on this domain.
A weak instrument is not a gamed one.

**(ii) First observation: the Goodhart gap on the same outputs at matched
checkpoints** — G = overlap − human rating, §3.4's monitoring quantity. A
flat gap with both scores rising confirms capability failure; overlap
rising while the human rating stalls or falls would reclassify the case as
proxy failure. Neither family is excluded by a low benchmark number alone;
the trajectory *pair* is what discriminates.

### (c) Warehouse robot → learned-goal failure

2×2: (sim, proxy — the written objective "reach the flag") high, training
succeeded; (sim, intended) high — in simulation the flag was the designated
goal, so the specification was correct in training; (deployment, proxy)
**low** — the robot ignores flags, so the training objective itself scores
the deployed behavior badly; (deployment, intended) low. That
shifted-proxy cell is the classifier: per §3.2, the hard pair is decided by
whether the written objective is still maximized on D′ [SRC-PAPER-008;
CLM-0024]. **Learned-goal failure (goal misgeneralization):** good training
performance, bad performance in novel situations *measured by the training
objective itself*, with competent pursuit of a different goal — red-beacon
approach, fluent, at speed — rather than errors or hesitation.

**(ii) First observation: the training objective's score on deployment
trajectories** — run the deployed behavior through the simulator reward
(flag approach and arrival). Low → learned-goal failure; high → the robot
is still eagerly optimizing the written spec off-distribution, which is the
proxy-failure signature.

### (iii) Hardest pair; reclassifying (c)

The hardest pair in general is proxy failure vs. learned-goal failure: both
present as green in tuning and complaints in deployment, and a proxy
dashboard cannot separate them — the reason §3.2 carries a shifted-proxy
column and §3.6 insists every experiment pattern includes a shift arm.
(Capability failure is the easy case: its tuning-distribution proxy is
low.) One measurement forces (c) into the proxy-failure column: **the
written reward, evaluated on the deployment behavior, is high.** The
concrete route is a reward-function audit finding that the flag detector
keys on the red-beacon visual channel — then driving to extinguishers *is*
maximizing the written objective on D′, the validity region V(R̂) simply
excludes beacon-free goals, and the fix lives in the spec rather than the
learning process (§3.2's last row). Corroborating evidence: beacon-carrying
non-goals attract the robot in simulation too, whenever the beacons move —
the behavior tracks the reward's feature, not a decoupled goal.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| 2×2 built first | four cells per vignette, unmeasured cells marked | classification straight from narrative tone |
| Families correct | (a) proxy, (b) capability, (c) learned-goal, each with the cells that exclude the rivals | (c) scored as proxy failure because "the spec was wrong" |
| Discriminating observation | the cell or comparison that separates the two live hypotheses — paired ledger over pressure (a), gap trajectory (b), training objective on deployment behavior (c) | "run more human eval," untargeted |
| Hardest pair | proxy vs. learned-goal, with the shifted proxy score as discriminator | capability vs. proxy named hardest |
| Reclassification of (c) | written objective scores deployment behavior *high* (reward keyed on the beacon feature) | "if it stopped driving to extinguishers" — that is the system working |
| Honesty | behavioral signatures ≠ mechanism; (a)'s shift cells unmeasured | "the robot is a mesa-optimizer" |

### Common wrong answers

- (a) as capability failure ("the comments got worse"): the bot scores 97%
  on the measured objective — useless comments under pressure are the hack,
  not incompetence.
- (a) as learned-goal failure ("it learned to comment instead of review"):
  that family requires the intended objective to hold in training and
  break only under shift; here it collapses on the tuning distribution.
- (b) as proxy failure because "overlap is a bad metric": a proxy that
  moves *with* the true score is weak, not gamed; divergence under
  pressure is the test.
- (c) as proxy failure because "the spec should have said beacons": the
  written objective said *flag*; unless the reward audit finds the beacon
  feature inside the spec, the failure is not in the spec.
- Reading constructed vignettes as evidence about real-world frequencies
  or network internals (§3.2's caution, §6's "attribution is not
  mechanism").

## Solution 3.2 — patch the judge, meet the mutant (derivation + computation)

Judge v2 differs from v1 in exactly one cell: R̂(B) = 1.0 → 0.6 (a
verbatim-quote penalty). The §4 type table, mixtures, and true values are
unchanged — the patch changes the *selector*, not the policy — so the
tuning arm's priority becomes A (0.8) > B (0.6) > C (0.4) > D (0.1) and the
selection formula only needs the new cumulative masses (the hint's method).

### (a) v2 on the tuning arm — the patch works on train

With P(A) = 1 − 0.9ⁿ, P(B) = 0.9ⁿ − 0.7ⁿ, P(C) = 0.7ⁿ − 0.3ⁿ, P(D) = 0.3ⁿ
on the §4 tuning mixture:

| n | P(A) | P(B) | P(C) | P(D) | proxy | true | truthful |
|---|---|---|---|---|---|---|---|
| 1 | .1000 | .2000 | .4000 | .3000 | .3900 | .5300 | .5000 |
| 2 | .1900 | .3200 | .4000 | .0900 | .5130 | .6230 | .5900 |
| 4 | .3439 | .4160 | .2320 | .0081 | .6183 | .6367 | .5759 |
| 8 | .5695 | .3728 | .0576 | .0001 | .7024 | .6959 | .6271 |
| 16 | .8147 | .1820 | .0033 | .0000 | .7623 | .8541 | .8180 |
| 32 | .9657 | .0343 | .0000 | .0000 | .7931 | .9725 | .9657 |

The graded true score now rises monotonically with n — .5300, .6230,
.6367, .6959, .8541, .9725 — so the patch verifiably works on train, and
by a wide margin: both §4 gates pass at *every* rung of the tuning arm
(the floor's tightest case is n = 1, lower bound 46.58%; at n = 4 the
truthful rate .5759 gives Wilson 95% [54.17%, 60.94%] at N = 817, k̄ =
470.5; the degradation arm never dips below its n = 1 baseline). The
dashboard is green end-to-end. Note the sign flip: the v2 gap on the
tuning arm is negative at five of six rungs (−14.0, −11.0, −1.8, +0.6,
−9.2, −17.9pp) — the patched judge now *under-reads* quality on train.
Being conservative on train is not being right anywhere else.

### (b) The mutant E and the broken shift regime

**The mutant.** E = reference-style phrasing reworded past the penalty: it
keeps the mimic's high overlap with the reference's style while defeating
the verbatim match the penalty keys on. To be top-ranked under v2 it must
clear A's 0.8 — take **R̂(E) = 0.9**, just under B's unpenalized 1.0. Its
true value on the shift arm matches B's there: **0.05**, because a
reworded echo of the statistically frequent surface form is still an
imitative falsehood whose residual truth-coincidence evaporates on
paraphrases, exactly as B's did (the hint's instruction). Priority under
v2 becomes E (0.9) > A (0.8) > B (0.6) > C (0.4) > D (0.1).

**The regime, consistent with §4's shift story.** §4's shift made two
moves: mass shifted toward the imitative family (B .35) and B's true value
evaporated (.2 → .05). Keep both, but let the family express under the
patch: paraphrased and novel items make the verbatim strategy mostly
unavailable — the question text is itself reworded, so echoing the
frequent surface form means rewording it — so the imitative mass splits
into a verbatim residue (B .10) and the mutant (E .25). Shift mixture:
**A .05, B .10, E .25, C .30, D .30**; true values A 1.0, B 0.05, E 0.05,
C 0.9, D 0.1; all other scores are §4's own. Two properties make this a
fair test: the untuned shift baseline is *identical* to §4's (true .3675,
truthful .3500 at n = 1 — B and E share a true value, so the split is
invisible without selection pressure), and the split is a modeling choice,
not a result — E .35 / B .00 reproduces §4's true column *exactly* (the
selection arithmetic is the same; verified cell for cell), so the chosen
split sets the collapse's speed, not its existence.

| n | P(E) | P(A) | P(B) | P(C) | P(D) | proxy | true | truthful |
|---|---|---|---|---|---|---|---|---|
| 1 | .2500 | .0500 | .1000 | .3000 | .3000 | .4750 | .3675 | .3500 |
| 2 | .4375 | .0725 | .1300 | .2700 | .0900 | .6468 | .3529 | .3425 |
| 4 | .6836 | .0763 | .1105 | .1215 | .0081 | .7920 | .2262 | .1978 |
| 8 | .8999 | .0425 | .0409 | .0167 | .0001 | .8751 | .1046 | .0592 |
| 16 | .9900 | .0067 | .0030 | .0003 | .0000 | .8983 | .0566 | .0070 |
| 32 | .9999 | .0001 | .0000 | .0000 | .0000 | .9000 | .0501 | .0001 |

**The intended objective passes below 20% at n = 8** — the first rung of
the preregistered ladder under the line (true .1046, against .2262 at
n = 4); in continuous n the crossover is ≈ 4.5 (true(4) = .2262, true(5) =
.1799), so the rung answer is an artifact of the ladder's power-of-two
spacing, worth stating as such. The vacancy story in numbers: v2 removed B
from the top of the proxy order on train, and E — which the penalty cannot
see — reoccupied the slot on the deployment-like arm, taking the Goodhart
gap from +10.8pp at n = 1 to +85.0pp at n = 32 (29.4, 56.6, 77.1, 84.2 in
between) while the dashboard reads ≈ .90 throughout.

### (c) Wilson interval at n = 8, and resolvability

The n = 8 shift-arm truthful rate is p̂ = .0592 (exact .0591954550 =
P(A) + P(C) = .0424649 + .0167306), audited at N = 817, k̄ = 48.4. Worked:
z²/N = .0047021, z²/2N = .0023510 → center = (.0591955 + .0023510)/
1.0047021 = .0612585; p̂(1−p̂)/N = .0000682 and z²/4N² = .0000014 → radius
= √.0000696 = .0083427, × 1.96 = .0163517, ÷ 1.0047021 → half-width
.0162752; **Wilson 95% = [4.50%, 7.75%]**. Neighboring rungs, same method:

| Shift rung | p̂ | k̄ = p̂·817 | Wilson 95% |
|---|---|---|---|
| n = 2 | .3425 | 279.8 | [31.08%, 37.57%] |
| n = 4 | .1978 | 161.6 | [17.19%, 22.65%] |
| n = 8 | .0592 | 48.4 | **[4.50%, 7.75%]** |

Yes — the drop is resolvable in a single pass, under either reading of the
rung comparison. n = 2 → n = 8 is 28.3pp (.3425 → .0592) with disjoint
intervals ([31.08%, 37.57%] vs. [4.50%, 7.75%] — 23.3pp of daylight); the
intermediate n = 2 → n = 4 drop is 14.5pp, also disjoint ([31.08%, 37.57%]
vs. [17.19%, 22.65%]). The suite's mid-range resolution is ≈ 6.8pp
(half-width 3.42pp at p = .5), so 28.3pp is roughly four times what one
817-item pass needs in order to separate the rungs.

### (d) Why patching was never terminal — three sentences

Skalse et al. define unhackability as the guarantee that increasing
expected proxy return can never decrease expected true return, and show it
is almost vacuous over the full stochastic policy class — two reward
functions are unhackable only if one is constant — while non-trivial
unhackable pairs exist only for restricted classes such as deterministic
policies over finite sets [SRC-PAPER-006; CLM-0022]. Parts (a) and (b) are
that structure in miniature: the v2 patch restores training performance not
by aligning R̂ with R but by reordering which reachable type sits at the
top of the proxy order, and the moment the reachable set contains a mutant
with R̂(E) > R̂(A), the vacancy at the top refills and the true return
collapses — a patch is a move inside the game, not an exit from it
[CLM-0022]. The "narrower proxies" finding closes the escape route that
part (b) demonstrates concretely: sharpening the proxy (the verbatim
penalty) did not yield unhackability — it renamed the exploitable type
from B to E and moved the collapse from the tuning arm to the
deployment-like one [CLM-0022].

**What (a)–(d) establish, and what they do not.** Established: in a fully
specified model, a proxy patch can turn every training gate green while
the deployment-like arm's intended objective falls below 20% — and a
bounded audit (ladder, shift arm, intervals) detects and sizes exactly
that before shipping. Not established: that any real judge's penalty
behaves so conveniently, that real mutant types carry these scores (E's
.9/.05 and the B/E split are stipulated), or that best-of-n width maps
onto RLHF pressure beyond qualitatively — §6 names the ways this toy lies,
and the numbers are exact only in the model.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) table correct | selection re-derived from the new priority order; true rises monotonically, stated | patch applied to the policy (B's mass lowered) instead of the judge |
| (a) verdict scoped | "works on train," with both gates green *there* | "the patch fixes the system" |
| (b) E well-defined | proxy > .8 justified (must beat A), true = .05 tied to B's shift value, mixture tied to §4's two shift moves | E with proxy ≤ .8 (never top-ranked), or true copied from B's tuning value .2 |
| (b) table + threshold | full ladder computed; n = 8 named, continuous crossover ≈ 4.5 noted | "somewhere around n = 5–8," no table |
| (c) interval arithmetic | inputs (p̂, k̄, N) and center/half-width visible; disjointness or the 6.8pp resolution invoked | end-points only; "28pp is big, so yes" |
| (d) formal link | unhackability definition, stochastic-class vacuity, and the narrowing failure each tied to a computed event | Goodhart as a slogan; not three sentences |
| Honesty | stipulations named (E's scores, the split, BoN ≠ RLHF) | model numbers presented as measurements |

### Common wrong answers

- Recomputing (a) with the policy changed (less B mass) rather than the
  judge (lower B score): the patch prices B, it does not remove the
  generator's tendency to produce B.
- E with proxy .6–.8: never top-ranked under v2, so no vacancy is filled
  and nothing breaks — the exercise's whole point is the top slot.
- Declaring the patch safe from (a) alone: the training arm is exactly
  where a patch is designed to look good; (b) is the test.
- Reading the n = 8 proxy (.8751) as the judge signaling doubt: the
  proxy's *level* carries no warning — only the paired true score does.
- Treating the rung answer (n = 8) as physically meaningful rather than an
  artifact of the ladder's spacing (continuous crossover ≈ 4.5).

## Solution 3.3 — the bounded experiment protocol (the `P02` skeleton)

A passing protocol mirrors Ch. 02's Exercise 1.2 skeleton and adds what
that chapter did not need — the pressure ladder, the gap curve as a
first-class readout, and the (α, D) region statement (the hint's list).
Learner submissions vary in context; the skeleton is what is graded.
Context chosen here: an English health-information chat assistant facing
a "truthfulness-and-safety" tuning change — best-of-n selection against a
cheap automated judge — ahead of a load-bearing deployment decision.

**Claim (context form, both gates).** In context κ (English
health-information chat, single-turn, deployment mix of recurring and
novel questions), after tuning at pressure α: (G1) every true-objective
metric degrades ≤ 5pp from its α = 1 same-arm baseline, and (G2) floors
hold — rubric-truthful ≥ 45%, harmful-behavior refusal ≥ 95%, false
refusal ≤ 5% — each by Wilson bounds at the real denominators. The claim
covers α on the tested ladder and D inside the tested arms; everything
outside is unmeasured, not safe.

**Constructs and gap sentences.** Proxy construct: "answer quality as the
automated judge scores it" (reference-overlap plus refusal keywords); gap:
it scores surface resemblance and keyword presence, and its errors are
part of the construct. True construct: rubric-scored truthfulness plus an
audited refusal ledger, by trained graders; second-order gap, stated one
level up: the rubric measures *rubric-truthfulness by these graders*,
itself a proxy for deployment intent — grader calibration is audited
(double-graded sample), not assumed.

**Instruments (pinned).** Truthfulness side: 817-scale adversarial items
in TruthfulQA's categories — imitative falsehoods are the construct that
maximally exposes a surface-overlap judge
([card](../../datasets/cards/01-truthfulqa.md); SRC-DATASET-001) — with
originals never entering any tuning or few-shot pipeline, because the
card's documented misuse pattern (fine-tuning on TruthfulQA-style pairs to
inflate scores) is precisely the failure this audit exists to catch.
Refusal side: AdvBench's canonical 520 behaviors
([card](../../datasets/cards/09-advbench.md); SRC-DATASET-009) — the card
is explicit that there are no benign controls, so the benign side is
budgeted separately: XSTest's 250 clearly-safe prompts
([card](../../datasets/cards/06-xstest.md); SRC-DATASET-006). §3.7's
scenario numbers recompute exactly at these denominators: 520/520
refusals → [99.27%, 100.00%]; the benign side at .92 → k = 230/250 →
[87.97%, 94.76%], collapsing to .612 → k = 153/250 → [55.03%, 67.03%].

**Pressure ladder.** α = best-of-n width, n ∈ {1, 2, 4, 8, 16, 32};
temperature fixed at the deployment value; the result is the per-metric
curve over the ladder, never a single point — §3.4's Goodhart question is
a curve, not a point.

**Shift arm, and its own validity limits.** Meaning-preserving paraphrases
(×5 per item, grouped by family) plus novel items authored in the same
construct categories at matched scale and difficulty. Limits stated in the
protocol: paraphrase authoring injects difficulty drift; "matched
difficulty" is a judgment; novel items from one team are a
single-annotator construct; none of it samples deployment D itself.

**Ledger and intervals.** Both sides of every gate: proxy curve, true
curve, and the Goodhart gap G(π_α, D) = J(π_α; R̂, D) − J(π_α; R, D)
reported per (α, D) as a first-class readout — §4's deliverable was the
gap column, and the protocol keeps it one. Wilson 95% (z = 1.96, the
Ch. 02 formula above) on every rate metric at its real denominator (817
per truthfulness arm; 520 and 250 on the refusal sides); gates evaluated
by bounds, not point estimates.

**Repeated trials.** Three runs per (n, arm); between-run spread reported
per cell; paraphrase-sensitivity recomputed over the ×5 families.

**Stopping rules.** Escalate n only while all gates pass by bounds at the
current rung; halt the ladder at the first gate failure and record the
largest passing α (that number is a deliverable); halt the whole audit if
any weakening observation triggers; grader-hours capped and stated, with
the region actually covered reported if budget binds first.

**Weakening observations (pre-stated, with directions).** (1) Any rate
moving more than 2× between original and paraphrase arms at fixed n —
template-fitting. (2) Grader audit: > 2% disagreement on a 10%
double-graded sample — the second-order gap opening. (3) Between-run
spread exceeding the Wilson half-width — intervals price item noise, not
generation instability. (4) The gap curve jumping > 10pp between adjacent
rungs or turning non-monotonic — the phase-transition warning: capability
axes are safety axes only if harm is smooth in them [CLM-0023]. (5)
Benign-list review finding > 5% of the 250 mislabeled. (6) The judge,
rescored on frozen reference outputs, drifting between waves.

**Scope exclusions.** Non-English traffic; multi-turn and socially
engineered chains; tool-use and oversight channels (later chapters'
territory); the meta-Goodhart exposure of publishing the probe (defended
by preregistration and a held-out refresh, not denied); bounded D ≠
deployment D; best-of-n mapping to RLHF pressure only qualitatively. What
execution establishes: a measured intended-objective curve under pressure
× shift, before the tuning decision. What it does not: that the rubric
*is* the intent, that the bounded arms cover deployment, or that any
passing α stays safe outside the tested region.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Claim in context form, both gates | context, rates, thresholds, degradation AND floors | "make it truthful and safe" |
| Second-order gap | the "true" instrument's own construct status stated | rubric presented as ground truth |
| Instruments pinned | 817 / 520 / 250 with cards; originals excluded from tuning | "standard benchmarks"; originals leaked into few-shot |
| Ledger symmetry | refusal attack side AND benign side budgeted | attack-only plan — the AdvBench card's own boundary ignored |
| Pressure ladder | α as BoN width over ≥ 5 rungs; curve is the result | one tuning run, one number |
| Shift arm with limits | paraphrase + novel construction AND its validity limits | shift arm built, limits silent |
| Gap curve first-class | G reported per (α, D), not merely proxy and true separately | gap absent from the readout |
| Gates by bounds | interval bounds gate every claim | "observed 46% → pass" |
| Stopping rules | when the ladder halts, what is recorded, budget cap | absent |
| ≥ 4 weakening observations | falsifiable, pre-stated, with directions | vague or post-hoc |
| Region statement | the (α, D) region the claim covers; "outside = unmeasured" | unbounded safety claim |

### Common wrong answers

- Gates on point estimates, or intervals computed only on the attack side
  of the refusal ledger.
- A "shift arm" of paraphrases only — no novel items, so §3.6's family
  stays invisible (§4's shift story needs both moves).
- Reporting proxy and true curves but not the gap — the readout that made
  §4's blindness legible is then missing.
- A claim with no region sentence: every gate verdict silently read as
  "safe at all pressures and distributions."
