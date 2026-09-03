"""Equivariant edge-message representations for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .features import NodeFeatures, ScalarFeatures, VectorFeatures


@dataclass(frozen=True, slots=True)
class EquivariantMessage:
    """Invariant scalar and equivariant vector message on one directed edge."""

    source: int
    receiver: int
    scalars: ScalarFeatures = ()
    vectors: VectorFeatures = ()

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

        validated = NodeFeatures(
            scalars=self.scalars,
            vectors=self.vectors,
        )

        object.__setattr__(
            self,
            "scalars",
            validated.scalars,
        )
        object.__setattr__(
            self,
            "vectors",
            validated.vectors,
        )

    @property
    def scalar_channel_count(self) -> int:
        """Return the number of invariant scalar message channels."""

        return len(self.scalars)

    @property
    def vector_channel_count(self) -> int:
        """Return the number of equivariant vector message channels."""

        return len(self.vectors)

    def as_node_features(self) -> NodeFeatures:
        """Return the message payload as node-feature channels."""

        return NodeFeatures(
            scalars=self.scalars,
            vectors=self.vectors,
        )
