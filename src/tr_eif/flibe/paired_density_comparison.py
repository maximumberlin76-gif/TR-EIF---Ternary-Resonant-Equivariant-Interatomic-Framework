"""Paired FLiBe MD density comparisons on registered reference states."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, hypot, isfinite, sqrt

from .registered_density_cross_model import (
    FLiBeRegisteredDensityComparison,
    FLiBeRegisteredDensityComparisonRow,
)
from .trajectory_state_correspondence import FLiBePressureRole
from .trajectory_pressure import FLiBeVelocityFrame


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _tolerance(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative.")
    return number


@dataclass(frozen=True, slots=True)
class FLiBePairedDensityRow:
    """One shared reference record with two independently computed model states."""

    first: FLiBeRegisteredDensityComparisonRow
    second: FLiBeRegisteredDensityComparisonRow
    first_velocity_frame: FLiBeVelocityFrame
    second_velocity_frame: FLiBeVelocityFrame
    model_temperature_tolerance_k: float
    model_pressure_tolerance_pa: float

    def __post_init__(self) -> None:
        if not isinstance(self.first, FLiBeRegisteredDensityComparisonRow):
            raise TypeError("first must be a FLiBeRegisteredDensityComparisonRow.")
        if not isinstance(self.second, FLiBeRegisteredDensityComparisonRow):
            raise TypeError("second must be a FLiBeRegisteredDensityComparisonRow.")
        if self.first.source_record != self.second.source_record:
            raise ValueError("paired rows must share the exact reference record.")
        if not isinstance(self.first_velocity_frame, FLiBeVelocityFrame) or not isinstance(
            self.second_velocity_frame, FLiBeVelocityFrame
        ):
            raise TypeError("velocity frames must be FLiBeVelocityFrame values.")
        _tolerance(self.model_temperature_tolerance_k, "model_temperature_tolerance_k")
        _tolerance(self.model_pressure_tolerance_pa, "model_pressure_tolerance_pa")

    @property
    def record_id(self) -> str:
        return self.first.record_id

    @property
    def model_temperature_difference_k(self) -> float:
        """Second model's mean kinetic temperature minus the first model's."""
        return (
            self.second.correspondence.model.mean_kinetic_temperature_k
            - self.first.correspondence.model.mean_kinetic_temperature_k
        )

    @property
    def model_pressure_difference_pa(self) -> float | None:
        """Second observed pressure minus first observed pressure, when defined."""
        first = self.first.correspondence.model.pressure
        second = self.second.correspondence.model.pressure
        if first is None or second is None:
            return None
        if (
            first.role is not FLiBePressureRole.OBSERVED
            or second.role is not FLiBePressureRole.OBSERVED
        ):
            return None
        return second.pressure_pa - first.pressure_pa

    @property
    def model_unmatched_axes(self) -> tuple[str, ...]:
        """State-coordinate differences between the two MD model realizations."""
        first = self.first.correspondence.model
        second = self.second.correspondence.model
        flags = (
            ("composition", first.density_trace.composition == second.density_trace.composition),
            (
                "temperature",
                abs(self.model_temperature_difference_k) <= self.model_temperature_tolerance_k,
            ),
            (
                "pressure",
                self.model_pressure_difference_pa is not None
                and abs(self.model_pressure_difference_pa) <= self.model_pressure_tolerance_pa,
            ),
            ("physical_state", first.physical_state_id == second.physical_state_id),
            ("velocity_frame", self.first_velocity_frame is self.second_velocity_frame),
        )
        return tuple(name for name, matched in flags if not matched)

    @property
    def model_state_match(self) -> bool:
        """Return state correspondence between the two model realizations."""
        return not self.model_unmatched_axes

    @property
    def model_density_difference_kg_m3(self) -> float | None:
        """Second minus first mean density, independent of source correspondence."""
        if not self.model_state_match:
            return None
        return (
            self.second.correspondence.model.density_trace.mean_density_kg_m3
            - self.first.correspondence.model.density_trace.mean_density_kg_m3
        )

    @property
    def paired_state_match(self) -> bool:
        """True when both model states also match the common source record."""
        return (
            self.model_state_match
            and self.first.correspondence.coordinate_match
            and self.second.correspondence.coordinate_match
        )

    @property
    def first_residual_kg_m3(self) -> float | None:
        """First model minus source density on the common matched subset."""
        if not self.paired_state_match:
            return None
        return self.first.density_residual_kg_m3

    @property
    def second_residual_kg_m3(self) -> float | None:
        """Second model minus source density on the common matched subset."""
        if not self.paired_state_match:
            return None
        return self.second.density_residual_kg_m3

    @property
    def second_minus_first_density_kg_m3(self) -> float | None:
        """Signed prediction difference on the identical reference row."""
        first = self.first_residual_kg_m3
        second = self.second_residual_kg_m3
        if first is None or second is None:
            return None
        return second - first

    @property
    def second_minus_first_absolute_error_kg_m3(self) -> float | None:
        """Difference of absolute errors, second model minus first model."""
        first = self.first_residual_kg_m3
        second = self.second_residual_kg_m3
        if first is None or second is None:
            return None
        return abs(second) - abs(first)


@dataclass(frozen=True, slots=True)
class FLiBePairedDensityMetrics:
    """Unweighted errors on the common pairwise-matched source-record subset."""

    count: int
    first_bias_kg_m3: float
    second_bias_kg_m3: float
    first_mae_kg_m3: float
    second_mae_kg_m3: float
    first_rmse_kg_m3: float
    second_rmse_kg_m3: float
    second_minus_first_mae_kg_m3: float
    second_minus_first_rmse_kg_m3: float
    mean_model_density_difference_kg_m3: float


@dataclass(frozen=True, slots=True)
class FLiBePairedDensityComparison:
    """Two distinct model predictions evaluated against the same source rows."""

    comparison_id: str
    first: FLiBeRegisteredDensityComparison
    second: FLiBeRegisteredDensityComparison
    first_velocity_frame: FLiBeVelocityFrame
    second_velocity_frame: FLiBeVelocityFrame
    model_temperature_tolerance_k: float
    model_pressure_tolerance_pa: float
    rows: tuple[FLiBePairedDensityRow, ...]

    def __post_init__(self) -> None:
        _identifier(self.comparison_id, "comparison_id")
        if not isinstance(self.first, FLiBeRegisteredDensityComparison) or not isinstance(
            self.second, FLiBeRegisteredDensityComparison
        ):
            raise TypeError("first and second must be FLiBeRegisteredDensityComparison values.")
        a_id = self.first.model.density_trace.model_id
        b_id = self.second.model.density_trace.model_id
        if a_id == b_id:
            raise ValueError("paired comparison requires distinct model identifiers.")
        if self.first.source_dataset_id != self.second.source_dataset_id:
            raise ValueError("source dataset identities must agree.")
        if self.first.source_file_sha256 != self.second.source_file_sha256:
            raise ValueError("source file fingerprints must agree.")
        if self.first.mapping != self.second.mapping:
            raise ValueError("observable mappings must agree.")
        if (
            self.first.temperature_tolerance_k != self.second.temperature_tolerance_k
            or self.first.pressure_tolerance_pa != self.second.pressure_tolerance_pa
        ):
            raise ValueError("reference correspondence tolerances must agree.")
        if not isinstance(self.first_velocity_frame, FLiBeVelocityFrame) or not isinstance(
            self.second_velocity_frame, FLiBeVelocityFrame
        ):
            raise TypeError("velocity frames must be FLiBeVelocityFrame values.")
        _tolerance(self.model_temperature_tolerance_k, "model_temperature_tolerance_k")
        _tolerance(self.model_pressure_tolerance_pa, "model_pressure_tolerance_pa")
        if not isinstance(self.rows, tuple) or not self.rows:
            raise ValueError("rows must be a nonempty tuple.")
        if len(self.rows) != len(self.first.rows) or len(self.rows) != len(self.second.rows):
            raise ValueError("paired rows must cover both complete source selections.")
        for row, first_row, second_row in zip(
            self.rows, self.first.rows, self.second.rows, strict=True
        ):
            if not isinstance(row, FLiBePairedDensityRow):
                raise TypeError("rows must contain FLiBePairedDensityRow values.")
            if row.first != first_row or row.second != second_row:
                raise ValueError("paired rows must preserve source record order.")
            if (
                row.first_velocity_frame is not self.first_velocity_frame
                or row.second_velocity_frame is not self.second_velocity_frame
                or row.model_temperature_tolerance_k != self.model_temperature_tolerance_k
                or row.model_pressure_tolerance_pa != self.model_pressure_tolerance_pa
            ):
                raise ValueError("paired row criteria must match report criteria.")

    @property
    def model_state_match(self) -> bool:
        """Return state correspondence between the two model realizations."""
        return self.rows[0].model_state_match

    @property
    def model_density_difference_kg_m3(self) -> float | None:
        """One model-to-model mean-density difference, counted once per pair."""
        return self.rows[0].model_density_difference_kg_m3

    @property
    def paired_count(self) -> int:
        """Number of source rows satisfying both reference and pair criteria."""
        return sum(row.paired_state_match for row in self.rows)

    @property
    def excluded_count(self) -> int:
        return len(self.rows) - self.paired_count

    @property
    def paired_record_ids(self) -> tuple[str, ...]:
        return tuple(row.record_id for row in self.rows if row.paired_state_match)

    @property
    def metrics(self) -> FLiBePairedDensityMetrics | None:
        """Evaluate both models on one identical paired reference subset."""
        paired = tuple(row for row in self.rows if row.paired_state_match)
        if not paired:
            return None
        a = tuple(row.first_residual_kg_m3 for row in paired)
        b = tuple(row.second_residual_kg_m3 for row in paired)
        if any(value is None for value in (*a, *b)):
            raise ValueError("paired residuals must be present for matched states.")
        ra = tuple(float(value) for value in a if value is not None)
        rb = tuple(float(value) for value in b if value is not None)
        n = len(paired)
        mae_a = fsum(abs(value) for value in ra) / n
        mae_b = fsum(abs(value) for value in rb) / n
        rmse_a = hypot(*ra) / sqrt(n)
        rmse_b = hypot(*rb) / sqrt(n)
        return FLiBePairedDensityMetrics(
            count=n,
            first_bias_kg_m3=fsum(ra) / n,
            second_bias_kg_m3=fsum(rb) / n,
            first_mae_kg_m3=mae_a,
            second_mae_kg_m3=mae_b,
            first_rmse_kg_m3=rmse_a,
            second_rmse_kg_m3=rmse_b,
            second_minus_first_mae_kg_m3=mae_b - mae_a,
            second_minus_first_rmse_kg_m3=rmse_b - rmse_a,
            mean_model_density_difference_kg_m3=(
                fsum(y - x for x, y in zip(ra, rb, strict=True)) / n
            ),
        )


def compare_flibe_paired_density_models(
    first: FLiBeRegisteredDensityComparison,
    second: FLiBeRegisteredDensityComparison,
    *,
    comparison_id: str,
    first_velocity_frame: FLiBeVelocityFrame,
    second_velocity_frame: FLiBeVelocityFrame,
    model_temperature_tolerance_k: float,
    model_pressure_tolerance_pa: float,
) -> FLiBePairedDensityComparison:
    """Compare two model density traces against one ordered registered source set.

    Both single-model reports carry their independent source correspondences.
    Their source identities, observable mappings and source tolerances must
    agree. Additional model-to-model temperature and pressure criteria are
    supplied before comparison; velocity-frame declarations are retained.
    """
    if not isinstance(first, FLiBeRegisteredDensityComparison) or not isinstance(
        second, FLiBeRegisteredDensityComparison
    ):
        raise TypeError("first and second must be FLiBeRegisteredDensityComparison values.")
    t_tol = _tolerance(model_temperature_tolerance_k, "model_temperature_tolerance_k")
    p_tol = _tolerance(model_pressure_tolerance_pa, "model_pressure_tolerance_pa")
    if len(first.rows) != len(second.rows):
        raise ValueError("source record selections must have equal lengths.")
    if any(
        a.source_record != b.source_record
        for a, b in zip(first.rows, second.rows, strict=True)
    ):
        raise ValueError("paired reports must have identical ordered source records.")
    rows = tuple(
        FLiBePairedDensityRow(
            first=a,
            second=b,
            first_velocity_frame=first_velocity_frame,
            second_velocity_frame=second_velocity_frame,
            model_temperature_tolerance_k=t_tol,
            model_pressure_tolerance_pa=p_tol,
        )
        for a, b in zip(first.rows, second.rows, strict=True)
    )
    return FLiBePairedDensityComparison(
        comparison_id=comparison_id,
        first=first,
        second=second,
        first_velocity_frame=first_velocity_frame,
        second_velocity_frame=second_velocity_frame,
        model_temperature_tolerance_k=t_tol,
        model_pressure_tolerance_pa=p_tol,
        rows=rows,
    )
