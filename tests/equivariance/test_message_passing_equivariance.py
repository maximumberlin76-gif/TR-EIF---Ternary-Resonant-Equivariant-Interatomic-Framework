"""Qualification tests for TR-EIF E(3)-equivariant message passing."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    message_passing_step,
)
from tr_eif.graph import build_cutoff_graph


def _assert_vector_close(
    actual: tuple[float, float, float],
    expected: tuple[float, float, float],
) -> None:
    assert actual == pytest.approx(expected)


def _transform_configuration(
    configuration: AtomicConfiguration,
    transformation: E3Transformation,
) -> AtomicConfiguration:
    positions = tuple(
        transformation.transform_position(position)
        for position in configuration.positions
    )

    cell = None

    if configuration.cell is not None:
        cell = tuple(
            transformation.transform_vector(vector)
            for vector in configuration.cell
        )

    return AtomicConfiguration(
        species=configuration.species,
        positions=positions,
        cell=cell,
        periodic=configuration.periodic,
    )


def test_message_passing_is_equivariant_under_rotation() -> None:
    """Message passing must commute with a proper spatial rotation."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
    )

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0,),
                vectors=((1.0, 2.0, 0.0),),
            ),
            NodeFeatures(
                scalars=(2.0,),
                vectors=((0.0, 1.0, 3.0),),
            ),
        )
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    operator = RadialMessageOperator(
        distance_scale=1.5,
    )

    reference = message_passing_step(
        configuration=configuration,
        graph=graph,
        features=features,
        operator=operator,
    )

    transformation = E3Transformation(
        matrix=(
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(4.0, -3.0, 2.0),
    )

    transformed_configuration = _transform_configuration(
        configuration,
        transformation,
    )

    transformed_features = transformation.transform_feature_vector(
        features
    )

    transformed_graph = build_cutoff_graph(
        configuration=transformed_configuration,
        cutoff=2.0,
    )

    transformed = message_passing_step(
        configuration=transformed_configuration,
        graph=transformed_graph,
        features=transformed_features,
        operator=operator,
    )

    assert (
        transformed.aggregated.scalar_channel_count
        == reference.aggregated.scalar_channel_count
    )
    assert (
        transformed.aggregated.vector_channel_count
        == reference.aggregated.vector_channel_count
    )

    for reference_node, transformed_node in zip(
        reference.aggregated.nodes,
        transformed.aggregated.nodes,
        strict=True,
    ):
        assert transformed_node.scalars == pytest.approx(
            reference_node.scalars
        )

        for reference_vector, transformed_vector in zip(
            reference_node.vectors,
            transformed_node.vectors,
            strict=True,
        ):
            expected = transformation.transform_vector(
                reference_vector
            )

            _assert_vector_close(
                transformed_vector,
                expected,
            )


def test_message_passing_is_equivariant_under_reflection() -> None:
    """Message passing must commute with an improper transformation."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (-0.5, 0.0, 0.0),
            (0.5, 0.0, 0.0),
        ),
    )

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.5,),
                vectors=((1.0, -2.0, 3.0),),
            ),
            NodeFeatures(
                scalars=(-0.5,),
                vectors=((-1.0, 4.0, 2.0),),
            ),
        )
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    operator = RadialMessageOperator()

    reference = message_passing_step(
        configuration=configuration,
        graph=graph,
        features=features,
        operator=operator,
    )

    reflection = E3Transformation(
        matrix=(
            (-1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        translation=(2.0, 1.0, -1.0),
    )

    transformed_configuration = _transform_configuration(
        configuration,
        reflection,
    )

    transformed_features = reflection.transform_feature_vector(
        features
    )

    transformed_graph = build_cutoff_graph(
        configuration=transformed_configuration,
        cutoff=2.0,
    )

    transformed = message_passing_step(
        configuration=transformed_configuration,
        graph=transformed_graph,
        features=transformed_features,
        operator=operator,
    )

    for reference_node, transformed_node in zip(
        reference.aggregated.nodes,
        transformed.aggregated.nodes,
        strict=True,
    ):
        assert transformed_node.scalars == pytest.approx(
            reference_node.scalars
        )

        for reference_vector, transformed_vector in zip(
            reference_node.vectors,
            transformed_node.vectors,
            strict=True,
        ):
            expected = reflection.transform_vector(
                reference_vector
            )

            _assert_vector_close(
                transformed_vector,
                expected,
            )
