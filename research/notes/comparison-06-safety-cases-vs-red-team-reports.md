# Comparison note C06 — Safety cases vs red-team reports: assurance's two documents

> Comparison notes: 5 planned + this extension (2026-10-25, prompted by
> the incident set and the P10 dossier build — the two documents
> below kept appearing as each other's missing half). Sources:
> SRC-PAPER-058 (Ganguli red teaming, abstract-read), SRC-PAPER-059
> (Perez LM-vs-LM, abstract-read), SRC-PAPER-060 (Casper
> Explore-Establish-Exploit, abstract-read), SRC-PAPER-022 (AI
> Control, abstract-read), SRC-REPORT-013 (Air Canada tribunal
> summary, page-inspected), SRC-REPORT-014 (DPD, page-inspected),
> SRC-REPORT-015/016 (Chevy dealership, page-inspected). Companion
> chapters: 22 (safety cases), 15 (red teaming), 02 (evaluation
> science), 24 (research practice).

## The question a comparison exists to answer

A deployer must eventually hand someone a document that says "this
system is safe enough to ship, and here is why." Two genres compete
for the job. The **safety case** (Ch.22) argues from claims to
evidence to residual risk — structured, decomposed, defeater-listed,
built to be attacked by a reviewer. The **red-team report** (Ch.15)
argues from discovered failures — coverage-honest, denominator-aware,
two-sided, built to show where the system actually broke. Practitioners
write one and wish they had the other; the field's most expensive
mistake is treating either as a substitute for its complement.

## What each document is, structurally

| | Safety case | Red-team report |
|---|---|---|
| Direction of argument | top-down: hazard → claim → evidence → residual | bottom-up: attack → finding → coverage → residual |
| Unit of work | a claim with rated evidence and a named defeater | a finding with a denominator and a benign-cost side |
| Completeness mechanism | the ODD scopes what the argument covers | coverage accounting scopes what the attacks reached |
| Failure mode | beautiful structure over stale evidence (the argument outlives the system) | vivid findings with no argument they aggregate into (the list outlives the claim) |
| The reviewer's question | "which defeater is unrebutted?" | "what is the denominator?" |
| Course anchor | Ch.22's grammar; P10's dossier (claims C1–C3 with caveats, verdict NOT DEPLOYABLE) | Ch.15's engagement discipline; the three incident reviews |

## The sharpest differences

**1. Where honesty lives.** A safety case is honest in its RESIDUAL
RISK section — what it did not establish, priced (P10's IA-1..IA-3
with expected recovery per action). A red-team report is honest in
its DENOMINATORS and its benign side — the zero-success bound, the
over-refusal ledger [SRC-PAPER-061's two-sided structure]. Both
genres can be dishonest in exactly the symmetric way: the safety case
that hides a defeater, the red-team report that hides a failure it
found and could not fix. The incident record shows the cost of the
first (Air Canada: no evidence any evaluation existed — the tribunal
read the absence as negligence [SRC-REPORT-013]) and the second's
cousin (DPD: a behavior-changing release with no regression gate at
all [SRC-REPORT-014]).

**2. What each cannot do alone.** The safety case cannot DISCOVER —
it inherits its hazard list from somewhere, and a hazard list
authored without red-team pressure is a guess dressed as a taxonomy
(the Chevy dealership's authority row was empty until the public
filled it [SRC-REPORT-015/016]). The red-team report cannot STOP —
findings without an argument do not compose into a deployment
decision, and "we found 14 issues and fixed 12" is not a safety
statement until someone says why the 2 remaining are tolerable
(Ch.15's reporting hazard, taught as a design decision).

**3. Time behavior.** The safety case decays by DRIFT (Ch.17: the
evidence was collected on a distribution that moved — the argument
is still valid, about a system that no longer exists). The red-team
report decays by COVERAGE ROT (the adversary population moved; your
denominators describe an attack surface that has since grown). The
maintenance answer differs accordingly: re-run the case's evidence
claims on schedule; re-estimate the report's coverage when the
threat model changes — and the release that changes behavior needs
BOTH re-run (the DPD lesson as a genre-theoretic sentence).

## The composition (what the course certifies)

The deployment-grade artifact is neither document alone but the
loop: red-team findings become the safety case's DEFEATERS (each
discovered failure either rebutted with new evidence or accepted
into residual risk with a price); the safety case's unrebutted
defeaters become the red team's NEXT TARGET LIST (Ch.15's adaptive
phase, pointed by Ch.22's structure). P10's dossier is the loop at
course scale: the held-out trials (a mini red-team round) produced
the monitor-hold findings that became improvement actions with
expected recovery — and the verdict NOT DEPLOYABLE is the loop
working, not failing, because the gate was preregistered before
either document existed.

## Three practitioner decisions this comparison settles

1. **"Which do we need first?"** — Red-team pressure first, or your
   hazard list is fiction; case structure second, or your findings
   never become a decision. The order is the loop's direction, not a
   preference.
2. **"Who reads which?"** — Reviewers and auditors attack the case
   (its defeaters); executives and incident responders need the
   report (its denominators and costs). Writing one document for
   both audiences produces the worst of each.
3. **"When is either DONE?"** — Never individually; the loop closes
   only at decommission. The honest completion criterion is a dated
   statement of what would re-open each: drift triggers for the case,
   threat-model changes for the report.

## Non-claims

This note compares document genres, not safety levels: neither
document "makes" a system safe, and a system can be safe with sloppy
documents or unsafe with beautiful ones — the documents' job is to
make the JUDGMENT auditable. No claim here about which genre
regulators will prefer (Ch.23's citation forensics apply: that is a
per-instrument, per-version question). The incident readings are
production single-events, not a sample of the genre's performance.
