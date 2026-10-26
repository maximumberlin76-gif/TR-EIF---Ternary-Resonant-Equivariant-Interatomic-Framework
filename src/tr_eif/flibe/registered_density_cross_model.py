"""Source-resolved FLiBe MD density comparison under declared state mappings."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite, sqrt

from .registered_density_sources import FLiBeRegisteredDensityRecord
from .trajectory_state_correspondence import (
    FLiBeDensityStateCorrespondence,
    FLiBeTrajectoryStateCoordinates,
    compare_flibe_density_state_coordinates,
)
from .units import ParameterProvenance


MODEL_DENSITY_STATISTIC = "mean-instantaneous-cell-density"


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


def _tolerance(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative.")
    return result


@dataclass(frozen=True, slots=True)
class FLiBeDensityObservableMapping:
    """Declared pairing of an MD density statistic and a source density.

    The current model statistic is the arithmetic mean of instantaneous
    cell mass densities. The source-normalization identity is read from
    the registered dataset. Mapping provenance identifies the comparison
    procedure and its stated assumptions, independently of source data.
    """

    mapping_id: str
    model_statistic_id: str
    source_normalization_id: str
    method_id: str
    provenance: ParameterProvenance
    assumptions: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "mapping_id", "model_statistic_id", "source_normalization_id", "method_id"
        ):
            _identifier(getattr(self, name), name)
        if self.model_statistic_id != MODEL_DENSITY_STATISTIC:
            raise ValueError("model_statistic_id must select the MD mean density.")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be a ParameterProvenance.")
        if not isinstance(self.assumptions, tuple):
            raise TypeError("assumptions must be a tuple.")
        if not self.assumptions:
            raise ValueError("assumptions must identify the comparison conditions.")
        for value in self.assumptions:
            _identifier(value, "assumption")
        if len(set(self.assumptions)) != len(self.assumptions):
            raise ValueError("assumptions must have distinct identifiers.")


@dataclass(frozen=True, slots=True)
class FLiBeRegisteredDensityComparisonRow:
    """One registered source row and the computed state-correspondence flags."""

    source_record: FLiBeRegisteredDensityRecord
    correspondence: FLiBeDensityStateCorrespondence

    def __post_init__(self) -> None:
        if not isinstance(self.source_record, FLiBeRegisteredDensityRecord):
            raise TypeError("source_record must be a FLiBeRegisteredDensityRecord.")
        if not isinstance(self.correspondence, FLiBeDensityStateCorrespondence):
            raise TypeError("correspondence must be a FLiBeDensityStateCorrespondence.")
        if self.source_record.coordinates != self.correspondence.reference:
            raise ValueError("source row and correspondence reference must agree.")

    @property
    def record_id(self) -> str:
        return self.source_record.record_id

    @property
    def matched_axes(self) -> tuple[str, ...]:
        """Return names of physical axes satisfying the declared criteria."""
        c = self.correspondence
        flags = (
            ("composition", c.composition_match),
            ("temperature", c.temperature_match),
            ("pressure", c.pressure_match),
            ("physical_state", c.physical_state_match),
            ("normalization", c.normalization_match),
        )
        return tuple(name for name, matched in flags if matched)

    @property
    def unmatched_axes(self) -> tuple[str, ...]:
        """Retain all coordinate failures, including missing source axes."""
        c = self.correspondence
        flags = (
            ("composition", c.composition_match),
            ("temperature", c.temperature_match),
            ("pressure", c.pressure_match),
            ("physical_state", c.physical_state_match),
            ("normalization", c.normalization_match),
        )
        return tuple(name for name, matched in flags if not matched)

    @property
    def missing_source_axes(self) -> tuple[str, ...]:
        """Identify absent source coordinates without replacing them by zero."""
        reference = self.source_record.coordinates
        return tuple(
            name for name, missing in (
                ("pressure", reference.pressure_pa is None),
                ("physical_state", reference.physical_state_id is None),
            ) if missing
        )

    @property
    def density_residual_kg_m3(self) -> float | None:
        """Return calculated minus source density for a matched state only."""
        if not self.correspondence.coordinate_match:
            return None
        return self.correspondence.density_residual_kg_m3

    @property
    def temperature_difference_k(self) -> float:
        return self.correspondence.temperature_difference_k

    @property
    def pressure_difference_pa(self) -> float | None:
        return self.correspondence.pressure_difference_pa

    @property
    def bef2_fraction_difference(self) -> float:
        return (
            self.correspondence.model.density_trace.composition.bef2_fraction
            - self.source_record.coordinates.composition.bef2_fraction
        )


@dataclass(frozen=True, slots=True)
class FLiBeDensityResidualMetrics:
    """Unweighted numerical metrics for a nonempty matched-record selection."""

    count: int
    mean_signed_kg_m3: float
    mean_absolute_kg_m3: float
    root_mean_square_kg_m3: float
    maximum_absolute_kg_m3: float


@dataclass(frozen=True, slots=True)
class FLiBeRegisteredDensityComparison:
    """Ordered, single-dataset correspondence report for an MD density trace."""

    model: FLiBeTrajectoryStateCoordinates
    mapping: FLiBeDensityObservableMapping
    source_dataset_id: str
    source_file_sha256: str
    temperature_tolerance_k: float
    pressure_tolerance_pa: float
    rows: tuple[FLiBeRegisteredDensityComparisonRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.model, FLiBeTrajectoryStateCoordinates):
            raise TypeError("model must be a FLiBeTrajectoryStateCoordinates.")
        if not isinstance(self.mapping, FLiBeDensityObservableMapping):
            raise TypeError("mapping must be a FLiBeDensityObservableMapping.")
        _identifier(self.source_dataset_id, "source_dataset_id")
        if not isinstance(self.source_file_sha256, str) or len(self.source_file_sha256) != 64:
            raise ValueError("source_file_sha256 must be a SHA-256 hex digest.")
        if any(character not in "0123456789abcdef" for character in self.source_file_sha256):
            raise ValueError("source_file_sha256 must be a SHA-256 hex digest.")
        _tolerance(self.temperature_tolerance_k, "temperature_tolerance_k")
        _tolerance(self.pressure_tolerance_pa, "pressure_tolerance_pa")
        if not isinstance(self.rows, tuple) or not self.rows:
            raise ValueError("rows must be a nonempty tuple.")
        seen: set[str] = set()
        for row in self.rows:
            if not isinstance(row, FLiBeRegisteredDensityComparisonRow):
                raise TypeError("rows must contain FLiBeRegisteredDensityComparisonRow values.")
            record = row.source_record
            if record.record_id in seen:
                raise ValueError("source record identities must be unique.")
            seen.add(record.record_id)
            if record.dataset_id != self.source_dataset_id:
                raise ValueError("source dataset identities must agree.")
            if record.source_file_sha256 != self.source_file_sha256:
                raise ValueError("source file fingerprints must agree.")
            if row.correspondence.model != self.model:
                raise ValueError("comparison rows must refer to the selected model state.")

    @property
    def matched_count(self) -> int:
        return sum(row.density_residual_kg_m3 is not None for row in self.rows)

    @property
    def unmatched_count(self) -> int:
        return len(self.rows) - self.matched_count

    @property
    def residual_metrics(self) -> FLiBeDensityResidualMetrics | None:
        """Aggregate residuals only over complete physical-state matches."""
        residuals = tuple(
            residual
            for row in self.rows
            if (residual := row.density_residual_kg_m3) is not None
        )
        if not residuals:
            return None
        count = len(residuals)
        squares = fsum(value * value for value in residuals)
        return FLiBeDensityResidualMetrics(
            count=count,
            mean_signed_kg_m3=fsum(residuals) / count,
            mean_absolute_kg_m3=fsum(abs(value) for value in residuals) / count,
            root_mean_square_kg_m3=sqrt(squares / count),
            maximum_absolute_kg_m3=max(abs(value) for value in residuals),
        )


def compare_flibe_registered_density_records(
    model: FLiBeTrajectoryStateCoordinates,
    records: tuple[FLiBeRegisteredDensityRecord, ...],
    *,
    mapping: FLiBeDensityObservableMapping,
    temperature_tolerance_k: float,
    pressure_tolerance_pa: float,
) -> FLiBeRegisteredDensityComparison:
    """Compare one MD density trace with registered source rows.

    Every registered record is included in source order. Composition, mean
    kinetic temperature, observed pressure, physical-state identity, and the
    declared normalization mapping are evaluated separately. Residuals and
    summary metrics are available for complete state matches; unresolved or
    differing coordinates remain visible in each source-row record.
    """
    if not isinstance(model, FLiBeTrajectoryStateCoordinates):
        raise TypeError("model must be a FLiBeTrajectoryStateCoordinates.")
    if not isinstance(mapping, FLiBeDensityObservableMapping):
        raise TypeError("mapping must be a FLiBeDensityObservableMapping.")
    if not isinstance(records, tuple) or not records:
        raise ValueError("records must be a nonempty tuple.")
    t_tol = _tolerance(temperature_tolerance_k, "temperature_tolerance_k")
    p_tol = _tolerance(pressure_tolerance_pa, "pressure_tolerance_pa")
    if not all(isinstance(record, FLiBeRegisteredDensityRecord) for record in records):
        raise TypeError("records must contain FLiBeRegisteredDensityRecord values.")

    rows = tuple(
        FLiBeRegisteredDensityComparisonRow(
            source_record=record,
            correspondence=compare_flibe_density_state_coordinates(
                model,
                record.coordinates,
                temperature_tolerance_k=t_tol,
                pressure_tolerance_pa=p_tol,
                normalization_id=mapping.source_normalization_id,
            ),
        )
        for record in records
    )
    return FLiBeRegisteredDensityComparison(
        model=model,
        mapping=mapping,
        source_dataset_id=records[0].dataset_id,
        source_file_sha256=records[0].source_file_sha256,
        temperature_tolerance_k=t_tol,
        pressure_tolerance_pa=p_tol,
        rows=rows,
    )
