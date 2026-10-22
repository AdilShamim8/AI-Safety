# Note: Towards Monosemanticity: Decomposing Language Models With Dictionary Learning (2023)

Source: SRC-PAPER-030 · Access: full-text-read (20.6MB page;
terminology spot-verified programmatically: Problem Setup, Sparse
Autoencoder Setup, the Arabic/DNA/base64/Hebrew feature
investigations, the Feature Splitting section, dead features, and
the intuition-and-anecdote sentence) · Read: 2026-10-21 · Note
level: **method-level**.

## The actual problem

The authors' framing: neurons are polysemantic (one neuron, many
meanings) because models store more features than neurons
(superposition) — so learn a *dictionary* that decomposes
activations into sparse feature combinations, and check whether the
dictionary's atoms are monosemantic. The operational version: train
sparse autoencoders on a one-layer model's MLP activations, inspect
the learned features, and establish the method's diagnostics.

## Method

The setup: an SAE trained on the MLP activations of a one-layer
transformer — encoder-decoder with a sparse bottleneck (dictionary
size >> neuron count, L1-style sparsity so few atoms fire per
token). The inspection program (spot-verified): specific feature
investigations — **Arabic script, DNA sequences, base64, and Hebrew**
among them — where a dictionary atom is shown to fire on exactly
that concept family, plus the global diagnostics.

The diagnostics the paper established (the method's self-checks, now
standard): **dead-feature counts** (atoms that never fire — wasted
capacity) and the **feature-density bimodality** (the firing-rate
distribution splitting into rare-semantic and frequent-structural
clusters). And the flagship phenomenon: **feature splitting** — as
dictionaries grow, one feature resolves into several more specific
ones (the San Francisco lineage in the successor paper).

The design logic: dictionary learning as the superposition antidote —
if polysemanticity is capacity-driven compression, then
overcomplete sparse coding should un-compress the representation
back into interpretable atoms.

## Central evidence

- The concept-feature demonstrations (Arabic, DNA, base64, Hebrew —
  the spot-verified investigations): individual atoms firing
  precisely on interpretable concept families in a real (if tiny)
  trained model.
- The self-diagnostics: dead features and density bimodality — the
  paper grading its own dictionaries rather than only showing
  highlights.
- The authors' own epistemics sentence (spot-verified as the
  intuition-and-anecdote line): the evaluation is largely intuition
  and anecdote — self-administered rubrics plus automated
  interpretability, stated by the authors themselves (the register's
  supports entry carries this verbatim).

What the evidence does NOT carry: no behavioral claims (features
found and inspected, not intervened with — the mediator upgrade is
chapter 11's discipline); one-layer-model scope only; no completeness
claim (the successor paper's London-boroughs exercise is the
quantified admission).

## Assumptions

Tested in-paper: the SAE training setup's stability (the
diagnostics); the interpretability of individual atoms on the toy
model.

Inherited: that the sparse-coding premise (activations = sparse
feature mixtures) matches the model's actual generative structure —
superposition is the hypothesis, dictionary learning is the test,
and the test is only as good as the inspection; that MLP activations
are the right site (the framework's residual-stream view says
computation is distributed — the site choice is a bet).

## Limitations

Authors' (fairly represented): the intuition-and-anecdote admission
— evaluation is self-administered; one-layer scope.
Mine: the toy model satisfies the method's premises by construction
(sparse features, weak superposition) — the pedagogically honest
reading is that the paper demonstrates the *method and diagnostics*
where they work best, and the successor paper demonstrates the
scaling caveats where reality bites; the register also notes the
URL path is /2023/monosemanticity (the canonical Transformer
Circuits Thread home).

## Nearest alternatives

- **Scaling Monosemanticity (SRC-PAPER-032)**: the successor —
  1M/4M/34M features on Claude 3 Sonnet, the same method's frontier
  stress test with splitting and incompleteness quantified.
- **The circuits framework (SRC-PAPER-025)**: the substrate — the
  residual-stream view that makes "MLP activations as feature
  mixtures" a well-posed idea at all.
- **Classic sparse coding / dictionary learning (the signal-
  processing ancestor)**: the mathematical machinery — the paper's
  novelty is the application and the interpretability reading, not
  the optimizer.

## Replication feasibility

High — the course's natural SAE unit (chapter 10's drill): train
SAEs at 512/2k/8k atoms on a one-layer model (the `ml` tier's
smallest setting), run the diagnostics (dead features, density
bimodality), and watch a coarse feature split. What breaks first:
interpretability itself is *easier* on toys (clean atoms) — the
small-scale replication honestly demonstrates the method, not the
difficulty, and must say so.

## Falsifiable extension

Hypothesis: dead-feature rate predicts interpretability-relevant
capacity loss non-linearly — dictionaries above a dead-feature
threshold show a disproportionate drop in *concept coverage*
(not just atom count), because dead atoms cluster at the
rare-semantic density mode where the interpretable concepts live.
Design: train SAEs across sparsity penalties (a dead-rate ladder);
per rung, measure concept coverage on a closed concept class plus
the dead rate. Metric: coverage with intervals vs dead rate — the
curve's shape is the result. What counts against: if coverage falls
linearly with dead rate, dead features are wasted capacity but not
concentrated waste — the diagnostic's importance is real but
unremarkable, and my clustering premise fails.

## My interpretation vs. their claims

Their claims: (1) dictionary learning decomposes a real trained
model into (largely) monosemantic features; (2) the method carries
its own diagnostics; (3) evaluation is, honestly, intuition and
anecdote at this stage.

My interpretation: (1) founded the current interpretability program
— the move from "neurons are inscrutable" to "atoms are inspectable"
is the field's biggest single step since the circuits framework; (2)
the self-diagnostics are the paper's most under-cited contribution:
grading your own dictionary (dead features, density bimodality) is
the difference between a method and a demo, and the successor
papers inherited exactly that discipline; (3) the
intuition-and-anecdote admission is the paper's best paragraph — it
prices its own evidence honestly, and the course's answer to that
price is the intervention leg (chapter 11) and the audit discipline
(chapter 10's reconstruction-intervention score), which is what
"towards" in the title turned out to mean.
