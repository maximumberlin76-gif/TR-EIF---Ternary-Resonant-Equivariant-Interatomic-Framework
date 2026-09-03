"""Invariant tests for TR-EIF multiscale mass-weighted vector averaging."""

import pytest

from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.vector_average import (
    mass_weighted_vector_average,
)


def test_identity_partition_preserves_vectors() -> None:
    """Identity averaging must preserve every fine-scale vector."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    vectors = (
        (1.0, 2.0, 3.0),
        (-4.0, 5.0, -6.0),
        (7.5, -8.0, 9.25),
    )

    coarse = mass_weighted_vector_average(
        vectors=vectors,
        masses=(
            1.0,
            2.0,
            3.0,
        ),
        partition=partition,
    )

    assert coarse == vectors


def test_equal_masses_produce_arithmetic_vector_average() -> None:
    """Equal masses must reduce to the arithmetic vector average."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (0.0, 2.0, 4.0),
            (4.0, 6.0, 8.0),
        ),
        masses=(
            1.0,
            1.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (2.0, 4.0, 6.0),
    )


def test_unequal_masses_use_mass_weighting() -> None:
    """Unequal masses must shift the average according to mass."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
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


def test_many_to_one_average_uses_partition_local_members() -> None:
    """Each coarse vector must use only its assigned fine members."""

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

    coarse = mass_weighted_vector_average(
        vectors=(
            (0.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 3.0, 0.0),
            (0.0, 6.0, 0.0),
            (0.0, 0.0, 9.0),
        ),
        masses=(
            1.0,
            3.0,
            1.0,
            1.0,
            1.0,
            2.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (3.0, 0.0, 0.0),
        (0.0, 3.0, 0.0),
        (0.0, 0.0, 9.0),
    )


def test_interleaved_partition_follows_explicit_assignments() -> None:
    """Averaging must follow partition membership rather than adjacency."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (6.0, 0.0, 0.0),
            (14.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            1.0,
            2.0,
            3.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (4.0, 0.0, 0.0),
        (13.0, 0.0, 0.0),
    )


def test_average_matches_explicit_mass_weighted_formula() -> None:
    """Each component must equal sum(m_i u_i) divided by sum(m_i)."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
        )
    )

    vectors = (
        (1.0, 2.0, 3.0),
        (4.0, -1.0, 2.0),
        (-2.0, 5.0, 7.0),
    )

    masses = (
        2.0,
        3.0,
        5.0,
    )

    coarse = mass_weighted_vector_average(
        vectors=vectors,
        masses=masses,
        partition=partition,
    )

    total_mass = sum(masses)

    expected = tuple(
        sum(
            mass * vector[component]
            for mass, vector in zip(
                masses,
                vectors,
            )
        )
        / total_mass
        for component in range(3)
    )

    for actual, reference in zip(
        coarse[0],
        expected,
    ):
        assert actual == pytest.approx(reference)


def test_uniform_mass_scaling_preserves_average() -> None:
    """Uniform positive scaling of all masses must preserve coarse vectors."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    vectors = (
        (0.0, 1.0, 2.0),
        (6.0, 3.0, 4.0),
        (-2.0, 5.0, 7.0),
        (4.0, 9.0, 11.0),
    )

    masses = (
        1.0,
        2.0,
        3.0,
        5.0,
    )

    scaled_masses = tuple(
        7.0 * mass
        for mass in masses
    )

    reference = mass_weighted_vector_average(
        vectors=vectors,
        masses=masses,
        partition=partition,
    )

    scaled = mass_weighted_vector_average(
        vectors=vectors,
        masses=scaled_masses,
        partition=partition,
    )

    for reference_vector, scaled_vector in zip(
        reference,
        scaled,
    ):
        for reference_component, scaled_component in zip(
            reference_vector,
            scaled_vector,
        ):
            assert scaled_component == pytest.approx(
                reference_component
            )


def test_constant_vector_field_is_preserved() -> None:
    """Mass-weighted averaging must preserve a constant vector field."""

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

    constant = (
        2.5,
        -3.0,
        7.0,
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            constant,
            constant,
            constant,
            constant,
            constant,
            constant,
        ),
        masses=(
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
        ),
        partition=partition,
    )

    assert coarse == (
        constant,
        constant,
        constant,
    )


def test_zero_vector_field_is_preserved() -> None:
    """A zero vector field must remain zero after averaging."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            2.0,
            3.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )


def test_signed_vector_components_are_allowed() -> None:
    """Mass weighting must preserve the signed Cartesian vector domain."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (-4.0, 2.0, -6.0),
            (2.0, -4.0, 3.0),
        ),
        masses=(
            1.0,
            1.0,
        ),
        partition=partition,
    )

    assert coarse == (
        (-1.0, -1.0, -1.5),
    )


def test_single_member_group_preserves_vector() -> None:
    """A one-member coarse entity must preserve its fine vector."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    vectors = (
        (1.0, 2.0, 3.0),
        (4.0, 5.0, 6.0),
        (-7.0, 8.0, -9.0),
    )

    coarse = mass_weighted_vector_average(
        vectors=vectors,
        masses=(
            1.0,
            2.0,
            10.0,
        ),
        partition=partition,
    )

    assert coarse[1] == vectors[2]


def test_integer_inputs_produce_float_output() -> None:
    """Accepted integer vectors and masses must normalize to float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (0, 2, 4),
            (2, 4, 6),
            (7, 8, 9),
        ),
        masses=(
            1,
            1,
            3,
        ),
        partition=partition,
    )

    assert coarse == (
        (1.0, 3.0, 5.0),
        (7.0, 8.0, 9.0),
    )

    assert all(
        isinstance(component, float)
        for vector in coarse
        for component in vector
    )


def test_output_count_matches_coarse_count() -> None:
    """The averaged field must contain one vector per coarse entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            2,
            1,
            2,
        )
    )

    coarse = mass_weighted_vector_average(
        vectors=(
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (3.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (5.0, 0.0, 0.0),
            (6.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ),
        partition=partition,
    )

    assert len(coarse) == partition.coarse_count


def test_average_requires_partition_instance() -> None:
    """Mass-weighted averaging requires an explicit MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
            ),
            masses=(
                1.0,
            ),
            partition=(0,),
        )


def test_vectors_must_be_tuple() -> None:
    """The canonical fine-vector container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="vectors must be a tuple",
    ):
        mass_weighted_vector_average(
            vectors=[
                (1.0, 2.0, 3.0),
            ],
            masses=(
                1.0,
            ),
            partition=partition,
        )


def test_vectors_must_not_be_empty() -> None:
    """Mass-weighted averaging requires a nonempty vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="vectors must not be empty",
    ):
        mass_weighted_vector_average(
            vectors=(),
            masses=(
                1.0,
            ),
            partition=partition,
        )


def test_vector_count_must_match_partition_fine_count() -> None:
    """One vector is required for every fine-scale entity."""

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
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
            ),
            masses=(
                1.0,
                1.0,
                1.0,
            ),
            partition=partition,
        )


def test_mass_count_must_match_partition_fine_count() -> None:
    """One mass is required for every fine-scale entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one scalar per fine-scale entity",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
                (7.0, 8.0, 9.0),
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


def test_vector_must_be_tuple() -> None:
    """Each fine vector must use the canonical tuple representation."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"vectors\[1\] must be a tuple",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                [4.0, 5.0, 6.0],
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_vector",
    (
        (),
        (1.0,),
        (1.0, 2.0),
        (1.0, 2.0, 3.0, 4.0),
    ),
)
def test_vector_requires_exactly_three_components(
    invalid_vector,
) -> None:
    """Every Cartesian vector must contain exactly three components."""

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
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                invalid_vector,
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
def test_vector_components_must_be_real_numbers(
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
        match=r"vectors\[0\]\[1\] must be a real number",
    ):
        mass_weighted_vector_average(
            vectors=(
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
def test_vector_components_must_be_finite(
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
        match=r"vectors\[0\]\[1\] must be finite",
    ):
        mass_weighted_vector_average(
            vectors=(
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


def test_masses_must_be_tuple() -> None:
    """The canonical fine-mass container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="masses must be a tuple",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
            ),
            masses=[
                1.0,
            ],
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        True,
        False,
        "1.0",
        None,
    ),
)
def test_masses_must_be_real_numbers(
    invalid_mass,
) -> None:
    """Masses must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"masses\[1\] must be a real number",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
            ),
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_masses_must_be_finite(
    invalid_mass: float,
) -> None:
    """Masses must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[1\] must be finite",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
            ),
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
        -10.5,
    ),
)
def test_masses_must_be_positive(
    invalid_mass: float,
) -> None:
    """Every fine-scale mass must be strictly positive."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[1\] must be greater than zero",
    ):
        mass_weighted_vector_average(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
            ),
            masses=(
                1.0,
                invalid_mass,
            ),
            partition=partition,
        )
