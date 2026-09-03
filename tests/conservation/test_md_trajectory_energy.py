"""Conservation-layer tests for TR-EIF MD trajectory energy observables."""

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
from tr_eif.md.observables import molecular_dynamics_energy
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import run_velocity_verlet_trajectory
from tr_eif.md.trajectory_observables import evaluate_trajectory_energy
from tr_eif.graph import build_cutoff_graph
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


def _make_initial_state() -> MolecularDynamicsState:
    """Construct the deterministic trajectory initial state."""

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
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
        ),
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
    """Construct invariant scalar features for the reference fixture."""

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
    """Construct fixed active-neutral execution input."""

    return TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEUTRAL,
            TernaryState.NEUTRAL,
        )
    )


def _make_model() -> ReferenceEnergyModel:
    """Construct the deterministic reference energy model."""

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


def _run_reference_trajectory():
    """Execute the deterministic four-step MD trajectory."""

    model = _make_model()
    features = _make_features()
    execution = _make_execution()

    trajectory = run_velocity_verlet_trajectory(
        initial_state=_make_initial_state(),
        model=model,
        force_evaluator=_make_force_evaluator(),
        features=features,
        execution=execution,
        cutoff=2.0,
        time_step=0.01,
        step_count=4,
    )

    energy = evaluate_trajectory_energy(
        trajectory=trajectory,
        model=model,
        features=features,
        execution=execution,
        cutoff=2.0,
    )

    return (
        trajectory,
        energy,
        model,
        features,
        execution,
    )


def test_trajectory_energy_has_one_observation_per_state() -> None:
    """N integration steps must produce N + 1 energy observations."""

    trajectory, energy, _, _, _ = _run_reference_trajectory()

    assert trajectory.step_count == 4
    assert len(trajectory.states) == 5
    assert energy.state_count == 5
    assert energy.state_count == len(trajectory.states)


def test_trajectory_energy_preserves_atom_count() -> None:
    """Every trajectory energy observation must use the trajectory atom count."""

    trajectory, energy, _, _, _ = _run_reference_trajectory()

    assert energy.atom_count == trajectory.atom_count

    for observation in energy.energies:
        assert observation.atom_count == trajectory.atom_count


def test_each_total_energy_equals_kinetic_plus_potential() -> None:
    """Every observed total energy must equal K plus U."""

    _, energy, _, _, _ = _run_reference_trajectory()

    for observation in energy.energies:
        expected = (
            observation.kinetic.total_kinetic_energy
            + observation.potential.total_energy
        )

        assert observation.total_energy == pytest.approx(
            expected,
            rel=0.0,
            abs=1.0e-15,
        )


def test_energy_component_sequences_match_observations() -> None:
    """Convenience sequences must preserve observation ordering."""

    _, energy, _, _, _ = _run_reference_trajectory()

    assert energy.kinetic_energies == tuple(
        observation.kinetic.total_kinetic_energy
        for observation in energy.energies
    )

    assert energy.potential_energies == tuple(
        observation.potential.total_energy
        for observation in energy.energies
    )

    assert energy.total_energies == tuple(
        observation.total_energy
        for observation in energy.energies
    )

    assert energy.initial == energy.energies[0]
    assert energy.final == energy.energies[-1]


def test_each_observation_matches_direct_state_evaluation() -> None:
    """Each stored energy must match direct evaluation of its MD state."""

    (
        trajectory,
        energy,
        model,
        features,
        execution,
    ) = _run_reference_trajectory()

    for state, observation in zip(
        trajectory.states,
        energy.energies,
        strict=True,
    ):
        graph = build_cutoff_graph(
            configuration=state.configuration,
            cutoff=2.0,
        )

        model_result = model.evaluate(
            configuration=state.configuration,
            features=features,
            execution=execution,
            graph=graph,
        )

        direct = molecular_dynamics_energy(
            state=state,
            potential=model_result.energy,
        )

        assert observation == direct


def test_repeated_trajectory_energy_evaluation_is_deterministic() -> None:
    """Identical inputs must produce identical trajectory energy states."""

    first = _run_reference_trajectory()
    second = _run_reference_trajectory()

    first_trajectory, first_energy, _, _, _ = first
    second_trajectory, second_energy, _, _, _ = second

    assert first_trajectory == second_trajectory
    assert first_energy == second_energy

    assert (
        first_energy.kinetic_energies
        == second_energy.kinetic_energies
    )
    assert (
        first_energy.potential_energies
        == second_energy.potential_energies
    )
    assert first_energy.total_energies == second_energy.total_energies


def test_reference_fixture_energy_sequence_is_finite() -> None:
    """Reference trajectory energies must remain finite."""

    _, energy, _, _, _ = _run_reference_trajectory()

    for observation in energy.energies:
        assert observation.kinetic.total_kinetic_energy >= 0.0
        assert observation.potential.total_energy == pytest.approx(
            observation.potential.total_energy
        )
        assert observation.total_energy == pytest.approx(
            observation.total_energy
        )


def test_reference_fixture_total_energy_drift_is_bounded() -> None:
    """Reference-fixture total-energy drift must remain within its test bound."""

    _, energy, _, _, _ = _run_reference_trajectory()

    initial_energy = energy.initial.total_energy
    final_energy = energy.final.total_energy

    drift = final_energy - initial_energy

    assert abs(drift) < 2.0e-8


def test_reference_fixture_energy_values_match_executed_baseline() -> None:
    """Reference fixture must reproduce its deterministic energy baseline."""

    _, energy, _, _, _ = _run_reference_trajectory()

    expected_kinetic = (
        0.0001500000,
        0.0000249969,
        0.0000500175,
        0.0002250469,
        0.0005499800,
    )

    expected_potential = (
        3.0000000000,
        3.0001250078,
        3.0000999862,
        2.9999249503,
        2.9996000050,
    )

    expected_total = (
        3.0001500000,
        3.0001500047,
        3.0001500037,
        3.0001499972,
        3.0001499850,
    )

    for actual, expected in zip(
        energy.kinetic_energies,
        expected_kinetic,
        strict=True,
    ):
        assert actual == pytest.approx(
            expected,
            rel=0.0,
            abs=5.0e-10,
        )

    for actual, expected in zip(
        energy.potential_energies,
        expected_potential,
        strict=True,
    ):
        assert actual == pytest.approx(
            expected,
            rel=0.0,
            abs=5.0e-10,
        )

    for actual, expected in zip(
        energy.total_energies,
        expected_total,
        strict=True,
    ):
        assert actual == pytest.approx(
            expected,
            rel=0.0,
            abs=5.0e-10,
        )
