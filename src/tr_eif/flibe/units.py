"""Units and provenance contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import TypeAlias


class FLiBeUnit(str, Enum):
    """Canonical units supported by the FLiBe parameter boundary."""

    KELVIN = "K"
    PASCAL = "Pa"
    ATOMIC_MASS_UNIT = "u"
    KILOGRAM_PER_CUBIC_METER = "kg/m^3"


class ParameterProvenance(str, Enum):
    """Canonical provenance classes for FLiBe physical parameters."""

    PRIMARY_SOURCE = "PRIMARY_SOURCE"
    DERIVED = "DERIVED"
    CALIBRATED = "CALIBRATED"
    AUTHOR_DEFINED = "AUTHOR_DEFINED"
    BENCHMARK = "BENCHMARK"
    TEST_FIXTURE = "TEST_FIXTURE"
    REQUIRES_SOURCE = "REQUIRES_SOURCE"
    REQUIRES_TEST = "REQUIRES_TEST"


ParameterValue: TypeAlias = float


def _validate_parameter_value(
    value: float,
) -> ParameterValue:
    """Validate one finite physical-parameter value."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "value must be a real non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            "value must be finite."
        )

    return normalized


def _validate_source(
    source: str | None,
    provenance: ParameterProvenance,
) -> str | None:
    """Validate provenance source metadata."""

    if source is not None and not isinstance(
        source,
        str,
    ):
        raise TypeError(
            "source must be a string or None."
        )

    if isinstance(
        source,
        str,
    ):
        if source == "":
            raise ValueError(
                "source must not be empty."
            )

        if source != source.strip():
            raise ValueError(
                "source must not contain leading "
                "or trailing whitespace."
            )

    if provenance is ParameterProvenance.PRIMARY_SOURCE:
        if source is None:
            raise ValueError(
                "PRIMARY_SOURCE provenance requires source."
            )

    return source


@dataclass(frozen=True)
class PhysicalParameter:
    """One explicit physical parameter with unit and provenance."""

    value: ParameterValue
    unit: FLiBeUnit
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate value, unit, provenance, and source metadata."""

        normalized_value = _validate_parameter_value(
            self.value
        )

        if not isinstance(
            self.unit,
            FLiBeUnit,
        ):
            raise TypeError(
                "unit must be an FLiBeUnit."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        normalized_source = _validate_source(
            self.source,
            self.provenance,
        )

        object.__setattr__(
            self,
            "value",
            normalized_value,
        )

        object.__setattr__(
            self,
            "source",
            normalized_source,
        )


def temperature_parameter(
    value: float,
    provenance: ParameterProvenance,
    *,
    source: str | None = None,
) -> PhysicalParameter:
    """Build one explicitly Kelvin-valued temperature parameter."""

    return PhysicalParameter(
        value=value,
        unit=FLiBeUnit.KELVIN,
        provenance=provenance,
        source=source,
    )


def pressure_parameter(
    value: float,
    provenance: ParameterProvenance,
    *,
    source: str | None = None,
) -> PhysicalParameter:
    """Build one explicitly Pascal-valued pressure parameter."""

    return PhysicalParameter(
        value=value,
        unit=FLiBeUnit.PASCAL,
        provenance=provenance,
        source=source,
    )


def atomic_mass_parameter(
    value: float,
    provenance: ParameterProvenance,
    *,
    source: str | None = None,
) -> PhysicalParameter:
    """Build one atomic-mass parameter expressed in unified atomic mass units."""

    return PhysicalParameter(
        value=value,
        unit=FLiBeUnit.ATOMIC_MASS_UNIT,
        provenance=provenance,
        source=source,
    )


def density_parameter(
    value: float,
    provenance: ParameterProvenance,
    *,
    source: str | None = None,
) -> PhysicalParameter:
    """Build one mass-density parameter expressed in kg/m^3."""

    return PhysicalParameter(
        value=value,
        unit=FLiBeUnit.KILOGRAM_PER_CUBIC_METER,
        provenance=provenance,
        source=source,
    )
