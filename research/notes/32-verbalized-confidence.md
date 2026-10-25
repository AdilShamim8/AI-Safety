# Note: Verbalized confidence — the channel the model can be taught to fake (2022)

Source: SRC-PAPER-017 · Access: **abstract-read** (arXiv page,
verified with the chapter-06 build) · Note level: **abstract-level**.

## The actual problem

Logit-based confidence comes for free with the architecture; VERBALIZED
confidence ("I'm 80% sure") is what users actually see. The paper's
question: can models express calibrated uncertainty in words, and —
the load-bearing half — what is that expression actually connected to?

## Method (as the abstract establishes it)

Fine-tuning models to verbalize calibrated confidence on factual
claims, then measuring whether the stated probabilities match the
empirical frequencies — with the sharpest finding this course records:
fine-tuned verbalized confidence can be BETTER calibrated than the
model's own logits (the statement "I'm 70% sure" out-predicts the
0.7 logit). That inversion is the paper's surprise and its caution in
one number.

## Results (abstract-level, honestly priced)

Calibrated verbalization is trainable and can exceed logit
calibration — as the abstract states. What it does not give: the
arena/subjective-question extension, the persuasion-pressure results,
and the failure modes under distribution shift. The course's chapter
06 prices the abstract-level conclusion as the SPOOFABLE channel:
verbalized confidence is an output the model was TRAINED to produce,
which means preference pressure (sycophancy — note 28) and
social-engineering pressure train it just as well as accuracy does.

## What this note does NOT claim

No claim that verbalized confidence is useless — the paper's result is
real and user-facing calibration matters. The note's boundary: the
result establishes trainability, not trustworthiness under adversarial
or pressure conditions, which is exactly the gap chapter 06's worked
example audits.

## Falsifiable extension

The unexamined interaction: verbalized confidence meets sycophancy
pressure. If a model verbalizes "70% sure" and the user pushes back
("are you really sure?"), what happens to the stated number? Design at
the deterministic tier: P04's preference organism with a
confidence-verbalization head (a second readout trained to predict
correctness probability), then apply the preference stream WITH and
WITHOUT pushback on incorrect answers. Stopping rule: if stated
confidence rises under pushback while correctness stays flat, the
verbalized channel inherits the preference pipeline's pressure —
trainable calibration and trained flattery in the same head, which is
the chapter's thesis made mechanical; if stated confidence holds under
pressure, the channel is more than a trained output, and the "spoofable"
label needs a boundary the course must record.

## My interpretation vs. their claims

Their claim: models can be taught to verbalize well-calibrated
uncertainty, sometimes better than their logits. My reading: correct,
and the finding CUTS BOTH WAYS — better-than-logit calibration proves
the verbal channel is a learned behavior with its own training
surface, so whoever controls the fine-tuning controls the displayed
confidence. The chapter-06 architecture (logit channel / P(True)
channel / verbal channel, each with its spoofing condition) is the
curriculum-shaped answer to this one paper, and the honest deployment
line is: verbalized confidence is a UI feature until its training
pressure history is auditable — then, and only then, is it evidence.
