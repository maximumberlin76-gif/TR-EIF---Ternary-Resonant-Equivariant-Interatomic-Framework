
"""Independent Table 4 qualification of the Vidrio 2022 FLiBe density data.

These tests validate source identity, registered measurements, units, and
qualification boundaries. They do not test TR-EIP prediction accuracy.
"""

from __future__ import annotations

import hashlib
import json
from math import isfinite
from pathlib import Path


_DATASET = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "reference"
    / "flibe_vidrio_2022_density_measurements.json"
)
_SOURCE_DOI = "10.1021/acs.jced.2c00212"
_TABLE4_VALUES_SHA256 = "8ff807a4b1b96a806be33277d9ad80338787836f619bbfe66500772e9b8899aa"
_RUN_LENGTHS = {"0A": 28, "1A": 7, "1B": 13, "1C": 13}
_COLUMNS = [
    "temperature_c",
    "temperature_standard_uncertainty_c",
    "density_kg_m3",
    "density_standard_uncertainty_kg_m3",
]
# Independently published Table 4 anchors, including uncertainty notation.
_PUBLISHED_ANCHORS = {
    "0A": {0: [461, 3, 2043, 3], 17: [601, 5, 1984, 3], 27: [700, 5, 1939, 3]},
    "1A": {0: [467, 5, 2046, 3], 5: [630, 6, 1974, 4], 6: [675, 6, 1958, 4]},
    "1B": {0: [447, 19, 2054, 4], 2: [457, 19, 2049, 4], 12: [817, 19, 1893, 7]},
    "1C": {0: [481, 5, 2045, 3], 9: [716, 7, 1953, 3], 12: [795, 7, 1916, 3]},
}


def _load() -> dict[str, object]:
    """Read the committed experimental data, never an inline synthetic fixture."""

    with _DATASET.open("r", encoding="utf-8") as handle:
        dataset = json.load(handle)
    assert isinstance(dataset, dict)
    return dataset


def test_primary_publication_identity_and_units() -> None:
    """Published source metadata and physical units must remain explicit."""

    record = _load()
    assert record["dataset_id"] == "tr-eif.flibe.vidrio-2022.experimental-density.v1"
    assert record["evidence_kind"] == "EXPERIMENTAL"
    assert record["provenance"] == "PRIMARY_SOURCE"
    assert record["observable_id"] == "mass_density"
    assert record["source"]["doi"] == _SOURCE_DOI
    assert record["source"]["measurement_method"] == "hydrostatic buoyancy"
    assert record["source"]["source_location"].startswith("Table 4")
    assert record["columns"] == _COLUMNS


def test_all_four_source_runs_have_declared_cardinality() -> None:
    """No measurement series may be silently omitted, duplicated, or padded."""

    record = _load()
    runs = record["runs"]
    assert isinstance(runs, dict)
    assert set(runs) == set(_RUN_LENGTHS)
    assert record["sample_count_by_run"] == _RUN_LENGTHS
    assert record["sample_count"] == 61
    assert sum(len(runs[name]) for name in _RUN_LENGTHS) == 61
    for run_id, length in _RUN_LENGTHS.items():
        assert len(runs[run_id]) == length


def test_published_table_four_anchor_measurements() -> None:
    """Check selected primary-paper values, not generated model expectations."""

    runs = _load()["runs"]
    for run_id, anchors in _PUBLISHED_ANCHORS.items():
        for index, expected in anchors.items():
            assert runs[run_id][index] == expected


def test_full_source_table_four_transcription_fingerprint() -> None:
    """Pin every reported measurement and uncertainty across the four runs."""

    runs = _load()["runs"]
    flat = [
        [run_id, *sample]
        for run_id in ("0A", "1A", "1B", "1C")
        for sample in runs[run_id]
    ]
    canonical = json.dumps(flat, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest() == _TABLE4_VALUES_SHA256


def test_positive_finite_uncertainties_and_experimental_domain() -> None:
    """Measured uncertainty is preserved without selecting a model tolerance."""

    record = _load()
    domain = record["domain"]
    melting_temperature = domain["reported_melting_temperature_c"]
    assert melting_temperature == 459.1
    assert domain["temperature_range_c"] == [447, 817]
    assert domain["below_reported_melting_temperature_point_count"] == 3
    assert domain["pressure_kpa"] == 102
    assert domain["pressure_standard_uncertainty_kpa"] == 1

    all_samples = []
    for run_id, run in record["runs"].items():
        previous_temperature = None
        for sample in run:
            assert isinstance(sample, list) and len(sample) == 4
            temperature, temperature_uncertainty, density, density_uncertainty = sample
            assert all(
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and isfinite(value)
                for value in sample
            )
            assert temperature_uncertainty > 0
            assert density_uncertainty > 0
            assert density > 0
            if previous_temperature is not None:
                assert temperature > previous_temperature
            previous_temperature = temperature
            all_samples.append((run_id, temperature))

    assert min(temperature for _, temperature in all_samples) == 447
    assert max(temperature for _, temperature in all_samples) == 817
    assert [
        (run_id, temperature)
        for run_id, temperature in all_samples
        if temperature < melting_temperature
    ] == [("1B", 447), ("1B", 452), ("1B", 457)]


def test_composition_mismatch_and_scientific_claims_remain_explicit() -> None:
    """Registered measurements must not become model-validated predictions."""

    record = _load()
    domain = record["domain"]
    boundary = record["qualification_boundary"]
    assert domain["reported_composition"] == "2 LiF : 1 BeF2 (nominal)"
    assert domain["model_composition_67_33_direct_match"] is False
    assert boundary["source_data_status"] == "MEASURED_POINTS_TRANSCRIBED"
    assert boundary["physical_validation_status"] == "NOT_EVALUATED"
    assert boundary["independent_model_prediction"] == "REQUIRES_MODEL_OUTPUT"
