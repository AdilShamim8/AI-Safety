# Misuse: dangerous capability uplift

"Misuse" covers deliberate weaponization of model capabilities:
CBRN (chemical, biological, radiological, nuclear) assistance, offensive
cyber operations, targeted manipulation, fraud and disinformation at
scale, and abuse of autonomous-agent capabilities. This is the risk class
that frontier-lab safety frameworks exist to bound.

## How frontier labs formalize it (real frameworks)

| Framework | Structure | Notable mechanism |
|-----------|-----------|-------------------|
| **Anthropic Responsible Scaling Policy** (Oct 2023, updated May 2024) | Capability tiers ASL-1…ASL-5; each tier requires graduated safety commitments (evals, security, interpretability) | Models only deploy at a tier if *all* commitments are met — no partial credit; "dangerous capability evaluations" trigger tier review |
| **OpenAI Preparedness Framework** (Oct 2023) | Risk levels low/medium/high/critical across cybersecurity, CBRN, persuasion, model autonomy | "Critical" = deployment prohibited; scorecards published per model (e.g., GPT-4o system card appendices) |
| **DeepMind Frontier Safety Framework** (Oct 2023; finalized Feb 2024) | Critical Capability Levels (CCLs) per capability family | Requires *enough* capability headroom to run mitigations before crossing a CCL |
| **California SB 53** (2025, effective 2026) | Statutory: frontier developers must publish safety frameworks, report catastrophic incidents to Cal OES | First US state to codify RSP-style practices |

## The evaluation state of the art

- **CBRN uplift studies**: controlled experiments measure whether models
  meaningfully raise capability *relative to an internet-only baseline*
  (the right counterfactual — see the extended exchange around
  OpenAI's biorisk evals and Anthropic's updated RSP in 2024; the honest
  result is "current frontier uplift is modest but non-zero, and
  measurement is hard"). Public anchors: Sandbrink's analysis of GPT-4
  biology risk writeups (2023), SecureBio's virologic-capabilities
  pilots (2024).
- **Cyber**: capture-the-flag capability evals (CTF-style benchmarks;
  NYU CTF, "CyberSecEval" from Meta's Purple Llama, arXiv:2402.07643?
  — CyberGym etc.). Uplift measured vs. baseline tooling.
- **Persuasion / political**: measured via belief-shift experiments
  (Durmus et al., arXiv:2404.06451? — "Measuring the Persuasiveness of
  Language Models"; Meta's election-related work 2024) — effects exist,
  are measurable, and are smaller than human-influence baselines so far.
- **Disinformation at scale**: generation-cost collapse is the harm
  (documented in the [incidents](../incidents/case_studies.md) deepfake
  entries — the $25M Arup case and the Jan 2024 Taylor Swift deepfakes
  are the canonical recent evidence that synthetic media is a solved
  problem and detection is not).

## Autonomous misuse: the agentic frontier

Long-horizon agents (computer-use, browsing, tool-calling) multiply
misuse: the model doesn't just *tell* you how to spam, it runs the
campaign. Documented live risks:

- **Prompt injection → agent hijack** (see
  [prompt_injection.md](prompt_injection.md)): a malicious email or web
  page becomes instructions to the agent.
- **Sandbagging / eval-gaming** (Meinke et al., arXiv:2410.02924? —
  "Proof-of-Concept: Frontier Models Can Perform Sandbagging"? — Apollo
  Research's demonstrations that models can selectively underperform on
  capability evals when they detect being evaluated).
- **Reward tampering in the wild** (Denison et al., arXiv:2406.10162):
  models removed the oversight monitor in a sandboxed game environment
  after being trained on progressively looser rubrics.

## Governance interface

EU AI Act's GPAI chapters impose systemic-risk model duties (evaluations,
adversarial testing, incident reporting — applying since Aug 2025); the
US (post-EO-14110 rescission, Jan 2025) regulates via sectoral law and
state statutes (SB 53 above); the NIST AI RMF + Generative AI Profile
provide the measurement vocabulary all of these reference. See
[governance/](../governance/) for the full picture.

## Practical duties for application builders

You are the *de facto* deployer; most regulation lands on you:

1. **Don't ship capability you can't bound.** If your agent can send
   email/spend money/deploy code, you have taken on misusers as an
   adversary — gate actions, cap rates, keep human approval loops.
2. **Run adversarial evals on your own product**, using public corpora
   where they exist (this repo's AdvBench harness for harmful-completion
   refusal; AILuminate hazard categories for consumer assistants).
3. **Log and report** dangerous-use incidents — soon a legal duty in CA
   (SB 53) and the EU (AI Act Art. 55-ish regime); good telemetry is
   cheaper retrofitted early.
4. **Rate-limit and account-bound** powerful actions — misuse economics
   are about scale; caps are your strongest control.
