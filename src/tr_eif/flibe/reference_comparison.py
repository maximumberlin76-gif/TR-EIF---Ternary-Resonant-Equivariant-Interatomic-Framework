"""Experimental and first-principles comparison contract for TR-EIF FLiBe."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite, sqrt
from typing import TypeAlias

from .composition import FLiBeComposition
from .thermodynamic_state import FLiBeThermodynamicState
from .units import ParameterProvenance


class FLiBeEvidenceKind(str, Enum):
    """Evidence classes admitted by the FLiBe comparison boundary."""

    EXPERIMENTAL = "EXPERIMENTAL"
    FIRST_PRINCIPLES = "FIRST_PRINCIPLES"


ReferenceValues: TypeAlias = tuple[float, ...]
ReferenceAxis: TypeAlias = tuple[float, ...]


def _validate_identifier(
    value: str,
    *,
    field_name: str,
) -> str:
    """Validate and normalize one nonempty comparison identifier."""

    if not isinstance(value, str):
        raise TypeError(
            f"{field_name} must be a string."
        )

    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{field_name} must not be empty or whitespace."
        )

    return normalized


def _validate_values(
    values: tuple[float, ...],
    *,
    field_name: str,
) -> tuple[float, ...]:
    """Validate one immutable nonempty finite numeric vector."""

    if not isinstance(values, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(values) == 0:
        raise ValueError(
            f"{field_name} must not be empty."
        )

    normalized: list[float] = []

    for index, value in enumerate(values):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError(
                f"{field_name}[{index}] must be a real number."
            )

        scalar = float(value)

        if not isfinite(scalar):
            raise ValueError(
                f"{field_name}[{index}] must be finite."
            )

        normalized.append(scalar)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class FLiBeReferenceObservable:
    """One source-backed FLiBe observable admitted to comparison.

    ``values`` may represent one scalar or an ordered sampled observable such
    as a structure factor or pair-correlation curve. When ``axis`` is present,
    it must have exactly the same cardinality as ``values``.

    Composition, thermodynamic state, physical-state identifier, units,
    normalization, method, source, evidence kind, and provenance remain
    explicit. No interpolation, resampling, unit conversion, or state mapping
    is performed by this record.
    """

    observable_id: str
    composition: FLiBeComposition
    thermodynamic_state: FLiBeThermodynamicState
    physical_state_id: str
    evidence_kind: FLiBeEvidenceKind
    values: ReferenceValues
    value_unit: str
    normalization_id: str
    source_id: str
    method_id: str
    provenance: ParameterProvenance
    axis: ReferenceAxis | None = None
    axis_unit: str | None = None

    def __post_init__(self) -> None:
        observable_id = _validate_identifier(
            self.observable_id,
            field_name="observable_id",
        )

        if not isinstance(self.composition, FLiBeComposition):
            raise TypeError(
                "composition must be an FLiBeComposition instance."
            )

        if not isinstance(
            self.thermodynamic_state,
            FLiBeThermodynamicState,
        ):
            raise TypeError(
                "thermodynamic_state must be an "
                "FLiBeThermodynamicState instance."
            )

        physical_state_id = _validate_identifier(
            self.physical_state_id,
            field_name="physical_state_id",
        )

        if not isinstance(self.evidence_kind, FLiBeEvidenceKind):
            raise TypeError(
                "evidence_kind must be an FLiBeEvidenceKind."
            )

        values = _validate_values(
            self.values,
            field_name="values",
        )
        value_unit = _validate_identifier(
            self.value_unit,
            field_name="value_unit",
        )
        normalization_id = _validate_identifier(
            self.normalization_id,
            field_name="normalization_id",
        )
        source_id = _validate_identifier(
            self.source_id,
            field_name="source_id",
        )
        method_id = _validate_identifier(
            self.method_id,
            field_name="method_id",
        )

        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        axis = self.axis
        axis_unit = self.axis_unit

        if axis is None:
            if axis_unit is not None:
                raise ValueError(
                    "axis_unit must be None when axis is None."
                )
        else:
            axis = _validate_values(
                axis,
                field_name="axis",
            )

            if len(axis) != len(values):
                raise ValueError(
                    "axis and values must have the same length."
                )

            if axis_unit is None:
                raise ValueError(
                    "axis_unit is required when axis is present."
                )

            axis_unit = _validate_identifier(
                axis_unit,
                field_name="axis_unit",
            )

        object.__setattr__(
            self,
            "observable_id",
            observable_id,
        )
        object.__setattr__(
            self,
            "physical_state_id",
            physical_state_id,
        )
        object.__setattr__(
            self,
            "values",
            values,
        )
        object.__setattr__(
            self,
            "value_unit",
            value_unit,
        )
        object.__setattr__(
            self,
            "normalization_id",
            normalization_id,
        )
        object.__setattr__(
            self,
            "source_id",
            source_id,
        )
        object.__setattr__(
            self,
            "method_id",
            method_id,
        )
        object.__setattr__(
            self,
            "axis",
            axis,
        )
        object.__setattr__(
            self,
            "axis_unit",
            axis_unit,
        )

    @property
    def sample_count(self) -> int:
        """Return the number of scalar samples represented."""

        return len(self.values)


@dataclass(frozen=True, slots=True)
class FLiBeReferenceComparison:
    """Direct comparison of matched experimental and first-principles data.

    Compatibility is intentionally strict. The two records must describe the
    same observable, composition, thermodynamic state, physical state, units,
    normalization, sample coordinates, and sample count.

    The comparison reports numerical residuals only. It does not assign a
    pass/fail status, select a tolerance, treat first-principles data as truth,
    or convert a validation result into a balanced-ternary state.
    """

    experimental: FLiBeReferenceObservable
    first_principles: FLiBeReferenceObservable

    def __post_init__(self) -> None:
        if not isinstance(
            self.experimental,
            FLiBeReferenceObservable,
        ):
            raise TypeError(
                "experimental must be an FLiBeReferenceObservable instance."
            )

        if not isinstance(
            self.first_principles,
            FLiBeReferenceObservable,
        ):
            raise TypeError(
                "first_principles must be an "
                "FLiBeReferenceObservable instance."
            )

        if (
            self.experimental.evidence_kind
            is not FLiBeEvidenceKind.EXPERIMENTAL
        ):
            raise ValueError(
                "experimental record must have EXPERIMENTAL evidence kind."
            )

        if (
            self.first_principles.evidence_kind
            is not FLiBeEvidenceKind.FIRST_PRINCIPLES
        ):
            raise ValueError(
                "first_principles record must have "
                "FIRST_PRINCIPLES evidence kind."
            )

        comparable_fields = (
            "observable_id",
            "composition",
            "thermodynamic_state",
            "physical_state_id",
            "value_unit",
            "normalization_id",
            "axis",
            "axis_unit",
        )

        for field_name in comparable_fields:
            if (
                getattr(self.experimental, field_name)
                != getattr(self.first_principles, field_name)
            ):
                raise ValueError(
                    f"experimental and first-principles {field_name} "
                    "must match for direct comparison."
                )

        if (
            self.experimental.sample_count
            != self.first_principles.sample_count
        ):
            raise ValueError(
                "experimental and first-principles sample counts must match."
            )

    @property
    def sample_count(self) -> int:
        """Return the number of directly compared samples."""

        return self.experimental.sample_count

    @property
    def residuals(self) -> tuple[float, ...]:
        """Return first-principles minus experimental residuals."""

        return tuple(
            calculated - measured
            for measured, calculated in zip(
                self.experimental.values,
                self.first_principles.values,
                strict=True,
            )
        )

    @property
    def absolute_residuals(self) -> tuple[float, ...]:
        """Return absolute pointwise comparison residuals."""

        return tuple(
            abs(value)
            for value in self.residuals
        )

    @property
    def mean_absolute_error(self) -> float:
        """Return the arithmetic mean absolute residual."""

        return sum(self.absolute_residuals) / float(self.sample_count)

    @property
    def root_mean_square_error(self) -> float:
        """Return the root-mean-square residual."""

        return sqrt(
            sum(
                value * value
                for value in self.residuals
            )
            / float(self.sample_count)
        )

    @property
    def max_absolute_error(self) -> float:
        """Return the maximum absolute pointwise residual."""

        return max(self.absolute_residuals)


def compare_flibe_experimental_first_principles(
    experimental: FLiBeReferenceObservable,
    first_principles: FLiBeReferenceObservable,
) -> FLiBeReferenceComparison:
    """Construct one strict experimental/first-principles comparison.

    No interpolation, resampling, unit conversion, state conversion,
    tolerance selection, or empirical correction is performed.
    """

    return FLiBeReferenceComparison(
        experimental=experimental,
        first_principles=first_principles,
    )
