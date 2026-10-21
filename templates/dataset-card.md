# Dataset-card template

Used by every project that touches a dataset (P03, P07, P09, P10, and any
chapter case studies). The card's most important section is the last one:
what the dataset cannot support.

```markdown
# Dataset card: <name>
Version/revision · License (verified URL) · Card date · Prepared by

## 1. Identity and provenance
- Canonical source (URL, repository, Hugging Face ID) and exact
  revision/version accessed.
- Who created it, for what stated purpose, and with what funding.
- How WE obtained it: access date, access path, checksum if published.
- If generated synthetically for this repository: the generation script,
  seed, and inputs — synthetic fixtures are labeled synthetic, always.

## 2. Composition
- Instances and fields (with units and semantics per field).
- Size: rows, tokens/characters, storage.
- Population sampled from, and sampling frame limitations.
- Known subgroup composition; linguistic/genre coverage.
- Content that could be considered sensitive or harmful, and how it is
  handled (it stays in the dataset only under its license and for the
  stated evaluation purpose).

## 3. Collection and labeling
- Collection process and time window.
- Label provenance: who labeled, with what instructions and pay, with what
  agreement measures (report kappa or percent-agreement with n — or record
  that none is published).
- Known labeling artifacts: order effects, instructions leakage, label
  noise structure.

## 4. Splits and leakage discipline
- The split discipline this repository enforces for the dataset
  (grouped/temporal/holdout as appropriate), and known leakage risks
  (near-duplicates, shared origins across splits).

## 5. Uses and known misuse
- What the dataset measures well.
- Documented failure modes when used for other purposes (contamination into
  pretraining corpora, benchmark overfitting, subgroup validity gaps).

## 6. What this dataset CANNOT support
The explicit negative-scope section: claims this dataset cannot ground, uses
it should not be put to. This section is mandatory and load-bearing for the
course's honesty rules — a card without it is incomplete by definition.

## 7. Maintenance
- Who maintains the upstream, update cadence, deprecation status.
- This repository's pinning policy for the dataset revision.
```
