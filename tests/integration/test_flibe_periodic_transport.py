
"""Independent qualification of species-resolved periodic FLiBe MD transport.

The tests reconstruct mean-squared displacement and velocity autocorrelation
from the state sequence, exercise laboratory and center-of-mass frames,
verify SI conversions and registered source identity, and detect wrapped
coordinates or modified velocity-Verlet updates.
"""

from __future__ import annotations

import copy
import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum, isfinite
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.periodic_coulomb_ewald import FLiBeEwaldParameters, FLiBePeriodicEwaldModel
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import (
    FLiBePeriodicMDRun,
    FLiBePeriodicMDUnits,
    run_flibe_periodic_velocity_verlet,
)
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.periodic_transport import (
    FLiBePeriodicTransportResult,
    FLiBeSpeciesTransportSeries,
    FLiBeTransportFrame,
    evaluate_flibe_periodic_transport,
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
    (0.0, 0.0, 0.0),
    (8.0, 0.0, 0.0),
    (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0),
    (8.0, 5.0, 6.0),
    (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITIES = (
    (0.01, 0.0, 0.0),
    (-0.01, 0.0, 0.0),
    (0.0, 0.005, 0.0),
    (0.0, -0.003, 0.0),
    (0.0, 0.0, 0.004),
    (0.0, 0.0, -0.004),
    (0.0, 0.0, 0.0),
)
CELL_EDGE = 18.0
CELL = ((CELL_EDGE, 0.0, 0.0), (0.0, CELL_EDGE, 0.0), (0.0, 0.0, CELL_EDGE))
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
BOHR_TO_M = 5.29177210903e-11
HARTREE_TO_J = 4.3597447222071e-18
TIME_UNIT_S = 1.0e-15
MASS_UNIT_KG = 1.0e-27
DT_CODE = 1.0e-3
PROVENANCE = ParameterProvenance.TEST_FIXTURE
MODEL_ID = "PERIODIC-FLIBE-TRANSPORT-QUALIFICATION"


def _model() -> FLiBePeriodicPolarizableModel:
    source = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25,
        real_image_shell=1,
        reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0,
        provenance=PROVENANCE,
        source_id="TRANSPORT-QUALIFICATION-EWALD",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="TRANSPORT-QUALIFICATION-FIXED",
            ewald_model=FLiBePeriodicEwaldModel("TRANSPORT-QUALIFICATION-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="TRANSPORT-QUALIFICATION-SHORT",
                parameters=source,
                coordinate_unit_to_bohr=1.0,
                image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="TRANSPORT-QUALIFICATION-POLARIZATION",
            parameters=source,
            ewald_parameters=ewald,
            damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _initial_state(*, positions=POSITIONS, velocities=VELOCITIES, time=0.0, step=0):
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=tuple(tuple(float(v) for v in vector) for vector in positions),
            cell=CELL,
            periodic=(True, True, True),
        ),
        velocities=tuple(tuple(float(v) for v in vector) for vector in velocities),
        masses=MASSES,
        step=step,
        time=time,
    )


def _units():
    return FLiBePeriodicMDUnits(
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=BOHR_TO_M,
        time_unit_to_second=TIME_UNIT_S,
        bohr_to_meter=BOHR_TO_M,
        hartree_to_joule=HARTREE_TO_J,
        provenance=PROVENANCE,
        source_id="TRANSPORT-QUALIFICATION-SI-UNITS",
    )


def _run(model, *, initial=None, step_count=2):
    return run_flibe_periodic_velocity_verlet(
        initial_state=_initial_state() if initial is None else initial,
        model=model,
        mass_parameters=FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        units=_units(),
        time_step=DT_CODE,
        step_count=step_count,
        neighbor_cutoff=4.0,
    )


def _mass_mean(vectors, masses):
    total_mass = fsum(masses)
    return tuple(
        fsum(mass * vector[axis] for mass, vector in zip(masses, vectors, strict=True))
        / total_mass
        for axis in range(3)
    )


def _independent_reference(run, frame, symbol):
    states = run.trajectory.states
    initial = states[0]
    indices = tuple(index for index, name in enumerate(initial.configuration.species)
                    if name == symbol)
    initial_position = initial.configuration.positions
    initial_velocity = initial.velocities
    masses = initial.masses
    center_velocity_0 = _mass_mean(initial_velocity, masses)
    length_factor = BOHR_TO_M
    velocity_factor = BOHR_TO_M / TIME_UNIT_S
    msd, vacf, times = [], [], []
    for state in states:
        times.append((state.time - initial.time) * TIME_UNIT_S)
        displacements = tuple(
            tuple(state.configuration.positions[i][a] - initial_position[i][a]
                  for a in range(3))
            for i in range(len(SPECIES))
        )
        center_displacement = _mass_mean(displacements, masses)
        center_velocity = _mass_mean(state.velocities, masses)
        if frame is FLiBeTransportFrame.LABORATORY:
            center_displacement = (0.0, 0.0, 0.0)
            center_velocity = (0.0, 0.0, 0.0)
            velocity_origin = (0.0, 0.0, 0.0)
        else:
            velocity_origin = center_velocity_0
        msd.append(
            fsum(
                fsum(
                    ((displacements[i][a] - center_displacement[a]) * length_factor)**2
                    for a in range(3)
                )
                for i in indices
            ) / len(indices)
        )
        vacf.append(
            fsum(
                fsum(
                    (initial_velocity[i][a] - velocity_origin[a])
                    * (state.velocities[i][a] - center_velocity[a])
                    * velocity_factor**2
                    for a in range(3)
                )
                for i in indices
            ) / len(indices)
        )
    return tuple(times), tuple(msd), tuple(vacf)


def _modified_state_run(run, index, state):
    """Construct an altered stored trajectory to exercise the independent guard."""
    steps = list(run.trajectory.steps)
    if index > 0:
        steps[index - 1] = replace(steps[index - 1], current=state)
    if index < len(steps):
        steps[index] = replace(steps[index], previous=state)
    changed = copy.copy(run)
    object.__setattr__(changed, "trajectory", MolecularDynamicsTrajectory(tuple(steps)))
    return changed


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def run(model):
    return _run(model)


@pytest.fixture(scope="module")
def com(run):
    return evaluate_flibe_periodic_transport(
        run, trajectory_id="FLIBE-TRANSPORT-COM",
    )


@pytest.fixture(scope="module")
def lab(run):
    return evaluate_flibe_periodic_transport(
        run, trajectory_id="FLIBE-TRANSPORT-LAB", frame=FLiBeTransportFrame.LABORATORY,
    )


def test_provenance_and_species_inventory(run, com):
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert isinstance(com, FLiBePeriodicTransportResult)
    assert com.model_id == run.model_id == MODEL_ID
    assert com.source_file_sha256 == run.source_file_sha256 == digest
    assert com.source_doi == SOURCE_DOI
    assert com.units_source_id == run.units.source_id
    assert com.trajectory_id == "FLIBE-TRANSPORT-COM"
    assert com.frame is FLiBeTransportFrame.CENTER_OF_MASS
    assert com.sample_count == run.trajectory.step_count + 1 == 3
    assert com.atom_count == len(SPECIES) == 7
    assert tuple(series.species for series in com.species_series) == ("Li", "Be", "F")
    assert tuple(series.atom_count for series in com.species_series) == (2, 1, 4)
    assert all(isinstance(row, FLiBeSpeciesTransportSeries) for row in com.species_series)


@pytest.mark.parametrize("frame", (
    FLiBeTransportFrame.LABORATORY,
    FLiBeTransportFrame.CENTER_OF_MASS,
))
def test_species_msd_and_vacf_equal_independent_si_recomputation(run, com, lab, frame):
    result = com if frame is FLiBeTransportFrame.CENTER_OF_MASS else lab
    for symbol in ("Li", "Be", "F"):
        times, reference_msd, reference_vacf = _independent_reference(run, frame, symbol)
        measured = result.for_species(symbol)
        assert result.times_s == pytest.approx(times, rel=1.0e-14, abs=0.0)
        assert measured.mean_squared_displacement_m2 == pytest.approx(
            reference_msd, rel=1.0e-12, abs=1.0e-43
        )
        assert measured.velocity_autocorrelation_m2_per_s2 == pytest.approx(
            reference_vacf, rel=1.0e-12, abs=1.0e-10
        )
        assert all(isfinite(value) and value >= 0.0
                   for value in measured.mean_squared_displacement_m2)
        assert all(isfinite(value) for value in measured.velocity_autocorrelation_m2_per_s2)
        assert measured.mean_squared_displacement_m2[0] == 0.0
        assert measured.velocity_autocorrelation_m2_per_s2[0] >= 0.0
        assert measured.mean_squared_displacement_m2[-1] > 0.0


def test_time_origin_and_si_scaling_are_explicit(run, com):
    assert run.trajectory.initial.time == 0.0
    assert com.times_s == pytest.approx((0.0, 1.0e-18, 2.0e-18), rel=1.0e-14, abs=0.0)
    assert com.times_s[0] == 0.0
    assert com.times_s[1] < com.times_s[2]
    assert BOHR_TO_M / TIME_UNIT_S == pytest.approx(52917.7210903, rel=1.0e-14)
    assert com.for_species("Li").velocity_autocorrelation_m2_per_s2[0] > 1.0e4
    assert 1.0e-33 < com.for_species("Li").mean_squared_displacement_m2[-1] < 1.0e-28


def test_replay_produces_identical_species_observations(model, run, com):
    again = _run(model)
    second = evaluate_flibe_periodic_transport(
        again, trajectory_id="FLIBE-TRANSPORT-COM",
    )
    assert again == run
    assert second == com
    assert second.for_species("Li") == com.for_species("Li")
    assert second.for_species("Be") == com.for_species("Be")
    assert second.for_species("F") == com.for_species("F")


def test_galilean_shift_preserves_com_msd_and_vacf(model, com):
    shift = (0.03, -0.04, 0.02)
    shifted_velocities = tuple(
        tuple(velocity[axis] + shift[axis] for axis in range(3))
        for velocity in VELOCITIES
    )
    translated_run = _run(model, initial=_initial_state(velocities=shifted_velocities))
    shifted_com = evaluate_flibe_periodic_transport(
        translated_run, trajectory_id="FLIBE-TRANSPORT-DRIFT-COM",
    )
    shifted_lab = evaluate_flibe_periodic_transport(
        translated_run, trajectory_id="FLIBE-TRANSPORT-DRIFT-LAB",
        frame=FLiBeTransportFrame.LABORATORY,
    )
    for symbol in ("Li", "Be", "F"):
        original = com.for_species(symbol)
        translated = shifted_com.for_species(symbol)
        assert translated.mean_squared_displacement_m2 == pytest.approx(
            original.mean_squared_displacement_m2, rel=2.0e-8, abs=3.0e-40
        )
        assert translated.velocity_autocorrelation_m2_per_s2 == pytest.approx(
            original.velocity_autocorrelation_m2_per_s2, rel=1.0e-12, abs=1.0e-8
        )
        assert (
            shifted_lab.for_species(symbol).mean_squared_displacement_m2[-1]
            > 2.0 * translated.mean_squared_displacement_m2[-1]
        )
    assert shifted_lab.frame is FLiBeTransportFrame.LABORATORY
    assert shifted_com.frame is FLiBeTransportFrame.CENTER_OF_MASS


def test_cell_crossing_retains_continuous_displacement(model):
    offset = CELL_EDGE - 5.0e-6
    initial = _initial_state(
        positions=tuple((point[0] + offset, point[1], point[2]) for point in POSITIONS)
    )
    crossing_run = _run(model, initial=initial)
    first, second = crossing_run.trajectory.states[:2]
    x0 = first.configuration.positions[0][0]
    x1 = second.configuration.positions[0][0]
    assert x0 < CELL_EDGE < x1
    assert 0.0 < x1 - x0 < 1.0e-3
    crossing = evaluate_flibe_periodic_transport(
        crossing_run, trajectory_id="FLIBE-TRANSPORT-LATTICE-CROSSING",
    )
    _, reference_msd, _ = _independent_reference(
        crossing_run, FLiBeTransportFrame.CENTER_OF_MASS, "Li"
    )
    assert crossing.for_species("Li").mean_squared_displacement_m2 == pytest.approx(
        reference_msd, rel=1.0e-12, abs=1.0e-42
    )
    assert crossing.for_species("Li").mean_squared_displacement_m2[1] < 1.0e-26


def test_wrapped_lattice_coordinate_is_rejected(run):
    original = run.trajectory.states[1]
    positions = list(original.configuration.positions)
    positions[0] = (positions[0][0] - CELL_EDGE, *positions[0][1:])
    changed = replace(original, configuration=replace(
        original.configuration, positions=tuple(positions)
    ))
    damaged = _modified_state_run(run, 1, changed)
    with pytest.raises(ValueError, match="unwrapped Verlet"):
        evaluate_flibe_periodic_transport(
            damaged, trajectory_id="FLIBE-TRANSPORT-WRAPPED"
        )


def test_modified_verlet_velocity_is_rejected(run):
    original = run.trajectory.states[1]
    velocities = list(original.velocities)
    velocities[0] = (velocities[0][0] + 0.1, *velocities[0][1:])
    damaged = _modified_state_run(run, 1, replace(original, velocities=tuple(velocities)))
    with pytest.raises(ValueError, match="velocity increment violates Verlet"):
        evaluate_flibe_periodic_transport(
            damaged, trajectory_id="FLIBE-TRANSPORT-ALTERED-VELOCITY"
        )


def test_modified_periodic_cell_is_rejected(run):
    original = run.trajectory.states[1]
    new_cell = tuple(tuple(1.01 * value for value in vector) for vector in CELL)
    changed = replace(original, configuration=replace(original.configuration, cell=new_cell))
    damaged = _modified_state_run(run, 1, changed)
    with pytest.raises(ValueError, match="fixed cell, species, and masses"):
        evaluate_flibe_periodic_transport(damaged, trajectory_id="FLIBE-TRANSPORT-CELL")


def test_nonzero_initial_clock_is_respected(model):
    shifted = _run(model, initial=_initial_state(time=1.25, step=10), step_count=1)
    result = evaluate_flibe_periodic_transport(
        shifted, trajectory_id="FLIBE-TRANSPORT-OFFSET-CLOCK"
    )
    assert result.sample_count == 2
    assert result.times_s[0] == 0.0
    assert result.times_s[1] == pytest.approx(DT_CODE * TIME_UNIT_S, rel=1.0e-12, abs=0.0)
    assert tuple(item.step for item in shifted.trajectory.states) == (10, 11)


@pytest.mark.parametrize("value,error", (
    (None, TypeError),
    ("CENTER_OF_MASS", TypeError),
))
def test_frame_argument_requires_enum(run, value, error):
    with pytest.raises(error, match="frame must be"):
        evaluate_flibe_periodic_transport(
            run, trajectory_id="FLIBE-TRANSPORT-INVALID-FRAME", frame=value
        )


@pytest.mark.parametrize("field,value,error", (
    ("trajectory_id", "", ValueError),
    ("trajectory_id", " UNTRIMMED ", ValueError),
    ("trajectory_id", None, TypeError),
    ("position_tolerance_code", -1.0, ValueError),
    ("position_tolerance_code", float("nan"), ValueError),
    ("position_tolerance_code", True, TypeError),
    ("velocity_tolerance_code", -1.0, ValueError),
    ("velocity_tolerance_code", float("inf"), ValueError),
    ("velocity_tolerance_code", False, TypeError),
))
def test_invalid_operator_arguments_are_rejected(run, field, value, error):
    kwargs = {"trajectory_id": "FLIBE-TRANSPORT-ARGUMENTS"}
    kwargs[field] = value
    with pytest.raises(error):
        evaluate_flibe_periodic_transport(run, **kwargs)


def test_operator_requires_flibe_md_run():
    with pytest.raises(TypeError, match="run must be"):
        evaluate_flibe_periodic_transport(None, trajectory_id="FLIBE-TRANSPORT-TYPE")


@pytest.mark.parametrize("update", (
    {"species": "Na"},
    {"atom_count": 0},
    {"atom_count": True},
    {"mean_squared_displacement_m2": (0.0, -1.0)},
    {"mean_squared_displacement_m2": (0.0, float("nan"))},
    {"mean_squared_displacement_m2": (0.1, 0.2)},
    {"velocity_autocorrelation_m2_per_s2": (1.0,)},
    {"velocity_autocorrelation_m2_per_s2": (-1.0, 1.0)},
    {"velocity_autocorrelation_m2_per_s2": (1.0, float("inf"))},
))
def test_species_series_rejects_invalid_data(com, update):
    with pytest.raises((TypeError, ValueError)):
        replace(com.species_series[0], **update)


@pytest.mark.parametrize("update", (
    {"source_file_sha256": "A" * 64},
    {"source_file_sha256": "bad"},
    {"trajectory_id": " BAD "},
    {"times_s": (0.0,)},
    {"times_s": (1.0, 2.0, 3.0)},
    {"times_s": (0.0, 0.0, 2.0)},
    {"times_s": (0.0, 2.0, 1.0)},
    {"times_s": (0.0, 1.0, float("nan"))},
    {"species_series": ()},
    {"species_series": ("Li", "Be", "F")},
    {"frame": "LABORATORY"},
))
def test_result_rejects_incoherent_metadata(com, update):
    with pytest.raises((TypeError, ValueError)):
        replace(com, **update)


def test_species_selector_and_frozen_results(com):
    assert com.for_species("Li") is com.species_series[0]
    assert com.for_species("Be") is com.species_series[1]
    assert com.for_species("F") is com.species_series[2]
    with pytest.raises(ValueError, match="species must be"):
        com.for_species("H")
    with pytest.raises(FrozenInstanceError):
        com.model_id = "ALTERED"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        com.species_series[0].atom_count = 5  # type: ignore[misc]
