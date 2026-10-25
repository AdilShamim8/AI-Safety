"""P06 — causal interpretability: the activation-patching audit (offline analogue).

Chapter links: 09 (activation patching with explicit contrasts and controls),
10 (intervention beats reconstruction), 11 (probe readout is not causal
evidence). This module reproduces the DISCIPLINE of a causal
interpretability study on a deterministic two-branch "model organism" with
known ground truth, so that every number in the audit is explainable and
byte-stable:

    channels: a = noisy core signal   (sign agreement with label ~84%)
              b = clean spurious signal (90% agreement in-distribution)
              t = topic nuisance       (label-independent)
    sites:    s0 embedding -> s1 (a-branch) and s2 (b-branch) -> s3 mixer
              -> logistic readout fit on in-distribution activations

The fitted readout demonstrably leans on the CLEAN spurious channel more
than the noisy core channel — the shortcut-learning setup of Ch. 03/17.
The audit then answers a vendor-shaped claim — "the model's behavior
lives in the s2/b circuit" — with the three-instrument battery:

    C1  label-flip contrast   (flip the core channel, resample b consistent
                               with the new label; topic matched)
    C2  b-isolate contrast    (flip b only; core and topic untouched)
    I   deployment-flip intervention (b anti-correlates on a held-out
                               slice; neutral-ablate the b input)

plus the machinery that makes patching numbers mean anything at all:
random-patch and matched-magnitude controls, Wilson intervals on decision
restoration, exact one-sided binomial tests with Holm-Bonferroni
multiplicity correction over the site grid, and the trivial-site band
(s0 and s3 restore nearly everything precisely because they sit at the
ends of the information flow — Ch. 09's first lesson as code).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from random import Random

SITES = ("s0", "s1", "s2", "s3")
Z_95 = 1.96

# ---------------------------------------------------------------------------
# Model organism: hand-specified sparse weights (every path explainable).
# Channel slots in s0: 0 = a, 1 = b, 2 = topic, 3 = weak mixed.
# ---------------------------------------------------------------------------

_EMBED = (  # s0 = _EMBED @ (a_obs, b, t); slots 2/3 carry topic only
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 0.0, 0.3),
)
_A_BRANCH = (  # s1 = tanh(_A_BRANCH @ s0): slot 0 = a mass, 3% b leak
    (1.5, 0.03, 0.0, 0.0),
    (0.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.5, 0.0),
    (0.0, 0.0, 0.0, 0.5),
)
_B_BRANCH = (  # s2 = tanh(_B_BRANCH @ s0): slot 1 = b mass, 3% a leak
    (0.0, 0.0, 0.0, 0.0),
    (0.03, 1.5, 0.0, 0.0),
    (0.0, 0.0, 0.5, 0.0),
    (0.0, 0.0, 0.0, 0.5),
)
_MIX_A = (  # s3 = tanh(_MIX_A @ s1 + _MIX_B @ s2): slot 0 = a mass
    (1.5, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.5, 0.0),
    (0.0, 0.0, 0.0, 0.5),
)
_MIX_B = (  # slot 1 = b mass
    (0.0, 0.0, 0.0, 0.0),
    (0.0, 1.5, 0.0, 0.0),
    (0.0, 0.0, 0.5, 0.0),
    (0.0, 0.0, 0.0, 0.5),
)

SIGMA_A = 1.2  # observation noise on the core channel (~82% sign agreement)


def _matvec(m: tuple[tuple[float, ...], ...], v: tuple[float, ...]) -> list[float]:
    return [sum(row[j] * v[j] for j in range(len(v))) for row in m]


def _tanh(v: list[float]) -> list[float]:
    return [math.tanh(x) for x in v]


def _add(u: list[float], v: list[float]) -> list[float]:
    return [a + b for a, b in zip(u, v, strict=True)]


@dataclass(frozen=True)
class Example:
    """One input with ground truth. y is the label of the CLEAN a."""

    a_obs: float  # noisy observation of the core signal a in {-1, +1}
    b: float  # spurious signal in {-1, +1}
    t: float  # topic nuisance
    y: int  # ground-truth label = 1[a > 0]


@dataclass
class Acts:
    """Cached activations of one forward pass."""

    s0: list[float]
    s1: list[float]
    s2: list[float]
    s3: list[float]

    def at(self, site: str) -> list[float]:
        return getattr(self, site)


def forward(
    x: tuple[float, float, float],
    patch: tuple[str, list[float]] | None = None,
    ablate_b: bool = False,
) -> tuple[float, Acts]:
    """Forward pass; optionally substitute a donor activation at `patch[0]`
    or run with the b channel neutralized (the ablation intervention).
    Returns (s3 proxy scalar, full activation record)."""
    xin = (x[0], 0.0 if ablate_b else x[1], x[2])
    s0 = _matvec(_EMBED, xin)
    if patch and patch[0] == "s0":
        s0 = list(patch[1])
    s1 = _tanh(_matvec(_A_BRANCH, s0))
    if patch and patch[0] == "s1":
        s1 = list(patch[1])
    s2 = _tanh(_matvec(_B_BRANCH, s0))
    if patch and patch[0] == "s2":
        s2 = list(patch[1])
    s3 = _tanh(_add(_matvec(_MIX_A, s1), _matvec(_MIX_B, s2)))
    if patch and patch[0] == "s3":
        s3 = list(patch[1])
    return s3[0], Acts(s0=s0, s1=s1, s2=s2, s3=s3)


# ---------------------------------------------------------------------------
# Readout: ridge-regularized logistic regression on s3 (Newton, deterministic).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Readout:
    w: tuple[float, float, float, float]
    c: float

    def logit(self, acts: Acts) -> float:
        return (
            self.w[0] * acts.s3[0]
            + self.w[1] * acts.s3[1]
            + self.w[2] * acts.s3[2]
            + self.w[3] * acts.s3[3]
            + self.c
        )

    def decide(self, acts: Acts) -> int:
        return 1 if self.logit(acts) > 0.0 else 0


def _logistic(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def _newton_logistic(
    feats: list[list[float]], labels: list[float], ridge: float = 0.5, iters: int = 60
) -> list[float]:
    """Newton-Raphson logistic fit, zeros init, fixed iterations, Jacobi
    sweeps for the small solve: fully deterministic, no RNG anywhere."""
    dim = len(feats[0])
    beta = [0.0] * dim
    for _ in range(iters):
        grad = [ridge * b for b in beta]
        hess = [[0.0] * dim for _ in range(dim)]
        for i in range(dim):
            hess[i][i] += ridge
        for f, yv in zip(feats, labels, strict=True):
            p = _logistic(sum(b * fj for b, fj in zip(beta, f, strict=True)))
            r = p * (1.0 - p) + 1e-9
            for i in range(dim):
                grad[i] += (p - yv) * f[i]
                for j in range(dim):
                    hess[i][j] += r * f[i] * f[j]
        d = [0.0] * dim
        for _ in range(40):
            for i in range(dim):
                sig = hess[i][i]
                acc = grad[i] - sum(hess[i][j] * d[j] for j in range(dim) if j != i)
                d[i] = acc / sig if sig > 1e-12 else 0.0
        beta = [b - dd for b, dd in zip(beta, d, strict=True)]
    return beta


def fit_readout(data: list[Example]) -> Readout:
    """Fit the s3 readout on in-distribution data."""
    feats: list[list[float]] = []
    labels: list[float] = []
    for ex in data:
        _, acts = forward((ex.a_obs, ex.b, ex.t))
        feats.append([1.0, *acts.s3])
        labels.append(float(ex.y))
    beta = _newton_logistic(feats, labels)
    return Readout(w=tuple(beta[1:]), c=beta[0])


def probe_accuracy(site: str, data: list[Example]) -> float:
    """Linear-probe readout accuracy at a site (Ch. 11's cautionary
    instrument): the same logistic fit on that site's activations alone."""
    feats: list[list[float]] = []
    labels: list[float] = []
    for ex in data:
        _, acts = forward((ex.a_obs, ex.b, ex.t))
        feats.append([1.0, *acts.at(site)])
        labels.append(float(ex.y))
    beta = _newton_logistic(feats, labels)
    ok = sum(
        1
        for f, yv in zip(feats, labels, strict=True)
        if (1 if sum(b * fj for b, fj in zip(beta, f, strict=True)) > 0.0 else 0) == int(yv)
    )
    return ok / len(feats)


# ---------------------------------------------------------------------------
# Deterministic data slices and corruption contrasts.
# ---------------------------------------------------------------------------


def make_slice(seed: int, n: int, b_agreement: float, sigma_a: float = SIGMA_A) -> list[Example]:
    """One labeled slice. b_agreement = P(b agrees with the label sign);
    sigma_a = observation noise on the core channel."""
    rng = Random(seed)
    out: list[Example] = []
    for _ in range(n):
        y = rng.randint(0, 1)
        a = 1.0 if y == 1 else -1.0
        a_obs = a + rng.gauss(0.0, sigma_a)
        agree = rng.random() < b_agreement
        b = a if agree else -a
        t = rng.uniform(-1.0, 1.0)
        out.append(Example(a_obs=a_obs, b=b, t=t, y=y))
    return out


def corrupt(ex: Example, kind: str, seed: int) -> Example:
    """The two corruption contrasts of the audit. Both keep the topic
    matched (Ch. 09's matched-topic control baked into the protocol)."""
    rng = Random(seed)
    if kind == "label_flip":
        y2 = 1 - ex.y
        a2 = 1.0 if y2 == 1 else -1.0
        a_obs2 = a2 + rng.gauss(0.0, SIGMA_A)
        agree = rng.random() < 0.9
        b2 = a2 if agree else -a2
        return Example(a_obs=a_obs2, b=b2, t=ex.t, y=ex.y)
    if kind == "b_flip":
        return Example(a_obs=ex.a_obs, b=-ex.b, t=ex.t, y=ex.y)
    raise ValueError(f"unknown contrast {kind}")


# ---------------------------------------------------------------------------
# Statistics: Wilson, exact binomial, Holm, McNemar.
# ---------------------------------------------------------------------------


def wilson_interval(k: int, n: int, z: float = Z_95) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def exact_binom_one_sided(k: int, n: int, p0: float = 0.5) -> float:
    """P[X >= k] under Binomial(n, p0)."""
    if n == 0:
        return 1.0
    total = 0.0
    for i in range(k, n + 1):
        total += math.comb(n, i) * (p0**i) * ((1.0 - p0) ** (n - i))
    return min(1.0, total)


def holm(pvals: dict[str, float]) -> dict[str, float]:
    """Holm-Bonferroni step-down adjusted p-values, capped at 1."""
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, float] = {}
    running = 0.0
    for rank, (key, p) in enumerate(items):
        adj = (m - rank) * p
        running = max(running, adj)
        out[key] = min(1.0, running)
    return out


def mcnemar_exact_one_sided(b: int, c: int) -> float:
    """One-sided exact McNemar: P[X >= b] under Binomial(b+c, 0.5)."""
    return exact_binom_one_sided(b, b + c)


# ---------------------------------------------------------------------------
# The audit.
# ---------------------------------------------------------------------------


@dataclass
class SiteStat:
    site: str
    k: int  # decisions restored to clean among discordant pairs
    n: int  # discordant pairs
    gap_R: float  # mean logit-gap restoration fraction
    rate: float
    ci: tuple[float, float]
    p_raw: float
    p_holm: float


@dataclass
class ControlStat:
    site: str
    k: int  # decisions accidentally restored by the control patch
    n: int  # discordant pairs
    rate: float
    ci: tuple[float, float]


@dataclass
class PatchAuditResult:
    seed: int
    readout: Readout
    probe_s1: float
    probe_s2: float
    shortcut_learned: bool  # |w_b| > |w_a| at the readout
    heldout_acc: float
    heldout_ci: tuple[float, float]
    heldout_ablated_acc: float
    heldout_ablated_ci: tuple[float, float]
    flip_acc: float
    flip_ci: tuple[float, float]
    flip_ablated_acc: float
    flip_ablated_ci: tuple[float, float]
    flip_mcnemar_p: float
    flip_recovery_b: int  # discordant: wrong before, right after ablation
    flip_recovery_c: int  # discordant: right before, wrong after
    c1: dict[str, SiteStat] = field(default_factory=dict)
    c2: dict[str, SiteStat] = field(default_factory=dict)
    random_controls_c1: dict[str, ControlStat] = field(default_factory=dict)
    matched_controls_c1: dict[str, ControlStat] = field(default_factory=dict)


def _accuracy(readout: Readout, data: list[Example], ablate_b: bool = False) -> int:
    ok = 0
    for ex in data:
        _, acts = forward((ex.a_obs, ex.b, ex.t), ablate_b=ablate_b)
        if readout.decide(acts) == ex.y:
            ok += 1
    return ok


def _grid(readout: Readout, data: list[Example], kind: str, seed: int) -> dict[str, SiteStat]:
    """Run clean + corrupted + per-site patched passes; return per-site
    restoration stats with Holm-corrected exact binomial p-values."""
    per_site: dict[str, dict[str, list[float]]] = {s: {"gap": [], "restored": []} for s in SITES}
    for i, ex in enumerate(data):
        x = (ex.a_obs, ex.b, ex.t)
        _, clean_acts = forward(x)
        z_clean = readout.logit(clean_acts)
        d_clean = readout.decide(clean_acts)
        cx = corrupt(ex, kind, seed * 100_003 + i)
        _, corr_acts = forward((cx.a_obs, cx.b, cx.t))
        z_corr = readout.logit(corr_acts)
        d_corr = readout.decide(corr_acts)
        gap = z_clean - z_corr
        if d_clean == d_corr:
            continue  # discordant-set discipline (Ch. 02 paired ledger)
        for site in SITES:
            _, patched_acts = forward((cx.a_obs, cx.b, cx.t), patch=(site, clean_acts.at(site)))
            z_patch = readout.logit(patched_acts)
            if abs(gap) > 1e-12:
                per_site[site]["gap"].append((z_patch - z_corr) / gap)
            d_patch = readout.decide(patched_acts)
            per_site[site]["restored"].append(1.0 if d_patch == d_clean else 0.0)
    raw: dict[str, float] = {}
    stats: dict[str, SiteStat] = {}
    for site in SITES:
        gaps = per_site[site]["gap"]
        rest = per_site[site]["restored"]
        n = len(rest)
        k = int(sum(rest))
        rate = k / n if n else 0.0
        gap_r = sum(gaps) / len(gaps) if gaps else 0.0
        raw[site] = exact_binom_one_sided(k, n) if n >= 5 else 1.0
        stats[site] = SiteStat(
            site=site,
            k=k,
            n=n,
            gap_R=gap_r,
            rate=rate,
            ci=wilson_interval(k, n),
            p_raw=raw[site],
            p_holm=1.0,
        )
    adjusted = holm(raw)
    for site in SITES:
        stats[site].p_holm = adjusted[site]
    return stats


def _controls(
    readout: Readout, data: list[Example], seed: int
) -> tuple[dict[str, ControlStat], dict[str, ControlStat]]:
    """C1 controls in decision form: a random-patch and a matched-
    magnitude-noise patch per site. A control that restored decisions at
    the same rate as the clean-donor patch would void the patching
    evidence, so these are the audit's own falsifiers."""
    rng = Random(seed * 7 + 13)
    random_R: dict[str, list[int]] = {s: [] for s in SITES}
    matched_R: dict[str, list[int]] = {s: [] for s in SITES}
    for i, ex in enumerate(data):
        x = (ex.a_obs, ex.b, ex.t)
        _, clean_acts = forward(x)
        d_clean = readout.decide(clean_acts)
        cx = corrupt(ex, "label_flip", seed * 100_003 + i)
        _, corr_acts = forward((cx.a_obs, cx.b, cx.t))
        d_corr = readout.decide(corr_acts)
        if d_clean == d_corr:
            continue
        for site in SITES:
            dim = len(clean_acts.at(site))
            rand_vec = [rng.uniform(-1.0, 1.0) for _ in range(dim)]
            _, r_acts = forward((cx.a_obs, cx.b, cx.t), patch=(site, rand_vec))
            random_R[site].append(1 if readout.decide(r_acts) == d_clean else 0)
            delta = [c - o for c, o in zip(clean_acts.at(site), corr_acts.at(site), strict=True)]
            nrm = math.sqrt(sum(d * d for d in delta)) or 1e-9
            noise = [rng.gauss(0.0, 1.0) for _ in range(dim)]
            nn = math.sqrt(sum(v * v for v in noise)) or 1e-9
            matched_vec = [o + nrm * v / nn for o, v in zip(corr_acts.at(site), noise, strict=True)]
            _, m_acts = forward((cx.a_obs, cx.b, cx.t), patch=(site, matched_vec))
            matched_R[site].append(1 if readout.decide(m_acts) == d_clean else 0)
    rand_out = {}
    match_out = {}
    for s in SITES:
        for src, out in ((random_R, rand_out), (matched_R, match_out)):
            rest = src[s]
            n = len(rest)
            k = int(sum(rest))
            out[s] = ControlStat(
                site=s, k=k, n=n, rate=(k / n if n else 0.0), ci=wilson_interval(k, n)
            )
    return rand_out, match_out


def run_patch_audit(seed: int = 11) -> PatchAuditResult:
    """The full deterministic audit. Every number pinned in the tests is
    produced by this function with the default seed."""
    train = make_slice(seed * 31 + 1, 400, 0.9)
    heldout = make_slice(seed * 31 + 2, 200, 0.9)
    flip = make_slice(seed * 31 + 3, 200, 0.3)
    readout = fit_readout(train)

    probe_s1 = probe_accuracy("s1", heldout)
    probe_s2 = probe_accuracy("s2", heldout)

    h_ok = _accuracy(readout, heldout)
    h_ab_ok = _accuracy(readout, heldout, ablate_b=True)
    f_ok = _accuracy(readout, flip)
    f_ab_ok = _accuracy(readout, flip, ablate_b=True)

    # Paired ledger for the ablation recovery on the flip slice.
    b_cnt = 0  # wrong before, right after (recovery)
    c_cnt = 0  # right before, wrong after (cost)
    for ex in flip:
        _, acts_before = forward((ex.a_obs, ex.b, ex.t))
        _, acts_after = forward((ex.a_obs, ex.b, ex.t), ablate_b=True)
        before = readout.decide(acts_before) == ex.y
        after = readout.decide(acts_after) == ex.y
        if not before and after:
            b_cnt += 1
        elif before and not after:
            c_cnt += 1

    c1 = _grid(readout, heldout, "label_flip", seed)
    c2 = _grid(readout, heldout, "b_flip", seed)
    rand_c, match_c = _controls(readout, heldout, seed)

    return PatchAuditResult(
        seed=seed,
        readout=readout,
        probe_s1=probe_s1,
        probe_s2=probe_s2,
        shortcut_learned=abs(readout.w[1]) > abs(readout.w[0]),
        heldout_acc=h_ok / len(heldout),
        heldout_ci=wilson_interval(h_ok, len(heldout)),
        heldout_ablated_acc=h_ab_ok / len(heldout),
        heldout_ablated_ci=wilson_interval(h_ab_ok, len(heldout)),
        flip_acc=f_ok / len(flip),
        flip_ci=wilson_interval(f_ok, len(flip)),
        flip_ablated_acc=f_ab_ok / len(flip),
        flip_ablated_ci=wilson_interval(f_ab_ok, len(flip)),
        flip_mcnemar_p=mcnemar_exact_one_sided(b_cnt, c_cnt),
        flip_recovery_b=b_cnt,
        flip_recovery_c=c_cnt,
        c1=c1,
        c2=c2,
        random_controls_c1=rand_c,
        matched_controls_c1=match_c,
    )
