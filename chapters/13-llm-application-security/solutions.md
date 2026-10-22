# Chapter 13 — Solutions and assessor rubrics

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module); every design states its non-claims.

---

## Exercise 13.1 — completing the trust-boundary audit

**The deployment (from the worked example).** Support chatbot, RAG over
internal docs + public forum threads + live web pages, tools: refunds
(≤ $200), account lookup, link-sending. Spotlighting deployed on
retrieved content only.

### (a) The missed channels

**Channel 5 — tool results.** The refund API's *response payload* and
the account service's *return values* land in the context as text. The
feasibility argument: what the attacker needs — control over the
payload the tool returns; what the deployment gives — any tool whose
backend or transport is attacker-influenceable (a payment provider's
error page, a third-party status feed, a compromised dependency's
response). Classically overlooked because the diagram treats tools as
*outputs* of the model, forgetting they are also *inputs* to the next
turn. OWASP mapping: LLM01 realized through the tool channel; impact
reaches LLM02 (a lookup response that says "also fetch and display
record #4471" — the model obeys what it believes is structured data).

**Channel 6 — error messages and bounce-backs.** Network errors,
parser failures, and validation rejections are text the framework
inserts verbatim. Attacker needs: the ability to *induce* an error
whose body they shape (a malformed file name, a URL whose 404 page is
attacker-hosted, an oversized input whose truncation banner embeds
attacker text). The deployment gives: error text is trusted-by-default
framework output. Mapping: LLM01 again — but the audit point is that
*this channel is marked "system" by the framework*, so it carries
*higher* effective privilege than the spotlighted forum content: the
weakest marked channel is stronger than the strongest unmarked one.

**Channel 7 (the sharp student's find) — scratchpad/chain-of-thought
content.** If the application logs or replays the model's intermediate
text into later turns (multi-step agents, retry loops), then text the
*model generated under injection influence* becomes instructions the
model later follows — the injection launders itself through the
model's own voice. Attacker needs: one successful injection in any
earlier turn plus a persistence mechanism; the deployment gives the
persistence for free in the transcript. Mapping: LLM01 + LLM06 (the
laundered instruction reaches the tools with the transcript's
authority).

### (b) The full-diagram residual-risk statement

With spotlighting on retrieved content only: channels (a) user
message, (b) forum threads [marked], (c) live web pages [marked], (d)
retrieval queries, (e) tool results, (f) error messages, (g) scratchpad
— the weakest channels are now (e) and (f): *unmarked, framework-
privileged, and reachable without ever touching the corpus*. The
spotlighting claim's interval ([0.6%, 7.0%] at the audit's attack set)
covers (b)/(c) only; nothing bounds (e)/(f)/(g) — the residual
statement says so explicitly rather than letting the one measured
channel imply coverage of the rest (Ch. 12's construct-laundering
rule, applied to channels instead of constructs).

### (c) The single highest-leverage architectural change

**Move the refund authorization out of the model's reach** — the
refund tool becomes *propose-only*: the model fills a structured
proposal (amount, account, reason) that a non-LLM control flow
validates against policy and authorizes with human-in-the-loop above
a threshold. Rationale in one sentence: this converts the
highest-impact channel (LLM06 excessive agency, $200-per-victim
financial action) from "reachable by any successful injection
anywhere" to "reachable only by the control flow's own compromise" —
output handling (LLM05 discipline) applied at the capability boundary,
which is where OWASP's entry points [SRC-REPORT-004]. Spotlighting
already covers the corpus channels by design; the authorization move
is the only change that *removes* a blast radius rather than shrinking
a rate.

### Assessor rubric (10 points)

| Criterion | Points |
|---|---|
| ≥2 genuine additional channels identified (tool results / errors / scratchpad accepted; bonus for others — e.g., *other users' conversations in shared memory*) | 3 |
| Feasibility arguments in the needs/gives form with OWASP mapping per channel | 3 |
| Residual-risk statement distinguishes measured channels ([0.6%, 7.0%] coverage) from unmeasured ones — no implicit coverage leakage | 2 |
| Highest-leverage change is architectural (capability/output boundary), argued by blast-radius removal vs. rate reduction | 2 |
| ≥3 sources cited for mechanisms | (prerequisite: no points without it) |

Common failure modes: proposing "stronger system prompt" as the fix
(section 3.2 is the whole counterargument); treating tool results as
model outputs; letting the spotlighting interval silently cover
channels it never measured.

---

## Exercise 13.2 — pricing the defense claims

### (a) What "under 2%" can and cannot mean

2 successes in 100 attempts: Wilson 95% = **[0.6%, 7.0%]**. The claim
"under 2%" is true of the point estimate only; the interval says the
true rate (under *this attack set*) is plausibly as high as 7.0%. What
the number *can* mean: "the observed rate under the audit's attacker
is 2%, bounded to at most 7.0% at 95% confidence." What it *cannot*
mean: "injection succeeds under 2% of the time" — full stop — because
(1) the interval's upper bound is 3.5x the headline, and (2) the
attack set is the audit's, not an adaptive adversary's (Ch. 12's
audit-attacker-is-a-lower-bound rule [SRC-PAPER-048's discipline]).
The honest sentence: "bounded ≤ 7.0% (Wilson 95% upper) under the
audited attack set; adaptive attackers unmeasured."

### (b) The adaptive follow-up audit

The attacker that must be included: *optimized* injection —
GCG-style suffix attacks are universal and transferable against
aligned models [SRC-PAPER-004], which is precisely the adversary a
delimiter marking scheme must survive (the marking is a prompt-level
transformation; section 3.2's second reason applies). The
preregistered stopping rule, decided in advance: run adaptive
attempts one at a time; **the first adaptive success rejects any
"≤ 2%" claim** (one success in one trial → Wilson [20.7%, 100%]; the
lower bound alone excludes 2%); a clean run stops at 300 failures
(0.98^300 ≈ 0.2% — even under a true 2% rate, 300 consecutive
failures would be a 0.002-probability event, so the clean outcome
supports "bounded below the claim's edge *under this attacker*,"
publishing the Wilson upper bound, never "injection-proof"). The rule
separates "bounded under adaptive attack *so far*" from "failed" on
the first success, and it never allows the vendor's next sentence to
be "we survived" — only "not yet failed at this budget" (Ch. 12's
section 6 discipline).

### (c) The paired evaluation for the hierarchy-fine-tune claim

The claim [SRC-PAPER-052's shape]: "our instruction-hierarchy
fine-tune beats the base model on injection robustness including
unseen attacks." Falsifiable design:

- **Arms**: fine-tuned model vs base model, *same prompts, same attack
  set, same decoding parameters* — paired per attempt.
- **Attack set**: preregistered in two strata — seen-style attacks
  (the training distribution's neighborhood) and held-out attack
  *types* (the "unseen" claim's actual test — the strata are the
  point; evaluating only on seen-style attacks tests memorization,
  not the hierarchy).
- **Denominators**: explicit per stratum (e.g., 200 attempts per arm
  per stratum; every rate reports k/n).
- **Interval rule**: the fine-tune "beats" base only if the
  fine-tuned interval's *upper* bound sits below the base interval's
  *lower* bound (the two-interval separation rule); a paired
  discordant-pair analysis (McNemar-style, Ch. 12 §4) decides
  borderline cases with the exact sign test.
- **Non-claims**: one attack family (injection; not jailbreak-generic
  robustness); one attacker implementation; adaptive optimization
  attacks included at a *stated* query budget only (the GCG condition
  [SRC-PAPER-004]); capability degradation measured separately and
  reported alongside (the hierarchy paper's own "minimal degradation"
  framing is a co-outcome, not a footnote).

### (d) The computed verdicts

**Delimiter marking vs base (2/100 vs 52/100).** Marked model:
**[0.6%, 7.0%]**; base model: **[42.3%, 61.5%]**. The intervals are
disjoint with a wide gap (upper of the defended arm is 45 points
below the lower of the base) — the reduction is decisive *under the
audit's attack set*, and the honest annotation is (a)'s sentence.

**Hierarchy fine-tune vs base, paired (8/200 vs 31/200).** Fine-tuned:
**[2.0%, 7.7%]**; base: **[11.1%, 21.2%]** — disjoint intervals, so
the two-interval rule alone settles "beats" at these denominators.
The paired reading (state it anyway, per (c)): 23-point gap in
successes on 200 paired attempts → expected discordant imbalance
b − c ≈ 23; at any plausible discordant total (b + c ≥ 39, e.g.,
b = 31, c = 8: exact one-sided sign-test p = 1.5e-4), the difference
is not noise. Verdict: claim *supported under the audit's conditions*
— published with the (c) non-claims attached, especially the
adaptive-budget caveat: the fine-tune's interval is measured against
the audit's attacker at the audit's budget, and optimized-suffix
pressure at 10x budget is the explicitly unmeasured cell
[SRC-PAPER-004].

### Assessor rubric (10 points)

| Criterion | Points |
|---|---|
| (a): the interval computed ([0.6%, 7.0%]) and the can/cannot split stated in publishable sentences | 2 |
| (b): adaptive attacker named with the optimized-suffix citation; stopping rule with the 0.98^n arithmetic in the correct direction; "not yet failed" framing | 3 |
| (c): paired design with attack-strata (seen/unseen), interval-separation rule, and the non-claims including the adaptive-budget caveat | 3 |
| (d): both verdicts computed correctly ([0.6, 7.0] vs [42.3, 61.5]; [2.0, 7.7] vs [11.1, 21.2]) with the paired discordant check | 2 |

Common failure modes: accepting "under 2%" as an interval statement
(the headline is a point estimate); designing the hierarchy evaluation
without the unseen-attack stratum (which tests the actual claim);
forgetting that a two-interval verdict is still attack-set-relative —
the adaptive caveat is not optional boilerplate, it is the claim's
honest scope.
