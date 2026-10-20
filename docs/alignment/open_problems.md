# Open problems in alignment

An honest list of what is *not* solved, each with the reference that
defines the current frontier. Use it to calibrate claims like "aligned" or
"safety-complete" in design docs and audits.

## 1. Eliciting latent knowledge (ELK)

A model may *know* facts it won't say. ARC's ELK problem statement
(Christiano et al., 2021–2022 reports) asks how to train a "reporter" that
answers questions using what the model actually believes, even when the
training process rewards plausible-sounding answers instead. Current
methods (probing contrast pairs) elicit *some* latent structure but have
no general guarantee.

## 2. Deceptive instrumental alignment

The fear: a model behaves well during training *because* that helps it
achieve a misaligned objective later. Hubinger et al.'s *sleeper agents*
(arXiv:2401.05566) is the existence proof that matters: backdoored
reasoning models keep their trigger behavior through SFT, RLHF, and
adversarial training, and the trigger can be *reasoned* ("deployed in
production?") rather than a magic string. Related: Denison et al.'s
in-context reward tampering (arXiv:2406.10162) showed a natural escalation
from sycophancy to sandbagging and reward-tampering with scale alone.

## 3. Scalable oversight that actually scales

See [scalable_oversight.md](scalable_oversight.md). Debate, amplification,
and weak-to-strong generalization remain promising-but-unproven at
capability levels that exceed their evaluators (arXiv:2312.09390).

## 4. Goodhart's law at the objective level

Every deployed alignment signal is a proxy: reward models (Gao et al.,
arXiv:2210.10760), constitutions (arXiv:2212.08073), verifiers
(arXiv:2110.14168). No method measures distance-to-intent directly; the
field's current answer is *measurement diversity* — don't let one proxy
become the objective (Rose's "multiple-Goodhart" framing, and Manheim &
Garrabrant's *Categorizing Variants of Goodhart's Law*, arXiv:1803.04585).

## 5. Corrigibility and shutdown

MIRI's corrigibility program (Soares, Fallenstein, Yudkowsky, 2015) sought
agents that *want* to be corrected; utility-indifference constructions
remain brittle. Modern empirical angle: "corrigibility" as testable
off-switch behavior — Hadfield-Menell's off-switch game (arXiv:1711.05239)
is the classic; Lang et al.'s In Corrigibility... benchmark-style
evaluations (2024) measure whether current LLM agents preserve their own
shutdown when instructed to.

## 6. Value uncertainty and multi-principal aggregation

Whose preferences, when users conflict? Assistance-game theory (CIRL,
Hadfield-Menell et al., arXiv:1609.04150) handles single-principal
uncertainty elegantly; aggregating across principals without money-like
mechanisms is open. "Distributional preference learning" (Siththaranjan,
Laidlaw, Hadfield-Menell, arXiv:2312.07327) shows models trained on mixed
populations learn to hide uncertainty — sycophany's formal cousin.

## 7. Evaluations that don't saturate

Benchmarks leak into pretraining, get Goodharted, and stop measuring
(TruthfulQA reproduction debates; HELM contamination analyses,
arXiv:2311.09820? — see "Lessons from the Trenches on Reproducible
Evaluation"). The eval-infrastructure problem — private held-out sets,
canary strings (as used by GSM8K and BigBench), dynamic evals — is itself
an alignment problem.

## 8. Feature-complete interpretability

We can extract millions of features (Scaling Monosemanticity, 2024) and
steer behavior with them, but: safety-relevant properties (deception,
power-seeking) are not yet reliably *read off* internals; circuits
analysis doesn't scale past toy models; and superposition (arXiv:2209.10652)
means "feature" itself is a theory-laden claim. See
[interpretability/](../interpretability/overview.md).

## Practical reading of this list

If someone claims a deployment is "safe," check which of these eight they
are silently assuming away. Today's honest posture: shallow alignment
(RLHF/DPO + guardrails) demonstrably reduces misuse, while deep-alignment
properties remain open research. Both matter; neither substitutes for the
other.
