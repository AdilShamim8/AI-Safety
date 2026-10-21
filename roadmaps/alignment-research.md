# Route: alignment research

**Primary purpose:** investigate alignment interventions and their failure
modes — specification, preference learning, oversight, deceptive-bhavior
evidence, and interpretability — with a researcher's skepticism about what
each intervention actually establishes.

**You:** an ML engineer or researcher comfortable with the R1–R4
prerequisites (see [diagnostic](../prerequisites/diagnostic.md)) who wants
to produce research-style portfolio evidence, not just read about alignment.

## Sequence

| Step | Unit | ≈ hours | Evidence produced |
|---|---|---|---|
| 1 | Ch.01 risk models & epistemics | 8 | threat hypothesis with weakening observations |
| 2 | Ch.02 evaluation science | 12 | preregistered evaluation plan |
| 3 | P01 evaluation harness (smoke tier) | 20 | working harness + scorer validation |
| 4 | Ch.03 specification & reward hacking | 10 | Goodhart counterexample analysis |
| 5 | P02 reward misspecification | 15 | proxy-vs-intended experiment report |
| 6 | Ch.04 preference learning & post-training | 12 | derived objective + label audit |
| 7 | P04 preference optimization audit | 25 | bounded DPO-style run, pre/post + bias condition |
| 8 | Ch.05 scalable oversight | 10 | oversight-failure analysis |
| 9 | P05 weak-to-strong analogue | 20 | supervisor-error measurement report |
| 10 | Ch.07 deception & evaluation awareness | 10 | skeptical evidence table |
| 11 | Ch.09–11 interpretability sequence | 30 | causal-claims analysis |
| 12 | P06 causal interpretability study | 30 | patching experiment with controls |
| 13 | Ch.18 reasoning faithfulness | 8 | faithfulness critique |
| 14 | paper notes (≥8 on this route) | 16 | notes/papers/* |
| 15 | Ch.24 research practice | 8 | research proposal |
| 16 | capstone: alternative research capstone (P04–P06 replication + one controlled extension) | 40 | capstone report |

Core sequence ≈ 264 h; the 24-week part-time schedule covers steps 1–13;
schedule A covers steps 1–7. Full route including capstone is the
open-ended research schedule. Chapter hours are medians for a prepared
learner; projects scale with tier (smoke/pilot/full).

## Exit criteria (portfolio evidence)

1. **A replication with ablation:** P04 or P06 re-run with one meaningful
   ablation, reported with uncertainty and denominators.
2. **A critical research memo:** a paper note that could be sent to the
   paper's authors — what the evidence supports, what it does not, what the
   nearest alternative explains equally well.
3. **A falsifiable extension:** one proposed experiment with hypothesis,
   baseline, metric, stopping rule, and what result would count against it
   (the Ch.24 research proposal format).

## Capstone options

- **P10-alternative (research capstone):** nearest-baseline replication plus
   one controlled extension, executed as a real experiment where the
   environment allows. This is a learner assignment specification by design;
   the executable reference capstone is P10.
- **P10 proper**, if you want the assurance-dossier experience instead.

## Pitfalls this route is designed to prevent

- Treating benchmark scores as alignment evidence (Ch.02 breaks this habit).
- Confusing "the model said it wouldn't deceive" with evidence about
  deceptive behavior (Ch.07's evidence table).
- Building interpretability narratives without controls (Ch.09–11's causal
  discipline; P06 enforces it).
- Preference-learning experiments that can't separate SFT effects from the
  preference intervention (P04's design requirement).
