"""Reference E(3)-equivariant layer execution for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import InteractionGraph

from .features import NodeFeatureVector
from .message import EquivariantMessage
from .message_operator import RadialMessageOperator
from .message_passing import MessagePassingResult, message_passing_step
from .update import update_feature_vector


@dataclass(frozen=True, slots=True)
class EquivariantLayerResult:
    """Result of one reference equivariant layer execution."""

    previous: NodeFeatureVector
    messages: tuple[EquivariantMessage, ...]
    aggregated: NodeFeatureVector
    current: NodeFeatureVector

    def __post_init__(self) -> None:
        if not isinstance(self.previous, NodeFeatureVector):
            raise TypeError(
                "previous must be a NodeFeatureVector instance."
            )

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

        if not isinstance(self.current, NodeFeatureVector):
            raise TypeError(
                "current must be a NodeFeatureVector instance."
            )

        node_count = self.previous.node_count

        if self.aggregated.node_count != node_count:
            raise ValueError(
                "aggregated node count must match previous node count."
            )

        if self.current.node_count != node_count:
            raise ValueError(
                "current node count must match previous node count."
            )


def equivariant_layer_step(
    configuration: AtomicConfiguration,
    graph: InteractionGraph,
    features: NodeFeatureVector,
    operator: RadialMessageOperator,
) -> EquivariantLayerResult:
    """Execute one reference equivariant message-and-update layer."""

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

    passing: MessagePassingResult = message_passing_step(
        configuration,
        graph,
        features,
        operator,
    )

    current = update_feature_vector(
        features,
        passing.aggregated,
    )

    return EquivariantLayerResult(
        previous=features,
        messages=passing.messages,
        aggregated=passing.aggregated,
        current=current,
    )
