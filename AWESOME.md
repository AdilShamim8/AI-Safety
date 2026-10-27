# AWESOME — the annotated resource index

A map, not a link dump. Every entry below is **registered, dated, and
access-leveled** in the [source register](research/source-register.yaml);
the bracketed ID is your audit trail — click through to see exactly what
was fetched, when, and how far into it this course actually read. The
[evidence ladder](index.html) shows the whole corpus at a glance.

And every line now carries its live link, verified — not
assumed. Across its rotations — 3 (2026-10-25) and 4 (2026-10-27,
the lecture-library opening) —
[scripts/verify_links.py](scripts/verify_links.py) fetched all 94
URLs cited on this page: the arXiv spine title-matched against the
arXiv API, the course videos and playlists against YouTube's oEmbed
and playlist endpoints, the rest fetched server-side. All
94 live — three hosts (OWASP, the American Bar Association,
ACM) bot-block datacenter clients while remaining real pages the
register corroborates, and exactly one URL is deliberately not
linked: the OpenAI Preparedness announcement, whose canonical 404
is recorded in the register. The runs are recorded as rotations 3
and 4 in [MAINTENANCE.md](MAINTENANCE.md).

How to read the annotations: each line says what the source is FOR —
the load-bearing idea a chapter or project takes from it — not a
generic summary. Where a source's honest access level matters (vendor
white paper, self-reported program data), the annotation says so.

The index is organized in media layers: the **video library** and the
**blogs and ongoing commentary** (the living layers, opened 2026-10-25),
then the paper spine's ten thematic sections, then the datasets,
courses and on-ramps, note companions, incidents, and career data.
The closing section states the extension discipline — the price of
admission for every new line in this file.

## The video library (watching tracks)

Videos carry the same register discipline as papers: every channel
below was opened at page level on 2026-10-25 (handle, description,
counts as displayed), every entry records what was and was not
inspected, and no spoken video content is quoted anywhere in this
repository. Subscriber and view counts are perishable display values,
not archival facts — the register prices them accordingly.

Four tracks, each with a job:

- **From-scratch and foundations** — the build-it-yourself lineage:
  - **[Andrej Karpathy's channel](https://www.youtube.com/@AndrejKarpathy)**
    [SRC-VIDEO-003] — "Let's build GPT: from scratch, in code, spelled out"
    and "Deep Dive into LLMs like ChatGPT" (the full chapter list is in the
    register): the video companion of the from-scratch researcher track —
    the same tokenization → transformer → post-training arc, taught at full
    scale by a founding OpenAI member.
  - **[3Blue1Brown's neural-networks series](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)**
    [SRC-VIDEO-004] — the visual-intuition layer for transformer mechanics
    (Deep Learning chapters 5–6, April 2024 lesson dates at fetch); what to
    watch before Chapter 09 if the residual stream still feels abstract.
  - **[The from-scratch video course](https://www.youtube.com/watch?v=44l-xL7OKLo)**
    [SRC-VIDEO-001] — Vuk Rosić's full course (the owner-selected mechanics
    track), with its MIT
    [companion repository](https://github.com/vukrosic/zero-to-ai-researcher)
    [SRC-REPO-001].
- **Safety explainers** — the vocabulary on-ramp:
  - **[Rob Miles AI Safety](https://www.youtube.com/@RobertMilesAI)**
    [SRC-VIDEO-002] — the dedicated explainer channel (about 174,000
    subscribers at the 2026-10-25 fetch); the field's common vocabulary,
    explained for everyone, before Chapter 01's risk models demand it.
  - **[Computerphile's Artificial Intelligence with Rob Miles playlist](https://www.youtube.com/playlist?list=PLzH6n4zXuckquVnQ0KlMDxyT5YE-sA8Ps)**
    [SRC-VIDEO-010] — where that explainer lineage began (University of
    Nottingham); the early videos that introduced a generation to alignment
    vocabulary.
- **Paper explainers and technical talk** — walkthroughs and
  interviews:
  - **[Yannic Kilcher's channel](https://www.youtube.com/c/YannicKilcher)**
    [SRC-VIDEO-005] — long-form paper walkthroughs; watch alongside — never
    instead of — reading the paper spine below.
  - **[AI Coffee Break with Letitia](https://www.youtube.com/c/aicoffeebreak)**
    [SRC-VIDEO-008] — bite-sized current-paper explainers (NLP and
    multimodal focus).
  - **[Machine Learning Street Talk](https://www.youtube.com/@MachineLearningStreetTalk)**
    [SRC-VIDEO-006] — the long-form technical interview channel; the video
    analogue of the note companions' method-level discussions.
- **Frontier coverage and lab channels** — the release-cycle layer:
  - **[AI Explained](https://www.youtube.com/@aiexplained-official)**
    [SRC-VIDEO-007] — frontier-release commentary, priced as
    news-and-frames: useful for orienting to the release cycle Chapter 20
    teaches you to audit, never as evidence.
  - **[Anthropic's channel](https://www.youtube.com/@anthropic-ai)**
    [SRC-VIDEO-009] — the vendor's own research-communication layer,
    including its reward-hacking explainer; institutional self-presentation,
    priced exactly like the
    [RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)
    [SRC-REPORT-008].

- **Full courses — the structured programs** (the
  [lecture library](courses/README.md)'s deep end):
  - **[Harvard CS 2881 — the AI Safety lecture playlist](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W)**
    [SRC-VIDEO-011] — Boaz Barak's graduate research seminar (Fall 2025
    and Fall 2026 iterations), 19 recorded lectures, each built on
    primary-source readings, a working guest, and a live student
    experiment. The course's own schedule pages
    ([SRC-CURR-012]) were read in full and registered; the companion
    ([courses/boaz-barak-cs2881/](courses/boaz-barak-cs2881/)) carries
    the complete video index, all 18 lecture companion notes, and the
    course's published reading lists reproduced as attribution.

  - **[The Google DeepMind AGI Safety Course](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)**
    [SRC-VIDEO-013] — the frontier lab's own ~85-minute statement of
    the alignment problem and its candidate answers: 16 parts in three
    bands (risk model with exercises; the alignment research program;
    institutions), verified via the playlist API and priced as a lab's
    self-description. The companion
    ([courses/google-deepmind-agi-safety/](courses/google-deepmind-agi-safety/))
    carries all 16 part notes and the pedagogy analysis.

## Blogs and ongoing commentary

Papers are the spine; blogs are the living layer — where the field
argues between publications, where practitioners report attacks
before any venue exists, and where measurement institutes publish
the trend lines the chapters lean on. Registered and priced like
everything else here: hubs are hubs, arguments are arguments, and
vendor-adjacent authors say so in the register entry.

- **[AI Alignment Forum](https://www.alignmentforum.org)** [SRC-BLOG-001] —
  the research hub where several register papers debuted as posts; read it
  for the current state of the argument, cite the paper version.
- **[LessWrong](https://www.lesswrong.com)** [SRC-BLOG-002] — the parent
  community (founded by Yudkowsky, 2009) the Alignment Forum layers on;
  rationality technique and AI-risk argument developed together here.
  Discourse, not evidence — the register says so.
- **[Simon Willison's prompt-injection series](https://simonwillison.net/series/prompt-injection/)**
  [SRC-BLOG-003] — the longest-running practitioner record of Chapter 13's
  attack class, from the first public demonstrations (September 2022)
  through the agent-security pattern posts (163 tagged posts at the
  2026-10-25 fetch); the living layer on the chapter's paper spine.
- **[Interconnects](https://www.interconnects.ai)** [SRC-BLOG-004] — Nathan
  Lambert's post-training practice layer for Chapter 04:
  state-of-post-training surveys and open-recipe analysis, from the author
  of the field's post-training textbook-in-progress.
- **[Lil'Log](https://lilianweng.github.io)** [SRC-BLOG-005] — Lilian Weng's
  survey-length technical posts: "Adversarial Attacks on LLMs" (2023-10-25)
  for Chapter 13, "Extrinsic Hallucinations in LLMs" (2024-07-07) for
  Chapter 06 — each a bridge between the chapter text and the primary
  papers.
- **[Cold Takes](https://www.cold-takes.com)** [SRC-BLOG-006] — Holden
  Karnofsky's "most important century" argument (2021): the canonical
  timelines position, taught here as a position to steelman and audit, not a
  consensus.
- **[Epoch AI](https://epoch.ai)** [SRC-BLOG-007] — the training-compute
  measurement source (frontier compute at 5× per year since 2020, at fetch);
  the empirical layer under Chapter 20's scaling arithmetic.
- **[Redwood Research blog](https://blog.redwoodresearch.org)**
  [SRC-BLOG-008] — the safety lab's own commentary on those same trends (its
  4.5×-per-year reading and the slope dispute it argues); the lab behind the
  [control paper](https://arxiv.org/abs/2312.06942) [SRC-PAPER-022].

## The paper spine (research papers)

The ten thematic sections below hold the 148 registered papers — 142
carrying arXiv URLs, every one of them title-verified against the
arXiv API in the final verification pass (zero mismatches). They are
organized by the job the field's literature does for this course,
not by venue or year; the note companions turn the load-bearing
subset into runnable analysis. How to add more papers — the register
route, the verification route, the note route — is the closing
section of this file.

## The methodological spine

- **[Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565)**
  [SRC-PAPER-001] — the field's five-problem decomposition (reward hacking,
  exploration, robustness, oversight, side effects) that Chapter 01's risk
  models build on.
- **[Risks from Learned Optimization](https://arxiv.org/abs/1906.01820)**
  [SRC-PAPER-002] — mesa-optimization and the specification–optimization
  gap; the vocabulary for every "the model learned something else" analysis
  in Ch.03.
- **[Defining and Characterizing Reward Hacking](https://arxiv.org/abs/2209.13085)**
  [SRC-PAPER-006] and
  **[The Effects of Reward Misspecification](https://arxiv.org/abs/2201.03544)**
  [SRC-PAPER-007] — the Goodhart taxonomy and the misalignment-mapping
  methodology behind P02's model organisms.
- **[The Benchmark Lottery](https://arxiv.org/abs/2107.07002)**
  [SRC-PAPER-105] — why leaderboard claims need their gap×n arithmetic; the
  chapter's flip-probability drill.
- **[Position: Embracing Negative Results in ML](https://arxiv.org/abs/2406.03980)**
  [SRC-PAPER-107] — the report structure Ch.24 requires of the capstone's
  honest halves.

## Preference learning and post-training

- **[InstructGPT](https://arxiv.org/abs/2203.02155)** [SRC-PAPER-009] — the
  RLHF pipeline (SFT → reward model → PPO) Ch.04 dissects, including its own
  stated limitations.
- **[DPO](https://arxiv.org/abs/2305.18290)** [SRC-PAPER-010] — the
  closed-form derivation the chapter carries end-to-end and P04 audits at
  the seam.
- **[Constitutional AI](https://arxiv.org/abs/2212.08073)** [SRC-PAPER-011]
  — RLAIF's two-phase recipe and the feedback-vs-oversight distinction.
- **[PPO](https://arxiv.org/abs/1707.06347)** [SRC-PAPER-070] — the
  surrogate objective mechanics, verified at abstract level with the
  general-RL scope priced honestly.
- **[HH-RLHF](https://arxiv.org/abs/2204.05862)** [SRC-PAPER-071] +
  **[BeaverTails](https://arxiv.org/abs/2307.04657)** [SRC-PAPER-072] — the
  preference datasets P04's label-quality audit leans on (cards in the
  [dataset catalog](datasets/catalog.yaml)).

## Oversight, uncertainty, and truthfulness

- **[Weak-to-Strong Generalization](https://arxiv.org/abs/2312.09390)**
  [SRC-PAPER-013] — the oversight gap P05 reproduces as a deterministic
  analogue.
- **[Measuring Progress on Scalable Oversight](https://arxiv.org/abs/2211.03540)**
  [SRC-PAPER-014] and
  **[AI Safety via Debate](https://arxiv.org/abs/1805.00899)**
  [SRC-PAPER-015] — the two oversight paradigms comparison note C03
  adjudicates.
- **[Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221)**
  [SRC-PAPER-016] and
  **[Teaching Models to Express Uncertainty in Words](https://arxiv.org/abs/2205.14334)**
  [SRC-PAPER-017] — the logit vs verbalized confidence channels of Ch.06;
  the second is the spoofable one.
- **[Towards Understanding Sycophancy](https://arxiv.org/abs/2310.13548)**
  [SRC-PAPER-018] — preference pipelines training in flattery; Ch.06's
  pressure mechanism.
- **[TruthfulQA](https://arxiv.org/abs/2109.07958)**
  [SRC-PAPER-073; dataset card DS-001] — imitative falsehoods as a
  construct-validity worked example.

## Deception evidence (the skeptical canon)

- **[Sleeper Agents](https://arxiv.org/abs/2401.05566)** [SRC-PAPER-019] —
  persistence of deceptive behavior through safety training; the
  constructed-organism evidence class.
- **[Alignment Faking](https://arxiv.org/abs/2412.14093)** [SRC-PAPER-020] —
  conditional compliance statistics (the 14%-in-context vs 78%-after-RL
  pair) and what they do and do not show.
- **[AI Sandbagging](https://arxiv.org/abs/2406.07358)** [SRC-PAPER-021] —
  strategic underperformance on evaluations; the gameability limit of
  benchmarks.
- **[AI Control](https://arxiv.org/abs/2312.06942)** [SRC-PAPER-022] +
  **[Evaluating Control Protocols](https://arxiv.org/abs/2511.02997)**
  [SRC-PAPER-023] +
  **[Adaptive Attacks on Trusted Monitors](https://arxiv.org/abs/2510.09462)**
  [SRC-PAPER-024] — the control paradigm Ch.08 teaches and P08 implements
  (the monitor's recall is the safety ceiling).

## Interpretability

- **[A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html)**
  [SRC-PAPER-025] — the residual stream / QK-OV / MLP decomposition Ch.09 is
  built on.
- **[Causal Mediation Analysis](https://arxiv.org/abs/2004.12265)**
  [SRC-PAPER-027] — the TE/IE/DE formalism behind activation patching.
- **[Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features)**
  [SRC-PAPER-030] and
  **[Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)**
  [SRC-PAPER-032] — dictionary learning and the feature-splitting story (the
  San Francisco 1→2→11 example, verified verbatim).
- **[Refusal Is Mediated by a Single Direction](https://arxiv.org/abs/2406.11717)**
  [SRC-PAPER-037] — the refusal direction Ch.11's steering audit re-prices
  with full intervals.
- **[Probing Classifiers: Promises, Shortcomings, Advances](https://arxiv.org/abs/2102.12452)**
  [SRC-PAPER-039] — why readout ≠ causation (P06's opening move).
- **[Faithfully Interpretable NLP Systems](https://arxiv.org/abs/2004.03685)**
  [SRC-PAPER-034] — faithfulness vs plausibility, the Ch.10 evidence
  standard.

## Adversarial ML and defense evaluation

- **[Intriguing Properties](https://arxiv.org/abs/1312.6199)**
  [SRC-PAPER-040] +
  **[Explaining and Harnessing](https://arxiv.org/abs/1412.6572)**
  [SRC-PAPER-046] — the founding transfer and linear-explanation results.
- **[BadNets](https://arxiv.org/abs/1708.06733)** [SRC-PAPER-042] —
  supply-chain poisoning with the 25%-accuracy-drop trigger; the backdoor
  archetype.
- **[Membership Inference](https://arxiv.org/abs/1610.05820)**
  [SRC-PAPER-041] +
  **[Stealing Models via Prediction APIs](https://arxiv.org/abs/1609.02943)**
  [SRC-PAPER-043] — the privacy/extraction pair Ch.12 and Ch.16 use.
- **[Carlini-Wagner](https://arxiv.org/abs/1608.04644)** [SRC-PAPER-044] —
  the 100%-vs-claimed-0.5% distillation autopsy; defense evaluation's
  founding failure.
- **[Reliable Evaluation of Adversarial Robustness](https://arxiv.org/abs/2003.01690)**
  [SRC-PAPER-047] and
  **[On Evaluating Adversarial Robustness](https://arxiv.org/abs/1902.06705)**
  [SRC-PAPER-048] — the ensemble/50+-model audits that make "our defense
  works" a testable claim.

## LLM application and agent security

- **[Not What You've Signed Up For](https://arxiv.org/abs/2302.12173)**
  [SRC-PAPER-050] — Greshake's indirect injection taxonomy; the Ch.13
  backbone.
- **[Ignore Previous Prompt](https://arxiv.org/abs/2211.09527)**
  [SRC-PAPER-051] — goal hijacking and prompt leaking as named classes.
- **[The Instruction Hierarchy](https://arxiv.org/abs/2404.13208)**
  [SRC-PAPER-052] — privileged-instruction training, honestly priced
  (same-channel defense).
- **[Spotlighting](https://arxiv.org/abs/2403.14720)** [SRC-PAPER-053] —
  delimiter defenses with measured ASR (the >50%→<2% pricing Ch.13 carries).
- **[Defeating Prompt Injections by Design](https://arxiv.org/abs/2503.18813)**
  [SRC-PAPER-054] — Dual LLM and CaMeL; the architecture-level boundary
  family.
- **[AgentDojo](https://arxiv.org/abs/2406.13352)** [SRC-PAPER-055] +
  **[LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817)**
  [SRC-PAPER-056] — agent attack surfaces and the ToolEmu-style evaluation
  topology behind P07/P10 fixtures.
- **[Programming Semantics for Multiprogrammed Computations](https://cacm.acm.org/research/programming-semantics-for-multiprogrammed-computations-2/)**
  [SRC-PAPER-057] — Dennis & Van Horn 1966: capabilities as the
  still-correct vocabulary for tool calls.
- **[OWASP LLM Top 10 (2025)](https://genai.owasp.org/llm-top-10/)**
  [SRC-REPORT-004] — the industry risk index Ch.13 maps onto (page-verified
  at the listed version).

## Red teaming

- **[Red Teaming Language Models to Reduce Harms](https://arxiv.org/abs/2209.07858)**
  [SRC-PAPER-058] — 38,961 released attacks and the human-scaling trend.
- **[Red Teaming with Language Models](https://arxiv.org/abs/2202.03286)**
  [SRC-PAPER-059] — LM-vs-LM attack generation.
- **[Explore, Establish, Exploit](https://arxiv.org/abs/2306.09442)**
  [SRC-PAPER-060] — from-scratch red teaming and the marginal-value
  inversion.
- **[XSTest](https://arxiv.org/abs/2308.01263)**
  [SRC-PAPER-003; dataset DS-006] — over-refusal as a safety failure of the
  second kind; the 250/200 structure the chapter's benign controls mirror.

## Reasoning, release, and governance

- The CoT-faithfulness set Ch.18 uses: [SRC-PAPER-083..087] —
  plausibility-vs-faithfulness, the monitorability tax, the oversight
  flip, self-instructed evasion; two at high-recency honesty.
- **[Evaluating Frontier Models for Dangerous Capabilities](https://arxiv.org/abs/2403.13793)**
  [SRC-PAPER-094] — the evaluation-suite approach to release gates Ch.20
  builds its release discipline on.
- **[Are Emergent Abilities a Mirage?](https://arxiv.org/abs/2304.15004)**
  [SRC-PAPER-095] — why emergent-capability claims need the scaling curves
  under them; the metric-choice lesson of Ch.20.
- **[Anthropic RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)**
  [SRC-REPORT-008] and **OpenAI Preparedness**
  [SRC-REPORT-009, with its 404 recorded] — the labs' own frameworks,
  fetched at page level where they were reachable.
- **[NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework)**
  [SRC-REPORT-010] — the four functions Ch.23 maps with citation forensics
  (JS-rendering honesty noted).
- **[MITRE ATLAS](https://atlas.mitre.org/)** [SRC-REPORT-011] — the
  adversarial knowledge base, pinned at fetch (16/208/40/73 counts,
  living-database caveat).
- **[EU AI Act](https://artificialintelligenceact.eu/implementation-timeline/)**
  [SRC-REPORT-012] — the timeline arithmetic (Annex III 405 days, Annex I
  649 days out at verification date) Ch.23 teaches as phase-in discipline.

## The dataset catalog (43 verified cards)

Not repeated here — the cards ARE the annotation:
[datasets/catalog.yaml](datasets/catalog.yaml). Each card traces every
composition number to the URL it was collected from, with license and
contamination status. Start with TruthfulQA [DS-001], AdvBench
[DS-009], and XSTest [DS-006] — the three the projects use most.

## Courses, fellowships, and the from-scratch track

- **[ARENA curriculum](https://www.arena.education/curriculum)**
  [SRC-CURR-001] — the ML-engineer-side safety curriculum this course's
  prerequisites are calibrated against.
- **The from-scratch researcher track**
  (research/ai-researcher-from-scratch/) — the owner-selected mechanics
  track, distilled into 7 module notes with runnable stdlib code; its
  [video course](https://www.youtube.com/watch?v=44l-xL7OKLo)
  [SRC-VIDEO-001] is indexed in the video library above, with the
  [companion repository](https://github.com/vukrosic/zero-to-ai-researcher)
  [SRC-REPO-001].
- **[MATS](https://matsprogram.org)** [SRC-CURR-006] — the alignment
  fellowship (12 weeks, Berkeley/London; self-reported outcomes priced as
  such in the register).
- **[80,000 Hours AI hub](https://80000hours.org/ai)** [SRC-CURR-005] —
  entry paths, advising, the 900+-role board; the careers index's structure
  source.
- **BlueDot Impact** (named on the 80k hub [SRC-CURR-005]) — free
  entry-level courses; the community on-ramp.
- **[AI Safety Camp](https://www.aisafety.camp)** [SRC-CURR-009] — the
  team-based project on-ramp: ten editions by 2025, join as project lead or
  team member, 10 hours/week for 3 months, fully online; its stated
  screening rule — rejecting projects whose capability acceleration
  outweighs their safety value — is itself a working example of the caution
  the field teaches.
- **[AISafety.info (Stampy)](https://aisafety.info)** [SRC-CURR-010] — Rob
  Miles's community-maintained FAQ wiki with a chatbot front end; the
  first-questions on-ramp for newcomers (community-maintained, priced as
  such).
- **[Neel Nanda's interpretability getting-started guide](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher)**
  [SRC-CURR-011] — the practitioner path beyond Chapters 09–11: pick a
  paper, load the model, re-run the analysis — the same loop the chapter
  exercises teach at toy scale, at research scale.

## The note companions (start from the map, land in the notebook)

The research notebook now carries 74 paper notes and 12 comparison
notes — each anchored to a register source at the level the access
supports, each ending in a falsifiable extension runnable at course
scale. The fastest way in: the chapter you are reading names its
note companions in the readings section; the full index is
[research/notes/README.md](research/notes/README.md). The notes added
in the milestone session: CaMeL (21 — the boundary that moved
out of the model), AgentDojo (22 — the environment as the
instrument), Sandbagging (23 — the evaluation channel's gameability),
Explore-Establish-Exploit (24 — red teaming as method), DPO (25 — the
reparameterization), InstructGPT (26 — the pipeline), Debate (27 —
the optimality assumption), Sycophancy (28 — the preference pipeline),
Mirage (29 — metric choice manufactures thresholds), Constitutional
AI (30 — supervision in a document), GCG (31 — the optimized attack),
Verbalized confidence (32 — the trained channel), plus comparison C06
(safety cases vs red-team reports — assurance's two documents). The
judged-deepening session then added the load-bearing spine of the
field — notes 33–74, from Concrete Problems (33) and Othello-GPT (34)
through the adversarial quartet (71 FGSM, 72 universal perturbations,
73 HotFlip, 74 ensemble training), including the oversight family
(sandbagging's cousins: reward tampering, power-seeking, CIRL), the
memorization family (Secret Sharer, extraction, the memorization
laws), the defense family (randomized smoothing, TRADES), and the
scale family (double descent, scaling laws) — plus comparisons
C07–C12, each settling a practitioner decision a single paper leaves
open (factuality instrument pairs, the one-bit jailbreak diagnostic,
budgeting drift, response postures, drift instruments, supply
strategies).

## The incident record

14 incidents reviewed under the strict template across four eras
([notes/incidents/](research/notes/incidents/README.md)): the
liability-and-authority era ([Air Canada
liability](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot)
[SRC-REPORT-013],
[DPD release regression](https://www.bbc.com/news/technology-68025677)
[SRC-REPORT-014],
[Chevy commitment authority](https://nhimg.org/chevrolet-dealer-chatbot-prompt-injection-2023-1-dollar-tahoe)
[SRC-REPORT-015/016]); the rollout-and-channel era (AI Overviews, NYC
MyCity, Cursor, Slack exfiltration, Samsung pastes); the history era (Bing's
prompt disclosure, Tay, Sydney); and the accountability era (Galactica's
withdrawal, the EEOC's first AI-bias settlement, Amazon's scrapped
recruiter) — every addition page-inspect-gated, registers
SRC-REPORT-013..041. [The AI Incident Database](https://incidentdatabase.ai)
[SRC-REPORT-015's host] is the field-wide record this collection grows from
— cite entries by ID with fetch dates.

## Career market data (perishable — re-verify before deciding)

- **[AISafety.com jobs board](https://aisafety.com/jobs)** [SRC-CURR-007] —
  553 roles at fetch (2026-10-25), employer-disclosed salary examples
  included.
- **[SANS AI cybersecurity careers white paper](https://www.sans.org/white-papers/sans-ai-cybersecurity-careers-guide)**
  [SRC-CURR-008] — the four titles hiring today, from 10,643 postings;
  vendor-mapped to its own curriculum (the caveat is the lesson).
- Both live in [roadmaps/careers-index.md](roadmaps/careers-index.md)
  with per-claim provenance and the five-rung progress ladder.

## How to extend this index

The discipline that keeps this file a map instead of a link dump.
Every rule below is enforced by the repository's own gates — the
audit fails on unregistered IDs, the count-drift tests fail on stale
numbers, and the validator fails on schema gaps.

1. **Register first, annotate second.** A new video, channel, blog,
   paper, or resource enters as a full
   [source-register.yaml](research/source-register.yaml) entry — all
   fourteen fields — and only then gets its line here, carrying the
   bracketed ID. The audit's cross-reference check guarantees no ID
   appears in prose without a register entry behind it.
2. **Open the page, date the look, level the access.** Channels at
   `page-inspected` means the channel page was actually seen (handle,
   description, counts as displayed) — record what was inspected and
   what was not. Blogs at `page-inspected` means the post listing was
   read. Papers enter at `abstract-read` minimum, with the arXiv API
   title match recorded. Perishable numbers (subscribers, post counts,
   open roles) always carry their fetch date.
3. **Annotate the job, not the subject.** One sentence on what the
   source is FOR — which track, chapter, or project leans on it and
   for which load-bearing idea. A generic summary is a rejection.
4. **Price the honesty in the line itself.** Vendor channels are
   institutional self-presentation; community wikis are
   community-maintained; argued positions are argued positions; the
   annotation says which, the same way the register does.
5. **Run the gate before committing.** `python scripts/validate_repo.py .`,
   `python scripts/audit_missing.py`, `pytest`, `ruff`, `black` — and
   regenerate the dashboard (`python scripts/build_dashboard.py`)
   whenever the registers changed, because the website renders
   register-derived counts.
   Since the link layer opened (2026-10-25), one more gate
   stands in front of every new link:
   `python scripts/verify_links.py --ids <the-new-ID>` must
   return LIVE before the URL enters this file — liveness AND
   page identity (the title the page serves is the title the
   register claims), not just a well-formed URL.

What never enters: unregistered or unverified links, resource-list
listicles, anything not opened at page level by the person adding it, and
any number without a fetch date attached.
