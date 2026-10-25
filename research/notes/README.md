# Research notes

Paper notes — methodological analyses of the register's sources, each
anchored to a [source-register](../source-register.yaml) entry and
written at the level the register's access supports (method-level for
full-text-read sources; abstract-level entries say so, per the
[paper-note template](../../templates/paper-note.md)'s rule).

| # | Note | Source | Level |
|---|---|---|---|
| 01 | [AI Control: Improving Safety Despite Intentional Subversion](01-ai-control.md) | SRC-PAPER-022 | method-level (full-text-read) |
| 02 | [Refusal in Language Models Is Mediated by a Single Direction](02-refusal-single-direction.md) | SRC-PAPER-037 | method-level (full-text-read) |
| 03 | [Scaling Monosemanticity](03-scaling-monosemanticity.md) | SRC-PAPER-032 | method-level (full-text-read) |
| 04 | [Sleeper Agents](04-sleeper-agents.md) | SRC-PAPER-019 | abstract-level |
| 05 | [Carlini & Wagner: Towards Evaluating the Robustness of Neural Networks](05-carlini-wagner-robustness.md) | SRC-PAPER-044 | abstract-level |
| 06 | [Greshake: Indirect Prompt Injection](06-greshake-indirect-injection.md) | SRC-PAPER-050 | abstract-level |
| 07 | [Croce & Hein: Reliable Evaluation of Adversarial Robustness](07-croce-hein-reliable-evaluation.md) | SRC-PAPER-047 | abstract-level |
| 08 | [Spotlighting](08-spotlighting.md) | SRC-PAPER-053 | abstract-level |
| 09 | [The Instruction Hierarchy](09-instruction-hierarchy.md) | SRC-PAPER-052 | abstract-level |
| 10 | [Weak-to-Strong Generalization](10-weak-to-strong.md) | SRC-PAPER-013 | abstract-level |
| 11 | [Language Models (Mostly) Know What They Know](11-models-know-what-they-know.md) | SRC-PAPER-016 | abstract-level |
| 12 | [Alignment Faking in Large Language Models](12-alignment-faking.md) | SRC-PAPER-020 | abstract-level |
| 13 | [BadNets](13-badnets.md) | SRC-PAPER-042 | abstract-level |
| 14 | [Stealing Machine Learning Models via Prediction APIs](14-model-extraction.md) | SRC-PAPER-043 | abstract-level |
| 15 | [Membership Inference Attacks](15-membership-inference.md) | SRC-PAPER-041 | abstract-level |
| 16 | [Faithfulness vs. Plausibility](16-faithfulness-vs-plausibility.md) | SRC-PAPER-034 | abstract-level (position paper) |
| 17 | [A Mathematical Framework for Transformer Circuits](17-transformer-circuits-framework.md) | SRC-PAPER-025 | method-level (full-text-read) |
| 18 | [Towards Monosemanticity](18-towards-monosemanticity.md) | SRC-PAPER-030 | method-level (full-text-read) |
| 19 | [Wild Patterns: Ten Years of Adversarial ML](19-wild-patterns-survey.md) | SRC-PAPER-049 | abstract-level |
| 20 | [Madry et al.: Adversarial Training](20-madry-adversarial-training.md) | SRC-PAPER-045 | abstract-level |
| 21 | [CaMeL: Defeating Prompt Injections by Design](21-camel-defeating-injections-by-design.md) | SRC-PAPER-054 | abstract-level |
| 22 | [AgentDojo: Dynamic Evaluation of Agent Attacks and Defenses](22-agentdojo-dynamic-evaluation.md) | SRC-PAPER-055 | abstract-level |
| 23 | [AI Sandbagging: Strategic Underperformance on Evaluations](23-ai-sandbagging.md) | SRC-PAPER-021 | abstract-level |
| 24 | [Explore, Establish, Exploit: Red Teaming from Scratch](24-explore-establish-exploit.md) | SRC-PAPER-060 | abstract-level |
| 25 | [DPO: the reparameterization that deleted the reward model](25-dpo-reparameterization.md) | SRC-PAPER-010 | abstract-level |
| 26 | [InstructGPT: the pipeline that made helpful a target](26-instructgpt-pipeline.md) | SRC-PAPER-009 | abstract-level |

**Build target met: 20/20 notes** (7 method-level from full-text-read
sources, 13 abstract-level honestly labeled — including one
position-paper-form entry). Every note carries: the actual problem,
method, central evidence with non-claims, tested-vs-inherited
assumptions, limitations (authors' and the note-author's), nearest
alternatives, replication feasibility at course scale, a falsifiable
extension with stopping rule, and interpretation kept separate from
the sources' claims.

## Comparison notes

Five planned (see `planning/content-matrix.yaml`); each compares at
the register's access level, exactly like paper notes.

| # | Note | Sources | Level |
|---|---|---|---|
| C01 | [RLHF vs DPO vs RLAIF](comparison-01-rlhf-vs-dpo-vs-rlaif.md) | SRC-PAPER-009/010/011/012 | abstract-read (all four) |
| C02 | [Behavioral vs mechanistic evidence](comparison-02-behavioral-vs-mechanistic-evidence.md) | SRC-PAPER-019/020/025/030/032/034/037 | mixed (2 abstract-read, 1 abstract position, 4 full-text-read) |
| C03 | [Alignment vs control](comparison-03-alignment-vs-control.md) | SRC-PAPER-006/008/010/011/013/019/020/022/023/024/054 | mixed (1 full-text-read, 10 abstract-read) |
| C04 | [Prompt defenses vs authorization boundaries](comparison-04-prompt-defenses-vs-authorization-boundaries.md) | SRC-PAPER-004/050/052/053/054; SRC-REPORT-004/005/006/007 | mixed (5 abstract-read, 4 page-inspected) |
| C05 | [Static benchmarks vs adaptive evaluation](comparison-05-static-benchmarks-vs-adaptive-evaluation.md) | SRC-PAPER-004/045/046/047/048/055/056/058/059/061 | abstract-read (all ten) |
