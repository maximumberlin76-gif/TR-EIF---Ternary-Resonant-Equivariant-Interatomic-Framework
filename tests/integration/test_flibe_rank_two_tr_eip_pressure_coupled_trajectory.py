"""Integration checks for scheduled FLiBe rank-two pressure-coupled MD.

Exercise multiple mechanical, phase and ternary event schedules with one
conservative rank-two model. Reconstruct the pressure/volume relation from
recorded velocities and stresses, and verify state continuity, active-neutral
routing, mass density, SI conversion and deterministic replay.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.flibe.rank_two_tr_eip_kinetic_barostat import (
    evaluate_flibe_rank_two_tr_eip_pressure,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_trajectory import (
    FLiBeRankTwoTREIPPressureCoupledInterval,
    FLiBeRankTwoTREIPPressureCoupledTrajectory,
    run_flibe_rank_two_tr_eip_pressure_coupled_trajectory,
)
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.flibe.units import pressure_parameter, temperature_parameter
from tr_eif.ternary import TernaryExecutionGuard, TernaryState

from test_flibe_rank_two_tr_eip_stress import (
    CUTOFF,
    MECHANICAL_DT,
    PHASE_PARAMETERS,
    PROVENANCE,
    THERMO as THERMODYNAMIC_STATE,
    _fixture,
    _run,
    _trace,
)

MASS_TO_KG = 1.66053906660e-27
LENGTH_TO_M = 1.0e-10
TIME_TO_S = 1.0e-15
STRESS_TO_PA = 1.602176634e11
COMPRESSIBILITY = 2.0e-14
COUPLING_TIME = 4.0e-4
SOURCE = "FLIBE-RANK-TWO-PRESSURE-TRAJECTORY-TEST"
FRAME = FLiBeVelocityFrame.CENTER_OF_MASS


def _cell_volume(cell):
    """Compute signed-determinant volume independently of production helpers."""
    a, b, c = cell
    return abs(
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def _parameters():
    return PHASE_PARAMETERS


def _schedule():
    return (
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            phase_parameters=_parameters(),
            phase_time_step=0.1,
            ternary_event=True,
        ),
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            ternary_event=True,
        ),
        FLiBeRankTwoTREIPPressureCoupledInterval(
            mechanical_time_step=MECHANICAL_DT,
            phase_parameters=_parameters(),
            phase_time_step=0.05,
        ),
    )


@pytest.fixture(scope="module")
def prepared_trajectory():
    initial, resources = _fixture()
    first_coupled = _run(
        initial, resources,
        phase_parameters=PHASE_PARAMETERS,
        phase_time_step=0.1,
        ternary_event=True,
        mechanical_time_step=MECHANICAL_DT,
    )
    first_trace = _trace(first_coupled, resources)
    first_pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        first_trace,
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=FRAME,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    # Tie the fixture target to the computed first mechanical state.
    target = pressure_parameter(
        max(101325.0, first_pressure.total_pressure.value + 100_000_000.0),
        PROVENANCE,
    )
    options = dict(
        schedule=_schedule(),
        **resources,
        target_pressure=target,
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=FRAME,
        compressibility_per_pascal=COMPRESSIBILITY,
        coupling_time=COUPLING_TIME,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    trajectory = run_flibe_rank_two_tr_eip_pressure_coupled_trajectory(
        initial, **options,
    )
    return trajectory, options


def test_complete_multirate_schedule_and_state_continuity(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    assert isinstance(trajectory, FLiBeRankTwoTREIPPressureCoupledTrajectory)
    assert trajectory.interval_count == 3
    assert len(trajectory.states) == 4
    assert trajectory.states[0] == trajectory.initial
    assert trajectory.states[-1] == trajectory.final
    for index, (interval, step) in enumerate(
        zip(trajectory.schedule, trajectory.steps, strict=True)
    ):
        before = trajectory.states[index]
        after = trajectory.states[index + 1]
        coupled = step.barostat.stress_trace.coupled
        assert coupled.coupled_step.previous == before
        assert coupled.coupled_step.current.md_state.step == before.md_state.step + 1
        assert step.barostat.current == after
        assert after.md_state.step == before.md_state.step + 1
        assert after.md_state.time == pytest.approx(
            before.md_state.time + interval.mechanical_time_step, abs=1e-12
        )
        assert after.resonance_step_count == (
            before.resonance_step_count + int(interval.phase_time_step is not None)
        )
        assert after.resonance_time == pytest.approx(
            before.resonance_time + (interval.phase_time_step or 0.0), abs=1e-12
        )
        assert after.ternary_event_count == (
            before.ternary_event_count + int(interval.ternary_event)
        )
        assert after.md_state.masses == trajectory.initial.md_state.masses
        assert after.md_state.configuration.species == (
            trajectory.initial.md_state.configuration.species
        )
        assert step.barostat.after_barostat.evaluation.configuration.configuration == (
            after.md_state.configuration
        )
        assert step.barostat.after_barostat.evaluation.execution == after.ternary_execution
        assert step.barostat.after_barostat.evaluation.resonance.resonance_state == (
            after.resonance_state
        )


def test_active_neutral_pending_route_and_event_isolation(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    initial, first, second, third = trajectory.states
    assert initial.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert first.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert first.ternary_execution.has_pending_targets
    assert all(
        state.pending_target is TernaryState.POSITIVE
        for state in first.ternary_execution.states
    )
    assert second.ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7
    assert not second.ternary_execution.has_pending_targets
    assert third.ternary_execution == second.ternary_execution
    assert second.resonance_state == first.resonance_state
    assert third.resonance_state != second.resonance_state
    for step in trajectory.steps:
        assert step.barostat.current.ternary_execution == (
            step.barostat.stress_trace.coupled.current.ternary_execution
        )


@pytest.mark.parametrize("index", (0, 1, 2))
def test_independent_pressure_balance_and_affine_volume(prepared_trajectory, index):
    trajectory, options = prepared_trajectory
    step = trajectory.steps[index]
    pressure = step.pressure
    barostat = step.barostat
    before = trajectory.states[index]
    after = trajectory.states[index + 1]
    mechanical = barostat.stress_trace.coupled.current.md_state
    kinetic = sum(pressure.kinetic_tensor_pa[a][a] for a in range(3)) / 3.0
    sigma = barostat.stress_trace.after_mechanics.stress.total_stress.tensor
    configurational = -sum(sigma[a][a] for a in range(3)) * STRESS_TO_PA / 3.0
    total = fsum((kinetic, configurational))
    dt = mechanical.time - before.md_state.time
    expected_ratio = 1.0 - (dt / COUPLING_TIME) * COMPRESSIBILITY * (
        options["target_pressure"].value - total
    )
    assert kinetic >= 0.0
    assert pressure.kinetic_pressure.value == pytest.approx(kinetic, rel=1e-12)
    assert pressure.potential_pressure_pa == pytest.approx(
        configurational, rel=1e-12, abs=1e-5
    )
    assert pressure.total_pressure.value == pytest.approx(total, rel=1e-12, abs=1e-5)
    assert barostat.current_pressure_pa == pytest.approx(total, rel=1e-12, abs=1e-5)
    assert barostat.volume_ratio == pytest.approx(expected_ratio, rel=1e-11)
    assert barostat.linear_scale**3 == pytest.approx(expected_ratio, rel=1e-11)
    assert _cell_volume(after.md_state.configuration.cell) == pytest.approx(
        _cell_volume(before.md_state.configuration.cell) * expected_ratio,
        rel=1e-11,
    )
    for p, q in zip(
        mechanical.configuration.positions,
        after.md_state.configuration.positions,
        strict=True,
    ):
        assert q == pytest.approx(
            tuple(barostat.linear_scale * component for component in p),
            rel=1e-12, abs=1e-12,
        )
    assert after.md_state.velocities == mechanical.velocities
    assert after.md_state.masses == mechanical.masses


def test_independent_density_volume_and_mass_conservation(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    mass_kg = sum(trajectory.initial.md_state.masses) * MASS_TO_KG
    assert len(trajectory.cell_volumes_m3) == len(trajectory.states)
    assert len(trajectory.densities_kg_m3) == len(trajectory.states)
    assert trajectory.volume_ratios == tuple(
        step.barostat.volume_ratio for step in trajectory.steps
    )
    assert trajectory.prebarostat_pressures_pa == tuple(
        step.pressure.total_pressure.value for step in trajectory.steps
    )
    for state, volume, density in zip(
        trajectory.states,
        trajectory.cell_volumes_m3,
        trajectory.densities_kg_m3,
        strict=True,
    ):
        expected_volume = _cell_volume(state.md_state.configuration.cell) * LENGTH_TO_M**3
        assert isfinite(volume) and volume > 0.0
        assert volume == pytest.approx(expected_volume, rel=1e-12)
        assert density == pytest.approx(mass_kg / expected_volume, rel=1e-12)


def test_complete_energy_channels_and_thermodynamic_separation(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    for step in trajectory.steps:
        record = step.barostat.after_barostat
        energy = record.evaluation.energy.total_energy
        reference = record.evaluation.reference_energy.total_energy
        tensor = record.evaluation.tensor_energy.total_energy
        assert energy == pytest.approx(fsum((reference, tensor)), rel=1e-12, abs=1e-10)
        assert record.evaluation.resonance.thermodynamic_state == THERMODYNAMIC_STATE
        assert record.evaluation.resonance.thermodynamic_state.pressure == 101325.0
        assert step.pressure.total_pressure.source == SOURCE
        for tensor_row in step.pressure.pressure_tensor_pa:
            assert all(isfinite(value) for value in tensor_row)


def test_deterministic_multistep_replay(prepared_trajectory):
    trajectory, options = prepared_trajectory
    replay = run_flibe_rank_two_tr_eip_pressure_coupled_trajectory(
        trajectory.initial, **options
    )
    assert replay == trajectory
    assert replay.final == trajectory.final
    assert replay.prebarostat_pressures_pa == trajectory.prebarostat_pressures_pa
    assert replay.volume_ratios == trajectory.volume_ratios


@pytest.mark.parametrize("index", (0, 1, 2))
def test_independent_lab_and_com_pressure_relationship(prepared_trajectory, index):
    trajectory, _ = prepared_trajectory
    step = trajectory.steps[index]
    com = step.pressure
    laboratory = evaluate_flibe_rank_two_tr_eip_pressure(
        step.barostat.stress_trace,
        mass_unit_to_kg=MASS_TO_KG,
        coordinate_unit_to_meter=LENGTH_TO_M,
        time_unit_to_second=TIME_TO_S,
        potential_stress_unit_to_pascal=STRESS_TO_PA,
        velocity_frame=FLiBeVelocityFrame.LABORATORY,
        provenance=PROVENANCE,
        source=SOURCE,
    )
    md = step.barostat.stress_trace.coupled.current.md_state
    total_mass = sum(md.masses)
    drift = tuple(
        sum(m * v[a] for m, v in zip(md.masses, md.velocities, strict=True)) / total_mass
        for a in range(3)
    )
    prefactor = total_mass * MASS_TO_KG * (LENGTH_TO_M / TIME_TO_S)**2 / (
        _cell_volume(md.configuration.cell) * LENGTH_TO_M**3
    )
    for a in range(3):
        for b in range(3):
            expected = prefactor * drift[a] * drift[b]
            assert laboratory.kinetic_tensor_pa[a][b] - com.kinetic_tensor_pa[a][b] == (
                pytest.approx(expected, rel=1e-10, abs=1e-5)
            )
    assert laboratory.potential_pressure_pa == pytest.approx(
        com.potential_pressure_pa, rel=1e-12, abs=1e-5,
    )
    assert laboratory.total_pressure.value >= com.total_pressure.value - 1e-5


@pytest.mark.parametrize("invalid,exception", (
    ({"mechanical_time_step": 0.0}, ValueError),
    ({"mechanical_time_step": True}, TypeError),
    ({"mechanical_time_step": float("nan")}, ValueError),
    ({"mechanical_time_step": 0.001, "phase_parameters": _parameters()}, ValueError),
    ({"mechanical_time_step": 0.001, "phase_time_step": 0.1}, TypeError),
    ({"mechanical_time_step": 0.001, "phase_time_step": -0.1,
      "phase_parameters": _parameters()}, ValueError),
    ({"mechanical_time_step": 0.001, "guards": (TernaryExecutionGuard.hold(),)},
     ValueError),
))
def test_invalid_independent_schedules_are_rejected(invalid, exception):
    with pytest.raises(exception):
        FLiBeRankTwoTREIPPressureCoupledInterval(**invalid)


@pytest.mark.parametrize("change,exception", (
    ({"schedule": ()}, ValueError),
    ({"steps": ()}, ValueError),
    ({"schedule": (_schedule()[0],)}, ValueError),
    ({"steps": (None, None, None)}, TypeError),
    ({"velocity_frame": FLiBeVelocityFrame.LABORATORY}, ValueError),
    ({"target_pressure": temperature_parameter(850.0, PROVENANCE)}, ValueError),
))
def test_trajectory_metadata_rejects_inconsistent_records(
    prepared_trajectory, change, exception,
):
    trajectory, _ = prepared_trajectory
    with pytest.raises(exception):
        replace(trajectory, **change)


def test_disconnected_steps_or_event_schedule_are_rejected(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    with pytest.raises(ValueError, match="follow"):
        replace(trajectory, steps=tuple(reversed(trajectory.steps)))
    wrong = replace(trajectory.schedule[1], ternary_event=False)
    with pytest.raises(ValueError, match="clock"):
        replace(trajectory, schedule=(trajectory.schedule[0], wrong, trajectory.schedule[2]))
    with pytest.raises(ValueError, match="follow"):
        replace(trajectory, initial=trajectory.final)


def test_inconsistent_si_factors_are_rejected_between_steps(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    second = trajectory.steps[1]
    changed_pressure = replace(second.pressure, mass_unit_to_kg=2.0 * MASS_TO_KG)
    changed_step = replace(second, pressure=changed_pressure)
    with pytest.raises(ValueError, match="SI conversion"):
        replace(trajectory, steps=(trajectory.steps[0], changed_step, trajectory.steps[2]))
