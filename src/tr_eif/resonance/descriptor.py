"""Resonance-coordinate descriptor construction for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .order import state_phase_order
from .state import ResonanceState
from .window import ResonanceCoordinate, ResonanceSpace


@dataclass(frozen=True, slots=True)
class ResonanceDescriptor:
    """Continuous descriptor used to construct a resonance coordinate."""

    phase_order: float
    frequency_spread: float

    def as_coordinate(self) -> ResonanceCoordinate:
        """Return the descriptor as a resonance-space coordinate."""

        return (
            self.phase_order,
            self.frequency_spread,
        )


def frequency_spread(state: ResonanceState) -> float:
    """Return the population standard deviation of oscillator frequencies."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    count = state.oscillator_count
    mean_frequency = sum(state.frequencies) / count

    variance = sum(
        (frequency - mean_frequency) ** 2
        for frequency in state.frequencies
    ) / count

    return sqrt(variance)


def resonance_descriptor(
    state: ResonanceState,
) -> ResonanceDescriptor:
    """Construct the reference continuous resonance descriptor."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    return ResonanceDescriptor(
        phase_order=state_phase_order(state),
        frequency_spread=frequency_spread(state),
    )


def resonance_coordinate(
    state: ResonanceState,
    space: ResonanceSpace,
) -> ResonanceCoordinate:
    """Construct and validate the reference resonance coordinate."""

    if not isinstance(space, ResonanceSpace):
        raise TypeError("space must be a ResonanceSpace instance.")

    descriptor = resonance_descriptor(state)
    coordinate = descriptor.as_coordinate()

    space.validate_coordinate(coordinate)

    return coordinate
