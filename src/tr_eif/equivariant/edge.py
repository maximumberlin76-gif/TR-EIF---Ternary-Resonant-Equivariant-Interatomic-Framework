"""Edge-local invariant and equivariant inputs for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.configuration import AtomicConfiguration, Vector3
from tr_eif.graph import (
    EdgeGeometry,
    InteractionEdge,
    evaluate_edge_geometry,
)


def _validate_vector3(
    value: Vector3,
    *,
    field_name: str,
) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple.")

    if len(value) != 3:
        raise ValueError(
            f"{field_name} must contain exactly three components."
        )

    if not all(isfinite(component) for component in value):
        raise ValueError(
            f"{field_name} must contain only finite values."
        )


@dataclass(frozen=True, slots=True)
class EquivariantEdgeInput:
    """Invariant and polar-vector inputs associated with one directed edge."""

    source: int
    receiver: int
    distance: float
    direction: Vector3

    def __post_init__(self) -> None:
        if not isinstance(self.source, int) or isinstance(self.source, bool):
            raise TypeError("source must be an integer.")

        if not isinstance(self.receiver, int) or isinstance(
            self.receiver,
            bool,
        ):
            raise TypeError("receiver must be an integer.")

        if self.source < 0:
            raise ValueError("source must be nonnegative.")

        if self.receiver < 0:
            raise ValueError("receiver must be nonnegative.")

        if not isinstance(self.distance, (int, float)) or isinstance(
            self.distance,
            bool,
        ):
            raise TypeError("distance must be a real number.")

        if not isfinite(self.distance):
            raise ValueError("distance must be finite.")

        if self.distance <= 0.0:
            raise ValueError("distance must be positive.")

        _validate_vector3(
            self.direction,
            field_name="direction",
        )

    @property
    def invariant_scalar(self) -> float:
        """Return the edge-distance invariant."""

        return float(self.distance)

    @property
    def equivariant_vector(self) -> Vector3:
        """Return the directed polar unit vector."""

        return self.direction


def edge_input_from_geometry(
    edge: InteractionEdge,
    geometry: EdgeGeometry,
) -> EquivariantEdgeInput:
    """Construct one equivariant edge input from evaluated edge geometry."""

    if not isinstance(edge, InteractionEdge):
        raise TypeError(
            "edge must be an InteractionEdge instance."
        )

    if not isinstance(geometry, EdgeGeometry):
        raise TypeError(
            "geometry must be an EdgeGeometry instance."
        )

    return EquivariantEdgeInput(
        source=edge.source,
        receiver=edge.receiver,
        distance=geometry.distance,
        direction=geometry.unit_direction,
    )


def evaluate_equivariant_edge_input(
    configuration: AtomicConfiguration,
    edge: InteractionEdge,
) -> EquivariantEdgeInput:
    """Evaluate one directed edge as invariant and equivariant inputs."""

    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError(
            "configuration must be an AtomicConfiguration instance."
        )

    if not isinstance(edge, InteractionEdge):
        raise TypeError(
            "edge must be an InteractionEdge instance."
        )

    geometry = evaluate_edge_geometry(
        configuration,
        edge,
    )

    return edge_input_from_geometry(
        edge,
        geometry,
    )
