"""Deterministic time integration for TR-EIF phase dynamics."""

from __future__ import annotations

from math import isfinite

from tr_eif.graph import InteractionGraph

from .dynamics import phase_derivatives
from .parameters import PhaseDynamicsParameters
from .state import ResonanceState, wrap_phases


def _validate_time_step(time_step: float) -> float:
    if not isinstance(time_step, (int, float)) or isinstance(time_step, bool):
        raise TypeError("time_step must be a real number.")

    if not isfinite(time_step):
        raise ValueError("time_step must be finite.")

    if time_step <= 0.0:
        raise ValueError("time_step must be positive.")

    return float(time_step)


def euler_step(
    state: ResonanceState,
    parameters: PhaseDynamicsParameters,
    graph: InteractionGraph,
    time_step: float,
) -> ResonanceState:
    """Advance continuous phase dynamics by one explicit Euler step."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    if not isinstance(parameters, PhaseDynamicsParameters):
        raise TypeError(
            "parameters must be a PhaseDynamicsParameters instance."
        )

    if not isinstance(graph, InteractionGraph):
        raise TypeError("graph must be an InteractionGraph instance.")

    dt = _validate_time_step(time_step)

    derivatives = phase_derivatives(
        state,
        parameters,
        graph,
    )

    next_phases = wrap_phases(
        tuple(
            phase + dt * derivative
            for phase, derivative in zip(
                state.phases,
                derivatives,
                strict=True,
            )
        )
    )

    return ResonanceState(
        phases=next_phases,
        frequencies=state.frequencies,
    )
