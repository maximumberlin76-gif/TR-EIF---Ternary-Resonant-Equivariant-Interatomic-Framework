
"""Independent qualification of the observed-state FLiBe density benchmark.

Recompute model mass density from the declared seven-atom cell, recover all
Vidrio and Baral source records directly from their registered JSON tables,
and independently evaluate each physical-coordinate correspondence gate.
Preserve missing pressure and physical-state coordinates and enforce the
qualification rule for density residuals.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
from math import fsum, isclose, isfinite
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK = ROOT / "benchmarks/flibe/periodic_md_density_source_gate.py"
PAIR_SOURCE = ROOT / "data/reference/flibe_smith_2020_pim_pair_coefficients.json"
VIDRIO = ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
BARAL = ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
BENCHMARK_ID = "tr-eif.flibe.periodic-md-density-source-state-gate.v1"
MODEL_ID = "FLIBE-PERIODIC-DENSITY-SOURCE-GATE"
DOIS = ("10.1021/acs.jced.2c00212", "10.1021/acsomega.1c02528")
AXES = ("composition", "temperature", "pressure", "physical_state", "normalization")
CHECKS = {
    "registered_pair_source",
    "complete_potential_state_observations",
    "target_initial_kinetic_temperature",
    "aimd_temperature_coordinate_exercised",
    "physical_mass_and_cell_density",
    "computed_pressure_tensor_trace",
    "finite_model_coordinates",
    "registered_source_counts",
    "registered_source_fingerprints",
    "all_rows_state_screened",
    "residual_only_on_matched_coordinates",
}
BOHR_TO_M = 5.29177210903e-11
U_TO_KG = 1.66053906660e-27
TIME_STEP = 0.001
TIME_STEP_S = 1.0e-15
CELL_EDGE_BOHR = 18.0
MASS_U = {"Li": 6.94, "Be": 9.0121831, "F": 18.998403163}
COUNTS = {"Li": 2, "Be": 1, "F": 4}


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _near(actual, expected, *, rtol=1.0e-12, atol=1.0e-10) -> None:
    assert isinstance(actual, (int, float)) and not isinstance(actual, bool)
    assert isfinite(actual) and isfinite(expected)
    assert isclose(actual, expected, rel_tol=rtol, abs_tol=atol)


def _execute() -> tuple[dict, bytes]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        value for value in (str(ROOT / "src"), env.get("PYTHONPATH", "")) if value
    )
    completed = subprocess.run(
        [sys.executable, str(BENCHMARK)],
        cwd=ROOT,
        env=env,
        capture_output=True,
        check=False,
        timeout=300,
    )
    assert completed.returncode == 0, (
        completed.stderr.decode("utf-8", errors="replace")
        + completed.stdout.decode("utf-8", errors="replace")[-2000:]
    )
    assert completed.stderr == b""
    report = json.loads(completed.stdout)
    assert isinstance(report, dict)
    return report, completed.stdout


@pytest.fixture(scope="module")
def execution() -> tuple[dict, bytes]:
    assert BENCHMARK.is_file()
    return _execute()


@pytest.fixture(scope="module")
def report(execution) -> dict:
    return execution[0]


def _expected_source_rows() -> tuple[tuple[dict, list[dict]], ...]:
    """Project primary JSON rows into source coordinates without calling a loader."""
    vidrio = _read(VIDRIO)
    baral = _read(BARAL)
    fraction = vidrio["domain"]["measured_composition"]["bef2_mol_percent"] / 100.0
    fraction_u = (
        vidrio["domain"]["measured_composition"]["bef2_reported_uncertainty_mol_percent"]
        / 100.0
    )
    pressure = vidrio["domain"]["pressure_kpa"] * 1000.0
    pressure_u = vidrio["domain"]["pressure_standard_uncertainty_kpa"] * 1000.0
    experimental = []
    for run_id in ("0A", "1A", "1B", "1C"):
        for index, (temp_c, temp_u, rho, rho_u) in enumerate(vidrio["runs"][run_id]):
            experimental.append({
                "record_id": f"{vidrio['dataset_id']}/{run_id}/{index:02d}",
                "run_id": run_id,
                "source_temperature_k": temp_c + 273.15,
                "source_density_kg_m3": rho,
                "source_pressure_pa": pressure,
                "source_physical_state_id": None,
                "source_bef2_fraction": fraction,
                "source_bef2_fraction_standard_uncertainty": fraction_u,
                "source_density_standard_uncertainty_kg_m3": rho_u,
                "source_temperature_standard_uncertainty_k": temp_u,
                "source_pressure_standard_uncertainty_pa": pressure_u,
            })
    first_principles = []
    for temp_k, _edge, _volume, rho_g_cm3 in baral["samples"]:
        first_principles.append({
            "record_id": f"{baral['dataset_id']}/T{temp_k:g}",
            "run_id": None,
            "source_temperature_k": temp_k,
            "source_density_kg_m3": rho_g_cm3 * 1000.0,
            "source_pressure_pa": None,
            "source_physical_state_id": None,
            "source_bef2_fraction": 1.0 / 3.0,
            "source_bef2_fraction_standard_uncertainty": None,
            "source_density_standard_uncertainty_kg_m3": None,
            "source_temperature_standard_uncertainty_k": None,
            "source_pressure_standard_uncertainty_pa": None,
        })
    return ((vidrio, experimental), (baral, first_principles))


def _audit_source_rows(report: dict) -> None:
    sources = report["sources"]
    assert isinstance(sources, list) and len(sources) == 2
    expected = _expected_source_rows()
    for index, ((source_data, expected_rows), actual, path, doi) in enumerate(zip(
        expected, sources, (VIDRIO, BARAL), DOIS, strict=True
    )):
        assert actual["dataset_id"] == source_data["dataset_id"]
        assert actual["doi"] == doi == source_data["source"]["doi"]
        assert actual["evidence_kind"] == source_data["evidence_kind"]
        assert actual["source_file_sha256"] == _sha256(path)
        assert actual["record_count"] == len(actual["records"]) == len(expected_rows)
        assert len({row["record_id"] for row in actual["records"]}) == len(expected_rows)
        for row, source in zip(actual["records"], expected_rows, strict=True):
            for field, value in source.items():
                if value is None:
                    assert row[field] is None
                elif isinstance(value, (float, int)):
                    _near(row[field], value)
                else:
                    assert row[field] == value
        assert actual["matched_count"] + actual["unmatched_count"] == len(expected_rows)
        if index == 0:
            assert len(expected_rows) == 61
        else:
            assert len(expected_rows) == 9


def _audit_model_si(report: dict) -> None:
    model = report["model"]
    observed = report["observed"]
    contract = report["comparison_contract"]
    assert report["benchmark_id"] == BENCHMARK_ID
    assert report["status"] == "PASS"
    assert set(report["checks"]) == CHECKS
    assert all(value is True for value in report["checks"].values())
    assert model["model_id"] == MODEL_ID
    assert model["provenance"] == "BENCHMARK"
    assert model["initial_species"] == ["Li", "Li", "Be", "F", "F", "F", "F"]
    assert model["atom_count"] == 7
    assert model["mass_values_u"] == MASS_U
    assert model["initial_cell_bohr"] == [
        [CELL_EDGE_BOHR, 0.0, 0.0],
        [0.0, CELL_EDGE_BOHR, 0.0],
        [0.0, 0.0, CELL_EDGE_BOHR],
    ]
    assert model["ensemble"] == "NVE_FIXED_CELL"
    assert model["initial_temperature_target_k"] == 850.0
    assert model["initial_temperature_target_role"] == "CONTROL_TARGET"
    assert model["time_step_code"] == TIME_STEP
    assert model["integration_steps"] == 1
    assert model["pressure_method"] == "PERIODIC-STATIONARY-DIPOLE-ENERGY-STRAIN"
    assert model["velocity_frame"] == "CENTER_OF_MASS"
    assert model["physical_state_id"] == "UNCLASSIFIED_MD_PHASE"
    assert model["pair_source_doi"] == "10.1016/j.molliq.2019.112165"
    assert model["pair_source_sha256"] == _sha256(PAIR_SOURCE)
    assert contract == {
        "composition_matching": "EXACT_FORMULA_UNIT_FRACTIONS",
        "temperature_tolerance_k": 5.0,
        "pressure_tolerance_pa": 1000.0,
        "physical_state_matching": "EXACT_REPORTED_STATE_IDENTIFIER",
        "pressure_role": "OBSERVED_ONLY",
        "normalization": "source-reported-mass-density",
        "qualified_residual_eligibility": "ALL_FIVE_STATE_COORDINATES_MATCH",
    }
    total_mass_kg = fsum(COUNTS[s] * MASS_U[s] for s in ("Li", "Be", "F")) * U_TO_KG
    volume_m3 = (CELL_EDGE_BOHR * BOHR_TO_M) ** 3
    density = total_mass_kg / volume_m3
    _near(observed["mean_density_kg_m3"], density)
    _near(observed["bef2_fraction"], 1.0 / 3.0)
    assert observed["density_statistic_id"] == "mean-instantaneous-cell-density"
    assert isinstance(observed["samples"], list) and len(observed["samples"]) == 2
    for index, sample in enumerate(observed["samples"]):
        assert sample["state_index"] == index
        _near(sample["md_time_code"], TIME_STEP * index, atol=1.0e-15)
        _near(sample["density_kg_m3"], density)
        assert isfinite(sample["kinetic_temperature_k"]) and sample["kinetic_temperature_k"] >= 0.0
        assert isfinite(sample["signed_pressure_pa"])
    _near(observed["samples"][0]["kinetic_temperature_k"], 850.0)
    _near(
        observed["mean_kinetic_temperature_k"],
        fsum(item["kinetic_temperature_k"] for item in observed["samples"]) / 2.0,
    )
    _near(
        observed["mean_signed_pressure_pa"],
        fsum(item["signed_pressure_pa"] for item in observed["samples"]) / 2.0,
    )
    assert isfinite(observed["energy_drift_hartree"])
    assert observed["energy_drift_hartree"] >= 0.0
    signed_pressure = observed["mean_signed_pressure_pa"]
    if signed_pressure < 0.0:
        assert observed["pressure_coordinate_pa"] is None
    else:
        _near(observed["pressure_coordinate_pa"], signed_pressure)


def _audit_matching(report: dict) -> None:
    observed = report["observed"]
    model = report["model"]
    contract = report["comparison_contract"]
    temp_tol = contract["temperature_tolerance_k"]
    pressure_tol = contract["pressure_tolerance_pa"]
    matched_total = 0
    for source in report["sources"]:
        matched = 0
        retained = []
        for row in source["records"]:
            source_p = row["source_pressure_pa"]
            model_p = observed["pressure_coordinate_pa"]
            flags = {
                "composition": observed["bef2_fraction"] == row["source_bef2_fraction"],
                "temperature": abs(
                    observed["mean_kinetic_temperature_k"] - row["source_temperature_k"]
                ) <= temp_tol,
                "pressure": (
                    model_p is not None and source_p is not None
                    and abs(model_p - source_p) <= pressure_tol
                ),
                "physical_state": (
                    row["source_physical_state_id"] is not None
                    and row["source_physical_state_id"] == model["physical_state_id"]
                ),
                "normalization": contract["normalization"] == "source-reported-mass-density",
            }
            assert row["matched_axes"] == [axis for axis in AXES if flags[axis]]
            assert row["unmatched_axes"] == [axis for axis in AXES if not flags[axis]]
            assert row["missing_source_axes"] == [
                axis for axis in ("pressure", "physical_state")
                if row[f"source_{axis}_pa" if axis == "pressure" else "source_physical_state_id"]
                is None
            ]
            _near(
                row["temperature_difference_k"],
                observed["mean_kinetic_temperature_k"] - row["source_temperature_k"],
            )
            _near(
                row["bef2_fraction_difference"],
                observed["bef2_fraction"] - row["source_bef2_fraction"],
            )
            if source_p is None:
                assert row["signed_md_minus_source_pressure_pa"] is None
            else:
                _near(
                    row["signed_md_minus_source_pressure_pa"],
                    observed["mean_signed_pressure_pa"] - source_p,
                )
            if source_p is None or model_p is None:
                assert row["pressure_difference_pa"] is None
            else:
                _near(row["pressure_difference_pa"], model_p - source_p)
            eligible = all(flags.values())
            if eligible:
                matched += 1
                matched_total += 1
                residual = observed["mean_density_kg_m3"] - row["source_density_kg_m3"]
                _near(row["qualified_density_residual_kg_m3"], residual)
                retained.append(residual)
            else:
                assert row["qualified_density_residual_kg_m3"] is None
        assert source["matched_count"] == matched
        assert source["unmatched_count"] == source["record_count"] - matched
        metrics = source["residual_metrics"]
        if not retained:
            assert metrics is None
        else:
            assert metrics["count"] == len(retained)
            _near(metrics["mean_signed_kg_m3"], fsum(retained) / len(retained))
            _near(metrics["mean_absolute_kg_m3"], fsum(map(abs, retained)) / len(retained))
            _near(metrics["root_mean_square_kg_m3"],
                  (fsum(v * v for v in retained) / len(retained)) ** 0.5)
            _near(metrics["maximum_absolute_kg_m3"], max(map(abs, retained)))
    assert matched_total == 0
    assert all(
        "physical_state" in row["unmatched_axes"]
        for source in report["sources"] for row in source["records"]
    )
    assert any(
        "temperature" in row["matched_axes"]
        for row in report["sources"][1]["records"]
    )


def test_cli_report_is_canonical_and_all_declared_gates_pass(execution) -> None:
    document, raw = execution
    assert raw.decode("utf-8") == json.dumps(
        document, sort_keys=True, indent=2, allow_nan=False
    ) + "\n"
    assert document["status"] == "PASS"
    assert set(document["checks"]) == CHECKS
    assert all(value is True for value in document["checks"].values())


def test_registered_primary_source_identity_and_all_70_rows(report) -> None:
    _audit_source_rows(report)


def test_independent_mass_volume_density_and_observed_state_units(report) -> None:
    _audit_model_si(report)


def test_independently_recomputed_five_axis_correspondence_and_residual_gate(report) -> None:
    _audit_matching(report)


def test_exact_source_composition_and_missing_aimd_pressure(report) -> None:
    experiment, aimd = report["sources"]
    assert all(row["source_bef2_fraction"] == 0.3358 for row in experiment["records"])
    assert all(row["source_bef2_fraction"] == (1.0 / 3.0) for row in aimd["records"])
    assert all(row["source_pressure_pa"] == 102000.0 for row in experiment["records"])
    assert all(row["source_pressure_pa"] is None for row in aimd["records"])
    assert all(row["source_physical_state_id"] is None for source in report["sources"]
               for row in source["records"])
    assert experiment["matched_count"] == aimd["matched_count"] == 0
    assert experiment["residual_metrics"] is None and aimd["residual_metrics"] is None


def test_output_detects_modified_source_fingerprint(report) -> None:
    damaged = copy.deepcopy(report)
    damaged["sources"][0]["source_file_sha256"] = "0" * 64
    with pytest.raises(AssertionError):
        _audit_source_rows(damaged)


def test_output_detects_modified_source_density(report) -> None:
    damaged = copy.deepcopy(report)
    damaged["sources"][1]["records"][3]["source_density_kg_m3"] += 10.0
    with pytest.raises(AssertionError):
        _audit_source_rows(damaged)


def test_output_detects_modified_model_cell_mass_density(report) -> None:
    damaged = copy.deepcopy(report)
    damaged["observed"]["mean_density_kg_m3"] *= 1.05
    with pytest.raises(AssertionError):
        _audit_model_si(damaged)


def test_output_detects_false_temperature_coordinate_match(report) -> None:
    damaged = copy.deepcopy(report)
    target = next(row for row in damaged["sources"][1]["records"]
                  if "temperature" not in row["matched_axes"])
    target["matched_axes"].append("temperature")
    with pytest.raises(AssertionError):
        _audit_matching(damaged)


def test_output_detects_qualified_residual_without_complete_state_match(report) -> None:
    damaged = copy.deepcopy(report)
    damaged["sources"][0]["records"][0]["qualified_density_residual_kg_m3"] = 0.0
    with pytest.raises(AssertionError):
        _audit_matching(damaged)


def test_output_detects_invalid_pressure_difference(report) -> None:
    damaged = copy.deepcopy(report)
    row = damaged["sources"][0]["records"][0]
    if row["pressure_difference_pa"] is None:
        row["pressure_difference_pa"] = 0.0
    else:
        row["pressure_difference_pa"] += 10000.0
    with pytest.raises(AssertionError):
        _audit_matching(damaged)


def test_deterministic_reexecution_is_byte_identical(execution) -> None:
    second, raw = _execute()
    assert second == execution[0]
    assert raw == execution[1]
