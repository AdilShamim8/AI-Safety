# Reference article map

Maps the repository owner's reference article — [AI Safety: From First Principles
to Practice](https://adilshamim8.medium.com/ai-safety-from-first-principles-to-practice-73ccd3ea73a0)
by Adil Shamim — to the modules of this course, records what was actually read, and
states the relationship precisely.

**Status of this document:** verified against a live fetch on 2026-10-21.

## Access record (what was actually read)

- **When:** 2026-10-21, via automated full-text fetch of the article URL.
- **Paywall:** none encountered at fetch time. (Note: the project brief prepared on
  2026-10-20 recorded full-text access as blocked during preparation, so access
  status appears session-dependent. Both facts are recorded rather than reconciled
  by assumption.)
- **Sections actually read:** the introduction ("How to work through this article"),
  all eleven numbered sections (1–11), and both closing resource lists ("Book shelf"
  and "Courses, curricula, and practical references").
- **Not retrieved:** a closing/conclusion section was not visible in the fetched
  portion; the page continued beyond the retrieved content. Nothing in this map
  relies on an unretrieved conclusion.
- **Publication date:** the platform displayed a relative timestamp ("47 min read ·
  23 hours ago" at fetch time), which places publication on **2026-10-20** at day
  precision. Treated as approximate; recorded in the source register as such.

## Relationship statement

The article is the repository owner's own synthesis and the inspiration for this
course's structure. It is treated as **inspiration and framing, not as independent
validation** of any technical claim made in this repository. No lengthy passages are
reproduced here, and no assumption is made about the article's reuse license: the
article text remains under Medium's platform terms. Where this repository states a
technical fact, it cites primary sources in `research/source-register.yaml`, not the
article.

## Theme-to-module map

| # | Article section (as read) | Repository module(s) | Relationship |
|---|---|---|---|
| — | How to work through this article | `START_HERE.md`, `ROADMAP.md` | Navigation intent; the course replaces "read linearly" with dependency-aware routes and artifact-based exit criteria |
| 1 | Safety is a claim about a system in a situation | Ch. 01 Risk models; Ch. 22 Safety engineering and assurance | The article's context-relative definition ("in this workflow, with these permissions, evidence supports keeping these risks below stated limits") is formalized here into threat models, assurance claims, and safety cases with claim–evidence–assumption–rebuttal structure |
| 2 | Learn to recognize different kinds of evidence | Ch. 01; Ch. 02 Evaluation science; `research/research-method.md` | The article's six evidence kinds (incidents, controlled experiments, formal results, benchmarks, forecasts, ethical judgments) align with the course's evidence-hierarchy work; the course adds the claim-level citation infrastructure the article implies but does not carry |
| 3 | What training gives us, and what it does not | Ch. 03 Specification; Ch. 04 Preference learning and post-training | The "two gaps" framing (training objective vs. desired behavior; model-as-component vs. deployed system) recurs as the spine of chapters 03–04 and the deployment chapters 17 and 22 |
| 4 | Map the risks before choosing a solution | Ch. 01; Ch. 20 Misuse and dangerous capabilities; Ch. 21 Sociotechnical and systemic risk | The article surveys catastrophic-risk pathways alongside present-day harms; the course separates these evidence classes explicitly and requires threat hypotheses with weakening observations |
| 5 | Objectives are smaller than intentions | Ch. 03; Project P02 | Goodhart effects, specification failure, and reward hacking become a full chapter with a runnable proxy-vs-intended-objective experiment |
| 6 | Why increasing capability can increase the stakes | Ch. 03; Ch. 07 Deception, scheming, and evaluation awareness | The article's treatment of instrumental convergence and power-seeking is carried forward with the course's added discipline: formal results are stated with their assumptions (e.g., optimal policies in specific MDP classes), not as blanket predictions |
| 7 | Making behavior better through training | Ch. 04; Ch. 06 Honesty, uncertainty, and selective prediction; Project P04 | SFT/RLHF/DPO/Constitutional AI and sycophancy get a technical treatment, including at least one derived objective and a label-quality audit |
| 8 | Hallucination is an evidence problem | Ch. 06; Project P03 | Fluency-vs-verification distinction and abstention become calibration, risk–coverage, and selective-prediction work with a runnable experiment |
| 9 | Security changes when documents can influence actions | Ch. 13 LLM application security; Ch. 14 Agent, tool, memory, and MCP security; Project P07 | The article's jailbreak/indirect-injection discussion and "enforce boundaries outside the prompt" principle become a working vulnerable-application-then-hardened-application comparison |
| 10 | Evaluation is an experiment, not a ceremony | Ch. 02; Ch. 15 Red teaming; Projects P01, P10 | Capability/behavioral/control evaluation distinction; the course adds statistical standards (denominators, cluster-aware uncertainty, power) and a reusable harness |
| 11 | Oversight becomes harder when the work becomes harder | Ch. 05 Scalable oversight; Ch. 08 AI control and monitoring; Projects P05, P08 | Process supervision, weak-to-strong, debate, decomposition, and formal verification are each taught with their documented failure modes, then exercised in bounded analogues |

## What this repository adds beyond the article

The article is a survey; the course is a curriculum with executable evidence. The
main additions, each justified by the article's own "evidence over ceremony" stance:

1. **Mechanistic interpretability with causal-evidence standards** (Ch. 09–11,
   Project P06): activation patching with controls, superposition and sparse
   autoencoders with the reconstruction-vs-usefulness critique, steering with
   held-out and side-effect evaluation. The article does not attempt this area.
2. **Classical adversarial ML** (Ch. 12): evasion, poisoning, backdoors,
   extraction, membership inference — the article treats security at the
   LLM-application level only.
3. **Privacy, provenance, and supply chains** (Ch. 16): memorization, privacy
   accounting concepts, dependency integrity, and dataset/model provenance audits.
4. **Distribution shift and deployment reliability** (Ch. 17, Project P09):
   the article's "deployment changes the problem" point is made testable.
5. **Reasoning faithfulness and monitorability** (Ch. 18): CoT-faithfulness
   evidence and its limits, distinct from the article's oversight framing.
6. **Multimodal and embodied safety** (Ch. 19): cross-modal injection and the
   limits of text-only evaluation.
7. **Safety engineering formalism** (Ch. 22): hazard analysis (FMEA/STPA-style),
   explicit assurance claims, and why compliance checklists are not safety proofs.
8. **Governance and standards with dated official sources** (Ch. 23): NIST AI RMF,
   NIST AML taxonomy, MITRE ATLAS, OWASP GenAI LLM Top 10, with document versions
   and the guidance/obligation/proposal distinction.
9. **Research practice and capstone execution** (Ch. 24, Project P10):
   preregistration, ablation design, negative results, and a full assurance dossier.
10. **Statistical and reporting infrastructure**: the result schema, denominator
    discipline, uncertainty that respects the sampling unit, and LLM-judge
    validation rules that the article gestures at but does not operationalize.

## Corrections and precision notes

These are refinements, not rebuttals; the article's own framing is compatible with
each.

- The article references the *International AI Safety Report 2026* as background for
  the scientific picture of GPAI risks. The course cites that report only after
  verifying edition and section metadata in the source register (planned with
  chapter 23), and distinguishes its synthesis status from primary studies.
- The article's power-seeking discussion already qualifies formal results ("under
  specific assumptions"). The course makes those assumptions explicit and gradeable
  (optimal-policy rather than learned-policy results; specific MDP structure), and
  separates them from deployment extrapolation (Ch. 07).
- The article lists OWASP 2026 resources among further reading. The course verifies
  exact entries, edition identifiers, and access dates before using them as
  mappings targets in chapter 13, since edition years and publication years need
  not match.
- The article's bookshelf includes titles spanning popular treatments and technical
  monographs. `AWESOME.md` keeps such entries in an explicitly marked supplementary
  tier, separated from the course's required primary readings.

## Access limitations (honest statement)

- One full-text fetch session on 2026-10-21; the conclusion portion was not
  retrieved and is not characterized anywhere in this repository.
- No assumption is made about the article's reuse license; nothing beyond short
  factual references and section titles is carried into repository content.
- The article is by the repository owner. Where this map or the course agrees with
  the article, that agreement is inspiration and overlap, **not** independent
  validation of the article, and not evidence that the article's claims were
  externally reviewed.
