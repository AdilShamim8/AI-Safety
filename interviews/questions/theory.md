# The theory bank — fundamentals, answered from the corpus

**Navigate:** [← questions](README.md) · [take-homes](../takehomes/README.md)

**How this bank works.** Each question, then where the corpus answers
it. Practice by answering aloud before following the link — the link
is the check, not the shortcut.

## The questions

**Q1. "What is the difference between AI safety and AI alignment?"**
Open [GLOSSARY.md](../../GLOSSARY.md): safety is the umbrella (reducing
harms from AI systems); alignment is making behavior and learned
objectives coincide with intended ones. The follow-up probe is always
"give a concrete failure" — use reward hacking from
[Ch.03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md).

**Q2. "Why does my classifier's 94% accuracy mean nothing on its own?"**
[Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md)
— evaluation science: baselines, paired tests, and the confidence
interval discipline. Interviewers here are testing whether you reach
for an interval before reaching for a conclusion; the Wilson interval
is this corpus's house answer (every project report carries one).

**Q3. "What did scaling monosemanticity actually show?"**
The paper note
[18-towards-monosemanticity.md](../../research/notes/18-towards-monosemanticity.md)
and [Ch.10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md).
One sentence: features become linearly decodable as scale grows; the
interview point is what that does and does not buy (a dictionary is
not an explanation — see faithfulness vs plausibility,
[16-faithfulness-vs-plausibility.md](../../research/notes/16-faithfulness-vs-plausibility.md)).

**Q4. "Why is weak-to-strong interesting instead of just wrong?"**
[10-weak-to-strong.md](../../research/notes/10-weak-to-strong.md) and
[Ch.05](../../chapters/05-scalable-oversight/README.md): the gap
between weak supervision and strong capability is the scalable
oversight problem in one experiment. The honest answer includes its
limits (which pairs, which tasks — the note says).

**Q5. "Models know what they know — so what?"**
[11-models-know-what-they-know.md](../../research/notes/11-models-know-what-they-know.md)
+
[Ch.06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md):
calibration as a safety property (selective prediction), not a
benchmark trophy. Follow-up probe: "how would you measure it here?" —
P03 is the answer.

**Q6. "What changes between jailbreaking and many-shot jailbreaking?"**
[04-sleeper-agents.md](../../research/notes/04-sleeper-agents.md) for
deception-persistence context; the many-shot entry is registered in
the claims register. The interview point: attack cost scaling with
context, i.e., attacks that get cheaper as capability grows — the
exact shape Ch.15 trains you to name.

**Q7. "Give me a failure mode that gets worse with scale."**
Pick any: deception persistence (sleeper agents), attack cost
(many-shot), or eval-awareness. Anchor in
[Ch.07](../../chapters/07-deception-scheming-and-evaluation-awareness/README.md).
The strong answer names the evidence and its access level — that is
this corpus's habit.
