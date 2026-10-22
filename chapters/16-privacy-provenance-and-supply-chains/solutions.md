# Chapter 16 — Solutions and assessor rubrics

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module); the sample-size arithmetic is shown in
full.

---

## Exercise 16.1 — audit the MedBrief-7B chain

### (a) The license lineage table and the fuse

| Artifact | Upstream | License/constraint | Inherited constraint on MedBrief-7B |
|---|---|---|---|
| Base model | unstated provenance | unknown (no model card, no hash) | **unverifiable — the chain starts with a gap** |
| Hospital data | licensed | deployment-permitted | none beyond attribution |
| Scraped clinical forums | web crawl | no established basis for weights redistribution | contested link — risk flagged |
| Purchased dataset | vendor | **no redistribution of derived weights** | **the fuse: shipping MedBrief-7B is the breach** |
| MedBrief-7B (product) | all of the above | — | most-restrictive-wins: not distributable |

The fuse is the purchased dataset's term: the *training* may or may
not be permitted, but the *distribution of derived weights* — the
entire product plan — violates the most restrictive link. A lineage
table drawn before training would have caught this at contract time;
drawn now, it converts a legal event into a decision.

### (b) What "deduplicated, no leakage found" does not cover

1. **Single-exposure memorization.** Dedup only attacks the
   duplication law; the foundational extraction work recovered
   verbatim PII, code, and UUIDs that appeared in *one document*
   [SRC-PAPER-062] — dedup cannot touch what was never duplicated.
2. **Capacity-driven memorization.** The same work found larger
   models more vulnerable, and the quantification work states the
   capacity law and the more-prevalent-than-believed conclusion
   [SRC-PAPER-063] — a 7B model's memorization is a function of its
   size, not of the team's diligence.
3. **Membership inference.** "No leakage" implicitly means no
   *content* leakage; participation disclosure is a separate channel
   (Ch. 12) that dedup does not address and that their statement
   shows no battery for. A statement without a canary ledger and an
   MI battery is a description of the team's confidence, not of the
   model.

### (c) The canary audit they should have run

- **Arms:** synthetic canaries at duplication {1, 10}, ≥50 per arm
  per corpus, inserted before dedup so the dedup effect is measured
  on the same canaries.
- **Battery:** ≥200,000 generations (the founding work's scale of
  manual search is the cautionary tale — the audit needs the
  generation budget stated, and the GitHub companion's warning that
  smaller batteries find less is the reason).
- **Paired comparison:** duplication-10 canaries before vs after
  dedup on the *same* plants — the paired design that Aurora's
  9/10 → 1/10 (p = 0.0107) exemplifies.
- **Release rule (pre-declared):** release proceeds only if the
  *upper* Wilson bound of the duplication-1 exposure arm is below
  the clinical-privacy threshold — the upper bound, not the point
  estimate, because a release decision must survive the unlucky
  audit, not the lucky one.

### (d) The two-sentence response on ε = 8

> "ε = 8 is a legitimate budget if it is stated on the artifact,
> composed across the fine-tune chain, and priced against the
> utility ledger — DP's contract is the numbers, not the acronym
> [SRC-PAPER-064]. What is not legitimate is treating 4 vs 8 as a
> quality knob while the memo says 'DP-trained' with no budget,
> no accounting method, and no utility cost — that sentence is a
> marketing adjective wearing a theorem's clothes."

Assessor rubric: full credit requires the fuse named as
*distribution* (not training) with the most-restrictive-wins logic;
the three coverage gaps each tied to the right source; the audit
design with paired arms, stated budget, and an upper-bound release
rule; and the ε response separating budget-choice legitimacy from
budget-statement dishonesty. Deduct for any "run more epochs of
dedup" style non-response.

---

## Exercise 16.2 — pricing the Aurora numbers

### (a) Four intervals and the paired sign test

Recomputed with the course's Wilson implementation (z = 1.95996):

| Quantity | Rate | Wilson 95% |
|---|---|---|
| Canaries, duplication 1 (post-dedup) | 12/50 = 24.0% | [14.3%, 37.4%] |
| Canaries, duplication 10, before dedup | 9/10 = 90.0% | [59.6%, 98.2%] |
| Canaries, duplication 10, after dedup | 1/10 = 10.0% | [1.8%, 40.4%] |
| Membership inference calls | 19/200 = 9.5% | [6.2%, 14.4%] |

Paired dedup comparison on the same 10 duplication-10 canaries:
9 exposed before, 1 after. The paired ledger: both-exposed = 1 (the
surviving canary was exposed before too), before-only = 8,
after-only = 0, neither = 1 → 8 discordant pairs, all improvements
→ exact one-sided sign test p = P(>=8 of 8) = (1/2)^8 = 0.0039.
The paired form is the correct one (an unpaired 9-of-10 comparison
would give 0.0107 while ignoring the pairing the audit designed in);
the rule the ledger enforces: **count discordant pairs, and show the
ledger, not just the tail probability.**

### (b) What 12/50 supports, and the n for ±5 points

"Consistent with industry norms" is unfalsifiable at this width:
12/50 supports any true rate in [14.3%, 37.4%] — a 23-point range
cannot be *inconsistent* with any norm in it. For a ±5-point Wilson
half-width at 95% around an observed 24%: solving
1.96·√(p(1−p)/n) ≈ 0.05 at p ≈ 0.24 gives
n ≈ (1.96² · 0.24 · 0.76)/0.05² ≈ **140**, and with the Wilson
centering correction **n ≈ 150** canaries per arm suffices (at
p = 0.24, half-width 5.0%). The audit's canary budget should be
sized to the decision it gates.

### (c) Pricing "0/60 leaks"

0/60 → Wilson 95% [0%, 6.0%]. The honest sentence: "no canary was
extracted in 60 attempts, bounding the *canary-scale* exposure rate
below 6.0% at 95% — this is evidence about planted secrets at the
tested duplication arms, not a bound on memorization of real
training data, whose rate the founding work measured directly and
found material at single-document exposure [SRC-PAPER-062]." The
non-claim clause is load-bearing: zero successes on 60 trials is a
bound, never an absence proof, and the canary scale is not the
production scale.

### (d) Why "weak MI" is the wrong summary for sensitive subsets

A 9.5% true-positive rate at a given false-positive rate is "weak"
when the base rate is high and the harm is diffuse. For a small
sensitive subset — patients under fraud investigation — the audit's
question inverts: how many non-members must be examined before one
member is identified at that advantage, and does the resulting
precision make membership *actionable*? At 9.5% TPR with even a 1%
FPR, members of a 1-in-500 subset are identified at roughly
9.5:1·(500/100)... — the arithmetic depends on the score
threshold, which is exactly what the audit must add: a
risk-conditional MI battery (thresholds swept, precision at the
operating point, Wilson intervals on both rates, subset-conditioned)
before "weak" is allowed into the memo. The rate that matters for a
small class is the *identification precision at a chosen threshold*,
not the marginal AUC.

Assessor rubric: full credit requires all four intervals correct;
the paired-vs-marginal correction in (a) shown or acknowledged;
the n ≈ 140–150 sizing with the formula visible; the 0/60 bound
priced with its canary-scale non-claim; and the subset-conditional
MI argument with threshold-sweep and precision framing. Deduct for
treating any interval overlap or zero-count as "no effect / no
leak."
