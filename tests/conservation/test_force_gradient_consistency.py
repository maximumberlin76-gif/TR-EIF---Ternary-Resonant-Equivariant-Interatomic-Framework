"""Qualification tests for TR-EIF conservative force evaluation."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
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


def _make_two_atom_reference_system() -> tuple[
    AtomicConfiguration,
    NodeFeatureVector,
    TernaryExecutionVector,
]:
    """Construct the two-atom analytic reference system."""

    configuration = AtomicConfiguration(
        species=("A", "A"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
    )

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0,),
            ),
            NodeFeatures(
                scalars=(1.0,),
            ),
        )
    )

    execution = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEUTRAL,
            TernaryState.NEUTRAL,
        )
    )

    return configuration, features, execution


def _make_reference_energy_model() -> ReferenceEnergyModel:
    """Construct the analytic radial reference energy model."""

    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(
            distance_scale=1.0,
        ),
        conditioning=TernaryConditioning(
            negative_scale=1.0,
            neutral_scale=1.0,
            positive_scale=1.0,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(1.0,),
            bias=0.0,
        ),
    )


def test_force_matches_analytic_radial_energy_gradient() -> None:
    """Numerical conservative force must match the analytic gradient."""

    configuration, features, execution = (
        _make_two_atom_reference_system()
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    model = _make_reference_energy_model()

    evaluator = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )

    force_state = evaluator.evaluate(
        model=model,
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    )

    assert force_state.forces[0] == pytest.approx(
        (-1.0, 0.0, 0.0),
        abs=1.0e-8,
    )

    assert force_state.forces[1] == pytest.approx(
        (1.0, 0.0, 0.0),
        abs=1.0e-8,
    )


def test_two_atom_internal_forces_sum_to_zero() -> None:
    """The analytic two-atom reference pair must have zero net force."""

    configuration, features, execution = (
        _make_two_atom_reference_system()
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    evaluator = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )

    force_state = evaluator.evaluate(
        model=_make_reference_energy_model(),
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    )

    net_force = tuple(
        force_state.forces[0][component]
        + force_state.forces[1][component]
        for component in range(3)
    )

    assert net_force == pytest.approx(
        (0.0, 0.0, 0.0),
        abs=1.0e-8,
    )


def test_transverse_force_components_are_zero() -> None:
    """A pair aligned with x must have no y or z force component."""

    configuration, features, execution = (
        _make_two_atom_reference_system()
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    evaluator = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )

    force_state = evaluator.evaluate(
        model=_make_reference_energy_model(),
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    )

    for force in force_state.forces:
        assert force[1] == pytest.approx(
            0.0,
            abs=1.0e-10,
        )
        assert force[2] == pytest.approx(
            0.0,
            abs=1.0e-10,
        )
