
"""Independent tests of FLiBe replica sampling-stationarity diagnostics.

Construct aligned periodic-MD thermodynamic observations for Li2BeF4.
Recalculate split-chain R-hat, pooled autocorrelation, positive-pair
correlation time, effective sample count, and half-window drift without
calling the estimator's internal statistical helpers. Check provenance,
physical-coordinate matching, declared screening thresholds, and constant
signed-pressure/density cases separately from sampling variability.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError, replace
from math import sqrt
from statistics import mean, stdev, variance

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
from tr_eif.flibe.trajectory_replica_convergence import FLiBeReplicaThermodynamicTrace
from tr_eif.flibe.trajectory_replica_stationarity import (
    METHOD_ID,
    FLiBeReplicaSamplingObservable,
    FLiBeTrajectoryStationarityDiagnostics,
    evaluate_flibe_replica_sampling_stationarity,
)
from tr_eif.flibe.trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K
from tr_eif.flibe.units import ParameterProvenance


PROVENANCE = ParameterProvenance.TEST_FIXTURE
SOURCE_SHA256 = hashlib.sha256(b"flibe-stationarity-fixture-v1").hexdigest()
MODEL_ID = "FLIBE-STATIONARITY-REFERENCE"
MASS_KG = 7.0e-26
TIME_UNIT_S = 1.0e-15
TIME_STEP_CODE = 0.25
DOF = 18
NUMBER_OF_FRAMES = 14
FIELDS = (
    ("temperature", "kinetic_temperature_k", "K"),
    ("pressure", "scalar_pressure_pa", "Pa"),
    ("density", "density_kg_m3", "kg/m^3"),
)


def _diagonal(value: float):
    return ((value, 0.0, 0.0), (0.0, value, 0.0), (0.0, 0.0, value))


def _replica(index: int, *, length=NUMBER_OF_FRAMES, dt=TIME_STEP_CODE,
             mode="drift", frame=FLiBeVelocityFrame.CENTER_OF_MASS, dof=DOF):
    density_rows, pressure_rows, temperature_rows = [], [], []
    for sample in range(length):
        if mode == "constant":
            temperature, pressure, density = 850.0, -100000.0, 2000.0
        elif mode == "constant_by_replica":
            temperature = 850.0 + 3.0 * index
            pressure = -100000.0 + 700.0 * index
            density = 2000.0 + 2.0 * index
        else:
            temperature = 820.0 + 2.7 * sample + 2.0 * index + 0.45 * ((sample + index) % 4)
            pressure = -150000.0 + 530.0 * sample - 90.0 * index + 30.0 * ((sample + index) % 3)
            density = (2000.0 if mode == "drift" else
                       1990.0 + 2.0 * sample + 3.0 * index + 0.2 * ((sample + index) % 3))
        volume = MASS_KG / density
        kinetic_energy = dof * BOLTZMANN_CONSTANT_J_PER_K * temperature / 2.0
        kinetic_pressure = 2.0 * kinetic_energy / (3.0 * volume)
        indices = dict(state_index=sample, md_step=2 * sample, md_time=dt * sample)
        density_rows.append(FLiBeDensitySample(
            **indices, cell_volume_m3=volume, density_kg_m3=density,
        ))
        pressure_rows.append(FLiBePressureSample(
            **indices, cell_volume_m3=volume,
            kinetic_tensor_pa=_diagonal(kinetic_pressure),
            configurational_tensor_pa=_diagonal(pressure - kinetic_pressure),
            pressure_tensor_pa=_diagonal(pressure), scalar_pressure_pa=pressure,
        ))
        temperature_rows.append(FLiBeFrameThermalSample(
            **indices, velocity_origin_m_s=(0.0, 0.0, 0.0),
            kinetic_energy_j=kinetic_energy, kinetic_temperature_k=temperature,
            kinetic_pressure_pa=kinetic_pressure,
        ))
    density_trace = FLiBeTrajectoryDensity(
        model_id=MODEL_ID, trajectory_id=f"FLIBE-STATIONARITY-TRAJECTORY-{index}",
        provenance=PROVENANCE, composition=FLiBeComposition(2.0, 1.0),
        atom_count=7, total_mass_kg=MASS_KG,
        mass_unit_to_kg=1.0e-27, coordinate_unit_to_meter=1.0e-10,
        samples=tuple(density_rows),
    )
    pressure_trace = FLiBeTrajectoryPressure(
        density_trace=density_trace, velocity_frame=frame,
        time_unit_to_second=TIME_UNIT_S, potential_stress_unit_to_pascal=1.0e5,
        stress_method_id="STATIONARITY-ENERGY-STRAIN",
        source_id="STATIONARITY-SIGNED-PRESSURE",
        provenance=PROVENANCE, samples=tuple(pressure_rows),
    )
    thermal = FLiBeFrameThermodynamicState(
        pressure_trace=pressure_trace, degrees_of_freedom=dof,
        physical_state_id="UNCLASSIFIED_MD_PHASE",
        physical_state_method_id="DECLARED-STATIONARITY-REFERENCE-STATE",
        samples=tuple(temperature_rows),
    )
    return FLiBeReplicaThermodynamicTrace(
        replica_id=f"REPLICA-{index}",
        initial_condition_sha256=hashlib.sha256(
            f"stationarity-initial-state-{index}".encode("utf-8")
        ).hexdigest(),
        parameter_source_sha256=SOURCE_SHA256,
        thermodynamics=thermal,
    )


def _traces(**kwargs):
    return tuple(_replica(index, **kwargs) for index in range(4))


def _values(traces, name: str, discard: int, length: int):
    chains = []
    for record in traces:
        thermal = record.thermodynamics
        samples = (
            thermal.samples if name == "temperature" else
            thermal.pressure_trace.samples if name == "pressure" else
            thermal.pressure_trace.density_trace.samples
        )
        attribute = next(field for label, field, _ in FIELDS if label == name)
        chains.append(tuple(getattr(row, attribute) for row in samples[discard:discard + length]))
    return tuple(chains)


def _independent_reference(chains):
    """Reference using explicit variance and lagged covariance arithmetic."""
    n = len(chains[0])
    count = len(chains)
    half = n // 2
    split = tuple(part for row in chains for part in (row[:half], row[-half:]))
    within = mean(variance(part) for part in split)
    rhat = None if within == 0.0 else sqrt(
        ((half - 1) * within / half + variance(tuple(mean(part) for part in split))) / within
    )
    centers = tuple(mean(row) for row in chains)
    centered_variance = sum(
        sum((value - center) ** 2 for value in row) / n
        for row, center in zip(chains, centers, strict=True)
    ) / count
    coefficients = []
    for lag in range(1, n):
        if centered_variance == 0.0:
            coefficients.append(None)
            continue
        covariance = sum(
            sum((row[i] - center) * (row[i + lag] - center)
                for i in range(n - lag)) / (n - lag)
            for row, center in zip(chains, centers, strict=True)
        ) / count
        coefficients.append(max(-1.0, min(1.0, covariance / centered_variance)))
    if coefficients[0] is None:
        lag_one, tau, effective = None, None, None
    else:
        accepted_pairs = []
        for k in range(0, len(coefficients) - 1, 2):
            next_pair = coefficients[k] + coefficients[k + 1]
            if next_pair <= 0.0:
                break
            accepted_pairs.append(
                min(next_pair, accepted_pairs[-1]) if accepted_pairs else next_pair
            )
        lag_one = coefficients[0]
        tau = max(1.0, 1.0 + 2.0 * sum(accepted_pairs))
        effective = count * n / tau
    shifts = []
    for row in chains:
        delta = abs(mean(row[-half:]) - mean(row[:half]))
        sd = stdev(row)
        shifts.append(0.0 if sd == 0.0 and delta == 0.0 else
                      None if sd == 0.0 else delta / sd)
    drift = None if any(value is None for value in shifts) else max(shifts)
    return centers, rhat, lag_one, tau, effective, drift


def _audit(result, traces, discard, length):
    assert isinstance(result, FLiBeTrajectoryStationarityDiagnostics)
    assert result.method_id == METHOD_ID
    assert result.model_id == MODEL_ID
    assert result.parameter_source_sha256 == SOURCE_SHA256
    assert result.provenance is PROVENANCE
    assert result.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS
    assert result.physical_state_id == "UNCLASSIFIED_MD_PHASE"
    assert result.physical_state_method_id == "DECLARED-STATIONARITY-REFERENCE-STATE"
    assert result.replica_ids == tuple(record.replica_id for record in traces)
    assert result.initial_condition_sha256 == tuple(
        record.initial_condition_sha256 for record in traces
    )
    assert result.replica_count == len(traces)
    assert result.discarded_initial_samples == discard
    assert result.retained_samples_per_replica == length
    assert result.central_sample_dropped_per_replica == length % 2
    assert result.sampling_interval_s == pytest.approx(
        TIME_STEP_CODE * TIME_UNIT_S, rel=1.0e-12, abs=1.0e-30
    )
    assert result.observed_duration_s == pytest.approx(
        (length - 1) * TIME_STEP_CODE * TIME_UNIT_S, rel=1.0e-12, abs=1.0e-30
    )
    for name, _, unit in FIELDS:
        series = getattr(result, name)
        assert isinstance(series, FLiBeReplicaSamplingObservable)
        assert series.unit == unit
        chains = _values(traces, name, discard, length)
        means, rhat, lag_one, tau, effective, drift = _independent_reference(chains)
        assert series.replica_means == pytest.approx(means, rel=1.0e-12)
        for value, expected in (
            (series.split_rhat, rhat),
            (series.pooled_lag_one_autocorrelation, lag_one),
            (series.positive_pair_autocorrelation_time_samples, tau),
            (series.effective_sample_size_proxy, effective),
            (series.maximum_standardized_half_window_shift, drift),
        ):
            if expected is None:
                assert value is None
            else:
                assert value == pytest.approx(expected, rel=1.0e-11, abs=1.0e-12)
        if all(value == chains[0][0] for chain in chains for value in chain):
            expected_status = "FIXED_SERIES_CONSTANT"
        elif None in (rhat, lag_one, tau, effective, drift):
            expected_status = "WITHIN_REPLICA_VARIANCE_ZERO"
        elif (
            rhat <= result.maximum_split_rhat
            and effective >= result.minimum_effective_sample_size
            and abs(lag_one) <= result.maximum_absolute_lag_one_correlation
            and drift <= result.maximum_standardized_half_window_shift
        ):
            expected_status = "SCREENING_CRITERIA_MET"
        else:
            expected_status = "SCREENING_CRITERIA_FLAGGED"
        assert series.diagnostic_status == expected_status


@pytest.fixture(scope="module")
def traces():
    return _traces()


@pytest.mark.parametrize("discard,length", ((0, 14), (1, 12), (2, 10), (2, 11), (4, 8)))
def test_reference_formulas_even_and_odd_windows(traces, discard, length):
    result = evaluate_flibe_replica_sampling_stationarity(
        traces, discarded_initial_samples=discard,
        retained_samples_per_replica=length,
    )
    _audit(result, traces, discard, length)
    assert result.temperature.diagnostic_status == "SCREENING_CRITERIA_FLAGGED"
    assert result.pressure.diagnostic_status == "SCREENING_CRITERIA_FLAGGED"
    assert result.density.diagnostic_status == "FIXED_SERIES_CONSTANT"


def test_default_scope_replay_and_frozen_results(traces):
    first = evaluate_flibe_replica_sampling_stationarity(traces)
    second = evaluate_flibe_replica_sampling_stationarity(traces)
    assert first == second and first is not second
    _audit(first, traces, 0, NUMBER_OF_FRAMES)
    with pytest.raises(FrozenInstanceError):
        first.retained_samples_per_replica = 8
    with pytest.raises(FrozenInstanceError):
        first.temperature.unit = "Pa"


@pytest.mark.parametrize("mode,expected", (
    ("constant", "FIXED_SERIES_CONSTANT"),
    ("constant_by_replica", "WITHIN_REPLICA_VARIANCE_ZERO"),
))
def test_constant_series_categories(mode, expected):
    traces = _traces(mode=mode)
    result = evaluate_flibe_replica_sampling_stationarity(
        traces, retained_samples_per_replica=12,
    )
    _audit(result, traces, 0, 12)
    assert all(getattr(result, name).diagnostic_status == expected for name, _, _ in FIELDS)


def test_variable_cell_density_and_signed_pressure_are_retained():
    traces = _traces(mode="variable_density")
    result = evaluate_flibe_replica_sampling_stationarity(
        traces, discarded_initial_samples=2, retained_samples_per_replica=10,
    )
    _audit(result, traces, 2, 10)
    assert result.density.split_rhat is not None
    assert all(value < 0 for value in result.pressure.replica_means)


def test_declared_screening_limits_change_only_status(traces):
    strict = evaluate_flibe_replica_sampling_stationarity(traces)
    relaxed = evaluate_flibe_replica_sampling_stationarity(
        traces, maximum_split_rhat=100.0,
        minimum_effective_sample_size=1.0,
        maximum_absolute_lag_one_correlation=1.0,
        maximum_standardized_half_window_shift=100.0,
    )
    assert relaxed.temperature.diagnostic_status == "SCREENING_CRITERIA_MET"
    assert relaxed.pressure.diagnostic_status == "SCREENING_CRITERIA_MET"
    for name, _, _ in FIELDS:
        a, b = getattr(strict, name), getattr(relaxed, name)
        assert a.replica_means == b.replica_means
        assert a.split_rhat == b.split_rhat
        assert a.effective_sample_size_proxy == b.effective_sample_size_proxy


@pytest.mark.parametrize("arguments", (
    {"retained_samples_per_replica": 7},
    {"retained_samples_per_replica": True},
    {"retained_samples_per_replica": 15},
    {"retained_samples_per_replica": 8.5},
    {"discarded_initial_samples": -1},
    {"discarded_initial_samples": True},
    {"discarded_initial_samples": 8},
    {"maximum_split_rhat": 0.0},
    {"maximum_split_rhat": True},
    {"minimum_effective_sample_size": float("nan")},
    {"maximum_absolute_lag_one_correlation": 1.1},
    {"maximum_standardized_half_window_shift": -0.5},
))
def test_invalid_window_or_screening_controls(traces, arguments):
    with pytest.raises((ValueError, TypeError)):
        evaluate_flibe_replica_sampling_stationarity(traces, **arguments)


@pytest.mark.parametrize("invalid", ((), None, [], ("invalid",)))
def test_requires_two_typed_replicas(invalid):
    with pytest.raises((ValueError, TypeError)):
        evaluate_flibe_replica_sampling_stationarity(invalid)


def _with_density_field(record, **changes):
    thermal = record.thermodynamics
    pressure = thermal.pressure_trace
    density = replace(pressure.density_trace, **changes)
    return replace(record, thermodynamics=replace(
        thermal, pressure_trace=replace(pressure, density_trace=density),
    ))


def _with_pressure_field(record, **changes):
    thermal = record.thermodynamics
    return replace(record, thermodynamics=replace(
        thermal, pressure_trace=replace(thermal.pressure_trace, **changes),
    ))


@pytest.mark.parametrize("case", (
    "duplicate_replica", "duplicate_initial", "duplicate_trajectory",
    "parameter_source", "model_id", "composition", "atom_count",
    "mass", "mass_unit", "coordinate_unit", "density_provenance",
    "velocity_frame", "stress_method", "pressure_source", "pressure_provenance",
    "time_unit", "degrees_of_freedom", "physical_state", "state_method",
    "time_grid", "short_record",
))
def test_rejects_mismatched_replica_conditions(traces, case):
    rows = list(traces)
    item = rows[1]
    thermal = item.thermodynamics
    if case == "duplicate_replica":
        item = replace(item, replica_id=rows[0].replica_id)
    elif case == "duplicate_initial":
        item = replace(item, initial_condition_sha256=rows[0].initial_condition_sha256)
    elif case == "duplicate_trajectory":
        item = _with_density_field(
            item, trajectory_id=rows[0].thermodynamics.pressure_trace.density_trace.trajectory_id
        )
    elif case == "parameter_source":
        item = replace(item, parameter_source_sha256="b" * 64)
    elif case == "model_id":
        item = _with_density_field(item, model_id="OTHER-MODEL")
    elif case == "composition":
        item = _with_density_field(item, composition=FLiBeComposition(3.0, 2.0))
    elif case == "atom_count":
        item = _with_density_field(item, atom_count=8)
    elif case == "mass":
        item = _with_density_field(item, total_mass_kg=MASS_KG * 1.01)
    elif case == "mass_unit":
        item = _with_density_field(item, mass_unit_to_kg=2.0e-27)
    elif case == "coordinate_unit":
        item = _with_density_field(item, coordinate_unit_to_meter=2.0e-10)
    elif case == "density_provenance":
        item = _with_density_field(item, provenance=ParameterProvenance.BENCHMARK)
    elif case == "velocity_frame":
        item = _with_pressure_field(item, velocity_frame=FLiBeVelocityFrame.LABORATORY)
    elif case == "stress_method":
        item = _with_pressure_field(item, stress_method_id="OTHER-STRESS")
    elif case == "pressure_source":
        item = _with_pressure_field(item, source_id="OTHER-PRESSURE")
    elif case == "pressure_provenance":
        item = _with_pressure_field(item, provenance=ParameterProvenance.BENCHMARK)
    elif case == "time_unit":
        item = _with_pressure_field(item, time_unit_to_second=2.0e-15)
    elif case == "degrees_of_freedom":
        item = _replica(1, dof=17)
    elif case == "physical_state":
        item = replace(item, thermodynamics=replace(thermal, physical_state_id="OTHER-STATE"))
    elif case == "state_method":
        item = replace(item, thermodynamics=replace(
            thermal, physical_state_method_id="OTHER-METHOD"
        ))
    elif case == "time_grid":
        item = _replica(1, dt=TIME_STEP_CODE * 1.1)
    elif case == "short_record":
        item = _replica(1, length=8)
    rows[1] = item
    with pytest.raises((ValueError, TypeError)):
        evaluate_flibe_replica_sampling_stationarity(tuple(rows))


def test_rejects_nonuniform_time_grid_inside_selected_window(traces):
    rows = list(traces)
    source = rows[2].thermodynamics
    old_p = source.pressure_trace
    old_d = old_p.density_trace
    index = 7
    def change(samples):
        sequence = list(samples)
        sequence[index] = replace(sequence[index], md_time=sequence[index].md_time + 0.04)
        return tuple(sequence)
    density = replace(old_d, samples=change(old_d.samples))
    pressure = replace(old_p, density_trace=density, samples=change(old_p.samples))
    thermal = replace(source, pressure_trace=pressure, samples=change(source.samples))
    rows[2] = replace(rows[2], thermodynamics=thermal)
    with pytest.raises(ValueError, match="uniform physical time grid"):
        evaluate_flibe_replica_sampling_stationarity(tuple(rows))


@pytest.mark.parametrize("field,value", (
    ("unit", "J"), ("split_rhat", 0.0),
    ("effective_sample_size_proxy", float("nan")),
    ("pooled_lag_one_autocorrelation", 1.5),
    ("maximum_standardized_half_window_shift", -1.0),
    ("diagnostic_status", "UNREGISTERED"),
    ("replica_means", (1.0,)),
))
def test_observable_record_rejects_invalid_fields(traces, field, value):
    result = evaluate_flibe_replica_sampling_stationarity(traces)
    with pytest.raises((ValueError, TypeError)):
        replace(result.temperature, **{field: value})


@pytest.mark.parametrize("field,value", (
    ("method_id", "OTHER"), ("parameter_source_sha256", "BAD"),
    ("sampling_interval_s", 0.0), ("maximum_split_rhat", -1.0),
    ("maximum_absolute_lag_one_correlation", 1.5),
    ("retained_samples_per_replica", 7),
    ("central_sample_dropped_per_replica", 1),
    ("replica_ids", ("DUPLICATE", "DUPLICATE")),
    ("temperature", None),
))
def test_result_record_rejects_invalid_fields(traces, field, value):
    result = evaluate_flibe_replica_sampling_stationarity(traces)
    with pytest.raises((ValueError, TypeError)):
        replace(result, **{field: value})
