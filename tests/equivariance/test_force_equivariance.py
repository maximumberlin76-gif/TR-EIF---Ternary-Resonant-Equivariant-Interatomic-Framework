"""Qualification tests for TR-EIF E(3)-equivariant conservative forces."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
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
    """Construct a non-collinear three-atom force fixture."""

    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.25, 0.0),
            (0.2, 1.1, 0.6),
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
    """Apply an E(3) transformation to a nonperiodic configuration."""

    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(
            transformation.transform_position(position)
            for position in configuration.positions
        ),
        periodic=configuration.periodic,
    )


def _evaluate_forces(
    configuration: AtomicConfiguration,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
):
    """Evaluate conservative forces with a rebuilt deterministic graph."""

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.5,
    )

    evaluator = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )

    return evaluator.evaluate(
        model=_make_energy_model(),
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    ).forces


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
def test_conservative_forces_are_e3_equivariant(
    transformation: E3Transformation,
) -> None:
    """Conservative forces must transform as polar vectors under E(3)."""

    configuration, features, execution = _make_reference_system()

    reference_forces = _evaluate_forces(
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

    transformed_forces = _evaluate_forces(
        transformed_configuration,
        transformed_features,
        execution,
    )

    expected_forces = tuple(
        transformation.transform_vector(force)
        for force in reference_forces
    )

    for actual_force, expected_force in zip(
        transformed_forces,
        expected_forces,
        strict=True,
    ):
        assert actual_force == pytest.approx(
            expected_force,
            rel=1.0e-7,
            abs=1.0e-7,
        )


def test_force_equivariance_preserves_atomwise_force_order() -> None:
    """Spatial transformation must not permute atomwise force records."""

    configuration, features, execution = _make_reference_system()

    transformation = E3Transformation(
        matrix=(
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
            (1.0, 0.0, 0.0),
        ),
        translation=(2.0, -1.0, 3.0),
    )

    reference_forces = _evaluate_forces(
        configuration,
        features,
        execution,
    )

    transformed_forces = _evaluate_forces(
        _transform_configuration(
            configuration,
            transformation,
        ),
        transformation.transform_feature_vector(features),
        execution,
    )

    for atom_index, reference_force in enumerate(reference_forces):
        assert transformed_forces[atom_index] == pytest.approx(
            transformation.transform_vector(reference_force),
            rel=1.0e-7,
            abs=1.0e-7,
        )
