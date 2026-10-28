# Chapter 24 — Research practice and capstone execution

**Chapter nav:** [← Ch. 23](../23-governance-and-standards/README.md) · [course map](../../SYLLABUS.md) · [course complete — pick a route →](../../ROADMAP.md)

| | |
|---|---|
| **Chapter** | 24 — Research practice and capstone execution: scoping a question until it is falsifiable, baselines that can win, preregistration, ablations, the benchmark lottery, negative results, and ethical release — the course's methodology, assembled into the capstone |
| **Questions** | You now hold every instrument in the book — measurement, intervals, paired tests, monitors, safety cases, standards maps. What does it take to turn them into *research*: a question whose answer could embarrass you, a design that decides before the data does, an analysis that ablates your own favorite mechanism, and a release that does not dump harm on the way out? |
| **Hard prerequisites** | [Chapter 02 — evaluation science](../02-evaluation-science-and-experimental-design/README.md) (the whole discipline); [Chapter 22 — safety engineering and assurance](../22-safety-engineering-and-assurance/README.md) (the argument form the capstone reports) |
| **Core artifact** | Research proposal + capstone report: a preregistered, powered, ablated, honestly-negative-where-it-is-negative study with an ethical-release section — the course's P10 |
| **Projects** | **P10 (capstone assurance dossier) is this chapter** — everything before it feeds here |
| **Readings** | Section 7 — three newly register-verified sources plus the course's own re-anchored methodology |

## 1. Research question and failure pathway

The capstone's failure pathway — the five ways a "study" produces a
sentence nobody should believe:

1. **The benchmark lottery decides, not the method.** The overall
   fragility of ML benchmarking: many factors other than fundamental
   algorithmic superiority may lead to a method being perceived as
   superior; relative performance can be altered significantly
   simply by choosing a different benchmark setup [SRC-PAPER-105].
   The chapter's own arithmetic (§4): with a 2-point true gap and
   n = 100, the *worse* system ranks first 40.8% of the time — a
   leaderboard is a lottery ticket unless the gap and n are stated.
2. **The benchmarks themselves are broken.** Popular commonsense
   MCQ benchmarks carry validity issues ranging from
   ungrammaticality and typos to misleading prompts and *equally
   correct options* — the HellaSwag case study documents the pattern
   [SRC-PAPER-106]. Your instrument may be measuring its own damage.
3. **Negative results are unpublished, so the field flies blind.**
   Predictive performance on selected problems is not a good
   indicator of a publication's worth; using it as such fosters
   inefficiency and wrong incentives — the call is to publish
   negative results to improve the community's scientific output
   [SRC-PAPER-107]. A capstone that only reports its wins is the
   failure mode in miniature.
4. **The design cannot embarrass the hypothesis.** An unfalsifiable
   study — no pre-stated decision rule, no power statement, no
   baselines that could win, analyses chosen after seeing the data —
   produces confirmation, not knowledge (Ch. 02's discipline, now
   the whole game).
5. **The release dumps harm on the way out.** Data with PII, probes
   that teach the attack, model weights whose license chain is
   broken (Ch. 16's fuses), results whose naming-and-shaming invites
   harassment — release is a safety decision (Ch. 22's form), not a
   button.

The chapter's reframe: the capstone is not "a project about AI
safety" — it is *research practice that is itself safe*: falsifiable,
powered, ablated, negative-honest, and released with the same hazard
analysis any deployed system gets.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 02 (everything); Chapter 22 (the report
inherits the safety-case form). The from-scratch track's three
preregistered protocol templates are the working scaffolding.

**Outcomes.** After this chapter you can:

- scope a question to a falsifiable, powered, preregisterable form;
- choose baselines that can win and state the stopping rules;
- design the ablation grid that attacks your own mechanism;
- quantify benchmark-lottery risk in your result's own numbers
  [SRC-PAPER-105];
- audit a benchmark for validity issues before trusting it
  [SRC-PAPER-106];
- commit to negative-result publication and write it well
  [SRC-PAPER-107];
- and run the ethical-release review (data, probes, weights,
  people).

**Scope exclusions.** This chapter does not teach statistics from
scratch (Ch. 02 did), does not cover ML conference submission
mechanics, and does not operationalize any harmful-content release —
the ethical-release section is a *review checklist*, and its
harmful-content rows stay at category level exactly as every chapter
before this one.

## 3. The core explanation

### 3.1 Scoping: the falsifiability bar

A research question is scoped when: (i) the claim is stated in
context form (population, intervention, comparator, outcome); (ii) a
*pre-stated decision rule* exists — the numbers that would count for
and against; (iii) the rule could fire *against* you (if no result
would embarrass the hypothesis, it is not a hypothesis); (iv) the
power statement is honest (what n buys what detectable effect). The
course's template: H1/H2 with disconfirming criteria and stopping
rules — the discipline the from-scratch track's protocol templates
operationalized.

### 3.2 Baselines that can win

The baseline's job is to be *able to win*: a strawman baseline
confirms nothing. The selection rule: include the strongest cheap
baseline (trivial heuristics), the strongest prior-method baseline
(the literature's best at your budget), and the *ablated-self*
baseline (your mechanism minus your contribution). Every result
table has all three, and the paper's story survives the ablated-self
row beating full-self (that is a negative result, and §3.5 says what
to do with it).

### 3.3 The lottery arithmetic, in your own numbers

[SRC-PAPER-105]'s fragility claim, made computable: for two systems
with true rates p₁ and p₂ measured on n items each, the probability
the worse one ranks first is a normal-approximation away — and at
realistic leaderboard n's and gaps it is *shockingly large* (§4's
table: 40.8% at 2 points and n = 100). The practice: every
comparison in the capstone report carries its gap, its n, its flip
probability — or it does not carry a rank claim at all. And before
trusting the instrument itself: the validity audit [SRC-PAPER-106]
— sample items, look for the documented issue classes (typos,
misleading prompts, equally correct options), and report what you
found with the same honesty you'd demand of a dataset card.

### 3.4 Preregistration and the ablation grid

Preregistration commits the design before the data: hypotheses,
arms, denominators, decision thresholds, analysis choice, stopping
rule — timestamped (a commit hash is a fine timestamp; this course's
registers are the pattern). The ablation grid then attacks the
mechanism *systematically*: every load-bearing component removed in
turn, the performance ledger reported per removal. The grid's
discipline is the safety-case discipline turned inward: your
mechanism is the claim, the ablations are the defeaters, the ledger
is the evidence table.

### 3.5 Negative results, written well

The position paper's argument [SRC-PAPER-107]: predictive
performance alone is a bad worth-indicator, and the missing negative
results leave the community re-running dead ends. The capstone's
commitment: whatever the result, the *report* ships — a negative
result written well states the design's power (what effect it could
have detected), the exact point estimates with intervals, the
ablation ledger, and the honest scope ("we failed to detect an
effect of size X at n = Y; effects smaller than Z remain possible") —
which is *more* useful to the field than a marginal win.

### 3.6 Ethical release

The release review, in the safety-case form: claims (this artifact
is safe to release), evidence (PII scan results; license lineage
per Ch. 16; harmful-content categorization; attack-operability
assessment of any probe), defeaters (the probe that teaches the
attack; the weights whose fuse blows at distribution), residual risk
named. People are part of the release: participant consent, the
naming-and-shaming question for model/system identities, the
vulnerability-disclosure route for anything that qualifies
(SECURITY.md's route).

## 4. Worked example — the capstone proposal, in miniature

The proposal (P10's form, compressed), with every number recomputed
2026-10-23:

**Question (scoped).** Does a provenance-spotlighting preprocessing
step reduce injection-attack success in a RAG pipeline without
degrading answer quality? — context form: population = the course's
synthetic injection scenarios; intervention = spotlighting transform
on; comparator = transform off; outcome = attack success rate +
answer-quality proxy.

**Hypotheses and decision rules (preregistered).** H1: spotlighting
reduces ASR by ≥ 10 points; H2: answer-quality degradation ≤ 3
points. Decision rule: H1 supported only if the *paired* interval on
the difference excludes 0 and the point estimate clears 10 points;
H2 fails the deployment if quality's interval includes −5.

**Power statement.** Detecting 0.30 vs 0.20 (a 10-point ASR
difference) at 80% power, α = 0.05 two-sided: **n = 295 per arm**
(pooled-variance two-proportion arithmetic) — the design sets n =
300 per arm and says so *before* collecting.

**Baselines.** (i) Trivial: refuse-on-keyword (must be reported even
though it will lose on quality); (ii) prior method: the delimiter
convention; (iii) ablated-self: spotlighting without the
provenance-marking step (the mechanism's own contribution removed).

**Lottery statement (the report's own numbers).** At the achieved
n = 300/arm and a 2-point true gap between any two compared
conditions, the worse one ranks first with probability 25.4% (the
§3.3 arithmetic) — so the report draws no sub-5-point rank
conclusions at this n, in those words.

**Ablation grid.** Spotlighting minus marking; minus encoding; minus
delimiters — the ledger row per removal, with intervals.

**Negative-result commitment.** Pre-stated: if H1's interval
includes 0, the report ships as a negative result with the power
statement and the "effects smaller than X remain possible" sentence.

**Ethical-release section.** PII scan (the synthetic corpus's
discipline); no attack operational detail beyond category level
(every chapter's rule); license lineage for any reused artifact (the
dataset cards' authority); the probe-teaching defeater answered by
the disclosure route.

## 5. Approach comparison

| Practice | Question answered | Strength | Failure it prevents | Cost |
|---|---|---|---|---|
| Preregistration (H1/H2 + rules) | Was the design decided before the data? | kills HARKing | confirmation theater | discipline |
| Power statement (n = 295/arm) | What effect could this detect? | honest ceilings | underpowered certainty | arithmetic |
| Lottery statement (flip probability) | Is the rank real? | gap × n honesty | leaderboard luck [SRC-PAPER-105] | one approximation |
| Benchmark validity audit | Is the instrument broken? | catches instrument damage [SRC-PAPER-106] | measuring typos | sampling labor |
| Ablation grid | Which component carries the effect? | mechanism evidence | story-driven attribution | k re-runs |
| Negative-result shipping | What did we learn by failing? | field-level correction [SRC-PAPER-107] | survivorship bias | courage |
| Ethical-release review | Is the artifact safe to publish? | safety-case form | harm dump | review labor |

## 6. Where the methods fail

- **Preregistration can be gamed by vague thresholds** — the rules
  must be numeric and pre-committed, or they are decoration.
- **Power statements age with the effect size** — a design powered
  for 10 points says nothing about 4-point effects, and the report
  must say which it is.
- **The lottery statement is per-comparison** — a report with 40
  pairwise comparisons has 40 flip probabilities; multiplicity is
  the unstated lottery multiplier.
- **Validity audits sample** — [SRC-PAPER-106]'s issue classes
  surface in samples; absence in your sample is not absence in the
  instrument.
- **Negative results need venues** — the position paper's own point:
  the publication system must want them [SRC-PAPER-107]; a capstone
  can model the behavior, not fix the incentives.
- **Release reviews miss people** — the PII/license/probe rows are
  the easy part; the naming-and-shaming and disclosure-route rows
  are where releases actually hurt.

## 7. Readings

**Verified for this chapter (2026-10-23):**

- Dehghani, Tay, Gritsenko, Zhao, Houlsby, +3 — *The Benchmark
  Lottery*, arXiv:2107.07002 [SRC-PAPER-105; CLM-0161]. Benchmarking
  fragility; non-superiority factors winning.
- Chizhov, Changalidis, Vijaya Kumar, Detrois, Nee, +2 — *Who
  Benchmarks the Benchmarks?*, arXiv:2504.07825 [SRC-PAPER-106;
  CLM-0162]. The HellaSwag validity case study.
- Karl, Kemeter, Dax, Sierak — *Position: Embracing Negative
  Results in Machine Learning*, arXiv:2406.03980 [SRC-PAPER-107;
  CLM-0163]. The negative-results call.

**Re-anchored from the course itself:** Chapter 02's full discipline
(power, preregistration, paired ledgers); the from-scratch track's
three preregistered protocol templates; Chapter 16's license
lineage; Chapter 22's safety-case form; the dataset cards' honesty
pattern; the wilson_interval machinery that recomputed every number
in this book.

**Note companions:** [24 Explore-Establish-Exploit — the research methodology](../../research/notes/24-explore-establish-exploit.md)

## 8. Exercises

**Exercise 24.1 — scoping drill (analysis).** Take three vague
questions ("is my model safe?", "does CoT help?", "is X better than
Y?") and scope each to context form + numeric decision rule + a
result that would embarrass the hypothesis. State for each what the
unscoped version silently protects.

**Exercise 24.2 — the lottery, computed (statistics).** (a) Derive
the two-proportion power arithmetic behind n = 295/arm for 0.30 vs
0.20 at 80%/0.05. (b) Compute the flip probability for a 3-point
true gap at n = 400/arm (normal approximation, continuity
correction). (c) A report compares 6 systems pairwise — state the
multiplicity problem in flip-probability terms and the correction
you demand before accepting any single "winner."

**Exercise 24.3 — negative-result writing (composition).** A study
finds ASR 22.4% (treatment) vs 24.1% (control), n = 300/arm,
paired interval including 0. Write the 250-word results section of
the *honest* negative-result report: the design's detectable effect,
the point estimates with intervals, the ablation ledger's fate, the
"effects smaller than X remain possible" sentence, and why this
report is useful.

**Exercise 24.4 — the capstone proposal (the chapter assessment).**
Write the complete proposal for your P10 study: scoped question,
preregistered H1/H2 with numeric rules, power statement with the
arithmetic shown, the three baseline classes, the lottery statement
at your planned n, the ablation grid, the negative-result
commitment, and the ethical-release review in safety-case form —
800-1,200 words. The proposal must contain at least one statement
that could embarrass its author.

## 9. Hints

- 24.1: "safe" cannot be embarrassed; "reduces ASR by ≥ 10 points"
  can be.
- 24.2(b): the flip probability needs both variances — the worse
  system's and the better one's.
- 24.3: the power statement *prevents* the dishonest reading "no
  effect"; the report's job is to make that reading impossible.
- 24.4: if nothing in your proposal could embarrass you, you have
  written a plan, not a study.

## 10. Completion

This chapter — and the course — is complete when you can:

- [ ] scope questions to falsifiable, powered, preregisterable form;
- [ ] run baselines that can win and report the ones that do;
- [ ] quantify the benchmark lottery in your own comparisons
      [SRC-PAPER-105] and audit your instruments [SRC-PAPER-106];
- [ ] ablate your own mechanism and report the ledger;
- [ ] ship negative results written to be useful [SRC-PAPER-107];
- [ ] and release ethically — the safety-case form applied to
      publishing itself;
- [ ] and assemble all of it into the capstone: a study that is
      itself an instance of the safety it studies.

Cross-links: the measurement discipline is
[Chapter 02](../02-evaluation-science-and-experimental-design/README.md)'s;
the protocol templates are the from-scratch track's; the release
hazard analysis is
[Chapter 16](../16-privacy-provenance-and-supply-chains/README.md)'s
and [Chapter 22](../22-safety-engineering-and-assurance/README.md)'s;
the report form is the safety case's; and the whole book's registers
— 150+ sources, every claim dated and access-level-honest — are the
pattern your capstone's evidence table inherits.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [f26-oral-presentations](../../courses/boaz-barak-cs2881/f26-oral-presentations.md) | Harvard CS 2881 | the defended-capstone model this chapter's project follows |
| [pedagogy](../../courses/boaz-barak-cs2881/pedagogy.md) | Harvard CS 2881 | how a working research seminar runs its evidence discipline |
| [lecture-04-safety-engineering](../../courses/cais-ethics-society/lecture-04-safety-engineering.md) | CAIS Ethics & Society | the incident-reporting culture as research practice |

---

**Course complete.** [Pick your route →](../../ROADMAP.md) or [watch the lecture library →](../../courses/README.md).
