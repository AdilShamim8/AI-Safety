# Chapter 16 — Privacy, provenance, and supply chains

| | |
|---|---|
| **Chapter** | 16 — Privacy, provenance, supply chains: memorization, privacy accounting concepts, model artifacts, licenses, dependency integrity |
| **Questions** | When a model is an artifact that anyone can download, fine-tune, and deploy — what leaks through it, and what does a *chain of custody* for model artifacts even look like? Why is "we deleted the data" not a privacy statement about a trained model? |
| **Hard prerequisites** | [Chapter 12 — adversarial ML](../12-adversarial-ml-and-robustness/README.md) (membership inference, extraction); [Chapter 02](../02-evaluation-science-and-experimental-design/README.md) (provenance questions, interval discipline) |
| **Core artifact** | Provenance audit: the full artifact chain of a deployed model — data sources with licenses, training inputs, the trained weights, the fine-tune, the dependencies — with each link's evidence, its leak surface, and its integrity control |
| **Projects** | P09 (shift/subgroup reliability) reuses the artifact-chain discipline; the repository's own licensing and notices files are the worked instance |
| **Readings** | Section 7 — four newly register-verified sources plus re-anchored earlier ones |

## 1. Research question and failure pathway

A trained model is a *compressed, queryable function of its training
data* — and every artifact in the chain that produced it (datasets,
weights, adapters, dependencies) is a place where someone else's
decisions become your deployment's properties. The failure pathway
this chapter instruments has four stations:

1. **The model memorizes.** Parts of the training set survive inside
   the weights and can be *emitted verbatim* under the right
   prompting — including personal information that appeared in a
   single document [SRC-PAPER-062]. "We deleted the data" says
   nothing about the function trained on it.
2. **Membership leaks without extraction.** Even when content cannot
   be recovered, *whether a record was in the training set* is
   itself a disclosure — the membership-inference channel
   (re-anchored from Ch. 12).
3. **The artifact chain is unaudited.** Base weights, fine-tunes,
   merged adapters, quantizations, prompts, and dataset slices flow
   through hubs whose *naming* is user-controlled — the model
   artifact inherits every compromise upstream of it, and OWASP's
   LLM03 exists because the chain is long and mostly invisible
   [SRC-REPORT-004].
4. **Licenses are load-bearing.** The legal terms on data, weights,
   and code are constraints on deployment and redistribution; a
   chain with one NC-licensed link and no policy is a lawsuit with a
   delay fuse — the reason this repository carries per-dataset
   license flags and a usage policy at all (the catalog's
   BeaverTails NC flag is the worked instance).

The reframe from Chapter 12: there, extraction and membership
inference were *attacks on a deployed API*; here, they are
*properties of an artifact* — measurable before deployment, priced
with the same interval discipline, and joined to the provenance and
integrity questions that classical supply-chain security asks of any
shipped binary.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Ch. 12's attacker-knowledge grid and the
extraction/membership-inference families; Ch. 02's provenance
questions and Wilson arithmetic.

**Outcomes.** After this chapter you can:

- state what memorization is operationally (verbatim emission under
  prompting) and the three log-linear laws that govern it — model
  capacity, duplication count, prompt context length
  [SRC-PAPER-063];
- distinguish content extraction from membership inference, and name
  what each does and does not disclose;
- explain differential privacy's contract at the concept level —
  the budget ε, what DP-SGD buys at what cost, and why "DP-trained"
  without numbers is not a claim [SRC-PAPER-064];
- audit an artifact chain link by link: data licenses, training
  inputs, weights, fine-tunes, dependencies — with integrity
  controls (hashes, pinning, signatures) at each hop;
- and run the canary/dedup audit pattern that turns "we think it's
  fine" into measured rates with intervals.

**Scope exclusions.** The chapter is conceptual-plus-measurement, not
legal advice: license interpretation is flagged, not adjudicated.
Formal DP proofs, the moments accountant's derivations, and
federated-learning variants are named and cited, not derived. Fair
use, copyright, and jurisdiction questions are explicitly
out of scope; the artifact *audit* pattern is the deliverable.

## 3. The core explanation

### 3.1 Memorization: the measured fact

The foundational demonstration: against GPT-2 — trained on public
Internet scrapes — a query-access adversary extracted *hundreds of
verbatim training sequences*, including names, phone numbers, email
addresses, IRC conversations, code, and 128-bit UUIDs, with each
sequence occurring in just *one* document in the training data; and
larger models were *more* vulnerable than smaller ones
[SRC-PAPER-062]. Two facts carry the chapter: memorization is
**extraction-recoverable**, and it grows with scale.

The follow-up made the laws quantitative — three log-linear
relationships: memorization grows with (1) model capacity, (2) the
number of times an example is duplicated, and (3) the tokens of
context used to prompt; with the complication that the laws
generalize imperfectly across model families, and the standing
conclusion that memorization is more prevalent than previously
believed and will likely worsen with scale absent active mitigation
[SRC-PAPER-063]. The follow-on work defined *extractable
memorization* — training data an adversary can efficiently extract
by querying — and demonstrated it against production systems
[SRC-PAPER-065].

The audit consequence: memorization is not a binary to be denied but
a rate to be measured — canary insertions (plant known
sequences at known duplication counts), extraction attempts, and
duplication-targeted dedup, each priced with denominators.

### 3.2 Membership inference: the quieter channel

Extraction recovers *content*; membership inference recovers
*participation* — "was this record in the training set?" — which is
a disclosure whenever membership itself is sensitive (a health
dataset, a fraud list). The two channels compose badly for the
defender: a model that resists extraction can still leak membership
(confidence patterns differ between trained-on and held-out
records), and a model that blunts membership signals (e.g., DP
training) also blunts extraction. The Ch. 12 attacker-knowledge grid
carries over: shadow-model attacks, confidence-only attacks, and
the calibration-aware defenses — with the Ch. 12 finding re-anchored
that early defenses fell to better attacks.

### 3.3 The privacy contract: differential privacy, at concept level

Differential privacy replaces "we tried not to leak" with a stated
bound: the model's output distribution changes by at most a factor
governed by ε when any single training record is added or removed.
DP-SGD operationalized this for deep learning — per-example gradient
clipping plus calibrated noise, with a refined accounting of the
privacy cost across training steps — demonstrating that deep
networks with non-convex objectives could be trained under a modest
privacy budget at a manageable cost in complexity, efficiency, and
model quality [SRC-PAPER-064]. What the contract buys: a *provable,
composable* bound that survives adaptive post-hoc analysis. What it
costs: measurable utility loss, careful tuning, and — the honest
part — a budget statement: "DP-trained" without ε, δ, and the
accounting method is a marketing adjective, not a claim. (The
derivations are named, not reproduced; the chapter's job is the
audit grammar, not the proof.)

### 3.4 The artifact chain and its integrity controls

The provenance audit treats the model as a binary in a supply chain.
Links and controls, link by link:

| Link | The question | The control |
|---|---|---|
| Data sources | whose text? what license? what PII? | dataset cards with per-fact references (the catalog's pattern); license flags; NC/quarantine policy |
| Training corpus | what actually entered, at what duplication? | ingestion manifests, dedup stats, canary ledger |
| Base weights | whose training run, what license, what provenance? | hash-pinned artifacts, model cards, signed releases |
| Fine-tunes/adapters | what data, what objective, what deltas? | adapter provenance records; the Ch. 14 tool-poisoning lesson generalized to *artifact* descriptions — untrusted text ships with artifacts |
| Dependencies | whose code, what versions? | lockfiles with hashes; CI pinned to SHAs (this repository's own practice, re-anchored) |
| Distribution | can naming be impersonated? | verified namespaces, signature checks — the classic typosquatting problem, now for model hubs |

OWASP's LLM03 (supply chain) exists because every one of these hops
is routinely unaudited [SRC-REPORT-004]; BadNets (Ch. 12) is what a
compromised hop *does* — the backdoor ships inside the weights,
surviving downstream fine-tuning.

### 3.5 Licenses as engineering constraints

The legal layer is a dependency of the artifact chain: dataset
licenses constrain redistribution and commercial use (the catalog's
NC flags), model licenses constrain derivative weights, code
licenses constrain distribution terms. The engineering discipline:
every artifact carries a machine-checkable license field; every
derived artifact inherits the *most restrictive* constraint in its
chain unless explicitly licensed otherwise; and the audit's output
includes a license lineage table — the same shape as the privilege
matrix of Ch. 14, but for legal rather than technical authority.

## 4. Worked example — the Aurora Health Scribe provenance audit

**Deployment.** "Aurora" is a clinical-notes summarization model:
a public base LLM, fine-tuned on 40M patient-note fragments from
three hospital systems, served on-premises, with a planned release
of the fine-tune adapter to partner hospitals. Synthetic example;
every number recomputed in the solutions.

**Link 1 — data sources.** The three hospital corpora carry data-use
agreements (research-only for one, deployment-permitted for two);
the base model's license permits derivative works; 2 of 47
third-party eval datasets are NC-licensed and quarantined from
training — the license lineage table flags the adapter as
*research-restricted* until the one agreement is renegotiated. The
audit artifact: the lineage table with the fuse visible.

**Link 2 — memorization measurement.** Before any release: 50
synthetic canaries planted per hospital corpus at duplication
counts {1, 10}; extraction attempt battery over 200,000 generations.
Post-dedup audit: canaries at duplication 1 → 12/50 exposed
(24.0%, Wilson 95% [14.3%, 37.4%]); canaries at duplication 10 →
1/10, paired with the pre-dedup 9/10 on the same plants: 8
discordant pairs, all improvements → exact one-sided sign test
p = 0.0039 — dedup demonstrably closed the duplication channel. The
audit verdict: dedup is load-bearing; the residual 24% single-exposure
rate is the release decision's real denominator, priced per-hospital.

**Link 3 — membership inference.** Shadow-model MI battery on
held-out patient records: 19/200 correct membership calls at the
0.5-confidence threshold (9.5%, [6.2%, 14.4%]) — weak but nonzero;
the finding is priced as "membership signal present; extraction is
the louder channel; DP decision below."

**Link 4 — the DP decision.** DP-SGD re-train at ε = 4: canary
exposure drops to 0/60 across both duplication arms (Wilson upper
bound 6.0%); the utility ledger: summarization quality -4.1 points
of ROUGE-L (priced, not hidden) and +2.3 seconds/epoch training
cost [SRC-PAPER-064's cost framing, at this course's fixture
scale]. The honest summary sentence: "DP at ε=4 removes measured
memorization at a 4.1-point utility cost; the budget statement is
part of the artifact."

**Link 5 — artifact integrity.** The released adapter is hash-pinned
and signed; the training manifest (corpus checksums, dedup stats,
canary ledger, DP budget) ships *with* the weights; the partner
distribution channel verifies namespaces. The chain's audit closes
with the one-sentence provenance statement a downstream auditor can
check: base@hash + corpus@checksums + recipe@commit → adapter@hash,
licenses lineage-constrained as flagged in Link 1.

## 5. Approach comparison

| Approach | What it buys | Measured anchor (source, level) | Failure mode |
|---|---|---|---|
| Deduplication | closes the duplication channel | log-linear duplication law [SRC-PAPER-063, abstract]; the 9/10→1/10 audit row | single-exposure memorization survives; dedup is per-corpus, not per-release |
| Canary audits | turns memorization into a rate with denominators | this course's audit pattern (Aurora) | canaries measure *planted* secrets; real-data memorization can be higher (the [SRC-PAPER-062] finding) |
| DP-SGD | provable, composable bound; adaptive-safe | deep nets under modest budget, manageable cost [SRC-PAPER-064, abstract] | utility cost; budget statements omitted in marketing; tuning burden |
| Access control (API-only) | artifact never leaves | standard deployment practice | does not protect against the operator; query-access extraction still applies [SRC-PAPER-062] |
| Artifact integrity (hashes, pinning, signing) | compromises become detectable | this repository's own lockfile/SHA practice; OWASP LLM03 [SRC-REPORT-004, page] | verified naming ≠ verified behavior; descriptions are untrusted text (Ch. 14's lesson) |
| License lineage tables | legal fuses made visible before they blow | the dataset catalog's per-dataset license flags | not legal advice; jurisdictions vary; terms change |

## 6. Where the methods fail

- **Dedup is a snapshot.** New corpora, re-crawls, and fine-tune
  data re-introduce duplication; the canary ledger must be re-run
  per training event, not once.
- **DP budgets decay silently under composition.** Fine-tuning a
  DP-trained model without DP accounting consumes budget the
  lineage table does not show unless the accounting travels with the
  artifact.
- **Canaries measure the audit's imagination.** Planted secrets
  probe known failure shapes; the single-document PII finding of the
  original extraction work [SRC-PAPER-062] was not a canary.
- **Integrity controls verify identity, not behavior.** A signed
  artifact from a verified namespace can still be a poisoned or
  stolen one — BadNets' persistence is the Ch. 12 reminder.
- **Licenses change and courts disagree.** The lineage table is an
  engineering instrument, not immunity; the NC flag is a fuse, and
  fuses only help if someone watches them.

## 7. Readings

Register-verified at the stated access levels (per
[research/source-register.yaml](../../research/source-register.yaml)):

1. **Carlini et al., "Extracting Training Data from Large Language
   Models"** [SRC-PAPER-062] — the foundational extraction
   demonstration: verbatim PII/code/UUIDs from single documents;
   larger models more vulnerable.
2. **Carlini et al., "Quantifying Memorization Across Neural
   Language Models"** [SRC-PAPER-063] — the three log-linear laws
   (capacity, duplication, context) and the
   more-prevalent-than-believed conclusion.
3. **Abadi et al., "Deep Learning with Differential Privacy"**
   [SRC-PAPER-064] — DP-SGD and the privacy-cost accounting that
   makes "DP-trained" a statement with numbers.
4. **Nasr et al., "Scalable Extraction of Training Data from
   Production Language Models"** [SRC-PAPER-065] — extractable
   memorization against production systems; the attack's modern
   scale.

Re-anchored from earlier chapters: Shokri et al. membership
inference (Ch. 12); BadNets (Ch. 12 — what a compromised chain hop
does); OWASP LLM03 supply chain [SRC-REPORT-004] (Ch. 13); this
repository's own dataset-card and license-flag practice (the
catalog) as the worked provenance instance.

Assigned-pending (never cited as verified): the moments accountant
derivation; DP fine-tuning composition analyses; empirical model-hub
compromise surveys; jurisdiction-specific license analyses.

**Note companions:** [13 BadNets — the founding backdoor paper](../../research/notes/13-badnets.md)[14 Model extraction — stealing the function](../../research/notes/14-model-extraction.md)[15 Membership inference — the privacy audit instrument](../../research/notes/15-membership-inference.md)[56 The Secret Sharer — memorization measured first](../../research/notes/56-secret-sharer-memorization.md)[57 Training-data extraction — the artifact contains the corpus](../../research/notes/57-extracting-training-data.md)[58 Quantifying memorization — three log-linear laws](../../research/notes/58-quantifying-memorization.md)[69 Trojan detection in LLMs — the specification question](../../research/notes/69-trojan-detection-llms.md)

## 8. Exercises

**Exercise 16.1 (analysis — audit the chain).** A team ships
"MedBrief-7B": a base model of unstated provenance, fine-tuned on a
mix of licensed hospital data, scraped clinical forums, and a
purchased dataset whose license prohibits redistribution of derived
*weights*. (a) Write the license lineage table and name the fuse.
(b) The team's privacy statement is "training data was deduplicated
and we found no leakage": name the three things this statement does
not cover, citing the extraction [SRC-PAPER-062], memorization-laws
[SRC-PAPER-063], and membership-inference channels. (c) Design the
canary audit they should have run — duplication arms, generation
budget, the paired dedup comparison, and the release-decision rule
with its interval. (d) They now consider DP-SGD at ε = 8 "because 4
hurt quality too much": write the two-sentence response that keeps
the budget statement honest [SRC-PAPER-064].

**Exercise 16.2 (empirical — pricing the Aurora numbers).** From
the worked example: canaries at duplication 1: 12/50 exposed;
duplication 10: 9/10 before dedup, 1/10 after; MI: 19/200;
DP re-train: 0/60. (a) Compute all four Wilson intervals and the
paired sign test for the dedup effect. (b) The release memo says
"canary exposure 24% — consistent with industry norms": what can and
cannot be concluded from 12/50, and what n would bound the rate
within ±5 points at 95%? (c) The DP claim "0/60 leaks": price it as
a bound and state the non-claim. (d) The MI rate is 9.5%: explain
why "weak" is the wrong summary if the protected class is "patients
in the fraud-investigation subset," and what the audit should add
before that concern is dismissed.

## 9. Hints

- For 16.1: (a) the purchased dataset's no-derived-weights term is
  the fuse — MedBrief-7B's *distribution* is the breach, not its
  training. (b) Dedup addresses only the duplication law;
  single-exposure memorization [SRC-PAPER-062], capacity growth
  [SRC-PAPER-063], and membership leakage are all live; "found no
  leakage" without a canary ledger and an MI battery is a vibe.
  (c) Mirror Aurora: arms at duplication {1, 10}, ≥50 canaries per
  arm per corpus, 200k-generation battery, paired comparison
  pre/post dedup, release rule on the *upper* Wilson bound of the
  duplication-1 arm. (d) ε = 8 is a valid budget *if stated,
  accounted, and composed honestly* — the dishonesty is omitting the
  budget and the utility ledger, not choosing a larger ε.
- For 16.2: (a) [14.3%, 37.4%]; [59.6%, 98.2%]; [1.8%, 40.4%];
  [6.2%, 14.4%]; sign p = 0.0039 (paired: 8 discordant improvements). (b) 12/50 bounds nothing tighter
  than [14.3%, 37.4%] — "consistent with norms" is unfalsifiable at
  that width; ±5 points at 95% needs roughly n ≈ 370 at the observed
  rate (compute in solutions). (c) 0/60 → [0%, 6.0%]: no evidence of
  leak at canary scale, *not* "cannot leak." (d) 9.5% on a small
  sensitive subset is a different object than 9.5% overall —
  condition the audit on the subset; the rate that matters is the
  false-positive-free identification of members of a small class.

## 10. Completion

This chapter is complete when you can:

- [ ] state memorization operationally and reproduce the three
      log-linear laws with their founding evidence
      [SRC-PAPER-062] [SRC-PAPER-063];
- [ ] distinguish extraction from membership inference and say what
      each discloses;
- [ ] explain DP's contract, what DP-SGD buys, and why budget-less
      "DP-trained" claims fail [SRC-PAPER-064];
- [ ] audit an artifact chain link by link with integrity controls
      and a license lineage table [SRC-REPORT-004];
- [ ] run the canary/dedup audit pattern with intervals, paired
      comparisons, and release rules;
- [ ] and write the one-sentence provenance statement a downstream
      auditor can check — base@hash + corpus@checksums + recipe@commit
      → artifact@hash.

Cross-links: the attack families' mechanics are
[Chapter 12](../12-adversarial-ml-and-robustness/README.md)'s;
untrusted artifact descriptions are
[Chapter 14](../14-agent-tool-memory-mcp-security/README.md)'s
tool-poisoning lesson generalized; the catalog's license flags are
the in-repository worked instance; drift of artifacts in deployment
continues in Chapter 17.
