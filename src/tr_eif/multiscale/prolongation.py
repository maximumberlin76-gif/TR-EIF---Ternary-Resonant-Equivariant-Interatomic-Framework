"""Partition-based prolongation operators for TR-EIF multiscale models."""

from __future__ import annotations

from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .partition import MultiscalePartition


CoarseScalars: TypeAlias = tuple[float, ...]
FineScalars: TypeAlias = tuple[float, ...]
CoarseVectors: TypeAlias = tuple[Vector3, ...]
FineVectors: TypeAlias = tuple[Vector3, ...]


def _validate_coarse_scalars(
    values: CoarseScalars,
    partition: MultiscalePartition,
) -> tuple[float, ...]:
    """Validate and normalize one scalar value per coarse entity."""

    if not isinstance(values, tuple):
        raise TypeError(
            "values must be a tuple."
        )

    if len(values) == 0:
        raise ValueError(
            "values must not be empty."
        )

    if len(values) != partition.coarse_count:
        raise ValueError(
            "values must contain one scalar per coarse-scale entity."
        )

    normalized: list[float] = []

    for index, value in enumerate(values):
        if not isinstance(
            value,
            (int, float),
        ) or isinstance(value, bool):
            raise TypeError(
                f"values[{index}] must be a real number."
            )

        scalar = float(value)

        if not isfinite(scalar):
            raise ValueError(
                f"values[{index}] must be finite."
            )

        normalized.append(scalar)

    return tuple(normalized)


def _validate_coarse_vectors(
    vectors: CoarseVectors,
    partition: MultiscalePartition,
) -> tuple[Vector3, ...]:
    """Validate and normalize one Cartesian vector per coarse entity."""

    if not isinstance(vectors, tuple):
        raise TypeError(
            "vectors must be a tuple."
        )

    if len(vectors) == 0:
        raise ValueError(
            "vectors must not be empty."
        )

    if len(vectors) != partition.coarse_count:
        raise ValueError(
            "vectors must contain one vector per coarse-scale entity."
        )

    normalized: list[Vector3] = []

    for vector_index, vector in enumerate(vectors):
        if not isinstance(vector, tuple):
            raise TypeError(
                f"vectors[{vector_index}] must be a tuple."
            )

        if len(vector) != 3:
            raise ValueError(
                f"vectors[{vector_index}] must contain exactly "
                "three components."
            )

        components: list[float] = []

        for component_index, component in enumerate(vector):
            if not isinstance(
                component,
                (int, float),
            ) or isinstance(component, bool):
                raise TypeError(
                    "vectors"
                    f"[{vector_index}][{component_index}] "
                    "must be a real number."
                )

            value = float(component)

            if not isfinite(value):
                raise ValueError(
                    "vectors"
                    f"[{vector_index}][{component_index}] "
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


def prolong_scalar_broadcast(
    values: CoarseScalars,
    partition: MultiscalePartition,
) -> FineScalars:
    """Broadcast coarse scalar values to their fine-scale members."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized = _validate_coarse_scalars(
        values=values,
        partition=partition,
    )

    return tuple(
        normalized[
            partition.coarse_index_for(
                fine_index
            )
        ]
        for fine_index in range(
            partition.fine_count
        )
    )


def prolong_vector_broadcast(
    vectors: CoarseVectors,
    partition: MultiscalePartition,
) -> FineVectors:
    """Broadcast coarse Cartesian vectors to their fine-scale members."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized = _validate_coarse_vectors(
        vectors=vectors,
        partition=partition,
    )

    return tuple(
        normalized[
            partition.coarse_index_for(
                fine_index
            )
        ]
        for fine_index in range(
            partition.fine_count
        )
    )
