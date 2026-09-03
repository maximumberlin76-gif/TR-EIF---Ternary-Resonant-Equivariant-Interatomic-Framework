"""Qualification tests for TR-EIF E(3)-equivariant feature transforms."""

import pytest

from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
)


def _assert_vector_close(
    actual: tuple[float, float, float],
    expected: tuple[float, float, float],
) -> None:
    assert actual == pytest.approx(expected)


def test_scalar_features_are_invariant_under_e3_transform() -> None:
    """Scalar channels must remain unchanged under E(3)."""

    features = NodeFeatures(
        scalars=(1.25, -0.5),
        vectors=((1.0, 2.0, 3.0),),
    )

    transformation = E3Transformation(
        matrix=(
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(4.0, -3.0, 2.0),
    )

    transformed = transformation.transform_node_features(features)

    assert transformed.scalars == features.scalars


def test_polar_vector_features_rotate_with_e3_matrix() -> None:
    """Polar-vector channels must transform with the orthogonal matrix."""

    features = NodeFeatures(
        scalars=(2.0,),
        vectors=(
            (1.0, 0.0, 0.0),
            (0.0, 2.0, 1.0),
        ),
    )

    transformation = E3Transformation(
        matrix=(
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )
    )

    transformed = transformation.transform_node_features(features)

    _assert_vector_close(
        transformed.vectors[0],
        (0.0, 1.0, 0.0),
    )
    _assert_vector_close(
        transformed.vectors[1],
        (-2.0, 0.0, 1.0),
    )


def test_translation_does_not_act_on_vector_features() -> None:
    """Translation must not alter polar-vector feature channels."""

    features = NodeFeatures(
        vectors=(
            (1.0, -2.0, 3.0),
        )
    )

    transformation = E3Transformation(
        matrix=(
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(10.0, -20.0, 30.0),
    )

    transformed = transformation.transform_node_features(features)

    assert transformed.vectors == features.vectors


def test_improper_orthogonal_transform_is_supported() -> None:
    """Polar-vector features must also transform under reflections."""

    features = NodeFeatures(
        scalars=(3.0,),
        vectors=(
            (1.0, 2.0, 3.0),
        ),
    )

    reflection = E3Transformation(
        matrix=(
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        )
    )

    transformed = reflection.transform_node_features(features)

    assert transformed.scalars == features.scalars
    _assert_vector_close(
        transformed.vectors[0],
        (-1.0, 2.0, 3.0),
    )


def test_feature_vector_transform_preserves_channel_structure() -> None:
    """E(3) transformation must preserve node and channel counts."""

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0, 2.0),
                vectors=((1.0, 0.0, 0.0),),
            ),
            NodeFeatures(
                scalars=(3.0, 4.0),
                vectors=((0.0, 1.0, 0.0),),
            ),
        )
    )

    transformation = E3Transformation(
        matrix=(
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(5.0, 6.0, 7.0),
    )

    transformed = transformation.transform_feature_vector(features)

    assert transformed.node_count == features.node_count
    assert (
        transformed.scalar_channel_count
        == features.scalar_channel_count
    )
    assert (
        transformed.vector_channel_count
        == features.vector_channel_count
    )

    assert transformed.nodes[0].scalars == features.nodes[0].scalars
    assert transformed.nodes[1].scalars == features.nodes[1].scalars

    _assert_vector_close(
        transformed.nodes[0].vectors[0],
        (0.0, 1.0, 0.0),
    )
    _assert_vector_close(
        transformed.nodes[1].vectors[0],
        (-1.0, 0.0, 0.0),
    )
