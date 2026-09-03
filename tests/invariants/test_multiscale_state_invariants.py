"""Invariant tests for TR-EIF coarse-scale state construction."""

import pytest

from tr_eif.multiscale.geometry import mass_weighted_centroids
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.reduction import reduce_masses
from tr_eif.multiscale.state import (
    CoarseScaleState,
    build_coarse_scale_state,
)


def test_direct_state_preserves_partition_and_values() -> None:
    """Direct construction must preserve its explicit scale mapping."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    state = CoarseScaleState(
        partition=partition,
        positions=(
            (1.0, 2.0, 3.0),
            (4.0, 5.0, 6.0),
        ),
        masses=(
            3.0,
            7.0,
        ),
    )

    assert state.partition == partition
    assert state.positions == (
        (1.0, 2.0, 3.0),
        (4.0, 5.0, 6.0),
    )
    assert state.masses == (
        3.0,
        7.0,
    )


def test_state_reports_fine_and_coarse_counts() -> None:
    """State cardinalities must derive from the stored partition."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            2,
        )
    )

    state = CoarseScaleState(
        partition=partition,
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
        masses=(
            2.0,
            3.0,
            4.0,
        ),
    )

    assert state.fine_count == 5
    assert state.coarse_count == 3


def test_state_total_mass_equals_sum_of_coarse_masses() -> None:
    """The total-mass observable must equal the stored coarse mass sum."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
        )
    )

    state = CoarseScaleState(
        partition=partition,
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
        masses=(
            2.5,
            7.5,
        ),
    )

    assert state.total_mass == pytest.approx(10.0)
    assert state.total_mass == pytest.approx(
        sum(state.masses)
    )


def test_direct_state_normalizes_integer_values_to_float() -> None:
    """Accepted integer coordinates and masses must normalize to floats."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
        )
    )

    state = CoarseScaleState(
        partition=partition,
        positions=(
            (1, 2, 3),
            (4, 5, 6),
        ),
        masses=(
            2,
            3,
        ),
    )

    assert state.positions == (
        (1.0, 2.0, 3.0),
        (4.0, 5.0, 6.0),
    )
    assert state.masses == (
        2.0,
        3.0,
    )

    assert all(
        isinstance(component, float)
        for position in state.positions
        for component in position
    )

    assert all(
        isinstance(mass, float)
        for mass in state.masses
    )


def test_builder_identity_partition_preserves_positions_and_masses() -> None:
    """Identity coarse construction must preserve fine geometry and masses."""

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
        (7.0, -8.0, 9.0),
    )

    masses = (
        1.0,
        2.0,
        3.0,
    )

    state = build_coarse_scale_state(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    assert state.partition == partition
    assert state.positions == positions
    assert state.masses == masses
    assert state.fine_count == 3
    assert state.coarse_count == 3
    assert state.total_mass == pytest.approx(
        sum(masses)
    )


def test_builder_many_to_one_constructs_expected_state() -> None:
    """Builder must combine mass reduction with mass-weighted geometry."""

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

    state = build_coarse_scale_state(
        positions=(
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

    assert state.masses == (
        4.0,
        3.0,
        2.0,
    )

    assert state.positions == (
        (3.0, 0.0, 0.0),
        (0.0, 3.0, 0.0),
        (0.0, 0.0, 9.0),
    )

    assert state.total_mass == pytest.approx(9.0)


def test_builder_matches_qualified_reduction_and_geometry_operators() -> None:
    """Builder output must equal the independent qualified operators."""

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

    positions = (
        (1.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
        (5.0, 0.0, 0.0),
        (0.0, 0.0, 4.0),
        (0.0, 8.0, 0.0),
        (0.0, 0.0, 10.0),
    )

    masses = (
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    )

    state = build_coarse_scale_state(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    expected_masses = reduce_masses(
        masses=masses,
        partition=partition,
    )

    expected_positions = mass_weighted_centroids(
        positions=positions,
        masses=masses,
        partition=partition,
    )

    assert state.masses == expected_masses

    for actual_position, expected_position in zip(
        state.positions,
        expected_positions,
    ):
        for actual_component, expected_component in zip(
            actual_position,
            expected_position,
        ):
            assert actual_component == pytest.approx(
                expected_component
            )


def test_builder_preserves_total_fine_mass() -> None:
    """Coarse-state construction must preserve the total fine mass."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            2,
            1,
            2,
        )
    )

    masses = (
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    )

    state = build_coarse_scale_state(
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
            (3.0, 0.0, 0.0),
            (4.0, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        ),
        masses=masses,
        partition=partition,
    )

    assert state.total_mass == pytest.approx(
        sum(masses)
    )


def test_direct_state_requires_partition_instance() -> None:
    """Direct state construction requires a MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        CoarseScaleState(
            partition=(0, 1),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
                1.0,
            ),
        )


def test_direct_state_requires_tuple_positions() -> None:
    """The coarse-position container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="positions must be a tuple",
    ):
        CoarseScaleState(
            partition=partition,
            positions=[
                (0.0, 0.0, 0.0),
            ],
            masses=(
                1.0,
            ),
        )


def test_direct_state_requires_tuple_masses() -> None:
    """The coarse-mass container must be a tuple."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match="masses must be a tuple",
    ):
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=[
                1.0,
            ],
        )


def test_direct_state_requires_one_position_per_coarse_entity() -> None:
    """Position cardinality must equal the coarse partition cardinality."""

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
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                2.0,
                3.0,
            ),
        )


def test_direct_state_requires_one_mass_per_coarse_entity() -> None:
    """Mass cardinality must equal the coarse partition cardinality."""

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
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            masses=(
                2.0,
            ),
        )


def test_direct_state_position_must_be_tuple() -> None:
    """Every coarse Cartesian position must use tuple representation."""

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
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
                [1.0, 2.0, 3.0],
            ),
            masses=(
                1.0,
                1.0,
            ),
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
def test_direct_state_position_requires_three_components(
    invalid_position,
) -> None:
    """Every coarse Cartesian position must have three components."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="must contain exactly three components",
    ):
        CoarseScaleState(
            partition=partition,
            positions=(
                invalid_position,
            ),
            masses=(
                1.0,
            ),
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
def test_direct_state_position_components_must_be_real(
    invalid_component,
) -> None:
    """Coarse Cartesian components must be non-Boolean real numbers."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"positions\[0\]\[1\] must be a real number",
    ):
        CoarseScaleState(
            partition=partition,
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
        )


@pytest.mark.parametrize(
    "invalid_component",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_direct_state_position_components_must_be_finite(
    invalid_component: float,
) -> None:
    """Coarse Cartesian components must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"positions\[0\]\[1\] must be finite",
    ):
        CoarseScaleState(
            partition=partition,
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
def test_direct_state_mass_must_be_real(
    invalid_mass,
) -> None:
    """Every coarse mass must be a non-Boolean real number."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        TypeError,
        match=r"masses\[0\] must be a real number",
    ):
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                invalid_mass,
            ),
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_direct_state_mass_must_be_finite(
    invalid_mass: float,
) -> None:
    """Every coarse mass must be finite."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[0\] must be finite",
    ):
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                invalid_mass,
            ),
        )


@pytest.mark.parametrize(
    "invalid_mass",
    (
        0.0,
        -1.0,
        -10.5,
    ),
)
def test_direct_state_mass_must_be_positive(
    invalid_mass: float,
) -> None:
    """Every coarse mass must be strictly positive."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"masses\[0\] must be greater than zero",
    ):
        CoarseScaleState(
            partition=partition,
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                invalid_mass,
            ),
        )


def test_builder_requires_partition_instance() -> None:
    """Builder requires an explicit MultiscalePartition."""

    with pytest.raises(
        TypeError,
        match="partition must be a MultiscalePartition instance",
    ):
        build_coarse_scale_state(
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
            ),
            partition=(0,),
        )


def test_builder_rejects_position_partition_cardinality_mismatch() -> None:
    """Builder must reject a fine-position count inconsistent with partition."""

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
        build_coarse_scale_state(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
                1.0,
                1.0,
            ),
            partition=partition,
        )


def test_builder_rejects_mass_partition_cardinality_mismatch() -> None:
    """Builder must reject a fine-mass count inconsistent with partition."""

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
        build_coarse_scale_state(
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (2.0, 0.0, 0.0),
            ),
            masses=(
                1.0,
                1.0,
            ),
            partition=partition,
        )


def test_builder_rejects_nonfinite_position() -> None:
    """Builder must preserve the finite Cartesian position boundary."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=r"positions\[0\]\[0\] must be finite",
    ):
        build_coarse_scale_state(
            positions=(
                (
                    float("nan"),
                    0.0,
                    0.0,
                ),
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
def test_builder_preserves_mass_domain_validation(
    invalid_mass: float,
) -> None:
    """Builder must preserve the positive finite fine-mass domain."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
        )
    )

    with pytest.raises(ValueError):
        build_coarse_scale_state(
            positions=(
                (0.0, 0.0, 0.0),
            ),
            masses=(
                invalid_mass,
            ),
            partition=partition,
        )
