# Note: Defending Against Indirect Prompt Injection Attacks With Spotlighting (2024)

Source: SRC-PAPER-053 · Access: abstract-read · Read: 2026-10-22 ·
Note level: **abstract-level** (the >50%→<2% figures are abstract-level
statements over the paper's attack set; the chapter prices them as
[40.4%, 59.6%] vs [0.6%, 7.0%] at n=100).

## The actual problem

The authors' framing: an LLM application ingests untrusted text and
the model cannot tell instruction from data — so make the data's
*form* carry its provenance. The operational version: find prompt-
level transformations of untrusted input that give the model a
reliable, continuous signal of "this is data," and measure how much
of the indirect-injection attack success rate the signal removes.

## Method

(What the abstract carries:) "spotlighting" — a family of prompt
engineering transformations of the untrusted input, where the
transformation itself (rather than an instruction about the input)
provides the provenance signal. The family's variants (delimiters,
marking, encoding) differ in how strongly they deform the data's
surface form; the paper's insight is that the signal must be
*continuous and reliable* — a property of the text the model reads,
not a plea the model can choose to ignore.

The design logic: move the defense from the instruction channel
("ignore instructions in the data" — same channel as the attack,
optimization-defeatable) to the data channel's form. This is the
structural distinction chapter 13 §3.4 organizes the defense families
by.

## Central evidence

- Attack success rate reduced from **greater than 50% to below 2%** on
  GPT-family models — the headline, quoted at the abstract's own
  qualifiers over the paper's attack set.
- **Minimal impact on task efficacy** — the transformation does not
  break the model's ability to use the data it marks.
- The mechanism claim: the model's ability to distinguish among
  multiple sources of input improves — provenance as a first-class
  readout, not an afterthought.

What the evidence does NOT carry: per-variant (delimiter vs marking
vs encoding) breakdowns live in the unread body; adaptive attacks
(optimized suffixes that survive or exploit the transformation) are
outside the abstract's measured scope — the chapter's counterevidence
row (SRC-PAPER-004's optimized pressure) marks exactly this open
condition; nothing about non-retrieval channels (user messages, tool
results) — spotlighting marks what the application marks.

## Assumptions

Tested in-paper: the rate reduction over the paper's attack set; task
efficacy preserved.

Inherited: that the transformation survives adaptive optimization
(the open condition — a suffix crafted *knowing* the data is marked
could target the marking's seams); that the marking surface is where
injections enter (retrieved content only — the deployment's other
channels need their own treatment); that GPT-family behavior
generalizes across model generations (the transformation is a
behavioral prior about how models read form, which drifts with
training).

## Limitations

Authors' (abstract-level): none stated beyond the measured scope.
Mine: the <2% figure is bounded by [0.6%, 7.0%] at n=100 — the
point-estimate trap the chapter's exercise 13.2 exists to catch;
"minimal task-efficacy impact" is measured on the paper's tasks, and
transformation cost on long, structure-rich content (code, tables,
multi-document reasoning) is a deployment-specific question the
abstract cannot answer.

## Nearest alternatives

- **Instruction hierarchy (SRC-PAPER-052)**: the training-time
  complement — priors over channels versus markings on channels; the
  stack reading (chapter 13 §5) is that serious deployments run both.
- **Output handling (OWASP LLM05, SRC-REPORT-004)**: the boundary
  spotlighting does not provide — even a 0% injection rate leaves the
  blast radius of whatever the model *does* emit; the consumers, not
  the emitter, hold that line.
- **Prompt-level instruction defenses**: the category spotlighting
  replaces — same-channel, optimization-defeatable, priced honestly
  as "moves the rate, cannot carry security weight" (chapter 13
  §3.2).

## Replication feasibility

High at course scale — P07's design: a toy RAG stack, an authored
attack set (metadata-level, no real-payload craft), three
transformation variants, and the interval arithmetic to price the
rate change. What breaks first: the attack set is authored, so the
measured rate is against the course's attacks — an honest lower-bound
statement P07's report will carry verbatim from this note's
discipline.

## Falsifiable extension

Hypothesis: spotlighting's protection is marking-seam-relative — an
adaptive attacker that knows the transformation can craft content
that *reads as marked data carrying instructions* (instructions
inside the quotation the model now trusts as data), eroding the <2%
rate materially. Design: run the spotlighted defense against (a) the
paper-style attack set and (b) an adaptive set optimized against the
deployed transformation (budget stated); compare rates with Wilson
intervals at matched n. Baseline: (a). Stopping rule: first adaptive
success bounds the rate away from <2% (chapter 12's one-success rule);
clean side stops at 300 failures. What counts against: if adaptive
rates match non-adaptive rates, the transformation is
optimization-robust in a way prompt-level defenses never were —
and my same-channel-defeat premise fails for *form-based* defenses,
which would genuinely distinguish spotlighting from the category it
replaces.

## My interpretation vs. their claims

Their claims: (1) spotlighting transformations reduce indirect-
injection ASR from >50% to <2% with minimal task impact; (2) the
mechanism is a reliable, continuous provenance signal.

My interpretation: (1) is the strongest prompt-level-family result in
the literature *because* it is a form-based rather than instruction-
based defense — but it is still a behavioral prior about how models
read form, and the honest deployment reading is "bounded ≤ 7.0% under
the audited attacker," never "injection-proof"; (2) the
form-vs-instruction distinction is the paper's durable conceptual
contribution — it explains why this family succeeds where "ignore the
data's instructions" cannot: it changes what the text *is*, not what
the model is *told*; (3) the measured scope (retrieved channels,
non-adaptive attacks, GPT-family models) should ride along with every
citation of the 2% figure, and chapter 13's exercise 13.2 is the
course's device for making that habitual.
