# A short history of AI safety

Safety concerns are as old as AI itself; the institutional apparatus is
recent. This page highlights events with primary sources.

## 1950s–1970s: the questions are asked

- **1950** — Turing's *Computing Machinery and Intelligence* asks how we
  would recognize machine intelligence, and notes the "argument from
  various disabilities" (machines will never do X) has historically failed.
- **1956** — Dartmouth workshop coins "artificial intelligence."
- **1960** — Wiener's *Some Moral and Technical Consequences of Automation*
  (Science, 131:1355) warns that we "had better be quite sure that the
  purpose put into the machine is the purpose which we really desire" —
  the alignment problem, stated 60+ years early.
- **1975** — Asilomar Conference on Recombinant DNA establishes the
  template for proactive, self-imposed research guidelines; AI borrows the
  playbook in 2017 (see below).

## 1980s–2014: foundations

- **1985** — Michie's elementary percepts on "human-compatible" machine
  intelligence.
- **2000s–2010s** — MIRI (formerly Singularity Institute, founded 2000) and
  FHI (Future of Humanity Institute, Oxford, 2005) develop formal
  treatments: Omohundro's basic AI drives (2008), Bostrom's *Superintelligence*
  (2014) popularizes instrumental convergence and orthogonality.
- **2011** — SIAI→MIRI shift toward "Friendly AI" math (corrigibility,
  Vingean uncertainty, tiling agents).

## 2016–2020: modern technical safety

- **2016** — *Concrete Problems in AI Safety* (arXiv:1606.06565; Amodei,
  Olah, Steinhardt, Christiano, Schulman, Mané) gives the field its working
  agenda. DeepMind founds its safety team; OpenAI follows.
- **2017** — Asilomar AI Principles signed by 1,200+ researchers; AI safety
  becomes a session topic at AAAI. "Alignment" enters the mainstream
  lexicon.
- **2017** — Deep RL from human preferences (arXiv:1706.03741; Christano et
  al.) proves preference learning can replace hand-written rewards.
- **2018** — AI Safety Gridworlds (arXiv:1711.09883) ships tests for
  specification gaming and safe exploration; AI Safety via Debate
  (arXiv:1805.00899) proposes scalable oversight.
- **2019** — Russell's *Human Compatible* reframes everything around
  uncertainty over human preferences (CIRL/assistance games).
- **2020** — GPT-3 (arXiv:2005.14165) makes alignment practical: the
  Stochastic Parrots paper (arXiv:2106.15031? — published FAccT 2021,
  Bender, Gebru et al.) documents its risks.

## 2021–2023: the LLM safety era

- **2021–2022** — InstructGPT (arXiv:2203.02155) demonstrates RLHF at
  scale: a 1.3B model preferred by humans over 175B GPT-3. Anthropic
  publishes Constitutional AI (arXiv:2212.08073) and the HH-RLHF dataset
  (arXiv:2204.05862).
- **2022, Nov 30** — ChatGPT ships RLHF safety training to 100M users in
  two months, and with it, jailbreaking becomes a mass hobby (DAN prompts).
- **2023, Mar–May** — The "godfather exits": Hinton leaves Google; the
  Center for AI Safety's one-sentence statement ("Mitigating the risk of
  extinction from AI should be a global priority alongside pandemics and
  nuclear war") is signed by Hinton, Bengio, Altman, Hassabis, and hundreds
  of senior researchers.
- **2023, Jul–Nov** — Frontier labs publish voluntary safety frameworks:
  Anthropic's Responsible Scaling Policy (Oct 2023), OpenAI's Preparedness
  Framework (Oct 2023), DeepMind's Frontier Safety Framework. The UK hosts
  the Bletchley Park AI Safety Summit (Nov 1–2): 28 countries + EU sign
  the Bletchley Declaration; the UK and US announce AI Safety Institutes.

## 2024–present: institutionalization

- **2024** — EU AI Act (Regulation 2024/1689) enters into force Aug 1.
  The Seoul Summit (May) collects signed frontier-safety commitments from
  16 companies. Anthropic's *sleeper agents* (arXiv:2401.05566) and
  *many-shot jailbreaking* (arXiv:2405.18678) show safety training is
  brittle under adversarial pressure. Scaling Monosemanticity
  (Anthropic, 2024) extracts millions of interpretable features from
  Claude 3 Sonnet and demos activation steering on a production model
  (Golden Gate Claude).
- **2025** — International AI Safety Report (chaired by Bengio) publishes
  ahead of the Paris AI Action Summit (Feb); the EU's GPAI obligations
  begin applying (Aug 2, 2025); California's SB 53 frontier-AI
  transparency law is signed (Sept 2025, effective 2026).

The trend line: from philosophical warnings → to research agendas → to
voluntary frameworks → to binding regulation with the field's research
output (benchmarks, interpretability, red-teaming) increasingly serving as
the *measurement infrastructure* compliance depends on.
