"""Velocity-Verlet integration primitives for TR-EIF molecular dynamics."""

from __future__ import annotations

from math import isfinite

from tr_eif.configuration import Vector3

from .dynamics import AtomicAccelerations
from .state import AtomicVelocities


def _validate_time_step(time_step: float) -> float:
    """Validate and normalize a positive integration time step."""

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


def velocity_verlet_position(
    position: Vector3,
    velocity: Vector3,
    acceleration: Vector3,
    time_step: float,
) -> Vector3:
    """Advance one Cartesian position by the velocity-Verlet drift."""

    dt = _validate_time_step(time_step)
    half_dt_squared = 0.5 * dt * dt

    return (
        position[0]
        + velocity[0] * dt
        + acceleration[0] * half_dt_squared,
        position[1]
        + velocity[1] * dt
        + acceleration[1] * half_dt_squared,
        position[2]
        + velocity[2] * dt
        + acceleration[2] * half_dt_squared,
    )


def velocity_verlet_velocity(
    velocity: Vector3,
    acceleration_before: Vector3,
    acceleration_after: Vector3,
    time_step: float,
) -> Vector3:
    """Complete one Cartesian velocity-Verlet velocity update."""

    dt = _validate_time_step(time_step)
    half_dt = 0.5 * dt

    return (
        velocity[0]
        + (
            acceleration_before[0]
            + acceleration_after[0]
        )
        * half_dt,
        velocity[1]
        + (
            acceleration_before[1]
            + acceleration_after[1]
        )
        * half_dt,
        velocity[2]
        + (
            acceleration_before[2]
            + acceleration_after[2]
        )
        * half_dt,
    )


def velocity_verlet_positions(
    positions: tuple[Vector3, ...],
    velocities: AtomicVelocities,
    accelerations: AtomicAccelerations,
    time_step: float,
) -> tuple[Vector3, ...]:
    """Advance all Cartesian positions by one Verlet drift."""

    if not isinstance(positions, tuple):
        raise TypeError(
            "positions must be a tuple."
        )

    if not isinstance(velocities, tuple):
        raise TypeError(
            "velocities must be a tuple."
        )

    if not isinstance(accelerations, tuple):
        raise TypeError(
            "accelerations must be a tuple."
        )

    if len(velocities) != len(positions):
        raise ValueError(
            "velocities must contain one vector per position."
        )

    if len(accelerations) != len(positions):
        raise ValueError(
            "accelerations must contain one vector per position."
        )

    dt = _validate_time_step(time_step)

    return tuple(
        velocity_verlet_position(
            position=position,
            velocity=velocities[index],
            acceleration=accelerations[index],
            time_step=dt,
        )
        for index, position in enumerate(positions)
    )


def velocity_verlet_velocities(
    velocities: AtomicVelocities,
    accelerations_before: AtomicAccelerations,
    accelerations_after: AtomicAccelerations,
    time_step: float,
) -> AtomicVelocities:
    """Complete all Cartesian velocity updates after force reevaluation."""

    if not isinstance(velocities, tuple):
        raise TypeError(
            "velocities must be a tuple."
        )

    if not isinstance(accelerations_before, tuple):
        raise TypeError(
            "accelerations_before must be a tuple."
        )

    if not isinstance(accelerations_after, tuple):
        raise TypeError(
            "accelerations_after must be a tuple."
        )

    node_count = len(velocities)

    if len(accelerations_before) != node_count:
        raise ValueError(
            "accelerations_before must contain "
            "one vector per velocity."
        )

    if len(accelerations_after) != node_count:
        raise ValueError(
            "accelerations_after must contain "
            "one vector per velocity."
        )

    dt = _validate_time_step(time_step)

    return tuple(
        velocity_verlet_velocity(
            velocity=velocity,
            acceleration_before=accelerations_before[index],
            acceleration_after=accelerations_after[index],
            time_step=dt,
        )
        for index, velocity in enumerate(velocities)
    )
