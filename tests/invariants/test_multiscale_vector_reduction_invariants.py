"""Invariant tests for TR-EIF multiscale vector reduction."""

import pytest

from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.vector_reduction import reduce_vector_sum


def test_identity_partition_preserves_vectors() -> None:
    """Identity reduction must preserve each fine-scale vector."""

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

    coarse = reduce_vector_sum(
        vectors=vectors,
        partition=partition,
    )

    assert coarse == vectors


def test_many_to_one_reduction_uses_partition_local_vector_sums() -> None:
    """Fine vectors must sum componentwise inside assigned coarse entities."""

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

    coarse = reduce_vector_sum(
        vectors=(
            (1.0, 2.0, 3.0),
            (-1.0, 4.0, 2.0),
            (2.0, 0.0, -1.0),
            (3.0, 5.0, 4.0),
            (-2.0, -1.0, 7.0),
            (8.0, -3.0, 1.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (0.0, 6.0, 5.0),
        (3.0, 4.0, 10.0),
        (8.0, -3.0, 1.0),
    )


def test_interleaved_partition_follows_explicit_assignments() -> None:
    """Reduction must follow partition membership rather than adjacency."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (1.0, 2.0, 3.0),
            (10.0, 20.0, 30.0),
            (4.0, 5.0, 6.0),
            (40.0, 50.0, 60.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (5.0, 7.0, 9.0),
        (50.0, 70.0, 90.0),
    )


def test_single_coarse_entity_sums_all_vectors() -> None:
    """One coarse entity may receive the complete fine vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
            0,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (1.0, 0.0, -1.0),
            (2.0, 3.0, 4.0),
            (-5.0, 6.0, 1.0),
            (2.0, -4.0, 8.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (0.0, 5.0, 12.0),
    )


def test_vector_reduction_preserves_global_component_sums() -> None:
    """Coarse reduction must preserve the global sum componentwise."""

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

    vectors = (
        (1.5, -2.0, 3.0),
        (-4.0, 5.5, 6.0),
        (7.0, 8.0, -9.0),
        (10.0, -11.0, 12.0),
        (-13.0, 14.0, 15.0),
        (16.0, 17.0, -18.0),
    )

    coarse = reduce_vector_sum(
        vectors=vectors,
        partition=partition,
    )

    fine_total = tuple(
        sum(vector[component] for vector in vectors)
        for component in range(3)
    )

    coarse_total = tuple(
        sum(vector[component] for vector in coarse)
        for component in range(3)
    )

    for actual, expected in zip(
        coarse_total,
        fine_total,
    ):
        assert actual == pytest.approx(expected)


def test_vector_reduction_allows_zero_vectors() -> None:
    """Zero vectors are valid values for an additive vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
    )


def test_vector_reduction_allows_signed_components() -> None:
    """Generic additive vectors may contain positive and negative components."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (-3.0, 2.0, -1.0),
            (1.0, -5.0, 4.0),
            (-7.0, -2.0, 6.0),
            (2.0, 3.0, -8.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (-2.0, -3.0, 3.0),
        (-5.0, 1.0, -2.0),
    )


def test_vector_reduction_does_not_average_members() -> None:
    """Additive vector reduction must use sums rather than member averages."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (2.0, 4.0, 6.0),
            (4.0, 8.0, 12.0),
        ),
        partition=partition,
    )

    assert coarse == (
        (6.0, 12.0, 18.0),
    )

    assert coarse != (
        (3.0, 6.0, 9.0),
    )


def test_integer_vectors_are_normalized_to_float() -> None:
    """Accepted integer components must produce canonical float output."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    coarse = reduce_vector_sum(
        vectors=(
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9),
        ),
        partition=partition,
    )

    assert coarse == (
        (5.0, 7.0, 9.0),
        (7.0, 8.0, 9.0),
    )

    assert all(
        isinstance(component, float)
        for vector in coarse
        for component in vector
    )


def test_vector_reduction_requires_partition_instance() -> None:
    """Vector reduction requires an explicit MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        reduce_vector_sum(
            vectors=(
                (1.0, 2.0, 3.0),
            ),
            partition=(0,),
        )


def test_vectors_must_be_tuple() -> None:
    """The canonical fine-scale vector container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="vectors must be a tuple",
    ):
        reduce_vector_sum(
            vectors=[
                (1.0, 2.0, 3.0),
            ],
            partition=partition,
        )


def test_vectors_must_not_be_empty() -> None:
    """Vector reduction requires a nonempty fine-scale vector field."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="vectors must not be empty",
    ):
        reduce_vector_sum(
            vectors=(),
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
        reduce_vector_sum(
            vectors=(
                (1.0, 2.0, 3.0),
                (4.0, 5.0, 6.0),
            ),
            partition=partition,
        )


def test_each_vector_must_be_tuple() -> None:
    """Every fine-scale vector must use tuple representation."""

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
        reduce_vector_sum(
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
def test_each_vector_requires_exactly_three_components(
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
        reduce_vector_sum(
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
def test_vector_components_must_be_real_numbers(
    invalid_component,
) -> None:
    """Vector components must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"vectors\[0\]\[1\] must be a real number",
    ):
        reduce_vector_sum(
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
def test_vector_components_must_be_finite(
    invalid_component: float,
) -> None:
    """Vector components must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"vectors\[0\]\[1\] must be finite",
    ):
        reduce_vector_sum(
            vectors=(
                (
                    0.0,
                    invalid_component,
                    0.0,
                ),
            ),
            partition=partition,
        )


def test_single_member_coarse_entity_preserves_vector() -> None:
    """A one-member coarse entity must retain its fine vector exactly."""

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

    coarse = reduce_vector_sum(
        vectors=vectors,
        partition=partition,
    )

    assert coarse[1] == vectors[2]


def test_reduction_output_count_matches_coarse_count() -> None:
    """The reduced vector field must contain one vector per coarse entity."""

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

    coarse = reduce_vector_sum(
        vectors=(
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (3.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (5.0, 0.0, 0.0),
            (6.0, 0.0, 0.0),
        ),
        partition=partition,
    )

    assert len(coarse) == partition.coarse_count
