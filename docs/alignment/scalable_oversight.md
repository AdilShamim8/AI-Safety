# Scalable oversight

Scalable oversight asks: **how do you supervise an AI that can produce
outputs you cannot competently evaluate?** The question predates LLMs — it
is the fourth of the *Concrete Problems* (arXiv:1606.06565) — and becomes
sharper as models match or exceed expert ability in coding, research math,
and long-horizon research tasks (METR's time-horizon results, 2024–2025).

## The canonical approaches

### Debate (Irving, Christiano, Amodei — arXiv:1805.00899)

Two AI debaters each see the question and argue opposing positions; a
human judges the transcript. The claim: adversarial pressure surfaces the
strongest evidence against each answer, letting a weaker judge extract the
truth from stronger debaters — "truth wins" when cross-examination forces
concessions. Empirical follow-ups (Michael et al., arXiv:2306.11701,
"Debate Helps Supervise Experts"; OpenAI's debate transcripts site) found
debate beats consultancy (single advisor) on hard reading-comprehension
judgments, with the effect shrinking as judge-skill rises. Limitation:
collusion between debaters and dishonest-but-persuasive strategies remain
open problems (Barnes et al. on obfuscated arguments, arXiv:2306.11701
discussion).

### Iterated amplification (Christiano, Shlegeris, Amodei — arXiv:1810.08575)

Decompose a hard question into easier sub-questions answerable by weaker
copies of the system, then compose the answers. If humans can supervise
each decomposition step, oversight scales recursively. Imitated
amplification was demonstrated on algorithmic tasks; the practical issue
is **factored-cognition overhead** — decomposition often costs more
capability than it buys oversight.

### Recursive reward modeling (Leike et al. — arXiv:1811.07871)

Chain the reward-model idea: agents learn rewards from users, and agent
helpers assist users in evaluating the next generation. This is,
implicitly, how frontier labs deploy tool-use: today's assistants already
draft evaluation rubrics and grader code used on tomorrow's models.

### Weak-to-strong generalization (Burns et al. — arXiv:2312.09390)

OpenAI's superalignment pivot: train a *strong* model using only a *weak*
supervisor's labels. Empirically, strong students initialized from weak
labels generalize *beyond* the supervisor on NLP tasks — but a "weak-to-
strong" gap remains on chess/NLP-style reasoning and collapses to
supervisor-capped performance when the strong model imitates the
supervisor's quirks. Co-authors showed naive prompting ("be better than
your teacher") recovers some of the gap.

## The honest state of the art

- None of these is *proven* to scale. They are existence proofs that
  oversight is *sometimes* easier than task performance.
- The best current practical hybrid: **generative evals + verifier
  ensembling + interpretability checks** — combine model-written tests,
  executable checkers (RLVR-style), and anomaly probes, and treat
  disagreement as a review trigger.
- For agentic systems the live problem is **oversight during long
  rollouts**: behavior policies, step-level approval gates, and tripwires
  (see the repo's guardrail pipeline, `src/aisafety/safety/guardrails/`).

## Practical takeaways for today's deployments

1. You don't need to solve superhuman oversight to benefit: rubric-based
   LLM grading with human spot-checks (as used in real eval pipelines from
   AlpacaEval to Anthropic's model cards) is already "weak-to-strong" in
   miniature.
2. Prefer **checkable outputs**. Restrict agents to domains with
   executable verifiers (tests, compilers, math checkers) where
   verification asymmetry works in your favor.
3. Log everything an agent did, not just final answers. Transcript-level
   review is the difference between oversight and hope.
