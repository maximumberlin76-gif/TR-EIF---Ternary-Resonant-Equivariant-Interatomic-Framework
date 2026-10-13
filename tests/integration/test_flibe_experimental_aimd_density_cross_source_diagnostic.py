
"""Execute and verify the Vidrio–Baral density comparison contract.

The tests use published source tables and independently evaluate temperature
screening, within-run interpolation, unit conversion, and density differences.
"""

from __future__ import annotations

import importlib.util
import json
from math import isclose, sqrt
from pathlib import Path
import subprocess
import sys

import pytest


_ROOT = Path(__file__).resolve().parents[2]
_BENCHMARK = _ROOT / "benchmarks/flibe/experimental_aimd_density_cross_source_diagnostic.py"
_EXPERIMENT = _ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
_AIMD = _ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
_RUN_IDS = ("0A", "1A", "1B", "1C")
_EVALUATED_K = (750, 850, 1000)
_PAIR_COUNTS_BY_TEMPERATURE = {750: 3, 850: 4, 1000: 2}
_ATOL = 1.0e-10  # Binary floating-point rounding in linear interpolation.


def _read(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _module():
    spec = importlib.util.spec_from_file_location("flibe_aimd_density_comparison", _BENCHMARK)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _execute() -> tuple[dict[str, object], bytes]:
    process = subprocess.run(
        [sys.executable, str(_BENCHMARK)],
        cwd=_ROOT,
        check=False,
        capture_output=True,
    )
    assert process.returncode == 0, process.stderr.decode("utf-8", errors="replace")
    assert process.stderr == b""
    report = json.loads(process.stdout)
    assert isinstance(report, dict)
    return report, process.stdout


def _equal(actual: float, expected: float) -> bool:
    return isclose(actual, expected, rel_tol=0.0, abs_tol=_ATOL)


def test_cli_json_is_deterministic_and_matches_callable() -> None:
    first, first_bytes = _execute()
    second, second_bytes = _execute()
    assert first == second == _module().run_comparison()
    assert first_bytes == second_bytes
    assert first_bytes.decode("utf-8") == json.dumps(first, sort_keys=True, indent=2) + "\n"


def test_report_source_identity_and_physical_units() -> None:
    report, _ = _execute()
    experiment = _read(_EXPERIMENT)
    aimd = _read(_AIMD)

    assert report["comparison_id"] == "tr-eif.flibe.vidrio-2022.baral-2021.density.v1"
    assert report["observable"] == "mass_density"
    assert report["method"] == "WITHIN_RUN_LINEAR_TEMPERATURE_INTERPOLATION"
    assert report["sources"]["experimental"] == {
        "dataset_id": experiment["dataset_id"],
        "doi": "10.1021/acs.jced.2c00212",
        "composition_bef2_mol_percent": 33.58,
        "composition_reported_uncertainty_mol_percent": 0.05,
        "pressure_kpa": 102,
        "pressure_standard_uncertainty_kpa": 1,
    }
    assert report["sources"]["first_principles"] == {
        "dataset_id": aimd["dataset_id"],
        "doi": "10.1021/acsomega.1c02528",
        "formula": "Li2BeF4",
        "composition_bef2_formula_unit_fraction": "1/3",
        "reported_supercell_atom_count": 504,
        "pressure_kpa": None,
        "density_standard_uncertainty_kg_m3": None,
    }
    assert aimd["table_units"]["temperature"] == "K"
    assert aimd["table_units"]["simulated_density"] == "g/cm^3"
    assert experiment["columns"] == [
        "temperature_c",
        "temperature_standard_uncertainty_c",
        "density_kg_m3",
        "density_standard_uncertainty_kg_m3",
    ]


def test_temperature_screening_against_source_table() -> None:
    report, _ = _execute()
    experiment = _read(_EXPERIMENT)
    aimd = _read(_AIMD)
    lower_c, upper_c = experiment["domain"]["temperature_range_c"]
    melting_c = experiment["domain"]["reported_melting_temperature_c"]

    expected_evaluated = []
    expected_screened = []
    for temperature_k, *_ in aimd["samples"]:
        temperature_c = temperature_k - 273.15
        if not lower_c <= temperature_c <= upper_c:
            expected_screened.append((temperature_k, "OUTSIDE_EXPERIMENTAL_TEMPERATURE_INTERVAL"))
        elif temperature_c < melting_c:
            expected_screened.append((temperature_k, "BELOW_REPORTED_EXPERIMENTAL_MELTING_TEMPERATURE"))
        else:
            expected_evaluated.append(temperature_k)

    assert tuple(expected_evaluated) == _EVALUATED_K
    assert report["temperature_screening"] == {
        "experimental_temperature_range_c": [447, 817],
        "experimental_melting_temperature_c": 459.1,
        "evaluated_aimd_temperatures_k": list(_EVALUATED_K),
    }
    assert [(row["temperature_k"], row["screening_category"])
            for row in report["screened_aimd_rows"]] == expected_screened
    assert [row["aimd_temperature_k"] for row in report["comparisons"]] == list(_EVALUATED_K)
    assert report["counts"] == {
        "experimental_measurements": 61,
        "aimd_table_rows": 9,
        "evaluated_aimd_rows": 3,
        "screened_aimd_rows": 6,
        "interpolated_pairs": 9,
    }


def test_interpolation_uses_adjacent_points_from_each_run() -> None:
    report, _ = _execute()
    experiment = _read(_EXPERIMENT)

    for comparison in report["comparisons"]:
        temperature_k = comparison["aimd_temperature_k"]
        temperature_c = temperature_k - 273.15
        pairs = comparison["within_run_comparisons"]
        assert _equal(comparison["aimd_temperature_c"], temperature_c)
        assert len(pairs) == _PAIR_COUNTS_BY_TEMPERATURE[temperature_k]
        assert len({pair["run_id"] for pair in pairs}) == len(pairs)
        assert all(pair["run_id"] in _RUN_IDS for pair in pairs)

        expected = []
        for run_id in _RUN_IDS:
            points = experiment["runs"][run_id]
            for lower, upper in zip(points, points[1:]):
                if lower[0] <= temperature_c <= upper[0]:
                    weight = (temperature_c - lower[0]) / (upper[0] - lower[0])
                    expected.append((run_id, lower, upper, weight))
                    break

        assert len(pairs) == len(expected)
        for actual, (run_id, lower, upper, weight) in zip(pairs, expected, strict=True):
            assert actual["run_id"] == run_id
            assert actual["lower_measurement"] == lower
            assert actual["upper_measurement"] == upper
            assert _equal(actual["interpolation_weight_upper"], weight)
            assert _equal(
                actual["interpolated_density_kg_m3"],
                (1 - weight) * lower[2] + weight * upper[2],
            )
            assert actual["source_columns"] == experiment["columns"]


def test_density_differences_and_statistics_from_primary_rows() -> None:
    report, _ = _execute()
    aimd = _read(_AIMD)
    source_by_temperature = {row[0]: row for row in aimd["samples"]}
    expected_differences = []

    for comparison in report["comparisons"]:
        temperature_k = comparison["aimd_temperature_k"]
        _, edge, volume, density_g_cm3 = source_by_temperature[temperature_k]
        density_kg_m3 = density_g_cm3 * 1000.0
        assert _equal(comparison["aimd_density_kg_m3"], density_kg_m3)
        assert comparison["aimd_cubic_cell_edge_angstrom"] == edge
        assert comparison["aimd_cell_volume_angstrom3"] == volume
        for pair in comparison["within_run_comparisons"]:
            lower, upper = pair["lower_measurement"], pair["upper_measurement"]
            weight = (temperature_k - 273.15 - lower[0]) / (upper[0] - lower[0])
            expected = density_kg_m3 - ((1 - weight) * lower[2] + weight * upper[2])
            expected_differences.append(expected)
            assert _equal(pair["aimd_minus_experimental_density_kg_m3"], expected)

    assert len(expected_differences) == 9
    summary = report["density_difference_summary_kg_m3"]
    assert _equal(summary["mean"], sum(expected_differences) / 9)
    assert _equal(summary["mean_absolute"], sum(map(abs, expected_differences)) / 9)
    assert _equal(
        summary["root_mean_square"],
        sqrt(sum(value * value for value in expected_differences) / 9),
    )
    assert _equal(summary["minimum"], min(expected_differences))
    assert _equal(summary["maximum"], max(expected_differences))


def test_interpolation_domain_at_endpoints_and_outside_interval() -> None:
    module = _module()
    records = [[500, 2, 2000, 3], [510, 3, 1990, 4]]
    assert module._interpolate_run(records, 499.0) is None
    assert module._interpolate_run(records, 511.0) is None
    assert module._interpolate_run(records, 500.0)["interpolated_density_kg_m3"] == 2000
    assert module._interpolate_run(records, 510.0)["interpolated_density_kg_m3"] == 1990
    assert module._interpolate_run(records, 505.0)["interpolated_density_kg_m3"] == 1995


def test_source_digest_detects_changed_experimental_measurement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _module()
    experiment = _read(_EXPERIMENT)
    experiment["runs"]["1C"][7][1] = 6
    changed_path = tmp_path / "density_measurement.json"
    changed_path.write_text(json.dumps(experiment), encoding="utf-8")
    monkeypatch.setattr(module, "_EXPERIMENT", changed_path)
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        module.run_comparison()


def test_source_digest_detects_changed_aimd_density(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _module()
    aimd = _read(_AIMD)
    aimd["samples"][4][3] += 0.001
    changed_path = tmp_path / "density_aimd.json"
    changed_path.write_text(json.dumps(aimd), encoding="utf-8")
    monkeypatch.setattr(module, "_AIMD", changed_path)
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        module.run_comparison()
