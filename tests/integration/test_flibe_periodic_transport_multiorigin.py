"""Independent integration checks for multi-origin periodic FLiBe transport.

Recompute species-resolved MSD and VACF from recorded states at each eligible
origin and lag. Verify sampling, units, continuous periodic Verlet dynamics,
source identity, and reference-frame transformation.
"""

from __future__ import annotations

import copy
import hashlib
from dataclasses import FrozenInstanceError, replace
from math import isfinite
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import (
    FLiBePeriodicMDUnits,
    run_flibe_periodic_velocity_verlet,
)
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.periodic_transport import FLiBeTransportFrame, evaluate_flibe_periodic_transport
from tr_eif.flibe.periodic_transport_multiorigin import (
    FLiBePeriodicMultiOriginResult,
    evaluate_flibe_periodic_multi_origin_transport,
)
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0), (8.0, 10.0, 11.0),
)
VELOCITIES = (
    (0.01, 0.0, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.005, 0.0),
    (0.0, -0.003, 0.0), (0.0, 0.0, 0.004), (0.0, 0.0, -0.004), (0.0, 0.0, 0.0),
)
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
CELL_EDGE = 18.0
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
BOHR_TO_M = 5.29177210903e-11
TIME_TO_S = 1.0e-15
DT = 1.0e-3
MODEL_ID = "PERIODIC-FLIBE-MULTI-ORIGIN-QUALIFICATION"
METHOD_ID = "tr-eif.flibe.periodic-multi-origin-msd-vacf.v1"


def _model():
    params = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25, real_image_shell=1, reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0, provenance=ParameterProvenance.TEST_FIXTURE,
        source_id="MULTI-ORIGIN-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="MULTI-ORIGIN-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("MULTI-ORIGIN-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="MULTI-ORIGIN-SHORT", parameters=params,
                coordinate_unit_to_bohr=1.0, image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="MULTI-ORIGIN-POLARIZATION", parameters=params,
            ewald_parameters=ewald, damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _initial(*, positions=POSITIONS, velocities=VELOCITIES, time=0.0, step=0):
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=tuple(tuple(float(x) for x in v) for v in positions),
            cell=CELL, periodic=(True, True, True),
        ),
        velocities=tuple(tuple(float(x) for x in v) for v in velocities),
        masses=MASSES, time=time, step=step,
    )


def _execute(model, *, initial=None, steps=4):
    return run_flibe_periodic_velocity_verlet(
        initial_state=_initial() if initial is None else initial,
        model=model,
        mass_parameters=FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        units=FLiBePeriodicMDUnits(
            mass_unit_to_kg=1.0e-27, coordinate_unit_to_meter=BOHR_TO_M,
            time_unit_to_second=TIME_TO_S, bohr_to_meter=BOHR_TO_M,
            hartree_to_joule=4.3597447222071e-18,
            provenance=ParameterProvenance.TEST_FIXTURE,
            source_id="MULTI-ORIGIN-UNITS",
        ),
        time_step=DT, step_count=steps, neighbor_cutoff=4.0,
    )


def _result(run, *, frame=FLiBeTransportFrame.CENTER_OF_MASS, **kwargs):
    options = {"trajectory_id": "FLIBE-MULTI-ORIGIN-QUALIFICATION", "frame": frame}
    options.update(kwargs)
    return evaluate_flibe_periodic_multi_origin_transport(run, **options)


def _alter_state(run, index, state):
    """Build a diagnostic run containing a changed recorded MD state."""
    steps = list(run.trajectory.steps)
    if index:
        steps[index - 1] = replace(steps[index - 1], current=state)
    if index < len(steps):
        steps[index] = replace(steps[index], previous=state)
    altered = copy.copy(run)
    object.__setattr__(altered, "trajectory", MolecularDynamicsTrajectory(tuple(steps)))
    return altered


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def run(model):
    return _execute(model)


@pytest.fixture(scope="module")
def com(run):
    return _result(run)


def _independent_reference(run, frame, start, stop, stride, last_lag):
    """Direct enumeration of all atom/origin pairs for each declared lag."""
    states = run.trajectory.states
    masses = states[0].masses
    mass_total = sum(masses)
    length_squared = run.units.coordinate_unit_to_meter ** 2
    speed_squared = (run.units.coordinate_unit_to_meter / run.units.time_unit_to_second) ** 2
    counts = []
    msd = {name: [] for name in ("Li", "Be", "F")}
    vacf = {name: [] for name in ("Li", "Be", "F")}
    for lag in range(last_lag + 1):
        origins = list(range(start, stop - lag, stride))
        counts.append(len(origins))
        for symbol in ("Li", "Be", "F"):
            selected = [i for i, name in enumerate(SPECIES) if name == symbol]
            squared, cross = [], []
            for origin in origins:
                first, last = states[origin], states[origin + lag]
                changes = [
                    [last.configuration.positions[i][a] - first.configuration.positions[i][a]
                     for a in range(3)] for i in range(len(SPECIES))
                ]
                if frame is FLiBeTransportFrame.CENTER_OF_MASS:
                    drift = [sum(MASSES[i] * changes[i][a] for i in range(len(SPECIES)))
                             / mass_total for a in range(3)]
                    first_com = [sum(MASSES[i] * first.velocities[i][a]
                                     for i in range(len(SPECIES))) / mass_total
                                 for a in range(3)]
                    last_com = [sum(MASSES[i] * last.velocities[i][a]
                                    for i in range(len(SPECIES))) / mass_total
                                for a in range(3)]
                else:
                    drift = [0.0] * 3
                    first_com = [0.0] * 3
                    last_com = [0.0] * 3
                for atom in selected:
                    squared.append(sum((changes[atom][a] - drift[a]) ** 2
                                       for a in range(3)))
                    cross.append(sum(
                        (first.velocities[atom][a] - first_com[a])
                        * (last.velocities[atom][a] - last_com[a])
                        for a in range(3)
                    ))
            msd[symbol].append(sum(squared) * length_squared / len(squared))
            vacf[symbol].append(sum(cross) * speed_squared / len(cross))
    return tuple(counts), msd, vacf


@pytest.mark.parametrize("frame", (
    FLiBeTransportFrame.CENTER_OF_MASS,
    FLiBeTransportFrame.LABORATORY,
))
@pytest.mark.parametrize("start,stop,stride,lag", (
    (0, 5, 1, 4), (0, 5, 2, 4), (0, 5, 3, 2), (0, 5, 5, 4),
    (1, 5, 1, 3), (1, 5, 2, 3), (1, 4, 1, 2), (1, 4, 2, 1),
    (2, 5, 1, 2), (3, 5, 7, 1),
))
def test_independent_msd_vacf_for_each_lag_origin_and_species(
    run, frame, start, stop, stride, lag
):
    observed = _result(
        run, frame=frame, origin_start_index=start, origin_stop_index=stop,
        origin_stride=stride, maximum_lag_steps=lag,
    )
    counts, msd, vacf = _independent_reference(run, frame, start, stop, stride, lag)
    assert isinstance(observed, FLiBePeriodicMultiOriginResult)
    assert observed.origin_count_by_lag == counts
    assert (observed.origin_start_index, observed.origin_stop_index, observed.origin_stride) == (
        start, stop, stride
    )
    assert observed.frame is frame
    assert observed.lag_times_s == pytest.approx(
        tuple(index * DT * TIME_TO_S for index in range(lag + 1)),
        rel=1.0e-12, abs=0.0,
    )
    for symbol, atom_count in (("Li", 2), ("Be", 1), ("F", 4)):
        row = observed.for_species(symbol)
        assert row.atom_count == atom_count
        assert row.mean_squared_displacement_m2 == pytest.approx(
            msd[symbol], rel=1.0e-11, abs=1.0e-42,
        )
        assert row.velocity_autocorrelation_m2_per_s2 == pytest.approx(
            vacf[symbol], rel=1.0e-11, abs=1.0e-8,
        )
        assert row.mean_squared_displacement_m2[0] == 0.0
        assert all(isfinite(value) and value >= 0.0
                   for value in row.mean_squared_displacement_m2)
        assert all(isfinite(value) for value in row.velocity_autocorrelation_m2_per_s2)


def test_default_metadata_and_registered_source(run, com):
    assert com.method_id == METHOD_ID
    assert com.trajectory_id == "FLIBE-MULTI-ORIGIN-QUALIFICATION"
    assert com.frame is FLiBeTransportFrame.CENTER_OF_MASS
    assert com.origin_start_index == 0
    assert com.origin_stop_index == 5
    assert com.origin_stride == 1
    assert com.origin_count_by_lag == (5, 4, 3, 2, 1)
    assert com.observables.sample_count == 5
    assert com.lag_times_s[0] == 0.0
    assert com.sampling_interval_s == pytest.approx(DT * TIME_TO_S, rel=1.0e-12)
    assert com.observables.model_id == run.model_id == MODEL_ID
    assert com.observables.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert com.observables.source_doi == SOURCE_DOI
    assert com.observables.units_source_id == run.units.source_id
    assert tuple(item.species for item in com.species_series) == ("Li", "Be", "F")
    assert com.observables.atom_count == len(SPECIES)


def test_origin_population_boundaries_and_partial_window(run):
    assert _result(run, origin_stride=2).origin_count_by_lag == (3, 2, 2, 1, 1)
    assert _result(run, origin_stride=99).origin_count_by_lag == (1, 1, 1, 1, 1)
    assert _result(run, maximum_lag_steps=2).origin_count_by_lag == (5, 4, 3)
    assert _result(run, origin_start_index=2).origin_count_by_lag == (3, 2, 1)
    assert _result(run, origin_stop_index=3).origin_count_by_lag == (3, 2, 1)
    assert _result(run, origin_start_index=1, origin_stop_index=3).origin_count_by_lag == (2, 1)


def test_terminal_lag_matches_single_origin_verlet_observables(run, com):
    single = evaluate_flibe_periodic_transport(
        run, trajectory_id="FLIBE-TERMINAL-REFERENCE",
    )
    assert com.origin_count_by_lag[-1] == 1
    assert com.lag_times_s[-1] == pytest.approx(single.times_s[-1], rel=1.0e-12)
    for symbol in ("Li", "Be", "F"):
        a, b = com.for_species(symbol), single.for_species(symbol)
        assert a.mean_squared_displacement_m2[-1] == pytest.approx(
            b.mean_squared_displacement_m2[-1], rel=1.0e-12, abs=1.0e-42,
        )
        assert a.velocity_autocorrelation_m2_per_s2[-1] == pytest.approx(
            b.velocity_autocorrelation_m2_per_s2[-1], rel=1.0e-12, abs=1.0e-8,
        )


def test_zero_lag_vacf_averages_all_origins(run, com):
    counts, _, vacf = _independent_reference(
        run, FLiBeTransportFrame.CENTER_OF_MASS, 0, 5, 1, 0,
    )
    assert counts == (5,)
    for symbol in ("Li", "Be", "F"):
        assert com.for_species(symbol).velocity_autocorrelation_m2_per_s2[0] == pytest.approx(
            vacf[symbol][0], rel=1.0e-12, abs=1.0e-8,
        )


def test_deterministic_replay_and_frozen_output(model, run, com):
    replay = _execute(model)
    assert replay == run
    second = _result(replay)
    assert second == com
    assert second.observables == com.observables
    for symbol, index in (("Li", 0), ("Be", 1), ("F", 2)):
        assert second.for_species(symbol) is second.species_series[index]
    with pytest.raises(ValueError, match="species"):
        com.for_species("H")
    with pytest.raises(FrozenInstanceError):
        com.origin_stride = 7  # type: ignore[misc]


def test_center_of_mass_transport_is_galilean_invariant(model, com):
    boost = (0.03, -0.02, 0.04)
    shifted_velocities = tuple(
        tuple(v[a] + boost[a] for a in range(3)) for v in VELOCITIES
    )
    shifted = _execute(model, initial=_initial(velocities=shifted_velocities))
    transformed = _result(shifted)
    laboratory = _result(shifted, frame=FLiBeTransportFrame.LABORATORY)
    for symbol in ("Li", "Be", "F"):
        original, current = com.for_species(symbol), transformed.for_species(symbol)
        assert current.mean_squared_displacement_m2 == pytest.approx(
            original.mean_squared_displacement_m2, rel=4.0e-8, abs=3.0e-40,
        )
        assert current.velocity_autocorrelation_m2_per_s2 == pytest.approx(
            original.velocity_autocorrelation_m2_per_s2, rel=1.0e-12, abs=1.0e-8,
        )
        assert laboratory.for_species(symbol).mean_squared_displacement_m2[-1] > (
            2 * current.mean_squared_displacement_m2[-1]
        )


def test_periodic_boundary_crossing_keeps_continuous_positions(model):
    shifted_positions = tuple(
        (p[0] + CELL_EDGE - 5.0e-6, p[1], p[2]) for p in POSITIONS
    )
    crossing = _execute(model, initial=_initial(positions=shifted_positions))
    assert crossing.trajectory.states[0].configuration.positions[0][0] < CELL_EDGE
    assert crossing.trajectory.states[1].configuration.positions[0][0] > CELL_EDGE
    observed = _result(crossing, origin_stride=2)
    counts, msd, _ = _independent_reference(
        crossing, FLiBeTransportFrame.CENTER_OF_MASS, 0, 5, 2, 4,
    )
    assert observed.origin_count_by_lag == counts
    for symbol in ("Li", "Be", "F"):
        assert observed.for_species(symbol).mean_squared_displacement_m2 == pytest.approx(
            msd[symbol], rel=1.0e-11, abs=1.0e-42,
        )
    original = crossing.trajectory.states[1]
    positions = list(original.configuration.positions)
    positions[0] = (positions[0][0] - CELL_EDGE, *positions[0][1:])
    altered_state = replace(original, configuration=replace(
        original.configuration, positions=tuple(positions)
    ))
    with pytest.raises(ValueError, match="unwrapped Verlet"):
        _result(_alter_state(crossing, 1, altered_state))


def test_changed_velocity_verlet_update_is_rejected(run):
    original = run.trajectory.states[2]
    velocities = list(original.velocities)
    velocities[0] = (velocities[0][0] + 0.15, *velocities[0][1:])
    altered_state = replace(original, velocities=tuple(velocities))
    with pytest.raises(ValueError, match="velocity increment violates Verlet"):
        _result(_alter_state(run, 2, altered_state))


def test_changed_periodic_cell_is_rejected(run):
    original = run.trajectory.states[2]
    changed_cell = tuple(tuple(v * 1.01 for v in direction) for direction in CELL)
    altered_state = replace(original, configuration=replace(
        original.configuration, cell=changed_cell
    ))
    with pytest.raises(ValueError, match="fixed cell"):
        _result(_alter_state(run, 2, altered_state))


@pytest.mark.parametrize("arguments,error", (
    ({"origin_start_index": -1}, ValueError),
    ({"origin_start_index": 4}, ValueError),
    ({"origin_start_index": 5}, ValueError),
    ({"origin_start_index": True}, TypeError),
    ({"origin_start_index": 0.5}, TypeError),
    ({"origin_stop_index": 1}, ValueError),
    ({"origin_stop_index": 6}, ValueError),
    ({"origin_stop_index": 0}, ValueError),
    ({"origin_stop_index": False}, TypeError),
    ({"origin_stop_index": "4"}, TypeError),
    ({"origin_start_index": 3, "origin_stop_index": 4}, ValueError),
    ({"origin_start_index": 3, "origin_stop_index": 2}, ValueError),
    ({"origin_stride": 0}, ValueError),
    ({"origin_stride": -2}, ValueError),
    ({"origin_stride": True}, TypeError),
    ({"origin_stride": 1.5}, TypeError),
    ({"maximum_lag_steps": 0}, ValueError),
    ({"maximum_lag_steps": -1}, ValueError),
    ({"maximum_lag_steps": 5}, ValueError),
    ({"maximum_lag_steps": False}, TypeError),
    ({"maximum_lag_steps": 1.5}, TypeError),
    ({"origin_start_index": 2, "maximum_lag_steps": 3}, ValueError),
    ({"frame": "LABORATORY"}, TypeError),
    ({"trajectory_id": ""}, ValueError),
    ({"trajectory_id": " BAD "}, ValueError),
    ({"trajectory_id": None}, TypeError),
    ({"position_tolerance_code": -1.0}, ValueError),
    ({"velocity_tolerance_code": float("nan")}, ValueError),
))
def test_invalid_sampling_arguments_are_rejected(run, arguments, error):
    with pytest.raises(error):
        _result(run, **arguments)


def test_operator_requires_periodic_flibe_md_run():
    with pytest.raises(TypeError, match="run must be"):
        _result(None)


@pytest.mark.parametrize("update", (
    {"method_id": "INVALID"},
    {"origin_start_index": -1},
    {"origin_start_index": True},
    {"origin_start_index": 4},
    {"origin_stop_index": 1},
    {"origin_stop_index": False},
    {"origin_stride": 0},
    {"origin_stride": True},
    {"origin_count_by_lag": (5, 5, 3, 2, 1)},
    {"origin_count_by_lag": (5, 4, 3)},
    {"origin_count_by_lag": (5, 4, 3, 2, True)},
    {"origin_count_by_lag": [5, 4, 3, 2, 1]},
    {"sampling_interval_s": 0.0},
    {"sampling_interval_s": -1.0},
    {"sampling_interval_s": float("nan")},
    {"sampling_interval_s": True},
))
def test_output_metadata_checks_origin_counts_and_units(com, update):
    with pytest.raises((TypeError, ValueError)):
        replace(com, **update)


def test_output_rejects_nonuniform_lag_axis_and_wrong_species_order(com):
    with pytest.raises((TypeError, ValueError)):
        replace(com, observables=replace(
            com.observables, times_s=(0.0, 1.0e-18, 2.0e-18, 3.1e-18, 4.0e-18)
        ))
    with pytest.raises((TypeError, ValueError)):
        replace(com, observables=replace(
            com.observables, species_series=tuple(reversed(com.observables.species_series))
        ))


def test_nonuniform_state_clock_is_rejected_by_lag_sampling(run):
    original = run.trajectory.states[2]
    shifted = replace(original, time=original.time + 1.0e-4)
    altered = _alter_state(run, 2, shifted)
    with pytest.raises(ValueError, match="uniformly sampled MD states"):
        _result(
            altered,
            position_tolerance_code=1.0e-3,
            velocity_tolerance_code=1.0e-3,
        )
