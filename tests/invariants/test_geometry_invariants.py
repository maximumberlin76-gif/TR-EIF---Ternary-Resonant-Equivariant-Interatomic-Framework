"""Qualification tests for TR-EIF Cartesian and periodic geometry invariants."""

import pytest

from tr_eif.geometry import (
    cartesian_to_fractional,
    displacement,
    distance,
    fractional_to_cartesian,
    minimum_image,
    minimum_image_displacement,
    periodic_image_displacement,
    squared_distance,
    unit_direction,
)


def _orthogonal_cell():
    return (
        (4.0, 0.0, 0.0),
        (0.0, 6.0, 0.0),
        (0.0, 0.0, 8.0),
    )


def test_cartesian_displacement_is_antisymmetric() -> None:
    """Reversing source and target must negate Cartesian displacement."""

    source = (1.0, -2.0, 3.0)
    target = (4.0, 2.0, -1.0)

    forward = displacement(source, target)
    reverse = displacement(target, source)

    assert forward == pytest.approx(
        (
            3.0,
            4.0,
            -4.0,
        )
    )

    assert reverse == pytest.approx(
        tuple(-component for component in forward)
    )


def test_distance_contract_matches_displacement_norm() -> None:
    """Distance and squared distance must match the displacement norm."""

    source = (1.0, 2.0, 3.0)
    target = (4.0, 6.0, 3.0)

    assert displacement(source, target) == pytest.approx(
        (
            3.0,
            4.0,
            0.0,
        )
    )
    assert squared_distance(source, target) == pytest.approx(25.0)
    assert distance(source, target) == pytest.approx(5.0)


def test_unit_direction_has_expected_orientation_and_norm() -> None:
    """Unit direction must point from source to target with unit norm."""

    source = (0.0, 0.0, 0.0)
    target = (3.0, 4.0, 0.0)

    direction = unit_direction(source, target)

    assert direction == pytest.approx(
        (
            0.6,
            0.8,
            0.0,
        )
    )

    norm_squared = sum(
        component * component
        for component in direction
    )

    assert norm_squared == pytest.approx(1.0)


def test_unit_direction_rejects_coincident_positions() -> None:
    """A direction is undefined for coincident Cartesian positions."""

    position = (1.0, 2.0, 3.0)

    with pytest.raises(
        ValueError,
        match="undefined for coincident Cartesian positions",
    ):
        unit_direction(position, position)


def test_fractional_cartesian_round_trip() -> None:
    """Fractional and Cartesian conversions must form a round trip."""

    cell = (
        (4.0, 0.0, 0.0),
        (1.0, 5.0, 0.0),
        (0.5, 1.0, 6.0),
    )

    fractional = (
        0.25,
        -0.40,
        1.20,
    )

    cartesian = fractional_to_cartesian(
        fractional,
        cell,
    )

    recovered = cartesian_to_fractional(
        cartesian,
        cell,
    )

    assert recovered == pytest.approx(fractional)


def test_explicit_periodic_image_displacement_uses_requested_image() -> None:
    """Explicit image displacement must apply the supplied lattice image."""

    cell = _orthogonal_cell()

    source = (0.5, 1.0, 2.0)
    target = (3.5, 5.0, 7.0)

    result = periodic_image_displacement(
        source,
        target,
        cell,
        image=(-1, 0, -1),
    )

    assert result == pytest.approx(
        (
            -1.0,
            4.0,
            -3.0,
        )
    )


def test_minimum_image_wraps_enabled_axes_only() -> None:
    """Minimum-image wrapping must leave nonperiodic axes unwrapped."""

    cell = _orthogonal_cell()

    source = (0.2, 0.5, 0.4)
    target = (3.8, 5.5, 7.6)

    wrapped, image = minimum_image(
        source,
        target,
        cell,
        periodic=(
            True,
            False,
            True,
        ),
    )

    assert image == (
        -1,
        0,
        -1,
    )

    assert wrapped == pytest.approx(
        (
            -0.4,
            5.0,
            -0.8,
        )
    )


def test_minimum_image_displacement_matches_full_result() -> None:
    """Displacement-only API must match the displacement from minimum_image."""

    cell = _orthogonal_cell()

    source = (0.2, 0.5, 0.4)
    target = (3.8, 5.5, 7.6)
    periodic = (
        True,
        False,
        True,
    )

    wrapped, _ = minimum_image(
        source,
        target,
        cell,
        periodic,
    )

    displacement_only = minimum_image_displacement(
        source,
        target,
        cell,
        periodic,
    )

    assert displacement_only == pytest.approx(wrapped)


def test_minimum_image_matches_explicit_recorded_image() -> None:
    """Returned image index must reproduce the wrapped displacement."""

    cell = _orthogonal_cell()

    source = (0.2, 0.5, 0.4)
    target = (3.8, 5.5, 7.6)
    periodic = (
        True,
        False,
        True,
    )

    wrapped, image = minimum_image(
        source,
        target,
        cell,
        periodic,
    )

    explicit = periodic_image_displacement(
        source,
        target,
        cell,
        image,
    )

    assert explicit == pytest.approx(wrapped)


def test_minimum_image_is_antisymmetric_away_from_tie_boundary() -> None:
    """Reversing a non-tie pair must negate displacement and image."""

    cell = _orthogonal_cell()

    source = (0.2, 0.3, 0.4)
    target = (3.7, 5.4, 7.2)
    periodic = (
        True,
        True,
        True,
    )

    forward_displacement, forward_image = minimum_image(
        source,
        target,
        cell,
        periodic,
    )

    reverse_displacement, reverse_image = minimum_image(
        target,
        source,
        cell,
        periodic,
    )

    assert reverse_displacement == pytest.approx(
        tuple(
            -component
            for component in forward_displacement
        )
    )

    assert reverse_image == tuple(
        -component
        for component in forward_image
    )


def test_nonperiodic_minimum_image_matches_cartesian_displacement() -> None:
    """With all axes nonperiodic, minimum-image mapping must not wrap."""

    cell = _orthogonal_cell()

    source = (0.2, 0.5, 0.4)
    target = (3.8, 5.5, 7.6)

    wrapped, image = minimum_image(
        source,
        target,
        cell,
        periodic=(
            False,
            False,
            False,
        ),
    )

    assert image == (
        0,
        0,
        0,
    )

    assert wrapped == pytest.approx(
        displacement(source, target)
    )
