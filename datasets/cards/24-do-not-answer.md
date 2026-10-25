# Dataset card: Do-Not-Answer

LICENSE observed 2026-10-25 (final verification pass): the Hugging Face
hosting LibrAI/do-not-answer carries the **apache-2.0** API license tag ·
verification date 2026-10-25 (arXiv abstract verified via API;
title/authors/date checked; license via HF API) · prepared by the course
build · status: card at abstract-read level; license now observed — the
earlier-recorded librarian-bots/do-not-answer hosting returns HTTP 401
and has been corrected to LibrAI (the paper-aligned org, page live)

## 1. Identity and provenance

- **What it is:** the abstract's claim to firstness — "the first
  open-source dataset to evaluate safeguards in LLMs" — built on a
  deliberate inversion of the usual harm-prompt design: instructions
  "curated and filtered to consist only of instructions that responsible
  language models should not follow." The evaluation target is the
  *refusal side*: six popular LLMs' responses to these instructions were
  annotated and assessed.
- **Canonical home:** the paper "Do-Not-Answer: A Dataset for Evaluating
  Safeguards in LLMs" (Wang et al., arXiv:2308.13387, 2023-08-25,
  API-verified 2026-10-25) with the dataset on Hugging Face.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes: the curation-and-filter design (only
  should-not-follow instructions), the six-model annotation exercise,
  and the open-source release. Sizes, category taxonomy, and the
  annotation scheme's detail are body-level and **not established at
  this access level** — recorded as the honest limit.
- The design direction is the card's teaching payload: harm benchmarks
  usually ask "does the model comply with harmful requests?";
  Do-Not-Answer's curation makes refusal-*quality* the measured
  construct — including, per the abstract's framing, the deployment
  goal of enabling "safer open-source LLMs at a low cost."

## 3. Collection and labeling

- Abstract-level: curated and filtered (no crowd-sourced free-for-all),
  with author-annotated model responses. The filtering criteria are
  body-level and unclaimed.
- Course-relevant honesty: "instructions that responsible models should
  not follow" is a *normative* curation standard — the dataset encodes
  its authors' harm taxonomy, which is exactly why Ch. 02's
  five-provenance-questions discipline asks "who decided, on what
  basis" before any safeguard eval borrows the set.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline for use:
  safeguard-tuning on any subset requires held-out reporting on the
  untouched remainder (the AdvBench rule, applied identically).

## 5. Where the course uses it

- **Ch. 04** (post-training): the refusal-side companion to harm-prompt
  sets — safeguards evaluated for what they *should* do, not only what
  they should avoid.
- **Ch. 15**: paired with StrongREJECT (card 23) as the two-sided
  evaluation cabinet: attack-side scoring (StrongREJECT) +
  refusal-side curation (Do-Not-Answer) — the paired-ledger discipline
  in dataset form.
- **P07**: the benign-cost arm's dataset citation (blocking attacks
  matters; refusing should-not-follow instructions *correctly* is the
  other side of the rate pair).

## 6. Honest limitations (this card)

- Abstract-read access: no composition numbers, no split structure, no
  annotation agreement statistics. The license was observed 2026-10-25
  (HF API tag, apache-2.0) — the one field this card previously recorded
  as open. The
  six-model list itself is body-level — the card counts the models,
  it does not name them.
