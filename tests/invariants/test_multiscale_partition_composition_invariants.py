"""Invariant tests for TR-EIF multiscale partition composition."""

import pytest

from tr_eif.multiscale.composition import compose_partitions
from tr_eif.multiscale.partition import MultiscalePartition


def test_identity_second_partition_preserves_first_partition() -> None:
    """Composition with an identity intermediate-to-coarse map preserves p."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            1,
            2,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert (
        composed.fine_to_coarse
        == fine_to_intermediate.fine_to_coarse
    )


def test_identity_first_partition_preserves_second_partition() -> None:
    """Composition with an identity fine-to-intermediate map preserves q."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert (
        composed.fine_to_coarse
        == intermediate_to_coarse.fine_to_coarse
    )


def test_identity_composed_with_identity_is_identity() -> None:
    """Two compatible identity mappings compose to an identity mapping."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    assert composed.is_identity
    assert composed.fine_to_coarse == (
        0,
        1,
        2,
        3,
    )


def test_many_to_one_two_level_composition() -> None:
    """Many-to-one mappings compose through the intermediate scale."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            2,
            2,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert composed.fine_to_coarse == (
        0,
        0,
        0,
        0,
        1,
        1,
    )


def test_composition_supports_single_final_coarse_entity() -> None:
    """All intermediate entities may map to one final coarse entity."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            2,
            1,
            2,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert composed.fine_to_coarse == (
        0,
        0,
        0,
        0,
        0,
        0,
    )

    assert composed.coarse_count == 1


def test_interleaved_first_mapping_is_composed_by_membership() -> None:
    """Composition follows explicit first-level membership, not adjacency."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            0,
            1,
            2,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            1,
            0,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert composed.fine_to_coarse == (
        1,
        0,
        1,
        1,
        0,
        1,
    )


def test_interleaved_second_mapping_is_composed_by_membership() -> None:
    """The second mapping may itself use interleaved coarse assignments."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            3,
            3,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert composed.fine_to_coarse == (
        0,
        0,
        1,
        0,
        1,
        1,
    )


def test_composition_matches_pointwise_function_composition() -> None:
    """Every fine entity must satisfy r(i) = q(p(i))."""

    fine_to_intermediate = MultiscalePartition(
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

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            1,
            0,
            1,
            2,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    for fine_index in range(
        fine_to_intermediate.fine_count
    ):
        intermediate_index = (
            fine_to_intermediate.coarse_index_for(
                fine_index
            )
        )

        expected = (
            intermediate_to_coarse.coarse_index_for(
                intermediate_index
            )
        )

        assert (
            composed.coarse_index_for(
                fine_index
            )
            == expected
        )


def test_composition_preserves_original_fine_count() -> None:
    """The composed map retains the domain cardinality of the first map."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            2,
            1,
            2,
            3,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert (
        composed.fine_count
        == fine_to_intermediate.fine_count
    )


def test_composition_uses_final_coarse_namespace() -> None:
    """The composed codomain is the represented final coarse namespace."""

    fine_to_intermediate = MultiscalePartition(
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

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    assert composed.coarse_count == 3

    assert set(
        composed.fine_to_coarse
    ) == {
        0,
        1,
        2,
    }


def test_composed_membership_covers_each_fine_entity_once() -> None:
    """Composed coarse memberships reconstruct the complete fine domain."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            0,
            3,
            1,
            2,
            3,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=fine_to_intermediate,
        intermediate_to_coarse=intermediate_to_coarse,
    )

    reconstructed = tuple(
        sorted(
            fine_index
            for coarse_index in range(
                composed.coarse_count
            )
            for fine_index in composed.fine_indices_for(
                coarse_index
            )
        )
    )

    assert reconstructed == tuple(
        range(
            composed.fine_count
        )
    )


def test_associativity_for_three_compatible_partitions() -> None:
    """Compatible partition composition is associative."""

    fine_to_level_one = MultiscalePartition(
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

    level_one_to_level_two = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
        )
    )

    level_two_to_level_three = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            1,
        )
    )

    left_intermediate = compose_partitions(
        fine_to_intermediate=fine_to_level_one,
        intermediate_to_coarse=level_one_to_level_two,
    )

    left = compose_partitions(
        fine_to_intermediate=left_intermediate,
        intermediate_to_coarse=level_two_to_level_three,
    )

    right_intermediate = compose_partitions(
        fine_to_intermediate=level_one_to_level_two,
        intermediate_to_coarse=level_two_to_level_three,
    )

    right = compose_partitions(
        fine_to_intermediate=fine_to_level_one,
        intermediate_to_coarse=right_intermediate,
    )

    assert (
        left.fine_to_coarse
        == right.fine_to_coarse
    )


def test_associativity_matches_direct_pointwise_mapping() -> None:
    """Three-level composition equals direct nested index lookup."""

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

    first_second = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    composed = compose_partitions(
        fine_to_intermediate=first_second,
        intermediate_to_coarse=third,
    )

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


def test_composition_returns_multiscale_partition() -> None:
    """Composition returns the canonical partition representation."""

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
            1,
        )
    )

    composed = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    assert isinstance(
        composed,
        MultiscalePartition,
    )


def test_first_argument_requires_multiscale_partition() -> None:
    """The fine-to-intermediate map must use MultiscalePartition."""

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=(
            "fine_to_intermediate must be a "
            "MultiscalePartition instance"
        ),
    ):
        compose_partitions(
            fine_to_intermediate=(0,),
            intermediate_to_coarse=second,
        )


def test_second_argument_requires_multiscale_partition() -> None:
    """The intermediate-to-coarse map must use MultiscalePartition."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=(
            "intermediate_to_coarse must be a "
            "MultiscalePartition instance"
        ),
    ):
        compose_partitions(
            fine_to_intermediate=first,
            intermediate_to_coarse=(0,),
        )


def test_incompatible_intermediate_cardinality_is_rejected() -> None:
    """The first codomain must equal the second domain cardinality."""

    fine_to_intermediate = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    intermediate_to_coarse = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    assert fine_to_intermediate.coarse_count == 2
    assert intermediate_to_coarse.fine_count == 3

    with pytest.raises(
        ValueError,
        match=(
            "fine_to_intermediate coarse count must equal "
            "intermediate_to_coarse fine count"
        ),
    ):
        compose_partitions(
            fine_to_intermediate=fine_to_intermediate,
            intermediate_to_coarse=intermediate_to_coarse,
        )


def test_composition_does_not_require_contiguous_fine_membership() -> None:
    """Fine members of one final coarse entity may remain interleaved."""

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

    composed = compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    assert composed.fine_to_coarse == (
        0,
        1,
        0,
        0,
        1,
        0,
    )

    assert composed.fine_indices_for(
        0
    ) == (
        0,
        2,
        3,
        5,
    )

    assert composed.fine_indices_for(
        1
    ) == (
        1,
        4,
    )
