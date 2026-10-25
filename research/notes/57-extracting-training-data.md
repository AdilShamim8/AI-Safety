# Note: Extracting Training Data from Large Language Models (2020)

Source: SRC-PAPER-132 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Note 56 measured memorization with the defender's instrument; this
paper runs the adversary's. The setting: billion-parameter models
trained on private datasets and *published* — the abstract's framing
of the era's emerging norm. The attack: **training-data extraction**
— recover individual training examples by querying the model. The
demonstration: against **GPT-2** (trained on public-Internet
scrapes), the authors extracted **hundreds of verbatim training
sequences**, including **personally identifiable information
(names, phone numbers, and email addresses)**, IRC conversations,
and more (the API record truncates mid-list; the extract classes
named are quoted, the rest recorded as enumerated-in-body).

The threat-model move is the note's core: the paper treats
*publishing the model* as publishing *some of the data* — the
artifact-contains-the-corpus claim that Ch. 16's supply-chain
unit now treats as a first principle. Every "we trained on private
data, but we only ship the weights" deployment carries this
paper's finding as its standing counterexample.

## What the abstract establishes

1. The extraction attack against trained-and-published LLMs, with
   individual-example recovery demonstrated.
2. GPT-2 as the target, with hundreds of verbatim extractions.
3. PII among the extract classes: names, phone numbers, email
   addresses; IRC conversations and further classes enumerated in
   the body.

Unclaimed: the attack's ranking strategy (the body's
perplexity-thresholding detail), extraction rates per class, and
the mitigation analysis — the note claims the attack class and
its yield classes, no rates.

## Why this note exists in the course

1. **Ch. 16's extraction unit.** The chapter's privacy-risk
   taxonomy (what you send out vs what the artifact remembers)
   gets its canonical attack citation: model inversion's
   language-model form, complementing [note 14](14-model-extraction.md)'s
   parameter-extraction (steal the function) with data-extraction
   (steal the corpus).
2. **The publication-gate implication.** If weights can leak
   training text, the release gate for any privately-trained model
   includes a memorization audit — [note 56](56-secret-sharer-memorization.md)'s
   exposure instrument as the pre-publication check. Ch. 22's
   release-gate template carries this as the privacy-tier check.
3. **The Samsung incident's mirror.** [Incident 08](incidents/08-samsung-chatgpt-pastes.md)
   is data flowing INTO a service whose retention was ungoverned;
   this note is data flowing OUT through the artifact itself. Ch. 16
   teaches the two directions as one perimeter — this pair is the
   teaching exhibit.
4. **The "public scrapes" honesty.** The demonstration target was
   trained on *public* data, and the extraction still yielded PII —
   the privacy failure does not require a private corpus, only a
   corpus containing people. The course files this against the
   "our data is public anyway" defense.

## What this note does NOT claim

No claim that current chat interfaces extract as easily (alignment
training changes the surface — the body-and-beyond question, noted
honestly); no extraction-rate numbers; no claim that deduplication
or differential privacy suffice (the follow-up literature carries
those evaluations at their own access levels).

## The falsifiable extension (deterministic tier)

The extraction *logic* (rank-by-likelihood, threshold, verify)
runs on P02's world without any model:

- Train the synthetic learner on a corpus containing k planted
  "PII-shaped" unique sequences (formatted identifiers, not real
  data); then run the extraction pipeline: generate, rank
  continuations by likelihood lift over a background model, and
  threshold at the exposure-calibrated cut.
- Prediction worth testing: the pipeline recovers planted sequences
  at a rate statistically above the chance baseline, and the
  recovery rate tracks duplication count (the bridge into note 58's
  laws, arriving next).
- Falsifier: chance-level recovery despite positive exposure (note
  56's instrument) would separate *memorization* from
  *extractability* in this world — a genuinely interesting boundary
  for the two-instrument stack.
