"""Independent density, kinetic-temperature, and signed-pressure MD contracts."""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum, isclose
from pathlib import Path

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import CellStrainDifferentiation
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.periodic_coulomb_ewald import (
    FLiBeEwaldParameters,
    FLiBePeriodicEwaldModel,
)
from tr_eif.flibe.periodic_fixed_charge import FLiBePeriodicFixedChargeModel
from tr_eif.flibe.periodic_polarizable import FLiBePeriodicPolarizableModel
from tr_eif.flibe.periodic_polarizable_md import (
    FLiBePeriodicMDUnits,
    run_flibe_periodic_velocity_verlet,
)
from tr_eif.flibe.periodic_polarizable_md_observables import (
    FLiBePeriodicMDObservables,
    evaluate_flibe_periodic_md_observables,
)
from tr_eif.flibe.periodic_polarization import FLiBePeriodicPolarizationModel
from tr_eif.flibe.periodic_short_range import FLiBePeriodicShortRangeModel
from tr_eif.flibe.registered_pair_coefficients import (
    SOURCE_DOI,
    load_flibe_registered_pair_parameters,
)
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_pressure import FLiBeVelocityFrame
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.md.state import MolecularDynamicsState


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
CELL = ((18.0, 0.0, 0.0), (0.0, 18.0, 0.0), (0.0, 0.0, 18.0))
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
VELOCITIES = (
    (0.01, 0.0, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.005, 0.0),
    (0.0, -0.003, 0.0), (0.0, 0.0, 0.004), (0.0, 0.0, -0.004),
    (0.0, 0.0, 0.0),
)
BOHR_M = 5.29177210903e-11
HARTREE_J = 4.3597447222071e-18
MASS_KG = 1.0e-27
TIME_S = 1.0e-15
DT = 1.0e-3
STRAIN_STEP = 2.0e-5
PROVENANCE = ParameterProvenance.TEST_FIXTURE
TRAJECTORY_ID = "FLIBE-POLARIZABLE-MD-OBSERVABLES-FIXTURE"
MODEL_ID = "FLIBE-PERIODIC-MD-OBSERVABLES"
STRESS_METHOD = "SYMMETRIC-RELAXED-STRAIN-FIXTURE"
SOURCE_ID = "PUBLISHED-PARAMETERS-MD-OBSERVABLES-FIXTURE"
STRESS_TO_PA = HARTREE_J / BOHR_M**3
CELL_VOLUME_M3 = 18.0**3 * BOHR_M**3
EXPECTED_DENSITY_KG_M3 = 27.0 * MASS_KG / CELL_VOLUME_M3


def _masses() -> FLiBeMassParameters:
    return FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0)


def _units() -> FLiBePeriodicMDUnits:
    return FLiBePeriodicMDUnits(
        mass_unit_to_kg=MASS_KG,
        coordinate_unit_to_meter=BOHR_M,
        time_unit_to_second=TIME_S,
        bohr_to_meter=BOHR_M,
        hartree_to_joule=HARTREE_J,
        provenance=PROVENANCE,
        source_id="DECLARED-SI-FIXTURE",
    )


def _model() -> FLiBePeriodicPolarizableModel:
    source = load_flibe_registered_pair_parameters(SOURCE)
    ewald = FLiBeEwaldParameters(
        alpha_inverse_bohr=0.25,
        real_image_shell=1,
        reciprocal_image_shell=3,
        coordinate_unit_to_bohr=1.0,
        provenance=PROVENANCE,
        source_id="DECLARED-EWALD-FIXTURE",
    )
    return FLiBePeriodicPolarizableModel(
        model_id=MODEL_ID,
        fixed_charge_model=FLiBePeriodicFixedChargeModel(
            model_id="FIXED-CHARGE-FIXTURE",
            ewald_model=FLiBePeriodicEwaldModel("EWALD-FIXTURE", ewald),
            short_range_model=FLiBePeriodicShortRangeModel(
                model_id="SHORT-RANGE-FIXTURE",
                parameters=source,
                coordinate_unit_to_bohr=1.0,
                image_shell=1,
            ),
        ),
        polarization_model=FLiBePeriodicPolarizationModel(
            model_id="STATIONARY-FLUORIDE-FIXTURE",
            parameters=source,
            ewald_parameters=ewald,
            damping_image_shell=1,
            stationarity_absolute_tolerance=1.0e-10,
        ),
    )


def _initial(velocities=VELOCITIES) -> MolecularDynamicsState:
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES,
            positions=POSITIONS,
            cell=CELL,
            periodic=(True, True, True),
        ),
        velocities=tuple(tuple(float(v) for v in row) for row in velocities),
        masses=MASSES,
        step=0,
        time=0.0,
    )


def _run(model, *, velocities=VELOCITIES, steps=2):
    return run_flibe_periodic_velocity_verlet(
        initial_state=_initial(velocities=velocities),
        model=model,
        mass_parameters=_masses(),
        units=_units(),
        time_step=DT,
        step_count=steps,
        neighbor_cutoff=4.0,
    )


def _observe(md_run, model, *, frame=FLiBeVelocityFrame.CENTER_OF_MASS,
             dof=None, first_state_index=0, stride=2, **updates):
    if dof is None:
        dof = 18 if frame is FLiBeVelocityFrame.CENTER_OF_MASS else 21
    arguments = {
        "trajectory_id": TRAJECTORY_ID,
        "velocity_frame": frame,
        "degrees_of_freedom": dof,
        "physical_state_id": "liquid",
        "physical_state_method_id": "DECLARED-FIXTURE-STATE",
        "stress_method_id": STRESS_METHOD,
        "source_id": SOURCE_ID,
        "provenance": PROVENANCE,
        "first_state_index": first_state_index,
        "stride": stride,
    }
    arguments.update(updates)
    return evaluate_flibe_periodic_md_observables(
        md_run, model, CellStrainDifferentiation(step=STRAIN_STEP), **arguments
    )


def _kinetic_reference(state, *, frame):
    """Independent mass-weighted SI energy and momentum tensor for one frame."""
    m_total = fsum(state.masses)
    origin = tuple(
        fsum(m*v[axis] for m, v in zip(state.masses, state.velocities, strict=True))/m_total
        for axis in range(3)
    ) if frame is FLiBeVelocityFrame.CENTER_OF_MASS else (0.0, 0.0, 0.0)
    velocity_unit = BOHR_M / TIME_S
    relative = tuple(tuple(v[a] - origin[a] for a in range(3))
                     for v in state.velocities)
    twice_energy_joule = fsum(
        mass * fsum(component**2 for component in vector)
        for mass, vector in zip(state.masses, relative, strict=True)
    ) * MASS_KG * velocity_unit**2
    tensor = tuple(tuple(
        fsum(m * v[a] * v[b] for m, v in zip(state.masses, relative, strict=True))
        * MASS_KG * velocity_unit**2 / CELL_VOLUME_M3
        for b in range(3)) for a in range(3))
    return origin, twice_energy_joule, tensor


@pytest.fixture(scope="module")
def model():
    return _model()


@pytest.fixture(scope="module")
def md_run(model):
    return _run(model)


@pytest.fixture(scope="module")
def com_result(md_run, model):
    return _observe(md_run, model)


@pytest.fixture(scope="module")
def lab_result(md_run, model):
    return _observe(md_run, model, frame=FLiBeVelocityFrame.LABORATORY)


def test_source_fingerprint_and_md_state_alignment(md_run, com_result):
    assert isinstance(com_result, FLiBePeriodicMDObservables)
    assert com_result.md_run == md_run
    assert com_result.source_file_sha256 == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert all(item.source_doi == SOURCE_DOI for item in md_run.evaluations)
    assert com_result.density_trace.model_id == MODEL_ID
    assert com_result.density_trace.trajectory_id == TRAJECTORY_ID
    assert com_result.density_trace.composition.formula_unit_fractions == (2/3, 1/3)
    assert com_result.provenance is PROVENANCE
    assert tuple(row.state_index for row in com_result.density_trace.samples) == (0, 2)
    assert tuple(row.md_step for row in com_result.density_trace.samples) == (0, 2)
    assert tuple(row.md_time for row in com_result.density_trace.samples) == pytest.approx((0.0, 2*DT))
    for sample, stress in zip(com_result.density_trace.samples, com_result.stress_results, strict=True):
        assert stress.reference == md_run.evaluations[sample.state_index]
        assert stress.reference.configuration.configuration == md_run.trajectory.states[sample.state_index].configuration
        assert stress.reference.max_stationarity_residual_atomic <= 1.0e-10


def test_density_is_independently_fixed_by_mass_and_cell_volume(com_result):
    density = com_result.density_trace
    assert density.atom_count == 7
    assert density.total_mass_kg == pytest.approx(27.0*MASS_KG, rel=1e-13)
    assert density.mass_unit_to_kg == MASS_KG
    assert density.coordinate_unit_to_meter == BOHR_M
    assert density.sample_count == 2
    for sample in density.samples:
        assert sample.cell_volume_m3 == pytest.approx(CELL_VOLUME_M3, rel=1e-13)
        assert sample.density_kg_m3 == pytest.approx(EXPECTED_DENSITY_KG_M3, rel=1e-13)
    assert com_result.mean_density_kg_m3 == pytest.approx(EXPECTED_DENSITY_KG_M3, rel=1e-13)
    assert density.density_at_mean_volume_kg_m3 == pytest.approx(EXPECTED_DENSITY_KG_M3, rel=1e-13)


@pytest.mark.parametrize("frame", (FLiBeVelocityFrame.CENTER_OF_MASS, FLiBeVelocityFrame.LABORATORY))
def test_independent_temperature_and_kinetic_tensor_per_frame(frame, md_run, com_result, lab_result):
    output = com_result if frame is FLiBeVelocityFrame.CENTER_OF_MASS else lab_result
    dof = 18 if frame is FLiBeVelocityFrame.CENTER_OF_MASS else 21
    assert output.frame_thermodynamics.velocity_frame is frame
    assert output.pressure_trace.velocity_frame is frame
    assert output.frame_thermodynamics.degrees_of_freedom == dof
    for density, thermal, pressure in zip(output.density_trace.samples,
                                         output.frame_thermodynamics.samples,
                                         output.pressure_trace.samples, strict=True):
        state = md_run.trajectory.states[density.state_index]
        origin, twice_kinetic, tensor = _kinetic_reference(state, frame=frame)
        assert thermal.velocity_origin_m_s == pytest.approx(tuple(x * BOHR_M/TIME_S for x in origin), abs=1e-10)
        assert thermal.kinetic_energy_j == pytest.approx(0.5 * twice_kinetic, rel=1e-12)
        assert thermal.kinetic_temperature_k == pytest.approx(
            twice_kinetic / (dof * BOLTZMANN_CONSTANT_J_PER_K), rel=1e-12)
        assert thermal.kinetic_pressure_pa == pytest.approx(twice_kinetic / (3*CELL_VOLUME_M3), rel=1e-12)
        for a in range(3):
            assert pressure.kinetic_tensor_pa[a] == pytest.approx(tensor[a], rel=1e-12, abs=1e-7)
    expected_mean = fsum(sample.kinetic_temperature_k for sample in output.frame_thermodynamics.samples)/2
    assert output.mean_kinetic_temperature_k == pytest.approx(expected_mean, rel=1e-12)


def test_mean_pressure_is_signed_and_preserves_potential_stress(com_result):
    assert com_result.signed_mean_pressure_pa < 0.0
    assert com_result.signed_mean_pressure_pa == pytest.approx(
        fsum(sample.scalar_pressure_pa for sample in com_result.pressure_trace.samples)/2, rel=1e-12)
    assert com_result.pressure_trace.potential_stress_unit_to_pascal == pytest.approx(STRESS_TO_PA)
    for pressure, stress in zip(com_result.pressure_trace.samples, com_result.stress_results, strict=True):
        for a in range(3):
            for b in range(3):
                potential_part = -stress.total_stress.tensor[a][b] * STRESS_TO_PA
                assert pressure.configurational_tensor_pa[a][b] == pytest.approx(potential_part, rel=1e-12, abs=1e-7)
                assert pressure.pressure_tensor_pa[a][b] == pytest.approx(
                    pressure.kinetic_tensor_pa[a][b] + potential_part, rel=1e-12, abs=1e-7)
        assert pressure.scalar_pressure_pa == pytest.approx(
            fsum(pressure.pressure_tensor_pa[k][k] for k in range(3))/3, rel=1e-12)
        assert stress.total_stress.trace == pytest.approx(
            stress.fixed_charge_stress.trace + stress.polarization_stress.trace, rel=1e-11)
        assert stress.potential_pressure_hartree_per_bohr3 == pytest.approx(
            -stress.total_stress.trace/3, rel=1e-12)


def test_independent_relaxed_strain_derivative_gives_configurational_pressure(md_run, model, com_result):
    """Differentiate reoptimized total energy without the stress implementation."""
    initial = md_run.trajectory.initial.configuration
    h = 4.0e-5

    def energy_at(strain):
        deformation = 1.0 + strain
        from tr_eif.flibe.configuration import FLiBeConfiguration

        deformed = AtomicConfiguration(
            species=initial.species,
            positions=tuple((p[0]*deformation, p[1], p[2]) for p in initial.positions),
            cell=tuple((v[0]*deformation, v[1], v[2]) for v in initial.cell),
            periodic=initial.periodic,
        )
        return model.evaluate(FLiBeConfiguration(deformed)).energy.total_energy

    d_energy_d_strain = (energy_at(h) - energy_at(-h))/(2.0*h)
    independent_stress = d_energy_d_strain/(18.0**3)
    observed = com_result.pressure_trace.samples[0]
    assert independent_stress == pytest.approx(
        com_result.stress_results[0].total_stress.tensor[0][0],
        rel=0.0, abs=2.0e-11,
    )
    assert observed.configurational_tensor_pa[0][0] == pytest.approx(
        -independent_stress * STRESS_TO_PA, rel=0.0, abs=20.0,
    )


def test_signed_pressure_remains_outside_nonnegative_source_coordinate(com_result):
    assert com_result.signed_mean_pressure_pa < 0.0
    with pytest.raises(ValueError, match="nonnegative pressure"):
        com_result.frame_thermodynamics.to_state_coordinates()


def test_frame_selection_changes_temperature_dof_without_changing_pressure(com_result, lab_result):
    assert com_result.density_trace == lab_result.density_trace
    assert com_result.stress_results == lab_result.stress_results
    assert com_result.mean_kinetic_temperature_k == pytest.approx(
        lab_result.mean_kinetic_temperature_k * 21 / 18, rel=1e-11)
    assert com_result.signed_mean_pressure_pa == pytest.approx(lab_result.signed_mean_pressure_pa, rel=1e-11)
    for com, laboratory in zip(com_result.pressure_trace.samples, lab_result.pressure_trace.samples, strict=True):
        for row_com, row_lab in zip(com.kinetic_tensor_pa, laboratory.kinetic_tensor_pa, strict=True):
            assert row_com == pytest.approx(row_lab, rel=1e-11, abs=1e-7)


def test_selected_sampling_skips_unsampled_mechanical_states(md_run, model, com_result):
    selected = _observe(md_run, model, first_state_index=1, stride=2)
    assert selected.density_trace.sample_count == 1
    assert len(selected.stress_results) == len(selected.pressure_trace.samples) == 1
    assert selected.density_trace.samples[0].state_index == 1
    assert selected.stress_results[0].reference == md_run.evaluations[1]
    assert selected.density_trace.samples[0].md_time == pytest.approx(DT)
    assert selected.mean_density_kg_m3 == pytest.approx(com_result.mean_density_kg_m3)


def test_lab_frame_uniform_boost_adds_expected_kinetic_pressure(model):
    boost = (0.015, -0.025, 0.035)
    shifted = tuple(tuple(v[a] + boost[a] for a in range(3)) for v in VELOCITIES)
    run = _run(model, velocities=shifted, steps=1)
    lab = _observe(run, model, frame=FLiBeVelocityFrame.LABORATORY, stride=2)
    com = _observe(run, model, frame=FLiBeVelocityFrame.CENTER_OF_MASS, stride=2)
    baseline = _initial()
    origin, reference_twice, _ = _kinetic_reference(baseline, frame=FLiBeVelocityFrame.LABORATORY)
    expected_increment = fsum(MASSES) * MASS_KG * (BOHR_M/TIME_S)**2 * fsum(x*x for x in boost)
    assert origin == pytest.approx((0.0, 0.0, 0.0), abs=1e-16)
    lab_twice = 2*lab.frame_thermodynamics.samples[0].kinetic_energy_j
    com_twice = 2*com.frame_thermodynamics.samples[0].kinetic_energy_j
    assert lab_twice - reference_twice == pytest.approx(expected_increment, rel=1e-12)
    assert com_twice == pytest.approx(reference_twice, rel=1e-12)
    assert lab.pressure_trace.samples[0].scalar_pressure_pa - com.pressure_trace.samples[0].scalar_pressure_pa == pytest.approx(
        expected_increment/(3*CELL_VOLUME_M3), rel=1e-9)
    assert com.frame_thermodynamics.samples[0].velocity_origin_m_s == pytest.approx(
        tuple(v * BOHR_M/TIME_S for v in boost), rel=1e-12)


def test_direct_density_operator_agrees_with_integrated_observables(md_run, com_result):
    independent = evaluate_flibe_trajectory_density(
        md_run.trajectory, md_run.mass_parameters,
        model_id=MODEL_ID, trajectory_id=TRAJECTORY_ID,
        provenance=PROVENANCE, mass_unit_to_kg=MASS_KG,
        coordinate_unit_to_meter=BOHR_M, first_state_index=0, stride=2)
    assert independent == com_result.density_trace


def test_all_frame_selection_has_one_stress_per_saved_md_state(md_run, model):
    observation = _observe(md_run, model, stride=1)
    assert tuple(sample.state_index for sample in observation.density_trace.samples) == (0, 1, 2)
    assert len(observation.stress_results) == len(observation.pressure_trace.samples) == 3
    assert len(observation.frame_thermodynamics.samples) == 3
    for sample, state in zip(observation.pressure_trace.samples, md_run.trajectory.states, strict=True):
        assert sample.md_step == state.step
        assert sample.md_time == state.time


def test_deterministic_replay_and_frozen_provenance(md_run, model, com_result):
    repeated = _observe(md_run, model)
    assert repeated == com_result
    assert com_result.stress_method_id == STRESS_METHOD
    assert com_result.source_id == SOURCE_ID
    assert com_result.differentiation.step == STRAIN_STEP
    with pytest.raises(FrozenInstanceError):
        com_result.source_id = "CHANGED"  # type: ignore[misc]


@pytest.mark.parametrize("field,invalid,error", (
    ("trajectory_id", "", ValueError),
    ("trajectory_id", " spaced ", ValueError),
    ("physical_state_id", " ", ValueError),
    ("physical_state_method_id", None, TypeError),
    ("stress_method_id", "", ValueError),
    ("source_id", "invalid ", ValueError),
    ("provenance", "TEST_FIXTURE", TypeError),
    ("velocity_frame", "CENTER_OF_MASS", TypeError),
    ("degrees_of_freedom", 19, ValueError),
    ("degrees_of_freedom", True, ValueError),
    ("first_state_index", -1, ValueError),
    ("stride", 0, ValueError),
))
def test_invalid_selection_identifiers_and_frame_contracts_rejected(md_run, model, field, invalid, error):
    with pytest.raises(error):
        _observe(md_run, model, **{field: invalid})


def test_invalid_md_run_model_and_differentiation_types(md_run, model):
    diff = CellStrainDifferentiation(step=STRAIN_STEP)
    arguments = dict(
        trajectory_id=TRAJECTORY_ID,
        velocity_frame=FLiBeVelocityFrame.CENTER_OF_MASS,
        degrees_of_freedom=18,
        physical_state_id="liquid",
        physical_state_method_id="DECLARED-FIXTURE-STATE",
        stress_method_id=STRESS_METHOD,
        source_id=SOURCE_ID,
        provenance=PROVENANCE,
    )
    with pytest.raises(TypeError, match="md_run must be"):
        evaluate_flibe_periodic_md_observables(None, model, diff, **arguments)
    with pytest.raises(TypeError, match="model must be"):
        evaluate_flibe_periodic_md_observables(md_run, None, diff, **arguments)
    with pytest.raises(TypeError, match="differentiation must be"):
        evaluate_flibe_periodic_md_observables(md_run, model, None, **arguments)


def test_model_identity_and_source_fingerprint_mismatches_rejected(md_run, model):
    with pytest.raises(ValueError, match="model identifiers must agree"):
        _observe(md_run, replace(model, model_id="DIFFERENT-MODEL"))
    old = model.polarization_model.parameters
    changed = replace(old, source_file_sha256="0" * 64)
    altered_fixed = replace(model.fixed_charge_model,
        short_range_model=replace(model.fixed_charge_model.short_range_model, parameters=changed))
    altered_model = replace(model, fixed_charge_model=altered_fixed,
                            polarization_model=replace(model.polarization_model, parameters=changed))
    with pytest.raises(ValueError, match="source fingerprint must match"):
        _observe(md_run, altered_model)


def test_result_rejects_misaligned_stress_sample_and_provenance(com_result):
    with pytest.raises(ValueError, match="relaxed stress count must match"):
        replace(com_result, stress_results=com_result.stress_results[:1])
    with pytest.raises(TypeError, match="stress_results must contain"):
        replace(com_result, stress_results=(object(), com_result.stress_results[1]))
    with pytest.raises(ValueError, match="relaxed stress must use the selected MD configuration"):
        replace(com_result, stress_results=tuple(reversed(com_result.stress_results)))
    with pytest.raises(ValueError, match="density and observables provenance"):
        replace(com_result, provenance=ParameterProvenance.PRIMARY_SOURCE)
    with pytest.raises(ValueError, match="pressure provenance identifiers"):
        replace(com_result, source_id="DIFFERENT-SOURCE")
    with pytest.raises(ValueError, match="all stress samples must use"):
        replace(com_result, differentiation=CellStrainDifferentiation(step=0.5*STRAIN_STEP))


def test_result_detects_modified_signed_configurational_pressure(com_result):
    pressure = com_result.pressure_trace
    first = pressure.samples[0]
    matrix = tuple(tuple(first.configurational_tensor_pa[a][b] + (1000.0 if a == b == 0 else 0.0)
                         for b in range(3)) for a in range(3))
    changed_first = replace(first, configurational_tensor_pa=matrix)
    changed_pressure = replace(pressure, samples=(changed_first, *pressure.samples[1:]))
    changed_thermal = replace(com_result.frame_thermodynamics, pressure_trace=changed_pressure)
    with pytest.raises(ValueError, match="configurational pressure must equal minus"):
        replace(com_result, pressure_trace=changed_pressure,
                frame_thermodynamics=changed_thermal)


def test_result_rejects_inconsistent_stress_conversion(com_result):
    pressure = com_result.pressure_trace
    changed_pressure = replace(pressure, potential_stress_unit_to_pascal=1.01 * pressure.potential_stress_unit_to_pascal)
    thermal = replace(com_result.frame_thermodynamics, pressure_trace=changed_pressure)
    with pytest.raises(ValueError, match="potential stress SI conversion"):
        replace(com_result, pressure_trace=changed_pressure, frame_thermodynamics=thermal)
