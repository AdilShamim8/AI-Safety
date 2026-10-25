# Incident review: Samsung's ChatGPT pastes — confidential code into a public channel

Class: **production incident (data-leak, no attacker)** · Date of
event: 2023-03 (pastes, per the Korean press record) → 2023-05-01
(restriction effective) → 2023-05-02 (Bloomberg/Forbes/TechCrunch
coverage) · Date of this note: 2026-10-25
Sources: SRC-REPORT-026 (Bloomberg, 2023-05-02, headline and core
facts page-inspected via search-result content), SRC-REPORT-027 (NHI
Management Group consolidated analysis with full reference list,
page-inspected in full 2026-10-25 — the same vendor-analysis tier the
Chevy note used, with the same honesty caveats) [CLM-0193].

## 1. What happened (observable facts only)

In March 2023, per the Korean press record consolidated by the
analysis page [SRC-REPORT-027, citing Economist Korea, 2023-03-30]:
three Samsung Semiconductor employees pasted confidential material
into the public ChatGPT service while doing their jobs — one pasted
"the full source code of a semiconductor equipment measurement
program," another pasted "source code from a yield and defect
analysis program," and a third entered a transcript of a recorded
meeting to generate minutes.

Samsung's internal memo (per the same consolidation) said engineers
"accidentally leaked internal source code." Effective 2023-05-01,
Samsung restricted generative-AI tools including ChatGPT on
company-owned devices and devices on internal networks, while it
developed security measures; staff using such tools elsewhere were
told not to submit company or personal data [SRC-REPORT-027;
SRC-REPORT-026 headline: the ban followed the leak]. Bloomberg's
report (2023-05-02) is the wire record of the ban; Forbes and
TechCrunch carried the same story the same day, citing Bloomberg
[SRC-REPORT-026; per the search-result record].

The consolidation's bottom lines, quoted for the course: "There was
no attacker. Employees entered confidential data into a public AI
service themselves while trying to do their work. The risk was that
the data left Samsung's control and could not be retrieved or
deleted. No misuse of the data has been reported" [SRC-REPORT-027].

## 2. What this incident teaches (established, attributed)

1. **Shadow AI is a data-provenance failure, not a model failure.**
   The model did exactly what it was asked; the *channel* was the
   incident: confidential data crossed into a third party's
   infrastructure with no retrieval path. Ch. 16's provenance
   discipline (know where your data goes) is the entire lesson —
   zero adversarial machinery required.
2. **The utility trap.** All three employees were *doing their work*
   — code questions, defect analysis, meeting minutes. The leak's
   cause was usefulness without boundaries, which is why blanket
   bans (the remediation) trade productivity for control and
   predictably spawn policy-evasion pressure. The course files this
   as Ch. 21's governance dilemma in miniature: prohibitions
   without sanctioned alternatives create the shadow usage they
   forbid.
3. **"Cannot be retrieved or deleted" is the harm statement.** The
   irrevocability — not any observed downstream misuse — is what
   makes this a security incident. The course's severity teaching
   (Ch. 01): harm = exposure × irrevocability, with likelihood of
   misuse unspecified and honestly left there.
4. **The vendor-ecosystem asymmetry.** The employees' tool choices
   were rational individually and catastrophic collectively — the
   aggregate of individually-safe pastes is an uncontrolled
   disclosure channel. Ch. 22's governance answer: sanctioned,
   boundary-enforced AI services (private deployments, data
   agreements) rather than individual judgment calls.

## 3. What this does NOT demonstrate

No claim of training-data incorporation by OpenAI (unverified — the
"your inputs may train future models" terms were the concern, not a
demonstrated outcome); no downstream misuse (explicitly unreported);
no claim about Samsung's later policy (the record here ends at the
2023 restriction; the later re-permitting history is out of scope).

## 4. Course wiring

- **Ch. 16** (privacy, provenance, supply chains): the flagship
  data-provenance incident — pairs with the BadNets note (13) as the
  two halves of third-party-artifact risk (what you send out vs
  what you bring in).
- **Ch. 21:** governance of useful-but-uncontrolled tools; the
  ban-vs-sandbox dilemma.
- **Ch. 22:** the sanctioned-alternative principle for enterprise AI
  policy.
- **P07:** the trust-boundary matrix's real-world motivation —
  tool reach (credential/data exposure) classified *before* use.

## 5. Honest limitations of this review

Bloomberg's article is paywalled — headline and ban facts verified
via search-result content only. The paste details come through the
NHI consolidation (vendor analysis, commercial motivation recorded
in the register) citing Economist Korea and GIGAZINE — the primary
Korean reporting was not independently fetched. The meeting-
transcript detail is recorded at that same second-hand level. The
wire record's consistency across Bloomberg/Forbes/TechCrunch (same
day, same facts) is the corroboration the note stands on.
