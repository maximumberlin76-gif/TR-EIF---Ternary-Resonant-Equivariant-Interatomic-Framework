"""Typed interaction-graph structures for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

ImageIndex: TypeAlias = tuple[int, int, int]


def _validate_node_index(value: int, *, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be an integer.")

    if value < 0:
        raise ValueError(f"{field_name} must be non-negative.")


def _validate_image_index(image: ImageIndex) -> None:
    if len(image) != 3:
        raise ValueError("image must contain exactly three integer indices.")

    if not all(
        isinstance(component, int) and not isinstance(component, bool)
        for component in image
    ):
        raise TypeError("image must contain only integer indices.")


@dataclass(frozen=True, slots=True)
class InteractionEdge:
    """Directed interaction edge from source node to receiver node."""

    source: int
    receiver: int
    image: ImageIndex = (0, 0, 0)

    def __post_init__(self) -> None:
        _validate_node_index(self.source, field_name="source")
        _validate_node_index(self.receiver, field_name="receiver")
        _validate_image_index(self.image)


@dataclass(frozen=True, slots=True)
class InteractionGraph:
    """Immutable directed interaction graph with explicit periodic images."""

    node_count: int
    edges: tuple[InteractionEdge, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.node_count, int) or isinstance(self.node_count, bool):
            raise TypeError("node_count must be an integer.")

        if self.node_count <= 0:
            raise ValueError("node_count must be positive.")

        for index, edge in enumerate(self.edges):
            if not isinstance(edge, InteractionEdge):
                raise TypeError(
                    f"edges[{index}] must be an InteractionEdge instance."
                )

            if edge.source >= self.node_count:
                raise ValueError(
                    f"edges[{index}].source is outside the graph node range."
                )

            if edge.receiver >= self.node_count:
                raise ValueError(
                    f"edges[{index}].receiver is outside the graph node range."
                )

        if len(set(self.edges)) != len(self.edges):
            raise ValueError(
                "InteractionGraph must not contain duplicate directed edges."
            )

    @property
    def edge_count(self) -> int:
        """Return the number of directed interaction edges."""

        return len(self.edges)

    def incoming_edges(self, receiver: int) -> tuple[InteractionEdge, ...]:
        """Return directed edges whose receiver is the requested node."""

        _validate_node_index(receiver, field_name="receiver")

        if receiver >= self.node_count:
            raise ValueError("receiver is outside the graph node range.")

        return tuple(edge for edge in self.edges if edge.receiver == receiver)

    def outgoing_edges(self, source: int) -> tuple[InteractionEdge, ...]:
        """Return directed edges whose source is the requested node."""

        _validate_node_index(source, field_name="source")

        if source >= self.node_count:
            raise ValueError("source is outside the graph node range.")

        return tuple(edge for edge in self.edges if edge.source == source)
