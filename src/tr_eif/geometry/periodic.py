"""Periodic-cell geometry operations for TR-EIF."""

from __future__ import annotations

from math import floor, isfinite
from typing import TypeAlias

from tr_eif.configuration import Cell3x3, PeriodicAxes, Vector3

ImageIndex: TypeAlias = tuple[int, int, int]


def _validate_vector3(value: Vector3, *, field_name: str) -> None:
    if len(value) != 3:
        raise ValueError(f"{field_name} must contain exactly three components.")

    if not all(isfinite(component) for component in value):
        raise ValueError(f"{field_name} must contain only finite values.")


def _validate_cell(cell: Cell3x3) -> None:
    if len(cell) != 3:
        raise ValueError("cell must contain exactly three lattice vectors.")

    for index, vector in enumerate(cell):
        _validate_vector3(vector, field_name=f"cell[{index}]")

    if _cell_determinant(cell) == 0.0:
        raise ValueError("cell lattice vectors must define a nonzero volume.")


def _validate_periodic(periodic: PeriodicAxes) -> None:
    if len(periodic) != 3:
        raise ValueError("periodic must contain exactly three boolean flags.")

    if not all(isinstance(flag, bool) for flag in periodic):
        raise TypeError("periodic must contain only boolean flags.")


def _validate_image_index(image: ImageIndex) -> None:
    if len(image) != 3:
        raise ValueError("image must contain exactly three integer indices.")

    if not all(
        isinstance(component, int) and not isinstance(component, bool)
        for component in image
    ):
        raise TypeError("image must contain only integer indices.")


def _cell_determinant(cell: Cell3x3) -> float:
    a, b, c = cell

    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def _inverse_cell(cell: Cell3x3) -> Cell3x3:
    determinant = _cell_determinant(cell)

    if determinant == 0.0:
        raise ValueError("cell lattice vectors must define a nonzero volume.")

    a, b, c = cell

    inverse_rows = (
        (
            (b[1] * c[2] - b[2] * c[1]) / determinant,
            (a[2] * c[1] - a[1] * c[2]) / determinant,
            (a[1] * b[2] - a[2] * b[1]) / determinant,
        ),
        (
            (b[2] * c[0] - b[0] * c[2]) / determinant,
            (a[0] * c[2] - a[2] * c[0]) / determinant,
            (a[2] * b[0] - a[0] * b[2]) / determinant,
        ),
        (
            (b[0] * c[1] - b[1] * c[0]) / determinant,
            (a[1] * c[0] - a[0] * c[1]) / determinant,
            (a[0] * b[1] - a[1] * b[0]) / determinant,
        ),
    )

    return (
        (
            inverse_rows[0][0],
            inverse_rows[1][0],
            inverse_rows[2][0],
        ),
        (
            inverse_rows[0][1],
            inverse_rows[1][1],
            inverse_rows[2][1],
        ),
        (
            inverse_rows[0][2],
            inverse_rows[1][2],
            inverse_rows[2][2],
        ),
    )


def fractional_to_cartesian(
    fractional: Vector3,
    cell: Cell3x3,
) -> Vector3:
    """Convert fractional coordinates to Cartesian coordinates."""

    _validate_vector3(fractional, field_name="fractional")
    _validate_cell(cell)

    a, b, c = cell

    return (
        fractional[0] * a[0] + fractional[1] * b[0] + fractional[2] * c[0],
        fractional[0] * a[1] + fractional[1] * b[1] + fractional[2] * c[1],
        fractional[0] * a[2] + fractional[1] * b[2] + fractional[2] * c[2],
    )


def cartesian_to_fractional(
    cartesian: Vector3,
    cell: Cell3x3,
) -> Vector3:
    """Convert Cartesian coordinates to fractional coordinates."""

    _validate_vector3(cartesian, field_name="cartesian")
    _validate_cell(cell)

    inverse = _inverse_cell(cell)
    a_star, b_star, c_star = inverse

    return (
        cartesian[0] * a_star[0]
        + cartesian[1] * a_star[1]
        + cartesian[2] * a_star[2],
        cartesian[0] * b_star[0]
        + cartesian[1] * b_star[1]
        + cartesian[2] * b_star[2],
        cartesian[0] * c_star[0]
        + cartesian[1] * c_star[1]
        + cartesian[2] * c_star[2],
    )


def periodic_image_displacement(
    source: Vector3,
    target: Vector3,
    cell: Cell3x3,
    image: ImageIndex,
) -> Vector3:
    """Return source-to-target displacement for an explicit periodic image."""

    _validate_vector3(source, field_name="source")
    _validate_vector3(target, field_name="target")
    _validate_cell(cell)
    _validate_image_index(image)

    image_translation = fractional_to_cartesian(
        (float(image[0]), float(image[1]), float(image[2])),
        cell,
    )

    return (
        target[0] + image_translation[0] - source[0],
        target[1] + image_translation[1] - source[1],
        target[2] + image_translation[2] - source[2],
    )


def minimum_image(
    source: Vector3,
    target: Vector3,
    cell: Cell3x3,
    periodic: PeriodicAxes,
) -> tuple[Vector3, ImageIndex]:
    """Return fractional-wrapped displacement and its periodic image index."""

    _validate_vector3(source, field_name="source")
    _validate_vector3(target, field_name="target")
    _validate_cell(cell)
    _validate_periodic(periodic)

    cartesian_delta = (
        target[0] - source[0],
        target[1] - source[1],
        target[2] - source[2],
    )

    fractional_delta = cartesian_to_fractional(cartesian_delta, cell)

    image_components: list[int] = []
    wrapped_components: list[float] = []

    for component, is_periodic in zip(
        fractional_delta,
        periodic,
        strict=True,
    ):
        if is_periodic:
            image_component = -floor(component + 0.5)
        else:
            image_component = 0

        image_components.append(image_component)
        wrapped_components.append(component + image_component)

    image: ImageIndex = (
        image_components[0],
        image_components[1],
        image_components[2],
    )

    wrapped_fractional: Vector3 = (
        wrapped_components[0],
        wrapped_components[1],
        wrapped_components[2],
    )

    return fractional_to_cartesian(wrapped_fractional, cell), image


def minimum_image_displacement(
    source: Vector3,
    target: Vector3,
    cell: Cell3x3,
    periodic: PeriodicAxes,
) -> Vector3:
    """Return a fractional-coordinate wrapped source-to-target displacement."""

    wrapped_displacement, _ = minimum_image(
        source,
        target,
        cell,
        periodic,
    )

    return wrapped_displacement
