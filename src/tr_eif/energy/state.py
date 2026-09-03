"""Scalar conservative energy representations for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

AtomicEnergies: TypeAlias = tuple[float, ...]


def _validate_energy(
    value: float,
    *,
    field_name: str,
) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a real number.")

    if not isfinite(value):
        raise ValueError(f"{field_name} must be finite.")

    return float(value)


@dataclass(frozen=True, slots=True)
class EnergyState:
    """Immutable atomic contributions and total scalar energy."""

    atomic_energies: AtomicEnergies
    total_energy: float

    def __post_init__(self) -> None:
        if not isinstance(self.atomic_energies, tuple):
            raise TypeError("atomic_energies must be a tuple.")

        if len(self.atomic_energies) == 0:
            raise ValueError("atomic_energies must not be empty.")

        validated = tuple(
            _validate_energy(
                value,
                field_name=f"atomic_energies[{index}]",
            )
            for index, value in enumerate(self.atomic_energies)
        )

        total = _validate_energy(
            self.total_energy,
            field_name="total_energy",
        )

        object.__setattr__(
            self,
            "atomic_energies",
            validated,
        )
        object.__setattr__(
            self,
            "total_energy",
            total,
        )

    @classmethod
    def from_atomic_energies(
        cls,
        atomic_energies: AtomicEnergies,
    ) -> EnergyState:
        """Construct an energy state from deterministic atomic contributions."""

        if not isinstance(atomic_energies, tuple):
            raise TypeError("atomic_energies must be a tuple.")

        if len(atomic_energies) == 0:
            raise ValueError("atomic_energies must not be empty.")

        validated = tuple(
            _validate_energy(
                value,
                field_name=f"atomic_energies[{index}]",
            )
            for index, value in enumerate(atomic_energies)
        )

        return cls(
            atomic_energies=validated,
            total_energy=sum(validated),
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atomic energy contributions."""

        return len(self.atomic_energies)
