"""Deterministic interaction-graph construction for TR-EIF."""

from __future__ import annotations

from math import isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.geometry import (
    displacement,
    minimum_image_displacement,
    squared_distance,
)

from .interaction import InteractionEdge, InteractionGraph


def _validate_cutoff(cutoff: float) -> None:
    if not isinstance(cutoff, (int, float)) or isinstance(cutoff, bool):
        raise TypeError("cutoff must be a real number.")

    if not isfinite(cutoff):
        raise ValueError("cutoff must be finite.")

    if cutoff <= 0.0:
        raise ValueError("cutoff must be positive.")


def build_cutoff_graph(
    configuration: AtomicConfiguration,
    cutoff: float,
) -> InteractionGraph:
    """Build a deterministic directed graph from a radial cutoff."""

    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError("configuration must be an AtomicConfiguration instance.")

    _validate_cutoff(cutoff)

    cutoff_squared = float(cutoff) * float(cutoff)
    edges: list[InteractionEdge] = []

    for source in range(configuration.atom_count):
        for receiver in range(configuration.atom_count):
            if source == receiver:
                continue

            source_position = configuration.positions[source]
            receiver_position = configuration.positions[receiver]

            if configuration.is_periodic:
                if configuration.cell is None:
                    raise ValueError(
                        "Periodic configuration requires a simulation cell."
                    )

                delta = minimum_image_displacement(
                    source_position,
                    receiver_position,
                    configuration.cell,
                    configuration.periodic,
                )
                distance_squared = squared_distance(
                    (0.0, 0.0, 0.0),
                    delta,
                )
            else:
                delta = displacement(
                    source_position,
                    receiver_position,
                )
                distance_squared = squared_distance(
                    (0.0, 0.0, 0.0),
                    delta,
                )

            if distance_squared <= cutoff_squared:
                edges.append(
                    InteractionEdge(
                        source=source,
                        receiver=receiver,
                    )
                )

    return InteractionGraph(
        node_count=configuration.atom_count,
        edges=tuple(edges),
    )
