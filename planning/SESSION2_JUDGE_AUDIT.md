# Session 2 — the LLM-as-judge audit (the verdict before the work)

**What this document is:** the owner asked for a judge's pass over the whole
build before the next 150 commits: *look at everything, say what is missing,
say where each missing piece can actually be collected from, then close the
gaps one commit at a time.* This is that verdict. It is written the way the
rest of the repo is written: every gap carries (a) what is missing, (b) the
evidence that it is missing, and (c) the named public source it will be
collected from — never "somewhere on the internet."

**What this document is not:** a promise that every gap closes in this
session. The backlog below is the *judged* priority order; the STATUS file
records the honest position after every commit, and anything that stays open
stays open in writing, not silently.

## 1. The judged state (at commit 150, 2026-10-25)

What the build has earned so far, with the evidence the judge accepts:

| Dimension | State at 150 | Judge's basis |
|---|---|---|
| Curriculum | 24/24 chapters, each with 10 sections incl. readings, exercises, hints, completion gates | content-matrix.yaml + validator |
| Projects | 10/10 implemented, stdlib-only, 594 tests green | pytest + pinned results |
| From-scratch track | 7/7 modules (math → methodology) | research/ai-researcher-from-scratch/ |
| Paper notes | 32 notes + 6 comparisons, every one register-verified at a stated access level | source-register.yaml |
| Incidents | 3 production incidents reviewed (Air Canada, DPD, Chevy) | notes/incidents/ |
| Datasets | 22 catalog cards, all real, all access-stated | datasets/catalog.yaml |
| Learner surface | START_HERE, FAQ, verifying-sources guide, AWESOME, MAINTENANCE, syllabus, schedules | root files |
| Careers | 3 roles, 4 routes, market demand snapshot with sources, first-90-days | roadmaps/ |
| Dashboard | index.html, 12 sections, self-contained, CI-pinned | tests/test_dashboard.py |
| Honesty | 248-term glossary, honesty ledger of not-executed tiers, 0 hard audit findings | audit_missing.py |

The judge's summary sentence: **the spine is complete and honest; the gap is
now coverage depth — the number of primary sources the learner can meet as
notes, the number of real-world datasets and incidents the claims touch, and
the absence of the one thing the owner named explicitly: step-by-step
progress tracking per career route.**

## 2. The gap register (what is missing, and where it lives)

Seven gaps, each with the collection source. Nothing below will be written
from memory alone; each item lands only with a register entry at its true
access level.

### G1 — Note coverage: the field's load-bearing papers without notes (32 → 50)

The readings sections cite these classics; the notes directory does not yet
meet them. Missing, in judged priority order, each with its collection point:

| # | Paper | Find it at | Access level we will claim |
|---|---|---|---|
| 33 | Concrete Problems in AI Safety (Amodei et al., 2016) | arXiv:1612.07903 abs page | abstract-read |
| 34 | Toy Models of Superposition (Elhage et al., 2022) | transformer-circuits.pub/toy_models/index.html | full-text-read (public HTML) |
| 35 | Obfuscated Gradients (Athalye et al., 2018) | arXiv:1803.00853 | abstract-read |
| 36 | Adversarial Examples Are Not Bugs, They Are Features (Ilyas et al., 2019) | arXiv:1905.02175 | abstract-read |
| 37 | Scaling Laws for Reward Model Overoptimization (Gao et al., 2023) | arXiv:2210.10760 | abstract-read |
| 38 | Language Models Don't Always Say What They Think (Turpin et al., 2023) | arXiv:2305.04388 | abstract-read |
| 39 | Lost in the Middle (Liu et al., 2023) | arXiv:2307.03172 | abstract-read |
| 40 | Taken Out of Context (Berglund et al., 2023) | arXiv:2309.01705 | abstract-read |
| 41 | Model-Written Evaluations (Perez et al., 2022) | arXiv:2212.09251 | abstract-read |
| 42 | Training a Helpful and Harmless Assistant (Bai et al., 2022) | arXiv:2204.05862 | abstract-read |
| 43 | Measuring Faithfulness in Chain-of-Thought Reasoning (Lanham et al., 2023) | arXiv:2307.13702 | abstract-read |
| 44 | Jailbroken: How Does LLM Safety Training Fail? (Wei et al., 2023) | arXiv:2307.15043 | abstract-read |
| 45 | Many-Shot Jailbreaking (Anil et al., 2024) | arXiv:2408.09687 | abstract-read |
| 46 | FActScore (Min et al., 2023) | arXiv:2305.14251 | abstract-read |
| 47 | SelfCheckGPT (Manakul et al., 2023) | arXiv:2303.08896 | abstract-read |
| 48 | Inverse Scaling Prize results (McKenzie et al., 2023) | arXiv:2306.09279 (openreview mirror) | abstract-read |
| 49 | Holistic Evaluation of Language Models, HELM (Liang et al., 2022) | arXiv:2211.09100 | abstract-read |
| 50 | In-Context Learning and Induction Heads (Olsson et al., 2022) | transformer-circuits.pub/2022/in-context-learning-and-induction-heads | full-text-read (public HTML) |

(Where a table row says abstract-read, the note is honest about pricing:
claims stop at what the abstract and public README establish.)

### G2 — Real-world dataset coverage (22 → 34 cards)

The catalog lacks the suites that the 2023–2025 safety-evaluation literature
actually runs on. Missing, with collection points (every card lands with a
Hugging Face or paper-anchored URL, license, and access level):

StrongREJECT (Souly et al., 2024, arXiv:2402.19210 + HF alexandrasouly/strongreject);
PKU-SafeRLHF (HF PKU-Alignment/PKU-SafeRLHF + arXiv:2406.15513); DoNotAnswer
(Huang et al., 2024, arXiv:2408.15254 + HF); AgentHarm (Andriushchenko et
al., 2024, arXiv:2410.09024 + GitHub); InjecAgent (Zhan et al., 2024,
arXiv:2403.02691 + GitHub); BIPIA (Yi et al., 2023, arXiv:2306.07854 +
GitHub); AgentDojo (NeurIPS 2024 D&B, GitHub ETH-SRI/agentdojo);
CounterFact (Meng et al., 2022 ROME, GitHub kmeng1/rome — ch11 causal
editing); TrojAI (DARPA/IARPA, GitHub darpa-i2o/trojai — ch16
poisoned-artifact detection); RobustBench (Croce et al., 2021,
robustbench.github.io — ch12 standardized adversarial evaluation); FEVER
(Nie et al., 2018, fever.ai — ch06 fact verification); FigStep (Gong et
al., 2023, arXiv:2307.16823 + HF — ch19 multimodal jailbreak).

### G3 — Incidents: 3 reviewed; the public record has more (3 → 11)

Judge's selection rule: only incidents with (a) a primary news/agency
report or database entry we can page-inspect, and (b) a mechanism that maps
onto a chapter. Candidates, each with its collection point:

| Incident | What it teaches | Find it at |
|---|---|---|
| 04 — Google AI Overviews "eat rocks" (2024) | hallucination meets deployed search; no abstention layer | The Verge 2024-05 report + Google statement |
| 05 — NYC MyCity chatbot illegal advice (2024) | deployment without domain guardrails | The Verge investigation 2024-03 |
| 06 — Cursor "refund policy" hallucination (2025) | chatbot commits hallucinated policy; small-claims reply | Ars Technica 2025-06 report |
| 07 — Slack AI prompt-injection exfiltration (2024) | channel-content injection → exfil; ch14 mechanism | PromptArmor disclosure + Slack KB |
| 08 — Samsung ChatGPT code paste (2023) | data leakage via employee tool use; ch16 | agency reports from 2023-04 (Bloomberg, Reuters) |
| 09 — Bing Chat web-content injection (2023) | hidden-page injection in search-adjacent chat; ch13/14 | Ars Technica 2023-02 report |
| 10 — Microsoft Tay corruption (2016) | online learning without input gating; ch04/ch21 | The Verge/ZDNet 2016 reports — the canonical historical case |
| 11 — Bing/Sydney persona collapse (2023) | long-context priming + persona drift; ch17 | NYT transcript + The Verge coverage, 2023-02 |

(Each row lands only if its primary page is reachable at build time and
says what the row claims it says; if a page-inspect fails, the incident is
replaced from the AIID backlog and the substitution is recorded here.)

### G4 — Career progress tracking (the owner's explicit ask) — MISSING ENTIRELY

The route pages say *what* to learn; nothing lets a learner *track step by
step* whether they learned it. Gap: per-route milestone checklists with
per-milestone evidence (which chapter gate, which note, which project
result). Collected from the repo itself (chapters, notes, projects) — the
sources are our own completed units — plus the market-signal sources already
in the register (SRC-CURR-005..008). Deliverable: `roadmaps/progress/*.md`,
one tracker per route, plus a dashboard widget that renders them.

### G5 — Dashboard interactivity for engagement — PARTIAL

The 12 sections render; the interactivity budget so far is one details/summary
pattern. Missing for the owner's "widget visualization" ask: a per-route
progress widget, an incidents timeline, a notes-coverage matrix against
chapters, and a dataset-catalog browser — all in the self-contained
no-dependency index.html the CI pins.

### G6 — Glossary and comparison depth (248 terms, 6 comparisons)

Notes 33–50 and the new datasets each mint terms; comparisons 07–12 should
name the pairs the new notes force (e.g., faithfulness-checking families,
jailbreak taxonomies vs attack taxonomies, eval-suites vs deployment
telemetry).

### G7 — Verification re-checks on standing claims

Every soft-note null in the register stays null only if still unreachable;
the session re-attempts page-inspect on a rotating sample and records the
result either way (the MAINTENANCE file's drift discipline applied to
claims, not just links).

## 3. The judge's rules for this session (unchanged from the first 150)

1. One commit at a time; each pushed and remote-verified before the next.
2. A source lands in the register with its access level BEFORE its claims.
3. Memory is not a source: every paper number below comes from a page we
   inspect this session or already carry at the right level.
4. When a page-inspect fails, the honest label ("not executed" /
   "unreachable at build time") beats an invented number.
5. Full gate (ruff, pytest, validator, audit, dashboard freshness) before
   every commit — the session's own earlier lesson applied to itself.

## 4. The 150-commit backlog (judged priority order)

| Phase | Commits | Closes |
|---|---|---|
| A. Judge audit + session records | 151–154 | this document; STATUS/README/CHANGELOG session-2 opens |
| B. Notes 33–50 (18 notes) | 155–176 | G1 (+ chapter cross-links, glossary mints) |
| C. Dataset cards 23–34 (12 cards) | 177–190 | G2 (+ catalog + dashboard + test updates) |
| D. Incidents 04–11 (up to 8, page-inspect-gated) | 191–202 | G3 |
| E. Career progress trackers + widget | 203–209 | G4 + G5 (first half) |
| F. Comparisons 07–12 | 210–215 | G6 |
| G. Glossary batches (+50 terms) | interleaved | G6 |
| H. Dashboard widget upgrades | 216–231 | G5 (second half: timeline, coverage, catalog) |
| I. Learner surface refresh + verification re-checks | 232–243 | G7 + FAQ/SYLLABUS/verifying-sources updates |
| J. Final milestone: STATUS, CHANGELOG, README tour, closing full-gate pass | 244–300 (contingency + per-chapter link sweeps + any honestly-earned extra depth the earlier phases surface) | all |

The contingency band is deliberate: the first 150 commits taught the judge
that real work surfaces real gaps; the reserve exists so that whatever
phases B–I surface gets closed inside this session instead of deferred.

## 5. The standing judgment

The build's honesty ledger is its most valuable artifact; this session's job
is to grow the *coverage* without ever trading that away. Every item in
section 2 lands with its source at its true access level, or it does not
land at all — and the difference is recorded here and in STATUS.
