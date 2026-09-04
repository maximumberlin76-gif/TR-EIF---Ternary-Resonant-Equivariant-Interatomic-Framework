"""Thermodynamic-state contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias


Temperature: TypeAlias = float
Pressure: TypeAlias = float


def _validate_temperature(
    value: float,
) -> Temperature:
    """Validate one absolute-temperature parameter."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "temperature must be a real non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            "temperature must be finite."
        )

    if normalized <= 0.0:
        raise ValueError(
            "temperature must be positive."
        )

    return normalized


def _validate_pressure(
    value: float,
) -> Pressure:
    """Validate one finite pressure parameter."""

    if isinstance(
        value,
        bool,
    ) or not isinstance(
        value,
        (int, float),
    ):
        raise TypeError(
            "pressure must be a real non-Boolean number."
        )

    normalized = float(
        value
    )

    if not isfinite(
        normalized
    ):
        raise ValueError(
            "pressure must be finite."
        )

    if normalized < 0.0:
        raise ValueError(
            "pressure must be nonnegative."
        )

    return normalized


@dataclass(frozen=True)
class FLiBeThermodynamicState:
    """Explicit thermodynamic state for the FLiBe domain."""

    temperature: Temperature
    pressure: Pressure

    def __post_init__(self) -> None:
        """Validate and normalize thermodynamic-state parameters."""

        object.__setattr__(
            self,
            "temperature",
            _validate_temperature(
                self.temperature
            ),
        )

        object.__setattr__(
            self,
            "pressure",
            _validate_pressure(
                self.pressure
            ),
        )

    def with_temperature(
        self,
        temperature: float,
    ) -> FLiBeThermodynamicState:
        """Return a state with replaced temperature and retained pressure."""

        return FLiBeThermodynamicState(
            temperature=temperature,
            pressure=self.pressure,
        )

    def with_pressure(
        self,
        pressure: float,
    ) -> FLiBeThermodynamicState:
        """Return a state with replaced pressure and retained temperature."""

        return FLiBeThermodynamicState(
            temperature=self.temperature,
            pressure=pressure,
        )
