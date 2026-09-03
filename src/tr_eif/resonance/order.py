"""Phase-order observables for TR-EIF."""

from __future__ import annotations

from math import cos, hypot, sin

from .state import PhaseVector, ResonanceState


def phase_order_parameter(phases: PhaseVector) -> float:
    """Return the magnitude of the mean complex phase vector."""

    if len(phases) == 0:
        raise ValueError("phases must not be empty.")

    mean_cosine = sum(cos(phase) for phase in phases) / len(phases)
    mean_sine = sum(sin(phase) for phase in phases) / len(phases)

    return hypot(mean_cosine, mean_sine)


def state_phase_order(state: ResonanceState) -> float:
    """Return the phase-order parameter of a resonance state."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    return phase_order_parameter(state.phases)
