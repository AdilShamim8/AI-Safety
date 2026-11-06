# Take-home: the audit format — the P04/P09 format

**Navigate:** [← take-homes](README.md) · [evaluator role](../roles/evaluator.md)

**The prompt as issued.** "Audit this dataset (or this model's
reliability). Tell us what the aggregate numbers hide."

**The mapping.** [P04](../../projects/p04-preference-optimization-audit/README.md)
for the dataset side (preference data: what the labels actually
encode); [P09](../../projects/p09-shift-subgroup-reliability/README.md)
for the reliability side — the project that exists because averages
lie: the same aggregate, decomposed, with the subgroup gap exposed.

**The rubric.**
1. **Decomposition before judgment.** Slice first (subgroups, shift
   cohorts, label sources); an audit that only re-computes the
   aggregate is a re-print.
2. **Both ledgers paired.** Before/after or system/reference on the
   same slices; the interval on every gap.
3. **Findings ranked.** What matters most, second, third — auditors
   who present an unordered list have not audited, only collected.
4. **The falsifier.** What evidence would overturn each finding —
   preregistration language in audit clothes.

**The honest tiers expected.** Slices not reachable with the given
data, named as such; the recommendation section carrying
uncertainty instead of false precision. The [governance
bank](../questions/governance.md)'s "conformance is not evidence"
lesson lands hardest in this format.
