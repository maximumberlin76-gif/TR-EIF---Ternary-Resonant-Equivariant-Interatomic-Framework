"""Independent velocity-Verlet and energy qualification for polarizable FLiBe MD."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum, sqrt
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.flibe.configuration import FLiBeConfiguration
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
from tr_eif.flibe.registered_pair_coefficients import SOURCE_DOI, load_flibe_registered_pair_parameters
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
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
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
VELOCITIES = (
    (0.01, 0.0, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.005, 0.0),
    (0.0, -0.003, 0.0), (0.0, 0.0, 0.004), (0.0, 0.0, -0.004),
    (0.0, 0.0, 0.0),
)
MASS_UNIT_KG = 1.0e-27
BOHR_M = 5.29177210903e-11
HARTREE_J = 4.3597447222071e-18
TIME_UNIT_S = 1.0e-15
TIME_STEP = 1.0e-3
NEIGHBOR_CUTOFF = 4.0
PROVENANCE = ParameterProvenance.TEST_FIXTURE
ENERGY_DRIFT_LIMIT_HARTREE = 2.0e-8
VERLET_ABSOLUTE_TOLERANCE = 4.0e-12
MOMENTUM_ABSOLUTE_TOLERANCE = 2.0e-12


def _mass_parameters() -> FLiBeMassParameters:
    return FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0)


def _units(**updates: object) -> FLiBePeriodicMDUnits:
    args: dict[str, object] = {
        "mass_unit_to_kg": MASS_UNIT_KG,
        "coordinate_unit_to_meter": BOHR_M,
        "time_unit_to_second": TIME_UNIT_S,
        "bohr_to_meter": BOHR_M,
        "hartree_to_joule": HARTREE_J,
        "provenance": PROVENANCE,
        "source_id": "PERIODIC-MD-EXPLICIT-UNIT-FIXTURE",
    }
    args.update(updates)
    return FLiBePeriodicMDUnits(**args)


def _model() -> FLiBePeriodicPolarizableModel:
    parameters = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25,
        real_image_shell=1,
        reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0,
        provenance=PROVENANCE,
        source_id="PERIODIC-MD-EWALD-FIXTURE",
    )
    return FLiBePeriodicPolarizableModel(
        model_id="PERIODIC-POLARIZABLE-FLIBE-MD-FIXTURE",
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="PERIODIC-MD-FIXED-CHARGE",
            ewald_model=FLiBePeriodicEwaldModel("PERIODIC-MD-COULOMB", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="PERIODIC-MD-SHORT-RANGE",
                parameters=parameters,
                coordinate_unit_to_bohr=1.0,
                image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="PERIODIC-MD-POLARIZATION",
            parameters=parameters,
            ewald_parameters=ewald,
            damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _state(*, positions=POSITIONS, velocities=VELOCITIES, species=SPECIES,
           periodic=(True, True, True), step=0, time=0.0) -> MolecularDynamicsState:
    configuration = AtomicConfiguration(
        species=tuple(species),
        positions=tuple(tuple(float(x) for x in r) for r in positions),
        cell=CELL,
        periodic=periodic,
    )
    return MolecularDynamicsState(
        configuration=configuration,
        velocities=tuple(tuple(float(v) for v in row) for row in velocities),
        masses=tuple(_mass_parameters().mass_for_symbol(name) for name in species),
        step=step,
        time=time,
    )


def _run(*, state=None, model=None, units=None, masses=None, time_step=TIME_STEP,
         step_count=2, neighbor_cutoff=NEIGHBOR_CUTOFF) -> FLiBePeriodicMDRun:
    return run_flibe_periodic_velocity_verlet(
        initial_state=_state() if state is None else state,
        model=_model() if model is None else model,
        mass_parameters=_mass_parameters() if masses is None else masses,
        units=_units() if units is None else units,
        time_step=time_step,
        step_count=step_count,
        neighbor_cutoff=neighbor_cutoff,
    )


def _momentum(state: MolecularDynamicsState) -> tuple[float, float, float]:
    return tuple(fsum(m * v[a] for m, v in zip(state.masses, state.velocities, strict=True))
                 for a in range(3))


@pytest.fixture(scope="module")
def model() -> FLiBePeriodicPolarizableModel:
    return _model()


@pytest.fixture(scope="module")
def run(model) -> FLiBePeriodicMDRun:
    return _run(model=model)


def test_si_units_have_independently_derived_acceleration_and_energy_factors():
    units = _units()
    acceleration = HARTREE_J * TIME_UNIT_S**2 / (MASS_UNIT_KG * BOHR_M**2)
    kinetic = MASS_UNIT_KG * BOHR_M**2 / (TIME_UNIT_S**2 * HARTREE_J)
    assert units.acceleration_factor == pytest.approx(acceleration, rel=1e-14)
    assert units.kinetic_energy_factor == pytest.approx(kinetic, rel=1e-14)
    assert units.acceleration_factor * units.kinetic_energy_factor == pytest.approx(1.0, rel=1e-14)
    assert units.provenance is PROVENANCE
    assert units.source_id == "PERIODIC-MD-EXPLICIT-UNIT-FIXTURE"


def test_one_run_records_every_state_and_relaxed_potential(run, model):
    assert isinstance(run, FLiBePeriodicMDRun)
    assert isinstance(run.trajectory, MolecularDynamicsTrajectory)
    assert run.model_id == model.model_id
    assert run.trajectory.step_count == 2
    assert run.trajectory.atom_count == 7
    assert len(run.trajectory.states) == len(run.evaluations) == 3
    assert len(run.kinetic_energies_hartree) == len(run.total_energies_hartree) == 3
    assert [s.step for s in run.trajectory.states] == [0, 1, 2]
    assert [s.time for s in run.trajectory.states] == pytest.approx((0.0, TIME_STEP, 2 * TIME_STEP))
    assert all(s.configuration.species == SPECIES and s.configuration.cell == CELL
               and s.configuration.periodic == (True, True, True) for s in run.trajectory.states)
    assert all(s.masses == MASSES for s in run.trajectory.states)
    assert all(e.configuration.configuration == s.configuration
               for e, s in zip(run.evaluations, run.trajectory.states, strict=True))
    assert all(e.max_stationarity_residual_atomic <= 1.0e-10 for e in run.evaluations)


def test_velocity_verlet_position_and_velocity_updates_are_independent(run):
    scale = HARTREE_J * TIME_UNIT_S**2 / (MASS_UNIT_KG * BOHR_M**2)
    for item in run.trajectory.steps:
        before, after = item.previous, item.current
        for i in range(before.atom_count):
            mass = before.masses[i]
            for axis in range(3):
                a0 = scale * item.forces_before.forces[i][axis] / mass
                a1 = scale * item.forces_after.forces[i][axis] / mass
                expected_r = (before.configuration.positions[i][axis]
                              + before.velocities[i][axis] * TIME_STEP
                              + 0.5 * a0 * TIME_STEP**2)
                expected_v = before.velocities[i][axis] + 0.5 * (a0 + a1) * TIME_STEP
                assert after.configuration.positions[i][axis] == pytest.approx(
                    expected_r, rel=0, abs=VERLET_ABSOLUTE_TOLERANCE
                )
                assert after.velocities[i][axis] == pytest.approx(
                    expected_v, rel=0, abs=VERLET_ABSOLUTE_TOLERANCE
                )


def test_total_momentum_and_each_channel_force_sum_are_balanced(run):
    initial = _momentum(run.trajectory.initial)
    assert initial == pytest.approx((0.0, 0.0, 0.0), abs=1e-16)
    for state in run.trajectory.states:
        assert _momentum(state) == pytest.approx(initial, rel=0, abs=MOMENTUM_ABSOLUTE_TOLERANCE)
    for evaluation in run.evaluations:
        for axis in range(3):
            assert abs(fsum(force[axis] for force in evaluation.forces.forces)) <= 1.0e-10


def test_total_energy_and_eight_component_decomposition(run):
    expected_names = (
        "ewald_real", "ewald_reciprocal", "ewald_self",
        "short_range_cross_atom", "short_range_self_image",
        "polarization_self", "polarization_charge_dipole", "polarization_dipole_dipole",
    )
    for state, evaluation, kinetic, total in zip(
        run.trajectory.states, run.evaluations, run.kinetic_energies_hartree,
        run.total_energies_hartree, strict=True,
    ):
        assert tuple(name for name, _ in evaluation.energy_components_hartree) == expected_names
        expected_kinetic = 0.5 * fsum(
            mass * fsum(velocity[a]**2 for a in range(3))
            for mass, velocity in zip(state.masses, state.velocities, strict=True)
        ) * MASS_UNIT_KG * (BOHR_M / TIME_UNIT_S)**2 / HARTREE_J
        assert kinetic == pytest.approx(expected_kinetic, rel=1e-13, abs=1e-14)
        assert evaluation.energy.total_energy == pytest.approx(
            fsum(value for _, value in evaluation.energy_components_hartree), abs=1e-12
        )
        assert total == pytest.approx(evaluation.energy.total_energy + expected_kinetic, abs=1e-12)
    assert run.maximum_absolute_energy_change_hartree <= ENERGY_DRIFT_LIMIT_HARTREE
    assert run.maximum_absolute_energy_change_hartree == max(
        abs(value - run.total_energies_hartree[0]) for value in run.total_energies_hartree
    )


def test_forces_and_geometric_neighbor_graphs_keep_separate_roles(run):
    for i, step in enumerate(run.trajectory.steps):
        assert step.forces_before == run.evaluations[i].forces
        assert step.forces_after == run.evaluations[i + 1].forces
        assert step.graph_before.node_count == step.graph_after.node_count == len(SPECIES)
    assert run.trajectory.steps[0].graph_after == run.trajectory.steps[1].graph_before


def test_source_identity_and_composition_are_constant_across_md(run):
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert run.source_file_sha256 == digest
    for observed in run.evaluations:
        assert observed.source_doi == SOURCE_DOI
        assert observed.source_file_sha256 == digest
        assert observed.configuration.composition().formula_unit_fractions == (2.0 / 3.0, 1.0 / 3.0)
        assert observed.polarization_force_result.polarization_result.polarizable_indices == (3, 4, 5, 6)


def test_md_trajectory_is_directly_compatible_with_density_operator(run):
    density = evaluate_flibe_trajectory_density(
        run.trajectory,
        run.mass_parameters,
        model_id=run.model_id,
        trajectory_id="POLARIZABLE-FLIBE-MD-DENSITY",
        provenance=PROVENANCE,
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=BOHR_M,
    )
    expected_volume_m3 = 18.0**3 * BOHR_M**3
    expected_density = fsum(MASSES) * MASS_UNIT_KG / expected_volume_m3
    assert density.sample_count == 3
    assert density.atom_count == 7
    assert density.composition.formula_unit_fractions == (2.0 / 3.0, 1.0 / 3.0)
    for i, sample in enumerate(density.samples):
        assert sample.state_index == i
        assert sample.cell_volume_m3 == pytest.approx(expected_volume_m3, rel=1e-13)
        assert sample.density_kg_m3 == pytest.approx(expected_density, rel=1e-13)
    assert density.mean_density_kg_m3 == pytest.approx(expected_density, rel=1e-13)


def test_traces_are_deterministic_and_frozen(model, run):
    second = _run(model=model)
    assert second == run
    assert run.trajectory.states == second.trajectory.states
    assert run.total_energies_hartree == second.total_energies_hartree
    with pytest.raises(FrozenInstanceError):
        run.model_id = "ALTERED"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        run.units.source_id = "ALTERED"  # type: ignore[misc]


def test_graph_cutoff_does_not_modify_interatomic_force_or_motion(model, run):
    another = _run(model=model, neighbor_cutoff=9.0)
    assert another.trajectory.states == run.trajectory.states
    assert another.evaluations == run.evaluations
    assert another.total_energies_hartree == run.total_energies_hartree
    assert another.neighbor_cutoff == 9.0


def test_nonzero_initial_step_and_clock_are_retained(model):
    result = _run(model=model, state=_state(step=7, time=1.25), step_count=1)
    assert tuple(s.step for s in result.trajectory.states) == (7, 8)
    assert tuple(s.time for s in result.trajectory.states) == pytest.approx((1.25, 1.25 + TIME_STEP))


def test_kinetic_energy_scales_with_mass_and_time_units():
    state = _state()
    base = _units().kinetic_energy_hartree(state)
    modified_time = _units(time_unit_to_second=2 * TIME_UNIT_S).kinetic_energy_hartree(state)
    modified_mass = _units(mass_unit_to_kg=2 * MASS_UNIT_KG).kinetic_energy_hartree(state)
    assert base > 0.0
    assert modified_time == pytest.approx(base / 4.0, rel=1e-13)
    assert modified_mass == pytest.approx(2.0 * base, rel=1e-13)


@pytest.mark.parametrize("field,invalid,error", (
    ("mass_unit_to_kg", 0.0, ValueError),
    ("mass_unit_to_kg", False, TypeError),
    ("coordinate_unit_to_meter", -1.0, ValueError),
    ("coordinate_unit_to_meter", float("nan"), ValueError),
    ("time_unit_to_second", 0.0, ValueError),
    ("time_unit_to_second", float("inf"), ValueError),
    ("bohr_to_meter", 0.0, ValueError),
    ("hartree_to_joule", -1.0, ValueError),
    ("source_id", " untrimmed ", ValueError),
    ("provenance", "TEST_FIXTURE", TypeError),
))
def test_invalid_unit_factors_and_provenance_are_rejected(field, invalid, error):
    with pytest.raises(error):
        _units(**{field: invalid})


@pytest.mark.parametrize("field,invalid,error", (
    ("time_step", 0.0, ValueError),
    ("time_step", False, TypeError),
    ("time_step", float("nan"), ValueError),
    ("step_count", 0, ValueError),
    ("step_count", True, TypeError),
    ("step_count", 1.5, TypeError),
    ("neighbor_cutoff", 0.0, ValueError),
    ("neighbor_cutoff", -2.0, ValueError),
))
def test_invalid_md_schedule_arguments_are_rejected(field, invalid, error):
    with pytest.raises(error):
        _run(**{field: invalid})


def test_incompatible_model_and_si_length_units_are_rejected(model):
    units = _units(coordinate_unit_to_meter=2 * BOHR_M)
    with pytest.raises(ValueError, match="coordinate-unit conversions must agree"):
        _run(model=model, units=units)
    with pytest.raises(TypeError, match="model must be"):
        _units().check_model(None)


def test_initial_mass_inventory_and_periodic_boundary_are_enforced(model):
    original = _state()
    incorrect_mass = replace(original, masses=MASSES[:-1] + (5.1,))
    with pytest.raises(ValueError, match="initial MD masses must equal"):
        _run(model=model, state=incorrect_mass)
    nonperiodic = replace(original, configuration=replace(
        original.configuration, periodic=(True, False, True)
    ))
    with pytest.raises(ValueError, match="three periodic axes"):
        _run(model=model, state=nonperiodic)


def test_result_rejects_corrupted_energy_and_observation_alignment(run):
    with pytest.raises(ValueError, match="observations must align"):
        replace(run, evaluations=run.evaluations[:-1])
    with pytest.raises(ValueError, match="kinetic energy must match"):
        replace(run, kinetic_energies_hartree=(run.kinetic_energies_hartree[0] + 1.0,
                                              *run.kinetic_energies_hartree[1:]))
    with pytest.raises(ValueError, match="total energy must equal"):
        replace(run, total_energies_hartree=(run.total_energies_hartree[0] + 1.0,
                                             *run.total_energies_hartree[1:]))
    with pytest.raises(ValueError, match="declared model identifier"):
        replace(run, model_id="OTHER")
    with pytest.raises(ValueError, match="MD mass inventory"):
        replace(run, mass_parameters=FLiBeMassParameters(lithium=2.1, beryllium=3.0, fluorine=5.0))


def test_result_rejects_wrong_stored_step_forces(run):
    from tr_eif.md.trajectory import MolecularDynamicsTrajectory

    original = run.trajectory.steps[0]
    modified = ForceState(tuple((0.0, 0.0, 0.0) for _ in SPECIES))
    corrupted = replace(original, forces_before=modified)
    trajectory = MolecularDynamicsTrajectory(steps=(corrupted, *run.trajectory.steps[1:]))
    with pytest.raises(ValueError, match="starting force must agree"):
        replace(run, trajectory=trajectory)
