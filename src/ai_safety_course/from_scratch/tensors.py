"""tensors — the from-scratch tensor toolbox (track modules 01–02).

This module implements, in pure Python 3.12 standard library, the tensor
machinery the video's PyTorch chapters teach (SRC-VIDEO-001, page-inspected:
*PyTorch Introduction; Tensor Operations; Creating Tensors; Matrix
Multiplication; Transposing & Permuting; Indexing & Slicing; Concatenating
Tensors; Special Tensors*) together with the companion repository's written
module ``03_pytorch_fundamentals`` (SRC-REPO-001, full-text-read — nine
lessons, the ninth being tokenization and embeddings). Notes:
``research/ai-researcher-from-scratch/01-math-foundations.md`` and
``02-python-and-pytorch-fundamentals.md``.

Design contract
---------------
* A :class:`Tensor` is a nested list of floats with a **uniform shape**
  (every axis the same length all the way down). Non-rectangular data
  raises :class:`ShapeError` at construction — never later, mid-operation.
* Operations are **pure**: they return new tensors and never mutate their
  inputs. There is no in-place arithmetic, no autograd, no GPU — those are
  exactly the parts the later modules add *by hand* so the mechanism stays
  visible.
* Shape errors are explicit: every check raises with the expected and the
  actual shape in the message. In from-scratch code the dominant bug class
  is shape confusion; the errors here are designed to be readable.
* Randomness is seeded and deterministic (:meth:`Tensor.rand`,
  :func:`randn`) — reproducibility is a course-wide rule (planning/
  BUILD_PLAN.md; the companion repo's methodology layer makes the same
  demand of its own experiments).

The module is deliberately small: it is the toolbox modules 03–05 build
neurons, networks, attention, and a small GPT with — nothing here exists
for its own sake.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Sequence


class ShapeError(ValueError):
    """Raised when data or an operation's shapes do not conform.

    The message always states the shapes involved so the failure is
    diagnosable without a debugger: from-scratch code fails loudly.
    """


# ---------------------------------------------------------------------------
# shape utilities
# ---------------------------------------------------------------------------


def shape_of(data: object) -> tuple[int, ...]:
    """Return the uniform nested-list shape of ``data``.

    A flat list of numbers is 1-D; a list of equal-length lists is 2-D,
    and so on. Raises :class:`ShapeError` for ragged nesting, for empty
    containers in the middle of a shape, or for non-numeric leaves.

    >>> shape_of([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    (3, 2)
    """
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        return ()
    if not isinstance(data, Sequence) or isinstance(data, (str, bytes)):
        raise ShapeError(f"tensor leaves must be numbers, got {type(data).__name__!r}")
    if len(data) == 0:
        raise ShapeError("cannot infer the shape of an empty sequence")
    first = data[0]
    inner = shape_of(first)
    for i, item in enumerate(data):
        if shape_of(item) != inner:
            raise ShapeError(
                f"ragged data: element 0 has shape {inner}, element {i} has {shape_of(item)}"
            )
    return (len(data), *inner)


def _flatten(data: object, out: list[float]) -> None:
    """Append the leaves of nested ``data`` to ``out`` in row-major order."""
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        out.append(float(data))
    else:
        for item in data:
            _flatten(item, out)


def _numel(shape: Sequence[int]) -> int:
    n = 1
    for d in shape:
        n *= d
    return n


def _unflatten(flat: Sequence[float], shape: Sequence[int]) -> object:
    """Rebuild nested lists from a flat row-major sequence (inverse of flatten)."""
    if not shape:
        return flat[0]
    if len(shape) == 1:
        return list(flat)
    stride = _numel(shape[1:])
    return [_unflatten(flat[i * stride : (i + 1) * stride], shape[1:]) for i in range(shape[0])]


# ---------------------------------------------------------------------------
# the tensor
# ---------------------------------------------------------------------------


class Tensor:
    """A dense rectangular array of floats with named-shape arithmetic.

    Construction validates uniformity once; every operation afterwards can
    trust ``self.shape``. Indexing follows NumPy/PyTorch conventions at the
    level this track needs: one int or slice (or ``None``-free tuple of
    them) per axis; an all-int tuple returns a plain ``float``, anything
    else returns a new :class:`Tensor`.
    """

    __slots__ = ("data", "shape")

    def __init__(self, data: object) -> None:
        if isinstance(data, Tensor):
            # copy constructor: shares nothing mutable
            data = data.tolist()
        self.shape = shape_of(data)
        flat: list[float] = []
        _flatten(data, flat)
        self.data: list[float] = flat  # row-major storage; shape interprets it

    # -- constructors ------------------------------------------------------

    @classmethod
    def zeros(cls, *shape: int) -> Tensor:
        """A tensor of zeros (0.0) with the given shape."""
        _check_shape_literal(shape)
        return cls(_unflatten([0.0] * _numel(shape), shape) if shape else 0.0)

    @classmethod
    def ones(cls, *shape: int) -> Tensor:
        """A tensor of ones (1.0) with the given shape."""
        _check_shape_literal(shape)
        return cls(_unflatten([1.0] * _numel(shape), shape) if shape else 1.0)

    @classmethod
    def full(cls, value: float, *shape: int) -> Tensor:
        """A tensor filled with ``value``."""
        _check_shape_literal(shape)
        return cls(_unflatten([float(value)] * _numel(shape), shape) if shape else float(value))

    @classmethod
    def arange(cls, start: float, stop: float | None = None, step: float = 1.0) -> Tensor:
        """A 1-D tensor like ``torch.arange(start, stop, step)`` over floats.

        ``arange(5)`` means ``arange(0, 5, 1)`` — the single-argument form
        counts from zero, matching the framework convention.
        """
        if stop is None:
            start, stop = 0.0, start
        if step == 0:
            raise ShapeError("arange step must be nonzero")
        vals = []
        x = float(start)
        if step > 0:
            while x < stop:
                vals.append(x)
                x += step
        else:
            while x > stop:
                vals.append(x)
                x += step
        if not vals:
            raise ShapeError(f"arange({start}, {stop}, {step}) produces no elements")
        return cls(vals)

    @classmethod
    def eye(cls, n: int) -> Tensor:
        """The ``n x n`` identity matrix (special tensor: ones on the diagonal)."""
        if n < 0:
            raise ShapeError(f"identity dimension must be >= 0, got {n}")
        return cls([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])

    @classmethod
    def rand(cls, *shape: int, seed: int = 0) -> Tensor:
        """Uniform ``[0, 1)`` values from a seeded Mersenne Twister.

        Determinism contract: the same ``shape`` and ``seed`` always
        produce the same tensor (same interpreter version), which is what
        makes the track's examples reproducible.
        """
        _check_shape_literal(shape)
        rng = random.Random(seed)
        flat = [rng.random() for _ in range(_numel(shape))]
        return cls(_unflatten(flat, shape) if shape else flat[0])

    @classmethod
    def randn(cls, *shape: int, seed: int = 0) -> Tensor:
        """Standard-normal values via Box–Muller from a seeded generator.

        Pairs of uniforms become pairs of normals; the generator is
        :func:`random.Random(seed)`, so the output is deterministic.
        """
        _check_shape_literal(shape)
        rng = random.Random(seed)
        flat: list[float] = []
        n = _numel(shape)
        while len(flat) < n:
            u1, u2 = rng.random() or 1e-16, rng.random()
            r = math.sqrt(-2.0 * math.log(u1))
            flat.append(r * math.cos(2.0 * math.pi * u2))
            flat.append(r * math.sin(2.0 * math.pi * u2))
        del flat[n:]
        return cls(_unflatten(flat, shape) if shape else flat[0])

    # -- basic properties --------------------------------------------------

    @property
    def ndim(self) -> int:
        """Number of axes."""
        return len(self.shape)

    def numel(self) -> int:
        """Total number of elements."""
        return _numel(self.shape)

    def tolist(self) -> object:
        """The nested-list form (deep copy; safe to mutate)."""
        return _unflatten(self.data, self.shape) if self.shape else self.data[0]

    def item(self) -> float:
        """The single element of a scalar (0-d or single-element) tensor."""
        if self.numel() != 1:
            raise ShapeError(f"item() requires exactly one element, shape {self.shape}")
        return self.data[0]

    # -- elementwise -------------------------------------------------------

    def map(self, fn: Callable[[float], float]) -> Tensor:
        """Elementwise ``fn`` (the primitive all pointwise math builds on)."""
        return _from_flat([fn(v) for v in self.data], self.shape)

    def __add__(self, other: Tensor | float) -> Tensor:
        if isinstance(other, Tensor):
            _require_same_shape(self, other, "addition")
            return _from_flat(
                [a + b for a, b in zip(self.data, other.data, strict=True)], self.shape
            )
        return self.map(lambda v: v + float(other))

    __radd__ = __add__

    def __sub__(self, other: Tensor | float) -> Tensor:
        if isinstance(other, Tensor):
            _require_same_shape(self, other, "subtraction")
            return _from_flat(
                [a - b for a, b in zip(self.data, other.data, strict=True)], self.shape
            )
        return self.map(lambda v: v - float(other))

    def __rsub__(self, other: float) -> Tensor:
        return self.map(lambda v: float(other) - v)

    def __mul__(self, other: Tensor | float) -> Tensor:
        if isinstance(other, Tensor):
            _require_same_shape(self, other, "elementwise multiplication")
            return _from_flat(
                [a * b for a, b in zip(self.data, other.data, strict=True)], self.shape
            )
        return self.map(lambda v: v * float(other))

    __rmul__ = __mul__

    def __neg__(self) -> Tensor:
        return self.map(lambda v: -v)

    def __truediv__(self, other: Tensor | float) -> Tensor:
        if isinstance(other, Tensor):
            _require_same_shape(self, other, "division")
            return _from_flat(
                [a / b for a, b in zip(self.data, other.data, strict=True)], self.shape
            )
        return self.map(lambda v: v / float(other))

    # -- reductions --------------------------------------------------------

    def sum(self, axis: int | None = None) -> Tensor:
        """Sum over all elements (``axis=None``) or over one axis."""
        if axis is None:
            return _from_flat([math.fsum(self.data)], ())
        ax = _norm_axis(axis, self.ndim)
        if self.ndim == 1:
            return _from_flat([math.fsum(self.data)], ())
        return _reduce_axis(self, ax, lambda xs: math.fsum(xs))

    def mean(self, axis: int | None = None) -> Tensor:
        """Mean over all elements or over one axis (explicit denominator)."""
        if axis is None:
            return _from_flat([math.fsum(self.data) / self.numel()], ())
        ax = _norm_axis(axis, self.ndim)
        if self.ndim == 1:
            return _from_flat([math.fsum(self.data) / self.shape[0]], ())
        return _reduce_axis(self, ax, lambda xs: math.fsum(xs) / len(xs))

    def max(self) -> float:
        """The maximum element (track only needs the whole-tensor form)."""
        return max(self.data)

    def min(self) -> float:
        """The minimum element."""
        return min(self.data)

    # -- shape manipulation -------------------------------------------------

    @property
    def T(self) -> Tensor:
        """Transpose: reverses all axes (for 2-D, the matrix transpose)."""
        return self.permute(*range(self.ndim - 1, -1, -1))

    def transpose(self, dim0: int = 0, dim1: int = 1) -> Tensor:
        """Swap two axes (PyTorch's ``transpose`` contract for the 2-D case)."""
        axes = list(range(self.ndim))
        a, b = _norm_axis(dim0, self.ndim), _norm_axis(dim1, self.ndim)
        axes[a], axes[b] = axes[b], axes[a]
        return self.permute(*axes)

    def permute(self, *axes: int) -> Tensor:
        """Reorder axes exactly as PyTorch's ``permute`` (all axes, once each)."""
        norm = [_norm_axis(a, self.ndim) for a in axes]
        if sorted(norm) != list(range(self.ndim)):
            raise ShapeError(
                f"permute needs each axis exactly once: got {axes} for shape {self.shape}"
            )
        # iterate flat indices under the new shape by walking the new axes
        new_shape = tuple(self.shape[a] for a in norm)
        # build index strides for old shape
        strides = [0] * self.ndim
        acc = 1
        for d in range(self.ndim - 1, -1, -1):
            strides[d] = acc
            acc *= self.shape[d]
        out: list[float] = []
        for new_idx in _iter_indices(new_shape):
            old_flat = sum(strides[norm[d]] * new_idx[d] for d in range(self.ndim))
            out.append(self.data[old_flat])
        return _from_flat(out, new_shape)

    def reshape(self, *shape: int) -> Tensor:
        """Row-major reinterpretation; ``-1`` infers one missing axis."""
        if len(shape) == 1 and isinstance(shape[0], (tuple, list)):
            shape = tuple(shape[0])
        explicit = [d for d in shape if d != -1]
        infer_count = sum(1 for d in shape if d == -1)
        if infer_count > 1:
            raise ShapeError("reshape allows at most one -1")
        if infer_count == 1:
            rest = _numel(explicit)
            if rest == 0 or self.numel() % rest != 0:
                raise ShapeError(f"cannot infer -1: {self.numel()} elements, rest {explicit}")
            inferred = self.numel() // rest
            shape = tuple(inferred if d == -1 else d for d in shape)
        if _numel(shape) != self.numel():
            raise ShapeError(
                f"reshape keeps element count: shape {self.shape} has {self.numel()}, "
                f"target {tuple(shape)} has {_numel(shape)}"
            )
        return _from_flat(list(self.data), tuple(shape))

    def flatten(self) -> Tensor:
        """Collapse to 1-D (row-major order)."""
        return _from_flat(list(self.data), (self.numel(),))

    # -- indexing ----------------------------------------------------------

    def __getitem__(self, key: int | slice | tuple[int | slice, ...]) -> float | Tensor:
        axes = key if isinstance(key, tuple) else (key,)
        if len(axes) > self.ndim:
            raise ShapeError(f"too many indices: {len(axes)} for shape {self.shape}")
        if (
            len(axes) == self.ndim
            and self.ndim > 0
            and all(isinstance(a, int) and not isinstance(a, bool) for a in axes)
        ):
            flat = self._flat_index(tuple(_norm_axis(a, self.ndim) for a in axes))
            return self.data[flat]
        # mixed ints/slices: build the sub-tensor
        cur_shape = list(self.shape)
        # walk: for each axis, int selects (drop axis), slice keeps (sized)
        out_shape: list[int] = []
        out_flat: list[float] = []
        normalized: list[int | range] = []
        for d, a in enumerate(axes):
            if isinstance(a, slice):
                rng = range(*a.indices(cur_shape[d]))
                normalized.append(rng)
                out_shape.append(len(rng))
            else:
                normalized.append(_norm_axis(int(a), self.ndim))
        out_shape.extend(cur_shape[len(axes) :])
        for idx in _iter_indices(tuple(out_shape)):
            # map out index -> in index
            in_idx: list[int] = []
            consumed = 0
            for d in range(len(axes)):
                sel = normalized[d]
                if isinstance(sel, range):
                    in_idx.append(sel[idx[consumed]])
                    consumed += 1
                else:
                    in_idx.append(sel)
            in_idx.extend(idx[consumed:])
            out_flat.append(self.data[self._flat_index(tuple(in_idx))])
        if not out_shape:
            return out_flat[0]
        return _from_flat(out_flat, tuple(out_shape))

    def _flat_index(self, idx: tuple[int, ...]) -> int:
        strides = [0] * self.ndim
        acc = 1
        for d in range(self.ndim - 1, -1, -1):
            strides[d] = acc
            acc *= self.shape[d]
        return sum(strides[d] * idx[d] for d in range(self.ndim))

    # -- comparison / repr --------------------------------------------------

    def allclose(self, other: Tensor, tol: float = 1e-9) -> bool:
        """Elementwise equality within ``tol`` (float-safe comparison)."""
        if not isinstance(other, Tensor) or other.shape != self.shape:
            return False
        return all(abs(a - b) <= tol for a, b in zip(self.data, other.data, strict=True))

    def __eq__(self, other: object) -> bool:  # pragma: no cover - convenience
        if isinstance(other, Tensor):
            return self.allclose(other)
        return NotImplemented

    def __repr__(self) -> str:  # pragma: no cover - display only
        body = repr(self.tolist())
        if len(body) > 96:
            body = body[:93] + "..."
        return f"Tensor({body}, shape={self.shape})"


# ---------------------------------------------------------------------------
# free functions (video chapters: matrix multiplication, concatenation)
# ---------------------------------------------------------------------------


def matmul(a: Tensor, b: Tensor) -> Tensor:
    """Matrix product ``A @ B`` with the shape rule made explicit.

    For 2-D inputs: ``(m, n) @ (n, p) -> (m, p)``; entry ``(i, j)`` is
    the dot product of row ``i`` of ``a`` with column ``j`` of ``b``
    (module note 01, section 5). A 1-D ``b`` (vector) is treated as a
    column vector: ``(m, n) @ (n,) -> (m,)``; a 1-D ``a`` as a row
    vector: ``(n,) @ (n, p) -> (p,)``. Batched inputs are out of scope —
    module 05 loops over the batch explicitly instead.
    """
    if b.ndim == 1 and a.ndim == 2:
        if a.shape[1] != b.shape[0]:
            raise ShapeError(
                f"matmul shape mismatch: {a.shape} @ {b.shape} "
                f"(inner dims {a.shape[1]} vs {b.shape[0]})"
            )
        out = [
            math.fsum(a.data[i * a.shape[1] + k] * b.data[k] for k in range(a.shape[1]))
            for i in range(a.shape[0])
        ]
        return _from_flat(out, (a.shape[0],))
    if a.ndim == 1 and b.ndim == 2:
        if a.shape[0] != b.shape[0]:
            raise ShapeError(
                f"matmul shape mismatch: {a.shape} @ {b.shape} "
                f"(inner dims {a.shape[0]} vs {b.shape[0]})"
            )
        out = [
            math.fsum(a.data[k] * b.data[k * b.shape[1] + j] for k in range(a.shape[0]))
            for j in range(b.shape[1])
        ]
        return _from_flat(out, (b.shape[1],))
    if a.ndim != 2 or b.ndim != 2:
        raise ShapeError(f"matmul supports 1-D/2-D operands, got {a.shape} @ {b.shape}")
    m, n, p = a.shape[0], a.shape[1], b.shape[1]
    if n != b.shape[0]:
        raise ShapeError(
            f"matmul shape mismatch: {a.shape} @ {b.shape} (inner dims {n} vs {b.shape[0]})"
        )
    out = [0.0] * (m * p)
    for i in range(m):
        for j in range(p):
            out[i * p + j] = math.fsum(a.data[i * n + k] * b.data[k * p + j] for k in range(n))
    return _from_flat(out, (m, p))


def concat(tensors: Sequence[Tensor], axis: int = 0) -> Tensor:
    """Join tensors along one axis (video chapter: *Concatenating Tensors*).

    All other axes must match exactly; the axis dimension sums. The
    video's ``torch.cat`` analogue, with the mismatch error spelled out.
    """
    if not tensors:
        raise ShapeError("concat needs at least one tensor")
    ndim = tensors[0].ndim
    for t in tensors:
        if t.ndim != ndim:
            raise ShapeError(f"concat ranks differ: {t.shape} vs {tensors[0].shape}")
    if ndim == 0:
        raise ShapeError("cannot concat 0-d tensors")
    ax = _norm_axis(axis, ndim)
    ref = list(tensors[0].shape)
    for t in tensors[1:]:
        other = list(t.shape)
        if other[:ax] + other[ax + 1 :] != ref[:ax] + ref[ax + 1 :]:
            raise ShapeError(
                f"concat non-axis shapes differ: {t.shape} vs {tensors[0].shape} on axis {ax}"
            )
    new_shape = list(ref)
    new_shape[ax] = sum(t.shape[ax] for t in tensors)
    out: list[float] = []
    # walk blocks of size = numel of everything after axis
    block = _numel(ref[ax + 1 :]) if ax + 1 < ndim else 1
    outer = _numel(ref[:ax])
    for o in range(outer):
        for t in tensors:
            base = o * (block * t.shape[ax])
            for inner in range(block * t.shape[ax]):
                out.append(t.data[base + inner])
    return _from_flat(out, tuple(new_shape))


# ---------------------------------------------------------------------------
# tokenization and embeddings (video lesson 9 of the PyTorch module)
# ---------------------------------------------------------------------------


class CharTokenizer:
    """A minimal character tokenizer (the companion repo's lesson 9).

    Vocabulary is the sorted set of characters seen at :meth:`fit`; encode
    maps each character to its index; decode maps back. Subword and
    byte-pair tokenization are deliberately out of scope — module 05's
    GPT needs exactly "text to integer sequence and back", and keeping it
    character-level makes the tokenizer inspectable in one screen.
    """

    def __init__(self, text: str) -> None:
        chars = sorted(set(text))
        if not chars:
            raise ValueError("tokenizer needs a nonempty training text")
        self.stoi: dict[str, int] = {c: i for i, c in enumerate(chars)}
        self.itos: list[str] = chars

    @property
    def vocab_size(self) -> int:
        return len(self.itos)

    def encode(self, text: str) -> list[int]:
        unknown = set(text) - set(self.stoi)
        if unknown:
            raise ValueError(
                f"cannot encode characters outside the vocabulary: {sorted(unknown)!r}"
            )
        return [self.stoi[c] for c in text]

    def decode(self, ids: Sequence[int]) -> str:
        for i in ids:
            if not 0 <= i < len(self.itos):
                raise ValueError(f"decode id {i} outside vocabulary of size {len(self.itos)}")
        return "".join(self.itos[i] for i in ids)


def embed(ids: Sequence[int], matrix: Tensor) -> Tensor:
    """Embedding lookup: rows of ``matrix`` selected by ``ids``.

    An embedding table is a ``(vocab_size, d_model)`` matrix and an
    embedding *is* row selection — which is the same as a one-hot matrix
    product (module note 02 makes that identification explicitly). The
    lookup form is what real implementations run; the one-hot form is
    what proves it is linear.
    """
    if matrix.ndim != 2:
        raise ShapeError(f"embedding table must be 2-D, got {matrix.shape}")
    vocab, d = matrix.shape
    for i in ids:
        if not 0 <= i < vocab:
            raise ValueError(f"embedding id {i} outside vocab size {vocab}")
    out = [matrix.data[i * d + j] for i in ids for j in range(d)]
    return _from_flat(out, (len(ids), d))


def one_hot(ids: Sequence[int], vocab_size: int) -> Tensor:
    """One-hot encoding of ``ids`` as a ``(len(ids), vocab_size)`` matrix."""
    for i in ids:
        if not 0 <= i < vocab_size:
            raise ValueError(f"one_hot id {i} outside vocab size {vocab_size}")
    rows = [[1.0 if j == i else 0.0 for j in range(vocab_size)] for i in ids]
    return _from_flat([v for row in rows for v in row], (len(ids), vocab_size))


# ---------------------------------------------------------------------------
# internal helpers
# ---------------------------------------------------------------------------


def _from_flat(flat: Sequence[float], shape: tuple[int, ...]) -> Tensor:
    t = Tensor.__new__(Tensor)
    t.shape = tuple(shape)
    t.data = list(flat)
    return t


def _check_shape_literal(shape: tuple[int, ...]) -> None:
    for d in shape:
        if not isinstance(d, int) or d < 0:
            raise ShapeError(f"shape entries must be non-negative ints, got {shape}")


def _require_same_shape(a: Tensor, b: Tensor, op: str) -> None:
    if a.shape != b.shape:
        raise ShapeError(f"{op} requires equal shapes: {a.shape} vs {b.shape}")


def _norm_axis(axis: int, ndim: int) -> int:
    a = axis + ndim if axis < 0 else axis
    if not 0 <= a < ndim:
        raise ShapeError(f"axis {axis} out of range for {ndim}-D tensor")
    return a


def _iter_indices(shape: tuple[int, ...]) -> list[tuple[int, ...]]:
    """All multi-indices of a shape, row-major (C order)."""
    if not shape:
        return [()]
    out: list[tuple[int, ...]] = [()]
    for d in shape:
        out = [idx + (i,) for idx in out for i in range(d)]
    return out


def _reduce_axis(t: Tensor, axis: int, fn: Callable[[list[float]], float]) -> Tensor:
    """Apply ``fn`` along one axis, keeping remaining axes in order."""
    remaining = [d for i, d in enumerate(t.shape) if i != axis]
    out: list[float] = []
    for idx in _iter_indices(tuple(remaining)):
        sel = list(idx[:axis]) + [None] + list(idx[axis:])
        vals = []
        for k in range(t.shape[axis]):
            full = sel[:axis] + [k] + sel[axis + 1 :]
            vals.append(t.data[t._flat_index(tuple(full))])
        out.append(fn(vals))
    return _from_flat(out, tuple(remaining))


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
