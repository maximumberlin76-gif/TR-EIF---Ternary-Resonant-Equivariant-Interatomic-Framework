"""Invariant tests for TR-EIF multiscale geometric coarse-graining."""

import pytest

from tr_eif.multiscale.geometry import mass_weighted_centroids
from tr_eif.multiscale.partition import MultiscalePartition


def test_identity_partition_preserves_positions() -> None:
    """Identity partition must preserve each fine-scale position."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    positions = (
        (1.0, 2.0, 3.0),
        (-4.0, 5.0, 6.0),
        (7.5, -8.0, 9.25),
    )

    coarse = mass_weighted_centroids(
        positions=positions,
        masses=(
            1.0,
            2.0,
            3.0,
        ),
        partition=partition,
    )

    assert coarse == positions


def test_equal_mass_centroid_matches_arithmetic_mean() -> None:
    """Equal masses must reduce a group to its Cartesian arithmetic mean."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_centroids(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 4.0, 6.0),
        ),
        masses=(
            1.0,
            1.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (1.0, 2.0, 3.0),
    )


def test_unequal_mass_centroid_uses_mass_weighting() -> None:
    """Unequal masses must shift the centroid according to mass."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_centroids(
        positions=(
            (0.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            3.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (3.0, 0.0, 0.0),
    )

    assert coarse != (
        (2.0, 0.0, 0.0),
    )


def test_many_to_one_centroids_follow_partition_groups() -> None:
    """Each coarse centroid must use only its assigned fine members."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            1,
            2,
        )
    )

    coarse = mass_weighted_centroids(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (0.0, 3.0, 0.0),
            (0.0, 6.0, 0.0),
            (0.0, 9.0, 0.0),
            (0.0, 0.0, 12.0),
        ),
        masses=(
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            2.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (1.0, 0.0, 0.0),
        (0.0, 6.0, 0.0),
        (0.0, 0.0, 12.0),
    )


def test_interleaved_partition_follows_explicit_assignments() -> None:
    """Centroid membership must not depend on fine-index adjacency."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    coarse = mass_weighted_centroids(
        positions=(
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (14.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            1.0,
            1.0,
            1.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (2.0, 0.0, 0.0),
        (12.0, 0.0, 0.0),
    )


def test_centroid_matches_explicit_mass_weighted_formula() -> None:
    """Centroid components must equal sum(m_i r_i) divided by sum(m_i)."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
        )
    )

    positions = (
        (1.0, 2.0, 3.0),
        (4.0, -1.0, 2.0),
        (-2.0, 5.0, 7.0),
    )

    masses = (
        2.0,
        3.0,
        5.0,
    )

    coarse = mass_weighted_centroids(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    total_mass = sum(masses)

    expected = (
        sum(
            mass * position[0]
            for mass, position in zip(masses, positions)
        )
        / total_mass,
        sum(
            mass * position[1]
            for mass, position in zip(masses, positions)
        )
        / total_mass,
        sum(
            mass * position[2]
            for mass, position in zip(masses, positions)
        )
        / total_mass,
    )

    for actual_component, expected_component in zip(
        coarse[0],
        expected,
    ):
        assert actual_component == pytest.approx(
            expected_component
        )


def test_centroid_is_invariant_under_uniform_mass_scaling() -> None:
    """Uniform positive scaling of all masses must preserve centroids."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    positions = (
        (0.0, 0.0, 0.0),
        (6.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
        (0.0, 8.0, 0.0),
    )

    masses = (
        1.0,
        2.0,
        3.0,
        1.0,
    )

    scaled_masses = tuple(
        7.0 * mass
        for mass in masses
    )

    reference = mass_weighted_centroids(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    scaled = mass_weighted_centroids(
        positions=positions,
        masses=scaled_masses,
        partition=partition,
    )

    for reference_position, scaled_position in zip(
        reference,
        scaled,
    ):
        for reference_component, scaled_component in zip(
            reference_position,
            scaled_position,
        ):
            assert scaled_component == pytest.approx(
                reference_component
            )


def test_centroid_is_translation_covariant() -> None:
    """Uniform Cartesian translation must translate every coarse centroid."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    positions = (
        (0.0, 1.0, 2.0),
        (2.0, 3.0, 4.0),
        (-1.0, 5.0, 7.0),
        (3.0, 9.0, 11.0),
    )

    masses = (
        1.0,
        3.0,
        2.0,
        5.0,
    )

    translation = (
        10.0,
        -4.0,
        2.5,
    )

    translated_positions = tuple(
        (
            position[0] + translation[0],
            position[1] + translation[1],
            position[2] + translation[2],
        )
        for position in positions
    )

    reference = mass_weighted_centroids(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    translated = mass_weighted_centroids(
        positions=translated_positions,
        masses=masses,
        partition=partition,
    )

    for reference_position, translated_position in zip(
        reference,
        translated,
    ):
        expected = (
            reference_position[0] + translation[0],
            reference_position[1] + translation[1],
            reference_position[2] + translation[2],
        )

        for actual_component, expected_component in zip(
            translated_position,
            expected,
        ):
            assert actual_component == pytest.approx(
                expected_component
            )


def test_single_member_group_preserves_member_position() -> None:
    """A one-member coarse entity must retain its fine position."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    positions = (
        (0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (7.0, -3.0, 5.0),
    )

    coarse = mass_weighted_centroids(
        positions=positions,
        masses=(
            1.0,
            1.0,
            9.0,
        ),
        partition=partition,
    )

    assert coarse[1] == positions[2]


def test_integer_positions_and_masses_produce_float_coordinates() -> None:
    """Accepted integer inputs must produce canonical float coordinates."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_centroids(
        positions=(
            (0, 2, 4),
            (2, 4, 6),
        ),
        masses=(
            1,
            1,
        ),
        partition=partition,
    )

    assert coarse == (
        (1.0, 3.0, 5.0),
    )

    assert all(
        isinstance(component, float)
        for component in coarse[0]
    )


def test_centroid_requires_partition_instance() -> None:
    """Centroid reduction requires an explicit MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
            ),
            partition=(0,),
        )


def test_positions_must_be_tuple() -> None:
    """The canonical fine-position container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="positions must be a tuple",
    ):
        mass_weighted_centroids(
            positions=[
                (0.0, 0.0, 0.0),
            ],
            masses=(
                1.0,
            ),
            partition=partition,
        )


def test_positions_must_not_be_empty() -> None:
    """Centroid reduction requires a nonempty position field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="positions must not be empty",
    ):
        mass_weighted_centroids(
            positions=(),
            masses=(
                1.0,
            ),
            partition=partition,
        )


def test_position_count_must_match_partition() -> None:
    """One position is required for every fine-scale entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one vector per fine-scale entity",
    ):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


def test_position_vector_must_be_tuple() -> None:
    """Each Cartesian position must use the canonical tuple representation."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"positions\[1\] must be a tuple",
    ):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
                [1.0, 2.0, 3.0],
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_position",
    (
        (),
        (1.0,),
        (1.0, 2.0),
        (1.0, 2.0, 3.0, 4.0),
    ),
)
def test_position_requires_exactly_three_components(
    invalid_position,
) -> None:
    """Every Cartesian position must contain exactly three components."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="must contain exactly three components",
    ):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
                invalid_position,
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_component",
    (
        True,
        False,
        "1.0",
        None,
    ),
)
def test_position_components_must_be_real_numbers(
    invalid_component,
) -> None:
    """Cartesian components must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"positions\[0\]\[1\] must be a real number",
    ):
        mass_weighted_centroids(
            positions=(
                (
                    0.0,
                    invalid_component,
                    0.0,
                ),
            ),
            masses=(
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_component",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_position_components_must_be_finite(
    invalid_component: float,
) -> None:
    """Cartesian components must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"positions\[0\]\[1\] must be finite",
    ):
        mass_weighted_centroids(
            positions=(
                (
                    0.0,
                    invalid_component,
                    0.0,
                ),
            ),
            masses=(
                1.0,
            ),
            partition=partition,
        )


def test_mass_count_must_match_position_count() -> None:
    """Mass and position fields must describe the same fine entities."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="one scalar per fine-scale entity",
    ):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
                (2.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_centroid_inherits_mass_domain_validation(
    invalid_mass: float,
) -> None:
    """Centroid construction must preserve the strict mass domain."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(ValueError):
        mass_weighted_centroids(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )
