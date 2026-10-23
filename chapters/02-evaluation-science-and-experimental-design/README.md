# Ch. 02 — Evaluation science and experimental design

> The chapter that makes every later chapter honest. Safety claims are
> measurement claims, and measurement claims live or die on design choices
> made *before* the first number is printed: what you measure, on what data,
> split how, scored by whom, with what uncertainty, declared when.

## 1. Research question and failure pathway

**The question this chapter answers:** *how do you produce a number about an
AI system's behavior that a skeptical expert should believe — and know
exactly how far that number reaches?*

**The failure pathway it prevents** (extending Ch. 01's decomposition):

```text
vague construct ──► convenient dataset ──► leakage-friendly split ──►
point estimate, no interval ──► post-hoc metric choice ──►
"safety score" quoted out of context
```

Each arrow is a place where validity leaks out silently. None of them is a
math error; all of them are design errors. This chapter installs the five
gates — construct, provenance, splits, uncertainty, preregistration — that
the failure has to pass through in the opposite direction.

Why this comes *second*, before any alignment or security content: every
later chapter ends in an evaluation. If your evaluation discipline is weak,
you cannot tell whether your reward model is better (Ch. 04), your injection
defense works (Ch. 13–15), or your interpretability claim is causal
(Ch. 09–11). You will produce conclusions indistinguishable from wishes.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites:** Ch. 01 (claims, evidence kinds, uncertainty taxonomy);
diagnostic task B (experiment hygiene); refresher R3.

**Outcomes.** After this chapter you can:

1. Define what a benchmark number measures as a *construct*, and name the
   gap between construct and score.
2. Run the five provenance questions on any dataset and act on the answers.
3. Choose split discipline (grouped / temporal / holdout) from the data's
   dependence structure, not from habit.
4. Explain contamination and adaptive overfitting, and design around them.
5. Compute and interpret Wilson intervals for rate metrics; distinguish
   statistical significance from effect size; state power limits.
6. Write a preregistered evaluation plan — the chapter's artifact.

**Scope exclusions** (what this chapter deliberately does *not* do): it does
not teach benchmark *engineering* at scale (that is P01), model-based judge
validation beyond the framework (Ch. 15 deepens it), or sociotechnical
validity beyond construct scope (Ch. 21). It does not certify any model as
"safe" — a passing evaluation is evidence about a construct in a context,
never a certificate (Ch. 01's rule; Ch. 22 formalizes it into safety cases).

## 3. Core explanation

### 3.1 Evaluation as measurement: construct validity first

A **construct** is the thing you intend to measure — "toxicity", "refusal
quality", "truthfulness". A **score** is what your instrument actually
returns. **Construct validity** is the disciplined gap-statement between
them: what the score is evidence *for*, and what it is silent on.

The course's catalog exists to make this concrete. Three worked examples,
all from verified cards:

- **Refusal quality.** XSTest's construct is *exaggerated safety*: 250 safe
  prompts across ten superficial-similarity types, with 200 unsafe prompts
  as contrasts [cards/06; SRC-PAPER-003]. A "refusal rate on XSTest" score
  is evidence about a *calibration corner* — how often the model refuses
  clearly-safe requests. It is silent on toxicity, bias, and borderline
  judgment. An aggregate "safety score" built from it would be construct
  laundering.
- **Truthfulness.** TruthfulQA's construct is *not repeating common human
  falsehoods* — 817 adversarial questions in categories like Misconceptions
  and Superstitions [cards/01; SRC-DATASET-001]. It is not general honesty,
  not calibration, and not long-horizon consistency.
- **Toxicity.** RealToxicityPrompts ships machine scores across eight
  subcategories — threat, insult, severe_toxicity, toxicity, profanity,
  sexually_explicit, identity_attack, flirtation [cards/03;
  SRC-DATASET-003]. Collapsing them into one "toxicity" number hides
  construct drift: identity_attack and insult are different hazards with
  different thresholds.

**The instrument is part of the construct.** If labels are machine scores,
your construct is "what that classifier, at that version, calls toxic".
That is a real and usable construct — but it must be *named as such*, and
the classifier version recorded, or cross-paper numbers are noise.

**Construct-first workflow** (the discipline this chapter drills):

1. Write the claim you want to make in context form (Ch. 01's σ, κ, b, τ).
2. Name the construct the claim needs.
3. Name the score you will actually compute.
4. Write the gap sentence: "score S is evidence for construct C except
   <known differences>".
5. Only then pick datasets and metrics.

### 3.2 Dataset provenance: the five questions

Before any dataset touches an evaluation, it passes the five provenance
questions. The dataset catalog ([datasets/](../../datasets/README.md)) is
the course's worked answers for 13 real datasets; the questions themselves:

1. **Who made it, for what stated purpose?** (Hosting organization is not
   authorship: BOLD is hosted under an `AmazonScience` Hugging Face
   organization while the paper is by other researchers — the card records
   the distinction rather than assuming [cards/02].)
2. **How was it built** — authored, sampled, machine-generated,
   machine-annotated, or mixed? BBQ's items are template-authored against
   attested stereotypes with a paired ambiguous/disambiguated design
   [cards/05]; ToxiGen's statements are machine-generated with a
   human-annotated subset [cards/04]. Different construction → different
   population → different validity reach.
3. **What license, verified where?** Licenses are dated observations, and
   they change: WildChat's 1M release moved to ODC-BY on 2024-06-26 with
   retroactive effect [cards/12; SRC-DATASET-012]; ToxiGen's page displayed
   no license at inspection time [cards/04]; BeaverTails is
   **CC BY-NC 4.0 — non-commercial** [cards/07]. An evaluation that
   violates a data license is not just illegal; it is *irreproducible by
   compliant teams*, which breaks the evidence chain.
4. **What revision did you load?** Row counts are living properties —
   AdvBench's canonical CSV has 520 behavior rows (521 lines including
   header, verified at the file view) while a mirror card describes the
   paper's 500-behavior framing [cards/09; SRC-DATASET-009]. Neither number
   is "wrong"; an evaluation must state which artifact it used. Pin the
   revision (commit hash or HF revision) in every result.
5. **What does it claim NOT to cover?** Every card in this course ends in
   the "cannot support" section because that section is where validity
   boundaries live. A dataset without a stated negative scope is a dataset
   you will misuse.

### 3.3 Splits that respect dependence

The default random split assumes exchangeable, independent items. Safety
data violates this in three recurring ways:

- **Grouped dependence.** Multiple items from one source/session/template
  share latent features. If they straddle train and test, leakage is
  structural. ToxiGen's machine-generated statements are paraphrase-prone
  by construction — near-duplicate checks across splits are mandatory
  before any classifier claim on it [cards/04].
- **Temporal dependence.** Real traffic is a time series. Split WildChat
  randomly and you evaluate on the past-predicting-the-past; split
  temporally and you measure what you actually deploy against — survival
  under drift [cards/12].
- **Scale/configuration confusion.** BeaverTails ships four configurations
  (two scales × train/test) [cards/07]. A number that does not name its
  configuration is uninterpretable: the 30k-scale test set (~3.02k rows)
  and the 330k-scale test set (~33.4k rows) give different resolution for
  the same true rate.

**Grouped split rule:** the *unit of independence* — user, session,
template, conversation — defines the split. If you cannot name the unit,
your error bars are decorative.

### 3.4 Contamination and adaptive overfitting

**Contamination**: evaluation items leaking into training corpora. The
classic safety example is TruthfulQA: 817 questions whose style and content
circulate widely in web text [cards/01]. A model whose training window
postdates the benchmark's release may have memorized question-answer
structure rather than learned the construct. Discipline: report the model's
knowledge cutoff against the benchmark's release date; treat suspiciously
perfect scores on old benchmarks as a *contamination signal to investigate*,
not as a victory.

**Adaptive overfitting** is contamination's active sibling: the field
iterating against a fixed test set until the benchmark measures
benchmark-specific skill. HarmBench's whole reason to exist, per its
abstract, is that attack/defense comparisons lacked a standardized
framework — comparing 18 red-teaming methods and 33 targets under shared
protocol [cards/11; SRC-PAPER-005]. Standardization helps comparability but
does *not* remove adaptivity; it concentrates it. The design answers are:

1. **Hold out data you never touch** until the final report (P07's
   discipline: report untouched-remainder results separately from anything
   the defense was tuned against).
2. **Report both sides of the ledger.** JailbreakBench ships 100 harmful
   *and* 100 benign behaviors [cards/10; SRC-DATASET-010]; XSTest pairs
   250 safe with 200 unsafe [cards/06]. An attack-success number without
   its false-refusal complement is half a confusion matrix.
3. **Refresh or perturb constructs** rather than items: rephrase, recontext-
   ualize, and check that the score moves for the claimed reason
   (manipulation checks).

### 3.5 Statistical power, cluster-aware intervals, effect sizes

Rate metrics (refusal rates, attack success rates, disparity gaps) need
intervals that behave near 0 and 1. Use the **Wilson interval**:

```text
           p-hat + z^2/2n              z * sqrt(p-hat(1-p-hat)/n + z^2/4n^2)
center  =  ---------------    half-width  =  --------------------------------
           1 + z^2/n                        1 + z^2/n
```

where p-hat is the observed rate, n the denominator, z = 1.96 for 95%.
Four worked numbers from *verified catalog sizes* (sizes from the cited
cards; arithmetic shown in the solutions):

| Scenario | p-hat | n | Wilson 95% | Lesson |
|---|---|---|---|---|
| XSTest safe-prompt compliance | 0.92 | 250 | **[88.0%, 94.8%]** | a 250-item suite resolves compliance only to about +/-3.5pp — small-n is intrinsic, so report the interval, not "92%" |
| Perfect attack defense | 1.00 | 100 | **[96.3%, 100%]** | the naive (Wald) interval here is degenerate — [100%, 100%] — an obviously false claim of zero uncertainty; Wilson stays honest |
| Attack success on AdvBench's 520 behaviors | 5/520 (~0.96%) | 520 | **[0.4%, 2.2%]** | five successes cannot distinguish "1% ASR" from ">2% ASR" — the point estimate understates the plausible rate by more than 2x |
| BOLD religious-domain sub-group rate | 0.50 | ~91 (639 prompts / 7 sub-groups) | **[39.9%, 60.1%]** | +/-10.1pp: within-domain sub-group disparities smaller than ~15pp are **unresolvable** on BOLD's religion domain [cards/02] |

Two consequences people resist:

- **Power is a design input, not a post-hoc apology.** If your decision
  needs to resolve a 3-point difference, compute the required n *before*
  running (a ~1,000-item denominator at mid-range p-hat). If you cannot
  afford n, say so in the report and weaken the claim — that is an honest
  result.
- **Significance is not size.** With 58,492 items (BBQ's verified mirror
  count [cards/05]), differences of a fraction of a point can be
  "significant" and behaviorally meaningless. Report effect sizes (rate
  differences, ratio-of-odds) next to every significance statement, and let
  the claim's threshold tau (Ch. 01) — not the p-value — decide what
  matters.

**Cluster-aware intervals.** When items share a unit of dependence
(3.3), the effective n is the number of *units*, not items. A 5,000-item
evaluation built from 40 sessions has at most 40 independent observations
of session-level behavior; intervals must widen accordingly. This is the
single most common silently-invalid number in agent evaluation (Ch. 14).

### 3.6 Repeated trials, variance decomposition, preregistration

**Repeated trials.** Generative evaluations inject stochasticity at two
layers: sampling temperature and prompt/format variation. A single-pass
score conflates model propensity with decode noise. Discipline: fix and
report seeds/temperature; for refusal-style evaluations, repeat over
prompt paraphrases and report the *spread across paraphrase sets* — a
defense whose ASR doubles under paraphrase is paraphrase-fitting, not
defending (the adaptive-attack lesson from 3.4, measured).

**Variance decomposition.** In a report: total variance = between-format +
between-prompt + decode noise. Even qualitative attribution ("most of the
movement is format sensitivity") beats silence, and prevents the classic
error of explaining decode noise with mechanism stories.

**Preregistration** closes the chapter's loop with Ch. 01: a safety claim
stated *before* data, with its construct, denominators, split discipline,
intervals, analysis choices, and weakening observations fixed in advance,
is a hypothesis. The same claim assembled after seeing the numbers is a
narrative. The artifact below is a preregistered evaluation plan; Exercise
1.2's output is its draft, and every project (P01-P10) starts from one.

## 4. Worked example: evaluating a refusal layer, end to end

**The system:** an assistant with a new refusal layer ("guard") that
should refuse genuinely harmful requests and comply with clearly-safe
ones. **Your job:** produce one number-set a reviewer can trust.

**Step 0 — the claim, in context form.** In deployment context kappa
(customer-support assistant, English chat), the guard's harmful-request
refusal rate is at least 95% and its clearly-safe-prompt false-refusal
rate is at most 5%. Everything downstream is chosen to make *this* claim
measurable.

**Step 1 — constructs and scores.** Two constructs: (a) *harmful-request
refusal* — scored as refusal-classified responses to a fixed harmful
behavior set; (b) *clearly-safe compliance* — scored as compliant responses
to safe prompts. Gap sentences are explicit: refusal is scored by a
string-classifier (a proxy — the classifier's false "refusal" labels are
part of the construct); the behavior sets are research-curated lists
(AdvBench-style), not a threat census [cards/09].

**Step 2 — instruments, from the catalog.** Attack side: a fixed
behavior set at the AdvBench scale (520 behaviors, revision pinned
[cards/09]) — or JailbreakBench's 100 harmful behaviors for
standardized comparability [cards/10]. Benign side: XSTest's 250 safe
prompts [cards/06] or JBB's 100 benign split [cards/10]. Both sides of the
ledger from the start — the design *cannot* produce an attack-only number.

**Step 3 — split discipline.** No training happens, so splits matter at
two seams: (a) paraphrase generation for repeats — paraphrase sets are the
grouping unit; (b) any tuning of the guard (thresholds, keyword lists) —
tuned-on behaviors are reported separately from untouched ones, forever.

**Step 4 — the numbers with intervals.** First full run:
- false-refusal on XSTest safe prompts: 10/250 = 4.0% → Wilson 95%
  **[2.2%, 7.2%]** (center 0.0470, half-width 0.0251; arithmetic in the
  solutions). Claim target "at most 5%": **the interval straddles the
  threshold — this run does not yet support the claim.** Either gather
  more evidence (more instruments, more runs) or weaken the claim. That
  conclusion *is* the correct output.
- attack refusal on the 520-behavior set: 494/520 = 95.0% → Wilson 95%
  **[92.8%, 96.6%]** (center 0.9467, half-width 0.0190). Claim target "at
  least 95%": again straddling — the lower bound sits below target.
  Honest report: "target not yet demonstrated at 95% confidence".

**Step 5 — preregistration record.** All of the above (constructs, gap
sentences, instruments with revisions, split rules, interval method,
decision thresholds, weakening observations: paraphrase-sensitivity run,
scorer-false-positive audit) written and timestamped *before* the first
full run — that document is the chapter's artifact.

**What this model does not cover:** severity heterogeneity across the
behavior list (all behaviors weigh equally); non-English traffic; attacks
not in the fixed list (coverage boundary); the guard's latency cost; the
complement — *appropriate* refusal on genuinely borderline prompts
(XSTest deliberately excludes the middle; see its card's negative scope).

## 5. Comparison of approaches to evaluation design

| Approach | What it optimizes | Failure mode | When it is right |
|---|---|---|---|
| Ad-hoc prompting ("we tried 20 prompts") | speed | anecdote dressed as rate; zero denominators | exploratory triage only, never reported as evidence |
| Fixed public benchmark, score quoted | comparability | construct laundering; contamination; adaptivity over time | coarse cross-model comparison, with cutoff dates stated |
| Standardized framework (XSTest-style paired suites; JBB/HarmBench protocols) | shared instruments and ledgers | standardization is not validity; still needs construct statement | the default backbone for course projects |
| Preregistered custom evaluation (this chapter) | claim validity | slower; smaller n; requires discipline | any load-bearing claim (deployments, papers, capstones) |
| Continuous deployment monitoring | reality | drift alerts are not experiments; observability is not explanation | complements, never replaces, designed evaluation |

The rows are cumulative, not exclusive: production teams run rows 2-5
together. The course's projects train exactly that stack: P01 builds row 3's
harness; P07/P09 add row 4's discipline; Ch. 17/22 connect to row 5.

## 6. Counterexample: where this chapter's method fails

**Precise measurement of the wrong thing.** Preregistration fixes analysis
flexibility, not construct misalignment. A perfectly powered, cleanly
split, interval-corrected evaluation of "refusal on 520 curated behaviors"
is still silent on the attacks that matter to your deployment if those
differ from the list. Goodhart operates upstream of statistics: when the
construct is wrong, rigor manufactures confidence, not validity.

**Interval assumptions violated quietly.** Wilson intervals assume
independent Bernoulli trials. Clustered data (3.3) breaks independence; the
interval is then anti-conservative in exactly the direction that flatters
your result. The fix (unit-level aggregation) is known; the *failure* is
that nothing in the output looks wrong — the number is presented with an
interval, so it *feels* rigorous while being invalid.

**Overpowering.** At BBQ's scale (58,492 items), tests detect differences
no user would notice. Statistical significance becomes noise mining unless
tau (the decision threshold) leads the analysis. The method fails by
succeeding too easily.

**Preregistration theater.** A plan registered but vague ("we will measure
safety") buys none of the discipline; the specification must be
operational enough that another team could grade compliance. And a
preregistered plan written *after* exploratory analysis is laundering with
extra steps — which is why the artifact's timestamp and the raw-run logs
are part of the evidence (P01's runner emits them automatically).

## 7. Readings

**Verified in this build** (access levels per the source register):

- XSTest paper — abstract-read; the paired safe/unsafe design this chapter's
  ledger logic is built on [SRC-PAPER-003; cards/06].
- Universal and Transferable Adversarial Attacks (GCG/AdvBench) —
  abstract-read; the target-set standardization problem and disclosure
  ethics [SRC-PAPER-004; cards/09].
- HarmBench — abstract-read; the standardization rationale (18 methods /
  33 targets under shared protocol) [SRC-PAPER-005; cards/11].
- International AI Safety Report 2026 — page-inspected (landing); current
  field-level calibration [SRC-REPORT-001].
- Dataset cards 01-13 — page-inspected provenance for every composition
  number used above [datasets/README.md](../../datasets/README.md).
- Owner's reference article — full-text-read; course framing [SRC-ARTICLE-001].

**Verified in a later round** (closes this chapter's 2026-10-21 pending markers):

- WILDS, arXiv:2012.07421 — abstract-read, verified 2026-10-22 with chapter 17
  [SRC-PAPER-067; CLM-0090]: the curated benchmark of 10 datasets with
  naturally arising distribution shifts; standard training yields lower
  out-of-distribution than in-distribution performance, with the gap
  persisting under existing methods.
- TruthfulQA paper, arXiv:2109.07958 — abstract-read, verified 2026-10-23
  [SRC-PAPER-073; CLM-0115]: 817 questions across 38 categories; best tested
  model truthful on 58% versus human 94%; largest models generally least
  truthful on the 2021 model set (dated evidence, priced in chapter 6). The
  chapter's composition facts remain card-anchored
  [cards/01](../../datasets/cards/01-truthfulqa.md).

## 8. Exercises

**Exercise 1.1 — construct audit.** A vendor reports "our model is 96%
safe on the industry-standard benchmark suite." Produce: (a) three
distinct constructs "safe" could mean here; (b) for each, one instrument
from the dataset catalog that would measure it, with its verified
composition numbers and its card's "cannot support" boundary; (c) the
single question you would ask the vendor first, and why that question
beats the other two you considered.

**Exercise 1.2 — preregistered evaluation plan (the chapter artifact).**
Write a complete plan for evaluating the guard in section 4 for a
*different* deployment context you choose (e.g., a coding assistant with
shell access). Minimum sections: claim in context form; constructs and gap
sentences; instruments with catalog identifiers and pinned revisions;
split/grouping discipline; interval method and decision thresholds;
repeated-trial design; weakening observations (pre-stated); scope
exclusions. 700-1,200 words.

**Exercise 1.3 — interval drill on verified numbers.** Compute Wilson 95%
intervals, showing the intermediate center and half-width, for:
(a) 12 refusals on XSTest's 200 unsafe prompts; (b) 0 attack successes on
JailbreakBench's 100 harmful behaviors; (c) a 30.0% refusal rate on
BOLD's political-ideology domain (1,984 prompts, 12 sub-groups — first
state the right denominator and grouping); (d) state for each: does the
interval support the claim "rate is at most 5%", "rate is 0%", "rate is
between 28% and 32%" respectively? (e) recompute (b) with the naive Wald
interval and explain in two sentences what goes wrong.

**Exercise 1.4 — contamination investigation design.** TruthfulQA has 817
questions publicly visible since 2021 [cards/01]. Design (do not execute) a
study deciding whether a given model's 0.92 average score reflects the
truthfulness construct or memorization: manipulation checks, timing
evidence, paraphrase arms, and what result would *weaken* the memorization
hypothesis. State the study's own validity limits.

**Exercise 1.5 — split repair.** For each of WildChat [cards/12],
BeaverTails [cards/07], and ToxiGen [cards/04]: name the dependence
structure, the split discipline you would enforce, the leakage risk your
discipline still does not eliminate, and one report sentence that would
make the remaining risk visible to a reader.

## 9. Hints and solutions

Full worked solutions with assessor rubrics are in
[solutions.md](solutions.md). Attempt every exercise first — the rubrics
grade reasoning transparency, not just final numbers.

## 10. Completion

You have completed this chapter when you can:

- [ ] Take any benchmark number in the wild and produce its construct, its
      instrument's composition facts (with provenance), and its interval.
- [ ] State, for a proposed evaluation, the grouping unit and why random
      splits fail it.
- [ ] Compute Wilson intervals by hand for rate metrics and interpret
      threshold-straddling honestly.
- [ ] Produce the preregistered plan (Exercise 1.2) at rubric level —
      the artifact that P01 operationalizes as a runner config.

Chapter 02 gates every later chapter: from here on, "we measured X"
without construct, provenance, denominators, and intervals is treated as
an error, not a style choice.
