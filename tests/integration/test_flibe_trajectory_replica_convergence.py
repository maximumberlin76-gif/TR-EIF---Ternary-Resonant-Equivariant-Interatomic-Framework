"""Independent integration tests for FLiBe replica-duration convergence.

Construct aligned thermodynamic traces with distinct initialization fingerprints;
recompute means, between-replica errors, block correlations, drift and duration
changes directly from frame records. Exercise provenance and sampling guards.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import fsum, isclose, sqrt
from statistics import mean, median, stdev

import pytest

from tr_eif.flibe.composition import FLiBeComposition
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
from tr_eif.flibe.trajectory_replica_convergence import (
    FLiBeReplicaConvergencePoint,
    FLiBeReplicaObservableConvergence,
    FLiBeReplicaThermodynamicTrace,
    FLiBeTrajectoryReplicaConvergence,
    evaluate_flibe_trajectory_replica_convergence,
)
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance


SOURCE_SHA = hashlib.sha256(b"registered FLiBe fixture parameters v1").hexdigest()
MASS_KG = 7.0e-26
TIME_UNIT_S = 1.0e-15
TIME_STEP_CODE = 0.25
DOF = 18
FRAMES = 14
DISCARD = 2
BLOCK_SIZE = 2
LENGTHS = (4, 8, 12)
REPLICAS = 4
MODEL_ID = "FLIBE-REPLICA-CONVERGENCE-QUALIFICATION"
METHOD_ID = "tr-eif.flibe.trajectory-replica-duration-convergence.v1"
PROVENANCE = ParameterProvenance.TEST_FIXTURE


def _diagonal(value: float):
    return ((value, 0.0, 0.0), (0.0, value, 0.0), (0.0, 0.0, value))


def _initial_digest(index: int) -> str:
    return hashlib.sha256(f"distinct-initial-condition:{index}".encode()).hexdigest()


def _series(index: int, quantity: str) -> tuple[float, ...]:
    """Fixed synthetic data with independent replica offsets and time evolution."""
    if quantity == "temperature":
        return tuple(800.0 + 5.0 * n + 3.0 * index + ((n + index) % 3 - 1) * 2.0
                     for n in range(FRAMES))
    if quantity == "pressure":
        return tuple(-2.0e6 + 13000.0 * n + 12000.0 * index
                     + 3000.0 * ((2 * n + index) % 4) for n in range(FRAMES))
    if quantity == "density":
        return tuple(1980.0 + 5.0 * index for _ in range(FRAMES))
    raise ValueError(quantity)


def _thermodynamics(
    index: int,
    *,
    frame: FLiBeVelocityFrame = FLiBeVelocityFrame.CENTER_OF_MASS,
    time_step_code: float = TIME_STEP_CODE,
    degrees_of_freedom: int | None = None,
) -> FLiBeFrameThermodynamicState:
    dof = (DOF if frame is FLiBeVelocityFrame.CENTER_OF_MASS else 21)
    if degrees_of_freedom is not None:
        dof = degrees_of_freedom
    densities, pressures, temperatures = [], [], []
    for n, (temperature, signed_pressure, density) in enumerate(zip(
        _series(index, "temperature"),
        _series(index, "pressure"),
        _series(index, "density"),
        strict=True,
    )):
        volume = MASS_KG / density
        kinetic_energy = 0.5 * dof * BOLTZMANN_CONSTANT_J_PER_K * temperature
        kinetic_pressure = 2.0 * kinetic_energy / (3.0 * volume)
        coordinate = {"state_index": n, "md_step": 2 * n,
                      "md_time": time_step_code * n}
        densities.append(FLiBeDensitySample(
            **coordinate, cell_volume_m3=volume, density_kg_m3=density,
        ))
        pressures.append(FLiBePressureSample(
            **coordinate, cell_volume_m3=volume,
            kinetic_tensor_pa=_diagonal(kinetic_pressure),
            configurational_tensor_pa=_diagonal(signed_pressure - kinetic_pressure),
            pressure_tensor_pa=_diagonal(signed_pressure),
            scalar_pressure_pa=signed_pressure,
        ))
        temperatures.append(FLiBeFrameThermalSample(
            **coordinate, velocity_origin_m_s=(0.0, 0.0, 0.0),
            kinetic_energy_j=kinetic_energy,
            kinetic_temperature_k=temperature,
            kinetic_pressure_pa=kinetic_pressure,
        ))
    density_trace = FLiBeTrajectoryDensity(
        model_id=MODEL_ID,
        trajectory_id=f"FLIBE-REPLICA-TRAJECTORY-{index}",
        provenance=PROVENANCE,
        composition=FLiBeComposition(2.0, 1.0),
        atom_count=7, total_mass_kg=MASS_KG,
        mass_unit_to_kg=1.0e-27,
        coordinate_unit_to_meter=1.0e-10,
        samples=tuple(densities),
    )
    pressure_trace = FLiBeTrajectoryPressure(
        density_trace=density_trace, velocity_frame=frame,
        time_unit_to_second=TIME_UNIT_S,
        potential_stress_unit_to_pascal=1.0e5,
        stress_method_id="ENERGY-STRAIN-REPLICA-REFERENCE",
        source_id="SIGNED-PRESSURE-REPLICA-REFERENCE",
        provenance=PROVENANCE,
        samples=tuple(pressures),
    )
    return FLiBeFrameThermodynamicState(
        pressure_trace=pressure_trace,
        degrees_of_freedom=dof,
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED-REPLICA-REFERENCE-STATE",
        samples=tuple(temperatures),
    )


def _replica(index: int, **options) -> FLiBeReplicaThermodynamicTrace:
    return FLiBeReplicaThermodynamicTrace(
        replica_id=f"REPLICA-{index}",
        initial_condition_sha256=_initial_digest(index),
        parameter_source_sha256=SOURCE_SHA,
        thermodynamics=_thermodynamics(index, **options),
    )


def _evaluate(traces, **options):
    parameters = {
        "block_size_samples": BLOCK_SIZE,
        "retained_sample_lengths": LENGTHS,
        "discarded_initial_samples": DISCARD,
    }
    parameters.update(options)
    return evaluate_flibe_trajectory_replica_convergence(traces, **parameters)


@pytest.fixture(scope="module")
def traces():
    return tuple(_replica(index) for index in range(REPLICAS))


@pytest.fixture(scope="module")
def result(traces):
    return _evaluate(traces)


def _raw(traces, replica_index: int, observable: str, length: int):
    source = traces[replica_index].thermodynamics
    if observable == "temperature":
        samples = source.samples
        attr = "kinetic_temperature_k"
    elif observable == "pressure":
        samples = source.pressure_trace.samples
        attr = "scalar_pressure_pa"
    else:
        samples = source.pressure_trace.density_trace.samples
        attr = "density_kg_m3"
    return tuple(getattr(sample, attr) for sample in samples[DISCARD:DISCARD + length])


def _lag_one(means: tuple[float, ...]) -> float | None:
    if len(means) < 3:
        return None
    left, right = means[:-1], means[1:]
    center_left, center_right = mean(left), mean(right)
    left_square = fsum((v - center_left) ** 2 for v in left)
    right_square = fsum((v - center_right) ** 2 for v in right)
    if left_square == 0.0 or right_square == 0.0:
        return None
    return fsum((a - center_left) * (b - center_right)
                for a, b in zip(left, right, strict=True)) / sqrt(left_square * right_square)


def _reference(traces, observable: str, length: int, replicas: int):
    rows = tuple(_raw(traces, i, observable, length) for i in range(replicas))
    means = tuple(mean(row) for row in rows)
    bse, drifts, correlations = [], [], []
    for row in rows:
        blocks = tuple(mean(row[j:j + BLOCK_SIZE])
                       for j in range(0, len(row), BLOCK_SIZE))
        bse.append(stdev(blocks) / sqrt(len(blocks)))
        half = len(blocks) // 2
        drifts.append(abs(mean(blocks[half:]) - mean(blocks[:half])))
        correlations.append(_lag_one(blocks))
    defined = tuple(abs(c) for c in correlations if c is not None)
    return {
        "means": means,
        "center": mean(means),
        "sd": stdev(means),
        "se": stdev(means) / sqrt(replicas),
        "within_se_median": median(bse),
        "maximum_drift": max(drifts),
        "maximum_correlation": max(defined) if defined else None,
        "undefined_correlations": len(correlations) - len(defined),
    }


def _close(actual, expected, *, abs_tol=1.0e-9):
    assert isclose(actual, expected, rel_tol=1.0e-12, abs_tol=abs_tol)


def test_matrix_metadata_source_and_scopes(result, traces):
    assert isinstance(result, FLiBeTrajectoryReplicaConvergence)
    assert result.method_id == METHOD_ID
    assert result.model_id == MODEL_ID
    assert result.parameter_source_sha256 == SOURCE_SHA
    assert result.provenance is PROVENANCE
    assert result.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
    assert result.physical_state_id == "UNCLASSIFIED_MD_PHASE"
    assert result.physical_state_method_id == "DECLARED-REPLICA-REFERENCE-STATE"
    _close(result.sampling_interval_s, TIME_STEP_CODE * TIME_UNIT_S, abs_tol=1e-29)
    assert result.discarded_initial_samples == DISCARD
    assert result.block_size_samples == BLOCK_SIZE
    assert result.retained_sample_lengths == LENGTHS
    assert result.replica_ids == tuple(x.replica_id for x in traces)
    assert result.trajectory_count == REPLICAS
    assert len(result.points) == len(LENGTHS) * (REPLICAS - 1)


@pytest.mark.parametrize("length", LENGTHS)
@pytest.mark.parametrize("replicas", (2, 3, 4))
def test_full_matrix_independent_estimates(result, traces, length, replicas):
    point = result.at(length, replicas)
    assert isinstance(point, FLiBeReplicaConvergencePoint)
    assert point.retained_samples_per_trajectory == length
    assert point.replica_count == replicas
    _close(point.observed_duration_s, (length - 1) * TIME_STEP_CODE * TIME_UNIT_S,
           abs_tol=1e-29)
    assert point.trajectory_ids == tuple(
        traces[i].thermodynamics.pressure_trace.density_trace.trajectory_id
        for i in range(replicas)
    )
    assert point.initial_condition_sha256 == tuple(
        _initial_digest(i) for i in range(replicas)
    )
    for observable, unit in (("temperature", "K"), ("pressure", "Pa"),
                             ("density", "kg/m^3")):
        actual = getattr(point, observable)
        assert isinstance(actual, FLiBeReplicaObservableConvergence)
        assert actual.unit == unit
        reference = _reference(traces, observable, length, replicas)
        assert actual.trajectory_means == pytest.approx(reference["means"], rel=1e-12)
        _close(actual.mean_of_trajectory_means, reference["center"])
        _close(actual.between_trajectory_sample_sd, reference["sd"])
        _close(actual.between_trajectory_standard_error, reference["se"])
        _close(actual.median_within_trajectory_block_se, reference["within_se_median"])
        _close(actual.maximum_absolute_half_window_shift, reference["maximum_drift"])
        if reference["maximum_correlation"] is None:
            assert actual.maximum_absolute_lag_one_block_correlation is None
        else:
            _close(actual.maximum_absolute_lag_one_block_correlation,
                   reference["maximum_correlation"], abs_tol=1e-12)
        assert actual.undefined_lag_one_correlation_count == reference["undefined_correlations"]
        if length == LENGTHS[0]:
            assert actual.mean_change_from_previous_duration is None
        else:
            previous_length = LENGTHS[LENGTHS.index(length) - 1]
            previous = _reference(traces, observable, previous_length, replicas)
            _close(actual.mean_change_from_previous_duration,
                   reference["center"] - previous["center"])


def test_signed_pressure_and_constant_per_run_density(result):
    point = result.at(12, 4)
    assert all(p < 0.0 for p in point.pressure.trajectory_means)
    assert point.pressure.mean_of_trajectory_means < 0.0
    assert point.density.between_trajectory_standard_error > 0.0
    assert point.density.median_within_trajectory_block_se == 0.0
    assert point.density.maximum_absolute_half_window_shift == 0.0
    assert point.density.maximum_absolute_lag_one_block_correlation is None
    assert point.density.undefined_lag_one_correlation_count == 4
    assert point.temperature.maximum_absolute_lag_one_block_correlation is not None


def test_output_is_deterministic_and_immutable(traces, result):
    replay = _evaluate(traces)
    assert replay == result
    assert replay is not result
    with pytest.raises(FrozenInstanceError):
        result.block_size_samples = 4  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        result.points[0].replica_count = 5  # type: ignore[misc]


def test_alternative_complete_block_partition(traces):
    actual = _evaluate(traces, block_size_samples=3,
                       retained_sample_lengths=(6, 12), discarded_initial_samples=0)
    assert actual.retained_sample_lengths == (6, 12)
    assert len(actual.points) == 6
    for length in (6, 12):
        for count in (2, 3, 4):
            point = actual.at(length, count)
            values = tuple(mean(_series(i, "temperature")[:length]) for i in range(count))
            assert point.temperature.trajectory_means == pytest.approx(values)
            _close(point.temperature.between_trajectory_standard_error,
                   stdev(values) / sqrt(count))


@pytest.mark.parametrize("value", (
    (), (3,), (4, 4), (8, 4), (5,), (4, 13), (4, 16), (True,),
))
def test_invalid_duration_grid_is_rejected(traces, value):
    with pytest.raises((TypeError, ValueError)):
        _evaluate(traces, retained_sample_lengths=value)


@pytest.mark.parametrize("options", (
    {"block_size_samples": 0}, {"block_size_samples": 1},
    {"block_size_samples": True}, {"block_size_samples": 2.5},
    {"discarded_initial_samples": -1}, {"discarded_initial_samples": True},
    {"discarded_initial_samples": 3},
))
def test_invalid_block_and_discard_parameters_are_rejected(traces, options):
    with pytest.raises((TypeError, ValueError)):
        _evaluate(traces, **options)


@pytest.mark.parametrize("invalid", (None, [], (), ("x",)))
def test_input_requires_two_typed_trajectories(invalid):
    with pytest.raises((TypeError, ValueError)):
        _evaluate(invalid)


def _replace_trace(replica, **updates):
    return replace(replica, thermodynamics=replace(replica.thermodynamics, **updates))


def _replace_pressure(replica, **updates):
    thermal = replica.thermodynamics
    return _replace_trace(replica, pressure_trace=replace(thermal.pressure_trace, **updates))


def _replace_density(replica, **updates):
    pressure = replica.thermodynamics.pressure_trace
    return _replace_pressure(replica, density_trace=replace(pressure.density_trace, **updates))


@pytest.mark.parametrize("condition", (
    "replica_id", "trajectory_id", "initial_sha", "parameter_sha",
    "model_id", "composition", "provenance", "velocity_frame",
    "stress_method", "pressure_source", "time_conversion",
    "physical_state", "degrees_of_freedom", "sampling_interval", "short_trace",
))
def test_incompatible_or_reused_replica_is_rejected(traces, condition):
    entries = list(traces)
    modified = entries[1]
    if condition == "replica_id":
        modified = replace(modified, replica_id=entries[0].replica_id)
    elif condition == "trajectory_id":
        existing_id = entries[0].thermodynamics.pressure_trace.density_trace.trajectory_id
        modified = _replace_density(modified, trajectory_id=existing_id)
    elif condition == "initial_sha":
        modified = replace(modified, initial_condition_sha256=entries[0].initial_condition_sha256)
    elif condition == "parameter_sha":
        modified = replace(modified, parameter_source_sha256="f" * 64)
    elif condition == "model_id":
        modified = _replace_density(modified, model_id="OTHER-MODEL")
    elif condition == "composition":
        modified = _replace_density(modified, composition=FLiBeComposition(3.0, 2.0))
    elif condition == "provenance":
        modified = _replace_density(modified, provenance=ParameterProvenance.BENCHMARK)
    elif condition == "velocity_frame":
        modified = replace(modified, thermodynamics=_thermodynamics(1, frame=FLiBeVelocityFrame.LABORATORY))
    elif condition == "stress_method":
        modified = _replace_pressure(modified, stress_method_id="DIFFERENT-STRESS-METHOD")
    elif condition == "pressure_source":
        modified = _replace_pressure(modified, source_id="DIFFERENT-PRESSURE-SOURCE")
    elif condition == "time_conversion":
        modified = _replace_pressure(modified, time_unit_to_second=2.0 * TIME_UNIT_S)
    elif condition == "physical_state":
        modified = _replace_trace(modified, physical_state_id="OTHER-PHYSICAL-STATE")
    elif condition == "degrees_of_freedom":
        modified = replace(modified, thermodynamics=_thermodynamics(
            1, degrees_of_freedom=DOF - 1
        ))
    elif condition == "sampling_interval":
        modified = replace(modified, thermodynamics=_thermodynamics(1, time_step_code=0.5))
    elif condition == "short_trace":
        thermal = modified.thermodynamics
        pressure = thermal.pressure_trace
        density = pressure.density_trace
        pressure = replace(pressure,
                           density_trace=replace(density, samples=density.samples[:10]),
                           samples=pressure.samples[:10])
        modified = _replace_trace(modified, pressure_trace=pressure,
                                  samples=thermal.samples[:10])
    entries[1] = modified
    with pytest.raises((TypeError, ValueError)):
        _evaluate(tuple(entries))


def test_selected_duration_lookup_rejects_unregistered_coordinates(result):
    with pytest.raises(ValueError, match="outside the declared grid"):
        result.at(6, 3)
    with pytest.raises(ValueError, match="outside the declared grid"):
        result.at(8, 1)


def test_rejects_nonuniform_frames_even_with_aligned_typed_traces(traces):
    entries = list(traces)
    replica = entries[2]
    thermal = replica.thermodynamics
    pressure = thermal.pressure_trace
    density = pressure.density_trace
    index = 5
    changes = {"md_time": pressure.samples[index].md_time + 0.03}
    density_rows = list(density.samples)
    pressure_rows = list(pressure.samples)
    thermal_rows = list(thermal.samples)
    density_rows[index] = replace(density_rows[index], **changes)
    pressure_rows[index] = replace(pressure_rows[index], **changes)
    thermal_rows[index] = replace(thermal_rows[index], **changes)
    density = replace(density, samples=tuple(density_rows))
    pressure = replace(pressure, density_trace=density, samples=tuple(pressure_rows))
    entries[2] = replace(replica, thermodynamics=replace(
        thermal, pressure_trace=pressure, samples=tuple(thermal_rows)
    ))
    with pytest.raises(ValueError, match="uniform sampling"):
        _evaluate(tuple(entries))


@pytest.mark.parametrize("field,value", (
    ("replica_id", " "), ("initial_condition_sha256", "a" * 63),
    ("parameter_source_sha256", "A" * 64),
    ("thermodynamics", None),
))
def test_trace_record_validates_identifiers_and_types(traces, field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(traces[0], **{field: value})


@pytest.mark.parametrize("field,value", (
    ("between_trajectory_standard_error", -1.0),
    ("between_trajectory_sample_sd", -1.0),
    ("mean_of_trajectory_means", float("nan")),
    ("maximum_absolute_lag_one_block_correlation", 1.01),
    ("undefined_lag_one_correlation_count", 5),
    ("trajectory_means", (0.0,)),
    ("unit", "J"),
))
def test_observable_record_rejects_corruption(result, field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(result.points[0].temperature, **{field: value})


@pytest.mark.parametrize("field,value", (
    ("replica_count", 1),
    ("trajectory_ids", ("A", "A")),
    ("initial_condition_sha256", ("b" * 64, "b" * 64)),
    ("retained_samples_per_trajectory", 1),
))
def test_point_record_rejects_corruption(result, field, value):
    with pytest.raises((TypeError, ValueError)):
        replace(result.points[0], **{field: value})


def test_result_record_rejects_corrupt_provenance_and_grid(result):
    with pytest.raises((TypeError, ValueError)):
        replace(result, parameter_source_sha256="bad")
    with pytest.raises((TypeError, ValueError)):
        replace(result, method_id="OTHER-METHOD")
    with pytest.raises((TypeError, ValueError)):
        replace(result, points=result.points[:-1])
