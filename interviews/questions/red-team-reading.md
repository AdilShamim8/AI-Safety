# The red-team reading bank — named threats, named defenses

**Navigate:** [← questions](README.md) · [security role](../roles/security-specialist.md)

**How this bank works.** Security rounds test naming precision: a
threat you cannot name, you cannot defend against. Every entry below
is a registered source; every defense states what it does not stop.

## The questions

**Q1. "Name the OWASP LLM Top 10 risks you'd check first for an
LLM app, and why."**
The register entry (SRC-REPORT-004) holds the list; the interview
answer leads with **LLM01 prompt injection** (the highest-leverage,
lowest-cost attack) and **LLM05 improper output handling** (the
confusion-prone one: it is not the model that is wrong, it is the
consumer of the output — see the OWASP page's own distinction). The
probe: "which of the ten is most over-rated?" — have a position.

**Q2. "What is the difference between prompt injection and jailbreaking?"**
Injections target the *application's* instruction trust (the model
cannot tell your instructions from the attacker's —
[Greshake et al.](../../research/notes/06-greshake-indirect-injection.md));
jailbreaking targets the *model's* trained refusal. Ch.13 trains the
distinction; the answer that survives the follow-up names both
surfaces.

**Q3. "Walk me through a MITRE ATLAS scenario for an ML system."**
ATLAS (registered source) adapts MITRE's tactics to ML: pick a
realistic chain (e.g., poisoning or model extraction — see notes
[13](../../research/notes/13-badnets.md) and
[14](../../research/notes/14-model-extraction.md)) and narrate it
against a deployment you can see in the room.

**Q4. "Your injection defense works on the benchmark. What does it
not stop?"**
The P07 answer: distribution shift in the wild, indirect vectors the
suite does not cover (the Greshake note is the canonical indirect
case), and the honest statement that the suite is a proxy. A defense
claim without a not-covered list is a red flag in this round.

**Q5. "Why is adversarial robustness still hard?"**
[Carlini-Wagner](../../research/notes/05-carlini-wagner-robustness.md)
and [Madry et al.](../../research/notes/20-madry-adversarial-training.md):
the robustness-accuracy tradeoff as a structural result (Ch.12), not
an engineering inconvenience. The strong answer includes the
certification limits.
