# Verifying sources — the learner's field guide

This course's core discipline: **no fact without a source, no source
without an access level, no claim without counterevidence.** You will
apply it in every chapter, every project, and — if you take nothing
else from the course — in your job. This page teaches the practical
mechanics: where information actually lives, how to check it, and how
to record what you did honestly.

The repository's own method document
([research/research-method.md](../research/research-method.md)) is the
binding version for contributors; this page is the same discipline
written for someone doing it for the first time.

## 1. Where each kind of information actually lives

| You need | The primary source | Never trust |
|---|---|---|
| A paper's claim | the arXiv **abstract page** (fetch it), then the PDF if the claim is in the body | a blog's summary of the paper, your memory of "having read it" |
| A dataset's size/license | the **canonical repository's README/LICENSE** and the hosting page (HF dataset page) | a tutorial, a mirror repo, the paper's abstract alone |
| A tool/framework's behavior | the **spec or the source code** at the pinned version | a course video from two years ago, a forum answer |
| A model's benchmark score | the paper **plus** the evaluation harness repo (reproducible numbers have code) | a leaderboard screenshot, a vendor deck |
| A statistic about the field | the **dated snapshot you fetched yourself**, with the count recorded | a number someone quoted without a date |
| A legal/policy fact | the ruling or the regulation text itself (or a professional summary that names the citation) | a tweet thread "explaining" the ruling |

The pattern: **always one step closer to the primary source than
wherever you first saw the fact.** If you saw it in a blog, find the
paper; if you saw the paper cited, fetch the abstract page; if the
number is in the abstract but you need the method, read the body.

## 2. Access levels — record what you ACTUALLY did

Every source you register carries one of five levels. Use them
honestly; over-claiming access is the failure mode this whole system
exists to prevent.

- **full-text-read** — you read the actual body of the document. You
  may cite body-level details.
- **abstract-read** — you fetched and read the abstract page. You may
  cite what the abstract says; body details are off-limits.
- **page-inspected** — you looked at the live page (a job board, a
  program site, a repo page) on a recorded date. You may cite what
  the page displayed, as a dated snapshot.
- **metadata-only** — you saw structure (title, authors, venue) but no
  content. You may cite existence, never facts.
- **unavailable** — you tried and could not fetch it. Record the
  failure; never silently fill the gap from memory.

If a fetch fails, say so in the register —
"Moffatt v. Air Canada's decision page returned an HTML conversion
error at fetch time" is a *recorded limitation*, and the note that
used the second-hand summary says exactly that
([SRC-REPORT-013](../research/source-register.yaml)).

## 3. The claim anatomy — falsifiable or it does not go in

A registered claim has five load-bearing parts (see
[research/claims-register.yaml](../research/claims-register.yaml) for
hundreds of worked examples):

1. **The statement** — specific enough to be wrong: "817 questions",
   not "a large benchmark". Include the date observed and the n.
2. **The source** — one register ID, already access-leveled.
3. **Evidence strength** — "page-inspected single fetch" is a real
   answer; so is "self-reported program statistics, not independently
   verified."
4. **Assumptions** — what must be true for the claim to hold (e.g.,
   "salary ranges reflect postings, not verified compensation").
5. **Counterevidence** — what would argue against it, including the
   discrepancy you noticed yourself. If you found none, write "none
   observed this session" — that is a claim about your search, not
   about the world, and it is honest.

## 4. The five-minute verification drill (do this once, now)

Take any fact you "know" about AI safety — say, "TruthfulQA has 817
questions." Now:

1. Fetch `https://arxiv.org/abs/2109.07958`. Read the abstract. Does
   it contain 817? (It does — you may now cite it as abstract-read.)
2. Fetch the canonical repo's README or the HF page. Does it agree?
   Where would you record a *disagreement* between abstract and
   artifact? (The repository has documented exactly this class of
   discrepancy — e.g., GSM8K's "8.5K abstract vs 8,792 released
   artifact" — in the dataset cards, with both numbers kept.)
3. Write the claim with all five parts. Congratulations: you have just
   done what this repository does 152 times in its claims register.

## 5. Red flags — when a source should NOT be trusted

- **Undated numbers.** "There are 500 open AI safety roles" — when?
  Counts are perishable; register them as dated snapshots.
- **Vendor-curriculum alignment.** A certification body's guide to
  which certifications you need (see the SANS white paper caveat,
  [SRC-CURR-008](../research/source-register.yaml)) is a real
  observation of the market AND a commercial for its own products.
  Both facts can be true at once; record both.
- **Self-reported outcomes.** A fellowship reporting its own alumni
  placement ([SRC-CURR-006](../research/source-register.yaml)) is
  structure and scale evidence, not independent outcome evidence.
- **The memory trap.** "I remember this paper showed X" is not an
  access level. If you cannot fetch it now, it is unavailable until
  you do.
- **Search-snippet citations.** A snippet is a rendering artifact of
  someone else's crawl; if the snippet is all you can reach, the
  access level is metadata-only at best.

## 6. Where this discipline shows up in the course

- Chapter 02 builds it into evaluation design (preregistration,
  dependence-aware splits) — verification is the experimental
  version of the same habit.
- Every chapter's **readings** section splits "verified" from
  "assigned, pending" access levels.
- The [dataset cards](../datasets/catalog.yaml) carry per-fact
  reference tables: every composition number traces to the URL it was
  collected from.
- The [incident notes](../research/notes/incidents/README.md) show the
  discipline under time pressure: what the record establishes, what it
  leaves unknown, and the "what this does NOT demonstrate" section
  that keeps hindsight honest.
- The [dashboard](../index.html)'s evidence ladder is the live state
  of all of it — every source the course uses, bucketed by the
  strength of your own two eyes.
