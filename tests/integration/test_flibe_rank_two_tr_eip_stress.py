
"""Integration checks for FLiBe rank-two TR-EIP stress and multirate MD.

Compare strain-derived stress with independently reconstructed energy samples,
retain the separate scalar/vector and rank-two contributions, and inspect
resonance, active-neutral routing, E(3) covariance and pressure boundaries.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    ConservativeStressEvaluator,
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
from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
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
    execute_flibe_rank_two_tr_eip_coupled_md_step,
)
from tr_eif.flibe.rank_two_tr_eip import FLiBeRankTwoTREIPModel
from tr_eif.flibe.rank_two_tr_eip_stress import (
    FLiBeRankTwoTREIPMDStressTrace,
    FLiBeRankTwoTREIPStressResult,
    evaluate_flibe_rank_two_tr_eip_md_stresses,
    evaluate_flibe_rank_two_tr_eip_stress,
)
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionState,
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
CELL = ((8.0, 0.0, 0.0), (0.0, 8.0, 0.0), (0.0, 0.0, 8.0))
MASSES = (6.94, 6.94, 9.0121831, 18.998403163, 18.998403163,
          18.998403163, 18.998403163)
VELOCITIES = tuple(
    (0.001 * (i - 3), 0.0005 * ((i % 3) - 1), 0.00025 * (i % 2))
    for i in range(7)
)
CUTOFF = 1.6
PHASE_DT = 0.1
MECHANICAL_DT = 1.0e-4
STRESS_STEP = 1.0e-6
PHASE_PARAMETERS = PhaseDynamicsParameters(
    coupling=(0.35,) * 7, phase_lag=(0.13,) * 7,
)
THRESHOLDS = TernaryTargetThresholds(negative=-0.25, positive=0.5)
THERMO = FLiBeThermodynamicState(850.0, 101325.0)
PROVENANCE = ParameterProvenance.TEST_FIXTURE
ROTATION = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
REFLECTION = ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
STRAIN_PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def _interpretation(reverse=False):
    return FLiBeTernaryInterpretation(
        projection=(ResonanceProjection(-1.0, 0.0) if reverse
                    else ResonanceProjection(1.0, -0.1)),
        thresholds=THRESHOLDS,
        provenance=PROVENANCE,
    )


def _fixture(*, transform=None, initial=TernaryState.NEGATIVE,
             zero_tensor=False, thermodynamic_state=THERMO):
    positions, velocities, cell = POSITIONS, VELOCITIES, CELL
    if transform is not None:
        positions = tuple(transform.transform_position(p) for p in positions)
        velocities = tuple(transform.transform_vector(v) for v in velocities)
        cell = tuple(transform.transform_vector(v) for v in cell)
    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(
                species=SPECIES, positions=positions,
                cell=cell, periodic=(True, True, True),
            ),
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
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        ) for i in range(7)
    ))
    tensors = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor(((1.0 + 0.1 * i, 0.2, -0.3),
                       (0.4, 0.8 - 0.05 * i, 0.1),
                       (-0.2, 0.3, 0.6))),
        RankTwoTensor.outer(
            (1.0, 0.25 * i - 0.5, 0.3), (0.2, 0.8, -0.1 * i),
        ),
    ) for i in range(7)))
    features = ScalarVectorTensorFeatures(base, tensors)
    if transform is not None:
        features = features.transformed(transform)
    reference = ReferenceEnergyModel(
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
        tr_eip_model=FLiBeTREIPModel(reference, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=reference,
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
        stress_evaluator=RankTwoConservativeStressEvaluator(
            CellStrainDifferentiation(step=STRESS_STEP),
        ),
        features=features,
        thermodynamic_state=thermodynamic_state,
        interpretation=_interpretation(),
        cutoff=CUTOFF,
    )
    return state, resources


def _run(state, resources, **schedule):
    return execute_flibe_rank_two_tr_eip_coupled_md_step(
        state,
        model=resources["model"],
        force_evaluator=resources["force_evaluator"],
        features=resources["features"],
        thermodynamic_state=resources["thermodynamic_state"],
        interpretation=resources["interpretation"],
        cutoff=resources["cutoff"],
        **schedule,
    )


def _trace(result, resources):
    return evaluate_flibe_rank_two_tr_eip_md_stresses(
        result, resources["model"], resources["stress_evaluator"],
    )


def _single_stress(state, resources, execution=None):
    configuration = FLiBeConfiguration(state.md_state.configuration)
    graph = build_cutoff_graph(configuration.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=resources["thermodynamic_state"],
        resonance_state=state.resonance_state,
        provenance=PROVENANCE,
    )
    return evaluate_flibe_rank_two_tr_eip_stress(
        resources["model"], resources["stress_evaluator"],
        configuration, graph, resources["features"], descriptor,
        state.ternary_execution if execution is None else execution,
    )


def _deform(configuration, i, j, strain):
    matrix = [[float(a == b) for b in range(3)] for a in range(3)]
    if i == j:
        matrix[i][i] += strain
    else:
        matrix[i][j] += strain / 2.0
        matrix[j][i] += strain / 2.0

    def transform(vector):
        return tuple(fsum(matrix[a][b] * vector[b] for b in range(3))
                     for a in range(3))

    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(transform(p) for p in configuration.positions),
        cell=tuple(transform(v) for v in configuration.cell),
        periodic=configuration.periodic,
    )


def _mat_transform(tensor, matrix):
    return tuple(tuple(
        fsum(matrix[i][a] * tensor[a][b] * matrix[j][b]
             for a in range(3) for b in range(3))
        for j in range(3)) for i in range(3))


@pytest.fixture(scope="module")
def completed():
    state, resources = _fixture()
    result = _run(
        state, resources,
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True, mechanical_time_step=MECHANICAL_DT,
    )
    return state, resources, result, _trace(result, resources)


def test_three_domain_stresses_match_independent_full_energy_evaluations(completed):
    state, resources, coupled, trace = completed
    assert isinstance(trace, FLiBeRankTwoTREIPMDStressTrace)
    assert trace.coupled == coupled
    for label in ("before_events", "after_events", "after_mechanics"):
        boundary = getattr(trace, label)
        assert isinstance(boundary, FLiBeRankTwoTREIPStressResult)
        assert boundary.evaluation == getattr(coupled, label)
        directly = resources["stress_evaluator"].evaluate(
            resources["model"].rank_two_model,
            boundary.evaluation.configuration.configuration,
            boundary.evaluation.graph,
            boundary.evaluation.resonance_features,
            boundary.evaluation.execution,
        )
        assert boundary.stress == directly
        assert directly.reference_evaluation == boundary.evaluation.augmented_result
        assert directly.reference_evaluation.reference_energy == boundary.evaluation.reference_energy
        assert directly.reference_evaluation.tensor_energy == boundary.evaluation.tensor_energy
        assert directly.reference_evaluation.energy == boundary.evaluation.energy
        assert boundary.evaluation.resonance.thermodynamic_state == THERMO
    assert trace.before_events.evaluation.execution == state.ternary_execution
    assert trace.after_events.evaluation.execution == coupled.current.ternary_execution
    assert trace.after_mechanics.evaluation.execution == coupled.current.ternary_execution


def test_six_strain_samples_and_three_stress_channels_match_direct_energy(completed):
    _, resources, _, trace = completed
    for label in ("before_events", "after_events", "after_mechanics"):
        recorded = getattr(trace, label)
        stress, evaluation = recorded.stress, recorded.evaluation
        assert tuple(sample.components for sample in stress.samples) == STRAIN_PAIRS
        assert stress.reference_volume == pytest.approx(512.0, rel=1e-12)
        h = stress.differentiation.step
        scale = 1.0 / (2.0 * h * stress.reference_volume)
        for sample in stress.samples:
            i, j = sample.components
            plus = resources["model"].rank_two_model.evaluate(
                _deform(evaluation.configuration.configuration, i, j, h),
                evaluation.graph, evaluation.resonance_features, evaluation.execution,
            )
            minus = resources["model"].rank_two_model.evaluate(
                _deform(evaluation.configuration.configuration, i, j, -h),
                evaluation.graph, evaluation.resonance_features, evaluation.execution,
            )
            for observed, expected in (
                (sample.reference_plus, plus.reference_energy.total_energy),
                (sample.reference_minus, minus.reference_energy.total_energy),
                (sample.tensor_plus, plus.tensor_energy.total_energy),
                (sample.tensor_minus, minus.tensor_energy.total_energy),
            ):
                assert observed == pytest.approx(expected, abs=1e-11)
            for field, channel in (
                ("reference_stress", "reference_energy"),
                ("tensor_stress", "tensor_energy"),
                ("total_stress", "energy"),
            ):
                derivative = (getattr(plus, channel).total_energy
                              - getattr(minus, channel).total_energy) * scale
                assert getattr(stress, field).tensor[i][j] == pytest.approx(
                    derivative, rel=1e-9, abs=1e-9,
                )


def test_independent_wider_strain_step_matches_total_stress(completed):
    _, resources, _, trace = completed
    for recorded in (trace.before_events, trace.after_mechanics):
        evaluation = recorded.evaluation
        h = 2.5e-5
        scale = 1.0 / (2.0 * h * recorded.stress.reference_volume)
        for i, j in ((0, 0), (1, 2), (2, 2)):
            plus = resources["model"].rank_two_model.evaluate(
                _deform(evaluation.configuration.configuration, i, j, h),
                evaluation.graph, evaluation.resonance_features, evaluation.execution,
            )
            minus = resources["model"].rank_two_model.evaluate(
                _deform(evaluation.configuration.configuration, i, j, -h),
                evaluation.graph, evaluation.resonance_features, evaluation.execution,
            )
            derivative = (plus.energy.total_energy - minus.energy.total_energy) * scale
            assert recorded.stress.total_stress.tensor[i][j] == pytest.approx(
                derivative, rel=5e-4, abs=3e-6,
            )


def test_potential_pressure_is_distinct_from_thermodynamic_pressure(completed):
    _, _, coupled, trace = completed
    assert trace.potential_pressures == tuple(
        getattr(trace, label).potential_pressure
        for label in ("before_events", "after_events", "after_mechanics")
    )
    for observed in (trace.before_events, trace.after_events, trace.after_mechanics):
        assert observed.potential_pressure == -observed.stress.total_stress.trace / 3.0
        assert isfinite(observed.potential_pressure)
        assert observed.evaluation.resonance.thermodynamic_state.pressure == THERMO.pressure
    assert trace.event_pressure_change == pytest.approx(
        trace.potential_pressures[1] - trace.potential_pressures[0]
    )
    assert trace.mechanical_pressure_change == pytest.approx(
        trace.potential_pressures[2] - trace.potential_pressures[1]
    )
    assert coupled.thermodynamic_state == THERMO


def test_phase_only_changes_continuous_clock_and_preserves_tensor_stress():
    state, resources = _fixture()
    coupled = _run(state, resources, phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT)
    trace = _trace(coupled, resources)
    assert coupled.current.md_state == state.md_state
    assert coupled.current.ternary_execution == state.ternary_execution
    assert coupled.current.resonance_step_count == state.resonance_step_count + 1
    assert coupled.current.ternary_event_count == state.ternary_event_count
    assert trace.after_events == trace.after_mechanics
    assert trace.before_events.stress.tensor_stress == trace.after_events.stress.tensor_stress
    assert trace.before_events.stress.reference_stress != trace.after_events.stress.reference_stress
    assert trace.mechanical_pressure_change == 0.0


def test_ternary_only_routes_via_active_neutral_at_fixed_geometry():
    state, resources = _fixture()
    coupled = _run(state, resources, ternary_event=True)
    trace = _trace(coupled, resources)
    assert coupled.current.md_state == state.md_state
    assert coupled.current.resonance_state == state.resonance_state
    assert coupled.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(n.pending_target is TernaryState.POSITIVE
               for n in coupled.current.ternary_execution.states)
    assert trace.after_events == trace.after_mechanics
    assert trace.before_events.stress != trace.after_events.stress
    assert trace.mechanical_pressure_change == 0.0


def test_mechanics_only_keeps_resonance_and_ternary_clocks():
    state, resources = _fixture()
    coupled = _run(state, resources, mechanical_time_step=MECHANICAL_DT)
    trace = _trace(coupled, resources)
    assert coupled.coupled_step.event_update is None
    assert coupled.coupled_step.mechanical_update is not None
    assert trace.before_events == trace.after_events
    assert trace.event_pressure_change == 0.0
    assert coupled.current.resonance_time == state.resonance_time
    assert coupled.current.ternary_event_count == state.ternary_event_count
    assert coupled.current.md_state.step == state.md_state.step + 1
    assert trace.after_mechanics.evaluation.configuration.configuration == coupled.current.md_state.configuration


def test_pending_target_is_not_substituted_for_retained_neutral():
    state, resources = _fixture()
    entry = _run(state, resources, ternary_event=True)
    assert entry.current.ternary_execution.has_pending_targets
    input_state = entry.current
    retained_without_pending = TernaryExecutionVector(states=tuple(
        TernaryExecutionState(TernaryState.NEUTRAL) for _ in range(7)
    ))
    with_pending = _single_stress(input_state, resources)
    without_pending = _single_stress(input_state, resources, retained_without_pending)
    assert with_pending.stress == without_pending.stress
    assert with_pending.evaluation.energy == without_pending.evaluation.energy
    assert with_pending.evaluation.execution.has_pending_targets
    assert not without_pending.evaluation.execution.has_pending_targets
    reversed_resources = {**resources, "interpretation": _interpretation(reverse=True)}
    held = _run(input_state, reversed_resources, ternary_event=True,
                guards=(TernaryExecutionGuard.hold(),) * 7)
    held_trace = _trace(held, reversed_resources)
    assert held.coupled_step.requested_target is TernaryState.NEGATIVE
    assert held.coupled_step.requested_targets == (TernaryState.POSITIVE,) * 7
    assert held.current.ternary_execution == input_state.ternary_execution
    assert held_trace.before_events.stress == held_trace.after_events.stress
    assert held_trace.event_pressure_change == 0.0


@pytest.mark.parametrize("start,reverse,target", (
    (TernaryState.NEGATIVE, False, TernaryState.POSITIVE),
    (TernaryState.POSITIVE, True, TernaryState.NEGATIVE),
))
def test_opposite_polarities_commit_two_distinct_neutral_legs(start, reverse, target):
    state, resources = _fixture(initial=start)
    inputs = {**resources, "interpretation": _interpretation(reverse=reverse)}
    entry = _run(state, inputs, ternary_event=True)
    assert entry.current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(n.pending_target is target for n in entry.current.ternary_execution.states)
    exit_step = _run(entry.current, inputs, ternary_event=True)
    assert exit_step.current.ternary_execution.retained_states == (target,) * 7
    assert not exit_step.current.ternary_execution.has_pending_targets
    for result in (entry, exit_step):
        for item in result.coupled_step.event_update.ternary_update.execution.node_steps:
            assert item.route is not None
            assert not is_direct_opposite_transition(
                item.route.transition.source, item.route.transition.target,
            )
    middle = _trace(entry, inputs)
    final = _trace(exit_step, inputs)
    assert middle.after_events.stress != final.after_events.stress


@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (2.0, -3.0, 1.0)),
    (REFLECTION, (-1.0, 0.5, 2.0)),
))
def test_e3_covariant_stresses_and_invariant_pressure(matrix, translation, completed):
    _, _, _, reference = completed
    transformation = E3Transformation(matrix, translation)
    state, resources = _fixture(transform=transformation)
    transformed_coupled = _run(
        state, resources,
        phase_parameters=PHASE_PARAMETERS, phase_time_step=PHASE_DT,
        ternary_event=True, mechanical_time_step=MECHANICAL_DT,
    )
    observed = _trace(transformed_coupled, resources)
    for label in ("before_events", "after_events", "after_mechanics"):
        original = getattr(reference, label)
        changed = getattr(observed, label)
        for channel in ("reference_stress", "tensor_stress", "total_stress"):
            expected = _mat_transform(getattr(original.stress, channel).tensor, matrix)
            measured = getattr(changed.stress, channel).tensor
            for row, expected_row in zip(measured, expected, strict=True):
                assert row == pytest.approx(expected_row, rel=3e-4, abs=3e-6)
        assert changed.potential_pressure == pytest.approx(
            original.potential_pressure, rel=3e-4, abs=3e-6,
        )
        assert changed.evaluation.execution == original.evaluation.execution
        assert changed.evaluation.resonance.coordinate == pytest.approx(
            original.evaluation.resonance.coordinate, abs=1e-12,
        )


def test_zero_tensor_readout_matches_reference_stress():
    state, resources = _fixture(zero_tensor=True)
    observed = _single_stress(state, resources)
    baseline = ConservativeStressEvaluator(
        resources["stress_evaluator"].differentiation,
    ).evaluate(
        resources["model"].tr_eip_model.energy_model,
        observed.evaluation.configuration.configuration,
        observed.evaluation.graph,
        observed.evaluation.resonance_features.base,
        observed.evaluation.execution,
    )
    assert observed.stress.reference_stress == baseline
    assert observed.stress.total_stress == baseline
    for row in observed.stress.tensor_stress.tensor:
        assert row == pytest.approx((0.0, 0.0, 0.0), abs=1e-12)
    assert observed.stress.reference_evaluation.tensor_energy.total_energy == 0.0


def test_thermodynamic_context_is_retained_without_pressure_relabeling():
    state, resources = _fixture()
    alternate = {**resources, "thermodynamic_state": FLiBeThermodynamicState(900.0, 202650.0)}
    first = _single_stress(state, resources)
    second = _single_stress(state, alternate)
    assert first.stress == second.stress
    assert first.potential_pressure == second.potential_pressure
    assert first.evaluation.resonance.coordinate == second.evaluation.resonance.coordinate
    assert first.evaluation.resonance.thermodynamic_state != second.evaluation.resonance.thermodynamic_state


def test_rejects_nonperiodic_cell_and_missing_cell():
    state, resources = _fixture()
    for periodic, cell, message in (
        ((True, False, True), CELL, "three periodic cell axes"),
        ((False, False, False), None, "simulation cell"),
    ):
        altered = replace(state.md_state.configuration, periodic=periodic, cell=cell)
        modified = replace(state, md_state=replace(state.md_state, configuration=altered))
        with pytest.raises(ValueError, match=message):
            _single_stress(modified, resources)


@pytest.mark.parametrize("name", (
    "model", "stress_evaluator", "configuration", "graph", "features", "resonance", "execution",
))
def test_standalone_stress_rejects_untyped_inputs(name):
    state, resources = _fixture()
    configuration = FLiBeConfiguration(state.md_state.configuration)
    graph = build_cutoff_graph(configuration.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=THERMO,
        resonance_state=state.resonance_state,
        provenance=PROVENANCE,
    )
    inputs = dict(
        model=resources["model"], stress_evaluator=resources["stress_evaluator"],
        configuration=configuration, graph=graph,
        features=resources["features"], resonance=descriptor,
        execution=state.ternary_execution,
    )
    inputs[name] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_tr_eip_stress(**inputs)


def test_md_stress_trace_rejects_corrupted_boundary_records(completed):
    _, resources, coupled, trace = completed
    with pytest.raises(ValueError, match="after_events stress differs"):
        replace(trace, after_events=trace.before_events)
    with pytest.raises(ValueError, match="after_mechanics stress differs"):
        replace(trace, after_mechanics=trace.before_events)
    with pytest.raises(ValueError, match="stress and FLiBe TR-EIP full-energy evaluations differ"):
        replace(trace.before_events, stress=trace.after_events.stress)
    with pytest.raises(TypeError, match="coupled"):
        replace(trace, coupled=None)
    with pytest.raises(TypeError, match="stress"):
        replace(trace.before_events, stress=None)
    with pytest.raises(FrozenInstanceError):
        trace.after_events = trace.before_events
    with pytest.raises(FrozenInstanceError):
        trace.before_events.stress = trace.after_events.stress
    assert _trace(coupled, resources) == trace


def test_model_identity_and_stress_evaluator_type_are_enforced(completed):
    _, resources, coupled, _ = completed
    altered_readout = RankTwoInvariantEnergyReadout((
        RankTwoChannelEnergyWeights(), RankTwoChannelEnergyWeights(),
    ))
    separate = FLiBeRankTwoTREIPModel(
        resources["model"].tr_eip_model,
        replace(resources["model"].rank_two_model, tensor_readout=altered_readout),
    )
    with pytest.raises(ValueError, match="recorded FLiBe TR-EIP evaluation differs"):
        evaluate_flibe_rank_two_tr_eip_md_stresses(
            coupled, separate, resources["stress_evaluator"],
        )
    with pytest.raises(TypeError, match="stress_evaluator"):
        evaluate_flibe_rank_two_tr_eip_md_stresses(
            coupled, resources["model"], None,
        )
    with pytest.raises(TypeError, match="coupled"):
        evaluate_flibe_rank_two_tr_eip_md_stresses(
            None, resources["model"], resources["stress_evaluator"],
        )
