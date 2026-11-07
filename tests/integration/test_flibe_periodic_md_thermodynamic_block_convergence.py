
"""Independent qualification of periodic FLiBe thermodynamic block evidence.

Reconstruct density, temperature, signed pressure, per-block statistics,
window sensitivity, and correlation flags from the serialized MD samples.
Registered source identity, sample timing, and deterministic replay are
checked independently of the benchmark's reported acceptance booleans.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
from math import hypot, isclose, isfinite, sqrt
from pathlib import Path
from statistics import correlation, mean, stdev

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_md_thermodynamic_block_convergence.py"
SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-thermodynamic-block-convergence.v1"
SOURCE_DOI = "10.1016/j.molliq.2019.112165"
SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
WINDOWS = (
    ("all_four_frame_blocks", 4, 0, 8),
    ("all_eight_frame_blocks", 8, 0, 4),
    ("discard_eight_samples", 4, 8, 6),
    ("discard_sixteen_samples", 4, 16, 4),
)
OBSERVABLES = (
    ("temperature", "kinetic_temperature_k", "K"),
    ("pressure", "signed_pressure_pa", "Pa"),
    ("density", "density_kg_m3", "kg/m^3"),
)
CHECKS = {
    "registered_parameter_fingerprint",
    "expected_species_and_periodic_cell",
    "exact_stride_and_sample_count",
    "density_mass_volume_identity",
    "aligned_thermodynamic_samples",
    "kinetic_temperature_identity",
    "signed_pressure_decomposition",
    "initial_kinetic_temperature_target",
    "predeclared_nonoverlapping_block_windows",
    "independently_recomputed_block_moments",
    "block_grouping_preserves_full_sample_mean",
    "finite_sampling_diagnostics",
    "constant_fixed_cell_density",
    "finite_md_energy_drift",
    "sampling_diagnostic_bookkeeping",
}
BOHR_TO_M = 5.29177210903e-11
U_TO_KG = 1.66053906660e-27
BOLTZMANN_J_PER_K = 1.380649e-23
DEGREES_OF_FREEDOM = 3 * (len(SPECIES) - 1)
TOTAL_MASS_U = 2 * 6.94 + 9.0121831 + 4 * 18.998403163


def _number(value: object) -> float:
    assert type(value) in (int, float)
    number = float(value)
    assert isfinite(number)
    return number


def _near(actual: object, expected: float, *, absolute: float = 1.0e-10) -> None:
    assert isclose(_number(actual), expected, rel_tol=1.0e-11, abs_tol=absolute)


def _execute() -> tuple[dict, bytes]:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), environment.get("PYTHONPATH", "")) if part
    )
    result = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        check=False,
        timeout=420,
    )
    assert result.returncode == 0, (
        result.stderr.decode("utf-8", errors="replace")
        + result.stdout.decode("utf-8", errors="replace")[-3000:]
    )
    assert result.stderr == b""
    report = json.loads(result.stdout)
    assert isinstance(report, dict)
    return report, result.stdout


@pytest.fixture(scope="module")
def execution() -> tuple[dict, bytes]:
    assert BENCHMARK.is_file() and SOURCE.is_file()
    return _execute()


@pytest.fixture(scope="module")
def report(execution) -> dict:
    return execution[0]


def _audit_identity(document: dict) -> None:
    assert document["benchmark_id"] == BENCHMARK_ID
    assert document["status"] == "PASS"
    assert set(document["checks"]) == CHECKS
    assert all(value is True for value in document["checks"].values())
    assert document["source"] == {
        "doi": SOURCE_DOI,
        "relative_path": "data/reference/flibe_smith_2020_pim_pair_coefficients.json",
        "sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "provenance": "PRIMARY_SOURCE",
    }
    method = document["protocol"]
    assert method["model_id"] == "FLIBE-PERIODIC-MD-THERMODYNAMIC-BLOCKS"
    assert method["trajectory_id"] == "FLIBE-PERIODIC-THERMODYNAMIC-SAMPLING"
    assert method["ensemble"] == "NVE_FIXED_CELL"
    assert method["velocity_frame"] == "CENTER_OF_MASS"
    assert method["physical_state_id"] == "UNCLASSIFIED_MD_PHASE"
    assert method["species"] == list(SPECIES)
    assert method["cell_edge_bohr"] == 10.0
    assert method["kinetic_temperature_initial_target_k"] == 850.0
    assert method["integration_steps"] == 63
    assert method["sample_stride"] == 2
    assert method["time_step_code"] == 0.01
    assert method["time_unit_to_second"] == 1.0e-15
    assert method["strain_step"] == 2.0e-5
    assert method["block_windows"] == [list(item[:3]) for item in WINDOWS]
    assert method["statistical_interpretation"] == (
        "SAMPLING_WINDOW_AND_BLOCK_SIZE_SENSITIVITY"
    )


def _audit_trajectory(document: dict) -> None:
    trajectory = document["trajectory"]
    samples = trajectory["samples"]
    assert trajectory["sample_count"] == len(samples) == 32
    assert isinstance(samples, list)
    total_mass = TOTAL_MASS_U * U_TO_KG
    volume = (10.0 * BOHR_TO_M) ** 3
    _near(trajectory["total_cell_mass_kg"], total_mass, absolute=1.0e-38)
    assert 0.0 <= _number(trajectory["maximum_absolute_energy_drift_hartree"]) < 1.0e-6
    for index, sample in enumerate(samples):
        assert sample["state_index"] == sample["md_step"] == 2 * index
        _near(sample["md_time_code"], 0.02 * index, absolute=1.0e-13)
        _near(sample["volume_m3"], volume, absolute=1.0e-38)
        _near(sample["density_kg_m3"], total_mass / volume)
        kinetic_energy = _number(sample["kinetic_energy_j"])
        assert kinetic_energy >= 0.0
        _near(sample["kinetic_temperature_k"],
              2.0 * kinetic_energy / (DEGREES_OF_FREEDOM * BOLTZMANN_J_PER_K))
        _near(sample["kinetic_pressure_pa"], 2.0 * kinetic_energy / (3.0 * volume),
              absolute=1.0e-3)
        _near(sample["signed_pressure_pa"],
              _number(sample["kinetic_pressure_pa"])
              + _number(sample["configurational_pressure_pa"]), absolute=1.0e-3)
    _near(samples[0]["kinetic_temperature_k"], 850.0)
    assert all(sample["density_kg_m3"] == samples[0]["density_kg_m3"] for sample in samples)


def _reference_observable(values: tuple[float, ...], size: int) -> dict:
    blocks = tuple(values[i:i + size] for i in range(0, len(values), size))
    block_means = tuple(mean(block) for block in blocks)
    middle = len(block_means) // 2
    left, right = block_means[:-1], block_means[1:]
    adjacent = (
        correlation(left, right)
        if len(block_means) >= 3 and stdev(left) > 0.0 and stdev(right) > 0.0
        else None
    )
    return {
        "mean": mean(values),
        "sample_standard_deviation": stdev(values),
        "block_means": block_means,
        "block_mean_standard_error": stdev(block_means) / sqrt(len(block_means)),
        "second_half_minus_first_half": (
            mean(block_means[middle:]) - mean(block_means[:middle])
        ),
        "lag_one_block_correlation": adjacent,
    }


def _audit_windows(document: dict) -> None:
    samples = document["trajectory"]["samples"]
    observed = document["windows"]
    assert len(observed) == len(WINDOWS)
    for row, (name, size, discard, count) in zip(observed, WINDOWS, strict=True):
        assert row["window_id"] == name
        assert row["block_size_samples"] == size
        assert row["discarded_initial_samples"] == discard
        assert row["discarded_tail_samples"] == 0
        assert row["block_count"] == count
        assert row["selected_sample_count"] == len(samples) - discard == size * count
        assert row["first_state_index"] == 2 * discard
        assert row["last_state_index"] == 62
        _near(row["sampling_interval_s"], 2.0e-17, absolute=1.0e-29)
        assert row["block_state_ranges"] == [
            [2 * (discard + i * size), 2 * (discard + (i + 1) * size - 1)]
            for i in range(count)
        ]
        for symbol, source_key, unit in OBSERVABLES:
            record = row[symbol]
            assert record["unit"] == unit
            values = tuple(_number(sample[source_key]) for sample in samples[discard:])
            expected = _reference_observable(values, size)
            for key in (
                "mean", "sample_standard_deviation", "block_mean_standard_error",
                "second_half_minus_first_half",
            ):
                _near(record[key], expected[key], absolute=1.0e-8)
            assert len(record["block_means"]) == count
            for actual, target in zip(record["block_means"], expected["block_means"], strict=True):
                _near(actual, target, absolute=1.0e-8)
            if expected["lag_one_block_correlation"] is None:
                assert record["lag_one_block_correlation"] is None
            else:
                _near(record["lag_one_block_correlation"],
                      expected["lag_one_block_correlation"], absolute=1.0e-10)


def _audit_sensitivity(document: dict) -> None:
    full, wide, late_eight, late_sixteen = document["windows"]
    for symbol, _, _ in OBSERVABLES:
        expected = {
            "eight_frame_minus_four_frame_mean": wide[symbol]["mean"] - full[symbol]["mean"],
            "discard_eight_minus_full_mean": late_eight[symbol]["mean"] - full[symbol]["mean"],
            "discard_sixteen_minus_full_mean": late_sixteen[symbol]["mean"] - full[symbol]["mean"],
            "eight_frame_minus_four_frame_standard_error": (
                wide[symbol]["block_mean_standard_error"]
                - full[symbol]["block_mean_standard_error"]
            ),
        }
        assert set(document["sensitivity"][symbol]) == set(expected)
        for field, target in expected.items():
            _near(document["sensitivity"][symbol][field], target, absolute=1.0e-8)
        _near(full[symbol]["mean"], wide[symbol]["mean"], absolute=1.0e-8)


def _audit_diagnostics(document: dict) -> None:
    screening = document["statistical_screening"]
    assert screening["scope"] == "DIAGNOSTIC_SAMPLING_CRITERIA"
    assert screening["comparison_windows_overlap"] is True
    assert screening["max_abs_adjacent_block_correlation"] == 0.5
    assert screening["max_block_se_change_fraction"] == 0.25
    assert screening["max_window_mean_shift_scaled_by_se"] == 1.0
    assert set(screening["observables"]) == {item[0] for item in OBSERVABLES}
    full, wide, _, late = document["windows"]
    samples = document["trajectory"]["samples"]
    for symbol, source_key, _ in OBSERVABLES:
        values = tuple(sample[source_key] for sample in samples)
        record = screening["observables"][symbol]
        full_se = _number(full[symbol]["block_mean_standard_error"])
        wide_se = _number(wide[symbol]["block_mean_standard_error"])
        late_se = _number(late[symbol]["block_mean_standard_error"])
        shift = late[symbol]["mean"] - full[symbol]["mean"]
        combined = hypot(full_se, late_se)
        scaled = abs(shift) / combined if combined else (0.0 if shift == 0.0 else None)
        larger = max(full_se, wide_se)
        change = abs(wide_se - full_se) / larger if larger else 0.0
        correlation_value = full[symbol]["lag_one_block_correlation"]
        weak = correlation_value is not None and abs(correlation_value) <= 0.5
        window_good = scaled is not None and scaled <= 1.0
        se_good = change <= 0.25
        constant = all(value == values[0] for value in values)
        status = (
            "FIXED_CELL_CONSTANT" if constant else
            "SCREENING_CRITERIA_MET" if weak and window_good and se_good
            else "SCREENING_CRITERIA_FLAGGED"
        )
        _near(record["mean_shift_last_sixteen_minus_full"], shift, absolute=1.0e-8)
        _near(record["block_se_change_fraction"], change, absolute=1.0e-10)
        if scaled is None:
            assert record["mean_shift_scaled_by_quadrature_block_se"] is None
        else:
            _near(record["mean_shift_scaled_by_quadrature_block_se"], scaled,
                  absolute=1.0e-10)
        if correlation_value is None:
            assert record["lag_one_block_correlation"] is None
        else:
            _near(record["lag_one_block_correlation"], correlation_value,
                  absolute=1.0e-10)
        assert record["weak_adjacent_block_correlation"] is weak
        assert record["window_mean_shift_within_threshold"] is window_good
        assert record["block_size_se_within_threshold"] is se_good
        assert record["diagnostic_status"] == status


def _audit_full(document: dict) -> None:
    _audit_identity(document)
    _audit_trajectory(document)
    _audit_windows(document)
    _audit_sensitivity(document)
    _audit_diagnostics(document)


def test_registered_benchmark_and_source_identity(report):
    _audit_identity(report)


def test_independent_mass_volume_temperature_pressure_and_sampling(report):
    _audit_trajectory(report)


def test_all_twelve_window_observables_against_independent_statistics(report):
    _audit_windows(report)


def test_all_window_and_block_size_sensitivities(report):
    _audit_sensitivity(report)


def test_diagnostic_criteria_recomputed_from_raw_frames(report):
    _audit_diagnostics(report)


def test_temperature_and_pressure_drift_remains_explicitly_flagged(report):
    results = report["statistical_screening"]["observables"]
    assert results["temperature"]["diagnostic_status"] == "SCREENING_CRITERIA_FLAGGED"
    assert results["pressure"]["diagnostic_status"] == "SCREENING_CRITERIA_FLAGGED"
    assert results["density"]["diagnostic_status"] == "FIXED_CELL_CONSTANT"
    assert results["temperature"]["lag_one_block_correlation"] > 0.99
    assert results["pressure"]["lag_one_block_correlation"] > 0.99
    assert results["density"]["lag_one_block_correlation"] is None


def test_canonical_json_and_deterministic_reexecution(execution):
    document, raw = execution
    assert raw.decode("utf-8") == json.dumps(
        document, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"
    repeated, second_raw = _execute()
    assert repeated == document
    assert second_raw == raw


@pytest.mark.parametrize("mutation", (
    "hash", "sampling_step", "density", "kinetic_temperature",
    "pressure", "window_count", "block_mean", "block_error",
    "block_correlation", "sensitivity", "screening_flag", "screening_status",
))
def test_modified_record_is_detected(report, mutation):
    damaged = copy.deepcopy(report)
    if mutation == "hash":
        damaged["source"]["sha256"] = "0" * 64
    elif mutation == "sampling_step":
        damaged["trajectory"]["samples"][3]["md_step"] += 1
    elif mutation == "density":
        damaged["trajectory"]["samples"][5]["density_kg_m3"] *= 1.01
    elif mutation == "kinetic_temperature":
        damaged["trajectory"]["samples"][5]["kinetic_temperature_k"] *= 1.01
    elif mutation == "pressure":
        damaged["trajectory"]["samples"][5]["signed_pressure_pa"] += 1.0e7
    elif mutation == "window_count":
        damaged["windows"][1]["block_count"] += 1
    elif mutation == "block_mean":
        damaged["windows"][2]["temperature"]["block_means"][0] += 1.0
    elif mutation == "block_error":
        damaged["windows"][0]["pressure"]["block_mean_standard_error"] *= 1.2
    elif mutation == "block_correlation":
        damaged["windows"][0]["temperature"]["lag_one_block_correlation"] = 0.0
    elif mutation == "sensitivity":
        damaged["sensitivity"]["temperature"]["discard_eight_minus_full_mean"] += 1.0
    elif mutation == "screening_flag":
        damaged["statistical_screening"]["observables"]["pressure"][
            "weak_adjacent_block_correlation"
        ] = True
    elif mutation == "screening_status":
        damaged["statistical_screening"]["observables"]["temperature"][
            "diagnostic_status"
        ] = "SCREENING_CRITERIA_MET"
    with pytest.raises(AssertionError):
        _audit_full(damaged)
