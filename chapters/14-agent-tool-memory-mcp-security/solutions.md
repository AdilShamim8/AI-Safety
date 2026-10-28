# Chapter 14 — Solutions and assessor rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module); every design states its non-claims.

---

## Exercise 14.1 — completing the Atlas audit

**The deployment (from the worked example).** Atlas: four MCP servers,
eleven tools, persistent memory, external mail arriving routinely.
New: a fifth server (CRM) with `crm.search`, `crm.update`,
`crm.export`.

### (a) The three CRM rows and the changed matrix

| Tool | Credential / scope | Objects reachable | Untrusted input feeds | Blast radius if hijacked |
|---|---|---|---|---|
| `crm.search` | CRM tenant, read | customer records | args from S | privacy: record enumeration at query scale |
| `crm.update` | CRM tenant, read+write on assigned records | customer fields | args from S | **data integrity**: edits persist and are later *read by honest flows* — poisoned-well persistence |
| `crm.export` | CRM tenant, bulk read + **egress** | CSV of any queryable record set | args from S (query, destination) | **mass disclosure**: whole-tenant exfiltration in one call; irreversible once delivered |

Which existing rows change:

- **The exfiltration pair widens from 3×1 to 4×2.** Entry channels
  that put attacker content or attacker-influenced queries into S
  (`mail.read`, `files.read`, `web.fetch`, and now `crm.search`
  results when records were attacker-editable upstream) exit
  channels that move data out under real credentials (`mail.send`
  and now `crm.export` to any destination). Counting pairs: before
  the CRM server, 3 entry tools × 1 irreversible-egress tool = 3
  pairs; after, 4 × 2 = **8 pairs** — an attack-surface doubling
  that no single tool review reveals, and exactly why the matrix,
  not the tool list, is the audit artifact.
- **`crm.update` changes the *meaning* of every read row.** A
  hijacked model that cannot exfiltrate directly can edit a customer
  record (" billing contact: analyst@attacker.example") and let a
  *later, honest* automated export deliver it. Blast radius is not
  what a tool reads or writes in one call; it is what it can leave
  behind for other tools to read. Row 8 (`files.write`) acquires
  the same property for `files.read` flows.

### (b) The R-rules for the CRM rows

- **R2 (argument integrity) applies to:** `crm.export`'s
  *destination* argument (it selects where data goes — a capability
  reference exactly like `mail.send`'s `recipient`); `crm.search`'s
  and `crm.export`'s *query* arguments insofar as they select
  *which* objects a read capability is exercised over (a `W`-tagged
  query string can still be data — but a `W`-tagged *destination*
  or *record selector* that a `W`-source chose must be consent-
  screened); `crm.update`'s *record id* and *field* arguments (they
  select which object the write capability touches — a `W`-tagged
  field name that reaches a webhook or email-sync field is a
  capability pivot). The *value* argument of `crm.update` may carry
  `W`-tagged data under R1's rules for what that field can later
  reach.
- **R1 (exfiltration) applies to:** `crm.export` — it is now an
  irreversible-egress tool alongside `mail.send`; any `U`-tagged
  record contents require per-destination consent this session, and
  a first-use authorization surface under R4.
- **R3 (memory provenance):** unchanged in form, but the CRM adds a
  second slow store — the CRM records themselves. A memory-poisoning
  analysis that audits only the agent's `memory.write` store misses
  that `crm.update` writes a store the *organization* reads; provenance
  tags on CRM edits (who/what chose this value) are the same
  discipline at the data-system layer.

### (c) Auditing "read-only mode"

For the claim to be *true*, "read-only" must be a property of the
**credential scope**: the OAuth token or service account the CRM
server holds must lack write scopes at the API level (a token whose
grants are `records:read`, no write endpoints reachable even if the
server code tries). That is an enforcement fact about the *auth
layer*, verifiable by inspecting the token's scopes and testing a
write attempt against the API directly.

What it degenerates to if enforced only at the **description
level**: the server ships a tool description reading "this tool is
read-only" — which is untrusted text by the protocol's own security
principle ("descriptions of tool behavior such as annotations should
be considered untrusted, unless obtained from a trusted server")
[SRC-REPORT-005], and the tool-poisoning demonstration shows
descriptions concealing behavior that contradicts their visible
benign part [SRC-REPORT-006]. A description-level promise is
marketing rendered into the model's context; a hijacked or
malicious server calls the write endpoint its token still reaches.
The audit question is always: *what does the credential allow?* —
never *what does the text say the credential allows?*

### (d) Residual-risk statement, fourteen tools under R1–R4

> Under R1–R4 with provenance-at-write on both stores, the
> exfiltration pairs (8 of them) are blocked at the edge for
> `U`-tagged flows and consent-gated for `W`-influenced capability
> arguments; residual risk concentrates in (i) consent decay — R4
> screens clicked through until the gate is ornamental; (ii) the
> authored-policy gap — any tool argument that is a capability
> reference in disguise and is not yet in R2's list; and (iii)
> slow-store poisoning via `crm.update`/`files.write` edits that
> alter what *later honest* flows disclose. The first channel a red
> team should probe is the `crm.search` → `crm.update` →
> `crm.export` *chain*: it exercises (iii) while every individual
> call is policy-clean — the artifact that catches it is the matrix
> read column-wise (which tools write stores other tools read),
> plus edit-provenance audit on the CRM records themselves.

Assessor rubric: full credit requires (a) the 8-pair count with the
pair-multiplication logic shown, (b) `destination`/`field`/`record
id` named as capability references with the R2 reasoning, (c) the
credential-vs-description distinction stated in exactly those terms
with both sources cited, and (d) the slow-store chain named as the
first probe with the matrix cross-read named as the catching
artifact. Deduct for any "the model should notice" reasoning — the
chapter's whole point is that nothing in this audit relies on the
model noticing anything.

---

## Exercise 14.2 — pricing a "provably secure" claim

### (a) The 7-point utility gap, recomputed

The vendor's "matching the published 77% vs 84%" is a claim about
point estimates. At the published benchmark's scale (AgentDojo's 97
tasks [SRC-PAPER-055]; CaMeL's abstract-level numbers
[SRC-PAPER-054]), treating 77% ≈ 75/97 and 84% ≈ 81/97:

- CaMeL arm: Wilson 95% **[68.0%, 84.5%]**
- Undefended arm: Wilson 95% **[74.9%, 89.6%]**
- The intervals overlap on **[76.0%, 84.5%]** — a wide band.

What can be concluded: the point estimates differ by 7 tasks; the
difference is *not statistically resolved from zero* at n = 97 (a
two-proportion comparison at these denominators does not clear
significance). What cannot be concluded: that the utility cost *is*
7 points (the true cost could plausibly range from ≈ 0 to ≈ 16
points at this resolution), or that the cost transfers to any other
task distribution. The honest form: "at benchmark scale, the
capability layer's utility cost is not yet distinguishable from
zero; the security property is architectural and does not depend on
this comparison." The vendor's sentence inverts the epistemics —
it uses the point estimate as the constant and ignores that the
*security* claim needs no statistic while the *utility* claim needs
a better one.

### (b) What sampling adds when the defense is a proof

"No exfiltration in 10,000 attempts" is the wrong genre of statement
for what the proof covers, and the right genre for what it does not:

- **Redundant under the proof:** whether attacks *that route data
  through unauthorized flows* succeed. If the implementation matches
  the policy, they cannot — running 10,000 of them measures the
  pseudorandom number generator, not the defense. (If one succeeds,
  the finding is an *implementation bug* — the proof's premises are
  violated somewhere — which is precisely information the sampling
  does add: proofs cover designs, deployments run code.)
- **What sampling still adds:** (i) *implementation fidelity* — the
  gap between the policy as specified and the code as executed (the
  10,000 attempts are a fuzz test of the enforcement layer);
  (ii) *policy coverage* — which flows the policy *permits* that the
  operator did not intend to permit (sampling with an attacker who
  reads the policy and aims at permitted edges: consent-decay under
  R4, click-through, capability-reference arguments not yet in
  R2's list); (iii) *completeness of the artifact itself* — whether
  the matrix (Section 4.1) from which the policy was derived
  enumerated all tools and channels.

The audit design: **artifact** — the privilege and trust-boundary
matrix, committed and versioned, as the coverage claim (every row
and every edge is either policy-governed or named as residual);
**attacker model** — an adaptive red team that receives the *policy*
and the matrix and is scored on finding *permitted* harmful flows,
not just blocked ones (the reward structure must not pay for
re-proving the proof); **stopping rule** — decided in advance:
"first successful exfiltration through a policy-permitted edge
closes the audit and reopens the policy" (a disconfirming event,
Ch. 02 discipline), with "no findings in N attempts" reported as an
interval on the *attempted* attack set only ([0%, 0.038%] at
0/10,000, Wilson) — never as a world-rate claim.

### (c) What a provable-flow guarantee subsumes for memory

Subsumed (if the capability layer genuinely mediates every tool
call, including `memory.read`'s re-entry into planning): **R1 and
R2's mechanics** — a `W`-tagged memory record cannot select
capability arguments and its `U`-tagged contents cannot reach
egress tools without per-destination consent. Not subsumed:

- **Dormancy** — the guarantee is per-flow, not per-time; a dormant
  instruction that fires when the *user* later consents to a
  plausible-looking destination is a policy-permitted flow
  exploiting consent decay, not a flow violation.
- **Provenance-at-write (R3's hard half)** — the guarantee tags data
  it carries; it cannot retroactively tag a store whose records were
  written before the layer existed. The write-time discipline is
  irrecoverable after the fact (Section 6's memory row).
- **Consent decay (R4's human half)** — proofs do not govern humans;
  a guarantee "covers" memory only down to the consent screen, and
  the screen is the softest component in the system.

### (d) The 23.9% figure, priced

At the source's own denominator (144 curated test cases
[SRC-PAPER-056]; 23.9% ≈ 34/144): Wilson 95% **[17.4%, 31.2%]**.
Required caption, one sentence:

> "On a curated benchmark of 144 high-stakes test cases, the safest
> evaluated agent still failed severely 23.9% of the time
> (evaluator-judged; Wilson 95% [17.4%, 31.2%]) — a statement about
> benchmark-elicited, judge-scored failures, not about incident
> rates among deployed agents."

Assessor rubric: full credit requires (a) both intervals, the
overlap stated, and the "point estimate as constant" critique
named; (b) the proof/sampling distinction split into
design-vs-implementation, and a red team rewarded for *permitted*
flows with a pre-declared stopping rule; (c) all three residual
mechanisms (dormancy, provenance-at-write, consent decay) named
with the subsumption boundary drawn at the consent screen; (d) the
interval plus a caption that carries the benchmark provenance and
the judge-scored qualifier. Deduct for any multiplication of 23.9%
by 68.8% into a deployed-incidence number — the 68.8% is the
emulator's *validity* rate over identified failures
[SRC-PAPER-056], not a prevalence factor, and its own denominator
is not stated in the abstract.

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **DeepMind course**, [part-02-06-safer-design-patterns](../../courses/google-deepmind-agi-safety/part-02-06-safer-design-patterns.md) — watch before working the privilege-boundary exercises.
