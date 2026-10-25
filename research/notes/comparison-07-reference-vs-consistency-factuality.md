# Comparison 07 — reference-anchored vs consistency-based factuality checking

**The practitioner's question:** my product generates long-form claims;
what instrument do I build to catch falsehoods — a reference check or
a consistency check?

**The two sides, at their sources:** [FActScore
(note 46)](../notes/46-factscore.md) decomposes generations into
atomic facts and scores each against **a named knowledge source** —
external, inspectable, agreement-priced. [SelfCheckGPT
(note 47)](../notes/47-selfcheckgpt.md) samples the same prompt
repeatedly and measures **consistency across samples** — internal,
zero-resource, stability-priced. Both are abstract-read level here;
the comparison is at the same honesty tier as its inputs.

| | Reference-anchored (FActScore-style) | Consistency-based (SelfCheck-style) |
|---|---|---|
| Signal source | an external corpus you name and can audit | the model's own output distribution |
| Catches | claims that contradict the reference | claims that vary across samples (invented content) |
| Misses | claims the reference is wrong or silent about | claims the model is *consistently* wrong about |
| Access needed | database + retrieval plumbing | sampling only (works at API tier) |
| Cost shape | per-claim lookups; decomposition-dependent | N× generation per audited response |
| Failure signature | granularity gaming; stale references | confident consensus errors (popular misconceptions pass) |
| Course project | P03's selective-prediction input (per-item support) | P03's sampling-consistency extension (note 47's falsifiable tier) |

## 1. What each instrument actually measures

Neither measures truth. The reference instrument measures
**agreement with a corpus at atomic granularity** — the corpus's
coverage and errors are inherited (the instrument-circularity
caution, now on the *reference* side). The consistency instrument
measures **stability of the output distribution** — training-prior
confident errors are invisible to it by construction. A deployment
that quotes "factuality score" without naming which of these two
constructs it measured has committed construct laundering
([Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md)'s
term, applied verbatim).

## 2. Why the failure sets are complementary, not overlapping

The interesting cases are the ones where exactly one instrument
fires. The **consistent falsehood** (the model's prior encodes a
popular misconception — incident 04's "geologists recommend eating
rocks" is adjacent: popular *and* wrong) sails through consistency
checking at full stability while a good reference flags it. The
**grounded-but-variable** claim (a legitimately multi-answerable
question) flags under consistency while a good reference passes it.
The two instruments' false-positive and false-negative sets are
nearly disjoint — which is the argument for running both when the
domain justifies the cost, and for knowing which one you skipped.

## 3. The deployment decision tree

1. **Is there a trustworthy, current, machine-readable reference for
   the domain?** If yes (regulatory text, product catalog, internal
   policy), reference-anchored wins — and the Air Canada
   ([incident 01](../notes/incidents/01-air-canada-chatbot-liability.md))
   and Cursor ([incident 06](../notes/incidents/06-cursor-invented-policy.md))
   lessons say: route the *policy* questions there and never let the
   prior answer them. If no (open-domain prose), the reference
   instrument has no leg to stand on — consistency is the floor.
2. **What is the sampling budget?** Consistency costs N× generation
   per audited response ([Ch.22](../../chapters/22-safety-engineering-and-assurance/README.md)'s
   monitor-price-tag discipline): the N is a governance decision,
   not an implementation detail.
3. **What happens on a flag?** Both instruments feed P03-style
   abstention policies — the flag is an input to a threshold, not an
   action. The paired ledger applies: selective risk *and*
   false-abstention rate, or the audit is half an audit.

## 4. The falsifiable resolution (deterministic tier)

The complementarity claim is testable on P03's organism: construct
three item classes — stable-grounded, unstable-invented, and
**consistent-falsehood** (fixed wrong answer across samples) — run
both instruments, and tabulate the 2×2. Prediction: the third class
shows the full asymmetry (consistency silent, reference-flagging
loud, given a reference that disagrees). Falsifier: if consistency
flags the third class, the synthetic world contradicts the
decomposition — a boundary result worth recording either way, per
the research-method standing instruments.

## 5. Bottom line

The instruments are complements with disjoint blind spots, and the
choice between them is a *domain* decision (does a reference exist?)
before it is a *budget* decision (what does sampling cost?). Quote
the construct you measured, name the reference or the sampling
budget, and the result is auditable; do neither and it is marketing.
