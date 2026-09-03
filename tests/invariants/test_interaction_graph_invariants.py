"""Qualification tests for TR-EIF interaction-graph invariants."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.graph import (
    InteractionEdge,
    InteractionGraph,
    build_cutoff_graph,
    evaluate_edge_geometry,
)


def test_cutoff_graph_construction_is_deterministic() -> None:
    """Identical configurations must produce identical interaction graphs."""

    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        ),
    )

    first = build_cutoff_graph(
        configuration=configuration,
        cutoff=1.5,
    )

    second = build_cutoff_graph(
        configuration=configuration,
        cutoff=1.5,
    )

    assert first == second

    assert first.edges == (
        InteractionEdge(source=0, receiver=1),
        InteractionEdge(source=0, receiver=2),
        InteractionEdge(source=1, receiver=0),
        InteractionEdge(source=1, receiver=2),
        InteractionEdge(source=2, receiver=0),
        InteractionEdge(source=2, receiver=1),
    )


def test_cutoff_graph_contains_no_self_edges() -> None:
    """Cutoff construction must exclude source-to-self interactions."""

    configuration = AtomicConfiguration(
        species=("A", "B", "C"),
        positions=(
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.0, 0.5, 0.0),
        ),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    assert graph.edge_count == 6

    for edge in graph.edges:
        assert edge.source != edge.receiver


def test_interaction_graph_rejects_duplicate_directed_edges() -> None:
    """The immutable graph must reject duplicate directed edge records."""

    edge = InteractionEdge(
        source=0,
        receiver=1,
        image=(0, 0, 0),
    )

    with pytest.raises(
        ValueError,
        match="must not contain duplicate directed edges",
    ):
        InteractionGraph(
            node_count=2,
            edges=(
                edge,
                edge,
            ),
        )


def test_periodic_cutoff_graph_records_explicit_image_indices() -> None:
    """Periodic neighbors must retain the image selected by wrapping."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.1, 0.0, 0.0),
            (3.9, 0.0, 0.0),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(True, True, True),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=0.5,
    )

    assert graph.edges == (
        InteractionEdge(
            source=0,
            receiver=1,
            image=(-1, 0, 0),
        ),
        InteractionEdge(
            source=1,
            receiver=0,
            image=(1, 0, 0),
        ),
    )


def test_periodic_edge_geometry_matches_recorded_image() -> None:
    """Edge geometry must evaluate the explicitly recorded periodic image."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.1, 0.0, 0.0),
            (3.9, 0.0, 0.0),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(True, True, True),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=0.5,
    )

    forward = evaluate_edge_geometry(
        configuration,
        graph.edges[0],
    )

    reverse = evaluate_edge_geometry(
        configuration,
        graph.edges[1],
    )

    assert forward.displacement == pytest.approx(
        (-0.2, 0.0, 0.0),
    )
    assert forward.distance == pytest.approx(0.2)
    assert forward.unit_direction == pytest.approx(
        (-1.0, 0.0, 0.0),
    )

    assert reverse.displacement == pytest.approx(
        (0.2, 0.0, 0.0),
    )
    assert reverse.distance == pytest.approx(0.2)
    assert reverse.unit_direction == pytest.approx(
        (1.0, 0.0, 0.0),
    )


def test_periodic_reverse_edges_have_opposite_images() -> None:
    """Reverse periodic edges must carry opposite image indices."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.1, 0.0, 0.0),
            (3.9, 0.0, 0.0),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(True, True, True),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=0.5,
    )

    forward = graph.edges[0]
    reverse = graph.edges[1]

    assert forward.source == reverse.receiver
    assert forward.receiver == reverse.source

    assert reverse.image == tuple(
        -component
        for component in forward.image
    )


def test_cutoff_boundary_is_inclusive() -> None:
    """An interaction exactly at the radial cutoff must be included."""

    configuration = AtomicConfiguration(
        species=("A", "B"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=1.0,
    )

    assert graph.edges == (
        InteractionEdge(source=0, receiver=1),
        InteractionEdge(source=1, receiver=0),
    )
