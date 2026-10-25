# Ch. 04 — Preference learning and post-training

> The chapter where behavior is manufactured. Pretraining decides what a model *can* do; post-training decides what it *does* — and post-training is mostly optimization against a learned scalar fitted to human (or AI) comparison labels. Every safety property you care about in a deployed assistant was inherited from pretraining data or installed here, under one of the objectives this chapter dissects.

## 1. Research question and failure pathway

**The question this chapter answers:** *when you optimize a model against labels that came from comparisons, what does the resulting objective actually maximize — and at which seams does what you intended leak out?*

**The failure pathway it prevents** — a three-proxy chain, each arrow a place where Goodhart pressure applies (the taxonomy is Ch. 03's; the math is here):

```text
intended values ──► labeling instructions ──► collected comparisons ──►
reward model r_φ ──► RL / DPO objective ──► optimized policy ──► "aligned model"
```

The labels proxy the values, the reward model proxies the labels, and the policy optimizes the *reward model* — an optimizer applied to a proxy finds the proxy's errors, which is why regularization and label auditing are load-bearing here, not hygiene. To a *deployer* it matters because propensity (Ch. 01) is set here: InstructGPT fine-tuned GPT-3 on labeler demonstrations, then on rankings of model outputs with RL from human feedback, and the 1.3B-parameter result was *preferred* to the 175B GPT-3 in human evaluations on its prompt distribution [CLM-0026] — the pipeline installed the behavior, not scale.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites:** Ch. 01 (capability vs. propensity, evidence kinds — [Ch. 01](../01-risk-models-and-research-epistemics/README.md)); Ch. 02 (construct validity, Wilson intervals, provenance — [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)); the proxy-objective machinery of `chapters/03-specification-reward-hacking-and-goal-misgeneralization` — this chapter supplies the objectives whose misspecification Ch. 03 predicts. Math floor: log-probabilities, gradients, expectations; KL is defined in §3.4.

**Outcomes.** After this chapter you can:

1. Write the KL-regularized RLHF objective and the Bradley–Terry likelihood, stating — term by term — what each does and does not imply.
2. Derive DPO end-to-end from the RLHF objective, justifying every step (§4.1; the "objective derivation" assessment).
3. Explain SFT, PPO-style RLHF, RLAIF, and Constitutional AI as *objectives* with assumptions, not brand names.
4. Design and execute a preference-label audit (order-swap consistency, length stratification, re-annotation agreement) with interval statistics on real dataset sizes (§4.2; the "label-quality audit" assessment).
5. Name the failure condition of each method, including the counterexample that scalar rewards cannot represent intransitive preferences (§6.3).

**Scope exclusions.** No PPO implementation mechanics, no runnable training loop — that is project P04 (`projects/p04-preference-optimization-audit`); no scalable-oversight labeling schemes (weak-to-strong, debate, decomposition) — Ch. 05's subject; no look inside the network at what RLHF changes (Ch. 09–11). The chapter restricts to the objective-level canon — SFT, reward modeling with KL-regularized RL, DPO, RLAIF, Constitutional AI — and flags newer variants (iterative, on-policy preference methods) as outside the verified baseline.

## 3. Core explanation

### 3.1 The post-training stack: where objectives enter

The production pattern, fixed by InstructGPT [CLM-0026], is a three-stage stack:

1. **Supervised fine-tuning (SFT).** Maximize the log-likelihood of demonstration responses, `max_θ E_{(x,y)∼D_demo}[log π_θ(y|x)]` — behavioral cloning. It moves the conditional toward the demonstrator's on demo-like prompts; it does not constrain behavior off that distribution, choose between two acceptable demonstrator styles, or express *degree* of preference — likelihood is per-example, not comparative. SFT alone caps the model at the demonstrators' behavior and cannot say "A is better than B," the information safety tuning most needs.
2. **Reward modeling.** Collect pairwise comparisons and fit a scalar (§3.2–3.3).
3. **Policy optimization against the scalar, with a drift budget** (§3.4–3.5, or its closed-form shortcut, §4.1).

### 3.2 Preference data and the Bradley–Terry model

A preference dataset is a set of triples D = {(x, y_w, y_l)}: under prompt x, response y_w ("chosen") was judged better than y_l ("rejected"). The course's two real-world anchors:

- **Anthropic HH-RLHF**: crowdworkers compared two model responses and chose the more helpful / less harmful one — 169k rows (train 161k, test 8.55k), MIT, page-verified [datasets/cards/08-hh-rlhf.md](../../datasets/cards/08-hh-rlhf.md). The card's warning is part of the data: preference is a *dated human judgment*, not an oracle, and worker-population details are pending the paper read.
- **BeaverTails**: 364k rows in the default subset across four configurations (`330k_train` 301k; `330k_test` 33.4k; `30k_train` 27.2k; `30k_test` 3.02k), rows carrying multi-dimensional safety annotations (animal abuse, child abuse, controversial topics/politics, discrimination/stereotype/injustice, … as displayed), CC BY-NC 4.0 — non-commercial — page-verified [datasets/cards/07-beavertails.md](../../datasets/cards/07-beavertails.md). Annotation protocol and agreement statistics were *not visible* at the achieved access level, recorded as pending — which is why §4.2 audits rather than assumes.

The standard link from comparisons to a scalar is the **Bradley–Terry (BT) model**: the probability that an annotator prefers y_w over y_l is

```text
P(y_w ≻ y_l | x) = σ( r_φ(x, y_w) − r_φ(x, y_l) ),     σ(z) = 1/(1+e^(−z))
```

Fitting r_φ maximizes the Bernoulli likelihood of the observed choices — minimize the logistic loss on pairs:

```text
L_RM(φ) = − E_{(x,y_w,y_l)∼D}[ log σ( r_φ(x,y_w) − r_φ(x,y_l) ) ]
```

Read the assumptions off the equation — they are §3.7's audit checklist: (a) a *scalar* explains preference; (b) pairs are independent draws; (c) annotators are interchangeable (there is one r); (d) order, length, and annotator identity have no effect — none appears in the formula. Ziegler et al.'s abstract is the canonical published admission of (d)'s failure: their summarization results "may be exploiting the fact that labelers rely on simple heuristics" [CLM-0029]. When the heuristics are length or order, the reward model learns them at scalar strength. Calibration (arithmetic in the solutions): reward gaps of 0.8 and 1.6 give pair losses of 0.371 and 0.184 — the loss pushes gaps to grow, then *saturates*.

### 3.3 Reward modeling: what the fit does not imply

A fitted r_φ is a smoothed scalar summary of the comparison distribution on its training prompts, no more. Three limits, each mapped to where it bites: (i) **validity** — r_φ is unconstrained off its prompt distribution, and an RL policy will actively search those regions (§6.1); (ii) **label bias** — the loss has no other target, so every label bias is fitted at full strength (§6.2); (iii) **representation** — no scalar represents an intransitive preference cycle, whatever the data size (§6.3 computes the exact price).

### 3.4 The RLHF objective and what KL regularization actually buys

For policy π_θ, reward r_φ, and frozen reference π_ref (the SFT model):

```text
maximize_π   E_{x∼D, y∼π(·|x)}[ r_φ(x,y) ]  −  β · KL( π(·|x) ‖ π_ref(·|x) )
```

β prices drift in units of reward (at β = 0.1, one nat of KL costs 0.1 reward units). The objective exists because the unregularized version is degenerate for language models: probability mass can migrate to bizarre high-reward strings while fluency collapses — the KL term is the leash. It has a closed-form solution per prompt (the fact DPO exploits):

```text
π*(y|x) = π_ref(y|x) · exp( r_φ(x,y) / β ) / Z(x),   Z(x) = Σ_y π_ref(y|x)·exp(r_φ(x,y)/β)
```

What the KL term *actually* buys — and what it does not:

- It preserves π_ref's generation quality and keeps the policy near the region where r_φ was fitted, which *limits* (does not eliminate) reward-model extrapolation error.
- It is **not a per-output safety bound**: it is an expectation under the policy's own occupancy, so small average KL coexists with large deviations on tail prompts — and π_ref itself can produce harmful text, so anchoring to it anchors to its harms too.
- It has a *ceiling*, not just a budget: in §4.1's toy, the most degenerate policy (all mass on one of four responses) sits at KL = ln 4 ≈ 1.386 nats — a modest number for a drastic change. Expected KL compresses; behavior does not.

### 3.5 PPO-style RLHF

The production instantiation of §3.4 is policy-gradient RL (PPO-class): the policy samples responses, scores them with r_φ, subtracts a per-token KL penalty against π_ref, and updates with a clipped surrogate objective — the standard implementation picture (PPO's surrogate-objective mechanics are now abstract-verified [SRC-PAPER-070; CLM-0112]; the LM-RLHF composition itself is from InstructGPT [CLM-0026]). What is *verified* here: InstructGPT used rankings of model outputs to fine-tune the supervised model with RL from human feedback [CLM-0026], and the DPO abstract characterizes that pipeline as "complex and often unstable" — reward model first, then fine-tuning to maximize the estimated reward without drifting too far from the original model [CLM-0027]. The objective buys on-policy search for high-r_φ regions under a drift budget; it does not certify that reward-score gains are preference gains — the policy optimizes the proxy wherever it can, including regions where the proxy is wrong (Ch. 03's reward hacking, seam located at r_φ's training-distribution boundary).

### 3.6 From RLAIF to Constitutional AI

**RLAIF** replaces the human in the comparison loop with a model: same objectives, AI-produced labels. **Constitutional AI (CAI)** is the fully worked instance: per the paper, a harmless assistant is trained with no human labels identifying harmful outputs — the only human oversight is a list of principles — in two phases: supervised (sample from an initial model, generate self-critiques and revisions against the principles, fine-tune on the revisions) and RL (sample pairs from the fine-tuned model, have a model judge which is better, train a preference model on those AI preferences, then run RL against it — "RL from AI Feedback") [CLM-0028]. The reported result is an assistant that engages harmful queries by explaining its objections rather than evading them [CLM-0028].

What the objectives imply: label supply decoupled from human hours, so preference tuning scales. What they do not: the measured construct silently becomes "this judge model's output under this prompt," and the judge has its own biases (style, length, self-preference) that the BT loss fits just as faithfully as any human bias. The principles list is itself a proxy for the intended values, and the paper's evidence for the whole loop is internal evaluation by its authors — a lab self-evaluation in this course's taxonomy: enough to establish *possibility*, not deployment-range validity (the upgrade path is Exercise 4.4).

### 3.7 Auditing preference-label quality

Label quality is measurable before any training — which is why this chapter assigns it as an assessment. Three instruments, all runnable on a corpus you can load:

1. **Order-swap consistency (position bias).** Present a sample of pairs in both orders. A label process with no position bias produces identical judgments both ways; the *inconsistency rate* — the share of pairs whose judgment flips — is a direct lower bound on order-driven noise. HH-RLHF is pairwise by construction, so the instrument fits natively [datasets/cards/08-hh-rlhf.md](../../datasets/cards/08-hh-rlhf.md).
2. **Length stratification (length bias).** Compute the share of pairs where the chosen response is strictly longer. Under a no-length-effect null this is binomial around 0.5; a rate materially above it, with a tight interval (Ch. 02's Wilson discipline), is a length-bias signal the reward model inherits at full strength.
3. **Re-annotation agreement (annotator disagreement).** Re-annotate a subsample with independent annotators; report raw agreement with a Wilson interval. On BeaverTails this doubles as a taxonomy audit — the card's dimensions mix content categories (hate speech) with topic categories (controversial topics/politics), so a re-annotator must first decide which axis a "positive" label is even on [datasets/cards/07-beavertails.md](../../datasets/cards/07-beavertails.md).

Every rate comes out with an interval and a pre-stated decision rule, per [Ch. 02](../02-evaluation-science-and-experimental-design/README.md) — an audit without denominators and thresholds is an anecdote. §4.2 executes all three on real catalog sizes.

## 4. Worked example / derivation

### 4.1 The DPO derivation, end to end

**Claim being derived** (matching the paper's abstract [CLM-0027]): the KL-regularized optimum can be re-parameterized so the reward is expressed through the policy itself, reducing RLHF to a classification loss on the preference pairs — no reward model, no sampling, no RL loop.

**Steps 0–1 — objective, collected.** Per prompt x, maximize over π the §3.4 objective; both terms are expectations under π, so by linearity they combine into one expectation of `log(π/π_ref) − r/β`:

```text
E_{y∼π}[r_φ(x,y)] − β·E_{y∼π}[log(π/π_ref)]  =  −β · E_{y∼π}[ log ( π(y|x) / (π_ref(y|x) · e^{ r_φ(x,y)/β }) ) ]
```

**Step 2 — normalize with a partition function.** Define Z(x) = Σ_y π_ref(y|x)·e^{r_φ(x,y)/β}, so π*(y|x) := π_ref(y|x)·e^{r_φ(x,y)/β}/Z(x) is a genuine distribution. The log of the quotient splits, log Z is constant in y, and E_{y∼π}[log(π(y|x)/π*(y|x))] is exactly KL(π‖π*):

```text
= −β · ( KL( π ‖ π* )  +  log Z(x) )
```

**Step 3 — optimize.** log Z(x) does not depend on π, so maximizing the objective is minimizing KL(π‖π*), whose unique minimum — zero — is attained at π = π*. Closed-form optimum: done.

**Step 4 — invert.** Rearranging π*'s definition: r_φ(x,y) = β·log(π*(y|x)/π_ref(y|x)) + β·log Z(x). The second term is intractable (it sums over all responses) but is the same constant for every y given x — so it cancels in any *difference* of rewards.

**Step 5 — substitute into Bradley–Terry.** Insert the inverted reward into the preference probability; both β·log Z(x) terms cancel:

```text
P(y_w ≻ y_l | x) = σ( β · [ log (π*(y_w|x)/π_ref(y_w|x))  −  log (π*(y_l|x)/π_ref(y_l|x)) ] )
```

**Step 6 — maximum likelihood over the policy.** The right side is a function of π* alone; parameterize π* with the language model π_θ and maximize the likelihood of the observed pairs:

```text
L_DPO(θ) = − E_{(x,y_w,y_l)∼D}[ log σ( β·( log (π_θ(y_w|x)/π_ref(y_w|x))  −  log (π_θ(y_l|x)/π_ref(y_l|x)) ) ) ]
```

That is DPO's entire loss; its gradient (derived in the solutions) is `−β·σ(−ẑ)·[∇_θ log π_θ(y_w|x) − ∇_θ log π_θ(y_l|x)]` — structurally the BT gradient with the reward model replaced by the policy's own log-ratios ("your language model is secretly a reward model" is the paper's title [CLM-0027]).

**Numeric instantiation — a four-response toy.** π_ref uniform over Y = {y1, y2, y3, y4} (0.25 each), r = [1, 0, −1, 2], β = 1. Then e^{r/β} = [2.718, 1.000, 0.368, 7.389], Z = 2.8688, and

```text
π*  = [ 0.23688, 0.08714, 0.03206, 0.64391 ]
E_{π*}[r] = 1.49265      KL(π* ‖ π_ref) = 0.43876 nats
```

Three checks, recomputed in the solutions: (a) adding +5 to every reward leaves π* *identical* (Z absorbs it: 2.8688 → 425.7683) — offsets never matter, only differences; (b) the policy-form differences recover the true reward gaps exactly (1.000000 on the pairs checked) — the implicit reward *is* the true reward, difference-wise; (c) at β = 0.1 the policy becomes [0.00005, 0.00000, 0.00000, 0.99995] — 99.995% mass on the argmax — while its KL is only 1.38579 = ln 4, the *maximum possible* KL from a uniform-four reference. The leash hit its ceiling without ever showing a large number.

**DPO loss on one pair, four policy states (β = 0.1).** Let Δ_w = log(π_θ(y_w|x)/π_ref(y_w|x)), Δ_l likewise for the rejected response:

| Policy state (Δ_w, Δ_l) | ẑ = β(Δ_w−Δ_l) | σ(ẑ) | Loss −ln σ(ẑ) | Gradient factor β·σ(−ẑ) |
|---|---|---|---|---|
| (+2.0, +1.5) — model mildly prefers y_w | +0.05 | 0.5125 | 0.6685 | 0.0488 |
| (+0.5, +1.5) — model prefers y_l (wrong) | −0.10 | 0.4750 | 0.7444 | 0.0525 |
| (+2.0, −1.0) — model strongly separates | +0.30 | 0.5744 | 0.5544 | 0.0426 |
| (−1.0, −1.5) — *both* below reference | +0.05 | 0.5125 | 0.6685 | 0.0488 |

Rows 1 and 4 have identical loss and identical gradient direction, yet in row 4 the *preferred* response is less likely than under the reference. The loss constrains the margin, not the levels — §6.4's failure condition, visible in the arithmetic.

**What this derivation establishes and does not.** Established: under BT pair data, the DPO loss has the same optima as KL-regularized RLHF with the corresponding reward — training a policy and training an implicit reward model are the same problem at fixed β and π_ref [CLM-0027]. Not established: that the pairs are BT-consistent (§6.3); that off-distribution behavior is controlled — DPO has no on-policy search, so no mechanism even *checks* where the policy drifts; or that label bias vanished — it is now fitted directly.

### 4.2 A label-quality audit on real catalog sizes

**Setup.** You are handed a preference corpus and must decide whether it can support a reward-model training claim. Instruments from §3.7; denominators from the verified cards. The audit is the course's worked protocol: the *outcome counts* are illustrative first-run values (the cards publish no agreement statistics — that gap is why the audit exists), while every denominator and instrument fact is card-verified.

- **Instrument 1 — order-swap consistency on HH-RLHF.** Sample n = 1,000 pairs from the 161k-row train split [datasets/cards/08-hh-rlhf.md](../../datasets/cards/08-hh-rlhf.md); re-present each pair reversed. Illustrative run: 132 flip → inconsistency 13.2%, Wilson 95% **[11.2%, 15.4%]** (center 0.1334, half-width 0.0210). Pre-stated rule: above 10% → collect both orders and average or drop conflicted pairs. **Triggered.** Corollary: at most 86.8% of labels can be order-stable signal — single-order training inherits a ≥ 13.2% noise floor.
- **Instrument 2 — length stratification, same pairs.** Chosen strictly longer in 614/1,000 → 61.4%, Wilson 95% **[58.3%, 64.4%]** (center 0.6136, half-width 0.0301). Exact binomial tail P(X ≥ 614 | n=1000, p=0.5) = 2.8×10⁻¹³ (z ≈ 7.21) — not sampling noise. Pre-stated rule: interval lower bound above 55% → length-balance the training mix or debias the reward. **Triggered.**
- **Instrument 3 — re-annotation agreement on BeaverTails.** Re-annotate n = 200 rows of the 30k_test configuration (3.02k rows) against the card's taxonomy [datasets/cards/07-beavertails.md](../../datasets/cards/07-beavertails.md); 142 match → agreement 71.0%, Wilson 95% **[64.4%, 76.8%]** (center 0.7060, half-width 0.0624). Pre-stated rule: interval upper bound below 80% → adjudication protocol and written dimension-level instructions before any classifier claim. **Triggered.**
- **Power check (design input, not apology).** Resolving an inconsistency *rate* to ±3pp needs n ≥ 490 near p̂ ≈ 0.13 and n ≥ 1,068 worst-case (p̂ = 0.5); the 1,000-pair instruments sit at the honest edge for mid-range rates, and the 200-row agreement instrument (±6.2pp) is a screening tool only — the pre-stated claim is worded to survive that width.

**What the audit does and does not establish.** It establishes measurable, interval-backed noise floors for three named biases on the audited sample. It does not certify the unaudited ~160k of HH-RLHF's train split (an extrapolation, to be reported as such); it cannot see biases absent from its instruments (style, sycophancy toward the prompter, topic-dependent drift); and its BeaverTails leg audits the hosted safety *annotations* while that project's preference-pair structure remains paper-level pending [datasets/cards/07-beavertails.md](../../datasets/cards/07-beavertails.md). Results are license-bound too: CC BY-NC 4.0 bars commercial downstream use of anything trained on BeaverTails.

## 5. Comparison of post-training approaches

| Approach | Objective (what is maximized) | Load-bearing assumption | What it implies | Characteristic failure | Evidence quality | When it is right |
|---|---|---|---|---|---|---|
| SFT | log-likelihood of demonstrations | demonstrations cover the target behavior distribution | imitate demonstrators on demo-like prompts | demonstrator ceiling; silent OOD behavior; no degree-of-preference | behavioral; easy to evaluate | cold-start; style/format; required as π_ref for the rest |
| Reward model + PPO RLHF | E[r_φ] − β·KL(π‖π_ref), on-policy | the scalar transfers where the policy will actually go | steers propensity toward r_φ's high region under a drift budget | reward hacking at r_φ's boundary; instability; engineering weight [CLM-0027] | strong with held-out preference evals; lab self-eval otherwise | precise steering at scale, when you can afford and monitor the loop |
| DPO | −ln σ(β·(log-ratio margin)) on fixed pairs | pairs are BT-consistent; fixed β and π_ref suffice | log-ratios realize the reward differences; stable, no sampling [CLM-0027] | margin-only updates (levels unconstrained); no on-policy guardrail; β sensitivity | matches/improves its reported tasks vs PPO-RLHF [CLM-0027] | compute-light preference tuning; the default first try |
| RLAIF | same objectives, AI-produced labels | the judge ≈ the target human preference construct | label supply scales past human hours | judge biases fitted at full strength; construct silently changes | needs a human-validation subsample to count as evidence | cheap iteration; label bootstrapping |
| Constitutional AI | SFT on self-revisions + RLAIF against a principles list | the principles capture intended values; self-critique is reliable | controllable, non-evasive harmlessness without harm-labels [CLM-0028] | constitution laundering; judge self-preference; all evidence internal | lab self-evaluation by authors [CLM-0028] | harmlessness at low human-label cost with explicit, auditable principles |

The rows are stations on one pipeline, not rivals: CAI *contains* RLAIF, which *contains* reward modeling; DPO is a drop-in replacement for the RL stage. The honest comparison axis is which assumption your deployment can actually carry — and §6 is about the conditions under which each dies.

## 6. Where this chapter's methods fail

**6.1 Goodhart at the reward-model boundary.** Every method above optimizes a fitted scalar; every fitted scalar is valid only on its comparison distribution; every optimizer is *motivated* to leave that distribution. The KL leash limits average drift, not per-prompt drift, and not the *quality* of r_φ where data was thin. This is Ch. 03's proxy failure located precisely: the seam is r_φ's training-distribution boundary, and the failure is silent because the reward keeps rising while it happens.

**6.2 Labels are not ground truth.** The HH-RLHF card's misuse list leads with exactly this: "preferred by a crowdworker in 2022" is a dated human judgment, not an oracle [datasets/cards/08-hh-rlhf.md](../../datasets/cards/08-hh-rlhf.md). Ziegler et al. conceded the mechanism in their own abstract — labelers relying on simple heuristics [CLM-0029] — and §4.2's numbers make it concrete: a 61.4% length preference with a tight interval is a bias the reward model will faithfully learn, and the optimized policy will faithfully be long. Verbosity is the visible symptom; the invisible ones (sycophantic agreement, confident hedging) do not announce themselves.

**6.3 The scalar-representation counterexample.** Suppose annotators hold a coherent-but-cyclic preference: A ≻ B, B ≻ C, C ≻ A (real with length/detail/style tradeoffs). BT requires r(A) > r(B) > r(C) > r(A) — impossible. The minimum achievable total loss on the three pairs is 3·ln 2 ≈ 2.079, attained only at probability 0.5 on every pair, i.e. all reward differences zero (derivation: Exercise 4.1b; verified numerically in the solutions). The failure is representational, not statistical — more data cannot fix it.

**6.4 DPO's margin-only property.** The loss constrains Δ_w − Δ_l and nothing else — rows 1 and 4 of the state table have identical loss while placing the preferred response above and *below* the reference respectively. DPO training can therefore lower the likelihood of both responses of a pair (and of typical text generally) as long as the rejected one falls faster. For safety tuning: "the bad response got less likely" is a different, weaker claim than "the good response got more likely," and only the margin is optimized.

**6.5 RLAIF/CAI: the judge is a model with opinions.** The preference construct becomes "this judge, under this prompt, at this date" — a moving target with its own length and style biases, fitted at full BT strength. The constitution is a proxy for values, chosen by the lab; a principles list that reads well can still launder its authors' blind spots, and the paper's own evidence base is internal self-evaluation [CLM-0028]. The upgrade path — a human-validation subsample with intervals on judge–human agreement — is Exercise 4.4.

**6.6 The audit's own blind spot.** §4.2's instruments measure the biases they name. Annotator-population drift between collection waves, prompter identity effects, and topic-dependent severity standards pass through unmeasured unless instrumented; agreement numbers describe the audited sample, not the corpus. An audit is evidence about a labeling process you instrumented — never a certificate for the whole dataset.

## 7. Readings

**Verified in this build** (access levels per the source register; arXiv abstract pages fetched 2026-10-21):

- InstructGPT — Ouyang et al., arXiv:2203.02155, abstract-read [SRC-PAPER-009; CLM-0026]. Why: the canonical three-stage pipeline and the scale-versus-preference result. Skeptical read: "preferred by labelers on our prompt distribution" is a construct statement, not alignment.
- DPO — Rafailov et al., arXiv:2305.18290, abstract-read [SRC-PAPER-010; CLM-0027]. Why: §4.1 is its derivation — check every step against the paper. Skeptical read: its PPO-RLHF comparisons are the authors' evaluations on their tasks.
- Constitutional AI — Bai et al., arXiv:2212.08073, abstract-read [SRC-PAPER-011; CLM-0028]. Why: the reference RLAIF instantiation whose two-phase structure §3.6 mirrors. Skeptical read: internal self-evaluation; judge–human agreement numbers live in the full text, unread this round.
- Ziegler et al. — Fine-Tuning Language Models from Human Preferences, arXiv:1909.08593, abstract-read [SRC-PAPER-012; CLM-0029]. Why: the pre-LLM reward-learning baseline and the most honest published sentence about label heuristics. Skeptical read: 2019-era models, label scales, tasks.

**Verified in a later round** (abstract pages fetched 2026-10-23, closing this chapter's 2026-10-21 pending markers):

- PPO — Schulman et al., arXiv:1707.06347, abstract-read [SRC-PAPER-070; CLM-0112]. Why: the §3.5 objective mechanics — multiple epochs of minibatch updates on a surrogate objective, TRPO-like benefits with simpler implementation. Skeptical read: a general RL method paper with no language-model or human-feedback experiments; the LM-RLHF composition is InstructGPT's, not this paper's.
- HH-RLHF — Bai et al., arXiv:2204.05862, abstract-read [SRC-PAPER-071; CLM-0113]. Why: alignment training improving almost all NLP evaluations; the weekly-cadence iterated online mode; the roughly linear reward-vs-sqrt(KL) robustness relation. Skeptical read: the worker protocol that exercise 4.2 audits still lives in the unread body; the card remains metadata-only on it.
- BeaverTails — Ji et al., arXiv:2307.04657, abstract-read [SRC-PAPER-072; CLM-0114]. Why: the 333,963 QA pairs / 361,903 expert-comparison counts, corroborating the card at abstract level; helpfulness/harmlessness separation. Skeptical read: annotation protocol and preference-pair construction remain body-level; CC BY-NC 4.0 constrains use.


**Note companions:** [25 DPO — the reparameterization](../../research/notes/25-dpo-reparameterization.md), [26 InstructGPT — the pipeline](../../research/notes/26-instructgpt-pipeline.md), [30 Constitutional AI — supervision in a document](../../research/notes/30-constitutional-ai.md). [37 Reward-model overoptimization — the budget behind the RLHF curve](../../research/notes/37-reward-overoptimization.md)[42 Helpful and harmless — the RLHF baseline and the sqrt-KL price of drift](../../research/notes/42-helpful-harmless-rlhf.md) [C09 KL budgets vs held-out gold gates — governing the Goodhart curve](../../research/notes/comparison-09-kl-budgets-vs-gold-gates.md) [61 Fine-tuning compromises safety — the privilege boundary](../../research/notes/61-finetuning-compromises-safety.md)

## 8. Exercises

**Exercise 4.1 — derivation and counterexample (analysis).** (a) Fill the two gaps in §4.1: (i) show Step 1→2 in full — that E[log(π/π_ref)] − E[r]/β equals KL(π‖π*) + log Z(x) with Z as defined; (ii) derive the DPO gradient from L_DPO and interpret each factor (when is its magnitude maximal? what does β multiply?). (b) Prove that the minimum total BT loss for the 3-cycle A ≻ B, B ≻ C, C ≻ A is 3·ln 2, attained when all three reward differences are zero. (c) Using the state table of §4.1, explain in ≤ 5 sentences why DPO cannot distinguish row 1 from row 4, and what a safety reviewer should therefore *not* conclude from a falling DPO loss.

**Exercise 4.2 — preregistered label-quality audit (the chapter artifact).** Write a complete audit plan for a preference corpus of your choice (HH-RLHF or BeaverTails, cards linked above) that a second team could execute unchanged. Required sections: the claim in context form (what label-quality statement the audit supports); instruments with card-verified denominators and pinned revisions; split/grouping discipline; interval method and pre-stated decision thresholds per instrument; power statement; weakening observations (≥ 3, falsifiable); scope exclusions including license constraints. 700–1,200 words.

**Exercise 4.3 — numeric drill (recompute everything).** (a) BT loss for r_φ(x,y_w) − r_φ(x,y_l) = 1.2 and for a tie; (b) DPO loss and gradient factor for (Δ_w, Δ_l) = (3.0, 1.0), (−0.5, 1.5), and (0, 0), with β = 0.1; (c) Wilson 95% intervals with visible center and half-width for 87/1,000 inconsistent under order swap and 165/200 re-annotation agreement; (d) for each interval, whether it supports "inconsistency below 10%" and "agreement at least 80%" respectively; (e) recompute the §4.1 toy at β = 0.5 and report π*, E[r], KL, and what changed versus β = 1.

**Exercise 4.4 — RLAIF evidence critique (critical).** From the verified abstract-level claims about CAI [CLM-0028] alone: (a) separate what the paper *establishes* from what a deployment decision would still need; (b) name three judge biases an AI preference labeler could inject that a naïve pipeline would then optimize; (c) design the validation study that upgrades the evidence class — a human-validation subsample of AI preference labels — with denominators, interval method, and the pre-stated number that would *weaken* the RLAIF-alignment hypothesis. State the study's own limits.

## 9. Hints and solutions

Hints: 4.1 — the convexity/KKT route for (b) is shorter than a grid search; for (a)(i), expand the log of a quotient and remember what is constant in y. 4.2 — mirror the Ch. 02 preregistration skeleton; denominators come from the cards, not from memory. 4.3 — σ(0) = 0.5 makes two cells free. 4.4 — the abstract says the *only* human oversight is the principles list; ask what that implies about who measured the result.

Full worked solutions with assessor rubrics are in [solutions.md](solutions.md). Attempt every exercise first — the rubrics grade the reasoning trail, and §6.6 applies to your write-ups too.

## 10. Completion

**Artifact this chapter produces:** (1) a completed DPO derivation with every step justified and its numeric checks recomputed (the "objective derivation" assessment); (2) a preregistered label-quality audit plan at rubric level (the "label-quality audit" assessment) — the document `projects/p04-preference-optimization-audit` executes as its first phase.

You have completed this chapter when you can:

- [ ] Write the KL-regularized RLHF objective from memory and state, per term, one thing it implies and one thing it does not.
- [ ] Reproduce the DPO derivation on a blank page, including why Z(x) cancels and what the gradient's σ(−ẑ) factor does.
- [ ] Execute the three label-audit instruments on a real pairwise corpus and report rates with Wilson intervals and pre-stated decision rules.
- [ ] State each approach's failure condition in §5 and the §6.3 counterexample with its computed price (3·ln 2).

**Links.** Previous: `chapters/03-specification-reward-hacking-and-goal-misgeneralization` (the proxy-failure theory this chapter's objectives are exposed to). Foundations: [Ch. 01](../01-risk-models-and-research-epistemics/README.md) · [Ch. 02](../02-evaluation-science-and-experimental-design/README.md). Next: `chapters/05-scalable-oversight` (where labels come from when humans cannot supply them well). Project track: `projects/p04-preference-optimization-audit`. Dataset anchors: [cards/07](../../datasets/cards/07-beavertails.md) · [cards/08](../../datasets/cards/08-hh-rlhf.md) · [datasets/README.md](../../datasets/README.md). Glossary: [GLOSSARY.md](../../GLOSSARY.md).

**References (claim anchors).** [CLM-0026] InstructGPT pipeline and scale-versus-preference result (SRC-PAPER-009, abstract-read). [CLM-0027] DPO closed-form re-parameterization and reported task comparisons (SRC-PAPER-010, abstract-read). [CLM-0028] CAI two-phase structure and harmless-but-non-evasive result (SRC-PAPER-011, abstract-read). [CLM-0029] Ziegler et al. comparison counts and labeler-heuristics caveat (SRC-PAPER-012, abstract-read). Dataset facts: [cards/07], [cards/08] as linked above. Toy arithmetic, audit-run outcome counts, and derived gradients are this course's own computations (recomputed in [solutions.md](solutions.md)).

**Notation table.**

| Symbol | Meaning | Introduced |
|---|---|---|
| x, y | prompt; response (y_w chosen, y_l rejected) | §3.2 |
| π_θ(y\|x) | policy: the language model's conditional over responses | §3.1 |
| π_ref | reference policy (frozen, usually the SFT model) anchoring drift | §3.4 |
| r_φ(x,y) | reward model: scalar fitted to pairwise comparisons | §3.2 |
| D | preference dataset of triples (x, y_w, y_l) | §3.2 |
| σ(z) | logistic sigmoid 1/(1+e^{−z}) | §3.2 |
| KL(π‖π_ref) | Kullback–Leibler divergence (expected log-ratio under π) | §3.4 |
| β | KL coefficient: nats of drift priced in reward units | §3.4 |
| Z(x) | partition function Σ_y π_ref(y\|x)e^{r(x,y)/β} | §3.4 |
| π*(y\|x) | closed-form KL-regularized optimum | §3.4 |
| Δ_w, Δ_l | log-ratios log(π_θ(y_w\|x)/π_ref(y_w\|x)), likewise y_l | §4.1 |
| ẑ | DPO margin β(Δ_w − Δ_l): the implicit reward difference | §4.1 |
| p̂, n, z | observed rate, denominator, normal quantile (Wilson, Ch. 02) | §4.2 |
