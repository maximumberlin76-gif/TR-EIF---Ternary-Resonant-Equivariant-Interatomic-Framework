"""Integration tests for deterministic TR-EIF molecular-dynamics neighbor lists."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.neighbor_list import (
    NeighborList,
    build_neighbor_list,
    interaction_graph_from_neighbor_list,
    neighbor_list_requires_rebuild,
)


def _nonperiodic_configuration(
    positions: tuple[tuple[float, float, float], ...],
    species: tuple[str, ...] | None = None,
) -> AtomicConfiguration:
    """Construct a nonperiodic atomic configuration."""

    if species is None:
        species = tuple(
            f"A{index}"
            for index in range(len(positions))
        )

    return AtomicConfiguration(
        species=species,
        positions=positions,
    )


def _periodic_configuration(
    positions: tuple[tuple[float, float, float], ...],
    *,
    cell: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ] = (
        (10.0, 0.0, 0.0),
        (0.0, 10.0, 0.0),
        (0.0, 0.0, 10.0),
    ),
    periodic: tuple[bool, bool, bool] = (
        True,
        True,
        True,
    ),
) -> AtomicConfiguration:
    """Construct a periodic atomic configuration."""

    return AtomicConfiguration(
        species=tuple(
            f"A{index}"
            for index in range(len(positions))
        ),
        positions=positions,
        cell=cell,
        periodic=periodic,
    )


def test_neighbor_list_uses_interaction_cutoff_plus_skin() -> None:
    """Candidate pairs must be selected using cutoff plus skin."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.9, 0.0, 0.0),
            (1.3, 0.0, 0.0),
            (3.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        configuration,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert neighbor_list.interaction_cutoff == 1.0
    assert neighbor_list.skin == 0.5
    assert neighbor_list.search_cutoff == 1.5
    assert neighbor_list.candidate_pairs == (
        (0, 1),
        (0, 2),
        (1, 2),
    )
    assert neighbor_list.candidate_pair_count == 3


def test_neighbor_list_build_is_deterministic() -> None:
    """Repeated construction must produce identical immutable snapshots."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
            (1.4, 0.0, 0.0),
        )
    )

    first = build_neighbor_list(
        configuration,
        interaction_cutoff=1.0,
        skin=0.5,
    )
    second = build_neighbor_list(
        configuration,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert first == second
    assert first.candidate_pairs == second.candidate_pairs


def test_reference_graph_matches_direct_cutoff_graph() -> None:
    """Neighbor-list evaluation must preserve existing cutoff-graph semantics."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.7, 0.0, 0.0),
            (1.3, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        configuration,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    from_neighbor_list = interaction_graph_from_neighbor_list(
        neighbor_list,
        configuration,
    )
    direct = build_cutoff_graph(
        configuration,
        cutoff=1.0,
    )

    assert from_neighbor_list == direct


def test_candidate_outside_interaction_cutoff_is_filtered() -> None:
    """Search-list membership must not imply an active interaction edge."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (1.2, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        configuration,
        interaction_cutoff=1.0,
        skin=0.5,
    )
    graph = interaction_graph_from_neighbor_list(
        neighbor_list,
        configuration,
    )

    assert neighbor_list.candidate_pairs == ((0, 1),)
    assert graph.edge_count == 0


def test_pair_can_enter_cutoff_without_rebuild() -> None:
    """Candidate pairs may enter the interaction cutoff inside the skin envelope."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (1.2, 0.0, 0.0),
        )
    )
    current = _nonperiodic_configuration(
        (
            (0.1, 0.0, 0.0),
            (1.1, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert not neighbor_list_requires_rebuild(
        neighbor_list,
        current,
    )

    graph = interaction_graph_from_neighbor_list(
        neighbor_list,
        current,
    )
    direct = build_cutoff_graph(
        current,
        cutoff=1.0,
    )

    assert graph == direct
    assert graph.edge_count == 2


def test_pair_can_leave_cutoff_without_rebuild() -> None:
    """Active interaction pairs may leave the cutoff inside the skin envelope."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.9, 0.0, 0.0),
        )
    )
    current = _nonperiodic_configuration(
        (
            (-0.1, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert not neighbor_list_requires_rebuild(
        neighbor_list,
        current,
    )

    graph = interaction_graph_from_neighbor_list(
        neighbor_list,
        current,
    )
    direct = build_cutoff_graph(
        current,
        cutoff=1.0,
    )

    assert graph == direct
    assert graph.edge_count == 0


def test_displacement_equal_to_half_skin_does_not_require_rebuild() -> None:
    """The rebuild boundary is strict beyond one half of the skin."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )
    current = _nonperiodic_configuration(
        (
            (0.25, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert not neighbor_list_requires_rebuild(
        neighbor_list,
        current,
    )


def test_displacement_above_half_skin_requires_rebuild() -> None:
    """Movement beyond one half of the skin must invalidate the snapshot."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )
    current = _nonperiodic_configuration(
        (
            (0.250001, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert neighbor_list_requires_rebuild(
        neighbor_list,
        current,
    )


def test_zero_skin_requires_rebuild_after_any_coordinate_change() -> None:
    """A zero-skin list is valid only at its reference coordinates."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        )
    )
    moved = _nonperiodic_configuration(
        (
            (1.0e-12, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.0,
    )

    assert not neighbor_list_requires_rebuild(
        neighbor_list,
        reference,
    )
    assert neighbor_list_requires_rebuild(
        neighbor_list,
        moved,
    )


def test_species_change_requires_rebuild() -> None:
    """Species metadata changes must invalidate the neighbor-list snapshot."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        ),
        species=("Li", "F"),
    )
    changed = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        ),
        species=("Li", "Li"),
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert neighbor_list_requires_rebuild(
        neighbor_list,
        changed,
    )


def test_atom_count_change_requires_rebuild() -> None:
    """Topology-size changes must invalidate the neighbor-list snapshot."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        )
    )
    changed = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
            (1.5, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert neighbor_list_requires_rebuild(
        neighbor_list,
        changed,
    )


def test_periodic_axis_change_requires_rebuild() -> None:
    """Periodic-boundary metadata changes must invalidate the snapshot."""

    reference = _periodic_configuration(
        (
            (0.2, 0.0, 0.0),
            (9.8, 0.0, 0.0),
        )
    )
    changed = _periodic_configuration(
        (
            (0.2, 0.0, 0.0),
            (9.8, 0.0, 0.0),
        ),
        periodic=(
            True,
            False,
            True,
        ),
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=0.5,
        skin=0.2,
    )

    assert neighbor_list_requires_rebuild(
        neighbor_list,
        changed,
    )


def test_cell_change_requires_rebuild() -> None:
    """Simulation-cell changes must invalidate the neighbor-list snapshot."""

    reference = _periodic_configuration(
        (
            (0.2, 0.0, 0.0),
            (9.8, 0.0, 0.0),
        )
    )
    changed = _periodic_configuration(
        (
            (0.2, 0.0, 0.0),
            (9.8, 0.0, 0.0),
        ),
        cell=(
            (11.0, 0.0, 0.0),
            (0.0, 10.0, 0.0),
            (0.0, 0.0, 10.0),
        ),
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=0.5,
        skin=0.2,
    )

    assert neighbor_list_requires_rebuild(
        neighbor_list,
        changed,
    )


def test_periodic_neighbor_graph_matches_direct_minimum_image_graph() -> None:
    """Neighbor-list evaluation must preserve minimum-image graph semantics."""

    configuration = _periodic_configuration(
        (
            (0.2, 0.0, 0.0),
            (9.8, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        configuration,
        interaction_cutoff=0.5,
        skin=0.2,
    )

    from_neighbor_list = interaction_graph_from_neighbor_list(
        neighbor_list,
        configuration,
    )
    direct = build_cutoff_graph(
        configuration,
        cutoff=0.5,
    )

    assert from_neighbor_list == direct
    assert from_neighbor_list.edge_count == 2


def test_periodic_boundary_crossing_uses_minimum_image_displacement() -> None:
    """Wrapped coordinate motion must be measured by periodic minimum image."""

    reference = _periodic_configuration(
        (
            (9.9, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        )
    )
    current = _periodic_configuration(
        (
            (0.1, 0.0, 0.0),
            (5.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    assert not neighbor_list_requires_rebuild(
        neighbor_list,
        current,
    )


def test_stale_neighbor_list_cannot_produce_interaction_graph() -> None:
    """Graph evaluation must reject a snapshot whose rebuild bound was exceeded."""

    reference = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )
    current = _nonperiodic_configuration(
        (
            (0.3, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        )
    )

    neighbor_list = build_neighbor_list(
        reference,
        interaction_cutoff=1.0,
        skin=0.5,
    )

    with pytest.raises(
        ValueError,
        match="Neighbor list must be rebuilt",
    ):
        interaction_graph_from_neighbor_list(
            neighbor_list,
            current,
        )


@pytest.mark.parametrize(
    ("interaction_cutoff", "skin", "exception"),
    (
        (0.0, 0.5, ValueError),
        (-1.0, 0.5, ValueError),
        (float("inf"), 0.5, ValueError),
        (float("nan"), 0.5, ValueError),
        (1.0, -0.1, ValueError),
        (1.0, float("inf"), ValueError),
        (True, 0.5, TypeError),
        (1.0, False, TypeError),
    ),
)
def test_neighbor_list_parameters_are_strictly_validated(
    interaction_cutoff: float,
    skin: float,
    exception: type[Exception],
) -> None:
    """Cutoff and skin must satisfy the declared finite-real contract."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        )
    )

    with pytest.raises(exception):
        build_neighbor_list(
            configuration,
            interaction_cutoff=interaction_cutoff,
            skin=skin,
        )


def test_neighbor_list_rejects_duplicate_candidate_pairs() -> None:
    """Manually supplied candidate pairs must remain unique."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
        )
    )

    with pytest.raises(
        ValueError,
        match="must not contain duplicates",
    ):
        NeighborList(
            interaction_cutoff=1.0,
            skin=0.5,
            reference_configuration=configuration,
            candidate_pairs=(
                (0, 1),
                (0, 1),
            ),
        )


def test_neighbor_list_rejects_noncanonical_candidate_order() -> None:
    """Candidate pairs must use deterministic canonical ordering."""

    configuration = _nonperiodic_configuration(
        (
            (0.0, 0.0, 0.0),
            (0.8, 0.0, 0.0),
            (1.4, 0.0, 0.0),
        )
    )

    with pytest.raises(
        ValueError,
        match="canonical sorted order",
    ):
        NeighborList(
            interaction_cutoff=1.0,
            skin=0.5,
            reference_configuration=configuration,
            candidate_pairs=(
                (1, 2),
                (0, 1),
            ),
        )
