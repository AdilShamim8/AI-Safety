# Note: Jailbroken — the two failure modes behind every jailbreak family (2023)

Source: SRC-PAPER-119 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

After a year of jailbreak-of-the-week blog posts, this paper did the
taxonomy work the field needed: stop cataloging prompts, start
explaining *the mechanism class*. The abstract's hypothesis pair — the
two failure modes of safety training:

1. **Competing objectives** — the model's capabilities and its safety
   goals conflict, and an attacker locates a context where the
   capability side wins (helpfulness, instruction-following, role
   play, formatting compliance).
2. **Mismatched generalization** — safety training failed to generalize
   to a domain where *capabilities* did generalize. The model can
   operate in the domain; the refusal behavior did not follow it there
   (encodings, low-resource languages, unusual modalities of the same
   request).

The paper then runs the loop that makes it more than a taxonomy: use
the two modes to *guide jailbreak design*, then evaluate GPT-4 and
Claude v1.3 against existing and newly designed attacks — and the
abstract's verdict is the sentence the course pins: **vulnerabilities
persist despite the extensive red-teami[ng]** (the API record truncates
there; the persistence claim stands, its magnitudes stay unclaimed).

## Why the taxonomy is the course's load-bearing import

Ch. 13 (LLM application security) organizes its defense sections by
attack surface; this paper supplies the *root cause* axis that makes
the organization diagnostic rather than encyclopedic:

- A competing-objectives jailbreak is patched by *priority structure*
  (instruction hierarchy — note 09; authorization boundaries — CaMeL,
  note 21) because the failure is in which objective wins.
- A mismatched-generalization jailbreak is patched by *coverage*
  (train or gate across domains; spotlighting-style canonicalization —
  note 08) because the failure is in where refusal generalizes.
- Optimized attacks (GCG, note 31; many-shot, note 45) are the
  adversarial search *over both failure modes* — which is why "we
  patched that jailbreak" is a category error the moment the search is
  adaptive (the Ch. 12 discipline, re-landing in Ch. 13).

The taxonomy also explains why red-teaming alone cannot close the
surface: each red-team find is one instance of one mode; the mode
generates unbounded instances. That is the paper's quiet contribution
to Ch. 15's adaptive-evaluation teaching: enumeration is not
elimination.

## What the abstract establishes

1. The two failure modes, defined and distinguished (quoted above).
2. The design-guided methodology: modes → new attacks → evaluation
   against GPT-4 and Claude v1.3.
3. Persistence of vulnerabilities despite extensive red-teaming
   (magnitude claims truncated — honestly priced).
4. The framing that attacks *succeed via* these modes rather than via
   some unbounded "model is broken" — the safety training is real and
   the bypasses are structured.

Body-level, unclaimed: the specific designed attacks, per-model attack
success rates, and the paper's recommendations section. The note claims
the taxonomy and the persistence verdict; it does not put numbers on
any model.

## Why this note exists in the course

Ch. 13's readings needed the mechanism paper that unifies: prompt-level
jailbreaks (the genre this paper explains), GCG's optimized suffixes
(note 31 — the search over the same failure surface), and the
instruction-hierarchy defense line (notes 09, 21). It also anchors
Ch. 15's red-team methodology: mode-guided attack design is what
separates *systematic* red-teaming from prompt graffiti — the
difference the chapter's preregistration discipline enforces.

The deployment consequence (Ch. 22): a release gate that tests only
*known* jailbreaks is testing instances, not modes. The assurance
question the safety-case template asks becomes: "what evidence bounds
*mismatched generalization* for our deployment domains?" — a coverage
question, answerable only by the gate's domain slice actually matching
the deployment domain slice (the Ch. 17 position-dependence lesson,
applied to refusal coverage).

## What this note does NOT claim

No claim that the two modes are exhaustive (later literature adds
others — e.g., fine-tuning-removed-refusal results, kept under note 12's
family); no per-model numbers; no claim that 2025 frontier models carry
the same vulnerabilities at the same rates (scale-drift honesty — the
note establishes the *analytic frame*, which survives model turnover
better than any attack list).

## The falsifiable extension (deterministic tier)

P07's agent_guard already separates objective conflict from coverage
gaps structurally (R-rules vs declared-capability coverage):

- Extend its attack set with two families designed by the paper's
  modes: (a) competing-objectives cases where a benign-declared tool
  call carries the harmful payload under a helpful framing; (b)
  mismatched-generalization cases where the same request recurs in an
  unanticipated encoding (nested JSON, indirect reference via the
  memory store).
- Prediction worth testing: R1–R4 capability rules catch (a)-family at
  the consent gates (they police which objective wins) while
  (b)-family leaks through as the honest residual — reproducing the
  paper's two-mode structure at deterministic tier, with the residual
  *classified by mode* instead of just counted.
- Falsifier: symmetric catch rates across both families would show
  this guard's failure surface does not decompose by the paper's modes
  — a genuine negative result for the note's transfer claim.
