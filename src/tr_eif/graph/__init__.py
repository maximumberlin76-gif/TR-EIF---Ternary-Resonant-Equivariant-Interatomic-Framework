"""Interaction-graph structures and operations for TR-EIF."""

from .builder import build_cutoff_graph
from .interaction import ImageIndex, InteractionEdge, InteractionGraph

__all__ = [
    "ImageIndex",
    "InteractionEdge",
    "InteractionGraph",
    "build_cutoff_graph",
]
