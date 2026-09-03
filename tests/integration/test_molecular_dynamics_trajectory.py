"""Integration tests for TR-EIF molecular-dynamics trajectories."""

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
from tr_eif.md import MolecularDynamicsState
from tr_eif.md.trajectory import run_velocity_verlet_trajectory
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


def _make_initial_state() -> MolecularDynamicsState:
    """Construct the deterministic trajectory initial state."""

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
        step=5,
        time=0.50,
    )


def _make_features() -> NodeFeatureVector:
    """Construct invariant scalar features for the trajectory fixture."""

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
    """Construct fixed retained ternary execution input."""

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
    """Construct the conservative central-difference force evaluator."""

    return ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )


def _run_trajectory(step_count: int = 4):
    """Execute one deterministic multi-step trajectory fixture."""

    return run_velocity_verlet_trajectory(
        initial_state=_make_initial_state(),
        model=_make_model(),
        force_evaluator=_make_force_evaluator(),
        features=_make_features(),
        execution=_make_execution(),
        cutoff=2.0,
        time_step=0.01,
        step_count=step_count,
    )


def test_trajectory_contains_requested_number_of_steps() -> None:
    """Trajectory length must equal the requested integration count."""

    trajectory = _run_trajectory(step_count=4)

    assert trajectory.step_count == 4
    assert len(trajectory.steps) == 4
    assert len(trajectory.states) == 5


def test_trajectory_states_are_continuous() -> None:
    """Each step must begin at the preceding step's current state."""

    trajectory = _run_trajectory(step_count=4)

    for index in range(1, trajectory.step_count):
        assert (
            trajectory.steps[index].previous
            == trajectory.steps[index - 1].current
        )

    for index, step in enumerate(trajectory.steps):
        assert trajectory.states[index] == step.previous
        assert trajectory.states[index + 1] == step.current


def test_trajectory_advances_step_indices_exactly() -> None:
    """Every trajectory state must advance the discrete clock by one."""

    trajectory = _run_trajectory(step_count=4)

    assert tuple(
        state.step
        for state in trajectory.states
    ) == (
        5,
        6,
        7,
        8,
        9,
    )

    assert trajectory.initial.step == 5
    assert trajectory.final.step == 9


def test_trajectory_advances_time_monotonically() -> None:
    """Every trajectory step must advance time by the configured timestep."""

    trajectory = _run_trajectory(step_count=4)

    expected_times = (
        0.50,
        0.51,
        0.52,
        0.53,
        0.54,
    )

    for state, expected_time in zip(
        trajectory.states,
        expected_times,
        strict=True,
    ):
        assert state.time == pytest.approx(expected_time)


def test_trajectory_preserves_static_configuration_metadata() -> None:
    """Species, cell, periodic axes, and masses must persist."""

    trajectory = _run_trajectory(step_count=4)

    initial = trajectory.initial

    for state in trajectory.states:
        assert (
            state.configuration.species
            == initial.configuration.species
        )
        assert state.configuration.cell == initial.configuration.cell
        assert (
            state.configuration.periodic
            == initial.configuration.periodic
        )
        assert state.masses == initial.masses


def test_trajectory_produces_dynamic_coordinate_evolution() -> None:
    """A nonstationary fixture must evolve positions and velocities."""

    trajectory = _run_trajectory(step_count=4)

    assert (
        trajectory.final.configuration.positions
        != trajectory.initial.configuration.positions
    )

    assert trajectory.final.velocities != trajectory.initial.velocities


def test_repeated_trajectory_execution_is_deterministic() -> None:
    """Identical trajectory inputs must produce identical results."""

    first = _run_trajectory(step_count=4)
    second = _run_trajectory(step_count=4)

    assert first == second
    assert first.states == second.states
    assert first.steps == second.steps


def test_each_trajectory_step_has_force_and_graph_boundaries() -> None:
    """Every step must retain both force and interaction-graph boundaries."""

    trajectory = _run_trajectory(step_count=4)

    for step in trajectory.steps:
        assert (
            step.graph_before.node_count
            == trajectory.atom_count
        )
        assert (
            step.graph_after.node_count
            == trajectory.atom_count
        )

        assert (
            step.forces_before.atom_count
            == trajectory.atom_count
        )
        assert (
            step.forces_after.atom_count
            == trajectory.atom_count
        )


def test_fixed_ternary_execution_input_is_not_mutated() -> None:
    """MD trajectory execution must not mutate retained ternary input."""

    execution = _make_execution()

    trajectory = run_velocity_verlet_trajectory(
        initial_state=_make_initial_state(),
        model=_make_model(),
        force_evaluator=_make_force_evaluator(),
        features=_make_features(),
        execution=execution,
        cutoff=2.0,
        time_step=0.01,
        step_count=4,
    )

    assert execution.retained_states == (
        TernaryState.NEUTRAL,
        TernaryState.NEUTRAL,
    )

    assert trajectory.atom_count == execution.node_count


@pytest.mark.parametrize(
    "invalid_step_count",
    (
        0,
        -1,
        -10,
    ),
)
def test_trajectory_requires_positive_step_count(
    invalid_step_count: int,
) -> None:
    """Trajectory execution must contain at least one MD step."""

    with pytest.raises(
        ValueError,
        match="step_count must be greater than zero",
    ):
        _run_trajectory(
            step_count=invalid_step_count,
        )
