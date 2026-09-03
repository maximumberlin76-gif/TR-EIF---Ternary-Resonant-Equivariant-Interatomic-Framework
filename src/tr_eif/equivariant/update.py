"""Deterministic equivariant node updates for TR-EIF."""

from __future__ import annotations

from tr_eif.configuration import Vector3

from .features import NodeFeatures, NodeFeatureVector


def _add_vector(
    left: Vector3,
    right: Vector3,
) -> Vector3:
    return (
        left[0] + right[0],
        left[1] + right[1],
        left[2] + right[2],
    )


def update_node_features(
    previous: NodeFeatures,
    aggregated: NodeFeatures,
) -> NodeFeatures:
    """Apply one additive equivariant update to a single node."""

    if not isinstance(previous, NodeFeatures):
        raise TypeError(
            "previous must be a NodeFeatures instance."
        )

    if not isinstance(aggregated, NodeFeatures):
        raise TypeError(
            "aggregated must be a NodeFeatures instance."
        )

    if (
        previous.scalar_channel_count
        != aggregated.scalar_channel_count
    ):
        raise ValueError(
            "previous and aggregated scalar channel counts must match."
        )

    if (
        previous.vector_channel_count
        != aggregated.vector_channel_count
    ):
        raise ValueError(
            "previous and aggregated vector channel counts must match."
        )

    scalars = tuple(
        previous_value + aggregated_value
        for previous_value, aggregated_value in zip(
            previous.scalars,
            aggregated.scalars,
            strict=True,
        )
    )

    vectors = tuple(
        _add_vector(previous_vector, aggregated_vector)
        for previous_vector, aggregated_vector in zip(
            previous.vectors,
            aggregated.vectors,
            strict=True,
        )
    )

    return NodeFeatures(
        scalars=scalars,
        vectors=vectors,
    )


def update_feature_vector(
    previous: NodeFeatureVector,
    aggregated: NodeFeatureVector,
) -> NodeFeatureVector:
    """Apply one additive equivariant update to all nodes."""

    if not isinstance(previous, NodeFeatureVector):
        raise TypeError(
            "previous must be a NodeFeatureVector instance."
        )

    if not isinstance(aggregated, NodeFeatureVector):
        raise TypeError(
            "aggregated must be a NodeFeatureVector instance."
        )

    if previous.node_count != aggregated.node_count:
        raise ValueError(
            "previous and aggregated node counts must match."
        )

    if (
        previous.scalar_channel_count
        != aggregated.scalar_channel_count
    ):
        raise ValueError(
            "previous and aggregated scalar channel counts must match."
        )

    if (
        previous.vector_channel_count
        != aggregated.vector_channel_count
    ):
        raise ValueError(
            "previous and aggregated vector channel counts must match."
        )

    return NodeFeatureVector(
        nodes=tuple(
            update_node_features(
                previous_node,
                aggregated_node,
            )
            for previous_node, aggregated_node in zip(
                previous.nodes,
                aggregated.nodes,
                strict=True,
            )
        )
    )
