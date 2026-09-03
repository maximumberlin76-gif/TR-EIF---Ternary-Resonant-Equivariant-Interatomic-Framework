"""Relative Cartesian geometry operations for TR-EIF."""

from __future__ import annotations

from math import isfinite, sqrt

from tr_eif.configuration import Vector3


def _validate_vector3(value: Vector3, *, field_name: str) -> None:
    if len(value) != 3:
        raise ValueError(f"{field_name} must contain exactly three components.")

    if not all(isfinite(component) for component in value):
        raise ValueError(f"{field_name} must contain only finite values.")


def displacement(source: Vector3, target: Vector3) -> Vector3:
    """Return the Cartesian displacement from source to target."""

    _validate_vector3(source, field_name="source")
    _validate_vector3(target, field_name="target")

    return (
        target[0] - source[0],
        target[1] - source[1],
        target[2] - source[2],
    )


def squared_distance(source: Vector3, target: Vector3) -> float:
    """Return the squared Euclidean distance between two Cartesian positions."""

    delta = displacement(source, target)

    return (
        delta[0] * delta[0]
        + delta[1] * delta[1]
        + delta[2] * delta[2]
    )


def distance(source: Vector3, target: Vector3) -> float:
    """Return the Euclidean distance between two Cartesian positions."""

    return sqrt(squared_distance(source, target))


def unit_direction(source: Vector3, target: Vector3) -> Vector3:
    """Return the unit vector directed from source to target."""

    delta = displacement(source, target)
    norm_squared = (
        delta[0] * delta[0]
        + delta[1] * delta[1]
        + delta[2] * delta[2]
    )

    if norm_squared == 0.0:
        raise ValueError(
            "unit_direction is undefined for coincident Cartesian positions."
        )

    norm = sqrt(norm_squared)

    return (
        delta[0] / norm,
        delta[1] / norm,
        delta[2] / norm,
    )
