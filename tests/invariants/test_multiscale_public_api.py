"""Invariant tests for the TR-EIF multiscale public API."""

import tr_eif.multiscale as multiscale


EXPECTED_PUBLIC_API = {
    "CoarseMasses",
    "CoarsePositions",
    "CoarseScaleState",
    "CoarseScalars",
    "CoarseVectors",
    "ElectronicReferenceEvaluator",
    "ElectronicReferenceRecord",
    "FineMasses",
    "FinePositions",
    "FineScalars",
    "FineVectors",
    "MultiscaleHierarchy",
    "MultiscalePartition",
    "MultiscaleStateHierarchy",
    "build_coarse_scale_state",
    "evaluate_electronic_reference",
    "build_multiscale_state_hierarchy",
    "compose_partitions",
    "mass_weighted_centroids",
    "mass_weighted_vector_average",
    "prolong_scalar_broadcast",
    "prolong_vector_broadcast",
    "reduce_masses",
    "reduce_scalar_sum",
    "reduce_vector_sum",
}


def test_public_api_matches_declared_contract() -> None:
    """The exported multiscale API must match the declared contract."""

    assert set(multiscale.__all__) == EXPECTED_PUBLIC_API


def test_public_api_contains_no_duplicate_exports() -> None:
    """Every public symbol must occur exactly once in __all__."""

    assert len(multiscale.__all__) == len(
        set(multiscale.__all__)
    )


def test_every_declared_public_symbol_is_available() -> None:
    """Every name declared in __all__ must be package-accessible."""

    for name in multiscale.__all__:
        assert hasattr(multiscale, name)


def test_public_api_excludes_internal_validation_helpers() -> None:
    """Internal validation helpers must not enter the public boundary."""

    assert all(
        not name.startswith("_validate")
        for name in multiscale.__all__
    )


def test_partition_constructor_is_publicly_executable() -> None:
    """MultiscalePartition must be constructible through the package API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    assert partition.fine_count == 4
    assert partition.coarse_count == 2


def test_partition_composition_is_publicly_executable() -> None:
    """Partition composition must execute through the package API."""

    first = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    second = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    composed = multiscale.compose_partitions(
        fine_to_intermediate=first,
        intermediate_to_coarse=second,
    )

    assert composed.fine_to_coarse == (
        0,
        0,
        0,
        0,
    )


def test_scalar_reduction_is_publicly_executable() -> None:
    """Scalar additive reduction must execute through the package API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    result = multiscale.reduce_scalar_sum(
        (
            1.0,
            2.0,
            3.0,
            4.0,
        ),
        partition,
    )

    assert result == (
        3.0,
        7.0,
    )


def test_mass_reduction_is_publicly_executable() -> None:
    """Mass reduction must execute through the package API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    result = multiscale.reduce_masses(
        (
            1.0,
            2.0,
            3.0,
            4.0,
        ),
        partition,
    )

    assert result == (
        3.0,
        7.0,
    )


def test_centroid_operator_is_publicly_executable() -> None:
    """Cartesian mass-weighted centroids must execute through the API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    result = multiscale.mass_weighted_centroids(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            3.0,
        ),
        partition=partition,
    )

    assert result == (
        (1.5, 0.0, 0.0),
    )


def test_coarse_state_builder_is_publicly_executable() -> None:
    """CoarseScaleState construction must execute through the API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    state = multiscale.build_coarse_scale_state(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
        masses=(
            1.0,
            3.0,
        ),
        partition=partition,
    )

    assert isinstance(
        state,
        multiscale.CoarseScaleState,
    )
    assert state.masses == (
        4.0,
    )
    assert state.positions == (
        (1.5, 0.0, 0.0),
    )


def test_vector_reduction_is_publicly_executable() -> None:
    """Additive vector reduction must execute through the package API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    result = multiscale.reduce_vector_sum(
        (
            (1.0, 2.0, 3.0),
            (4.0, -2.0, 1.0),
        ),
        partition,
    )

    assert result == (
        (5.0, 0.0, 4.0),
    )


def test_mass_weighted_vector_average_is_publicly_executable() -> None:
    """Mass-weighted vector averaging must execute through the API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    result = multiscale.mass_weighted_vector_average(
        vectors=(
            (0.0, 0.0, 0.0),
            (4.0, 2.0, 0.0),
        ),
        masses=(
            1.0,
            3.0,
        ),
        partition=partition,
    )

    assert result == (
        (3.0, 1.5, 0.0),
    )


def test_scalar_prolongation_is_publicly_executable() -> None:
    """Scalar broadcast prolongation must execute through the API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
        )
    )

    result = multiscale.prolong_scalar_broadcast(
        (
            2.0,
            -3.0,
        ),
        partition,
    )

    assert result == (
        2.0,
        -3.0,
        2.0,
        -3.0,
    )


def test_vector_prolongation_is_publicly_executable() -> None:
    """Vector broadcast prolongation must execute through the API."""

    partition = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
        )
    )

    result = multiscale.prolong_vector_broadcast(
        (
            (1.0, 2.0, 3.0),
            (-1.0, 0.0, 4.0),
        ),
        partition,
    )

    assert result == (
        (1.0, 2.0, 3.0),
        (-1.0, 0.0, 4.0),
        (1.0, 2.0, 3.0),
    )


def test_hierarchy_constructor_is_publicly_executable() -> None:
    """MultiscaleHierarchy must be constructible through the API."""

    first = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
        )
    )

    second = multiscale.MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
        )
    )

    hierarchy = multiscale.MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    assert hierarchy.level_counts == (
        4,
        2,
        1,
    )


def test_hierarchy_composition_is_publicly_executable() -> None:
    """Hierarchy composition must remain available through public objects."""

    hierarchy = multiscale.MultiscaleHierarchy(
        partitions=(
            multiscale.MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                )
            ),
            multiscale.MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    composed = hierarchy.composed_partition()

    assert composed.fine_to_coarse == (
        0,
        0,
        0,
        0,
    )


def test_hierarchy_state_builder_is_publicly_executable() -> None:
    """Multilevel coarse-state construction must execute through the API."""

    hierarchy = multiscale.MultiscaleHierarchy(
        partitions=(
            multiscale.MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                )
            ),
            multiscale.MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                )
            ),
        )
    )

    result = multiscale.build_multiscale_state_hierarchy(
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 8.0, 0.0),
        ),
        masses=(
            1.0,
            3.0,
            2.0,
            2.0,
        ),
        hierarchy=hierarchy,
    )

    assert isinstance(
        result,
        multiscale.MultiscaleStateHierarchy,
    )
    assert result.state_count == 2
    assert result.coarsest_state.masses == (
        8.0,
    )
    assert result.coarsest_state.positions == (
        (0.75, 3.0, 0.0),
    )


def test_public_type_aliases_are_available() -> None:
    """Declared transfer and state aliases must remain package-visible."""

    names = (
        "CoarseMasses",
        "CoarsePositions",
        "CoarseScalars",
        "CoarseVectors",
        "FineMasses",
        "FinePositions",
        "FineScalars",
        "FineVectors",
    )

    for name in names:
        assert hasattr(
            multiscale,
            name,
        )


def test_no_private_name_is_declared_in_public_api() -> None:
    """The declared API must contain only public symbol names."""

    assert all(
        not name.startswith("_")
        for name in multiscale.__all__
    )
