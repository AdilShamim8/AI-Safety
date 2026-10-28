# Ch. 10 — Sparse features, circuits, and interpretability evaluation

**Chapter nav:** [← Ch. 09](../09-mechanistic-interpretability-foundations/README.md) · [course map](../../SYLLABUS.md) · [Ch. 11 →](../11-behavioral-steering-and-representation-interventions/README.md)

> The chapter that keeps interpretability evidence honest. "We found the
> deception feature" is a claim about *why a model computes what it computes*,
> and it is among the easiest impressive-sounding claims in AI to produce
> without evidence. This chapter separates a decomposition you can intervene
> on from a dashboard you can screenshot.

## 1. Research question and failure pathway

**The question this chapter answers:** *when someone shows you a sparse
feature, a circuit diagram, or a beautiful activation visualization, what
evidence would make the accompanying mechanistic claim believable — and what
evidence do these demonstrations usually actually provide?*

**The failure pathway it prevents:**

```text
polysemantic activations ──► sparse decomposition looks interpretable ──►
feature dashboard impresses (plausibility) ──► one steering demo on 5 prompts ──►
"the model's deception feature" quoted in a safety argument ──►
monitoring or ablation shipped on the strength of a picture
```

Each arrow leaks evidentiary rigor silently. The first two are genuine
progress — sparse autoencoders (SAEs) really do extract directions markedly
more interpretable than neurons [CLM-0051; CLM-0052]. The last three are
where safety-relevant overclaiming happens: a compelling visualization is
*plausibility* evidence, not *faithfulness* evidence, and the two must be
evaluated explicitly and independently [CLM-0055]. A team that deploys a
"deception monitor" on the strength of a dashboard has skipped this chapter's
core step — interventional evaluation with controls at stated denominators.
For the interpretability track this chapter is what
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) is for
the course: the construct, denominator, interval, and preregistration habits
applied unchanged to a new audited object — internal computation.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.**
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(construct validity, paired ledgers, Wilson intervals, preregistration);
`chapters/09-mechanistic-interpretability-foundations/` (residual streams,
activation patching with baselines and controls — the intervention toolkit
this chapter evaluates claims *with*); diagnostic task B
([diagnostic](../../prerequisites/diagnostic.md)); refresher R3
([targeted refreshers](../../prerequisites/targeted-refreshers.md)).

**Outcomes.** After this chapter you can:

1. Explain superposition and polysemanticity, and why dictionary learning
   with sparse autoencoders is the field's leading response to them.
2. Distinguish SAE *reconstruction* quality from SAE *usefulness*, and state
   why low reconstruction error is not evidence that a decomposition is
   causally meaningful.
3. Explain feature splitting and feature absorption, and their consequence:
   feature identity is dictionary-relative, so "feature #3412 means X" is a
   claim about a (dictionary, model) pair, never about the model alone.
4. Evaluate the faithfulness and completeness of a circuit or feature claim
   with necessity/sufficiency tests, mediation fractions, controls, and
   paired statistics at stated denominators.
5. Explain, with the vocabulary to say precisely why, a compelling
   visualization is insufficient evidence for any mechanistic claim.

**Scope exclusions.** Training SAEs in practice (the optional SAE extension
of `projects/p06-causal-interpretability-study/`); steering methodology and
probe baselines (`chapters/11-behavioral-steering-and-representation-interventions/`,
planned); the intervention toolkit itself
(`chapters/09-mechanistic-interpretability-foundations/`); chain-of-thought
faithfulness (`chapters/18-reasoning-faithfulness-and-monitorability/`,
planned). This chapter evaluates *claims about* features and circuits — it
does not certify any model as interpretable or safe; those words are
constructs needing their own Ch. 02 treatment.

## 3. Core explanation

### 3.1 Superposition: more features than dimensions

A **feature** is a direction-like element of the model's internal
representation such that the computation can be usefully described in terms
of its activations. The natural candidate — one neuron, one feature — fails
empirically: many neurons are **polysemantic**, responding to mixtures of
semantically unrelated inputs, which blocks concise human-understandable
descriptions [CLM-0052]. The leading explanation is **superposition**: a
network represents more features than it has neurons by assigning features
to an overcomplete set of directions, with sparsity in the data letting the
model disambiguate which combination produced any activation vector
[CLM-0051]. Superposition remains a hypothesis with strong toy-model and
observational support, not a settled fact — dictionary-learning results are
the best current evidence it buys interpretive power [CLM-0051; CLM-0052].
The response is to search the overcomplete basis directly: **dictionary
learning** decomposes activations x into a sparse combination z of dictionary
vectors, and the SAE implementation extracts directions markedly more
interpretable than neurons across independent groups and scales [CLM-0051;
CLM-0052; CLM-0053].

### 3.2 The SAE setup and notation

Fix an activation site (MLP output or residual-stream position) with
dimension d; a dictionary of size d_SAE ≫ d (the **expansion factor** is
d_SAE/d) encodes and decodes:

```text
z  = ReLU(W_enc x + b_enc)          encoder: d -> d_SAE features
x̂  = W_dec z + b_dec                decoder: d_SAE -> d reconstruction
L  = ‖x − x̂‖²  +  λ‖z‖₁             reconstruction loss + sparsity penalty
```

Feature j has decoder direction W_dec[:, j] and activation a_j(x) = z_j; it
**fires** on x when a_j(x) > ε for a stated threshold ε. Mean **L0** is the
average number of active features per token; the **fraction of variance
unexplained** is FVU = Σ‖x − x̂‖² / Σ‖x − x̄‖² on held-out activations.
Verified anchors: Bricken et al. train SAEs on the MLP activations of a
one-layer transformer with a 512-neuron MLP, using 8 billion activation
samples from 100 billion tokens of The Pile, with dictionaries from 1× (512
features) to 256× (131,072 features) [CLM-0051]; Templeton et al. scale the
recipe to Claude 3 Sonnet with roughly 1M, 4M, and 34M features [CLM-0053].

### 3.3 Reconstruction vs. usefulness: the metric answering the wrong question

FVU is the natural first metric and the wrong load-bearing metric. The
dictionary-learning authors evaluate with more than reconstruction error —
manual inspection, feature density (live vs. dead), toy models with ground
truth, downstream checks — and note explicitly that runs with low
reconstruction error can carry *less* usable information than sparser runs
with higher error, because average L0 and interpretability do not track
reconstruction quality [CLM-0051]. Dead features inflate the dictionary while
representing nothing: in the A/1 autoencoder of Bricken et al., 168 of 4,096
features are dead (active on none of 100 million dataset examples) and 292
more fire on fewer than one in a million — 4.10% and 7.13% of the dictionary,
recomputed exactly in §4 [CLM-0051]. The course's operational distinction: a
decomposition is a **good reconstruction** if FVU is low on held-out
activations; it is **useful** if replacing activations with SAE
reconstructions preserves the behaviors you care about *and* the features
support correct causal predictions under intervention [CLM-0051; CLM-0052;
CLM-0053]. The two come apart in both directions, and §4 measures both —
with a further trap waiting: at 34M features, Templeton et al. still found
features for only about 60% of London boroughs Sonnet demonstrably knows,
with feature presence tracking concept frequency in training data
[CLM-0053]. Incompleteness is the default state of current dictionaries.

### 3.4 Feature splitting and absorption: feature identity is dictionary-relative

**Feature splitting**: as dictionary size grows, one broad feature resolves
into several narrower ones. Verified anchors: features specific to base64
contexts go from 1 to 3 to "many more" as the dictionary grows 512 (A/0) →
4,096 (A/1) → 16,384 (A/2) [CLM-0051]; in Sonnet, a "San Francisco" feature
in the 1M dictionary splits into two features at 4M and eleven at 34M
[CLM-0053]. Splitting is progress (finer concepts become addressable) and a
bookkeeping hazard (the thing you called "the" feature does not exist at the
next dictionary size). **Feature absorption** is its nastier cousin: at a
given dictionary size a concept's activation can be carried by a more
specific neighboring feature on exactly the inputs where that neighbor
fires, so the general feature under-fires on a sub-concept it nominally
covers. Templeton et al. name "illusions from suboptimal dictionary
learning, such as messy feature splitting" and "cases where the downstream
effects of features diverge from what we might expect given their activation
patterns" as failure modes they have not seen evidence of but do not rule
out [CLM-0053]. The consequence either way: a firing pattern measured with
dictionary D is a fact about (D, model); selectivity numbers must name their
dictionary, and an evaluation pipeline must check whether a *different*
feature carries the activation on the inputs the main feature misses. §4
does this and finds exactly that.

### 3.5 Circuits: faithfulness and completeness as measurable quantities

A **circuit claim** has the form "component set C (features, heads, MLPs) is
how model M computes behavior B on distribution D." The course evaluates
such claims with three operational tests, each yielding a number — this
operationalization is the course's own, built from the intervention logic
the verified sources use [CLM-0052; CLM-0053; CLM-0054]. **Necessity**
(ablate C, replaced by a reference): does B degrade, by how much, relative
to matched controls — the register Cunningham et al. work in when they
pinpoint features causally responsible for counterfactual behavior on the
indirect-object-identification task [CLM-0052]. **Sufficiency** (keep only
C, ablate the complement): does B survive — a circuit necessary but not
sufficient is a participant, not the mechanism. **Completeness** (graded):
the fraction of the total causal effect — the clean-vs-corrupted behavioral
gap that patching C restores — is a number in [0, 1], mirroring the graded
notion of faithfulness Jacovi and Goldberg argue the field should adopt
instead of a binary verdict [CLM-0055].

**Faithfulness**, in their formulation, is the criterion an interpretation
satisfies when it accurately represents the reasoning process behind the
model's prediction; **plausibility** is how convincing the interpretation is
to a human [CLM-0055]. Their guidelines are pointed here: be explicit about
which criterion you evaluate, and do not involve human judgment in
faithfulness evaluation, because human judgment measures plausibility
[CLM-0055]. The benchmark-level analogue is RAVEL, which replaces eyeballing
with tightly controlled, quantitative comparisons of interpretability
methods on entangled attributes, arguing evaluations must go beyond
neuron-level analyses [CLM-0054].

### 3.6 Why a compelling visualization is insufficient evidence

A feature dashboard — top-activating examples, curated transcripts, a UMAP
cluster shaped like a concept — is *plausibility* instrumentation: it shows
the interpretation convinces a human reader [CLM-0055]. Plausibility is
worth measuring and easy to inflate, because the person grading it chose the
examples. Visualization cannot support causal claims for a structural
reason: activation is correlational, and multiple internal arrangements
produce the same activations on the same inputs — the model-assumption gap
Jacovi and Goldberg identify in faithfulness evaluation [CLM-0055]. The
verified literature contains the positive version too: in Scaling
Monosemanticity, interpretations were formed from activation contexts alone,
then tested by intervening in contexts where the feature was *inactive* —
clamping the Golden Gate Bridge feature (34M/31164353) at 10× its maximum
activation made the model start self-identifying as the bridge [CLM-0053].
That is what upgrades a story to evidence: a prediction, fixed in advance,
tested by intervention, with failure live. Even then the authors caution
that the existence of "deception" or "sycophancy" features supports little —
there is a difference between knowing about lies, being capable of lying,
and actually lying [CLM-0053]. The chapter's rule: a visualization earns
attention; only intervention with controls at stated denominators earns
belief; and belief arrives graded — "F mediates about a fifth of the effect"
— not binary.

## 4. Worked example: auditing a claimed "misconception feature," end to end

**Grounding note (explicit).** The dataset catalog holds no interpretability
benchmark, so per this course's grounding rule the worked example's
evaluation-methodology numbers anchor in two real cards: TruthfulQA — 817
questions in a single validation split, adversarial categories including
Misconceptions, multiple-choice and generative regimes
([datasets/cards/01-truthfulqa.md](../../datasets/cards/01-truthfulqa.md)) —
and SafetyBench — 11,435 multiple-choice questions across 7 categories,
Chinese and English
([datasets/cards/13-safetybench.md](../../datasets/cards/13-safetybench.md))
— the unrelated-task control. Every run number below is this course's own
designed illustration, computed exactly by the script in
[solutions.md](solutions.md); none is a result from any paper. The
denominators, 817 and 11,435, are the card-verified facts.

**Step 0 — the claim, stated before any evidence.** System: a small
open-weight model M with an SAE of d_SAE = 16,384 features trained on
residual-stream activations. The claim under audit, in Ch. 01's context form:
"feature F (index 3412), labeled *common human misconceptions* on the team's
dashboard, is the causal channel through which M selects false-but-common
answers on misconception-style multiple-choice questions; ablating F shifts
M toward the true answer." Everything downstream grades *this* sentence,
and is merciless about the difference between "the" and "a."

**Step 1 — reconstruction vs. usefulness.** Held-out FVU is 0.18 at mean
L0 = 24: 82% of activation variance explained. As a *task* number the same
SAE is much weaker. Replacing M's activations with SAE reconstructions on
all 817 multiple-choice questions moves the score from 353/817 (43.2%,
Wilson 95% [39.8%, 46.6%]) to 313/817 (38.3%, [35.0%, 41.7%]) — a net loss
of 40 questions, 4.9pp, with 47 flipping to incorrect against 7 flipping to
correct (exact paired p ≈ 2.3×10⁻⁸; arithmetic in the solutions). The
control that makes this interpretable: Gaussian noise matched to the same
18% unexplained variance costs only 4 net questions (349/817, 42.7%, 0.5pp).
The SAE's error is *structured* — concentrated in exactly the rare,
adversarial contexts the benchmark probes — while isotropic error of the
same magnitude is nearly free. FVU 0.18 was true and nearly useless; the
reconstruction-intervention score is the number that describes the tradeoff.

**Step 2 — selectivity, with the dictionary-relative caveat.** On a
hand-labeled subsample of 200 of the 817 questions (labeling is this
course's operationalization; the card publishes total counts, not
per-category counts), 108 are misconception-labeled. F fires on 87 of 108
(recall 80.6%, Wilson 95% [72.1%, 86.9%]) and on 17 of the 92 others
(precision 87/104 = 83.7%). So far, a plausible dashboard story. The
required next check: *what fires on the 21 misses?* On 10 of them a single
other feature (a health-myths feature from the same dictionary) fires
instead — an absorption-shaped signature: the sub-concept's activation is
carried by a neighbor, so a monitor keyed to F alone under-covers exactly
one sub-family of the construct. Feature identity is dictionary-relative
(§3.4), so the honest sentence is "F covers ~80% of misconception-labeled
items *in this dictionary*, with a known absorbed sub-family."

**Step 3 — the causal test, with controls.** Ablating F (zeroing its
activation) across all 817 questions: 77 flip to correct, 32 flip to
incorrect, 708 unchanged (77 + 32 + 708 = 817 ✓). New score 398/817 = 48.7%;
net +45/817 = +5.5pp; exact McNemar on the 109 discordant questions,
two-sided p = 1.94×10⁻⁵. Two controls bracket the result: a
frequency-matched random feature gives net +3/817 (+0.4pp), two-sided
p = 0.78 — noise; the same F-ablation on SafetyBench's 11,435 questions
gives −23/11,435 = −0.2pp — small but nonzero, and reported because a
monitoring intervention that silently costs accuracy elsewhere is a
deployment fact, not a footnote. One statistical trap, caught: the Wilson
intervals [39.8%, 46.6%] (baseline) and [45.3%, 52.1%] (ablated) *overlap*
while the paired test is decisive — overlapping independent-sample intervals
license no conclusion about paired data; the discordant pairs carry the
information.

**Step 4 — completeness: how much of the effect does F mediate?** Define the
total effect TE per labeled question as the clean-vs-corrupted logit gap,
the corrupted input being the minimal phrasing edit that removes the
misconception reading (the patching protocol of
`chapters/09-mechanistic-interpretability-foundations/`). Patching F from
clean into corrupted restores 22% of mean |TE|; patching the identified
40-feature set restores 71%; 29% stays unexplained. Direction consistency:
on 73 of the 87 questions where F fires, patching moves the logit gap the
way the interpretation predicts (83.9%, Wilson 95% [74.8%, 90.2%]). The
strong claim — F *is* the channel — fails completeness outright: F mediates
about a fifth of the effect. The weak claim — F is *a* channel, partially
necessary, direction-consistent — survives with numbers attached. Those are
different scientific objects, and the difference is the chapter's point.

**Step 5 — what the dashboard was worth.** Everything in the original
presentation — top-activating examples, category labels, the UMAP — is
plausibility evidence: it convinced a human reader ([CLM-0055] supplies the
criterion, not the example). It was worth Step 2 as a sanity check and
nothing as a causal claim; what grades the claim is Steps 1–4 —
reconstruction-intervention cost, dictionary-relative selectivity with the
absorption check, controlled paired ablation, and a graded completeness
fraction, each with denominators and intervals, exactly as Ch. 02 drilled
for behavior. **What this example does not establish:** that F's label is
the right description rather than a correlate (formality, answer-position
priors, and topic stay confounded until a RAVEL-style disentanglement
separates them [CLM-0054]); anything about other dictionaries, models, or
sites; anything about the generative regime (the card lists both regimes
and they rank models differently [datasets/cards/01-truthfulqa.md]); or
that +5.5pp would survive the contamination questions the card itself
raises for models whose training window postdates the benchmark.

## 5. Comparison of approaches to validating feature/circuit claims

| Approach | What it optimizes | Assumptions | Failure mode | Evidence quality | When right |
|---|---|---|---|---|---|
| Manual inspection / feature dashboard | communicability | the interpreter is honest, calibrated; top activations represent the distribution | cherry-picking; plausibility mistaken for faithfulness [CLM-0055] | plausibility only — never causal | hypothesis generation; communicating verified results |
| Automated interpretability (LLM-judged explanations) | labeling scale | the judge's descriptions track the true function | judge bias; label laundering; no intervention [CLM-0052; CLM-0053] | plausibility at scale | triage over 16k+ features feeding human review |
| Steering/clamping demo | intuitive causal force | one context, one feature, one narrative | anecdote: a handful of prompts, no controls or denominators [CLM-0053] | existence proof of *an* effect | sanity check before real evaluation |
| Necessity/sufficiency ablation with controls | causal localization | ablation reference ≈ baseline behavior; controls matched; paired data analyzed paired | off-distribution artifacts; reconstruction side effects (§4 Step 1) | causal, local to D and the reference | the default core of any circuit claim |
| Benchmark interventional evaluation (RAVEL-style) | method comparability | the benchmark's entanglement structure matches your claim's confounds | passes on the benchmark's attributes, untested elsewhere [CLM-0054] | causal + comparative | choosing between methods; designing confound controls |
| Preregistered feature-evaluation protocol (this chapter) | claim validity | the two above — adds discipline, not new tests | slower; smaller n; forces stating the claim in advance | all of the above at stated denominators | any load-bearing safety claim |

The rows are cumulative: a serious team runs manual/automated triage, then
steering sanity checks, then controlled ablations, then benchmark-style
comparisons, and preregisters whichever result will be quoted — Templeton et
al.'s own pipeline (automated interpretation for breadth, clamping for
causal sanity, frequency studies for completeness, named unexcluded failure
modes) is a live example of the stack [CLM-0053].

## 6. Where this chapter's methods fail

**Dictionary-relativity without a fix.** Every number in the worked example
is a fact about one (dictionary, model, site) triple. Splitting and
absorption mean there is no dictionary-free notion of "feature F" to be
faithful *to* [CLM-0051; CLM-0053]. The protocol controls for this by naming
the dictionary and checking absorption — it cannot eliminate it: a monitor
built on F is hostage to the next dictionary release.

**Incomplete dictionaries, quoted as models.** At 34M features, coverage of
known concepts was partial (about 60% of London boroughs) and
frequency-biased [CLM-0053]. A "no deception feature fired" monitoring
result therefore has a silent false-negative channel — absent features
cannot fire. Course rule: absence of activation is evidence only about
concepts the dictionary is known to represent.

**Reconstruction-quality theater.** FVU and L0 are cheap to compute, easy to
improve by growing dictionaries and resampling dead features [CLM-0051], and
only loosely coupled to what safety claims need. A methods paper whose
evaluation stops at reconstruction error plus dashboards has not evaluated
usefulness — Ch. 02's construct gap wearing interpretability clothes.

**The circularity problem.** Faithfulness evaluation should not involve
human judgment, because human judgment measures plausibility [CLM-0055] —
yet the field's automated judges are themselves LLMs whose alignment to
ground truth is assumed, and the community evaluating interpretability
methods largely produces them. RAVEL's tightly controlled comparisons are
the strongest verified corrective [CLM-0054], and they cover one family of
claims (attribute entanglement), not the safety-relevant feature zoo.
Treat "method X beats Y" as self-evaluation until the comparison is
external.

**Paired statistics are still statistics, and interventions are
off-distribution.** McNemar assumes exchangeable discordant pairs under the
null; benchmark questions share templates and authorial style, so the
effective number of independent observations is smaller than 109 and §4's
p-values flatter the result (the Ch. 02 cluster-aware discipline transfers
directly). Ablating a feature with zeros or means also moves activations
into regions the model never saw in training — the measured effect is real
for that intervention but is not automatically the model's "natural"
counterfactual, and Templeton et al. name divergent downstream effects as an
unexcluded failure mode [CLM-0053]. Necessity under one reference value is
not necessity under another; the reference must be reported with the result.

## 7. Readings

**Essential (verified in this build; access levels per the source register):**

- Bricken et al., *Towards Monosemanticity: Decomposing Language Models With
  Dictionary Learning* (transformer-circuits.pub, 2023) — full-text-read.
  Why: the founding SAE result §3.1–3.4 builds on. Read: Problem Setup;
  Sparse Autoencoder Setup; Global Analysis (the metrics discussion and the
  dead-feature counts); Phenomenology (feature splitting). Skeptically:
  evaluation is self-administered rubrics plus automated interpretability,
  and the authors say plainly that some justifications are intuition and
  anecdote rather than rigorous ablations [CLM-0051; SRC-PAPER-030].
- Cunningham et al., *Sparse Autoencoders Find Highly Interpretable Features
  in Language Models* (arXiv:2309.08600) — abstract-read. Why: the
  independent-group confirmation, the automated-interpretability evaluation
  stance, and the causal-counterfactual pinpointing on the IOI task that
  §3.5's necessity test mirrors [CLM-0052; SRC-PAPER-031].
- Templeton et al., *Scaling Monosemanticity: Extracting Interpretable
  Features from Claude 3 Sonnet* (transformer-circuits.pub, 2024) —
  full-text-read. Why: scale changes the stakes — 34M-feature dictionaries,
  safety-relevant features, splitting (San Francisco: 1 → 2 → 11), the
  London-borough completeness gap, and the authors' own named failure modes.
  Read: Feature Survey / Feature Neighborhoods; Feature Completeness;
  Safety-Relevant Features; Discussion. Skeptically: self-evaluation on a
  frontier model by its own manufacturer [CLM-0053; SRC-PAPER-032].
- Jacovi and Goldberg, *Towards Faithfully Interpretable NLP Systems: How
  should we define and evaluate faithfulness?* (arXiv:2004.03685, ACL 2020)
  — full-text-read. Why: the vocabulary (faithfulness vs. plausibility vs.
  readability), the three assumptions underlying faithfulness evaluation,
  and the guideline that human judgment measures plausibility — outcome (c)
  in six pages [CLM-0055; SRC-PAPER-034].

**Optional deeper material, clearly separated:**

- Huang et al., *RAVEL: Evaluating Interpretability Methods on Disentangling
  Language Model Representations* (arXiv:2402.17700, ACL 2024) — abstract-read
  [SRC-PAPER-033]. Turns "did the method disentangle the attributes?" into a
  controlled quantitative comparison; read alongside the exercises, which
  borrow its confound logic [CLM-0054].
- The predecessor *Toy Models of Superposition* is referenced — not verified
  in this session — inside both transformer-circuits articles above; consult
  it through their citations rather than via this course's register.

**Note companions:** [03 Scaling Monosemanticity — features at scale](../../research/notes/03-scaling-monosemanticity.md)[18 Towards Monosemanticity — the foundational dictionary](../../research/notes/18-towards-monosemanticity.md)

## 8. Exercises

**Exercise 10.1 (analysis — the SAE-critique table; the chapter's declared
assessment).** A vendor's technical report presents: (i) a 4M-feature SAE
with FVU 0.12 at L0 18; (ii) a dashboard of "deception feature" 4M/2371917
with 12 top-activating transcripts; (iii) a demo where clamping that feature
makes the model refuse a role-play request in 5 of 5 prompts; (iv) the
sentence "our model's deception is now monitorable in production." Produce
the critique: a table with one row per item and columns for evidence kind
(plausibility / causal anecdote / none), the assumption it silently makes,
the missing control, and what a pass on that control would require —
denominators and all. Then write the three questions you would ask the
vendor first, in order, and justify the order. Finally, state what evidence
would upgrade claim (iv) to defensible, and which parts of that upgrade no
current method delivers [CLM-0053; CLM-0055].

**Exercise 10.2 (design/critical — preregistered feature-evaluation
protocol).** Design — do not run — the evaluation protocol for a claimed
*sycophancy* feature in a small open model, as §4's successor. Required:
(i) the claim in context form with the feature-effect threshold your team
would act on; (ii) instruments from the dataset catalog with pinned
revisions, both ledger sides, and each card's "cannot support" boundary
honored — TruthfulQA's 817-question validation split as the
sycophancy-adjacent behavior instrument and SafetyBench's 11,435 questions
as the unrelated-task capability side-effect control are the natural pair
([datasets/cards/01-truthfulqa.md](../../datasets/cards/01-truthfulqa.md),
[datasets/cards/13-safetybench.md](../../datasets/cards/13-safetybench.md));
(iii) dictionary-relativity controls: version pinned, absorption check on
the misses, splitting check against one larger dictionary; (iv) statistical
plan: paired design, exact McNemar, cluster caveat for shared templates,
Wilson intervals on all rates; (v) preregistration elements from
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) —
conditions fixed in advance, ≥ 3 weakening observations, stopping rules;
(vi) the scope statement: what a negative result does *not* establish.
700–1,200 words.

**Exercise 10.3 (empirical drill — recomputation on designed numbers).**
You audit a claimed "conspiracy-claim credulity" feature; the run produced:
ablation flips 55 questions to correct and 21 to incorrect on the
817-question instrument; the feature fires on 96 of 124 hand-labeled
concept-positive questions; patching the feature alone restores 31% of the
clean-vs-corrupted logit gap while the identified 35-feature circuit
restores 64%; the same ablation moves SafetyBench accuracy by −41/11,435.
Compute exactly: (a) the new score and net effect in pp, the discordant
count, and the two-sided exact McNemar p-value (show the binomial sum or
the code); (b) the Wilson 95% interval for firing recall with center and
half-width; (c) the completeness shortfall and what fraction of the
*circuit's* restored effect the single feature carries; (d) the SafetyBench
side effect in pp and whether it is material at that denominator; (e) two
sentences on why the independent Wilson intervals for before/after scores
can overlap while the paired test is nevertheless decisive.

## 9. Hints and solutions

Hints: 10.1 — grade each item against §3.6's criterion split before judging
the vendor's sentence; item (iv) is a construct claim wearing a measurement's
clothing. 10.2 — the two most common failures are inheriting §4's numbers
without redesigning for the new construct, and treating the unrelated-task
control as a courtesy rather than part of the claim. 10.3 — (b) has n = 124,
not 817; (e)'s answer is §4 Step 3's trap.

Full worked solutions with exact arithmetic and assessor rubrics are in
[solutions.md](solutions.md). Attempt every exercise first — the rubrics
grade the reasoning trail, and an unsupported right answer scores below a
well-argued approximate one.

## 10. Completion

**Artifact:** the SAE-critique analysis (Exercise 10.1): one row per
presented piece of evidence with its evidence kind, hidden assumption,
missing control, and required upgrade — the table format this chapter
applies to every interpretability claim it meets later.

**Completion criteria (checkable):**

- [ ] You can explain superposition, why it blocks neuron-level reading, and
      what dictionary learning proposes to do about it [CLM-0051; CLM-0052].
- [ ] Given an SAE paper's evaluation section, you can name which numbers
      measure reconstruction, which measure usefulness, and which measure
      neither.
- [ ] You can state feature splitting and absorption in one sentence each,
      and why both make feature identity dictionary-relative [CLM-0051;
      CLM-0053].
- [ ] You can design necessity, sufficiency, and graded-completeness tests
      for a circuit claim, with matched controls and paired statistics.
- [ ] You can say precisely why a dashboard is not evidence, using the
      faithfulness/plausibility distinction [CLM-0055], and what it *is*
      for.
- [ ] You can produce Exercise 10.2's protocol at rubric level, including
      the negative-result scope statement.

**Prev (prerequisite):**
[Ch. 02 — Evaluation science and experimental design](../02-evaluation-science-and-experimental-design/README.md)
(the construct/denominator/interval machinery reused throughout, and this
chapter's most direct dependency); `chapters/09-mechanistic-interpretability-foundations/`
(the intervention toolkit — residual streams, activation patching with
baselines and controls — planned; §4 Step 4 states the patching protocol
self-containedly). **Next:** `chapters/11-behavioral-steering-and-representation-interventions/`
(planned; steering as an intervention class with linear-representation
assumptions and capability side effects). **Cross-track:**
[Ch. 07](../07-deception-scheming-and-evaluation-awareness/README.md) (the
evidence ladder a "deception feature" claim must climb);
[Ch. 08](../08-ai-control-and-monitoring/README.md) (where a feature-based
monitor would be deployed, and the audit-budget arithmetic it must survive);
[projects/p01-evaluation-harness/](../../projects/p01-evaluation-harness/README.md)
(the runner that would execute a paired feature evaluation with pinned
revisions).

**References:** claim anchors resolve to
[research/claims-register.yaml](../../research/claims-register.yaml)
records CLM-0051–CLM-0055; source records resolve to
[research/source-register.yaml](../../research/source-register.yaml)
entries SRC-PAPER-030–SRC-PAPER-034. Dataset facts resolve to the cited
cards in [datasets/README.md](../../datasets/README.md): TruthfulQA
composition facts to
[datasets/cards/01-truthfulqa.md](../../datasets/cards/01-truthfulqa.md),
SafetyBench composition facts to
[datasets/cards/13-safetybench.md](../../datasets/cards/13-safetybench.md).
All five sources were fetched and verified in-session on 2026-10-21; the
prompted candidate list contained two vague identifiers (a RAVEL arXiv
number and an "arXiv 2201...." critique), and the actually-fetched records
are those listed above — RAVEL located by title search on the arXiv API
(2402.17700), and the Jacovi–Goldberg faithfulness paper (2004.03685)
chosen in preference to the saliency-interpretation paper that partial ID
resolves to. The worked-example numbers are the course's own designed
illustration, recomputed exactly in [solutions.md](solutions.md).

**Notation used in this chapter:**

| Symbol | Meaning | Introduced |
|---|---|---|
| x, x̂ | activation vector at a site; SAE reconstruction | §3.2 |
| d, d_SAE | site dimension; dictionary size (expansion factor d_SAE/d) | §3.2 |
| W_enc, W_dec | SAE encoder / decoder matrices | §3.2 |
| z, a_j(x) | sparse feature-activation vector; activation of feature j | §3.2 |
| λ | L1 sparsity penalty coefficient | §3.2 |
| L0 | mean number of active features per token | §3.2 |
| FVU | fraction of variance unexplained, Σ‖x−x̂‖²/Σ‖x−x̄‖² | §3.2 |
| F, F′ | the audited feature; the absorbing neighbor feature | §4 |
| MC | multiple-choice score: true option ranked above all false options (course operationalization) | §4 |
| b, c | paired flip counts: correct→incorrect, incorrect→correct | §4 |
| n, n_d | questions; discordant pairs (b + c) | §4 |
| TE | total causal effect: clean-vs-corrupted behavioral gap on a question | §4 |
| ρ_C | completeness: fraction of mean \|TE\| restored by patching component set C | §4 |

Chapter 10 sets the evidence standard for every mechanistic claim the course
meets later: from here on, "we found the feature for X" without
dictionary-version, controls, denominators, and a graded completeness number
is treated as an error, not a style choice.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [lecture-10-mechanistic-interpretability](../../courses/boaz-barak-cs2881/lecture-10-mechanistic-interpretability.md) | Harvard CS 2881 | the SAE program and its stress tests (AxBench, persona vectors) |
| [part-02-05-interpretability](../../courses/google-deepmind-agi-safety/part-02-05-interpretability.md) | DeepMind AGI Safety | the evaluation problem for interpretability itself |

---

**Next:** [Ch. 11 — Behavioral steering and representation interventions →](../11-behavioral-steering-and-representation-interventions/README.md)
