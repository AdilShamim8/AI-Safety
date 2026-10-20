# Constitutional AI: harmlessness from AI feedback

Constitutional AI (Bai et al., arXiv:2212.08073, Anthropic, Dec 2022) is
the production alternative to human-labeled harmlessness preferences:
write down the model's principles (a *constitution*), have the model revise
its own responses against them, then train a preference model on the
revisions — **RLAIF**, RL from AI feedback. Claude's harmlessness training
has used this family of methods since before public release.

## The two-stage recipe

**Stage 1 — Supervised learning on self-revisions.**

1. Sample harmful responses from an initial model (via a "red team" prompt
   distribution).
2. Ask the model to critique its own response against a constitution
   principle: *"Identify specific ways in which the assistant's last
   response is harmful, unethical, racist, sexist, toxic, dangerous, or
   illegal."*
3. Ask it to rewrite the response fixing those issues.
4. SFT on the (prompt, revision) pairs.

**Stage 2 — RLAIF preference learning.**

Generate pairs (original response, revised response), label preferences
*using the constitution*: the model itself judges which response a
principle would prefer, chain-of-thought style. Train an RM on these AI
labels, then run PPO against it. The result: harmlessness that approaches
human-feedback quality at a fraction of the labeling cost, and — the key
finding — far less evasive "I can't do that" refusals, because principles
specify *what to do instead* rather than just prohibiting.

## What constitutions actually look like

Anthropic's published Claude constitution (blog: "Claude's Constitution",
May 2023) drew on:

- the **UN Universal Declaration of Human Rights** (dignity, equal rights),
- **DeepMind's Sparrow rules** (be helpful, honest, harmless; stay in
  role; no stereotyping),
- **Apple's terms of service** style rules on avoiding illegal activity,
- trust & safety best practices, and
- **non-Western and collective-value** principles (e.g., "Choose the
  response that is most respectful of cultural traditions").

Typical published principles (quoted from the arXiv paper's appendix):
*"Please choose the response that is most supportive of life, liberty, and
personal security"*; *"Choose the response that is most respectful of the
right to privacy"*; *"Please choose the response that the least likely to
be seen as toxic or harmful."

## Why it matters

| Property | RLHF-only | Constitutional / RLAIF |
|----------|-----------|--------------------------|
| Label cost at scale | Expensive humans | Cheap model-generated |
| Label consistency | Noisy across raters | Consistent with written principles (auditable!) |
| Transparency | Rater guidelines are internal | Constitution is a reviewable artifact |
| New hazard discovered | Re-label with humans | Amend principle, regenerate |
| Failure mode | Rater bias ingestion | Constitutional blind spots; sycophancy toward principles |

The auditability point is underrated: a constitution is *diff*-able.
When a behavior is wrong, you can point at the principle that caused it,
argue about it, and change it — impossible with preferences locked inside
a reward model.

## Known limitations

- **Constitutions encode choices.** Whose values, which trade-offs — the
  paper itself notes Western/professional skew in early drafts, motivating
  the non-Western principles added later.
- **Self-critique inherits model blind spots.** A model that can't see the
  harm won't revise it away (relevant to [deceptive alignment](../risks/deceptive_alignment.md)).
- **RLAIF can be reward-hacked** like any learned signal; the paper
  reports the same overoptimization caveats as RLHF.
- **It is not alignment for dangerous capabilities.** Constitutions steer
  *expressed behavior*; they do not by themselves remove latent
  capabilities (see Anthropic's Responsible Scaling Policy for the
  capability side).

## Where to read more

- Constitutional AI: Bai et al., arXiv:2212.08073
- "Claude's Constitution" (Anthropic blog, May 2023)
- RLAIF scaling analysis: "RLAIF vs. RLHF" (Lee et al., arXiv:2309.00267)
- Open implementation of principle-driven critique loops in
  `ConstitutionalAI` hooks of `trl` and AllenAI's `open-instruct`
