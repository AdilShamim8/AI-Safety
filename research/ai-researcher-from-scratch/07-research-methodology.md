# Module 7 — Research methodology: ablation, search, and the discipline of claiming

> Track: [AI Researcher From Scratch](README.md) · module 7 of 7 (the
> final module; protocol-only — no new code, by design: this module's
> artifact is a *way of working*, carried as preregistered protocol
> templates).
> Written companion: the research-methodology layer of
> vukrosic/zero-to-ai-researcher (SRC-REPO-001, full-text-read — its
> README's methodology section and the three experiment directories'
> designs), and its paper's abstract-level findings (claim `CLM-0073`).
> This course's own standards that the module maps onto: chapter 02
> (evaluation science and experimental design), P02 (preregistered
> reward-misspecification experiments), the
> [claims register](../claims-register.yaml) (evidence pricing).

## 0. Why this module exists

The track has built things. This module is about the other half of the
companion repo's title — *researcher* — which its methodology layer
defines by what you do after the model runs: form a hypothesis that
could fail, isolate the variable that tests it, compare against a
baseline you did not handicap, and report what happened including the
runs that did not. The companion structures this as three experiments
of increasing search-space size, and the track's version converts each
into a **preregistered protocol template** — the artifact format this
course already uses for its compute-tier projects — so a learner who
finishes the track can run the source's experiments (on the source's
GPU terms) or their own (on the track's stdlib terms) with the
claiming discipline already in place.

The mapping is the module's real content: the companion's
"research skills" list and this course's evaluation-science chapter
are the same discipline wearing different clothes, and seeing the
correspondence — hypothesis formation ↔ preregistration; ablation ↔
controlled comparison; learning-rate search ↔ hyperparameter protocols
with recorded grids; reproducibility ↔ seeded determinism — is what
turns a course taker into someone who can *contribute* evidence rather
than consume it.

## 1. The three experiments, as the companion designs them

The companion repo's methodology layer (README, "Research
Methodology"; SRC-REPO-001) specifies three experiments, each stated
with purpose, variables, method, and key learning — the fields of a
protocol, already:

**Experiment 1 — simplified ablation study.** *Purpose*: compare
architectural components at a manageable scale. *Models*: five
variants — baseline, MLP, attention+MLP, MoE, attention+MoE. *Scale*:
512 hidden dimensions. *Evaluation*: HellaSwag. *Stated learning*:
understanding how different components contribute to performance.
This is the controlled-comparison design: one factor changed at a
time against a fixed baseline, everything else (data, training
budget, seed policy) held constant — or, where not held constant,
*recorded* as a limitation. The paper reports an 8.7× gap between
best and worst of the five (abstract-level, `CLM-0073`); the
protocol's job is to make such a number *reproducible or refutable*,
not merely quotable.

**Experiment 2 — learning-rate search.** *Purpose*: find optimal
learning rates for DeepSeek-attention+MLP architectures. *Method*:
systematic exploration. *Metrics*: validation loss, accuracy,
perplexity. The paper reports 3e-3 as the identified optimum (0.015
validation loss, 99.7% accuracy as stated — abstract-level). The
track's connection is direct: module 03's exercise 5 derived *why*
the safe learning rate is curvature-dependent (the quadratic-bowl
contraction bound), and module 05's training runs chose 0.1 for a
2,000-parameter model — the "right" lr is a function of architecture
and scale, which is precisely why searching beats asserting.

**Experiment 3 — expert-configuration search.** *Purpose*: optimize
MoE configurations. *Variables*: expert count, learning rates,
top-k. *Method*: grid search with validation. The paper reports 4
experts with top-2 routing as best (0.061 validation loss, 98.7%
accuracy as stated). The track's connection: module 06's exercise 5
instrumented routing imbalance and derived what a balance loss would
cost — the search space of this experiment is exactly where those
trade-offs get measured.

Three honest notes about these designs, priced like everything else
in the track: the HellaSwag integration means the evaluation runs on a
real public benchmark (good — and outside this course's verified
dataset catalog, so it is cited at the companion's word, not
independently verified here); the experiments' *executions* are GPU
work this course has not run (this repo's experiments-executed counter
stays at 0 for them — they are the source's runs, reported at
abstract strength); and "grid search with validation" without a
stated grid, seed policy, and variance estimate is a method sketch,
not yet a protocol — which is what the next section adds.

## 2. The protocol templates (the module's artifact)

Three templates, one per experiment family, each mapped onto this
course's preregistration discipline (P02's protocol format: design
decisions fixed before the run, gates stated with numbers, claims
pre-priced). A learner fills one in *before* running; the filled
template is the preregistration.

**Template A — component ablation (maps to chapter 02's controlled
comparison):**

```yaml
hypothesis: "adding <component> improves <metric> by <amount> on <task>"
  # falsifiable as stated: a number, a direction, a task
variants:            # the companion's five-slot design, parameterized
  - {name: baseline, changes: []}
  - {name: <component-only>, changes: [<one factor>]}
  - {name: <component+peer>, changes: [<two factors>]}
  # ... every other factor identical: init seed, data order, budget
controls:
  - "identical token budget across variants"
  - "identical seed policy; N seeds, both reported (mean and spread)"
  - "matched-parameter or stated-parameter-count caveat where variants differ"
primary_metric: <validation loss, with its units and evaluation split>
decision_rule: "record the full grid; claim 'improves' only if the
  interval around the difference excludes zero at the stated N"
gates: ["preregistered before any variant is trained", "no variant
  re-run for a better seed without recording the re-run"]
```

**Template B — hyperparameter search (maps to chapter 02's adaptive
overfitting and the held-out discipline):**

```yaml
search_space: {"lr": [<grid>], "<second knob>": [<grid>]}   # stated before running
splits: "search on validation; report on test ONCE, last"
  # the chapter's contamination rule: a test set touched twice is a validation set
budget: "<total training runs, fixed in advance>"
selection: "argmin validation loss; report the runner-up gap"
  # a 3e-3 that beats 1e-3 by 0.001 is a different claim than by 0.1
variance: "N seeds at the optimum; report spread, not just the best"
```

**Template C — architecture-configuration search (maps to module 06's
MoE trades):**

```yaml
variables: {"n_experts": [...], "top_k": [...], "lr": [...]}  # the companion's grid
constraints: ["parameter budget matched or stated", "per-token FLOPs
  reported per configuration (the sparsity contract of module 06)"]
balance_instrument: "per-expert routing counts recorded per run
  (module 06 exercise 5's instrument, built in)"
failure_modes: ["router collapse recorded, not discarded", "dead
  experts reported with their token counts"]
```

Why templates rather than code: the track's code modules end at
module 06 because methodology is not a function you import — it is
the difference between the companion paper's numbers being *quotable*
and being *checkable*. The templates make the checkable version
cheap to start: fill, commit, run, compare claim-to-result. This
course's own P02 and P03 followed exactly this path
(preregistration committed before the runs; example reports from
genuine executions; the claims register pricing every number), so the
track's graduate has three worked examples of the discipline in the
same repository as the templates.

## 3. The skills list, mapped

The companion's stated research skills — hypothesis formation,
controlled experiments, ablation studies, baseline comparisons,
reproducibility, documentation — each map onto something the learner
has already *done* in this track or the main curriculum:

| companion skill | where this course makes you practice it |
| --- | --- |
| hypothesis formation | module 03–05 exercises ("predict, then run"); chapter 01's threat-hypothesis artifact; P02's preregistered gates |
| controlled experiments | module 04's linear control for XOR (the dead-baseline that pins 0.25); P01's scorer validation against hand-verified examples |
| ablation studies | module 06's dead-sublayer and unselected-expert tests (ablation as *test*, at toy scale); template A above |
| baseline comparisons | module 04's identity-activation control; chapter 02's baseline-and-paired-ledger discipline |
| reproducibility | seeded determinism throughout the track (curves pinned by re-running them in CI); P03's resumable, checksummed runner |
| documentation | this track's notes themselves — every number traced to a run or a source, every source priced |

The mapping is the module's closing argument: the from-scratch track
and the safety curriculum are one course. Building the object teaches
you what the evaluations are evaluating; the evaluation discipline
teaches you what your building claims are worth.

## 4. Where this connects

- **To the track**: this is the exit module — the track's README flips
  to complete with this note, and the learner's next moves are
  concrete: fill template A against the track's own TinyGPT (a real,
  cheap first ablation: width, depth, activation — on hardware this
  repo's CI already runs), or take the companion's designs to a GPU
  budget and preregister before running.
- **To the safety curriculum**: everything in chapters 01–02's
  epistemics and P01–P03's project discipline — this module is the
  bridge that lets the from-scratch learner cross into the main
  course without relearning what they already practiced.
- **To the sources**: the three-experiment structure, the skills list,
  and each experiment's stated purpose/focus/method/metrics follow the
  companion repo's README methodology section (SRC-REPO-001,
  full-text-read); the paper's quantitative findings remain at
  abstract strength under `CLM-0073`, and the templates are this
  course's contribution on top.

## 5. Exercises

1. Fill template A for a real ablation you can run today: the
   track's TinyGPT with `{silu, relu}` hidden activations at fixed
   d_model/seed/epochs, on the "hello" memorization task. Write the
   hypothesis with a number and direction *before* running, then run
   both variants (20 lines with the committed code) and report
   against your preregistered decision rule.
2. Fill template B for a learning-rate search over
   `{0.05, 0.1, 0.2, 0.4}` on the same setup. Which clause of the
   template does the "hello" task violate (hint: there is no
   train/validation/test split in a memorization run), and what does
   that make your search results — evidence of what, exactly?
3. The companion's experiment 1 evaluates on HellaSwag. Write the
   three questions this course's dataset-card discipline (the five
   provenance questions of chapter 02) would ask of that integration
   before citing its results, and find (in the HellaSwag paper's
   public description) the license and construction-method answers
   you would need to record.
4. Claim pricing drill: rewrite each of these into register-grade
   claims with evidence class and counterevidence — (a) "latent
   attention is 16× faster"; (b) "4 experts beat 8"; (c) "our MoE's
   unselected experts get zero gradient".
5. Design (do not run) the smallest experiment that would test
   whether the routing-imbalance observation from module 06's
   exercise 5 *persists after training*: variables held fixed, the
   instrument, the decision rule, and the honest stopping rule.

### Solutions

1. A filled template (values from an actual run will vary by the
   learner's seed; the *shape* is the answer): hypothesis "silu
   reaches final loss below relu's by epoch 400 on the 'hello' task,
   same seeds"; variants = two TinyGPTs differing only in the FFN
   activation (requires a one-line extension of `SwiGLUFFN`'s
   constructor — an honest implementation note to record); control =
   identical seeds, epochs, lr; metric = final training loss (with
   the caveat that a memorization task's loss floor is near zero for
   both, so the interesting comparison is *epochs to threshold*, not
   final loss — a design improvement discovered *by filling the
   template*, which is the exercise's real lesson). Decision rule:
   "claim 'faster' only if silu reaches loss < 0.01 at least 25%
   fewer epochs across 3 seeds."
2. The violated clause: no held-out split — "hello" is both the
   training set and the entirety of the evaluation, so the search
   selects on training loss and the template's "report on test ONCE"
   has no test to report on. The results are therefore evidence
   about *optimization speed on this exact sequence*, not about
   generalization; the honest register entry prices them as such
   (evidence class: memorization dynamics, single task, no split).
   Fixing it needs a longer corpus with a held-out continuation —
   which is the moment the learner understands *why* the companion's
   experiments evaluate on HellaSwag instead of their training data.
3. The five provenance questions applied to HellaSwag: who built it
   and why (Hendrycks et al., commonsense reasoning evaluation); how
   was it constructed (from ActivityNet captions and Wikihow, filtered
   against language-model shortcuts — the paper's design goal was
   exactly to defeat surface heuristics); what license (the paper's
   repo states its license — record it at fetch time, do not assume);
   what does a score mean (accuracy against adversarially-filtered
   wrong continuations — the "score" is shortcut-resistance, not
   knowledge); and what is it *not* evidence of (not safety, not
   calibration, not anything beyond commonsense continuation). Each
   answer must be recorded at the access level actually verified —
   the course's own dataset cards are the worked example.
4. (a) Register-grade: "the latent-token attention *gather step*
   costs N·M pairs versus N² for dense (7.6× for the full three-step
   pipeline at N=1000, M=64); 'faster' is a pair-count statement, not
   a wall-clock claim" — evidence: derivation + `attention_pairs`
   test; counterevidence: wall-clock includes projections and memory
   effects; (b) "the companion paper *reports* 4 experts with top-2
   beating their 8-expert configurations at 0.061 vs their 8-expert
   loss (abstract-level, single-setup, unreplicated)" — evidence:
   CLM-0073; counterevidence: per-run variance and grid contents
   unread; (c) "our SparseMoE's unselected experts receive exactly
   zero gradient (asserted on all expert parameter tensors, pinned
   by `test_moe_unselected_experts_get_zero_gradient`)" — evidence:
   executed test in CI; counterevidence: none within its scope — but
   the scope is *this implementation*, not MoE implementations
   generally.
5. Design: fixed TinyGPT-with-SparseMoE (module 06's classes compose
   directly), seed policy N=3; instrument = per-expert routing counts
   recorded at epochs {0, 50, 100, 200} (the exercise-5 instrument,
   called mid-training); hypothesis "max/min expert token-share ratio
   at epoch 200 exceeds 3× (imbalance persists)"; decision rule:
   mean ratio across seeds with the spread reported; honest stopping
   rule "if training loss has not converged by epoch 200, the run is
   void — imbalance of an unconverged router is not evidence about
   the trained one". The design's cost is minutes on this repo's CI,
   which is the point: the methodology module's first experiment is
   within reach of the code the track already committed.

## 6. Readings and provenance

- SRC-REPO-001 — vukrosic/zero-to-ai-researcher: the README's
  "Research Methodology" section (the three experiments' designs and
  the research-skills list — quoted at the level stated throughout
  this note) and the `experiments/` directory structure (designs
  inventoried; executions not run by this course). Access:
  full-text-read 2026-10-22 (cloned).
- This course's own artifacts the module maps onto: chapter 02
  (`chapters/02-evaluation-science-and-experimental-design/`), P02's
  preregistered protocol
  (`projects/p02-reward-misspecification-and-generalization/`), the
  claims register (`research/claims-register.yaml`).
- HellaSwag is referenced at the companion's word for experiment 1's
  evaluation; its paper and license were not fetched during this
  build, and exercise 3 is built on exactly that gap — the honest
  next fetch, recorded when done.
