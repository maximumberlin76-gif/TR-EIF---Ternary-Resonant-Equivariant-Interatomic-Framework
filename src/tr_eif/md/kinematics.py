"""Cartesian kinematic operations for TR-EIF molecular dynamics."""

from __future__ import annotations

from math import isfinite

from tr_eif.configuration import Vector3


def _validate_time_step(time_step: float) -> float:
    """Validate and normalize a positive molecular-dynamics time step."""

    if not isinstance(time_step, (int, float)) or isinstance(
        time_step,
        bool,
    ):
        raise TypeError(
            "time_step must be a real number."
        )

    if not isfinite(time_step):
        raise ValueError(
            "time_step must be finite."
        )

    normalized = float(time_step)

    if normalized <= 0.0:
        raise ValueError(
            "time_step must be greater than zero."
        )

    return normalized


def advance_velocity(
    velocity: Vector3,
    acceleration: Vector3,
    time_step: float,
) -> Vector3:
    """Advance one Cartesian velocity by constant acceleration."""

    dt = _validate_time_step(time_step)

    return (
        velocity[0] + acceleration[0] * dt,
        velocity[1] + acceleration[1] * dt,
        velocity[2] + acceleration[2] * dt,
    )


def advance_position(
    position: Vector3,
    velocity: Vector3,
    time_step: float,
) -> Vector3:
    """Advance one Cartesian position by constant velocity."""

    dt = _validate_time_step(time_step)

    return (
        position[0] + velocity[0] * dt,
        position[1] + velocity[1] * dt,
        position[2] + velocity[2] * dt,
    )
