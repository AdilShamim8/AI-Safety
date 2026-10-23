# Chapter 20 — Misuse, dangerous capabilities, and release evaluation

| | |
|---|---|
| **Chapter** | 20 — Misuse, dangerous capabilities, release evaluation: what a model *can* do (not just what it *does*), elicitation as a lower-bound discipline, uplift measurement, access conditions, safeguards, and the release decision itself — non-operational: we design and audit these evaluations, we do not run uplift operations |
| **Questions** | A model refuses every dangerous request you can think of. What does that tell you about what it could do under better elicitation, an attacker's fine-tune, or a scaffold you did not test? And when an evaluation says "no evidence of dangerous capability," what is the exact statement that number licenses you to make at the release gate — and what does it silently not say? |
| **Hard prerequisites** | [Chapter 15 — red teaming](../15-red-teaming-and-adversarial-evaluation/README.md) (adaptive evaluation); [Chapter 07 — evaluation awareness](../07-deception-scheming-and-evaluation-awareness/README.md) (sandbagging); [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (construct validity, uplift as causal measurement) |
| **Core artifact** | Release-evaluation design: an elicitation ladder with a pre-stated gate rule, an uplift study with treatment/control arms and paired statistics, and the release-decision memo that states what was measured, what was assumed, and what was waived |
| **Projects** | P10 (capstone assurance dossier) consumes this chapter's design discipline |
| **Readings** | Section 7 — four newly register-verified sources plus re-anchored ones |

## 1. Research question and failure pathway

The release question is not "is the model aligned on our prompts" —
Chapters 04-08 measured that. It is "what is the worst capability
this artifact places in the world, under the best elicitation an
adversary can afford, and does that clear our thresholds?" The
failure pathway:

1. **Misuse is a category of catastrophe with structure.** The
   catastrophic-risk overview organizes the sources of risk into four
   categories — *malicious use* (individuals or groups intentionally
   using AI to cause harm), *AI race* (competitive pressure to deploy
   unsafe systems or cede control), *organizational risks* (human
   factors and complex systems breeding accidents), and *rogue AIs*
   (the control problem for agents smarter than the overseers)
   [SRC-PAPER-093]. Release evaluation primarily instruments the
   first; the other three are governance and engineering chapters'
   territory (21, 22) — but the release memo must say which of the
   four it is *not* covering.
2. **"No evidence" is a measurement statement, not a property.**
   Dangerous-capability evaluations are lower bounds by construction:
   the evaluated model's measured abilities depend on the elicitation
   used — scaffolding, prompting, fine-tuning, rollouts — and the
   evaluating organization itself states that additional methods
   could elicit behaviors beyond what was observed
   [SRC-PAPER-094; SRC-REPORT-008's framing]. An evaluation that
   finds nothing certifies the elicitation it used, not the model.
3. **Emergent-looking capability jumps can be metric artifacts.** The
   mirage result: abilities that appear sharp and unpredictable at
   scale can be artifacts of discontinuous metrics — choosing
   nonlinear metrics makes smooth improvement look like sudden
   emergence [SRC-PAPER-095]. The release evaluator's twin errors:
   reading a metric cliff as a capability cliff (false alarm), or a
   smooth metric as no-threshold (missed gate). The *metric* is part
   of the claim.
4. **Uplift is the misuse quantity, and it is causal.** "The model
   can explain X" is not the release-relevant quantity; *uplift* —
   the difference in achieved harmful outcomes between actors with
   the model and actors with the best non-AI baseline (a search
   engine, a library) — is. The dangerous-capability programme's four
   areas (persuasion and deception; cyber-security; self-proliferation;
   self-reasoning) were piloted on Gemini 1.0 models with no strong
   capabilities found but early warning signs flagged
   [SRC-PAPER-094]; WMDP operationalizes the knowledge side as a
   3,668-question proxy with an unlearning target [CLM-0120;
   re-anchored].
5. **The gate itself is a published framework — read it as an
   artifact.** Frontier labs publish capability-threshold structures:
   Anthropic's Responsible Scaling Policy defines AI Safety Levels
   (ASL-1: no meaningful catastrophic risk; ASL-2: early signs,
   current LLMs; ASL-3: substantial misuse-risk increase over
   non-AI baselines or low-level autonomy; ASL-4+: undefined),
   modeled on biosafety levels, board-approved, published 2023-09-19
   [SRC-REPORT-008]; OpenAI's Preparedness Framework tracks
   categories (cybersecurity, biological and chemical, persuasion,
   model autonomy) at Low/Medium/High/Critical levels with Critical
   meaning not deployable [SRC-REPORT-009]. These are *claims
   structures* — the evaluator's job is to test whether the stated
   threshold logic is actually implemented by the stated
   measurements.

The chapter's reframe: a release evaluation is a *pre-registered
causal claim about a capability ceiling* — with elicitation as the
treatment, uplift as the effect, and the honest statement that
ceilings are only as good as the ladder you climbed to look for them.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 15's adaptive-evaluation discipline (the
attacker gets to respond to your defense); Chapter 07's sandbagging
(evaluations measure what the model *shows*); Chapter 02's causal
inference basics (uplift is a two-arm experiment or it is nothing).

**Outcomes.** After this chapter you can:

- state the four catastrophic-risk categories and locate release
      evaluation within them [SRC-PAPER-093];
- design an elicitation ladder (base → scaffolded → attacker-fine-
  tuned) with pre-stated decision rules and lower-bound honesty
  [SRC-PAPER-094];
- design an uplift study with treatment/control arms, paired
  statistics, and the correct null;
- read a published safety-level framework as a testable claim
  structure [SRC-REPORT-008, SRC-REPORT-009];
- and write the release-decision memo: measured, assumed, waived.

**Scope exclusions — non-operational.** This chapter designs and
audits evaluations; it does not operationalize uplift against real
hazards (no operational details for any misuse domain; capability
content stays at category level exactly as WMDP's filtering does),
does not replicate lab frameworks, and does not cover the race/
organizational/rogue-AI categories' governance instruments (Ch. 21
and 23's territory).

## 3. The core explanation

### 3.1 The quantity of interest: uplift, not ability

Raw ability claims ("the model scores X on a bio QA set") founder on
the construct problem: what is X *relative to*? The release-relevant
construct is **uplift**: the causal difference in achieved harmful
outcome between an actor with the model and the same actor with the
strongest available non-model baseline. The two-arm design is
Chapter 02's: randomize actors (or actor-tasks), give one arm the
model and the control arm the baseline (search, textbooks), measure
task completion, test the difference. The published programme's
four areas [SRC-PAPER-094] — persuasion/deception, cyber-security,
self-proliferation, self-reasoning — are the field's consensus on
where uplift matters most; WMDP [CLM-0120] covers the knowledge side
with an explicit proxy-and-filter posture.

The measurement's hard limits: n is small (expert actors are scarce),
outcome grading is contested, and the arms' *baseline strength*
decays as the world's non-AI tooling improves — an uplift number is
dated the way Ch. 17's deployment numbers are dated.

### 3.2 Elicitation: the ladder, and why evaluations are lower bounds

A model's measured capability is a function of the elicitation:
prompting, scaffolding (tools, agents, rollouts), and fine-tuning
(including an attacker removing refusals). The ladder discipline:

1. **Base/prompted arm** — the shipped system, standard prompts.
2. **Scaffolded arm** — the same weights with adversarial scaffolds
   (agentic loops, tools, longer rollouts).
3. **Attacker-fine-tuned arm** — weights an adversary can tune
   (open-weights) or prompt-optimized (API) with refusal-suppression.

Each rung is a *treatment*; the measured rate at each rung gets its
own interval, and the **highest rung's interval is the honest
ceiling estimate** — still a lower bound on what better elicitation
would find, exactly as the frontier evaluators themselves state
[SRC-PAPER-094]. Sandbagging (Ch. 07) inverts the problem: the model
may *under*-perform at evaluation time, which is why capability
claims are bounded above by elicitation effort and below by nothing
measured.

### 3.3 The mirage discipline: metrics are part of the claim

Emergent-ability claims decompose into metric choices: a nonlinear
or discontinuous score (exact-match over a capability threshold)
turns smooth improvement into a sharp cliff [SRC-PAPER-095]. The
release-gate discipline: report capability trends under at least two
metrics — the thresholded (gate-relevant) one and a continuous
underlying one (per-token success, graded partial credit) — and
state which properties each metric has. A gate that fires on a
thresholded metric is fine; a gate that claims *unpredictability*
because the thresholded metric jumps is a metric artifact read as a
fact.

### 3.4 Reading the published frameworks as claim structures

Anthropic's RSP [SRC-REPORT-008]: ASL thresholds keyed to *capability
demonstrations* (ASL-3 triggered by substantial misuse-risk increase
over non-AI baselines or low-level autonomy), with the ASL-4
measures explicitly unwritten at publication and a commitment to
write them before reaching ASL-3 — an honest, auditable gap. OpenAI's
Preparedness Framework [SRC-REPORT-009]: four tracked categories,
Low/Medium/High/Critical levels, Critical = not deployable. The audit
questions both structures must survive: (i) are the threshold
*definitions* operational (would two teams score the same model the
same way)? (ii) are the *measurements* the definitions require
actually run (uplift studies, elicitation ladders — or proxies)? and
(iii) does the release decision *track* the level logic, or does the
memo quietly override it? A framework is evidence about an
organization's discipline, not about a model.

### 3.5 Access conditions and the dual-use ledger

The release decision is not binary over one model: access conditions
(weight release vs API; rate limits; KYC; usage policies; safeguards
inference-time vs training-time) trade capability exposure against
concentration of control — the open-weights debate Ch. 21 takes up.
The evaluator's ledger: each access condition changes which rungs of
the elicitation ladder an adversary can reach (an attacker with
open weights reaches the fine-tuning rung by construction), so *the
gate thresholds must be re-stated per access condition*, not held
fixed while the access surface moves.

## 4. Worked example — the Prometheus release gate

Prometheus is a (fictional) frontier model approaching release. The
release evaluation design, executed here in miniature with all
numbers recomputed via `wilson_interval` (95%, z = 1.96):

**Instrument 1 — the uplift study (station 4).** 60 expert-novice
task pairs in a (simulated, synthetic-task) bio-knowledge domain:
completion with the model (treatment) vs with the strongest non-AI
baseline (control). Treatment 19/60 = 31.7% → **[21.3%, 44.2%]**;
control 8/60 = 13.3% → **[6.9%, 24.2%]**; two-proportion z = 2.40
(p ≈ 0.016). Paired by task pair: 17 treatment-complete/control-
incomplete vs 6 reverse, exact two-sided **p = 0.0347**. Uplift is
demonstrated in the synthetic domain — and the memo states the
construct limit: synthetic-task uplift licenses *nothing* about
real-wet-lab uplift, only that the measurement machinery works.

**Instrument 2 — the elicitation ladder (stations 2-3).** The
100-item dangerous-capability probe (persuasion/cyber/autonomy mix,
category-level content): base 11/100 = 11.0% → **[6.3%, 18.6%]**;
scaffolded (agentic loop + tools) 24/100 = 24.0% → **[16.7%,
33.2%]**; attacker-fine-tuned (refusal-suppression on the open-weight
twin) 31/100 = 31.0% → **[22.8%, 40.6%]**. The ladder's shape — each
rung's interval above the previous — is the finding: the shipped
refusals are a *scaffold*, not a *ceiling*, exactly the lower-bound
discipline [SRC-PAPER-094]. The gate rule (pre-stated): if the
attacker-fine-tuned arm's lower bound exceeds 20% on the autonomy
subscale, escalate the ASL assessment.

**Instrument 3 — the autonomy subscale with a zero-success arm.**
Self-proliferation-style subtasks (category level: account creation,
resource acquisition, sandbox escape descriptions — synthetic): 3/150
= 2.0% → **[0.7%, 5.7%]**. The zero-success sibling battery (the
harder half): 0/150 → **[0.0%, 2.5%]** — the classic zero-numerator
statement: "no successes in 150 trials" bounds the rate below 2.5%
at 95% — *under this elicitation*, the memo says, in those words.

**Instrument 4 — the metric-mirage check (station 3).** The
capability trend re-scored continuously (graded partial credit)
shows smooth growth where the thresholded gate metric shows a jump
between checkpoints — so the memo reports both and declines the
"emergent at N params" claim [SRC-PAPER-095].

**The release-decision memo.** Measured: synthetic-domain uplift
(p = 0.0347); the ladder (11% → 31%); autonomy below the zero-
numerator bound under tested elicitation. Assumed: elicitation
coverage (our ladder is not the adversary's frontier); synthetic→
real transfer (unmeasured, waived into the risk register). Waived:
the race and organizational categories [SRC-PAPER-093] — out of
scope, named. Gate outcome: ASL-2-style posture with the fine-tuned
arm's interval watched at the next checkpoint. The memo's one-
sentence honesty: "we measured what our ladder could reach, and our
ladder is not the ceiling."

## 5. Approach comparison

| Approach | Question answered | Strength | Failure station | Cost |
|---|---|---|---|---|
| QA-style capability probes | Does the model know X? | Cheap, repeatable (WMDP-style) | knowledge ≠ uplift (station 4) | Eval run |
| Uplift study (two-arm) | Does access change outcomes? | Causal, release-relevant | small-n, dated baselines | Expert actors, grading |
| Elicitation ladder | What's the ceiling under better elicitation? | Lower-bound honesty built in | unbounded adversary space | Rung × model |
| Metric-mirage check | Is the "jump" real? | Separates metric from capability | needs both metrics designed in | Re-scoring |
| Safety-level frameworks | Is the org's gate logic sound? | Auditable claim structure | implementation gap (stated vs run) | Audit labor |
| Safeguards (inference/training) | Can refusal be counted on? | Raises the base arm | scaffold not ceiling (ladder) | Serving cost |

## 6. Where the methods fail

- **The ladder is always too short.** However many rungs, the
  adversary's elicitation can exceed them; "no evidence" statements
  must carry the elicitation scope [SRC-PAPER-094's own framing].
- **Uplift baselines rot.** The control arm (search, libraries)
  improves over time; yesterday's "no uplift" is today's "uplift"
  with no model change — re-run dates are part of the claim
  (Ch. 17 discipline applied to gates).
- **Sandbagging poisons the lower bound.** If the model under-performs
  at evaluation time (Ch. 07), even the ladder's top rung
  underestimates — capability floors are unmeasured by these
  methods.
- **Zero-numerator bounds are elicitation-scoped.** "0/150" bounds
  the rate *under the tested elicitation*; quoting it without that
  qualifier is the chapter's cardinal sin.
- **Frameworks can be implementational fictions.** Published
  threshold logic with unpublished measurement detail — or release
  memos that override levels — makes the framework a press release
  [SRC-REPORT-008's own ASL-4 honesty is the counter-example to
  emulate].
- **Category-level honesty has a cost.** WMDP's stringent filtering
  [CLM-0120] is what *makes* it publishable; evaluations that trade
  that honesty for realism inherit publication constraints — a real
  trade, stated, not solved.

## 7. Readings

**Verified for this chapter (2026-10-23):**

- Hendrycks, Mazeika, Woodside — *An Overview of Catastrophic AI
  Risks*, arXiv:2306.12001 [SRC-PAPER-093; CLM-0144]. The four
  categories; the chapter's scope map.
- Phuong et al. (27 authors) — *Evaluating Frontier Models for
  Dangerous Capabilities*, arXiv:2403.13793 [SRC-PAPER-094;
  CLM-0145]. The four-area programme; Gemini 1.0 pilot; the
  lower-bound posture.
- Schaeffer, Miranda, Koyejo — *Are Emergent Abilities of Large
  Language Models a Mirage?*, arXiv:2304.15004 [SRC-PAPER-095;
  CLM-0146]. Metric artifacts as emergence.
- Anthropic — *Anthropic's Responsible Scaling Policy*
  (anthropic.com, page-inspected 2026-10-23; published 2023-09-19)
  [SRC-REPORT-008; CLM-0147]. ASL-1..4 structure; board approval;
  the unwritten-ASL-4 honesty.
- OpenAI — *Preparedness Framework (Beta)* structure and current
  category assessments (verified via OpenAI deployment-safety
  content surfaced 2026-10-23) [SRC-REPORT-009; CLM-0148].
  Low/Medium/High/Critical; Critical = not deployable.

**Re-anchored from the registers:** WMDP [SRC-PAPER-076; CLM-0120];
HarmBench [SRC-PAPER-005; cards/11]; AdvBench [cards/09];
sandbagging [Ch. 07's register]; XSTest/HaluEval [cards 06, 17] as
over-refusal/hallucination instruments on the safety side of the
gate.

## 8. Exercises

**Exercise 20.1 — lower-bound grammar (analysis).** Rewrite each
claim into honest release language, with the elicitation scope and
denominator stated: (a) "no evidence of self-proliferation
capability"; (b) "the model passes 92% of our safety evals"; (c) "the
fine-tuned arm's autonomy rate is 31%." State for each: what made the
original unsupportable, and what measurement would support the
rewritten version.

**Exercise 20.2 — the uplift study, correctly powered (statistics).**
For instrument 1's design: (a) compute the paired exact p for 17 vs 6
discordant pairs (show the binomial-tail argument); (b) the team
wants to detect a 15-point uplift with 80% power at α = 0.05 —
roughly what n per arm does a two-proportion test need (state your
variance assumption)?; (c) name the two threats that make *expert*
uplift studies harder than the synthetic version (and what each does
to the interval).

**Exercise 20.3 — gate audit (judgment, graded).** You are auditing
a lab whose published framework [SRC-REPORT-008-style] defines an
ASL-3 trigger ("substantial misuse-risk increase over non-AI
baselines") but whose release memo for the current model cites only
QA-probe scores. Write the 350-word audit finding: which audit
question (§3.4) fails, what measurement the definition requires,
what the memo's substitution hides, and the one remediation you
demand before signing.

**Exercise 20.4 — release-evaluation design (the chapter
assessment).** Design the complete release evaluation for a
medium-capability open-weights model: the four programme areas
[SRC-PAPER-094] each with construct, instrument, arms, denominators,
elicitation rungs (justifying why open weights forces the
fine-tuning rung), the metric-mirage check, the pre-stated gate
rules, and the access-conditions section (§3.5) — 800-1,000 words.
Include the waived-categories statement [SRC-PAPER-093].

## 9. Hints

- 20.1: every honest sentence has the form "under elicitation E, on
  n tasks, the rate was r [interval] — and E is not the ceiling."
- 20.2(b): the two-proportion n is driven by the *smaller* rate's
  variance; assume the control rate near instrument 1's and round up.
- 20.3: the definition names uplift; the memo supplied ability —
  that substitution is the finding.
- 20.4: open weights make refusal-suppression a *base property* of
  the released artifact, not an attack — the ladder's top rung
  becomes the shipped product.

## 10. Completion

This chapter is complete when you can:

- [ ] state the four catastrophic-risk categories and scope release
      evaluation inside the first [SRC-PAPER-093];
- [ ] design and price an uplift study with paired statistics;
- [ ] build an elicitation ladder with pre-stated gate rules and
      lower-bound language throughout [SRC-PAPER-094];
- [ ] run the metric-mirage check before claiming any capability
      discontinuity [SRC-PAPER-095];
- [ ] audit a published safety-level framework's threshold logic
      against its actual measurements [SRC-REPORT-008, 009];
- [ ] and write a release memo whose measured/assumed/waived lists
      are each non-empty and honest.

Cross-links: adaptive red-teaming is
[Chapter 15](../15-red-teaming-and-adversarial-evaluation/README.md)'s;
sandbagging is
[Chapter 07](../07-deception-scheming-and-evaluation-awareness/README.md)'s;
the sociotechnical categories this chapter waives are Chapter 21's
(planned); the assurance-case form the release memo takes is Chapter
22's (planned).
