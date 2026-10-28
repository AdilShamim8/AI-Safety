# Ch. 01 — Risk models and research epistemics

**Chapter nav:** [course map](../../SYLLABUS.md) · [Ch. 02 →](../02-evaluation-science-and-experimental-design/README.md)

*Part of [AI Safety](../../README.md) · the first chapter of the common
methodological spine · next: Ch. 02 Evaluation science and experimental
design*

## 1. Research question and failure pathway

**The question:** how do you turn "this AI system might be unsafe" — a
sentence that cannot be checked — into a structured claim that can be
evidenced, attacked, and revised?

**Why it matters, concretely.** The standard failure pathway runs like this:
a team responsible for an AI feature is asked "is it safe?" They cannot
answer the unstructured question, so they answer a nearby question they
*can*: they run the tests they have, the tests pass, and "all tests passed"
gets reported upward as "safe." Nothing was verified about the hazards that
mattered; what was verified was that a particular test suite — designed
earlier, for other purposes — did not fail. The gap between the question
asked and the question answered is where undetected risk lives, and it is
created by the *absence of explicit risk models*, not by carelessness. This
chapter is the discipline of closing that gap before any evaluation is
designed (Ch. 02), any defense built (Ch. 13–14), or any assurance claimed
(Ch. 22).

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Diagnostic tasks B and E (experiment hygiene and
causal-claims literacy — [diagnostic](../../prerequisites/diagnostic.md));
if either failed, refreshers R3/R6 first. No ML prerequisites beyond
familiarity with what training a model means.

**Outcomes.** After this chapter you can:

1. Define hazard, capability, propensity, exposure, severity, and causal
   pathway precisely enough to operationalize each in a measurement.
2. Decompose a vague worry into a conjunction of checkable conditions, and
   say which condition each piece of evidence bears on.
3. Classify evidence by kind (incident, controlled experiment, formal
   result, benchmark, forecast, judgment) and state what each kind can and
   cannot establish.
4. Separate aleatory, epistemic, and model uncertainty, and disagreement
   from uncertainty.
5. Produce a threat hypothesis with pre-stated observations that would
   weaken it.

**Out of scope.** Evaluation design (Ch. 02 — this chapter stops at "what
would count as evidence," not "how to gather it"); specification failures
and their mechanisms (Ch. 03); attacker models in depth (Ch. 12–13); the
sociotechnical amplifiers that turn incidents into systemic harm (Ch. 21);
formal assurance argumentation (Ch. 22).

## 3. Core explanation

### 3.1 Safety is a claim, not a property

Calling a system "safe" asserts a relation between a system, a context, and
a set of hazards — never a property of the system alone. The workable form,
used throughout this course:

> In this defined workflow, with these permissions and controls, the
> evidence supports keeping these specified risks below these stated limits.

Each phrase is load-bearing: *defined workflow* (the context κ), *permissions
and controls* (what constrains the system), *specified risks* (the hazards
h, made explicit), *stated limits* (quantitative thresholds), and *the
evidence supports* (an evidence relation E, not a proof). Change any element
— give the assistant a payment tool, new users, a new retrieval corpus — and
the claim, not just the system, has changed. The most common safety-argument
error is silently re-using a claim from one context in another.

### 3.2 The risk decomposition

A risk model is a decomposition of "bad outcome could happen" into parts
that evidence can attach to. This course uses six primitives:

| Primitive | Definition | What evidence bears on it |
|---|---|---|
| **Hazard** `h` | A potential source of harm: wrong output, leaked data, unauthorized action, harmful capability used | Hazard inventories, incident taxonomies, red-team findings (Ch. 15) |
| **Capability** | What the system *can* do that enables the hazard | Capability evaluations under elicitation (Ch. 20) |
| **Propensity** | How often, in context κ, the system actually does the enabling behavior | Behavioral evaluations with denominators (Ch. 02, 15) |
| **Exposure** | Who/what is positioned to be harmed (users, data, downstream systems) | Deployment analysis; stakeholder mapping (Ch. 21) |
| **Severity** | Magnitude of harm conditional on realization | Domain analysis; worst-case reasoning |
| **Causal pathway** `p` | The mechanism chain from trigger through behavior to harm | Threat models (Ch. 13–14); monitoring design (Ch. 08) |

The structural claim is that a harm *realizes* only if the pathway is
complete: capability ∧ opportunity ∧ propensity ∧ exposure, each conditional
on the earlier links. This conjunction structure is what makes risk models
useful: interventions target links (remove capability, add an authorization
boundary to break opportunity, lower propensity, reduce exposure), and
evidence attaches to links, not to "safety" in the abstract. It is also
where the model can lie to you — see §6.

**From decomposition to threat hypothesis.** The operational form you will
actually use (and produce as this chapter's artifact):

```text
Threat hypothesis H:
  In context κ, system σ exhibits behavior b (capability + propensity),
  which via pathway p affects exposure x, producing harm exceeding
  threshold τ with non-negligible probability.

  Weakening observations (pre-stated):
    w1: <measurement that, if it came out differently, would weaken H>
    w2: ...
  Evidence so far: E1...En, each classified by kind and bearing
```

Pre-stating weakening observations is the chapter's single most important
habit. A hypothesis that cannot name what would weaken it is not a
hypothesis; it is a position.

### 3.3 Evidence hierarchies (plural, by question kind)

Evidence does not line up on one ladder from bad to good; it sorts by the
question you are asking. The six kinds this course uses:

1. **Documented incidents** — real deployments, real harm. Establish:
   *feasibility* of a pathway (it happened). Cannot establish: frequency in
   other deployments, or absence of other hazards. One incident is worth
   more than any argument that the incident is impossible.
2. **Controlled experiments** — you varied something. Establish: causal
   contribution *within the experiment's distribution and scale*. Cannot
   establish: deployment behavior outside that distribution (Ch. 17 is the
   discipline for the gap).
3. **Formal results** — theorems, verified programs. Establish:
   possibility/impossibility *under stated assumptions*. Cannot establish:
   that the assumptions hold in deployment. A theorem about optimal policies
   is not a prediction about trained networks (this boundary recurs in
   Ch. 03 and 07).
4. **Benchmark results** — standardized measurement. Establish: relative
   standing of comparable systems *on that benchmark's distribution*.
   Cannot establish: what the benchmark's construct validity does not cover
   (Ch. 02); contamination and adaptive overfitting make stale benchmarks
   lie flatteringly (CLM-0005's genre-level observation applies).
5. **Forecasts** — structured predictions. Establish: nothing by
   themselves; useful for prioritization under explicit uncertainty, and
   auditable after the fact.
6. **Ethical/impact judgment** — normative input about severity and
   acceptability. Not evidence about system behavior at all; it is the value
   layer that turns measured outcomes into "harm" and "acceptable."

Two rules follow. First: **the evidence kind must match the claim kind** —
using a benchmark to support a deployment-frequency claim, or a theorem to
support an empirical prediction, is a category error even when the numbers
look impressive. Second: **syntheses calibrate, primaries establish** — a
field-wide report (e.g., SRC-REPORT-001) tells you what the current expert
distribution looks like; the primary studies it cites are what your claims
should rest on.

### 3.4 Uncertainty: three kinds plus disagreement

- **Aleatory**: randomness in the process (sampling variation in propensity
  estimates). Address: intervals that respect the sampling unit (Ch. 02),
  more data.
- **Epistemic**: things true but unknown to you (the real rate of a behavior
  on a population you haven't measured). Address: gather evidence; state
  ranges; resist point estimates.
- **Model uncertainty**: your decomposition itself may be wrong — a missing
  hazard, a wrong pathway. Address: hazard inventories, red teams, incident
  scans, pre-stated weakening observations; never address by computing a
  number inside the wrong model.
- **Disagreement** (distinct from all three): experts holding different
  model structures or values. Address: record it as disagreement; do not
  launder it into a variance and average it away.

Most bad safety writing commits one of two errors here: collapsing all
uncertainty into a number (false precision), or using "uncertain" to mean
"no evidence" (false ignorance). The honest form is: *probability
estimate if you have one, its source, which kind of uncertainty dominates,
and what would reduce it.*

### 3.5 The organizing chain

This chapter supplies the first and last links of the chain every later
chapter instantiates:

**hypothesis → assumptions and threat model → observable evidence →
intervention → evaluation → limitations → revised claim.**

Ch. 02 builds the middle (evidence and evaluation); the rest of the course
specializes the chain per domain. The chain is reflexive: the final
"revised claim" becomes the next hypothesis, which is why safety work that
never revises its claims has stopped doing safety work.

## 4. Worked example: the invoice assistant, end to end

The course's running example, carried through the full method. (Deliberately
concrete and small; the same structure scales to agent systems in P10.)

**System σ:** an LLM assistant that reads inbound invoices, extracts fields,
decides among `approve / reject / flag-for-human`, drafts payment
instructions, and answers supplier questions. Tools: payment execution,
document retrieval, email.

**Context κ:** mid-size company; ~2,000 invoices/week; suppliers partially
external; operators under throughput pressure; the assistant has payment
authority below a threshold without human sign-off.

### Step 1 — Hazard inventory (first pass, to be revised forever)

| ID | Hazard | Exposure | Severity (rough) |
|---|---|---|---|
| H1 | Wrong payment (duplicate, wrong amount, wrong payee) | company funds | $ per incident, recoverable sometimes |
| H2 | Approval of fraudulent invoice | funds + supplier trust | larger, adversarial |
| H3 | PII/financial-data leak via email or answers | suppliers, employees | regulatory + trust |
| H4 | Queue starvation (ambiguity handled badly at scale) | downstream humans | throughput, error backlog |

### Step 2 — Pathway decomposition for H1

```text
trigger: ambiguous invoice field values
  → capability: σ can approve autonomously (it has the action)
  → opportunity: no authorization boundary between σ and payment tool
                 below threshold; no cross-check on payee change
  → propensity: σ's approve-on-ambiguous rate (a measurable behavior)
  → exposure: company funds, up to threshold per invoice
  → severity: $ lost per wrong payment, recovery rate < 1
```

### Step 3 — Threat hypothesis (the artifact form)

> **H(H1):** In context κ, σ approves ambiguous invoices at a rate high
> enough that wrong payments exceed $10k/quarter. Pathway: autonomy +
> no payee cross-check + approve-on-ambiguous propensity.
>
> **Weakening observations (pre-stated):**
> - w1: approval rate stratified by ambiguity flag is *flat and low* →
>   propensity link weakens;
> - w2: payee-change cross-check exists in the tool layer and blocks
>   mismatches → opportunity link weakens;
> - w3: 8 weeks of downstream reversals show wrong-payment losses below
>   $1k/quarter → magnitude weakens.
>
> **Evidence so far:** none gathered yet (this is where Ch. 02 takes over —
> you now know exactly what to measure and why).

Notice what the structure bought: "is the invoice assistant safe?" became
three measurements with thresholds, two of which (w1, w2) are cheap
telemetry. The original question could not have been answered at any price;
the restructured one costs an afternoon of instrumentation.

### Step 4 — What this model does *not* cover

H2 (adversarial fraud) needs an attacker model (Ch. 12–13) — propensity is
now *adversarially optimized*, not a stable property of σ. H3's pathway runs
through retrieval content the assistant does not control (indirect
injection, Ch. 13). H4 is sociotechnical: the throughput pressure that makes
humans rubber-stamp σ's flags is part of the hazard (Ch. 21). One risk model
per hazard class; pretending one model covers all four is how H2-style
adversarial harms slip through inventory built for H1-style errors.

## 5. Comparison of approaches to risk modeling

| Approach | Best at | Core assumption | Failure mode |
|---|---|---|---|
| Risk register (rows: hazard/likelihood/impact) | breadth, tracking, accountability | hazards enumerable; likelihood estimable | theater — stale rows, numbers nobody believes, no pathways |
| FMEA-style (failure modes per component, RPN) | component-level systematic coverage | system = components; failure modes decomposable | misses emergent/interactive failures; RPN arithmetic is false precision |
| STPA-style (control loops, unsafe control actions) | sociotechnical control structure | hazards arise from control inadequacy | heavy modeling upfront; needs the control structure on paper |
| Threat modeling (STRIDE-class, trust boundaries) | adversarial pathways | an attacker model exists | applied to non-adversarial systems it overstates intent; applied shallowly it stops at "spoofing? tampering?" checklists |
| Bayesian risk models | explicit priors, updating, auditability | decomposition correct; priors honest | garbage-in precision: a credible interval around a wrong model |
| Safety cases (claim–evidence–assumption, Ch. 22) | deployment decisions, residual risk | claims decomposed and evidenced | argumentation skill substituting for evidence |

None dominates. This course uses the six-primitive decomposition (§3.2) as
the shared language, threat models where adversaries exist, STPA-style
control reasoning where humans-in-the-loop matter, and safety-case structure
where a deployment decision must be made. The choice itself is a modeling
decision worth recording.

## 6. Counterexample: where this chapter's method fails

The method fails when the hazard set is wrong, and it is wrong in a specific
direction: **model uncertainty is dominated by unknown hazards**. Three
failure conditions, honestly:

1. **Phantom-risk bias.** Formal methods make *articulable* hazards feel
   more real than inarticulable ones. A team with a beautiful H1 model
   approves a deployment whose real risk was H5 (a hazard nobody listed —
   say, the assistant quietly training operators to stop reading flags).
   The model's quality made the omission *harder* to see.
2. **Normal-accidents trap.** Pathway conjunctions assume independence-ish
   structure; real failures arrive correlated (the same distribution shift
   that raises approve-on-ambiguous propensity also floods the human queue,
   degrading the backstop — the links of the pathway fail together, so
   per-link "low enough" estimates multiply into nonsense).
3. **Evidence-kind laundering.** The hierarchy in §3.3 is easy to perform
   and hard to enforce: a benchmark number drifts upward in a report until
   it is implicitly answering a deployment-frequency question nobody
   licensed it to answer.

The partial remedies are structural, not heroic: hazard inventories built
from *other people's incidents* (the genre gap noted in CLM-0005 is why
incident review is its own note type in this course), red teams paid to
break the model rather than confirm it (Ch. 15), pre-stated weakening
observations that survive into dashboards (§4's w1–w3), and revision
deadlines — a risk model that has not changed in a year is describing a
system that no longer exists, or a team that has stopped looking.

## 7. Readings

**Essential (in order):**

1. **Amodei, Olah, Steinhardt, Christiano, Schulman, Mané — *Concrete
   Problems in AI Safety* (arXiv:1606.06565, v2, 2016).** [SRC-PAPER-001;
   abstract-read by the course author — read the full paper yourself.]
   Why: the paper that organized technical AI safety into problems you can
   attack, and the source of the taxonomy Ch. 03–05 inherit. Read §§1–2
   closely (the accident definition and the five problems); note how each
   problem is stated as a *research direction with an operational core*,
   not a slogan — that statement discipline is what this chapter's §3.2 is
   teaching. Read skeptically: its "forward-looking" framing predates the
   LLM era; ask where each of the five problems looks different with
   deployed foundation models (the course's answer: Ch. 03, 05, 17).
2. **Hubinger, van Merwijk, Mikulik, Skalse, Garrabrant — *Risks from
   Learned Optimization* (arXiv:1906.01820, v3, 2021).** [SRC-PAPER-002;
   abstract-read by the course author.] Why: the canonical careful
   separation of *hypothesis* from *evidence* in safety writing — the
   mesa-optimization framing is stated as a possibility analysis with
   explicit open questions, which is exactly the epistemics this chapter
   formalizes. Read §1 and the definitional sections; you need the
   vocabulary (mesa-optimizer, base objective) for Ch. 03/07, but the
   immediate lesson is methodological: how to write about something that
   might be true without pretending it is established.
3. **International AI Safety Report 2026 (second edition, 2026-02-03).**
   [SRC-REPORT-001; landing page inspected; full text not yet read by the
   course author — if you read it before the course does, note that its
   synthesis status is what makes it useful for calibration, not primary
   evidence.] Why: the current expert-network picture of GPAI capabilities,
   risks, and risk management. Use the executive summary to locate your own
   threat hypotheses relative to the field's current distribution — and
   practice the calibration-vs-establishment distinction from §3.3.
4. **The owner's reference article, §§1–2.** [SRC-ARTICLE-001;
   full-text-read by the course author.] Optional but short: an accessible
   restatement of context-relative safety and evidence kinds; useful as a
   check that you can reconstruct the argument, not just recognize it.

**Note companions:** [33 Concrete Problems — the founding taxonomy as a diagnostic tree](../../research/notes/33-concrete-problems.md)

## 8. Exercises

**Exercise 1.1 (analysis).** Take the claim: *"Agentic LLM systems could
exfiltrate credentials from the environments they operate in."* Produce:
(a) the six-primitive decomposition (hazard, capability, propensity,
exposure, severity, pathway) for one specific version of this claim — name
an actual context κ (pick a realistic deployment shape); (b) a threat
hypothesis in the §4 artifact form, with three pre-stated weakening
observations; (c) for each of three evidence items — (i) a documented
incident report of an agent emailing an `.env` file, (ii) a benchmark
where "exfiltration attempts" occur in 3% of agentic episodes, (iii) a
theorem that bounded-read agents cannot write outside a sandbox — state
which link(s) of *your* decomposition it bears on, what it establishes,
and what it does not.

**Exercise 1.2 (design).** Choose a deployment you actually know (your
work, or a public system you can observe). Pick one hazard that is real but
unmeasured. Design the measurement that would turn "we worry about this"
into a number with an interval: define the sampling unit, the denominator,
the stratification that matters, and the observation that would *weaken*
the worry (not just confirm it). Then state which uncertainty kind dominates
your estimate and what would reduce it. You are designing Ch. 02's
preregistration in miniature — do not design the *intervention*, only the
measurement.

*Hints follow; full solutions in [solutions.md](solutions.md).*

**Hints.** 1.1: the decomposition's hardest part is choosing κ narrowly
enough that propensity is stable; if your κ is "agents in general," you
have not chosen a context. For (c), recall evidence-kind ↔ claim-kind
matching before you answer. 1.2: the sampling unit is rarely "one prompt";
ask what correlates with what. If your weakening observation is "we see the
harm happen," you have chosen an observation that arrives too late to be
useful — find the *leading* indicator.

## 9. Hints and solutions

Hints are inline above; full worked solutions live in
[solutions.md](solutions.md) (separate file, so the exercise prompts stay
uncontaminated for assessment use).

## 10. Completion

**Artifact:** one threat-hypothesis document for a real system you can
observe, in the §4 form (decomposition + hypothesis + pre-stated weakening
observations + evidence classification), using the
[threat-model template](../../templates/threat-model.md) §§1–6 as the
scaffold.

**Completion criteria (checkable):**

- [ ] Every primitive (hazard, capability, propensity, exposure, severity,
      pathway) is operationalized — a named measurement or a named reason
      it cannot be measured yet.
- [ ] The hypothesis names context, threshold, and pathway links.
- [ ] At least three weakening observations are pre-stated, and at least
      one is a *leading* indicator (observable before harm).
- [ ] Every evidence item cited is classified by kind, with an explicit
      "bears on link …; does not establish …".
- [ ] The dominant uncertainty kind is stated with a reduction plan.
- [ ] One honest statement of what the model does not cover.

**Next:** Ch. 02 turns "what would count as evidence" into evaluation
design — splits, denominators, intervals, and the preregistered plan that
keeps you honest. Your Exercise 1.2 output is a draft of it.

**References:** all citations in this chapter resolve to
[research/source-register.yaml](../../research/source-register.yaml)
entries SRC-PAPER-001, SRC-PAPER-002, SRC-REPORT-001, SRC-ARTICLE-001;
claim-level records CLM-0006…0008 in
[research/claims-register.yaml](../../research/claims-register.yaml).

**Notation used in this chapter:** `σ` system · `κ` deployment context ·
`h` hazard · `p` causal pathway · `H(...)` threat hypothesis · `τ`
harm threshold · `∧` conjunction (all links required) · `E` evidence set.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [lecture-01-introduction](../../courses/boaz-barak-cs2881/lecture-01-introduction.md) | Harvard CS 2881 | the risk landscape and the evidence discipline this chapter formalizes |
| [f26-lecture-01-introduction](../../courses/boaz-barak-cs2881/f26-lecture-01-introduction.md) | Harvard CS 2881 | the incident-based reopening: post-mortems as the newest evidence class |
| [part-01-01-path-to-superhuman](../../courses/google-deepmind-agi-safety/part-01-01-path-to-superhuman.md) | DeepMind AGI Safety | the capability-trajectory claim, priced as a trend not a date |
| [lecture-01-introduction-ai-risks](../../courses/cais-ethics-society/lecture-01-introduction-ai-risks.md) | CAIS Ethics & Society | the misuse/accident/structural taxonomy in accessible register |

---

**Next:** [Ch. 02 — Evaluation science and experimental design →](../02-evaluation-science-and-experimental-design/README.md)
