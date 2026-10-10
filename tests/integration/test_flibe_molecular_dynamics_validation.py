"""Integration validation of FLiBe TR-EIP molecular-dynamics execution."""

from math import pi

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
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.mass import FLiBeMassParameters, configuration_masses
from tr_eif.flibe.resonance_descriptor import (
    FLiBeResonanceDescriptor,
    build_flibe_resonance_descriptor,
)
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import run_velocity_verlet_trajectory
from tr_eif.md.trajectory_observables import evaluate_trajectory_energy
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)


CUTOFF = 1.6
TIME_STEP = 1.0e-3
STEP_COUNT = 5


def _configuration() -> FLiBeConfiguration:
    """Construct a non-collinear exact 2 LiF : 1 BeF2 test fixture."""

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=(
                "Li",
                "Li",
                "Be",
                "F",
                "F",
                "F",
                "F",
            ),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.4, 0.9, 0.2),
                (0.2, 0.3, 1.0),
                (1.1, 0.7, 0.8),
                (1.7, 0.2, 0.5),
                (0.8, 1.5, 0.4),
            ),
        )
    )


def _features() -> NodeFeatureVector:
    """Construct scalar-plus-polar-vector base node features."""

    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(
                scalars=(0.5 + 0.25 * index,),
                vectors=((1.0, 0.1 * index, -0.05 * index),),
            )
            for index in range(7)
        )
    )


def _execution() -> TernaryExecutionVector:
    """Construct retained balanced -1/0/1 execution state."""

    return TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
        )
    )


def _resonance_state() -> ResonanceState:
    """Construct one deterministic continuous resonance state."""

    return ResonanceState(
        phases=(
            0.0,
            0.25 * pi,
            0.5 * pi,
            0.75 * pi,
            pi,
            1.25 * pi,
            1.5 * pi,
        ),
        frequencies=(
            -0.3,
            -0.2,
            -0.1,
            0.0,
            0.1,
            0.2,
            0.3,
        ),
    )


def _descriptor(
    configuration: FLiBeConfiguration,
    resonance_state: ResonanceState | None = None,
) -> FLiBeResonanceDescriptor:
    """Build explicit FLiBe resonance context for one configuration."""

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

    return build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(
            configuration,
            graph,
        ),
        thermodynamic_state=FLiBeThermodynamicState(
            temperature=1000.0,
            pressure=0.0,
        ),
        resonance_state=(
            _resonance_state()
            if resonance_state is None
            else resonance_state
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _energy_model() -> ReferenceEnergyModel:
    """Construct the deterministic conditioned equivariant energy model."""

    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(
            distance_scale=1.1,
        ),
        conditioning=TernaryConditioning(
            negative_scale=0.5,
            neutral_scale=1.25,
            positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3),
            bias=0.1,
        ),
    )


def _tr_eip_model() -> FLiBeTREIPModel:
    """Construct one test-fixture FLiBe TR-EIP realization."""

    return FLiBeTREIPModel(
        energy_model=_energy_model(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _force_evaluator() -> ConservativeForceEvaluator:
    """Construct the fixed-graph conservative-force evaluator."""

    return ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )


def _md_state(
    configuration: FLiBeConfiguration,
) -> MolecularDynamicsState:
    """Construct an MD state using explicit test-fixture mass parameters."""

    masses = configuration_masses(
        configuration,
        FLiBeMassParameters(
            lithium=1.0,
            beryllium=2.0,
            fluorine=3.0,
        ),
    )

    velocities = tuple(
        (
            1.0e-3 * (index + 1),
            -5.0e-4 * index,
            2.5e-4 * (index % 3),
        )
        for index in range(configuration.atom_count)
    )

    return MolecularDynamicsState(
        configuration=configuration.configuration,
        velocities=velocities,
        masses=masses,
    )


def _trajectory_bundle():
    """Execute the deterministic FLiBe TR-EIP-driven MD fixture."""

    configuration = _configuration()
    model = _tr_eip_model()
    descriptor = _descriptor(configuration)
    execution = _execution()

    tr_eip_result = model.evaluate(
        configuration=configuration,
        graph=build_cutoff_graph(
            configuration.configuration,
            cutoff=CUTOFF,
        ),
        features=_features(),
        resonance=descriptor,
        execution=execution,
    )

    trajectory = run_velocity_verlet_trajectory(
        initial_state=_md_state(configuration),
        model=model.energy_model,
        force_evaluator=_force_evaluator(),
        features=tr_eip_result.resonance_conditioned_features,
        execution=execution,
        cutoff=CUTOFF,
        time_step=TIME_STEP,
        step_count=STEP_COUNT,
    )

    energy = evaluate_trajectory_energy(
        trajectory=trajectory,
        model=model.energy_model,
        features=tr_eip_result.resonance_conditioned_features,
        execution=execution,
        cutoff=CUTOFF,
    )

    return (
        configuration,
        model,
        descriptor,
        execution,
        tr_eip_result,
        trajectory,
        energy,
    )


def test_tr_eip_conditioned_energy_drives_md_force_evaluation() -> None:
    """MD forces must use the same resonance-augmented conditioned energy path."""

    (
        configuration,
        model,
        _,
        execution,
        tr_eip_result,
        trajectory,
        _,
    ) = _trajectory_bundle()

    direct = _force_evaluator().evaluate(
        model=model.energy_model,
        configuration=configuration.configuration,
        graph=build_cutoff_graph(
            configuration.configuration,
            cutoff=CUTOFF,
        ),
        features=tr_eip_result.resonance_conditioned_features,
        execution=execution,
    )

    assert trajectory.steps[0].forces_before == direct


def test_md_trajectory_preserves_flibe_composition() -> None:
    """MD coordinate evolution must preserve the exact FLiBe species composition."""

    *_, trajectory, _ = _trajectory_bundle()

    for state in trajectory.states:
        flibe = FLiBeConfiguration(
            configuration=state.configuration
        )
        composition = flibe.composition()

        assert composition.lif_fraction == pytest.approx(
            2.0 / 3.0
        )
        assert composition.bef2_fraction == pytest.approx(
            1.0 / 3.0
        )


def test_md_trajectory_preserves_atom_identity_and_cardinality() -> None:
    """Velocity-Verlet must retain FLiBe species order and atom count."""

    configuration, *_, trajectory, _ = _trajectory_bundle()

    for state in trajectory.states:
        assert state.atom_count == configuration.atom_count
        assert (
            state.configuration.species
            == configuration.configuration.species
        )


def test_md_trajectory_uses_explicit_frozen_resonance_channels() -> None:
    """One MD trajectory must not silently evolve the resonance descriptor."""

    (
        _,
        _,
        descriptor,
        _,
        tr_eip_result,
        trajectory,
        _,
    ) = _trajectory_bundle()

    expected = descriptor.coordinate

    for state in trajectory.states:
        rebound = _descriptor(
            FLiBeConfiguration(
                configuration=state.configuration
            ),
            resonance_state=descriptor.resonance_state,
        )

        assert rebound.coordinate == pytest.approx(
            expected
        )

    for node in tr_eip_result.resonance_conditioned_features.nodes:
        assert node.scalars[-2:] == pytest.approx(
            expected
        )


def test_md_trajectory_does_not_execute_ternary_transitions() -> None:
    """MD propagation must consume retained ternary state without changing it."""

    _, _, _, execution, _, trajectory, _ = _trajectory_bundle()

    retained = execution.retained_states

    assert execution.has_pending_targets is False
    assert retained == (
        TernaryState.NEGATIVE,
        TernaryState.NEUTRAL,
        TernaryState.POSITIVE,
        TernaryState.NEUTRAL,
        TernaryState.NEGATIVE,
        TernaryState.POSITIVE,
        TernaryState.NEUTRAL,
    )
    assert trajectory.step_count == STEP_COUNT
    assert execution.retained_states == retained


def test_pending_target_does_not_replace_executed_neutral_in_md_force_path(
) -> None:
    """MD forces must depend on retained state, not an unexecuted target."""

    configuration = _configuration()
    model = _tr_eip_model()
    descriptor = _descriptor(configuration)
    features = _features()

    base_states = list(
        _execution().states
    )

    base_states[1] = TernaryExecutionState(
        retained_state=TernaryState.NEUTRAL,
    )
    without_pending = TernaryExecutionVector(
        states=tuple(base_states)
    )

    base_states[1] = TernaryExecutionState(
        retained_state=TernaryState.NEUTRAL,
        pending_target=TernaryState.POSITIVE,
    )
    with_pending = TernaryExecutionVector(
        states=tuple(base_states)
    )

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

    augmented = model.evaluate(
        configuration,
        graph,
        features,
        descriptor,
        without_pending,
    ).resonance_conditioned_features

    evaluator = _force_evaluator()

    first = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        augmented,
        without_pending,
    )
    second = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        augmented,
        with_pending,
    )

    assert first == second


def test_resonance_changes_md_forces_with_fixed_ternary_state() -> None:
    """Continuous resonance must have an executable pathway into MD forces."""

    configuration = _configuration()
    model = _tr_eip_model()
    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )
    execution = _execution()
    features = _features()

    first_descriptor = _descriptor(
        configuration
    )
    second_descriptor = _descriptor(
        configuration,
        resonance_state=ResonanceState(
            phases=(0.0,) * 7,
            frequencies=(0.0,) * 7,
        ),
    )

    first_features = model.evaluate(
        configuration,
        graph,
        features,
        first_descriptor,
        execution,
    ).resonance_conditioned_features

    second_features = model.evaluate(
        configuration,
        graph,
        features,
        second_descriptor,
        execution,
    ).resonance_conditioned_features

    evaluator = _force_evaluator()

    first_forces = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        first_features,
        execution,
    )
    second_forces = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        second_features,
        execution,
    )

    assert (
        first_descriptor.coordinate
        != second_descriptor.coordinate
    )
    assert first_forces != second_forces


def test_ternary_state_changes_md_forces_with_fixed_resonance() -> None:
    """Retained -1/0/1 conditioning must independently alter MD forces."""

    configuration = _configuration()
    model = _tr_eip_model()
    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )
    descriptor = _descriptor(configuration)
    features = _features()

    negative = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEGATIVE,) * 7
    )
    positive = TernaryExecutionVector.from_retained_states(
        (TernaryState.POSITIVE,) * 7
    )

    augmented = model.evaluate(
        configuration,
        graph,
        features,
        descriptor,
        negative,
    ).resonance_conditioned_features

    evaluator = _force_evaluator()

    negative_forces = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        augmented,
        negative,
    )
    positive_forces = evaluator.evaluate(
        model.energy_model,
        configuration.configuration,
        graph,
        augmented,
        positive,
    )

    assert negative_forces != positive_forces


def test_post_step_tr_eip_requires_explicit_resonance_rebinding() -> None:
    """A moved MD configuration cannot reuse a descriptor bound to old geometry."""

    (
        _,
        model,
        descriptor,
        execution,
        _,
        trajectory,
        _,
    ) = _trajectory_bundle()

    current = FLiBeConfiguration(
        configuration=trajectory.final.configuration
    )
    graph = build_cutoff_graph(
        current.configuration,
        cutoff=CUTOFF,
    )

    with pytest.raises(
        ValueError,
        match=(
            "resonance descriptor configuration must match "
            "TR-EIP configuration"
        ),
    ):
        model.evaluate(
            current,
            graph,
            _features(),
            descriptor,
            execution,
        )


def test_explicit_post_step_rebinding_matches_md_potential_energy() -> None:
    """Explicit descriptor rebinding must reproduce the frozen-resonance path."""

    (
        _,
        model,
        descriptor,
        execution,
        _,
        trajectory,
        energy,
    ) = _trajectory_bundle()

    current = FLiBeConfiguration(
        configuration=trajectory.final.configuration
    )
    graph = build_cutoff_graph(
        current.configuration,
        cutoff=CUTOFF,
    )
    rebound = _descriptor(
        current,
        resonance_state=descriptor.resonance_state,
    )

    result = model.evaluate(
        current,
        graph,
        _features(),
        rebound,
        execution,
    )

    assert rebound.coordinate == pytest.approx(
        descriptor.coordinate
    )
    assert (
        result.energy_result.energy
        == energy.final.potential
    )


def test_reference_flibe_md_total_energy_drift_is_bounded() -> None:
    """The frozen-state FLiBe MD fixture must bound total-energy drift."""

    *_, energy = _trajectory_bundle()

    drift = (
        energy.final.total_energy
        - energy.initial.total_energy
    )

    assert abs(drift) < 1.0e-9


def test_reference_flibe_md_fixture_is_deterministic() -> None:
    """Identical FLiBe TR-EIP MD inputs must reproduce the same trajectory."""

    first = _trajectory_bundle()
    second = _trajectory_bundle()

    assert first[-2] == second[-2]
    assert first[-1] == second[-1]
