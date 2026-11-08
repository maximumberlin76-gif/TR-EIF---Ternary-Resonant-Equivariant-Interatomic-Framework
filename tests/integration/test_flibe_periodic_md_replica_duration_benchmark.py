
"""Independent integration qualification of FLiBe MD replica-duration evidence.

Reconstruct the initial microstates, SI density, per-replica observations,
block statistics, duration changes and between-replica standard errors from
the benchmark's serialized output. Each output mutation is audited against
independently recomputed evidence. One CLI execution supplies all tests.
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
from statistics import mean, median, stdev

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_md_replica_duration_benchmark.py"
PAIR_SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-replica-duration-convergence.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
MODEL_ID = "FLIBE-PERIODIC-REPLICA-DURATION-BENCHMARK"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
MASS_BY_SPECIES = {"Li": 6.94, "Be": 9.0121831, "F": 18.998403163}
MASS_U = tuple(MASS_BY_SPECIES[symbol] for symbol in SPECIES)
POSITIONS_BASE = (
    (0.0, 0.0, 0.0), (8.0, 0.0, 0.0), (4.0, 7.0, 0.0),
    (2.0, 1.0, 6.0), (8.0, 5.0, 6.0), (1.0, 8.0, 8.0),
    (8.0, 10.0, 11.0),
)
VELOCITY_PATTERN = (
    (0.03, 0.01, 0.0), (-0.03, -0.01, 0.02), (0.02, 0.03, -0.02),
    (0.0, -0.02, 0.01), (0.01, 0.005, -0.02),
    (-0.015, 0.02, 0.0), (-0.015, -0.015, 0.01),
)
CELL_EDGE_BOHR = 10.0
BOHR_TO_M = 5.29177210903e-11
MASS_U_TO_KG = 1.66053906660e-27
TIME_TO_S = 1.0e-15
BOLTZMANN = 1.380649e-23
INITIAL_TEMPERATURE_K = 850.0
REPLICAS = 4
SAMPLES_PER_REPLICA = 9
DISCARD = 1
BLOCK_SIZE = 2
DURATIONS = (4, 6, 8)
FIELDS = (
    ("temperature", "temperature_k", "K"),
    ("pressure", "signed_pressure_pa", "Pa"),
    ("density", "density_kg_m3", "kg/m^3"),
)
CHECKS = {
    "source_fingerprint_and_doi",
    "identical_first_replica_replay",
    "zero_center_of_mass_initial_velocity",
    "different_initial_conditions",
    "uniform_replica_protocol",
    "aligned_times_and_steps",
    "common_initial_kinetic_temperature",
    "mass_volume_density_identity",
    "dipole_stationarity",
    "finite_energy_drift_and_observables",
    "complete_duration_replica_matrix",
    "source_and_sampling_provenance",
    "independent_replica_mean_and_se_recalculation",
    "diagnostic_values_finite_or_undefined",
}


def _number(value: object) -> float:
    assert type(value) in (int, float)
    result = float(value)
    assert isfinite(result)
    return result


def _near(actual: object, expected: float, *, atol: float = 1.0e-9) -> None:
    assert isclose(_number(actual), expected, rel_tol=1.0e-11, abs_tol=atol)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cli() -> tuple[dict, bytes]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        entry for entry in (str(ROOT / "src"), env.get("PYTHONPATH", "")) if entry
    )
    completed = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT, env=env, capture_output=True, check=False, timeout=420,
    )
    assert completed.returncode == 0, (
        completed.stderr.decode("utf-8", errors="replace")
        + completed.stdout.decode("utf-8", errors="replace")[-3000:]
    )
    assert completed.stderr == b""
    result = json.loads(completed.stdout)
    assert isinstance(result, dict)
    return result, completed.stdout


@pytest.fixture(scope="module")
def execution() -> tuple[dict, bytes]:
    assert BENCHMARK.is_file() and PAIR_SOURCE.is_file()
    return _cli()


@pytest.fixture(scope="module")
def report(execution) -> dict:
    return execution[0]


def _initial_velocities(replica_index: int) -> tuple[tuple[float, ...], ...]:
    varied = tuple(
        (
            base[0] + 0.0010 * replica_index * ((atom % 3) - 1),
            base[1] + 0.0015 * replica_index * (((atom + 1) % 3) - 1),
            base[2] + 0.0008 * replica_index * (((atom + 2) % 3) - 1),
        )
        for atom, base in enumerate(VELOCITY_PATTERN)
    )
    mass_sum = fsum(MASS_U)
    center = tuple(
        fsum(m * velocity[a] for m, velocity in zip(MASS_U, varied, strict=True))
        / mass_sum for a in range(3)
    )
    centered = tuple(tuple(v[a] - center[a] for a in range(3)) for v in varied)
    twice_kinetic = (
        fsum(m * fsum(x * x for x in v) for m, v in zip(MASS_U, centered, strict=True))
        * MASS_U_TO_KG * (BOHR_TO_M / TIME_TO_S) ** 2
    )
    scale = sqrt(3 * (len(SPECIES) - 1) * BOLTZMANN * INITIAL_TEMPERATURE_K
                 / twice_kinetic)
    return tuple(tuple(scale * x for x in v) for v in centered)


def _initial_digest(velocities: tuple[tuple[float, ...], ...]) -> str:
    data = {
        "species": SPECIES,
        "positions_bohr": tuple(
            tuple(CELL_EDGE_BOHR / 18.0 * coordinate for coordinate in point)
            for point in POSITIONS_BASE
        ),
        "cell_bohr": ((10.0, 0.0, 0.0), (0.0, 10.0, 0.0), (0.0, 0.0, 10.0)),
        "periodic": (True, True, True),
        "velocities_bohr_per_fs": velocities,
        "masses_u": MASS_U,
        "initial_step": 0,
        "initial_time_code": 0.0,
    }
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _audit_identity(data: dict) -> None:
    assert data["benchmark_id"] == BENCHMARK_ID
    assert data["status"] == "PASS"
    assert set(data["checks"]) == CHECKS
    assert all(value is True for value in data["checks"].values())
    assert data["source"] == {
        "doi": SOURCE_DOI,
        "relative_path": "data/reference/flibe_smith_2020_pim_pair_coefficients.json",
        "sha256": _sha256(PAIR_SOURCE),
        "provenance": "PRIMARY_SOURCE",
    }
    protocol = data["protocol"]
    assert protocol["model_id"] == MODEL_ID
    assert protocol["ensemble"] == "NVE_FIXED_CELL"
    assert protocol["species"] == list(SPECIES)
    assert protocol["cell_edge_bohr"] == CELL_EDGE_BOHR
    assert protocol["initial_kinetic_temperature_target_k"] == INITIAL_TEMPERATURE_K
    assert protocol["time_step_code"] == 0.01
    assert protocol["time_unit_to_second"] == TIME_TO_S
    assert protocol["integration_steps"] == 16
    assert protocol["sampling_stride"] == 2
    assert protocol["replica_count"] == REPLICAS
    assert protocol["discard_initial_samples"] == DISCARD
    assert protocol["block_size_samples"] == BLOCK_SIZE
    assert protocol["retained_sample_lengths"] == list(DURATIONS)
    assert protocol["stress_strain_step"] == 2.0e-5
    assert protocol["velocity_frame"] == "CENTER_OF_MASS"
    assert protocol["physical_state_id"] == "UNCLASSIFIED_MD_PHASE"
    assert protocol["statistical_scope"] == "DURATION_AND_REPLICA_COUNT_SENSITIVITY"
    assert protocol["initial_input_distinctness"] == "SHA256_OF_INITIAL_FULL_MICROSTATE"
    assert protocol["statistical_independence_qualification"] == "UNASSESSED"
    assert protocol["equilibrium_qualification"] == "UNASSESSED"


def _audit_replicas(data: dict) -> None:
    records = data["replicas"]
    assert isinstance(records, list) and len(records) == REPLICAS
    expected_density = fsum(MASS_U) * MASS_U_TO_KG / (CELL_EDGE_BOHR * BOHR_TO_M) ** 3
    digests = set()
    velocities_seen = set()
    for index, record in enumerate(records):
        assert record["replica_id"] == f"REPLICA-{index:02d}"
        assert record["trajectory_id"] == f"FLIBE-PERIODIC-REPLICA-{index:02d}"
        assert record["source_file_sha256"] == _sha256(PAIR_SOURCE)
        expected_velocities = _initial_velocities(index)
        actual_velocities = record["initial_velocities_bohr_per_fs"]
        assert len(actual_velocities) == len(SPECIES)
        for actual, expected in zip(actual_velocities, expected_velocities, strict=True):
            assert len(actual) == 3
            for component, reference in zip(actual, expected, strict=True):
                _near(component, reference, atol=1.0e-14)
        for axis in range(3):
            assert abs(fsum(m * row[axis] for m, row in zip(
                MASS_U, actual_velocities, strict=True
            ))) <= 1.0e-12
        kinetic_twice = (
            fsum(m * fsum(v * v for v in row)
                 for m, row in zip(MASS_U, actual_velocities, strict=True))
            * MASS_U_TO_KG * (BOHR_TO_M / TIME_TO_S) ** 2
        )
        _near(kinetic_twice / (18 * BOLTZMANN), INITIAL_TEMPERATURE_K)
        digest = _initial_digest(expected_velocities)
        assert record["initial_condition_sha256"] == digest
        digests.add(digest)
        velocities_seen.add(json.dumps(actual_velocities))
        assert 0 <= _number(record["maximum_dipole_stationarity_residual_atomic"]) <= 1.0e-10
        assert _number(record["maximum_absolute_energy_change_hartree"]) >= 0.0
        samples = record["samples"]
        assert len(samples) == SAMPLES_PER_REPLICA
        for sample_number, sample in enumerate(samples):
            expected_step = 2 * sample_number
            assert sample["state_index"] == sample["md_step"] == expected_step
            _near(sample["md_time_code"], expected_step * 0.01, atol=1.0e-14)
            _near(sample["density_kg_m3"], expected_density)
            _number(sample["signed_pressure_pa"])
            assert _number(sample["temperature_k"]) >= 0.0
        _near(samples[0]["temperature_k"], INITIAL_TEMPERATURE_K)
    assert len(digests) == len(velocities_seen) == REPLICAS


def _correlation(means: tuple[float, ...]) -> float | None:
    if len(means) < 3:
        return None
    left, right = means[:-1], means[1:]
    first, second = mean(left), mean(right)
    left_var = fsum((value - first) ** 2 for value in left)
    right_var = fsum((value - second) ** 2 for value in right)
    if left_var == 0.0 or right_var == 0.0:
        return None
    return fsum((a - first) * (b - second)
                for a, b in zip(left, right, strict=True)) / sqrt(left_var * right_var)


def _ensemble_values(records: list, name: str, duration: int, count: int):
    field = next(key for label, key, _ in FIELDS if label == name)
    raw = [tuple(row[field] for row in record["samples"][DISCARD:DISCARD + duration])
           for record in records[:count]]
    means = tuple(mean(row) for row in raw)
    block_errors = []
    half_shifts = []
    correlations = []
    for row in raw:
        blocks = tuple(mean(row[block:block + BLOCK_SIZE])
                       for block in range(0, len(row), BLOCK_SIZE))
        block_errors.append(stdev(blocks) / sqrt(len(blocks)))
        middle = len(blocks) // 2
        half_shifts.append(abs(mean(blocks[middle:]) - mean(blocks[:middle])))
        correlations.append(_correlation(blocks))
    defined = tuple(abs(value) for value in correlations if value is not None)
    return {
        "trajectory_means": means,
        "mean_of_trajectory_means": mean(means),
        "between_trajectory_sample_sd": stdev(means),
        "between_trajectory_standard_error": stdev(means) / sqrt(count),
        "median_within_trajectory_block_se": median(block_errors),
        "maximum_absolute_half_window_shift": max(half_shifts),
        "maximum_absolute_lag_one_block_correlation": max(defined) if defined else None,
        "undefined_lag_one_correlation_count": len(correlations) - len(defined),
    }


def _audit_matrix(data: dict) -> None:
    convergence = data["convergence"]
    _near(convergence["sampling_interval_s"], 2.0e-17, atol=1.0e-29)
    points = convergence["points"]
    expected_grid = [(duration, count) for duration in DURATIONS for count in (2, 3, 4)]
    assert [(row["retained_samples_per_trajectory"], row["replica_count"])
            for row in points] == expected_grid
    records = data["replicas"]
    for point, (duration, count) in zip(points, expected_grid, strict=True):
        _near(point["observed_duration_s"], (duration - 1) * 2.0e-17, atol=1.0e-29)
        assert point["trajectory_ids"] == [row["trajectory_id"] for row in records[:count]]
        assert point["initial_condition_sha256"] == [
            row["initial_condition_sha256"] for row in records[:count]
        ]
        for name, _, unit in FIELDS:
            actual = point[name]
            assert actual["unit"] == unit
            expected = _ensemble_values(records, name, duration, count)
            assert len(actual["trajectory_means"]) == count
            for x, y in zip(actual["trajectory_means"], expected["trajectory_means"], strict=True):
                _near(x, y)
            for key in (
                "mean_of_trajectory_means", "between_trajectory_sample_sd",
                "between_trajectory_standard_error", "median_within_trajectory_block_se",
                "maximum_absolute_half_window_shift",
            ):
                _near(actual[key], expected[key])
            key = "maximum_absolute_lag_one_block_correlation"
            if expected[key] is None:
                assert actual[key] is None
            else:
                _near(actual[key], expected[key], atol=1.0e-11)
            assert actual["undefined_lag_one_correlation_count"] == (
                expected["undefined_lag_one_correlation_count"]
            )
            previous_index = DURATIONS.index(duration) - 1
            previous_change = (None if previous_index < 0 else
                               expected["mean_of_trajectory_means"] -
                               _ensemble_values(records, name, DURATIONS[previous_index], count)[
                                   "mean_of_trajectory_means"])
            if previous_change is None:
                assert actual["mean_change_from_previous_duration"] is None
            else:
                _near(actual["mean_change_from_previous_duration"], previous_change)


def _audit_screening(data: dict) -> None:
    screening = data["statistical_screening"]
    assert screening["correlation_limit"] == 0.5
    assert screening["duration_shift_scaled_by_se_limit"] == 1.0
    assert set(screening["observables"]) == {name for name, _, _ in FIELDS}
    final = next(point for point in data["convergence"]["points"]
                 if (point["retained_samples_per_trajectory"], point["replica_count"])
                 == (DURATIONS[-1], REPLICAS))
    for name, _, _ in FIELDS:
        summary = final[name]
        actual = screening["observables"][name]
        correlation = summary["maximum_absolute_lag_one_block_correlation"]
        shift = summary["mean_change_from_previous_duration"]
        se = summary["between_trajectory_standard_error"]
        scaled = abs(shift) / se if shift is not None and se > 0.0 else None
        weak = correlation is not None and correlation <= 0.5
        duration_good = scaled is not None and scaled <= 1.0
        constant = name == "density" and all(
            sample["density_kg_m3"] == data["replicas"][0]["samples"][0]["density_kg_m3"]
            for replica in data["replicas"] for sample in replica["samples"]
        )
        expected_status = (
            "FIXED_CELL_CONSTANT" if constant else
            "SCREENING_CRITERIA_MET" if weak and duration_good else
            "SCREENING_CRITERIA_FLAGGED"
        )
        assert actual["diagnostic_status"] == expected_status
        assert actual["weak_block_correlation"] is weak
        assert actual["duration_mean_shift_within_between_replica_se"] is duration_good
        if correlation is None:
            assert actual["maximum_absolute_lag_one_block_correlation"] is None
        else:
            _near(actual["maximum_absolute_lag_one_block_correlation"], correlation, atol=1.0e-11)
        if shift is None:
            assert actual["last_duration_mean_change"] is None
        else:
            _near(actual["last_duration_mean_change"], shift)
        if scaled is None:
            assert actual["last_duration_mean_change_scaled_by_between_replica_se"] is None
        else:
            _near(actual["last_duration_mean_change_scaled_by_between_replica_se"], scaled,
                  atol=1.0e-11)


def _audit_all(data: dict) -> None:
    _audit_identity(data)
    _audit_replicas(data)
    _audit_matrix(data)
    _audit_screening(data)


def test_canonical_report_and_declared_gates(execution):
    report, stdout = execution
    assert stdout.decode("utf-8") == json.dumps(
        report, sort_keys=True, indent=2, allow_nan=False
    ) + "\n"
    _audit_identity(report)


def test_initial_velocities_fingerprints_and_common_temperature(report):
    _audit_replicas(report)


def test_independent_nine_point_duration_by_replica_matrix(report):
    _audit_matrix(report)


def test_statistical_screening_recalculated_from_raw_trajectories(report):
    _audit_screening(report)


def test_distinguishes_numerical_pass_from_statistical_stationarity(report):
    assert report["status"] == "PASS"
    flags = report["statistical_screening"]["observables"]
    assert flags["temperature"]["diagnostic_status"] == "SCREENING_CRITERIA_FLAGGED"
    assert flags["pressure"]["diagnostic_status"] == "SCREENING_CRITERIA_FLAGGED"
    assert flags["density"]["diagnostic_status"] == "FIXED_CELL_CONSTANT"
    assert report["protocol"]["equilibrium_qualification"] == "UNASSESSED"


@pytest.mark.parametrize("alteration", (
    "source", "input_digest", "velocity", "initial_temperature", "density",
    "sampling_time", "energy", "dipole", "matrix_size", "trajectory_mean",
    "between_standard_error", "block_correlation", "duration_change",
    "screening_flag", "screening_status", "physical_scope",
))
def test_corrupted_benchmark_output_is_detected(report, alteration):
    changed = copy.deepcopy(report)
    if alteration == "source":
        changed["source"]["sha256"] = "0" * 64
    elif alteration == "input_digest":
        changed["replicas"][0]["initial_condition_sha256"] = "0" * 64
    elif alteration == "velocity":
        changed["replicas"][1]["initial_velocities_bohr_per_fs"][0][0] += 0.1
    elif alteration == "initial_temperature":
        changed["replicas"][1]["samples"][0]["temperature_k"] += 5.0
    elif alteration == "density":
        changed["replicas"][0]["samples"][4]["density_kg_m3"] *= 1.01
    elif alteration == "sampling_time":
        changed["replicas"][0]["samples"][5]["md_time_code"] += 0.01
    elif alteration == "energy":
        changed["replicas"][0]["maximum_absolute_energy_change_hartree"] = -1.0
    elif alteration == "dipole":
        changed["replicas"][0]["maximum_dipole_stationarity_residual_atomic"] = 1.0
    elif alteration == "matrix_size":
        changed["convergence"]["points"].pop()
    elif alteration == "trajectory_mean":
        changed["convergence"]["points"][0]["temperature"]["trajectory_means"][0] += 2.0
    elif alteration == "between_standard_error":
        changed["convergence"]["points"][1]["pressure"]["between_trajectory_standard_error"] += 1000
    elif alteration == "block_correlation":
        changed["convergence"]["points"][-1]["temperature"]["maximum_absolute_lag_one_block_correlation"] = 0.0
    elif alteration == "duration_change":
        changed["convergence"]["points"][-1]["pressure"]["mean_change_from_previous_duration"] += 1000
    elif alteration == "screening_flag":
        changed["statistical_screening"]["observables"]["temperature"]["weak_block_correlation"] = True
    elif alteration == "screening_status":
        changed["statistical_screening"]["observables"]["pressure"]["diagnostic_status"] = "SCREENING_CRITERIA_MET"
    elif alteration == "physical_scope":
        changed["protocol"]["equilibrium_qualification"] = "CONFIRMED"
    with pytest.raises((AssertionError, KeyError)):
        _audit_all(changed)
