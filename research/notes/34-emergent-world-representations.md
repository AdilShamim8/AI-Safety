# Note: Emergent World Representations — Othello-GPT and the evidence ladder (2022)

Source: SRC-PAPER-109 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Interpretability's hardest question is not "what does this head attend to"
but "does the model have a world model at all, and what would count as
evidence?" The paper takes the cleanest available version of that question:
a transformer trained *only* to predict legal Othello moves — an objective
with no incentive to represent the board, only move legality — and asks
whether the network's activations nonetheless encode the board state. If a
pure next-token objective on a game corpus builds an internal board
representation, then "next-token prediction cannot yield world models" is
empirically dead in its weakest form, and the interesting question moves to
*when* and *which* representations form (the Ch. 09 → Ch. 10 progression).

The abstract establishes the two results that carry the course's Ch. 09
bridge from "probing finds features" to "intervening on features changes
computation":

1. **Probing evidence** — linear probes trained on intermediate activations
   decode the board state. The model's residual stream carries a board
   representation the objective never demanded.
2. **Causal evidence** — the paper's central intervention: change the
   internal representation mid-game (a "latent move") and the model's
   *subsequent* move predictions update as if the latent move had been
   played. The representation is not a correlational shadow; it sits in
   the computational path.

The distinction between those two sentences is the entire difference
between Ch. 09's correlation caveats and Ch. 11's intervention discipline —
the note's reason for existing. Note 06 (P06's project) makes the same
distinction with the deployment-flip intervention; this paper is its
canonical source in the literature.

## Method (as the abstract prices it)

Train a transformer on synthetic Othello game transcripts (the objective:
predict the next legal move); train linear probes on activations to decode
board state; run the latent-intervention experiment. The abstract also
names the two-training-corpus comparison — transcripts of *legal* games
versus randomly generated (sometimes illegal) move sequences — with the
probes decoding board state in both cases, which the paper uses to argue
the representation is built by the learning problem, not memorized
transcripts.

What abstract-read does not establish: the probe accuracies, the layer
localization, the exact intervention magnitudes, and the nonlinear-probe
results the body carries. This note claims the two load-bearing results
above and nothing numerical.

## Why this note exists in the course

Chapter 09 needs a canonical example of *representation discoverable by
probing and load-bearing under intervention* in one paper, because the
chapter's core epistemic warning — readout is not causation (the same
warning P06's fixture pins at 0.915 probe accuracy on a spurious channel)
— is only half the lesson. The other half is that intervention can *settle*
the question probes raise. Othello-GPT is the standard citation for both
halves in one system, which is why it appears in Ch. 09's readings and in
Ch. 10's build-up to sparse features: a board state encoded in activations
is the toy-scale version of features encoding concepts (notes 03, 18), and
the latent-move intervention is the toy-scale version of the causal
feature edits Ch. 11 teaches.

The note also prices the field's standard objection honestly: a game with
fifty-eight reachable board squares and deterministic legality is about
the friendliest possible world for "world model" claims. The abstract
itself stays modest (it does not claim the result transfers); the note
inherits that modesty — the course's claim is about the *evidence pattern*
(probe + intervention), not about LLMs having human-like world models.

## The falsifiable extension (deterministic tier)

The paper's probe-vs-intervention logic is runnable on P06's organism
without any new compute:

- P06 already trains linear probes at two sites and runs the
  patching grid; the extension is the Othello move: **probe the mixer
  output, decode the *shortcut* feature (channel b), intervene on it in a
  direction the input never took, and test whether downstream predictions
  track the intervened value.** P06's b-ablation shows removal; the
  Othello-style experiment shows *setting* — a stronger form.
- Prediction worth testing: a linear probe on the mixer decodes channel-b
  presence at ≥0.9 accuracy (the fixture's spurious readout is 0.915 at
  s2), and a direction-aligned intervention flips downstream behavior at
  a rate statistically distinguishable from the random-patch control
  (which P06 already ships).
- Falsifier: if no single direction's intervention moves downstream
  predictions beyond the random-patch band, then the shortcut is
  distributed (not Othello-like), and the note's "toy-scale version of
  feature edits" analogy fails at this organism — a real result either
  way, and exactly the kind the research-method standing instruments
  section says to record.

One session, no model calls, and it turns P06 from a patching exercise
into a two-evidence-class replication of this paper's logic.
