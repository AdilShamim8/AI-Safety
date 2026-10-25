# Dataset card: TrojAI

LICENSE observed via the NIST data.gov catalog record: **public-domain-
style NIST open data license** (license URL recorded as
`https://www.nist.gov/open/license` in the catalog metadata; the
program page itself uninspected) · verification date 2026-10-25
(IARPA program page and NIST catalog verified via search-result
inspection — snippet-level page content, recorded honestly) ·
prepared by the course build · status: card at page-inspected
(search-snippet) level

## 1. Identity and provenance

- **What it is:** the dataset series from the **TrojAI program** — an
  IARPA research program whose stated goal, from the program page:
  "deliver easily integrable software that can quickly, accurately,
  and robustly detect Trojans in AIs **before they are deployed**."
  The datasets are collections of trained AI models — some poisoned
  with trojans, some clean — built as detection challenges across
  rounds (image classification, NLP, and later pre-trained-LLM
  rounds; the challenge series culminating in the Trojan Detection
  Challenge collaboration with ICML 2023, which the course knows
  through the Mazeika et al. lineage it shares with HarmBench).
- **Canonical home:** the IARPA program page
  (iarpa.gov/research-programs/trojai) and the NIST-published
  challenge datasets (catalog.data.gov, publisher NIST, contact
  Michael Paul Majurski, public access level per the catalog
  record).
- **How WE obtained it:** search-result inspection of the IARPA
  program page and the NIST data.gov catalog record, 2026-10-25; no
  model files downloaded or redistributed.

## 2. Composition (page-verified, snippet-level)

- The NIST catalog record establishes: trained AI models as the data
  unit (an unusual and deliberate choice — the benchmark distributes
  *models*, not examples), public access level, NIST open license,
  and the program's publishing cadence (rounds, with the "Leftovers"
  collection honestly labeled as unreleased/failed-release models
  that "should not be considered high quality" — the catalog's own
  warning, quoted, and a small masterpiece of dataset honesty in
  itself).
- Round-level composition counts and trojan-trigger taxonomies:
  distributed across the round-specific NIST pages, uninspected this
  session — recorded as the limit.

## 3. Collection and labeling

- Program-level, page-verified: models constructed *for* the program
  with controlled trojan planting — the adversary is built in by
  design, with attack success rates among the release criteria (the
  Leftovers record's "did not meet the release criteria for accuracy
  or trojan attack success rate" confirms the criteria exist and what
  they measured).
- Course-relevant: poisoned-model detection is the *artifact-level*
  security problem — Ch. 16's supply-chain story (BadNets, note 13)
  made operational: given an opaque trained artifact, decide whether
  it contains a trigger. No other carded dataset measures this.

## 4. Splits and leakage discipline

- The challenge structure *is* the split discipline: detection
  methods score on held-out rounds they cannot train against — the
  program's rounds function as the grouped splits, and the course
  notes this as the design other security benchmarks copied.

## 5. Where the course uses it

- **Ch. 16** (privacy, provenance, and supply chains): the canonical
  artifact-security benchmark — pairs with BadNets (note 13) as
  theory-then-instrument, and with the provenance discussions as the
  "can you trust the artifact you downloaded" evidence base.
- **P10:** the dossier's supply-chain risk section cites it as the
  reference for what artifact-screening evaluation looks like at
  scale.
- **Ch. 22:** release-gate discussions of third-party models cite
  the program's own framing — detection *before deployment* — as the
  gate principle stated in its purest form.

## 6. Honest limitations (this card)

- Search-snippet page inspection: the IARPA page's full program
  description, the round datasets themselves, and the challenge
  results are uninspected; the license is recorded from catalog
  metadata, not the license page.
- The "Leftovers" honesty note cuts both ways: it is a warning about
  a specific collection, and a reminder that dataset provenance
  labels deserve reading before use — which is this card's closing
  lesson and the five-provenance-questions discipline in miniature.
