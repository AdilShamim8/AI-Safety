# Chapter 12 — Adversarial ML and robustness

| | |
|---|---|
| **Chapter** | 12 — Adversarial ML and robustness: evasion, poisoning, backdoors, extraction, membership inference; attacker knowledge; adaptive evaluation |
| **Questions** | When is an attack on a learned model *security* rather than accuracy loss? What does each attack family actually exploit, and what exactly does a defense claim have to survive before it means anything? |
| **Hard prerequisites** | [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (construct validity, preregistration, interval-bound gates) |
| | Chapter 03's proxy-discipline vocabulary (the attack surface is where a proxy's blindness becomes an asset) |
| **Core artifact** | Threat-model comparison for a deployed model: the attacker-knowledge grid, each cell's feasibility argument, and a preregistered adaptive audit design with interval arithmetic |
| **Projects** | P07 (injection defense) builds on this chapter's adaptive-evaluation discipline; P10's assurance dossier consumes the threat-model grid |
| **Readings** | Section 7 — ten primary sources, all register-verified at stated access levels |

## 1. Research question and failure pathway

The failure pathway this chapter instruments runs backward: a deployed
model degrades in a way its owner did not predict, because an adversary
spent compute to find inputs the model's training distribution never
priced. The adversary does not need a new exploit class every time —
it needs only the gap between what the model's objective measured and
what the deployment actually depends on. That is why this chapter sits
after specification (Ch. 03) rather than after performance: adversarial
vulnerability is a *specification failure under an opponent*, and every
attack family below is a different way to live in that gap.

The pathway has four stations, and every attack in the chapter maps onto
them:

1. **The model is a proxy** — training minimized a loss on a finite
   sample; the deployment depends on behavior over a distribution no
   one controls.
2. **An adversary optimizes against the proxy** — with whatever
   knowledge it has (section 3.1's grid), spending queries or
   poisoning compute to find the proxy's blind spots.
3. **The blind spot transfers to the deployment** — the found input is
   *in* the deployment distribution even though it was vanishingly rare
   in the training sample (an evasion), or the blind spot was
   *installed* during training (a poisoning or backdoor).
4. **The operator's measurement misses it** — the defense evaluation
   used non-adaptive attacks, unlabeled baselines, or point estimates,
   so the deployment decision was made on a number that measured
   something else. This last station is the one the course can
   actually close, and most of the chapter's discipline lives there.

The through-line to later chapters: prompt injection (Ch. 13) is
evasion against an instruction-following objective; supply-chain
compromise of model artifacts (Ch. 16) is the backdoor story at the
artifact level; monitor evasion (Ch. 08, Ch. 18) is adversarial pressure
against a *classifier of text the adversary generates* — which is why
the adaptive-evaluation rules here (section 3.6) reappear there word
for word.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 02's evaluation discipline (construct
validity, denominators, Wilson intervals, preregistered gates) is used
in every worked number below; Chapter 03's Goodhart vocabulary
(proxy/pressure/gap) is assumed. No deep-learning mathematics beyond
gradients and norms is required: the chapter is about threat modeling
and measurement, not about optimizing attack loss functions.

**Outcomes.** After this chapter you can:

- place any attack you read about into the attacker-knowledge grid
  (knowledge × phase) and say what the cell's feasibility argument
  would have to be (section 3.1);
- explain what each of the five canonical families exploits — evasion,
  poisoning, backdoors, extraction, membership inference — at the level
  of the mechanism, with the founding paper for each (sections 3.2–3.5);
- explain why *most published defenses failed*, with the two canonical
  pieces of evidence: the Carlini–Wagner result against defensive
  distillation and the Croce–Hein audit of 50+ published models
  (section 3.6);
- run a preregistered adaptive audit of a robustness claim — the power
  arithmetic, the stopping rules, and the interval-bound verdict — which
  is the chapter's core artifact (section 4);
- and say precisely what each family's attack does *not* show — the
  scope exclusions below are part of the competence.

**Scope exclusions (stated, not implied).**

- This chapter is about the *evaluation and threat-modeling* discipline
  of adversarial ML, taught with the founding results. It is not an
  attack cookbook: no attack code, no hyperparameters for attacks
  against deployed systems, and no operational guidance for attacking
  anything the reader does not own. The chapters that reach deployment
  realism (Ch. 13–15, Ch. 20) inherit this line.
- Certified robustness (interval-bound propagation, randomized
  smoothing) is named and positioned (section 5) but not derived; its
  guarantees are exactly the kind of claim the audit discipline exists
  to check, and a full treatment belongs to a compute-tier unit.
- LLM-specific jailbreak craft is *not* this chapter — it arrives with
  Ch. 13 and 15. What this chapter provides is the substrate those
  chapters reuse: attacker knowledge, adaptive evaluation, and the
  bitter lesson of defense evaluation.

## 3. Core explanation

### 3.1 The attacker-knowledge grid: knowledge × phase

Every attack claim is a cell in a grid whose axes are **what the
attacker knows** and **when the attacker acts**.

Knowledge, weakest to strongest:

- **Black-box with decisions only** — the attacker observes labels (or
  accept/reject) for inputs it chooses.
- **Black-box with scores** — the attacker observes confidence scores or
  probabilities (the standard ML-API case; Tramèr et al.'s extraction
  attacks live exactly here, and even decision-only APIs proved
  attackable in their setting [SRC-PAPER-043]).
- **Gray-box** — the attacker knows the architecture and training
  procedure but not the weights (transfer attacks: craft against a
  local substitute, hope the blind spot transfers; Szegedy et al.'s
  original observation that perturbations transfer across networks
  trained on different subsets of a dataset is the founding transfer
  claim [SRC-PAPER-040]).
- **White-box** — gradients and weights fully available (Carlini–Wagner
  [SRC-PAPER-044], Madry et al.'s first-order adversary [SRC-PAPER-045]).

Phase: **training time** (the attacker influences the data or the
learning process — poisoning, backdoors, supply-chain compromise) or
**inference time** (the attacker acts on a frozen model — evasion,
extraction, membership inference).

The grid is not decoration; each cell carries a different *feasibility
argument burden*. A poisoning claim must say how the attacker's samples
entered training; a backdoor claim must say who trained the model
(BadNets' outsourced-training scenario [SRC-PAPER-042]); an extraction
claim must say what the API returns and at what query cost
[SRC-PAPER-043]; a membership-inference claim must say what the
adversary already knows about the candidate record [SRC-PAPER-041]. A
threat model that names neither the knowledge level nor the phase is
not a threat model — it is a mood.

Biggio and Roli's survey is the field's map of this territory: ten
years of adversarial ML from the first poisoning and evasion work
against non-deep classifiers through the deep-learning era, organized
around exactly these threat-model distinctions, with the security
evaluation misconceptions called out as first-class content
[SRC-PAPER-049].

### 3.2 Evasion: imperceptible perturbation and the adversary's optimization

The founding observation (2013): apply a perturbation that is
imperceptible to humans and a deep network misclassifies the image —
and the *same* perturbation transfers to networks trained on different
subsets of the data [SRC-PAPER-040]. Two properties made this a
security problem rather than a curiosity: the attacker only needs to
*find* one such input (an optimization problem), and the found input is
a legitimate member of the deployment distribution (nothing about it is
statistically anomalous to a human observer).

The linear explanation followed in 2014: for high-dimensional
near-linear behavior, small per-coordinate perturbations add up —
which yields the single-step attack (the "fast gradient sign method")
and the first adversarial *training* result: training on these examples
reduced the maxout network's test-set error on adversarial examples
[SRC-PAPER-046]. The conceptual takeaway for this course: adversarial
examples were not an exotic bug but a predictable consequence of the
objective's geometry — the loss surface the training set sampled does
not constrain behavior off-sample, and an adversary is a search
process pointed exactly at the unconstrained region. That is Chapter
03's Goodhart story with the pressure supplied by the attacker instead
of the trainer.

Evasion at inference time against a frozen model is the family every
later chapter reuses. Prompt injection is evasion where the "model" is
the instruction-following composite system and the perturbation is
natural language (no epsilon-ball needed); monitor evasion (Ch. 08) is
evasion against a classifier whose inputs the adversary writes.

### 3.3 Poisoning and backdoors: attacking the training process

Poisoning: the attacker contributes training data chosen so the learned
boundary bends to its advantage — the classic pre-deep-learning form
Biggio and Roli trace to the field's beginnings [SRC-PAPER-049].

Backdoors are the sharp modern form: a trigger pattern installed at
training time that maps trigger-bearing inputs to attacker-chosen
outputs while clean accuracy stays state-of-the-art. The BadNets result
made the supply-chain reading explicit: a US street-sign classifier
that identifies stop signs as speed limits when a particular sticker is
present, with the backdoor persisting even after retraining for another
task, and an average 25% accuracy drop when the trigger is present —
while the backdoored network's clean-task performance gives its owner
no signal that anything is wrong [SRC-PAPER-042]. Three properties make
backdoors the cleanest illustration of the chapter's pathway: the
attack lives in the *data provenance*, not the code; the clean-distribution
evaluation cannot see it (the proxy is healthy exactly where the owner
measures); and the trigger is an input-distribution event the deployed
model will meet whenever the attacker chooses.

The supply-chain generalization — who touched the training data, the
labels, the pretrained weights, the fine-tune — is Chapter 16's
provenance audit, which consumes this section's threat-model grid
directly.

### 3.4 Extraction and membership inference: the model as the secret

**Extraction.** Given a prediction API, an attacker can recover the
model itself — or an equivalent — with query access alone: near-perfect
fidelity extraction of logistic regression, neural networks, and
decision trees, demonstrated against the online services of BigML and
Amazon Machine Learning, including cases where confidence values were
withheld [SRC-PAPER-043]. The mechanism is an inversion of supervised
learning: the attacker *labels* its own queries with the API's outputs
and trains a student on the transcript. Two consequences: model
confidentiality is not a property of model quality, and every
rate-limited query budget is a *defense claim* that deserves the
section 4 audit treatment (how many queries does the claimed fidelity
actually require?).

**Membership inference.** Given black-box access, an attacker can
often tell whether a specific record was in the training set: Shokri
et al. trained inference models to recognize the difference between a
target's predictions on records it trained on versus records it did
not, evaluated against commercial "machine learning as a service"
offerings including Google's and Amazon's, with a hospital-discharge
dataset as the motivating sensitive-membership case [SRC-PAPER-041].
The mechanism is that models leak their training data through
calibration differences — the privacy reading of overfitting. The
measurement discipline this chapter adds: a membership-inference
result is a *classification metric* (accuracy/AUC over member and
non-member candidates, with explicit denominators and baselines), and
"better than chance" claims are exactly the kind that need interval
arithmetic before deployment decisions rest on them.

### 3.5 The defense side: adversarial training and what it claims

Adversarial training — optimize against the worst-case perturbation
found so far during training — is the canonical defense. Madry et al.
formulated the first-order-adversary frame: security against an
attacker equipped with gradients (first-order information) as a
natural, broad guarantee, with training methods that significantly
improve resistance to a wide range of attacks [SRC-PAPER-045]. Two
things to hold onto: the guarantee is explicitly *conditional on the
attacker class* (a first-order adversary is a strong but particular
opponent), and the paper's framing — availability of code and
pretrained models, resistance ranges rather than a single number — is
what honest defense reporting looks like.

The tension the course keeps alive: adversarial training buys
robustness inside the perturbation ball it trained against, at
measured cost elsewhere (the robustness–accuracy tradeoff literature
that grew from this frame), and it says nothing about poisoning,
backdoors, extraction, or membership — each family needs its own
defense story and its own audit.

### 3.6 Why most defense papers failed: the two canonical pieces of evidence

**Evidence one: defensive distillation.** Papernot et al.'s defensive
distillation reported reducing the success rate of then-current
attacks from 95% to 0.5% (as quoted in the Carlini–Wagner abstract
[SRC-PAPER-044]). Carlini and Wagner then introduced three attack
algorithms tailored to three distance metrics that succeeded **with
100% probability on both distilled and undistilled networks**, showed
their attacks never perform worse than previous ones, and introduced a
high-confidence transfer test that breaks distillation across the
board [SRC-PAPER-044]. The defense did not fail because distillation
got weaker; the *evaluation* had failed — the attacks used to certify
0.5% did not adapt to what distillation actually changed.

**Evidence two: the fifty-model audit.** Croce and Hein built a
parameter-free ensemble of complementary attacks and evaluated it
against more than fifty models from recent top ML and computer-vision
venues: in all but one case the ensemble achieved *lower* robust test
accuracy than the papers reported, often by more than 10 percentage
points, identifying several broken defenses [SRC-PAPER-047]. The
published robustness numbers — numbers that passed peer review at top
venues — were systematically inflated by non-adaptive or mis-tuned
evaluation. An entire subfield's measurement was off by double digits
until a standardized adversarial audit existed.

Carlini, Athalye, Papernot, Brendel, Rauber, Tsipras, Goodfellow, and
Madry distilled the methodological response: correctly evaluating
defenses has proven extremely difficult; most proposed defenses are
quickly shown incorrect; the paper reviews accepted best practices and
adds evaluation methods designed to avoid the known pitfalls
[SRC-PAPER-048]. For this course the distillation is one sentence:
**an evaluation that the defense's author did not design to survive an
adaptive attacker is not evidence about security.** That sentence
reappears in Ch. 15 (red teaming) and Ch. 08 (control protocols) with
the same meaning.

### 3.7 The vocabulary check (before the worked example)

- **Threat model** = knowledge axis × phase axis + a feasibility
  argument per cell. Not a vibe.
- **Adaptive evaluation** = the attacker in the evaluation knows the
  defense exists and optimizes against the *deployed* system, not the
  paper's toy surrogate [SRC-PAPER-048].
- **Robust accuracy** = accuracy *under the specified attack and
  perturbation budget* — a number that is meaningless without both
  qualifiers attached.
- **Overfitted defenses** (Croce–Hein's finding) = evaluations that
  certify against the attacks they were tuned to, reported as
  robustness against attacks generally [SRC-PAPER-047].

## 4. Worked example: stress-testing a claimed defense, end to end

The scenario, built from the real defensive-distillation record: a
team deploys a defense and reports a 0.5% attack success rate (the
distillation-era claim form [SRC-PAPER-044]). You are the auditor.
Your job is to *reject or bound* the claim — and to know in advance
what evidence would move you, by how much, and at what cost. Every
number below is computed, with the arithmetic shown in full.

**Step 0 — preregister the audit before touching the model.** The
claim to test: "attack success rate ≤ 0.5% for the attack families the
defense's authors used." Note what is *not* claimed: nothing about
adaptive attackers. The audit's hypotheses:

- H1: under an attacker that adapts to the deployed defense, the
  success rate is materially higher than 0.5% (the Carlini–Wagner
  shape of outcome [SRC-PAPER-044]).
- H0 (the defense's claim): rate ≤ 0.5%.

**Step 1 — the detection arithmetic (how many queries does the audit
need?).** Suppose the true adaptive success rate is high — say the
worst case, 100% (the Carlini–Wagner outcome on their test set
[SRC-PAPER-044]). Under H0 at exactly 0.5%, the probability that the
first adaptive query fails is 0.995. The probability that *n*
consecutive queries all fail is 0.995^n:

| n adaptive queries | P(all fail \| rate=0.5%) | P(all fail \| rate=100%) |
|---|---|---|
| 1 | 0.995 | 0 |
| 10 | 0.951 | 0 |
| 100 | 0.606 | 0 |

One single successful adaptive query is a likelihood-ratio event of
roughly 200:1 against H0's upper edge (1/0.005). Ten successes in ten
attempts: H0 (any rate ≤ 0.5%) is dead — P(10/10 successes | rate
0.5%) = (0.005)^10 ≈ 1e-23. The audit's stopping rule writes itself:
run adaptive queries one at a time; the first success already bounds
the rate away from 0.5% at the 95% level (one success in one trial
gives a Wilson 95% interval of [20.7%, 100%] — the lower bound alone
refutes ≤ 0.5%); stop at ten successes or at n = 500 failures
(0.995^500 ≈ 8.2% — even 500 consecutive failures leave a >8% chance
of consistency with a true 0.5% rate, so a *clean* audit outcome
supports "consistent with the claim," never "proof of the claim").

**Step 2 — the interval-bound verdict when successes arrive.** Suppose
the adaptive attack succeeds on 100 of the first 100 held-out test
inputs (the Carlini–Wagner outcome shape). Wilson 95% on 100/100:
center = (1 + z²/200)/(1 + z²/100) = 0.9815, half-width = 0.0185, so
**[96.3%, 100.0%]** (z = 1.95996, full precision — recomputed with the
course's own metric module). Verdict: the defense's 0.5% claim is
rejected by the interval's *lower* bound — the point estimate needs no
appeal. And the
honest framing: this measures the success rate *of the audit's
attacker*, which is a lower bound on the *best* attacker; a defense
that fails one adaptive attacker fails, and a defense that survives
one has merely not yet failed.

**Step 3 — the Croce–Hein gap in audit terms.** Now the subtler case:
the deployed team reports robust accuracy of 60% on a held-out suite
under their attack. Your standardized audit finds 50% on the same
suite — a 10-point gap, the median shape of Croce–Hein's fifty-model
finding [SRC-PAPER-047]. Is a 50% vs 60% gap on n = 500 paired inputs
distinguishable from evaluation noise? Under a paired design, what
matters is the *discordant* count: inputs your attack breaks that
theirs does not (b), and theirs that yours does not (c). With robust
accuracy differing by 10 points on n = 500, expect b − c ≈ 50
discordant-pair imbalance; even if every concordant pair is noise, an
exact McNemar-style sign test on b = 75, c = 25 (b + c = 100
discordant pairs) rejects "no difference" with p ≈ 2.8e-7 one-sided
(the exact binomial probability of a 75/25-or-worse split under
p = 0.5; two-sided ≈ 5.6e-7). The
audit conclusion writes itself: the reported number is not the
deployed number, and the difference is not noise.

**Step 4 — what the audit does *not* establish.** The audit bounds
*attack success under the audited attacker* on *the audited input
suite*. It says nothing about: other attack families (the audit
attacked evasion; poisoning/backdoors/extraction/membership each need
their own cell of section 3.1's grid), distribution shift between the
suite and deployment, or attackers with more query budget. A robustness
*claim* that silently widens beyond what the audit measured is the
same construct-laundering Chapter 02 diagnosed — the number was
measured for one construct and quoted for a wider one.

**Step 5 — the deliverable.** The core artifact: the attacker-knowledge
grid for this deployment (which cells are feasible, with the argument
for each), the preregistered audit (hypotheses, stopping rule, n, the
attack's adaptivity statement per Carlini et al.'s guidelines
[SRC-PAPER-048]), the interval-bound verdicts, and the explicitly
stated non-claims. That document is the chapter's completion artifact
because it is the minimum a deployment decision can actually consume.

## 5. Comparison of attack families and defense postures

| Family | Phase | Attacker knowledge needed | Exploits | Canonical evidence | What a defense claim must survive |
|---|---|---|---|---|---|
| Evasion | inference | black-box (transfer) to white-box | off-sample geometry of the objective | Szegedy et al. transfer [SRC-PAPER-040]; C&W 100% vs distillation's claimed 0.5% [SRC-PAPER-044] | adaptive attack at the deployment's perturbation budget, interval-bounded |
| Poisoning | training | influence over training data | the learning process as the attack surface | surveyed in Biggio–Roli [SRC-PAPER-049] | provenance-controlled data + attack-specific audit |
| Backdoor | training | training pipeline access (outsourcing, supply chain) | clean-accuracy-blind triggers | BadNets: 25% avg drop under trigger; persists retraining [SRC-PAPER-042] | trigger-search audit + provenance chain (Ch. 16) |
| Extraction | inference | API access (scores or decisions) | queries as labels for a student model | near-perfect fidelity vs BigML/Amazon [SRC-PAPER-043] | query-budget + fidelity-vs-queries curve, audited |
| Membership inference | inference | API access + candidate records | overfitting leakage | Shokri et al. vs commercial MLaaS [SRC-PAPER-041] | member/non-member benchmarks with baselines and intervals |
| (Defense) Adversarial training | — | — | — | first-order-adversary guarantee [SRC-PAPER-045] | standardized audits of the Croce–Hein kind [SRC-PAPER-047] |

The table's last column is the chapter compressed: every family's
defense story ends in an audit that must be *designed to break the
defense* — which is why section 4's arithmetic is the core artifact.

## 6. Where this chapter's methods fail

- **The adaptive-evaluation rule is unfalsifiable in the wrong
  direction.** "Survive an adaptive attacker" has no terminal success
  condition — every clean audit is a *not yet failed*. A defense can
  pass every published attack and still fall to the next one; the
  discipline bounds claims, it does not prove safety. Anyone selling
  "adversarially robust" without naming the attacker class is selling
  a cell of the grid as if it were the whole grid.
- **The grid idealizes the attacker.** Real attackers are constrained
  by budgets, indirection, and goals the grid does not model
  (graffiti artist, fraud economics, state actor). A feasibility
  argument per cell is necessary, not sufficient — the chapter's
  grid prices *possibility*, not *profitability*.
- **Robustness is budget-relative and budget-dependent.** A model
  robust at epsilon = 8/255 is a different claim at epsilon = 16/255;
  a query-limited defense is a different claim at 10x budget. Numbers
  without budgets attached (section 3.7) are how the fifty-model
  overestimation happened [SRC-PAPER-047].
- **The chapter's canonical evidence is vision-era.** The founding
  numbers (perturbation balls, image classifiers) do not transfer
  quantitatively to language inputs, where "perturbation" has no
  epsilon-ball and the deployment distribution is adversary-written
  (Ch. 13's problem). The *discipline* — threat model, adaptive
  audit, interval-bound verdict — transfers exactly; the numbers do
  not, and pretending otherwise is construct laundering.
- **Membership-inference metrics are baseline-sensitive.** "Better
  than chance" depends on what chance means for the specific
  member/non-member base rates; a 55% accuracy claim with a 50%
  baseline and wide intervals (Ch. 02's small-n discipline) is a
  different animal from the same point estimate at n = 100,000.
- **Nothing here is a security guarantee.** The chapter's honest
  output is a *measurement protocol* — the thing that makes the next
  defense claim falsifiable. Claims of robustness beyond the audited
  cell are exactly what the protocol exists to prevent.

## 7. Readings

All ten sources are register-verified at the stated access level
(register IDs; the access levels and per-fact notes are in
[research/source-register.yaml](../../research/source-register.yaml)).
Read in this order.

1. **Biggio & Roli, "Wild Patterns: Ten Years After the Rise of
   Adversarial Machine Learning"** [SRC-PAPER-049] — *first*: the map.
   Threat models, the train/test-time split, the security-evaluation
   misconceptions. Read the abstract and taxonomy sections; the survey
   is the chapter's spine.
2. **Szegedy et al., "Intriguing properties of neural networks"**
   [SRC-PAPER-040] — the founding observation: imperceptible
   perturbation, cross-network transfer. Short; read for how little
   was claimed in 2013 and how well it aged.
3. **Goodfellow, Shlens & Szegedy, "Explaining and Harnessing
   Adversarial Examples"** [SRC-PAPER-046] — the linear explanation,
   the single-step attack, the first adversarial training result.
4. **Carlini & Wagner, "Towards Evaluating the Robustness of Neural
   Networks"** [SRC-PAPER-044] — the distillation-breaking result:
   100% success against a defense reporting 0.5%. Read primarily as a
   *measurement* paper: what did the earlier evaluation miss?
5. **Madry et al., "Towards Deep Learning Models Resistant to
   Adversarial Attacks"** [SRC-PAPER-045] — the defense-side
   formulation: the first-order adversary, and what an honest defense
   claim looks like.
6. **Gu, Dolan-Gavitt & Garg, "BadNets"** [SRC-PAPER-042] — the
   backdoor result and the supply-chain threat model. The 25% trigger
   drop and retraining persistence are the numbers to remember.
7. **Tramèr et al., "Stealing Machine Learning Models via Prediction
   APIs"** [SRC-PAPER-043] — extraction with near-perfect fidelity
   against BigML and Amazon; the queries-as-labels mechanism.
8. **Shokri et al., "Membership Inference Attacks against Machine
   Learning Models"** [SRC-PAPER-041] — the privacy reading of
   overfitting, against commercial MLaaS.
9. **Carlini et al., "On Evaluating Adversarial Robustness"**
   [SRC-PAPER-048] — the evaluation guidelines paper: nine authors
   from both the attack and defense sides agreeing on how to evaluate.
   The chapter's section 3.6 discipline in primary form.
10. **Croce & Hein, "Reliable evaluation of adversarial robustness
    with an ensemble of diverse parameter-free attacks"**
    [SRC-PAPER-047] — the fifty-model audit: all but one model
    overestimated, often by >10 points. The reason standardized
    adversarial evaluation exists.

Assigned-pending (not yet register-verified; never cited as verified):
Papernot et al.'s original defensive-distillation paper (the 95%→0.5%
claim is quoted here *as reported by* Carlini–Wagner's abstract, which
is how it should be cited until the primary is verified); certified
robustness literature (randomized smoothing, interval bounds) for the
compute-tier treatment.

**Note companions:** [35 Obfuscated gradients — attack failure is not defense success](../../research/notes/35-obfuscated-gradients.md)[36 Adversarial examples are features — the non-robust-features thesis](../../research/notes/36-adversarial-features-not-bugs.md) [53 Double descent — scale non-monotonicity, dynamics version](../../research/notes/53-deep-double-descent.md)[54 Randomized smoothing — certification instead of attack-resistance](../../research/notes/54-randomized-smoothing.md)[55 TRADES — the robustness-accuracy trade, decomposed](../../research/notes/55-trades-robustness-accuracy.md) [64 Physical-world adversarial examples — the channel survives](../../research/notes/64-physical-world-adversarial.md)

## 8. Exercises

**Exercise 12.1 (analysis — the grid for a real deployment).** A
company fine-tunes a public pretrained LLM on private customer-support
transcripts and exposes it behind a rate-limited chat API that returns
only text (no token probabilities). Customers' future chats are
retained for retraining. Construct the attacker-knowledge grid for
this deployment: for each of the five families (evasion, poisoning,
backdoor, extraction, membership inference), determine the phase and
the knowledge level available to (a) an outside attacker, (b) a
malicious customer, (c) the pretraining-model provider. For each
non-vacuous cell, write the feasibility argument in two sentences:
what the attacker would need and what the deployment already gives
it. Conclude with the single cell you would audit first and why —
your answer must cite at least three of the chapter's sources for the
mechanisms you rely on.

**Exercise 12.2 (empirical/design — the preregistered audit).** A
vendor claims their deployed classifier withstands "state-of-the-art
attacks with under 1% success" and separately reports "robust accuracy
85%" on a 1,000-image audit suite using their own attack. Design the
preregistered audit that would make both claims falsifiable: (a) the
hypotheses and the stopping rules, including how many adaptive
successes or failures decide each; (b) the sample-size arithmetic for
distinguishing 85% from a Croce–Hein-shaped 75% true robust accuracy
(paired design; state your discordant-pair assumptions and the
resulting exact-test significance); (c) the interval-bound verdict
rules (Wilson-based, per the course's metric discipline); and (d) the
explicit non-claims your audit will publish. Then compute the actual
verdicts for two outcomes: the adaptive attack succeeds 3/3 on the
first three tries; the standardized audit finds 750/1,000 robust
against the vendor's 850/1,000.

## 9. Hints

- For 12.1: start from what the API *returns* (text only — what does
  that make extraction? Tramèr et al.'s decision-only case
  [SRC-PAPER-043] is the reference) and who *touches training*
  (retained chats — what does that make poisoning?). The provider's
  cell is the one people forget: what did the pretraining already
  install (BadNets' supply-chain shape [SRC-PAPER-042])?
- For 12.2: mirror section 4's arithmetic exactly — the 0.995^n table
  for the ≤1% claim (how many failures does a clean audit need before
  "consistent with the claim" is even sayable?), and the McNemar-style
  discordant-pair computation for the robust-accuracy gap with your
  stated assumptions. The Wilson lower bound on 3/3 decides (a) faster
  than you might expect; [43.9%, 100%] already excludes 1%.

## 10. Completion

This chapter is complete when you can:

- [ ] write the attacker-knowledge grid for an arbitrary deployed
      model, with a feasibility argument per cell (not a checklist —
      an argument);
- [ ] state what each of the five families exploits and name the
      canonical evidence (the two BadNets numbers, the C&W
      100%-vs-0.5% result, the Croce–Hein >10-point finding, the
      near-perfect-fidelity extraction result, the commercial-MLaaS
      membership result);
- [ ] explain why most published defenses failed, and say what an
      adaptive evaluation is required to include before a robustness
      number means anything;
- [ ] run the audit arithmetic of section 4 cold: the 0.995^n
      stopping-rule table, the Wilson interval on an all-successes
      audit, and the discordant-pair significance for a
      reported-vs-audited gap;
- [ ] and state the chapter's own limits (grid prices possibility not
      profitability; vision-era numbers do not transfer to language;
      every clean audit is "not yet failed") without prompting.

The next chapter (13 — LLM application security, planned) applies this
discipline where the input distribution is written by the adversary:
injection attacks and trust boundaries.
