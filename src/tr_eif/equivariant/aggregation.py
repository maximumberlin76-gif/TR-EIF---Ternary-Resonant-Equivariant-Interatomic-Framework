"""Deterministic equivariant message aggregation for TR-EIF."""

from __future__ import annotations

from tr_eif.configuration import Vector3

from .features import NodeFeatures, NodeFeatureVector
from .message import EquivariantMessage


def _add_vector(
    left: Vector3,
    right: Vector3,
) -> Vector3:
    return (
        left[0] + right[0],
        left[1] + right[1],
        left[2] + right[2],
    )


def aggregate_messages(
    messages: tuple[EquivariantMessage, ...],
    node_count: int,
) -> NodeFeatureVector:
    """Aggregate directed messages by receiver using channel-wise sums."""

    if not isinstance(messages, tuple):
        raise TypeError("messages must be a tuple.")

    if not isinstance(node_count, int) or isinstance(node_count, bool):
        raise TypeError("node_count must be an integer.")

    if node_count <= 0:
        raise ValueError("node_count must be positive.")

    if len(messages) == 0:
        raise ValueError("messages must not be empty.")

    for index, message in enumerate(messages):
        if not isinstance(message, EquivariantMessage):
            raise TypeError(
                f"messages[{index}] must be an EquivariantMessage instance."
            )

        if message.source >= node_count:
            raise ValueError(
                f"messages[{index}].source is outside the node range."
            )

        if message.receiver >= node_count:
            raise ValueError(
                f"messages[{index}].receiver is outside the node range."
            )

    scalar_count = messages[0].scalar_channel_count
    vector_count = messages[0].vector_channel_count

    for index, message in enumerate(messages[1:], start=1):
        if message.scalar_channel_count != scalar_count:
            raise ValueError(
                f"messages[{index}] has an inconsistent number "
                "of scalar channels."
            )

        if message.vector_channel_count != vector_count:
            raise ValueError(
                f"messages[{index}] has an inconsistent number "
                "of vector channels."
            )

    if scalar_count == 0 and vector_count == 0:
        raise ValueError(
            "messages must contain at least one feature channel."
        )

    scalar_sums = [
        [0.0 for _ in range(scalar_count)]
        for _ in range(node_count)
    ]
    vector_sums = [
        [
            (0.0, 0.0, 0.0)
            for _ in range(vector_count)
        ]
        for _ in range(node_count)
    ]
    receiver_counts = [0 for _ in range(node_count)]

    ordered_messages = sorted(
        messages,
        key=lambda message: (
            message.receiver,
            message.source,
            message.scalars,
            message.vectors,
        ),
    )

    for message in ordered_messages:
        receiver = message.receiver
        receiver_counts[receiver] += 1

        for channel, value in enumerate(message.scalars):
            scalar_sums[receiver][channel] += value

        for channel, vector in enumerate(message.vectors):
            vector_sums[receiver][channel] = _add_vector(
                vector_sums[receiver][channel],
                vector,
            )

    nodes: list[NodeFeatures] = []

    for receiver in range(node_count):
        if receiver_counts[receiver] == 0:
            scalars = tuple(
                0.0
                for _ in range(scalar_count)
            )
            vectors = tuple(
                (0.0, 0.0, 0.0)
                for _ in range(vector_count)
            )
        else:
            scalars = tuple(scalar_sums[receiver])
            vectors = tuple(vector_sums[receiver])

        nodes.append(
            NodeFeatures(
                scalars=scalars,
                vectors=vectors,
            )
        )

    return NodeFeatureVector(
        nodes=tuple(nodes)
    )
