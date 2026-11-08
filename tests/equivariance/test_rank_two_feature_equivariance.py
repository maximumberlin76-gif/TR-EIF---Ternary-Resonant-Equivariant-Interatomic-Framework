
"""Independent E(3) qualification of Cartesian rank-two TR-EIF features.

Reconstruct Q T Q^T directly, verify the rank-two outer product and tensor
invariants, and test decomposition, group composition, and aligned scalar,
vector, and tensor feature channels. Both proper and improper orthogonal
transformations are exercised with nonzero spatial translations.
"""

from dataclasses import FrozenInstanceError, replace
from math import isfinite

import pytest

from tr_eif.equivariant.features import NodeFeatures, NodeFeatureVector
from tr_eif.equivariant.rank_two import (
    RankTwoFeatureVector,
    RankTwoTensor,
    ScalarVectorTensorFeatures,
)
from tr_eif.equivariant.transform import E3Transformation


IDENTITY = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
ROT_Z = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
ROT_X = ((1.0, 0.0, 0.0), (0.0, 0.0, -1.0), (0.0, 1.0, 0.0))
REFLECT_X = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
INVERT = ((-1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, -1.0))

TRANSFORMS = (
    E3Transformation(IDENTITY, (3.0, -2.0, 5.0)),
    E3Transformation(ROT_Z, (-4.0, 1.5, 2.0)),
    E3Transformation(ROT_X, (0.3, -1.2, 4.0)),
    E3Transformation(REFLECT_X, (1.0, 2.0, -7.0)),
    E3Transformation(INVERT, (-5.0, 0.0, 3.0)),
)

TENSOR = RankTwoTensor((
    (3.0, 2.0, -4.0),
    (-1.0, 5.0, 0.5),
    (1.25, -7.0, -2.0),
))

SECOND = RankTwoTensor((
    (-1.0, 0.75, 2.0),
    (4.0, 0.0, -3.0),
    (1.0, 5.0, 6.0),
))


def _matmul(a, b):
    return tuple(
        tuple(
            sum(a[i][k] * b[k][j] for k in range(3))
            for j in range(3)
        )
        for i in range(3)
    )


def _transpose(a):
    return tuple(
        tuple(a[j][i] for j in range(3))
        for i in range(3)
    )


def _reference_action(tensor, matrix):
    return _matmul(
        _matmul(matrix, tensor.rows),
        _transpose(matrix),
    )


def _assert_tensor_close(actual: RankTwoTensor, expected):
    for row, target in zip(actual.rows, expected, strict=True):
        assert row == pytest.approx(
            target, rel=1.0e-12, abs=1.0e-12
        )


def _sum_tensors(*tensors):
    return tuple(
        tuple(
            sum(t.rows[i][j] for t in tensors)
            for j in range(3)
        )
        for i in range(3)
    )


def _base_features():
    return NodeFeatureVector(nodes=(
        NodeFeatures(
            scalars=(1.0, -0.2),
            vectors=((1.0, -2.0, 0.5),),
        ),
        NodeFeatures(
            scalars=(0.5, 3.0),
            vectors=((0.0, 1.0, 2.0),),
        ),
        NodeFeatures(
            scalars=(-1.0, 4.0),
            vectors=((3.0, 0.0, -0.5),),
        ),
    ))


def _rank_two_features():
    return RankTwoFeatureVector(nodes=(
        (TENSOR, SECOND),
        (
            RankTwoTensor.outer(
                (1.0, -2.0, 0.5),
                (0.0, 3.0, -1.0),
            ),
            TENSOR,
        ),
        (
            SECOND,
            RankTwoTensor.outer(
                (0.0, 1.0, 0.0),
                (2.0, 0.0, 3.0),
            ),
        ),
    ))


@pytest.mark.parametrize("transform", TRANSFORMS)
@pytest.mark.parametrize("tensor", (TENSOR, SECOND))
def test_rank_two_action_matches_independent_matrix_product(
    transform, tensor
):
    _assert_tensor_close(
        tensor.transformed(transform),
        _reference_action(tensor, transform.matrix),
    )


@pytest.mark.parametrize("transform", TRANSFORMS)
def test_invariants_and_double_contraction(transform):
    rotated = TENSOR.transformed(transform)
    other = SECOND.transformed(transform)

    assert rotated.trace == pytest.approx(
        sum(TENSOR.rows[i][i] for i in range(3))
    )

    assert rotated.frobenius_norm_squared == pytest.approx(
        sum(value * value for row in TENSOR.rows for value in row)
    )

    reference = sum(
        TENSOR.rows[i][j] * SECOND.rows[i][j]
        for i in range(3)
        for j in range(3)
    )

    assert rotated.double_contract(other) == pytest.approx(
        reference, abs=1.0e-11
    )

    assert TENSOR.double_contract(SECOND) == pytest.approx(
        reference
    )

    assert TENSOR.double_contract(SECOND) == pytest.approx(
        SECOND.double_contract(TENSOR)
    )

    assert rotated.double_contract(rotated) == pytest.approx(
        rotated.frobenius_norm_squared
    )


@pytest.mark.parametrize("transform", TRANSFORMS)
def test_outer_product_covariance_and_independent_components(
    transform
):
    left = (1.25, -2.0, 0.4)
    right = (-3.0, 0.75, 2.5)

    outer = RankTwoTensor.outer(left, right)

    expected_rows = tuple(
        tuple(left[i] * right[j] for j in range(3))
        for i in range(3)
    )

    assert outer.rows == expected_rows

    transformed = outer.transformed(transform)

    rotated_outer = RankTwoTensor.outer(
        transform.transform_vector(left),
        transform.transform_vector(right),
    )

    _assert_tensor_close(transformed, rotated_outer.rows)

    _assert_tensor_close(
        transformed,
        _reference_action(outer, transform.matrix),
    )


@pytest.mark.parametrize("transform", TRANSFORMS)
def test_cartesian_decomposition_reconstructs_and_commutes_with_e3(
    transform
):
    isotropic, traceless, antisymmetric = (
        TENSOR.cartesian_decomposition()
    )

    _assert_tensor_close(
        TENSOR,
        _sum_tensors(isotropic, traceless, antisymmetric),
    )

    assert isotropic.trace == pytest.approx(TENSOR.trace)
    assert traceless.trace == pytest.approx(0.0, abs=1.0e-12)
    assert antisymmetric.trace == pytest.approx(0.0, abs=1.0e-12)

    for i in range(3):
        for j in range(3):
            assert isotropic.rows[i][j] == pytest.approx(
                TENSOR.trace / 3 if i == j else 0.0
            )
            assert traceless.rows[i][j] == pytest.approx(
                traceless.rows[j][i]
            )
            assert antisymmetric.rows[i][j] == pytest.approx(
                -antisymmetric.rows[j][i]
            )

    actual = TENSOR.transformed(
        transform
    ).cartesian_decomposition()

    for part, transformed_part in zip(
        (isotropic, traceless, antisymmetric),
        actual,
        strict=True,
    ):
        _assert_tensor_close(
            transformed_part,
            part.transformed(transform).rows,
        )


def test_decomposition_parts_are_orthogonal_in_frobenius_product():
    iso, sym, anti = TENSOR.cartesian_decomposition()

    for left, right in (
        (iso, sym),
        (iso, anti),
        (sym, anti),
    ):
        assert left.double_contract(right) == pytest.approx(
            0.0, abs=1.0e-12
        )

    assert sum(
        part.frobenius_norm_squared
        for part in (iso, sym, anti)
    ) == pytest.approx(TENSOR.frobenius_norm_squared)


def test_group_composition_and_inverse_actions():
    first = E3Transformation(ROT_Z, (2.0, 4.0, 1.0))
    second = E3Transformation(ROT_X, (-1.0, 3.0, 5.0))

    composed = E3Transformation(_matmul(ROT_X, ROT_Z))

    _assert_tensor_close(
        TENSOR.transformed(first).transformed(second),
        TENSOR.transformed(composed).rows,
    )

    inverse = E3Transformation(_transpose(ROT_Z))

    _assert_tensor_close(
        TENSOR.transformed(first).transformed(inverse),
        TENSOR.rows,
    )


def test_translation_never_affects_internal_tensor_channels():
    no_shift = E3Transformation(ROT_Z)
    shifted = E3Transformation(
        ROT_Z, (100.0, -250.0, 35.0)
    )

    assert TENSOR.transformed(no_shift) == TENSOR.transformed(
        shifted
    )

    assert SECOND.transformed(no_shift) == SECOND.transformed(
        shifted
    )

    assert TENSOR.transformed(
        E3Transformation(
            IDENTITY, (10.0, 20.0, -3.0)
        )
    ) == TENSOR


def test_inversion_is_even_for_polar_rank_two_and_odd_for_polar_vectors():
    inversion = E3Transformation(INVERT)

    _assert_tensor_close(
        TENSOR.transformed(inversion),
        TENSOR.rows,
    )

    assert inversion.transform_vector(
        (1.0, -2.0, 3.0)
    ) == (-1.0, 2.0, -3.0)


def test_known_outer_product_rotates_xx_into_yy():
    xx = RankTwoTensor.outer(
        (1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    )
    yy = RankTwoTensor.outer(
        (0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0),
    )

    assert xx.transformed(E3Transformation(ROT_Z)) == yy
    assert xx.trace == yy.trace == 1.0
    assert (
        xx.frobenius_norm_squared
        == yy.frobenius_norm_squared
        == 1.0
    )


@pytest.mark.parametrize("transform", TRANSFORMS)
def test_aligned_scalar_vector_tensor_features_transform_consistently(
    transform
):
    base = _base_features()
    tensors = _rank_two_features()

    bundle = ScalarVectorTensorFeatures(
        base=base,
        rank_two=tensors,
    )

    transformed = bundle.transformed(transform)

    assert bundle.node_count == transformed.node_count == 3

    assert (
        tensors.tensor_channel_count
        == transformed.rank_two.tensor_channel_count
        == 2
    )

    assert transformed.base == transform.transform_feature_vector(
        base
    )

    assert transformed.rank_two == tensors.transformed(transform)

    assert (
        transformed.base.scalar_channel_count
        == base.scalar_channel_count
    )

    assert (
        transformed.base.vector_channel_count
        == base.vector_channel_count
    )

    for old, new in zip(
        tensors.nodes,
        transformed.rank_two.nodes,
        strict=True,
    ):
        for original, observed in zip(old, new, strict=True):
            _assert_tensor_close(
                observed,
                _reference_action(original, transform.matrix),
            )

    for old, new in zip(
        base.nodes,
        transformed.base.nodes,
        strict=True,
    ):
        assert new.scalars == old.scalars

        for a, b in zip(new.vectors, old.vectors, strict=True):
            assert a == pytest.approx(
                transform.transform_vector(b)
            )


def test_feature_bundle_group_composition_does_not_lose_channels():
    bundle = ScalarVectorTensorFeatures(
        _base_features(),
        _rank_two_features(),
    )

    first = E3Transformation(ROT_Z)
    second = E3Transformation(REFLECT_X)
    composed = E3Transformation(
        _matmul(REFLECT_X, ROT_Z)
    )

    lhs = bundle.transformed(first).transformed(second)
    rhs = bundle.transformed(composed)

    assert lhs.base.node_count == rhs.base.node_count
    assert (
        lhs.base.scalar_channel_count
        == rhs.base.scalar_channel_count
    )
    assert (
        lhs.rank_two.tensor_channel_count
        == rhs.rank_two.tensor_channel_count
    )

    for anode, bnode in zip(
        lhs.base.nodes,
        rhs.base.nodes,
        strict=True,
    ):
        assert anode.scalars == pytest.approx(bnode.scalars)

        for av, bv in zip(anode.vectors, bnode.vectors, strict=True):
            assert av == pytest.approx(bv, abs=1.0e-12)

    for anode, bnode in zip(
        lhs.rank_two.nodes,
        rhs.rank_two.nodes,
        strict=True,
    ):
        for a, b in zip(anode, bnode, strict=True):
            _assert_tensor_close(a, b.rows)


@pytest.mark.parametrize("rows,exception", (
    ([list(row) for row in TENSOR.rows], TypeError),
    ((), ValueError),
    (
        ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        ValueError,
    ),
    (
        ((1.0, 0.0, 0.0), (0.0, 1.0), (0.0, 0.0, 1.0)),
        ValueError,
    ),
    (
        ((1.0, 0.0, 0.0), [0.0, 1.0, 0.0], (0.0, 0.0, 1.0)),
        TypeError,
    ),
    (
        ((1.0, 0.0, 0.0), (0.0, True, 0.0), (0.0, 0.0, 1.0)),
        TypeError,
    ),
    (
        (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, float("nan")),
        ),
        ValueError,
    ),
    (
        (
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, float("inf")),
        ),
        ValueError,
    ),
))
def test_tensor_rejects_invalid_shape_type_or_nonfinite_components(
    rows, exception
):
    with pytest.raises(exception):
        RankTwoTensor(rows)


@pytest.mark.parametrize("vector,exception", (
    ([1.0, 2.0, 3.0], TypeError),
    ((1.0, 2.0), ValueError),
    ((1.0, False, 3.0), TypeError),
    ((1.0, float("nan"), 3.0), ValueError),
    ((1.0, 2.0, float("-inf")), ValueError),
))
def test_outer_product_rejects_invalid_vector(vector, exception):
    with pytest.raises(exception):
        RankTwoTensor.outer(
            vector, (1.0, 0.0, 0.0)
        )

    with pytest.raises(exception):
        RankTwoTensor.outer(
            (1.0, 0.0, 0.0), vector
        )


@pytest.mark.parametrize("nodes,exception", (
    ([], TypeError),
    ((), ValueError),
    (((),), ValueError),
    (([TENSOR],), TypeError),
    (((TENSOR,), (TENSOR, SECOND)), ValueError),
    (((TENSOR,), ("tensor",)), TypeError),
))
def test_rank_two_feature_vector_rejects_invalid_nodes(
    nodes, exception
):
    with pytest.raises(exception):
        RankTwoFeatureVector(nodes)


def test_feature_alignment_and_type_contracts():
    base = _base_features()
    tensors = _rank_two_features()

    assert (
        RankTwoFeatureVector(tensors.nodes).node_count
        == base.node_count
    )

    assert all(len(node) == 2 for node in tensors.nodes)

    with pytest.raises(ValueError, match="node counts"):
        ScalarVectorTensorFeatures(
            NodeFeatureVector(nodes=base.nodes[:2]),
            tensors,
        )

    with pytest.raises(TypeError, match="base"):
        ScalarVectorTensorFeatures(
            base=None,
            rank_two=tensors,
        )

    with pytest.raises(TypeError, match="rank_two"):
        ScalarVectorTensorFeatures(
            base=base,
            rank_two=None,
        )

    with pytest.raises(TypeError):
        TENSOR.double_contract(None)

    with pytest.raises(TypeError):
        TENSOR.transformed(None)

    with pytest.raises(TypeError):
        tensors.transformed(None)

    with pytest.raises(TypeError):
        ScalarVectorTensorFeatures(
            base, tensors
        ).transformed(None)


def test_repeated_transform_is_deterministic_and_records_are_immutable():
    bundle = ScalarVectorTensorFeatures(
        _base_features(),
        _rank_two_features(),
    )

    transform = TRANSFORMS[1]

    assert bundle.transformed(transform) == bundle.transformed(
        transform
    )

    assert all(
        isfinite(t.trace) and isfinite(t.frobenius_norm_squared)
        for node in bundle.rank_two.nodes
        for t in node
    )

    with pytest.raises(FrozenInstanceError):
        TENSOR.rows = ((0.0, 0.0, 0.0),) * 3

    with pytest.raises(FrozenInstanceError):
        bundle.rank_two.nodes = ()

    with pytest.raises(FrozenInstanceError):
        bundle.base = _base_features()

    with pytest.raises(ValueError):
        replace(
            bundle,
            rank_two=RankTwoFeatureVector(
                nodes=((TENSOR,),)
            ),
        )
