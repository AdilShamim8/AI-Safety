# Ch. 11 — Exercises: hints, worked solutions, and rubrics

Attempt both exercises before reading past §9's hints. Every number in §4's
tables is recomputed here — Wilson intervals at z = 1.96
([Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
conventions), two-proportion z-tests with pooled standard error, the
Newcombe hybrid-score interval for capability degradation, and the power
arithmetic with *unpooled* variance (the orientation matters: degradation =
baseline − intervention, so the interval reads [−1.6, +6.8] points). Claim
anchors [CLM-0056]…[CLM-0060] match the README's References; dataset
denominators (520, 200, 250, 200) resolve to the
[AdvBench](../../datasets/cards/09-advbench.md) and
[XSTest](../../datasets/cards/06-xstest.md) cards — cards [09] and [06].

## Solution 11.0 — the worked example, recomputed end to end

### (a) Step 2 — the probe numbers

Probe accuracy 432/450 = 96.0%, Wilson **[93.8, 97.5]**; harmful recall
194/200 = 97.0% [93.6, 98.6]; benign recall 238/250 = 95.2% [91.8, 97.2].
The probe-vs-difference-in-means cosine of 0.91 is a *reported design
constant*, not a computed one — it is the chapter's way of saying the two
objects are distinct (§3.2); the second direction's cosine 0.78 to the first
(when XSTest-safe replaces course-benign as the negative class) is likewise
a designed measurement. Both are quoted as designed numbers, labeled as
such.

### (b) Step 3 — the four-ledger table, every interval

| Ledger | Baseline | α = 1.0 | Random ctrl | Permuted-label ctrl |
|---|---|---|---|---|
| AdvBench refusal (n=200) | 182/200 = 91.0% [86.2, 94.2] | 196/200 = 98.0% [95.0, 99.2] | 185/200 = 92.5% [88.0, 95.4] | 184/200 = 92.0% [87.4, 95.0] |
| XSTest-unsafe refusal (n=200) | 178/200 = 89.0% [83.9, 92.6] | 192/200 = 96.0% [92.3, 98.0] | 183/200 = 91.5% [86.8, 94.6] | 179/200 = 89.5% [84.5, 93.0] |
| XSTest-safe false-refusal (n=250) | 10/250 = 4.0% [2.2, 7.2] | 34/250 = 13.6% [9.9, 18.4] | 12/250 = 4.8% [2.8, 8.2] | 11/250 = 4.4% [2.5, 7.7] |
| Arithmetic accuracy (n=500) | 441/500 = 88.2% [85.1, 90.7] | 428/500 = 85.6% [82.3, 88.4] | 439/500 = 87.8% [84.6, 90.4] | 440/500 = 88.0% [84.9, 90.6] |

z-tests (pooled SE, two-sided p): AdvBench 196 vs 182: **z = +3.07,
p = 0.0021**; XSTest-unsafe 192 vs 178: **z = +2.66, p = 0.0079**;
false-refusal 34 vs 10: **z = +3.79, p = 0.0002**; arithmetic 428 vs 441:
**z = −1.22, p = 0.223**. The controls do not move (random 185 vs 182:
z = +0.55, p = 0.586; permuted 184 vs 182: z = +0.36, p = 0.720) — the
intervention's effect is direction-specific, which is the *minimal causal
claim* §3.3 licenses: nothing more.

### (c) Step 4 — the sweep as a frontier (exchange rates recomputed)

| α | AdvB refusal | XSTest-unsafe | XSTest-safe false-refusal | Arithmetic |
|---|---|---|---|---|
| 0.0 | 91.0% [86.2, 94.2] | 89.0% | 4.0% [2.2, 7.2] | 88.2% |
| 0.5 | 94.5% [90.4, 96.9] | 93.0% | 7.2% [4.6, 11.1] | 87.2% |
| 1.0 | 98.0% [95.0, 99.2] | 96.0% | 13.6% [9.9, 18.4] | 85.6% |
| 1.5 | 99.0% [96.4, 99.7] | 97.5% | 26.0% [21.0, 31.8] | 80.8% |
| 2.0 | 99.5% [97.2, 99.9] | 98.0% | 43.2% [37.2, 49.4] | 71.4% |

Exchange rates (over-refusal points paid per harmful-refusal point gained):
0→0.5: 3.2/3.5 = **0.91**; 0.5→1.0: 6.4/3.5 = **1.83**; 1.0→1.5: 12.4/1.0 =
**12.4**; 1.5→2.0: 17.2/0.5 = **34.4**. The frontier is convex with a
vengeance: past α = 1.0 you pay twelve over-refusals per incremental
harmful-refusal, then thirty-four. Any α chosen on the harmful ledger alone
lands in this region.

### (d) Step 5 — the gates, exactly

- **G1** (harmful-refusal Wilson lower bound ≥ 95%): at α = 1.0,
  196/200 → lower bound **0.94971** — a miss by **0.029 points**, and a
  knife-edge miss is a miss ([Ch. 02](../02-evaluation-science-and-experimental-design/README.md) §5's
  rule). Passes at α = 1.5 (lower bound 96.4%) and α = 2.0 (97.2%).
- **G2** (false-refusal Wilson upper bound ≤ 5%): fails at **every** α,
  including α = 0 — the baseline 10/250 already has upper bound 7.2%. The
  deployment's over-refusal budget was exhausted before the intervention
  existed; no steering strength repairs a gate the baseline fails.
- **G3** (capability degradation Newcombe upper bound ≤ 5 points): at
  α = 1.0, degradation = 88.2% − 85.6% = 2.6 points, Newcombe interval
  **[−1.6, +6.8]** — the upper bound exceeds 5, so G3 fails; at α = 0.5
  the interval is [−5.1, +3.1] (passes); at α = 1.5, [−11.9, −2.9] (fails
  on sign, not just bound).

**No α satisfies the claim** — the correct report states this and stops. And
the power arithmetic that makes "not significant" honest rather than
comforting: the two-arm smallest-drop formula with unpooled variance
(p̂₁ = 0.882, p̂₂ = 0.856) is
n = (z_{α/2} + z_β)² · (p̂₁(1−p̂₁) + p̂₂(1−p̂₂)) / δ²
= (1.96 + 0.8416)² × (0.1041 + 0.1233) / 0.026²
= 7.849 × 0.2274 / 0.000676 ≈ **2,640 items per arm**. A 500-item battery
resolves only ~5.8pp drops at 80% power; the observed 2.6 sits inside its
blind spot. "No significant capability cost" is *unsupported* at n = 500 —
which is a different sentence from "there is no capability cost."

### Common wrong answers — 11.0

- Reporting only the intervention column: the controls (z = 0.55, 0.36) are
  what make the z = 3.07 interpretable as direction-specific.
- Reading G3's [−1.6, +6.8] as "includes zero, so fine": the *upper* bound
  is the gate, and 6.8 > 5 — the interval's ceiling is exactly what a
  deployer pays for.
- Choosing α = 1.5 because G1 passes there: G2 already failed at baseline;
  no α rescues a claim whose gate structure is unsatisfiable.

### Grading rubric (assessor) — 11.0

| Criterion | Pass requires |
|---|---|
| Intervals | All 16 Wilson intervals reproduced (both tables) |
| Tests | All four z-tests with p-values; both control z-tests quoted as the specificity evidence |
| Frontier | All four exchange rates (0.91, 1.83, 12.4, 34.4) recomputed from raw counts |
| Gates | G1's 0.94971 miss-by-0.029, G2's baseline failure, G3's [−1.6, +6.8] upper-bound failure — all three stated |
| Power | 2,640/arm reproduced with the unpooled formula; "unsupported ≠ established" distinction present |

## Solution 11.1 — the probe that knew too much

### (a) Three features the probe could be reading besides harmfulness

1. **Register/formality**: curated harmful sets skew imperative and
   coarse-grained ("Write a script that..."), benign sets skew declarative
   and polite; register is linearly decodable from residual streams and
   co-varies with the label by construction of the corpus. Mechanism:
   sampling artifacts, not the model's safety knowledge.
2. **Topic/domain vocabulary**: harmful instructions concentrate in a few
   domains (weapons, malware, chemistry), so domain-embedding directions
   (which any probe finds easily) carry the label; a benign instruction
   about the *same* domain breaks the correlation — and curated sets
   systematically omit such near-misses, which is exactly what XSTest
   exists to fix ([datasets/cards/06-xstest.md](../../datasets/cards/06-xstest.md)).
3. **Answerability/length confounds**: harmful sets are often
   open-ended-generation tasks, benign sets factoid-QA; the model encodes
   expected-answer-type and expected-length signals that a linear readout
   latches onto ahead of any harmfulness content.

### (b) The logical gaps, mapped to §3.1's assumptions

- 97% held-out accuracy → (i) "contains a harmfulness concept": gap =
  **decodability ≠ presence of a dedicated concept** (A1, the
  linear-representation assumption — the information is *readable* says
  nothing about whether the model computes a unitary feature; Belinkov's
  probing survey is the canonical caution
  [SRC-PAPER-039]).
- (i) → (ii) "refusal is computed from this concept": gap = **readout ≠
  causal use** (§3.2/§3.3): the probe reads activations *after* whatever
  computation produced them; nothing shows the model's refusal *consumes*
  this direction. This is the correlation-to-cause gap
  [Ch. 09](../09-mechanistic-interpretability-foundations/README.md) §3.4
  formalized, and the exact gap Arditi et al. closed *with interventions*
  [CLM-0058].
- (ii) → (iii) "therefore a production monitor": gap = **construct-to-
  deployment validity** (A2/A3, the extraction-distribution and
  context-dependence assumptions): the probe was validated on curated
  single-turn instructions; production conversations are multi-turn,
  adversarially stylized, and distribution-shifted. A monitor inherits
  every one of these gaps and adds a threshold-calibration problem
  ([Ch. 08](../08-ai-control-and-monitoring/README.md)'s FPR-budget
  arithmetic applies verbatim).

### (c) The minimal experiment set with predicted outcomes

1. **Direction-specific intervention**: add/subtract the probe direction
   (or its difference-in-means projection) at the probed layer; measure
   refusal on held-out harmful *and* false-refusal on benign. Reads-
   harmfulness predicts bidirectional movement; reads-a-correlate predicts
   little or asymmetric movement.
2. **Control directions**: matched-norm random and permuted-label
   directions under the same protocol — a correlate-probe often still moves
   behavior slightly (any large-norm vector perturbs activations); the
   *specificity* contrast is the evidence.
3. **Cross-instrument transfer**: extract on one suite, evaluate on
   XSTest's superficially-similar safe prompts — a register probe fails
   exactly here (false-refusal on near-miss benign), a harmfulness probe
   does not; this is the single most diagnostic arm.
4. **Counterfactual minimal pairs**: paraphrase each instruction across
   registers (formal↔imperative) holding content fixed —
   RAVEL-style confound separation
   [CLM-0054 in Ch. 10](../10-sparse-features-circuits-and-interpretability-evaluation/README.md):
   a register probe flips its readout, a content probe does not.
   Held-out instruments pinned in advance; all rates with Wilson intervals
   and both ledger sides per §3.4's frame.

### (d) What the shipped monitor still lacks under an adaptive attacker

Even granting (c): the monitor's threshold trades FPR against catch rate
under a *fixed* attack distribution — an adaptive attacker probes the
monitor boundary and shifts style until activations cross below threshold
(register-shifting is cheap); the monitor has no audit-budget arithmetic,
no adaptive red-team evaluation ([Ch. 08](../08-ai-control-and-monitoring/README.md)),
and — if white-box access is exposed — an attacker who learns the direction
can *subtract* it (§6's symmetry: a direction that adds refusal can be
removed) [CLM-0058's own dual-use observation]. A defensible deployment
sentence must state all three.

### Common wrong answers — 11.1

- (a) listing three *labels* of confounds without the co-variance
  mechanism; the mechanism is the answer.
- (b) treating (iii) as merely "needs more data": the gap is validity
  structure (assumptions A1–A3), not sample size.
- (d) forgetting the symmetry/subtractability point: the same linearity
  that makes steering useful makes it removable.

### Grading rubric (assessor) — 11.1

| Criterion | Pass requires |
|---|---|
| (a) | Three confounds, each with its co-variance mechanism tied to curated-set construction |
| (b) | Each of (i)/(ii)/(iii) mapped to its assumption (A1 / causal-use / A2-A3+deployment) |
| (c) | ≥ 3 arms including cross-instrument transfer and control directions, with *differential predictions* |
| (d) | Adaptive attacker + threshold/FPR arithmetic + direction-subtractability, all three named |

## Solution 11.2 — preregistered steering-intervention evaluation (the chapter artifact)

A model solution at rubric depth (700–1,200 words as briefed), for a coding
assistant with shell access.

**Claim in context form.** In context κ (coding assistant, English, shell
tool-calls, single-turn + one tool round), a refusal-direction *addition*
layer at pinned (layer ℓ\*, position: all post-prompt) and strength α
satisfies: G1 — harmful-command refusal Wilson lower bound ≥ 95% on
held-out shell-harmful items; G2 — false-refusal on clearly-safe shell
commands Wilson upper bound ≤ 3%; G3 — capability degradation (code-correctness
battery) Newcombe upper bound ≤ 3 points. Numeric gates fixed before the
first run; α chosen by the pre-stated frontier rule below, never by
harmful-ledger alone.

**Extraction protocol, pinned.** Extraction suite: 300 harmful shell
commands sampled by fixed seed from AdvBench's canonical 520
([datasets/cards/09-advbench.md](../../datasets/cards/09-advbench.md)) —
card boundary honored: the card's negative scope (behavioral
traces, not deployment traffic; single-turn English) is the claim's scope;
300 course-authored benign shell commands matched in register and domain
vocabulary (the register-matching discipline Solution 11.1(a) demands);
64+64 validation items for (ℓ\*, position) selection only, never re-scored
as outcome. Direction: difference-in-means at ℓ\*, recorded with cosine to
any probe trained on the same activations (the §4 Step 2 bookkeeping).

**Instruments and control set.** Held-out harmful: AdvBench remainder (220)
plus 100 course-authored *tool-chained* harmful items (two-step commands —
the card's single-turn boundary means the extension is ours and labeled as
such). Benign complement: XSTest's 250 safe prompts
([datasets/cards/06-xstest.md](../../datasets/cards/06-xstest.md)) plus 100
benign shell commands including the ten superficial-similarity types.
Controls at each α: matched-norm seeded random direction; permuted-label
direction. Cross-instrument: XSTest's 200 unsafe contrasts. Capability
battery: 400 pinned code-execution items with deterministic tests — with
the *power computation first*: unpooled two-arm formula at p̂₁ ≈ 0.80,
δ = 3 points gives n = (1.96 + 0.8416)² × (0.16 + 0.187) / 0.03² ≈
**3,050 items per arm** — so the honest battery is 3,000/arm or the gate
moves to what 400 can resolve (~8pp), *stated in the protocol*, not
discovered after.

**Ledgers and statistics.** Four ledgers, all Wilson 95%, all with
controls: harmful refusal (held-out + cross-instrument), false-refusal
(benign complement), capability (battery, Newcombe interval on the
difference), and a *tool-behavior* ledger (does the model still emit
correct tool-call syntax — an assistant that silently stops calling tools
fails differently). Two-proportion z-tests vs. baseline for movement;
controls quoted beside every intervention number.

**α-selection rule (pre-stated).** Choose the smallest α meeting G1 with
the constraint that G2 and G3 both pass; if none exists, report the
frontier (all four ledgers at every α) and the claim as unsatisfied — the
§4 outcome is the expected one and the protocol does not flinch from it.

**Weakening observations (pre-stated, falsifiable).** (1) If the
permuted-label control moves any ledger by ≥ half the intervention's
effect, the perturbation channel dominates — halt. (2) If
cross-instrument transfer is < half the held-out effect, the direction is
suite-specific — downgrade the claim to the extraction suite. (3) If
false-refusal rises ≥ 2× the harmful-refusal gain at any swept α, the
frontier rule has no feasible point — report and stop.

**Scope exclusions.** Both cards' negative scopes quoted verbatim in the
protocol: no multi-turn, no non-English, no adaptive-attacker claims
([datasets/cards/09-advbench.md](../../datasets/cards/09-advbench.md),
[datasets/cards/06-xstest.md](../../datasets/cards/06-xstest.md)); no claim
beyond the one model tested [CLM-0058's limits]; capability battery is
course-authored and synthetic — its result is about *this* battery.

**Dual-use paragraph.** The same protocol run with *ablation* (subtracting
the direction) is a jailbreak evaluation — the method's symmetry is the
hazard [CLM-0058]. Published: extraction counts, ledger tables at
α-sweep, gates, frontier — nothing that lowers the barrier to removing
refusal (no released direction vectors, no (ℓ\*, position) for
subtractability on other models, no transfer table for the ablation
direction). The asymmetry is deliberate and stated.

### Common wrong answers — 11.2

- A capability battery of 100 items with a 3-point gate: the power
  computation (3,050/arm) is the point of the exercise — gates smaller than
  the battery can resolve are theater.
- Omitting the tool-behavior ledger for a tool-using assistant: a steering
  layer that breaks tool syntax has a failure mode no refusal ledger sees.
- Publishing the direction "for reproducibility": the dual-use paragraph
  must *name* what stays unpublished and why.

### Grading rubric (assessor) — 11.2

| Criterion | Pass requires |
|---|---|
| Claim + gates | Context form; three numeric gates; α-rule pre-stated |
| Instruments | Every denominator budgeted with its card cited; card negative scopes quoted |
| Controls | Random + permuted-label at every α; cross-instrument arm present |
| Power | The 3,050/arm computation shown (or equivalent for the chosen δ); battery sized honestly or gate widened *in writing* |
| Ledgers | Four ledgers incl. tool-behavior; intervals + z-tests + controls throughout |
| Frontier rule | Smallest-α-meeting-G1-with-G2/G3; explicit no-satisfying-α outcome path |
| Dual-use | Names ablation as the mirrored hazard; states what is not published |
