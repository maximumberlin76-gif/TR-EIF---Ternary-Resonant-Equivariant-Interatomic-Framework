
"""Integration qualification of the FLiBe rank-two registered-density benchmark.

Execute the three-interval TR-EIP MD benchmark in an independent interpreter.
Reconstruct sampled mass densities, event clocks and observed-pressure means;
check every registered Vidrio and Baral row against the original source tables.
Retain the distinction between measured and computed state coordinates, the
barostat target, missing source axes, and committed ternary execution states.
"""

from __future__ import annotations

import hashlib
import json
import os
from math import fsum, isfinite
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/rank_two_tr_eip_registered_density_state_gate.py"
VIDRIO = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
BENCHMARK_ID = "tr-eif.flibe.rank-two-registered-density-state-gate.v1"
VIDRIO_ID = "tr-eif.flibe.vidrio-2022.experimental-density.v1"
BARAL_ID = "tr-eif.flibe.baral-2021.aimd-structural-density.v1"
MASS_TO_KG = 1.66053906660e-27
TIME_TO_SECOND = 1.0e-15
MECHANICAL_DT = 1.0e-4
CELL_MASSES = (6.94, 6.94, 9.0121831, 18.998403163, 18.998403163,
               18.998403163, 18.998403163)
CHECKS = {
    "three_mechanical_intervals",
    "registered_source_cardinalities",
    "source_record_order",
    "source_row_metadata",
    "density_residual_domain",
    "fixed_mass_inventory",
    "neutral_mediation",
    "signed_observed_pressures",
}
SOURCE_CASES = (
    (0, VIDRIO, VIDRIO_ID, "EXPERIMENTAL", 61),
    (1, BARAL, BARAL_ID, "FIRST_PRINCIPLES", 9),
)


def _execute() -> tuple[dict[str, object], bytes]:
    """Run the committed executable rather than importing its test helpers."""
    assert BENCHMARK.is_file()
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(ROOT / "src"), environment.get("PYTHONPATH", ""))
        if part
    )
    process = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        timeout=180,
        check=False,
    )
    assert process.returncode == 0, process.stderr.decode("utf-8", errors="replace")
    assert process.stderr == b""
    result = json.loads(process.stdout)
    assert isinstance(result, dict)
    return result, process.stdout


@pytest.fixture(scope="module")
def executed_benchmark() -> tuple[dict[str, object], bytes]:
    return _execute()


@pytest.fixture(scope="module")
def source_tables() -> tuple[dict[str, object], dict[str, object]]:
    return tuple(json.loads(path.read_text(encoding="utf-8"))
                 for path in (VIDRIO, BARAL))


def test_executable_benchmark_identity_and_checks(executed_benchmark):
    result, serialized = executed_benchmark
    assert serialized.endswith(b"\n")
    assert result["benchmark_id"] == BENCHMARK_ID
    assert result["model_id"] == "FLIBE-RANK-TWO-TR-EIP-ANALYTIC-MD-FIXTURE"
    assert result["trajectory_id"] == "FLIBE-RANK-TWO-THREE-INTERVAL-MD"
    assert result["provenance"] == "BENCHMARK"
    assert result["source_ids"] == [VIDRIO_ID, BARAL_ID]
    checks = result["checks"]
    assert isinstance(checks, dict) and set(checks) == CHECKS
    assert all(value is True for value in checks.values())
    assert len(result["source_comparisons"]) == 2
    assert len(result["observed_state_samples"]) == 3


def test_mechanical_density_is_independent_mass_over_volume(executed_benchmark):
    result, _ = executed_benchmark
    mass_kg = fsum(CELL_MASSES) * MASS_TO_KG
    samples = result["observed_state_samples"]
    assert tuple(row["interval_index"] for row in samples) == (0, 1, 2)
    assert tuple(row["md_step"] for row in samples) == (5, 6, 7)
    for index, row in enumerate(samples):
        volume = row["volume_m3"]
        density = row["density_kg_m3"]
        temperature = row["kinetic_temperature_k"]
        assert all(isfinite(value) and value > 0.0 for value in (volume, density, temperature))
        assert density * volume == pytest.approx(mass_kg, rel=1e-11)
        assert row["md_time_s"] == pytest.approx(
            (0.3 + (index + 1) * MECHANICAL_DT) * TIME_TO_SECOND,
            rel=1e-12,
        )
    assert all(a["md_time_s"] < b["md_time_s"]
               for a, b in zip(samples, samples[1:]))


def test_separate_resonance_ternary_and_mechanical_clocks(executed_benchmark):
    samples = executed_benchmark[0]["observed_state_samples"]
    assert tuple(row["resonance_step_count"] for row in samples) == (3, 3, 4)
    assert tuple(row["ternary_event_count"] for row in samples) == (6, 7, 7)
    assert tuple(row["retained_states"] for row in samples) == (
        [0] * 7,
        [1] * 7,
        [1] * 7,
    )
    assert tuple(row["pending_target_count"] for row in samples) == (7, 0, 0)
    for row in samples:
        assert row["pending_target_count"] >= 0
        assert all(state in (-1, 0, 1) for state in row["retained_states"])
    assert all(state == 0 for state in samples[0]["retained_states"])


def test_observed_pressure_mean_does_not_substitute_control_target(executed_benchmark):
    result = executed_benchmark[0]
    samples = result["observed_state_samples"]
    pressures = tuple(row["signed_observed_pressure_pa"] for row in samples)
    assert all(isfinite(value) for value in pressures)
    mean_pressure = fsum(pressures) / len(pressures)
    target = result["barostat_target_pressure_pa"]
    assert isfinite(target) and target > 0.0
    for comparison in result["source_comparisons"]:
        assert comparison["model_mean_signed_observed_pressure_pa"] == pytest.approx(
            mean_pressure, rel=1e-12, abs=1e-6,
        )
        observed_coordinate = comparison["model_pressure_coordinate_pa"]
        if mean_pressure >= 0.0:
            assert observed_coordinate == pytest.approx(mean_pressure, rel=1e-12, abs=1e-6)
        else:
            assert observed_coordinate is None


def test_source_level_observables_match_selected_md_frames(executed_benchmark):
    result = executed_benchmark[0]
    samples = result["observed_state_samples"]
    mean_density = fsum(row["density_kg_m3"] for row in samples) / len(samples)
    mean_temperature = fsum(row["kinetic_temperature_k"] for row in samples) / len(samples)
    for comparison in result["source_comparisons"]:
        assert comparison["model_mean_density_kg_m3"] == pytest.approx(mean_density, rel=1e-12)
        assert comparison["model_mean_kinetic_temperature_k"] == pytest.approx(
            mean_temperature, rel=1e-12,
        )
        assert comparison["model_physical_state_id"] == "DECLARED-ANALYTIC-FIXTURE-STATE"
        assert comparison["source_mapping_id"] == (
            "RANK-TWO-OBSERVED-DENSITY-STATE-CORRESPONDENCE"
        )
        assert comparison["temperature_tolerance_k"] == 1.0e-8
        assert comparison["pressure_tolerance_pa"] == 1.0e-5


@pytest.mark.parametrize("position,path,identity,kind,count", SOURCE_CASES)
def test_registered_source_identity_fingerprint_and_row_order(
    executed_benchmark, source_tables, position, path, identity, kind, count,
):
    result = executed_benchmark[0]["source_comparisons"][position]
    original = source_tables[position]
    assert original["dataset_id"] == identity == result["dataset_id"]
    assert original["evidence_kind"] == kind == result["source_evidence_kind"]
    assert result["source_file_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert result["doi"] == original["source"]["doi"]
    assert len(result["rows"]) == result["source_row_count"] == count
    assert result["matched_source_row_count"] + result["unmatched_source_row_count"] == count
    assert result["source_record_order_preserved"] is True
    assert result["source_metadata_preserved"] is True
    assert result["density_residual_only_for_matched_state"] is True
    assert result["matched_source_row_count"] == 0
    assert result["unmatched_source_row_count"] == count
    assert result["matched_density_metrics"] is None
    assert result["missing_source_axis_counts"]["physical_state"] == count
    assert all(row["density_residual_kg_m3"] is None for row in result["rows"])
    assert all(row["physical_state_id"] is None for row in result["rows"])
    assert all("physical_state" in row["missing_source_axes"] for row in result["rows"])
    assert all(set(row["matched_axes"]).isdisjoint(row["unmatched_axes"])
               for row in result["rows"])
    assert all(set(row["matched_axes"]) | set(row["unmatched_axes"]) == {
        "composition", "temperature", "pressure", "physical_state", "normalization"
    } for row in result["rows"])


def test_vidrio_measured_composition_uncertainty_and_61_source_rows(
    executed_benchmark, source_tables,
):
    comparison = executed_benchmark[0]["source_comparisons"][0]
    original = source_tables[0]
    assert comparison["missing_source_axis_counts"]["pressure"] == 0
    assert tuple(len(original["runs"][key]) for key in ("0A", "1A", "1B", "1C")) == (
        28, 7, 13, 13,
    )
    rows = comparison["rows"]
    index = 0
    for run in ("0A", "1A", "1B", "1C"):
        for position, values in enumerate(original["runs"][run]):
            row = rows[index]
            index += 1
            assert row["record_id"] == f"{VIDRIO_ID}/{run}/{position:02d}"
            assert row["source_values"] == values
            assert row["temperature_k"] == pytest.approx(values[0] + 273.15, abs=1e-10)
            assert row["density_kg_m3"] == values[2]
            assert row["temperature_standard_uncertainty_k"] == values[1]
            assert row["density_standard_uncertainty_kg_m3"] == values[3]
            assert row["bef2_formula_fraction"] == pytest.approx(0.3358, abs=1e-12)
            assert row["lif_formula_fraction"] == pytest.approx(0.6642, abs=1e-12)
            assert row["bef2_fraction_standard_uncertainty"] == pytest.approx(0.0005)
            assert row["pressure_pa"] == 102000.0
            assert row["pressure_standard_uncertainty_pa"] == 1000.0
            assert row["source_location"] and row["method_id"]
    assert index == 61


def test_baral_aimd_rows_have_missing_pressure_and_exact_formula_composition(
    executed_benchmark, source_tables,
):
    comparison = executed_benchmark[0]["source_comparisons"][1]
    original = source_tables[1]
    assert comparison["missing_source_axis_counts"]["pressure"] == 9
    for index, (row, raw) in enumerate(zip(
        comparison["rows"], original["samples"], strict=True,
    )):
        assert row["record_id"] == f"{BARAL_ID}/T{raw[0]:g}"
        assert row["source_values"] == raw
        assert row["temperature_k"] == raw[0]
        assert row["density_kg_m3"] == pytest.approx(raw[3] * 1000.0, rel=1e-12)
        assert row["bef2_formula_fraction"] == pytest.approx(1.0 / 3.0, rel=1e-12)
        assert row["lif_formula_fraction"] == pytest.approx(2.0 / 3.0, rel=1e-12)
        assert row["pressure_pa"] is None
        assert row["physical_state_id"] is None
        assert row["density_standard_uncertainty_kg_m3"] is None
        assert row["temperature_standard_uncertainty_k"] is None
        assert "pressure" in row["missing_source_axes"]
        assert row["source_location"] and row["method_id"]
    assert len(comparison["rows"]) == 9


def test_repeat_execution_is_byte_deterministic(executed_benchmark):
    original_report, original_bytes = executed_benchmark
    replay, replay_bytes = _execute()
    assert replay == original_report
    assert replay_bytes == original_bytes
    assert json.loads(replay_bytes)["checks"] == original_report["checks"]
