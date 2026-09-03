"""Coarse-scale state representation for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .geometry import mass_weighted_centroids
from .partition import MultiscalePartition
from .reduction import reduce_masses


CoarsePositions: TypeAlias = tuple[Vector3, ...]
CoarseMasses: TypeAlias = tuple[float, ...]


@dataclass(frozen=True)
class CoarseScaleState:
    """Explicit coarse-scale state associated with a fine-to-coarse partition."""

    partition: MultiscalePartition
    positions: CoarsePositions
    masses: CoarseMasses

    def __post_init__(self) -> None:
        """Validate and normalize the coarse-scale state."""

        if not isinstance(
            self.partition,
            MultiscalePartition,
        ):
            raise TypeError(
                "partition must be a MultiscalePartition instance."
            )

        if not isinstance(self.positions, tuple):
            raise TypeError(
                "positions must be a tuple."
            )

        if not isinstance(self.masses, tuple):
            raise TypeError(
                "masses must be a tuple."
            )

        if len(self.positions) != self.partition.coarse_count:
            raise ValueError(
                "positions must contain one vector per coarse-scale entity."
            )

        if len(self.masses) != self.partition.coarse_count:
            raise ValueError(
                "masses must contain one scalar per coarse-scale entity."
            )

        normalized_positions: list[Vector3] = []

        for index, position in enumerate(self.positions):
            if not isinstance(position, tuple):
                raise TypeError(
                    f"positions[{index}] must be a tuple."
                )

            if len(position) != 3:
                raise ValueError(
                    f"positions[{index}] must contain exactly three components."
                )

            components: list[float] = []

            for component_index, component in enumerate(position):
                if not isinstance(
                    component,
                    (int, float),
                ) or isinstance(component, bool):
                    raise TypeError(
                        "positions"
                        f"[{index}][{component_index}] "
                        "must be a real number."
                    )

                value = float(component)

                if not isfinite(value):
                    raise ValueError(
                        "positions"
                        f"[{index}][{component_index}] "
                        "must be finite."
                    )

                components.append(value)

            normalized_positions.append(
                (
                    components[0],
                    components[1],
                    components[2],
                )
            )

        normalized_masses: list[float] = []

        for index, mass in enumerate(self.masses):
            if not isinstance(
                mass,
                (int, float),
            ) or isinstance(mass, bool):
                raise TypeError(
                    f"masses[{index}] must be a real number."
                )

            value = float(mass)

            if not isfinite(value):
                raise ValueError(
                    f"masses[{index}] must be finite."
                )

            if value <= 0.0:
                raise ValueError(
                    f"masses[{index}] must be greater than zero."
                )

            normalized_masses.append(value)

        object.__setattr__(
            self,
            "positions",
            tuple(normalized_positions),
        )
        object.__setattr__(
            self,
            "masses",
            tuple(normalized_masses),
        )

    @property
    def fine_count(self) -> int:
        """Return the number of fine-scale entities represented."""

        return self.partition.fine_count

    @property
    def coarse_count(self) -> int:
        """Return the number of coarse-scale entities."""

        return self.partition.coarse_count

    @property
    def total_mass(self) -> float:
        """Return the total mass represented at the coarse scale."""

        return sum(self.masses)


def build_coarse_scale_state(
    positions: tuple[Vector3, ...],
    masses: tuple[float, ...],
    partition: MultiscalePartition,
) -> CoarseScaleState:
    """Construct a coarse state from fine Cartesian positions and masses."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    coarse_masses = reduce_masses(
        masses=masses,
        partition=partition,
    )

    coarse_positions = mass_weighted_centroids(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    return CoarseScaleState(
        partition=partition,
        positions=coarse_positions,
        masses=coarse_masses,
    )
