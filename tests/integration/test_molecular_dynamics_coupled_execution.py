
"""Integration qualification of multirate resonance-ternary-interatomic MD.

Reconstruct each scheduled phase, ternary, and mechanical operation through its
independent reference operator. Verify retained active-neutral routing, pending
targets, conservative force integration, E(3) covariance, clock separation,
and distinct potential-energy changes at event and mechanical boundaries.
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
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import (
    CoupledMolecularDynamicsState,
    CoupledMolecularDynamicsStep,
    append_md_resonance_features,
    execute_coupled_md_step,
)
from tr_eif.md.dynamics import accelerations_from_forces
from tr_eif.md.execution import velocity_verlet_step
from tr_eif.md.integrator import velocity_verlet_positions, velocity_verlet_velocities
from tr_eif.md.resonance_propagation import propagate_md_resonance_state
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.ternary_propagation import propagate_md_ternary_state
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceState,
    resonance_descriptor,
)
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
    is_direct_opposite_transition,
    ternary_target_from_descriptor,
)

POSITIONS = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
VELOCITIES = ((0.0, 0.01, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.0, 0.01))
MASSES = (1.0, 2.0, 3.0)
PHASE_PARAMETERS = PhaseDynamicsParameters(
    coupling=(0.2, 0.2, 0.2), phase_lag=(0.1, 0.1, 0.1)
)
POSITIVE_PROJECTION = ResonanceProjection(1.0, -0.1)
NEGATIVE_PROJECTION = ResonanceProjection(-1.0, 0.0)
THRESHOLDS = TernaryTargetThresholds(negative=-0.3, positive=0.5)
PHASE_DT = 0.2
MD_DT = 0.0001
CUTOFF = 1.6


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
            configuration=AtomicConfiguration(
                species=("A", "B", "C"), positions=positions,
            ),
            velocities=velocities, masses=MASSES, step=4, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.15, 0.3), frequencies=(0.1, -0.1, 0.2),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (retained,) * len(POSITIONS)
        ),
        resonance_time=0.4,
        resonance_step_count=2,
        ternary_event_count=5,
    )
    base_features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(scalars=(float(index + 1),), vectors=((0.2, -0.1, 0.05),))
        for index in range(len(POSITIONS))
    ))
    if transformation is not None:
        base_features = transformation.transform_feature_vector(base_features)
    model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.0),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.2, positive_scale=1.7,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.3, 0.4, 0.7), bias=0.1,
        ),
    )
    resources = dict(
        model=model,
        force_evaluator=ConservativeForceEvaluator(
            differentiation=CoordinateDifferentiation(step=1.0e-5)
        ),
        base_features=base_features,
        cutoff=CUTOFF,
    )
    return state, resources


def _run(state, resources, **schedule):
    return execute_coupled_md_step(state, **resources, **schedule)


def _event(projection=POSITIVE_PROJECTION, **kwargs):
    return dict(
        ternary_event=True,
        projection=projection,
        thresholds=THRESHOLDS,
        **kwargs,
    )


def _full_schedule():
    return _event(
        phase_parameters=PHASE_PARAMETERS,
        phase_time_step=PHASE_DT,
        mechanical_time_step=MD_DT,
    )


def test_explicit_three_clock_schedule_and_exact_reference_phase_step():
    start, resources = _fixture()
    result = _run(start, resources, phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT)
    reference = propagate_md_resonance_state(
        start.md_state, start.resonance_state, PHASE_PARAMETERS, CUTOFF, PHASE_DT,
    )
    assert result.resonance_update == reference
    assert result.current.resonance_state == reference.current
    assert result.current.resonance_time == pytest.approx(start.resonance_time + PHASE_DT)
    assert result.current.resonance_step_count == start.resonance_step_count + 1
    assert result.current.ternary_event_count == start.ternary_event_count
    assert result.current.md_state is start.md_state
    assert result.current.ternary_execution is start.ternary_execution
    assert result.descriptor == resonance_descriptor(reference.current)
    assert result.ternary_update is None and result.mechanical_update is None
    assert result.mechanical_potential_energy_change == 0.0
    assert result.event_potential_energy_change != 0.0


def test_resonance_channels_preserve_original_scalar_and_vector_features():
    start, resources = _fixture()
    descriptor = resonance_descriptor(start.resonance_state)
    output = append_md_resonance_features(resources["base_features"], descriptor)
    assert output.node_count == start.md_state.atom_count
    assert output.scalar_channel_count == resources["base_features"].scalar_channel_count + 2
    for original, extended in zip(resources["base_features"].nodes, output.nodes, strict=True):
        assert extended.scalars == (*original.scalars, descriptor.phase_order, descriptor.frequency_spread)
        assert extended.vectors == original.vectors


def test_request_is_sampled_after_phase_step_and_mechanical_force_uses_retained_neutral():
    start, resources = _fixture()
    result = _run(start, resources, **_full_schedule())
    assert result.resonance_update is not None
    assert result.ternary_update is not None
    assert result.mechanical_update is not None
    expected_target = ternary_target_from_descriptor(
        resonance_descriptor(result.resonance_update.current), POSITIVE_PROJECTION, THRESHOLDS,
    )
    assert expected_target is TernaryState.POSITIVE
    assert result.requested_target is expected_target
    assert result.requested_targets == (expected_target,) * start.md_state.atom_count
    reference_ternary = propagate_md_ternary_state(
        start.md_state, start.ternary_execution, result.requested_targets,
    )
    assert result.ternary_update == reference_ternary
    assert result.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in result.current.ternary_execution.states)
    assert result.ternary_update.committed_count == 3

    graph = build_cutoff_graph(start.md_state.configuration, CUTOFF)
    base = resources["base_features"]
    before_features = append_md_resonance_features(base, resonance_descriptor(start.resonance_state))
    after_features = append_md_resonance_features(base, result.descriptor)
    model = resources["model"]
    before = model.evaluate(start.md_state.configuration, graph, before_features, start.ternary_execution)
    after_event = model.evaluate(start.md_state.configuration, graph, after_features, reference_ternary.current)
    assert result.energy_before_events == before.energy
    assert result.energy_after_events == after_event.energy

    mechanical_reference = velocity_verlet_step(
        state=start.md_state, model=model, force_evaluator=resources["force_evaluator"],
        features=after_features, execution=reference_ternary.current,
        cutoff=CUTOFF, time_step=MD_DT,
    )
    assert result.mechanical_update == mechanical_reference
    final = model.evaluate(
        result.current.md_state.configuration,
        mechanical_reference.graph_after,
        after_features,
        reference_ternary.current,
    ).energy
    assert result.energy_after_mechanics == final
    assert result.event_potential_energy_change == pytest.approx(
        after_event.energy.total_energy - before.energy.total_energy
    )
    assert result.mechanical_potential_energy_change == pytest.approx(
        final.total_energy - after_event.energy.total_energy
    )
    assert result.current.md_state.step == start.md_state.step + 1
    assert result.current.md_state.time == pytest.approx(start.md_state.time + MD_DT)
    assert result.current.resonance_time == pytest.approx(start.resonance_time + PHASE_DT)
    assert result.current.ternary_event_count == start.ternary_event_count + 1


def test_verlet_positions_and_velocities_match_independent_force_kinematics():
    state, resources = _fixture()
    result = _run(state, resources, mechanical_time_step=MD_DT)
    step = result.mechanical_update
    assert step is not None
    acceleration_before = accelerations_from_forces(step.forces_before, state.md_state.masses)
    acceleration_after = accelerations_from_forces(step.forces_after, state.md_state.masses)
    expected_positions = velocity_verlet_positions(
        state.md_state.configuration.positions, state.md_state.velocities,
        acceleration_before, MD_DT,
    )
    expected_velocities = velocity_verlet_velocities(
        state.md_state.velocities, acceleration_before, acceleration_after, MD_DT,
    )
    for actual, expected in zip(step.current.configuration.positions, expected_positions, strict=True):
        assert actual == pytest.approx(expected, abs=1.0e-12)
    for actual, expected in zip(step.current.velocities, expected_velocities, strict=True):
        assert actual == pytest.approx(expected, abs=1.0e-12)
    assert step.graph_before == build_cutoff_graph(state.md_state.configuration, CUTOFF)
    assert step.graph_after == build_cutoff_graph(step.current.configuration, CUTOFF)
    assert result.event_potential_energy_change == 0.0
    assert result.resonance_update is None and result.ternary_update is None
    assert result.current.resonance_state == state.resonance_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.current.resonance_time == state.resonance_time
    assert result.current.ternary_event_count == state.ternary_event_count


def test_neutral_entry_hold_and_exit_are_separate_events_with_pending():
    state, resources = _fixture()
    entry = _run(state, resources, **_event())
    assert entry.current.md_state is state.md_state
    assert entry.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert entry.current.ternary_execution.has_pending_targets
    assert entry.ternary_update.committed_count == 3
    for node in entry.ternary_update.execution.node_steps:
        assert node.route is not None
        assert node.route.transition.target is TernaryState.NEUTRAL
        assert not is_direct_opposite_transition(node.route.transition.source, node.route.transition.target)
    held = _run(entry.current, resources, **_event(
        projection=NEGATIVE_PROJECTION,
        guards=(TernaryExecutionGuard.hold(),) * 3,
    ))
    assert held.requested_target is TernaryState.NEGATIVE
    assert held.requested_targets == (TernaryState.POSITIVE,) * 3
    assert held.current.ternary_execution == entry.current.ternary_execution
    assert held.event_potential_energy_change == 0.0
    assert held.ternary_update.committed_count == 0
    exit_step = _run(held.current, resources, **_event(projection=NEGATIVE_PROJECTION))
    assert exit_step.requested_target is TernaryState.NEGATIVE
    assert exit_step.current.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 3
    assert not exit_step.current.ternary_execution.has_pending_targets
    assert exit_step.ternary_update.committed_count == 3
    assert exit_step.current.ternary_event_count == state.ternary_event_count + 3
    for node in exit_step.ternary_update.execution.node_steps:
        assert node.route is not None
        assert node.route.transition.source is TernaryState.NEUTRAL
        assert not is_direct_opposite_transition(node.route.transition.source, node.route.transition.target)
    assert entry.current.resonance_state == exit_step.current.resonance_state
    assert entry.current.md_state == exit_step.current.md_state


def test_reverse_polarity_also_enters_neutral_before_negative():
    state, resources = _fixture(retained=TernaryState.POSITIVE)
    entry = _run(state, resources, **_event(projection=NEGATIVE_PROJECTION))
    assert entry.requested_target is TernaryState.NEGATIVE
    assert entry.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert all(node.pending_target is TernaryState.NEGATIVE
               for node in entry.current.ternary_execution.states)
    exit_step = _run(entry.current, resources, **_event(projection=POSITIVE_PROJECTION))
    assert exit_step.current.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 3
    assert all(node.pending_target is None for node in exit_step.current.ternary_execution.states)
    assert exit_step.ternary_update.committed_count == 3
    for stage in (entry, exit_step):
        assert all(not is_direct_opposite_transition(s.route.transition.source, s.route.transition.target)
                   for s in stage.ternary_update.execution.node_steps if s.route is not None)


def test_separate_interleaved_clocks_and_deterministic_replay():
    start, resources = _fixture()
    schedules = (
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=0.15),
        _event(guards=(TernaryExecutionGuard.neutral_entry_only(),) * 3),
        dict(mechanical_time_step=0.0002),
        _event(guards=(TernaryExecutionGuard.hold(),) * 3),
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=0.05),
        _event(guards=(TernaryExecutionGuard.neutral_exit_only(),) * 3),
        dict(mechanical_time_step=0.0001),
    )

    def execute_sequence():
        current = start
        outputs = []
        for options in schedules:
            step = _run(current, resources, **options)
            assert step.previous == current
            outputs.append(step)
            current = step.current
        return tuple(outputs)

    first = execute_sequence()
    assert execute_sequence() == first
    last = first[-1].current
    assert last.md_state.step == start.md_state.step + 2
    assert last.md_state.time == pytest.approx(start.md_state.time + 0.0003)
    assert last.resonance_step_count == start.resonance_step_count + 2
    assert last.resonance_time == pytest.approx(start.resonance_time + 0.2)
    assert last.ternary_event_count == start.ternary_event_count + 3
    assert last.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 3
    assert not last.ternary_execution.has_pending_targets


@pytest.mark.parametrize("matrix,translation", (
    (((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), (2.0, -3.0, 1.0)),
    (((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), (0.0, 0.0, 0.0)),
))
def test_e3_covariance_energy_invariance_and_ternary_polarity(matrix, translation):
    transformation = E3Transformation(matrix=matrix, translation=translation)
    original, resources = _fixture()
    transformed, transformed_resources = _fixture(transformation)
    original_step = _run(original, resources, **_full_schedule())
    transformed_step = _run(transformed, transformed_resources, **_full_schedule())
    assert original_step.descriptor == transformed_step.descriptor
    assert original_step.requested_targets == transformed_step.requested_targets
    assert original_step.current.ternary_execution == transformed_step.current.ternary_execution
    for field in ("energy_before_events", "energy_after_events", "energy_after_mechanics"):
        a = getattr(original_step, field)
        b = getattr(transformed_step, field)
        assert b.total_energy == pytest.approx(a.total_energy, rel=1e-11, abs=1e-9)
    for before, after in zip(original_step.current.md_state.configuration.positions,
                             transformed_step.current.md_state.configuration.positions, strict=True):
        assert after == pytest.approx(transformation.transform_position(before), abs=1.0e-8)
    for before, after in zip(original_step.current.md_state.velocities,
                             transformed_step.current.md_state.velocities, strict=True):
        assert after == pytest.approx(transformation.transform_vector(before), abs=1.0e-8)
    assert transformed_step.current.resonance_state == original_step.current.resonance_state


@pytest.mark.parametrize("changes,exception", (
    ({}, ValueError),
    ({"phase_time_step": 0.0}, ValueError),
    ({"phase_time_step": float("nan")}, ValueError),
    ({"phase_time_step": 0.1}, TypeError),
    ({"phase_parameters": PHASE_PARAMETERS}, ValueError),
    ({"ternary_event": True}, TypeError),
    ({"ternary_event": True, "projection": POSITIVE_PROJECTION}, TypeError),
    ({"projection": POSITIVE_PROJECTION}, ValueError),
    ({"ternary_event": 1}, TypeError),
    ({"mechanical_time_step": -1.0}, ValueError),
    ({"mechanical_time_step": True}, TypeError),
    ({"mechanical_time_step": float("inf")}, ValueError),
    ({"cutoff": 0.0, "mechanical_time_step": 0.01}, ValueError),
    ({"cutoff": float("nan"), "mechanical_time_step": 0.01}, ValueError),
    ({"ternary_event": False, "guards": (TernaryExecutionGuard.hold(),) * 3}, ValueError),
))
def test_invalid_schedule_contracts(changes, exception):
    state, resources = _fixture()
    inputs = dict(resources)
    inputs.update(changes)
    with pytest.raises(exception):
        execute_coupled_md_step(state, **inputs)


def test_feature_count_and_scalar_energy_channel_mismatch_are_rejected():
    state, resources = _fixture()
    single = NodeFeatureVector(nodes=(NodeFeatures(scalars=(1.0,)),))
    with pytest.raises(ValueError, match="feature node count"):
        _run(state, {**resources, "base_features": single}, mechanical_time_step=0.01)
    mismatched = ReferenceEnergyModel(
        message_operator=resources["model"].message_operator,
        conditioning=resources["model"].conditioning,
        energy_functional=LinearInvariantEnergyFunctional(weights=(1.0,)),
    )
    with pytest.raises(ValueError, match="scalar channels"):
        _run(state, {**resources, "model": mismatched}, mechanical_time_step=0.01)


@pytest.mark.parametrize("invalid_field", (
    "md_state", "resonance_state", "ternary_execution", "resonance_time",
    "resonance_step_count", "ternary_event_count",
))
def test_composite_state_rejects_invalid_typed_or_clock_fields(invalid_field):
    state, _ = _fixture()
    changes = {
        "md_state": None,
        "resonance_state": None,
        "ternary_execution": None,
        "resonance_time": -1.0,
        "resonance_step_count": -1,
        "ternary_event_count": True,
    }
    with pytest.raises((ValueError, TypeError)):
        replace(state, **{invalid_field: changes[invalid_field]})


def test_composite_state_rejects_node_count_mismatch():
    state, _ = _fixture()
    one = TernaryExecutionVector.from_retained_states((TernaryState.NEUTRAL,))
    with pytest.raises(ValueError, match="counts differ"):
        replace(state, ternary_execution=one)


def test_result_rejects_unscheduled_clock_and_mechanical_mutations():
    state, resources = _fixture()
    phase_only = _run(state, resources, phase_parameters=PHASE_PARAMETERS, phase_time_step=0.2)
    with pytest.raises(ValueError, match="ternary state changed"):
        replace(phase_only, current=replace(
            phase_only.current, ternary_event_count=phase_only.current.ternary_event_count + 1,
        ))
    with pytest.raises(ValueError, match="MD state changed"):
        replace(phase_only, current=replace(
            phase_only.current, md_state=replace(
                phase_only.current.md_state, time=phase_only.current.md_state.time + 0.01,
            ),
        ))
    mechanical = _run(state, resources, mechanical_time_step=MD_DT)
    with pytest.raises(ValueError, match="resonance changed"):
        replace(mechanical, current=replace(
            mechanical.current, resonance_time=mechanical.current.resonance_time + 0.1,
        ))
    with pytest.raises(ValueError, match="ternary state changed"):
        replace(mechanical, requested_target=TernaryState.POSITIVE)
    event = _run(state, resources, **_event())
    with pytest.raises(ValueError, match="ternary event"):
        replace(event, requested_target=None)
    with pytest.raises(ValueError, match="mechanics-free event"):
        replace(event, energy_after_mechanics=event.energy_before_events)


def test_result_dataclasses_are_frozen():
    state, resources = _fixture()
    result = _run(state, resources, mechanical_time_step=MD_DT)
    with pytest.raises(FrozenInstanceError):
        result.current.ternary_event_count = 99
    with pytest.raises(FrozenInstanceError):
        result.current = state
    assert isinstance(result, CoupledMolecularDynamicsStep)
