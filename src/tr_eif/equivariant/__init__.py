"""E(3)-equivariant feature representations and operations for TR-EIF."""

from .aggregation import aggregate_messages
from .conditioning import (
    TernaryConditioning,
    condition_feature_vector,
    condition_node_features,
)
from .edge import (
    EquivariantEdgeInput,
    edge_input_from_geometry,
    evaluate_equivariant_edge_input,
)
from .features import (
    NodeFeatures,
    NodeFeatureVector,
    ScalarFeatures,
    VectorFeatures,
)
from .layer import EquivariantLayerResult, equivariant_layer_step
from .message import EquivariantMessage
from .message_operator import RadialMessageOperator
from .message_passing import (
    MessagePassingResult,
    message_passing_step,
)
from .transform import E3Transformation, Matrix3x3
from .update import (
    update_feature_vector,
    update_node_features,
)

__all__ = [
    "E3Transformation",
    "EquivariantEdgeInput",
    "EquivariantLayerResult",
    "EquivariantMessage",
    "Matrix3x3",
    "MessagePassingResult",
    "NodeFeatures",
    "NodeFeatureVector",
    "RadialMessageOperator",
    "ScalarFeatures",
    "TernaryConditioning",
    "VectorFeatures",
    "aggregate_messages",
    "condition_feature_vector",
    "condition_node_features",
    "edge_input_from_geometry",
    "equivariant_layer_step",
    "evaluate_equivariant_edge_input",
    "message_passing_step",
    "update_feature_vector",
    "update_node_features",
]
