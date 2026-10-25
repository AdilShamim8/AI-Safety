# Chapter 21 — Sociotechnical and systemic risk

| | |
|---|---|
| **Chapter** | 21 — Sociotechnical and systemic risk: automation bias and overreliance; disparate impact and the fairness impossibility landscape; incentives and competitive pressure; stakeholder analysis; linguistic coverage; power and concentration |
| **Questions** | The model is only one actor in the system that deploys it. When the humans defer too much, the metrics split by group in ways no single number can repair, the incentives reward shipping over verifying, and whole languages are simply absent — which failure modes belong to the model, which to the system, and who gets to decide? |
| **Hard prerequisites** | [Chapter 01 — risk models](../01-risk-models-and-research-epistemics/README.md) (the six-primitive decomposition; evidence kinds); [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (construct validity — this chapter weaponizes it) |
| **Core artifact** | Stakeholder and failure-pathway analysis: a deployment mapped to stakeholders, each systemic failure mode located (model, decision-rule, deployment context, incentive structure), with measured rates by group and the fairness-trade-off statement |
| **Projects** | Feeds P09 (shift/subgroup reliability) and P10 (capstone) |
| **Readings** | Section 7 — four newly register-verified sources plus re-anchored dataset cards |

## 1. Research question and failure pathway

Every chapter before this one located risk *in the model or its
inputs*. This chapter locates risk in the *system around the model* —
the humans who defer to it, the decision rules that consume its
scores, the incentives that fund it, and the populations it silently
omits. The failure pathway has five stations:

1. **Overreliance is a first-class risk, not user error.** LLMs
   function as collaborative "thought partners," and as they
   influence consequential decisions from healthcare to personal
   advice, the risk of *relying on them beyond their capabilities*
   grows; the risks consolidate at individual and societal levels —
   high-stakes errors, governance challenges, and *cognitive
   deskilling* — with LLM characteristics, system design features,
   and user cognitive biases jointly raising the concern
   [SRC-PAPER-096]. The measured signature (this chapter's worked
   example): the human-in-the-loop adds almost nothing over the AI
   alone, because humans rubber-stamp AI errors.
2. **"Bias" without normative reasoning is measurement without a
   claim.** The critical survey of 146 bias-in-NLP papers found
   motivations often vague, inconsistent, and lacking in normative
   reasoning — despite bias analysis being *inherently normative* —
   and proposed quantitative techniques poorly matched to their
   motivations, largely unengaged with non-NLP literature
   [SRC-PAPER-097]. The stakeholder analysis must therefore *name
   the harm and the harmed* before any metric is computed.
3. **Fairness definitions conflict — provably.** Three fairness
   conditions at the heart of public debates (calibration, error-rate
   balance, and the third condition) *cannot be satisfied
   simultaneously* except in highly constrained special cases; even
   approximate satisfaction requires the base rates to be equal
   across groups [SRC-PAPER-098]. Choosing a fairness metric is
   choosing a trade-off — a decision with stakeholders, not a
   technical detail.
4. **Fairness debates are older than ML and the lessons repeat.**
   Quantitative fairness definitions have circulated for 50+ years
   in education and hiring testing; earlier definitions are similar
   or identical to modern ML ones, and the testing communities'
   cultural and social context explains which definitions emerged
   when [SRC-PAPER-099]. The ML field's novelty claim is itself a
   systemic failure: we re-litigate settled debates without the
   history.
5. **Coverage is power.** The model speaks some languages well,
   others not at all, and "not at all" is not an error state — it is
   a design decision about whom the deployment is *for*. The bias
   benchmark cards (BOLD, BBQ, CrowS-Pairs, Winogender — all
   US/Western-English scoped, verified in the dataset catalog)
   measure bias *within* covered populations; the stakeholder
   analysis must also measure the *boundary of coverage itself*.

The chapter's reframe: systemic risk is not aggregated model risk —
it is the risk the *system* creates that no model fix addresses:
deference, decision-rule artifacts, incentive pressure, and exclusion.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 01's six-primitive decomposition (this
chapter extends it beyond the model); Chapter 02's construct
validity (fairness metrics are constructs; the impossibility result
is why construct choice is a stakeholder decision).

**Outcomes.** After this chapter you can:

- measure overreliance in a human-AI decision loop (the complementarity
  gap and the AI-error catch rate) with intervals;
- state the fairness impossibility result and its practical meaning
  for metric choice [SRC-PAPER-098];
- run a disparate-impact measurement with the four-fifths screen and
  per-group error rates, each with denominators and intervals;
- build the stakeholder-and-failure-pathway analysis: stakeholders
  named, harms named, each failure located (model / decision rule /
  deployment context / incentive structure), coverage boundary
  mapped;
- and write the fairness-trade-off statement that a deployment's
  chosen metric *silently makes* [SRC-PAPER-097, 098, 099].

**Scope exclusions.** This chapter is analysis, not legal advice —
the four-fifths rule is used as a screening statistic with its
regulatory *context* noted, not as compliance counsel; it does not
cover governance instruments (Ch. 23) or assurance-case form (Ch.
22); and it does not operationalize any fairness intervention — the
trade-off statement precedes any mitigation.

## 3. The core explanation

### 3.1 Overreliance: measuring the human in the loop

The overreliance framework [SRC-PAPER-096] names the mechanism
stack: LLM characteristics (fluency, confidence-styled outputs),
system design (defaults, friction, interface), and user cognitive
biases (automation bias — the documented human tendency to follow
automated recommendations even against contradicting evidence). The
measurement discipline this chapter instruments:

- **Complementarity gap:** (human+AI) accuracy minus max(human, AI)
  accuracy. Positive = the human adds signal; ~zero = rubber-
  stamping; negative = the interface *destroys* human signal.
- **AI-error catch rate:** on the items the AI gets wrong, the
  fraction the human+AI system still gets right. This is the number
  that dies first under automation bias — and the deskilling
  concern [SRC-PAPER-096] is its longitudinal version: catch rates
  atrophy when the human never has to decide alone.

Both rates get intervals; both are reported next to the human-alone
and AI-alone baselines; the paired test between combined and AI-
alone tells you whether "human in the loop" is a safety property or
a story.

### 3.2 The normative step: name the harm before the metric

The survey's finding [SRC-PAPER-097] becomes the chapter's
procedure: before computing any group-disaggregated metric, the
analysis must state (i) *which population is at risk of what harm*
(the decision's consequence), (ii) *which construct* connects the
model's output to that harm, and (iii) *whose definition* of fair is
being operationalized. A "bias score" without those three is the
vague-motivation pattern the survey documented 146 times.

### 3.3 The impossibility landscape, operationally

Kleinberg, Mullainathan, and Raghavan [SRC-PAPER-098]: calibration,
error-rate balance, and predictive-parity-style conditions are
mutually unsatisfiable except when base rates are equal across
groups. Operationally, for a deployment with unequal base rates:

- choosing *calibration* means accepting unequal error rates per
  group;
- choosing *equal error rates* means accepting miscalibration for at
  least one group;
- the choice is a **stakeholder-visible decision** that the release
  memo must state — not a default buried in a library.

Hutchinson and Mitchell's history [SRC-PAPER-099] adds the field's
humility: these debates have run since the 1960s in education and
hiring testing; the ML rediscovery inherits both the definitions and
the political context, and ignoring the history repeats its mistakes.

### 3.4 Coverage as a design decision

The linguistic-coverage audit: which languages does the deployment
serve at what quality — and what happens to a speaker outside the
boundary? Coverage failure is not an error rate (there is no
denominator); it is exclusion. The stakeholder analysis maps the
boundary and names who is outside it. The bias-cards' US-English
scoping (verified: CrowS-Pairs "protected demographic groups in the
US"; BOLD/WinoGender/BOLD seeds all English corpora) is the concrete
anchor: within-population bias instruments say nothing about the
unserved.

### 3.5 Incentives and the race condition

Hendrycks et al.'s second category [SRC-PAPER-093, re-anchored] —
the AI race, where competitive environments compel deploying unsafe
systems — is the systemic station the stakeholder analysis must
include even though it has no per-query metric: its instruments are
organizational (release-gate discipline, Ch. 20's frameworks) and
its failure mode is *the quiet removal of every friction the earlier
chapters installed*. The analysis names which frictions the
deployment's incentives are pushing against.

## 4. Worked example — the Ceres loan-screening audit

Ceres deploys an LLM-assisted loan pre-screening tool. The
sociotechnical audit (this chapter's core artifact, miniature):

**Instrument 1 — disparate impact (stations 2-3).** 200 applicants
per group (matched synthetic file pairs): group A pass 132/200 =
66.0% → **[59.2%, 72.2%]**; group B pass 78/200 = 39.0% →
**[32.5%, 45.9%]**. Impact ratio = 0.390/0.660 = **0.591** — below
the four-fifths screen (0.80) by a wide margin. Per-group FPR (of
true negatives): A 14/120 = 11.7% → **[7.1%, 18.6%]**; B 31/110 =
28.2% → **[20.6%, 37.2%]** — error-rate balance also fails. The
normative step first: the harm is *denied credit*, the construct is
the decision rule's threshold applied to the model's score, and the
impossibility statement is on the memo — no single metric repair
exists [SRC-PAPER-098]; the deployment must *choose* which condition
to relax, with stakeholders seeing the choice.

**Instrument 2 — overreliance (station 1).** 120 loan decisions,
three arms: human alone 72/120 = 60.0% → **[51.1%, 68.3%]**; AI
alone 102/120 = 85.0% → **[77.5%, 90.3%]**; human+AI (advisory
interface) 104/120 = 86.7% → **[79.4%, 91.6%]**. The complementarity
gap is +1.7 points and the paired test says nothing (discordant 14
vs 12 of 26, two-sided p = 0.845) — the human contribution is not
distinguishable from noise. On the 18 AI-wrong items the human+AI
system caught only 5 = 27.8% → **[12.5%, 50.9%]**: the safety story
("a human reviews everything") is measured and false in the
automation-bias direction [SRC-PAPER-096].

**Instrument 3 — coverage boundary (station 5).** The deployment
serves 4 languages at measured quality; the applicant population
includes a fifth at 9% frequency — those applicants receive the
fallback path (a slower human queue, measured: 3.2x cycle time).
The analysis maps it: exclusion from the fast path is a design
property, its stakeholders named, its rate reported.

**The report's verdict.** The tool's group-B disparity is a decision-
rule + base-rate artifact that fairness metrics cannot jointly fix
[impossibility, SRC-PAPER-098]; the human oversight is measured
rubber-stamping; the coverage boundary is a design decision. The
remediation memo names the trade-off choice, re-instruments the
human loop (forced-independence sampling — re-measure the catch
rate), and moves the coverage decision to stakeholders. No sentence
says "the model is biased" alone — every finding is located in the
system.

## 5. Approach comparison

| Approach | Question answered | Strength | Failure station | Cost |
|---|---|---|---|---|
| Complementarity/catch-rate measurement | Does the human add signal? | Direct overreliance evidence [SRC-PAPER-096] | longitudinal deskilling needs cohorts | Experiment design |
| Four-fifths screen | Is there a prima facie disparity? | Simple, regulatory-anchored | screening only — construct not established | Cheap |
| Per-group error/calibration rates | Where does the disparity live? | Locates the failure (rule vs model) | which metric = which trade-off [SRC-PAPER-098] | Disaggregation |
| Stakeholder analysis | Who is harmed by what, and who decides? | Forces the normative step [SRC-PAPER-097] | can become theater without measured rates | Facilitation |
| Coverage mapping | Whom does the system exclude? | Makes design boundaries visible | no denominator — exclusion is not error | Language audit |
| Incentive mapping (race condition) | What frictions are under pressure? | Names removal risks [SRC-PAPER-093] | organizational honesty required | Governance |

## 6. Where the methods fail

- **Fairness metrics cannot be stacked.** The impossibility result
  means "we satisfy every fairness check" is false for any
  unequal-base-rate deployment unless special conditions hold
  [SRC-PAPER-098] — a vendor claiming it has not made the choice the
  result forces.
- **The four-fifths screen is not a construct.** It flags ratios;
  whether the flagged disparity is the *harm* requires the normative
  step [SRC-PAPER-097] and the base-rate analysis — a legal-context
  statistic misused as a fairness definition is the survey's
  vague-motivation pattern re-run.
- **Catch-rate measurements decay.** A catch rate measured at launch
  measures fresh humans; deskilling is longitudinal [SRC-PAPER-096]
  and needs cohort re-measurement the way Ch. 17 needs drift
  re-measurement.
- **Stakeholder processes get captured.** The analysis's value
  survives only if the *trade-off choice* [SRC-PAPER-098] is made
  visibly after the analysis, not before it in a vendor's slide.
- **Coverage mapping without service data is self-report.** "We
  support language X" needs a measured quality arm per language, or
  it is marketing.

## 7. Readings

**Verified for this chapter (2026-10-23):**

- Ibrahim et al. (17 authors) — *Measuring and mitigating
  overreliance to build human-compatible AI*, arXiv:2509.08010
  [SRC-PAPER-096; CLM-0149]. The risk consolidation; the mechanism
  stack; the measurement gaps and directions.
- Blodgett, Barocas, Daumé, Wallach — *Language (Technology) is
  Power: A Critical Survey of "Bias" in NLP*, arXiv:2005.14050
  [SRC-PAPER-097; CLM-0150]. The 146-paper finding; the normative
  requirement.
- Kleinberg, Mullainathan, Raghavan — *Inherent Trade-Offs in the
  Fair Determination of Risk Scores*, arXiv:1609.05807
  [SRC-PAPER-098; CLM-0151]. The impossibility result.
- Hutchinson, Mitchell — *50 Years of Test (Un)fairness: Lessons
  for Machine Learning*, arXiv:1811.10104 [SRC-PAPER-099;
  CLM-0152]. The historical continuity of fairness definitions.

**Re-anchored from the registers:** the bias dataset cards (BOLD,
BBQ, CrowS-Pairs, Winogender — with their verified US-English
scoping); the AI-race category [SRC-PAPER-093]; Ch. 17's
worst-group discipline; Ch. 20's gate memos.

**Note companions:** [19 Wild patterns — a survey of real-world ML failures](../../research/notes/19-wild-patterns-survey.md)

## 8. Exercises

**Exercise 21.1 — the normative step, first (analysis).** For a
hiring-screening deployment: write the three normative statements
(population-at-risk/harm, construct, whose fairness definition)
*before* any metric; then name the two fairness conditions the
deployment's chosen metric silently sacrifices [SRC-PAPER-098], and
what the release memo must therefore say.

**Exercise 21.2 — complementarity arithmetic (statistics).** From
the Ceres arms: (a) compute the complementarity gap and its honest
uncertainty (which comparison, which test?); (b) the AI-error catch
rate is 5/18 — compute the interval and state what it does and does
not establish about automation bias; (c) design the forced-
independence re-measurement (sampling design, denominator, the pre-
stated catch-rate threshold that would count as "oversight
restored").

**Exercise 21.3 — impossibility, concretely (derivation-light).**
Explain to a hiring manager in ≤ 200 words why "make the model
calibrated *and* treat every group's errors equally" is not a goal
but a choice — using the base-rate condition [SRC-PAPER-098] and one
concrete unequal-base-rate example. Then write the one-sentence
trade-off statement their release memo needs.

**Exercise 21.4 — stakeholder and failure-pathway analysis (the
chapter assessment).** Build the full artifact for a (chosen)
deployment: stakeholder map with power/interest axes; the five
stations each located (model / decision rule / deployment context /
incentive structure / coverage boundary); the measured rates by
group with intervals; the coverage map; the incentive-friction list;
and the fairness-trade-off statement — 800-1,000 words, every
finding located in the system, none blamed on "the model" alone.

## 9. Hints

- 21.1: if you can't name the harmed population, you are computing a
  number, not a claim [SRC-PAPER-097's finding, applied].
- 21.2(a): the gap is a *difference of dependent proportions* — the
  paired discordant test, not two independent intervals.
- 21.3: the special case where all three conditions hold is *equal
  base rates* — start there and break it.
- 21.4: the analysis fails if every failure lands in the "model"
  box — the stations exist to force the system into view.

## 10. Completion

This chapter is complete when you can:

- [ ] measure overreliance (complementarity gap, catch rate) and
      state what the human-in-the-loop is worth;
- [ ] run the normative step before any fairness metric
      [SRC-PAPER-097];
- [ ] state the impossibility result and write the trade-off
      statement it forces [SRC-PAPER-098];
- [ ] place modern fairness debates in their 50-year testing
      context [SRC-PAPER-099];
- [ ] map coverage as exclusion, not error;
- [ ] and deliver a stakeholder analysis whose findings are located
      in the system, with the incentive station honestly populated.

Cross-links: the six-primitive decomposition is
[Chapter 01](../01-risk-models-and-research-epistemics/README.md)'s;
construct validity is
[Chapter 02](../02-evaluation-science-and-experimental-design/README.md)'s;
worst-group measurement is
[Chapter 17](../17-distribution-shift-and-deployment-reliability/README.md)'s;
the release-memo form is
[Chapter 20](../20-misuse-dangerous-capabilities-release-evaluation/README.md)'s;
assurance-case form is Chapter 22's (planned); governance
instruments are Chapter 23's (planned).
