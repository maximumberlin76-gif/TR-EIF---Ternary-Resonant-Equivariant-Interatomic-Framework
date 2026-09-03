"""Integration tests for transfer consistency across multiscale hierarchies."""

import pytest

from tr_eif.multiscale.hierarchy import MultiscaleHierarchy
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.prolongation import (
    prolong_scalar_broadcast,
    prolong_vector_broadcast,
)
from tr_eif.multiscale.reduction import (
    reduce_masses,
    reduce_scalar_sum,
)
from tr_eif.multiscale.vector_average import (
    mass_weighted_vector_average,
)
from tr_eif.multiscale.vector_reduction import (
    reduce_vector_sum,
)


def _hierarchy() -> MultiscaleHierarchy:
    """Return a deterministic three-transition hierarchy."""

    return MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
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
            ),
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    1,
                    0,
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


def _scalar_values() -> tuple[float, ...]:
    """Return deterministic fine-scale scalar values."""

    return (
        1.0,
        -2.0,
        3.0,
        4.0,
        -1.0,
        5.0,
        2.0,
        -3.0,
    )


def _masses() -> tuple[float, ...]:
    """Return deterministic positive fine-scale masses."""

    return (
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
    )


def _vectors() -> tuple[tuple[float, float, float], ...]:
    """Return deterministic fine-scale vector values."""

    return (
        (1.0, 0.0, -1.0),
        (2.0, 1.0, 0.0),
        (-1.0, 2.0, 3.0),
        (0.0, -2.0, 1.0),
        (4.0, 1.0, 2.0),
        (-3.0, 0.0, 1.0),
        (2.0, -1.0, -2.0),
        (1.0, 3.0, 0.0),
    )


def _staged_scalar_reduction(
    values: tuple[float, ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[float, ...]:
    """Reduce scalar values sequentially through all transitions."""

    current = values

    for partition in hierarchy.partitions:
        current = reduce_scalar_sum(
            current,
            partition,
        )

    return current


def _staged_mass_reduction(
    masses: tuple[float, ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[float, ...]:
    """Reduce masses sequentially through all transitions."""

    current = masses

    for partition in hierarchy.partitions:
        current = reduce_masses(
            current,
            partition,
        )

    return current


def _staged_vector_reduction(
    vectors: tuple[tuple[float, float, float], ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[tuple[float, float, float], ...]:
    """Reduce vectors sequentially through all transitions."""

    current = vectors

    for partition in hierarchy.partitions:
        current = reduce_vector_sum(
            current,
            partition,
        )

    return current


def _staged_mass_weighted_vector_average(
    vectors: tuple[tuple[float, float, float], ...],
    masses: tuple[float, ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[tuple[float, float, float], ...]:
    """Average vectors sequentially using the mass state at each level."""

    current_vectors = vectors
    current_masses = masses

    for partition in hierarchy.partitions:
        next_vectors = mass_weighted_vector_average(
            current_vectors,
            current_masses,
            partition,
        )

        next_masses = reduce_masses(
            current_masses,
            partition,
        )

        current_vectors = next_vectors
        current_masses = next_masses

    return current_vectors


def _staged_scalar_prolongation(
    values: tuple[float, ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[float, ...]:
    """Broadcast scalar values from coarsest to finest level."""

    current = values

    for partition in reversed(
        hierarchy.partitions
    ):
        current = prolong_scalar_broadcast(
            current,
            partition,
        )

    return current


def _staged_vector_prolongation(
    vectors: tuple[tuple[float, float, float], ...],
    hierarchy: MultiscaleHierarchy,
) -> tuple[tuple[float, float, float], ...]:
    """Broadcast vectors from coarsest to finest level."""

    current = vectors

    for partition in reversed(
        hierarchy.partitions
    ):
        current = prolong_vector_broadcast(
            current,
            partition,
        )

    return current


def test_staged_scalar_reduction_matches_direct_composition() -> None:
    """Additive scalar reduction must commute with partition composition."""

    hierarchy = _hierarchy()

    staged = _staged_scalar_reduction(
        _scalar_values(),
        hierarchy,
    )

    direct = reduce_scalar_sum(
        _scalar_values(),
        hierarchy.composed_partition(),
    )

    assert staged == pytest.approx(
        direct
    )


def test_staged_mass_reduction_matches_direct_composition() -> None:
    """Mass reduction must commute with partition composition."""

    hierarchy = _hierarchy()

    staged = _staged_mass_reduction(
        _masses(),
        hierarchy,
    )

    direct = reduce_masses(
        _masses(),
        hierarchy.composed_partition(),
    )

    assert staged == pytest.approx(
        direct
    )


def test_staged_vector_reduction_matches_direct_composition() -> None:
    """Additive vector reduction must commute with partition composition."""

    hierarchy = _hierarchy()

    staged = _staged_vector_reduction(
        _vectors(),
        hierarchy,
    )

    direct = reduce_vector_sum(
        _vectors(),
        hierarchy.composed_partition(),
    )

    assert len(staged) == len(direct)

    for staged_vector, direct_vector in zip(
        staged,
        direct,
    ):
        assert staged_vector == pytest.approx(
            direct_vector
        )


def test_staged_mass_weighted_average_matches_direct_composition() -> None:
    """Mass-weighted vector averaging must agree across composed scales."""

    hierarchy = _hierarchy()

    staged = _staged_mass_weighted_vector_average(
        _vectors(),
        _masses(),
        hierarchy,
    )

    direct = mass_weighted_vector_average(
        _vectors(),
        _masses(),
        hierarchy.composed_partition(),
    )

    assert len(staged) == len(direct)

    for staged_vector, direct_vector in zip(
        staged,
        direct,
    ):
        assert staged_vector == pytest.approx(
            direct_vector
        )


def test_staged_scalar_broadcast_matches_direct_composition() -> None:
    """Scalar broadcast through adjacent scales must equal direct broadcast."""

    hierarchy = _hierarchy()

    coarsest_values = (
        7.5,
    )

    staged = _staged_scalar_prolongation(
        coarsest_values,
        hierarchy,
    )

    direct = prolong_scalar_broadcast(
        coarsest_values,
        hierarchy.composed_partition(),
    )

    assert staged == pytest.approx(
        direct
    )


def test_staged_vector_broadcast_matches_direct_composition() -> None:
    """Vector broadcast through adjacent scales must equal direct broadcast."""

    hierarchy = _hierarchy()

    coarsest_vectors = (
        (
            2.0,
            -3.0,
            4.0,
        ),
    )

    staged = _staged_vector_prolongation(
        coarsest_vectors,
        hierarchy,
    )

    direct = prolong_vector_broadcast(
        coarsest_vectors,
        hierarchy.composed_partition(),
    )

    assert len(staged) == len(direct)

    for staged_vector, direct_vector in zip(
        staged,
        direct,
    ):
        assert staged_vector == pytest.approx(
            direct_vector
        )


def test_scalar_reduction_preserves_global_additive_total() -> None:
    """Every staged scalar reduction preserves the global additive total."""

    hierarchy = _hierarchy()

    current = _scalar_values()
    expected_total = sum(current)

    for partition in hierarchy.partitions:
        current = reduce_scalar_sum(
            current,
            partition,
        )

        assert sum(current) == pytest.approx(
            expected_total
        )


def test_mass_reduction_preserves_total_mass_at_every_level() -> None:
    """Every hierarchy level must preserve total positive mass."""

    hierarchy = _hierarchy()

    current = _masses()
    expected_total = sum(current)

    for partition in hierarchy.partitions:
        current = reduce_masses(
            current,
            partition,
        )

        assert sum(current) == pytest.approx(
            expected_total
        )


def test_vector_reduction_preserves_componentwise_global_total() -> None:
    """Every staged vector reduction preserves componentwise sums."""

    hierarchy = _hierarchy()

    current = _vectors()

    expected = tuple(
        sum(
            vector[component]
            for vector in current
        )
        for component in range(3)
    )

    for partition in hierarchy.partitions:
        current = reduce_vector_sum(
            current,
            partition,
        )

        actual = tuple(
            sum(
                vector[component]
                for vector in current
            )
            for component in range(3)
        )

        assert actual == pytest.approx(
            expected
        )


def test_constant_mass_weighted_vector_field_survives_all_levels() -> None:
    """A constant vector field remains constant under weighted averaging."""

    hierarchy = _hierarchy()

    constant = (
        3.0,
        -2.0,
        5.0,
    )

    vectors = tuple(
        constant
        for _ in range(
            hierarchy.finest_count
        )
    )

    staged = _staged_mass_weighted_vector_average(
        vectors,
        _masses(),
        hierarchy,
    )

    for vector in staged:
        assert vector == pytest.approx(
            constant
        )


def test_zero_mass_weighted_vector_field_survives_all_levels() -> None:
    """The zero vector field remains zero under weighted averaging."""

    hierarchy = _hierarchy()

    vectors = tuple(
        (
            0.0,
            0.0,
            0.0,
        )
        for _ in range(
            hierarchy.finest_count
        )
    )

    staged = _staged_mass_weighted_vector_average(
        vectors,
        _masses(),
        hierarchy,
    )

    for vector in staged:
        assert vector == pytest.approx(
            (
                0.0,
                0.0,
                0.0,
            )
        )


def test_uniform_mass_scaling_preserves_hierarchical_vector_average() -> None:
    """Uniform positive mass scaling leaves weighted averages unchanged."""

    hierarchy = _hierarchy()

    original = _staged_mass_weighted_vector_average(
        _vectors(),
        _masses(),
        hierarchy,
    )

    scaled = _staged_mass_weighted_vector_average(
        _vectors(),
        tuple(
            11.0 * mass
            for mass in _masses()
        ),
        hierarchy,
    )

    for original_vector, scaled_vector in zip(
        original,
        scaled,
    ):
        assert original_vector == pytest.approx(
            scaled_vector
        )


def test_scalar_broadcast_reconstructs_coarsest_membership() -> None:
    """Direct broadcast assigns each fine entity its final coarse value."""

    hierarchy = _hierarchy()
    composed = hierarchy.composed_partition()

    coarse_values = tuple(
        float(index + 10)
        for index in range(
            composed.coarse_count
        )
    )

    fine_values = _staged_scalar_prolongation(
        coarse_values,
        hierarchy,
    )

    for fine_index in range(
        composed.fine_count
    ):
        coarse_index = composed.coarse_index_for(
            fine_index
        )

        assert (
            fine_values[fine_index]
            == coarse_values[coarse_index]
        )


def test_vector_broadcast_reconstructs_coarsest_membership() -> None:
    """Vector broadcast follows final composed membership exactly."""

    hierarchy = _hierarchy()
    composed = hierarchy.composed_partition()

    coarse_vectors = tuple(
        (
            float(index),
            float(index + 1),
            float(index + 2),
        )
        for index in range(
            composed.coarse_count
        )
    )

    fine_vectors = _staged_vector_prolongation(
        coarse_vectors,
        hierarchy,
    )

    for fine_index in range(
        composed.fine_count
    ):
        coarse_index = composed.coarse_index_for(
            fine_index
        )

        assert fine_vectors[
            fine_index
        ] == pytest.approx(
            coarse_vectors[
                coarse_index
            ]
        )


def test_scalar_broadcast_is_not_additive_redistribution() -> None:
    """Broadcast copies a coarse scalar to every mapped fine entity."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            0,
        )
    )

    fine = prolong_scalar_broadcast(
        (
            6.0,
        ),
        partition,
    )

    assert fine == pytest.approx(
        (
            6.0,
            6.0,
            6.0,
        )
    )

    assert sum(fine) == pytest.approx(
        18.0
    )


def test_vector_broadcast_is_not_additive_redistribution() -> None:
    """Broadcast copies a coarse vector without dividing by membership."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    fine = prolong_vector_broadcast(
        (
            (
                4.0,
                -2.0,
                1.0,
            ),
        ),
        partition,
    )

    assert fine[0] == pytest.approx(
        (
            4.0,
            -2.0,
            1.0,
        )
    )

    assert fine[1] == pytest.approx(
        (
            4.0,
            -2.0,
            1.0,
        )
    )


def test_reduction_then_broadcast_is_not_identity_for_nonuniform_scalar_field() -> None:
    """Coarse reduction followed by broadcast loses fine-scale variation."""

    hierarchy = _hierarchy()

    reduced = _staged_scalar_reduction(
        _scalar_values(),
        hierarchy,
    )

    reconstructed = _staged_scalar_prolongation(
        reduced,
        hierarchy,
    )

    assert reconstructed != _scalar_values()


def test_vector_reduction_then_broadcast_is_not_identity() -> None:
    """Additive vector reduction and broadcast do not invert coarse-graining."""

    hierarchy = _hierarchy()

    reduced = _staged_vector_reduction(
        _vectors(),
        hierarchy,
    )

    reconstructed = _staged_vector_prolongation(
        reduced,
        hierarchy,
    )

    assert reconstructed != _vectors()


def test_mass_weighted_average_then_broadcast_is_not_general_inverse() -> None:
    """Weighted averaging followed by broadcast cannot restore fine variation."""

    hierarchy = _hierarchy()

    averaged = _staged_mass_weighted_vector_average(
        _vectors(),
        _masses(),
        hierarchy,
    )

    reconstructed = _staged_vector_prolongation(
        averaged,
        hierarchy,
    )

    assert reconstructed != _vectors()


def test_identity_hierarchy_preserves_all_transfer_values() -> None:
    """Identity partitions preserve scalar and vector transfers exactly."""

    identity = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            identity,
            identity,
        )
    )

    scalars = (
        1.0,
        -2.0,
        3.0,
    )

    masses = (
        2.0,
        4.0,
        8.0,
    )

    vectors = (
        (1.0, 2.0, 3.0),
        (-1.0, 0.0, 2.0),
        (4.0, -3.0, 1.0),
    )

    assert _staged_scalar_reduction(
        scalars,
        hierarchy,
    ) == pytest.approx(
        scalars
    )

    assert _staged_mass_reduction(
        masses,
        hierarchy,
    ) == pytest.approx(
        masses
    )

    reduced_vectors = _staged_vector_reduction(
        vectors,
        hierarchy,
    )

    averaged_vectors = _staged_mass_weighted_vector_average(
        vectors,
        masses,
        hierarchy,
    )

    prolonged_scalars = _staged_scalar_prolongation(
        scalars,
        hierarchy,
    )

    prolonged_vectors = _staged_vector_prolongation(
        vectors,
        hierarchy,
    )

    for actual, expected in zip(
        reduced_vectors,
        vectors,
    ):
        assert actual == pytest.approx(
            expected
        )

    for actual, expected in zip(
        averaged_vectors,
        vectors,
    ):
        assert actual == pytest.approx(
            expected
        )

    assert prolonged_scalars == pytest.approx(
        scalars
    )

    for actual, expected in zip(
        prolonged_vectors,
        vectors,
    ):
        assert actual == pytest.approx(
            expected
        )


def test_interleaved_hierarchy_transfer_matches_composed_membership() -> None:
    """Cross-scale transfer follows explicit interleaved partition mappings."""

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
            1,
            0,
            1,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    values = (
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    )

    staged = _staged_scalar_reduction(
        values,
        hierarchy,
    )

    direct = reduce_scalar_sum(
        values,
        hierarchy.composed_partition(),
    )

    assert staged == pytest.approx(
        direct
    )

    assert staged == pytest.approx(
        (
            7.0,
            14.0,
        )
    )
