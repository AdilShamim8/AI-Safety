# Careers index — three roles, one methodological spine

**What this page is:** the bridge from this course's routes to the job
market — what the three role families actually are, what the live
demand signal looks like (with sources and dates), and how to track
your progress step by step toward each one. The route pages own the
*learning* sequences; this page owns the *career* mapping.

**What this page is not:** a guarantee. Every market number below is a
dated snapshot with its access level stated; the honest version of
career planning re-checks the primary sources, and every figure here
traces to a register entry you can audit
([source register](../research/source-register.yaml),
[claims register](../research/claims-register.yaml)).

## The three roles at a glance

| | **AI safety researcher** | **AI security specialist** | **AI (safety) engineer** |
|---|---|---|---|
| Core question | *why* does the system fail, and what does that teach us about alignment? | *how* does an adversary break it, and what boundary stops them? | *what* do we ship, with which safeguards, at what utility price? |
| Course route | [alignment research](alignment-research.md) | [AI security engineering](ai-security-engineering.md) | [evaluations & assurance](evaluations-and-assurance.md) |
| Capstone that fits | P06 + research proposal (Ch.24) | P07 + P10 dossier | P01→P10 harness-to-dossier spine |
| Day-job artifacts | papers, eval reports, falsified hypotheses | threat models, red-team reports, regression suites | guardrails, monitors, release gates, runbooks |
| Employer shape (observed) | labs' safety teams, eval orgs, fellowships [SRC-CURR-005/006] | every org shipping LLM features [SRC-CURR-008] | labs' safeguards/infra teams [SRC-CURR-007] |

The three roles share this course's entire methodological spine —
paired ledgers, Wilson intervals, preregistration, honest residuals —
because all three jobs die the same death without it: a safety claim
nobody can audit.

## The live demand signal (dated 2026-10-25, honestly priced)

- **Volume:** the AISafety.com board listed **553 open roles** (updated
  2 days prior), spanning Anthropic, Google DeepMind, METR, Redwood
  Research, UK AISI, RAND, FAR AI, Constellation, Epoch AI, Apart
  Research and more [CLM-0166]; 80,000 Hours' board advertises **900+
  roles** across problem areas [CLM-0164].
- **Security titles:** a SANS analysis of **10,643 postings** (Sept
  2026) maps ten AI-security roles and reports four hiring under their
  own titles today — AI/ML Security Engineer, AI Red Team Engineer, AI
  Governance and Security Risk Lead, AI Security Architect [CLM-0167;
  vendor-published, commercially motivated, caveat recorded].
- **Compensation (employer-disclosed, posting-level):** $320,000–$405,000
  (Anthropic Research Engineer / Security Engineer, RL Security),
  $320,000–$485,000 (Staff SRE, Safeguards ML Infrastructure),
  $265,000–$295,000 (Policy Development, Technical AI Governance)
  [CLM-0166]. Ranges reflect postings, not verified pay.
- **The fellowship path:** MATS — 12 weeks in Berkeley or London,
  $1,250/week stipend plus $2k/week compute, 631 researchers trained
  since late 2021, 75% of alumni reported working in alignment
  [CLM-0165; self-reported program figures, priced as such].

Every bracket above is a claim with an ID, a source, an access level,
and a date. When you re-check them months from now, expect drift —
that is what live market data does.

## Entry mechanisms, by role

### AI safety researcher

1. **Fellowships first.** [MATS](https://matsprogram.org) is the
   established route (12 weeks, mentored, extension possible); it
   expects demonstrated research behavior — preregistered questions,
   falsifiable results — exactly what this course's projects produce
   [SRC-CURR-006]. Applications run roughly twice a year; Winter 2027
   was closed at fetch time, so track the page.
2. **Research artifacts over credentials.** The route's exit criteria
   (a falsified hypothesis, a paper note set, a causal-claims analysis)
   are the portfolio. 80,000 Hours' entry advice ("how to get into AI
   safety in three months") centers on building exactly this kind of
   evidence and entering the community programs it lists
   [SRC-CURR-005].
3. **Community programs.** BlueDot Impact courses, the EA Forum, AI
   Alignment Slack, EA Global / NeurIPS — named on the 80,000 Hours
   hub as the low-cost entry surface [SRC-CURR-005].
4. **Where the roles are:** labs' safety/alignment teams and
   independent eval orgs (METR, Redwood, FAR AI on the board snapshot
   [SRC-CURR-007]).

### AI security specialist

1. **The four titles that hire today** (SANS's observed taxonomy):
   AI/ML Security Engineer, AI Red Team Engineer, AI Governance and
   Security Risk Lead, AI Security Architect [CLM-0167]. Search those
   exact strings, not just "AI security."
2. **Vocabulary that transfers directly from this course:** OWASP LLM
   Top 10 (Ch.13's framework), MITRE ATLAS (Ch.15), threat modeling
   (Ch.14's matrices), red-team reporting with denominators (Ch.15's
   two-sided ledger). The course's P07/P10 artifacts ARE portfolio
   pieces for these titles.
3. **Certifications exist but are vendor-mapped.** The SANS paper maps
   its roles to SANS courses and GIAC certifications [SRC-CURR-008] —
   useful as a structured curriculum, priced as a commercial
   recommendation, not a hiring requirement. The equivalent honest
   signal is a public repo with isolated attack/defense evaluations
   and regression suites, which this course's security route produces.
4. **Where the roles are:** every organization shipping LLM features —
   the demand is broader-based than safety research and less
   fellowship-gated, per the SANS market framing [CLM-0167].

### AI (safety) engineer

1. **The build-and-gate craft.** This role ships the safeguards:
   guardrails, monitors, evaluation harnesses, release gates,
   rollback runbooks — the operational layer between research findings
   and deployed systems. The course's P01→P03→P08→P10 spine (harness,
   calibration, control protocol, dossier) is a miniature of the job.
2. **Infrastructure strength matters.** The board snapshot's
   engineering listings emphasize production systems (e.g., Staff SRE,
   Safeguards ML Infrastructure [CLM-0166]) — the same reliability
   discipline Ch.17 teaches, applied to the safety stack itself.
3. **Where the roles are:** labs' safeguards/infrastructure teams and
   larger platform companies; the title is newer and appears as
   "Member of Technical Staff" / "Safety Engineer" / "Responsible AI
   Engineer" variants on the boards [SRC-CURR-007].

## The concrete version: first 90 days

The ladder above maps the whole journey; [first-90-days.md](first-90-days.md)
makes the opening concrete — shared weeks 1-4 (the spine), then a
week-by-week plan per role with an ARTIFACT gating every Friday,
day-90 checkpoints defined as things you can hand a stranger, and the
three honest failure modes (reading without artifacts, tutorial drift,
skipping the spine).

## Progress tracking — the step-by-step ladder

Track progress in artifacts, not hours. Each rung below is complete
only when the artifact exists and is auditable (a repo, a report, a
published note). Copy this into your own tracker; the checkboxes are
the course's honest definition of "done."

### Rung 0 — orientation (both roles, ~1 week)

- [ ] Read [START_HERE.md](../START_HERE.md) and take the
      [diagnostic](../prerequisites/diagnostic.md); know your R1–R5 gaps
- [ ] Read [Ch.01](../chapters/01-risk-models-and-research-epistemics/README.md)
      and write one threat hypothesis with weakening observations
- [ ] Set up the repo: `uv sync`, `uv run pytest` green
- [ ] Pick a primary route (the table above) and a schedule
      ([study-schedules.md](study-schedules.md))

### Rung 1 — the methodological spine (all roles, ~4 weeks)

- [ ] Ch.02 evaluation plan preregistered (construct validity, splits,
      power) — the artifact every interviewer can probe
- [ ] P01 harness smoke tier: runner + scorer validation green
- [ ] First paper note published in your fork (falsifiable extension
      included) — begin the public trail
- [ ] First [dataset card](../datasets/catalog.yaml) studied end-to-end
      (composition, license, contamination status)

### Rung 2 — the role fork

- [ ] **Researcher:** Ch.03→04→05 chain + P02 + P04; one Goodhart-style
      result with honest intervals; 4+ paper notes on the route's list
- [ ] **Security:** Ch.12→13→14 chain + P07; one threat model and one
      isolated attack/defense evaluation with false-block rate reported
- [ ] **Engineer:** P03 + Ch.08 + P08; one calibration audit and one
      control-protocol tradeoff at a stated budget

### Rung 3 — the differentiators

- [ ] **Researcher:** P06 causal-claims study executed (real model if
      compute allows; the deterministic analogue plus the protocol
      otherwise); research proposal drafted per Ch.24
- [ ] **Security:** red-team report with denominators per Ch.15;
      provenance audit per Ch.16
- [ ] **Engineer:** P09 shift/subgroup audit; release-gate design
      argued in safety-case grammar per Ch.22

### Rung 4 — the market step (all roles)

- [ ] P10 capstone dossier: the integration artifact — send THIS to
      reviewers, not a resume bullet
- [ ] Portfolio assembled: 10 projects, notes set, this fork's commit
      history as the evidence of practice
- [ ] Applications out: the boards above (re-check counts the week you
      apply), fellowships if research-track (MATS timing), the four
      security titles searched directly
- [ ] One community surface active (Slack / forum / local group) —
      where referrals actually come from

## Pitfalls this page is designed to prevent

1. **Title blindness.** "AI safety" jobs hide under Member of Technical
   Staff, Safeguards, Trust & Safety, Responsible AI, Governance Lead;
   search by the WORK described, not the title [SRC-CURR-007].
2. **Certification theater.** The security market has real
   certifications mapped by vendors to their own curricula
   [SRC-CURR-008]; the durable signal is an auditable evaluation repo —
   which you will have by rung 4.
3. **Snapshot worship.** Every number on this page is dated
   2026-10-25; market data drifts. The register entries make
   re-verification one fetch away — do it before making decisions.
4. **Skipping the spine.** Role-specific depth without Ch.01–02
   discipline produces the exact failure this course exists to
   prevent: safety claims nobody can audit. Every interviewer from
   every org on this page probes for it eventually.
