
"""End-to-end checks for the typed FLiBe rank-two TR-EIP/MD boundary.

Reconstruct the general multirate step and its three domain energy evaluations
independently. Qualify force gradients of the complete energy, active-neutral
routing with pending targets, independent clocks, E(3) transformations and
retained thermodynamic context.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

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
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.coupled_rank_two_tr_eip_md import (
    FLiBeRankTwoTREIPMDCoupledStep,
    execute_flibe_rank_two_tr_eip_coupled_md_step,
)
from tr_eif.flibe.rank_two_tr_eip import FLiBeRankTwoTREIPModel
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState, append_md_resonance_features
from tr_eif.md.execution import velocity_verlet_step
from tr_eif.md.rank_two_coupled_execution import execute_rank_two_coupled_md_step
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
MASSES = (6.94, 6.94, 9.0121831, 18.998403163, 18.998403163,
          18.998403163, 18.998403163)
VELOCITIES = tuple(
    (0.001 * (i - 3), 0.0005 * ((i % 3) - 1), 0.00025 * (i % 2))
    for i in range(7)
)
CUTOFF = 1.6
PHASE_DT = 0.1
MECHANICAL_DT = 1.0e-4
PHASE_PARAMETERS = PhaseDynamicsParameters(
    coupling=(0.35,) * 7, phase_lag=(0.13,) * 7,
)
THRESHOLDS = TernaryTargetThresholds(negative=-0.25, positive=0.5)
PROVENANCE = ParameterProvenance.TEST_FIXTURE
THERMO = FLiBeThermodynamicState(850.0, 101325.0)
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def _interpretation(reverse=False):
    return FLiBeTernaryInterpretation(
        projection=(ResonanceProjection(-1.0, 0.0) if reverse
                    else ResonanceProjection(1.0, -0.1)),
        thresholds=THRESHOLDS, provenance=PROVENANCE,
    )


def _fixture(transform=None, initial=TernaryState.NEGATIVE, zero_tensor=False):
    positions, velocities = POSITIONS, VELOCITIES
    if transform is not None:
        positions = tuple(transform.transform_position(p) for p in positions)
        velocities = tuple(transform.transform_vector(v) for v in velocities)
    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(species=SPECIES, positions=positions),
            velocities=velocities, masses=MASSES, step=4, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
            frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states((initial,) * 7),
        resonance_time=0.4, resonance_step_count=2, ternary_event_count=5,
    )
    base = NodeFeatureVector(nodes=tuple(
        NodeFeatures(scalars=(0.5 + 0.25 * i,),
                     vectors=((1.0, 0.1 * i, -0.05 * i),))
        for i in range(7)
    ))
    tensors = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor(((1.0 + 0.1 * i, 0.2, -0.3),
                       (0.4, 0.8 - 0.05 * i, 0.1),
                       (-0.2, 0.3, 0.6))),
        RankTwoTensor.outer((1.0, 0.25 * i - 0.5, 0.3),
                            (0.2, 0.8, -0.1 * i)),
    ) for i in range(7)))
    features = ScalarVectorTensorFeatures(base, tensors)
    if transform is not None:
        features = features.transformed(transform)
    shared = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    weights = (
        RankTwoChannelEnergyWeights() if zero_tensor else RankTwoChannelEnergyWeights(
            trace=0.15, isotropic_norm_squared=0.08,
            symmetric_traceless_norm_squared=0.3,
            antisymmetric_norm_squared=0.2,
        ),
        RankTwoChannelEnergyWeights() if zero_tensor else RankTwoChannelEnergyWeights(
            trace=-0.12, isotropic_norm_squared=0.05,
            symmetric_traceless_norm_squared=-0.08,
            antisymmetric_norm_squared=0.1,
        ),
    )
    model = FLiBeRankTwoTREIPModel(
        tr_eip_model=FLiBeTREIPModel(shared, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=shared,
            tensor_readout=RankTwoInvariantEnergyReadout(weights),
            coupling=RankTwoMessageCoupling(
                tensor_scale=0.7, scalar_dyad_scale=0.2,
                vector_dyad_scale=-0.15,
                scalar_channel_index=0, vector_channel_index=0,
            ),
        ),
    )
    resources = dict(
        model=model,
        force_evaluator=RankTwoConservativeForceEvaluator(
            CoordinateDifferentiation(step=1.0e-5),
        ),
        features=features,
        thermodynamic_state=THERMO,
        interpretation=_interpretation(),
        cutoff=CUTOFF,
    )
    return state, resources


def _run(state, resources, **schedule):
    return execute_flibe_rank_two_tr_eip_coupled_md_step(
        state, **resources, **schedule,
    )


def _full_schedule():
    return dict(
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True, mechanical_time_step=MECHANICAL_DT,
    )


def _boundary(model, features, md_state, resonance, retained, thermodynamic_state):
    config = FLiBeConfiguration(md_state.configuration)
    graph = build_cutoff_graph(config.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=config,
        coordination=build_flibe_coordination_state(config, graph),
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance,
        provenance=model.tr_eip_model.provenance,
        source=model.tr_eip_model.source,
    )
    return model.evaluate(config, graph, features, descriptor, retained)


@pytest.fixture(scope="module")
def combined():
    state, resources = _fixture()
    return state, resources, _run(state, resources, **_full_schedule())


def test_domain_wrapper_matches_generic_rank_two_scheduler(combined):
    state, inputs, result = combined
    assert isinstance(result, FLiBeRankTwoTREIPMDCoupledStep)
    direct = execute_rank_two_coupled_md_step(
        state, model=inputs["model"].rank_two_model,
        force_evaluator=inputs["force_evaluator"],
        features=inputs["features"], cutoff=CUTOFF,
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True,
        projection=inputs["interpretation"].projection,
        thresholds=inputs["interpretation"].thresholds,
        mechanical_time_step=MECHANICAL_DT,
    )
    assert result.coupled_step == direct
    assert result.current == direct.current
    assert result.current.resonance_step_count == state.resonance_step_count + 1
    assert result.current.ternary_event_count == state.ternary_event_count + 1
    assert result.current.md_state.step == state.md_state.step + 1
    assert direct.requested_target is TernaryState.POSITIVE
    assert direct.requested_targets == (TernaryState.POSITIVE,) * 7


def test_all_three_flibe_energy_boundaries_are_independently_rebuilt(combined):
    state, inputs, result = combined
    model, features = inputs["model"], inputs["features"]
    expected = (
        _boundary(model, features, state.md_state, state.resonance_state,
                  state.ternary_execution, THERMO),
        _boundary(model, features, state.md_state, result.current.resonance_state,
                  result.current.ternary_execution, THERMO),
        _boundary(model, features, result.current.md_state, result.current.resonance_state,
                  result.current.ternary_execution, THERMO),
    )
    assert (result.before_events, result.after_events, result.after_mechanics) == expected
    for observed, recorded in zip(
        expected,
        (result.coupled_step.energy_before_events,
         result.coupled_step.energy_after_events,
         result.coupled_step.energy_after_mechanics),
        strict=True,
    ):
        assert observed.augmented_result == recorded
        assert observed.reference_result.energy_result.energy == recorded.reference_energy
        assert observed.reference_energy == recorded.reference_energy
        assert observed.tensor_energy == recorded.tensor_energy
        assert observed.energy == recorded.energy
        for reference, tensor, total in zip(
            observed.reference_energy.atomic_energies,
            observed.tensor_energy.atomic_energies,
            observed.energy.atomic_energies, strict=True,
        ):
            assert total == fsum((reference, tensor))
    assert result.event_potential_energy_change == pytest.approx(
        expected[1].energy.total_energy - expected[0].energy.total_energy
    )
    assert result.mechanical_potential_energy_change == pytest.approx(
        expected[2].energy.total_energy - expected[1].energy.total_energy
    )
    assert abs(expected[1].tensor_energy.total_energy) > 1.0e-8


def test_resonance_ternary_coordination_and_thermodynamic_types_remain_distinct(combined):
    state, inputs, result = combined
    assert result.before_events.resonance.resonance_state == state.resonance_state
    assert result.after_events.resonance.resonance_state == result.current.resonance_state
    assert result.after_mechanics.resonance.resonance_state == result.current.resonance_state
    assert result.before_events.resonance.coordinate != result.after_events.resonance.coordinate
    for boundary in (result.before_events, result.after_events, result.after_mechanics):
        assert boundary.configuration.species == boundary.resonance.configuration.species
        assert boundary.resonance.thermodynamic_state == result.thermodynamic_state == THERMO
        assert boundary.resonance.coordinate == resonance_descriptor(
            boundary.resonance.resonance_state
        ).as_coordinate()
        assert boundary.resonance.coordination == build_flibe_coordination_state(
            boundary.configuration, boundary.graph
        )
        assert boundary.resonance_features.base.scalar_channel_count == (
            inputs["features"].base.scalar_channel_count + 2
        )
        assert boundary.resonance_features.rank_two == inputs["features"].rank_two
        assert boundary.execution.node_count == len(SPECIES)


def test_opposite_request_enters_active_neutral_before_mechanics(combined):
    state, _, result = combined
    update = result.coupled_step.event_update
    assert update is not None
    assert update.ternary_update is not None
    assert update.ternary_update.committed_count == len(SPECIES)
    assert result.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(n.pending_target is TernaryState.POSITIVE
               for n in result.current.ternary_execution.states)
    assert result.after_events.execution == result.after_mechanics.execution
    for node in update.ternary_update.execution.node_steps:
        assert node.route is not None
        assert node.route.transition.source is TernaryState.NEGATIVE
        assert node.route.transition.target is TernaryState.NEUTRAL
        assert not is_direct_opposite_transition(
            node.route.transition.source, node.route.transition.target,
        )


def test_full_energy_forces_are_coordinate_derivatives(combined):
    state, inputs, result = combined
    md = result.coupled_step.mechanical_update
    assert md is not None
    force_model = inputs["model"].rank_two_model
    force_evaluator = inputs["force_evaluator"]
    graph = build_cutoff_graph(state.md_state.configuration, CUTOFF)
    augmented = result.coupled_step.features_after_events
    retained = result.current.ternary_execution
    assert md.forces_before == force_evaluator.evaluate(
        force_model, state.md_state.configuration, graph, augmented, retained,
    )
    assert md.forces_after == force_evaluator.evaluate(
        force_model, md.current.configuration, md.graph_after, augmented, retained,
    )
    step = 2.5e-5
    for atom, axis in ((0, 0), (2, 1), (5, 2)):
        energies = []
        for displacement in (step, -step):
            positions = list(state.md_state.configuration.positions)
            p = list(positions[atom])
            p[axis] += displacement
            positions[atom] = tuple(p)
            trial = MolecularDynamicsState(
                configuration=AtomicConfiguration(species=SPECIES, positions=tuple(positions)),
                velocities=state.md_state.velocities, masses=state.md_state.masses,
                step=state.md_state.step, time=state.md_state.time,
            )
            energy = _boundary(
                inputs["model"], inputs["features"], trial,
                result.current.resonance_state, retained, THERMO,
            ).energy.total_energy
            energies.append(energy)
        gradient = -(energies[0] - energies[1]) / (2.0 * step)
        assert md.forces_before.forces[atom][axis] == pytest.approx(
            gradient, rel=5.0e-4, abs=5.0e-5,
        )
    assert all(isfinite(component) for force in md.forces_before.forces
               for component in force)


def test_phase_only_changes_resonance_clock_without_mechanical_step():
    state, inputs = _fixture()
    result = _run(state, inputs, phase_parameters=PHASE_PARAMETERS,
                  phase_time_step=PHASE_DT)
    assert result.coupled_step.event_update is not None
    assert result.coupled_step.mechanical_update is None
    assert result.current.md_state == state.md_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.current.resonance_time == pytest.approx(state.resonance_time + PHASE_DT)
    assert result.current.ternary_event_count == state.ternary_event_count
    assert result.after_events == result.after_mechanics
    assert result.after_events.tensor_energy == result.before_events.tensor_energy
    assert result.before_events.reference_energy != result.after_events.reference_energy


def test_ternary_only_updates_retained_state_without_phase_or_mechanics():
    state, inputs = _fixture()
    result = _run(state, inputs, ternary_event=True)
    assert result.coupled_step.event_update is not None
    assert result.coupled_step.mechanical_update is None
    assert result.current.md_state == state.md_state
    assert result.current.resonance_state == state.resonance_state
    assert result.current.resonance_time == state.resonance_time
    assert result.current.ternary_event_count == state.ternary_event_count + 1
    assert result.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert result.after_events == result.after_mechanics
    assert result.event_potential_energy_change == pytest.approx(
        result.after_events.energy.total_energy - result.before_events.energy.total_energy,
    )


def test_mechanics_only_preserves_resonance_and_ternary_clocks():
    state, inputs = _fixture()
    result = _run(state, inputs, mechanical_time_step=MECHANICAL_DT)
    assert result.coupled_step.event_update is None
    assert result.coupled_step.mechanical_update is not None
    assert result.before_events == result.after_events
    assert result.event_potential_energy_change == 0.0
    assert result.current.resonance_state == state.resonance_state
    assert result.current.ternary_execution == state.ternary_execution
    assert result.current.resonance_time == state.resonance_time
    assert result.current.ternary_event_count == state.ternary_event_count
    assert result.current.md_state.step == state.md_state.step + 1


def test_pending_target_survives_hold_and_new_opposite_request():
    state, inputs = _fixture()
    entry = _run(state, inputs, ternary_event=True,
                 guards=(TernaryExecutionGuard.neutral_entry_only(),) * 7)
    assert entry.current.ternary_execution.has_pending_targets
    reverse = {**inputs, "interpretation": _interpretation(reverse=True)}
    held = _run(entry.current, reverse, ternary_event=True,
                guards=(TernaryExecutionGuard.hold(),) * 7)
    assert held.coupled_step.requested_target is TernaryState.NEGATIVE
    assert held.coupled_step.requested_targets == (TernaryState.POSITIVE,) * 7
    assert held.coupled_step.event_update.ternary_update.committed_count == 0
    assert held.current.ternary_execution == entry.current.ternary_execution
    assert held.event_potential_energy_change == 0.0
    exit_step = _run(held.current, reverse, ternary_event=True,
                     guards=(TernaryExecutionGuard.neutral_exit_only(),) * 7)
    assert exit_step.current.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7
    assert not exit_step.current.ternary_execution.has_pending_targets
    assert exit_step.current.ternary_event_count == state.ternary_event_count + 3
    assert exit_step.current.md_state == state.md_state


def test_reverse_polarity_also_routes_via_active_neutral():
    state, inputs = _fixture(initial=TernaryState.POSITIVE)
    reverse = {**inputs, "interpretation": _interpretation(reverse=True)}
    entry = _run(state, reverse, ternary_event=True)
    assert entry.coupled_step.requested_target is TernaryState.NEGATIVE
    assert entry.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(node.pending_target is TernaryState.NEGATIVE
               for node in entry.current.ternary_execution.states)
    exit_step = _run(entry.current, inputs, ternary_event=True)
    assert exit_step.current.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert not exit_step.current.ternary_execution.has_pending_targets
    for event in (entry, exit_step):
        for node in event.coupled_step.event_update.ternary_update.execution.node_steps:
            assert node.route is not None
            assert not is_direct_opposite_transition(node.route.transition.source,
                                                     node.route.transition.target)


def test_independent_interleaved_schedulers_and_deterministic_replay():
    state, inputs = _fixture()
    schedules = (
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.neutral_entry_only(),) * 7),
        dict(mechanical_time_step=MECHANICAL_DT),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.hold(),) * 7),
        dict(phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT / 2),
        dict(ternary_event=True, guards=(TernaryExecutionGuard.neutral_exit_only(),) * 7),
    )

    def replay():
        current = state
        history = []
        for schedule in schedules:
            result = _run(current, inputs, **schedule)
            assert result.coupled_step.previous == current
            history.append(result)
            current = result.current
        return tuple(history)

    first = replay()
    assert replay() == first
    last = first[-1].current
    assert last.md_state.step == state.md_state.step + 1
    assert last.md_state.time == pytest.approx(state.md_state.time + MECHANICAL_DT)
    assert last.resonance_time == pytest.approx(state.resonance_time + 1.5 * PHASE_DT)
    assert last.resonance_step_count == state.resonance_step_count + 2
    assert last.ternary_event_count == state.ternary_event_count + 3
    assert last.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 0.5)),
    (REFLECTION, (-1.0, 0.7, 2.0)),
))
def test_e3_energy_invariance_and_force_covariance(matrix, translation):
    transform = E3Transformation(matrix, translation)
    state, inputs = _fixture()
    transformed_state, transformed_inputs = _fixture(transform=transform)
    baseline = _run(state, inputs, **_full_schedule())
    transformed = _run(transformed_state, transformed_inputs, **_full_schedule())
    assert transformed.current.resonance_state == baseline.current.resonance_state
    assert transformed.current.ternary_execution == baseline.current.ternary_execution
    for name in ("before_events", "after_events", "after_mechanics"):
        a = getattr(baseline, name)
        b = getattr(transformed, name)
        for field in ("reference_energy", "tensor_energy", "energy"):
            assert getattr(b, field).total_energy == pytest.approx(
                getattr(a, field).total_energy, rel=1.0e-11, abs=1.0e-8,
            )
    for f0, f1 in zip(
        baseline.coupled_step.mechanical_update.forces_before.forces,
        transformed.coupled_step.mechanical_update.forces_before.forces,
        strict=True,
    ):
        assert f1 == pytest.approx(transform.transform_vector(f0), rel=5e-4, abs=2e-5)
    for p0, p1 in zip(baseline.current.md_state.configuration.positions,
                      transformed.current.md_state.configuration.positions, strict=True):
        assert p1 == pytest.approx(transform.transform_position(p0), abs=1e-7)
    for v0, v1 in zip(baseline.current.md_state.velocities,
                      transformed.current.md_state.velocities, strict=True):
        assert v1 == pytest.approx(transform.transform_vector(v0), abs=1e-7)


def test_zero_tensor_weights_recover_reference_md_mechanics():
    state, inputs = _fixture(zero_tensor=True)
    result = _run(state, inputs, mechanical_time_step=MECHANICAL_DT)
    reference = velocity_verlet_step(
        state=state.md_state,
        model=inputs["model"].tr_eip_model.energy_model,
        force_evaluator=ConservativeForceEvaluator(inputs["force_evaluator"].differentiation),
        features=append_md_resonance_features(
            inputs["features"].base, resonance_descriptor(state.resonance_state),
        ),
        execution=state.ternary_execution,
        cutoff=CUTOFF, time_step=MECHANICAL_DT,
    )
    assert result.before_events.tensor_energy.total_energy == 0.0
    assert result.after_mechanics.tensor_energy.total_energy == 0.0
    assert result.current.md_state == reference.current
    assert result.coupled_step.mechanical_update.forces_before == reference.forces_before
    assert result.coupled_step.mechanical_update.forces_after == reference.forces_after


def test_thermodynamic_context_changes_without_relabeling_resonance():
    state, inputs = _fixture()
    first = _run(state, inputs, phase_parameters=PHASE_PARAMETERS,
                 phase_time_step=PHASE_DT)
    changed = FLiBeThermodynamicState(900.0, 202650.0)
    second = _run(state, {**inputs, "thermodynamic_state": changed},
                  phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT)
    assert first.current == second.current
    for name in ("before_events", "after_events", "after_mechanics"):
        assert getattr(first, name).resonance.coordinate == getattr(second, name).resonance.coordinate
        assert getattr(first, name).energy == getattr(second, name).energy
        assert getattr(first, name).resonance.thermodynamic_state == THERMO
        assert getattr(second, name).resonance.thermodynamic_state == changed


@pytest.mark.parametrize("missing", (
    "model", "force_evaluator", "features", "thermodynamic_state", "interpretation",
))
def test_untyped_dependencies_are_rejected(missing):
    state, inputs = _fixture()
    inputs[missing] = None
    with pytest.raises(TypeError):
        _run(state, inputs, mechanical_time_step=MECHANICAL_DT)


@pytest.mark.parametrize("schedule,error", (
    ({}, ValueError),
    ({"phase_parameters": PHASE_PARAMETERS}, ValueError),
    ({"phase_time_step": -0.1, "phase_parameters": PHASE_PARAMETERS}, ValueError),
    ({"mechanical_time_step": 0.0}, ValueError),
    ({"mechanical_time_step": True}, TypeError),
    ({"ternary_event": True, "phase_time_step": PHASE_DT}, TypeError),
    ({"ternary_event": 1}, TypeError),
    ({"ternary_event": False, "guards": (TernaryExecutionGuard.hold(),) * 7}, ValueError),
))
def test_invalid_schedule_contracts(schedule, error):
    state, inputs = _fixture()
    with pytest.raises(error):
        _run(state, inputs, **schedule)


def test_species_stoichiometry_and_node_count_are_checked():
    state, inputs = _fixture()
    invalid_species = replace(state.md_state.configuration,
                              species=("Li", "Li", "Be", "F", "F", "F", "Li"))
    changed = replace(state, md_state=replace(state.md_state, configuration=invalid_species))
    with pytest.raises(ValueError, match="stoichiometry"):
        _run(changed, inputs, mechanical_time_step=MECHANICAL_DT)
    features = ScalarVectorTensorFeatures(
        base=NodeFeatureVector(nodes=inputs["features"].base.nodes[:2]),
        rank_two=RankTwoFeatureVector(nodes=inputs["features"].rank_two.nodes[:2]),
    )
    with pytest.raises(ValueError, match="feature and atom counts"):
        _run(state, {**inputs, "features": features}, mechanical_time_step=MECHANICAL_DT)


def test_corrupted_boundary_records_are_rejected(combined):
    state, inputs, result = combined
    with pytest.raises(ValueError, match="before_events continuous resonance"):
        replace(result, before_events=result.after_events)
    with pytest.raises(ValueError, match="after_events continuous resonance"):
        replace(result, after_events=result.before_events)
    with pytest.raises(ValueError, match="after_mechanics atomic configuration"):
        replace(result, after_mechanics=result.before_events)
    with pytest.raises(ValueError, match="thermodynamic context"):
        replace(result, thermodynamic_state=FLiBeThermodynamicState(900.0, 101325.0))
    with pytest.raises(ValueError, match="ternary request"):
        replace(result, interpretation=_interpretation(reverse=True))
    with pytest.raises(TypeError, match="before_events"):
        replace(result, before_events=None)


def test_immutable_evidence_and_determinism(combined):
    state, inputs, result = combined
    with pytest.raises((FrozenInstanceError, TypeError)):
        result.current = state
    with pytest.raises(FrozenInstanceError):
        result.after_events = result.before_events
    first = _run(state, inputs, phase_parameters=PHASE_PARAMETERS,
                 phase_time_step=PHASE_DT, ternary_event=True)
    assert first == _run(state, inputs, phase_parameters=PHASE_PARAMETERS,
                         phase_time_step=PHASE_DT, ternary_event=True)
