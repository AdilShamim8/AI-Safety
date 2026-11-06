# Take-home: the harness build — the P01 format

**Navigate:** [← take-homes](README.md) · [coding bank](../questions/coding.md)

**The prompt as issued.** "Build an evaluation harness for a small
classifier. Report results in a way we can audit." Deliberately
under-specified — the take-home is testing what you choose to
report, not just whether the code runs.

**The mapping.** [P01](../../projects/p01-evaluation-harness/README.md)
is this exact assignment; the [example
report](../../projects/p01-evaluation-harness/example-report.md) is
the house format: cases, baselines, paired ledgers, Wilson
intervals, and the residual section.

**The rubric (what graders look for).**
1. **Baselines named.** A harness without a baseline row is a demo.
2. **Paired comparisons.** Same cases through every system — the
   ledger discipline; unpaired numbers are the most common rejection.
3. **Intervals, not points.** A mean without an interval is exactly
   what the [theory bank](../questions/theory.md) trains you to
   refuse.
4. **Determinism stated.** Fixed seeds, fixed versions, rerunnable
   by the grader — the corpus's offline/stdlib-first rule is the
   portable version of this.

**The honest tiers expected.** State what the harness does not
cover: case families not generated, models not compared, and the
compute the next tier would need. A submission with a not-covered
list reads as senior; one without reads as unaware.
