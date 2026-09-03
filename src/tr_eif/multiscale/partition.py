"""Discrete fine-to-coarse partitions for TR-EIF multiscale models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MultiscalePartition:
    """Immutable mapping from fine-scale entities to coarse-scale entities."""

    fine_to_coarse: tuple[int, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.fine_to_coarse, tuple):
            raise TypeError(
                "fine_to_coarse must be a tuple."
            )

        if len(self.fine_to_coarse) == 0:
            raise ValueError(
                "fine_to_coarse must not be empty."
            )

        normalized: list[int] = []

        for index, coarse_index in enumerate(
            self.fine_to_coarse
        ):
            if not isinstance(coarse_index, int) or isinstance(
                coarse_index,
                bool,
            ):
                raise TypeError(
                    f"fine_to_coarse[{index}] must be an integer."
                )

            if coarse_index < 0:
                raise ValueError(
                    f"fine_to_coarse[{index}] must be nonnegative."
                )

            normalized.append(coarse_index)

        present = set(normalized)
        expected = set(range(max(normalized) + 1))

        if present != expected:
            raise ValueError(
                "coarse indices must form a contiguous range "
                "starting at zero."
            )

        object.__setattr__(
            self,
            "fine_to_coarse",
            tuple(normalized),
        )

    @property
    def fine_count(self) -> int:
        """Return the number of fine-scale entities."""

        return len(self.fine_to_coarse)

    @property
    def coarse_count(self) -> int:
        """Return the number of represented coarse-scale entities."""

        return max(self.fine_to_coarse) + 1

    def coarse_index_for(
        self,
        fine_index: int,
    ) -> int:
        """Return the coarse entity containing one fine-scale entity."""

        if not isinstance(fine_index, int) or isinstance(
            fine_index,
            bool,
        ):
            raise TypeError(
                "fine_index must be an integer."
            )

        if fine_index < 0 or fine_index >= self.fine_count:
            raise IndexError(
                "fine_index is outside the partition."
            )

        return self.fine_to_coarse[fine_index]

    def fine_indices_for(
        self,
        coarse_index: int,
    ) -> tuple[int, ...]:
        """Return the fine-scale members of one coarse entity."""

        if not isinstance(coarse_index, int) or isinstance(
            coarse_index,
            bool,
        ):
            raise TypeError(
                "coarse_index must be an integer."
            )

        if coarse_index < 0 or coarse_index >= self.coarse_count:
            raise IndexError(
                "coarse_index is outside the partition."
            )

        return tuple(
            fine_index
            for fine_index, assigned_coarse_index in enumerate(
                self.fine_to_coarse
            )
            if assigned_coarse_index == coarse_index
        )

    @property
    def coarse_members(
        self,
    ) -> tuple[tuple[int, ...], ...]:
        """Return all coarse entities as ordered fine-index memberships."""

        return tuple(
            self.fine_indices_for(coarse_index)
            for coarse_index in range(self.coarse_count)
        )

    @property
    def is_identity(self) -> bool:
        """Return whether every fine entity forms its own coarse entity."""

        return self.fine_to_coarse == tuple(
            range(self.fine_count)
        )
