"""Qualification tests for TR-EIF E(3)-invariant energy evaluation."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.graph import build_cutoff_graph
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


def _make_reference_system() -> tuple[
    AtomicConfiguration,
    NodeFeatureVector,
    TernaryExecutionVector,
]:
    """Construct a non-collinear three-atom reference system."""

    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.25, 1.0, 0.5),
        ),
    )

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0, 0.5),
                vectors=((1.0, 0.0, 0.0),),
            ),
            NodeFeatures(
                scalars=(-0.5, 2.0),
                vectors=((0.0, 1.0, 0.0),),
            ),
            NodeFeatures(
                scalars=(1.5, -1.0),
                vectors=((0.0, 0.0, 1.0),),
            ),
        )
    )

    execution = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
        )
    )

    return configuration, features, execution


def _make_energy_model() -> ReferenceEnergyModel:
    """Construct the reference invariant energy model."""

    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(
            distance_scale=1.25,
        ),
        conditioning=TernaryConditioning(
            negative_scale=0.75,
            neutral_scale=1.0,
            positive_scale=1.25,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(1.5, -0.25),
            bias=0.125,
        ),
    )


def _transform_configuration(
    configuration: AtomicConfiguration,
    transformation: E3Transformation,
) -> AtomicConfiguration:
    """Apply an E(3) transformation to atomic positions."""

    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(
            transformation.transform_position(position)
            for position in configuration.positions
        ),
        cell=None,
        periodic=configuration.periodic,
    )


def _evaluate(
    configuration: AtomicConfiguration,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
) -> float:
    """Evaluate total energy with a graph rebuilt from the configuration."""

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.5,
    )

    result = _make_energy_model().evaluate(
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    )

    return result.energy.total_energy


@pytest.mark.parametrize(
    "transformation",
    (
        E3Transformation(
            matrix=(
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(4.0, -3.0, 2.0),
        ),
        E3Transformation(
            matrix=(
                (0.0, -1.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(1.0, 2.0, -4.0),
        ),
        E3Transformation(
            matrix=(
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(-2.0, 3.0, 1.0),
        ),
    ),
)
def test_reference_energy_is_invariant_under_e3(
    transformation: E3Transformation,
) -> None:
    """Total scalar energy must be invariant under E(3)."""

    configuration, features, execution = _make_reference_system()

    reference_energy = _evaluate(
        configuration,
        features,
        execution,
    )

    transformed_configuration = _transform_configuration(
        configuration,
        transformation,
    )

    transformed_features = transformation.transform_feature_vector(
        features
    )

    transformed_energy = _evaluate(
        transformed_configuration,
        transformed_features,
        execution,
    )

    assert transformed_energy == pytest.approx(
        reference_energy,
        rel=1.0e-12,
        abs=1.0e-12,
    )


def test_ternary_conditioning_is_preserved_under_spatial_transform() -> None:
    """Spatial transformation must not alter retained ternary semantics."""

    configuration, features, execution = _make_reference_system()

    transformation = E3Transformation(
        matrix=(
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0),
        ),
        translation=(5.0, -2.0, 3.0),
    )

    transformed_configuration = _transform_configuration(
        configuration,
        transformation,
    )

    transformed_features = transformation.transform_feature_vector(
        features
    )

    reference_energy = _evaluate(
        configuration,
        features,
        execution,
    )

    transformed_energy = _evaluate(
        transformed_configuration,
        transformed_features,
        execution,
    )

    assert execution.retained_states == (
        TernaryState.NEGATIVE,
        TernaryState.NEUTRAL,
        TernaryState.POSITIVE,
    )

    assert transformed_energy == pytest.approx(
        reference_energy,
        rel=1.0e-12,
        abs=1.0e-12,
    )
