"""Invariant tests for TR-EIF multiscale hierarchy state construction."""

import pytest

from tr_eif.multiscale.composition import compose_partitions
from tr_eif.multiscale.hierarchy import MultiscaleHierarchy
from tr_eif.multiscale.hierarchy_state import (
    MultiscaleStateHierarchy,
    build_multiscale_state_hierarchy,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.state import (
    CoarseScaleState,
    build_coarse_scale_state,
)


def _three_level_hierarchy() -> MultiscaleHierarchy:
    """Return a deterministic three-transition hierarchy."""

    return MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    0,
                    1,
                    1,
                    2,
                    2,
                )
            ),
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    1,
                    0,
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


def _positions() -> tuple[tuple[float, float, float], ...]:
    """Return deterministic fine-scale Cartesian positions."""

    return (
        (0.0, 0.0, 0.0),
        (2.0, 0.0, 0.0),
        (0.0, 4.0, 0.0),
        (0.0, 8.0, 0.0),
        (0.0, 0.0, 6.0),
        (0.0, 0.0, 12.0),
    )


def _masses() -> tuple[float, ...]:
    """Return deterministic positive fine-scale masses."""

    return (
        1.0,
        3.0,
        2.0,
        2.0,
        1.0,
        5.0,
    )


def test_builder_creates_one_state_per_transition() -> None:
    """Every hierarchy transition must generate one coarse state."""

    hierarchy = _three_level_hierarchy()

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    assert result.state_count == 3
    assert len(result.states) == hierarchy.transition_count


def test_builder_preserves_hierarchy_reference() -> None:
    """The generated state hierarchy retains its mapping hierarchy."""

    hierarchy = _three_level_hierarchy()

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    assert result.hierarchy is hierarchy


def test_each_state_uses_corresponding_partition() -> None:
    """Each generated state must retain its adjacent partition."""

    hierarchy = _three_level_hierarchy()

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    for index, state in enumerate(result.states):
        assert state.partition == hierarchy.partition_at(index)


def test_generated_state_cardinalities_follow_level_counts() -> None:
    """Generated coarse counts must match hierarchy cardinalities."""

    hierarchy = _three_level_hierarchy()

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    assert hierarchy.level_counts == (
        6,
        3,
        2,
        1,
    )

    assert tuple(
        state.coarse_count
        for state in result.states
    ) == (
        3,
        2,
        1,
    )


def test_first_level_masses_are_partition_local_sums() -> None:
    """First coarse masses must equal explicit fine-scale sums."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    assert result.state_at(1).masses == (
        4.0,
        4.0,
        6.0,
    )


def test_second_level_masses_use_previous_level_masses() -> None:
    """Second-level masses must aggregate the first coarse masses."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    assert result.state_at(2).masses == (
        10.0,
        4.0,
    )


def test_coarsest_mass_equals_total_fine_mass() -> None:
    """The final coarse mass must equal total microscopic mass."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    assert result.coarsest_state.masses == (
        14.0,
    )

    assert result.coarsest_state.total_mass == pytest.approx(
        sum(_masses())
    )


def test_total_mass_is_preserved_at_every_generated_level() -> None:
    """Every coarse level must preserve total mass."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    expected_total = sum(_masses())

    for state in result.states:
        assert state.total_mass == pytest.approx(
            expected_total
        )


def test_first_level_centroids_match_explicit_values() -> None:
    """First-level positions must be mass-weighted centroids."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    positions = result.state_at(1).positions

    assert positions[0] == pytest.approx(
        (1.5, 0.0, 0.0)
    )
    assert positions[1] == pytest.approx(
        (0.0, 6.0, 0.0)
    )
    assert positions[2] == pytest.approx(
        (0.0, 0.0, 11.0)
    )


def test_second_level_centroids_use_previous_coarse_state() -> None:
    """Second-level centroids must use first-level masses and positions."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    positions = result.state_at(2).positions

    assert positions[0] == pytest.approx(
        (0.6, 0.0, 6.6)
    )
    assert positions[1] == pytest.approx(
        (0.0, 6.0, 0.0)
    )


def test_coarsest_centroid_matches_total_mass_weighted_centroid() -> None:
    """Final staged centroid must equal the direct fine-scale centroid."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    expected = (
        6.0 / 14.0,
        24.0 / 14.0,
        66.0 / 14.0,
    )

    assert result.coarsest_state.positions[0] == pytest.approx(
        expected
    )


def test_staged_coarse_state_matches_direct_composed_partition() -> None:
    """Staged coarse-graining must equal direct composed coarse-graining."""

    hierarchy = _three_level_hierarchy()

    staged = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    direct = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=hierarchy.composed_partition(),
    )

    assert staged.coarsest_state.masses == pytest.approx(
        direct.masses
    )

    assert (
        staged.coarsest_state.coarse_count
        == direct.coarse_count
    )

    for staged_position, direct_position in zip(
        staged.coarsest_state.positions,
        direct.positions,
    ):
        assert staged_position == pytest.approx(
            direct_position
        )


def test_internal_staged_state_matches_partial_composed_partition() -> None:
    """An internal staged level must equal direct prefix coarse-graining."""

    hierarchy = _three_level_hierarchy()

    staged = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    direct_partition = hierarchy.composed_partition(
        start_level=0,
        end_level=2,
    )

    direct = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=direct_partition,
    )

    internal = staged.state_at(2)

    assert internal.masses == pytest.approx(
        direct.masses
    )

    for staged_position, direct_position in zip(
        internal.positions,
        direct.positions,
    ):
        assert staged_position == pytest.approx(
            direct_position
        )


def test_explicit_pairwise_composition_matches_coarsest_state() -> None:
    """Explicit partition composition must reproduce the final state."""

    hierarchy = _three_level_hierarchy()

    first_two = compose_partitions(
        fine_to_intermediate=hierarchy.partition_at(0),
        intermediate_to_coarse=hierarchy.partition_at(1),
    )

    complete = compose_partitions(
        fine_to_intermediate=first_two,
        intermediate_to_coarse=hierarchy.partition_at(2),
    )

    direct = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=complete,
    )

    staged = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    assert staged.coarsest_state.masses == pytest.approx(
        direct.masses
    )

    assert staged.coarsest_state.positions[0] == pytest.approx(
        direct.positions[0]
    )


def test_single_transition_hierarchy_matches_direct_builder() -> None:
    """A one-transition hierarchy must reduce to one coarse-state build."""

    partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            0,
            1,
            1,
            1,
            0,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            partition,
        )
    )

    staged = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    direct = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=partition,
    )

    assert staged.state_count == 1
    assert staged.coarsest_state == direct


def test_identity_hierarchy_preserves_positions_and_masses() -> None:
    """Identity transitions must preserve represented state values."""

    first = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
            4,
            5,
        )
    )

    second = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            2,
            3,
            4,
            5,
        )
    )

    hierarchy = MultiscaleHierarchy(
        partitions=(
            first,
            second,
        )
    )

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    expected_positions = tuple(
        tuple(float(component) for component in position)
        for position in _positions()
    )

    expected_masses = tuple(
        float(mass)
        for mass in _masses()
    )

    for state in result.states:
        assert state.positions == expected_positions
        assert state.masses == expected_masses


def test_interleaved_mapping_uses_explicit_membership() -> None:
    """State construction must follow mapping indices, not spatial order."""

    hierarchy = MultiscaleHierarchy(
        partitions=(
            MultiscalePartition(
                fine_to_coarse=(
                    0,
                    1,
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

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    first = result.state_at(1)

    assert first.masses == (
        4.0,
        10.0,
    )

    assert first.positions[0] == pytest.approx(
        (0.0, 2.0, 1.5)
    )

    assert first.positions[1] == pytest.approx(
        (0.6, 2.0, 6.0)
    )


def test_uniform_mass_scaling_preserves_all_coarse_positions() -> None:
    """Uniform positive mass scaling must preserve staged centroids."""

    hierarchy = _three_level_hierarchy()

    original = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    scaled_masses = tuple(
        7.0 * mass
        for mass in _masses()
    )

    scaled = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=scaled_masses,
        hierarchy=hierarchy,
    )

    for original_state, scaled_state in zip(
        original.states,
        scaled.states,
    ):
        for original_position, scaled_position in zip(
            original_state.positions,
            scaled_state.positions,
        ):
            assert original_position == pytest.approx(
                scaled_position
            )


def test_uniform_mass_scaling_scales_all_coarse_masses() -> None:
    """Uniform positive mass scaling propagates through every level."""

    hierarchy = _three_level_hierarchy()

    original = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    scale = 5.0

    scaled = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=tuple(
            scale * mass
            for mass in _masses()
        ),
        hierarchy=hierarchy,
    )

    for original_state, scaled_state in zip(
        original.states,
        scaled.states,
    ):
        assert scaled_state.masses == pytest.approx(
            tuple(
                scale * mass
                for mass in original_state.masses
            )
        )


def test_uniform_translation_propagates_to_every_coarse_level() -> None:
    """Cartesian centroid construction must be translation covariant."""

    hierarchy = _three_level_hierarchy()

    original = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    shift = (
        3.0,
        -2.0,
        5.0,
    )

    translated_positions = tuple(
        (
            position[0] + shift[0],
            position[1] + shift[1],
            position[2] + shift[2],
        )
        for position in _positions()
    )

    translated = build_multiscale_state_hierarchy(
        positions=translated_positions,
        masses=_masses(),
        hierarchy=hierarchy,
    )

    for original_state, translated_state in zip(
        original.states,
        translated.states,
    ):
        for original_position, translated_position in zip(
            original_state.positions,
            translated_state.positions,
        ):
            assert translated_position == pytest.approx(
                (
                    original_position[0] + shift[0],
                    original_position[1] + shift[1],
                    original_position[2] + shift[2],
                )
            )


def test_state_at_maps_level_one_to_first_generated_state() -> None:
    """Level one must address the first generated coarse state."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    assert result.state_at(1) is result.states[0]


def test_state_at_maps_final_level_to_coarsest_state() -> None:
    """The final hierarchy level must address the coarsest state."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    assert result.state_at(3) is result.coarsest_state
    assert result.coarsest_state is result.states[-1]


@pytest.mark.parametrize(
    "invalid_level",
    (
        1.0,
        True,
        False,
        "1",
        None,
    ),
)
def test_state_at_requires_integer_level(
    invalid_level,
) -> None:
    """Generated coarse-state lookup requires a non-Boolean integer."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    with pytest.raises(
        TypeError,
        match="level must be an integer",
    ):
        result.state_at(invalid_level)


@pytest.mark.parametrize(
    "invalid_level",
    (
        -1,
        0,
        4,
        5,
    ),
)
def test_state_at_rejects_unrepresented_coarse_level(
    invalid_level: int,
) -> None:
    """Finest and out-of-range levels have no generated coarse state."""

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=_three_level_hierarchy(),
    )

    with pytest.raises(
        IndexError,
        match="level is out of range for generated coarse states",
    ):
        result.state_at(invalid_level)


def test_state_hierarchy_requires_multiscale_hierarchy() -> None:
    """Direct state-hierarchy construction requires a valid hierarchy."""

    state = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=MultiscalePartition(
            fine_to_coarse=(
                0,
                0,
                1,
                1,
                2,
                2,
            )
        ),
    )

    with pytest.raises(
        TypeError,
        match="hierarchy must be a MultiscaleHierarchy instance",
    ):
        MultiscaleStateHierarchy(
            hierarchy=None,
            states=(
                state,
            ),
        )


def test_state_hierarchy_requires_tuple_states() -> None:
    """Generated states use the canonical tuple container."""

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
                )
            ),
        )
    )

    state = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=hierarchy.partition_at(0),
    )

    with pytest.raises(
        TypeError,
        match="states must be a tuple",
    ):
        MultiscaleStateHierarchy(
            hierarchy=hierarchy,
            states=[
                state,
            ],
        )


def test_state_hierarchy_requires_one_state_per_transition() -> None:
    """Direct construction must cover every hierarchy transition."""

    hierarchy = _three_level_hierarchy()

    with pytest.raises(
        ValueError,
        match=(
            "states must contain one coarse state per "
            "hierarchy transition"
        ),
    ):
        MultiscaleStateHierarchy(
            hierarchy=hierarchy,
            states=(),
        )


def test_state_hierarchy_rejects_excess_states() -> None:
    """Direct construction must not contain states beyond the hierarchy."""

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
                )
            ),
        )
    )

    state = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=hierarchy.partition_at(0),
    )

    with pytest.raises(
        ValueError,
        match=(
            "states must contain one coarse state per "
            "hierarchy transition"
        ),
    ):
        MultiscaleStateHierarchy(
            hierarchy=hierarchy,
            states=(
                state,
                state,
            ),
        )


def test_state_hierarchy_rejects_non_coarse_state_entry() -> None:
    """Every direct state entry must be a CoarseScaleState."""

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
                )
            ),
        )
    )

    with pytest.raises(
        TypeError,
        match=r"states\[0\] must be a CoarseScaleState instance",
    ):
        MultiscaleStateHierarchy(
            hierarchy=hierarchy,
            states=(
                None,
            ),
        )


def test_state_hierarchy_rejects_partition_mismatch() -> None:
    """Each direct state must correspond to its hierarchy transition."""

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
                )
            ),
        )
    )

    different_partition = MultiscalePartition(
        fine_to_coarse=(
            0,
            1,
            0,
            1,
            0,
            1,
        )
    )

    state = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=different_partition,
    )

    with pytest.raises(
        ValueError,
        match=(
            r"states\[0\] partition must match "
            "the corresponding hierarchy transition"
        ),
    ):
        MultiscaleStateHierarchy(
            hierarchy=hierarchy,
            states=(
                state,
            ),
        )


def test_builder_requires_multiscale_hierarchy() -> None:
    """Hierarchy builder rejects objects without hierarchy semantics."""

    with pytest.raises(
        TypeError,
        match="hierarchy must be a MultiscaleHierarchy instance",
    ):
        build_multiscale_state_hierarchy(
            positions=_positions(),
            masses=_masses(),
            hierarchy=None,
        )


def test_builder_propagates_fine_position_cardinality_validation() -> None:
    """Initial position count must match the finest hierarchy level."""

    hierarchy = _three_level_hierarchy()

    with pytest.raises(ValueError):
        build_multiscale_state_hierarchy(
            positions=_positions()[:-1],
            masses=_masses(),
            hierarchy=hierarchy,
        )


def test_builder_propagates_fine_mass_cardinality_validation() -> None:
    """Initial mass count must match the finest hierarchy level."""

    hierarchy = _three_level_hierarchy()

    with pytest.raises(ValueError):
        build_multiscale_state_hierarchy(
            positions=_positions(),
            masses=_masses()[:-1],
            hierarchy=hierarchy,
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
def test_builder_propagates_mass_value_validation(
    invalid_mass: float,
) -> None:
    """Invalid microscopic masses must not enter the hierarchy."""

    hierarchy = _three_level_hierarchy()

    masses = list(_masses())
    masses[0] = invalid_mass

    with pytest.raises(
        (TypeError, ValueError)
    ):
        build_multiscale_state_hierarchy(
            positions=_positions(),
            masses=tuple(masses),
            hierarchy=hierarchy,
        )


@pytest.mark.parametrize(
    "invalid_component",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_builder_propagates_position_finiteness_validation(
    invalid_component: float,
) -> None:
    """Non-finite microscopic coordinates must not enter the hierarchy."""

    hierarchy = _three_level_hierarchy()

    positions = list(_positions())
    positions[0] = (
        invalid_component,
        0.0,
        0.0,
    )

    with pytest.raises(
        (TypeError, ValueError)
    ):
        build_multiscale_state_hierarchy(
            positions=tuple(positions),
            masses=_masses(),
            hierarchy=hierarchy,
        )


def test_builder_normalizes_integer_input_to_float_state_values() -> None:
    """Hierarchy construction retains canonical floating-point state values."""

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

    result = build_multiscale_state_hierarchy(
        positions=(
            (0, 0, 0),
            (2, 0, 0),
            (0, 4, 0),
            (0, 8, 0),
        ),
        masses=(
            1,
            3,
            2,
            2,
        ),
        hierarchy=hierarchy,
    )

    for state in result.states:
        assert all(
            isinstance(mass, float)
            for mass in state.masses
        )

        assert all(
            isinstance(component, float)
            for position in state.positions
            for component in position
        )


def test_coarsest_state_partition_is_final_adjacent_partition() -> None:
    """The final state retains the hierarchy's last adjacent mapping."""

    hierarchy = _three_level_hierarchy()

    result = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    )

    assert (
        result.coarsest_state.partition
        == hierarchy.partition_at(
            hierarchy.transition_count - 1
        )
    )


def test_staged_and_direct_final_states_have_same_physical_values() -> None:
    """Staged and composed routes agree on masses and Cartesian centroids."""

    hierarchy = _three_level_hierarchy()

    staged = build_multiscale_state_hierarchy(
        positions=_positions(),
        masses=_masses(),
        hierarchy=hierarchy,
    ).coarsest_state

    direct = build_coarse_scale_state(
        positions=_positions(),
        masses=_masses(),
        partition=hierarchy.composed_partition(),
    )

    assert staged.masses == pytest.approx(
        direct.masses
    )

    for staged_position, direct_position in zip(
        staged.positions,
        direct.positions,
    ):
        assert staged_position == pytest.approx(
            direct_position
        )
