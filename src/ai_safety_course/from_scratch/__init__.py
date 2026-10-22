"""from_scratch — the AI Researcher From Scratch track's code modules.

Track notes: ``research/ai-researcher-from-scratch/`` (7 modules).
Sources: SRC-VIDEO-001 (video, page-inspected) and SRC-REPO-001
(companion repository, full-text-read) in ``research/source-register.yaml``.

Stdlib-only by design (ADR-0002 dependency floor): a from-scratch
implementation that imports a deep-learning framework is not from
scratch. Modules:

* :mod:`tensors` — the tensor toolbox (creation, shapes, matmul,
  transpose/permute, indexing/slicing, concatenation, special tensors,
  char tokenization, embeddings).
* ``neuron`` / ``activations`` — one neuron and six activation functions.
* ``network`` — a layer, a network, manual backpropagation, SGD.
* ``attention`` — scaled dot-product, causal, multi-head attention.
* ``transformer`` — embeddings, positional encoding, blocks, a small GPT.
* ``moe`` — sparse mixture-of-experts and low-rank latent attention.
"""

from ai_safety_course.from_scratch.tensors import (
    CharTokenizer,
    ShapeError,
    Tensor,
    concat,
    embed,
    matmul,
    one_hot,
    shape_of,
)

__all__ = [
    "CharTokenizer",
    "ShapeError",
    "Tensor",
    "concat",
    "embed",
    "matmul",
    "one_hot",
    "shape_of",
]
