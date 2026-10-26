"""Independent qualification of typed Vidrio and Baral density-table loading."""

from __future__ import annotations

import hashlib
import json
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest

from tr_eif.flibe.registered_density_sources import (
    FLiBeRegisteredDensityRecord,
    load_flibe_density_source_records,
)
from tr_eif.flibe.reference_comparison import FLiBeEvidenceKind
from tr_eif.flibe.trajectory_state_correspondence import FLiBeDensitySourceCoordinates
from tr_eif.flibe.units import ParameterProvenance


_ROOT = Path(__file__).resolve().parents[2]
_VIDRIO_PATH = _ROOT / "data/reference/flibe_vidrio_2022_density_measurements.json"
_BARAL_PATH = _ROOT / "data/reference/flibe_baral_2021_aimd_density.json"
_VIDRIO_ID = "tr-eif.flibe.vidrio-2022.experimental-density.v1"
_BARAL_ID = "tr-eif.flibe.baral-2021.aimd-structural-density.v1"
_VIDRIO_DOI = "10.1021/acs.jced.2c00212"
_BARAL_DOI = "10.1021/acsomega.1c02528"
_RUN_COUNTS = {"0A": 28, "1A": 7, "1B": 13, "1C": 13}
_NORMALIZATION = "source-reported-mass-density"
_VIDRIO_COLUMNS = (
    "temperature_c",
    "temperature_standard_uncertainty_c",
    "density_kg_m3",
    "density_standard_uncertainty_kg_m3",
)
_BARAL_COLUMNS = (
    "temperature_k",
    "cubic_cell_edge_angstrom",
    "reported_cell_volume_angstrom3",
    "simulated_density_g_cm3",
)

# Published Table 4 anchors, including measured standard uncertainties.
_VIDRIO_ANCHORS = (
    ("0A", 0, (461, 3, 2043, 3)),
    ("0A", 17, (601, 5, 1984, 3)),
    ("0A", 27, (700, 5, 1939, 3)),
    ("1A", 0, (467, 5, 2046, 3)),
    ("1A", 6, (675, 6, 1958, 4)),
    ("1B", 0, (447, 19, 2054, 4)),
    ("1B", 2, (457, 19, 2049, 4)),
    ("1B", 12, (817, 19, 1893, 7)),
    ("1C", 0, (481, 5, 2045, 3)),
    ("1C", 12, (795, 7, 1916, 3)),
)

# Published Baral Table 1 positive-temperature labels and densities in g/cm^3.
_BARAL_TEMPERATURE_DENSITY = (
    (300, 1.866), (450, 1.840), (700, 1.800),
    (730, 1.788), (750, 1.757), (850, 1.731),
    (1000, 1.675), (1500, 1.597), (2000, 1.571),
)


def _json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _write_changed(tmp_path: Path, source: Path, data: dict[str, Any]) -> Path:
    changed = tmp_path / source.name
    changed.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return changed


def _assign(data: dict[str, Any], path: tuple[str, ...], value: object) -> None:
    target: dict[str, Any] = data
    for name in path[:-1]:
        target = target[name]
    target[path[-1]] = value


def test_vidrio_all_runs_and_distinct_record_identities() -> None:
    records = load_flibe_density_source_records(_VIDRIO_PATH)
    assert isinstance(records, tuple)
    assert len(records) == 61
    assert len({record.record_id for record in records}) == 61
    assert [record.run_id for record in records] == [
        run for run, length in _RUN_COUNTS.items() for _ in range(length)
    ]
    for run_id, expected_count in _RUN_COUNTS.items():
        subset = [record for record in records if record.run_id == run_id]
        assert len(subset) == expected_count
        assert [record.row_index for record in subset] == list(range(expected_count))
        assert [record.record_id for record in subset] == [
            f"{_VIDRIO_ID}/{run_id}/{index:02d}" for index in range(expected_count)
        ]


def test_vidrio_independent_published_measurement_anchors() -> None:
    by_key = {
        (record.run_id, record.row_index): record
        for record in load_flibe_density_source_records(_VIDRIO_PATH)
    }
    for run_id, row_index, expected in _VIDRIO_ANCHORS:
        record = by_key[run_id, row_index]
        assert record.source_values == expected
        assert record.coordinates.temperature_k == pytest.approx(expected[0] + 273.15)
        assert record.coordinates.temperature_standard_uncertainty_k == expected[1]
        assert record.coordinates.density_kg_m3 == expected[2]
        assert record.coordinates.density_standard_uncertainty_kg_m3 == expected[3]


def test_vidrio_all_rows_preserve_source_values_and_si_uncertainties() -> None:
    source = _json(_VIDRIO_PATH)
    records = load_flibe_density_source_records(_VIDRIO_PATH)
    for record in records:
        original = source["runs"][record.run_id][record.row_index]
        assert record.source_columns == _VIDRIO_COLUMNS
        assert record.source_values == tuple(original)
        assert record.coordinates.temperature_k == pytest.approx(original[0] + 273.15)
        assert record.coordinates.density_kg_m3 == original[2]
        assert record.coordinates.temperature_standard_uncertainty_k == original[1]
        assert record.coordinates.density_standard_uncertainty_kg_m3 == original[3]
        assert record.coordinates.pressure_pa == 102000.0
        assert record.coordinates.pressure_standard_uncertainty_pa == 1000.0
        assert record.coordinates.bef2_fraction_standard_uncertainty == 0.0005
        assert record.coordinates.physical_state_id is None
        assert record.coordinates.normalization_id == _NORMALIZATION
        assert record.coordinates.evidence_kind is FLiBeEvidenceKind.EXPERIMENTAL
        assert record.coordinates.provenance is ParameterProvenance.PRIMARY_SOURCE
        assert record.coordinates.source_id == _VIDRIO_ID
        assert record.coordinates.method_id == "hydrostatic buoyancy"
        assert record.dataset_id == _VIDRIO_ID
        assert record.doi == _VIDRIO_DOI
        assert record.source_location.startswith("Table 4")


def test_vidrio_measured_composition_and_below_melting_rows_remain_distinct() -> None:
    records = load_flibe_density_source_records(_VIDRIO_PATH)
    for record in records:
        composition = record.coordinates.composition
        assert composition.bef2_fraction == pytest.approx(0.3358, abs=1e-15)
        assert composition.lif_fraction == pytest.approx(0.6642, abs=1e-15)
        assert composition.bef2_fraction != 1.0 / 3.0
        assert composition.bef2_fraction != 0.33
    below_melting = [
        (record.run_id, record.source_values[0])
        for record in records if record.source_values[0] < 459.1
    ]
    assert below_melting == [("1B", 447.0), ("1B", 452.0), ("1B", 457.0)]
    assert all(record.coordinates.physical_state_id is None for record in records)


def test_baral_all_nine_source_temperatures_and_densities() -> None:
    records = load_flibe_density_source_records(_BARAL_PATH)
    assert isinstance(records, tuple)
    assert len(records) == 9
    assert [record.record_id for record in records] == [
        f"{_BARAL_ID}/T{temperature}" for temperature, _ in _BARAL_TEMPERATURE_DENSITY
    ]
    assert len({record.record_id for record in records}) == 9
    for index, (record, (temperature, density_g_cm3)) in enumerate(
        zip(records, _BARAL_TEMPERATURE_DENSITY, strict=True)
    ):
        assert record.row_index == index
        assert record.run_id is None
        assert record.source_values[0] == temperature
        assert record.source_values[3] == density_g_cm3
        assert record.coordinates.temperature_k == temperature
        assert record.coordinates.density_kg_m3 == pytest.approx(density_g_cm3 * 1000.0)
        assert record.coordinates.evidence_kind is FLiBeEvidenceKind.FIRST_PRINCIPLES
        assert record.coordinates.provenance is ParameterProvenance.PRIMARY_SOURCE
        assert record.coordinates.source_id == _BARAL_ID
        assert record.coordinates.method_id == "ab initio molecular dynamics"
        assert record.dataset_id == _BARAL_ID
        assert record.doi == _BARAL_DOI
        assert record.source_location.startswith("Table 1")
        assert record.source_columns == _BARAL_COLUMNS
        assert record.coordinates.normalization_id == _NORMALIZATION


def test_baral_source_geometry_is_preserved_without_recomputing_density() -> None:
    payload = _json(_BARAL_PATH)
    records = load_flibe_density_source_records(_BARAL_PATH)
    assert len(payload["samples"]) == len(records) == 9
    for record, original in zip(records, payload["samples"], strict=True):
        assert record.source_values == tuple(original)
        assert record.source_values[1] > 0.0  # Published cell edge, angstrom.
        assert record.source_values[2] > 0.0  # Published cell volume, angstrom^3.
    assert records[0].source_values == (300, 18.538, 6370.928, 1.866)
    assert records[4].source_values == (750, 18.915, 6767.367, 1.757)
    assert records[8].source_values == (2000, 19.597, 7525.745, 1.571)


def test_baral_missing_pressure_phase_and_uncertainties_remain_missing() -> None:
    records = load_flibe_density_source_records(_BARAL_PATH)
    for record in records:
        state = record.coordinates
        assert state.composition.lif_fraction == pytest.approx(2.0 / 3.0)
        assert state.composition.bef2_fraction == pytest.approx(1.0 / 3.0)
        assert state.composition.bef2_fraction != pytest.approx(0.3358, abs=1e-5)
        assert state.pressure_pa is None
        assert state.physical_state_id is None
        assert state.density_standard_uncertainty_kg_m3 is None
        assert state.temperature_standard_uncertainty_k is None
        assert state.pressure_standard_uncertainty_pa is None
        assert state.bef2_fraction_standard_uncertainty is None


@pytest.mark.parametrize("source", (_VIDRIO_PATH, _BARAL_PATH))
def test_source_provenance_digest_matches_independently_hashed_file(source: Path) -> None:
    records = load_flibe_density_source_records(source)
    independent_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    assert {record.source_file_sha256 for record in records} == {independent_sha256}
    assert len(independent_sha256) == 64
    assert records == load_flibe_density_source_records(str(source))
    assert all(isinstance(record, FLiBeRegisteredDensityRecord) for record in records)
    assert all(isinstance(record.coordinates, FLiBeDensitySourceCoordinates) for record in records)


def test_record_fields_are_immutable() -> None:
    record = load_flibe_density_source_records(_BARAL_PATH)[0]
    with pytest.raises(FrozenInstanceError):
        record.record_id = "changed"  # type: ignore[misc]


def test_source_fingerprint_changes_for_modified_valid_row(tmp_path: Path) -> None:
    baseline = load_flibe_density_source_records(_VIDRIO_PATH)
    payload = _json(_VIDRIO_PATH)
    payload["runs"]["0A"][0][2] = 2044
    changed = load_flibe_density_source_records(_write_changed(tmp_path, _VIDRIO_PATH, payload))
    assert changed[0].source_values == (461, 3, 2044, 3)
    assert changed[0].coordinates.density_kg_m3 == 2044.0
    assert changed[0].source_file_sha256 != baseline[0].source_file_sha256
    assert changed[1].record_id == baseline[1].record_id


@pytest.mark.parametrize(
    ("source", "path", "value", "message"),
    (
        (_VIDRIO_PATH, ("evidence_kind",), "FIRST_PRINCIPLES", "identity or column"),
        (_VIDRIO_PATH, ("provenance",), "DERIVED", "identity or column"),
        (_VIDRIO_PATH, ("observable_id",), "viscosity", "identity or column"),
        (_VIDRIO_PATH, ("source", "doi"), "10.0000/wrong", "identity or column"),
        (_VIDRIO_PATH, ("columns",), ["temperature_c"], "identity or column"),
        (_VIDRIO_PATH, ("source", "measurement_method"), None, "method identifier"),
        (_VIDRIO_PATH, ("source", "source_location"), "", "table location"),
        (_VIDRIO_PATH, ("sample_count",), 60, "run or measurement count"),
        (_VIDRIO_PATH, ("domain", "pressure_kpa"), -10, "pressure_kpa"),
        (_VIDRIO_PATH, ("domain", "measured_composition", "bef2_mol_percent"), 101.0, "molar fraction"),
        (_VIDRIO_PATH, ("domain", "measured_composition", "bef2_mol_percent"), False, "finite numeric"),
        (_VIDRIO_PATH, ("domain", "measured_composition", "bef2_reported_uncertainty_mol_percent"), -0.05, "uncertainty"),
        (_BARAL_PATH, ("evidence_kind",), "EXPERIMENTAL", "identity or column"),
        (_BARAL_PATH, ("provenance",), "DERIVED", "identity or column"),
        (_BARAL_PATH, ("source", "doi"), "10.0000/wrong", "identity or column"),
        (_BARAL_PATH, ("source", "computational_method"), "", "method identifier"),
        (_BARAL_PATH, ("material", "formula"), "LiF", "composition or source-unit"),
        (_BARAL_PATH, ("material", "bef2_formula_unit_fraction"), "0.33", "composition or source-unit"),
        (_BARAL_PATH, ("table_units", "simulated_density"), "kg/m^3", "composition or source-unit"),
        (_BARAL_PATH, ("sample_count",), 8, "cardinality"),
    ),
)
def test_loader_rejects_mismatched_registered_contracts(
    tmp_path: Path,
    source: Path,
    path: tuple[str, ...],
    value: object,
    message: str,
) -> None:
    payload = _json(source)
    _assign(payload, path, value)
    with pytest.raises(ValueError, match=message):
        load_flibe_density_source_records(_write_changed(tmp_path, source, payload))


@pytest.mark.parametrize(
    ("run", "row", "column", "value", "message"),
    (
        ("0A", 0, 0, True, "finite numeric"),
        ("0A", 0, 0, None, "finite numeric"),
        ("0A", 0, 1, 0, "positive"),
        ("0A", 0, 2, -1, "positive"),
        ("0A", 0, 2, float("nan"), "positive"),
        ("1B", 2, 0, 452, "temperatures must increase"),
        ("1C", 0, 3, 0, "positive"),
    ),
)
def test_vidrio_malformed_source_measurements_raise(
    tmp_path: Path, run: str, row: int, column: int, value: object, message: str,
) -> None:
    payload = _json(_VIDRIO_PATH)
    payload["runs"][run][row][column] = value
    with pytest.raises(ValueError, match=message):
        load_flibe_density_source_records(_write_changed(tmp_path, _VIDRIO_PATH, payload))


def test_vidrio_missing_row_and_malformed_row_length_raise(tmp_path: Path) -> None:
    missing = _json(_VIDRIO_PATH)
    missing["runs"]["0A"].pop()
    with pytest.raises(ValueError, match="must contain 28 rows"):
        load_flibe_density_source_records(_write_changed(tmp_path, _VIDRIO_PATH, missing))
    malformed = _json(_VIDRIO_PATH)
    malformed["runs"]["1A"][0] = [467, 5, 2046]
    with pytest.raises(ValueError, match="cardinality"):
        load_flibe_density_source_records(_write_changed(tmp_path, _VIDRIO_PATH, malformed))


@pytest.mark.parametrize(
    ("row", "column", "value", "message"),
    (
        (0, 0, False, "finite numeric"),
        (0, 1, 0.0, "positive"),
        (0, 2, -1.0, "positive"),
        (0, 3, float("inf"), "positive"),
        (2, 0, 450, "temperature order or source label"),
    ),
)
def test_baral_malformed_samples_raise(
    tmp_path: Path, row: int, column: int, value: object, message: str,
) -> None:
    payload = _json(_BARAL_PATH)
    payload["samples"][row][column] = value
    with pytest.raises(ValueError, match=message):
        load_flibe_density_source_records(_write_changed(tmp_path, _BARAL_PATH, payload))


def test_baral_mismatched_label_and_row_cardinality_raise(tmp_path: Path) -> None:
    wrong_label = _json(_BARAL_PATH)
    wrong_label["source_temperature_labels_included"][4] = "T751"
    with pytest.raises(ValueError, match="temperature order or source label"):
        load_flibe_density_source_records(_write_changed(tmp_path, _BARAL_PATH, wrong_label))
    missing_row = _json(_BARAL_PATH)
    missing_row["samples"].pop()
    with pytest.raises(ValueError, match="cardinality"):
        load_flibe_density_source_records(_write_changed(tmp_path, _BARAL_PATH, missing_row))
    wrong_width = _json(_BARAL_PATH)
    wrong_width["samples"][0] = [300, 18.538, 6370.928]
    with pytest.raises(ValueError, match="cardinality"):
        load_flibe_density_source_records(_write_changed(tmp_path, _BARAL_PATH, wrong_width))


@pytest.mark.parametrize("invalid", (None, 4, True, 3.5, object()))
def test_loader_rejects_nonpath_arguments(invalid: object) -> None:
    with pytest.raises(TypeError, match="path must be"):
        load_flibe_density_source_records(invalid)


def test_loader_rejects_unknown_dataset_and_nonmapping_json(tmp_path: Path) -> None:
    unknown = tmp_path / "unknown.json"
    unknown.write_text('{"dataset_id": "UNREGISTERED"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Unknown FLiBe density dataset"):
        load_flibe_density_source_records(unknown)
    nonmapping = tmp_path / "array.json"
    nonmapping.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        load_flibe_density_source_records(nonmapping)


def test_loader_propagates_missing_file_and_invalid_json(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_flibe_density_source_records(tmp_path / "missing.json")
    invalid = tmp_path / "malformed.json"
    invalid.write_text("{", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_flibe_density_source_records(invalid)
