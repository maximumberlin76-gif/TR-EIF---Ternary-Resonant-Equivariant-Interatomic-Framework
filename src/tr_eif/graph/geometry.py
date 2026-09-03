"""Geometric evaluation of TR-EIF interaction-graph edges."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from tr_eif.configuration import AtomicConfiguration, Vector3
from tr_eif.geometry import periodic_image_displacement

from .interaction import InteractionEdge


@dataclass(frozen=True, slots=True)
class EdgeGeometry:
    """Geometric quantities associated with one directed interaction edge."""

    displacement: Vector3
    distance: float
    unit_direction: Vector3


def evaluate_edge_geometry(
    configuration: AtomicConfiguration,
    edge: InteractionEdge,
) -> EdgeGeometry:
    """Evaluate displacement, distance, and direction for an interaction edge."""

    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError("configuration must be an AtomicConfiguration instance.")

    if not isinstance(edge, InteractionEdge):
        raise TypeError("edge must be an InteractionEdge instance.")

    if edge.source >= configuration.atom_count:
        raise ValueError("edge.source is outside the configuration atom range.")

    if edge.receiver >= configuration.atom_count:
        raise ValueError("edge.receiver is outside the configuration atom range.")

    if configuration.cell is None:
        if edge.image != (0, 0, 0):
            raise ValueError(
                "A nonzero periodic image requires a simulation cell."
            )

        source_position = configuration.positions[edge.source]
        target_position = configuration.positions[edge.receiver]

        delta = (
            target_position[0] - source_position[0],
            target_position[1] - source_position[1],
            target_position[2] - source_position[2],
        )
    else:
        for axis, image_component in enumerate(edge.image):
            if image_component != 0 and not configuration.periodic[axis]:
                raise ValueError(
                    "A nonzero image component is not allowed on a "
                    "non-periodic axis."
                )

        delta = periodic_image_displacement(
            configuration.positions[edge.source],
            configuration.positions[edge.receiver],
            configuration.cell,
            edge.image,
        )

    norm_squared = (
        delta[0] * delta[0]
        + delta[1] * delta[1]
        + delta[2] * delta[2]
    )

    if norm_squared == 0.0:
        raise ValueError(
            "Edge direction is undefined for zero-length interaction geometry."
        )

    norm = sqrt(norm_squared)

    direction = (
        delta[0] / norm,
        delta[1] / norm,
        delta[2] / norm,
    )

    return EdgeGeometry(
        displacement=delta,
        distance=norm,
        unit_direction=direction,
    )
