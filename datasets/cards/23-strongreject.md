# Dataset card: StrongREJECT

LICENSE not observed this session — the canonical repository's license was
not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked) ·
prepared by the course build · status: card at abstract-read level; paper
verified at `abstract-read`; license open

## 1. Identity and provenance

- **What it is:** a jailbreak-evaluation benchmark built to fix a
  measurement problem, not a prompt-collection problem: the abstract's
  diagnosis is that jailbreak papers "often boast near-100% attack
  success rates" while developers "substantially exaggerate the
  effectiveness of their jailbreaks" — because there is no standard,
  high-quality benchmark, so every paper rolls its own prompts and its
  own scoring. StrongREJECT supplies both halves: a curated set of
  forbidden prompts and an evaluation method that scores the
  harmfulness of responses.
- **Canonical home:** the StrongREJECT repository (GitHub), with the
  paper at arXiv:2402.10260 — "A StrongREJECT for Empty Jailbreaks"
  (Souly et al., 2024-02-15, verified via the arXiv API 2026-10-25).
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes the two components (forbidden-prompt set +
  response-harmfulness scorer) and the motivation: existing benchmarks
  "suffer from significant shortcomings" — which the card records as
  the paper's stated finding, with the specifics of those shortcomings
  (string-matching failures, rubric gaming) at body level, unclaimed
  here.
- Sizes, categories, and the rubric structure: **not established at
  this access level** — the abstract truncates before composition
  detail. The card records this as the honest limit rather than
  importing numbers from memory.

## 3. Collection and labeling

- Construction and labeling method: abstract announces the benchmark;
  its curation protocol is body-level and unclaimed. The scorer is
  described as evaluating "the harmfulness of the victim model's
  responses" — the abstract's own scope statement.
- The measurement-discipline point the course pins: StrongREJECT is
  named for rejecting *empty jailbreaks* — attacks that "succeed"
  under weak scoring while producing non-harmful output. That is
  exactly the paired-ledger discipline (P07's two-sided reporting)
  applied to jailbreak evaluation itself.

## 4. Splits and leakage discipline

- Not established at abstract level. The course's discipline for use:
  benchmark prompts are evaluation items; any defense or classifier
  tuned on them must report on a held-out untouched subset — the
  grouped-split rule from Ch. 02 applied verbatim.

## 5. Where the course uses it

- **Ch. 15** (red teaming and adversarial evaluation): the canonical
  citation for *jailbreak evaluation methodology* — the note that
  attack-success numbers are only as good as the scorer behind them,
  pairing with notes 31 (GCG) and 45 (many-shot) as the evaluation
  leg of the jailbreak trio.
- **P01/P07:** the harness's scorer-quality lesson (a weak scorer
  manufactures both false attacks and false refusals) cites this
  benchmark's motivation.
- **Ch. 02:** a construct-validity case: "attack success rate" is a
  construct whose operationalization (the scorer) can silently break
  it — construct laundering's most operational example.

## 6. Honest limitations (this card)

- Abstract-read access: no composition numbers, no license observed,
  no split structure. Every un-inspected field above says so.
- The paper's claims about *other* benchmarks' shortcomings are the
  authors' findings, recorded as such — the course has not
  independently evaluated the alternatives.
