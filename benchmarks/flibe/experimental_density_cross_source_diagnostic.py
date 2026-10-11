
"""Unmatched-source diagnostic for registered FLiBe density evidence.

This compares measured Vidrio 2022 density observations against the registered
Janz 1974 source-derived density correlation only where their nominal
*temperature* domains overlap. Measured versus registered compositions differ;
pressure equivalence is not established. Residuals are exploratory, not
TR-EIP predictions, a physical validation, or a cross-model qualification.
"""

from __future__ import annotations

import hashlib
import json
from math import sqrt
from pathlib import Path
import runpy


_ROOT = Path(__file__).resolve().parents[2]
_DATASET = _ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
_BASELINE = _ROOT / "benchmarks/flibe/reference_property_reproduction.py"
_EXPECTED_DATASET_ID = "tr-eif.flibe.vidrio-2022.experimental-density.v1"
_EXPECTED_SOURCE_DOI = "10.1021/acs.jced.2c00212"
_EXPECTED_BASELINE_ID = "tr-eif.flibe.reference-property-reproduction.v1"
_EXPECTED_CORRELATION_SOURCE = "FLIBE-REFERENCE-JANZ-1974-DENSITY"
_MEASUREMENTS_SHA256 = (
    "8ff807a4b1b96a806be33277d9ad80338787836f619bbfe66500772e9b8899aa"
)
_RUN_COUNTS = {"0A": 28, "1A": 7, "1B": 13, "1C": 13}
_CELSIUS_TO_KELVIN = 273.15


def _load_dataset() -> dict[str, object]:
    """Read the committed primary-source measurements, not generated data."""

    with _DATASET.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("experimental dataset must be a JSON object")
    if (
        data.get("dataset_id") != _EXPECTED_DATASET_ID
        or data.get("evidence_kind") != "EXPERIMENTAL"
        or data.get("provenance") != "PRIMARY_SOURCE"
        or data.get("observable_id") != "mass_density"
        or data["source"]["doi"] != _EXPECTED_SOURCE_DOI
        or data.get("sample_count") != 61
        or data.get("sample_count_by_run") != _RUN_COUNTS
    ):
        raise ValueError("experimental dataset identity or provenance changed")

    runs = data["runs"]
    if set(runs) != set(_RUN_COUNTS):
        raise ValueError("experimental run identity changed")
    if any(len(runs[name]) != count for name, count in _RUN_COUNTS.items()):
        raise ValueError("experimental run cardinality changed")

    flat = [
        [run_id, *record]
        for run_id in _RUN_COUNTS
        for record in runs[run_id]
    ]
    serialized = json.dumps(flat, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(serialized.encode("ascii")).hexdigest()
    if digest != _MEASUREMENTS_SHA256:
        raise ValueError("experimental table fingerprint mismatch")
    return data


def _load_registered_correlation() -> dict[str, object]:
    """Obtain live correlation metadata from the existing executable benchmark."""

    namespace = runpy.run_path(str(_BASELINE), run_name="density_baseline_import")
    baseline = namespace["run_benchmark"]()
    if (
        baseline["status"] != "PASS"
        or baseline["benchmark_id"] != _EXPECTED_BASELINE_ID
        or baseline["source_id"] != _EXPECTED_CORRELATION_SOURCE
    ):
        raise ValueError("registered baseline benchmark is not qualified")
    return baseline["source_correlation"]


def run_diagnostic() -> dict[str, object]:
    """Compute unmatched-source residuals without claiming physical validation."""

    dataset = _load_dataset()
    correlation = _load_registered_correlation()
    domain = dataset["domain"]
    measured = domain["measured_composition"]
    measured_bef2 = measured["bef2_mol_percent"]
    registered_bef2 = correlation["bef2_mol_percent"]
    if (
        measured["method"] != "ICP-MS"
        or domain["model_composition_67_33_direct_match"] is not False
        or measured_bef2 == registered_bef2
    ):
        raise ValueError("the non-matched composition evidence boundary changed")

    samples: list[dict[str, object]] = []
    excluded: dict[str, int] = {
        "outside_correlation_temperature_domain": 0,
        "below_reported_melting_temperature": 0,
    }
    by_run = {run_id: 0 for run_id in _RUN_COUNTS}
    residuals: list[float] = []
    lower = correlation["temperature_min_k"]
    upper = correlation["temperature_max_k"]

    for run_id, run in dataset["runs"].items():
        for temperature_c, temperature_u_c, density, density_u in run:
            temperature_k = temperature_c + _CELSIUS_TO_KELVIN
            if temperature_c < domain["reported_melting_temperature_c"]:
                excluded["below_reported_melting_temperature"] += 1
            if not lower <= temperature_k <= upper:
                excluded["outside_correlation_temperature_domain"] += 1
                continue
            if temperature_c < domain["reported_melting_temperature_c"]:
                continue

            baseline_density = (
                correlation["density_intercept_kg_m3"]
                + correlation["density_slope_kg_m3_per_k"] * temperature_k
            )
            residual = baseline_density - density
            residuals.append(residual)
            by_run[run_id] += 1
            samples.append(
                {
                    "run_id": run_id,
                    "temperature_c": temperature_c,
                    "temperature_k": temperature_k,
                    "temperature_standard_uncertainty_c": temperature_u_c,
                    "measured_density_kg_m3": density,
                    "measured_density_standard_uncertainty_kg_m3": density_u,
                    "registered_correlation_density_kg_m3": baseline_density,
                    "unmatched_source_residual_kg_m3": residual,
                }
            )

    if not residuals:
        raise ValueError("no observations in the registered temperature domain")
    count = len(residuals)
    return {
        "diagnostic_id": "tr-eif.flibe.vidrio-vs-registered-density.unmatched.v1",
        "status": "DIAGNOSTIC_ONLY",
        "experimental_dataset_id": dataset["dataset_id"],
        "experimental_source_doi": dataset["source"]["doi"],
        "registered_correlation_source_id": _EXPECTED_CORRELATION_SOURCE,
        "observable": "mass_density",
        "comparison_scope": "OVERLAPPING_NOMINAL_TEMPERATURE_ONLY",
        "physical_validation_status": "NOT_ESTABLISHED",
        "tr_eip_prediction_status": "REQUIRES_MODEL_OUTPUT",
        "first_principles_comparison_status": "REQUIRES_SOURCE",
        "source_state_compatibility": {
            "measured_bef2_mol_percent": measured_bef2,
            "measured_bef2_reported_uncertainty_mol_percent": (
                measured["bef2_reported_uncertainty_mol_percent"]
            ),
            "registered_bef2_mol_percent": registered_bef2,
            "composition_exact_match": False,
            "pressure_match": "NOT_ESTABLISHED_FOR_REGISTERED_CORRELATION",
            "experimental_pressure_kpa": domain["pressure_kpa"],
            "experimental_pressure_standard_uncertainty_kpa": (
                domain["pressure_standard_uncertainty_kpa"]
            ),
            "uncertainty_policy": (
                "Measured uncertainties preserved; not applied as acceptance "
                "tolerances and no source-correlation uncertainty inferred."
            ),
        },
        "counts": {
            "registered_measurements": dataset["sample_count"],
            "temperature_domain_samples": count,
            "by_run": by_run,
            "excluded": excluded,
            "below_melting_is_subset_of_outside_temperature_domain": True,
        },
        "exploratory_error_summary": {
            "mean_absolute_residual_kg_m3": sum(map(abs, residuals)) / count,
            "root_mean_square_residual_kg_m3": sqrt(
                sum(residual * residual for residual in residuals) / count
            ),
            "maximum_absolute_residual_kg_m3": max(map(abs, residuals)),
        },
        "samples": samples,
        "qualification_boundary": (
            "These are unmatched source-to-source diagnostics, not direct "
            "state-matched evidence, not TR-EIP predictions, and not model "
            "validation. Do not apply these residuals as a physical PASS criterion."
        ),
    }


def main() -> None:
    """Emit deterministic diagnostic JSON without a physical PASS claim."""

    print(json.dumps(run_diagnostic(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
