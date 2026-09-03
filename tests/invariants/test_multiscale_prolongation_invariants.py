"""Invariant tests for TR-EIF multiscale broadcast prolongation."""

import pytest

from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.prolongation import (
    prolong_scalar_broadcast,
    prolong_vector_broadcast,
)


def test_scalar_identity_partition_preserves_values() -> None:
    """Scalar broadcast over an identity partition preserves values."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    values = (
        1.0,
        -2.0,
        3.5,
    )

    fine = prolong_scalar_broadcast(
        values=values,
        partition=partition,
    )

    assert fine == values


def test_scalar_many_to_one_broadcast_repeats_coarse_values() -> None:
    """Each fine entity receives its assigned coarse scalar."""

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

    fine = prolong_scalar_broadcast(
        values=(
            2.0,
            -3.0,
            7.0,
        ),
        partition=partition,
    )

    assert fine == (
        2.0,
        2.0,
        -3.0,
        -3.0,
        -3.0,
        7.0,
    )


def test_scalar_interleaved_partition_follows_assignments() -> None:
    """Scalar broadcast follows partition membership, not adjacency."""

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

    fine = prolong_scalar_broadcast(
        values=(
            10.0,
            20.0,
            30.0,
        ),
        partition=partition,
    )

    assert fine == (
        10.0,
        20.0,
        10.0,
        30.0,
        20.0,
        30.0,
    )


def test_scalar_constant_field_is_preserved() -> None:
    """Broadcast preserves a constant coarse scalar field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
        )
    )

    fine = prolong_scalar_broadcast(
        values=(
            4.5,
            4.5,
            4.5,
        ),
        partition=partition,
    )

    assert fine == (
        4.5,
        4.5,
        4.5,
        4.5,
        4.5,
    )


def test_scalar_broadcast_preserves_signed_and_zero_values() -> None:
    """Signed and zero scalar values remain ordinary numerical values."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            0,
            1,
        )
    )

    fine = prolong_scalar_broadcast(
        values=(
            -1.0,
            0.0,
            1.0,
        ),
        partition=partition,
    )

    assert fine == (
        -1.0,
        0.0,
        1.0,
        -1.0,
        0.0,
    )


def test_scalar_integer_values_are_normalized_to_float() -> None:
    """Accepted integer scalar values produce canonical float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    fine = prolong_scalar_broadcast(
        values=(
            2,
            5,
        ),
        partition=partition,
    )

    assert fine == (
        2.0,
        5.0,
        2.0,
    )

    assert all(
        isinstance(value, float)
        for value in fine
    )


def test_scalar_output_count_matches_fine_count() -> None:
    """Scalar prolongation returns one value per fine entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
            1,
        )
    )

    fine = prolong_scalar_broadcast(
        values=(
            1.0,
            2.0,
            3.0,
        ),
        partition=partition,
    )

    assert len(fine) == partition.fine_count


def test_scalar_members_reconstruct_exact_coarse_values() -> None:
    """Every partition member receives exactly its coarse scalar."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            2,
            1,
            0,
            2,
            1,
        )
    )

    coarse = (
        -4.0,
        6.5,
        9.0,
    )

    fine = prolong_scalar_broadcast(
        values=coarse,
        partition=partition,
    )

    for fine_index in range(
        partition.fine_count
    ):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        assert fine[fine_index] == coarse[coarse_index]


def test_scalar_broadcast_is_not_additive_redistribution() -> None:
    """Broadcast copies a coarse scalar rather than dividing it among members."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
        )
    )

    fine = prolong_scalar_broadcast(
        values=(
            6.0,
        ),
        partition=partition,
    )

    assert fine == (
        6.0,
        6.0,
        6.0,
    )

    assert sum(fine) == 18.0
    assert sum(fine) != 6.0


def test_vector_identity_partition_preserves_vectors() -> None:
    """Vector broadcast over an identity partition preserves vectors."""

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

    fine = prolong_vector_broadcast(
        vectors=vectors,
        partition=partition,
    )

    assert fine == vectors


def test_vector_many_to_one_broadcast_repeats_coarse_vectors() -> None:
    """Each fine entity receives its assigned coarse vector."""

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

    fine = prolong_vector_broadcast(
        vectors=(
            (1.0, 2.0, 3.0),
            (-4.0, 5.0, -6.0),
            (7.0, 8.0, 9.0),
        ),
        partition=partition,
    )

    assert fine == (
        (1.0, 2.0, 3.0),
        (1.0, 2.0, 3.0),
        (-4.0, 5.0, -6.0),
        (-4.0, 5.0, -6.0),
        (-4.0, 5.0, -6.0),
        (7.0, 8.0, 9.0),
    )


def test_vector_interleaved_partition_follows_assignments() -> None:
    """Vector broadcast follows partition membership, not adjacency."""

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

    fine = prolong_vector_broadcast(
        vectors=(
            (1.0, 0.0, 0.0),
            (0.0, 2.0, 0.0),
            (0.0, 0.0, 3.0),
        ),
        partition=partition,
    )

    assert fine == (
        (1.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 3.0),
        (0.0, 2.0, 0.0),
        (0.0, 0.0, 3.0),
    )


def test_vector_constant_field_is_preserved() -> None:
    """Broadcast preserves a constant coarse vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
        )
    )

    constant = (
        2.5,
        -3.0,
        7.0,
    )

    fine = prolong_vector_broadcast(
        vectors=(
            constant,
            constant,
            constant,
        ),
        partition=partition,
    )

    assert fine == (
        constant,
        constant,
        constant,
        constant,
        constant,
    )


def test_vector_zero_field_is_preserved() -> None:
    """Broadcast preserves a zero Cartesian vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    fine = prolong_vector_broadcast(
        vectors=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        ),
        partition=partition,
    )

    assert fine == (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )


def test_vector_signed_components_are_preserved() -> None:
    """Broadcast preserves signed Cartesian vector components."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    fine = prolong_vector_broadcast(
        vectors=(
            (-1.0, 2.0, -3.0),
            (4.0, -5.0, 6.0),
        ),
        partition=partition,
    )

    assert fine == (
        (-1.0, 2.0, -3.0),
        (4.0, -5.0, 6.0),
        (-1.0, 2.0, -3.0),
    )


def test_vector_integer_components_are_normalized_to_float() -> None:
    """Accepted integer components produce canonical float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    fine = prolong_vector_broadcast(
        vectors=(
            (1, 2, 3),
            (4, 5, 6),
        ),
        partition=partition,
    )

    assert fine == (
        (1.0, 2.0, 3.0),
        (4.0, 5.0, 6.0),
        (1.0, 2.0, 3.0),
    )

    assert all(
        isinstance(component, float)
        for vector in fine
        for component in vector
    )


def test_vector_output_count_matches_fine_count() -> None:
    """Vector prolongation returns one vector per fine entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
            1,
        )
    )

    fine = prolong_vector_broadcast(
        vectors=(
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
        partition=partition,
    )

    assert len(fine) == partition.fine_count


def test_vector_members_reconstruct_exact_coarse_vectors() -> None:
    """Every partition member receives exactly its coarse vector."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            2,
            1,
            0,
            2,
            1,
        )
    )

    coarse = (
        (-4.0, 1.0, 2.0),
        (6.5, -3.0, 4.0),
        (9.0, 5.0, -7.0),
    )

    fine = prolong_vector_broadcast(
        vectors=coarse,
        partition=partition,
    )

    for fine_index in range(
        partition.fine_count
    ):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        assert fine[fine_index] == coarse[coarse_index]


def test_vector_broadcast_is_not_additive_redistribution() -> None:
    """Broadcast copies a vector rather than dividing it among members."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    fine = prolong_vector_broadcast(
        vectors=(
            (6.0, -4.0, 2.0),
        ),
        partition=partition,
    )

    assert fine == (
        (6.0, -4.0, 2.0),
        (6.0, -4.0, 2.0),
    )

    total = tuple(
        sum(vector[component] for vector in fine)
        for component in range(3)
    )

    assert total == (
        12.0,
        -8.0,
        4.0,
    )


def test_scalar_prolongation_requires_partition_instance() -> None:
    """Scalar prolongation requires a MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        prolong_scalar_broadcast(
            values=(
                1.0,
            ),
            partition=(0,),
        )


def test_vector_prolongation_requires_partition_instance() -> None:
    """Vector prolongation requires a MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        prolong_vector_broadcast(
            vectors=(
                (1.0, 2.0, 3.0),
            ),
            partition=(0,),
        )


def test_scalar_values_must_be_tuple() -> None:
    """The canonical coarse scalar container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="values must be a tuple",
    ):
        prolong_scalar_broadcast(
            values=[
                1.0,
            ],
            partition=partition,
        )


def test_scalar_values_must_not_be_empty() -> None:
    """Scalar prolongation requires a nonempty coarse field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        prolong_scalar_broadcast(
            values=(),
            partition=partition,
        )


def test_scalar_count_must_match_coarse_count() -> None:
    """One scalar is required for every coarse entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one scalar per coarse-scale entity",
    ):
        prolong_scalar_broadcast(
            values=(
                1.0,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        True,
        False,
        "1.0",
        None,
    ),
)
def test_scalar_values_must_be_real_numbers(
    invalid_value,
) -> None:
    """Coarse scalar values must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"values\[1\] must be a real number",
    ):
        prolong_scalar_broadcast(
            values=(
                1.0,
                invalid_value,
            ),
            partition=partition,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_scalar_values_must_be_finite(
    invalid_value: float,
) -> None:
    """Coarse scalar values must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"values\[1\] must be finite",
    ):
        prolong_scalar_broadcast(
            values=(
                1.0,
                invalid_value,
            ),
            partition=partition,
        )


def test_vector_values_must_be_tuple() -> None:
    """The canonical coarse vector container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="vectors must be a tuple",
    ):
        prolong_vector_broadcast(
            vectors=[
                (1.0, 2.0, 3.0),
            ],
            partition=partition,
        )


def test_vector_values_must_not_be_empty() -> None:
    """Vector prolongation requires a nonempty coarse field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="vectors must not be empty",
    ):
        prolong_vector_broadcast(
            vectors=(),
            partition=partition,
        )


def test_vector_count_must_match_coarse_count() -> None:
    """One vector is required for every coarse entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        ValueError,
        match="one vector per coarse-scale entity",
    ):
        prolong_vector_broadcast(
            vectors=(
                (1.0, 2.0, 3.0),
            ),
            partition=partition,
        )


def test_each_coarse_vector_must_be_tuple() -> None:
    """Each coarse vector must use tuple representation."""

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
        prolong_vector_broadcast(
            vectors=(
                (1.0, 2.0, 3.0),
                [4.0, 5.0, 6.0],
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
def test_each_coarse_vector_requires_three_components(
    invalid_vector,
) -> None:
    """Every coarse Cartesian vector requires exactly three components."""

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
        prolong_vector_broadcast(
            vectors=(
                (1.0, 2.0, 3.0),
                invalid_vector,
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
def test_coarse_vector_components_must_be_real_numbers(
    invalid_component,
) -> None:
    """Coarse vector components must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"vectors\[0\]\[1\] must be a real number",
    ):
        prolong_vector_broadcast(
            vectors=(
                (
                    0.0,
                    invalid_component,
                    0.0,
                ),
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
def test_coarse_vector_components_must_be_finite(
    invalid_component: float,
) -> None:
    """Coarse vector components must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"vectors\[0\]\[1\] must be finite",
    ):
        prolong_vector_broadcast(
            vectors=(
                (
                    0.0,
                    invalid_component,
                    0.0,
                ),
            ),
            partition=partition,
        )
