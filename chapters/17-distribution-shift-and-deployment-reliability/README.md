# Chapter 17 — Distribution shift and deployment reliability

| | |
|---|---|
| **Chapter** | 17 — Distribution shift and deployment reliability: OOD, worst-group, drift, uncertainty under shift; covariate vs label vs concept change |
| **Questions** | What does your evaluation number promise about a world that keeps moving? When the training distribution and the deployment distribution diverge — across hospitals, regions, months, or populations — which evaluation catches it, which silently misses it, and what does "reliable" even mean for a system whose input distribution is a moving target? |
| **Hard prerequisites** | [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (dependence-aware splits, construct validity); [Chapter 06 — honesty and selective prediction](../06-honesty-uncertainty-and-selective-prediction/README.md) (calibration, abstention) |
| **Core artifact** | Shift-taxonomy analysis: a deployed system's failure modes decomposed into covariate / label / concept / group / temporal shift, each with its detection signal, its evaluation instrument, and its mitigation lever |
| **Projects** | P09 (shift/subgroup reliability) implements this chapter's discipline as code |
| **Readings** | Section 7 — four newly register-verified sources plus re-anchored earlier ones |

## 1. Research question and failure pathway

The i.i.d. promise — "test set like train set, so test accuracy
predicts deployment accuracy" — is the load-bearing assumption of
every number in every model card, and it is the first thing the
world breaks. The failure pathway this chapter instruments:

1. **The benchmark itself is a snapshot.** Rebuilding CIFAR-10 and
   ImageNet test sets by the *original* creation process — no
   adversary, no novel domain, just fresh sampling — drops accuracy
   by 3-15% (CIFAR-10) and 11-14% (ImageNet): the drops come not
   from adaptivity but from slightly *harder* images
   [SRC-PAPER-066]. The i.i.d. promise fails before the
   distribution even shifts on purpose.
2. **Real shifts are structured, not random.** Deployment differs
   across hospitals, camera models, demographics, countries, time
   periods — and on real shift benchmarks, standard training yields
   substantially lower out-of-distribution than in-distribution
   performance, with the gap persisting even under existing
   robustness methods [SRC-PAPER-067].
3. **Averages hide groups.** An overparameterized model can be
   excellent on average and consistently wrong on atypical groups —
   spurious correlations that hold in aggregate fail exactly where
   the model has least data [SRC-PAPER-068].
4. **Uncertainty degrades faster than accuracy.** Under shift, both
   accuracy *and* calibration degrade — the confidence that gated
   your abstention policy (Ch. 06) was calibrated on a distribution
   that no longer holds [SRC-PAPER-069].
5. **Drift is temporal and unbounded.** The world moves after
   deployment; a system validated once is a system whose evaluation
   has an expiry date that nobody printed.

The chapter's reframe: "reliability" for deployed systems is not a
score but a *monitoring claim* — measured per group, per domain, per
time window, with intervals, and with the honest statement of which
shifts are instrumented and which are simply not watched.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Ch. 02's split discipline and interval grammar;
Ch. 06's calibration and risk-coverage machinery.

**Outcomes.** After this chapter you can:

- reproduce the taxonomy — covariate, label, concept, group, and
  temporal shift — with the canonical evidence for each
  [SRC-PAPER-066] [SRC-PAPER-067] [SRC-PAPER-068] [SRC-PAPER-069];
- explain why average accuracy is a dishonest deployment metric for
  any system serving heterogeneous groups, and what worst-group
  measurement requires (pre-declared groups; DRO's regularization
  lesson [SRC-PAPER-068]);
- state what happens to calibrated confidence under shift
  [SRC-PAPER-069] and what that does to Ch. 06's selective-prediction
  guarantees;
- build the shift-taxonomy analysis: per-shift detection signals,
  evaluation instruments, and mitigation levers;
- and design the monitoring loop — drift indicators, re-evaluation
  triggers, and validity windows — that keeps a deployment's numbers
  dated rather than eternal.

**Scope exclusions.** The formal learning-theory of domain
adaptation (bounds, divergences) is named, not derived; causality is
used at the level of Ch. 03's intervention vocabulary; unsupervised
drift-detection method comparisons are surveyed at concept level
only. Continual learning and retraining policy design are scoped to
P09's protocol, not covered here.

## 3. The core explanation

### 3.1 The taxonomy, with its canonical evidence

**Covariate shift** — P(x) changes, P(y|x) does not: new cameras,
new hospitals, new regions. The WILDS catalog gives the canonical
instances (tumor identification across hospitals; wildlife
monitoring across camera traps; poverty mapping across time and
location), with the standing finding that the ID-OOD gap survives
existing methods [SRC-PAPER-067].

**Label shift** — P(y) changes, P(x|y) does not: disease prevalence
changes between seasons; the base rate moves and every
threshold-tuned system inherits the movement (Bayes, collecting its
rent).

**Concept shift** — P(y|x) itself changes: the relation between
features and outcome moves (fraud tactics evolve; the label's
*meaning* drifts). The hardest family: undetectable from inputs
alone; requires outcome monitoring, which deployments often lack.

**Group / subpopulation shift** — the mixture reweights: the average
stays flat while a group collapses. The group-DRO finding: naive
worst-case training fails in the overparameterized regime (training
loss already vanishes everywhere); the *generalization* gap is the
problem, and coupling DRO with stronger-than-typical regularization
yields 10-40 percentage-point worst-group improvements while
holding average accuracy [SRC-PAPER-068].

**Temporal shift (drift)** — the previous four, distributed over
time: the world's default mode.

And the meta-finding that grounds them all: even *fresh i.i.d.
sampling* of the same benchmark construction process drops accuracy
materially [SRC-PAPER-066] — the snapshot problem precedes every
structured shift.

### 3.2 What shift does to calibration — and to abstention

The uncertainty benchmark's result: under dataset shift, accuracy
and calibration degrade together, and methods compared for
uncertainty improvement behave differently under shift than at
distribution [SRC-PAPER-069]. The deployment consequence is the
chapter's sharpest practical point: Ch. 06's selective-prediction
guarantees — risk-coverage curves, threshold policies, the entire
"gate on confidence" architecture — are *conditional on the
calibration being measured on the deployment distribution*. Under
shift, the gate's meter breaks while the gate keeps clicking:
overconfident errors pass as calibrated answers. The two-ledger
discipline from Ch. 15 returns as a *distribution* ledger: report
risk-coverage per domain and per time window, not in aggregate.

### 3.3 The monitoring loop

The reliability program for deployed systems, as four instruments:

1. **Shadow evaluation on held-out domains** — the WILDS pattern
   applied to one's own deployment: pre-declare the domains
   (regions, client types, channels), hold out at the group level
   (Ch. 02's dependence-aware splits), and report per-domain rates
   with intervals [SRC-PAPER-067].
2. **Worst-group tracking** — pre-declared groups, worst-group rate
   as a first-class metric with its own interval and alert
   threshold; the group-DRO lesson available when retraining
   [SRC-PAPER-068].
3. **Calibration surveillance** — per-window ECE and reliability
   tables (Ch. 06/P03 machinery) recomputed as the window rolls;
   a validity window stamped on every published number
   [SRC-PAPER-069].
4. **Drift triggers** — input-distribution indicators (cheap,
   unsupervised) wired to re-evaluation triggers (the expensive,
   supervised instruments) — the design that converts "we were
   accurate once" into "we know when we stopped being accurate."

## 4. Worked example — the Halcyon content classifier

**Deployment.** "Halcyon" classifies user-uploaded content for
policy violations, trained on 2024 data from four regions,
deployed in eleven, with a confidence-based escalation policy
(high-confidence violations auto-actioned; low-confidence routed to
human review — the Ch. 06 gate). Synthetic example; every number
recomputed in the solutions.

**The taxonomy audit.** Per shift class: *covariate* — new upload
sources and devices post-launch; *label* — violation base rates
moved after a policy update (3.1% → 5.4%); *concept* — adversarial
users adapt content to the classifier (concept shift *induced*,
Ch. 12 meeting Ch. 17); *group* — region E entered with a device
mix unlike any training region; *temporal* — all of it, over twelve
months.

**The evaluation that caught it.** Shadow domains held out by
region-and-month: ID accuracy 481/500 = 96.2% [94.1%, 97.6%] vs
OOD accuracy 421/500 = 84.2% [80.7%, 87.1%] — a 12-point snapshot
drop of the Recht kind [SRC-PAPER-066], before any adversarial
adaptation. Worst-group: 61/100 = 61.0% [51.2%, 70.0%] for region E
against an average-group 92/100 = 92.0% [85.0%, 95.9%] — the
average metric never mentions the 31-point gap underneath it
[SRC-PAPER-068's shape].

**The gate breaking silently.** Per-window calibration: at
deployment, ECE 0.042 with the escalation threshold tuned to a 2%
false-escalation budget; at month 12 under drift, ECE 0.187 — the
same threshold now passes overconfident errors: false escalations
run at 37/200 = 18.5% [13.7%, 24.5%] on the month-12 audit sample
[SRC-PAPER-069's mechanism, at fixture scale]. The monitoring
report's headline: the *policy*, not the model, is what the drift
broke — the model's accuracy dropped 4 points; the gate's error
rate grew 9-fold.

**The mitigation ledger.** Retraining with region-E data +
group-DRO-style upweighting: worst-group 61% → 78% (interval
pricing in solutions), average unchanged — with the
regularization caveat carried explicitly (the improvement came with
L2 doubled; the paper's own lesson is that the coupling, not DRO
alone, does the work [SRC-PAPER-068]). The re-dated validity
window: all published numbers now carry a 90-day expiry and a
drift-trigger re-evaluation clause.

## 5. Approach comparison

| Approach | Shift class addressed | Evidence anchor (source, level) | Failure mode |
|---|---|---|---|
| Fresh i.i.d. re-sampling of test sets | none (the baseline pathology) | 3-15% / 11-14% drops without any shift [SRC-PAPER-066, abstract] | snapshot numbers read as eternal |
| Held-out-domain evaluation | covariate, temporal | WILDS: ID-OOD gap persists under existing methods [SRC-PAPER-067, abstract] | domains you did not enumerate are unwatched |
| Group-DRO + regularization | group | 10-40pp worst-group gains with coupling [SRC-PAPER-068, abstract] | groups must be pre-declared; unseen groups unprotected |
| Calibration surveillance + validity windows | all (detection) | uncertainty degrades under shift [SRC-PAPER-069, abstract] | indicators drift *behind* the shift they track |
| Monitoring triggers → re-evaluation | temporal (response) | this course's P09 protocol | trigger thresholds are themselves tuned on old data |
| Domain-adversarial / invariant learning | covariate | named; evidence base treated as assigned-pending | invariance to the wrong partition can erase signal |

## 6. Where the methods fail

- **Unenumerated domains are unwatched domains.** Held-out-domain
  evaluation covers the partition you named; region F's arrival is
  invisible until its failure rate is a incident report.
- **Worst-group metrics need declared groups.** The group taxonomy
  is authored, not discovered — the Ch. 14 authored-policy lesson
  recurring at the data layer.
- **Concept shift evades input-side detection.** When P(y|x) moves,
  input-distribution indicators show nothing; only outcome
  monitoring catches it, and outcome labels are the scarcest
  resource in most deployments.
- **Calibration repair is per-window.** Recalibrating on drifted
  data fit the drift; the Ch. 06 discipline (validation-only fits)
  must now carry a *window* discipline — a map fit on last quarter
  anti-calibrates this quarter.
- **The snapshot problem has no cure, only honesty.** Fresh i.i.d.
  sampling itself drops accuracy materially [SRC-PAPER-066]; the
  response is dating every number, not chasing a timeless one.

## 7. Readings

Register-verified at the stated access levels (per
[research/source-register.yaml](../../research/source-register.yaml)):

1. **Recht et al., "Do ImageNet Classifiers Generalize to
   ImageNet?"** [SRC-PAPER-066] — the fresh-test-set result:
   3-15%/11-14% drops with gains transferring; the snapshot
   pathology measured.
2. **Koh et al., "WILDS: A Benchmark of in-the-Wild Distribution
   Shifts"** [SRC-PAPER-067] — ten real-world shift datasets; the
   ID-OOD gap that survives existing methods.
3. **Sagawa et al., "Distributionally Robust Neural Networks for
   Group Shifts"** [SRC-PAPER-068] — the worst-group failure of
   overparameterized average-accuracy models; DRO + regularization
   with 10-40pp improvements.
4. **Ovadia et al., "Can You Trust Your Model's Uncertainty?"**
   [SRC-PAPER-069] — accuracy and calibration degrading together
   under shift; the benchmark for uncertainty methods under
   distribution change.

Re-anchored from earlier chapters: Ch. 02 (dependence-aware splits,
adaptive overfitting), Ch. 06/P03 (calibration and selective
prediction — whose guarantees this chapter re-conditions), Ch. 12
(induced concept shift: adversaries adapting to the classifier).

Assigned-pending (never cited as verified): domain-adversarial
invariant-learning evidence; unsupervised drift-detection method
comparisons; label-shift correction estimators.

**Note companions:** [39 Lost in the middle — position as a reliability variable](../../research/notes/39-lost-in-the-middle.md) [C11 Situational awareness vs persona drift — the deployment-side drift](../../research/notes/comparison-11-situational-awareness-vs-persona-drift.md) [66 Underspecification — equivalent in training, divergent in deployment](../../research/notes/66-underspecification.md)[70 Scaling laws — the predictability floor](../../research/notes/70-scaling-laws.md)

## 8. Exercises

**Exercise 17.1 (analysis — the taxonomy audit).** A medical
triage assistant is deployed across a hospital network: trained on
2024 data from three urban hospitals, now serving twelve sites
including two rural clinics, with a fall flu season approaching and
a severity-threshold policy gating referrals. (a) Write the
shift-taxonomy analysis: per shift class, the concrete instance in
this deployment, the detection signal, and the evaluation
instrument. (b) The vendor's report cites 96% average accuracy:
write the two-sentence response naming what the average hides, with
the group-DRO finding as evidence [SRC-PAPER-068]. (c) The referral
policy was threshold-tuned at deployment: state what drift does to
it (cite the uncertainty-degradation evidence [SRC-PAPER-069]) and
design the calibration surveillance that keeps the policy honest.
(d) Name the one shift class in this deployment that input-side
monitoring cannot catch, and say why.

**Exercise 17.2 (empirical — pricing the Halcyon numbers).** From
the worked example: ID 481/500; OOD 421/500; worst-group 61/100;
average-group 92/100; false escalations 37/200 at month 12 (2% at
deployment). (a) Compute all five Wilson intervals. (b) The vendor
says "the 4-point accuracy drop is within tolerance": what does the
*gate's* 9-fold error growth say about which metric the tolerance
should be written on? (c) After group-DRO retraining, worst-group
moves to 78/100: compute the interval and state honestly what
improved, what did not, and what the regulariz coupling caveat
means for the retraining recipe [SRC-PAPER-068]. (d) Design the
validity-window statement that the month-12 report must carry: what
is dated, what triggers re-evaluation, and what remains unwatched.

## 9. Hints

- For 17.1: (a) rural clinics = covariate; flu season = label
  (base rate); clinician-adapted presentations = concept; site
  type = group; all over time. (b) The average hides a worst-group
  collapse — overparameterized models fit the aggregate and fail
  atypical groups [SRC-PAPER-068]; demand worst-site rates with
  intervals. (c) Threshold policies inherit calibration; under
  shift ECE degrades [SRC-PAPER-069] — per-window reliability
  tables and a dated validity window. (d) Concept shift — P(y|x)
  moves invisibly to input-side indicators; only outcome labels
  catch it.
- For 17.2: (a) [94.1%, 97.6%]; [80.7%, 87.1%]; [51.2%, 70.0%];
  [85.0%, 95.9%]; [13.7%, 24.5%]. (b) The tolerance metric is the
  *policy error rate*, not model accuracy — the 9-fold growth is
  the deployment fact. (c) 78/100 → [68.9%, 85.0%] — improved and
  resolved from the pre-retraining worst-group interval? compute;
  the caveat: the gain came with the regularization coupling, so
  the recipe is DRO *plus* L2/early-stopping, and the average
  traded nothing only as measured. (d) The statement dates every
  number, names its drift triggers, and admits the unwatched
  (unenumerated sources, induced concept shift).

## 10. Completion

This chapter is complete when you can:

- [ ] reproduce the five-class shift taxonomy with its canonical
      evidence [SRC-PAPER-066] [SRC-PAPER-067] [SRC-PAPER-068]
      [SRC-PAPER-069];
- [ ] explain the snapshot pathology and why fresh i.i.d. sampling
      is not a cure but a measurement [SRC-PAPER-066];
- [ ] argue why average accuracy is dishonest for heterogeneous
      deployments, and what worst-group measurement requires
      [SRC-PAPER-068];
- [ ] state what shift does to calibration and therefore to Ch. 06's
      selective-prediction guarantees [SRC-PAPER-069];
- [ ] build the shift-taxonomy analysis and the monitoring loop —
      detection signals, instruments, triggers, validity windows;
- [ ] and date every number you publish about a deployed system,
      with the unwatched named.

Cross-links: the split discipline is
[Chapter 02](../02-evaluation-science-and-experimental-design/README.md)'s;
the calibration machinery is
[Chapter 06](../06-honesty-uncertainty-and-selective-prediction/README.md)'s
and P03's; adversaries *inducing* concept shift is
[Chapter 12](../12-adversarial-ml-and-robustness/README.md)'s;
faithfulness of deployed reasoning continues in Chapter 18.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [part-02-03-robust-training-monitoring](../../courses/google-deepmind-agi-safety/part-02-03-robust-training-monitoring.md) | DeepMind AGI Safety | training-time robustness plus deployment-time monitoring |
| [module-12-lifecycle-governance](../../courses/safeshield-governance/module-12-lifecycle-governance.md) | Safeshield Governance | change management and the gates that keep deployed systems true |
