
"""Independent integration qualification of the FLiBe TR-EIP/MD boundary.

The generic TR-EIF multirate executor and the FLiBe-specific TR-EIP energy
interface are evaluated from their own inputs at three explicit boundaries.
The tests preserve resonance, retained ternary, geometric, and thermodynamic
types and independently check active-neutral routing and E(3) covariance.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

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
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.coupled_tr_eip_md import (
    FLiBeTREIPMDCoupledStep,
    execute_flibe_tr_eip_coupled_md_step,
)
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import (
    CoupledMolecularDynamicsState,
    append_md_resonance_features,
    execute_coupled_md_step,
)
from tr_eif.md.execution import velocity_verlet_step
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState, resonance_descriptor
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
    is_direct_opposite_transition,
)

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0), (1.1, 0.7, 0.8), (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
VELOCITIES = (
    (0.01, 0.0, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.01, 0.0),
    (0.0, -0.01, 0.0), (0.0, 0.0, 0.01), (0.0, 0.0, -0.01),
    (0.0, 0.0, 0.0),
)
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
PHASE_PARAMETERS = PhaseDynamicsParameters(
    coupling=(0.35,) * 7, phase_lag=(0.13,) * 7,
)
PHASE_DT = 0.1
MECHANICAL_DT = 1.0e-4
CUTOFF = 1.6
PROVENANCE = ParameterProvenance.TEST_FIXTURE
THERMO = FLiBeThermodynamicState(temperature=850.0, pressure=101325.0)
THRESHOLDS = TernaryTargetThresholds(negative=-0.25, positive=0.5)


def _interpretation(reverse: bool = False) -> FLiBeTernaryInterpretation:
    return FLiBeTernaryInterpretation(
        projection=(ResonanceProjection(-1.0, 0.0) if reverse
                    else ResonanceProjection(1.0, -0.1)),
        thresholds=THRESHOLDS,
        provenance=PROVENANCE,
    )


def _fixture(
    transformation: E3Transformation | None = None,
    retained: TernaryState = TernaryState.NEGATIVE,
):
    positions = POSITIONS
    velocities = VELOCITIES
    if transformation is not None:
        positions = tuple(transformation.transform_position(p) for p in positions)
        velocities = tuple(transformation.transform_vector(v) for v in velocities)
    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(species=SPECIES, positions=positions),
            velocities=velocities, masses=MASSES, step=4, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
            frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (retained,) * 7,
        ),
        resonance_time=0.4, resonance_step_count=2, ternary_event_count=5,
    )
    base_features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        ) for i in range(7)
    ))
    if transformation is not None:
        base_features = transformation.transform_feature_vector(base_features)
    reference_model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    model = FLiBeTREIPModel(energy_model=reference_model, provenance=PROVENANCE)
    inputs = dict(
        model=model,
        force_evaluator=ConservativeForceEvaluator(
            differentiation=CoordinateDifferentiation(step=1.0e-5),
        ),
        base_features=base_features,
        thermodynamic_state=THERMO,
        interpretation=_interpretation(),
        cutoff=CUTOFF,
    )
    return state, inputs


def _run(state, inputs, **schedule):
    return execute_flibe_tr_eip_coupled_md_step(state, **inputs, **schedule)


def _full_schedule():
    return dict(
        phase_parameters=PHASE_PARAMETERS,
        phase_time_step=PHASE_DT,
        ternary_event=True,
        mechanical_time_step=MECHANICAL_DT,
    )


def _independent_energy(state, inputs):
    """Rebuild FLiBe context and evaluate the domain model independently."""
    configuration = FLiBeConfiguration(state.md_state.configuration)
    graph = build_cutoff_graph(state.md_state.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=inputs["thermodynamic_state"],
        resonance_state=state.resonance_state,
        provenance=inputs["model"].provenance,
        source=inputs["model"].source,
    )
    return inputs["model"].evaluate(
        configuration, graph, inputs["base_features"],
        descriptor, state.ternary_execution,
    )


@pytest.fixture(scope="module")
def coupled():
    state, inputs = _fixture()
    return state, inputs, _run(state, inputs, **_full_schedule())


def test_three_energy_boundaries_equal_independent_tr_eip_evaluations(coupled):
    state, inputs, result = coupled
    assert isinstance(result, FLiBeTREIPMDCoupledStep)
    before = _independent_energy(state, inputs)
    event_state = replace(
        state, resonance_state=result.current.resonance_state,
        ternary_execution=result.current.ternary_execution,
    )
    after_events = _independent_energy(event_state, inputs)
    after_mechanics = _independent_energy(result.current, inputs)
    assert result.before_events == before
    assert result.after_events == after_events
    assert result.after_mechanics == after_mechanics
    assert result.before_events.energy_result.energy == result.coupled_step.energy_before_events
    assert result.after_events.energy_result.energy == result.coupled_step.energy_after_events
    assert result.after_mechanics.energy_result.energy == result.coupled_step.energy_after_mechanics
    assert result.event_potential_energy_change == pytest.approx(
        after_events.energy_result.energy.total_energy - before.energy_result.energy.total_energy
    )
    assert result.mechanical_potential_energy_change == pytest.approx(
        after_mechanics.energy_result.energy.total_energy - after_events.energy_result.energy.total_energy
    )


def test_generic_multirate_executor_matches_flibe_domain_wrapper(coupled):
    state, inputs, result = coupled
    direct = execute_coupled_md_step(
        state, model=inputs["model"].energy_model,
        force_evaluator=inputs["force_evaluator"],
        base_features=inputs["base_features"], cutoff=CUTOFF,
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True,
        projection=inputs["interpretation"].projection,
        thresholds=inputs["interpretation"].thresholds,
        mechanical_time_step=MECHANICAL_DT,
    )
    assert result.coupled_step == direct
    assert result.current == direct.current
    assert result.coupled_step.mechanical_update is not None
    assert result.coupled_step.resonance_update is not None
    assert result.coupled_step.ternary_update is not None
    assert result.coupled_step.requested_target is TernaryState.POSITIVE
    assert result.current.resonance_step_count == state.resonance_step_count + 1
    assert result.current.ternary_event_count == state.ternary_event_count + 1
    assert result.current.md_state.step == state.md_state.step + 1


def test_resonance_context_is_continuous_and_thermodynamics_remains_typed(coupled):
    state, inputs, result = coupled
    assert result.before_events.resonance.resonance_state is state.resonance_state
    assert result.after_events.resonance.resonance_state == result.current.resonance_state
    assert result.after_mechanics.resonance.resonance_state == result.current.resonance_state
    assert result.before_events.resonance.coordinate != result.after_events.resonance.coordinate
    for boundary in (result.before_events, result.after_events, result.after_mechanics):
        assert boundary.resonance.thermodynamic_state == THERMO
        assert boundary.resonance.configuration == boundary.configuration
        assert boundary.resonance.coordination == build_flibe_coordination_state(
            boundary.configuration, boundary.graph,
        )
        assert boundary.resonance.phase_order == pytest.approx(
            resonance_descriptor(boundary.resonance.resonance_state).phase_order
        )
        assert boundary.resonance.frequency_spread == pytest.approx(
            resonance_descriptor(boundary.resonance.resonance_state).frequency_spread
        )
        assert boundary.resonance_conditioned_features.scalar_channel_count == 3
        assert boundary.input_features.scalar_channel_count == 1
        for original, augmented in zip(
            boundary.input_features.nodes,
            boundary.resonance_conditioned_features.nodes, strict=True,
        ):
            assert augmented.scalars[:-2] == original.scalars
            assert augmented.vectors == original.vectors


def test_active_neutral_entry_is_committed_before_mechanics(coupled):
    state, _, result = coupled
    step = result.coupled_step.ternary_update
    assert step is not None
    assert result.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert result.current.ternary_execution.has_pending_targets
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in result.current.ternary_execution.states)
    assert result.after_events.execution == result.current.ternary_execution
    assert result.after_mechanics.execution == result.current.ternary_execution
    assert step.committed_count == 7
    for node in step.execution.node_steps:
        assert node.route is not None
        assert node.route.transition.source is TernaryState.NEGATIVE
        assert node.route.transition.target is TernaryState.NEUTRAL
        assert not is_direct_opposite_transition(
            node.route.transition.source, node.route.transition.target,
        )


def test_pending_route_is_held_then_exits_on_a_separate_event():
    state, inputs = _fixture()
    first = _run(state, inputs, ternary_event=True,
                 guards=(TernaryExecutionGuard.neutral_entry_only(),) * 7)
    assert first.current.ternary_execution.has_pending_targets
    changed_interpretation = {**inputs, "interpretation": _interpretation(reverse=True)}
    held = _run(first.current, changed_interpretation, ternary_event=True,
                guards=(TernaryExecutionGuard.hold(),) * 7)
    assert held.coupled_step.ternary_update.committed_count == 0
    assert held.current.ternary_execution == first.current.ternary_execution
    assert held.coupled_step.requested_target is TernaryState.NEGATIVE
    assert held.coupled_step.requested_targets == (TernaryState.POSITIVE,) * 7
    assert held.event_potential_energy_change == 0.0
    final = _run(held.current, changed_interpretation, ternary_event=True,
                 guards=(TernaryExecutionGuard.neutral_exit_only(),) * 7)
    assert final.current.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7
    assert not final.current.ternary_execution.has_pending_targets
    assert final.coupled_step.ternary_update.committed_count == 7
    assert final.current.ternary_event_count == state.ternary_event_count + 3
    assert final.current.md_state == state.md_state


def test_reverse_polarity_passes_through_active_neutral():
    state, inputs = _fixture(retained=TernaryState.POSITIVE)
    inputs["interpretation"] = _interpretation(reverse=True)
    first = _run(state, inputs, ternary_event=True)
    assert first.coupled_step.requested_target is TernaryState.NEGATIVE
    assert first.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(n.pending_target is TernaryState.NEGATIVE for n in first.current.ternary_execution.states)
    second = _run(first.current, inputs, ternary_event=True)
    assert second.current.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert not second.current.ternary_execution.has_pending_targets
    for event in (first, second):
        for node in event.coupled_step.ternary_update.execution.node_steps:
            assert node.route is not None
            assert not is_direct_opposite_transition(
                node.route.transition.source, node.route.transition.target,
            )


def test_phase_only_does_not_run_mechanics_or_ternary():
    state, inputs = _fixture()
    result = _run(state, inputs, phase_parameters=PHASE_PARAMETERS,
                  phase_time_step=PHASE_DT)
    assert result.coupled_step.resonance_update is not None
    assert result.coupled_step.ternary_update is None
    assert result.coupled_step.mechanical_update is None
    assert result.current.md_state == state.md_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.after_mechanics == result.after_events
    assert result.mechanical_potential_energy_change == 0.0
    assert result.current.resonance_time == pytest.approx(state.resonance_time + PHASE_DT)
    assert result.current.ternary_event_count == state.ternary_event_count


def test_ternary_only_does_not_advance_phase_or_mechanics():
    state, inputs = _fixture()
    result = _run(state, inputs, ternary_event=True)
    assert result.coupled_step.resonance_update is None
    assert result.coupled_step.mechanical_update is None
    assert result.current.resonance_state == state.resonance_state
    assert result.current.resonance_time == state.resonance_time
    assert result.current.md_state == state.md_state
    assert result.after_mechanics == result.after_events
    assert result.current.ternary_event_count == state.ternary_event_count + 1
    assert result.event_potential_energy_change == pytest.approx(
        result.after_events.energy_result.energy.total_energy
        - result.before_events.energy_result.energy.total_energy
    )


def test_mechanics_only_matches_reference_verlet_with_frozen_features():
    state, inputs = _fixture()
    result = _run(state, inputs, mechanical_time_step=MECHANICAL_DT)
    features = append_md_resonance_features(
        inputs["base_features"], resonance_descriptor(state.resonance_state)
    )
    direct = velocity_verlet_step(
        state=state.md_state, model=inputs["model"].energy_model,
        force_evaluator=inputs["force_evaluator"], features=features,
        execution=state.ternary_execution, cutoff=CUTOFF,
        time_step=MECHANICAL_DT,
    )
    assert result.coupled_step.mechanical_update == direct
    assert result.current.md_state == direct.current
    assert result.current.resonance_state == state.resonance_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.current.md_state.time == pytest.approx(state.md_state.time + MECHANICAL_DT)
    assert result.event_potential_energy_change == 0.0


def test_interleaved_phase_ternary_md_clocks_and_replay():
    state, inputs = _fixture()
    schedules = (
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=0.1),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.neutral_entry_only(),) * 7),
        dict(mechanical_time_step=MECHANICAL_DT),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.hold(),) * 7),
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=0.2),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.neutral_exit_only(),) * 7),
        dict(mechanical_time_step=MECHANICAL_DT),
    )

    def replay():
        current = state
        history = []
        for schedule in schedules:
            event = _run(current, inputs, **schedule)
            assert event.coupled_step.previous == current
            history.append(event)
            current = event.current
        return tuple(history)

    first = replay()
    assert replay() == first
    final = first[-1].current
    assert final.md_state.step == state.md_state.step + 2
    assert final.md_state.time == pytest.approx(state.md_state.time + 2 * MECHANICAL_DT)
    assert final.resonance_step_count == state.resonance_step_count + 2
    assert final.resonance_time == pytest.approx(state.resonance_time + 0.3)
    assert final.ternary_event_count == state.ternary_event_count + 3
    assert final.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7
    assert not final.ternary_execution.has_pending_targets


@pytest.mark.parametrize("matrix,translation", (
    (((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), (2.0, -3.0, 1.0)),
    (((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), (0.0, 0.0, 0.0)),
))
def test_e3_invariance_of_boundaries_and_covariance_of_motion(matrix, translation):
    transform = E3Transformation(matrix=matrix, translation=translation)
    start, inputs = _fixture()
    changed, changed_inputs = _fixture(transform)
    before = _run(start, inputs, **_full_schedule())
    after = _run(changed, changed_inputs, **_full_schedule())
    assert before.current.ternary_execution == after.current.ternary_execution
    assert before.current.resonance_state == after.current.resonance_state
    for key in ("before_events", "after_events", "after_mechanics"):
        expected = getattr(before, key).energy_result.energy.total_energy
        actual = getattr(after, key).energy_result.energy.total_energy
        assert actual == pytest.approx(expected, rel=1.0e-11, abs=1.0e-8)
    for old, new in zip(
        before.current.md_state.configuration.positions,
        after.current.md_state.configuration.positions, strict=True,
    ):
        assert new == pytest.approx(transform.transform_position(old), abs=1.0e-7)
    for old, new in zip(before.current.md_state.velocities,
                        after.current.md_state.velocities, strict=True):
        assert new == pytest.approx(transform.transform_vector(old), abs=1.0e-7)
    for key in ("before_events", "after_events", "after_mechanics"):
        a, b = getattr(before, key), getattr(after, key)
        assert a.resonance.coordinate == pytest.approx(b.resonance.coordinate, abs=1.0e-12)
        assert a.execution.retained_states == b.execution.retained_states


def test_deterministic_repetition_with_identical_microstate_and_schedule():
    state, inputs = _fixture()
    first = _run(state, inputs, **_full_schedule())
    second = _run(state, inputs, **_full_schedule())
    assert first == second
    assert first is not second
    assert first.current == second.current


@pytest.mark.parametrize("incorrect,keyword", (
    ("model", "model"),
    ("force_evaluator", "force_evaluator"),
    ("base_features", "base_features"),
    ("thermodynamic_state", "thermodynamic_state"),
    ("interpretation", "interpretation"),
))
def test_input_contract_rejects_untyped_dependency(incorrect, keyword):
    state, inputs = _fixture()
    inputs[incorrect] = None
    with pytest.raises(TypeError, match=keyword):
        _run(state, inputs, mechanical_time_step=MECHANICAL_DT)


def test_feature_and_species_constraints_reject_invalid_inputs():
    state, inputs = _fixture()
    inputs["base_features"] = NodeFeatureVector(nodes=(NodeFeatures(scalars=(1.0,)),))
    with pytest.raises(ValueError, match="feature and atom counts"):
        _run(state, inputs, mechanical_time_step=MECHANICAL_DT)
    state, inputs = _fixture()
    invalid = replace(state.md_state.configuration, species=("Li", "Li", "Be", "F", "F", "F", "Li"))
    with pytest.raises(ValueError, match="stoichiometry"):
        _run(replace(state, md_state=replace(state.md_state, configuration=invalid)),
             inputs, mechanical_time_step=MECHANICAL_DT)


@pytest.mark.parametrize("schedule", (
    {},
    {"ternary_event": True, "phase_time_step": PHASE_DT},
    {"phase_parameters": PHASE_PARAMETERS},
    {"mechanical_time_step": 0.0},
    {"mechanical_time_step": True},
    {"phase_time_step": -1.0, "phase_parameters": PHASE_PARAMETERS},
    {"ternary_event": False, "guards": (TernaryExecutionGuard.hold(),) * 7},
))
def test_invalid_schedule_fails_explicitly(schedule):
    state, inputs = _fixture()
    with pytest.raises((ValueError, TypeError)):
        _run(state, inputs, **schedule)


def test_result_detects_corrupted_energy_resonance_execution_and_context(coupled):
    state, inputs, result = coupled
    with pytest.raises(ValueError, match="energy boundaries"):
        replace(result, coupled_step=replace(
            result.coupled_step,
            energy_after_events=result.coupled_step.energy_before_events,
        ))
    with pytest.raises(ValueError, match="TR-EIP resonance"):
        replace(result, after_events=replace(
            result.after_events, resonance=result.before_events.resonance,
        ))
    with pytest.raises(ValueError, match="TR-EIP retained execution"):
        replace(result, before_events=replace(
            result.before_events, execution=result.after_events.execution,
        ))
    with pytest.raises(ValueError, match="thermodynamic context"):
        replace(result, thermodynamic_state=FLiBeThermodynamicState(temperature=900.0, pressure=101325.0))
    with pytest.raises(ValueError, match="ternary request"):
        replace(result, interpretation=_interpretation(reverse=True))
    with pytest.raises(ValueError, match="final FLiBe configuration"):
        replace(result, after_mechanics=result.before_events)


def test_frozen_evidence_records(coupled):
    _, _, result = coupled
    with pytest.raises(FrozenInstanceError):
        result.coupled_step = None  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.current.ternary_event_count = 99  # type: ignore[misc]
