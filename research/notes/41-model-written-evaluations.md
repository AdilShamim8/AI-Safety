# Note: Model-Written Evaluations — when the instrument is made of the thing it measures (2022)

Source: SRC-PAPER-116 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Evaluating scaled LLMs needs eval data faster than crowdwork can make it
and broader than existing benchmarks reach. This paper's proposal:
**generate the evaluations with LMs themselves** — from yes/no questions
to multi-stage generated-and-filtered Winogender schemas. The abstract's
validation evidence: crowdworkers rate the generated examples as highly
relevant and **agree with 90–100% of the labels**, "sometimes more so
than corresponding human-written datasets." The yield: **154 generated
datasets**, and new cases of **inverse scaling** — models getting
*worse* with size on some of them (the thread note 48 picks up as its
own paper).

For Ch. 02 this is a genuine methodological gift: cheap, broad,
coverage-adaptive evaluations. For the course's measurement discipline,
it is also the cleanest available instance of a deeper problem: **the
measuring instrument is manufactured by the system class it measures.**
A model-written eval inherits the generator's blind spots as *design*
— the questions it never thinks to ask are structurally absent, and no
crowdworker agreement number can detect an absence. The 90–100%
agreement figure measures *label quality given the example exists*;
it cannot measure *what the example space omitted*. That asymmetry —
validated on the inside, blind on the outside — is the note's reason
for existing, and it is exactly Ch. 02's construct-validity caveat
materialized.

## What the abstract establishes

1. The generation pipeline family (varying human effort, LM effort
   scaling with complexity) and its validation at 90–100% crowdworker
   label agreement.
2. The 154-dataset yield and new inverse-scaling cases — the empirical
   payload.
3. The abstract's own honest tail: "larger LMs repeat back…" —
   truncated in the API record at the very sentence where the paper
   names its own artifact concern (larger generators repeating dominant
   training patterns). The note records the truncation and claims
   nothing from the cut-off clause beyond the existence of a
   pattern-repetition finding the body reports.

## Why this note exists in the course

Chapter 02 (evaluation science) teaches that an eval is a claim about
what it measures, and its readings section now carries this paper as the
**instrument-provenance** citation. Three course threads descend from
it:

1. **Eval supply at scale.** Dynamic and generated evaluations are now
   the field's default for novel behaviors (AgentDojo, note 22, is a
   later instance); the learner needs the founding source and its
   honest limits together, which is what pairing this note with
   comparison-05 (static vs adaptive) does.
2. **Circularity risk.** When the eval generator and the eval subject
   share training data and priors, "passes the eval" drifts toward
   "agrees with its own generator" — the model-written-evals version of
   Ch. 02's contamination problem, and the reason P01's harness uses
   case sets with pinned provenance rather than generated-on-the-fly
   items.
3. **Inverse-scaling discovery as evidence of surprising scale
   behavior.** The note hands note 48 its founding observation: some
   measured abilities *anti-improve* with scale — which is load-bearing
   for any "scale will fix it" safety argument (Ch. 17's drift
   discussions and the glossary's scale-drift honesty).

## What this note does NOT claim

No claim that model-written evals are *invalid* — the paper's agreement
numbers are real and the method is now field-standard for breadth; the
note's caution is about *blind-spot inheritance*, which is a coverage
property the agreement metric cannot see. No claim about the specific
inverse-scaling datasets (body-level); no claim about label-agreement
comparisons beyond the abstract's stated range.

## The falsifiable extension (deterministic tier)

Blind-spot inheritance has a synthetic test:

- Generate a case set with generator A (a family of synthetic templates
  with known coverage: N distinct violation classes), then measure what
  a second generator B, *trained on A's output*, produces when asked to
  extend the eval: does B's case distribution cover the N classes
  uniformly, or does it concentrate on A's most frequent classes?
- Prediction worth testing: B's coverage concentrates (frequency
  inheritance), and B's *self-agreement* stays high even as coverage
  narrows — the instrument quality metric stays flat while the
  instrument's blind spot grows.
- Falsifier: uniform coverage under inheritance would show this
  synthetic world lacks the effect — bounding the note's caution and
  recording where the circularity question must instead be answered at
  model tier (honestly marked not-executed).
- Instrument: P01's case-set machinery already supports class-pinned
  generation; the extension is a coverage-vs-agreement paired ledger,
  which is the report format Ch. 02 drills.
