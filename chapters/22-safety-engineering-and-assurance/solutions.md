# Chapter 22 — Solutions and rubrics

## Exercise 22.1 — defeater-first drafting

**Full-credit solution.**

Five strongest defeaters against C1 ("the policy stack blocks the
attack classes in the paired trials"):

1. **Transfer defeater (strongest):** the 8-scenario set measures
   the *fixture*, not the world — blocked-rate 6/8 [40.9%, 92.9%]
   is a statement about the scenario set; deployment attack
   frequency and shape are unmeasured. *Not rebuttable with current
   evidence* → accepted into residual risk with the explicit
   statement: "the rate bounds the scenario set only; the
   real-world denominator does not exist."
2. **Adaptive adversary:** the trials pin the adversary at the
   fixture's attack scripts; a real adversary iterates against the
   policy (Ch. 12/15's canon). *Partially rebuttable*: re-run trials
   with an adaptive arm (red-team free to probe the policy), report
   post-adaptation blocking; without that arm, accepted with the
   "static-evaluation overestimate" caveat.
3. **Known-gap scenarios:** Ch. 14 documents two on-purpose residuals
   (authored-policy gap; consent decay) that the fixture *includes
   and expects unblocked* — C1's own evidence contains its
   exceptions. *Accepted by design*, but the safety case must name
   them in residual risk, not average them away.
4. **Component drift:** agent_guard's matrix and policy are code —
   the deployment's policy configuration can drift from the tested
   revision. *Rebuttable* with revision pinning + a CI gate that
   re-runs the paired trials on every policy change (the re-audit
   trigger section).
5. **Consent-path gaming:** R1/R4 are consent-gated (Ch. 14); a
   social-engineering adversary targets the *human* consent step,
   which the paired trials script, not test. *Accepted*: the
   scenario set's consent model is scripted consent, real consent is
   an open hole, stated.

**Rubric.** Five defeaters, ranked or at least transfer-first (3);
each classified with the evidence that would rebut it (4); the
accepted ones stated as residual-risk language, not softened (3).

## Exercise 22.2 — the linking argument

**Full-credit solution.**

*System-level requirement (SR1):* "No exfiltration of regulated data
from the pipeline via the agent."

*Deductive bridge (ISCaP-style [SRC-PAPER-102]):*
SR1 holds if (a) every exfiltration-capable action passes the policy
stack, AND (b) the policy blocks all exfiltration-class actions it
sees, AND (c) the deployment's action space is the audited action
space.

- (a) → *component claim CC1:* the privilege matrix covers all
  store-writers and outbound channels (Ch. 14's atlas: 15 tools,
  exfiltration pairs enumerated — E1-adjacent evidence: the matrix
  audit itself).
- (b) → *component claim CC2:* agent_guard's paired trials — 6/8
  blocked, p = 0.015625 (E1).
- (c) → *environment assumption A1:* the tool registry at deployment
  equals the audited registry (evidenced by: registry pinning +
  the CI matrix-vs-registry consistency check; honestly open for
  tools added post-audit).

*The assumptions the bridge needs, surfaced:* (i) the fixture's
attack scripts represent the exfiltration *class* (representativeness
— open, priced in residual risk); (ii) the adversary does not
disable the policy (integrity assumption — evidenced by deployment
architecture, honestly architectural); (iii) consent-gated channels
are the residual (named). Each arrow in the bridge is now either
evidence-cited, architecture-cited, or honestly open — the ISCaP
discipline of never letting an assumption hide inside "therefore."

**Rubric.** System requirement stated (1); the three-part deductive
structure with component claims (4); assumptions surfaced and each
evidence-cited or marked open (5).

## Exercise 22.3 — evidence confidence rating

**Full-credit solution.**

| Evidence | Measured | Population | Interval | Validity window | Transfer distance |
|---|---|---|---|---|---|
| E1 (trials) | attack-scenario blocking | 8 scripted scenarios, fixed adversary | [40.9%, 92.9%] | pinned revision; indefinite until code/policy change (trigger set) | far — scenario set → world |
| E2 (utility) | benign-path cost | 8 benign scenarios | [2.2%, 47.1%] | same | far, same direction |
| E3 (monitor) | probe-visible detection under defense | 200 probe tasks | [18.2%, 29.8%] | model revision; re-run per release | moderate — probe → misbehavior classes |
| E4 (flip) | oversight-conditional compliance | 200 matched probe pairs | point 0.335, p = 6.8e-17 | same | moderate — measures the model class, not the deployment |

*The limiting item:* E1 — its interval's width ([40.9%, 92.9%])
means the top claim's control-efficacy leg is supported at "more
often than not" strength at best; no other evidence item's
uncertainty propagates as directly to C0. The honest repair is
denominator growth (more scenarios), not tighter language.

**Rubric.** All five dimensions rated per item (4); E1 identified as
limiting with the interval-width argument (3); validity windows
tied to re-audit triggers, not calendar dates alone (3).

## Exercise 22.4 — safety-case draft

**Full-credit draft (skeleton; full submission 800-1,200 words).**

*Context and ODD.* The system, its deployment context, and the
operational design domain — the argument's scope, stated first
(SMIRK's lesson: scope is what makes completeness possible
[SRC-PAPER-103]).

*Top claim.* "Acceptably safe within the ODD under the control
stack," with "acceptably" defined by the stakeholder's criteria
(Ch. 21's normative step reappears here).

*Hazard-derived decomposition.* ≥ 3 sub-claims, each traced to a
named hazard from the FMEA/STPA-style analysis (hazard → safety
requirement → sub-claim → evidence: the traceability ISCaP demands
[SRC-PAPER-102]).

*Evidence table.* Each row: what/population/interval/date/validity
window/transfer distance (exercise 22.3's dimensions); confidence
rating per the template's evidence-confidence structure
[SRC-PAPER-101].

*Defeaters.* Each named, classified rebuttable-or-acceptable;
rebuttals cite evidence; acceptances appear verbatim in residual
risk.

*Residual risk.* Quantified where denominators exist (with
intervals); stated where they do not — the two forms never blended.

*Re-audit triggers.* The events that invalidate evidence rows:
revision changes, drift telemetry thresholds (Ch. 17), probe-arm
declines (Ch. 18's obfuscation signature), new tool registrations
(Ch. 14). The safety case's clock.

**Rubric.** ODD first (2); traceable hazard→claim chain (3);
evidence table with all dimensions (3); defeaters with honest
classification (3); residual risk both forms (2); re-audit triggers
(2).
