"""Multilevel partition hierarchies for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass

from .composition import compose_partitions
from .partition import MultiscalePartition


@dataclass(frozen=True)
class MultiscaleHierarchy:
    """Ordered compatible sequence of multiscale partitions."""

    partitions: tuple[MultiscalePartition, ...]

    def __post_init__(self) -> None:
        """Validate the hierarchy and all adjacent scale boundaries."""

        if not isinstance(
            self.partitions,
            tuple,
        ):
            raise TypeError(
                "partitions must be a tuple."
            )

        if len(self.partitions) == 0:
            raise ValueError(
                "partitions must not be empty."
            )

        for index, partition in enumerate(
            self.partitions
        ):
            if not isinstance(
                partition,
                MultiscalePartition,
            ):
                raise TypeError(
                    f"partitions[{index}] must be a "
                    "MultiscalePartition instance."
                )

        for index in range(
            len(self.partitions) - 1
        ):
            current = self.partitions[index]
            following = self.partitions[
                index + 1
            ]

            if (
                current.coarse_count
                != following.fine_count
            ):
                raise ValueError(
                    "adjacent partitions must have matching "
                    "coarse and fine cardinalities."
                )

    @property
    def level_count(self) -> int:
        """Return the number of represented scale levels."""

        return len(self.partitions) + 1

    @property
    def transition_count(self) -> int:
        """Return the number of scale transitions."""

        return len(self.partitions)

    @property
    def finest_count(self) -> int:
        """Return the entity count at the finest represented level."""

        return self.partitions[0].fine_count

    @property
    def coarsest_count(self) -> int:
        """Return the entity count at the coarsest represented level."""

        return self.partitions[-1].coarse_count

    @property
    def level_counts(self) -> tuple[int, ...]:
        """Return entity cardinalities for all represented levels."""

        return (
            self.partitions[0].fine_count,
            *(
                partition.coarse_count
                for partition in self.partitions
            ),
        )

    def partition_at(
        self,
        transition_index: int,
    ) -> MultiscalePartition:
        """Return the partition for one adjacent scale transition."""

        if not isinstance(
            transition_index,
            int,
        ) or isinstance(
            transition_index,
            bool,
        ):
            raise TypeError(
                "transition_index must be an integer."
            )

        if (
            transition_index < 0
            or transition_index
            >= self.transition_count
        ):
            raise IndexError(
                "transition_index is out of range."
            )

        return self.partitions[
            transition_index
        ]

    def composed_partition(
        self,
        start_level: int = 0,
        end_level: int | None = None,
    ) -> MultiscalePartition:
        """Compose adjacent partitions between two represented levels."""

        if not isinstance(
            start_level,
            int,
        ) or isinstance(
            start_level,
            bool,
        ):
            raise TypeError(
                "start_level must be an integer."
            )

        if end_level is None:
            end_level = self.level_count - 1
        elif not isinstance(
            end_level,
            int,
        ) or isinstance(
            end_level,
            bool,
        ):
            raise TypeError(
                "end_level must be an integer or None."
            )

        if (
            start_level < 0
            or start_level
            >= self.level_count
        ):
            raise IndexError(
                "start_level is out of range."
            )

        if (
            end_level < 0
            or end_level
            >= self.level_count
        ):
            raise IndexError(
                "end_level is out of range."
            )

        if end_level <= start_level:
            raise ValueError(
                "end_level must be greater than start_level."
            )

        result = self.partitions[
            start_level
        ]

        for transition_index in range(
            start_level + 1,
            end_level
        ):
            result = compose_partitions(
                fine_to_intermediate=result,
                intermediate_to_coarse=self.partitions[
                    transition_index
                ],
            )

        return result
