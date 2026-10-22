# P03 experiment report: calibration-three-instruments-v1

Run ID: `calibration-three-instruments-v1` · Project: P03 · Status: implemented (synthetic fixture with scripted instruments — the measurement discipline is the deliverable; the ml compute tier with a licensed dataset and local model is marked honestly in the project README) · Date: 2026-10-22

Split: 30 validation / 30 evaluation items (round-robin by case order — even validation, odd evaluation; calibrators fit on validation only and frozen before evaluation).

## Pair: `well-calibrated-v1` under `identity`

Calibration map (frozen before evaluation): identity (no parameters; validation accuracy 0.4667)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 4 | 0.026 | 0.000 | [0.000, 0.490] | -0.026 |
| [0.2, 0.3) | 1 | 0.294 | 0.000 | [0.000, 0.793] | -0.294 |
| [0.3, 0.4) | 2 | 0.332 | 0.000 | [0.000, 0.658] | -0.332 |
| [0.4, 0.5) | 4 | 0.457 | 0.500 | [0.150, 0.850] | +0.043 |
| [0.5, 0.6) | 8 | 0.534 | 0.625 | [0.306, 0.863] | +0.091 |
| [0.7, 0.8) | 5 | 0.746 | 1.000 | [0.566, 1.000] | +0.254 |
| [0.8, 0.9) | 1 | 0.891 | 1.000 | [0.207, 1.000] | +0.109 |
| [0.9, 1.0) | 5 | 0.992 | 1.000 | [0.566, 1.000] | +0.008 |

ECE = 0.1127 at K = 10 (bin counts: 4, 1, 2, 4, 8, 5, 1, 5) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.1189 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.3678 (clipped at 1e-15)
- Mean gap: -0.0419 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1308 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0307 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 19 | 63.3% | 3 | 0.1579 | 2 | 6.7% |
| 0.70 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |
| 0.90 | 5 | 16.7% | 0 | 0.0000 | 13 | 43.3% |

## Pair: `well-calibrated-v1` under `platt`

Calibration map (frozen before evaluation): platt: sigmoid(14.1901 * s + -6.6787) (Newton, 100 iterations, |params| <= 25.0)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 6 | 0.030 | 0.000 | [0.000, 0.390] | -0.030 |
| [0.1, 0.2) | 1 | 0.149 | 0.000 | [0.000, 0.793] | -0.149 |
| [0.2, 0.3) | 1 | 0.291 | 0.000 | [0.000, 0.793] | -0.291 |
| [0.4, 0.5) | 1 | 0.487 | 1.000 | [0.207, 1.000] | +0.513 |
| [0.5, 0.6) | 2 | 0.519 | 0.500 | [0.095, 0.905] | -0.019 |
| [0.6, 0.7) | 4 | 0.632 | 0.750 | [0.301, 0.954] | +0.118 |
| [0.7, 0.8) | 4 | 0.777 | 0.500 | [0.150, 0.850] | -0.277 |
| [0.9, 1.0) | 11 | 0.990 | 1.000 | [0.741, 1.000] | +0.010 |

ECE = 0.0954 at K = 10 (bin counts: 6, 1, 1, 1, 2, 4, 4, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.0968 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2862 (clipped at 1e-15)
- Mean gap: 0.0226 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1308 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0307 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 21 | 70.0% | 4 | 0.1905 | 1 | 3.3% |
| 0.70 | 15 | 50.0% | 2 | 0.1333 | 5 | 16.7% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Pair: `well-calibrated-v1` under `histogram`

Calibration map (frozen before evaluation): histogram: K=5 bin accuracies (0.000, 0.000, 0.667, 1.000, 1.000); empty-bin fallback 0.4667

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 7 | 0.000 | 0.000 | [0.000, 0.354] | +0.000 |
| [0.6, 0.7) | 12 | 0.667 | 0.583 | [0.320, 0.807] | -0.083 |
| [0.9, 1.0) | 11 | 1.000 | 1.000 | [0.741, 1.000] | +0.000 |

ECE = 0.0333 at K = 10 (bin counts: 7, 12, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.1000 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2777 (clipped at 1e-15)
- Mean gap: 0.0333 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1132 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0131 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 23 | 76.7% | 5 | 0.2174 | 0 | 0.0% |
| 0.70 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Pair: `overconfident-v1` under `identity`

Calibration map (frozen before evaluation): identity (no parameters; validation accuracy 0.4667)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.4, 0.5) | 4 | 0.416 | 0.000 | [0.000, 0.490] | -0.416 |
| [0.5, 0.6) | 2 | 0.583 | 0.000 | [0.000, 0.658] | -0.583 |
| [0.6, 0.7) | 5 | 0.661 | 0.400 | [0.118, 0.769] | -0.261 |
| [0.7, 0.8) | 8 | 0.720 | 0.625 | [0.306, 0.863] | -0.095 |
| [0.8, 0.9) | 5 | 0.848 | 1.000 | [0.566, 1.000] | +0.152 |
| [0.9, 1.0) | 6 | 0.985 | 1.000 | [0.610, 1.000] | +0.015 |

ECE = 0.1915 at K = 10 (bin counts: 4, 2, 5, 8, 5, 6) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.1637 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.4736 (clipped at 1e-15)
- Mean gap: 0.1349 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1308 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0307 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 26 | 86.7% | 8 | 0.3077 | 0 | 0.0% |
| 0.70 | 19 | 63.3% | 3 | 0.1579 | 2 | 6.7% |
| 0.90 | 6 | 20.0% | 0 | 0.0000 | 12 | 40.0% |

## Pair: `overconfident-v1` under `platt`

Calibration map (frozen before evaluation): platt: sigmoid(23.6313 * s + -16.1202) (Newton, 100 iterations, |params| <= 25.0)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 6 | 0.031 | 0.000 | [0.000, 0.390] | -0.031 |
| [0.1, 0.2) | 1 | 0.151 | 0.000 | [0.000, 0.793] | -0.151 |
| [0.2, 0.3) | 1 | 0.294 | 0.000 | [0.000, 0.793] | -0.294 |
| [0.4, 0.5) | 1 | 0.487 | 1.000 | [0.207, 1.000] | +0.513 |
| [0.5, 0.6) | 2 | 0.520 | 0.500 | [0.095, 0.905] | -0.020 |
| [0.6, 0.7) | 4 | 0.634 | 0.750 | [0.301, 0.954] | +0.116 |
| [0.7, 0.8) | 3 | 0.770 | 0.667 | [0.208, 0.939] | -0.103 |
| [0.8, 0.9) | 1 | 0.801 | 0.000 | [0.000, 0.793] | -0.801 |
| [0.9, 1.0) | 11 | 0.990 | 1.000 | [0.741, 1.000] | +0.010 |

ECE = 0.0954 at K = 10 (bin counts: 6, 1, 1, 1, 2, 4, 3, 1, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.0968 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2864 (clipped at 1e-15)
- Mean gap: 0.0230 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1308 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0307 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 21 | 70.0% | 4 | 0.1905 | 1 | 3.3% |
| 0.70 | 15 | 50.0% | 2 | 0.1333 | 5 | 16.7% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Pair: `overconfident-v1` under `histogram`

Calibration map (frozen before evaluation): histogram: K=5 bin accuracies (0.467, 0.467, 0.000, 0.556, 1.000); empty-bin fallback 0.4667

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 6 | 0.000 | 0.000 | [0.000, 0.390] | +0.000 |
| [0.5, 0.6) | 13 | 0.556 | 0.538 | [0.291, 0.768] | -0.017 |
| [0.9, 1.0) | 11 | 1.000 | 1.000 | [0.741, 1.000] | +0.000 |

ECE = 0.0074 at K = 10 (bin counts: 6, 13, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.1078 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2993 (clipped at 1e-15)
- Mean gap: 0.0074 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1147 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0146 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 24 | 80.0% | 6 | 0.2500 | 0 | 0.0% |
| 0.70 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Pair: `inverted-v1` under `identity`

Calibration map (frozen before evaluation): identity (no parameters; validation accuracy 0.4667)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 5 | 0.008 | 1.000 | [0.566, 1.000] | +0.992 |
| [0.1, 0.2) | 1 | 0.109 | 1.000 | [0.207, 1.000] | +0.891 |
| [0.2, 0.3) | 5 | 0.254 | 1.000 | [0.566, 1.000] | +0.746 |
| [0.4, 0.5) | 7 | 0.461 | 0.714 | [0.359, 0.918] | +0.253 |
| [0.5, 0.6) | 5 | 0.535 | 0.400 | [0.118, 0.769] | -0.135 |
| [0.6, 0.7) | 2 | 0.669 | 0.000 | [0.000, 0.658] | -0.669 |
| [0.7, 0.8) | 1 | 0.706 | 0.000 | [0.000, 0.793] | -0.706 |
| [0.9, 1.0) | 4 | 0.974 | 0.000 | [0.000, 0.490] | -0.974 |

ECE = 0.5989 at K = 10 (bin counts: 5, 1, 5, 7, 5, 2, 1, 4) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.5609 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 6.9324 (clipped at 1e-15)
- Mean gap: -0.1581 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.7178 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.6178 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 12 | 40.0% | 10 | 0.8333 | 16 | 53.3% |
| 0.70 | 5 | 16.7% | 5 | 1.0000 | 18 | 60.0% |
| 0.90 | 4 | 13.3% | 4 | 1.0000 | 18 | 60.0% |

## Pair: `inverted-v1` under `platt`

Calibration map (frozen before evaluation): platt: sigmoid(-14.1901 * s + 7.5114) (Newton, 100 iterations, |params| <= 25.0)

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 6 | 0.030 | 0.000 | [0.000, 0.390] | -0.030 |
| [0.1, 0.2) | 1 | 0.149 | 0.000 | [0.000, 0.793] | -0.149 |
| [0.2, 0.3) | 1 | 0.291 | 0.000 | [0.000, 0.793] | -0.291 |
| [0.4, 0.5) | 1 | 0.487 | 1.000 | [0.207, 1.000] | +0.513 |
| [0.5, 0.6) | 2 | 0.519 | 0.500 | [0.095, 0.905] | -0.019 |
| [0.6, 0.7) | 4 | 0.632 | 0.750 | [0.301, 0.954] | +0.118 |
| [0.7, 0.8) | 4 | 0.777 | 0.500 | [0.150, 0.850] | -0.277 |
| [0.9, 1.0) | 11 | 0.990 | 1.000 | [0.741, 1.000] | +0.010 |

ECE = 0.0954 at K = 10 (bin counts: 6, 1, 1, 1, 2, 4, 4, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.0968 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2862 (clipped at 1e-15)
- Mean gap: 0.0226 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1308 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0307 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 21 | 70.0% | 4 | 0.1905 | 1 | 3.3% |
| 0.70 | 15 | 50.0% | 2 | 0.1333 | 5 | 16.7% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Pair: `inverted-v1` under `histogram`

Calibration map (frozen before evaluation): histogram: K=5 bin accuracies (1.000, 1.000, 0.667, 0.000, 0.000); empty-bin fallback 0.4667

### Reliability table (evaluation split)

Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%
interval on accuracy (z at full precision).

| bin | n | conf | acc | Wilson 95% | gap |
|---|---|---|---|---|---|
| [0.0, 0.1) | 7 | 0.000 | 0.000 | [0.000, 0.354] | +0.000 |
| [0.6, 0.7) | 12 | 0.667 | 0.583 | [0.320, 0.807] | -0.083 |
| [0.9, 1.0) | 11 | 1.000 | 1.000 | [0.741, 1.000] | +0.000 |

ECE = 0.0333 at K = 10 (bin counts: 7, 12, 11) — ECE is a binning artifact; the counts ride along.

### Proper scores and marginals (evaluation split)

- Brier: 0.1000 (proper score: punishes miscalibration and rewards discrimination)
- Log loss: 0.2777 (clipped at 1e-15)
- Mean gap: 0.0333 (marginal confidence − accuracy; NOT a calibration measure — bins cancel)

### Selective prediction (evaluation split)

- AURC: 0.1132 (mean selective risk over all coverage levels)
- Oracle AURC: 0.1001 (correct-first ceiling for this set)
- AURC gap: 0.0131 (ranking information the score failed to extract)
- Full-coverage risk: 0.4000 (answering everything)

| tau | answered | coverage | errors | selective risk | false abstentions | false-abstention rate |
|---|---|---|---|---|---|---|
| 0.50 | 23 | 76.7% | 5 | 0.2174 | 0 | 0.0% |
| 0.70 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |
| 0.90 | 11 | 36.7% | 0 | 0.0000 | 7 | 23.3% |

## Cross-pair comparison (the deployer's view)

| Instrument | Calibrator | Brier | Log loss | ECE | AURC | AURC gap | Full-coverage risk |
|---|---|---|---|---|---|---|---|
| well-calibrated-v1 | identity | 0.1189 | 0.3678 | 0.1127 | 0.1308 | 0.0307 | 0.4000 |
| well-calibrated-v1 | platt | 0.0968 | 0.2862 | 0.0954 | 0.1308 | 0.0307 | 0.4000 |
| well-calibrated-v1 | histogram | 0.1000 | 0.2777 | 0.0333 | 0.1132 | 0.0131 | 0.4000 |
| overconfident-v1 | identity | 0.1637 | 0.4736 | 0.1915 | 0.1308 | 0.0307 | 0.4000 |
| overconfident-v1 | platt | 0.0968 | 0.2864 | 0.0954 | 0.1308 | 0.0307 | 0.4000 |
| overconfident-v1 | histogram | 0.1078 | 0.2993 | 0.0074 | 0.1147 | 0.0146 | 0.4000 |
| inverted-v1 | identity | 0.5609 | 6.9324 | 0.5989 | 0.7178 | 0.6178 | 0.4000 |
| inverted-v1 | platt | 0.0968 | 0.2862 | 0.0954 | 0.1308 | 0.0307 | 0.4000 |
| inverted-v1 | histogram | 0.1000 | 0.2777 | 0.0333 | 0.1132 | 0.0131 | 0.4000 |

Reading rules: a calibrator earns its parameters only if it beats identity *on the evaluation split* (Brier/log loss); an AURC above the full-coverage risk means the gate is worse than answering everything (the inverted-signal signature); the AURC gap is the information the score failed to extract, not an error bar.

## Honest limitations

- The instruments are scripted confidence scores over synthetic items — the *measurement discipline* (splits, intervals, both ledger sides) is the deliverable; the numbers are properties of the authored fixture, not of any deployed model.
- Calibration maps are fit on a round-robin validation split of the same authored distribution; a deployment-grade fit needs an external calibration set, and the ml compute tier is where that lands (marked honestly in the project README).
- ECE is reported at the configured K only; sensitivity to K is a property of the binning, not the instrument (the metrics tests pin the K-dependence).
- Threshold operating points carry conditional rates whose denominators move with tau; the Wilson intervals ride along and small-n points are correspondingly wide.

## Provenance

| Field | Value |
|---|---|
| run id | `calibration-three-instruments-v1` |
| config SHA-256 | `3e8f8ecfc4995a1baefd2f710cdc7c0b41b7028fd50084ffeb54e656b1c90b6c` |
| case set | calibration-cases-v1 1.0.0 (`e9a61df198a66f24…`) |
| binning | K = 10 |
| split | round-robin by case order (even validation, odd evaluation) |
| code version | 0.1.0 |
| python | 3.12.15 |
| run date | 2026-10-22 |

Reproduce: `PYTHONPATH=src python -m ai_safety_course.calibration.runner <config.yaml>` — outputs are byte-stable for a fixed configuration.
