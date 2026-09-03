"""Reference E(3)-equivariant message operator for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.configuration import Vector3

from .edge import EquivariantEdgeInput
from .features import NodeFeatures
from .message import EquivariantMessage


def _scale_vector(
    vector: Vector3,
    scale: float,
) -> Vector3:
    return (
        scale * vector[0],
        scale * vector[1],
        scale * vector[2],
    )


@dataclass(frozen=True, slots=True)
class RadialMessageOperator:
    """Reference radial operator preserving feature-channel dimensions."""

    distance_scale: float = 1.0

    def __post_init__(self) -> None:
        if not isinstance(
            self.distance_scale,
            (int, float),
        ) or isinstance(self.distance_scale, bool):
            raise TypeError(
                "distance_scale must be a real number."
            )

        if not isfinite(self.distance_scale):
            raise ValueError(
                "distance_scale must be finite."
            )

        if self.distance_scale <= 0.0:
            raise ValueError(
                "distance_scale must be positive."
            )

        object.__setattr__(
            self,
            "distance_scale",
            float(self.distance_scale),
        )

    def radial_weight(
        self,
        distance: float,
    ) -> float:
        """Return the reference invariant radial weight."""

        if not isinstance(distance, (int, float)) or isinstance(
            distance,
            bool,
        ):
            raise TypeError(
                "distance must be a real number."
            )

        if not isfinite(distance):
            raise ValueError(
                "distance must be finite."
            )

        if distance <= 0.0:
            raise ValueError(
                "distance must be positive."
            )

        ratio = distance / self.distance_scale
        return 1.0 / (1.0 + ratio * ratio)

    def message(
        self,
        source_features: NodeFeatures,
        edge_input: EquivariantEdgeInput,
    ) -> EquivariantMessage:
        """Construct one deterministic radial equivariant message."""

        if not isinstance(source_features, NodeFeatures):
            raise TypeError(
                "source_features must be a NodeFeatures instance."
            )

        if not isinstance(edge_input, EquivariantEdgeInput):
            raise TypeError(
                "edge_input must be an EquivariantEdgeInput instance."
            )

        weight = self.radial_weight(
            edge_input.distance
        )

        scalar_messages = tuple(
            weight * scalar
            for scalar in source_features.scalars
        )

        vector_messages = tuple(
            _scale_vector(vector, weight)
            for vector in source_features.vectors
        )

        return EquivariantMessage(
            source=edge_input.source,
            receiver=edge_input.receiver,
            scalars=scalar_messages,
            vectors=vector_messages,
        )
