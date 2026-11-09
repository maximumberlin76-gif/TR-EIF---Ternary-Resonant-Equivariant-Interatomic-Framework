
"""Integration tests for rank-two multirate execution in TR-EIF.

Reconstruct resonance and ternary events with the generic executor, then
independently verify full-energy boundaries and velocity-Verlet kinematics
using the tensor-augmented conservative forces. Preserve distinct scheduler
clocks, active-neutral mediation, E(3) covariance and replay determinism.
"""

from dataclasses import FrozenInstanceError, replace
from math import isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.energy.rank_two_model import (
    RankTwoChannelEnergyWeights,
    RankTwoConservativeEnergyModel,
    RankTwoConservativeForceEvaluator,
    RankTwoInvariantEnergyReadout,
)
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.equivariant.rank_two import (
    RankTwoFeatureVector,
    RankTwoTensor,
    ScalarVectorTensorFeatures,
)
from tr_eif.equivariant.rank_two_message_passing import RankTwoMessageCoupling
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import (
    CoupledMolecularDynamicsState,
    append_md_resonance_features,
    execute_coupled_md_step,
)
from tr_eif.md.dynamics import accelerations_from_forces
from tr_eif.md.execution import velocity_verlet_step
from tr_eif.md.integrator import velocity_verlet_positions, velocity_verlet_velocities
from tr_eif.md.rank_two_coupled_execution import (
    RankTwoCoupledMolecularDynamicsStep,
    execute_rank_two_coupled_md_step,
)
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

POSITIONS = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.3, 1.1, 0.2))
VELOCITIES = ((0.001, 0.002, 0.0), (-0.002, 0.001, 0.001), (0.0, -0.001, 0.002))
MASSES = (1.5, 2.5, 3.5)
CUTOFF = 1.7
PHASE_DT = 0.1
MECHANICAL_DT = 1.0e-4
PHASE_PARAMETERS = PhaseDynamicsParameters(
    coupling=(0.25, 0.25, 0.25), phase_lag=(0.1, 0.1, 0.1),
)
POSITIVE = ResonanceProjection(1.0, -0.1)
NEGATIVE = ResonanceProjection(-1.0, 0.0)
THRESHOLDS = TernaryTargetThresholds(negative=-0.3, positive=0.5)
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def _fixture(transformation=None, initial_state=TernaryState.NEGATIVE, zero_tensor=False):
    positions, velocities = POSITIONS, VELOCITIES
    if transformation is not None:
        positions = tuple(transformation.transform_position(p) for p in positions)
        velocities = tuple(transformation.transform_vector(v) for v in velocities)
    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(species=("A", "B", "C"), positions=positions),
            velocities=velocities, masses=MASSES, step=3, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.15, 0.3), frequencies=(0.1, -0.1, 0.2),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (initial_state,) * 3
        ),
        resonance_time=0.4, resonance_step_count=2, ternary_event_count=5,
    )
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.2 * i,),
            vectors=((0.3 + 0.1 * i, -0.2, 0.1 * i),),
        ) for i in range(3)
    ))
    rank_two = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.2, -0.1),
            (0.3, 0.7 - 0.05 * i, 0.15),
            (-0.2, 0.1, 0.6),
        )),
        RankTwoTensor.outer((1.0, i * 0.3 - 0.2, 0.4), (0.3, 0.7, -0.1)),
    ) for i in range(3)))
    features = ScalarVectorTensorFeatures(base=base, rank_two=rank_two)
    if transformation is not None:
        features = features.transformed(transformation)
    reference = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.7,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.6, -0.2), bias=0.1,
        ),
    )
    weights = (
        RankTwoChannelEnergyWeights() if zero_tensor else RankTwoChannelEnergyWeights(
            trace=0.15, isotropic_norm_squared=0.05,
            symmetric_traceless_norm_squared=0.25,
            antisymmetric_norm_squared=0.12,
        ),
        RankTwoChannelEnergyWeights() if zero_tensor else RankTwoChannelEnergyWeights(
            trace=-0.1, isotropic_norm_squared=0.06,
            symmetric_traceless_norm_squared=-0.04,
            antisymmetric_norm_squared=0.09,
        ),
    )
    model = RankTwoConservativeEnergyModel(
        reference_model=reference,
        tensor_readout=RankTwoInvariantEnergyReadout(weights),
        coupling=RankTwoMessageCoupling(
            tensor_scale=0.7, scalar_dyad_scale=0.2,
            vector_dyad_scale=-0.15,
            scalar_channel_index=0, vector_channel_index=0,
        ),
    )
    resources = dict(
        model=model,
        force_evaluator=RankTwoConservativeForceEvaluator(
            CoordinateDifferentiation(step=1.0e-5),
        ),
        features=features,
        cutoff=CUTOFF,
    )
    return state, resources


def _run(state, resources, **schedule):
    return execute_rank_two_coupled_md_step(state, **resources, **schedule)


def _event(projection=POSITIVE, **other):
    return dict(ternary_event=True, projection=projection, thresholds=THRESHOLDS, **other)


def _full():
    return _event(
        phase_parameters=PHASE_PARAMETERS,
        phase_time_step=PHASE_DT,
        mechanical_time_step=MECHANICAL_DT,
    )


def _full_features(resources, state):
    return ScalarVectorTensorFeatures(
        base=append_md_resonance_features(
            resources["features"].base, resonance_descriptor(state.resonance_state),
        ),
        rank_two=resources["features"].rank_two,
    )


def _energy(resources, md_state, features, retained, graph=None):
    if graph is None:
        graph = build_cutoff_graph(md_state.configuration, CUTOFF)
    return resources["model"].evaluate(md_state.configuration, graph, features, retained)


@pytest.fixture(scope="module")
def full_execution():
    initial, resources = _fixture()
    return initial, resources, _run(initial, resources, **_full())


def test_full_schedule_delegates_phase_and_ternary_events_exactly(full_execution):
    state, resources, result = full_execution
    assert isinstance(result, RankTwoCoupledMolecularDynamicsStep)
    reference = execute_coupled_md_step(
        state, model=resources["model"].reference_model,
        force_evaluator=ConservativeForceEvaluator(resources["force_evaluator"].differentiation),
        base_features=resources["features"].base, cutoff=CUTOFF,
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True, projection=POSITIVE, thresholds=THRESHOLDS,
    )
    assert result.event_update == reference
    assert result.descriptor == resonance_descriptor(reference.current.resonance_state)
    assert result.requested_target is TernaryState.POSITIVE
    assert result.requested_targets == (TernaryState.POSITIVE,) * 3
    assert result.current.resonance_time == pytest.approx(state.resonance_time + PHASE_DT)
    assert result.current.resonance_step_count == state.resonance_step_count + 1
    assert result.current.ternary_event_count == state.ternary_event_count + 1
    assert result.current.md_state.step == state.md_state.step + 1
    assert result.current.md_state.time == pytest.approx(state.md_state.time + MECHANICAL_DT)
    assert result.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert all(n.pending_target is TernaryState.POSITIVE
               for n in result.current.ternary_execution.states)


def test_three_full_energy_boundaries_are_independently_recomputed(full_execution):
    state, resources, result = full_execution
    before_features = _full_features(resources, state)
    after_features = _full_features(resources, result.current)
    before = _energy(resources, state.md_state, before_features, state.ternary_execution)
    event = _energy(resources, state.md_state, after_features,
                    result.current.ternary_execution)
    after = _energy(resources, result.current.md_state, after_features,
                    result.current.ternary_execution)
    assert result.features_before_events == before_features
    assert result.features_after_events == after_features
    assert result.energy_before_events == before
    assert result.energy_after_events == event
    assert result.energy_after_mechanics == after
    assert result.event_potential_energy_change == pytest.approx(
        event.energy.total_energy - before.energy.total_energy,
    )
    assert result.mechanical_potential_energy_change == pytest.approx(
        after.energy.total_energy - event.energy.total_energy,
    )
    assert event.reference_energy == result.event_update.energy_after_events
    assert before.reference_energy == result.event_update.energy_before_events
    assert abs(after.tensor_energy.total_energy) > 1.0e-8


def test_tensor_forces_drive_both_velocity_verlet_endpoints(full_execution):
    state, resources, result = full_execution
    mechanical = result.mechanical_update
    assert mechanical is not None
    features = result.features_after_events
    execution = result.current.ternary_execution
    graph_before = build_cutoff_graph(state.md_state.configuration, CUTOFF)
    expected_before = resources["force_evaluator"].evaluate(
        resources["model"], state.md_state.configuration, graph_before,
        features, execution,
    )
    assert mechanical.forces_before == expected_before
    accelerations_before = accelerations_from_forces(expected_before, state.md_state.masses)
    expected_positions = velocity_verlet_positions(
        state.md_state.configuration.positions, state.md_state.velocities,
        accelerations_before, MECHANICAL_DT,
    )
    for actual, expected in zip(mechanical.current.configuration.positions,
                                expected_positions, strict=True):
        assert actual == pytest.approx(expected, abs=1.0e-11)
    expected_after = resources["force_evaluator"].evaluate(
        resources["model"], mechanical.current.configuration,
        mechanical.graph_after, features, execution,
    )
    assert mechanical.forces_after == expected_after
    accelerations_after = accelerations_from_forces(expected_after, state.md_state.masses)
    expected_velocities = velocity_verlet_velocities(
        state.md_state.velocities, accelerations_before,
        accelerations_after, MECHANICAL_DT,
    )
    for actual, expected in zip(mechanical.current.velocities,
                                expected_velocities, strict=True):
        assert actual == pytest.approx(expected, abs=1.0e-11)
    h = 2.5e-5
    for atom, axis in ((0, 0), (1, 1), (2, 2)):
        values = []
        for signed in (h, -h):
            positions = list(state.md_state.configuration.positions)
            point = list(positions[atom])
            point[axis] += signed
            positions[atom] = tuple(point)
            trial = AtomicConfiguration(species=("A", "B", "C"), positions=tuple(positions))
            values.append(resources["model"].evaluate(
                trial, graph_before, features, execution,
            ).energy.total_energy)
        independent = -(values[0] - values[1]) / (2.0 * h)
        assert expected_before.forces[atom][axis] == pytest.approx(
            independent, rel=3.0e-4, abs=1.0e-5,
        )


def test_phase_only_retains_mechanical_and_discrete_state():
    state, resources = _fixture()
    result = _run(state, resources, phase_parameters=PHASE_PARAMETERS,
                  phase_time_step=PHASE_DT)
    assert result.event_update is not None
    assert result.event_update.resonance_update is not None
    assert result.event_update.ternary_update is None
    assert result.mechanical_update is None
    assert result.current.md_state == state.md_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.energy_after_mechanics == result.energy_after_events
    assert result.mechanical_potential_energy_change == 0.0
    assert result.energy_after_events.tensor_energy == result.energy_before_events.tensor_energy
    assert result.current.resonance_time == pytest.approx(state.resonance_time + PHASE_DT)


def test_ternary_only_routes_through_active_neutral_without_md_update():
    state, resources = _fixture()
    entered = _run(state, resources, **_event())
    assert entered.event_update is not None
    assert entered.event_update.resonance_update is None
    assert entered.event_update.ternary_update.committed_count == 3
    assert entered.mechanical_update is None
    assert entered.current.md_state is state.md_state
    assert entered.current.resonance_state is state.resonance_state
    assert entered.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert entered.current.ternary_execution.has_pending_targets
    assert entered.energy_after_mechanics == entered.energy_after_events
    assert entered.event_potential_energy_change != 0.0


def test_mechanics_only_retains_phase_and_ternary_clocks():
    state, resources = _fixture()
    result = _run(state, resources, mechanical_time_step=MECHANICAL_DT)
    assert result.event_update is None
    assert result.mechanical_update is not None
    assert result.energy_before_events == result.energy_after_events
    assert result.event_potential_energy_change == 0.0
    assert result.current.resonance_time == state.resonance_time
    assert result.current.resonance_step_count == state.resonance_step_count
    assert result.current.ternary_event_count == state.ternary_event_count
    assert result.current.ternary_execution == state.ternary_execution
    assert result.current.md_state.step == state.md_state.step + 1


def test_pending_target_survives_guarded_hold_and_reverse_request():
    state, resources = _fixture()
    entered = _run(state, resources, **_event())
    held = _run(entered.current, resources, **_event(
        projection=NEGATIVE, guards=(TernaryExecutionGuard.hold(),) * 3,
    ))
    assert held.requested_target is TernaryState.NEGATIVE
    assert held.requested_targets == (TernaryState.POSITIVE,) * 3
    assert held.event_update.ternary_update.committed_count == 0
    assert held.current.ternary_execution == entered.current.ternary_execution
    assert held.energy_before_events == held.energy_after_events
    exited = _run(held.current, resources, **_event(projection=NEGATIVE))
    assert exited.requested_target is TernaryState.NEGATIVE
    assert exited.current.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 3
    assert not exited.current.ternary_execution.has_pending_targets
    for stage in (entered, exited):
        for node in stage.event_update.ternary_update.execution.node_steps:
            assert node.route is not None
            assert not is_direct_opposite_transition(
                node.route.transition.source, node.route.transition.target,
            )


def test_reverse_polarity_also_commits_two_distinct_neutral_legs():
    state, resources = _fixture(initial_state=TernaryState.POSITIVE)
    first = _run(state, resources, **_event(projection=NEGATIVE))
    assert first.requested_target is TernaryState.NEGATIVE
    assert first.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 3
    assert all(n.pending_target is TernaryState.NEGATIVE
               for n in first.current.ternary_execution.states)
    second = _run(first.current, resources, **_event(projection=POSITIVE))
    assert second.current.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 3
    assert not second.current.ternary_execution.has_pending_targets
    assert first.event_update.ternary_update.committed_count == 3
    assert second.event_update.ternary_update.committed_count == 3


def test_mixed_schedule_counters_and_deterministic_replay():
    state, resources = _fixture()
    schedules = (
        dict(phase_time_step=PHASE_DT, phase_parameters=PHASE_PARAMETERS),
        _event(guards=(TernaryExecutionGuard.neutral_entry_only(),) * 3),
        dict(mechanical_time_step=MECHANICAL_DT),
        _event(guards=(TernaryExecutionGuard.hold(),) * 3),
        dict(phase_time_step=PHASE_DT / 2, phase_parameters=PHASE_PARAMETERS),
        _event(guards=(TernaryExecutionGuard.neutral_exit_only(),) * 3),
        dict(mechanical_time_step=MECHANICAL_DT),
    )

    def replay():
        current, steps = state, []
        for schedule in schedules:
            outcome = _run(current, resources, **schedule)
            assert outcome.previous == current
            steps.append(outcome)
            current = outcome.current
        return tuple(steps)

    first = replay()
    assert replay() == first
    final = first[-1].current
    assert final.md_state.step == state.md_state.step + 2
    assert final.md_state.time == pytest.approx(state.md_state.time + 2 * MECHANICAL_DT)
    assert final.resonance_time == pytest.approx(state.resonance_time + 1.5 * PHASE_DT)
    assert final.resonance_step_count == state.resonance_step_count + 2
    assert final.ternary_event_count == state.ternary_event_count + 3
    assert final.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 3
    assert not final.ternary_execution.has_pending_targets


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 0.5)),
    (REFLECTION, (-1.0, 0.7, 2.0)),
))
def test_e3_invariant_energies_and_covariant_full_forces(matrix, translation):
    transform = E3Transformation(matrix, translation)
    state, resources = _fixture()
    transformed, changed_resources = _fixture(transform)
    baseline = _run(state, resources, **_full())
    changed = _run(transformed, changed_resources, **_full())
    assert changed.descriptor == baseline.descriptor
    assert changed.current.resonance_state == baseline.current.resonance_state
    assert changed.current.ternary_execution == baseline.current.ternary_execution
    for boundary in ("energy_before_events", "energy_after_events", "energy_after_mechanics"):
        before = getattr(baseline, boundary)
        after = getattr(changed, boundary)
        for component in ("reference_energy", "tensor_energy", "energy"):
            assert getattr(after, component).total_energy == pytest.approx(
                getattr(before, component).total_energy, rel=1.0e-11, abs=1.0e-9,
            )
    for f0, f1 in zip(baseline.mechanical_update.forces_before.forces,
                      changed.mechanical_update.forces_before.forces, strict=True):
        assert f1 == pytest.approx(transform.transform_vector(f0), rel=5e-4, abs=2e-5)
    for p0, p1 in zip(baseline.current.md_state.configuration.positions,
                      changed.current.md_state.configuration.positions, strict=True):
        assert p1 == pytest.approx(transform.transform_position(p0), abs=1.0e-7)
    for v0, v1 in zip(baseline.current.md_state.velocities,
                      changed.current.md_state.velocities, strict=True):
        assert v1 == pytest.approx(transform.transform_vector(v0), abs=1.0e-7)


def test_zero_tensor_readout_reduces_mechanical_step_to_reference_model():
    state, resources = _fixture(zero_tensor=True)
    result = _run(state, resources, mechanical_time_step=MECHANICAL_DT)
    features = _full_features(resources, state)
    reference = velocity_verlet_step(
        state=state.md_state, model=resources["model"].reference_model,
        force_evaluator=ConservativeForceEvaluator(resources["force_evaluator"].differentiation),
        features=features.base, execution=state.ternary_execution,
        cutoff=CUTOFF, time_step=MECHANICAL_DT,
    )
    assert result.energy_before_events.tensor_energy.total_energy == 0.0
    assert result.energy_after_mechanics.tensor_energy.total_energy == 0.0
    assert result.current.md_state == reference.current
    assert result.mechanical_update.forces_before == reference.forces_before
    assert result.mechanical_update.forces_after == reference.forces_after


def test_all_full_energy_channels_are_finite(full_execution):
    _, _, outcome = full_execution
    for energy in (outcome.energy_before_events, outcome.energy_after_events,
                   outcome.energy_after_mechanics):
        assert all(isfinite(v) for v in energy.energy.atomic_energies)
        assert isfinite(energy.tensor_energy.total_energy)
        assert energy.energy.total_energy == sum(energy.energy.atomic_energies)


@pytest.mark.parametrize("extra,error", (
    ({}, ValueError),
    ({"mechanical_time_step": 0.0}, ValueError),
    ({"mechanical_time_step": True}, TypeError),
    ({"mechanical_time_step": float("nan")}, ValueError),
    ({"mechanical_time_step": -0.1}, ValueError),
    ({"cutoff": 0.0, "mechanical_time_step": MECHANICAL_DT}, ValueError),
    ({"phase_parameters": PHASE_PARAMETERS}, ValueError),
    ({"ternary_event": True}, TypeError),
    ({"ternary_event": 1}, TypeError),
    ({"projection": POSITIVE, "mechanical_time_step": MECHANICAL_DT}, ValueError),
))
def test_invalid_schedule_controls_are_rejected(extra, error):
    state, resources = _fixture()
    kwargs = dict(resources)
    kwargs.update(extra)
    with pytest.raises(error):
        execute_rank_two_coupled_md_step(state, **kwargs)


def test_mismatched_feature_and_energy_channels_are_rejected():
    state, resources = _fixture()
    wrong_nodes = ScalarVectorTensorFeatures(
        base=NodeFeatureVector(nodes=(NodeFeatures(scalars=(1.0,)),)),
        rank_two=RankTwoFeatureVector(nodes=(resources["features"].rank_two.nodes[0],)),
    )
    with pytest.raises(ValueError):
        _run(state, {**resources, "features": wrong_nodes}, mechanical_time_step=MECHANICAL_DT)
    model = resources["model"]
    reference = replace(model.reference_model,
                        energy_functional=LinearInvariantEnergyFunctional((1.0,)))
    with pytest.raises(ValueError, match="two resonance channels"):
        _run(state, {**resources, "model": replace(model, reference_model=reference)},
             mechanical_time_step=MECHANICAL_DT)


def test_result_detects_unscheduled_clock_or_state_changes(full_execution):
    state, _, result = full_execution
    with pytest.raises(ValueError, match="event state differs"):
        replace(result, current=replace(result.current, resonance_time=0.0))
    with pytest.raises(ValueError, match="mechanical trajectory step differs"):
        replace(result, current=replace(result.current, md_state=state.md_state))
    with pytest.raises(ValueError, match="initial energy input"):
        replace(result, features_before_events=result.features_after_events)
    with pytest.raises(ValueError, match="mechanical state changed"):
        replace(result, mechanical_update=None)


def test_deterministic_result_is_frozen(full_execution):
    _, _, result = full_execution
    with pytest.raises(FrozenInstanceError):
        result.current = result.previous
    with pytest.raises(FrozenInstanceError):
        result.features_after_events = result.features_before_events
