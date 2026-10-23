# Real-world dataset catalog — verified safety-evaluation datasets

This catalog is the course's bridge between **methodology chapters** and **real
evaluation practice**. Every dataset here is a real, publicly documented
benchmark used by working safety teams and researchers. Every card records,
fact by fact, **where each piece of information was collected** — the URL, the
access level, and the date — so a learner can re-walk the verification chain
themselves instead of trusting our summary.

Why this catalog exists, in one paragraph: evaluation science (Ch.02) teaches
that a benchmark number is only as good as the dataset's *construct validity*,
*provenance*, and *labeling process*. Reading dataset cards critically — with
the actual composition numbers in hand — is the fastest way to internalize
that discipline. Each card below is written as a worked example of that
critique, ending in the section no marketing brochure ever includes: what the
dataset **cannot** support.

## How to read this catalog (learner instructions)

1. **Do not memorize sizes.** Memorize the *questions*: who wrote the items,
   what population they sample, what the labels actually measure, and what
   license constrains your use.
2. **Follow the references.** Each card body cites facts as `[R1]`, `[R2]`,
   … and the final section resolves every marker to a URL with what was
   collected there and when. If you cannot rebuild a fact from its reference,
   treat the fact as unverified — we do.
3. **Use the curriculum map** below to pick the datasets tied to the chapter
   you are studying, and to the project you are building (P01 harness, P03
   calibration, P07 red-teaming, P09 shift).
4. **Respect the licenses.** We deliberately do **not** redistribute any
   dataset in this repository. Two datasets in this catalog are
   **non-commercial** (see [usage policy](#usage-and-licensing-policy)); all
   cards describe, they do not ship.

## Verification methodology (what "verified" means here)

Research baseline 2026-10-20; verification performed 2026-10-21 by direct
inspection of canonical pages (Hugging Face dataset pages, GitHub repositories
and file views, arXiv abstract pages, ACL Anthology pages). Access levels
follow the repository-wide convention in
[research/research-method.md](../research/research-method.md):

- `page-inspected` — the live canonical page was fetched and read; numbers
  quoted are what the page displayed on that date.
- `abstract-read` — the arXiv abstract page was read in full.
- `metadata-only` — secondary reporting of a canonical identifier; used only
  for the [pending verification](#pending-verification-queue) queue, never for
  card facts.

What we intentionally do **not** claim: row counts are living properties of
hosted datasets (mirrors drift, upstreams revise); a verified count is a dated
observation, not an eternal truth. Where two hosted versions disagree (for
example AdvBench's 520-row canonical CSV vs. a mirror card describing the
paper's 500-behavior framing), the card records **both** numbers with both
provenances rather than silently picking one.

## The catalog (22 verified datasets)

| # | Dataset | Risk area | Task shape | License (as observed) | Card |
|---|---------|-----------|------------|-----------------------|------|
| 01 | TruthfulQA | Truthfulness / imitative falsehoods | 817 open questions, QA | apache-2.0 (HF page) | [card](cards/01-truthfulqa.md) |
| 02 | BOLD | Social bias in generation | 23,679 generation prompts | CC BY-SA 4.0 (HF page) | [card](cards/02-bold.md) |
| 03 | RealToxicityPrompts | Toxicity in generation | ~99.4k scored prompt rows | apache-2.0 (HF page) | [card](cards/03-real-toxicity-prompts.md) |
| 04 | ToxiGen | Implicit toxicity / benign-counterfactual | 274k-scale generations, 9.9k annotated | MIT text (Microsoft, upstream repo; HF-page scope caveat) | [card](cards/04-toxigen.md) |
| 05 | BBQ | Stereotype bias in QA | 58,492 multiple-choice items | CC-BY-4.0 (canonical repo) | [card](cards/05-bbq.md) |
| 06 | XSTest | Over-refusal | 250 safe + 200 unsafe prompts | CC BY 4.0 (prompts; repo) | [card](cards/06-xstest.md) |
| 07 | BeaverTails | Safety annotation / preference | ~364k prompt–response rows | **CC BY-NC 4.0** (HF page) | [card](cards/07-beavertails.md) |
| 08 | HH-RLHF | Preference data / red-teaming | ~169k preference-pair rows | MIT (HF page) | [card](cards/08-hh-rlhf.md) |
| 09 | AdvBench | Adversarial suffix attacks | 520 harmful-behavior rows | MIT (canonical llm-attacks repo, read directly) | [card](cards/09-advbench.md) |
| 10 | JailbreakBench (JBB-Behaviors) | Standardized jailbreak eval | 100 harmful + 100 benign behaviors | MIT (HF page + canonical repo, both read) | [card](cards/10-jailbreakbench.md) |
| 11 | HarmBench | Automated red teaming | framework + 400 text behaviors (200/100/100) | MIT (canonical repo) | [card](cards/11-harmbench.md) |
| 12 | WildChat | Real user–assistant traffic | 650K → 1M → 3.2M conversation releases | ODC-BY (1M release, 2024-06-26) | [card](cards/12-wildchat.md) |
| 13 | SafetyBench | Multi-category safety MCQ | 11,435 questions, EN+ZH | MIT (canonical repo) | [card](cards/13-safetybench.md) |
| 14 | OR-Bench | Over-refusal (exaggerated safety) | 80,000 prompts, 10 categories + ~1,000 hard + 600 toxic | CC-BY-4.0 (both HF hostings) | [card](cards/14-or-bench.md) |
| 15 | WildJailbreak | Adversarial safety training | 262K vanilla + adversarial pairs | ODC-BY (HF page) | [card](cards/15-wildjailbreak.md) |
| 16 | WMDP | Hazardous-knowledge proxy | 3,668 MCQ (bio/cyber/chem) | MIT (HF page) | [card](cards/16-wmdp.md) |
| 17 | HaluEval | Hallucination recognition | 35K samples (5K general + 3x10K tasks) | apache-2.0 (HF mirror) | [card](cards/17-halueval.md) |
| 18 | SimpleQA | Short-form factuality | 4,326 questions, 10 topics | repo MIT; data-file license unstated | [card](cards/18-simpleqa.md) |
| 19 | CrowS-Pairs | Stereotype pairs (masked-LM bias) | 1,508 pairs, 9 bias types | CC BY-SA 4.0 (README statement) | [card](cards/19-crows-pairs.md) |
| 20 | Winogender Schemas | Gender-bias coreference probe | 120 templates -> 720 sentences | MIT (canonical repo) | [card](cards/20-winogender.md) |
| 21 | MMLU | General-capability anchor | 57 tasks; test 14,042 | MIT (HF page) | [card](cards/21-mmlu.md) |
| 22 | GSM8K | General-capability anchor (reasoning) | 8.5K abstract / 8,792 artifact | MIT (canonical repo) | [card](cards/22-gsm8k.md) |

## Curriculum integration map

Where each dataset is *used by the course* (unit → datasets → role):

| Unit | Datasets used | Role in that unit |
|------|---------------|-------------------|
| Ch.02 Evaluation science | all 13 core (01-13) | construct-validity worked examples; contamination, denominator, and adaptive-overfitting discussions use the real composition numbers above |
| Ch.04 Preference learning | BeaverTails, HH-RLHF | label-quality audit material: annotation dimensions, preference-pair structure |
| Ch.06 Honesty & calibration | TruthfulQA | truthfulness construct; MC scoring; abstention behavior |
| Ch.12 Adversarial ML | AdvBench | gradient-based suffix attack target set; ASR metric construction |
| Ch.15 Red teaming | XSTest, AdvBench, JailbreakBench, HarmBench | benign controls, explicit denominators, adaptive evaluation discipline |
| Ch.16 Privacy & provenance | WildChat | real-user-data ethics, de-identification limits, license archaeology (Ai2 Impact License → ODC-BY) |
| Ch.21 Sociotechnical risk | BOLD, BBQ, ToxiGen | bias constructs: disparity, ambiguity, implicit vs explicit toxicity |
| Ch.23 Governance | SafetyBench | multi-category MCQ coverage in two languages as a governance-mapped evaluation |
| P01 Evaluation harness | TruthfulQA, XSTest | runner cases with transparent scoring; scorer-validation examples |
| P03 Calibration & abstention | TruthfulQA | free-response scoring limitations; selective-prediction curves |
| P07 Injection defense | JailbreakBench behaviors | held-out attack cases and benign-controls design (metadata only; no redistribution) |
| P09 Shift & subgroups | BOLD, BBQ | subgroup tables; worst-group reasoning with real category structure |

This map is also the honest statement of scope: no dataset is *executed* in
this repository yet (project code lands in P01 onward); the catalog is the
research layer that later projects cite.

## Usage and licensing policy

- **We never redistribute dataset content.** Cards carry metadata and
  structure only. Harmful-content datasets (AdvBench, JBB-Behaviors,
  HarmBench, BeaverTails) are described at the category level; no harmful
  prompts are reproduced in this repository.
- **BeaverTails is CC BY-NC 4.0** — non-commercial. Any course project that
  uses it must remain evaluation/research use, and the project's own MIT
  license must never imply relicensing of upstream data.
- **License statements are dated observations.** "License (as observed)"
  columns record what the named page displayed on the verification date.
  Before any real use, re-check the canonical source; licenses do change
  (WildChat's 2024-06-26 ODC-BY change, recorded in its card, is the
  worked example of exactly this).
- Dataset text and model outputs are **untrusted data** under
  [AGENTS.md](../AGENTS.md): they are never treated as instructions.

## Pending-verification queue

Datasets we consider important but which were **not verified in this round**
(2026-10-21 web-verification budget was finite; recorded at `metadata-only`
level until inspected). The 2026-10-23 rounds verified every item below that
had been queued — the queue is now **empty**; new entries appear here only
when a future unit names a dataset it cannot yet verify:



Resolved 2026-10-23 (moved out of this queue by direct verification, recorded
in the cards and catalog): ToxiGen license (MIT text, Microsoft copyright,
upstream repo — HF-page scope caveat recorded); BBQ canonical license
(CC-BY-4.0, canonical repository); HarmBench license (MIT) and behavior-set
composition (400/200/100/100 by direct CSV read); SafetyBench license (MIT);
AdvBench direct LICENSE read (MIT, llm-attacks repo); JailbreakBench repo
license confirmation (MIT).

Also verified 2026-10-23 and promoted to full cards (DS-014..DS-018): OR-Bench
(paper abstract + both HF hostings; org-name discrepancy recorded); WildJailbreak
(WildTeaming paper abstract + HF page; 262K pairs, ODC-BY); WMDP (paper abstract
+ HF page; 3,668 MCQ, MIT); HaluEval (paper abstract + canonical README + mirror
page; 35K composition); SimpleQA (paper abstract + simple-evals repo + canonical
CSV parsed directly; 4,326 questions with topic distribution).

Also verified 2026-10-23 (DS-019..DS-022, completing the queue): CrowS-Pairs
(1,508 pairs; CC BY-SA 4.0 from the README statement with ROCStories+MNLI seed
provenance); Winogender (120 templates -> 720 sentences with the authors' PPV
interpretation rule; MIT); MMLU (57 tasks; test 14,042 / validation 1,531 / dev
285 / auxiliary_train 99,842); GSM8K (8.5K-abstract vs 8,792-artifact documented
discrepancy; MIT).

Adjacent datasets observed at page level during verification (recorded so the
next round does not have to rediscover them): lmsys/toxic-chat (10K annotated
Vicuna-demo prompts), walledai/JailbreakHub (15,140 jailbreak prompts
collected Dec 2022–Dec 2023 from Reddit, Discord, websites, and open datasets),
thu-coai/Agent-SafetyBench (agent-safety environments, Dec 2024),
ucf-crcv/BBQ-V (14,144 image-question pairs, visual stereotypes).

## Card index

1. [TruthfulQA — truthfulness under imitative falsehoods](cards/01-truthfulqa.md)
2. [BOLD — bias in open-ended generation](cards/02-bold.md)
3. [RealToxicityPrompts — toxicity propensity of prompts](cards/03-real-toxicity-prompts.md)
4. [ToxiGen — machine-generated implicit toxicity with benign counterfactuals](cards/04-toxigen.md)
5. [BBQ — stereotype bias in question answering](cards/05-bbq.md)
6. [XSTest — exaggerated safety / over-refusal](cards/06-xstest.md)
7. [BeaverTails — safety-annotated prompt–response pairs (non-commercial)](cards/07-beavertails.md)
8. [HH-RLHF — preference pairs from a production assistant](cards/08-hh-rlhf.md)
9. [AdvBench — harmful-behavior targets for adversarial attacks](cards/09-advbench.md)
10. [JailbreakBench — an open, standardized jailbreak benchmark](cards/10-jailbreakbench.md)
11. [HarmBench — standardized automated red teaming](cards/11-harmbench.md)
12. [WildChat — real user traffic at three scales](cards/12-wildchat.md)
13. [SafetyBench — bilingual multi-category safety MCQ](cards/13-safetybench.md)
14. [OR-Bench — large-scale over-refusal measurement](cards/14-or-bench.md)
15. [WildJailbreak — open adversarial safety training data](cards/15-wildjailbreak.md)
16. [WMDP — hazardous-knowledge proxy and unlearning benchmark](cards/16-wmdp.md)
17. [HaluEval — hallucination recognition benchmark](cards/17-halueval.md)
18. [SimpleQA — short-form factuality with abstention grading](cards/18-simpleqa.md)
19. [CrowS-Pairs — stereotype pairs for masked-LM bias](cards/19-crows-pairs.md)
20. [Winogender — gender-bias coreference probe](cards/20-winogender.md)
21. [MMLU — multitask knowledge anchor](cards/21-mmlu.md)
22. [GSM8K — grade-school reasoning anchor](cards/22-gsm8k.md)
