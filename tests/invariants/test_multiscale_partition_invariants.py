"""Invariant tests for TR-EIF multiscale partitions."""

import pytest

from tr_eif.multiscale.partition import MultiscalePartition


def test_identity_partition_preserves_entity_count() -> None:
    """Identity partition must preserve one coarse entity per fine entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
        )
    )

    assert partition.fine_count == 4
    assert partition.coarse_count == 4
    assert partition.is_identity

    assert partition.coarse_members == (
        (0,),
        (1,),
        (2,),
        (3,),
    )


def test_many_to_one_partition_groups_fine_entities() -> None:
    """Multiple fine entities may map to one coarse entity."""

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

    assert partition.fine_count == 6
    assert partition.coarse_count == 3
    assert not partition.is_identity

    assert partition.coarse_members == (
        (0, 1),
        (2, 3, 4),
        (5,),
    )


def test_single_coarse_entity_may_contain_all_fine_entities() -> None:
    """A valid partition may map every fine entity to one coarse entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
            0,
        )
    )

    assert partition.fine_count == 4
    assert partition.coarse_count == 1
    assert partition.coarse_members == (
        (0, 1, 2, 3),
    )


def test_coarse_index_lookup_matches_partition_mapping() -> None:
    """Fine-index lookup must reproduce the stored mapping exactly."""

    mapping = (
        0,
        0,
        1,
        2,
        2,
        2,
    )

    partition = MultiscalePartition(
        fine_to_coarse=mapping
    )

    reconstructed = tuple(
        partition.coarse_index_for(fine_index)
        for fine_index in range(partition.fine_count)
    )

    assert reconstructed == mapping


def test_membership_reconstruction_preserves_all_fine_indices() -> None:
    """Coarse memberships must cover every fine entity exactly once."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            1,
            2,
            2,
            2,
            3,
        )
    )

    flattened = tuple(
        fine_index
        for members in partition.coarse_members
        for fine_index in members
    )

    assert sorted(flattened) == list(
        range(partition.fine_count)
    )

    assert len(flattened) == partition.fine_count
    assert len(set(flattened)) == partition.fine_count


def test_each_fine_entity_appears_in_its_assigned_membership() -> None:
    """Every fine entity must occur in exactly its assigned coarse entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
        )
    )

    for fine_index in range(partition.fine_count):
        coarse_index = partition.coarse_index_for(
            fine_index
        )

        assert fine_index in partition.fine_indices_for(
            coarse_index
        )

        for other_coarse_index in range(
            partition.coarse_count
        ):
            if other_coarse_index == coarse_index:
                continue

            assert fine_index not in partition.fine_indices_for(
                other_coarse_index
            )


def test_partition_rejects_empty_mapping() -> None:
    """A partition must contain at least one fine-scale entity."""

    with pytest.raises(
        ValueError,
        match="fine_to_coarse must not be empty",
    ):
        MultiscalePartition(
            fine_to_coarse=()
        )


def test_partition_requires_tuple_mapping() -> None:
    """The canonical partition mapping container must be a tuple."""

    with pytest.raises(
        TypeError,
        match="fine_to_coarse must be a tuple",
    ):
        MultiscalePartition(
            fine_to_coarse=[0, 0, 1]
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        1.5,
        "1",
        None,
        True,
        False,
    ),
)
def test_partition_rejects_noninteger_coarse_index(
    invalid_value,
) -> None:
    """Every coarse assignment must be a non-Boolean integer."""

    with pytest.raises(
        TypeError,
        match="must be an integer",
    ):
        MultiscalePartition(
            fine_to_coarse=(
                0,
                invalid_value,
            )
        )


def test_partition_rejects_negative_coarse_index() -> None:
    """Coarse entity identifiers must be nonnegative."""

    with pytest.raises(
        ValueError,
        match="must be nonnegative",
    ):
        MultiscalePartition(
            fine_to_coarse=(
                0,
                -1,
            )
        )


@pytest.mark.parametrize(
    "mapping",
    (
        (1,),
        (0, 2),
        (0, 0, 3),
        (0, 2, 2, 4),
    ),
)
def test_partition_requires_contiguous_coarse_namespace(
    mapping: tuple[int, ...],
) -> None:
    """Represented coarse identifiers must form 0 through N - 1."""

    with pytest.raises(
        ValueError,
        match="coarse indices must form a contiguous range",
    ):
        MultiscalePartition(
            fine_to_coarse=mapping
        )


@pytest.mark.parametrize(
    "invalid_fine_index",
    (
        -1,
        4,
        100,
    ),
)
def test_coarse_lookup_rejects_out_of_range_fine_index(
    invalid_fine_index: int,
) -> None:
    """Fine-index lookup must remain inside the partition domain."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    with pytest.raises(
        IndexError,
        match="fine_index is outside the partition",
    ):
        partition.coarse_index_for(
            invalid_fine_index
        )


@pytest.mark.parametrize(
    "invalid_fine_index",
    (
        1.0,
        "1",
        None,
        True,
    ),
)
def test_coarse_lookup_requires_integer_fine_index(
    invalid_fine_index,
) -> None:
    """Fine-index lookup requires a non-Boolean integer."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    with pytest.raises(
        TypeError,
        match="fine_index must be an integer",
    ):
        partition.coarse_index_for(
            invalid_fine_index
        )


@pytest.mark.parametrize(
    "invalid_coarse_index",
    (
        -1,
        3,
        100,
    ),
)
def test_membership_lookup_rejects_out_of_range_coarse_index(
    invalid_coarse_index: int,
) -> None:
    """Membership lookup must remain inside the coarse namespace."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
        )
    )

    with pytest.raises(
        IndexError,
        match="coarse_index is outside the partition",
    ):
        partition.fine_indices_for(
            invalid_coarse_index
        )


@pytest.mark.parametrize(
    "
