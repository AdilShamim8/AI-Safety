"""Tests for ai_safety_course.from_scratch.tensors (track modules 01-02).

Every operation the video's PyTorch chapters teach gets at least one
hand-computed positive case and one explicit failure case: creation and
shape inference, elementwise arithmetic, matrix multiplication (the
module-01 worked example is reused as the reference), transpose/permute,
reshape, indexing and slicing, concatenation, special tensors,
deterministic randomness, and the tokenization/embeddings lesson
(including the one-hot identification: lookup == matrix product).
"""

import math

import pytest

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

# ---------------------------------------------------------------------------
# construction and shapes
# ---------------------------------------------------------------------------


def test_shape_of_inference() -> None:
    assert shape_of([1.0, 2.0]) == (2,)
    assert shape_of([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]) == (3, 2)
    assert shape_of([[[1.0], [2.0]], [[3.0], [4.0]]]) == (2, 2, 1)


def test_shape_of_rejects_ragged() -> None:
    with pytest.raises(ShapeError, match="ragged"):
        shape_of([[1.0, 2.0], [3.0]])


def test_shape_of_rejects_non_numeric_leaf() -> None:
    with pytest.raises(ShapeError, match="numbers"):
        shape_of([1.0, "two"])


def test_tensor_properties() -> None:
    t = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    assert t.shape == (3, 2)
    assert t.ndim == 2
    assert t.numel() == 6
    assert t.tolist() == [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]


def test_tensor_copy_constructor_is_deep() -> None:
    a = Tensor([[1.0, 2.0]])
    b = Tensor(a)
    b.data[0] = 99.0
    assert a.data[0] == 1.0


def test_scalar_tensor() -> None:
    t = Tensor(3.5)
    assert t.shape == () and t.ndim == 0 and t.numel() == 1
    assert t.item() == 3.5


def test_item_rejects_multi_element() -> None:
    with pytest.raises(ShapeError, match="exactly one element"):
        Tensor([1.0, 2.0]).item()


# ---------------------------------------------------------------------------
# special tensors and deterministic randomness
# ---------------------------------------------------------------------------


def test_zeros_ones_full() -> None:
    assert Tensor.zeros(2, 3).tolist() == [[0.0] * 3] * 2
    assert Tensor.ones(2).tolist() == [1.0, 1.0]
    assert Tensor.full(7.0, 3, 1).tolist() == [[7.0], [7.0], [7.0]]


def test_arange() -> None:
    assert Tensor.arange(5).tolist() == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert Tensor.arange(1, 5, 2.0).tolist() == [1.0, 3.0]
    assert Tensor.arange(2, -1, -1).tolist() == [2.0, 1.0, 0.0]
    with pytest.raises(ShapeError, match="nonzero"):
        Tensor.arange(5, step=0.0)
    with pytest.raises(ShapeError, match="no elements"):
        Tensor.arange(2, 1)


def test_eye_is_identity_under_matmul() -> None:
    i3 = Tensor.eye(3)
    x = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert matmul(x, i3).allclose(x)
    assert matmul(i3, x.T).allclose(x.T)


def test_rand_is_deterministic_and_bounded() -> None:
    a = Tensor.rand(4, 5, seed=7)
    b = Tensor.rand(4, 5, seed=7)
    c = Tensor.rand(4, 5, seed=8)
    assert a.allclose(b)
    assert not a.allclose(c)
    assert a.min() >= 0.0 and a.max() < 1.0


def test_randn_is_deterministic_and_centered() -> None:
    a = Tensor.randn(50, 50, seed=3)
    b = Tensor.randn(50, 50, seed=3)
    assert a.allclose(b)
    # weak distributional checks (mean near 0, variance near 1, mostly |x|<4)
    m = a.mean().item()
    v = a.map(lambda v: (v - m) ** 2).mean().item()
    assert abs(m) < 0.1
    assert 0.7 < v < 1.4
    assert a.map(lambda v: 1.0 if abs(v) < 4.0 else 0.0).mean().item() > 0.999


# ---------------------------------------------------------------------------
# elementwise arithmetic
# ---------------------------------------------------------------------------


def test_add_sub_mul_div_tensor_and_scalar() -> None:
    a = Tensor([[1.0, 2.0], [3.0, 4.0]])
    b = Tensor([[10.0, 20.0], [30.0, 40.0]])
    assert (a + b).tolist() == [[11.0, 22.0], [33.0, 44.0]]
    assert (b - a).tolist() == [[9.0, 18.0], [27.0, 36.0]]
    assert (a * 2.0).tolist() == [[2.0, 4.0], [6.0, 8.0]]
    assert (2.0 * a).tolist() == [[2.0, 4.0], [6.0, 8.0]]
    assert (b / 10.0).tolist() == [[1.0, 2.0], [3.0, 4.0]]
    assert (10.0 - a).tolist() == [[9.0, 8.0], [7.0, 6.0]]
    assert (-a).tolist() == [[-1.0, -2.0], [-3.0, -4.0]]


def test_elementwise_mismatch_raises() -> None:
    a = Tensor([[1.0, 2.0]])
    b = Tensor([[1.0], [2.0]])
    with pytest.raises(ShapeError, match="equal shapes"):
        _ = a + b


def test_map_is_elementwise() -> None:
    t = Tensor([1.0, 4.0, 9.0])
    assert t.map(math.sqrt).tolist() == [1.0, 2.0, 3.0]


# ---------------------------------------------------------------------------
# reductions
# ---------------------------------------------------------------------------


def test_sum_and_mean_whole_and_axis() -> None:
    t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert t.sum().item() == 21.0
    assert t.mean().item() == 3.5
    assert t.sum(axis=0).tolist() == [5.0, 7.0, 9.0]
    assert t.sum(axis=1).tolist() == [6.0, 15.0]
    assert t.mean(axis=1).tolist() == [2.0, 5.0]
    assert t.sum(axis=-1).tolist() == [6.0, 15.0]


def test_min_max() -> None:
    t = Tensor([[3.0, 1.0], [2.0, 5.0]])
    assert t.min() == 1.0 and t.max() == 5.0


# ---------------------------------------------------------------------------
# matrix multiplication (module-01 worked example is the reference)
# ---------------------------------------------------------------------------


def test_matmul_module01_worked_example() -> None:
    w = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    x = Tensor([1.0, 2.0])
    assert matmul(w, x).tolist() == [5.0, 11.0, 17.0]


def test_matmul_2d_2d() -> None:
    a = Tensor([[1.0, 2.0], [3.0, 4.0]])
    b = Tensor([[0.0, 1.0], [1.0, 0.0]])
    assert matmul(a, b).tolist() == [[2.0, 1.0], [4.0, 3.0]]
    assert matmul(b, a).tolist() == [[3.0, 4.0], [1.0, 2.0]]


def test_matmul_row_vector_case() -> None:
    a = Tensor([1.0, 2.0, 3.0])
    b = Tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    assert matmul(a, b).tolist() == [4.0, 5.0]


def test_matmul_inner_dim_mismatch_raises() -> None:
    a = Tensor([[1.0, 2.0, 3.0]])  # (1, 3)
    b = Tensor([[1.0], [2.0]])  # (2, 1)
    with pytest.raises(ShapeError, match="inner dims 3 vs 2"):
        matmul(a, b)


def test_matmul_rejects_3d() -> None:
    a = Tensor.ones(2, 2, 2)
    with pytest.raises(ShapeError, match="1-D/2-D"):
        matmul(a, Tensor.ones(2, 2))


def test_matmul_associativity_holds() -> None:
    a = Tensor([[1.0, 2.0], [3.0, 4.0]])
    b = Tensor([[0.0, 1.0], [1.0, 0.0]])
    c = Tensor([[2.0, 0.0], [0.0, 2.0]])
    left = matmul(matmul(a, b), c)
    right = matmul(a, matmul(b, c))
    assert left.allclose(right)


# ---------------------------------------------------------------------------
# transpose / permute / reshape
# ---------------------------------------------------------------------------


def test_transpose_2d() -> None:
    t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert t.T.tolist() == [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    assert t.transpose(0, 1).tolist() == t.T.tolist()
    assert t.T.T.allclose(t)


def test_permute_3d_full_reversal() -> None:
    t = Tensor([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    assert t.shape == (2, 2, 2)
    p = t.permute(2, 0, 1)
    assert p.shape == (2, 2, 2)
    # p[i, j, k] == t[j, k, i]
    assert p[0, 1, 0] == t[1, 0, 0] == 5.0
    assert p[1, 0, 1] == t[0, 1, 1] == 4.0


def test_permute_rejects_repeated_axes() -> None:
    t = Tensor.ones(2, 3, 4)
    with pytest.raises(ShapeError, match="exactly once"):
        t.permute(0, 0, 1)


def test_reshape_row_major_and_inference() -> None:
    t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert t.reshape(3, 2).tolist() == [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    assert t.reshape(-1).tolist() == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    assert t.reshape(6, 1).tolist() == [[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]
    assert t.reshape((2, 3)).allclose(t)


def test_reshape_element_count_mismatch_raises() -> None:
    t = Tensor.ones(2, 3)
    with pytest.raises(ShapeError, match="element count"):
        t.reshape(4, 2)
    with pytest.raises(ShapeError, match="at most one -1"):
        t.reshape(-1, -1)


def test_flatten() -> None:
    t = Tensor([[1.0, 2.0], [3.0, 4.0]])
    assert t.flatten().tolist() == [1.0, 2.0, 3.0, 4.0]


# ---------------------------------------------------------------------------
# indexing and slicing
# ---------------------------------------------------------------------------


def test_full_int_indexing_returns_float() -> None:
    t = Tensor([[1.0, 2.0], [3.0, 4.0]])
    assert t[1, 0] == 3.0
    assert t[-1, -1] == 4.0


def test_partial_int_index_returns_row() -> None:
    t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    row = t[0]
    assert isinstance(row, Tensor)
    assert row.tolist() == [1.0, 2.0, 3.0]


def test_slice_indexing() -> None:
    t = Tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    assert t[0:2].tolist() == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    assert t[:, 1].tolist() == [2.0, 5.0, 8.0]
    assert t[0, 0:2].tolist() == [1.0, 2.0]
    assert t[1:3, 0:2].tolist() == [[4.0, 5.0], [7.0, 8.0]]
    assert t[::2].tolist() == [[1.0, 2.0, 3.0], [7.0, 8.0, 9.0]]


def test_too_many_indices_raises() -> None:
    t = Tensor.ones(2, 2)
    with pytest.raises(ShapeError, match="too many indices"):
        _ = t[0, 0, 0]


# ---------------------------------------------------------------------------
# concatenation
# ---------------------------------------------------------------------------


def test_concat_axis_0_and_1() -> None:
    a = Tensor([[1.0, 2.0], [3.0, 4.0]])
    b = Tensor([[5.0, 6.0]])
    assert concat([a, b], axis=0).tolist() == [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    c = Tensor([[5.0], [6.0]])
    assert concat([a, c], axis=1).tolist() == [[1.0, 2.0, 5.0], [3.0, 4.0, 6.0]]


def test_concat_three_tensors_order() -> None:
    parts = [Tensor([[i]]) for i in range(3)]
    assert concat(parts, axis=0).tolist() == [[0.0], [1.0], [2.0]]


def test_concat_mismatch_raises() -> None:
    a = Tensor.ones(2, 2)
    b = Tensor.ones(3, 2)
    ok = concat([a, b], axis=0)
    assert ok.shape == (5, 2)
    with pytest.raises(ShapeError, match="non-axis shapes differ"):
        concat([a, b], axis=1)


def test_concat_rank_mismatch_raises() -> None:
    with pytest.raises(ShapeError, match="ranks differ"):
        concat([Tensor.ones(2), Tensor.ones(2, 2)], axis=0)


# ---------------------------------------------------------------------------
# tokenization and embeddings (lesson 9)
# ---------------------------------------------------------------------------


def test_char_tokenizer_round_trip() -> None:
    tok = CharTokenizer("hello")
    assert tok.vocab_size == 4  # e, h, l, o
    ids = tok.encode("hello")
    assert ids == [tok.stoi["h"], tok.stoi["e"], tok.stoi["l"], tok.stoi["l"], tok.stoi["o"]]
    assert tok.decode(ids) == "hello"


def test_char_tokenizer_unknown_char_raises() -> None:
    tok = CharTokenizer("abc")
    with pytest.raises(ValueError, match="outside the vocabulary"):
        tok.encode("abcd")


def test_char_tokenizer_decode_out_of_range_raises() -> None:
    tok = CharTokenizer("abc")
    with pytest.raises(ValueError, match="outside vocabulary"):
        tok.decode([17])


def test_embed_selects_rows() -> None:
    table = Tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    got = embed([2, 0], table)
    assert got.tolist() == [[5.0, 6.0], [1.0, 2.0]]


def test_embed_equals_one_hot_matmul() -> None:
    """The identification the module-02 note makes: lookup == one-hot @ table."""
    table = Tensor([[0.1, 0.9], [0.8, 0.2], [0.5, 0.5]])
    ids = [2, 0, 1, 0]
    lookup = embed(ids, table)
    product = matmul(one_hot(ids, 3), table)
    assert lookup.allclose(product)


def test_embed_rejects_out_of_vocab() -> None:
    table = Tensor.ones(3, 2)
    with pytest.raises(ValueError, match="outside vocab"):
        embed([3], table)


def test_one_hot_shape_and_rows() -> None:
    oh = one_hot([1, 0], 3)
    assert oh.shape == (2, 3)
    assert oh.tolist() == [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
    with pytest.raises(ValueError, match="outside vocab"):
        one_hot([3], 3)
