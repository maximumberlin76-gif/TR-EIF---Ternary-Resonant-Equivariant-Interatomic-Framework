
"""Integration qualification of FLiBe rank-two pressure-volume energy accounting.

Reconstruct each affine-cell volume increment, signed configurational work,
separate event/mechanical/barostat energy changes and the target-pressure
energy coordinate from a three-interval TR-EIP molecular-dynamics trajectory.
Verify continuity, cumulative identities, active-neutral state retention and
rejection of inconsistent energy, pressure and volume records.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_observables import (
    evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_volume_work import (
    FLiBeRankTwoTREIPPressureVolumeWorkInterval,
    FLiBeRankTwoTREIPPressureVolumeWorkLedger,
    evaluate_flibe_rank_two_tr_eip_pressure_volume_work,
)
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.ternary import TernaryState

from test_flibe_rank_two_tr_eip_pressure_coupled_trajectory import (
    LENGTH_TO_M,
    MASS_TO_KG,
    STRESS_TO_PA,
    TIME_TO_S,
    _cell_volume,
    prepared_trajectory,
)

ENERGY_TO_JOULE = STRESS_TO_PA * LENGTH_TO_M**3


@pytest.fixture(scope="module")
def qualified_work(prepared_trajectory):
    trajectory, _ = prepared_trajectory
    observables = evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables(
        trajectory,
        energy_unit_to_joule=ENERGY_TO_JOULE,
        degrees_of_freedom=18,
    )
    ledger = evaluate_flibe_rank_two_tr_eip_pressure_volume_work(observables)
    return trajectory, observables, ledger


def _kinetic_j(md_state, frame):
    """Independent kinetic-energy sum in the chosen velocity frame."""
    total_mass = sum(md_state.masses)
    center = (
        tuple(
            sum(mass * velocity[axis] for mass, velocity in zip(
                md_state.masses, md_state.velocities, strict=True,
            )) / total_mass for axis in range(3)
        )
        if frame is FLiBeVelocityFrame.CENTER_OF_MASS else (0.0, 0.0, 0.0)
    )
    return (
        0.5 * MASS_TO_KG * (LENGTH_TO_M / TIME_TO_S) ** 2
        * sum(
            mass * sum((velocity[axis] - center[axis]) ** 2 for axis in range(3))
            for mass, velocity in zip(md_state.masses, md_state.velocities, strict=True)
        )
    )


def _pressure_pa(stress_tensor):
    return -STRESS_TO_PA * sum(stress_tensor[axis][axis] for axis in range(3)) / 3.0


def test_typed_ledger_and_three_interval_alignment(qualified_work):
    trajectory, observables, ledger = qualified_work
    assert isinstance(ledger, FLiBeRankTwoTREIPPressureVolumeWorkLedger)
    assert ledger.observables == observables
    assert len(ledger.intervals) == trajectory.interval_count == 3
    assert all(isinstance(item, FLiBeRankTwoTREIPPressureVolumeWorkInterval)
               for item in ledger.intervals)
    assert tuple(item.interval_index for item in ledger.intervals) == (0, 1, 2)
    assert ledger.initial_volume_m3 == ledger.intervals[0].volume_before_m3
    assert ledger.final_volume_m3 == ledger.intervals[-1].volume_after_m3
    assert ledger.initial_total_energy_j == ledger.intervals[0].total_energy_before_j
    assert ledger.final_total_energy_j == ledger.intervals[-1].total_energy_after_j


@pytest.mark.parametrize("index", (0, 1, 2))
def test_independent_volume_stress_and_quadrature(qualified_work, index):
    trajectory, observables, ledger = qualified_work
    step = trajectory.steps[index]
    entry = ledger.intervals[index]
    source = step.barostat.stress_trace
    before_md = source.coupled.current.md_state
    after_md = step.barostat.current.md_state
    volume_before = _cell_volume(before_md.configuration.cell) * LENGTH_TO_M**3
    volume_after = _cell_volume(after_md.configuration.cell) * LENGTH_TO_M**3
    difference = volume_after - volume_before
    pressure_before = _pressure_pa(source.after_mechanics.stress.total_stress.tensor)
    pressure_after = _pressure_pa(step.barostat.after_barostat.stress.total_stress.tensor)
    independent_work = -0.5 * (pressure_before + pressure_after) * difference
    potential_change = (
        step.barostat.after_barostat.evaluation.energy.total_energy
        - source.coupled.after_mechanics.energy.total_energy
    ) * ENERGY_TO_JOULE

    assert entry.volume_before_m3 == pytest.approx(volume_before, rel=2e-12)
    assert entry.volume_after_m3 == pytest.approx(volume_after, rel=2e-12)
    assert entry.volume_change_m3 == pytest.approx(difference, rel=2e-12, abs=1e-45)
    assert entry.potential_pressure_before_pa == pytest.approx(
        pressure_before, rel=2e-12, abs=1e-5
    )
    assert entry.potential_pressure_after_pa == pytest.approx(
        pressure_after, rel=2e-12, abs=1e-5
    )
    assert entry.trapezoidal_potential_work_j == pytest.approx(
        independent_work, rel=2e-12, abs=1e-30
    )
    assert entry.potential_work_estimate_j == entry.trapezoidal_potential_work_j
    assert entry.affine_potential_change_j == pytest.approx(
        potential_change, rel=2e-12, abs=1e-30
    )
    assert entry.pressure_quadrature_residual_j == pytest.approx(
        potential_change - independent_work, rel=2e-12, abs=1e-30
    )
    assert observables.samples[index].volume_m3 == pytest.approx(volume_after, rel=2e-12)


@pytest.mark.parametrize("index", (0, 1, 2))
def test_complete_energy_and_target_pressure_coordinate(qualified_work, index):
    trajectory, observables, ledger = qualified_work
    step = trajectory.steps[index]
    entry = ledger.intervals[index]
    coupled = step.barostat.stress_trace.coupled
    md_before = coupled.coupled_step.previous.md_state
    md_mechanical = coupled.coupled_step.current.md_state
    md_scaled = step.barostat.current.md_state
    k0 = _kinetic_j(md_before, trajectory.velocity_frame)
    k1 = _kinetic_j(md_mechanical, trajectory.velocity_frame)
    k2 = _kinetic_j(md_scaled, trajectory.velocity_frame)
    u0, u_event, u_mechanical, u_scaled = (
        evaluation.energy.total_energy * ENERGY_TO_JOULE
        for evaluation in (
            coupled.before_events, coupled.after_events, coupled.after_mechanics,
            step.barostat.after_barostat.evaluation,
        )
    )
    event_change = u_event - u0
    mechanical_change = (u_mechanical - u_event) + (k1 - k0)
    affine_change = u_scaled - u_mechanical
    net_change = (u_scaled + k2) - (u0 + k0)
    pressure_term = trajectory.target_pressure.value * entry.volume_change_m3

    assert k2 == pytest.approx(k1, rel=2e-12, abs=1e-30)
    assert entry.total_energy_before_j == pytest.approx(u0 + k0, rel=2e-12)
    assert entry.total_energy_after_j == pytest.approx(u_scaled + k2, rel=2e-12)
    assert entry.event_potential_change_j == pytest.approx(
        event_change, rel=2e-12, abs=1e-30
    )
    assert entry.mechanical_total_change_j == pytest.approx(
        mechanical_change, rel=2e-12, abs=1e-30
    )
    assert entry.affine_potential_change_j == pytest.approx(
        affine_change, rel=2e-12, abs=1e-30
    )
    assert entry.net_total_energy_change_j == pytest.approx(
        net_change, rel=2e-12, abs=1e-30
    )
    assert entry.target_pressure_volume_term_j == pytest.approx(
        pressure_term, rel=2e-12, abs=1e-30
    )
    assert entry.target_pressure_energy_change_j == pytest.approx(
        net_change + pressure_term, rel=2e-12, abs=1e-30
    )
    assert entry.target_energy_after_j - entry.target_energy_before_j == pytest.approx(
        net_change + pressure_term, rel=2e-12, abs=1e-30
    )
    assert entry.net_total_energy_change_j == observables.samples[index].net_total_energy_change_j


def test_cumulative_work_mass_energy_and_state_continuity(qualified_work):
    trajectory, _, ledger = qualified_work
    entries = ledger.intervals
    assert ledger.total_volume_change_m3 == pytest.approx(
        trajectory.cell_volumes_m3[-1] - trajectory.cell_volumes_m3[0],
        rel=2e-12, abs=1e-45,
    )
    assert ledger.total_energy_change_j == pytest.approx(
        ledger.final_total_energy_j - ledger.initial_total_energy_j,
        rel=2e-12, abs=1e-30,
    )
    for name in (
        "event_potential_change_j", "mechanical_total_change_j",
        "affine_potential_change_j", "pressure_quadrature_residual_j",
        "target_pressure_volume_term_j", "target_pressure_energy_change_j",
    ):
        assert getattr(ledger, name) == pytest.approx(
            fsum(getattr(entry, name) for entry in entries),
            rel=2e-12, abs=1e-30,
        )
    assert ledger.total_energy_change_j == pytest.approx(fsum((
        ledger.event_potential_change_j, ledger.mechanical_total_change_j,
        ledger.affine_potential_change_j,
    )), rel=2e-12, abs=1e-30)
    assert ledger.target_pressure_volume_term_j == pytest.approx(
        trajectory.target_pressure.value * ledger.total_volume_change_m3,
        rel=2e-12, abs=1e-30,
    )
    assert ledger.target_pressure_energy_change_j == pytest.approx(
        ledger.total_energy_change_j + ledger.target_pressure_volume_term_j,
        rel=2e-12, abs=1e-30,
    )
    for previous, following in zip(entries, entries[1:]):
        assert following.volume_before_m3 == pytest.approx(previous.volume_after_m3, rel=2e-12)
        assert following.total_energy_before_j == pytest.approx(
            previous.total_energy_after_j, rel=2e-12, abs=1e-30,
        )
    for state, volume, density in zip(
        trajectory.states, trajectory.cell_volumes_m3, trajectory.densities_kg_m3,
        strict=True,
    ):
        assert state.md_state.masses == trajectory.initial.md_state.masses
        assert density * volume == pytest.approx(
            sum(state.md_state.masses) * MASS_TO_KG, rel=2e-12,
        )


def test_active_neutral_pending_and_separate_clocks_remain_aligned(qualified_work):
    trajectory, observables, ledger = qualified_work
    assert trajectory.initial.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert tuple(sample.retained_states for sample in observables.samples) == (
        (TernaryState.NEUTRAL,) * 7,
        (TernaryState.POSITIVE,) * 7,
        (TernaryState.POSITIVE,) * 7,
    )
    assert tuple(sample.pending_target_count for sample in observables.samples) == (7, 0, 0)
    for index, (entry, sample) in enumerate(zip(
        ledger.intervals, observables.samples, strict=True,
    )):
        state = trajectory.states[index + 1]
        assert entry.interval_index == index
        assert sample.md_step == state.md_state.step
        assert sample.resonance_step_count == state.resonance_step_count
        assert sample.ternary_event_count == state.ternary_event_count
        assert sample.retained_states == state.ternary_execution.retained_states
        assert sample.pending_target_count == sum(
            node.pending_target is not None for node in state.ternary_execution.states
        )


def test_deterministic_reconstruction_and_pure_input(qualified_work):
    trajectory, observables, ledger = qualified_work
    assert evaluate_flibe_rank_two_tr_eip_pressure_volume_work(observables) == ledger
    assert ledger.observables == observables
    assert trajectory == observables.trajectory
    assert all(isfinite(entry.pressure_quadrature_residual_j) for entry in ledger.intervals)


@pytest.mark.parametrize("ratio", (0.98, 1.0, 1.02))
def test_independent_linear_pressure_work_sign_and_zero_volume(ratio):
    """A linear pressure law is exactly integrated by the trapezoidal rule."""
    before_volume = 1.0e-27
    after_volume = before_volume * ratio
    change = after_volume - before_volume
    pressure_before, pressure_after = 200000.0, 100000.0
    target = 150000.0
    affine = -0.5 * (pressure_before + pressure_after) * change
    starting_energy = 8.0e-20
    item = FLiBeRankTwoTREIPPressureVolumeWorkInterval(
        interval_index=0,
        volume_before_m3=before_volume,
        volume_after_m3=after_volume,
        volume_change_m3=change,
        potential_pressure_before_pa=pressure_before,
        potential_pressure_after_pa=pressure_after,
        target_pressure_pa=target,
        total_energy_before_j=starting_energy,
        total_energy_after_j=starting_energy + affine,
        event_potential_change_j=0.0,
        mechanical_total_change_j=0.0,
        affine_potential_change_j=affine,
        net_total_energy_change_j=affine,
        trapezoidal_potential_work_j=affine,
        pressure_quadrature_residual_j=0.0,
        target_pressure_volume_term_j=target * change,
        target_pressure_energy_change_j=fsum((affine, target * change)),
    )
    assert item.pressure_quadrature_residual_j == 0.0
    assert item.potential_work_estimate_j == affine
    assert item.target_energy_after_j - item.target_energy_before_j == pytest.approx(
        affine + target * change, rel=1e-11, abs=1e-30,
    )
    if ratio > 1.0:
        assert item.volume_change_m3 > 0.0 and affine < 0.0
    elif ratio < 1.0:
        assert item.volume_change_m3 < 0.0 and affine > 0.0
    else:
        assert item.volume_change_m3 == affine == 0.0


@pytest.mark.parametrize("field,invalid,error", (
    ("interval_index", -1, ValueError),
    ("interval_index", True, TypeError),
    ("volume_before_m3", 0.0, ValueError),
    ("volume_after_m3", -1.0, ValueError),
    ("volume_change_m3", float("nan"), ValueError),
    ("target_pressure_pa", float("inf"), ValueError),
    ("potential_pressure_after_pa", True, TypeError),
    ("total_energy_before_j", float("nan"), ValueError),
))
def test_invalid_interval_types_and_values(qualified_work, field, invalid, error):
    _, _, ledger = qualified_work
    with pytest.raises(error):
        replace(ledger.intervals[0], **{field: invalid})


@pytest.mark.parametrize("field,increment", (
    ("volume_change_m3", 1.0e-27),
    ("trapezoidal_potential_work_j", 1.0e-18),
    ("pressure_quadrature_residual_j", 1.0e-18),
    ("target_pressure_volume_term_j", 1.0e-18),
    ("target_pressure_energy_change_j", 1.0e-18),
    ("event_potential_change_j", 1.0e-18),
    ("net_total_energy_change_j", 1.0e-18),
))
def test_interval_rejects_broken_algebraic_identity(qualified_work, field, increment):
    _, _, ledger = qualified_work
    entry = ledger.intervals[0]
    with pytest.raises(ValueError):
        replace(entry, **{field: getattr(entry, field) + increment})


@pytest.mark.parametrize("field,increment", (
    ("volume_before_m3", 1.0e-28),
    ("volume_after_m3", 1.0e-28),
    ("potential_pressure_before_pa", 1.0e9),
    ("potential_pressure_after_pa", 1.0e9),
    ("target_pressure_pa", 1.0e9),
    ("total_energy_before_j", 1.0e-18),
    ("total_energy_after_j", 1.0e-18),
))
def test_ledger_rejects_source_mismatch_or_broken_identity(qualified_work, field, increment):
    _, _, ledger = qualified_work
    entry = ledger.intervals[0]
    with pytest.raises(ValueError):
        changed = replace(entry, **{field: getattr(entry, field) + increment})
        replace(ledger, intervals=(changed, *ledger.intervals[1:]))


def test_ledger_rejects_missing_reordered_and_untyped_intervals(qualified_work):
    _, _, ledger = qualified_work
    with pytest.raises(ValueError, match="interval count"):
        replace(ledger, intervals=ledger.intervals[:-1])
    with pytest.raises(ValueError, match="indices"):
        replace(ledger, intervals=tuple(reversed(ledger.intervals)))
    with pytest.raises(TypeError, match="typed"):
        replace(ledger, intervals=(None, *ledger.intervals[1:]))
    with pytest.raises(ValueError, match="interval count"):
        replace(ledger, intervals=())
    with pytest.raises(TypeError, match="observables"):
        evaluate_flibe_rank_two_tr_eip_pressure_volume_work(None)
