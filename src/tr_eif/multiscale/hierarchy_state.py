"""State construction across TR-EIF multiscale hierarchies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from tr_eif.configuration import Vector3

from .hierarchy import MultiscaleHierarchy
from .state import (
    CoarseScaleState,
    build_coarse_scale_state,
)


FinePositions: TypeAlias = tuple[Vector3, ...]
FineMasses: TypeAlias = tuple[float, ...]


@dataclass(frozen=True)
class MultiscaleStateHierarchy:
    """Ordered coarse states generated across a multiscale hierarchy."""

    hierarchy: MultiscaleHierarchy
    states: tuple[CoarseScaleState, ...]

    def __post_init__(self) -> None:
        """Validate hierarchy-state correspondence."""

        if not isinstance(
            self.hierarchy,
            MultiscaleHierarchy,
        ):
            raise TypeError(
                "hierarchy must be a MultiscaleHierarchy instance."
            )

        if not isinstance(
            self.states,
            tuple,
        ):
            raise TypeError(
                "states must be a tuple."
            )

        if len(self.states) != self.hierarchy.transition_count:
            raise ValueError(
                "states must contain one coarse state per "
                "hierarchy transition."
            )

        for index, state in enumerate(
            self.states
        ):
            if not isinstance(
                state,
                CoarseScaleState,
            ):
                raise TypeError(
                    f"states[{index}] must be a "
                    "CoarseScaleState instance."
                )

            expected_partition = (
                self.hierarchy.partition_at(
                    index
                )
            )

            if state.partition != expected_partition:
                raise ValueError(
                    f"states[{index}] partition must match "
                    "the corresponding hierarchy transition."
                )

            expected_coarse_count = (
                self.hierarchy.level_counts[
                    index + 1
                ]
            )

            if state.coarse_count != expected_coarse_count:
                raise ValueError(
                    f"states[{index}] coarse count must match "
                    "the corresponding hierarchy level."
                )

    @property
    def state_count(self) -> int:
        """Return the number of generated coarse states."""

        return len(self.states)

    @property
    def coarsest_state(self) -> CoarseScaleState:
        """Return the state at the coarsest represented level."""

        return self.states[-1]

    def state_at(
        self,
        level: int,
    ) -> CoarseScaleState:
        """Return the generated coarse state for a non-finest level."""

        if not isinstance(
            level,
            int,
        ) or isinstance(
            level,
            bool,
        ):
            raise TypeError(
                "level must be an integer."
            )

        if (
            level <= 0
            or level >= self.hierarchy.level_count
        ):
            raise IndexError(
                "level is out of range for generated coarse states."
            )

        return self.states[
            level - 1
        ]


def build_multiscale_state_hierarchy(
    positions: FinePositions,
    masses: FineMasses,
    hierarchy: MultiscaleHierarchy,
) -> MultiscaleStateHierarchy:
    """Build coarse states sequentially across a multiscale hierarchy."""

    if not isinstance(
        hierarchy,
        MultiscaleHierarchy,
    ):
        raise TypeError(
            "hierarchy must be a MultiscaleHierarchy instance."
        )

    current_positions = positions
    current_masses = masses

    states: list[CoarseScaleState] = []

    for transition_index in range(
        hierarchy.transition_count
    ):
        partition = hierarchy.partition_at(
            transition_index
        )

        state = build_coarse_scale_state(
            positions=current_positions,
            masses=current_masses,
            partition=partition,
        )

        states.append(state)

        current_positions = state.positions
        current_masses = state.masses

    return MultiscaleStateHierarchy(
        hierarchy=hierarchy,
        states=tuple(states),
    )
