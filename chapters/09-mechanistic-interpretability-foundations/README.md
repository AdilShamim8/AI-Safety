# Ch. 09 — Mechanistic interpretability foundations

> The chapter that turns "we looked inside the model" into a causal claim
> you can defend. Every interpretability result — a heatmap, a "circuit",
> an edited model — is either a controlled intervention with baselines,
> controls, and off-distribution checks, or a correlation wearing a
> mechanism's clothes. This chapter builds the first kind.

## 1. Research question and failure pathway

**The question this chapter answers:** *when a language model produces a
safety-relevant behavior — refusing a harmful request, contradicting a
popular misconception — where in the network is that behavior computed, and
how do you prove it causally rather than just point at it?* The failure
pathway it prevents:

```text
colorful attribution map ──► "component X lights up" ──► causal language
("X decides", "X is the honesty module") ──► intervention launched
(edit / ablate / steer at X) ──► behavior breaks somewhere unmonitored
```

Each arrow leaks validity quietly. An attribution map is an observation, not
an experiment; "lights up" conflates correlation with mediation — a late
layer "lights up" for every behavior because every finished computation
passes through it; and an intervention built on an unvalidated location
claim fails silently, because nothing in the output looks wrong until you
probe the capability you did not monitor. The antidote is the discipline
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) installed
for behavioral claims — baselines, denominators, controls, intervals —
applied to *internal* variables.

Behavioral evaluation tells you *what* a model does; this chapter asks
*where* it is done, so later units can edit it (`chapters/10-...`), steer it
(`chapters/11-...`), or trust a monitor built on it
([Ch. 08](../08-ai-control-and-monitoring/README.md)). Those interventions
stand on interpretability claims, which are falsifiable only when the
intervention design is.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites:** [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(constructs and instruments, baselines, Wilson intervals, preregistration —
all reused here); diagnostic task B
([diagnostic](../../prerequisites/diagnostic.md)); refresher R3
([targeted refreshers](../../prerequisites/targeted-refreshers.md)). No
deep-learning research background is assumed.

**Outcomes.** After this chapter you can:

1. Explain the residual-stream architecture of a decoder-only transformer
   and what attention and MLP blocks each write into it.
2. Define a feature representation and state the linear-representation view
   with its evidence and its limits.
3. Design an activation-patching experiment: clean and corrupted runs, a
   restoration metric, a patching grid, and control arms that make the
   result interpretable.
4. Distinguish where a behavior is *stored* from where it is *computed*, and
   say why single-site patching alone cannot separate the two.
5. Produce the chapter's artifact: a causal claim about a component with
   controls, intervals, transfer results, and off-distribution checks — the
   claim format project `P06` operationalizes.

**Scope exclusions** (deliberate, with pointers): superposition, sparse
autoencoders, automated circuit discovery, and faithfulness evaluation are
`chapters/10-...`; steering vectors and probes are `chapters/11-...`. Model
*editing* appears only as evidence about localization. One model, small
prompt sets; interpretability scaling laws are out of scope.

## 3. Core explanation

### 3.1 The residual stream: the transformer's communication channel

A decoder-only transformer is a stack of blocks that all read and write one
shared workspace. Following the framework that named it: the **residual
stream** at layer `l`, position `t` is "simply the sum of the output of all
the previous layers and the original embedding" — a communication channel
that "doesn't do any processing itself," through which all layers
communicate [CLM-0046]. With token embedding `x_t^(0)`:

```text
x_t^(l) = x_t^(0) + Σ_{j<l} ( a_t^(j) + m_t^(j) )
```

where `a_t^(j)` and `m_t^(j)` are the attention and MLP block outputs at
layer `j`. The final logits read the accumulated stream, so each block's
contribution is additive, and the architecture has "a deeply linear
structure" at this macro level [CLM-0046]. Two consequences drive this
chapter: **position is a real axis** (each token carries its own stream
vector, and blocks at one position read information written at another via
attention), and **subspaces matter** (embeddings, heads, MLPs, and the
unembedding "communicate by reading and writing to *different subspaces* of
the residual stream" [CLM-0046], so components coexist until one reads
another's subspace). Patching "activations at layer 7" overwrites one slice
of this shared channel at chosen positions.

### 3.2 Attention and MLP contributions: QK/OV and the four-wide MLP

Each attention head decomposes into two nearly independent circuits
[CLM-0046]. The **QK circuit** (`W_QK`) decides *where to look*: it maps
source and destination representations to a query and a key whose dot
product scores attention. The **OV circuit** (`W_OV`) decides *what moves*:
it maps attended-to tokens' representations to the contribution written into
the destination's stream. Patterns depend on QK; effects depend on OV —
which is why "the head that looks at the subject" and "the head that copies
the subject's features" are different mechanistic claims. Heads also
**compose** through the stream in Q-, K-, or V-composition, and two layers
of composition already suffice to build induction heads, a general
in-context-learning algorithm [CLM-0046]. The **MLP blocks** are
position-wise function layers, typically four times wider than the stream,
that read one position's vector and write back a transformed one
[CLM-0046]; they are the usual suspects for feature storage, because
causal-tracing experiments on factual recall find mid-layer feed-forward
modules mediate factual predictions while processing the *subject tokens* of
the prompt [CLM-0047]. Our notation keeps blocks separate (`a` vs `m`) so
patching can ask which block at which layer carries a behavior — the layer-7
attention patch and the layer-7 MLP patch are different experiments.

### 3.3 Features and (linear) representations

A **feature** is a property of the input or context that the model's
internals represent measurably — "sentiment", "the sentence's subject",
"this request is about harming someone" — and the **linear-representation
view** encodes it as a direction in activation space, read out by
projection. The strongest evidence in our reading list: across a range of
models, sentiment is represented linearly — "a single direction in
activation space mostly captures the feature," one pole positive, the other
negative — and causal interventions on that direction change
classification behavior, with mechanisms concentrated in a small subset of
attention heads and neurons [CLM-0049]. Ablating the direction destroys most
of the signal: zero-shot sentiment classification on Stanford Sentiment
Treebank loses 76% of its above-chance accuracy when the direction is
ablated, and 36% from ablating it *only at comma positions* — intermediate
positions summarize the sentence's sentiment [CLM-0049]. Treat the linear
view as a working hypothesis, not a theorem: features may share directions
(superposition), some are plausibly multi-dimensional, and a direction that
behaves linearly on a curated distribution can stop doing so off it
(`chapters/10` and `chapters/11` push on exactly those limits). This chapter
needs only the weaker, safe claim: *some* behaviors are mediated by
localized components whose causal role patching can measure.

### 3.4 From correlation to cause: the mediation framing

For intervention talk we borrow the estimand language of causal mediation
analysis, as brought into NLP interpretability by Vig et al. [CLM-0048].
The input `X` (prompt) influences the output `Y` (our metric) both directly
and through internal components — **mediators** `M_s`, the activations at
site `s`. The **total effect** (TE) of switching `X` from clean to corrupted
is the metric change with no intervention; the **indirect effect** (IE)
through `s` is the part flowing through `M_s`; the **direct effect** (DE) is
what remains when `M_s` is held fixed. (This Pearl-style decomposition is
the course's operationalization of the mediation literature; the verified
papers apply it in their own terms [CLM-0047, CLM-0048].) **Activation
patching** estimates the IE at a site by force-association — run the
corrupted prompt, but at site `s` overwrite activations with the clean run's
values there:

```text
clean:      X_clean -> (M_s = m_clean)  -> Y_clean
corrupted:  X_corr  -> (M_s = m_corr)   -> Y_corr
patched:    X_corr  -> (M_s := m_clean) -> Y_patched(s)
```

If the metric moves back toward clean, information that matters for the
behavior flowed through `s`. Vig et al.'s mediation analysis of gender bias
found the mediating effects *sparse* — concentrated in a small part of the
network — and *synergistic*, with components amplifying or repressing each
other, the total decomposing into direct and indirect parts [CLM-0048];
sparsity is what makes patching informative, and synergy is what makes it
hard. The causal reading rests on three assumptions you must state: the
intervention is *surgical* (replacing `M_s` perturbs nothing except through
the model's own downstream reaction); the corruption *defines the contrast*
(change the corruption, change the question); and the metric is a valid
instrument for the behavior construct ([Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
§3.1 applies verbatim). Drop any of these and a restoration number becomes
a Rorschach test.

### 3.5 Metrics and statistics for patching experiments

The output metric should be a *margin*, not the probability of one answer.
Our standard choice is the **logit difference** between competing
continuations at the answer position — for the worked example, `Δ = logit
(true answer) − logit (imitative answer)`. Margins are unconstrained in
sign, linear in the underlying evidence, and comparable across prompts in a
way single-answer probabilities are not. Define the **restoration fraction**
`R(s) = (Δ_patched(s) − Δ_corrupted) / (Δ_clean − Δ_corrupted)`: `R = 0`
means the patch did nothing, `R = 1` full restoration, `R < 0` harm. Because
`Δ_clean` and `Δ_corrupted` are reference arms of the experiment, every
patching study is a three-arm comparison by construction — you already have
baselines if you run them first and report them. Statistics: patching yields
one `R` per prompt per site — report the mean with a 95% interval over
prompts (normal-approximation CI for the mean; Wilson intervals when you
threshold `R` into a rate, e.g. "fraction of prompts restoring at least half
the effect" — [Ch. 02](../02-evaluation-science-and-experimental-design/README.md) §3.5 applied to internal variables). Preselect sites or correct for
multiplicity: 24 grid sites tested at per-site α = 0.05 give a ~71% chance
of at least one spurious "significant" site under a global null (computed in
the solutions), and a single-site number is never interpretable without its
control arms.

## 4. Worked example: locating the misconception-refutation signal

**The behavioral construct.** TruthfulQA's core phenomenon is the imitative
falsehood: questions "targeting falsehoods that humans commonly believe or
repeat," where the wrong answer is more statistically frequent in the
training distribution [datasets/cards/01-truthfulqa.md]. The benchmark is an
817-question validation split, single split, evaluation-only, with
adversarial subcategories including **Misconceptions** observable on the
canonical page [datasets/cards/01-truthfulqa.md]. Our construct: is the
*refutation signal* — the computation that makes the true answer
out-compete the imitative one — localizable in the network? We ask it with
M12, a 12-layer decoder-only reference model (a course-designed stand-in for
the pre-trained transformer LMs the patching literature analyzes [CLM-0047,
CLM-0048]) and `n = 100` misconception-style short-answer prompts drawn from
the Misconceptions pool, pinned by index list before any patching run, each
with a designated true answer and the paired common-falsehood answer (the
817-row split is the verified pool size; the 100-prompt subsample is our
design budget). Everything below is a *designed numerical example*: the
numbers are the course's own, recomputed exactly in the solutions — not
measurements of a named deployed model.

**Step 1 — the three baseline arms.** Clean run: `Δ_clean = +2.40`. Corruption
A, embedding noise on the question tokens: `Δ_corrA = −1.60` — the margin
flips, the imitative answer wins, and the total effect to explain is
`TE = 2.40 − (−1.60) = 4.00` logits. Corruption B, subject substitution: `Δ_corrB = −0.80`. Two corruptions on purpose: a site that mediates the
behavior under only one corruption is explaining the corruption, not the
behavior.

**Step 2 — the patching grid.** Patch clean activations into the corrupted
run (corruption A) at each of 24 sites (12 layers × {attention, MLP}), all
token positions (representative rows shown; full grid recomputed in the solutions):

| Layer | attn Δ_p → R | MLP Δ_p → R |
|---|---|---|
| 0 | −1.52 → 0.02 | −1.48 → 0.03 |
| 2 | −1.28 → 0.08 | −1.12 → 0.12 |
| 4 | −0.64 → 0.24 | −0.28 → 0.33 |
| 5 | −0.16 → 0.36 | +0.16 → 0.44 |
| 6 | +0.24 → 0.46 | +0.64 → 0.56 |
| **7** | +0.56 → 0.54 | **+1.04 → 0.66** |
| 8 | +0.32 → 0.48 | +0.88 → 0.62 |
| 11 | +1.76 → 0.84 | +2.00 → 0.90 |

Read the table twice, differently. Mid-network (layers 5–8) the MLP sites
restore substantially, peaking at layer 7 (`R = 0.66`), with the same
layer's attention carrying less (`R = 0.54`) — a shape echoing the
literature's mid-MLP findings [CLM-0047, CLM-0049]. But layer 11 restores
*more* than layer 7 — see section 6: late sites are where the answer
already sits, and patching them is close to tautological.

**Step 3 — position refinement.** At (layer 7, MLP), restrict which token
positions receive the patch: last subject token only → `Δ_p = +0.60`,
`R = 0.55`; full three-token subject span → `Δ_p = +0.92`, `R = 0.63`;
non-subject tokens → `Δ_p = −1.28`, `R = 0.08`. The decisive activations ride
on the subject tokens, mostly the final one — the subject-token signature the
causal-tracing literature reports for factual recall [CLM-0047].

**Step 4 — control arms.** Same site, same corruption, different donors:
patch with activations from an *unrelated* prompt → `R = 0.04`
(random-patch control); from a *different clean misconception question* at
the same positions → `R = 0.10` (matched-topic control) — the site is
question-specific, not merely "active", and a clean-into-clean sanity patch
reproduces `Δ = 2.40` (`R = 1.00` by construction), confirming the patching
machinery itself does not perturb an uncorrupted run. **Step 5 —
statistics.** Per-prompt restoration at the winning site: mean `R = 0.66`,
SD `0.16`, `n = 100` → SE `0.016`, 95% CI **[0.63, 0.69]**; as a rate,
69/100 prompts restore at least half the effect → Wilson 95% **[0.59,
0.77]** (arithmetic in the solutions) — not one or two runaway prompts.

**Step 6 — the causal claim (the artifact).** A claim that survives the
controls, with its scope fenced in:

> In reference model M12, on 100 TruthfulQA-Misconceptions-style prompts,
> layer-7 MLP activations at the subject tokens mediate a substantial share
> of the true-vs-imitative answer margin (R = 0.66, 95% CI [0.63, 0.69])
> under embedding-noise corruption; the mediation replicates under subject
> substitution (R = 0.68), is absent under random-patch (0.04) and
> matched-topic (0.10) controls, and transfers partially to paraphrases of
> the same questions (R = 0.52) and less to a novel subcategory (R = 0.38).
> The claim covers this model, these prompt distributions, and these
> corruption contrasts — not an "honesty module".

Note what the claim *refuses* to say: nothing about all misconceptions
(transfer said so); nothing about where the fact is *stored* (layer 11 also
restores — section 6); nothing about other behaviors (refusal, sycophancy)
in the same model, superposition (`chapters/10`), deployed models, or
editing the model to change its answers. It cannot rule out redundancy
either: components elsewhere may compute the same signal and only matter
when layer 7 is broken — the ablation-with-backup phenomenon reported as
synergistic components in the mediation literature [CLM-0048].

## 5. Comparison of approaches to "where is it computed?"

| Approach | What it asks | Key assumptions | Failure modes | When it is right |
|---|---|---|---|---|
| Logit / path attribution (decompose the clean run) | which components *contribute* to the output | linearity of the decomposition; no counterfactual | pure correlation; late layers dominate by construction | fast triage of a clean run; hypothesis generation |
| Ablation (zero / mean / noise out a component) | is the component *necessary* | "off" is a meaningful baseline; no downstream compensation | redundancy: backups mask the component; mean-ablation drifts off-distribution | necessity checks; monitors that must survive component loss |
| Activation patching (this chapter) | does information *flow through* the site, clean vs corrupted | surgical intervention; corruption defines the contrast | corruption-specificity; trivial late sites; synergy breaks additivity | localizing a behavior's carriers before deeper analysis |
| Path patching (patch a component's *output* into another run) | which component *uses* the information | you already know which sites to connect | combinatorial site pairs; same controls still mandatory | separating writers from readers within a candidate circuit |
| Model editing (change weights, re-measure) | does changing the site durably *change the behavior* | edit stays local; no side effects elsewhere | specificity loss: other behaviors degrade silently | when persistent change is needed, audited with held-out checks |

The rows are complementary, and project `P06` runs them in order:
attribution to propose, patching to localize, ablation for necessity. The
ordering rule that matters: **attribution proposes, intervention disposes**
— no clean-run decomposition substitutes for the corrupted-run contrast, and
all interventional rows inherit [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)'s
ledger: denominators, intervals, and both sides — what the intervention
fixes *and* what it breaks.

## 6. Counterexample: where this chapter's methods fail

**The trivial-site confound (stored ≠ computed).** In the worked example,
layer 11's MLP restores `R = 0.90` — more than the "interesting" layer-7
`0.66` — because by layer 11 the answer is already written into the stream,
so patching there re-installs the conclusion rather than the computation.
Single-site restoration cannot distinguish the site that *computes* a
feature from every later site that merely *relays* it; the honest reading of
a patching grid is "the earliest layer where restoration climbs is where the
computation begins to matter" — and even that presumes the corruption did
not shift the computation itself.

**Corruption-dependence and redundancy.** `R(s)` is defined relative to a
corruption: in our example the layer-7 estimate is stable across two
corruptions (0.66 vs 0.68), but that is a check you must run, not a property
you can assume — which is why the artifact's claim names its contrast. And
if two components compute overlapping signals, single-site patches over- or
under-count their roles, while ablating one can trigger compensation by
another — the mediation literature reports components that amplify or repress
each other's effects [CLM-0048]. The fix for both is joint patches and joint
ablations; skipping them is invisible in every single-site heatmap.

**Off-distribution interventions break the linear story.** Scale the patched
clean-minus-corrupted contribution at the winning site by α: measured `Δ`
tracks the linear prediction at α = 0.5 and 1.0, saturates at α = 1.5
(+1.92 vs +2.36 linear), and degrades at α = 2.0 (+2.30 vs +3.68, with
14/100 prompts degenerating into repetition loops) — a causal claim validated
at the clean-vs-corrupted contrast does not license turning the site into a
dial. The collateral ledger agrees: at α = 1.5, accuracy on a 60-item
unrelated QA set falls from 49/60 (Wilson 95% [0.70, 0.89]) to 38/60
([0.51, 0.74]) — an 18.3-point drop (arithmetic in the solutions).

**Multiplicity and small grids.** A 24-site grid at per-site α = 0.05 yields
at least one spurious "significant" site with probability ≈ 0.708 under a
global null (~1.2 expected false positives; computed in the solutions):
preselect sites, correct for multiplicity, or replicate the grid on a second
prompt set. And a compelling visualization is not evidence at all: the map
renders one of these numbers, and `chapters/10` makes faithfulness evaluation
its whole subject.

**The construct gap, inherited.** If `Δ` is not a valid instrument for the
behavior construct, the patching experiment is a beautifully controlled
measurement of the wrong thing — [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
§6's "precise measurement of the wrong thing" applies verbatim here. A
perfectly controlled patching grid of a mis-specified margin manufactures
confidence, not validity. No internal-machinery sophistication repairs an
upstream construct error.

## 7. Readings

**Verified in this build** — all five fetched in-session on 2026-10-21 (access levels per the source register):

- Elhage et al., *A Mathematical Framework for Transformer Circuits*
  (Transformer Circuits, 2021) — full-text-read (the site's full HTML). The
  residual-stream framing, QK/OV decomposition, and composition taxonomy
  section 3 is built on [CLM-0046]. Skeptical note: cleanest results are for
  *attention-only* models; the framework is a lens, not a proof.
- Meng, Bau, Andonian, and Belinkov, *Locating and Editing Factual
  Associations in GPT* (arXiv:2202.05262) — abstract-read. The
  causal-tracing design our clean/corrupted/patch logic follows, and the
  mid-MLP, subject-token findings our grid echoes [CLM-0047]. Skeptical
  note: "storage" is inferred from mediation plus editing.
- Vig et al., *Causal Mediation Analysis for Interpreting Neural NLP: The
  Case of Gender Bias* (arXiv:2004.12265) — abstract-read. The
  total/direct/indirect-effect framing and the sparse, synergistic
  mediation findings behind sections 3.4 and 6 [CLM-0048].
- Tigges, Hollinsworth, Geiger, and Nanda, *Linear Representations of
  Sentiment in Large Language Models* (arXiv:2310.15154) — abstract-read.
  The feature-representation evidence (single-direction sentiment, causal
  interventions, the 76%/36% ablation numbers) grounding section 3.3
  [CLM-0049]. Skeptical note: one feature family on curated distributions.
- TransformerLens (TransformerLensOrg/TransformerLens, GitHub) —
  page-inspected. The tooling: loads 15,000+ open models across 140+
  architecture families, exposes internal activations, and lets you hook
  functions that edit, remove, or replace activations as the model runs —
  the interface project `P06` builds on [CLM-0050].

**Verification notes** (registers record the details): the Vig candidate
title resolved to the retitled version above; `activationpatching.com` was
unreachable in-session (DNS failure, 2026-10-21); the candidate "Not All
Language Model Features Are Linear" paper was not findable by title on
arXiv this session, so Tigges et al. is the verified replacement. **Optional
deeper material** (not verified this build): the `chapters/10` and
`chapters/11` reading lists.

**Note companions:** [34 Othello-GPT — the probe-plus-intervention evidence pattern](../../research/notes/34-emergent-world-representations.md)[50 Induction heads — the six-argument mechanism hypothesis](../../research/notes/50-induction-heads.md) [52 ROME — facts as localized, editable computation](../../research/notes/52-rome-factual-associations.md)

## 8. Exercises

**Exercise 9.1 — analysis: auditing a "we found the refusal module" claim.**
A team patches an 8-layer model's *refusal margin* (logit of
refusal-continuation minus logit of compliance-continuation) on 40
harmful-request prompts: clean margin `Δ_c = +1.80`, corrupted
(embedding-noise) `Δ_k = −2.20`, single-site patches — layer-4 attention
`Δ_p = −0.92`; layer-5 MLP `Δ_p = +0.64`; layer-6 MLP `Δ_p = +0.76`;
layer-7 MLP `Δ_p = +1.12`; random-patch control `Δ_p = −1.96`. Per-prompt
restoration at layer-5 MLP: mean 0.71, SD 0.24; on a 20-prompt paraphrase
set it drops to 0.44. The team concludes: "layer-5 MLP computes the refusal
decision; layer-5 is where refusal lives." (a) Compute the restoration
fractions and the 95% CI for the layer-5 mean (show the arithmetic).
(b) Using their own numbers, explain why the conclusion is unsupported —
name at least three distinct problems, including the layer-7 number and the
paraphrase drop. (c) Write the claim sentence they are actually entitled to.
(d) Specify two missing control arms and what each would rule out.

**Exercise 9.2 — design: a patching protocol for a harmfulness feature.**
Design (do not run) a complete activation-patching study that localizes the
computation distinguishing harmful from benign requests in a chat model,
using XSTest's 250 safe prompts across ten superficial-similarity types
plus its 200 unsafe contrast prompts [datasets/cards/06-xstest.md]. The
protocol must specify: the construct and its gap sentence; the metric and
why it is a margin; clean, corrupted, and at least two control arms
(including how the corrupted prompt family is constructed and why that
family defines the claim's scope); the patching grid and multiplicity plan;
the statistics (intervals, denominators); off-distribution checks (transfer
to paraphrases and across XSTest prompt types, an amplification sweep with a
collateral-damage ledger); stopping rules and pre-stated disconfirming
criteria; and the exact causal-claim sentence you could write if everything
passes. State the two most likely ways your own protocol produces a
misleading result anyway. 700–1,200 words.

## 9. Hints and solutions

Full worked solutions with all arithmetic recomputed programmatically and
assessor rubrics are in [solutions.md](solutions.md). Attempt both first —
the rubrics grade the reasoning trail (which controls fire, which claims get
fenced) at least as heavily as the numbers.

## 10. Completion

**You have completed this chapter when you can:**

- [ ] Draw the residual-stream computation of a decoder-only transformer
      and name what attention and MLP blocks each write.
- [ ] Write the three-arm patching design with two control donors and say
      what each arm rules out.
- [ ] Compute restoration fractions and intervals from raw logit-difference tables, and tell a trivial late site from an informative mid-site.
- [ ] Produce Exercise 9.2's protocol at rubric level — the artifact that
      project `P06` turns into code.

**Prev:** [Ch. 08 — AI control and monitoring](../08-ai-control-and-monitoring/README.md)
(monitors are consumers of interpretability claims). **Next:**
`chapters/10-sparse-features-circuits-and-interpretability-evaluation`
(backtick mention only; does not exist yet). **Cross-track:**
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) and
[Ch. 07](../07-deception-scheming-and-evaluation-awareness/README.md);
project `P06` operationalizes this chapter's claim format.

### References

- [CLM-0046] Elhage et al., *A Mathematical Framework for Transformer Circuits*, 2021 (full-text-read).
- [CLM-0047] Meng et al., *Locating and Editing Factual Associations in GPT*, arXiv:2202.05262 (abstract-read).
- [CLM-0048] Vig et al., *Causal Mediation Analysis for Interpreting Neural NLP: The Case of Gender Bias*, arXiv:2004.12265 (abstract-read).
- [CLM-0049] Tigges et al., *Linear Representations of Sentiment in Large Language Models*, arXiv:2310.15154 (abstract-read).
- [CLM-0050] TransformerLens repository, TransformerLensOrg/TransformerLens (page-inspected).
- [datasets/cards/01-truthfulqa.md] — 817-question validation split, Misconceptions subcategory (page-inspected).
- [datasets/cards/06-xstest.md] — 250 safe + 200 unsafe prompts for Exercise 9.2 (page-inspected).

### Notation

| Symbol | Meaning | Introduced |
|---|---|---|
| `x_t^(0)`, `x_t^(l)` | token embedding; residual stream at position `t` after layer `l` | §3.1 |
| `a_t^(l)`, `m_t^(l)` | attention / MLP block output written at layer `l` | §3.1 |
| `W_QK`, `W_OV` | query-key and output-value circuits of an attention head | §3.2 |
| `X`, `Y`, `M_s` | input (prompt), output metric, mediator at site `s` | §3.4 |
| `TE`, `IE`, `DE` | total, indirect, direct effects | §3.4 |
| `Δ`, `Δ_c`, `Δ_k`, `Δ_p(s)` | logit-difference margin; clean, corrupted, patched runs | §3.5 |
| `R(s)` | restoration fraction at site `s` | §3.5 |
| `s = (l, block, positions)` | a patch site: layer, block, token positions | §4 |
| `α` | amplification factor for off-distribution checks | §6 |

Chapter 09 opens Phase E: from here on, every interpretability claim — in a
paper, a product, or a `P06` output — is graded by its controls, not its heatmap.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [lecture-10-mechanistic-interpretability](../../courses/boaz-barak-cs2881/lecture-10-mechanistic-interpretability.md) | Harvard CS 2881 | four labs' bets on opening the box — activations, SAEs, circuits |
| [part-02-05-interpretability](../../courses/google-deepmind-agi-safety/part-02-05-interpretability.md) | DeepMind AGI Safety | why the internal channel matters for safety claims |
