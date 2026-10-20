# DPO: Direct Preference Optimization

DPO (Rafailov et al., arXiv:2305.18290, NeurIPS 2023) reframed alignment as
a classification problem, eliminating the reward model and PPO loop
entirely. It is now the default alignment recipe for open-weight models —
Llama 3's post-training, Mistral's instruct variants, and Zephyr
(arXiv:2310.16944) all use DPO-style objectives, and open preference
datasets (UltraFeedback, arXiv:2310.01377; Argilla's distilabel sets) made
it reproducible outside big labs.

## The insight

The reward model in RLHF is only ever used *through the policy
optimization*. DPO derives the change of variables that skips it: for the
 Bradley–Terry preference model with an RLHF-style KL-constrained optimum,
the optimal policy `π*` induces a reward `r(x,y) = β log(π*(y|x)/π_ref(y|x)) + const`.
Substituting into the preference loss gives a direct objective on policies:

```text
L_DPO = −E[ log σ( β log (π_θ(y_w|x)/π_ref(y_w|x))
                   − β log (π_θ(y_l|x)/π_ref(y_l|x)) ) ]
```

where `(y_w, y_l)` are the preferred/rejected pair. Intuition: raise the
log-ratio of the chosen response, lower the rejected one, relative to the
reference (usually the SFT checkpoint). `β` plays the KL-penalty role.

## Why practitioners adopted it

| Property | RLHF (PPO) | DPO |
|----------|-----------|-----|
| Components | SFT + RM + PPO rollout infra + reward baseline | SFT + one loss |
| Stability | Reward hacking, hyperparameter-sensitive | Remarkably stable |
| Compute | High (online rollouts during training) | Low (offline preference pairs) |
| Ceiling (at frontier) | Higher in head-to-head studies | Comparable on standard chat evals; slightly behind at the very top |
| Overfitting risk | Reward-model overoptimization | Memorizing preference pairs; needs β & label-quality care |

## The variant zoo (all real, all cited)

- **IPO** (Azar et al., arXiv:2310.12036) — fixes DPO's unbounded
  preference-ratio problem with a squared, bounded loss.
- **KTO** (Ethayarajh et al., arXiv:2402.01306) — models Kahneman-Tversky
  prospect theory; needs only binary good/bad signals (no pairs), matching
  production thumbs-up/down data.
- **ORPO** (Hong et al., arXiv:2403.07691) — folds the preference
  objective into SFT, removing the reference model.
- **SimPO** (Meng et al., arXiv:2405.14734) — length-normalized implicit
  reward; strong MT-Bench results without a reference model.
- **cDPO / rDPO** — noise-robust DPO variants handling corrupted labels
  (Mitchell, arXiv:2311.08145 analyzes label noise).

## Practical guidance

1. **DPO inherits its data's biases.** Preference pairs scraped or
   model-graded (e.g., UltraFeedback's GPT-4 grading) import the grader's
   blind spots; document your grader.
2. **Watch length and verbosity** — chosen responses are usually longer,
   and DPO will happily learn "longer = better." Length-controlled evals
   (e.g., AlpacaEval LC, arXiv:2405.03535) exist precisely for this.
3. **β is your only KL knob.** Too high: nothing changes. Too low: policy
   drifts, output diversity collapses. Typical published values: 0.01–0.3.
4. **DPO does not fix safety by itself.** On public safety preference sets
   (PKU-Alignment/BeaverTails, arXiv:2307.04657) it reduces harmful
   responses substantially, but the resulting refusals are as
   jailbreak-removable as RLHF's (see [risks/jailbreaks.md](../risks/jailbreaks.md)).
5. **Consider iterative DPO** (rounds of sampling + filtering) when you
   can't afford PPO but want some on-policy flavor (e.g., SPIN, arXiv:2401.01335).

## Where to read more

- DPO: Rafailov et al., arXiv:2305.18290; code in `huggingface/trl`
- Zephyr: Tunstall et al., arXiv:2310.16944 (DPO on UltraFeedback)
- KTO: Ethayarajh et al., arXiv:2402.01306
- A survey of DPO-family methods: Wang et al., arXiv:2403.03683? — see
  "Insights into Alignment" (Rafailov et al., arXiv:2402.19403)
