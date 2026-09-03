"""Molecular-dynamics state representation for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import AtomicConfiguration, Vector3


AtomicVelocities: TypeAlias = tuple[Vector3, ...]
AtomicMasses: TypeAlias = tuple[float, ...]


def _validate_velocity(
    velocity: Vector3,
    *,
    field_name: str,
) -> Vector3:
    """Validate and normalize one Cartesian velocity vector."""

    if not isinstance(velocity, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(velocity) != 3:
        raise ValueError(
            f"{field_name} must contain exactly three components."
        )

    validated: list[float] = []

    for component_index, component in enumerate(velocity):
        if not isinstance(component, (int, float)) or isinstance(
            component,
            bool,
        ):
            raise TypeError(
                f"{field_name}[{component_index}] "
                "must be a real number."
            )

        if not isfinite(component):
            raise ValueError(
                f"{field_name}[{component_index}] must be finite."
            )

        validated.append(float(component))

    return (
        validated[0],
        validated[1],
        validated[2],
    )


def _validate_mass(
    mass: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one positive atomic mass."""

    if not isinstance(mass, (int, float)) or isinstance(
        mass,
        bool,
    ):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(mass):
        raise ValueError(
            f"{field_name} must be finite."
        )

    normalized = float(mass)

    if normalized <= 0.0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class MolecularDynamicsState:
    """Immutable molecular-dynamics state for one atomic configuration."""

    configuration: AtomicConfiguration
    velocities: AtomicVelocities
    masses: AtomicMasses
    step: int = 0
    time: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(
            self.configuration,
            AtomicConfiguration,
        ):
            raise TypeError(
                "configuration must be an AtomicConfiguration instance."
            )

        if not isinstance(self.velocities, tuple):
            raise TypeError(
                "velocities must be a tuple."
            )

        if len(self.velocities) != self.configuration.atom_count:
            raise ValueError(
                "velocities must contain one vector per atom."
            )

        validated_velocities = tuple(
            _validate_velocity(
                velocity,
                field_name=f"velocities[{index}]",
            )
            for index, velocity in enumerate(self.velocities)
        )

        if not isinstance(self.masses, tuple):
            raise TypeError(
                "masses must be a tuple."
            )

        if len(self.masses) != self.configuration.atom_count:
            raise ValueError(
                "masses must contain one value per atom."
            )

        validated_masses = tuple(
            _validate_mass(
                mass,
                field_name=f"masses[{index}]",
            )
            for index, mass in enumerate(self.masses)
        )

        if not isinstance(self.step, int) or isinstance(
            self.step,
            bool,
        ):
            raise TypeError(
                "step must be an integer."
            )

        if self.step < 0:
            raise ValueError(
                "step must be nonnegative."
            )

        if not isinstance(self.time, (int, float)) or isinstance(
            self.time,
            bool,
        ):
            raise TypeError(
                "time must be a real number."
            )

        if not isfinite(self.time):
            raise ValueError(
                "time must be finite."
            )

        if self.time < 0.0:
            raise ValueError(
                "time must be nonnegative."
            )

        object.__setattr__(
            self,
            "velocities",
            validated_velocities,
        )

        object.__setattr__(
            self,
            "masses",
            validated_masses,
        )

        object.__setattr__(
            self,
            "time",
            float(self.time),
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atoms in the molecular-dynamics state."""

        return self.configuration.atom_count
