"""Deterministic equivariant message passing for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import InteractionGraph

from .aggregation import aggregate_messages
from .edge import evaluate_equivariant_edge_input
from .features import NodeFeatureVector
from .message import EquivariantMessage
from .message_operator import RadialMessageOperator


@dataclass(frozen=True, slots=True)
class MessagePassingResult:
    """Messages and receiver-wise aggregates from one message-passing pass."""

    messages: tuple[EquivariantMessage, ...]
    aggregated: NodeFeatureVector

    def __post_init__(self) -> None:
        if not isinstance(self.messages, tuple):
            raise TypeError("messages must be a tuple.")

        if len(self.messages) == 0:
            raise ValueError("messages must not be empty.")

        for index, message in enumerate(self.messages):
            if not isinstance(message, EquivariantMessage):
                raise TypeError(
                    f"messages[{index}] must be an "
                    "EquivariantMessage instance."
                )

        if not isinstance(self.aggregated, NodeFeatureVector):
            raise TypeError(
                "aggregated must be a NodeFeatureVector instance."
            )


def message_passing_step(
    configuration: AtomicConfiguration,
    graph: InteractionGraph,
    features: NodeFeatureVector,
    operator: RadialMessageOperator,
) -> MessagePassingResult:
    """Execute one deterministic equivariant message-passing pass."""

    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError(
            "configuration must be an AtomicConfiguration instance."
        )

    if not isinstance(graph, InteractionGraph):
        raise TypeError(
            "graph must be an InteractionGraph instance."
        )

    if not isinstance(features, NodeFeatureVector):
        raise TypeError(
            "features must be a NodeFeatureVector instance."
        )

    if not isinstance(operator, RadialMessageOperator):
        raise TypeError(
            "operator must be a RadialMessageOperator instance."
        )

    if graph.node_count != configuration.atom_count:
        raise ValueError(
            "graph node count must match configuration atom count."
        )

    if features.node_count != graph.node_count:
        raise ValueError(
            "feature node count must match graph node count."
        )

    if len(graph.edges) == 0:
        raise ValueError(
            "message passing requires at least one interaction edge."
        )

    ordered_edges = sorted(
        graph.edges,
        key=lambda edge: (
            edge.receiver,
            edge.source,
            edge.image,
        ),
    )

    messages: list[EquivariantMessage] = []

    for edge in ordered_edges:
        edge_input = evaluate_equivariant_edge_input(
            configuration,
            edge,
        )

        source_features = features.nodes[edge.source]

        messages.append(
            operator.message(
                source_features,
                edge_input,
            )
        )

    message_tuple = tuple(messages)

    aggregated = aggregate_messages(
        message_tuple,
        graph.node_count,
    )

    return MessagePassingResult(
        messages=message_tuple,
        aggregated=aggregated,
    )
