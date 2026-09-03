"""Geometric coarse-graining operators for TR-EIF multiscale models."""

from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .partition import MultiscalePartition
from .reduction import reduce_masses


FinePositions: TypeAlias = tuple[Vector3, ...]
CoarsePositions: TypeAlias = tuple[Vector3, ...]
FineMasses: TypeAlias = tuple[float, ...]


def _validate_positions(
    positions: FinePositions,
) -> tuple[Vector3, ...]:
    """Validate and normalize Cartesian fine-scale positions."""

    if not isinstance(positions, tuple):
        raise TypeError(
            "positions must be a tuple."
        )

    if len(positions) == 0:
        raise ValueError(
            "positions must not be empty."
        )

    normalized: list[Vector3] = []

    for index, position in enumerate(positions):
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

        normalized.append(
            (
                components[0],
                components[1],
                components[2],
            )
        )

    return tuple(normalized)


def mass_weighted_centroids(
    positions: FinePositions,
    masses: FineMasses,
    partition: MultiscalePartition,
) -> CoarsePositions:
    """Compute Cartesian mass-weighted centroids for coarse entities."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized_positions = _validate_positions(
        positions
    )

    if len(normalized_positions) != partition.fine_count:
        raise ValueError(
            "positions must contain one vector per fine-scale entity."
        )

    coarse_masses = reduce_masses(
        masses=masses,
        partition=partition,
    )

    if len(masses) != len(normalized_positions):
        raise ValueError(
            "masses and positions must contain the same number of fine-scale entities."
        )

    weighted_x = [0.0] * partition.coarse_count
    weighted_y = [0.0] * partition.coarse_count
    weighted_z = [0.0] * partition.coarse_count

    for fine_index, position in enumerate(
        normalized_positions
    ):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        mass = float(masses[fine_index])

        weighted_x[coarse_index] += (
            mass * position[0]
        )
        weighted_y[coarse_index] += (
            mass * position[1]
        )
        weighted_z[coarse_index] += (
            mass * position[2]
        )

    coarse_positions: list[Vector3] = []

    for coarse_index, coarse_mass in enumerate(
        coarse_masses
    ):
        coarse_positions.append(
            (
                weighted_x[coarse_index]
                / coarse_mass,
                weighted_y[coarse_index]
                / coarse_mass,
                weighted_z[coarse_index]
                / coarse_mass,
            )
        )

    return tuple(coarse_positions)
