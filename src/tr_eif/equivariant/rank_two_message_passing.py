"""Rank-two Cartesian messages alongside the existing TR-EIF E(3) layer.

Scalar/vector messages use the registered radial message-passing layer.
Polar rank-two channels use the same directed graph and radial weight with
an explicit combination of source tensor, scalar-direction dyad, and
symmetric vector-direction dyad. Under Q in O(3), each tensor term transforms
as Q T Q^T; Cartesian translations leave internal feature channels unchanged.

The retained balanced-ternary state conditions all three feature types using
one declared scale per state. Pending targets remain separate from retained
states. Resonance-derived invariant scalars, when supplied as base channels,
retain their scalar representation and channel order through this layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import InteractionEdge, InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .conditioned_layer import (
    ConditionedEquivariantLayerResult,
    conditioned_equivariant_layer_step,
)
from .conditioning import TernaryConditioning
from .edge import EquivariantEdgeInput, evaluate_equivariant_edge_input
from .features import NodeFeatures
from .message_operator import RadialMessageOperator
from .rank_two import (
    RankTwoFeatureVector,
    RankTwoTensor,
    ScalarVectorTensorFeatures,
)


def _coefficient(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean coefficient.")
    number = float(value)
    if not isfinite(number):
        raise ValueError(f"{name} must be finite.")
    return number


def _optional_index(value: int | None, name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be a nonnegative integer or None.")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative.")
    return value


@dataclass(frozen=True, slots=True)
class RankTwoMessageCoupling:
    """Declared O(3)-equivariant Cartesian rank-two message coefficients.

    For each tensor channel c of a source node i and directed edge i -> j:

        M_ij[c] = w(r_ij) * (
            tensor_scale * T_i[c]
            + scalar_dyad_scale * s_i[k] * (u_ij outer u_ij)
            + vector_dyad_scale * sym(v_i[l] outer u_ij)
        )

    The optional scalar/vector source channels are explicitly selected and
    broadcast to the registered tensor channels. Zero weights disable their
    respective terms. The direction is the polar unit edge displacement.
    """

    tensor_scale: float = 1.0
    scalar_dyad_scale: float = 0.0
    vector_dyad_scale: float = 0.0
    scalar_channel_index: int | None = None
    vector_channel_index: int | None = None

    def __post_init__(self) -> None:
        for name in ("tensor_scale", "scalar_dyad_scale", "vector_dyad_scale"):
            object.__setattr__(self, name, _coefficient(getattr(self, name), name))
        for name in ("scalar_channel_index", "vector_channel_index"):
            object.__setattr__(self, name, _optional_index(getattr(self, name), name))
        if self.scalar_dyad_scale != 0.0 and self.scalar_channel_index is None:
            raise ValueError("scalar_dyad_scale requires scalar_channel_index.")
        if self.vector_dyad_scale != 0.0 and self.vector_channel_index is None:
            raise ValueError("vector_dyad_scale requires vector_channel_index.")
        if (self.tensor_scale == 0.0 and self.scalar_dyad_scale == 0.0
                and self.vector_dyad_scale == 0.0):
            raise ValueError("at least one rank-two message term must be active.")

    def message(
        self,
        source_features: NodeFeatures,
        source_tensors: tuple[RankTwoTensor, ...],
        edge_input: EquivariantEdgeInput,
        radial_operator: RadialMessageOperator,
    ) -> tuple[RankTwoTensor, ...]:
        """Evaluate all tensor channels on a single directed geometric edge."""
        if not isinstance(source_features, NodeFeatures):
            raise TypeError("source_features must be NodeFeatures.")
        if (not isinstance(source_tensors, tuple) or not source_tensors
                or any(not isinstance(t, RankTwoTensor) for t in source_tensors)):
            raise TypeError("source_tensors must be a nonempty tuple of RankTwoTensor.")
        if not isinstance(edge_input, EquivariantEdgeInput):
            raise TypeError("edge_input must be EquivariantEdgeInput.")
        if not isinstance(radial_operator, RadialMessageOperator):
            raise TypeError("radial_operator must be RadialMessageOperator.")

        scalar = 0.0
        if self.scalar_dyad_scale != 0.0:
            assert self.scalar_channel_index is not None
            if self.scalar_channel_index >= source_features.scalar_channel_count:
                raise ValueError("selected scalar channel is outside the source features.")
            scalar = source_features.scalars[self.scalar_channel_index]

        vector = (0.0, 0.0, 0.0)
        if self.vector_dyad_scale != 0.0:
            assert self.vector_channel_index is not None
            if self.vector_channel_index >= source_features.vector_channel_count:
                raise ValueError("selected vector channel is outside the source features.")
            vector = source_features.vectors[self.vector_channel_index]

        u = edge_input.direction
        weight = radial_operator.radial_weight(edge_input.distance)
        return tuple(
            RankTwoTensor(tuple(
                tuple(weight * fsum((
                    self.tensor_scale * tensor.rows[i][j],
                    self.scalar_dyad_scale * scalar * u[i] * u[j],
                    0.5 * self.vector_dyad_scale * (
                        vector[i] * u[j] + u[i] * vector[j]
                    ),
                )) for j in range(3))
                for i in range(3)
            ))
            for tensor in source_tensors
        )


@dataclass(frozen=True, slots=True)
class RankTwoDirectedMessage:
    """One registered directed graph edge and its rank-two messages."""

    edge: InteractionEdge
    tensors: tuple[RankTwoTensor, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.edge, InteractionEdge):
            raise TypeError("edge must be InteractionEdge.")
        if (not isinstance(self.tensors, tuple) or not self.tensors
                or any(not isinstance(t, RankTwoTensor) for t in self.tensors)):
            raise TypeError("tensors must be a nonempty tuple of RankTwoTensor.")


@dataclass(frozen=True, slots=True)
class RankTwoConditionedLayerResult:
    """Full scalar/vector/tensor trace of one ternary-conditioned layer."""

    previous: ScalarVectorTensorFeatures
    conditioned: ScalarVectorTensorFeatures
    base_layer: ConditionedEquivariantLayerResult
    tensor_messages: tuple[RankTwoDirectedMessage, ...]
    tensor_aggregated: RankTwoFeatureVector
    current: ScalarVectorTensorFeatures
    receiver_message_counts: tuple[int, ...]

    def __post_init__(self) -> None:
        for name in ("previous", "conditioned", "current"):
            if not isinstance(getattr(self, name), ScalarVectorTensorFeatures):
                raise TypeError(f"{name} must be ScalarVectorTensorFeatures.")
        if not isinstance(self.base_layer, ConditionedEquivariantLayerResult):
            raise TypeError("base_layer must be ConditionedEquivariantLayerResult.")
        if not isinstance(self.tensor_aggregated, RankTwoFeatureVector):
            raise TypeError("tensor_aggregated must be RankTwoFeatureVector.")
        if (not isinstance(self.tensor_messages, tuple) or not self.tensor_messages
                or any(not isinstance(m, RankTwoDirectedMessage) for m in self.tensor_messages)):
            raise TypeError("tensor_messages must be a nonempty tuple of RankTwoDirectedMessage.")
        nodes = self.previous.node_count
        channels = self.previous.rank_two.tensor_channel_count
        if any(record.node_count != nodes for record in (
            self.conditioned, self.current, self.tensor_aggregated,
        )):
            raise ValueError("all rank-two layer results must align by node count.")
        if any(record.tensor_channel_count != channels for record in (
            self.conditioned.rank_two, self.current.rank_two, self.tensor_aggregated,
        )):
            raise ValueError("rank-two channel counts must be preserved.")
        if (self.base_layer.input_features != self.previous.base
                or self.base_layer.conditioned_features != self.conditioned.base
                or self.base_layer.current != self.current.base):
            raise ValueError("scalar/vector layer state correspondence differs.")
        if (len(self.tensor_messages) != len(self.base_layer.layer_result.messages)
                or len(self.receiver_message_counts) != nodes):
            raise ValueError("rank-two and scalar/vector message accounting differs.")
        if any(type(count) is not int or count < 0 for count in self.receiver_message_counts):
            raise ValueError("receiver message counts must be nonnegative integers.")
        if sum(self.receiver_message_counts) != len(self.tensor_messages):
            raise ValueError("receiver counts must cover every tensor message.")
        for rank_two_msg, base_msg in zip(
            self.tensor_messages, self.base_layer.layer_result.messages, strict=True,
        ):
            if (rank_two_msg.edge.source != base_msg.source
                    or rank_two_msg.edge.receiver != base_msg.receiver
                    or len(rank_two_msg.tensors) != channels):
                raise ValueError("rank-two and scalar/vector message edge ordering differs.")


def rank_two_conditioned_layer_step(
    configuration: AtomicConfiguration,
    graph: InteractionGraph,
    features: ScalarVectorTensorFeatures,
    radial_operator: RadialMessageOperator,
    execution: TernaryExecutionVector,
    conditioning: TernaryConditioning,
    coupling: RankTwoMessageCoupling | None = None,
) -> RankTwoConditionedLayerResult:
    """Run aligned scalar/vector and rank-two conditioned E(3) message passing.

    Source tensors are conditioned by executed retained -1/0/1 states. One
    immutable tensor message per edge preserves the same ordering as the
    existing scalar/vector layer. A zero-incoming-edge node retains its
    conditioned tensor channels through the additive residual update.
    """
    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError("configuration must be AtomicConfiguration.")
    if not isinstance(graph, InteractionGraph):
        raise TypeError("graph must be InteractionGraph.")
    if not isinstance(features, ScalarVectorTensorFeatures):
        raise TypeError("features must be ScalarVectorTensorFeatures.")
    if not isinstance(radial_operator, RadialMessageOperator):
        raise TypeError("radial_operator must be RadialMessageOperator.")
    if not isinstance(execution, TernaryExecutionVector):
        raise TypeError("execution must be TernaryExecutionVector.")
    if not isinstance(conditioning, TernaryConditioning):
        raise TypeError("conditioning must be TernaryConditioning.")
    if coupling is None:
        coupling = RankTwoMessageCoupling()
    if not isinstance(coupling, RankTwoMessageCoupling):
        raise TypeError("coupling must be RankTwoMessageCoupling.")
    if (graph.node_count != configuration.atom_count
            or features.node_count != graph.node_count
            or execution.node_count != graph.node_count):
        raise ValueError("atomic, graph, feature, and execution node counts differ.")
    if not graph.edges:
        raise ValueError("rank-two message passing requires at least one graph edge.")

    base_layer = conditioned_equivariant_layer_step(
        configuration, graph, features.base, execution, conditioning, radial_operator,
    )
    conditioned_rank_two = RankTwoFeatureVector(tuple(
        tuple(RankTwoTensor(tuple(tuple(
            conditioning.scale_for_state(node.retained_state) * tensor.rows[i][j]
            for j in range(3)) for i in range(3))) for tensor in channels)
        for node, channels in zip(execution.states, features.rank_two.nodes, strict=True)
    ))
    conditioned = ScalarVectorTensorFeatures(
        base=base_layer.conditioned_features,
        rank_two=conditioned_rank_two,
    )

    ordered_edges = sorted(
        graph.edges, key=lambda edge: (edge.receiver, edge.source, edge.image),
    )
    messages = tuple(
        RankTwoDirectedMessage(
            edge=edge,
            tensors=coupling.message(
                conditioned.base.nodes[edge.source],
                conditioned.rank_two.nodes[edge.source],
                evaluate_equivariant_edge_input(configuration, edge),
                radial_operator,
            ),
        )
        for edge in ordered_edges
    )
    counts = tuple(sum(m.edge.receiver == node for m in messages)
                   for node in range(graph.node_count))
    channels = conditioned.rank_two.tensor_channel_count
    aggregated = RankTwoFeatureVector(tuple(
        tuple(RankTwoTensor(tuple(
            tuple(fsum(
                m.tensors[channel].rows[i][j] for m in messages
                if m.edge.receiver == receiver
            ) for j in range(3))
            for i in range(3)
        )) for channel in range(channels))
        for receiver in range(graph.node_count)
    ))
    updated = RankTwoFeatureVector(tuple(
        tuple(RankTwoTensor(tuple(
            tuple(fsum((old.rows[i][j], aggregate.rows[i][j]))
                  for j in range(3))
            for i in range(3)
        )) for old, aggregate in zip(source, added, strict=True))
        for source, added in zip(
            conditioned.rank_two.nodes, aggregated.nodes, strict=True,
        )
    ))
    return RankTwoConditionedLayerResult(
        previous=features,
        conditioned=conditioned,
        base_layer=base_layer,
        tensor_messages=messages,
        tensor_aggregated=aggregated,
        current=ScalarVectorTensorFeatures(
            base=base_layer.current, rank_two=updated,
        ),
        receiver_message_counts=counts,
    )
