# Chapter 15 — Red teaming and adversarial evaluation

| | |
|---|---|
| **Chapter** | 15 — Red teaming and adversarial evaluation: coverage, adaptive attacks, benign controls, scoring with denominators, over-refusal, responsible reporting |
| **Questions** | What does a red-team *finding* actually establish about a deployed system — and what does it never establish? When is "we red-teamed it" evidence, and when is it a ritual? |
| **Hard prerequisites** | [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (interval arithmetic, adaptive overfitting); [Chapter 12 — adversarial ML](../12-adversarial-ml-and-robustness/README.md) (attacker-knowledge grid, defense-evaluation failures); [Chapter 13](../13-llm-application-security/README.md) (injection mechanics) |
| **Core artifact** | Attack/defense report: a preregistered red-team engagement with a coverage taxonomy, explicit denominators, benign controls, an adaptive phase, a two-sided ledger (safety up / false refusal), and a responsible-disclosure section |
| **Projects** | P07 (injection defense) supplies the paired-harness discipline; P10 carries the capstone version |
| **Readings** | Section 7 — four newly register-verified sources plus re-anchored earlier ones |

## 1. Research question and failure pathway

Red teaming is the practice of *attacking your own system before
someone else does* — simultaneously discovering, measuring, and
attempting to reduce harmful outputs, in the founding paper's
three-verb formulation [SRC-PAPER-058]. The failure pathway this
chapter instruments is not "the red team failed to break the model"
but "the red team *succeeded*, and the result still taught the
operator nothing true":

1. **Coverage is enumerable; attacks are not.** A red-team effort
   samples an attack space with no known closure. Whatever it finds
   is a lower bound; what it does *not* find is compatible with both
   "no more attacks exist" and "we ran out of budget" — the same
   0.995^n discipline Chapter 12 applies to defense audits applies
   here to the audit itself.
2. **The oracle problem.** Recognizing a failure is itself a task —
   when failures are cheaply classifiable in advance, red teaming has
   limited marginal value (you could just filter); the hard cases
   require establishing what counts as failure *as part of the
   exercise* [SRC-PAPER-060].
3. **Overfitting to the red team.** A model patched against
   yesterday's attacks degrades on tomorrow's; the adaptive
   evaluation discipline (attack the *defense*, not the benchmark)
   is the only thing standing between a mitigation report and a
   Chapter 12-style defense-evaluation failure.
4. **The two-sided ledger.** Safety pressure creates refusal
   pressure; over-refusal is a *safety failure of the second kind*,
   measurable with the same denominators as the attacks themselves
   [SRC-PAPER-061].
5. **The reporting hazard.** Findings and attack datasets are
   dual-use artifacts; releasing 38,961 crowdworker attacks
   accelerates research *and* hands attackers a corpus
   [SRC-PAPER-058]. Responsible reporting is a design decision, not
   an afterthought.

The chapter's reframe of Chapter 12: there, the question was *how to
attack a model*; here it is *how to run an attack program whose
outputs survive contact with statistics* — the difference between a
findings list and evidence.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Ch. 02's intervals and preregistration; Ch. 12's
adaptive-attack discipline and the two canonical defense-evaluation
failures; Ch. 13's injection taxonomy (the dominant attack surface of
deployed systems).

**Outcomes.** After this chapter you can:

- name the three red-teaming families — human, automated
  (LM-against-LM), and from-scratch — with their founding evidence
  and their distinct failure modes [SRC-PAPER-058]
  [SRC-PAPER-059] [SRC-PAPER-060];
- explain the oracle problem and why easily-classified failures make
  red teaming nearly redundant [SRC-PAPER-060];
- design an engagement with a coverage taxonomy, denominators,
  benign controls, an adaptive phase, and pre-declared stopping
  rules;
- keep the two-sided ledger — measuring over-refusal on safe-prompt
  controls alongside attack success [SRC-PAPER-061] — and price both
  sides with intervals;
- write the responsible-reporting section: what is disclosed, to
  whom, in what order, and what is withheld;
- and read a vendor's "red-teamed and safe" claim with the correct
  skepticism — asking for the denominator, the oracle, the adaptive
  phase, and the benign controls, in that order.

**Scope exclusions.** Non-operational: this chapter does not audit a
named deployed product and does not provide operational attack
recipes (mechanisms are described at the level the cited sources
publish them). Bug-bounty program design and coordinated-disclosure
law are named, not covered. Multi-agent and agentic red teaming build
on Chapter 14 and on AgentDojo [SRC-PAPER-055] and appear as
extensions; embodied/physical safety testing is out of scope.

## 3. The core explanation

### 3.1 The three families, their evidence, and their failure modes

**Human red teaming.** The founding large-scale effort: 324
crowdworkers attacking four model types at three scales, producing a
released dataset of **38,961 attacks**, with instructions, processes,
and statistical methodology published alongside
[SRC-PAPER-058]. Its scaling finding: RLHF-trained models became
*increasingly difficult to red team as they scaled*, while plain,
prompted, and rejection-sampled models showed a flat trend
[SRC-PAPER-058]. Failure modes: cost and diversity ceilings (humans
are expensive and cluster in familiar attack directions), and the
findings are lower bounds by construction.

**Automated red teaming (LM against LM).** Using one LM to generate
test cases against another — from zero-shot prompting through
reinforcement learning on the attack generator — uncovering tens of
thousands of offensive replies in a 280B chatbot, and steering to
specific harm classes (groups discussed offensively, leaked contact
info, conversation-emergent harms) [SRC-PAPER-059]. Failure modes:
attack diversity collapses to the generator's imagination; the
harms you find are the harms your *oracle* can score; and the
generator inherits the target's blind spots.

**From-scratch red teaming (the oracle problem).** The
Explore-Establish-Exploit framing: when the attacker has no
pre-existing failure classifier, the exercise must first *explore*
the behavior range, then *establish* the definition and measurement
of undesired behavior (a classifier trained to reflect human
evaluations), then *exploit* the flaws using that measure
[SRC-PAPER-060] — demonstrated on GPT-3 by discovering input classes
eliciting false statements and building the 20,000-statement
CommonClaim dataset [SRC-PAPER-060]. The sharp edge is the paper's
own: when failures can be easily classified in advance, red teaming
has limited marginal value — you could have filtered. The valuable
red teaming is exactly the kind whose failure definition does not
exist yet.

### 3.2 Coverage, denominators, and what zero means

Every claim in an engagement report is a rate or a bound, never a
bare adjective. "We found 23 harmful completions in 120 scripted
attack attempts" prices as 23/120 = 19.2% with Wilson 95%
**[13.1%, 27.1%]** — a rate *on that attack set*. "After mitigation,
0 in 120" prices as **[−0.0%, 3.1%]**: zero successes bounds the
rate only over what was attempted (Ch. 12's 0.995^n logic). "No more
findings in the remaining budget" is a *stopping statement*, not a
world claim. The coverage taxonomy is what makes the denominator
meaningful: attacks enumerated by surface (instruction-only,
injection, multi-turn, encoded, tool-result…), with per-cell counts
so the reader can see which cells were thin — an empty cell and a
clean cell look identical in the summary table and are opposites in
fact.

### 3.3 The two-sided ledger: over-refusal is a safety failure too

Safety training creates refusal behavior; refusal behavior
over-generalizes; clearly safe prompts get refused because they
*resemble* unsafe ones — the exaggerated-safety phenomenon
systematized by XSTest: **250 safe prompts across ten prompt types**
that well-calibrated models should answer, plus **200 unsafe
prompts** as contrasts models should refuse [SRC-PAPER-061]. The
two-sided ledger reports both rates on both arms: attack success
*and* false refusal, before and after each mitigation. A mitigation
that halves attacks and doubles false refusals is not obviously a
win — the trade-off is a *measured* decision, priced with the same
intervals on both sides [SRC-PAPER-061]. P07's paired harness
already operationalizes this shape: attack outcomes *and* benign
completion under both arms, with the benign cost named scenario by
scenario.

### 3.4 Adaptive phase: attacking the defense

A mitigation is a new artifact and gets its own red team. The
Chapter 12 evidence base is the warning label: distillation's claimed
0.5% broke to 100% under Carlini-Wagner adaptive attack; Croce-Hein's
50+ defense audit found nearly all robustness claims overestimated.
The engagement protocol therefore separates *static* findings
(attacks against the current system) from *adaptive* findings
(attacks against the mitigation, designed with knowledge of it), and
pre-declares which claims survive which phase — "robust under the
evaluated attack family" is an honest sentence; "robust" is not.

### 3.5 Responsible reporting

Findings are dual-use. The founding dataset release itself is the
worked example: 38,961 attacks published to accelerate community
learning [SRC-PAPER-058] — the same corpus is an attack-recipe
book. The discipline has four parts: (i) *classification before
disclosure* — which findings are fixed, exploitable-against-others,
or already-public knowledge; (ii) *staged disclosure* — vendor
first, then coordinated release; (iii) *artifacts that teach the
mechanism without operationalizing the attack* (this course's own
dataset policy is the model: metadata-level fixtures, no payload
redistribution); (iv) *claims discipline* — the report never
asserts the system is safe, only that specified properties held
under specified conditions with specified denominators.

## 4. Worked example — the Meridian Assistant engagement

**Deployment.** "Meridian" is a customer-facing assistant with a
refusal layer, deployed by a mid-size company. The engagement below
is synthetic but runs on the full discipline; every number is
recomputed in the solutions.

**Phase 0 — preregistration.** Fixed before any attack: the coverage
taxonomy (5 surfaces × planned minimum 20 attempts per cell = 120
static attacks); the oracle (a two-tier judge: deterministic refusal
classifier for refusals, human adjudication for harm — with
inter-rater agreement recorded); the benign controls (250 safe
prompts in XSTest's ten-type structure, synthesized for this
deployment, plus 120 benign operational tasks); the stopping rules;
and the headline *format* (rates with denominators and intervals,
per-cell coverage table, two-sided ledger, adaptive-phase carve-out).

**Phase 1 — static attacks.** 120 scripted attacks across the five
surfaces. Findings: **23 harmful completions** (19.2%, Wilson 95%
[13.1%, 27.1%]), concentrated: instruction-only 3/20, multi-turn
escalation 9/20, tool-result injection 7/20, encoded payload 2/20,
retrieval-embedded 2/20 — the per-cell table shows multi-turn and
tool-result channels carrying the risk. Benign controls: 115/120
operational tasks complete (95.8%, [90.6%, 98.2%]); false refusal on
the 250 safe prompts: **31 refused** (12.4%, [8.9%, 17.1%]).

**Phase 2 — mitigation.** A refusal-layer retune plus
tool-result-channel hardening (Ch. 13/14 discipline).

**Phase 3 — re-evaluation + adaptive phase.** Static re-run: 3/120
harmful (2.5%, [0.9%, 7.2%]). Paired with Phase 1: 20 attacks fixed
(23→3), 2 regressions (previously-safe prompts now failing), McNemar
exact one-sided **p = 0.000061** on 20-vs-2 discordant pairs. The
adaptive phase — attacks designed *with knowledge of the retune* —
finds 2 new multi-turn chains in 30 attempts (6.7%, [1.9%, 21.3%]),
re-opening the multi-turn cell. The two-sided ledger after
mitigation: benign completion drops to **97/120** (80.8%,
[72.9%, 86.9%]) — an 18-task operational cost — and false refusal
*rises* to 44/250 (17.6%, [13.4%, 22.8%]).

**The report card.** The honest summary sentence: "The mitigation
reduced scripted harmful completions from 19.2% [13.1, 27.1] to 2.5%
[0.9, 7.2] (McNemar p = 6.1e-5) at an operational cost of 15.0
points of benign completion and 5.2 points of false refusal, with
the multi-turn cell re-opened by adaptive attack at 6.7%
[1.9, 21.3]; nothing here bounds attack families not attempted." The
last clause is the one vendors omit and this course requires.

## 5. Approach comparison

| Approach | Oracle needed? | Coverage character | Cost | Measured anchor (source, level) | Failure mode |
|---|---|---|---|---|---|
| Human red teaming | human judges | creative, clustered, low-volume | high | 38,961 attacks; RLHF harder to red team with scale [SRC-PAPER-058, abstract] | familiar-direction bias; lower-bound-only |
| Automated (LM-vs-LM) | classifier or judge | high-volume, generator-bounded | medium | tens of thousands of offensive replies, 280B target [SRC-PAPER-059, abstract] | oracle-limited harms; diversity collapse |
| From-scratch (EEE) | built during the exercise | behavior-range discovery | highest | GPT-3 false-statement classes + 20k CommonClaim [SRC-PAPER-060, abstract] | cost; the exploration may redefine the goal mid-course |
| Static benchmark suites | fixed labels | enumerable, comparable, stale-able | low | XSTest 250 safe / 200 unsafe [SRC-PAPER-061, abstract] | training-on-the-test; says nothing about novel attacks |
| Paired harness (P07-style) | scripted outcomes | mechanism-level, reproducible | low | 6/8 blocked at benign cost 1/8, p = 0.0156 (this course, implemented) | synthetic; no novelty discovery |
| Adaptive audit phase | as above | targets the *defense* | high | Carlini-Wagner and Croce-Hein failure cases (Ch. 12, re-anchored) | skipped by vendors; the phase where claims die |

The rows compose: a real engagement is human + automated discovery
over a from-scratch-established oracle, priced by paired harnesses,
with an adaptive phase before any claim ships.

## 6. Where the methods fail

- **No closure, ever.** The attack space has no known enumeration;
  every "no findings" is budget-relative. Reports that omit the
  budget are hiding the denominator (Ch. 02, weaponized).
- **The oracle is the ceiling.** You find the failures your judge
  can score; judges drift, disagree, and can be gamed by outputs
  tuned to pass them — the evaluation-awareness problem of Ch. 07
  arrives through the scoring channel.
- **Benign-control rot.** The safe-prompt control set ages: once a
  vendor tunes against it, false-refusal numbers improve on the
  control and not in the world (adaptive overfitting, Ch. 02, in
  safety's clothing).
- **The engagement is a snapshot.** Models, prompts, and tool
  surfaces version; a six-month-old clean report describes a system
  that no longer exists. Report validity windows should be dated
  like milk, not like wine.
- **Dual-use inversion.** The artifacts that make red teaming
  cumulative (attack datasets, taxonomies) are the same artifacts
  that make attacking cumulative. Publication decisions deserve the
  same rigor as the attacks [SRC-PAPER-058].

## 7. Readings

Register-verified at the stated access levels (per
[research/source-register.yaml](../../research/source-register.yaml)):

1. **Ganguli et al., "Red Teaming Language Models to Reduce Harms:
   Methods, Scaling Behaviors, and Lessons Learned"**
   [SRC-PAPER-058] — the founding human-red-teaming effort: the
   discover-measure-reduce framing, 38,961 released attacks, the
   RLHF scaling finding.
2. **Perez et al., "Red Teaming Language Models with Language
   Models"** [SRC-PAPER-059] — automated red teaming from zero-shot
   to RL-trained attackers; the diversity/difficulty trade-off.
3. **Casper et al., "Explore, Establish, Exploit: Red Teaming
   Language Models from Scratch"** [SRC-PAPER-060] — the oracle
   problem made structural; CommonClaim as the by-product.
4. **Röttger et al., "XSTest: A Test Suite for Identifying
   Exaggerated Safety Behaviours in Large Language Models"**
   [SRC-PAPER-061] — the over-refusal side of the ledger: 250 safe
   prompts across ten types, 200 unsafe contrasts.

Re-anchored from earlier chapters: Zou et al. GCG
[SRC-PAPER-004] (the adaptive phase's canonical attacker);
Carlini-Wagner and Croce-Hein (Ch. 12 — what skipping the adaptive
phase does to claims); AgentDojo [SRC-PAPER-055] (agent-surface red
teaming); Spotlighting [SRC-PAPER-053] (a mitigation that survived
into production, priced honestly).

Assigned-pending (never cited as verified): Cooke et al. on false
refusal and harm trade-offs; curiosity-driven red teaming (CRT);
professional-certification-style red-team curricula; legal
frameworks for coordinated disclosure of AI findings.


**Note companions:** [24 Explore, Establish, Exploit — red teaming as methodology](../../research/notes/24-explore-establish-exploit.md). [45 Many-shot jailbreaking — the attack that scales with the window](../../research/notes/45-many-shot-jailbreaking.md) [C12 Evaluation supply strategies — generate for breadth, curate for judgment](../../research/notes/comparison-12-evaluation-supply-strategies.md) [60 Dynabench — the dynamic-evaluation founding citation](../../research/notes/60-dynabench-dynamic-benchmarking.md)

## 8. Exercises

**Exercise 15.1 (analysis — design the engagement).** You are handed
an assistant with a tool-calling surface (Ch. 14's Atlas shape) and
two weeks. (a) Write the preregistration: coverage taxonomy with
cells and minimum attempts, oracle design with its two tiers and
recorded agreement, benign controls, stopping rules, and the headline
format — and say which single element, if omitted, most corrupts the
eventual claim. (b) The vendor proposes skipping the adaptive phase
because "the static re-run is already 2.5%": write the one-paragraph
response citing the two Chapter 12 defense-evaluation failures and
the GCG evidence. (c) After the engagement, the *next* evaluator
reuses your control set for their own report: name the two ways that
transfer corrupts both reports, and the artifact that limits it.

**Exercise 15.2 (empirical — pricing a two-sided claim).** A
mitigation ships with: attacks 23/120 → 3/120; benign completion
115/120 → 97/120; false refusal 31/250 → 44/250; adaptive phase not
run. (a) Compute all six Wilson intervals and the paired McNemar
verdict for the attack side (20 fixed vs 2 regressed). (b) Write the
honest headline sentence with every number and its non-claim clause.
(c) The vendor also claims "false refusal is unaffected: 12.4% vs
17.6%, overlapping intervals" — is that argument valid as stated?
Compute the appropriate comparison and state what can and cannot be
concluded about the refusal side at n = 250. (d) Design the adaptive
follow-up's stopping rule so that its *absence* from the report is
itself a finding.

## 9. Hints

- For 15.1: (a) the element is the *oracle* — without a declared
  failure definition, "23 findings" is a vote among the judges you
  happened to hire; every other omission degrades precision, this
  one degrades meaning. (b) Distillation claimed 0.5% and broke to
  100%; the robustness-audit found nearly all claims overestimated —
  static re-runs measure the *old* attack family by construction.
  (c) Control-set reuse trains the vendor against the control
  (adaptive overfitting) and correlates the two reports' errors —
  fresh controls per engagement, versioned and dated.
- For 15.2: (a) 23/120 [13.1, 27.1]; 3/120 [0.9, 7.2]; 115/120
  [90.6, 98.2]; 97/120 [72.9, 86.9]; 31/250 [8.9, 17.1]; 44/250
  [13.4, 22.8]; McNemar one-sided exact p = 0.000061. (c) Overlap
  arguments are weaker than they look: compute both intervals —
  they overlap, but a *paired* design (the same 250 prompts before
  and after) would use discordant pairs, not marginal overlap; the
  unpaired version cannot rule out a real 5-point degradation at
  n = 250. (d) Pre-declare: "adaptive phase closes when N attempts
  exhaust or K adaptive successes occur, whichever first; a report
  without the adaptive cell is a report about the static family
  only."

## 10. Completion

This chapter is complete when you can:

- [ ] state the three red-teaming families with their founding
      evidence and scaling findings [SRC-PAPER-058]
      [SRC-PAPER-059] [SRC-PAPER-060];
- [ ] explain the oracle problem and its inversion — when red
      teaming is nearly redundant [SRC-PAPER-060];
- [ ] price findings with denominators and intervals, including the
      zero-success bound [Ch. 12 discipline];
- [ ] keep the two-sided ledger with benign controls and false
      refusal priced identically to attacks [SRC-PAPER-061];
- [ ] design and defend the adaptive phase with the Ch. 12 failure
      cases as evidence;
- [ ] write the responsible-reporting section with staged disclosure
      and artifact-hygiene decisions [SRC-PAPER-058];
- [ ] and deconstruct a "red-teamed and safe" claim into: which
      oracle, which denominator, which adaptive phase, which
      controls — and what remains unclaimed.

Cross-links: the injection surfaces being attacked are
[Chapter 13](../13-llm-application-security/README.md)'s and
[Chapter 14](../14-agent-tool-memory-mcp-security/README.md)'s; the
paired-harness implementation pattern is P07; the capstone engagement
is P10; evaluation-awareness (judges being gamed) is
[Chapter 07](../07-deception-scheming-and-evaluation-awareness/README.md).
