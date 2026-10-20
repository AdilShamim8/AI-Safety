# Bias and fairness

LLMs inherit statistical patterns from training corpora — including
stereotypical associations. Unlike a biased database column, a biased LM
*samples* from the association every time it generates, so bias appears in
word choice, example selection, named-entity portrayal, and in downstream
scores (ranking, matching, scoring) built on LM outputs.

## The canonical evidence base (all real, all public)

| Dataset / study | What it showed | Citation |
|-----------------|----------------|----------|
| **Word Embedding Association Test** | "man:doctor :: woman:nurse"-style analogies encode historical stereotype in embeddings (Wikipedia-trained word2vec) | Caliskan et al., Science Advances 2017 (arXiv:1608.07187) |
| **Stochastic Parrots** | Documentation of risks & homogenization of LM training data | Bender, Gebru, McMillan-Major, Shmitchell, FAccT 2021 |
| **BOLD** | 43,623 prompts across professions/gender/race/religion/politics for *open-ended generation* bias; professions carry strong valence differences | Dhamala et al., arXiv:2101.11718 (EMNLP 2021); amazon-science/bold-dataset |
| **BBQ** | ~58k QA pairs; models pick stereotyped answers under ambiguity, and amplify stereotypes when disambiguated | Parrish et al., arXiv:2110.05828 (ACL 2022) |
| **Winogender / WinoBias** | Coreference resolution flips on gender-occupation co-occurrence; *doctor/pronoun* resolution tracks occupation statistics | Rudinger et al., arXiv:1804.09301; Zhao et al., arXiv:1808.06361 |
| **CrowS-Pairs** | 1,508 minimal pairs (stereotype vs anti-stereotype) for masked-LM scoring | Nangia et al., arXiv:2010.14033 (EMNLP 2020) |
| **ToxiGen** | 274k machine-generated statements about 13 minority groups; *implicit* toxicity that human-written benchmarks miss | Hartvigsen et al., arXiv:2203.09509 (NAACL 2022) |
| **Hiring-tool & sentencing precedents** | Amazon's scrapped recruiting model (Reuters, Dastin, 2018); COMPAS recidivism scores (ProPublica "Machine Bias," Angwin et al., 2016) | see [incidents/case_studies.md](../incidents/case_studies.md) |

## Where bias enters an LM pipeline

1. **Corpus** — who is over-represented (Common Crawl skews Anglophone,
   male-authored, formal text; C4 documentation: Dodge et al., arXiv:2104.08758).
2. **Preprocessing** — blocklists and quality filters that remove dialects
   (the "African-American English" filter problem in C4).
3. **Preference data** — raters' dialect/demographic preferences become
   the model's (InstructGPT §3; rater-agreement analyses).
4. **Deployment** — the *product* chooses what the model sees (search
   queries, uploaded docs) and what outputs reach users (thresholds).

## Fairness definitions actually used in audits

- **Demographic parity / disparate impact** — the 80% rule's AI
  descendant: positive-outcome rates across protected groups (EEOC/US
  framework context; EU AI Act uses similar concepts for high-risk
  systems).
- **Equalized odds / error-rate balance** — equal FPR/FNR across groups
   (Hardt et al., arXiv:1610.02413). This is what COMPAS analyses
   actually measured.
- **Calibration within groups** — scores mean the same thing per group
  (Kleinberg et al.'s impossibility, arXiv:1609.05807: calibration +
  error balance are mutually exclusive except in degenerate cases — know
  which one your regulator implicitly assumes).
- **Counterfactual fairness** — outcome unchanged under demographic
  counterfactual (Kusner et al., arXiv:1609.08207? — the canonical
  definition paper; this is what Winogender-style minimal pairs test,
  n=1 at a time).

## Mitigations, with honest trade-offs

1. **Dataset documentation** (Datasheets for Datasets, arXiv:1803.09010;
   Data Statements for NLP, Bender & Friedman 2018) — cheap, prevents
   downstream misuse, the single highest-leverage practice.
2. **Audits on the generation side** — run BOLD-style prompting over your
   actual user distribution; measure with Perspective API toxicity +
   sentiment gaps across group conditions (the repo's
   `benchmarks/bold.py` implements this on the real BOLD prompts).
3. **Counterfactual test suites** — Winogender/WinoBias-style minimal
   pairs on *your* task; a swap that changes a downstream decision is a
   finding, not a statistic.
4. **Debiasing interventions** — counterfactual data augmentation (Zhao
   et al. above), distributionally robust fine-tuning; effects are
   task-local and decay — re-audit after every model change.
5. **Post-hoc score adjustment** — group-aware thresholds (with legal
   review; disparate-impact law is jurisdiction-specific and not a
   technical decision).
6. **Don't**: "debias" by a blocklist alone. It moves the harm to
   harder-to-measure phrasings (ToxiGen's whole point about implicit
   toxicity).

## The policy interface

EU AI Act Annex III systems (hiring, credit, essential services, law
enforcement...) carry explicit bias-testing and logging duties; NIST AI
RMF "harmful bias" is a measured risk category (see
[governance/](../governance/nist_ai_rmf.md)). Technical audits
(BOLD/BBQ-style) are the evidence base those processes consume —
structured, versioned, and reproducible, which is why they live in this
repo's `benchmarks/` as code, not prose.
