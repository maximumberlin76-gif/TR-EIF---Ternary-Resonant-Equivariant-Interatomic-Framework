"""Mass-weighted vector averaging for TR-EIF multiscale models."""

from __future__ import annotations

from typing import TypeAlias

from tr_eif.configuration import Vector3

from .partition import MultiscalePartition
from .reduction import reduce_masses
from .vector_reduction import _validate_vectors


FineVectors: TypeAlias = tuple[Vector3, ...]
FineMasses: TypeAlias = tuple[float, ...]
CoarseVectors: TypeAlias = tuple[Vector3, ...]


def mass_weighted_vector_average(
    vectors: FineVectors,
    masses: FineMasses,
    partition: MultiscalePartition,
) -> CoarseVectors:
    """Compute partition-local mass-weighted averages of Cartesian vectors."""

    if not isinstance(
        partition,
        MultiscalePartition,
    ):
        raise TypeError(
            "partition must be a MultiscalePartition instance."
        )

    normalized_vectors = _validate_vectors(
        vectors
    )

    if len(normalized_vectors) != partition.fine_count:
        raise ValueError(
            "vectors must contain one vector per fine-scale entity."
        )

    coarse_masses = reduce_masses(
        masses=masses,
        partition=partition,
    )

    if len(masses) != len(normalized_vectors):
        raise ValueError(
            "masses and vectors must contain the same number "
            "of fine-scale entities."
        )

    weighted_x = [0.0] * partition.coarse_count
    weighted_y = [0.0] * partition.coarse_count
    weighted_z = [0.0] * partition.coarse_count

    for fine_index, vector in enumerate(
        normalized_vectors
    ):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        mass = float(masses[fine_index])

        weighted_x[coarse_index] += (
            mass * vector[0]
        )
        weighted_y[coarse_index] += (
            mass * vector[1]
        )
        weighted_z[coarse_index] += (
            mass * vector[2]
        )

    return tuple(
        (
            weighted_x[coarse_index]
            / coarse_masses[coarse_index],
            weighted_y[coarse_index]
            / coarse_masses[coarse_index],
            weighted_z[coarse_index]
            / coarse_masses[coarse_index],
        )
        for coarse_index in range(
            partition.coarse_count
        )
    )
