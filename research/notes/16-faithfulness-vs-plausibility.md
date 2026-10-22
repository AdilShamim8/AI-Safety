# Note: Towards Faithfully Interpretable NLP Systems: How should we define and evaluate faithfulness? (2020)

Source: SRC-PAPER-034 · Access: abstract-read (a short, widely
mirrored position paper; the faithfulness-vs-plausibility distinction
confirmed from the abstract directly) · Read: 2026-10-21 · Note
level: **abstract-level, position-paper form** (no empirical results
to report — the note's evidence section prices the *distinction's*
consequences instead).

## The actual problem

The authors' framing: interpretability claims in NLP conflate two
different properties — does the explanation reflect the model's
actual reasoning (faithfulness), or is it convincing to a human
(plausibility)? The operational version: define the two precisely,
show that the field's evaluation practices measure the second while
claiming the first, and set the vocabulary the field should use.

## Method

(What the abstract carries:) the definitional split and its
evaluation consequence: human judgment measures plausibility — it
cannot measure faithfulness, because a human rater has no access to
the model's internal computation, only to the explanation's
persuasiveness. Faithfulness requires evidence from the model's
behavior under intervention — the explanation must predict what
happens when the model is perturbed in ways the explanation
describes.

This is a position paper — the method is the argument, and its
product is vocabulary that other papers' experiments then operational
ize (the chapter-10 discipline: faithfulness requires the
intervention leg; every dashboard is plausibility evidence by
definition).

## Central evidence

(No empirical results — the position-paper form is itself the
register's caveat.) The load-bearing moves:

- **Faithfulness**: the interpretation accurately reflects the
  mechanism that produced the behavior — checkable only against the
  model's actual computation (interventions, counterfactuals).
- **Plausibility**: the interpretation is convincing to a human
  judge — measurable with human studies, and *only* that.
- **The conflation trap**: a compelling attribution dashboard is
  plausible by construction; nothing about its compellingness is
  evidence about the model — human judgment is measuring the
  explanation's rhetoric, not its accuracy.

What the distinction does NOT carry (my discipline note, in the
paper's spirit): faithfulness is not binary either — it is graded by
what the explanation lets you predict about which perturbations
(the chapter-10 completeness/faithfulness quantities), and an
explanation can be faithful about one margin and silent about
another.

## Assumptions

The position's premises: that "the model's actual reasoning process"
is a well-defined thing an explanation can reflect (the mechanistic
stance — chapter 09's residual-stream program operationalizes it);
that human raters cannot access it (true by construction — they see
outputs); that the field's evaluation practices were dominated by
human-judgment protocols (the 2020 state of the interpretability
literature — saliency maps scored by rater agreement).

## Limitations

Authors' (position-paper form): no experiments to limit.
Mine: the faithfulness definition leans on "actual reasoning
process," which for superposed, distributed computation is not a
given — the interpretability program's later turns (features,
circuits, dictionary relativity) are the field negotiating what
"the mechanism" even is; and the plausibility side is not worthless
(it measures communication quality — an explanation no clinician
can read fails at its job) — the error is *substituting* it for
faithfulness, not measuring it.

## Nearest alternatives

- **Intervention-based interpretability evaluation** (activation
  patching, chapter 09; ablation-graded completeness, chapter 10):
  the operationalizations of faithfulness this paper's vocabulary
  licensed.
- **Debate and oversight protocols (chapter 05)**: the same trap in
  a different costume — a persuasive debater is plausibility
  evidence; the protocol's value comes from the parts that check
  claims against ground truth.
- **The saliency-map literature it critiqued**: the named offender —
  gradient attributions whose evaluations were rater-agreement
  studies.

## Replication feasibility

The distinction is a *methodological instrument*, not an experiment —
the course replicates it by use: every interpretability claim in
chapters 09–11 carries an intervention leg (patching, ablation,
steering-with-controls) because this paper established that without
it, the claim is plausibility. A learner "replicates" the paper by
taking a compelling attribution, perturbing the model as the
attribution implies, and watching the prediction fail or hold —
the chapter-10 worked example's exact shape.

## Falsifiable extension

Hypothesis: plausibility and faithfulness are empirically separable
in the expected direction — explanations tuned for rater
persuasiveness (styled, coherent, confident) show *no greater*
intervention-prediction accuracy than unstyled ones, while
intervention-derived explanations beat both. Design: one model and
behavior; three explanation families (rhetoric-enhanced, plain,
intervention-derived); measure (a) rater persuasiveness and (b)
accuracy at predicting perturbation outcomes. Baseline: plain.
Metric: two rates with intervals — the two-by-two is the result.
What counts against: if persuasiveness correlates with intervention
accuracy, the two properties are entangled in practice (not merely
conceptually distinct) and the paper's clean split is a
first-approximation — a genuinely interesting complication.

## My interpretation vs. their claims

Their claims: (1) faithfulness and plausibility are different
properties; (2) human judgment measures only plausibility; (3) the
field conflated them in evaluation practice.

My interpretation: (1)–(3) all hold and the paper earned its
canonical status — it is the single vocabulary fix that most
cleanly explains *why* the interpretability literature's evaluation
crisis existed; the under-credited corollary is that plausibility
evidence is not merely weak, it is *systematically misleading in
deployment* — the audience that most needs faithful explanations
(safety reviewers auditing a monitor) is exactly the audience most
susceptible to plausible ones, which is why the course puts the
intervention leg in the *curriculum's* completion criteria rather
than in a footnote.
