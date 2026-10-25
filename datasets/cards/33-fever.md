# Dataset card: FEVER

LICENSE not observed this session — the canonical site's licensing
terms were not inspected; **unknown (pending page-inspect)** ·
verification date 2026-10-25 (arXiv abstract verified via API;
title/authors/date checked) · prepared by the course build · status:
card at abstract-read level; license open

## 1. Identity and provenance

- **What it is:** the founding fact-verification corpus — "a new
  publicly available dataset for verification against textual
  sources" — whose design has been quietly load-bearing for every
  later factuality instrument in this catalog: claims verified
  *against retrieved evidence*, not against the annotator's own
  knowledge.
- **Canonical home:** "FEVER: a large-scale dataset for Fact
  Extraction and VERification" (Nie et al., arXiv:1803.05355,
  2018-03-14, API-verified 2026-10-25); the dataset's canonical home
  is the fever.ai site with the corpus distributed through its
  channels.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-stated)

- **185,445 claims**, generated "by altering sentences extracted from
  Wikipedia and subsequently verified without knowledge of the
  sentence they were derived from" — the abstract's own construction
  and blinding design, both quoted.
- **Three-way labels:** Supported, Refuted, or NotEnoughInfo — the
  third class being the design's quiet genius: the label space
  includes *insufficient evidence* as a first-class outcome, which is
  exactly the abstention channel Ch. 06 and P03 spend their time on.
- **Annotator agreement: 0.6841 Fleiss' κ** — the abstract's own
  number, quoted; and **evidence sentences recorded** for the
  Supported and Refuted classes, making every judgment auditable
  against its cited source.

## 3. Collection and labeling

- Abstract-level, fully stated: claim generation by mutation of
  Wikipedia sentences, blinded verification, three-way labeling with
  measured agreement, and evidence-linked labels. The annotation
  pipeline's operational detail (annotator training, rounds) is
  body-level.
- Course-relevant: the evidence-linked label is the property that
  separates verification datasets from mere classification corpora —
  each label ships with the sentences that justify it, which is the
  dataset-side version of the gap sentence (Ch. 02's discipline:
  a score is evidence for a construct except named differences).

## 4. Splits and leakage discipline

- The Wikipedia-derived construction carries the standing
  contamination caveat: pre-2018 Wikipedia is in every large model's
  training corpus, so verification performance partly measures
  memorization — the course's standard contamination note, applied
  verbatim. Split structure is body-level, unclaimed.

## 5. Where the course uses it

- **Ch. 06:** the founding citation for evidence-anchored factuality
  — the ancestor that FActScore (card 17-adjacent, note 46) and the
  retrieval-verification pipelines descend from; paired with
  SelfCheckGPT (note 47) as the two evidence philosophies (external
  corpus vs internal consistency).
- **P03:** the NotEnoughInfo class is the dataset-side precedent for
  selective prediction and abstention — the third label IS the
  abstention channel, pre-dating the safety literature's version by
  years.
- **Ch. 02:** construct-validity study — what "verification" means
  operationally (three-way, evidence-linked, agreement-measured)
  versus the folk "fact-checking" construct.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; split structure, the
  pipeline baseline's scores, and the dataset's revision history
  (FEVER 2.0-era adversarial follow-ups) are body/site-level,
  unclaimed (abstract truncates at the pipeline comparison —
  recorded).
- The 2018 date is a feature for one lesson (everything predates the
  LLM era) and a caveat for another (training-corpus contamination is
  maximal) — the card carries both, which is the honest way to hold
  an old dataset.
