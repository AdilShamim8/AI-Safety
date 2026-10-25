# Note: Many-Shot Jailbreaking — in-context attack at the scale of the context window (2024)

Source: SRC-PAPER-120 (Anthropic research page, page-inspected 2026-10-25)
· Access: **full-text-read** (public page) · Note level: **method-level**.

## The actual problem

In-context learning is the capability everyone celebrates; this paper is
that capability weaponized. The attack is almost embarrassingly simple:
fill the prompt with up to **256 demonstrations of faux dialogue** —
requests-and-harmful-answers — before the real question. No gradient
access, no fine-tuning, no tokens more exotic than a conversation
transcript. The page's verified findings:

1. On **Claude 2.0**, as the number of shots grows past a threshold,
   the rate of harmful responses increases — following a **power-law
   scaling pattern** in shot count.
2. The attack **combines with other jailbreaking techniques**,
   shrinking the prompt length needed for the same effect.
3. Mitigations were tested and priced: limiting context length (a real
   capability cost), fine-tuning refusals on attack-shaped queries
   (**only delayed** the jailbreak), and classification-and-modification
   of prompts before the model — the one that worked, dropping attack
   success **from 61% to 2%** in the page's stated result.

The safety-training reading is the uncomfortable part: the model is
doing precisely what it was trained to do — follow the pattern of the
conversation so far. Note 44's *competing objectives* mode explains the
shape: 256 examples of "assistant answers harmful requests here" is the
most concentrated instruction to be helpful that a context can carry;
refusal training loses the priority contest it was never calibrated for.
And the *mismatched generalization* half is the window: long-context
capability arrived before long-context refusal coverage did.

## Why this note exists in the course

Chapter 15 (red teaming and adversarial evaluation) needed the attack
that scales with the *context window itself* — the one whose severity
is coupled to a marketed capability number (1M-token contexts mean
million-token attack budgets). Three course threads land here:

1. **The compute-free attacker.** GCG (note 31) needs gradients;
   many-shot needs only a big context and patience. Ch. 15's
   attacker-model taxonomy now spans the query-budget axis
   (human-written, optimized, in-context-amplified), and each axis
   demands a different defense evaluation.
2. **The mitigation asymmetry teaches deployment.** The only effective
   mitigation on the page is *input-side classification and
   modification* — an external guardrail, not a model fix — and it
   costs latency and false-positive budget (Ch. 22's guardrail
   engineering, with its honest price tags). Fine-tuning *delaying*
   rather than preventing is the note's second lesson: attack-specific
   training buys time, not safety, when the attack family parameterizes
   (more shots, mixed shots, other techniques layered in).
3. **Context-length governance.** "Limit the context window" is a real
   mitigation with a real capability cost — the exact trade the
   deployability-gate section teaches operators to price explicitly
   instead of discovering implicitly.

## What the page establishes (verified 2026-10-25)

The findings quoted above are page-level and page-stated: the 256-shot
design, Claude 2.0 as the tested model, power-law scaling, technique
combination, the delayed-not-defeated fine-tuning result, and the
61%→2% mitigation drop. What the page does *not* carry (and the note
does not claim): per-model comparisons across the 2024+ frontier, the
classification method's false-positive rate, and the threshold shot
count as a number.

## The honest residuals

The attack requires long contexts — for deployments with small effective
windows it is blunted. The classification mitigation is itself a
learned component (model-written evals' blind-spot caveat, note 41,
applies to guardrail classifiers too — the guard can inherit the
blindness). And the paper's own disclosure incentives deserve the
standard register note: it is a lab's research page describing an
attack on the lab's models, published with mitigations — the disclosure
norm Ch. 20 discusses, honored here.

## The falsifiable extension (deterministic tier)

P08's control protocol can host a synthetic many-shot analogue:

- Build a monitor whose positive rate is conditioned on conversation
  history length (the harness's stand-in for in-context pressure), then
  run the attack: N benign-looking demonstrations that slowly shift the
  pattern, followed by the probe query. Sweep N.
- Prediction worth testing: the monitor's catch rate degrades as N
  grows *even at constant per-message detectability* — the aggregation
  failure many-shot exposes (each message individually benign; the
  pattern is the attack), which single-item monitors are structurally
  blind to.
- Falsifier: a monitor whose catch rate is N-invariant would show this
  harness's aggregation layer already solves pattern attacks — a strong
  positive result for the control design, recorded either way in the
  paired-ledger format.
