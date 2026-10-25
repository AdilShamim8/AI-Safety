# Chapter 23 — Governance and standards for researchers

| | |
|---|---|
| **Chapter** | 23 — Governance and standards: the NIST AI RMF, the NIST adversarial-ML taxonomy, MITRE ATLAS, OWASP GenAI, the EU AI Act's obligations, corporate responsible-scaling frameworks — sorted by what they actually are: guidance, obligation, or proposal |
| **Questions** | Every safety document wants you to do something — but which of them can *make* you, which merely advise, and which are a lab's promise to itself? When a deployment cites "NIST-aligned" and "EU AI Act-ready," what would it take to check either claim — and what does the citation hide when the standards themselves carry versions, dates, and revision pipelines you were not told about? |
| **Hard prerequisites** | [Chapter 22 — safety engineering and assurance](../22-safety-engineering-and-assurance/README.md) (the safety case these instruments plug into); [Chapter 13 — LLM application security](../13-llm-application-security/README.md) (OWASP's vocabulary in use) |
| **Core artifact** | Standards mapping with versions: a deployment's controls mapped onto the relevant instruments — each entry carrying the instrument's version, date, legal force (guidance / obligation / proposal), and the gap between cited and actual |
| **Projects** | Feeds P10 (capstone assurance dossier) |
| **Readings** | Section 7 — three newly verified sources plus re-anchored ones |

## 1. Research question and failure pathway

Governance instruments are claims about processes. The researcher's
failure pathway:

1. **Genre confusion: citing a voluntary framework as if it were
   law, or a law as if it were advice.** The NIST AI Risk Management
   Framework (AI RMF 1.0, published 2023-01-26) is explicitly
   *intended for voluntary use* — page-verified — and is now being
   revised under the White House AI Action Plan [SRC-REPORT-010].
   "NIST-aligned" is a statement about which document version you
   walked through, nothing more.
2. **The obligation clock is already running.** The EU AI Act
   entered into force 2024-08-01; general-purpose AI model
   requirements (Chapter V) have applied since 2025-08-02 — 447
   days before this chapter's verification date; Annex III
   high-risk obligations apply 2027-12-02 (405 days out); Annex I
   2028-08-02 (649 days out) [SRC-REPORT-012]. "AI-Act-ready" has a
   date arithmetic that a citation must survive.
3. **Knowledge bases are not standards.** MITRE ATLAS is a *living
   knowledge base* of adversary tactics and techniques for AI
   systems — 16 tactics, 208 techniques, 40 mitigations, 73 case
   studies, built from real-world attacks and red-team
   demonstrations, with ATT&CK-adapted entries [SRC-REPORT-011]. It
   tells you what adversaries do; it obligates no one.
4. **Community lists carry version drift.** The OWASP Top 10 for LLM
   Applications 2025 lists document versions spanning April 2024 to
   July 2025 with no single stated release date — the entry
   vocabulary (LLM01 Prompt Injection … LLM10 Unbounded Consumption)
   is a shared language, not a compliance regime [SRC-REPORT-004,
   re-anchored].
5. **Corporate frameworks are promises with owners.** Anthropic's
   RSP (board-approved, with ASL-4 measures explicitly unwritten at
   publication [SRC-REPORT-008, re-anchored]) and OpenAI's
   Preparedness Framework (Critical = not deployable [SRC-REPORT-009,
   re-anchored]) are *self-commitments* — auditable precisely
   because they are published, binding on no one else, and only as
   strong as the measurement discipline behind the levels (Ch. 20's
   audit questions).

The chapter's reframe: read every instrument as an artifact with a
genre, a version, a date, and an enforcement mechanism — the
researcher's skill is *citation forensics*: what exactly is being
cited, at which version, with what force, and what did the citer
actually do?

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 22's safety-case form (instruments supply
evidence rows); Chapter 13's OWASP vocabulary in use; Chapter 20's
framework-audit discipline (the same questions, now generalized).

**Outcomes.** After this chapter you can:

- classify any instrument into guidance / obligation / proposal and
  state what each genre can and cannot support in an assurance
  argument;
- build the standards map with versions: instrument, version, date,
  force, mapped controls, and the cited-vs-actual gap;
- run the EU AI Act's date arithmetic for a deployment
  [SRC-REPORT-012];
- use ATLAS and OWASP as *vocabularies* for hazard analysis without
  pretending they are requirements [SRC-REPORT-011, 004];
- and audit a "compliant" or "aligned" claim to the evidence.

**Scope exclusions.** This chapter is not legal advice — the EU AI
Act's articles are used as verified facts about dates and
obligation structure, never interpreted for a specific legal
position; multi-jurisdiction survey (China, UK, ISO 42001's
certification ecosystem) is referenced only where already verified
in the registers; and the NIST AML taxonomy is carried at the
register's earlier honesty level rather than re-verified here.

## 3. The core explanation

### 3.1 The three genres

- **Guidance (voluntary):** NIST's AI RMF — "intended for voluntary
  use," now under revision [SRC-REPORT-010]. Its four functions
  (Govern, Map, Measure, Manage — the NIST AI 100-1 structure; see
  the register's honest access note) organize *how to think*; citing
  alignment means "we walked this structure," and the honest citation
  names which functions were performed with what evidence.
- **Obligation (law):** the EU AI Act — entry into force
  2024-08-01; GPAI model requirements applying since 2025-08-02;
  high-risk chapters phasing in 2027-12-02 (Annex III) and
  2028-08-02 (Annex I) [SRC-REPORT-012]. Obligations have dates,
  scopes, and enforcement — and a compliance claim must state which
  article, which class, which date.
- **Proposal / self-commitment:** corporate frameworks (RSP,
  Preparedness — Ch. 20's audit questions apply) and community
  knowledge bases (ATLAS, OWASP) — published, versioned, useful as
  vocabularies and precedent, binding on no one.

The genre determines the assurance case's citation grammar: *law*
rows cite articles and dates; *guidance* rows cite functions and the
performed evidence; *self-commitment* rows cite the published
commitment and its audit trail.

### 3.2 The version discipline

Every instrument in this field moves: AI RMF under revision
[SRC-REPORT-010]; OWASP's 2025 list carrying documents from April
2024 to July 2025 [SRC-REPORT-004]; ATLAS *living* — its counts
(16/208/40/73 [SRC-REPORT-011]) are a snapshot with a fetch date;
the AI Act's phases still phasing [SRC-REPORT-012]. The standards
map therefore pins, for every row: instrument name, version or list
date, fetch/verification date, and the honest note that counts and
entries move. A compliance citation without a version is a
coordinate without a map.

### 3.3 Where the instruments plug into the safety case

Chapter 22's argument slots, filled by genre:

- **Hazard vocabulary** ← ATLAS techniques (the adversary side) and
  OWASP entries (the deployment side) — the shared language that
  lets two teams mean the same thing by "prompt injection."
- **Process evidence** ← NIST functions: the safety case's
  governance/measurement rows cite *which* function's activities
  were performed (the Govern/Map/Measure/Manage structure).
- **Legal scope statements** ← the AI Act's classes and dates: the
  ODD's legal boundary (is the deployment's system in an Annex III
  class? when does the clock strike?) [SRC-REPORT-012].
- **Commitment evidence** ← the corporate frameworks: Ch. 20's
  audit questions (threshold definitions operational? measurements
  run? decisions track levels?) are how a proposal row earns its
  place.

### 3.4 Citation forensics: the four-question protocol

For any "aligned/compliant/ready" claim: (1) *Which instrument,
which version?* (2) *Which genre — what does alignment even
consist of?* (3) *What did the citer actually do — where is the
evidence row?* (4) *What does the citation hide — the revision
pipeline, the phase-in date, the unwritten level?* A claim that
survives all four is rare and valuable; most do not survive (3).

## 4. Worked example — the Meridian standards map

Meridian's deployment (Ch. 14/18/22's system) gets the full mapping,
versions pinned, gaps named. All date arithmetic recomputed from the
verified timeline [SRC-REPORT-012], as of the chapter's verification
date 2026-10-23:

**Legal row (obligation).** EU AI Act: in force 813 days
(since 2024-08-01). GPAI Chapter V: in force 447 days (since
2025-08-02) — if Meridian's underlying model is a GPAI model placed
on the market after that date, provider obligations already apply;
the map states the *class question honestly open* (which Annex, if
any, the deployment's use case falls under) with the phase-in
arithmetic: Annex III high-risk obligations 405 days out
(2027-12-02); Annex I 649 days out (2028-08-02). The compliance
claim this row supports: "class determination documented; timeline
arithmetic current as of 2026-10-23" — not "compliant," which is a
legal conclusion this course does not draw.

**Guidance rows.** NIST AI RMF 1.0 (2023-01-26, voluntary
[SRC-REPORT-010]): the map's process columns — Govern (roles for the
agent_guard policy owner), Map (the Ch. 14 context/tool inventory),
Measure (the paired trials, the Ch. 18 instruments), Manage (the
re-audit triggers of Ch. 22) — each cell citing the course's own
committed artifacts as the performed evidence. Honest note pinned:
the framework is under revision; the map's rows name version 1.0.

**Vocabulary rows.** OWASP 2025 (LLM01..LLM10 [SRC-REPORT-004]):
Meridian's controls cover LLM01 (injection → the R1-R4 policy),
LLM06 (excessive agency → the privilege matrix), LLM05 (output
handling → the store-writer controls), with LLM03/LLM04 mapped to
Ch. 16's supply-chain and poisoning rows — coverage stated as "7 of
10 entries have mapped controls; LLM08/09/10 unmapped (vector store,
misinformation, consumption) — open gaps, named." ATLAS
[SRC-REPORT-011]: the red-team scenario set's classes cross-referenced
to technique families (counts pinned at the fetch date's 16 tactics /
208 techniques / 73 case studies).

**Commitment rows.** The vendor's safety-level claim (Ch. 20's
memo): mapped with the four audit questions — threshold definitions
operational? measurements run? decisions track levels? version
pinned? The map's cell answers each with a citation or a gap.

**The cited-vs-actual column (the artifact's point).** Every row
carries it: "cited: NIST-aligned (vendor deck, undated); actual:
AI RMF 1.0 functions Govern/Map/Measure performed with evidence
rows E1-E4, Manage partial (re-audit triggers exist, untested);
gap: framework revision pending, map pinned to 1.0."

## 5. Approach comparison

| Instrument | Genre | What it gives the safety case | Version discipline needed | Failure mode |
|---|---|---|---|---|
| NIST AI RMF 1.0 [SRC-REPORT-010] | guidance (voluntary) | process structure; citation grammar for "performed" evidence | pin 1.0; revision under way | "aligned" with no function-level evidence |
| EU AI Act [SRC-REPORT-012] | obligation (law) | legal scope; date arithmetic; class determinations | pin article + phase date | "ready" for a date that has not struck (or has) |
| MITRE ATLAS [SRC-REPORT-011] | knowledge base | adversary vocabulary for hazard rows | pin counts at fetch date (living) | cited as a requirement that doesn't exist |
| OWASP LLM Top 10 2025 [SRC-REPORT-004] | community list | deployment vocabulary; coverage grid | pin the list's mixed doc dates | coverage % without named gaps |
| Corporate frameworks [SRC-REPORT-008, 009] | self-commitment | auditable promise; level logic | pin version; audit the measurement | levels as marketing, memo overrides |

## 6. Where the methods fail

- **Genre laundering is the default failure.** Voluntary frameworks
  acquire the rhetoric of law in sales decks; the four-question
  protocol exists to price the difference.
- **Version drift invalidates maps silently.** AI RMF under revision;
  ATLAS living; OWASP's mixed dates — an unpinned map rots faster
  than the code it describes.
- **Obligation phase-ins cut both ways.** "Ready" claims about dates
  405 or 649 days out [SRC-REPORT-012] are predictions about the
  deployment's future state, not statements about its present one.
- **Coverage percentages hide the unmapped.** "7 of 10 OWASP
  entries" is honest only with the three named gaps beside it —
  averaging away the unmapped entries is the Ch. 21 vague-motivation
  pattern in compliance clothing.
- **Self-commitments decay without audits.** Ch. 20's questions are
  the only instrument; a framework row without its audit-trail cell
  is a press release.
- **This chapter is not legal advice.** The verified dates and
  structure support *mapping and forensics*; any actual compliance
  determination belongs to counsel — the map's legal row says so in
  those words.

## 7. Readings

**Verified for this chapter (2026-10-23):**

- NIST — *AI Risk Management Framework (AI RMF 1.0)* landing page:
  title, version, publication date 2023-01-26, "intended for
  voluntary use," DOI NIST.AI.100-1, companion documents, revision
  under the White House AI Action Plan [SRC-REPORT-010; CLM-0158;
  the four functions carried at document-structure confidence with
  the JS-rendering honesty note].
- MITRE — *ATLAS (Adversarial Threat Landscape for
  Artificial-Intelligence Systems)*: the living knowledge base —
  16 tactics, 208 techniques, 40 mitigations, 73 case studies;
  empirical basis in real-world attacks and red-team demonstrations;
  ATT&CK-adapted entries [SRC-REPORT-011; CLM-0159].
- EU AI Act — implementation timeline (artificialintelligenceact.eu):
  entry into force 2024-08-01; GPAI Chapter V applying 2025-08-02;
  Annex III high-risk 2027-12-02; Annex I 2028-08-02
  [SRC-REPORT-012; CLM-0160].

**Re-anchored from the registers:** OWASP LLM Top 10 2025
[SRC-REPORT-004]; Anthropic RSP [SRC-REPORT-008]; OpenAI
Preparedness [SRC-REPORT-009]; Ch. 13's OWASP usage; Ch. 20's
framework-audit questions; Ch. 22's safety-case slots.

**Note companions:** [19 Wild patterns — surveying the governance-visible failures](../../research/notes/19-wild-patterns-survey.md) Incidents: [incident 13](../../research/notes/incidents/13-eeoc-itutorgroup.md)

## 8. Exercises

**Exercise 23.1 — genre sorting (analysis).** Classify six
instruments (AI RMF, AI Act, ATLAS, OWASP 2025, a corporate RSP, a
conference paper's best-practices section) into guidance /
obligation / proposal, and for each state: what an assurance-case
row citing it must contain, and the one failure mode its genre
invites.

**Exercise 23.2 — the clock (arithmetic).** From the verified
timeline [SRC-REPORT-012] and a deployment decision date of your
choosing: compute the phase-in distances, state which obligations
are already in force, and write the map's legal row — with the
class-determination question honestly separated from the date
arithmetic.

**Exercise 23.3 — coverage honesty (audit).** A vendor claims "full
OWASP Top 10 coverage." Design the check: the coverage grid, the
named-gaps requirement, the evidence row per claimed entry, and the
sentence you write when three entries turn out unmapped.

**Exercise 23.4 — standards mapping with versions (the chapter
assessment).** Build the complete map for a deployment of your
choosing: all five instrument genres represented, every row with
instrument / version / date / force / mapped controls / evidence
citation / cited-vs-actual gap; the date arithmetic current as of
your verification date; and the four-question protocol applied to
one real "aligned" claim you find in the wild (or construct
honestly).

## 9. Hints

- 23.1: the conference paper's best-practices section is the
  *proposal* genre wearing academic clothing — evidence, no force.
- 23.2: in-force distances are negative numbers; the sign is the
  point.
- 23.3: "full coverage" and "7 of 10 with three named gaps" are
  different claims; only one survives an audit.
- 23.4: the cited-vs-actual column is where the artifact earns its
  name — leave it empty and you have a brochure.

## 10. Completion

This chapter is complete when you can:

- [ ] classify instruments by genre and state each genre's citation
      grammar;
- [ ] run the AI Act's date arithmetic and separate class
      determination from timeline facts [SRC-REPORT-012];
- [ ] use ATLAS and OWASP as vocabularies with pinned versions and
      named coverage gaps [SRC-REPORT-011, 004];
- [ ] map NIST functions to performed evidence with the voluntary
      status stated [SRC-REPORT-010];
- [ ] and run the four-question citation-forensics protocol on any
      alignment claim you encounter.

Cross-links: the safety-case slots are
[Chapter 22](../22-safety-engineering-and-assurance/README.md)'s;
the OWASP vocabulary in use is
[Chapter 13](../13-llm-application-security/README.md)'s; the
framework-audit questions are
[Chapter 20](../20-misuse-dangerous-capabilities-release-evaluation/README.md)'s;
capstone execution is Chapter 24's (planned).
