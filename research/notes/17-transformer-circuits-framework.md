# Note: A Mathematical Framework for Transformer Circuits (2021)

Source: SRC-PAPER-025 · Access: full-text-read (2.4M characters of
page text; terminology spot-verified programmatically: residual
stream as communication channel, QK/OV circuits, heads independent
and additive) · Read: 2026-10-21 · Note level: **method-level**.

## The actual problem

The authors' framing: interpretability research was drowning in
empirical phenomena without a shared formal object — so give the
transformer a mathematical decomposition precise enough that
"an attention head did X" becomes a claim with defined parts. The
operational version: the residual-stream view — the transformer as
a communication channel architecture where components read and write
by addition, making every intervention and attribution well-defined.

## Method

The framework's core moves (each now load-bearing vocabulary in
chapters 09–11):

- **The residual stream as a shared communication channel**: each
  token position carries a vector that attention and MLP blocks
  *read from and write to by addition* — x_t^(l+1) = x_t^(l) +
  a_t^(l) + m_t^(l). The model is a growing sum, not a stack of
  opaque layers.
- **Attention heads as independent, additive, parallel components**:
  heads are (in the two-layer analysis) separable contributors to
  the stream — the property that makes "remove this head" and
  "patch that head's output" well-typed interventions.
- **The QK/OV split**: each head factors into W_QK (where to look —
  the query-key pattern over positions) and W_OV (what moves — the
  value-to-output map). Information *movement* and information *use*
  become separately analyzable circuits.
- **MLP blocks as key-value memories** (the two-layer-attention-
  equivalent reading): layers as associative memories whose keys
  and values can be read out.

The cleanest results are stated for **two-layer models and induction
heads** — the framework's demonstration cases. The method is the
decomposition itself; everything downstream (patching, circuits,
feature attribution against the stream) is the vocabulary in use.

## Central evidence

- The two-layer analyses and the induction-head account (the named
  demonstration phenomena) — where the framework's claims are proven,
  not sketched.
- The additivity of head contributions — the property the entire
  intervention program (chapter 09's patching grids) depends on:
  patching is well-defined because writing is addition.
- The register's own caveat, carried verbatim: the claim that the
  framework "scales" to production models was **aspiration at
  publication date, not demonstration** — the scaling story is the
  later program's (monosemanticity, features), not this paper's.

What the evidence does NOT carry: no production-model circuit
analyses (two-layer and toy demonstrations only); no superposition
treatment (the framework predates the superposition hypothesis's
center stage — heads are analyzed as if features were sparse and
monosemantic); no account of nonlinear composition beyond the
two-layer case.

## Assumptions

Tested in-paper: the decomposition's well-definedness on two-layer
models; the induction-head phenomena.

Inherited: additivity as *sufficient* for interpretability (heads
interact — the later synergistic-components finding (chapter 09's
mediation discussion) shows additive bookkeeping can miss
amplification); the sparse-features premise (superposition makes
"one head, one behavior" the exception); the framework's
transferability to deep models (aspiration then, program now).

## Limitations

Authors' (fairly represented): the two-layer scope and the scaling
aspiration are the paper's own framing.
Mine: the framework's cleanest abstractions (independent heads, QK/OV
factorization) are first-order approximations whose error grows with
depth and superposition — the field's own later results (feature
splitting, absorption) are the correction terms; and the
mathematical precision creates a rhetoric risk the course prices:
equations over two-layer toys can read as if production models were
understood — the register's caveat exists to keep that reading
honest.

## Nearest alternatives

- **Activation patching / causal mediation (chapter 09's instrument
  family)**: the experimental methods the framework's vocabulary
  made rigorous — patching is well-typed *because* writing is
  addition.
- **Towards/Scaling Monosemanticity (SRC-PAPER-030/032)**: the
  superposition-aware continuation — the dictionary-learning program
  that handles what the clean framework assumed away.
- **The circuits-as-algorithms literature (induction heads and
  descendants)**: the phenomena-first tradition the framework
  formalized.

## Replication feasibility

High — chapter 09's worked example is the replication: the residual-
stream arithmetic, the QK/OV factorization, and a patching grid on a
small model are course-scale with the `ml` tier's smallest setting
(1–2 layer attention-only models). What breaks first: nothing in the
framework itself at toy scale — the honest course-scale finding is
that the framework *works* on toys precisely because toys satisfy
its premises (sparse features, weak superposition), which is the
aspiration-vs-demonstration caveat experienced rather than stated.

## Falsifiable extension

Hypothesis: additivity's interpretability value degrades measurably
with superposition density — in models where features are
superposed, per-head attribution (the framework's natural unit)
explains a shrinking fraction of intervention outcomes, and the
unexplained fraction is predicted by a superposition measure
(feature-density bimodality per the Monosemanticity diagnostics).
Design: attention-only models at increasing width/token counts (a
superposition ladder); at each rung, measure per-head ablation
outcome coverage vs the residual explained by head-sum predictions.
Metric: coverage fraction with intervals; correlation with the
density measure. What counts against: if coverage is flat across
the ladder, additivity survives superposition for the
intervention-outcome question (even if features are superposed) —
and the framework's first-order approximations are sturdier than my
degradation premise claims.

## My interpretation vs. their claims

Their claims: (1) the transformer admits a precise, compositional
mathematical description (residual stream, independent heads,
QK/OV); (2) two-layer analyses and induction heads demonstrate the
framework's power; (3) the framework is a foundation for scaling
interpretability to production models.

My interpretation: (1) is the most load-bearing conceptual
contribution in the interpretability literature — it converted
"understanding the model" from a metaphor into a decomposition with
well-typed interventions, and every course chapter in the
mechanistic arc is downstream of it; (2) the two-layer honesty is
underrated — the paper's willingness to prove things only where it
could is why the framework aged into a foundation rather than a
falsified fashion; (3) the scaling aspiration was the paper's
marketing and the field's to-do list, and the honest scorecard a
half-decade later is: vocabulary scaled completely (every paper
speaks residual stream), interventions scaled well (patching grids
on production models), and the clean circuit analyses scaled least
(superposition and scale broke the independence assumptions) — a
partial vindication whose shape the course teaches directly.
