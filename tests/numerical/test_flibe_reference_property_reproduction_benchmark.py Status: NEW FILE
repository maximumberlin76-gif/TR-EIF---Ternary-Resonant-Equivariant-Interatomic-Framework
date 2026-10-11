
"""Executable qualification of the registered FLiBe density benchmark contract.

This test qualifies deterministic benchmark execution and internal consistency;
it does not independently validate the underlying experimental correlation.
"""

from __future__ import annotations

import json
from math import isfinite
from pathlib import Path
import subprocess
import sys


_ROOT = Path(__file__).resolve().parents[2]
_BENCHMARK = _ROOT / "benchmarks" / "flibe" / "reference_property_reproduction.py"
_BENCHMARK_ID = "tr-eif.flibe.reference-property-reproduction.v1"
_SOURCE_ID = "FLIBE-REFERENCE-JANZ-1974-DENSITY"
_EXPECTED_TEMPERATURES = (800.0, 850.0, 900.0, 950.0, 1000.0, 1050.0, 1080.0)
_EXPECTED_CHECKS = {
    "reference_composition",
    "exact_two_to_one_is_distinct",
    "reference_points_inside_registered_range",
    "density_metadata_preserved",
    "reference_values_reproduced",
    "density_decreases_over_registered_samples",
    "outside_domain_rejected",
}


def _execute() -> tuple[dict[str, object], bytes]:
    result = subprocess.run(
        [sys.executable, str(_BENCHMARK)],
        cwd=_ROOT,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert result.stderr == b""
    report = json.loads(result.stdout)
    assert isinstance(report, dict)
    return report, result.stdout


def test_registered_benchmark_present_and_qualified() -> None:
    assert _BENCHMARK.is_file()
    report, _ = _execute()
    assert report["benchmark_id"] == _BENCHMARK_ID
    assert report["provenance"] == "BENCHMARK"
    assert report["source_id"] == _SOURCE_ID
    assert report["status"] == "PASS"
    assert isinstance(report["checks"], dict)
    assert set(report["checks"]) == _EXPECTED_CHECKS
    assert all(value is True for value in report["checks"].values())


def test_registered_domain_and_composition_are_explicit() -> None:
    report, _ = _execute()
    correlation = report["source_correlation"]
    assert correlation == {
        "density_intercept_kg_m3": 2413.0,
        "density_slope_kg_m3_per_k": -0.488,
        "temperature_min_k": 800.0,
        "temperature_max_k": 1080.0,
        "lif_mol_percent": 67.0,
        "bef2_mol_percent": 33.0,
    }
    observed = report["observed"]
    assert observed["exact_two_to_one_lif_fraction"] == 2.0 / 3.0
    assert observed["exact_two_to_one_bef2_fraction"] == 1.0 / 3.0
    assert correlation["lif_mol_percent"] / 100 != observed["exact_two_to_one_lif_fraction"]


def test_density_samples_match_predeclared_correlation() -> None:
    report, _ = _execute()
    tolerance = report["absolute_tolerance_kg_m3"]
    assert tolerance == 1.0e-9
    samples = report["observed"]["samples"]
    assert isinstance(samples, list)
    assert tuple(sample["temperature_k"] for sample in samples) == _EXPECTED_TEMPERATURES
    residuals = []
    densities = []
    for sample in samples:
        temperature = sample["temperature_k"]
        model = sample["model_density_kg_m3"]
        reference = sample["reference_density_kg_m3"]
        residual = sample["residual_kg_m3"]
        assert all(isfinite(value) for value in (temperature, model, reference, residual))
        assert abs(model - (2413.0 - 0.488 * temperature)) <= tolerance
        assert abs(reference - (2413.0 - 0.488 * temperature)) <= tolerance
        assert abs(residual - (model - reference)) <= tolerance
        assert abs(residual) <= tolerance
        residuals.append(abs(residual))
        densities.append(model)
    assert all(later < earlier for earlier, later in zip(densities, densities[1:]))
    assert abs(report["observed"]["max_absolute_error_kg_m3"] - max(residuals)) <= tolerance
    assert abs(report["observed"]["mean_absolute_error_kg_m3"] - sum(residuals) / len(residuals)) <= tolerance


def test_benchmark_json_is_byte_deterministic_and_canonical() -> None:
    first, first_bytes = _execute()
    second, second_bytes = _execute()
    assert first == second
    assert first_bytes == second_bytes
    assert first_bytes.decode("utf-8") == json.dumps(first, indent=2, sort_keys=True) + "\n"
