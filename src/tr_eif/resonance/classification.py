"""Resonance-window classification for TR-EIF."""

from __future__ import annotations

from enum import Enum

from .window import ResonanceCoordinate, ResonanceWindow


class ResonanceRegion(Enum):
    """Geometric classification relative to a resonance window."""

    OUTSIDE = "outside"
    BOUNDARY = "boundary"
    INSIDE = "inside"


def classify_resonance_region(
    coordinate: ResonanceCoordinate,
    window: ResonanceWindow,
) -> ResonanceRegion:
    """Classify a coordinate relative to a finite resonance window."""

    if not isinstance(window, ResonanceWindow):
        raise TypeError("window must be a ResonanceWindow instance.")

    window.space.validate_coordinate(coordinate)

    if window.is_boundary(coordinate):
        return ResonanceRegion.BOUNDARY

    if window.is_interior(coordinate):
        return ResonanceRegion.INSIDE

    return ResonanceRegion.OUTSIDE
