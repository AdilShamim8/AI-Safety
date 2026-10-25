# Ch. 05 — Scalable oversight

> Every safety method in this course ends with something checking the system: a human rater,
> an eval suite, a monitor model, a reviewer committee. This chapter is about the case where the
> checker is the weak link — weaker than the system it checks, and wrong in ways that repeat.

## 1. Research question and failure pathway

**The question this chapter answers:** *how do you supervise a system whose behavior you
cannot reliably evaluate — and how do you measure, before you depend on it, whether your
supervision scheme has a ceiling it can never cross no matter how much you spend?*

**The failure pathway it prevents:**

```text
system capability grows ──► honest evaluation exceeds supervisor budget ──►
oversight quietly becomes rubber-stamping ──► the system optimizes against the
supervisor signal ──► failures concentrate exactly where supervision is weakest
```

Each arrow is a place where the *checking*, not the system, degrades. The RLHF loop that
aligns a production assistant is literally "humans supervise model behavior" — and the
weak-to-strong literature opens from the observation that humans will eventually only be able
to *weakly* supervise systems more capable than they are, so techniques like RLHF may scale
poorly without dedicated work [CLM-0033]. For a deployer there is no opting out: your
evaluation team, your monitoring pipeline, and your acceptance tests are all supervisors.
Whatever they cannot check is behavior you shipped unaudited — and your training process is
quietly selecting *for* it, because whatever the supervisor rewards gets reinforced.

The chapter sits at the seam [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
built: Ch. 02 made the *measurement* trustworthy; this chapter asks what happens when the
measuring instrument is a model or a human with a bounded error profile and the thing measured
outstrips it. Ch. 02's discipline carries over unchanged, plus one new instrument:
supervisor-error arithmetic, including the correlated-error floor that bounds every committee
and every weak-to-strong setup (§3.6, §4).

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(construct validity, paired ledgers, Wilson intervals, denominators); diagnostic task B
([diagnostic](../../prerequisites/diagnostic.md)); refresher R3
([targeted refreshers](../../prerequisites/targeted-refreshers.md)).

**Outcomes.** After this chapter you can:

1. Explain weak-to-strong supervision, debate, decomposition, and process vs outcome
   supervision — for each, the mechanism, the load-bearing assumption, and the named failure
   mode.
2. Identify oversight failures, evaluator capability limits, and correlated errors; compute
   how error correlation sets a floor under committee-based oversight, with concrete numbers
   carried end-to-end.
3. Design a bounded comparison with checkable ground truth — the chapter's artifact, and the
   direct precursor of `projects/p05-weak-to-strong-or-scalable-oversight-analogue/`.

**Scope exclusions.** Preference-learning mechanics (reward models, DPO, Constitutional AI —
`chapters/04-preference-learning-and-post-training/`), control protocols under audit budgets
(`chapters/08-ai-control-and-monitoring/`), chain-of-thought faithfulness
(`chapters/18-reasoning-faithfulness-and-monitorability/`), and the human factors of
over-trusting automated checkers (`chapters/21-sociotechnical-and-systemic-risk/`) are each
covered by their own chapters. This chapter also does not run a live weak-to-strong experiment
— that is `projects/p05-weak-to-strong-or-scalable-oversight-analogue/`'s job; here we supply
the design and the arithmetic it must pass.

## 3. Core explanation

### 3.1 The oversight gap and the supervisor-error model

Let **σ** be the system being supervised (a strong model, an agent) and **ω** a supervisor (a
weaker model, a human rater, a judge). Let **G** be ground truth — labels that are cheap to
check and agreed correct for a *bounded* task (a fixed-option exam, a paired refusal suite).
A supervisor has a per-item error rate **ε** = Pr[ω disagrees with G]. The **oversight gap**
is the regime where σ's behavior is harder to evaluate than ω can afford: items too hard, too
numerous, or too slow to check honestly. Any oversight scheme must answer three questions,
and the third is the one teams skip:

1. **Coverage** — which behaviors does the supervisor actually see?
2. **Cost** — what does checking one item spend, and what budget exists?
3. **Error structure** — not just the error *rate* ε, but how errors are *distributed and
   correlated* across items and across supervisors.

Question 3 is the technical core: two supervisors with identical ε are interchangeable only if
their errors are independent. If they share failure modes — same pretraining distribution,
same human misconceptions, same blind spots — then more supervisors of the same kind stop
helping at a floor set by the shared error mass (§3.6). Correlated error is also the mechanism
behind TruthfulQA's construct: its 817 adversarial questions target *imitative falsehoods* —
falsehoods humans commonly repeat, which a model pretrained on human text reproduces *because
the wrong answer is more statistically frequent*
([TruthfulQA card](../../datasets/cards/01-truthfulqa.md)) — a catalog of correlated
human–model error, not random noise.

### 3.2 Weak-to-strong supervision

Weak-to-strong supervision is the empirical analogy: a weak model ω labels a task, a strong
model σ finetunes on those labels, and you measure how much of σ's capability survives. The
canonical study ran this across pretrained language models in the GPT-4 family on NLP, chess,
and reward modeling tasks: strong models naively finetuned on weak-model labels *consistently
outperform their weak supervisors* — weak-to-strong generalization — yet remain far from
recovering their full capabilities; simple methods helped substantially, e.g. GPT-4 finetuned
with a GPT-2-level supervisor and an auxiliary confidence loss recovering close to
GPT-3.5-level performance on NLP tasks [CLM-0030].

Two forces pull against each other:

- **Error inheritance.** The student learns the signal the labels carry, and errors that look
  like *signal* — systematic, structured, plausible — get reproduced confidently. The
  generalization bonus comes from the student's pretrained structure resolving items the
  supervisor got wrong, which works while supervisor errors are *uninformative noise* to the
  student; when they correlate with the student's own priors (overlapping pretraining text),
  the bonus shrinks — the imitative-falsehood trap again (mechanism statement: this course's
  operationalization; registered anchor: [CLM-0030]).
- **The elicitation gap.** Even with perfect labels, naive finetuning does not surface
  everything a strong model can do [CLM-0030] — supervision quality and *elicitation* are
  separate problems.

This course measures weak-to-strong runs with **performance gap recovered**,
PGR = (a_W2S − a_ω)/(a_σ\* − a_ω), where a_σ\* is the strong model's ceiling with ground-truth
labels on the same split (operationalization; §4 carries synthetic numbers through it).
PGR = 0 means the student sank to its supervisor; PGR = 1 means the gap fully closed.

### 3.3 Debate

Debate reframes supervision as an adversarial game: given a question or proposed action, two
agents take turns making short statements up to a limit, then a human judge decides which side
gave the most true, useful information; training is self-play on this zero-sum game
[CLM-0032]. The bet is that *judging a clash is easier than judging an answer* — a dishonest
debater is constrained by an opponent that can quote its earlier statements against it.

The theoretical framing — with optimal play, debate can answer any question in PSPACE given
polynomial-time judges, where direct judging manages only NP [CLM-0032] — is the paper's
stated analogy *assuming optimal play*, not a deployment guarantee. The empirical
proof-of-concept is an MNIST experiment: debating agents argue over digits shown to a judge
that sees only a few pixels, lifting that judge-analogue's accuracy from 59.4% to 88.9%
(6 visible pixels) and from 48.2% to 85.2% (4 pixels) [CLM-0032]. Recomputed: absolute gains
of +29.5 and +37.0 percentage points — the judge's error rate fell from 40.6% to 11.1% (a
72.7% reduction) and from 51.8% to 14.8% (71.4%) — a large effect, on a small toy, with a
classifier standing in for the human judge.

The load-bearing assumption is that **truth wins arguments in front of this judge**. The
failure mode is the evaluator capability limit: a judge persuaded by rhetoric, confidence, or
fabricated citations flips the advantage, and debate then *amplifies* the exploit it was meant
to contain. Nothing in the MNIST result tests persuadable human judges at deployment scale;
the paper itself flags open questions about scaling [CLM-0032].

### 3.4 Decomposition

Decomposition attacks the oversight gap by cutting a task into pieces a bounded supervisor
*can* check — verify each step, sub-claim, or component, then compose the verdicts. Real
datasets show the pattern: BBQ's paired design decomposes "stereotype bias" into two
separately measurable components — an *ambiguous* context where any specific answer reveals
reliance on stereotypes (the correct answer is "unknown"), and a *disambiguated* context where
knowledge is scored separately — across its 58,492 multiple-choice items
([BBQ card](../../datasets/cards/05-bbq.md)). Without that decomposition, "bias" is one
unmeasurable blob; with it, the construct splits into checkable sub-constructs with their own
denominators. The arithmetic has two faces, and the second is routinely ignored:

- **Catching power.** A wrong final answer is usually wrong because of one localized step. If
  a per-step check catches a wrong step with probability 1 − s, a solution whose single wrong
  step must survive scrutiny is wrongly approved with probability s — often far below the miss
  rate of an equivalent whole-answer audit, because steps are easier to check than wholes.
- **False-rejection compounding.** Each of the k checks is a new place to wrongly reject a
  *correct* item. If each correct step is falsely flagged with probability f, a correct k-step
  item survives all checks with probability (1 − f)^k — the false-rejection rate is
  1 − (1 − f)^k, which grows with k: at f = 2% and k = 8, 14.9% of correct solutions are
  falsely rejected somewhere; at k = 16, 27.6%. Decomposition buys catching power by spending
  correctness overhead, and the exchange rate worsens with chain length (Exercise 5.3).

Decomposition fails outright under **false decomposability**: if the "subtasks" are not
actually easier for *this* supervisor to check than the whole, the scheme adds overhead and
false rejections while catching nothing new — so decompositions must be validated per
supervisor, not assumed from the task's shape.

### 3.5 Process vs outcome supervision

Two places a supervision signal can attach. **Outcome supervision** labels the final product —
was the answer right, the response acceptable; cheap per item and deployment-aligned, but with
no gradient about *where* things went wrong. **Process supervision** labels each intermediate
step — is this step reasonable so far; it localizes errors (the catching-power face of §3.4)
and multiplies labeling cost and false-rejection surface (the second face). The distinction
and its tradeoffs as presented here are this course's operationalization; the canonical
empirical comparison is Lightman et al., *Let's Verify Step by Step* (arXiv:2305.20050), whose
abstract was fetched this session (2026-10-21) but which is deliberately **not** cited as
register-anchored fact here — no source-register ID was allocated to this unit for it — so it
stands as assigned deeper reading, not as evidence.

The catalog's real artifacts show where outcome labels live at scale: HH-RLHF's ~169k rows
(161k train / 8.55k test) are *pairwise outcome-level preferences* — a crowdworker judged
which of two whole responses was more helpful / less harmful ([HH-RLHF
card](../../datasets/cards/08-hh-rlhf.md)) — and 10% label noise on the train side alone is
16,100 noisy preference labels, a weak-supervision budget problem before training begins.
XSTest's 250 safe + 200 unsafe prompts are design-determined *outcome* labels on whole prompts
([XSTest card](../../datasets/cards/06-xstest.md)). Step-level ground truth is expensive —
which is why the catching-power vs false-rejection tradeoff deserves arithmetic first.

### 3.6 Correlated errors: the committee floor

The workhorse oversight design in practice is a committee: m supervisors vote (majority rules,
m odd) and the majority's verdict becomes the supervision signal. Under *independent* errors,
majority voting is Condorcet's machine: error falls toward zero as m grows. Under correlated
errors it stalls, and the stall point does not depend on m. Model the correlation with a
**shared blind spot**: with probability **q** a randomly drawn item sits in a failure mode
where *every* supervisor errs together (a shared misconception, a shared pretraining artifact,
a shared rater blind spot); otherwise supervisors err independently with residual rate
**ε′**. A supervisor's marginal error rate is then ε = q + (1 − q)ε′, and the pairwise error
correlation is ρ = [q + (1 − q)ε′² − ε²]/[ε(1 − ε)]. A committee of m errs when a blind-spot
item appears (contribution q) or when at least (m+1)/2 residual errors coincide. Carry
concrete numbers end-to-end (the error profile is a synthetic, declared teaching scenario;
the §4 denominators are verified card numbers): q = 0.04, ε′ = 1/16 = 0.0625, hence
ε = 0.04 + 0.96 × 0.0625 = 0.10 — each supervisor is a 90%-accurate checker — and ρ = 0.375,
moderate correlation. Majority vote gives:

| Committee size m | Committee error (blind spot) | Committee error (if independent) |
|---|---|---|
| 1 | 10.00% | 10.00% |
| 3 | **5.08%** | 2.80% |
| 5 | 4.21% | 0.86% |
| 7 | 4.04% | 0.27% |
| 9 | 4.01% | 0.09% |
| 11 | 4.00% | 0.03% |
| m → ∞ | **4.00% — the floor equals q** | → 0% |

Three supervisors cut the error rate in half (10% → 5.08%); five more judges buy 1.1 points;
infinity buys 1.08. The independent-error committee would have reached 0.86% at m = 5 and
0.03% at m = 11 — the entire difference between the columns is the 4% shared mass at
ρ = 0.375. **The asymptote of committee oversight is set by error correlation, not by error
rate or committee size.** The only levers that move the floor are *decorrelation* —
supervisors with genuinely different failure modes (different model families, human experts
auditing the blind-spot mass, different evidence sources) — or shrinking the blind spot itself.

This is the quantitative reason "evaluator capability limits" (outcome 2) is a measurement
problem, not a vibe: ρ is measurable per supervisor pair from an agreement/confusion audit on
labeled items, q is estimable as the all-wrong mass, and both belong in every oversight report
next to ε — which is what Exercise 5.4's design demands and what `projects/p05-weak-to-strong-or-scalable-oversight-analogue/`
will instrument.

## 4. Worked example: an oversight committee on a paired refusal suite

**The system.** An assistant σ answers prompts; before shipping, a committee of m = 3
supervisor models reviews each draft and can block it. **Your job:** predict what this
oversight layer actually catches *before* running it, so the report contains arithmetic
rather than hope.

**Step 0 — the task with checkable ground truth.** Both sides of the ledger, per Ch. 02's
paired-ledger rule, from one instrument: XSTest's verified composition of **250 safe prompts**
a calibrated model should comply with and **200 unsafe prompts** it should refuse, labels
design-determined by construction ([XSTest card](../../datasets/cards/06-xstest.md)). Ground
truth here is *checkable* — fixed, published, disagreement-free by design. The card's negative
scope carries over: XSTest excludes the borderline middle, so nothing here certifies judgment
on genuinely ambiguous prompts.

**Step 1 — the supervisors' error profile (synthetic, declared).** Each supervisor has ε = 0.10
against ground truth with a shared blind spot q = 0.04 (hence ρ = 0.375, §3.6) — a teaching
scenario, not a measured property of any model; in production it is obtained by the agreement
audit of Exercise 5.4 on a few hundred labeled items.

**Step 2 — single supervisor.** Expected mis-flags: 0.10 × 250 = 25.0 of 250 clearly-safe
requests wrongly blocked, and 0.10 × 200 = 20.0 of 200 harmful requests wrongly passed. A
measured 25/250 = 10% carries a Wilson 95% interval of [6.9%, 14.3%] — Ch. 02's arithmetic,
unchanged.

**Step 3 — the committee of three.** Committee error = q + (1 − q)[3ε′²(1 − ε′) + ε′³] with
ε′ = 1/16: the residual term is 3(1/16)²(15/16) + (1/16)³ = 46/4096 ≈ 0.01123, so the
committee errs on 0.04 + 0.96 × 0.01123 = **5.08%** of items (exactly 13/256). Expected
mis-flags: **12.7** on the safe side (vs 25.0) and **10.2** on the unsafe side (vs 20.0). If
the run flags 13 of 250, the measured rate 5.2% has Wilson 95% interval [3.1%, 8.7%] (center
0.0588, half-width 0.0281); 10 of 200 gives 5.0%, interval [2.7%, 9.0%].

**Step 4 — the projection trap.** Had the team assumed independent judges (same ε = 0.10
each), the projected committee error would be 3ε²(1 − ε) + ε³ = 2.80% — 7.0 expected mis-flags
on the safe side. The blind-spot number is 12.7: **the independence assumption under-resources
review by 1.8×**, and the entire discrepancy is the 4% shared error mass. A report quoting
"three-way redundancy" without ρ or q has quoted a design aspiration, not a measurement.

**Step 5 — scaling the committee.** Going to m = 5 yields 4.21%, m = 9 yields 4.01% (§3.6
table): every additional same-kind judge now buys hundredths of a point. The arithmetic forces
a decision: decorrelate the committee (different failure distributions, *verified*), or accept
a ~4% unaudited mass and state it in the report as a residual-risk line item.

**Step 6 — hand the committee's labels to a stronger student.** The same committee is now a
weak labeler for finetuning a stronger model (§3.2's setup). Majority labels are 94.9% correct
overall but carry the 4% blind-spot mass *as consensus* — indistinguishable from truth by any
vote. The student inherits that mass as training signal: the committee's floor becomes the
label ceiling unless the student's own knowledge resolves it, which is what PGR on a
checkable-ground-truth holdout measures. (The inheritance statement is this course's
operationalization; the registered empirical anchor is [CLM-0030].)

**What this example does and does not establish.** It establishes the arithmetic of correlated
committees on a fixed paired suite with design-determined ground truth at real verified
denominators (250 safe / 200 unsafe, [card](../../datasets/cards/06-xstest.md)). It does *not*
establish any real supervisor's error profile (Step 1 is synthetic); it does not face an
*adaptive* adversary (`chapters/08-ai-control-and-monitoring/` and
`chapters/15-red-teaming-and-adversarial-evaluation/` territory); and design ground truth is
not deployment ground truth — XSTest items are deliberately clearly safe or unsafe
([card](../../datasets/cards/06-xstest.md)), so a 4%-floor conclusion does not transfer to
borderline content.

## 5. Comparison of oversight approaches

| Approach | Mechanism | Load-bearing assumption | Dominant failure mode | Evidence status |
|---|---|---|---|---|
| Outcome supervision (human raters, RLHF-style) | label final outputs; train on the aggregate | raters can judge whole outputs; errors behave as noise | correlated rater errors become training signal; sycophancy to rater tastes | production practice; real ~169k-row corpora exist ([HH-RLHF card](../../datasets/cards/08-hh-rlhf.md)) |
| Weak-to-strong supervision | weak model labels; strong student finetunes; measure the recovered gap | the student's own knowledge resolves supervisor noise | error inheritance when supervisor errors correlate with student priors; elicitation gap | GPT-4-family study: consistent W2S generalization, far from full capability [CLM-0030] |
| Debate | two adversarial agents; a human judges the clash | truth has an argumentative advantage in front of this judge | persuadable judge: rhetoric beats truth; debater collusion | proposal + MNIST judge-analogue: +29.5 / +37.0pp on sparse-pixel classification [CLM-0032] |
| Decomposition | split the task into supervisor-checkable parts; compose verdicts | subtasks are genuinely easier for *this* supervisor | false decomposability; false-rejection compounding 1 − (1 − f)^k | design pattern with real examples (BBQ paired conditions, [card](../../datasets/cards/05-bbq.md)); tradeoff arithmetic §3.4 |
| Process supervision | label each intermediate step | plausible-looking steps track correct steps (faithfulness) | rewarding polished-but-wrong reasoning; label cost scales with k | course operationalization here; canonical comparison assigned as deeper reading (arXiv:2305.20050, not register-anchored) |
| Committee / ensemble oversight | m supervisors vote | errors independent, or ρ measured and reported | correlated-error floor q: majority vote cannot beat the shared blind spot | arithmetic §3.6–§4; the floor is a theorem of the model, the profile must be measured |
| Sandwich evaluation | human + unreliable assistant on tasks above both | the task has a middle band where assisted humans succeed | no sandwich exists for the task; assistant errors mislead rather than scaffold | MMLU + time-limited QuALITY proof-of-concept: assisted humans beat both baselines [CLM-0031] |

Read the last column with Ch. 02's discipline: [CLM-0031] and [CLM-0032] are existence proofs
that the *designs can be studied*, not evidence that any method scales to deployment. The rows
are combinable — decompose, debate the contested pieces, vote the checks, train on the
composite — and the failure modes compound rather than cancel.

## 6. Where this chapter's methods fail

**Debate fails on persuadable judges.** Every benefit routes through the judge; a judge that
rewards confidence, fluency, or fabricated citations inverts the mechanism, and debate becomes
a *training environment for exploiting that judge*. The verified MNIST result used a sparse
classifier as judge-analogue [CLM-0032], not a human under adversarial rhetoric.

**Weak-to-strong fails when errors are informative.** The W2S bonus comes from noise the
student can see through [CLM-0030]. If the supervisor's errors are structured the way the
student's own priors are — shared pretraining, shared misconceptions
([TruthfulQA card](../../datasets/cards/01-truthfulqa.md)) — the student learns the errors as
signal. And the analogy has limits: the label-noise structure of "GPT-2 supervising GPT-4"
differs in kind, not just size, from "human supervising a superhuman system."

**Committees fail on unmeasured correlation.** The floor q is invisible to the naive pipeline:
every observable (accuracy, agreement rates) can look healthy while 4% of items sail through
all judges in consensus. The fix is an agreement-confusion audit against checkable ground
truth — which is why Exercise 5.4 makes it a required design element.

**Decomposition fails on false decomposability and overhead.** If the subtasks are not easier
for the actual supervisor, decomposition adds false rejections (1 − (1 − f)^k: 14.9% of
correct 8-step items at f = 2%) while catching nothing new. Process supervision inherits the
faithfulness problem — rewarding well-formed steps rewards plausible-looking wrongness, the
Goodhart dynamic of
`chapters/03-specification-reward-hacking-and-goal-misgeneralization/` applied to review.

**Checkable ground truth fails by construct substitution.** "Checkable" is not "valid":
SafetyBench's 11,435 bilingual MCQs measure safety *knowledge* in fixed-option format and
cannot support behavioral safety claims
([SafetyBench card](../../datasets/cards/13-safetybench.md)); a TruthfulQA score is not
general honesty ([TruthfulQA card](../../datasets/cards/01-truthfulqa.md)). A bounded
comparison that runs beautifully on MCQ ground truth has measured oversight on MCQs —
Ch. 02's construct-laundering check applies before any headline is written.

**Sandwich evaluation fails when there is no sandwich.** The design needs tasks where human
specialists succeed but unaided humans and current general AI systems fail [CLM-0031]. Where
even specialists cannot verify outcomes, the middle band is empty — the honest output is
"this task is not currently oversight-tractable," not a weaker proxy quietly substituted.

## 7. Readings

**Essential, verified this build** (access levels per the source register):

- *Weak-to-Strong Generalization: Eliciting Strong Capabilities With Weak Supervision* (Burns
  et al., arXiv:2312.09390) — abstract-read [SRC-PAPER-013]. Why: the canonical empirical
  opening of the field. Read skeptically: the weak/strong capability gap is small relative to
  the human/superhuman gap it stands in for.
- *Measuring Progress on Scalable Oversight for Large Language Models* (Bowman et al.,
  arXiv:2211.03540) — abstract-read [SRC-PAPER-014]. Why: the experimental-design paper — the
  "tasks in the middle band" move that converts an impossible problem into a measurable one.
  Read skeptically: the assistant condition is a self-described trivial baseline, and the
  unaided-human floor may be depressed by the time-limited format.
- *AI Safety via Debate* (Irving, Christiano, and Amodei, arXiv:1805.00899) — abstract-read
  [SRC-PAPER-015]. Why: the proposal that frames oversight as an adversarial game judged by
  humans; the PSPACE/NP framing and the MNIST experiment still set the terms of the debate.
  Read skeptically: the complexity claim assumes optimal play, and the judge is a
  sparse-pixel classifier, not a persuadable human.

**Deeper material, clearly separated:**

- Lightman et al., *Let's Verify Step by Step* (arXiv:2305.20050) — abstract fetched in-session
  on 2026-10-21 but deliberately not registered in this unit (no source-register ID was
  allocated to it here); no register-anchored claims are made from it. It is the assigned
  primary source for the process-vs-outcome empirical comparison.
- Re-read Amodei et al., *Concrete Problems in AI Safety* [SRC-PAPER-001, registered with
  Ch. 01]: the 2016 framing of scalable supervision as one of five accident problems, rooted
  in expensive-to-evaluate objectives [CLM-0007] — the ancestor of everything above.


**Note companions:** [27 Debate — the optimality claim and its load-bearing assumption](../../research/notes/27-debate-optimality.md).

## 8. Exercises

**Exercise 5.1 (analysis — correlated-error arithmetic).** A team fields a 5-judge model
committee that majority-votes approvals on a paired refusal suite. Each judge errs against
design ground truth at marginal rate ε = 0.08; a shared blind spot fires on a q = 0.03 mass of
items (all judges err together); otherwise judges err independently at the residual rate.
(a) Derive the residual rate ε′ and the implied pairwise error correlation ρ. (b) Compute the
committee's error rate, and the independent-error committee's rate for contrast. (c) State the
floor as m → ∞, and give the smallest odd m that brings the *independent* version below 2%
and below 0.5%. (d) Can any committee size bring the correlated version below 2%? Justify.
(e) In two sentences: why does adding a sixth judge from the same model family move the number
less than adding one human expert with different failure modes, even though both are "one more
~92%-accurate checker"?

**Exercise 5.2 (analysis — evaluator capability limits and debate).** Start from the verified
MNIST numbers [CLM-0032]: sparse-pixel judge accuracy 59.4% → 88.9% (6 pixels) and 48.2% →
85.2% (4 pixels) with debating agents. (a) Recompute the absolute gains and the error-rate
reductions, showing arithmetic. (b) Name three assumptions the result depends on, and state
for each what breaks if it fails. (c) Design the minimal experiment that tests the
*judge-capability limit* on refusal oversight using XSTest's paired structure (250 safe / 200
unsafe, [card](../../datasets/cards/06-xstest.md)): who debates, who judges, what the ground
truth is, which result would *weaken* the "debate helps judges" hypothesis, and what your
design still cannot test.

**Exercise 5.3 (drill — process vs outcome arithmetic).** A generation pipeline produces
k = 8-step solutions, wrong iff at least one step is wrong; in the operating regime, 70% of
items are fully correct and 30% have exactly one wrong step. Two oversight schemes are
proposed. (A) Outcome check: one final review catches a wrong final answer with probability
0.85, and falsely rejects a correct item with probability 0.01. (B) Process check: each step
is reviewed separately; a wrong step is caught with probability 0.90, and each correct step is
falsely flagged with probability f = 0.02. (a) Compute the per-item probability that a wrong
item is approved under A and under B. (b) Compute the probability a correct item is falsely
rejected under each. (c) Compute each scheme's overall false-approval rate for wrong items and
false-rejection rate for correct items, and state which you would ship and why. (d) Find the
per-step false-flag rate f at which process checking falsely rejects more than 20% of correct
8-step items, and the corresponding threshold for 4-step items. (e) One sentence: what property
of real step-checkers does this arithmetic expose as the binding constraint?

**Exercise 5.4 (design — bounded comparison with checkable ground truth; the chapter
artifact).** Design — do not run — a bounded weak-to-strong comparison, as the precursor of
`projects/p05-weak-to-strong-or-scalable-oversight-analogue/`. Required elements: (i) task
selection from the dataset catalog with checkable ground truth, citing the card's verified
composition numbers and its "cannot support" boundary (candidates: TruthfulQA's 817 questions,
[card](../../datasets/cards/01-truthfulqa.md); BBQ's 58,492 items,
[card](../../datasets/cards/05-bbq.md); SafetyBench's 11,435 MCQs,
[card](../../datasets/cards/13-safetybench.md)); (ii) the weak supervisor and strong learner
roles, with the supervisor's error profile declared or measured by an agreement audit; (iii)
the primary metric (PGR or a declared alternative) with Wilson intervals and a resolution table
at n = 817, 250, and 100; (iv) an error-correlation audit design — how you would estimate ρ
and q between supervisor and learner errors; (v) preregistration elements carried over from
Ch. 02 (claim in context form, weakening observations, split and contamination discipline —
TruthfulQA items circulate in web text, [card](../../datasets/cards/01-truthfulqa.md));
(vi) the small-analogue scope statement: what this comparison cannot tell you about superhuman
supervision. 800–1,200 words.

## 9. Hints and solutions

Hints: 5.1 — the residual rate is not ε − q; condition on the blind spot not firing. 5.2 —
the judge-analogue substitution is the assumption to attack first. 5.3 — false rejection
under B is 1 − (1 − f)^k, not f. 5.4 — if the primary comparison is unresolvable at your
affordable n, the design is not done; it needs a larger n or a weaker claim.

Full worked solutions with assessor rubrics are in [solutions.md](solutions.md). Attempt every
exercise first — the rubrics grade the reasoning trail, including the direction of every
"what would weaken it" statement.

## 10. Completion

**Artifact:** a bounded-comparison design document (Exercise 5.4) for a weak-to-strong or
committee-oversight analogue with checkable ground truth: card-cited instruments with verified
denominators; a supervisor error profile with ρ and q (measured, or declared synthetic); a
PGR-style metric with Wilson intervals and a resolution table; an error-correlation audit
plan; preregistration elements; and a small-analogue scope statement. It is the input
specification for `projects/p05-weak-to-strong-or-scalable-oversight-analogue/`.

**Completion criteria (checkable):**

- [ ] For each of the four method families (weak-to-strong, debate, decomposition, process vs
      outcome), you can state the mechanism, the load-bearing assumption, and a named failure
      mode.
- [ ] You can derive the committee-error formula under the shared blind-spot model, compute it
      for m = 3 and m = 5, and explain why the floor is q and not a function of m.
- [ ] You can compute the false-rejection compounding 1 − (1 − f)^k and say what it implies
      for long reasoning chains.
- [ ] You can produce the Exercise 5.4 design at rubric level, including the resolution table
      and the correlation audit.
- [ ] Every quantitative claim you make about a dataset traces to its card; every claim about
      a paper traces to a claims-register anchor.

**Prev:** [Ch. 02 — Evaluation science and experimental design](../02-evaluation-science-and-experimental-design/README.md)
(the measurement discipline this chapter's ceilings are computed with). **Next:**
`chapters/06-honesty-uncertainty-and-selective-prediction/` (what a supervisor can and cannot
read off a model). **Cross-track:** `chapters/04-preference-learning-and-post-training/` (the
training side of weak human labels); `chapters/08-ai-control-and-monitoring/` (oversight under
adversarial pressure and audit budgets); `chapters/18-reasoning-faithfulness-and-monitorability/`
(whether the supervised process caused the output);
`projects/p05-weak-to-strong-or-scalable-oversight-analogue/` (the bounded experiment this
chapter designs).

**References:** citations resolve to
[research/source-register.yaml](../../research/source-register.yaml) entries SRC-PAPER-001,
SRC-PAPER-013–015, and claim-level records CLM-0030–0033 (plus CLM-0007 from Ch. 01) in
[research/claims-register.yaml](../../research/claims-register.yaml). Dataset facts resolve to
the cited cards in [datasets/README.md](../../datasets/README.md).

**Notation used in this chapter:**

| Symbol | Meaning | Introduced |
|---|---|---|
| σ | the system being supervised (strong model / agent) | §3.1 |
| ω | a supervisor (weak model, rater, judge, committee member) | §3.1 |
| G, gᵢ | ground-truth labels of the checkable task | §3.1 |
| ε | marginal per-item error rate of a supervisor vs G | §3.1 |
| q | shared blind-spot probability (all supervisors err together) | §3.6 |
| ε′ | residual independent error rate; ε = q + (1 − q)ε′ | §3.6 |
| ρ | pairwise error correlation between two supervisors | §3.6 |
| m | committee size (odd; majority vote) | §3.6 |
| k | number of subtasks / steps in a decomposition | §3.4 |
| s | per-step miss rate (a wrong step slips its check) | §3.4 |
| f | per-step false-rejection rate (a correct step is flagged) | §3.4 |
| n | denominator: number of items a rate is computed over (Ch. 02) | §4 |
| PGR | performance gap recovered: (a_W2S − a_ω)/(a_σ\* − a_ω) | §3.2 |

Chapter 05 sets the ceiling conversation for everything that supervises: from here on, "we
check it with X" without X's error rate, correlation structure, and floor is treated as an
error, not a style choice.
