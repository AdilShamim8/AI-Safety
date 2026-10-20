# Red teaming: overview

Red teaming is the disciplined search for failures — adversarial,
creative, and adversarially-creative. For LLM systems it covers model
jailbreaks, [prompt injection](../risks/prompt_injection.md), multi-turn
manipulation, agent sandbox escapes, privacy extraction, and
product-level abuse (what can a hostile user *make your product do*).

The term comes from Cold War-era adversarial testing (red vs. blue
teams), but modern AI red-teaming practice descends more directly from
Microsoft's and IBM's adversarial-ML programs (Microsoft's AI Red Team
formalized "breaking AI before deployment" with their published
framework: "Lessons Learned on AI Red Teaming," Microsoft, 2023? — the
canonical industry writeup) and Anthropic's red-team effort (Ganguli et
al., "Red Teaming Language Models to Reduce Harms," arXiv:2202.01296).

## What red teaming is *not*

- **Not a pass/fail gate.** Any system with a human adversary is
  eventually exploitable; red teaming *finds and ranks* problems, it
  doesn't certify absence.
- **Not fuzzing.** Random mutation finds shallow bugs; LLM failures are
  semantic. The attacker loop is *intelligent optimization* — you are
  simulating an adversary with compute, not noise.
- **Not one discipline.** Model red-teaming (weights/API only) vs.
  system red-teaming (full product: retrieval, tools, UI, humans) vs.
  pipeline red-teaming (fine-tuning supply chain) are different scopes
  with different teams.

## The evidence it produced (why vendors pay for it)

- Ganguli et al. (arXiv:2202.01296): human red-teamers + model-generated
  attacks measurably reduced harmful output rates — the empirical case
  that red-team data *trains* safety.
- Zou et al. (arXiv:2307.15043): automated optimization (GCG) finds
  suffix attacks invisible to humans — the case for *automated* red
  teaming.
- Chao et al. (arXiv:2310.08419, PAIR): attacker-LLM red teaming needs
  ~20 queries/attack — the case for cheap automated loops.
- Russinovich et al. (arXiv:2404.06469, Crescendo): multi-turn drift
  defeats single-turn defenses — the case for conversation-level
  testing.
- Perez et al. (arXiv:2212.09251): *model-written* evaluations
  discovered sycophancy — the case for letting models propose the
  attacks humans wouldn't think of.

## Organizational patterns that work

1. **Separate adversarial incentives.** Red teamers report outside the
   feature-delivery org, or engagement rules guarantee "found = fixed or
   risk-accepted-in-writing."
2. **Time-box and scope.** Like pentests: defined surfaces, defined
   time, defined reporting — otherwise it's infinite.
3. **Automate the loop, human the novel.** Fuzz with PAIR/GCG-class
   tooling; spend human hours on the *new* attack categories (tools,
   multi-agent, modality tricks).
4. **Persist artifacts.** Every finding becomes a regression test in the
   eval suite (this repo's philosophy: `benchmarks/` + findings logged as
   structured records).
5. **Coordinated disclosure for anything transferable.** If your finding
   affects other vendors' products (a universal jailbreak, an
   architecture-level injection), disclose to them first — the norm
   established by the GCG and many-shot papers (days-to-weeks lead time,
   patched-then-published). Anthropic's many-shot paper
   (arXiv:2405.18678) and the refusal-direction work
   (arXiv:2406.11717) both followed this pattern.

## Standard methodology references

- Microsoft AI Red Team framework (Perrig et al.? — the 2023 "Lessons
  Learned" writeup; now the ML Commons / AILuminate adversarial-testing
  guidance lineage)
- NIST AI 600-1 §"adversarial testing" (the GenAI Profile's take)
- OpenAI's "red teaming network" publication practice
- The EU AI Act's systemic-risk adversarial-testing duty (Art. 55-era
  obligations — red teaming as *law*, not practice)

Next: [methodologies.md](methodologies.md) — the actual playbook.
