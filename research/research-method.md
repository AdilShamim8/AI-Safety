# Research method

How this repository finds, verifies, and cites sources. This page documents the
search scope and the remaining gaps, as required for honest use of the materials.

## Purpose

Every substantive claim in this course is supposed to trace to a recorded source.
This page defines what "recorded" means here, what was actually searched, and what
this repository's evidence base can and cannot support. It is written for a reader
who wants to know how much to trust the citations before trusting the claims.

## Search scope

- **Window.** Sources available by the research baseline of **2026-10-20**. This
  build executed on **2026-10-21**; anything located after the baseline is recorded
  with its actual access date and, where relevant, labeled as a post-baseline
  addition rather than folded silently into the baseline snapshot.
- **Corpus types.** Academic preprints and papers (primarily arXiv), author
  repositories on GitHub, official standards and institute documentation (for
  example NIST, OWASP, MITRE), first-party incident reports and postmortems,
  evaluation-tool documentation, and a deliberately small set of secondary
  explainers used only as supplementary reading.
- **Languages and regions.** Searches were conducted primarily in English. Some
  multilingual and non-US/UK sources are included where they are technically
  relevant and verifiable. There is no nationality quota and no claim of global
  consensus; regional and linguistic coverage limitations are recorded below.
- **Selection rule.** Prefer one strong canonical source over several redundant
  introductions. Prefer original papers over explainers. Prefer dated official
  documents over press coverage of those documents.

## Verification standards

Each source is recorded in `research/source-register.yaml` with the schema defined
in the project brief: stable ID, verified title and attribution, canonical URL,
source type, publication date (verified or null), version, actual access date,
access level, evidence class, peer-review status, supported claims/modules,
limitations, and license. Two fields deserve emphasis because they are easy to
fudge and expensive to fake:

- **Access level** is what was actually read, not what was linked. A paper whose
  method and limitations sections were read is marked `full-text-read`; one where
  only the abstract loaded is `abstract-read`; a landing page that confirmed title
  and authorship is `page-inspected`. Downgrading an entry after a re-check is
  expected behavior, not an error.
- **Accessed-on dates** are the dates this repository's fetches happened. They are
  never used as publication dates.

Claims live in `research/claims-register.yaml` with claim text, source ID, relevant
section or page, evidence strength, assumptions, counterevidence, and date.
Unsupported conjecture is either labeled explicitly in prose or moved into
`RESEARCH_QUESTIONS.md` as an open question. Where a claim in the course depends on
an assumption (for example, "the theorems apply to optimal policies in finite
MDPs"), the assumption is stated with the claim, not in a footnote nobody reads.

## What this repository is not

This is not a systematic review or meta-analysis. There is no preregistered search
protocol, no dual-screening of abstracts, and no inter-rater statistics on source
selection. It is a curated engineering curriculum: the filtering is judgment-based,
done by the repository authors, and therefore subject to the biases listed next.
The three self-review passes required by the project brief (curriculum coherence,
scientific validity, engineering reproducibility) are self-reviews and are labeled
as such; they are not peer review.

## Known limitations and gaps

1. **Coverage bias.** The source base skews toward English-language material and
   toward US, UK, and EU institutions (arXiv, NIST, OWASP, MITRE, UK AI Security
   Institute). Relevant work from other research communities is included where
   identifiable, but no claim is made that coverage is geographically representative.
2. **Verification depth varies.** Early-build entries in the source register may be
   `page-inspected` where later entries are `full-text-read`. Chapter-level reading
   assignments are added only after the reading itself is done at the stated depth.
3. **Tooling APIs drift.** Evaluation and interpretability tooling changes quickly.
   Tool-specific guidance in this repository records the tool version tested, and
   code is only written against APIs that were imported and exercised locally.
4. **Single-maintainer error rate.** One agent (plus the repository owner) performs
   the verification. Counterevidence fields exist precisely because first passes
   are sometimes wrong; corrections are recorded rather than silently overwritten.
5. **Rapid-moving topics.** For governance and standards (chapter 23) and the
   frontier snapshot, the risk is not missing sources but stale ones. Each dated
   claim there names the document version it rests on.

## Standing instruments (2026-10-25 and later)

The method is executable, not aspirational — three instruments now run
in CI on every push:

- **`scripts/validate_repo.py`** — register schemas, local-link
  integrity, artifact hygiene (the original gate).
- **`scripts/audit_missing.py`** — the missing-values audit: every
  register entry's full schema, every claim's source reference, every
  unit's path and completeness, every card's license/verification
  statements, and every SRC-*/CLM-* cross-reference across all prose.
- **`scripts/build_dashboard.py`** — regenerates `index.html` from
  the registers; CI's freshness test compares the committed payload's
  counts field-by-field so the public page cannot drift from the data.

MAINTENANCE.md is the operating manual for all three. A method that
is not machine-checked decays into a style; these three are how this
repository keeps that from happening.

## Corrections policy

Errors found in this repository's own content are fixed in visible commits with the
reason stated in the message. Errors found in cited sources are recorded in the
source register's `limitations` field for that source. If you find an error, the
contribution path is `CONTRIBUTING.md`.
