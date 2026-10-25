# Note: DPO — the objective that deleted the reward model (2023)

Source: SRC-PAPER-010 · Access: **abstract-read** (arXiv v3 page,
verified with the chapter-04 build) · Note level: **abstract-level**.

## The actual problem

RLHF's pipeline has three moving parts (SFT, a learned reward model,
RL against it) and every part adds a failure surface: the reward model
can be gamed (Ch.03's Goodhart chain), the RL is unstable and
expensive, and the KL leash trades honesty for control. The paper's
question: if what you ultimately want is "make the policy prefer the
chosen response over the rejected one," why route through a reward
model at all?

## Method (as the abstract establishes it)

The reparameterization: derive a closed-form loss on the POLICY
directly from the preference pairs — the Bradley–Terry preference
model inverted to express the optimal policy as a function of the
reference policy, giving a classification-style objective on paired
comparisons with no reward-model inference step and no RL loop. The
register's supports field records what this course takes from it:
chapter 04 carries the complete derivation end-to-end, and P04 audits
the seam it opens (below).

## Results (abstract-level, honestly priced)

Stable, performant preference tuning at RLHF-comparable quality with
a simpler pipeline — as an abstract statement about the paper's
benchmarks. What the abstract does NOT give: the beta (reference
weighting) sensitivity analysis, the limits under off-distribution
preference pairs, and the label-noise behavior P04's audit measures
on its own organism. Those live in the unread body; the course's
positions on them come from its own pinned experiments, honestly
labeled as such.

## What this note does NOT claim

No benchmark reproduction, no body-level claims about the paper's
specific comparisons. The derivation itself is mathematics — chapter
04 verified it by hand (it either follows or it does not), which is a
stronger check than an abstract read, and that distinction is recorded
here.

## Falsifiable extension

P04 already runs the seam: DPO's closed form inherits Bradley–Terry's
four silent assumptions (transitivity, scale separability, pair
exchangeability, label noise as symmetric), and a biased label stream
should produce a calibrated-looking model with a shifted optimum.
The extension P04 pins: label-bias drift of −0.0645 on the drift
condition, and proxy/held-out divergence +8 — the numbers to beat.
Next step at course scale: sweep beta at three values under the SAME
biased stream and report whether the drift shrinks monotonically with
the reference weight (the "KL leash" hypothesis carried into DPO's
vocabulary) or is beta-insensitive (the bias lives in the pairs, not
the objective). Stopping rule: monotone in beta confirms the leash;
flat confirms the pairs. Either result is a real finding about where
DPO's protection actually comes from.

## My interpretation vs. their claims

Their claim: preference tuning without RL is stable and effective.
My reading: correct, and the durable contribution is the
REPARAMETERIZATION pattern — find what the intermediate model was
computing, express it as a constraint on the thing you actually train.
But the pattern's honesty clause is what this course teaches: deleting
the reward model deletes the *observable* misalignment surface, not
the misalignment risk. The proxy moved inside the objective (P04's
headline), and "no reward model to game" became "the objective itself
is the proxy" — a cleaner sentence in the safety case, not a smaller
one.
