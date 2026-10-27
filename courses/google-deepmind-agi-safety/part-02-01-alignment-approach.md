# Part 2.1 — The alignment approach: what 'aligned' is supposed to mean

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 1. Alignment approach](https://www.youtube.com/watch?v=RGh8wP9PjJw) (3:44) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

Part 2's opening move: define the target before
presenting the mechanisms. The course's framing — aligning the model's
objectives and behavior with human intentions and values, such that
the system remains corrigible, honest, and safe even as capabilities
grow.

## Core ideas, explained

### 1. The definitional gauntlet

"Alignment" is famously contested — instruction-following? preference
satisfaction? value learning? corrigibility? The course's compressed
move is to treat alignment as a *design target with properties*
(honest, corrigible, bounded in impact) rather than a philosophical
essence. That is the same move the repo makes in
[Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md):
operationalize the goal into measurable properties, because an
undefined target cannot be trained toward or evaluated against.

### 2. Corrigibility as the hinge property

The load-bearing property in most working definitions is corrigibility
— the system remains open to correction, does not resist shutdown or
modification. It is the property instrumental convergence attacks
first (self-preservation serves every goal), which is why it sits at
the hinge between Part 1's risk model and Part 2's mechanisms. The
off-switch-game literature in the repo's notes (the CIRL/assistance-games
line) is the formal treatment.

### 3. Why a stack, not a switch

The part sets up Part 2's remaining videos as a *portfolio*: oversight,
robustness, control, interpretability, design. No single mechanism is
presented as sufficient — each covers a failure surface the others
miss. The repo's architecture (five interpretability-plus-oversight
chapters, adversarial chapters, control chapter) is that portfolio at
course depth.

## Through-line to this repository's chapters

- [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) —
  operationalizing the alignment target.
- [research/notes/62-cirl-assistance-games.md](../../research/notes/62-cirl-assistance-games.md)
  and [research/notes/63-off-switch-game.md](../../research/notes/63-off-switch-game.md) —
  corrigibility's formal core.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
