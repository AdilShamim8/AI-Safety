# Note: Trojan Detection in LLMs — the TDC2023 insights (2024)

Source: SRC-PAPER-144 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.
Companion card: [TrojAI (card 34)](../../datasets/cards/34-trojai.md).

## The actual problem

The [BadNets](13-badnets.md)-to-[TrojAI](../../datasets/cards/34-trojai.md)
line reaches LLMs: models vulnerable to trojan/backdoor attacks, and
a competition — the **Trojan Detection Competition 2023 (TDC2023)** —
organized around *identifying and evaluating* trojan attacks on
LLMs. The paper's insight agenda, from the abstract: the difficulty
of **distinguishing intended from unintended triggers** (a model
trains on all sorts of natural prompt-response regularities — which
of them count as a backdoor?), and **the feasibility of reverse
engineering troj[ans]** (truncation recorded; the reverse-
engineering program is the body's subject).

The course's framing: this is the artifact-security question at
LLM scale, inheriting [note 61](61-finetuning-compromises-safety.md)'s
derivative-artifact problem — when anyone can fine-tune and
redistribute, the receiver's question "does this artifact contain
an installed behavior?" needs an instrument, and the instrument's
hardness is *definitional* before it is technical: the
intended-vs-unintended-trigger line is a specification question
wearing a detection costume.

## What the abstract establishes

1. TDC2023's existence, focus (trojan identification and
   evaluation on LLMs), and this paper's insights-from-competition
   structure.
2. The trigger-distinguishing difficulty as a named challenge.
3. The reverse-engineering feasibility question as the program's
   second axis.

Unclaimed: competition results, winning approaches, detection
rates — body-level throughout.

## Why this note exists in the course

1. **Ch. 16's LLM-era supply-chain unit.** The chapter's
   third-party-artifact screening story now has its modern station:
   the program-scale [TrojAI](../../datasets/cards/34-trojai.md)
   → the LLM-scale TDC lineage, with this note as the connective
   citation.
2. **The specification reading of detection.** "Intended versus
   unintended triggers" is [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md)'s
   vocabulary in disguise: what the artifact is *supposed* to do is
   a specification claim someone must own, and detection inherits
   every ambiguity of that ownership. The course wires this as the
   note's deepest teaching — supply-chain security bottoms out in
   specification clarity.
3. **Ch. 12's adaptive logic, inherited.** A detector that finds
   known trigger shapes is a defense claim; adaptive adversaries
   design triggers outside the searched family — the
   [obfuscated-gradients](35-obfuscated-gradients.md) discipline
   applies to detectors with no changes.

## What this note does NOT claim

No detection-rate numbers; no claim that competition-winning
methods transfer to production screening; no claim about the
competition's scale (body-level).

## The falsifiable extension (deterministic tier)

P06's organism can host a mini-TDC:

- Plant N trojans of varying subtlety (from a single-vocabulary
  trigger to a distributed three-token conjunction); hand the
  detector-analogue (probe + activation-clustering style
  instruments at deterministic tier) the artifact and ask which
  trojans it flags, with the intended-behavior specification
  written down first.
- Prediction worth testing: detection rate decays with trigger
  subtlety, and — the intended/unintended lesson — the detector
  also flags *natural* regularities at a nonzero rate: the
  false-positive side of the specification ambiguity, tabulated.
- Falsifier: uniform detection across subtlety would bound the
  instrument at this tier — recorded, with the false-positive
  rate reported beside it, the paired ledger as always.
