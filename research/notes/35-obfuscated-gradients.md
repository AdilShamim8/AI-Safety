# Note: Obfuscated Gradients — why most advertised defenses were not defenses (2018)

Source: SRC-PAPER-110 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

By 2018, the adversarial-example literature had a defense-paper genre:
claim robustness, show that gradient-based attacks now fail. This paper's
contribution — the load-bearing one for Ch. 12 — is the diagnosis that
*attacks failing is not attacks being stopped*. Defenses were breaking the
*optimization signal* (the gradient), not the vulnerability: **obfuscated
gradients**, a form of gradient masking. An attack that relies on
gradients sees a masked gradient, stalls, and the defense reports a high
attack failure rate that measures the attack's blindness, not the model's
robustness.

The abstract's case study is the number the course pins: at ICLR 2018,
**7 of 9** non-certified white-box-secure defenses exhibited obfuscated
gradients, and the authors' adapted attacks circumvented **6 completely
and 1 partially, in each paper's original threat model**. That ratio —
roughly four out of five published defenses falling to the evaluation
that should have been run before publication — is why Ch. 12's
adaptive-evaluation discipline (section 3.6) exists, and why the repo's
comparison-05 note (static benchmarks vs adaptive evaluation) treats
"attack didn't work" as a hypothesis, not a result.

## The three-type taxonomy (as the abstract prices it)

The paper names **three types** of obfuscated gradients and pairs each
with an attack technique that overcomes it. The abstract does not list
the three types' names (shattered, stochastic, exploding/vanishing —
those live in the body); what it establishes is the *taxonomy-then-
countermeasure* structure: each masking mechanism has a signature and a
circumvention. That structure is the course's repeated answer to defense
claims: classify the mechanism, then attack *the mechanism*, not the
endpoint. Note 07 (Croce & Hein's reliable evaluation) extends exactly
this line; GCG (note 31) is the same discipline on the language side.

Characteristic behaviors of masked-gradient defenses are also promised
("we describe characteristic behaviors") — at abstract level the note
records that they exist and that the body enumerates them; Ch. 12's
red-flag list (one attack succeeds while others fail; attacks do
*worse* than random at some budgets) is the course's rendering of that
promise, sourced through the later evaluation literature it cites.

## Why this note exists in the course

Chapter 12's central claim — *a defense means something only after it
survives adaptive evaluation in its own threat model* — descends from
this paper more directly than from any other single source. The ICLR
2018 case study is also the course's canonical example of **publication
bias in defense evaluation**: the defenses were peer-reviewed, the
evaluation was the field's standard practice, and the practice was
measuring the wrong thing. That is the same institutional failure Ch. 02
documents for benchmarks generally (comparison-05) and Ch. 22 rediscovers
for safety cases; the note ties the three together.

The through-line to deployment: an operator reading a defense paper's
headline number ("99% attack failure") is reading a masked-gradient
artifact unless the evaluation adapted. The course's threat-model
comparison artifact (Ch. 12's core deliverable) forces the question the
paper forces: *what exactly did the attack optimize against, and what
would its failure mean?*

## What this note does NOT claim

No claim that obfuscated gradients explain all defense failures
(the body's own scope is the 2018 white-box crop); no claim that the
three attack techniques transfer unmodified to modern LLM defenses; no
numbers beyond the 7/9 and 6+1 counts the abstract states. Certified
defenses (the parallel track the paper's "non-certified" qualifier
implies) get their own treatment in Ch. 12's reading list, not here.

## The falsifiable extension (deterministic tier)

The diagnosis has a testable signature in the repo's own projects:

- P02's optimizer can be run in a masked-gradient configuration
  (e.g., a quantized/noisy objective) and a clean configuration; the
  prediction from this note: the masked configuration's *reported*
  attack failure rate rises while its true vulnerability (found by
  random search or by attack on the clean path) is unchanged — a
  synthetic obfuscated-gradient demonstration.
- Falsifier: if the masked objective's random-search vulnerability also
  drops proportionally, the masking is real robustness, not obfuscation
  — the discrimination the paper's characteristic behaviors support.
- This is a fixture-tier experiment (deterministic, stdlib-only, a day),
  and it gives Ch. 12's exercise set a runnable version of the case
  study's method: evaluate a defense with both the attack it fails and
  the attack it was never evaluated against.
