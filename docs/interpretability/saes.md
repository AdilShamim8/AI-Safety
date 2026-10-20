# Sparse autoencoders (SAEs)

Sparse autoencoders are the field's current best tool for decomposing
neural activations into interpretable features, cutting through
superposition (Elhage et al., arXiv:2209.10652). If you are doing any
interpretability work on LLMs today, you will touch released SAEs.

## The setup

Train an autoencoder on activations `x ∈ R^d_model` from a specific site
(usually MLP output or residual stream, per-layer):

```text
encoder:  z = ReLU(W_enc (x − b_pre))          # z ∈ R^{d_sae}, d_sae ≫ d_model
decoder:  x̂ = W_dec z + b_pre                  # reconstruct x
loss:     ‖x − x̂‖²  +  λ · ‖z‖₁               # sparsity penalty
```

The dictionary vectors (decoder rows) are candidate *features*; a sparse
`z` says which few features were "active." The magic trick is
**overcompleteness** (d_sae = 8×–32× the width): superposed features get
separate directions to live in.

## Timeline of the real results

- **2022–2023 — Toy Monosemanticity / Towards Monosemanticity** (Bricken
  et al., transformer-circuits.pub, Oct 2023): a 512-neuron MLP layer of
  a 1-layer model decomposed into 4096+ interpretable features
  (DNA strings, legal language, Arabic script...). Proof that dictionary
  learning beats neuron-by-neuron reading.
- **2024 — Scaling Monosemanticity** (Templeton et al.): Claude 3 Sonnet
  SAEs with millions of features, including the famous **Golden Gate
  Bridge feature**; clamping it produced the public Golden Gate Claude
  demo (May 2024). Also: features for code-backdoor behavior,
  sycophantic praise, unsafe-code patterns — safety-relevant concepts do
  get linear-ish representations in production models.
- **2024 — Public SAE releases**: OpenAI released GPT-4-top-layer SAEs
  (16M features, May 2024); Google DeepMind released Gemma-2 SAEs (July
  2024); EleutherAI's SAELens and Neuronpedia (Joseph Bloom & Curt
  Tigges) made SAE exploration point-and-click.
- **2025 — Cross-layer transcoders / Matryoshka SAEs** and Anthropic's
  circuit tracing on transcript-level reasoning push toward features that
  compose across layers, where the single-site assumption breaks.

## Architectural variants (why your colleague's SAE has a different loss)

| Variant | Change | Why |
|---------|--------|-----|
| TopK SAE | Keep only top-k activations, λ dropped | Cleaner sparsity, no L1 shrinkage artifacts (Makhzani & Frey 2013 lineage; OpenAI's GPT-4 SAEs) |
| JumpReLU SAE | JumpReLU nonlinearity + L0 penalty | Better FLOP-sparse Pareto (DeepMind Gemma release) |
| Gated SAE | Separate magnitude/phase paths | Handles "dead feature" pathology (Rajamanoharan et al., arXiv:2404.16014? — "Gated SAEs", DeepMind 2024) |
| BatchTopK | Top-k across batch | Improved training stability (2024–2025 releases) |
| End-to-end SAEs | Trained to make *downstream* predictions sparser | Avoids reconstruction not aligning with behavior (Cohen et al., 2024) |

## Known problems — read before trusting an SAE analysis

1. **No ground-truth decomposition.** Different SAEs on the same model
   give different feature sets; "the features" is category error (see
   Sharkey et al. Open Source Implementation rounds; "SAE splits" of
   concepts).
2. **Reconstruction ≠ behavior.** High reconstruction loss at a site can
   coexist with behavioral fidelity, and vice versa; use
   **effective-reconstruction / downstream-loss metrics** (e.g., SAELens's
   CE-lossRecovered), not MSE, when stakes are safety-relevant.
3. **Feature splitting & shrinkage** make feature counting non-monotone
   with dictionary size (Engels et al. on "not all features are used"; L1
   shrinkage biases activations downward).
4. **Auto-interpretability is lossy.** Naming features with GPT-4-class
   labelers works ~60–80% of the time depending on task (Bills et al.,
  "Language models can explain neurons in language models," OpenAI 2023);
   human verification remains necessary for safety claims.
5. **Context contamination** — features active on your eval prompts may
   reflect dataset artifacts, not the concept; test on multiple corpora.

## Practical starter path

```python
# With SAELens (pip install sae-lens), loading public Gemma-2 SAEs:
from sae_lens import SAE
sae, _, _ = SAE.from_pretrained(
    release="gemma-sae-2b-canonical",  # public DeepMind release
    sae_id="blocks.12.hook_z",
)
# then run feature dashboards via Neuronpedia before writing any claims
```

Rule of thumb: **dashboard first, claims second**. Every feature you cite
in an audit should have a recorded activation-pattern demo (top activating
examples from multiple datasets) attached.
