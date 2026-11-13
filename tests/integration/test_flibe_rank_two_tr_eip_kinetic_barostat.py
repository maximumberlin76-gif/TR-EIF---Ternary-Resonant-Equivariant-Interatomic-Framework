
"""Integrated FLiBe rank-two kinetic-pressure and barostat qualification.

Reconstruct the post-mechanical kinetic momentum flux with an independent
Cartesian reference calculation. Exercise both velocity frames, signed
configurational pressure, explicit SI units, affine volume coupling and
retention of independent resonance, ternary and mechanical clocks.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.flibe.rank_two_tr_eip_kinetic_barostat import (
    FLiBeRankTwoTREIPKineticBarostatStep,
    apply_flibe_rank_two_tr_eip_kinetic_barostat,
    evaluate_flibe_rank_two_tr_eip_pressure,
)
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.flibe.units import (
    FLiBeUnit,
    ParameterProvenance,
    pressure_parameter,
    temperature_parameter,
)
from tr_eif.ternary import TernaryState

from test_flibe_rank_two_tr_eip_barostat import (
    CUTOFF,
    COMPRESSIBILITY,
    COUPLING_TIME,
    PROVENANCE,
    prepared,
)


MASS_TO_KG = 1.66053906660e-27
LENGTH_TO_M = 1.0e-10
TIME_TO_S = 1.0e-15
STRESS_TO_PA = 1.602176634e11
SOURCE = "FLIBE-RANK-TWO-KINETIC-QUALIFICATION"
FRAMES = (
    FLiBeVelocityFrame.CENTER_OF_MASS,
    FLiBeVelocityFrame.LABORATORY,
)


def _pressure_args(frame, **overrides):
    args = dict(
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=frame,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    args.update(overrides)
    return args


def _reference_pressure(trace, frame):
    """Evaluate Cartesian momentum flux without production pressure helpers."""
    md = trace.coupled.current.md_state
    a, b, c = md.configuration.cell
    determinant = (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )
    volume_m3 = abs(determinant) * LENGTH_TO_M**3
    total_mass = sum(md.masses)
    drift = [0.0, 0.0, 0.0]
    if frame is FLiBeVelocityFrame.CENTER_OF_MASS:
        for atom in range(len(md.masses)):
            for axis in range(3):
                drift[axis] += md.masses[atom] * md.velocities[atom][axis]
        drift = [component / total_mass for component in drift]

    prefactor = MASS_TO_KG * (LENGTH_TO_M / TIME_TO_S)**2 / volume_m3
    sigma = trace.after_mechanics.stress.total_stress.tensor
    kinetic = [[0.0] * 3 for _ in range(3)]
    configurational = [[0.0] * 3 for _ in range(3)]
    full = [[0.0] * 3 for _ in range(3)]
    for row in range(3):
        for col in range(3):
            flux = 0.0
            for mass, velocity in zip(md.masses, md.velocities, strict=True):
                flux += mass * (velocity[row] - drift[row]) * (velocity[col] - drift[col])
            kinetic[row][col] = flux * prefactor
            configurational[row][col] = -sigma[row][col] * STRESS_TO_PA
            full[row][col] = kinetic[row][col] + configurational[row][col]
    return volume_m3, kinetic, configurational, full


def _assert_tensor(actual, expected):
    for row in range(3):
        for col in range(3):
            assert isfinite(actual[row][col])
            assert actual[row][col] == pytest.approx(
                expected[row][col], rel=2e-12, abs=2e-6,
            )


def _trace(tensor):
    return sum(tensor[axis][axis] for axis in range(3)) / 3.0


@pytest.mark.parametrize("frame", FRAMES)
def test_independent_si_momentum_flux_and_full_pressure(prepared, frame):
    _, _, _, trace = prepared
    result = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(frame),
    )
    volume, kinetic, configurational, full = _reference_pressure(trace, frame)
    assert result.velocity_frame is frame
    assert result.stress_trace == trace
    assert result.cell_volume_m3 == pytest.approx(volume, rel=1e-13)
    assert result.kinetic_pressure.unit is FLiBeUnit.PASCAL
    assert result.total_pressure.unit is FLiBeUnit.PASCAL
    assert result.total_pressure.provenance is PROVENANCE
    assert result.total_pressure.source == SOURCE
    _assert_tensor(result.kinetic_tensor_pa, kinetic)
    _assert_tensor(result.configurational_tensor_pa, configurational)
    _assert_tensor(result.pressure_tensor_pa, full)
    assert result.kinetic_pressure.value == pytest.approx(_trace(kinetic), rel=2e-12)
    assert result.potential_pressure_pa == pytest.approx(
        _trace(configurational), rel=2e-12, abs=2e-6,
    )
    assert result.total_pressure.value == pytest.approx(
        _trace(full), rel=2e-12, abs=2e-6,
    )
    assert result.total_pressure.value == pytest.approx(
        fsum((result.kinetic_pressure.value, result.potential_pressure_pa)),
        rel=2e-12, abs=2e-6,
    )


def test_center_of_mass_frame_removes_translational_flux(prepared):
    _, _, _, trace = prepared
    com = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    laboratory = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(FLiBeVelocityFrame.LABORATORY),
    )
    md = trace.coupled.current.md_state
    mass_sum = sum(md.masses)
    mean_velocity = [
        sum(md.masses[i] * md.velocities[i][axis] for i in range(len(md.masses)))
        / mass_sum for axis in range(3)
    ]
    coefficient = MASS_TO_KG * (LENGTH_TO_M / TIME_TO_S)**2 / com.cell_volume_m3
    for a in range(3):
        for b in range(3):
            expected_difference = coefficient * mass_sum * mean_velocity[a] * mean_velocity[b]
            assert laboratory.kinetic_tensor_pa[a][b] - com.kinetic_tensor_pa[a][b] == (
                pytest.approx(expected_difference, rel=2e-11, abs=2e-6)
            )
    assert laboratory.kinetic_pressure.value >= com.kinetic_pressure.value
    assert laboratory.configurational_tensor_pa == com.configurational_tensor_pa
    assert laboratory.pressure_tensor_pa != com.pressure_tensor_pa
    assert laboratory.total_pressure.value >= com.total_pressure.value


@pytest.mark.parametrize("frame", FRAMES)
@pytest.mark.parametrize("target_offset", (-25000.0, 0.0, 25000.0))
def test_derived_pressure_drives_affine_barostat_and_preserves_clocks(
    prepared, frame, target_offset,
):
    initial, model, evaluator, trace = prepared
    pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(frame),
    )
    barostat_pressure = fsum((
        trace.after_mechanics.potential_pressure * STRESS_TO_PA,
        pressure.kinetic_pressure.value,
    ))
    target = pressure_parameter(barostat_pressure + target_offset, PROVENANCE)
    step = apply_flibe_rank_two_tr_eip_kinetic_barostat(
        trace, model, evaluator,
        cutoff=CUTOFF,
        target_pressure=target,
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
        **_pressure_args(frame),
    )
    assert isinstance(step, FLiBeRankTwoTREIPKineticBarostatStep)
    assert step.pressure == pressure
    assert step.barostat.target_pressure == target
    assert step.barostat.kinetic_pressure == pressure.kinetic_pressure
    assert step.barostat.current_pressure_pa == pytest.approx(
        pressure.total_pressure.value, rel=2e-12, abs=2e-6,
    )
    mechanical = trace.coupled.current
    dt = mechanical.md_state.time - trace.coupled.coupled_step.previous.md_state.time
    independent_volume_ratio = (
        1.0 - dt * COMPRESSIBILITY * target_offset / COUPLING_TIME
    )
    assert step.barostat.volume_ratio == pytest.approx(independent_volume_ratio, rel=1e-12)
    assert step.barostat.linear_scale**3 == pytest.approx(independent_volume_ratio, rel=1e-12)
    if target_offset > 0:
        assert step.barostat.linear_scale < 1.0
    elif target_offset < 0:
        assert step.barostat.linear_scale > 1.0
    else:
        assert step.barostat.linear_scale == pytest.approx(1.0, abs=1e-12)
        for actual, original in zip(
            step.barostat.current.md_state.configuration.positions,
            mechanical.md_state.configuration.positions,
            strict=True,
        ):
            assert actual == pytest.approx(original, abs=1e-11)

    current = step.barostat.current
    assert current.md_state.velocities == mechanical.md_state.velocities
    assert current.md_state.masses == mechanical.md_state.masses
    assert current.md_state.time == mechanical.md_state.time
    assert current.md_state.step == mechanical.md_state.step
    assert current.resonance_state == mechanical.resonance_state
    assert current.resonance_time == mechanical.resonance_time
    assert current.resonance_step_count == mechanical.resonance_step_count
    assert current.ternary_execution == mechanical.ternary_execution
    assert current.ternary_event_count == mechanical.ternary_event_count
    assert initial.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert current.ternary_execution.has_pending_targets
    assert all(item.pending_target is TernaryState.POSITIVE
               for item in current.ternary_execution.states)
    assert step.barostat.after_barostat.evaluation.execution == current.ternary_execution
    assert step.barostat.after_barostat.evaluation.resonance.resonance_state == (
        current.resonance_state
    )
    assert step.barostat.after_barostat.evaluation.resonance.thermodynamic_state == (
        trace.coupled.thermodynamic_state
    )
    assert step.barostat.after_barostat.evaluation.configuration.configuration == (
        current.md_state.configuration
    )


def test_deterministic_kinetic_pressure_and_barostat_replay(prepared):
    _, model, evaluator, trace = prepared
    pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    args = dict(
        cutoff=CUTOFF,
        target_pressure=pressure_parameter(
            fsum((trace.after_mechanics.potential_pressure * STRESS_TO_PA,
                  pressure.kinetic_pressure.value)) + 25000.0,
            PROVENANCE,
        ),
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
        **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    first = apply_flibe_rank_two_tr_eip_kinetic_barostat(trace, model, evaluator, **args)
    second = apply_flibe_rank_two_tr_eip_kinetic_barostat(trace, model, evaluator, **args)
    assert first == second
    assert first.barostat.current.ternary_execution == trace.coupled.current.ternary_execution


@pytest.mark.parametrize("field,value,exception", (
    ("mass_unit_to_kg", 0.0, ValueError),
    ("mass_unit_to_kg", True, TypeError),
    ("coordinate_unit_to_meter", float("nan"), ValueError),
    ("coordinate_unit_to_meter", 0.0, ValueError),
    ("time_unit_to_second", float("inf"), ValueError),
    ("time_unit_to_second", 0.0, ValueError),
    ("potential_stress_unit_to_pascal", -1.0, ValueError),
    ("potential_stress_unit_to_pascal", False, TypeError),
    ("velocity_frame", "LABORATORY", TypeError),
    ("provenance", "TEST_FIXTURE", TypeError),
    ("source", "", ValueError),
))
def test_invalid_pressure_inputs_are_rejected(prepared, field, value, exception):
    _, _, _, trace = prepared
    with pytest.raises(exception):
        evaluate_flibe_rank_two_tr_eip_pressure(
            trace, **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS, **{field: value}),
        )


def test_primary_source_provenance_requires_source(prepared):
    _, _, _, trace = prepared
    with pytest.raises(ValueError, match="PRIMARY_SOURCE"):
        evaluate_flibe_rank_two_tr_eip_pressure(
            trace,
            **_pressure_args(
                FLiBeVelocityFrame.CENTER_OF_MASS,
                provenance=ParameterProvenance.PRIMARY_SOURCE,
                source=None,
            ),
        )


@pytest.mark.parametrize("name,value", (
    ("kinetic_pressure", pressure_parameter(1.0, PROVENANCE)),
    ("total_pressure", temperature_parameter(850.0, PROVENANCE)),
    ("cell_volume_m3", -1.0),
    ("pressure_tensor_pa", ((0.0, 0.0, 0.0),) * 3),
))
def test_pressure_closure_rejects_inconsistent_components(prepared, name, value):
    _, _, _, trace = prepared
    closure = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    with pytest.raises((ValueError, TypeError)):
        replace(closure, **{name: value})


@pytest.mark.parametrize("overrides,exception", (
    ({"target_pressure": 101325.0}, TypeError),
    ({"target_pressure": temperature_parameter(850.0, PROVENANCE)}, ValueError),
    ({"cutoff": 0.0}, ValueError),
    ({"compressibility_per_pascal": 0.0}, ValueError),
    ({"coupling_time": 0.0}, ValueError),
))
def test_invalid_barostat_boundary_is_rejected(prepared, overrides, exception):
    _, model, evaluator, trace = prepared
    pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        trace, **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    args = dict(
        cutoff=CUTOFF,
        target_pressure=pressure_parameter(pressure.total_pressure.value, PROVENANCE),
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
        **_pressure_args(FLiBeVelocityFrame.CENTER_OF_MASS),
    )
    args.update(overrides)
    with pytest.raises(exception):
        apply_flibe_rank_two_tr_eip_kinetic_barostat(trace, model, evaluator, **args)
