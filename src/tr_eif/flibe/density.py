"""Mass-density contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Callable, TypeAlias

from .thermodynamic_state import FLiBeThermodynamicState
from .units import (
    FLiBeUnit,
    ParameterProvenance,
    PhysicalParameter,
    density_parameter,
)


Density: TypeAlias = float
DensityEvaluator: TypeAlias = Callable[
    [FLiBeThermodynamicState],
    float,
]


def _validate_density(
    value: float,
) -> Density:
    """Validate one finite positive mass-density value."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "density must be a real non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            "density must be finite."
        )

    if normalized <= 0.0:
        raise ValueError(
            "density must be positive."
        )

    return normalized


@dataclass(frozen=True)
class FLiBeDensityModel:
    """Explicit mass-density model with provenance metadata."""

    evaluator: DensityEvaluator
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate density-model metadata."""

        if not callable(
            self.evaluator
        ):
            raise TypeError(
                "evaluator must be callable."
            )

        if not isinstance(
            self.provenance,
            ParameterProvenance,
        ):
            raise TypeError(
                "provenance must be a ParameterProvenance."
            )

        if self.source is not None and not isinstance(
            self.source,
            str,
        ):
            raise TypeError(
                "source must be a string or None."
            )

        if isinstance(
            self.source,
            str,
        ):
            if self.source == "":
                raise ValueError(
                    "source must not be empty."
                )

            if self.source != self.source.strip():
                raise ValueError(
                    "source must not contain leading "
                    "or trailing whitespace."
                )

        if (
            self.provenance
            is ParameterProvenance.PRIMARY_SOURCE
            and self.source is None
        ):
            raise ValueError(
                "PRIMARY_SOURCE provenance requires source."
            )

    def evaluate(
        self,
        state: FLiBeThermodynamicState,
    ) -> PhysicalParameter:
        """Evaluate density for one explicit thermodynamic state."""

        if not isinstance(
            state,
            FLiBeThermodynamicState,
        ):
            raise TypeError(
                "state must be an FLiBeThermodynamicState."
            )

        value = _validate_density(
            self.evaluator(
                state
            )
        )

        return density_parameter(
            value,
            self.provenance,
            source=self.source,
        )


@dataclass(frozen=True)
class ConstantFLiBeDensity:
    """Explicit constant-density model for controlled use."""

    density: Density
    provenance: ParameterProvenance
    source: str | None = None

    def __post_init__(self) -> None:
        """Validate constant density and provenance metadata."""

        normalized = _validate_density(
            self.density
        )

        parameter = density_parameter(
            normalized,
            self.provenance,
            source=self.source,
        )

        object.__setattr__(
            self,
            "density",
            parameter.value,
        )

    def evaluate(
        self,
        state: FLiBeThermodynamicState,
    ) -> PhysicalParameter:
        """Return the constant density for a validated state."""

        if not isinstance(
            state,
            FLiBeThermodynamicState,
        ):
            raise TypeError(
                "state must be an FLiBeThermodynamicState."
            )

        return density_parameter(
            self.density,
            self.provenance,
            source=self.source,
        )


def evaluate_density(
    model: FLiBeDensityModel | ConstantFLiBeDensity,
    state: FLiBeThermodynamicState,
) -> PhysicalParameter:
    """Evaluate one supported FLiBe density model."""

    if not isinstance(
        model,
        (
            FLiBeDensityModel,
            ConstantFLiBeDensity,
        ),
    ):
        raise TypeError(
            "model must be an FLiBeDensityModel "
            "or ConstantFLiBeDensity."
        )

    parameter = model.evaluate(
        state
    )

    if parameter.unit is not FLiBeUnit.KILOGRAM_PER_CUBIC_METER:
        raise ValueError(
            "density model must return kg/m^3."
        )

    return parameter
