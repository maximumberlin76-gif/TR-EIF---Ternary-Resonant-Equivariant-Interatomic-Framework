
"""Compare published FLiBe density measurements and AIMD reference results.

Match AIMD temperatures to individual experimental series through piecewise
linear interpolation. Report density differences, input-source metadata,
measurement uncertainties, and the precise temperature selection procedure.
"""

from __future__ import annotations

import hashlib
import json
from math import isfinite, sqrt
from pathlib import Path


_ROOT = Path(__file__).resolve().parents[2]
_EXPERIMENT = _ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
_AIMD = _ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
_EXPERIMENT_TABLE_SHA256 = (
    "8ff807a4b1b96a806be33277d9ad80338787836f619bbfe66500772e9b8899aa"
)
_AIMD_TABLE_SHA256 = (
    "d19ea3d55e4c48f77d377571f3db3e01df5230c775ae9187ca9ba38a4601ccce"
)
_RUN_COUNTS = {"0A": 28, "1A": 7, "1B": 13, "1C": 13}
_KELVIN_OFFSET = 273.15
_G_CM3_TO_KG_M3 = 1000.0


def _read_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        result = json.load(handle)
    if not isinstance(result, dict):
        raise ValueError(f"Expected a JSON object in {path.name}")
    return result


def _digest(rows: list[object]) -> str:
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def _finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(value)
    )


def _load_experiment() -> dict[str, object]:
    source = _read_json(_EXPERIMENT)
    if (
        source.get("dataset_id") != "tr-eif.flibe.vidrio-2022.experimental-density.v1"
        or source.get("evidence_kind") != "EXPERIMENTAL"
        or source.get("provenance") != "PRIMARY_SOURCE"
        or source.get("observable_id") != "mass_density"
        or source["source"]["doi"] != "10.1021/acs.jced.2c00212"
        or source.get("columns") != [
            "temperature_c",
            "temperature_standard_uncertainty_c",
            "density_kg_m3",
            "density_standard_uncertainty_kg_m3",
        ]
        or source.get("sample_count") != 61
        or source.get("sample_count_by_run") != _RUN_COUNTS
    ):
        raise ValueError("Experimental source identity or table contract changed")

    runs = source["runs"]
    if set(runs) != set(_RUN_COUNTS):
        raise ValueError("Experimental run identifiers changed")
    for run_id, expected_count in _RUN_COUNTS.items():
        rows = runs[run_id]
        if len(rows) != expected_count:
            raise ValueError(f"Experimental run {run_id} cardinality changed")
        for row in rows:
            if (
                not isinstance(row, list)
                or len(row) != 4
                or not all(_finite_number(value) for value in row)
                or row[1] <= 0
                or row[2] <= 0
                or row[3] <= 0
            ):
                raise ValueError(f"Experimental run {run_id} measurement format changed")
        if any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
            raise ValueError(f"Experimental run {run_id} temperature ordering changed")

    flat = [[run_id, *row] for run_id in _RUN_COUNTS for row in runs[run_id]]
    if _digest(flat) != _EXPERIMENT_TABLE_SHA256:
        raise ValueError("Experimental table SHA-256 mismatch")

    composition = source["domain"]["measured_composition"]
    if (
        composition["method"] != "ICP-MS"
        or composition["bef2_mol_percent"] != 33.58
        or composition["bef2_reported_uncertainty_mol_percent"] != 0.05
    ):
        raise ValueError("Experimental composition record changed")
    return source


def _load_aimd() -> dict[str, object]:
    source = _read_json(_AIMD)
    if (
        source.get("dataset_id") != "tr-eif.flibe.baral-2021.aimd-structural-density.v1"
        or source.get("evidence_kind") != "FIRST_PRINCIPLES"
        or source.get("provenance") != "PRIMARY_SOURCE"
        or source.get("observable_id") != "mass_density"
        or source["source"]["doi"] != "10.1021/acsomega.1c02528"
        or source.get("columns") != [
            "temperature_k",
            "cubic_cell_edge_angstrom",
            "reported_cell_volume_angstrom3",
            "simulated_density_g_cm3",
        ]
        or source["table_units"]["temperature"] != "K"
        or source["table_units"]["simulated_density"] != "g/cm^3"
        or source.get("sample_count") != 9
        or source["material"]["bef2_formula_unit_fraction"] != "1/3"
        or source["material"]["lif_formula_unit_fraction"] != "2/3"
    ):
        raise ValueError("AIMD source identity or table contract changed")

    rows = source["samples"]
    for row in rows:
        if (
            not isinstance(row, list)
            or len(row) != 4
            or not all(_finite_number(value) and value > 0 for value in row)
        ):
            raise ValueError("AIMD table row format changed")
    if any(b[0] <= a[0] for a, b in zip(rows, rows[1:])):
        raise ValueError("AIMD temperature ordering changed")
    if _digest(rows) != _AIMD_TABLE_SHA256:
        raise ValueError("AIMD table SHA-256 mismatch")
    return source


def _interpolate_run(
    rows: list[list[float]], temperature_c: float
) -> dict[str, object] | None:
    """Interpolate between adjacent source measurements in one run."""

    for lower, upper in zip(rows, rows[1:]):
        if lower[0] <= temperature_c <= upper[0]:
            weight = (temperature_c - lower[0]) / (upper[0] - lower[0])
            return {
                "lower_measurement": lower,
                "upper_measurement": upper,
                "source_columns": [
                    "temperature_c",
                    "temperature_standard_uncertainty_c",
                    "density_kg_m3",
                    "density_standard_uncertainty_kg_m3",
                ],
                "interpolation_weight_upper": weight,
                "interpolated_density_kg_m3": (
                    (1.0 - weight) * lower[2] + weight * upper[2]
                ),
            }
    return None


def run_comparison() -> dict[str, object]:
    """Calculate reproducible temperature-screened source density differences."""

    experiment = _load_experiment()
    aimd = _load_aimd()
    domain = experiment["domain"]
    if (
        domain["temperature_range_c"] != [447, 817]
        or domain["reported_melting_temperature_c"] != 459.1
        or domain["pressure_kpa"] != 102
        or domain["pressure_standard_uncertainty_kpa"] != 1
    ):
        raise ValueError("Experimental state metadata changed")

    comparisons: list[dict[str, object]] = []
    screened_rows: list[dict[str, object]] = []
    residuals: list[float] = []
    for temperature_k, edge, volume, density_g_cm3 in aimd["samples"]:
        temperature_c = temperature_k - _KELVIN_OFFSET
        if not domain["temperature_range_c"][0] <= temperature_c <= domain["temperature_range_c"][1]:
            screened_rows.append({
                "temperature_k": temperature_k,
                "screening_category": "OUTSIDE_EXPERIMENTAL_TEMPERATURE_INTERVAL",
            })
            continue
        if temperature_c < domain["reported_melting_temperature_c"]:
            screened_rows.append({
                "temperature_k": temperature_k,
                "screening_category": "BELOW_REPORTED_EXPERIMENTAL_MELTING_TEMPERATURE",
            })
            continue

        density_kg_m3 = density_g_cm3 * _G_CM3_TO_KG_M3
        brackets: list[dict[str, object]] = []
        for run_id in _RUN_COUNTS:
            value = _interpolate_run(experiment["runs"][run_id], temperature_c)
            if value is None:
                continue
            residual = density_kg_m3 - value["interpolated_density_kg_m3"]
            residuals.append(residual)
            brackets.append({
                "run_id": run_id,
                **value,
                "aimd_minus_experimental_density_kg_m3": residual,
            })

        comparisons.append({
            "aimd_temperature_k": temperature_k,
            "aimd_temperature_c": temperature_c,
            "aimd_density_kg_m3": density_kg_m3,
            "aimd_cubic_cell_edge_angstrom": edge,
            "aimd_cell_volume_angstrom3": volume,
            "within_run_comparisons": brackets,
        })

    temperatures = [row["aimd_temperature_k"] for row in comparisons]
    if temperatures != [750, 850, 1000]:
        raise ValueError("Temperature selection cardinality changed")
    if len(residuals) != 9 or len(screened_rows) != 6:
        raise ValueError("Comparison cardinality changed")

    return {
        "comparison_id": "tr-eif.flibe.vidrio-2022.baral-2021.density.v1",
        "observable": "mass_density",
        "method": "WITHIN_RUN_LINEAR_TEMPERATURE_INTERPOLATION",
        "temperature_screening": {
            "experimental_temperature_range_c": domain["temperature_range_c"],
            "experimental_melting_temperature_c": domain["reported_melting_temperature_c"],
            "evaluated_aimd_temperatures_k": temperatures,
        },
        "sources": {
            "experimental": {
                "dataset_id": experiment["dataset_id"],
                "doi": experiment["source"]["doi"],
                "composition_bef2_mol_percent": (
                    domain["measured_composition"]["bef2_mol_percent"]
                ),
                "composition_reported_uncertainty_mol_percent": (
                    domain["measured_composition"]["bef2_reported_uncertainty_mol_percent"]
                ),
                "pressure_kpa": domain["pressure_kpa"],
                "pressure_standard_uncertainty_kpa": (
                    domain["pressure_standard_uncertainty_kpa"]
                ),
            },
            "first_principles": {
                "dataset_id": aimd["dataset_id"],
                "doi": aimd["source"]["doi"],
                "formula": aimd["material"]["formula"],
                "composition_bef2_formula_unit_fraction": "1/3",
                "reported_supercell_atom_count": aimd["source"]["reported_supercell_atom_count"],
                "pressure_kpa": None,
                "density_standard_uncertainty_kg_m3": None,
            },
        },
        "counts": {
            "experimental_measurements": experiment["sample_count"],
            "aimd_table_rows": aimd["sample_count"],
            "evaluated_aimd_rows": len(comparisons),
            "screened_aimd_rows": len(screened_rows),
            "interpolated_pairs": len(residuals),
        },
        "density_difference_summary_kg_m3": {
            "mean": sum(residuals) / len(residuals),
            "mean_absolute": sum(abs(value) for value in residuals) / len(residuals),
            "root_mean_square": sqrt(sum(value * value for value in residuals) / len(residuals)),
            "minimum": min(residuals),
            "maximum": max(residuals),
        },
        "comparisons": comparisons,
        "screened_aimd_rows": screened_rows,
    }


def main() -> None:
    print(json.dumps(run_comparison(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
