"""Force representations for conservative TR-EIF energy models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

AtomicForces: TypeAlias = tuple[Vector3, ...]


def _validate_force_vector(
    vector: Vector3,
    *,
    field_name: str,
) -> Vector3:
    if not isinstance(vector, tuple):
        raise TypeError(
            f"{field_name} must be a tuple."
        )

    if len(vector) != 3:
        raise ValueError(
            f"{field_name} must contain exactly three components."
        )

    validated: list[float] = []

    for component_index, component in enumerate(vector):
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


@dataclass(frozen=True, slots=True)
class ForceState:
    """Immutable Cartesian force vectors for one atomic configuration."""

    forces: AtomicForces

    def __post_init__(self) -> None:
        if not isinstance(self.forces, tuple):
            raise TypeError("forces must be a tuple.")

        if len(self.forces) == 0:
            raise ValueError("forces must not be empty.")

        validated = tuple(
            _validate_force_vector(
                force,
                field_name=f"forces[{index}]",
            )
            for index, force in enumerate(self.forces)
        )

        object.__setattr__(
            self,
            "forces",
            validated,
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atomic force vectors."""

        return len(self.forces)
