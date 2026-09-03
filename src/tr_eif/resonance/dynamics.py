"""Graph-coupled continuous phase dynamics for TR-EIF."""

from __future__ import annotations

from math import sin
from typing import TypeAlias

from tr_eif.graph import InteractionGraph

from .parameters import PhaseDynamicsParameters
from .state import ResonanceState

PhaseDerivativeVector: TypeAlias = tuple[float, ...]


def phase_derivatives(
    state: ResonanceState,
    parameters: PhaseDynamicsParameters,
    graph: InteractionGraph,
) -> PhaseDerivativeVector:
    """Evaluate graph-coupled Kuramoto-Sakaguchi phase derivatives."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    if not isinstance(parameters, PhaseDynamicsParameters):
        raise TypeError(
            "parameters must be a PhaseDynamicsParameters instance."
        )

    if not isinstance(graph, InteractionGraph):
        raise TypeError("graph must be an InteractionGraph instance.")

    parameters.validate_oscillator_count(state.oscillator_count)

    if graph.node_count != state.oscillator_count:
        raise ValueError(
            "graph node count must match the resonance-state oscillator count."
        )

    derivatives = list(state.frequencies)

    for edge in graph.edges:
        source = edge.source
        receiver = edge.receiver

        phase_difference = (
            state.phases[source]
            - state.phases[receiver]
            - parameters.phase_lag[receiver]
        )

        derivatives[receiver] += (
            parameters.coupling[receiver] * sin(phase_difference)
        )

    return tuple(derivatives)
