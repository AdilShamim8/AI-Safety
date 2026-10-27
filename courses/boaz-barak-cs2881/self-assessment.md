# CS 2881 — the self-assessment

*Part of the Harvard CS 2881 companion · 2026-10-27*

Twenty questions on the course's announced scope — the
topics its schedule pages publish. They test the understanding the
course's own method prizes: can you price a claim, name the evidence
class it belongs to, and state what would weaken it?

## The instrument

**Risk models and trajectory (1–5)**

1. State the two organizing axes of the course in your own words,
   and give one example of a safety question that changes answer
   under each axis.
2. What does METR's long-task measurement actually measure, and what
   three things is it NOT evidence for?
3. Name the three types of intelligence explosion in the Davidson
   typology, and state which one leaves monitoring the least
   wall-clock time.
4. Why does the course assign both *AI 2027* and "AI as Normal
   Technology" in week one? What methodological promise does that
   pairing make?
5. The Fall 2026 opener replaced scenario debates with incident
   post-mortems. What does that substitution claim about the field's
   evidentiary maturity?

**The training stack (6–9)**

6. Draw the modern training pipeline from pretraining to safety
   training, and mark the safety-relevant failure surface of each
   stage.
7. What is the safety-relevant difference between RLHF and RLVR —
   and what failure surface does each open?
8. Why does on-policy distillation make safety properties harder to
   certify? What exactly bypasses what?
9. What did the Canaries-in-the-Coal-Mine line find, and what
   self-reported quantity did it show to be unreliable?

**Security, specification, control (10–16)**

10. Why is prompt injection structurally harder than SQL injection
    to close? Name the channel that cannot be cleanly separated.
11. What does the Nasr et al. extraction result sever? State the
    inference it forbids about aligned models.
12. What is the adjudication gap in model specs, and what fills the
    equivalent gap in real legal systems?
13. Define scheming operationally — the three observable parts —
    and say which part alignment-faking demonstrated.
14. What is the obfuscation trap in CoT monitoring, and what general
    rule does it state about monitors?
15. Why does the control paradigm assume adversarial capability, and
    what does trusted/untrusted separation buy?
16. What did the Under Pressure experiment show about the *elicited*
    nature of evaluation gaming, and what design principle is the
    honest-exit lesson?

**Interpretability, economics, governance (17–20)**

17. What are the four labs' interpretability bets, per the lecture's
    guest roster? What does AxBench's finding say about the SAE bet?
18. State the Turing Trap's argument in two sentences, and explain
    what a centaur evaluation measures that an AI-only benchmark
    cannot.
19. What is GDPval's construct, and why is its estimate a leading
    indicator rather than a deployment forecast?
20. What does the open-weights debate's "gradient of release" say is
    NOT a binary — and why does data consent sit beneath the whole
    question?

**Pointers** (after attempting): 1–5 — Ch. 01 and the CS 2881 lecture-01 notes; 6–9 — Ch. 04, the lecture-02 notes; 10–16 — Ch. 12–15 and the lecture-03/08 notes; 17 — Ch. 09–11 and the lecture-10 notes; 18–20 — Ch. 20–21 and the lecture-09/12 notes.

## How to use this

Work each item in writing before looking at the pointers. The
questions are calibrated so that a learner who has only watched the
videos will find several of them sharp, and one who has also worked
the repository chapters will find them fair. That gap is the
diagnostic: it is what "watched" leaves out, measured.
