# Ch. 02 — Exercises: hints, worked solutions, and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Attempt every exercise before reading past its hint. Rubrics grade the
reasoning trail, not just the final number — an unsupported right answer
scores below a well-argued approximate one.

## Solution 1.1 — construct audit

### (a) Three constructs "96% safe" could mean

1. **Compliance-refusal calibration**: the model refuses a curated harmful
   behavior list at rate r₁ while complying with clearly-safe prompts at
   rate r₂. "96% safe" = some blend of the two ledgers.
2. **Toxicity avoidance**: generated outputs fall below a toxicity
   classifier's threshold at rate 0.96 under a prompt distribution.
3. **Safety knowledge**: the model selects the correct answer on
   multiple-choice safety-concept items (a *knowledge* construct —
   SafetyBench's shape [cards/13], not a behavior construct at all).

### (b) One instrument per construct (verified composition facts)

1. Calibration: **XSTest** — 250 safe prompts across ten types + 200 unsafe
   contrasts [cards/06; SRC-PAPER-003]; or **JBB-Behaviors** — 100 harmful +
   100 benign behaviors with in-file source lineage [cards/10]. Boundary
   (from the card): English-only; no borderline-middle prompts; measures a
   calibration corner, not overall safety.
2. Toxicity: **RealToxicityPrompts** — ~99.4k rows scored across eight
   subcategories [cards/03]. Boundary: machine-scored labels (the
   classifier is part of the construct); English; completion-style, not
   chat.
3. Knowledge: **SafetyBench** — 11,435 MCQs across 7 categories, Chinese
   and English [cards/13]. Boundary: fixed-option items measure knowledge
   *about* safety norms, not safe behavior.

### (c) The first question

"What exact behaviors were refused, out of how many, on which revision of
which behavior set — and what was the false-refusal rate on the benign
side?" This beats "which benchmark did you use?" (still no denominators)
and "is it peer-reviewed?" (venue does not supply splits or intervals).
The chosen question forces **both sides of the ledger plus provenance** —
the three things a "96% safe" claim cannot survive without.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Constructs distinct | three genuinely different measurement targets | three synonyms for refusal |
| Instruments + verified numbers | composition facts cited with card references | "a large prompt set" with no provenance |
| Negative scope honored | each instrument paired with its card's boundary | instrument presented as measuring "safety" |
| Question choice justified | denominators + benign side + provenance named | "what's your benchmark score?" |

## Solution 1.2 — preregistered evaluation plan (worked skeleton)

A passing plan for a coding assistant with shell access, in the required
sections (learner submissions vary in context; the *skeleton* is what is
graded):

**Claim.** In context κ (coding assistant, English, shell access limited to
the repository working directory, human reviews diffs before merge): the
guard refuses ≥ 95% of destructive-command requests (Wilson lower bound ≥
0.95) and false-refuses ≤ 5% of routine development requests (Wilson upper
bound ≤ 0.05).

**Constructs and gap sentences.** Destructive-request refusal — scored by a
refusal classifier on model responses; the gap: classifier false negatives
under-report refusals, so the measured rate is a *lower* bound only if the
classifier's false-refusal rate is itself audited. Routine-request
compliance — scored by attempted completion; the gap: "routine" is defined
by our curated list, not by user-population statistics (coverage boundary
stated).

**Instruments (pinned).** Attack side: destructive-command behaviors
authored for the context (rm -rf variants, force-push, secret exfiltration
attempts) at the AdvBench scale discipline (520-slot budget, revision
hash recorded; category-level description only — the list itself is the
repository's held-out asset, not published) [cards/09 discipline]. Benign
side: routine requests sampled to XSTest's structure (ten
superficial-similarity types, 250-slot budget) [cards/06].

**Splits/grouping.** No training; grouping unit = *request template family*
for paraphrase repeats (each behavior × 5 paraphrases; spread across
families reported, not pooled). Tuned-vs-untouched: any guard threshold
tuning happens on a declared 20% of behaviors; results reported separately
on the untouched 80% forever.

**Intervals and thresholds.** Wilson 95% on both ledgers; decision rule
pre-stated: "support" = both thresholds met *by the bounds*, not point
estimates.

**Repeated trials.** Temperature fixed at deployment value; 3 runs;
between-run spread reported; paraphrase-sensitivity run: ASR and
false-refusal recomputed over the 5× paraphrase family — a doubling
flags template-fitting.

**Weakening observations (pre-stated).** (1) paraphrase-sensitivity
doubling; (2) scorer audit finds > 2% false-refusal labels; (3) benign
list review finds > 5% mislabeled "routine" items; (4) between-run spread
exceeds interval width.

**Scope exclusions.** Non-English; multi-turn social-engineering chains;
tool-output injection (Ch. 13's territory); latency.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Claim in context form | context, rates, thresholds stated | "make it safe" |
| Gap sentences | score-construct gap explicit per metric | construct and score conflated |
| Pinned instruments | revisions/names recorded | "standard benchmarks" |
| Ledger symmetry | attack AND benign sides budgeted | attack-only plan |
| Decision rule by bounds | bounds, not point estimates, gate the claim | "95% observed → pass" |
| Weakening observations | pre-stated, falsifiable, ≥ 3 | absent or vague |
| Grouping unit | named and applied to repeats | pooled paraphrases |

## Solution 1.3 — interval drill (full arithmetic)

Method (z = 1.96, z² = 3.8416): center = (p̂ + z²/2n)/(1 + z²/n);
half-width = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n).

**(a) 12/200 refusals (p̂ = 0.06, n = 200).**
z²/2n = 0.0096; z²/n = 0.0192. center = (0.06 + 0.0096)/1.0192 = 0.0683.
p̂(1−p̂)/n = 0.0564/200 = 0.000282; z²/4n² = 0.0000240; √ = 0.017493;
×z = 0.034287; ÷1.0192 → half = 0.0336.
**Wilson 95% = [3.5%, 10.2%].** Claim "rate ≤ 5%": **not supported** —
the interval extends to 10.2%.

**(b) 0/100 attack successes.**
center = (0 + 0.0192)/1.0384 = 0.0185; half: p̂(1−p̂) = 0, so half =
z·√(z²/4n²)/(1+z²/n) = 0.0185.
**Wilson 95% = [0%, 3.7%].** Claim "rate is 0%": **not supported** — 0/100
is consistent with true rates up to ~3.7%. (Compare the Clopper-Pearson
exact upper bound ≈ 3.7% — the two agree here; the "rule of three"
approximation gives ~3%.)

**(c) 30.0% on BOLD political domain (1,984 prompts, 12 sub-groups).**
The right denominator is **per sub-group** (~165 prompts each) for any
*disparity* claim, because the political-ideology domain's prompts are
seeded by sub-group [cards/02] — sub-group is the grouping unit. Domain-
level rate (independent-items assumption, n = 1,984): center 0.3004, half
0.0201 → **[28.0%, 32.1%]** — the claim "between 28% and 32%" **just
fails** (upper bound 32.1%). Per-sub-group (n ≈ 165): center 0.3046,
half 0.0693 → **[23.5%, 37.4%]** — decisively unresolvable. The honest
answer must state which assumption it used and why.

**(d)** Covered inline above: (a) not ≤ 5%; (b) not 0%; (c) not
[28%, 32%] under either assumption (marginal under independence, clear
under grouping).

**(e) Wald on (b):** 0 ± 1.96·√(0·1/100) = **[0, 0]** — degenerate. The
Wald standard error vanishes when p̂ = 0, so the interval asserts *zero*
uncertainty from finite evidence: "no failures in 100 trials" becomes
"the true rate is exactly zero", which 100 trials cannot establish. Wilson
keeps the uncertainty honest by construction (its √ term never collapses
while n is finite).

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Arithmetic shown | center and half-width visible | end-points only, unverifiable |
| (b) interpretation | "consistent with up to 3.7%", not "zero" | "proves rate is 0%" |
| (c) grouping caught | sub-group identified as the unit | naive n = 1,984 presented as unproblematic |
| (e) mechanism | SE-collapse at p̂ = 0 explained | "Wald is just inaccurate" |

## Solution 1.4 — contamination investigation design

**Design skeleton.** Timing evidence: score the model against its
documented knowledge cutoff — a score jump *coincident with the benchmark
entering web crawl windows* is the primary timing signature. Paraphrase
arm: rephrase all 817 questions (meaning-preserving) — construct skill
transfers to paraphrases; memorized surface forms partially do not, so a
large drop (pre-registered magnitude, e.g. > 10 points) weakens... wait —
it *supports* contamination and weakens the construct interpretation.
State the direction correctly: **paraphrase robustness weakens the
memorization hypothesis; paraphrase fragility weakens the construct
interpretation.** Format arm: MC-option reordering (TruthfulQA's
multiple-choice forms) — memorized answer-letter mappings break under
reordering. Novel-item arm: author fresh questions in the same
adversarial categories (Misconceptions-style) — if performance collapses
on matched-difficulty novel items while remaining high on originals,
memorization is the parsimonious explanation.

**What would weaken the memorization hypothesis:** (1) high paraphrase
robustness; (2) high performance on matched novel items; (3) error
*structure* aligned with the construct (failures concentrate in the same
categories humans fail) rather than with item popularity/recency in web
text.

**Validity limits of the study itself:** paraphrase authoring is itself
noise-injecting (difficulty drift); "matched difficulty" is a judgment;
novel-item authoring by one team is a single-annotator construct; and the
arms cannot fully separate "memorized items" from "memorized
*patterns*" — the deepest form of contamination is distributional, not
item-level, and no item-level study resolves it.

### Grading rubric (assessor)

Pass requires: ≥ 3 arms with predicted directions stated *before*
results; at least one result pattern that would *weaken* the memorization
hypothesis (not only confirm it); and an explicit statement of the
study's own limits. Fail signatures: arms without directional
predictions; "high score = contamination" as the only reading; no limits.

## Solution 1.5 — split repair

**WildChat** [cards/12]: dependence = conversation sessions (multi-turn,
same user across sessions, temporal drift). Discipline: **temporal split**
(train < validation < test in time; never random), session-disjoint.
Remaining risk: periodic content recurrence (news cycles, viral prompts)
correlates distant periods — temporal disjointness does not remove
semantic recurrence. Report sentence: "Train and test windows are
temporally disjoint (dates pinned); semantic recurrence across windows
(e.g. recurring viral templates) is not controlled and could inflate
transfer."

**BeaverTails** [cards/07]: dependence = prompt–response families and the
four-scale configurations. Discipline: **configuration-named,
prompt-disjoint splits** (a prompt's responses never straddle train/test);
report results per configuration (30k-scale and 330k-scale are different
instruments). Remaining risk: near-duplicate prompts *across* the 30k and
330k families — a model validated on one family may have seen
paraphrases in the other. Report sentence: "Results use the
[configuration] test set; cross-configuration prompt overlap was not
measured and could bridge the reported train/test separation."

**ToxiGen** [cards/04]: dependence = machine-generated statements from
shared prompts (paraphrase-prone by construction). Discipline: **grouped
split by generating prompt** (all descendants of one prompt stay on one
side) + near-duplicate hashing across splits before any claim. Remaining
risk: generator style itself is a shared shortcut across the whole
dataset — even a clean split leaves "detects this generator's style"
confusable with "detects implicit toxicity". Report sentence: "Splits are
grouped by generating prompt and near-duplicate-checked; classifier
performance may still partially reflect generator style, which grouping
cannot remove."

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Dependence named | session/config/prompt respectively | generic "correlated" |
| Discipline matches | temporal / named-config / grouped-by-prompt | "random is fine" |
| Residual risk honest | a risk the discipline does NOT remove | claims the fix is complete |
| Report sentence | reader-visible, specific | boilerplate disclaimer |

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-07-lab-vs-field](../../courses/boaz-barak-cs2881/lecture-07-lab-vs-field.md) — watch before working the measurement-design exercises.
- **DeepMind course**, [part-03-03-dangerous-capability-evaluations](../../courses/google-deepmind-agi-safety/part-03-03-dangerous-capability-evaluations.md) — watch before working the construct-validity exercises.
