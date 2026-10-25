# Dataset card: CounterFact (ROME evaluation suite)

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open

## 1. Identity and provenance

- **What it is:** the evaluation suite shipped with **ROME (Rank-One
  Model Editing)** — the paper's instrument for testing whether
  feed-forward weight edits successfully *update specific factual
  associations*. The card's subject is the evaluation data (the
  zsRE-style fact pairs and the CounterFact relation templates the
  repository ships), whose role in the field is larger than the paper:
  it became the de facto measuring stick for the model-editing
  literature that followed.
- **Canonical home:** "Locating and Editing Factual Associations in
  GPT" (Meng et al., arXiv:2202.05262, 2022-02-10, API-verified
  2026-10-25); the `kmeng1/rome` repository is the canonical code and
  data home.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes the evaluation shape: ROME is "effective on
  a standard zero-shot relation extraction (zsRE) mo[del…]" — the API
  record truncates; the zsRE anchor and the fact-pair evaluation
  design are stated, while the CounterFact-specific composition
  (relation counts, entity pairs) is body-level and **not established
  at this access level**.
- The card's structural note: the suite measures *editing success* —
  did the targeted fact change — alongside the side effects the
  abstract's analysis concerns itself with (the paper's later
  sections discuss generalization and specificity trade-offs; the
  course files those under the body, unclaimed).

## 3. Collection and labeling

- Abstract-level: factual-association pairs drawn from relation-
  extraction-style resources, formatted for causal-tracing and editing
  evaluation. The curation detail is body-level.
- Course-relevant design principle (from the paper's method): the
  causal-intervention-first design — identify decisive activations
  before editing — is the same correlation-then-intervention ladder
  as notes 34 and 50, applied to factual storage. The dataset exists
  to *service that ladder*, which is why Ch. 11 files it as an
  instrument rather than a corpus.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline: editing
  evaluations must report both the edit-success side and the
  untouched-fact side (the paired ledger, again) — an editor that
  breaks nine facts to fix one is not an editor, and the suite's
  template structure supports exactly that two-sided reporting.

## 5. Where the course uses it

- **Ch. 11** (behavioral steering and representation interventions):
  the canonical citation for *causal editing's* evaluation — pairs
  with note 06's patching grid (P06) and the latent-move intervention
  (note 34) as the intervention family's instrument set.
- **Ch. 09:** the causal-trace methodology the suite services —
  middle-layer feed-forward modules as the located site of factual
  recall — is a founding result in the localization literature.
- **P06:** the deterministic-tier analogue's real-world reference
  point (what the organism's two-branch structure simulates).

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; CounterFact template
  counts, zsRE detail, and the paper's specificity/generalization
  numbers are body-level, unclaimed (truncation recorded).
- The model-editing literature's later critiques (edit cascades,
  evaluation incompleteness) are *not* carried here — the card stays
  at what this paper's abstract establishes, and Ch. 11's readings
  carry the follow-up literature at their own access levels.
