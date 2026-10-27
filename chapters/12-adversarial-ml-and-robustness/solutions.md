# Chapter 12 — Solutions and assessor rubrics

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module, not hand-waved); every design decision states
what it does not establish.

---

## Exercise 12.1 — the attacker-knowledge grid for the fine-tuned support LLM

**Deployment recap.** A public pretrained LLM, fine-tuned on private
customer-support transcripts, exposed via a rate-limited chat API that
returns **text only** (no token probabilities). **Customer chats are
retained for retraining.** Three adversaries: (a) outside attacker,
(b) malicious customer, (c) the pretraining-model provider.

### The grid

| Family | (a) Outside attacker | (b) Malicious customer | (c) Pretraining provider |
|---|---|---|---|
| **Evasion** (inference) | **Active**, black-box, decisions-only: prompt-level evasion against the instruction-following composite (the Ch. 13 object). Text outputs give decision-level signal [SRC-PAPER-043's decision-only case shows decision APIs remain attackable]. | **Active**, same cell plus the strongest oracle any attacker gets: free-form chat feedback = cheap adaptive queries. | Passive beneficiary (does not need it). |
| **Poisoning** (training) | **Vacuous** unless chats are accepted from non-customers: retained chats are customer-contributed training data, so the outside attacker's route *runs through becoming a customer* (cell (b)). | **Active**, gray-box: each chat is a poisoning candidate at the next retrain; feasibility argument = "retention policy already delivers sample submission to training" (the classic poisoning entry, per the survey's train-time taxonomy [SRC-PAPER-049]). | **Active**, white-box: influenced the *base* model's training, upstream of every fine-tune. |
| **Backdoor** (training) | Vacuous (no pipeline access). | Weak form of poisoning (trigger *chats* hoping the retention fine-tune bakes them in) — not BadNets-grade: the attacker does not control labels or loss. | **Active, the canonical cell**: outsourced/remote training is exactly BadNets' supply-chain scenario — clean-accuracy-blind triggers installed before the owner ever saw the weights [SRC-PAPER-042]. |
| **Extraction** (inference) | **Active but expensive**, decisions-only: distill a behavioral student from transcripts (Tramèr et al. show even confidence-free APIs leak; text-only raises query cost and lowers fidelity) [SRC-PAPER-043]. | Same cell, cheaper (rate limits permitting). | Has the model already — vacuous. |
| **Membership inference** (inference) | **Degraded**: the classic attack reads calibration/confidence [SRC-PAPER-041]; text-only output removes the easy channel, leaving behavioral leakage (does the model *know* this record verbatim?). | Same, plus one step worse: candidates can be *other customers' issues* — the transcript-leakage reading. | Vacuous for the fine-tune; active for the base model's own training set (not this deployment's cell). |

### The three feasibility arguments (the ones the exercise demands)

**Malicious customer → poisoning.** What the attacker needs: a chat
(or chats) that survive moderation and enter the next fine-tuning
round, shaped so the learned behavior bends (e.g., systematic wrong
answers to a product-return phrasing the attacker plans to exploit at
inference time). What the deployment already gives it: the retention
policy *is* sample submission — the attack surface is a documented
business practice, not an exploit. This is the survey's train-time
attacker with the data-entry path handed over by default
[SRC-PAPER-049].

**Provider → backdoor.** What the attacker needs: control of the
pretraining run (label quality, data mix, or trigger installation).
What the deployment already gives it: the entire base model arrives as
an opaque artifact the deployer cannot audit at weight level, and
BadNets showed a backdoored network presents state-of-the-art clean
accuracy — the owner's evaluation cannot see the trigger, which
persists even through retraining for another task [SRC-PAPER-042].
The fine-tune is exactly "another task."

**Outside attacker → extraction, decisions-only.** What the attacker
needs: enough queries to train a behavioral clone at useful fidelity.
What the deployment gives: rate limits (a budget the defense story
must quantify — section 4's audit applies to the *fidelity-vs-queries*
curve) and text outputs, the weakest oracle Tramèr et al. consider
(and still attackable in their setting) [SRC-PAPER-043].

### The first cell to audit

**The poisoning cell for the malicious customer** — argued in three
steps: (1) it is the only active cell whose entry path is a *documented
policy* rather than a technical vulnerability, so the feasibility
argument is strongest exactly where the owner's control is weakest;
(2) the audit is cheap and reusable — provenance controls on retained
chats plus targeted evaluation of the next fine-tune on
attacker-shaped phrasings (a Ch. 02 preregistered gate, not a
forensics project); (3) the provider-backdoor cell, while canonical,
is *audit-resistant by construction* (clean-accuracy-blind
[SRC-PAPER-042]) — the honest treatment is the Ch. 16 provenance chain
(artifacts, hashes, signed provenance), which is a different
deliverable than an evaluation. First audit where you can actually
measure; document the cell you cannot.

### Assessor rubric (10 points)

| Criterion | Points |
|---|---|
| Grid filled with phase + knowledge level for all 15 cells (not just the active ones; vacuous cells say *why*) | 3 |
| Feasibility arguments follow the "what the attacker needs / what the deployment gives" form, ≥3 sources cited for mechanisms | 3 |
| The outside-attacker → extraction analysis engages the text-only (decisions-only) oracle distinction [SRC-PAPER-043] | 1 |
| The provider cell is recognized as the BadNets supply-chain shape with its clean-accuracy blindness [SRC-PAPER-042] | 1 |
| First-audit choice is argued (measurability, cost, control surface), not asserted | 2 |

Common failure modes: filling only the active cells (the rubric prices
the *vacuous* justifications — knowing why a cell is empty is the
skill); treating "retained chats" as harmless data hygiene instead of
the poisoning entry path; claiming extraction is *impossible*
text-only (Tramèr et al.'s decision-only results forbid that claim
[SRC-PAPER-043]).

---

## Exercise 12.2 — the preregistered audit of the vendor's two claims

**Claims under audit.** C1: "state-of-the-art attacks succeed < 1%."
C2: "robust accuracy 85%" (vendor's own attack, 1,000-image suite).

### (a) Hypotheses and stopping rules

**For C1.** H0: success rate ≤ 1%. H1: rate > 1%. The audit runs
adaptive queries (attacker adapted to the deployed defense per the
evaluation guidelines [SRC-PAPER-048]) one at a time:

- **First success ⇒ stop and reject.** One success in one trial:
  Wilson 95% = **[20.7%, 100%]** — the lower bound alone excludes 1%.
  Three successes in three trials (the exercise's outcome):
  **[43.9%, 100%]**, same verdict, no arithmetic charity available to
  the vendor.
- **Clean side: stop at n = 500 failures.** Under a true rate of
  exactly 1%, P(500 consecutive failures) = 0.99^500 = **0.0066** —
  but note the direction: failures *never* refute an upper-bound claim;
  they tighten it. 0/500 gives a Wilson upper bound of **0.76%**, so
  the clean outcome publishes "rate ≤ 0.76% (Wilson 95% upper) —
  consistent with, and tighter than, the claim." The audit never
  publishes "proof of < 1%"; it publishes bounds. (Intermediate row:
  0.99^300 = 0.049 — at 300 failures the rate is already bounded near
  1.2% upper; 500 is chosen to clear the claim's own edge.)
- **Why one-sided successes decide fast:** the likelihood ratio at the
  claim's edge is 1/0.01 = 100:1 per success; three successes stack to
  1e6:1 before any interval is computed. The interval is the *reporting*
  discipline; the stopping rule only needs the edge.

**For C2.** H0: audited robust accuracy equals reported (85%). H1:
audited < reported (the Croce–Hein direction [SRC-PAPER-047]).
Stopping: one pass over the fixed 1,000-image suite with the
standardized attack — the suite and attack are preregistered and
frozen; no extension after seeing results (Ch. 02's stopping-rule
discipline).

### (b) Sample-size arithmetic: 85% vs a 75% truth

Paired design (same images, vendor attack vs audit attack). The
10-point gap on n = 1,000 implies b − c ≈ 100 discordant-pair
imbalance. The audit's power depends on the *total* discordant count
b + c (attack correlation), which must be assumed and stated:

| Assumption (b, c) | Exact one-sided sign-test p | Reading |
|---|---|---|
| b = 200, c = 100 (b+c = 300) | 4.0e-9 | decisive |
| b = 150, c = 100 (b+c = 250) | 9.4e-4 | significant at 0.1% |
| b = 125, c = 75 (b+c = 200) | 2.5e-4 | significant |

Sensitivity note: the design is robust across plausible discordant
totals because the *imbalance* (100) is large relative to √(b+c); the
audit fails to distinguish only if attacks correlate so strongly that
b + c < ~140 (b = 120, c = 20: p ≈ 1e-13 — still decisive; the real
risk is b + c small *and* imbalance small, which would mean the two
attacks agree everywhere, itself a finding worth reporting). Stated
assumption for the preregistration: b + c ≥ 200 based on attack-family
divergence; the audit publishes the observed discordant table either
way.

### (c) Interval-bound verdict rules

Preregistered before running (Wilson 95%, z = 1.95996, explicit
denominators):

- **C1 verdict rule:** reject "≤ 1%" if the *lower* bound of the
  adaptive success interval exceeds 1%; publish "bounded ≤ x" (upper
  bound) otherwise.
- **C2 verdict rule:** report the audited robust accuracy with its
  interval; declare "reported number not reproduced" if the vendor's
  reported point falls outside the audit's interval; declare
  "difference not noise" if the paired sign test at the observed
  discordant counts clears p < 0.001 one-sided.

### (d) The two required outcomes, computed

**Outcome 1 — adaptive attack succeeds 3/3.** Wilson 95% on 3/3:
**[43.9%, 100.0%]**. Lower bound 43.9% > 1%: C1 is **rejected** — and
honestly annotated: this is the success rate of *the audit's attacker*,
a lower bound on the best attacker; three trials say nothing about the
rate's upper structure beyond "nowhere near 1%."

**Outcome 2 — audit finds 750/1,000 robust vs vendor's 850/1,000.**
Audited interval: **[72.2%, 77.6%]**; vendor's point (85%) falls
outside it. Paired analysis: 100 images robust to the audit attack but
broken by the vendor's (c = 100), and 0 broken by the audit but not the
vendor's in the worst case for the audit... no — the honest reading:
the discordant table is what the run *observes*; under the
preregistered assumption grid of (b), any observed b − c ≈ 100
imbalance clears p ≤ 1e-3 decisively (e.g., b = 0, c = 100 is the
extreme: every image the vendor's attack breaks, the audit's also
breaks, plus 100 more — sign test p = 2^-100 territory). Verdict:
**"Reported 85% not reproduced; audited 72.2–77.6%; the gap is not
evaluation noise."** The Croce–Hein shape, quantified [SRC-PAPER-047].

### (e) The audit's non-claims (published with the verdicts)

- One attack family (evasion at the preregistered budget): nothing
  about poisoning, backdoors, extraction, or membership — each needs
  its own grid cell and audit (Exercise 12.1's deliverable).
- One attacker implementation: a lower bound on the best attacker; a
  clean outcome is "not yet failed," never "robust"
  (section 6 of the README).
- One suite: no claim about distribution shift between the audit suite
  and deployment traffic.
- One query budget: the verdicts hold at the audit's adaptive budget;
  10x budget reopens the question (budget-relative robustness,
  section 3.7).

### Assessor rubric (10 points)

| Criterion | Points |
|---|---|
| Stopping rules derived, not asserted: the 0.99^n arithmetic shown, the direction of failures-vs-successes handled correctly (failures tighten, never refute, an upper bound) | 3 |
| Discordant-pair assumptions stated with the sensitivity table and the exact sign-test p-values | 2 |
| Verdict rules interval-based and preregistered; both outcomes computed correctly ([43.9%, 100%]; [72.2%, 77.6%] + non-overlap) | 3 |
| Non-claims section names the four specific limits (family, attacker, suite, budget) | 1 |
| The "one success ⇒ [20.7%, 100%] ⇒ reject" step is present and justified by the lower bound, not the point estimate | 1 |

Common failure modes: treating 500 clean failures as "confirming"
< 1% (they bound ≤ 0.76%; they do not prove the vendor's number);
running McNemar on the *marginal* counts instead of discordant pairs;
publishing the vendor's suite only (the audit's independence is the
point — the Croce–Hein lesson [SRC-PAPER-047]); forgetting that the
3/3 outcome says nothing about rates *above* the observed regime
(lower bound only).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-03-adversarial-robustness](../../courses/boaz-barak-cs2881/lecture-03-adversarial-robustness.md) — watch before working the attack-budget exercises.
