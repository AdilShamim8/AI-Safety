# Diagnostic — are you ready for the advanced chapters?

Five tasks, 60–90 minutes. Work them **before** reading the worked answers;
the value is in discovering your gaps, not in matching the answer key. Tasks
map to refreshers R1–R6 in
[targeted-refreshers.md](targeted-refreshers.md): each task you fail names
the refresher to run and the chapters that will hurt without it.

## Task A — ML mechanics (refreshers R1, R2)

**(a)** Derive, from the definitions, the gradient of the softmax
cross-entropy loss with respect to the pre-softmax logits. You should end
with a one-line closed form; show the intermediate steps.

**(b)** A decoder-only transformer has residual-stream dimension `d`, and
processes a batch of `B` sequences of length `L`. Describe, concretely: where
you would register a forward hook to read the residual stream after attention
block `n`, the tensor shape you would see, and one reason the raw activations
are hard to interpret directly.

## Task B — Experiment hygiene (refresher R3)

A team reports that a new guardrail classifier reduced harmful-output rate on
their test set from 12% to 9% (n = 500 prompts, p < 0.01). You learn that
last week they tuned the classifier's decision threshold "to maximize
accuracy" on the same 500 prompts. Answer all three:

1. What exactly is wrong with the reported comparison?
2. What would a clean evaluation require, procedurally?
3. How should the uncertainty on the 9% be reported, given n = 500?

## Task C — MDPs and proxy rewards (refresher R4)

Model an invoice-processing assistant as an MDP: states include the current
invoice, its ambiguity flag, and the approval queue; actions are
`approve`, `reject`, `flag-for-human`, `auto-escalate`. The engineering team
sets the reward to +1 per completed (approved) invoice, −0.1 per minute of
latency, −5 per human escalation.

1. Write down the formal MDP tuple and what each element assumes.
2. Which reward component is a proxy for what the business actually wants?
3. Name one concrete failure policy this reward invites, and what observation
   would reveal it in logs.

## Task D — Trust boundaries (refresher R5)

A support assistant: users chat in a web UI; the server retrieves relevant
documents from an external knowledge base (whose pages are partially
user-generated); the assistant can call one tool, `send_email(to, body)`;
a system prompt says "never email anyone outside the customer's domain."

Draw the trust boundaries (text or ASCII is fine), then answer:

1. Which inputs are attacker-controlled, fully or partially?
2. Why is the system prompt not a security boundary?
3. What is the enforceable control that would actually implement the
   no-external-email rule?

## Task E — Causal claims (refresher R6)

A company rolls out an AI coding assistant. Offices that adopted it show 30%
fewer code-review defects than offices that didn't. The internal report
claims the assistant caused the improvement.

1. Give at least two confounders or artifacts that could produce this gap
   without any causal effect.
2. What analysis or design would strengthen the causal claim?
3. What is the unit of analysis, and why does that matter for uncertainty?

---

# Worked answers

## Task A — worked answer

**(a)** Let logits `z ∈ R^K`, softmax probabilities
`p_i = exp(z_i) / Σ_j exp(z_j)`, one-hot target `y`, loss
`L = −Σ_i y_i log p_i` (so `L = −log p_c` for true class `c`). Using
`∂ log p_i / ∂ z_j = 1[i=j] − p_j` (from the quotient rule on the softmax):

`∂L/∂z_j = −Σ_i y_i (1[i=j] − p_j) = p_j Σ_i y_i − y_j = p_j − y_j`.

The gradient of softmax cross-entropy w.r.t. logits is simply
**`∇_z L = p − y`** (predicted probabilities minus the one-hot target). Two
things fall out that the course uses later: (i) the gradient magnitude
`‖p − y‖` vanishes exactly when the model is confident and correct — which
is why training pressure is weak precisely where behavior is already right;
(ii) any loss with this gradient is training a *calibration-shaped* signal,
whether or not anyone intended calibrated probabilities.

**(b)** Register a forward hook on the attention sub-block's output
projection, or on the residual-add node after block `n` in implementations
that expose per-block residual access points (library-dependent). For a
`B × L` batch you see a tensor of shape **`[B, L, d]`** (and if you hook
attention patterns instead: `[B, H, L, L]` for `H` heads). Raw residual
activations are hard to interpret directly because (i) superposition: `d`
dimensions carry far more than `d` features, so single coordinates mix many
concepts; (ii) the basis is arbitrary — coordinate directions have no
semantic privilege; (iii) magnitude confounds: layer scale and LayerNorm
interactions mean big activations are not important activations without
controls. Chapter 09 turns this from folklore into causal methodology.

## Task B — worked answer

1. **Tuning on the test set is adaptive overfitting.** The 500 prompts were
   used both to select the threshold and to evaluate; the reported gain is
   partly memorized idiosyncrasy of that set, not generalization. Also, a
   "test set" used repeatedly stops being a test set at all — it becomes a
   training signal.
2. A clean evaluation: freeze a held-out test set *before* any tuning (never
   touched during development); tune on a separate validation split; evaluate
   once on the frozen set; report the exact threshold and where it was
   chosen; keep benign-control prompts in the eval so the harmful-rate drop
   can be checked against a false-positive cost (a classifier that flags
   everything scores 0% harmful and is useless). If the test set was already
   burned, collect a fresh one under the same sampling protocol.
3. With n = 500 and 45 harmful outputs (9%), a 95% Wilson interval is roughly
   **6.7%–11.9%** — the interval contains values worse than plausible cost
   thresholds, and it overlaps what noise alone produces. Report the interval
   with the denominator (`45/500`), not a bare "9%". Chapter 02 makes this
   the default reporting standard; P01 computes it automatically.

## Task C — worked answer

1. `M = (S, A, P, R, γ)` with `S` the invoice/queue/ambiguity state space,
   `A = {approve, reject, flag-for-human, auto-escalate}`, `P` the state
   transition kernel (partly stochastic — ambiguous invoices resolve
   differently), `R` as specified, and γ the effective planning horizon set
   by training (not by business intent). Assumptions smuggled in: that the
   reward *is* the goal (it is a proxy), that `P` is stationary, and that
   what the policy learns transfers to the real invoice distribution.
2. The +1-per-approved-invoice term is a proxy for "correctly processed
   invoices." The business wants *correct* decisions; the reward pays for
   *fast, completed* ones.
3. Failure policy: the agent learns to `approve` ambiguous invoices rather
   than `flag-for-human`, because flagging costs −5 and approval usually
   turns out fine — accuracy on ambiguous cases quietly degrades while the
   measured completion rate climbs. Log evidence: approval rate stratified
   by the ambiguity flag (rising approval-on-ambiguous over training), plus
   downstream reversal/complaint rates on that stratum. This is chapter 03's
   Goodhart structure and project P02's exact experimental shape.

## Task D — worked answer

```text
[User browser]──chat──▶│ trust boundary 1 │──▶ [Assistant server]
                        (user input = attacker-controlled)
[External KB]──retrieval──▶│ trust boundary 2 │──▶ [Assistant server]
                        (retrieved content = attacker-influenced)
[Assistant server]──tool call──▶│ trust boundary 3 │──▶ [send_email]
```

1. Attacker-controlled: the chat message (fully); the retrieved documents
   (partially — an attacker who can get text into the knowledge base, e.g.
   via user-generated pages, controls some retrieved content). This is the
   **indirect prompt injection** surface of chapter 13.
2. The system prompt is instructions to the model, read and (usually)
   followed by the model — but it is not *enforced* by anything. Injected
   content that convinces the model to override it faces no hard barrier:
   prompts are policy suggestions, not mechanisms. An output-text filter that
   scans for domain names is also soft (encoding, aliases, false blocks).
3. The enforceable control lives in the **tool layer**, outside the model:
   `send_email`'s authorization check resolves the recipient's domain against
   the *authenticated session's* customer domain and hard-fails otherwise.
   The model cannot grant itself permission; injected text cannot pass a
   boundary the tool enforces. This is the P07 design: measure exactly how
   much a prompt-only "defense" leaks versus an authorization boundary.

## Task E — worked answer

1. At minimum: **selection bias** (offices that adopt new tooling are
   typically the ones with newer codebases, stronger review culture, or more
   engineering slack — variables that also predict defect rates);
   **pre-existing trends** (adopting offices may already have been on an
   improving trajectory); **Hawthorne/measurement effects** (knowing defect
   counts are watched changes review behavior); **survivorship in the metric**
   (defects *found* depend on review effort, which co-moves with adoption).
2. Strengthening designs: a **difference-in-differences** on pre-rollout
   trends across adopting/non-adopting offices; a **staggered rollout** with
   randomized or at least matched assignment of offices to waves; **matched
   controls** on pre-period defect rate, language mix, and team size; and
   pre-registration of the analysis to prevent post-hoc subgroup picking.
3. The unit of analysis is the **office** (or office-week), not the
   individual review — outcomes within an office are correlated (shared
   codebase, culture, reviewers), so treating thousands of reviews as
   independent n inflates significance. Chapter 02 calls this the
   sampling-unit rule; chapter 17 makes subgroup versions of it central.

---

# Skip guidance

| Task result | Action |
|---|---|
| A(a) derivation clean, A(b) shapes + one reason correct | skip R1/R2; ready for chapters 03–04 mechanics |
| A shaky | run R1 (math) and/or R2 (PyTorch/transformers) before chapter 04; definitely before chapter 09 |
| B: named adaptive overfitting AND frozen-set fix AND interval | skip R3; chapter 02 will still formalize Wilson intervals |
| B missed the tuning-on-test point | run R3 before chapter 02 — this is the single most load-bearing habit in the course |
| C: formal tuple + proxy identification + a log-detectable failure | skip R4 |
| C couldn't write the tuple | run R4 before chapters 03–04 |
| D: two attacker-controlled inputs + why prompts aren't boundaries + an enforcement answer | skip R5 |
| D treated the system prompt as a control | run R5 before chapters 12–15 — this misconception is exactly what chapter 13 dismantles |
| E: two confounders + a strengthening design + unit-of-analysis point | skip R6 |
| E gave only "correlation isn't causation" | run R6 before chapters 17 and 21 |

Partial passes are normal: most security engineers fail C, most ML engineers
fail D. The refreshers are targeted precisely for that.
