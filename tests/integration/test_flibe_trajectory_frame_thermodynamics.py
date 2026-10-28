"""Independent frame-resolved FLiBe kinetic-temperature and pressure contracts."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import fsum

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState, StressState
from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.mass import FLiBeMassParameters
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.trajectory_density import evaluate_flibe_trajectory_density
from tr_eif.flibe.trajectory_frame_thermodynamics import (
    evaluate_flibe_frame_thermodynamics,
)
from tr_eif.flibe.trajectory_pressure import (
    FLiBePotentialStressSample,
    FLiBeVelocityFrame,
    evaluate_flibe_trajectory_pressure,
)
from tr_eif.flibe.trajectory_state_correspondence import (
    BOLTZMANN_CONSTANT_J_PER_K,
    FLiBeDensitySourceCoordinates,
    FLiBePressureRole,
    compare_flibe_density_state_coordinates,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import InteractionGraph
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory


SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASSES = (2.0, 2.0, 3.0, 5.0, 5.0, 5.0, 5.0)
POSITIONS = (
    (0.1, 0.1, 0.1), (0.6, 0.1, 0.1), (0.2, 0.6, 0.2),
    (0.3, 0.3, 0.7), (0.8, 0.3, 0.7), (0.4, 0.9, 1.1),
    (0.9, 0.7, 1.3),
)
VELOCITIES = (
    (1.0, 2.0, 0.0), (-1.0, -2.0, 0.0), (0.0, 1.0, 0.0),
    (0.0, -0.6, 0.0), (0.0, 0.0, 2.0), (0.0, 0.0, -2.0),
    (0.0, 0.0, 0.0),
)
STRESS = ((1.5, 0.25, 0.0), (0.25, -0.5, 0.0), (0.0, 0.0, 2.0))
MASS_UNIT_KG = 1.0e-27
LENGTH_UNIT_M = 1.0e-10
TIME_UNIT_S = 1.0e-12
STRESS_UNIT_PA = 1.0e5
VELOCITY_UNIT_M_S = LENGTH_UNIT_M / TIME_UNIT_S
ENERGY_UNIT_J = MASS_UNIT_KG * VELOCITY_UNIT_M_S**2
MOMENT_TRACE = 64.8
TOTAL_MASS = 27.0
COM_DOF = 18
LAB_DOF = 21
PROVENANCE = ParameterProvenance.TEST_FIXTURE


def _cell(index: int):
    return ((2.0 * (index + 1), 0.0, 0.0), (0.0, 3.0, 0.0), (0.0, 0.0, 4.0))


def _state(index: int, *, velocities=VELOCITIES, periodic=(True, True, True)):
    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=SPECIES, positions=POSITIONS, cell=_cell(index), periodic=periodic,
        ),
        velocities=velocities, masses=MASSES, step=index, time=0.25 * index,
    )


def _trajectory(states=None):
    ordered = tuple(_state(i) for i in range(3)) if states is None else states
    graph = InteractionGraph(node_count=len(SPECIES), edges=())
    forces = ForceState(forces=((0.0, 0.0, 0.0),) * len(SPECIES))
    return MolecularDynamicsTrajectory(steps=tuple(
        MolecularDynamicsStepResult(
            previous=previous, current=current,
            graph_before=graph, graph_after=graph,
            forces_before=forces, forces_after=forces,
        )
        for previous, current in zip(ordered[:-1], ordered[1:], strict=True)
    ))


def _density(trajectory, *, first_state_index=0, stride=1):
    return evaluate_flibe_trajectory_density(
        trajectory,
        FLiBeMassParameters(lithium=2.0, beryllium=3.0, fluorine=5.0),
        model_id="TR-EIP-FRAME-ANALYTIC-FIXTURE",
        trajectory_id="FLIBE-FRAME-TRAJECTORY-001",
        provenance=PROVENANCE,
        mass_unit_to_kg=MASS_UNIT_KG,
        coordinate_unit_to_meter=LENGTH_UNIT_M,
        first_state_index=first_state_index,
        stride=stride,
    )


def _pressure(trajectory, density, *, frame=FLiBeVelocityFrame.CENTER_OF_MASS,
              stress=STRESS, time_unit_to_second=TIME_UNIT_S):
    stress_samples = tuple(
        FLiBePotentialStressSample(
            state_index=sample.state_index,
            md_step=sample.md_step,
            md_time=sample.md_time,
            stress=StressState(tensor=stress),
        ) for sample in density.samples
    )
    return evaluate_flibe_trajectory_pressure(
        trajectory, density, stress_samples,
        time_unit_to_second=time_unit_to_second,
        potential_stress_unit_to_pascal=STRESS_UNIT_PA,
        velocity_frame=frame,
        stress_method_id="ENERGY-STRAIN-ANALYTIC-FIXTURE",
        source_id="FLIBE-FRAME-PRESSURE-FIXTURE",
        provenance=PROVENANCE,
    )


def _thermal(*, trajectory=None, pressure=None, frame=FLiBeVelocityFrame.CENTER_OF_MASS,
             degrees_of_freedom=None, stride=1, time_unit_to_second=TIME_UNIT_S):
    current = _trajectory() if trajectory is None else trajectory
    result = pressure
    if result is None:
        density = _density(current, stride=stride)
        result = _pressure(current, density, frame=frame, time_unit_to_second=time_unit_to_second)
    if degrees_of_freedom is None:
        degrees_of_freedom = COM_DOF if result.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS else LAB_DOF
    return evaluate_flibe_frame_thermodynamics(
        current, result,
        degrees_of_freedom=degrees_of_freedom,
        physical_state_id="liquid",
        physical_state_method_id="DECLARED-FIXTURE-STATE",
    )


def _boosted(boost):
    velocities = tuple(tuple(v[a] + boost[a] for a in range(3)) for v in VELOCITIES)
    return _trajectory(tuple(_state(i, velocities=velocities) for i in range(3)))


def _assert_samples_equal(left, right):
    for a, b in zip(left.samples, right.samples, strict=True):
        assert a.kinetic_energy_j == pytest.approx(b.kinetic_energy_j, rel=1e-12)
        assert a.kinetic_temperature_k == pytest.approx(b.kinetic_temperature_k, rel=1e-12)
        assert a.kinetic_pressure_pa == pytest.approx(b.kinetic_pressure_pa, rel=1e-12)


def test_independent_kinetic_energy_temperature_and_pressure_per_frame() -> None:
    result = _thermal()
    assert result.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
    assert result.degrees_of_freedom == COM_DOF
    assert len(result.samples) == 3
    assert result.pressure_trace.density_trace.total_mass_kg == pytest.approx(27.0e-27)
    energy = 0.5 * MOMENT_TRACE * ENERGY_UNIT_J
    temperature = MOMENT_TRACE * ENERGY_UNIT_J / (COM_DOF * BOLTZMANN_CONSTANT_J_PER_K)
    for index, sample in enumerate(result.samples):
        volume_m3 = 24.0 * (index + 1) * LENGTH_UNIT_M**3
        expected_kinetic_pressure = MOMENT_TRACE * ENERGY_UNIT_J / (3.0 * volume_m3)
        assert sample.state_index == sample.md_step == index
        assert sample.md_time == pytest.approx(0.25 * index)
        assert sample.velocity_origin_m_s == pytest.approx((0.0, 0.0, 0.0), abs=1e-12)
        assert sample.kinetic_energy_j == pytest.approx(energy, rel=1e-13)
        assert sample.kinetic_temperature_k == pytest.approx(temperature, rel=1e-13)
        assert sample.kinetic_pressure_pa == pytest.approx(expected_kinetic_pressure, rel=1e-13)
        pressure = result.pressure_trace.samples[index]
        assert sample.kinetic_pressure_pa == pytest.approx(
            sum(pressure.kinetic_tensor_pa[i][i] for i in range(3)) / 3.0, rel=1e-13,
        )
    assert result.mean_kinetic_temperature_k == pytest.approx(temperature)


def test_lab_and_center_of_mass_degree_count_remain_distinct() -> None:
    com = _thermal()
    lab = _thermal(frame=FLiBeVelocityFrame.LABORATORY)
    assert lab.degrees_of_freedom == LAB_DOF
    assert lab.velocity_frame is FLiBeVelocityFrame.LABORATORY
    for com_sample, lab_sample in zip(com.samples, lab.samples, strict=True):
        assert com_sample.kinetic_energy_j == pytest.approx(lab_sample.kinetic_energy_j)
        assert lab_sample.kinetic_temperature_k == pytest.approx(
            com_sample.kinetic_temperature_k * COM_DOF / LAB_DOF,
        )
        assert lab_sample.kinetic_pressure_pa == pytest.approx(com_sample.kinetic_pressure_pa)
        assert lab_sample.velocity_origin_m_s == (0.0, 0.0, 0.0)


def test_uniform_velocity_boost_is_removed_in_center_of_mass_frame() -> None:
    boost = (3.0, -4.0, 7.0)
    baseline = _thermal()
    shifted = _thermal(trajectory=_boosted(boost))
    _assert_samples_equal(shifted, baseline)
    for sample in shifted.samples:
        assert sample.velocity_origin_m_s == pytest.approx(tuple(x * VELOCITY_UNIT_M_S for x in boost))
    assert shifted.pressure_trace.mean_pressure_pa == pytest.approx(
        baseline.pressure_trace.mean_pressure_pa
    )


def test_lab_frame_boost_preserves_the_full_kinetic_increment() -> None:
    boost = (3.0, -4.0, 7.0)
    baseline = _thermal(frame=FLiBeVelocityFrame.LABORATORY)
    shifted = _thermal(trajectory=_boosted(boost), frame=FLiBeVelocityFrame.LABORATORY)
    extra_twice_energy = TOTAL_MASS * sum(component**2 for component in boost) * ENERGY_UNIT_J
    for index, (before, after) in enumerate(zip(baseline.samples, shifted.samples, strict=True)):
        volume = 24.0 * (index + 1) * LENGTH_UNIT_M**3
        assert after.velocity_origin_m_s == (0.0, 0.0, 0.0)
        assert after.kinetic_energy_j - before.kinetic_energy_j == pytest.approx(
            extra_twice_energy / 2.0, rel=1e-12,
        )
        assert after.kinetic_temperature_k - before.kinetic_temperature_k == pytest.approx(
            extra_twice_energy / (LAB_DOF * BOLTZMANN_CONSTANT_J_PER_K), rel=1e-12,
        )
        assert after.kinetic_pressure_pa - before.kinetic_pressure_pa == pytest.approx(
            extra_twice_energy / (3.0 * volume), rel=1e-12,
        )


def test_selected_frames_preserve_indices_and_mean_temperature() -> None:
    result = _thermal(stride=2)
    assert len(result.samples) == 2
    assert tuple(sample.state_index for sample in result.samples) == (0, 2)
    assert tuple(sample.md_step for sample in result.samples) == (0, 2)
    assert tuple(sample.md_time for sample in result.samples) == (0.0, 0.5)
    assert result.mean_kinetic_temperature_k == pytest.approx(
        fsum(s.kinetic_temperature_k for s in result.samples) / 2.0
    )
    assert result.pressure_trace.density_trace.sample_count == 2


def test_explicit_si_time_factor_scales_temperature_and_kinetic_pressure() -> None:
    first = _thermal()
    twice_time = _thermal(time_unit_to_second=2.0 * TIME_UNIT_S)
    for before, after in zip(first.samples, twice_time.samples, strict=True):
        assert after.kinetic_energy_j == pytest.approx(before.kinetic_energy_j / 4.0)
        assert after.kinetic_temperature_k == pytest.approx(before.kinetic_temperature_k / 4.0)
        assert after.kinetic_pressure_pa == pytest.approx(before.kinetic_pressure_pa / 4.0)
        assert after.velocity_origin_m_s == pytest.approx(tuple(v / 2.0 for v in before.velocity_origin_m_s))


def test_declared_degrees_of_freedom_change_temperature_only() -> None:
    initial = _thermal(degrees_of_freedom=18)
    selected = _thermal(degrees_of_freedom=15)
    assert selected.degrees_of_freedom == 15
    for before, after in zip(initial.samples, selected.samples, strict=True):
        assert after.kinetic_energy_j == pytest.approx(before.kinetic_energy_j)
        assert after.kinetic_temperature_k == pytest.approx(before.kinetic_temperature_k * 18.0 / 15.0)
        assert after.kinetic_pressure_pa == pytest.approx(before.kinetic_pressure_pa)


def test_zero_velocities_preserve_zero_kinetic_temperature() -> None:
    zero = ((0.0, 0.0, 0.0),) * len(SPECIES)
    trajectory = _trajectory(tuple(_state(i, velocities=zero) for i in range(3)))
    result = _thermal(trajectory=trajectory)
    assert result.mean_kinetic_temperature_k == 0.0
    assert all(sample.kinetic_energy_j == 0.0 for sample in result.samples)
    assert all(sample.kinetic_pressure_pa == 0.0 for sample in result.samples)
    assert result.pressure_trace.mean_pressure_pa == pytest.approx(-1.0e5)
    with pytest.raises(ValueError, match="nonnegative pressure"):
        result.to_state_coordinates()


def test_derived_pressure_and_temperature_feed_typed_state_comparison() -> None:
    result = _thermal()
    state = result.to_state_coordinates()
    assert state.density_trace == result.pressure_trace.density_trace
    assert state.kinetic_temperature_k == tuple(s.kinetic_temperature_k for s in result.samples)
    assert state.degrees_of_freedom == COM_DOF
    assert state.pressure is not None
    assert state.pressure.role is FLiBePressureRole.OBSERVED
    assert state.pressure.pressure_pa == pytest.approx(result.pressure_trace.mean_pressure_pa)
    assert state.pressure.source_id == "FLIBE-FRAME-PRESSURE-FIXTURE"
    source = FLiBeDensitySourceCoordinates(
        density_kg_m3=690.0,
        composition=FLiBeComposition(2.0, 1.0),
        temperature_k=result.mean_kinetic_temperature_k,
        pressure_pa=result.pressure_trace.mean_pressure_pa,
        physical_state_id="liquid",
        normalization_id="source-reported-mass-density",
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        source_id="SYNTHETIC-FRAME-DENSITY",
        method_id="INDEPENDENT-ANALYTIC-FIXTURE",
        provenance=PROVENANCE,
    )
    comparison = compare_flibe_density_state_coordinates(
        state, source,
        temperature_tolerance_k=1.0e-10,
        pressure_tolerance_pa=1.0e-6,
        normalization_id="source-reported-mass-density",
    )
    assert comparison.coordinate_match
    assert comparison.density_residual_kg_m3 == pytest.approx(
        (1125.0 + 562.5 + 375.0) / 3.0 - 690.0,
    )
    assert not compare_flibe_density_state_coordinates(
        state, replace(source, pressure_pa=source.pressure_pa + 1000.0),
        temperature_tolerance_k=1.0e-10,
        pressure_tolerance_pa=1.0e-6,
        normalization_id="source-reported-mass-density",
    ).coordinate_match


def test_temperature_and_pressure_tensor_detect_cross_frame_mixing() -> None:
    original = _trajectory()
    pressure_com = _pressure(original, _density(original), frame=FLiBeVelocityFrame.CENTER_OF_MASS)
    shifted = _boosted((3.0, -4.0, 7.0))
    with pytest.raises(ValueError, match="kinetic pressure tensor and velocity frame differ"):
        _thermal(trajectory=shifted, pressure=replace(pressure_com, velocity_frame=FLiBeVelocityFrame.LABORATORY), degrees_of_freedom=LAB_DOF)
    pressure_shifted = _pressure(shifted, _density(shifted), frame=FLiBeVelocityFrame.LABORATORY)
    with pytest.raises(ValueError, match="kinetic pressure tensor and velocity frame differ"):
        _thermal(trajectory=original, pressure=pressure_shifted, degrees_of_freedom=LAB_DOF)


def test_rotation_preserves_thermal_scalar_in_both_frames() -> None:
    def rotate(v):
        return (-v[1], v[0], v[2])

    rotated = _trajectory(tuple(_state(i, velocities=tuple(rotate(v) for v in VELOCITIES)) for i in range(3)))
    for frame, dof in ((FLiBeVelocityFrame.CENTER_OF_MASS, COM_DOF), (FLiBeVelocityFrame.LABORATORY, LAB_DOF)):
        reference = _thermal(frame=frame, degrees_of_freedom=dof)
        transformed = _thermal(trajectory=rotated, frame=frame, degrees_of_freedom=dof)
        _assert_samples_equal(reference, transformed)


def test_repeated_evaluation_and_immutable_records() -> None:
    first = _thermal()
    second = _thermal()
    assert first == second
    assert first.physical_state_id == "liquid"
    assert first.physical_state_method_id == "DECLARED-FIXTURE-STATE"
    with pytest.raises(FrozenInstanceError):
        first.physical_state_id = "solid"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        first.samples[0].kinetic_temperature_k = 0.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("degrees", "frame"),
    ((0, FLiBeVelocityFrame.CENTER_OF_MASS),
     (-1, FLiBeVelocityFrame.CENTER_OF_MASS),
     (True, FLiBeVelocityFrame.CENTER_OF_MASS),
     (18.0, FLiBeVelocityFrame.CENTER_OF_MASS),
     (19, FLiBeVelocityFrame.CENTER_OF_MASS),
     (21, FLiBeVelocityFrame.CENTER_OF_MASS),
     (22, FLiBeVelocityFrame.LABORATORY)),
)
def test_invalid_frame_degrees_of_freedom_rejected(degrees, frame) -> None:
    with pytest.raises(ValueError, match="degrees_of_freedom must fit"):
        _thermal(frame=frame, degrees_of_freedom=degrees)


@pytest.mark.parametrize(
    ("field", "invalid", "error"),
    (("physical_state_id", "liquid ", ValueError),
     ("physical_state_id", "", ValueError),
     ("physical_state_id", None, TypeError),
     ("physical_state_method_id", " ", ValueError),
     ("physical_state_method_id", False, TypeError)),
)
def test_invalid_metadata_rejected(field, invalid, error) -> None:
    trajectory = _trajectory()
    pressure = _pressure(trajectory, _density(trajectory))
    arguments = dict(degrees_of_freedom=COM_DOF, physical_state_id="liquid",
                     physical_state_method_id="DECLARED-FIXTURE-STATE")
    arguments[field] = invalid
    with pytest.raises(error):
        evaluate_flibe_frame_thermodynamics(trajectory, pressure, **arguments)


def test_untyped_trajectory_and_pressure_inputs_rejected() -> None:
    trajectory = _trajectory()
    pressure = _pressure(trajectory, _density(trajectory))
    with pytest.raises(TypeError, match="trajectory must be"):
        evaluate_flibe_frame_thermodynamics(None, pressure, degrees_of_freedom=COM_DOF,
            physical_state_id="liquid", physical_state_method_id="TEST")
    with pytest.raises(TypeError, match="pressure_trace must be"):
        evaluate_flibe_frame_thermodynamics(trajectory, None, degrees_of_freedom=COM_DOF,
            physical_state_id="liquid", physical_state_method_id="TEST")


def test_sample_records_reject_negative_nonfinite_and_malformed_values() -> None:
    sample = _thermal().samples[0]
    with pytest.raises(ValueError, match="kinetic_energy_j"):
        replace(sample, kinetic_energy_j=-1.0)
    with pytest.raises(ValueError, match="kinetic_temperature_k"):
        replace(sample, kinetic_temperature_k=float("nan"))
    with pytest.raises(ValueError, match="kinetic_pressure_pa"):
        replace(sample, kinetic_pressure_pa=float("inf"))
    with pytest.raises(ValueError, match="three components"):
        replace(sample, velocity_origin_m_s=(0.0, 0.0))
    with pytest.raises(ValueError, match="finite real components"):
        replace(sample, velocity_origin_m_s=(0.0, 0.0, float("nan")))
    with pytest.raises(ValueError, match="nonnegative integer"):
        replace(sample, state_index=-1)
    with pytest.raises(ValueError, match="nonnegative integer"):
        replace(sample, md_step=True)
    with pytest.raises(ValueError, match="md_time"):
        replace(sample, md_time=-0.1)


def test_thermal_record_constructor_checks_sample_count_and_order() -> None:
    result = _thermal()
    with pytest.raises(ValueError, match="sample counts must agree"):
        replace(result, samples=result.samples[:-1])
    with pytest.raises(ValueError, match="state identities must agree"):
        replace(result, samples=(replace(result.samples[0], md_step=3), *result.samples[1:]))
    with pytest.raises(TypeError, match="FLiBeFrameThermalSample"):
        replace(result, samples=(object(), *result.samples[1:]))
    with pytest.raises(TypeError, match="FLiBeTrajectoryPressure"):
        replace(result, pressure_trace=None)


def test_constructor_checks_energy_temperature_kinetic_pressure_relation() -> None:
    result = _thermal()
    sample = result.samples[0]
    with pytest.raises(ValueError, match="energy and temperature must agree"):
        replace(result, samples=(replace(sample, kinetic_temperature_k=1.1 * sample.kinetic_temperature_k), *result.samples[1:]))
    with pytest.raises(ValueError, match="energy and kinetic pressure must agree"):
        replace(result, samples=(replace(sample, kinetic_pressure_pa=1.1 * sample.kinetic_pressure_pa), *result.samples[1:]))
    with pytest.raises(ValueError, match="thermal sample and pressure tensor trace must agree"):
        # Divide energy, temperature, and kinetic pressure consistently, but
        # leave the independently supplied pressure tensor unchanged.
        scaled = replace(sample,
            kinetic_energy_j=0.5 * sample.kinetic_energy_j,
            kinetic_temperature_k=0.5 * sample.kinetic_temperature_k,
            kinetic_pressure_pa=0.5 * sample.kinetic_pressure_pa,
        )
        replace(result, samples=(scaled, *result.samples[1:]))


def test_mismatched_density_volume_and_stale_sample_indices_rejected() -> None:
    trajectory = _trajectory()
    density = _density(trajectory)
    pressure = _pressure(trajectory, density)
    altered_density = replace(density, samples=(
        replace(density.samples[0], cell_volume_m3=1.5 * density.samples[0].cell_volume_m3),
        *density.samples[1:],
    ))
    changed_pressure = replace(pressure, density_trace=altered_density, samples=(
        replace(pressure.samples[0], cell_volume_m3=altered_density.samples[0].cell_volume_m3),
        *pressure.samples[1:],
    ))
    with pytest.raises(ValueError, match="thermal and density cell volumes must agree"):
        _thermal(trajectory=trajectory, pressure=changed_pressure)
    # A stale density sample index must not be used to access a different state.
    changed_sample = replace(density.samples[2], state_index=4)
    changed_density = replace(density, samples=(*density.samples[:2], changed_sample))
    changed_pressure = replace(pressure, density_trace=changed_density, samples=(
        *pressure.samples[:2], replace(pressure.samples[2], state_index=4),
    ))
    with pytest.raises(ValueError, match="sample index exceeds trajectory length"):
        _thermal(trajectory=trajectory, pressure=changed_pressure)


def test_thermal_state_detects_mismatched_species_and_atomic_masses() -> None:
    base = _trajectory()
    pressure = _pressure(base, _density(base))
    states = tuple(_state(i) for i in range(3))
    swapped = replace(states[2], configuration=replace(states[2].configuration,
        species=("Be", "Li", "Li", "F", "F", "F", "F")))
    with pytest.raises(ValueError, match="ordered species and atomic masses"):
        _thermal(trajectory=_trajectory(states[:2] + (swapped,)), pressure=pressure)
    changed = replace(states[2], masses=MASSES[:-1] + (6.0,))
    with pytest.raises(ValueError, match="ordered species and atomic masses"):
        _thermal(trajectory=_trajectory(states[:2] + (changed,)), pressure=pressure)
    partial = replace(states[2], configuration=replace(states[2].configuration, periodic=(True, False, True)))
    with pytest.raises(ValueError, match="three periodic cell axes"):
        _thermal(trajectory=_trajectory(states[:2] + (partial,)), pressure=pressure)


def test_energy_and_pressure_tensor_mismatch_is_detected() -> None:
    trajectory = _trajectory()
    pressure = _pressure(trajectory, _density(trajectory))
    sample = pressure.samples[0]
    # Alter off-diagonal kinetic momentum flux without changing scalar trace.
    bad_kinetic = (
        (sample.kinetic_tensor_pa[0][0], sample.kinetic_tensor_pa[0][1] + 100000.0, sample.kinetic_tensor_pa[0][2]),
        sample.kinetic_tensor_pa[1], sample.kinetic_tensor_pa[2],
    )
    changed = replace(pressure, samples=(replace(sample, kinetic_tensor_pa=bad_kinetic), *pressure.samples[1:]))
    with pytest.raises(ValueError, match="kinetic pressure tensor and velocity frame differ"):
        _thermal(trajectory=trajectory, pressure=changed)
