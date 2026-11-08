"""Independent integration checks for periodic FLiBe MD stationarity evidence.

The recorded microstates, periodic mass density, uniformly sampled frame data,
and two window-specific stationarity estimators are independently reconstructed.
The test preserves the execution boundary of the interatomic MD layer within
TR-EIF and checks the registered scope of the coupled architectural contracts.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from math import fsum, isclose, isfinite, sqrt
from pathlib import Path
from statistics import mean, stdev

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_md_replica_stationarity_benchmark.py"
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-replica-stationarity-benchmark.v1"
METHOD_ID = "tr-eif.flibe.replica-sampling-stationarity.v1"
MODEL_ID = "FLIBE-PERIODIC-REPLICA-DURATION-BENCHMARK"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
BASE_POSITIONS = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITY_PATTERN = (
    (0.03, 0.01, 0.0), (-0.03, -0.01, 0.02),
    (0.02, 0.03, -0.02), (0.0, -0.02, 0.01),
    (0.01, 0.005, -0.02), (-0.015, 0.02, 0.0),
    (-0.015, -0.015, 0.01),
)
MASSES_U = tuple({"Li": 6.94, "Be": 9.0121831, "F": 18.998403163}[s]
                 for s in SPECIES)
BOHR_TO_M = 5.29177210903e-11
U_TO_KG = 1.66053906660e-27
TIME_TO_S = 1.0e-15
BOLTZMANN = 1.380649e-23
EDGE_BOHR = 10.0
SAMPLE_STEP = 0.02
WINDOWS = (("all_nine_frames", 0, 9), ("discard_first_frame", 1, 8))
FIELDS = (("temperature", "temperature_k", "K"),
          ("pressure", "signed_pressure_pa", "Pa"),
          ("density", "density_kg_m3", "kg/m^3"))
CRITERIA = {
    "maximum_split_rhat": 1.05,
    "minimum_effective_sample_size": 40.0,
    "maximum_absolute_lag_one_correlation": 0.5,
    "maximum_standardized_half_window_shift": 0.5,
}
CHECK_NAMES = {
    "registered_pair_fingerprint",
    "replica_initialization_distinctness",
    "common_md_protocol",
    "same_initial_temperature",
    "zero_initial_center_of_mass_velocity",
    "fixed_cell_density_identity",
    "finite_signed_pressures",
    "dipole_stationarity",
    "two_declared_sampling_windows",
    "identical_physical_state_metadata",
    "independently_recalculated_sampling_estimators",
    "independently_recalculated_statuses",
    "fixed_cell_density_status",
    "finite_sample_size_boundary",
}


def _number(value: object) -> float:
    assert type(value) in (float, int)
    result = float(value)
    assert isfinite(result)
    return result


def _near(actual: object, target: float, *, atol: float = 1.0e-11) -> None:
    assert isclose(_number(actual), target, rel_tol=1.0e-10, abs_tol=atol)


def _optional_near(actual: object, target: float | None) -> None:
    if target is None:
        assert actual is None
    else:
        _near(actual, target)


def _run_cli() -> tuple[dict, bytes]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), env.get("PYTHONPATH", "")) if part
    )
    completed = subprocess.run(
        [sys.executable, str(BENCHMARK)], cwd=ROOT, env=env,
        capture_output=True, check=False, timeout=480,
    )
    assert completed.returncode == 0, (
        completed.stderr.decode("utf-8", errors="replace")
        + completed.stdout.decode("utf-8", errors="replace")[-3000:]
    )
    assert completed.stderr == b""
    report = json.loads(completed.stdout)
    assert isinstance(report, dict)
    return report, completed.stdout


@pytest.fixture(scope="module")
def execution() -> tuple[dict, bytes]:
    assert BENCHMARK.is_file() and SOURCE.is_file()
    return _run_cli()


@pytest.fixture(scope="module")
def report(execution) -> dict:
    return execution[0]


def _velocities(replica_index: int) -> tuple[tuple[float, float, float], ...]:
    varied = tuple((
        pattern[0] + 0.0010 * replica_index * ((atom % 3) - 1),
        pattern[1] + 0.0015 * replica_index * (((atom + 1) % 3) - 1),
        pattern[2] + 0.0008 * replica_index * (((atom + 2) % 3) - 1),
    ) for atom, pattern in enumerate(VELOCITY_PATTERN))
    center = tuple(
        fsum(mass * v[axis] for mass, v in zip(MASSES_U, varied, strict=True))
        / fsum(MASSES_U) for axis in range(3)
    )
    centered = tuple(tuple(v[axis] - center[axis] for axis in range(3))
                     for v in varied)
    energy_twice = (
        fsum(mass * fsum(component**2 for component in v)
             for mass, v in zip(MASSES_U, centered, strict=True))
        * U_TO_KG * (BOHR_TO_M / TIME_TO_S)**2
    )
    factor = sqrt(18 * BOLTZMANN * 850.0 / energy_twice)
    return tuple(tuple(factor * x for x in v) for v in centered)


def _initial_digest(velocities: tuple) -> str:
    input_state = {
        "species": SPECIES,
        "positions_bohr": tuple(tuple(EDGE_BOHR / 18.0 * x for x in point)
                                for point in BASE_POSITIONS),
        "cell_bohr": ((10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0)),
        "periodic": (True, True, True),
        "velocities_bohr_per_fs": velocities,
        "masses_u": MASSES_U,
        "initial_step": 0,
        "initial_time_code": 0.0,
    }
    raw = json.dumps(input_state, separators=(",", ":"), sort_keys=True,
                     allow_nan=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _reference(chains: tuple[tuple[float, ...], ...]) -> dict[str, object]:
    count, samples = len(chains), len(chains[0])
    half = samples // 2
    parts = tuple(part for row in chains for part in (row[:half], row[-half:]))
    within = mean(stdev(part)**2 for part in parts)
    between = half * stdev(tuple(mean(part) for part in parts))**2
    rhat = sqrt(((half - 1) * within + between) / (half * within)) if within else None

    centers = tuple(mean(row) for row in chains)
    pooled_variance = fsum(
        fsum((value - center)**2 for value in row) / samples
        for row, center in zip(chains, centers, strict=True)
    ) / count
    if pooled_variance == 0.0:
        lag_one = tau = ess = None
    else:
        correlations = []
        for lag in range(1, samples):
            covariance = fsum(
                fsum((row[i] - center) * (row[i + lag] - center)
                     for i in range(samples - lag)) / (samples - lag)
                for row, center in zip(chains, centers, strict=True)
            ) / count
            correlations.append(max(-1.0, min(1.0, covariance / pooled_variance)))
        lag_one = correlations[0]
        pairs = []
        for index in range(0, len(correlations) - 1, 2):
            pair = correlations[index] + correlations[index + 1]
            if pair <= 0.0:
                break
            pairs.append(min(pair, pairs[-1]) if pairs else pair)
        tau = max(1.0, 1.0 + 2.0 * fsum(pairs))
        ess = count * samples / tau

    shifts = []
    for row in chains:
        half_difference = abs(mean(row[-half:]) - mean(row[:half]))
        sample_sd = stdev(row)
        shifts.append(half_difference / sample_sd if sample_sd
                      else (0.0 if half_difference == 0.0 else None))
    drift = max(shifts) if all(value is not None for value in shifts) else None

    constant = all(value == chains[0][0] for row in chains for value in row)
    if constant:
        status = "FIXED_SERIES_CONSTANT"
    elif None in (rhat, lag_one, tau, ess, drift):
        status = "WITHIN_REPLICA_VARIANCE_ZERO"
    elif (rhat <= CRITERIA["maximum_split_rhat"]
          and ess >= CRITERIA["minimum_effective_sample_size"]
          and abs(lag_one) <= CRITERIA["maximum_absolute_lag_one_correlation"]
          and drift <= CRITERIA["maximum_standardized_half_window_shift"]):
        status = "SCREENING_CRITERIA_MET"
    else:
        status = "SCREENING_CRITERIA_FLAGGED"
    return {
        "replica_means": centers,
        "split_rhat": rhat,
        "pooled_lag_one_autocorrelation": lag_one,
        "positive_pair_autocorrelation_time_samples": tau,
        "effective_sample_size_proxy": ess,
        "maximum_standardized_half_window_shift": drift,
        "diagnostic_status": status,
    }


def _audit_protocol(data: dict) -> None:
    assert data["benchmark_id"] == BENCHMARK_ID
    assert data["status"] == "PASS"
    assert set(data["checks"]) == CHECK_NAMES
    assert all(v is True for v in data["checks"].values())
    assert data["source"] == {
        "doi": SOURCE_DOI,
        "relative_path": "data/reference/flibe_smith_2020_pim_pair_coefficients.json",
        "sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "provenance": "PRIMARY_SOURCE",
    }
    assert data["protocol"] == {
        "model_id": MODEL_ID,
        "md_ensemble": "NVE_FIXED_CELL",
        "cell_edge_bohr": EDGE_BOHR,
        "species": list(SPECIES),
        "time_step_code": 0.01,
        "time_unit_to_second": TIME_TO_S,
        "integration_steps": 16,
        "sampling_stride": 2,
        "replica_count": 4,
        "windows": [list(item) for item in WINDOWS],
        "stationarity_estimator": METHOD_ID,
        "statistical_independence_qualification": "UNASSESSED",
        "thermodynamic_state_qualification": "UNASSESSED",
        "architectural_scope": {
            "executed_layer": "PERIODIC_POLARIZABLE_INTERATOMIC_MD",
            "continuous_resonance_coupling": "SEPARATE_CONTRACT",
            "balanced_ternary_execution": "SEPARATE_CONTRACT",
            "equivariant_mapping_coupling": "SEPARATE_CONTRACT",
        },
    }


def _audit_replicas(data: dict) -> None:
    rows = data["replicas"]
    assert isinstance(rows, list) and len(rows) == 4
    expected_density = fsum(MASSES_U) * U_TO_KG / (EDGE_BOHR * BOHR_TO_M)**3
    expected_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    fingerprints = set()
    for index, row in enumerate(rows):
        assert row["replica_id"] == f"REPLICA-{index:02d}"
        assert row["trajectory_id"] == f"FLIBE-PERIODIC-REPLICA-{index:02d}"
        assert row["source_file_sha256"] == expected_hash
        assert _number(row["maximum_absolute_energy_change_hartree"]) >= 0.0
        assert 0.0 <= _number(row["maximum_dipole_stationarity_residual_atomic"]) <= 1.0e-10
        velocities = _velocities(index)
        for actual, target in zip(row["initial_velocities_bohr_per_fs"], velocities, strict=True):
            assert len(actual) == 3
            for value, desired in zip(actual, target, strict=True):
                _near(value, desired, atol=1.0e-14)
        for axis in range(3):
            assert abs(fsum(m * v[axis] for m, v in zip(MASSES_U, velocities, strict=True))) <= 1.0e-12
        digest = _initial_digest(velocities)
        assert row["initial_condition_sha256"] == digest
        fingerprints.add(digest)
        samples = row["samples"]
        assert isinstance(samples, list) and len(samples) == 9
        for n, sample in enumerate(samples):
            assert sample["state_index"] == sample["md_step"] == 2 * n
            _near(sample["md_time_code"], n * SAMPLE_STEP, atol=1.0e-14)
            _near(sample["density_kg_m3"], expected_density)
            assert _number(sample["temperature_k"]) >= 0.0
            _number(sample["signed_pressure_pa"])
        _near(samples[0]["temperature_k"], 850.0)
    assert len(fingerprints) == 4


def _audit_windows(data: dict) -> None:
    records = data["replicas"]
    assert len(data["windows"]) == len(WINDOWS)
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    for actual, (tag, discard, length) in zip(data["windows"], WINDOWS, strict=True):
        assert actual["window_id"] == tag
        assert actual["method_id"] == METHOD_ID
        assert actual["model_id"] == MODEL_ID
        assert actual["parameter_source_sha256"] == source_hash
        assert actual["provenance"] == "BENCHMARK"
        assert actual["velocity_frame"] == "CENTER_OF_MASS"
        assert actual["physical_state_id"] == "UNCLASSIFIED_MD_PHASE"
        assert actual["physical_state_method_id"] == "DECLARED_UNCLASSIFIED_BENCHMARK_STATE"
        assert actual["replica_ids"] == [row["replica_id"] for row in records]
        assert actual["initial_condition_sha256"] == [
            row["initial_condition_sha256"] for row in records
        ]
        assert actual["discarded_initial_samples"] == discard
        assert actual["retained_samples_per_replica"] == length
        assert actual["central_sample_dropped_per_replica"] == length % 2
        _near(actual["sampling_interval_s"], SAMPLE_STEP * TIME_TO_S, atol=1.0e-29)
        _near(actual["observed_duration_s"], (length - 1) * SAMPLE_STEP * TIME_TO_S,
              atol=1.0e-29)
        assert actual["criteria"] == CRITERIA
        assert set(actual["observables"]) == {field[0] for field in FIELDS}
        for name, raw_field, unit in FIELDS:
            measured = actual["observables"][name]
            chains = tuple(tuple(sample[raw_field] for sample in row["samples"][discard:discard + length])
                           for row in records)
            expected = _reference(chains)
            assert measured["unit"] == unit
            assert len(measured["replica_means"]) == len(records)
            for x, y in zip(measured["replica_means"], expected["replica_means"], strict=True):
                _near(x, y)
            for field in (
                "split_rhat", "pooled_lag_one_autocorrelation",
                "positive_pair_autocorrelation_time_samples", "effective_sample_size_proxy",
                "maximum_standardized_half_window_shift",
            ):
                _optional_near(measured[field], expected[field])
            assert measured["diagnostic_status"] == expected["diagnostic_status"]


def _audit_all(data: dict) -> None:
    _audit_protocol(data)
    _audit_replicas(data)
    _audit_windows(data)


def test_canonical_json_and_registered_benchmark_contract(execution):
    report, raw = execution
    assert raw.decode("utf-8") == json.dumps(
        report, sort_keys=True, indent=2, allow_nan=False
    ) + "\n"
    _audit_protocol(report)


def test_microstate_fingerprints_and_periodic_mass_density(report):
    _audit_replicas(report)


@pytest.mark.parametrize("index", (0, 1))
def test_independent_split_rhat_ess_and_drift_for_both_windows(report, index):
    tag, discard, length = WINDOWS[index]
    recorded = report["windows"][index]
    assert recorded["window_id"] == tag
    for name, raw_field, unit in FIELDS:
        values = tuple(
            tuple(sample[raw_field] for sample in replica["samples"][discard:discard + length])
            for replica in report["replicas"]
        )
        expected = _reference(values)
        measured = recorded["observables"][name]
        assert measured["unit"] == unit
        for field in (
            "split_rhat", "pooled_lag_one_autocorrelation",
            "positive_pair_autocorrelation_time_samples", "effective_sample_size_proxy",
            "maximum_standardized_half_window_shift",
        ):
            _optional_near(measured[field], expected[field])
        assert measured["diagnostic_status"] == expected["diagnostic_status"]


def test_numerical_acceptance_and_sampling_screening_remain_distinct(report):
    assert report["status"] == "PASS"
    assert all(
        window["observables"][name]["diagnostic_status"] == "SCREENING_CRITERIA_FLAGGED"
        for window in report["windows"] for name in ("temperature", "pressure")
    )
    assert all(
        window["observables"]["density"]["diagnostic_status"] == "FIXED_SERIES_CONSTANT"
        for window in report["windows"]
    )
    for window in report["windows"]:
        for name in ("temperature", "pressure"):
            assert window["observables"][name]["effective_sample_size_proxy"] < 40.0
    assert report["protocol"]["statistical_independence_qualification"] == "UNASSESSED"
    assert report["protocol"]["thermodynamic_state_qualification"] == "UNASSESSED"


@pytest.mark.parametrize("mutation", (
    "source", "architecture", "replica_identity", "initial_microstate", "velocity",
    "temperature", "density", "pressure", "sampling_time", "energy", "dipole",
    "window_length", "window_digest", "window_units", "rhat", "ess", "drift",
    "correlation", "density_status", "screening_threshold",
))
def test_independent_checks_detect_modified_evidence(report, mutation):
    altered = copy.deepcopy(report)
    if mutation == "source":
        altered["source"]["sha256"] = "0" * 64
    elif mutation == "architecture":
        altered["protocol"]["architectural_scope"]["balanced_ternary_execution"] = "EXECUTED"
    elif mutation == "replica_identity":
        altered["replicas"][1]["replica_id"] = altered["replicas"][0]["replica_id"]
    elif mutation == "initial_microstate":
        altered["replicas"][0]["initial_condition_sha256"] = "0" * 64
    elif mutation == "velocity":
        altered["replicas"][1]["initial_velocities_bohr_per_fs"][0][0] += 0.01
    elif mutation == "temperature":
        altered["replicas"][0]["samples"][0]["temperature_k"] += 5.0
    elif mutation == "density":
        altered["replicas"][0]["samples"][4]["density_kg_m3"] *= 1.01
    elif mutation == "pressure":
        altered["replicas"][0]["samples"][5]["signed_pressure_pa"] += 1.0e7
    elif mutation == "sampling_time":
        altered["replicas"][0]["samples"][4]["md_time_code"] += 0.01
    elif mutation == "energy":
        altered["replicas"][0]["maximum_absolute_energy_change_hartree"] = -1.0
    elif mutation == "dipole":
        altered["replicas"][0]["maximum_dipole_stationarity_residual_atomic"] = 1.0
    elif mutation == "window_length":
        altered["windows"][1]["retained_samples_per_replica"] = 9
    elif mutation == "window_digest":
        altered["windows"][0]["parameter_source_sha256"] = "f" * 64
    elif mutation == "window_units":
        altered["windows"][1]["observables"]["pressure"]["unit"] = "K"
    elif mutation == "rhat":
        altered["windows"][0]["observables"]["temperature"]["split_rhat"] = 1.0
    elif mutation == "ess":
        altered["windows"][1]["observables"]["temperature"]["effective_sample_size_proxy"] += 4.0
    elif mutation == "drift":
        altered["windows"][1]["observables"]["pressure"]["maximum_standardized_half_window_shift"] = 0.0
    elif mutation == "correlation":
        altered["windows"][0]["observables"]["pressure"]["pooled_lag_one_autocorrelation"] = 0.0
    elif mutation == "density_status":
        altered["windows"][0]["observables"]["density"]["diagnostic_status"] = "SCREENING_CRITERIA_MET"
    elif mutation == "screening_threshold":
        altered["windows"][1]["criteria"]["maximum_split_rhat"] = 2.0
    with pytest.raises((AssertionError, KeyError, TypeError)):
        _audit_all(altered)
