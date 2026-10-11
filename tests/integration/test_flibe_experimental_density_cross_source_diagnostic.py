
"""Independent execution checks for the unmatched-source FLiBe density diagnostic.

These tests qualify source provenance, exclusion rules, residual arithmetic,
and deterministic output. They do not establish matched-state physical
validation, first-principles agreement, or TR-EIP prediction accuracy.
"""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from math import isclose, sqrt
from pathlib import Path
import subprocess
import sys

import pytest


_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "benchmarks/flibe/experimental_density_cross_source_diagnostic.py"
_SOURCE = _ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"

# Expected domain boundaries are taken from the registered correlation and
# independently reviewed Table 4 temperatures, not from diagnostic output.
_T_MIN_K = 800.0
_T_MAX_K = 1080.0
_INTERCEPT_KG_M3 = 2413.0
_SLOPE_KG_M3_PER_K = -0.488
_BY_RUN = {"0A": 18, "1A": 3, "1B": 7, "1C": 11}
# This tolerance covers floating-point evaluation, not physical agreement.
_ROUNDING_ATOL = 1.0e-10


def _execute() -> tuple[dict[str, object], bytes]:
    result = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        cwd=_ROOT,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert result.stderr == b""
    report = json.loads(result.stdout)
    assert isinstance(report, dict)
    return report, result.stdout


def _diagnostic_module():
    spec = importlib.util.spec_from_file_location("flibe_density_cross_source_diagnostic", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _close(observed: float, expected: float) -> bool:
    return isclose(observed, expected, rel_tol=0.0, abs_tol=_ROUNDING_ATOL)


def test_report_retains_nonvalidation_evidence_boundary() -> None:
    report, _ = _execute()
    assert report["diagnostic_id"] == "tr-eif.flibe.vidrio-vs-registered-density.unmatched.v1"
    assert report["status"] == "DIAGNOSTIC_ONLY"
    assert report["experimental_dataset_id"] == "tr-eif.flibe.vidrio-2022.experimental-density.v1"
    assert report["experimental_source_doi"] == "10.1021/acs.jced.2c00212"
    assert report["registered_correlation_source_id"] == "FLIBE-REFERENCE-JANZ-1974-DENSITY"
    assert report["observable"] == "mass_density"
    assert report["comparison_scope"] == "OVERLAPPING_NOMINAL_TEMPERATURE_ONLY"
    assert report["physical_validation_status"] == "NOT_ESTABLISHED"
    assert report["tr_eip_prediction_status"] == "REQUIRES_MODEL_OUTPUT"
    assert report["first_principles_comparison_status"] == "REQUIRES_SOURCE"
    assert "not model validation" in report["qualification_boundary"]

    compatibility = report["source_state_compatibility"]
    assert compatibility["measured_bef2_mol_percent"] == 33.58
    assert compatibility["measured_bef2_reported_uncertainty_mol_percent"] == 0.05
    assert compatibility["registered_bef2_mol_percent"] == 33.0
    assert compatibility["composition_exact_match"] is False
    assert compatibility["pressure_match"] == "NOT_ESTABLISHED_FOR_REGISTERED_CORRELATION"
    assert compatibility["experimental_pressure_kpa"] == 102
    assert compatibility["experimental_pressure_standard_uncertainty_kpa"] == 1
    assert "not applied as acceptance" in compatibility["uncertainty_policy"]


def test_diagnostic_cli_output_is_byte_deterministic() -> None:
    first, first_bytes = _execute()
    second, second_bytes = _execute()
    assert first == second
    assert first_bytes == second_bytes
    assert first_bytes.decode("utf-8") == json.dumps(first, indent=2, sort_keys=True) + "\n"


def test_temperature_selection_and_uncertainties_against_source_records() -> None:
    report, _ = _execute()
    with _SOURCE.open("r", encoding="utf-8") as handle:
        source = json.load(handle)
    samples = report["samples"]
    counts = report["counts"]
    assert counts["registered_measurements"] == 61
    assert counts["temperature_domain_samples"] == 39
    assert counts["by_run"] == _BY_RUN
    assert counts["excluded"] == {
        "outside_correlation_temperature_domain": 22,
        "below_reported_melting_temperature": 3,
    }
    assert counts["below_melting_is_subset_of_outside_temperature_domain"] is True
    assert len(samples) == 39

    accepted = []
    rejected = 0
    below_melting = 0
    for run_id in ("0A", "1A", "1B", "1C"):
        for temp_c, temp_unc, density, density_unc in source["runs"][run_id]:
            temp_k = temp_c + 273.15
            if temp_c < 459.1:
                below_melting += 1
            if not (_T_MIN_K <= temp_k <= _T_MAX_K):
                rejected += 1
                continue
            assert temp_c >= 459.1
            accepted.append((run_id, temp_c, temp_k, temp_unc, density, density_unc))

    assert rejected == 22
    assert below_melting == 3
    assert len(accepted) == len(samples)
    for observed, (run_id, temp_c, temp_k, temp_unc, density, density_unc) in zip(
        samples, accepted, strict=True
    ):
        assert observed["run_id"] == run_id
        assert observed["temperature_c"] == temp_c
        assert _close(observed["temperature_k"], temp_k)
        assert observed["temperature_standard_uncertainty_c"] == temp_unc
        assert observed["measured_density_kg_m3"] == density
        assert observed["measured_density_standard_uncertainty_kg_m3"] == density_unc


def test_residuals_and_aggregate_statistics_match_independent_arithmetic() -> None:
    report, _ = _execute()
    samples = report["samples"]
    residuals = []
    for sample in samples:
        expected_density = (
            _INTERCEPT_KG_M3 + _SLOPE_KG_M3_PER_K * (sample["temperature_c"] + 273.15)
        )
        expected_residual = expected_density - sample["measured_density_kg_m3"]
        assert _close(sample["registered_correlation_density_kg_m3"], expected_density)
        assert _close(sample["unmatched_source_residual_kg_m3"], expected_residual)
        residuals.append(expected_residual)

    # Fixed source-point anchors detect sign and unit mistakes independently.
    first = samples[0]
    last = samples[-1]
    assert (first["run_id"], first["temperature_c"], first["measured_density_kg_m3"]) == (
        "0A", 531, 2014
    )
    assert _close(first["registered_correlation_density_kg_m3"], 2020.5748)
    assert (last["run_id"], last["temperature_c"], last["measured_density_kg_m3"]) == (
        "1C", 795, 1916
    )
    assert _close(last["registered_correlation_density_kg_m3"], 1891.7428)

    summary = report["exploratory_error_summary"]
    assert _close(summary["mean_absolute_residual_kg_m3"], sum(map(abs, residuals)) / 39)
    assert _close(
        summary["root_mean_square_residual_kg_m3"],
        sqrt(sum(residual * residual for residual in residuals) / 39),
    )
    assert _close(summary["maximum_absolute_residual_kg_m3"], max(map(abs, residuals)))


def test_mutated_primary_measurement_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    module = _diagnostic_module()
    with _SOURCE.open("r", encoding="utf-8") as handle:
        tampered = json.load(handle)
    tampered["runs"]["1C"][7][1] = 6  # Source value: 677 C with 7 C uncertainty.
    altered = tmp_path / "altered_measurements.json"
    altered.write_text(json.dumps(tampered), encoding="utf-8")
    monkeypatch.setattr(module, "_DATASET", altered)
    with pytest.raises(ValueError, match="fingerprint mismatch"):
        module.run_diagnostic()


@pytest.mark.parametrize("mutation", ("composition", "match_flag", "method"))
def test_composition_boundary_cannot_be_relabeled_as_matched(
    mutation: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = _diagnostic_module()
    with _SOURCE.open("r", encoding="utf-8") as handle:
        altered = deepcopy(json.load(handle))
    if mutation == "composition":
        altered["domain"]["measured_composition"]["bef2_mol_percent"] = 33.0
    elif mutation == "match_flag":
        altered["domain"]["model_composition_67_33_direct_match"] = True
    else:
        altered["domain"]["measured_composition"]["method"] = "UNVERIFIED"
    monkeypatch.setattr(module, "_load_dataset", lambda: altered)
    with pytest.raises(ValueError, match="non-matched composition evidence boundary"):
        module.run_diagnostic()
