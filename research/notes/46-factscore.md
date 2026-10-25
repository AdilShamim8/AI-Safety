# Note: FActScore — decomposing factuality into countable atomic facts (2023)

Source: SRC-PAPER-121 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

"Is this generation factual?" is a badly-formed question — the abstract's
own diagnosis: long-form generations contain **a mixture of supported
and unsupported information**, so binary judgments are inadequate, and
human evaluation of the mixture is too slow to scale. FActScore's move:
decompose the generation into **atomic facts** and report **the
percentage supported by a reliable knowledge source**. Factuality
becomes a rate over decomposed units — countable, per-claim auditable,
and (the evaluation-science point Ch. 02 drills) a *measurement with an
error model* rather than a vibe.

The design choice that carries the most teaching weight: the score
presupposes a **reference corpus** deemed reliable. FActScore does not
measure truth; it measures *agreement with a named source at atomic
granularity*. That is a feature (the source is inspectable, the
disagreements are listed) and a limitation (the score inherits the
source's coverage and errors — the same instrument-provenance caveat
as note 41, now on the *reference* side instead of the *generator*
side). The course keeps both halves visible.

## What the abstract establishes

1. The decomposition design: atomic facts + percentage supported by a
   named knowledge source.
2. The extensive human evaluation of **people-biography generations**
   across InstructGPT, ChatGPT, and retrieval-augmented PerplexityAI.
3. New analysis demonstrating the need for fine-grained scoring — the
   abstract's cut-off example begins "ChatGPT onl[y]…" (the API record
   truncates; the note records the truncation honestly and claims only
   the demonstrated-need finding, not the specific number).

Body-level, unclaimed: the actual FActScores per model, the
atomic-decomposition protocol's inter-annotator numbers, the
retrieval-source details, and the error analysis of the decomposition
itself (atomic facts can be ambiguous — the body discusses; the note
flags it as a known limitation class without claiming its magnitude).

## Why this note exists in the course

Chapter 06 (honesty, uncertainty, selective prediction) needs
factuality *measurement* to pair with its hallucination *detection*
(note 47) and its calibration instruments (P03). FActScore is the
measurement half's canonical citation:

1. **The evaluation-unit discipline.** Ch. 02 teaches: a metric is a
   claim about what counts as one success and one failure. FActScore
   makes that concrete — the atomic fact is the unit, and the
   decomposition rule *is* part of the metric. Change the
   decomposition, change the score: the same construct-validity
   lesson the chapter's preregistration rule exists for.
2. **The selective-prediction bridge.** A per-fact support rate is
   exactly the input an abstention policy needs (P03's threshold
   policies consume per-item risk): "generate only when expected
   support clears a threshold" is FActScore logic turned into a
   deployable gate — the note is the citation for that design line.
3. **Long-form honesty in production.** Ch. 22's release-gate
   discussions for generation features (bios, summaries, reports) list
   atomic-support sampling as the audit instrument; the note anchors
   it. The incident record (Air Canada's chatbot inventing policy;
   Google AI Overviews) is the failure mode this instrument would have
   priced — incident 04's review makes that connection explicitly.

## What this note does NOT claim

No per-model scores (truncated abstract); no claim that FActScore is
unbiased (the body's own error analysis is unread); no claim about
which knowledge source is "reliable" — that is a deployment decision
the course treats as an explicit, recorded choice (the register's
evidence-ladder discipline applied to references).

## The falsifiable extension (deterministic tier)

P03's calibration machinery supports an atomic-support analogue:

- Build a synthetic biography-style case set where each generation
  decomposes into atomic claims with *known* support labels against a
  pinned reference table (deterministic by construction). Compute the
  FActScore-analogue; then perturb the decomposition granularity
  (fine vs coarse atomization) and recompute.
- Prediction worth testing: the score moves with decomposition
  granularity *at fixed generation quality* — quantifying the
   construct-sensitivity the note warns about, which is exactly the
   number a preregistration should pin before anyone reports a
   factuality delta between two systems.
- Falsifier: granularity-invariance would show this synthetic metric
  robust to its main reported weakness — also worth recording, since
  it would license coarser (cheaper) audits at this tier.
