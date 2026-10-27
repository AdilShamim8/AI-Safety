# Chapter 23 — Solutions and rubrics

## Exercise 23.1 — genre sorting

**Full-credit solution.**

| Instrument | Genre | Required row contents | Invited failure |
|---|---|---|---|
| NIST AI RMF 1.0 | guidance (voluntary [SRC-REPORT-010]) | version 1.0; which functions performed; the evidence row per function | "aligned" with no function-level evidence — the structure walked in name only |
| EU AI Act | obligation (law [SRC-REPORT-012]) | article, class determination, phase date, in-force arithmetic | "ready" as a prediction about 405/649-days-out dates presented as present fact |
| MITRE ATLAS | knowledge base [SRC-REPORT-011] | counts pinned at fetch date; technique families used in hazard rows | cited as a requirement — it obligates no one |
| OWASP 2025 | community list [SRC-REPORT-004] | list date; coverage grid with named gaps | coverage % averaging away unmapped entries |
| Corporate RSP | self-commitment [SRC-REPORT-008] | published version; level logic; audit trail (Ch. 20's questions) | levels as marketing; memo overrides quietly |
| Paper's best-practices section | proposal (academic) | citation; the evidence the paper provides; explicitly no force | borrowed as if it were a standard because it has a bibliography |

The grammar difference in one line each: law rows answer *must you,
by when*; guidance rows answer *did you, with what evidence*;
self-commitment rows answer *did you keep your own promise*;
knowledge-base rows answer *what vocabulary did you use*; proposal
rows answer *what does the evidence suggest*.

**Rubric.** Correct genre per instrument (3); per-genre row contents
(3); the failure mode matched to the genre's specific weakness (3);
the five-grammar summary or equivalent (1).

## Exercise 23.2 — the clock

**Full-credit solution.**

Using the verified timeline [SRC-REPORT-012] with a decision date of
2026-10-23 (the chapter's verification date; any chosen date works
if stated):

- Entry into force: 2024-08-01 → in force 813 days — the Act is
  law now, not pending.
- GPAI Chapter V: 2025-08-02 → in force 447 days — provider
  obligations for GPAI models placed after that date are already
  live; the map's model-provenance row must state the placement
  date question.
- Annex III high-risk: 2027-12-02 → 405 days out (13.3 months) —
  any "ready" claim about Annex III obligations is a *prediction*
  about the deployment's state a year out, not a present property.
- Annex I high-risk: 2028-08-02 → 649 days out (21.3 months).

*The legal row, written:* "EU AI Act in force since 2024-08-01 (813
days). GPAI Chapter V in force since 2025-08-02 (447 days); this
deployment's model-placement date determines provider-obligation
applicability [stated, not concluded]. Class determination (Annex
III vs Annex I vs neither) is a legal question this map separates
from the date arithmetic and does not answer. Phase-in distances
computed 2026-10-23: Annex III 405 days; Annex I 649 days. The map
is not legal advice."

*The separation discipline:* the timeline facts are verified and
computable; the class determination requires interpreting articles
against the deployment's use case — counsel's job; the map keeps
the two in different rows so the arithmetic cannot masquerade as
the determination.

**Rubric.** Correct arithmetic with signs (4); in-force vs pending
distinction explicit (2); the legal row with the separation
discipline (3); the not-legal-advice boundary stated (1).

## Exercise 23.3 — coverage honesty

**Full-credit solution.**

*The check design:* (1) Build the grid: rows = the ten OWASP 2025
entries (LLM01..LLM10, pinned to the list as fetched
[SRC-REPORT-004]); columns = control, evidence, test, gap. (2) The
named-gaps requirement: every entry with no control is listed by
name in the coverage statement — "7 of 10 with LLM08 (vector and
embedding weaknesses), LLM09 (misinformation), LLM10 (unbounded
consumption) unmapped." (3) The evidence row per claimed entry: not
"we handle injection" but the Ch. 22 form — control name, test
citation with denominator and interval (e.g., agent_guard's 6/8
[40.9%, 92.9%] for the LLM01 row). (4) The sentence when three
entries are unmapped: "Coverage is 7 of 10 entries with named
controls and evidence; LLM08/09/10 are unmapped and open — tracked
in the risk register" — never "full coverage" with a footnote.

*Why the design works:* the grid makes absence visible (an empty
row is harder to average away than a missing bullet); the named-gaps
rule converts the coverage number into a falsifiable claim; the
evidence column inherits Ch. 22's confidence ratings; and the
sentence template forecloses the "full coverage" reading that the
unmapped entries would otherwise silently contradict.

**Rubric.** Grid with pinned list version (2); named-gaps requirement
(3); evidence-row standard with intervals (3); the honest sentence
(2).

## Exercise 23.4 — standards mapping with versions

**Full-credit map (skeleton).**

*Rows by genre (all five represented):*

- **Obligation:** the AI Act row (exercise 23.2's form) with the
  decision date, arithmetic, and separation discipline.
- **Guidance:** the NIST row — version 1.0 pinned, the four
  functions each with its performed-evidence cell (Govern: named
  policy owner; Map: the context/tool inventory; Measure: the
  paired trials + Ch. 18 instruments with intervals; Manage: re-audit
  triggers, tested or honestly untested), and the revision-pending
  note.
- **Knowledge base:** the ATLAS row — counts pinned at fetch date
  (16/208/40/73 [SRC-REPORT-011]), the technique families used in
  the hazard analysis, the living-knowledge-base caveat.
- **Community list:** the OWASP row (exercise 23.3's grid, embedded
  or referenced).
- **Self-commitment:** the vendor-framework row with Ch. 20's four
  audit questions answered by citation or gap, version pinned.

*The cited-vs-actual column:* every row's final cell — what the
vendor deck says vs. what the map found, in the Meridian style
("cited: NIST-aligned (undated); actual: 1.0, four functions with
evidence, Manage partial; gap: revision pending").

*The four-question protocol applied:* (1) instrument+version from
the claim's citation (or "unstated" — itself a finding); (2) genre
determination; (3) the evidence hunt — which rows of the map
correspond to the claim; (4) the hidden items — revision pipelines,
phase-in dates, unwritten levels, unpinned versions.

**Rubric.** Five genres present with version/date/force (4);
evidence cells with intervals where they exist (3); cited-vs-actual
on every row (3); the protocol applied to a real or constructed
claim with findings (3).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **Safeshield**, [module-11-eu-ai-act](../../courses/safeshield-governance/module-11-eu-ai-act.md) — watch before working the obligation-mapping exercises.
- **Safeshield**, [module-10-nist-ai-rmf](../../courses/safeshield-governance/module-10-nist-ai-rmf.md) — watch before working the framework-function exercises.
