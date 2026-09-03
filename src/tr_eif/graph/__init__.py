"""Interaction-graph structures and operations for TR-EIF."""

from .builder import build_cutoff_graph
from .geometry import EdgeGeometry, evaluate_edge_geometry
from .interaction import ImageIndex, InteractionEdge, InteractionGraph

__all__ = [
    "EdgeGeometry",
    "ImageIndex",
    "InteractionEdge",
    "InteractionGraph",
    "build_cutoff_graph",
    "evaluate_edge_geometry",
]
