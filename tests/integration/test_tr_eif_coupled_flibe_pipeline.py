
"""End-to-end resonance/ternary/equivariant energy qualification in TR-EIF.

A seven-atom FLiBe fixture exercises the framework's coupled execution path:
Kuramoto-Sakaguchi phase integration, continuous resonance description,
explicit ternary target request, guarded active-neutral routing, retained
state conditioning, E(3)-equivariant message passing and scalar energy.
Each scheduler boundary is explicit; pending targets are kept distinct from
committed states, and geometric transformations never reverse ternary polarity.
"""

from __future__ import annotations

from math import isclose, pi

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import LinearInvariantEnergyFunctional, ReferenceEnergyModel
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceState,
    euler_step,
    phase_derivatives,
)
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
    execute_ternary_vector_step,
    is_direct_opposite_transition,
)

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0),
    (1.1, 0.7, 0.8),
    (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
TIME_STEP = 0.1


def _geometry(transformation: E3Transformation | None = None):
    positions = (
        POSITIONS if transformation is None else tuple(
            transformation.transform_position(point) for point in POSITIONS
        )
    )
    config = FLiBeConfiguration(AtomicConfiguration(species=SPECIES, positions=positions))
    graph = build_cutoff_graph(config.configuration, cutoff=1.6)
    assert graph.node_count == len(SPECIES) and graph.edges
    return config, graph


def _features(transformation: E3Transformation | None = None):
    features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * atom,),
            vectors=((1.0, 0.1 * atom, -0.05 * atom),),
        )
        for atom in range(len(SPECIES))
    ))
    return features if transformation is None else transformation.transform_feature_vector(features)


def _resonance_initial() -> ResonanceState:
    return ResonanceState(
        phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
        frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
    )


def _phase_parameters() -> PhaseDynamicsParameters:
    return PhaseDynamicsParameters(
        coupling=(0.35,) * len(SPECIES),
        phase_lag=(0.13,) * len(SPECIES),
    )


def _descriptor(configuration, graph, state):
    return build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=FLiBeThermodynamicState(temperature=850.0, pressure=101325.0),
        resonance_state=state,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _model() -> FLiBeTREIPModel:
    return FLiBeTREIPModel(
        energy_model=ReferenceEnergyModel(
            message_operator=RadialMessageOperator(distance_scale=1.1),
            conditioning=TernaryConditioning(
                negative_scale=0.5,
                neutral_scale=1.25,
                positive_scale=1.5,
            ),
            energy_functional=LinearInvariantEnergyFunctional(
                weights=(0.4, 0.7, -0.3), bias=0.1,
            ),
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _chain():
    configuration, graph = _geometry()
    state_initial = _resonance_initial()
    state_next = euler_step(state_initial, _phase_parameters(), graph, TIME_STEP)
    descriptor_initial = _descriptor(configuration, graph, state_initial)
    descriptor_next = _descriptor(configuration, graph, state_next)
    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0, frequency_spread_weight=-0.1,
        ),
        thresholds=TernaryTargetThresholds(negative=-0.25, positive=0.5),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )
    requested = interpretation.target_from_descriptor(descriptor_next.descriptor)
    retained = TernaryExecutionVector.from_retained_states(
        (TernaryState.NEGATIVE,) * len(SPECIES)
    )
    entry = execute_ternary_vector_step(
        retained, requested_targets=(requested,) * len(SPECIES),
        guards=(TernaryExecutionGuard.neutral_entry_only(),) * len(SPECIES),
    )
    held = execute_ternary_vector_step(
        entry.current, guards=(TernaryExecutionGuard.hold(),) * len(SPECIES),
    )
    exit_step = execute_ternary_vector_step(
        held.current, guards=(TernaryExecutionGuard.neutral_exit_only(),) * len(SPECIES),
    )
    model = _model()
    results = tuple(
        model.evaluate(configuration, graph, _features(), descriptor_next, stage)
        for stage in (retained, entry.current, held.current, exit_step.current)
    )
    return (
        state_initial, state_next, descriptor_initial, descriptor_next,
        requested, retained, entry, held, exit_step, results, model,
    )


def test_nonlinear_resonance_step_precedes_ternary_request():
    initial, evolved, before, after, target, *_ = _chain()
    graph = _geometry()[1]
    derivatives = phase_derivatives(initial, _phase_parameters(), graph)
    assert evolved != initial
    assert evolved.frequencies == initial.frequencies
    for previous, next_phase, derivative in zip(
        initial.phases, evolved.phases, derivatives, strict=True,
    ):
        assert next_phase == pytest.approx((previous + TIME_STEP * derivative) % (2.0 * pi))
    assert before.resonance_state is initial
    assert after.resonance_state is evolved
    assert after.coordinate != before.coordinate
    assert target is TernaryState.POSITIVE
    assert after.phase_order != after.frequency_spread


def test_opposite_request_routes_through_active_neutral_with_pending_retention():
    _, _, _, _, requested, retained, entry, held, exit_step, *_ = _chain()
    assert requested is TernaryState.POSITIVE
    assert retained.retained_states == (TernaryState.NEGATIVE,) * len(SPECIES)
    assert entry.committed_count == len(SPECIES)
    assert entry.current.retained_states == (TernaryState.NEUTRAL,) * len(SPECIES)
    assert all(s.pending_target is requested for s in entry.current.states)
    assert held.committed_count == 0
    assert held.current == entry.current
    assert held.current.has_pending_targets
    assert exit_step.committed_count == len(SPECIES)
    assert exit_step.current.retained_states == (requested,) * len(SPECIES)
    assert not exit_step.current.has_pending_targets
    for stage in (entry, exit_step):
        for step in stage.node_steps:
            assert step.route is not None
            assert not is_direct_opposite_transition(step.route.transition.source, step.route.transition.target)
    assert all(
        step.route.transition.target is TernaryState.NEUTRAL
        for step in entry.node_steps
    )
    assert all(
        step.route.transition.source is TernaryState.NEUTRAL
        for step in exit_step.node_steps
    )


def test_interatomic_energy_consumes_committed_not_requested_ternary_state():
    *_, retained, entry, held, exit_step, evaluations, model = _chain()
    negative, neutral, neutral_hold, positive = evaluations
    for execution, result in zip(
        (retained, entry.current, held.current, exit_step.current),
        evaluations, strict=True,
    ):
        assert result.execution == execution
        assert result.energy_result.energy.atom_count == len(SPECIES)
        assert result.energy_result.layer_result.input_features == result.resonance_conditioned_features
        for input_node, conditioned_node in zip(
            result.input_features.nodes,
            result.resonance_conditioned_features.nodes, strict=True,
        ):
            assert conditioned_node.scalars[:-2] == input_node.scalars
            assert conditioned_node.vectors == input_node.vectors
    assert neutral.energy_result.energy.total_energy == neutral_hold.energy_result.energy.total_energy
    assert not isclose(negative.energy_result.energy.total_energy, neutral.energy_result.energy.total_energy,
                       rel_tol=1.0e-12, abs_tol=1.0e-12)
    assert not isclose(neutral.energy_result.energy.total_energy, positive.energy_result.energy.total_energy,
                       rel_tol=1.0e-12, abs_tol=1.0e-12)
    assert model.resonance_scalar_channel_count == 2


@pytest.mark.parametrize("matrix,translation", (
    (((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)), (2.0, -3.0, 1.0)),
    (((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)), (0.0, 0.0, 0.0)),
))
def test_full_energy_trace_is_e3_invariant_with_fixed_ternary_polarity(matrix, translation):
    *_, entry, held, exit_step, evaluations, model = _chain()
    transformation = E3Transformation(matrix=matrix, translation=translation)
    config, graph = _geometry(transformation)
    initial = _resonance_initial()
    evolved = euler_step(initial, _phase_parameters(), graph, TIME_STEP)
    descriptor = _descriptor(config, graph, evolved)
    assert descriptor.coordinate == pytest.approx(evaluations[0].resonance.coordinate)
    features = _features(transformation)
    states = (evaluations[0].execution, entry.current, held.current, exit_step.current)
    for baseline, state in zip(evaluations, states, strict=True):
        transformed = model.evaluate(config, graph, features, descriptor, state)
        assert transformed.execution.retained_states == baseline.execution.retained_states
        assert transformed.energy_result.energy.total_energy == pytest.approx(
            baseline.energy_result.energy.total_energy, rel=1.0e-12, abs=1.0e-12,
        )
        expected_features = transformation.transform_feature_vector(
            baseline.energy_result.layer_result.current,
        )
        for expected, actual in zip(
            expected_features.nodes, transformed.energy_result.layer_result.current.nodes, strict=True,
        ):
            assert actual.scalars == pytest.approx(expected.scalars, rel=1.0e-12, abs=1.0e-12)
            for av, ev in zip(actual.vectors, expected.vectors, strict=True):
                assert av == pytest.approx(ev, rel=1.0e-12, abs=1.0e-12)


def test_pending_target_cannot_be_replaced_by_next_request():
    *_, entry, _, _, _, _ = _chain()
    with pytest.raises(ValueError, match="pending target"):
        execute_ternary_vector_step(
            entry.current,
            requested_targets=(TernaryState.NEGATIVE,) * len(SPECIES),
        )


def test_repeated_coupled_pipeline_is_deterministic():
    a = _chain()
    b = _chain()
    assert a == b


def test_continuous_resonance_changes_energy_at_fixed_retained_state():
    _, _, before, after, _, retained, *_ = _chain()
    config, graph = _geometry()
    model = _model()
    energy_before = model.evaluate(
        config, graph, _features(), before, retained
    ).energy_result.energy.total_energy
    energy_after = model.evaluate(
        config, graph, _features(), after, retained
    ).energy_result.energy.total_energy
    assert not isclose(energy_before, energy_after, rel_tol=1.0e-12, abs_tol=1.0e-12)


def test_reverse_polarity_request_uses_separate_neutral_entry_and_exit():
    config, graph = _geometry()
    state = ResonanceState(
        phases=(0.0, pi / 2, pi, 3 * pi / 2, 0.0, pi / 2, pi),
        frequencies=(-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0),
    )
    evolved = euler_step(state, _phase_parameters(), graph, TIME_STEP)
    descriptor = _descriptor(config, graph, evolved)
    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(
            phase_order_weight=1.0, frequency_spread_weight=-0.4,
        ),
        thresholds=TernaryTargetThresholds(negative=-0.25, positive=0.5),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )
    target = interpretation.target_from_descriptor(descriptor.descriptor)
    assert target is TernaryState.NEGATIVE
    starting = TernaryExecutionVector.from_retained_states(
        (TernaryState.POSITIVE,) * len(SPECIES)
    )
    first = execute_ternary_vector_step(
        starting, requested_targets=(target,) * len(SPECIES),
        guards=(TernaryExecutionGuard.neutral_entry_only(),) * len(SPECIES),
    )
    assert first.current.retained_states == (TernaryState.NEUTRAL,) * len(SPECIES)
    assert all(node.pending_target is target for node in first.current.states)
    second = execute_ternary_vector_step(
        first.current, guards=(TernaryExecutionGuard.neutral_exit_only(),) * len(SPECIES),
    )
    assert second.current.retained_states == (TernaryState.NEGATIVE,) * len(SPECIES)
    assert not second.current.has_pending_targets
    assert all(
        not is_direct_opposite_transition(
            step.route.transition.source, step.route.transition.target
        )
        for stage in (first, second) for step in stage.node_steps
    )
    model = _model()
    outputs = tuple(
        model.evaluate(config, graph, _features(), descriptor, execution)
        for execution in (starting, first.current, second.current)
    )
    assert outputs[0].energy_result.energy.total_energy != pytest.approx(
        outputs[1].energy_result.energy.total_energy
    )
    assert outputs[1].energy_result.energy.total_energy != pytest.approx(
        outputs[2].energy_result.energy.total_energy
    )


def test_neutral_entry_guard_preserves_retained_state_and_energy():
    _, _, _, descriptor, requested, retained, *_ = _chain()
    blocked = execute_ternary_vector_step(
        retained, requested_targets=(requested,) * len(SPECIES),
        guards=(TernaryExecutionGuard.hold(),) * len(SPECIES),
    )
    assert blocked.committed_count == 0
    assert blocked.current == retained
    config, graph = _geometry()
    model = _model()
    first = model.evaluate(config, graph, _features(), descriptor, retained)
    second = model.evaluate(config, graph, _features(), descriptor, blocked.current)
    assert first.energy_result.energy == second.energy_result.energy
