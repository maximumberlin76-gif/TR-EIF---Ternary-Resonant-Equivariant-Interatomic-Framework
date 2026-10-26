"""Source-resolved FLiBe density records from registered reference tables."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

from .composition import FLiBeComposition
from .reference_comparison import FLiBeEvidenceKind
from .trajectory_state_correspondence import FLiBeDensitySourceCoordinates
from .units import ParameterProvenance


_VIDRIO_ID = "tr-eif.flibe.vidrio-2022.experimental-density.v1"
_BARAL_ID = "tr-eif.flibe.baral-2021.aimd-structural-density.v1"
_VIDRIO_DOI = "10.1021/acs.jced.2c00212"
_BARAL_DOI = "10.1021/acsomega.1c02528"

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

_RUN_COUNTS = {
    "0A": 28,
    "1A": 7,
    "1B": 13,
    "1C": 13,
}

_NORMALIZATION = "source-reported-mass-density"


@dataclass(frozen=True, slots=True)
class FLiBeRegisteredDensityRecord:
    """One source table row and its SI-valued physical coordinates."""

    dataset_id: str
    record_id: str
    doi: str
    source_location: str
    source_file_sha256: str
    run_id: str | None
    row_index: int
    source_columns: tuple[str, ...]
    source_values: tuple[float, ...]
    coordinates: FLiBeDensitySourceCoordinates

    def __post_init__(self) -> None:
        for name in (
            "dataset_id",
            "record_id",
            "doi",
            "source_location",
        ):
            value = getattr(self, name)

            if (
                not isinstance(value, str)
                or not value
                or value != value.strip()
            ):
                raise ValueError(
                    f"{name} must be a nonempty trimmed string."
                )

        digest = self.source_file_sha256

        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(
                character not in "0123456789abcdef"
                for character in digest
            )
        ):
            raise ValueError(
                "source_file_sha256 must contain 64 hexadecimal digits."
            )

        if self.run_id is not None and (
            not isinstance(self.run_id, str)
            or not self.run_id
        ):
            raise ValueError(
                "run_id must be a nonempty string or None."
            )

        if (
            isinstance(self.row_index, bool)
            or not isinstance(self.row_index, int)
            or self.row_index < 0
        ):
            raise ValueError(
                "row_index must be a nonnegative integer."
            )

        if len(self.source_columns) != len(self.source_values):
            raise ValueError(
                "source columns and row values must have equal lengths."
            )

        if not isinstance(
            self.coordinates,
            FLiBeDensitySourceCoordinates,
        ):
            raise TypeError(
                "coordinates must be FLiBeDensitySourceCoordinates."
            )


def _mapping(
    value: object,
    name: str,
) -> dict[str, object]:
    if (
        not isinstance(value, dict)
        or any(not isinstance(k, str) for k in value)
    ):
        raise ValueError(
            f"{name} must be a JSON object with string keys."
        )

    return value


def _number(
    value: object,
    name: str,
    *,
    positive: bool = False,
) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
    ):
        raise ValueError(
            f"{name} must be a finite numeric value."
        )

    number = float(value)

    if (
        not isfinite(number)
        or number < 0.0
        or (positive and number == 0.0)
    ):
        requirement = "positive" if positive else "nonnegative"

        raise ValueError(
            f"{name} must be finite and {requirement}."
        )

    return number


def _row(
    value: object,
    columns: tuple[str, ...],
) -> tuple[float, ...]:
    if (
        not isinstance(value, list)
        or len(value) != len(columns)
    ):
        raise ValueError(
            "Source row cardinality differs from declared columns."
        )

    return tuple(
        _number(item, name, positive=True)
        for name, item in zip(columns, value)
    )


def _header(
    data: dict[str, object],
    *,
    dataset_id: str,
    doi: str,
    evidence_kind: FLiBeEvidenceKind,
    columns: tuple[str, ...],
) -> tuple[str, str]:
    source = _mapping(
        data.get("source"),
        "source",
    )

    if (
        data.get("dataset_id") != dataset_id
        or data.get("observable_id") != "mass_density"
        or data.get("provenance") != "PRIMARY_SOURCE"
        or data.get("evidence_kind") != evidence_kind.value
        or source.get("doi") != doi
        or data.get("columns") != list(columns)
    ):
        raise ValueError(
            "FLiBe source identity or column contract differs."
        )

    location = source.get("source_location")

    if (
        not isinstance(location, str)
        or not location.strip()
    ):
        raise ValueError(
            "Source table location must be specified."
        )

    method_name = (
        "measurement_method"
        if evidence_kind is FLiBeEvidenceKind.EXPERIMENTAL
        else "computational_method"
    )

    method = source.get(method_name)

    if (
        not isinstance(method, str)
        or not method.strip()
    ):
        raise ValueError(
            "Source method identifier must be specified."
        )

    return location, method


def _vidrio_records(
    data: dict[str, object],
    digest: str,
) -> tuple[FLiBeRegisteredDensityRecord, ...]:
    location, method = _header(
        data,
        dataset_id=_VIDRIO_ID,
        doi=_VIDRIO_DOI,
        evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
        columns=_VIDRIO_COLUMNS,
    )

    domain = _mapping(
        data.get("domain"),
        "domain",
    )

    measured = _mapping(
        domain.get("measured_composition"),
        "measured_composition",
    )

    be_fraction = (
        _number(
            measured.get("bef2_mol_percent"),
            "BeF2 mol%",
        )
        / 100.0
    )

    be_uncertainty = (
        _number(
            measured.get(
                "bef2_reported_uncertainty_mol_percent"
            ),
            "BeF2 reported uncertainty mol%",
        )
        / 100.0
    )

    if not 0.0 <= be_fraction <= 1.0:
        raise ValueError(
            "Measured BeF2 molar fraction must be within [0, 1]."
        )

    composition = FLiBeComposition(
        1.0 - be_fraction,
        be_fraction,
    )

    pressure_pa = (
        _number(
            domain.get("pressure_kpa"),
            "pressure_kpa",
        )
        * 1000.0
    )

    pressure_uncertainty_pa = (
        _number(
            domain.get("pressure_standard_uncertainty_kpa"),
            "pressure uncertainty",
        )
        * 1000.0
    )

    runs = _mapping(
        data.get("runs"),
        "runs",
    )

    if (
        set(runs) != set(_RUN_COUNTS)
        or data.get("sample_count_by_run") != _RUN_COUNTS
        or data.get("sample_count") != sum(_RUN_COUNTS.values())
    ):
        raise ValueError(
            "Vidrio registered run or measurement count differs."
        )

    records: list[FLiBeRegisteredDensityRecord] = []

    for run_id, expected_count in _RUN_COUNTS.items():
        values = runs[run_id]

        if (
            not isinstance(values, list)
            or len(values) != expected_count
        ):
            raise ValueError(
                f"Vidrio run {run_id} must contain "
                f"{expected_count} rows."
            )

        last_temperature_c = float("-inf")

        for row_index, raw in enumerate(values):
            temperature_c, u_t, density, u_density = _row(
                raw,
                _VIDRIO_COLUMNS,
            )

            if temperature_c <= last_temperature_c:
                raise ValueError(
                    f"Vidrio run {run_id} temperatures must increase."
                )

            last_temperature_c = temperature_c

            coordinates = FLiBeDensitySourceCoordinates(
                density_kg_m3=density,
                composition=composition,
                temperature_k=temperature_c + 273.15,
                pressure_pa=pressure_pa,
                physical_state_id=None,
                normalization_id=_NORMALIZATION,
                evidence_kind=FLiBeEvidenceKind.EXPERIMENTAL,
                source_id=_VIDRIO_ID,
                method_id=method,
                provenance=ParameterProvenance.PRIMARY_SOURCE,
                density_standard_uncertainty_kg_m3=u_density,
                temperature_standard_uncertainty_k=u_t,
                pressure_standard_uncertainty_pa=(
                    pressure_uncertainty_pa
                ),
                bef2_fraction_standard_uncertainty=(
                    be_uncertainty
                ),
            )

            records.append(
                FLiBeRegisteredDensityRecord(
                    dataset_id=_VIDRIO_ID,
                    record_id=(
                        f"{_VIDRIO_ID}/{run_id}/{row_index:02d}"
                    ),
                    doi=_VIDRIO_DOI,
                    source_location=location,
                    source_file_sha256=digest,
                    run_id=run_id,
                    row_index=row_index,
                    source_columns=_VIDRIO_COLUMNS,
                    source_values=(
                        temperature_c,
                        u_t,
                        density,
                        u_density,
                    ),
                    coordinates=coordinates,
                )
            )

    return tuple(records)


def _baral_records(
    data: dict[str, object],
    digest: str,
) -> tuple[FLiBeRegisteredDensityRecord, ...]:
    location, method = _header(
        data,
        dataset_id=_BARAL_ID,
        doi=_BARAL_DOI,
        evidence_kind=FLiBeEvidenceKind.FIRST_PRINCIPLES,
        columns=_BARAL_COLUMNS,
    )

    material = _mapping(
        data.get("material"),
        "material",
    )

    units = _mapping(
        data.get("table_units"),
        "table_units",
    )

    if (
        material.get("formula") != "Li2BeF4"
        or material.get("lif_formula_unit_fraction") != "2/3"
        or material.get("bef2_formula_unit_fraction") != "1/3"
        or units.get("temperature") != "K"
        or units.get("simulated_density") != "g/cm^3"
        or units.get("cubic_cell_edge") != "angstrom"
        or units.get("reported_cell_volume") != "angstrom^3"
    ):
        raise ValueError(
            "Baral composition or source-unit contract differs."
        )

    values = data.get("samples")

    labels = data.get(
        "source_temperature_labels_included"
    )

    if (
        not isinstance(values, list)
        or data.get("sample_count") != 9
        or len(values) != 9
        or not isinstance(labels, list)
        or len(labels) != 9
    ):
        raise ValueError(
            "Baral temperature-record cardinality differs."
        )

    composition = FLiBeComposition(
        2.0,
        1.0,
    )

    records: list[FLiBeRegisteredDensityRecord] = []

    last_temperature_k = float("-inf")

    for row_index, raw in enumerate(values):
        temperature_k, edge, volume, density_g_cm3 = _row(
            raw,
            _BARAL_COLUMNS,
        )

        label = labels[row_index]

        if (
            temperature_k <= last_temperature_k
            or not isinstance(label, str)
            or label != f"T{temperature_k:g}"
        ):
            raise ValueError(
                "Baral temperature order or source label differs."
            )

        last_temperature_k = temperature_k

        coordinates = FLiBeDensitySourceCoordinates(
            density_kg_m3=density_g_cm3 * 1000.0,
            composition=composition,
            temperature_k=temperature_k,
            pressure_pa=None,
            physical_state_id=None,
            normalization_id=_NORMALIZATION,
            evidence_kind=FLiBeEvidenceKind.FIRST_PRINCIPLES,
            source_id=_BARAL_ID,
            method_id=method,
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )

        records.append(
            FLiBeRegisteredDensityRecord(
                dataset_id=_BARAL_ID,
                record_id=f"{_BARAL_ID}/{label}",
                doi=_BARAL_DOI,
                source_location=location,
                source_file_sha256=digest,
                run_id=None,
                row_index=row_index,
                source_columns=_BARAL_COLUMNS,
                source_values=(
                    temperature_k,
                    edge,
                    volume,
                    density_g_cm3,
                ),
                coordinates=coordinates,
            )
        )

    return tuple(records)


def load_flibe_density_source_records(
    path: str | Path,
) -> tuple[FLiBeRegisteredDensityRecord, ...]:
    """Load the registered Vidrio or Baral density table with provenance.

    The caller supplies the repository data-file path. Returned source
    rows retain original table values and SI-converted physical coordinates.
    Unknown row-level phase and unregistered AIMD pressure are represented
    by None. Physical-state correspondence is evaluated by a separate
    operator.
    """

    if not isinstance(path, (str, Path)):
        raise TypeError(
            "path must be a string or pathlib.Path."
        )

    raw = Path(path).read_bytes()

    digest = hashlib.sha256(raw).hexdigest()

    payload = _mapping(
        json.loads(raw.decode("utf-8")),
        "source dataset",
    )

    dataset_id = payload.get("dataset_id")

    if dataset_id == _VIDRIO_ID:
        return _vidrio_records(
            payload,
            digest,
        )

    if dataset_id == _BARAL_ID:
        return _baral_records(
            payload,
            digest,
        )

    raise ValueError(
        "Unknown FLiBe density dataset identifier."
    )
