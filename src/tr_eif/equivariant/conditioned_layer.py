"""Ternary-conditioned E(3)-equivariant layer execution for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .conditioning import TernaryConditioning, condition_feature_vector
from .features import NodeFeatureVector
from .layer import EquivariantLayerResult, equivariant_layer_step
from .message_operator import RadialMessageOperator


@dataclass(frozen=True, slots=True)
class ConditionedEquivariantLayerResult:
    """Result of one ternary-conditioned equivariant layer execution."""

    input_features: NodeFeatureVector
    conditioned_features: NodeFeatureVector
    layer_result: EquivariantLayerResult

    def __post_init__(self) -> None:
        if not isinstance(self.input_features, NodeFeatureVector):
            raise TypeError(
                "input_features must be a NodeFeatureVector instance."
            )

        if not isinstance(self.conditioned_features, NodeFeatureVector):
            raise TypeError(
                "conditioned_features must be a NodeFeatureVector instance."
            )

        if not isinstance(self.layer_result, EquivariantLayerResult):
            raise TypeError(
                "layer_result must be an EquivariantLayerResult instance."
            )

        node_count = self.input_features.node_count

        if self.conditioned_features.node_count != node_count:
            raise ValueError(
                "conditioned feature node count must match input node count."
            )

        if self.layer_result.previous != self.conditioned_features:
            raise ValueError(
                "layer_result.previous must equal conditioned_features."
            )

    @property
    def current(self) -> NodeFeatureVector:
        """Return the current feature state after conditioned execution."""

        return self.layer_result.current


def conditioned_equivariant_layer_step(
    configuration: AtomicConfiguration,
    graph: InteractionGraph,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
    conditioning: TernaryConditioning,
    operator: RadialMessageOperator,
) -> ConditionedEquivariantLayerResult:
    """Execute one retained-state-conditioned equivariant layer."""

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

    if not isinstance(execution, TernaryExecutionVector):
        raise TypeError(
            "execution must be a TernaryExecutionVector instance."
        )

    if not isinstance(conditioning, TernaryConditioning):
        raise TypeError(
            "conditioning must be a TernaryConditioning instance."
        )

    if not isinstance(operator, RadialMessageOperator):
        raise TypeError(
            "operator must be a RadialMessageOperator instance."
        )

    if features.node_count != execution.node_count:
        raise ValueError(
            "feature and ternary execution node counts must match."
        )

    conditioned = condition_feature_vector(
        features,
        execution,
        conditioning,
    )

    layer_result = equivariant_layer_step(
        configuration,
        graph,
        conditioned,
        operator,
    )

    return ConditionedEquivariantLayerResult(
        input_features=features,
        conditioned_features=conditioned,
        layer_result=layer_result,
    )
