# Note: Stealing Machine Learning Models via Prediction APIs (2016)

Source: SRC-PAPER-043 · Access: abstract-read · Read: 2026-10-22 ·
Note level: **abstract-level**.

## The actual problem

The authors' framing: ML-as-a-service APIs sell predictions — but
predictions leak the model. The operational version: extraction
attacks that recover the target model (or an equivalent) through
query access alone, across model classes, against real services.

## Method

(What the abstract carries:) extraction attacks against prediction
APIs spanning logistic regression, neural networks, and decision
trees — two families: equation-solving (recover parameters
analytically from crafted queries) and model-reconstruction (train a
student on the transcript of query-answer pairs). Demonstrated
against BigML and Amazon Machine Learning's live services.

The design logic: invert supervised learning — the attacker chooses
the inputs (queries) and receives the labels (API outputs), so the
API *is* a labeled-data oracle for the model itself. Confidentiality
of the model is then a property of the *query budget and output
channel*, not of the model's quality.

## Central evidence

- **Near-perfect fidelity extraction** across the three model classes
  — the headline, quoted at the abstract's own qualifier.
- **Confidence-free APIs remain attackable** — decision-only outputs
  still leak enough for extraction (the register's supports entry
  carries this as the surprising case): withholding scores raises
  cost, not immunity.
- Real-service demonstrations: BigML and Amazon Machine Learning —
  the 2016 commercial deployments, named.

What the evidence does NOT carry: per-model query counts and the
fidelity-vs-queries curves live in the unread body; nothing about
modern LLM APIs (extraction of a 2026 frontier model is a different
cost structure — the *principle* transfers, the price does not);
nothing about defenses (rate limits, output rounding, query
anomaly detection are the response literature).

## Assumptions

Tested in-paper: extraction feasibility across model classes and
against deployed services; the decision-only case.

Inherited: that the attacker can afford the query volume (the
cost model is the deployment's rate limits and pricing — a defense
variable the paper treats as the attack's budget, correctly);
that an "equivalent" student satisfies the attacker (near-perfect
fidelity on the *query distribution* may leave tails unextracted —
the attacker's distribution choice is part of the attack).

## Limitations

Authors' (abstract-level): none stated beyond scope.
Mine: near-perfect fidelity is measured on the attacker's query
distribution — a deployer's rare, high-value inputs may survive in
the unqueried tail, and no one has priced that tail; the 2016 model
classes (shallow models, decision trees) leak structurally more than
deep nets with softmax temperature — the *ranking* of extractability
across architectures is not established by three classes.

## Nearest alternatives

- **Membership inference (SRC-PAPER-041)**: the privacy sibling —
  the API leaks *about the training set* rather than the model; same
  query surface, different secret.
- **Model inversion literature**: the third sibling — reconstructing
  training *inputs* from outputs; the three together define the
  leak surface of prediction APIs.
- **Rate limiting / output perturbation defenses**: the response
  family — the honest framing (chapter 12 §3.4) is that every
  defense here is a *fidelity-vs-queries curve* claim that deserves
  the audit arithmetic.

## Replication feasibility

High at course scale — this is P02-adjacent territory: a small
model served behind a toy API, an extraction attack implemented as
a student-training loop on the transcript, and the fidelity-vs-
queries curve measured with intervals. What breaks first: the
equation-solving family needs analytic model classes (logistic
regression is the honest course-scale target); deep-model
extraction at scale is compute-tier.

## Falsifiable extension

Hypothesis: extraction fidelity is output-channel-dependent in a
quantifiable exchange — decision-only APIs require a
super-linear query multiplier for the same fidelity as score APIs,
and the multiplier grows with class count. Design: serve one model
under three output regimes (scores / top-k / decision-only); run
student extraction at matched query budgets; measure fidelity on a
held-out probe set (with the tail explicitly sampled). Baseline:
the scores channel. Metric: fidelity with Wilson intervals at three
budgets. What counts against: if decision-only extraction reaches
comparable fidelity at linear cost, the output-channel defense
buys far less than the multiplier premise claims — and the
deployer's "we withhold scores" comfort is even weaker than the
paper's already-weak result suggests.

## My interpretation vs. their claims

Their claims: (1) prediction APIs leak their models with
near-perfect fidelity; (2) across model classes and real services;
(3) including confidence-free APIs.

My interpretation: (1) is the founding statement of a principle the
industry keeps relearning — *serving a model is publishing it* — and
every subsequent API hardening (rate limits, rounding, query
monitoring) is a renegotiation of the publication price, not a
revocation; (2) the 2016 demonstrations matter as evidence the
attack was live against commercial practice, not as a statement
about modern architectures; (3) the decision-only result is the
paper's most decision-relevant finding — it kills the "we don't
return scores" defense in principle, leaving only cost arguments,
and cost arguments belong to the fidelity-vs-queries audit the
course's arithmetic exists to price.
