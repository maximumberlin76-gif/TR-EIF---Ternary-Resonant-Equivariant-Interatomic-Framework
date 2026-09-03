"""Resonance-coordinate spaces and finite windows for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

ResonanceCoordinate: TypeAlias = tuple[float, ...]


def _validate_coordinate(
    coordinate: ResonanceCoordinate,
    *,
    field_name: str,
) -> None:
    if len(coordinate) == 0:
        raise ValueError(f"{field_name} must not be empty.")

    if not all(isfinite(component) for component in coordinate):
        raise ValueError(f"{field_name} must contain only finite values.")


@dataclass(frozen=True, slots=True)
class ResonanceSpace:
    """Finite-dimensional resonance-coordinate space."""

    dimension: int

    def __post_init__(self) -> None:
        if not isinstance(self.dimension, int) or isinstance(
            self.dimension,
            bool,
        ):
            raise TypeError("dimension must be an integer.")

        if self.dimension <= 0:
            raise ValueError("dimension must be positive.")

    def validate_coordinate(
        self,
        coordinate: ResonanceCoordinate,
    ) -> None:
        """Validate one coordinate as an element of this resonance space."""

        _validate_coordinate(coordinate, field_name="coordinate")

        if len(coordinate) != self.dimension:
            raise ValueError(
                "coordinate dimension does not match the resonance space."
            )


@dataclass(frozen=True, slots=True)
class ResonanceWindow:
    """Closed axis-aligned finite window in a resonance-coordinate space."""

    space: ResonanceSpace
    lower: ResonanceCoordinate
    upper: ResonanceCoordinate

    def __post_init__(self) -> None:
        if not isinstance(self.space, ResonanceSpace):
            raise TypeError("space must be a ResonanceSpace instance.")

        self.space.validate_coordinate(self.lower)
        self.space.validate_coordinate(self.upper)

        for axis, (lower, upper) in enumerate(
            zip(self.lower, self.upper, strict=True)
        ):
            if lower >= upper:
                raise ValueError(
                    f"lower[{axis}] must be strictly less than upper[{axis}]."
                )

    @property
    def dimension(self) -> int:
        """Return the dimension of the resonance window."""

        return self.space.dimension

    def contains(
        self,
        coordinate: ResonanceCoordinate,
    ) -> bool:
        """Return whether a coordinate belongs to the closed window."""

        self.space.validate_coordinate(coordinate)

        return all(
            lower <= component <= upper
            for component, lower, upper in zip(
                coordinate,
                self.lower,
                self.upper,
                strict=True,
            )
        )

    def is_boundary(
        self,
        coordinate: ResonanceCoordinate,
    ) -> bool:
        """Return whether a coordinate lies on the exact window boundary."""

        if not self.contains(coordinate):
            return False

        return any(
            component == lower or component == upper
            for component, lower, upper in zip(
                coordinate,
                self.lower,
                self.upper,
                strict=True,
            )
        )

    def is_interior(
        self,
        coordinate: ResonanceCoordinate,
    ) -> bool:
        """Return whether a coordinate lies in the window interior."""

        self.space.validate_coordinate(coordinate)

        return all(
            lower < component < upper
            for component, lower, upper in zip(
                coordinate,
                self.lower,
                self.upper,
                strict=True,
            )
        )
