"""Typed atomic-configuration state for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

Vector3: TypeAlias = tuple[float, float, float]
Cell3x3: TypeAlias = tuple[Vector3, Vector3, Vector3]
PeriodicAxes: TypeAlias = tuple[bool, bool, bool]


def _validate_vector3(value: Vector3, *, field_name: str) -> None:
    if len(value) != 3:
        raise ValueError(f"{field_name} must contain exactly three components.")

    if not all(isfinite(component) for component in value):
        raise ValueError(f"{field_name} must contain only finite values.")


def _validate_cell(cell: Cell3x3) -> None:
    if len(cell) != 3:
        raise ValueError("cell must contain exactly three lattice vectors.")

    for index, vector in enumerate(cell):
        _validate_vector3(vector, field_name=f"cell[{index}]")


def _cell_determinant(cell: Cell3x3) -> float:
    a, b, c = cell

    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


@dataclass(frozen=True, slots=True)
class AtomicConfiguration:
    """Immutable atomic configuration in Cartesian coordinates."""

    species: tuple[str, ...]
    positions: tuple[Vector3, ...]
    cell: Cell3x3 | None = None
    periodic: PeriodicAxes = (False, False, False)

    def __post_init__(self) -> None:
        atom_count = len(self.species)

        if atom_count == 0:
            raise ValueError("AtomicConfiguration must contain at least one atom.")

        if len(self.positions) != atom_count:
            raise ValueError(
                "species and positions must contain the same number of atoms."
            )

        for index, symbol in enumerate(self.species):
            if not isinstance(symbol, str):
                raise TypeError(f"species[{index}] must be a string.")

            if not symbol.strip():
                raise ValueError(f"species[{index}] must not be empty.")

        for index, position in enumerate(self.positions):
            _validate_vector3(position, field_name=f"positions[{index}]")

        if len(self.periodic) != 3:
            raise ValueError("periodic must contain exactly three boolean flags.")

        if not all(isinstance(flag, bool) for flag in self.periodic):
            raise TypeError("periodic must contain only boolean flags.")

        if self.cell is None:
            if any(self.periodic):
                raise ValueError(
                    "A simulation cell is required when any periodic axis is enabled."
                )
            return

        _validate_cell(self.cell)

        if _cell_determinant(self.cell) == 0.0:
            raise ValueError("cell lattice vectors must define a nonzero volume.")

    @property
    def atom_count(self) -> int:
        """Return the number of atoms in the configuration."""

        return len(self.species)

    @property
    def is_periodic(self) -> bool:
        """Return whether at least one periodic axis is enabled."""

        return any(self.periodic)
