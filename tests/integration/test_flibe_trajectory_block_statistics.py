"""Independent integration tests for aligned FLiBe MD block statistics.

Build thermodynamically consistent density, kinetic-temperature and signed
pressure records, then independently reconstruct the complete-block means,
sample standard deviations, block standard errors, half-window differences
and adjacent-block correlations. Exercise discarded samples, time alignment,
physical units, provenance, and damaged-record rejection.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from math import isfinite, sqrt
from statistics import mean, stdev

import pytest

from tr_eif.flibe.composition import FLiBeComposition
from tr_eif.flibe.trajectory_block_statistics import (
    FLiBeBlockObservable,
    FLiBeThermodynamicBlock,
    FLiBeTrajectoryBlockStatistics,
    evaluate_flibe_trajectory_block_statistics,
)
from tr_eif.flibe.trajectory_density import FLiBeDensitySample, FLiBeTrajectoryDensity
from tr_eif.flibe.trajectory_frame_thermodynamics import (
    FLiBeFrameThermalSample,
    FLiBeFrameThermodynamicState,
)
from tr_eif.flibe.trajectory_pressure import (
    FLiBePressureSample,
    FLiBeTrajectoryPressure,
    FLiBeVelocityFrame,
)
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance


TEMPERATURES_K = (790.0, 830.0, 825.0, 875.0, 860.0, 910.0, 905.0, 955.0, 950.0, 990.0)
PRESSURES_PA = (-150000.0, -110000.0, -90000.0, -60000.0, -25000.0,
                10000.0, 35000.0, 60000.0, 85000.0, 120000.0)
DENSITIES_KG_M3 = (1890.0, 1940.0, 2010.0, 1970.0, 2040.0,
                   1990.0, 2070.0, 2020.0, 2110.0, 2060.0)
TOTAL_MASS_KG = 7.0e-26
TIME_UNIT_TO_S = 1.0e-12
TIME_INCREMENT_CODE = 0.25
DEGREES_OF_FREEDOM = 18
PROVENANCE = ParameterProvenance.TEST_FIXTURE
MODEL_ID = "FLIBE-BLOCK-STATISTICS-REFERENCE"
TRAJECTORY_ID = "FLIBE-THERMODYNAMIC-BLOCK-REFERENCE"


def _diagonal(value: float):
    return ((value, 0.0, 0.0), (0.0, value, 0.0), (0.0, 0.0, value))


def _build_trace(
    temperatures=TEMPERATURES_K,
    pressures=PRESSURES_PA,
    densities=DENSITIES_KG_M3,
    *,
    frame=FLiBeVelocityFrame.CENTER_OF_MASS,
) -> FLiBeFrameThermodynamicState:
    assert len(temperatures) == len(pressures) == len(densities)
    dof = DEGREES_OF_FREEDOM if frame is FLiBeVelocityFrame.CENTER_OF_MASS else 21
    density_samples = []
    pressure_samples = []
    thermal_samples = []

    for index, (temperature, signed_pressure, density) in enumerate(
        zip(temperatures, pressures, densities, strict=True)
    ):
        volume = TOTAL_MASS_KG / density
        kinetic_energy = 0.5 * dof * BOLTZMANN_CONSTANT_J_PER_K * temperature
        kinetic_pressure = 2.0 * kinetic_energy / (3.0 * volume)
        time_code = index * TIME_INCREMENT_CODE
        step = 2 * index
        density_samples.append(FLiBeDensitySample(
            state_index=index, md_step=step, md_time=time_code,
            cell_volume_m3=volume, density_kg_m3=density,
        ))
        pressure_samples.append(FLiBePressureSample(
            state_index=index, md_step=step, md_time=time_code,
            cell_volume_m3=volume,
            kinetic_tensor_pa=_diagonal(kinetic_pressure),
            configurational_tensor_pa=_diagonal(signed_pressure - kinetic_pressure),
            pressure_tensor_pa=_diagonal(signed_pressure),
            scalar_pressure_pa=signed_pressure,
        ))
        thermal_samples.append(FLiBeFrameThermalSample(
            state_index=index, md_step=step, md_time=time_code,
            velocity_origin_m_s=(0.0, 0.0, 0.0),
            kinetic_energy_j=kinetic_energy,
            kinetic_temperature_k=temperature,
            kinetic_pressure_pa=kinetic_pressure,
        ))

    density_trace = FLiBeTrajectoryDensity(
        model_id=MODEL_ID, trajectory_id=TRAJECTORY_ID,
        provenance=PROVENANCE,
        composition=FLiBeComposition(2.0, 1.0), atom_count=7,
        total_mass_kg=TOTAL_MASS_KG,
        mass_unit_to_kg=1.0e-27, coordinate_unit_to_meter=1.0e-10,
        samples=tuple(density_samples),
    )
    pressure_trace = FLiBeTrajectoryPressure(
        density_trace=density_trace, velocity_frame=frame,
        time_unit_to_second=TIME_UNIT_TO_S, potential_stress_unit_to_pascal=1.0e5,
        stress_method_id="ENERGY-STRAIN-REFERENCE",
        source_id="SIGNED-PRESSURE-REFERENCE",
        provenance=PROVENANCE, samples=tuple(pressure_samples),
    )
    return FLiBeFrameThermodynamicState(
        pressure_trace=pressure_trace, degrees_of_freedom=dof,
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED-REFERENCE-STATE",
        samples=tuple(thermal_samples),
    )


def _statistics(values: tuple[float, ...], block_size: int):
    """Numerical reference based on Python's independent statistics functions."""
    blocks = tuple(
        tuple(values[start:start + block_size])
        for start in range(0, len(values), block_size)
    )
    block_means = tuple(mean(block) for block in blocks)
    midpoint = len(block_means) // 2
    left, right = block_means[:-1], block_means[1:]
    if len(block_means) < 3 or stdev(left) == 0.0 or stdev(right) == 0.0:
        correlation = None
    else:
        covariance = sum((a - mean(left)) * (b - mean(right))
                         for a, b in zip(left, right, strict=True))
        variation = sqrt(
            sum((a - mean(left)) ** 2 for a in left)
            * sum((b - mean(right)) ** 2 for b in right)
        )
        correlation = covariance / variation
    return {
        "mean": mean(values),
        "sample_standard_deviation": stdev(values),
        "block_means": block_means,
        "block_mean_standard_error": stdev(block_means) / sqrt(len(block_means)),
        "second_half_minus_first_half": (
            mean(block_means[midpoint:]) - mean(block_means[:midpoint])
        ),
        "lag_one_block_correlation": correlation,
    }


def _assert_independent_observable(actual: FLiBeBlockObservable,
                                   selected: tuple[float, ...], block_size: int,
                                   expected_unit: str):
    expected = _statistics(selected, block_size)
    assert actual.unit == expected_unit
    assert actual.mean == pytest.approx(expected["mean"], rel=1.0e-12, abs=1.0e-12)
    assert actual.sample_standard_deviation == pytest.approx(
        expected["sample_standard_deviation"], rel=1.0e-12, abs=1.0e-12
    )
    assert actual.block_means == pytest.approx(expected["block_means"], rel=1.0e-12)
    assert actual.block_mean_standard_error == pytest.approx(
        expected["block_mean_standard_error"], rel=1.0e-12, abs=1.0e-12
    )
    assert actual.second_half_minus_first_half == pytest.approx(
        expected["second_half_minus_first_half"], rel=1.0e-12, abs=1.0e-12
    )
    correlation = expected["lag_one_block_correlation"]
    if correlation is None:
        assert actual.lag_one_block_correlation is None
    else:
        assert actual.lag_one_block_correlation == pytest.approx(
            correlation, rel=1.0e-12, abs=1.0e-12
        )


@pytest.fixture(scope="module")
def trace():
    return _build_trace()


@pytest.mark.parametrize("size,discard,allow_tail", (
    (2, 0, False), (2, 1, True), (2, 2, False), (2, 3, True),
    (2, 4, False), (2, 5, True), (3, 0, True), (3, 1, False),
    (3, 2, True), (4, 0, True), (4, 1, True),
))
def test_independent_all_observables_and_windows(trace, size, discard, allow_tail):
    result = evaluate_flibe_trajectory_block_statistics(
        trace, block_size_samples=size, discarded_initial_samples=discard,
        discard_incomplete_tail=allow_tail,
    )
    expected_blocks, tail = divmod(len(TEMPERATURES_K) - discard, size)
    stop = discard + expected_blocks * size
    assert isinstance(result, FLiBeTrajectoryBlockStatistics)
    assert result.discarded_initial_samples == discard
    assert result.discarded_tail_samples == tail
    assert result.block_size_samples == size
    assert result.block_count == expected_blocks
    assert result.selected_sample_count == expected_blocks * size
    assert len(result.blocks) == expected_blocks
    assert result.sampling_interval_s == pytest.approx(
        TIME_INCREMENT_CODE * TIME_UNIT_TO_S, rel=1.0e-12
    )
    _assert_independent_observable(result.temperature, TEMPERATURES_K[discard:stop], size, "K")
    _assert_independent_observable(result.pressure, PRESSURES_PA[discard:stop], size, "Pa")
    _assert_independent_observable(result.density, DENSITIES_KG_M3[discard:stop], size, "kg/m^3")
    for i, block in enumerate(result.blocks):
        assert isinstance(block, FLiBeThermodynamicBlock)
        first = discard + i * size
        last = first + size - 1
        assert (block.block_index, block.first_state_index, block.last_state_index) == (i, first, last)
        assert block.first_time_s == pytest.approx(first * TIME_INCREMENT_CODE * TIME_UNIT_TO_S)
        assert block.last_time_s == pytest.approx(last * TIME_INCREMENT_CODE * TIME_UNIT_TO_S)
        assert block.mean_temperature_k == pytest.approx(mean(TEMPERATURES_K[first:last + 1]))
        assert block.mean_signed_pressure_pa == pytest.approx(mean(PRESSURES_PA[first:last + 1]))
        assert block.mean_density_kg_m3 == pytest.approx(mean(DENSITIES_KG_M3[first:last + 1]))
        assert result.temperature.block_means[i] == block.mean_temperature_k
        assert result.pressure.block_means[i] == block.mean_signed_pressure_pa
        assert result.density.block_means[i] == block.mean_density_kg_m3


def test_source_identity_velocity_frame_and_si_units(trace):
    result = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    pressure = trace.pressure_trace
    density = pressure.density_trace
    assert result.model_id == density.model_id == MODEL_ID
    assert result.trajectory_id == density.trajectory_id == TRAJECTORY_ID
    assert result.provenance is PROVENANCE
    assert result.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
    assert result.stress_method_id == pressure.stress_method_id
    assert result.pressure_source_id == pressure.source_id
    assert result.pressure_provenance is pressure.provenance is PROVENANCE
    assert result.temperature_degrees_of_freedom == DEGREES_OF_FREEDOM
    assert result.physical_state_id == trace.physical_state_id
    assert result.physical_state_method_id == trace.physical_state_method_id
    assert (result.temperature.unit, result.pressure.unit, result.density.unit) == (
        "K", "Pa", "kg/m^3"
    )
    assert any(value < 0.0 for value in result.pressure.block_means)
    assert any(value > 0.0 for value in result.pressure.block_means)
    assert all(isfinite(value) for observable in (result.temperature, result.pressure, result.density)
               for value in observable.block_means)


@pytest.mark.parametrize("frame", (
    FLiBeVelocityFrame.CENTER_OF_MASS, FLiBeVelocityFrame.LABORATORY,
))
def test_frame_identity_retained_with_independent_kinetic_contract(frame):
    trace = _build_trace(frame=frame)
    output = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    assert output.velocity_frame is frame
    assert output.temperature_degrees_of_freedom == (
        18 if frame is FLiBeVelocityFrame.CENTER_OF_MASS else 21
    )
    _assert_independent_observable(output.temperature, TEMPERATURES_K, 2, "K")
    _assert_independent_observable(output.pressure, PRESSURES_PA, 2, "Pa")


def test_constant_signed_pressure_and_zero_variance_statistics():
    thermal = _build_trace(
        temperatures=(850.0,) * 10,
        pressures=(-102000.0,) * 10,
        densities=(2000.0,) * 10,
    )
    output = evaluate_flibe_trajectory_block_statistics(thermal, block_size_samples=2)
    for series, expected in (
        (output.temperature, 850.0),
        (output.pressure, -102000.0),
        (output.density, 2000.0),
    ):
        assert series.mean == expected
        assert series.block_means == (expected,) * 5
        assert series.sample_standard_deviation == 0.0
        assert series.block_mean_standard_error == 0.0
        assert series.second_half_minus_first_half == 0.0
        assert series.lag_one_block_correlation is None


def test_two_blocks_do_not_infer_a_lag_correlation(trace):
    output = evaluate_flibe_trajectory_block_statistics(
        trace, block_size_samples=4, discard_incomplete_tail=True,
    )
    assert output.block_count == 2
    assert output.discarded_tail_samples == 2
    assert all(series.lag_one_block_correlation is None for series in (
        output.temperature, output.pressure, output.density,
    ))


def test_repeated_evaluation_is_deterministic_and_results_are_frozen(trace):
    a = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    b = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    assert a == b
    assert a is not b
    with pytest.raises(FrozenInstanceError):
        a.block_size_samples = 4  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        a.temperature.mean = 1.0  # type: ignore[misc]


@pytest.mark.parametrize("arguments,error", (
    ({"block_size_samples": 0}, ValueError),
    ({"block_size_samples": 1}, ValueError),
    ({"block_size_samples": -2}, ValueError),
    ({"block_size_samples": True}, TypeError),
    ({"block_size_samples": 2.5}, TypeError),
    ({"block_size_samples": "2"}, TypeError),
    ({"block_size_samples": 6}, ValueError),
    ({"block_size_samples": 3}, ValueError),
    ({"block_size_samples": 2, "discarded_initial_samples": -1}, ValueError),
    ({"block_size_samples": 2, "discarded_initial_samples": True}, TypeError),
    ({"block_size_samples": 2, "discarded_initial_samples": 1}, ValueError),
    ({"block_size_samples": 2, "discarded_initial_samples": 8}, ValueError),
    ({"block_size_samples": 2, "discarded_initial_samples": 10}, ValueError),
    ({"block_size_samples": 2, "discarded_initial_samples": 0.5}, TypeError),
    ({"block_size_samples": 2, "discard_incomplete_tail": 1}, TypeError),
))
def test_invalid_sampling_parameters_are_rejected(trace, arguments, error):
    with pytest.raises(error):
        evaluate_flibe_trajectory_block_statistics(trace, **arguments)


def test_rejects_non_thermodynamic_input():
    with pytest.raises(TypeError, match="FLiBeFrameThermodynamicState"):
        evaluate_flibe_trajectory_block_statistics(None, block_size_samples=2)


def _replace_aligned_coordinate(trace, index: int, *, md_time=None, md_step=None):
    """Change an MD coordinate consistently across the three typed traces."""
    old_thermal = trace.samples[index]
    changes = {}
    if md_time is not None:
        changes["md_time"] = md_time
    if md_step is not None:
        changes["md_step"] = md_step
    temperatures = list(trace.samples)
    temperatures[index] = replace(old_thermal, **changes)
    pressures = list(trace.pressure_trace.samples)
    pressures[index] = replace(pressures[index], **changes)
    densities = list(trace.pressure_trace.density_trace.samples)
    densities[index] = replace(densities[index], **changes)
    density_trace = replace(trace.pressure_trace.density_trace, samples=tuple(densities))
    pressure_trace = replace(trace.pressure_trace, density_trace=density_trace,
                             samples=tuple(pressures))
    return replace(trace, pressure_trace=pressure_trace, samples=tuple(temperatures))


@pytest.mark.parametrize("coordinate,changed", (
    ("md_time", 1.35),
    ("md_step", 13),
))
def test_nonuniform_md_sampling_is_rejected(trace, coordinate, changed):
    altered = _replace_aligned_coordinate(trace, 5, **{coordinate: changed})
    with pytest.raises(ValueError, match="uniform sampling"):
        evaluate_flibe_trajectory_block_statistics(altered, block_size_samples=2)


def test_corrupted_density_mass_volume_identity_is_rejected():
    altered = _build_trace()
    density = altered.pressure_trace.density_trace.samples[2]
    object.__setattr__(density, "density_kg_m3", density.density_kg_m3 * 1.1)
    with pytest.raises(ValueError, match="mass and cell volume"):
        evaluate_flibe_trajectory_block_statistics(altered, block_size_samples=2)


def test_corrupted_kinetic_pressure_tensor_is_rejected():
    altered = _build_trace()
    pressure = altered.pressure_trace.samples[2]
    object.__setattr__(pressure, "kinetic_tensor_pa", _diagonal(123.0))
    with pytest.raises(ValueError, match="kinetic temperature/pressure"):
        evaluate_flibe_trajectory_block_statistics(altered, block_size_samples=2)


@pytest.mark.parametrize("change", (
    {"unit": "joule"},
    {"block_means": (1.0,)},
    {"sample_standard_deviation": -1.0},
    {"block_mean_standard_error": float("nan")},
    {"lag_one_block_correlation": 1.01},
))
def test_observable_contract_rejects_corrupted_fields(trace, change):
    result = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    with pytest.raises((TypeError, ValueError)):
        replace(result.temperature, **change)


@pytest.mark.parametrize("change", (
    {"block_size_samples": 0},
    {"sampling_interval_s": 0.0},
    {"discarded_tail_samples": -1},
    {"temperature_degrees_of_freedom": 0},
    {"physical_state_id": " "},
    {"provenance": "TEST_FIXTURE"},
    {"blocks": ()},
))
def test_result_metadata_contract_rejects_corrupted_fields(trace, change):
    result = evaluate_flibe_trajectory_block_statistics(trace, block_size_samples=2)
    with pytest.raises((TypeError, ValueError)):
        replace(result, **change)
