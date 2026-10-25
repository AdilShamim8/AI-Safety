# Dataset card: GAIA

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a benchmark for General AI Assistants posing
  **real-world questions requiring fundamental abilities** —
  reasoning, multi-modality handling, web browsing, and tool-use
  proficiency — where questions are "conceptually simple for humans
  yet challenging for most advanced AIs." The abstract's headline
  numbers: **human respondents obtain 92% vs. 15% for GPT-4
  equipped** [with tools — the API record truncates mid-clause;
  recorded].
- **Canonical home:** "GAIA: a benchmark for General AI Assistants"
  (Mialon et al., arXiv:2311.12983, 2023-11-21, API-verified
  2026-10-25).

## 2. Composition (abstract-stated)

- Real-world questions across the ability set; the **92%-vs-15%
  human-GPT-4 gap** with the truncation honestly noted on the
  tooling clause. Question counts and task taxonomy: body-level,
  unclaimed.

## 3. Collection and labeling

- Abstract-level: questions designed to be human-easy and
  AI-hard — the inversion that makes GAIA a *capability*
  benchmark rather than a knowledge one. The verification
  protocol is body-level.

## 4. Splits and leakage discipline

- Standard contamination discipline; the course's honest note: a
  2023 benchmark's questions circulate, so post-2023 model scores
  carry leakage risk — the same dated caveat every old card
  carries, applied forward.

## 5. Where the course uses it

- **Ch. 14:** the general-assistant capability reference — pairing
  with WebArena (card 39) (environment realism)
  as the two general-agent instruments; the inversion (human-easy,
  AI-hard) is the diagnostic for brittle tool-use competence.
- **Ch. 20:** the capability-evaluation framing — what "general
  assistant competence" means operationally, priced honestly with
  the human baseline attached.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; counts, taxonomy, and the
  truncated tooling detail unclaimed; the 92/15 figures quoted as
  the abstract's own, at its date.
