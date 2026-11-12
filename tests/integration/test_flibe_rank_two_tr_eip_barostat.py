"""Integration qualification of FLiBe rank-two TR-EIP/MD pressure coupling.

Independently reconstruct the pressure balance, affine geometry, periodic
volume, full conservative energy and stress after a scheduled mechanical step.
Check retained active-neutral routing, pending destinations, separate clocks,
deterministic replay, physical units and rejected inconsistent boundaries.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
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
from tr_eif.flibe.rank_two_tr_eip_barostat import (
    FLiBeRankTwoTREIPBarostatStep,
    apply_flibe_rank_two_tr_eip_barostat,
)
from tr_eif.flibe.rank_two_tr_eip_stress import (
    evaluate_flibe_rank_two_tr_eip_md_stresses,
)
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.ternary_interpretation import FLiBeTernaryInterpretation
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import (
    ParameterProvenance,
    pressure_parameter,
    temperature_parameter,
)
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
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
PROVENANCE = ParameterProvenance.TEST_FIXTURE
THERMODYNAMIC_STATE = FLiBeThermodynamicState(850.0, 101325.0)
CUTOFF = 1.6
MECHANICAL_DT = 1.0e-4
PRESSURE_CONVERSION = 1.0e6
COMPRESSIBILITY = 2.0e-7
COUPLING_TIME = 4.0e-4


def _setup():
    initial = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(
                species=SPECIES, positions=POSITIONS,
                cell=CELL, periodic=(True, True, True),
            ),
            velocities=VELOCITIES, masses=MASSES, step=4, time=0.3,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.04, 0.09, 0.15, 0.22, 0.31, 0.43),
            frequencies=(-0.25, -0.15, -0.05, 0.0, 0.10, 0.20, 0.30),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (TernaryState.NEGATIVE,) * len(SPECIES)
        ),
        resonance_time=0.4, resonance_step_count=2, ternary_event_count=5,
    )
    base_features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(0.5 + 0.25 * i,),
            vectors=((1.0, 0.1 * i, -0.05 * i),),
        )
        for i in range(len(SPECIES))
    ))
    rank_two_features = RankTwoFeatureVector(nodes=tuple((
        RankTwoTensor((
            (1.0 + 0.1 * i, 0.2, -0.3),
            (0.4, 0.8 - 0.05 * i, 0.1),
            (-0.2, 0.3, 0.6),
        )),
        RankTwoTensor.outer(
            (1.0, 0.25 * i - 0.5, 0.3), (0.2, 0.8, -0.1 * i),
        ),
    ) for i in range(len(SPECIES))))
    features = ScalarVectorTensorFeatures(base_features, rank_two_features)
    reference_model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.1),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.4, 0.7, -0.3), bias=0.1,
        ),
    )
    model = FLiBeRankTwoTREIPModel(
        tr_eip_model=FLiBeTREIPModel(reference_model, PROVENANCE),
        rank_two_model=RankTwoConservativeEnergyModel(
            reference_model=reference_model,
            tensor_readout=RankTwoInvariantEnergyReadout((
                RankTwoChannelEnergyWeights(
                    trace=0.15, isotropic_norm_squared=0.08,
                    symmetric_traceless_norm_squared=0.30,
                    antisymmetric_norm_squared=0.20,
                ),
                RankTwoChannelEnergyWeights(
                    trace=-0.12, isotropic_norm_squared=0.05,
                    symmetric_traceless_norm_squared=-0.08,
                    antisymmetric_norm_squared=0.10,
                ),
            )),
            coupling=RankTwoMessageCoupling(
                tensor_scale=0.7, scalar_dyad_scale=0.2,
                vector_dyad_scale=-0.15,
                scalar_channel_index=0, vector_channel_index=0,
            ),
        ),
    )
    force_evaluator = RankTwoConservativeForceEvaluator(
        CoordinateDifferentiation(step=1.0e-5)
    )
    stress_evaluator = RankTwoConservativeStressEvaluator(
        CellStrainDifferentiation(step=1.0e-6)
    )
    interpretation = FLiBeTernaryInterpretation(
        projection=ResonanceProjection(1.0, -0.1),
        thresholds=TernaryTargetThresholds(negative=-0.25, positive=0.5),
        provenance=PROVENANCE,
    )
    return initial, model, force_evaluator, stress_evaluator, features, interpretation


@pytest.fixture(scope="module")
def prepared():
    initial, model, forces, stress_evaluator, features, interpretation = _setup()
    coupled = execute_flibe_rank_two_tr_eip_coupled_md_step(
        initial,
        model=model,
        force_evaluator=forces,
        features=features,
        thermodynamic_state=THERMODYNAMIC_STATE,
        interpretation=interpretation,
        cutoff=CUTOFF,
        phase_parameters=PhaseDynamicsParameters(
            coupling=(0.35,) * len(SPECIES),
            phase_lag=(0.13,) * len(SPECIES),
        ),
        phase_time_step=0.1,
        ternary_event=True,
        mechanical_time_step=MECHANICAL_DT,
    )
    trace = evaluate_flibe_rank_two_tr_eip_md_stresses(
        coupled, model, stress_evaluator
    )
    return initial, model, stress_evaluator, trace


def _inputs(trace, *, difference=0.0, kinetic=None, **overrides):
    potential_pa = trace.after_mechanics.potential_pressure * PRESSURE_CONVERSION
    if kinetic is None:
        kinetic = max(120000.0, 120000.0 - potential_pa)
    current_pa = fsum((potential_pa, kinetic))
    args = dict(
        cutoff=CUTOFF,
        target_pressure=pressure_parameter(current_pa + difference, PROVENANCE),
        kinetic_pressure=pressure_parameter(kinetic, PROVENANCE),
        potential_stress_unit_to_pascal=PRESSURE_CONVERSION,
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
    )
    args.update(overrides)
    return args


def _apply(prepared, *, difference=0.0, **overrides):
    _, model, evaluator, trace = prepared
    return apply_flibe_rank_two_tr_eip_barostat(
        trace, model, evaluator,
        **_inputs(trace, difference=difference, **overrides),
    )


def _volume(cell):
    a, b, c = cell
    return abs(fsum((
        a[0] * (b[1] * c[2] - b[2] * c[1]),
        a[1] * (b[2] * c[0] - b[0] * c[2]),
        a[2] * (b[0] * c[1] - b[1] * c[0]),
    )))


def _scaled_configuration(configuration, factor):
    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(tuple(factor * coordinate for coordinate in position)
                        for position in configuration.positions),
        cell=tuple(tuple(factor * coordinate for coordinate in vector)
                   for vector in configuration.cell),
        periodic=configuration.periodic,
    )


@pytest.mark.parametrize("difference,relation", (
    (25000.0, "compress"),
    (-25000.0, "expand"),
    (0.0, "stationary"),
))
def test_pressure_balance_geometry_and_volume(prepared, difference, relation):
    _, _, _, trace = prepared
    step = _apply(prepared, difference=difference)
    mechanical = trace.coupled.current.md_state
    potential = trace.after_mechanics.potential_pressure * PRESSURE_CONVERSION
    kinetic = step.kinetic_pressure.value
    pressure = fsum((potential, kinetic))
    dt = mechanical.time - trace.coupled.coupled_step.previous.md_state.time
    independent_volume_factor = (
        1.0 - dt / COUPLING_TIME * COMPRESSIBILITY
        * (step.target_pressure.value - pressure)
    )
    assert isinstance(step, FLiBeRankTwoTREIPBarostatStep)
    assert step.stress_trace == trace
    assert step.mechanical_time_step == pytest.approx(dt, rel=1e-12)
    assert step.potential_pressure_pa == pytest.approx(potential, rel=1e-12)
    assert step.current_pressure_pa == pytest.approx(pressure, rel=1e-12)
    assert step.linear_scale ** 3 == pytest.approx(independent_volume_factor, rel=1e-12)
    assert step.volume_ratio == pytest.approx(independent_volume_factor, rel=1e-12)
    assert step.current.md_state.configuration == _scaled_configuration(
        mechanical.configuration, step.linear_scale
    )
    assert _volume(step.current.md_state.configuration.cell) == pytest.approx(
        _volume(mechanical.configuration.cell) * independent_volume_factor, rel=1e-12
    )
    assert all(isfinite(value) for value in (
        step.potential_pressure_pa,
        step.current_pressure_pa,
        step.after_barostat_potential_pressure_pa,
    ))
    if relation == "compress":
        assert step.linear_scale < 1.0
    elif relation == "expand":
        assert step.linear_scale > 1.0
    else:
        assert step.linear_scale == 1.0
        assert step.current.md_state == mechanical
        assert step.after_barostat == trace.after_mechanics


@pytest.mark.parametrize("difference", (-25000.0, 25000.0))
def test_post_barostat_full_energy_stress_and_graph_are_reconstructed(prepared, difference):
    _, model, evaluator, trace = prepared
    step = _apply(prepared, difference=difference)
    configuration = FLiBeConfiguration(step.current.md_state.configuration)
    graph = build_cutoff_graph(configuration.configuration, CUTOFF)
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=THERMODYNAMIC_STATE,
        resonance_state=step.current.resonance_state,
        provenance=model.tr_eip_model.provenance,
        source=model.tr_eip_model.source,
    )
    features = trace.coupled.after_mechanics.input_features
    expected = model.evaluate(
        configuration, graph, features, descriptor, step.current.ternary_execution
    )
    expected_stress = evaluator.evaluate(
        model.rank_two_model, configuration.configuration,
        graph, expected.resonance_features, step.current.ternary_execution,
    )
    assert step.after_barostat.evaluation == expected
    assert step.after_barostat.stress == expected_stress
    assert step.after_barostat.evaluation.graph == graph
    assert step.after_barostat.evaluation.energy.total_energy == pytest.approx(
        fsum((step.after_barostat.evaluation.reference_energy.total_energy,
              step.after_barostat.evaluation.tensor_energy.total_energy)),
        rel=1e-12,
    )
    stress = step.after_barostat.stress.total_stress.tensor
    independent_potential = -fsum(stress[i][i] for i in range(3)) / 3.0
    assert step.after_barostat_potential_pressure_pa == pytest.approx(
        independent_potential * PRESSURE_CONVERSION, rel=1e-12, abs=1e-8
    )
    assert trace.before_events == step.stress_trace.before_events
    assert trace.after_events == step.stress_trace.after_events
    assert trace.after_mechanics == step.stress_trace.after_mechanics


@pytest.mark.parametrize("difference", (-25000.0, 0.0, 25000.0))
def test_active_neutral_pending_and_independent_clocks(prepared, difference):
    initial, _, _, trace = prepared
    after_mechanics = trace.coupled.current
    assert initial.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert after_mechanics.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert after_mechanics.ternary_execution.has_pending_targets
    assert all(n.pending_target is TernaryState.POSITIVE
               for n in after_mechanics.ternary_execution.states)
    step = _apply(prepared, difference=difference)
    current = step.current
    assert current.ternary_execution == after_mechanics.ternary_execution
    assert current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert current.ternary_execution.has_pending_targets
    assert current.resonance_state == after_mechanics.resonance_state
    assert current.resonance_time == after_mechanics.resonance_time
    assert current.resonance_step_count == after_mechanics.resonance_step_count
    assert current.ternary_event_count == after_mechanics.ternary_event_count
    assert current.md_state.step == after_mechanics.md_state.step
    assert current.md_state.time == after_mechanics.md_state.time
    assert current.md_state.velocities == after_mechanics.md_state.velocities
    assert current.md_state.masses == after_mechanics.md_state.masses
    assert step.after_barostat.evaluation.execution == current.ternary_execution
    assert step.after_barostat.evaluation.resonance.thermodynamic_state == THERMODYNAMIC_STATE
    assert step.after_barostat.evaluation.resonance.resonance_state == current.resonance_state
    assert step.after_barostat.evaluation.resonance.thermodynamic_state.pressure == 101325.0


def test_deterministic_replay_and_external_kinetic_pressure(prepared):
    _, _, _, trace = prepared
    first = _apply(prepared, difference=25000.0)
    second = _apply(prepared, difference=25000.0)
    assert first == second
    different_kinetic = pressure_parameter(first.kinetic_pressure.value + 2500.0, PROVENANCE)
    changed = _apply(prepared, difference=25000.0, kinetic_pressure=different_kinetic)
    assert changed.stress_trace == first.stress_trace
    assert changed.potential_pressure_pa == first.potential_pressure_pa
    assert changed.current_pressure_pa == pytest.approx(first.current_pressure_pa + 2500.0)
    assert changed.linear_scale != first.linear_scale
    assert changed.current.md_state.velocities == first.current.md_state.velocities
    assert changed.current.md_state.masses == first.current.md_state.masses
    assert changed.after_barostat.evaluation != first.after_barostat.evaluation
    assert trace.after_mechanics.evaluation == first.stress_trace.after_mechanics.evaluation


@pytest.mark.parametrize("invalid,expected", (
    ({"cutoff": 0.0}, ValueError),
    ({"cutoff": 0.9}, ValueError),
    ({"target_pressure": 101325.0}, TypeError),
    ({"target_pressure": temperature_parameter(850.0, PROVENANCE)}, ValueError),
    ({"kinetic_pressure": pressure_parameter(-1.0, PROVENANCE)}, ValueError),
    ({"kinetic_pressure": temperature_parameter(850.0, PROVENANCE)}, ValueError),
    ({"potential_stress_unit_to_pascal": 0.0}, ValueError),
    ({"potential_stress_unit_to_pascal": float("nan")}, ValueError),
    ({"potential_stress_unit_to_pascal": True}, TypeError),
    ({"compressibility_per_pascal": 0.0}, ValueError),
    ({"compressibility_per_pascal": float("inf")}, ValueError),
    ({"coupling_time": 0.0}, ValueError),
    ({"coupling_time": False}, TypeError),
))
def test_invalid_units_coefficients_and_graph_are_rejected(prepared, invalid, expected):
    with pytest.raises(expected):
        _apply(prepared, difference=25000.0, **invalid)


def test_nonpositive_volume_scale_is_rejected(prepared):
    with pytest.raises(ValueError, match="volume scale"):
        _apply(prepared, difference=100_000_000.0)


@pytest.mark.parametrize("field,replacement", (
    ("current_pressure_pa", 0.0),
    ("linear_scale", 1.1),
    ("mechanical_time_step", 0.001),
))
def test_inconsistent_pressure_scale_and_mechanical_interval_are_rejected(
    prepared, field, replacement,
):
    step = _apply(prepared, difference=25000.0)
    with pytest.raises(ValueError):
        replace(step, **{field: replacement})


def test_inconsistent_clocks_and_post_cell_are_rejected(prepared):
    step = _apply(prepared, difference=25000.0)
    with pytest.raises(ValueError, match="clocks"):
        replace(step, current=replace(
            step.current, ternary_event_count=step.current.ternary_event_count + 1
        ))
    with pytest.raises(ValueError, match="geometry"):
        replace(step, after_barostat=step.stress_trace.after_mechanics)
    with pytest.raises(FrozenInstanceError):
        step.linear_scale = 2.0


def test_mechanics_free_stress_trace_is_rejected(prepared):
    initial, model, _, _ = prepared
    _, _, _, evaluator, features, interpretation = _setup()
    coupled = execute_flibe_rank_two_tr_eip_coupled_md_step(
        initial, model=model, force_evaluator=RankTwoConservativeForceEvaluator(
            CoordinateDifferentiation(step=1.0e-5)
        ), features=features, thermodynamic_state=THERMODYNAMIC_STATE,
        interpretation=interpretation, cutoff=CUTOFF, ternary_event=True,
    )
    trace = evaluate_flibe_rank_two_tr_eip_md_stresses(coupled, model, evaluator)
    with pytest.raises(ValueError, match="mechanical interval"):
        apply_flibe_rank_two_tr_eip_barostat(
            trace, model, evaluator,
            **_inputs(trace, difference=25000.0),
        )
