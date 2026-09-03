"""Force-to-acceleration dynamics for TR-EIF molecular dynamics."""

from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3
from tr_eif.energy import ForceState
from tr_eif.md.state import AtomicMasses


AtomicAccelerations: TypeAlias = tuple[Vector3, ...]


def acceleration_from_force(
    force: Vector3,
    mass: float,
) -> Vector3:
    """Convert one Cartesian force vector to acceleration."""

    return (
        force[0] / mass,
        force[1] / mass,
        force[2] / mass,
    )


def accelerations_from_forces(
    forces: ForceState,
    masses: AtomicMasses,
) -> AtomicAccelerations:
    """Convert atomwise Cartesian forces to accelerations."""

    if not isinstance(forces, ForceState):
        raise TypeError(
            "forces must be a ForceState instance."
        )

    if not isinstance(masses, tuple):
        raise TypeError(
            "masses must be a tuple."
        )

    if len(masses) != forces.atom_count:
        raise ValueError(
            "masses must contain one value per force vector."
        )

    validated_masses: list[float] = []

    for index, mass in enumerate(masses):
        if not isinstance(mass, (int, float)) or isinstance(
            mass,
            bool,
        ):
            raise TypeError(
                f"masses[{index}] must be a real number."
            )

        normalized = float(mass)

        if not isfinite(normalized):
            raise ValueError(
                f"masses[{index}] must be finite."
            )

        if normalized <= 0.0:
            raise ValueError(
                f"masses[{index}] must be greater than zero."
            )

        validated_masses.append(normalized)

    return tuple(
        acceleration_from_force(
            force,
            validated_masses[index],
        )
        for index, force in enumerate(forces.forces)
    )
