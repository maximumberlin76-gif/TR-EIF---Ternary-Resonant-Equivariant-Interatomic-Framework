"""Scalar and vector feature representations for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import Vector3

ScalarFeatures: TypeAlias = tuple[float, ...]
VectorFeatures: TypeAlias = tuple[Vector3, ...]


def _validate_scalar_features(
    values: ScalarFeatures,
    *,
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple.")

    if not all(isfinite(value) for value in values):
        raise ValueError(f"{field_name} must contain only finite values.")


def _validate_vector_features(
    values: VectorFeatures,
    *,
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple.")

    for index, vector in enumerate(values):
        if not isinstance(vector, tuple):
            raise TypeError(
                f"{field_name}[{index}] must be a tuple."
            )

        if len(vector) != 3:
            raise ValueError(
                f"{field_name}[{index}] must contain exactly "
                "three components."
            )

        if not all(isfinite(component) for component in vector):
            raise ValueError(
                f"{field_name}[{index}] must contain only finite values."
            )


@dataclass(frozen=True, slots=True)
class NodeFeatures:
    """Invariant scalar and equivariant vector features for one node."""

    scalars: ScalarFeatures = ()
    vectors: VectorFeatures = ()

    def __post_init__(self) -> None:
        _validate_scalar_features(
            self.scalars,
            field_name="scalars",
        )
        _validate_vector_features(
            self.vectors,
            field_name="vectors",
        )

        if len(self.scalars) == 0 and len(self.vectors) == 0:
            raise ValueError(
                "NodeFeatures must contain at least one feature channel."
            )

    @property
    def scalar_channel_count(self) -> int:
        """Return the number of invariant scalar channels."""

        return len(self.scalars)

    @property
    def vector_channel_count(self) -> int:
        """Return the number of equivariant vector channels."""

        return len(self.vectors)


@dataclass(frozen=True, slots=True)
class NodeFeatureVector:
    """Immutable feature state for an ordered collection of nodes."""

    nodes: tuple[NodeFeatures, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.nodes, tuple):
            raise TypeError("nodes must be a tuple.")

        if len(self.nodes) == 0:
            raise ValueError("nodes must not be empty.")

        for index, node in enumerate(self.nodes):
            if not isinstance(node, NodeFeatures):
                raise TypeError(
                    f"nodes[{index}] must be a NodeFeatures instance."
                )

        scalar_count = self.nodes[0].scalar_channel_count
        vector_count = self.nodes[0].vector_channel_count

        for index, node in enumerate(self.nodes[1:], start=1):
            if node.scalar_channel_count != scalar_count:
                raise ValueError(
                    f"nodes[{index}] has an inconsistent number "
                    "of scalar channels."
                )

            if node.vector_channel_count != vector_count:
                raise ValueError(
                    f"nodes[{index}] has an inconsistent number "
                    "of vector channels."
                )

    @property
    def node_count(self) -> int:
        """Return the number of nodes represented by the feature state."""

        return len(self.nodes)

    @property
    def scalar_channel_count(self) -> int:
        """Return the common number of scalar channels per node."""

        return self.nodes[0].scalar_channel_count

    @property
    def vector_channel_count(self) -> int:
        """Return the common number of vector channels per node."""

        return self.nodes[0].vector_channel_count
