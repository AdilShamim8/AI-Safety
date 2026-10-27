# Targeted refreshers

Six short, targeted refreshers (R1–R6), one per diagnostic failure mode. Each
tells you what to rebuild, the fastest way to rebuild it, and which chapters
assume it. The refreshers deliberately avoid linking to unverified web
resources: chapter reading lists supply the verified primary sources, and any
rigorous textbook you already own covers R1–R4. Estimated effort assumes you
once knew the material.

## R1 — Probability and linear algebra for ML (~4–8 h)

**Rebuild:** conditional expectation and variance; law of total expectation;
common discrete distributions (binomial, categorical) and what "n independent
trials" actually buys you; the Central Limit Theorem's conditions and its
failure under correlation; matrix multiplication as composition; norms and
inner products; eigendecomposition intuition (why directions of variance
matter). 

**Check you're ready:** you can explain why a Wilson interval is safer than
a normal approximation at n = 20, and why `‖p − y‖` in the diagnostic's
gradient shrinks as predictions improve.

**Assumed by:** chapters 02 (intervals, power), 06 (calibration), 09–11
(linear algebra of activations and probes).

## R2 — PyTorch mechanics and transformer internals (~6–10 h)

**Rebuild:** tensors, broadcasting, autograd graphs; writing a training loop
without copying one; registering forward hooks and reading activations; the
decoder-only transformer data path — embeddings, residual stream, attention
(Q/K/V, softmax over `L×L`), MLP blocks, LayerNorm placement, causal mask;
what "logits" and "sampling" mean operationally.

**Check you're ready:** you can sketch the shape changes through one
transformer block for `[B, L, d]` input and say where you'd hook to capture
attention patterns.

**Assumed by:** chapters 04 (training objectives), 09–11 (all
interpretability work), projects P04 and P06.

## R3 — Experiment hygiene (~3–5 h)

**Rebuild:** train/validation/test as *roles*, not files; leakage taxonomy
(temporal, group, feature, target); why tuning on test is silent
contamination; uncertainty that respects the sampling unit (cluster-aware
intervals); effect size vs. significance; what a failed replication tells
you; preregistration as a commitment device.

**Check you're ready:** you can state, without prompting, the three things
wrong with "we tuned the threshold on the test set and got p < 0.01."

**Assumed by:** every chapter; load-bearing in 02, 15, 17, 20, 24. This is
the course's most-used refresher.

## R4 — RL and MDP basics (~4–6 h)

**Rebuild:** the MDP tuple and what each element assumes; policies and value
functions; the discount factor as horizon; policy-gradient intuition (REINFORCE
shape) without derivations; reward as *specification*, not intention;
multi-epoch RLHF-style fine-tuning at a conceptual level.

**Check you're ready:** you can write the invoice-assistant MDP from the
diagnostic cold, and say what γ = 0.99 implies about the horizon the policy
plans over.

**Assumed by:** chapters 03, 04, 07; projects P02, P04, P05.

## R5 — Threat modeling basics (~3–5 h)

**Rebuild:** assets, actors, trust boundaries, data flow diagrams;
attacker-controlled vs. attacker-influenced vs. trusted inputs; the
STRIDE-style categories as a coverage checklist, not a taxonomy of
equivalents; least privilege and capability-based authorization; why
"the LLM will follow the system prompt" is not a control.

**Check you're ready:** given any system sketch, you can draw its trust
boundaries in under five minutes and name one attacker-controlled input per
boundary.

**Assumed by:** chapters 12–15, 19, 22; projects P07, P08, P10.

## R6 — Causal-claims literacy (~3–4 h)

**Rebuild:** confounding, selection bias, pre-trends; the difference between
"associated with" and "causes" in measured language; difference-in-differences
logic; why randomization identifies effects; Simpson's-paradox-style
aggregation traps; the unit of analysis and clustering.

**Check you're ready:** you can take any "X improved metric Y" claim and
produce two plausible non-causal explanations plus one design that would
disentangle them.

**Assumed by:** chapters 17, 21; every project's error analysis.

## How to run a refresher

Do it just-in-time, not all upfront: run R3 before chapter 02, R4 before
chapter 03, and so on, per the skip guidance in
[diagnostic.md](diagnostic.md). Each refresher's "check you're ready" is the
actual re-test — if you can pass it, stop; do not gold-plate.

## Watching companions for the refreshers

The lecture library's accessible layer can substitute for a refresher
session when reading stamina runs out: the CAIS fundamentals lecture
(52 minutes, no math) covers the same ground as R2's model-behavior
refresher in a different register, and the DeepMind course's Part 1
makes a good pre-diagnostic warm-up. Watch, then return to the
written refresher — the diagnostic still requires the written form.
