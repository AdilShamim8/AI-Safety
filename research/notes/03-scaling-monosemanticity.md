# Note: Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet (2024)

Source: SRC-PAPER-032 · Access: full-text-read (Transformer Circuits
Thread web article, 16.3MB page, key claims spot-verified
programmatically: the 1M/4M/34M sizes, the San Francisco splitting
sentence, the London-boroughs completeness sentence, the safety-feature
section list) · Read: 2026-10-21 · Note level: **method-level**.

## The actual problem

The authors' framing: can sparse-autoencoder dictionary learning —
which the same group demonstrated on a one-layer toy model (Towards
Monosemanticity, SRC-PAPER-030) — scale to a production frontier model
and still yield interpretable features? The operational version: train
SAEs with millions of dictionary vectors on Claude 3 Sonnet's
activations and check (a) whether the learned features are
interpretable at all at that scale, (b) whether safety-relevant
concepts (deception, sycophancy, bias) show up as features, and (c)
what happens to feature identity as the dictionary grows.

## Method

The setup: sparse autoencoders trained at three dictionary sizes — 1M,
4M, and 34M (33,554,432) features — on Claude 3 Sonnet activations at
chosen sites. The sparse bottleneck plus L1-style sparsity pressure
yields dictionary vectors meant to carve superposed features into
one-direction-one-concept pieces. Evaluation is interpretability-
driven: inspect what activates each feature (representative example
inputs), trace activations through text, and — for the safety reading —
search for features corresponding to deception, sycophancy, and bias
categories.

The clever part: the scale ladder (1M → 4M → 34M on the same model)
turns dictionary size into the experimental variable — feature
splitting becomes an observable phenomenon rather than a conjecture.
The fragile part (the authors' own framing): evaluation is
representative-example inspection plus the authors' interpretive
judgment, self-administered by the model's manufacturer — there is no
external, preregistered interpretability benchmark, and the article
says so in its own epistemics.

## Central evidence

- **Interpretability at scale**: features at 34M remain individually
  interpretable (the article's central qualitative claim, carried by
  worked examples rather than counts).
- **Feature splitting, verbatim-verified**: a San Francisco feature in
  the 1M SAE splits into two features in the 4M and eleven in the 34M
  — feature identity is dictionary-size-relative; the "same" concept
  resolves differently at each scale.
- **The completeness gap**: features were found for only about 60% of
  London boroughs in the 34M SAE — the dictionary is incomplete even
  at 34M vectors, i.e., "the features" are not yet all of the features.
- **Safety-relevant categories present**: deception-, sycophancy-,
  and bias-related features found and inspected — the existence claim,
  not a monitor claim.

What the evidence does NOT carry: no claim that SAE features support
reliable safety monitoring (features fire on representative examples;
no exhaustive audit of activation coverage — the chapter-10 absorption
lesson); no claim that the 34M dictionary is complete (the 60%
London-boroughs number is the paper's own incompleteness admission);
no independent evaluation (manufacturer self-study, carried as a
caveat); no behavioral-intervention evidence (the features are found
and inspected, not steered with — Chapter 11's intervention leg is
what would upgrade them to mediator candidates).

## Assumptions

Tested in-article: interpretability of individual features at scale
(inspection); splitting (the scale ladder); incompleteness (the London
exercise).

Inherited: the SAE training objective's dictionary-as-features premise
(reconstruction with sparsity yields the model's features — a
hypothesis, Chapter 10's framing); inspection-based evaluation as
sufficient evidence for "interpretable" (the Jacovi–Goldberg
plausibility-vs-faithfulness problem — SRC-PAPER-034 — applies
directly); the site choice (features are extracted where the SAEs were
trained, not everywhere the model computes).

## Limitations

Authors' stated (fairly represented): self-evaluation by the
manufacturer; representative-example presentation rather than
exhaustive audits; the feature-completeness gap.

Ones I see that they do not foreground: dictionary-relativity means
cross-dictionary feature comparison is undefined (the 1M "San
Francisco" and the 34M "San Francisco #7" are not the same object in
any operational sense — indices are unstable across sizes, so any
downstream monitor keyed to feature indices inherits a version-
pinning burden the article does not discuss); absorption (a
sub-concept's activation carried by a neighbor) is the silent failure
mode of coverage claims — the 60% London number could understate
either incompleteness or absorption, and the article's method cannot
distinguish the two.

## Nearest alternatives

- **Towards Monosemanticity (SRC-PAPER-030)**: the one-layer
  foundation — same method family, toy scale, plus the dead-feature
  and density-bimodality self-diagnostics that the scaling article
  inherits; read together they bracket the scale question.
- **Probing and steering work (Chapter 11's canon)**: probes and
  interventions on raw activations — cheaper, no dictionary, but
  polysemantic by construction; SAEs trade training cost for
  (hypothesized) monosemanticity.
- **Circuit-level analysis (SRC-PAPER-025 / Chapter 09)**: finer-
  grained than features (QK/OV composition), far harder to scale —
  the two programs answer different questions about the same model.

## Replication feasibility

Not at course scale for the frontier claims: training 34M-feature SAEs
on a production model's activations is industrial compute. What IS
course-scale: the splitting phenomenon on a small open model (train
SAEs at 512/2k/8k features on a 1–2 layer model or a small open-weights
model's MLP activations; watch a coarse feature resolve into several);
the completeness probe (pick a closed concept class — e.g., the
warehouse environment's macro set — and measure dictionary coverage of
it); the absorption audit (find misses, inspect what fired instead —
the chapter-10 worked example's autopsy pattern). What breaks first at
small scale: interpretability itself becomes easier (toy features are
clean), so the *evaluation* difficulty — not the training — is what
the small-scale replication fails to reproduce.

## Falsifiable extension

Hypothesis: feature-splitting is concept-frequency-dependent — high-
frequency concepts split earlier (more sub-features at smaller
dictionaries) than low-frequency ones, so the 1M→4M splitting set is
predictable from corpus statistics. Design: at each dictionary size,
count sub-features for a preregistered concept list binned by corpus
frequency; test the monotonicity of split-count vs frequency rank.
Baseline: split-constant-across-frequency (splitting as pure dictionary
geometry). Metric: rank correlation with interval via bootstrap over
concepts. Stopping rule: three dictionary sizes; one model. What
counts against: if splitting is frequency-flat, my predictability
premise fails and splitting is a geometry phenomenon, not a usage
phenomenon.

## My interpretation vs. their claims

Their claims: (1) SAE features scale to a frontier model and remain
interpretable; (2) safety-relevant concepts appear as features; (3)
splitting occurs as dictionaries grow; (4) the dictionary is
incomplete even at 34M.

My interpretation: (1) is the article's strongest result and its
weakest-evidenced one simultaneously — "interpretable" is judged by
the authors' inspection, and the field still lacks the preregistered
external benchmark that would make it falsifiable; (2) should be read
as *existence of readouts*, never as monitoring capability — an
absorption-prone dictionary can show a beautiful deception feature and
still miss the attack family a deployer cares about (the chapter-10
selectivity discipline exists precisely for this gap); (3) is quietly
the most consequential result: dictionary-relativity breaks feature
identity across sizes, which makes "the X feature" an index-unstable
reference and imposes version-pinning on every downstream use; (4) the
60% London-boroughs number deserves more weight than its citation
graph gives it — it is a rare quantified incompleteness admission in a
field prone to completeness-by-vibes.
