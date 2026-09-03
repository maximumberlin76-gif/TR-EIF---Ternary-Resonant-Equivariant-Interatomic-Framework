"""Partition-aware vector reductions for TR-EIF multiscale models."""

from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .partition import MultiscalePartition


FineVectors: TypeAlias = tuple[Vector3, ...]
CoarseVectors: TypeAlias = tuple[Vector3, ...]


def _validate_vectors(
    vectors: FineVectors,
) -> tuple[Vector3, ...]:
    """Validate and normalize a fine-scale Cartesian vector field."""

    if not isinstance(vectors, tuple):
        raise TypeError(
            "vectors must be a tuple."
        )

    if len(vectors) == 0:
        raise ValueError(
            "vectors must not be empty."
        )

    normalized: list[Vector3] = []

    for index, vector in enumerate(vectors):
        if not isinstance(vector, tuple):
            raise TypeError(
                f"vectors[{index}] must be a tuple."
            )

        if len(vector) != 3:
            raise ValueError(
                f"vectors[{index}] must contain exactly three components."
            )

        components: list[float] = []

        for component_index, component in enumerate(vector):
            if not isinstance(
                component,
                (int, float),
            ) or isinstance(component, bool):
                raise TypeError(
                    "vectors"
                    f"[{index}][{component_index}] "
                    "must be a real number."
                )

            value = float(component)

            if not isfinite(value):
                raise ValueError(
                    "vectors"
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


def reduce_vector_sum(
    vectors: FineVectors,
    partition: MultiscalePartition,
) -> CoarseVectors:
    """Reduce fine-scale Cartesian vectors by partition-local summation."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized = _validate_vectors(
        vectors
    )

    if len(normalized) != partition.fine_count:
        raise ValueError(
            "vectors must contain one vector per fine-scale entity."
        )

    coarse_x = [0.0] * partition.coarse_count
    coarse_y = [0.0] * partition.coarse_count
    coarse_z = [0.0] * partition.coarse_count

    for fine_index, vector in enumerate(normalized):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        coarse_x[coarse_index] += vector[0]
        coarse_y[coarse_index] += vector[1]
        coarse_z[coarse_index] += vector[2]

    return tuple(
        (
            coarse_x[coarse_index],
            coarse_y[coarse_index],
            coarse_z[coarse_index],
        )
        for coarse_index in range(
            partition.coarse_count
        )
    )
