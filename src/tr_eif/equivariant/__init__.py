"""E(3)-equivariant feature representations and operations for TR-EIF."""

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
from .transform import E3Transformation, Matrix3x3

__all__ = [
    "E3Transformation",
    "EquivariantEdgeInput",
    "Matrix3x3",
    "NodeFeatures",
    "NodeFeatureVector",
    "ScalarFeatures",
    "VectorFeatures",
    "edge_input_from_geometry",
    "evaluate_equivariant_edge_input",
]
