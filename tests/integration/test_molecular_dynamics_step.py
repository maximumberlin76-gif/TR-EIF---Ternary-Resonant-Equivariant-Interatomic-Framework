"""Integration tests for TR-EIF force-driven molecular dynamics."""

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
from tr_eif.md.execution import velocity_verlet_step
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


def _make_state() -> MolecularDynamicsState:
    """Construct a periodic two-atom molecular-dynamics state."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(
            True,
            True,
            True,
        ),
    )

    return MolecularDynamicsState(
        configuration=configuration,
        velocities=(
            (0.01, 0.0, 0.0),
            (-0.01, 0.0, 0.0),
        ),
        masses=(
            1.0,
            2.0,
        ),
        step=3,
        time=0.30,
    )


def _make_features() -> NodeFeatureVector:
    """Construct one invariant scalar channel per atom."""

    return NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0,),
            ),
            NodeFeatures(
                scalars=(1.0,),
            ),
        )
    )


def _make_execution() -> TernaryExecutionVector:
    """Construct retained active-neutral execution states."""

    return TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEUTRAL,
            TernaryState.NEUTRAL,
        )
    )


def _make_model() -> ReferenceEnergyModel:
    """Construct the reference coordinate-dependent energy model."""

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


def _make_force_evaluator() -> ConservativeForceEvaluator:
    """Construct the central-difference conservative force evaluator."""

    return ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )


def _execute_step():
    """Execute one deterministic velocity-Verlet integration step."""

    return velocity_verlet_step(
        state=_make_state(),
        model=_make_model(),
        force_evaluator=_make_force_evaluator(),
        features=_make_features(),
        execution=_make_execution(),
        cutoff=2.0,
        time_step=0.01,
    )


def test_velocity_verlet_step_advances_step_and_time() -> None:
    """One MD execution must advance the discrete and continuous clocks."""

    result = _execute_step()

    assert result.previous.step == 3
    assert result.current.step == 4

    assert result.previous.time == pytest.approx(0.30)
    assert result.current.time == pytest.approx(0.31)


def test_velocity_verlet_step_preserves_static_configuration_metadata() -> None:
    """Species, cell, periodic axes, and masses must survive one MD step."""

    result = _execute_step()

    assert (
        result.current.configuration.species
        == result.previous.configuration.species
    )
    assert (
        result.current.configuration.cell
        == result.previous.configuration.cell
    )
    assert (
        result.current.configuration.periodic
        == result.previous.configuration.periodic
    )
    assert result.current.masses == result.previous.masses


def test_velocity_verlet_step_updates_positions_and_velocities() -> None:
    """Force-driven Verlet execution must update dynamic state variables."""

    result = _execute_step()

    assert (
        result.current.configuration.positions
        != result.previous.configuration.positions
    )
    assert result.current.velocities != result.previous.velocities


def test_velocity_verlet_step_returns_atomwise_forces_at_both_states() -> None:
    """The step result must expose force evaluations before and after drift."""

    result = _execute_step()

    assert result.forces_before.atom_count == result.previous.atom_count
    assert result.forces_after.atom_count == result.current.atom_count

    for force_state in (
        result.forces_before,
        result.forces_after,
    ):
        for force in force_state.forces:
            for component in force:
                assert component == pytest.approx(component)
                assert abs(component) < float("inf")


def test_velocity_verlet_step_reevaluates_forces_after_drift() -> None:
    """Changed coordinates must receive a second force evaluation."""

    result = _execute_step()

    assert result.forces_after.forces != result.forces_before.forces


def test_velocity_verlet_step_returns_graphs_for_both_time_states() -> None:
    """Interaction graphs must correspond to both MD time boundaries."""

    result = _execute_step()

    assert result.graph_before.node_count == result.previous.atom_count
    assert result.graph_after.node_count == result.current.atom_count

    assert result.graph_before.edges == (
        result.graph_after.edges
    )


def test_velocity_verlet_step_preserves_active_neutral_execution_input() -> None:
    """MD coordinate evolution must not reinterpret active neutral as missing."""

    execution = _make_execution()

    result = velocity_verlet_step(
        state=_make_state(),
        model=_make_model(),
        force_evaluator=_make_force_evaluator(),
        features=_make_features(),
        execution=execution,
        cutoff=2.0,
        time_step=0.01,
    )

    assert execution.retained_states == (
        TernaryState.NEUTRAL,
        TernaryState.NEUTRAL,
    )

    assert result.current.atom_count == execution.node_count
