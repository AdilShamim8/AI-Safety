# Comparison note 01 — RLHF vs DPO vs RLAIF: three ways to buy the same thing

> Comparison notes: 1 of 5 planned (the others: behavioral vs mechanistic
> evidence; alignment vs control; prompt defenses vs authorization
> boundaries; benchmark scores vs deployment assurance). Sources:
> SRC-PAPER-009 (InstructGPT), SRC-PAPER-010 (DPO), SRC-PAPER-011
> (Constitutional AI), SRC-PAPER-012 (Ziegler et al.) — all
> **abstract-read** in the register, so this note compares at exactly
> that level: what each abstract states, what the chapter derived
> independently, and what no fetched text can yet settle. Companion
> chapter: 04 (preference learning and post-training); companion
> project: P02 (what proxy-objective training actually does).

## The question a comparison exists to answer

All three methods answer the same buyer's question — *I have a base
model and preferences I cannot write down as a loss function; how do I
make the model serve them?* — and they differ in the *intermediate
object* each inserts between the preferences and the policy:

| | RLHF | DPO | RLAIF |
|---|---|---|---|
| intermediate object | a trained reward model | none — the policy is the reward model | a preference model trained on AI feedback |
| loop | RL (PPO-style) against the reward | direct classification on preference pairs | RL against the AI-trained preference model |
| whose feedback trains the intermediate | human labelers | human labelers (the same pairs) | a constitution + the model itself |
| canonical source | InstructGPT (SRC-PAPER-009) | DPO (SRC-PAPER-010) | Constitutional AI (SRC-PAPER-011) |

The comparison that matters is not "which wins on benchmarks" (each
paper's evaluations are its own, on its tasks, at its scale — cited at
exactly that strength) but *what each method's machinery buys and
costs* — because the costs show up later as safety problems, and the
safety curriculum's chapters 03–05 exist to catalog them.

## The three methods, each stated at its evidence level

**RLHF (InstructGPT, SRC-PAPER-009, abstract-read):** the three-stage
pipeline — supervised fine-tuning, then a reward model trained on
human preference comparisons, then PPO-style RL against that reward —
with the abstract-level result that a 1.3B RLHF model's outputs are
*preferred* to the 175B base model's on the authors' prompt
distribution. The register's limitation paragraph is the comparison's
first honest entry: the preference result is a **construct statement**
(labelers, distribution, and comparison protocol are all
authors-chosen), not a general alignment claim — a 1.3B model being
"better than" a 175B one *at being preferred by those labelers on
those prompts* is the actual content. The safety cost the chapter
attaches: the reward model is a **proxy** (chapter 03's whole
subject), and PPO optimizes against it *hard* — Goodhart belongs to
this row of the table by construction.

**DPO (SRC-PAPER-010, abstract-read):** the derivation the chapter
rebuilt and numerically verified — under a KL-constrained RLHF
objective with a Bradley–Terry preference model, the optimal policy has
a closed form *in terms of the reference policy*, so the RL loop can
be eliminated entirely and the policy trained by a classification loss
directly on preference pairs. What the elimination buys (the abstract
stated program; the chapter's own derivation and toy-policy checks):
no reward model to exploit, no PPO machinery, offline stability. What
it quietly changes: the KL anchor moves from "a penalty inside an RL
objective" to "a structural fact of the loss" — the policy is
*always* tethered to the reference by the closed form, which is a
different kind of constraint than the one you can anneal. The safety
cost the chapter attaches: DPO optimizes the *same* preference signal
with *different* failure geometry — proxy mis-specification survives
the change of machinery (a bad preference pair is still a bad
preference pair), while the PPO-specific overoptimization pressure is
replaced by classification-specific ones (the chapter's gradient
structure discussion).

**RLAIF (Constitutional AI, SRC-PAPER-011, abstract-read):** the
two-phase structure — supervised self-critique and revision
fine-tuning against explicit principles (the "constitution"), then RL
from AI feedback via a preference model the model's own critiques
trained. What it buys: preference signal at RLHF-like method shape
without RLHF-like labeler volume — the constitution is written once,
the AI feedback scales. What it costs, and this is the comparison's
sharpest entry: the feedback loop *folds back on the model itself* —
the same system generates, critiques, and judges (with principles as
the stated control), and the register's limitation paragraph already
carries the honest tag: internal self-evaluation by the authors'
organization, method reference, **not an independent audit**. The
judge-agreement numbers that would calibrate "AI feedback tracks
human judgment" live in the unread full text; this note does not
quote them.

## The cross-comparison, dimension by dimension

**Feedback source and its audits.** All three train on preference
comparisons, and all three inherit the label-quality problem that
SRC-PAPER-012 (Ziegler et al., abstract-read) made explicit early:
the published admission that labelers may rely on simple heuristics,
at 60,000-comparison summarization scale (2019). RLHF's audits are
human-labeler audits; DPO inherits them unchanged (the same pairs);
RLAIF's audits become *AI-judge audits* — cheaper, faster, and one
indirection further from the preference you actually wanted, which is
why the constitutional layer exists at all: it is the stated
mechanism for keeping the AI's judgments tethered to written
principles rather than to the model's own drift.

**The proxy problem.** Chapter 03's frame prices all three rows the
same way at the top: preferences you cannot write down are
*specifications you are training an approximation to*, and every
method here trains a model *of the specification* and then optimizes
a policy *against the model*. RLHF: reward model → PPO
(overoptimization pressure, the Goodhart lane). DPO: Bradley–Terry
surrogate folded into the loss (the surrogate *is* now the
specification — cleaner, not safer). RLAIF: preference model trained
on self-critique (the specification's approximation is itself
approximated — one more derivative of the thing you wanted). A buyer
who can state their preference as a loss function should notice that
*none of these methods is for them* — and a buyer who cannot should
notice that each indirection is a place mis-specification can enter
silently. P02's environments exist to make that statement checkable.

**Engineering surface.** RLHF: reward model training + PPO (rollouts,
value estimates, KL penalty tuning — the largest surface). DPO: a
classification loss (the smallest surface — its abstract-level selling
point, and honest). RLAIF: constitution authoring + self-critique
generation + preference-model training + RL (the largest *thinking*
surface: the engineering moves into prompt/constitution design, where
evaluation is hardest to standardize).

**What each abstract-level result actually licenses.** InstructGPT's
1.3B-vs-175B *preference* result: preference under stated labelers and
distribution, nothing about capability or safety. DPO's
derivation: mathematically checkable and *independently re-derived
and numerically verified by this course's chapter 04* (the strongest
evidence class in this comparison — a derivation you can check beats
an evaluation you cannot); its PPO-vs-DPO comparisons: the authors'
task suite. Constitutional AI's harmlessness results: the authors'
internal evaluations, method reference only. The comparison note's
own register-grade summary sentence: *DPO's core claim is checkable
without access; the other two are audits of other people's setups.*

## What this comparison cannot settle (and what would settle it)

At abstract-read strength, none of: per-method label-cost curves,
judge-human agreement for RLAIF, overoptimization-depth comparisons
under matched budgets, or preference-model scaling behavior — all
live in unread full texts, and each is listed as a candidate next
fetch in the register's pending pattern. What *would* settle the
safety-relevant slice: a paired, preregistered comparison (chapter
02's discipline; P02's protocol format) holding data, budget, and
evaluation fixed across the three objectives on a task with a known
ground-truth specification — which is exactly the experiment family
P02's environments were built to host, and the honest gap this note
records rather than papers over.

## Where this connects

- Chapter 04 (sections 3–4): the pipeline descriptions, the DPO
  derivation, and the label-quality audit this note compares.
- Chapter 03 + P02: the proxy-specification frame that prices all
  three rows identically at the top.
- The from-scratch track (research/ai-researcher-from-scratch/): module
  07's template B — a learning-rate/hyperparameter search protocol —
  is the artifact a learner would fill to run any of the three at toy
  scale with preregistered claiming.
