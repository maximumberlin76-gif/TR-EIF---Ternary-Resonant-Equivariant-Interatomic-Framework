"""Invariant tests for TR-EIF multiscale partition hierarchies."""

import pytest

from tr_eif.multiscale.composition import compose_partitions
from tr_eif.multiscale.hierarchy import MultiscaleHierarchy
from tr_eif.multiscale.partition import MultiscalePartition


def test_single_transition_hierarchy_has_two_levels() -> None:
    """One partition represents two scale levels."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            partition,
        )
    )

    assert hierarchy.level_count == 2
    assert hierarchy.transition_count == 1
    assert hierarchy.finest_count == 4
    assert hierarchy.coarsest_count == 2
    assert hierarchy.level_counts == (
        4,
        2,
    )


def test_multilevel_hierarchy_reports_cardinality_chain() -> None:
    """Level counts must represent every scale in order."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                    2,
                    2,
                    3,
                    3,
                )
            ),
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                )
            ),
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    assert hierarchy.level_count == 4
    assert hierarchy.transition_count == 3
    assert hierarchy.finest_count == 8
    assert hierarchy.coarsest_count == 1
    assert hierarchy.level_counts == (
        8,
        4,
        2,
        1,
    )


def test_partition_at_returns_exact_adjacent_partition() -> None:
    """Adjacent scale transitions remain directly accessible."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    assert hierarchy.partition_at(0) is first
    assert hierarchy.partition_at(1) is second


def test_single_transition_composition_returns_partition() -> None:
    """Composing the only represented transition returns that mapping."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            partition,
        )
    )

    composed = hierarchy.composed_partition()

    assert (
        composed.fine_to_coarse
        == partition.fine_to_coarse
    )


def test_default_composition_spans_finest_to_coarsest() -> None:
    """Default composition must span the complete hierarchy."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
            0,
            1,
            2,
            3,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    composed = hierarchy.composed_partition()

    assert composed.fine_count == 8
    assert composed.coarse_count == 1
    assert composed.fine_to_coarse == (
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )


def test_full_composition_matches_explicit_pairwise_composition() -> None:
    """Hierarchy composition must equal explicit partition composition."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            2,
            1,
            3,
            0,
            2,
            3,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            1,
            2,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            1,
            0,
            1,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    first_second = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    expected = compose_partitions(
        fine_to_intermediate=first_second,
        intermediate_to_coarse=third,
    )

    actual = hierarchy.composed_partition()

    assert (
        actual.fine_to_coarse
        == expected.fine_to_coarse
    )


def test_partial_composition_from_finest_level() -> None:
    """A prefix of the hierarchy may be composed explicitly."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
            0,
            1,
            2,
            3,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    actual = hierarchy.composed_partition(
        start_level=0,
        end_level=2,
    )

    expected = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    assert (
        actual.fine_to_coarse
        == expected.fine_to_coarse
    )

    assert actual.fine_count == 8
    assert actual.coarse_count == 2


def test_partial_composition_between_internal_levels() -> None:
    """Composition may begin and end at internal hierarchy levels."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            2,
            2,
            3,
            3,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    actual = hierarchy.composed_partition(
        start_level=1,
        end_level=3,
    )

    expected = compose_partitions(
        fine_to_intermediate=second,
        intermediate_to_coarse=third,
    )

    assert (
        actual.fine_to_coarse
        == expected.fine_to_coarse
    )

    assert actual.fine_count == 4
    assert actual.coarse_count == 1


def test_adjacent_level_composition_returns_adjacent_partition() -> None:
    """A one-transition level range preserves its adjacent mapping."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    actual = hierarchy.composed_partition(
        start_level=1,
        end_level=2,
    )

    assert (
        actual.fine_to_coarse
        == second.fine_to_coarse
    )


def test_composed_mapping_matches_nested_lookup() -> None:
    """Full hierarchy mapping must equal nested adjacent lookups."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            2,
            1,
            3,
            0,
            3,
            2,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            1,
            2,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            1,
            0,
            1,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    composed = hierarchy.composed_partition()

    for fine_index in range(
        first.fine_count
    ):
        level_one = first.coarse_index_for(
            fine_index
        )

        level_two = second.coarse_index_for(
            level_one
        )

        expected = third.coarse_index_for(
            level_two
        )

        assert (
            composed.coarse_index_for(
                fine_index
            )
            == expected
        )


def test_interleaved_hierarchy_preserves_explicit_membership() -> None:
    """Hierarchy composition follows explicit mappings, not adjacency."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            0,
            1,
            2,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    composed = hierarchy.composed_partition()

    assert composed.fine_to_coarse == (
        0,
        1,
        0,
        0,
        1,
        0,
    )


def test_identity_transitions_are_supported() -> None:
    """Identity partitions may occur inside a hierarchy."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    assert hierarchy.level_counts == (
        3,
        3,
        3,
    )

    assert hierarchy.composed_partition().is_identity


def test_partitions_container_must_be_tuple() -> None:
    """Hierarchy partitions must use the canonical tuple container."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="partitions must be a tuple",
    ):
        MultiscaleHierarchy(
            partitions=[
                partition,
            ]
        )


def test_partitions_must_not_be_empty() -> None:
    """A hierarchy requires at least one scale transition."""

    with pytest.raises(
        ValueError,
        match="partitions must not be empty",
    ):
        MultiscaleHierarchy(
            partitions=()
        )


@pytest.mark.parametrize(
    "invalid_partition",
    (
        (0,),
        None,
        "partition",
        1,
    ),
)
def test_each_partition_requires_multiscale_partition(
    invalid_partition,
) -> None:
    """Every hierarchy transition must be a MultiscalePartition."""

    valid = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"partitions\[1\] must be a MultiscalePartition instance",
    ):
        MultiscaleHierarchy(
            partitions=(
                valid,
                invalid_partition,
            )
        )


def test_incompatible_adjacent_partitions_are_rejected() -> None:
    """Adjacent scale boundaries require matching cardinalities."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    assert first.coarse_count == 2
    assert second.fine_count == 3

    with pytest.raises(
        ValueError,
        match=(
            "adjacent partitions must have matching "
            "coarse and fine cardinalities"
        ),
    ):
        MultiscaleHierarchy(
            partitions=(
                first,
                second,
            )
        )


@pytest.mark.parametrize(
    "invalid_index",
    (
        0.0,
        True,
        False,
        "0",
        None,
    ),
)
def test_partition_at_requires_integer_index(
    invalid_index,
) -> None:
    """Transition lookup index must be a non-Boolean integer."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        TypeError,
        match="transition_index must be an integer",
    ):
        hierarchy.partition_at(
            invalid_index
        )


@pytest.mark.parametrize(
    "invalid_index",
    (
        -1,
        1,
        2,
    ),
)
def test_partition_at_rejects_out_of_range_index(
    invalid_index: int,
) -> None:
    """Transition lookup rejects indices outside the hierarchy."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        IndexError,
        match="transition_index is out of range",
    ):
        hierarchy.partition_at(
            invalid_index
        )


@pytest.mark.parametrize(
    "invalid_start",
    (
        0.0,
        True,
        False,
        "0",
        None,
    ),
)
def test_composition_requires_integer_start_level(
    invalid_start,
) -> None:
    """Composition start level must be a non-Boolean integer."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        TypeError,
        match="start_level must be an integer",
    ):
        hierarchy.composed_partition(
            start_level=invalid_start,
        )


@pytest.mark.parametrize(
    "invalid_end",
    (
        1.0,
        True,
        False,
        "1",
    ),
)
def test_composition_requires_integer_or_none_end_level(
    invalid_end,
) -> None:
    """Composition end level must be a non-Boolean integer or None."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        TypeError,
        match="end_level must be an integer or None",
    ):
        hierarchy.composed_partition(
            end_level=invalid_end,
        )


@pytest.mark.parametrize(
    "invalid_start",
    (
        -1,
        2,
        3,
    ),
)
def test_composition_rejects_out_of_range_start_level(
    invalid_start: int,
) -> None:
    """Start level must identify a represented hierarchy level."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        IndexError,
        match="start_level is out of range",
    ):
        hierarchy.composed_partition(
            start_level=invalid_start,
        )


@pytest.mark.parametrize(
    "invalid_end",
    (
        -1,
        2,
        3,
    ),
)
def test_composition_rejects_out_of_range_end_level(
    invalid_end: int,
) -> None:
    """End level must identify a represented hierarchy level."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        IndexError,
        match="end_level is out of range",
    ):
        hierarchy.composed_partition(
            start_level=0,
            end_level=invalid_end,
        )


def test_composition_rejects_equal_start_and_end_levels() -> None:
    """A composed partition requires at least one scale transition."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="end_level must be greater than start_level",
    ):
        hierarchy.composed_partition(
            start_level=1,
            end_level=1,
        )


def test_composition_rejects_reverse_level_range() -> None:
    """Hierarchy composition is defined only in the fine-to-coarse direction."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                )
            ),
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="end_level must be greater than start_level",
    ):
        hierarchy.composed_partition(
            start_level=2,
            end_level=1,
        )


def test_default_end_level_uses_coarsest_level() -> None:
    """None selects the coarsest represented hierarchy level."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    implicit = hierarchy.composed_partition(
        start_level=0,
    )

    explicit = hierarchy.composed_partition(
        start_level=0,
        end_level=2,
    )

    assert (
        implicit.fine_to_coarse
        == explicit.fine_to_coarse
    )


def test_internal_default_end_level_reaches_coarsest_level() -> None:
    """Default end level also applies when composition starts internally."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            2,
            2,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    third = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
            third,
        )
    )

    implicit = hierarchy.composed_partition(
        start_level=1,
    )

    explicit = hierarchy.composed_partition(
        start_level=1,
        end_level=3,
    )

    assert (
        implicit.fine_to_coarse
        == explicit.fine_to_coarse
    )
