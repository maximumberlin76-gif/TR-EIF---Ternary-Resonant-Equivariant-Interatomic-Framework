"""Composition of TR-EIF multiscale partitions."""

from __future__ import annotations

from .partition import MultiscalePartition


def compose_partitions(
    fine_to_intermediate: MultiscalePartition,
    intermediate_to_coarse: MultiscalePartition,
) -> MultiscalePartition:
    """Compose two consecutive multiscale partitions."""

    if not isinstance(
        fine_to_intermediate,
        MultiscalePartition,
    ):
        raise TypeError(
            "fine_to_intermediate must be a "
            "MultiscalePartition instance."
        )

    if not isinstance(
        intermediate_to_coarse,
        MultiscalePartition,
    ):
        raise TypeError(
            "intermediate_to_coarse must be a "
            "MultiscalePartition instance."
        )

    if (
        fine_to_intermediate.coarse_count
        != intermediate_to_coarse.fine_count
    ):
        raise ValueError(
            "fine_to_intermediate coarse count must equal "
            "intermediate_to_coarse fine count."
        )

    composed = tuple(
        intermediate_to_coarse.coarse_index_for(
            fine_to_intermediate.coarse_index_for(
                fine_index
            )
        )
        for fine_index in range(
            fine_to_intermediate.fine_count
        )
    )

    return MultiscalePartition(
        fine_to_coarse=composed
    )
