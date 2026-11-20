
"""Integration qualification of analytic FLiBe rank-two cutoff crossings.

Verify radial crossing scales, directed graph events and full-energy jumps
at identical boundary geometry. Keep the continuous resonance features and
retained balanced-ternary execution fixed across each graph replacement.
"""

from __future__ import annotations

from dataclasses import replace
from math import dist, fsum, isfinite

import pytest

from tr_eif.equivariant import E3Transformation
from tr_eif.flibe.rank_two_tr_eip_cutoff_transition_scan import (
    FLiBeCutoffSweepDirection,
    FLiBeRankTwoCutoffCrossing,
    FLiBeRankTwoCutoffTransitionScan,
    locate_flibe_rank_two_cutoff_transitions,
)
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.barostat import scale_periodic_configuration
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)

from test_flibe_rank_two_tr_eip_stress import (
    CUTOFF,
    REFLECTION,
    ROTATION,
    _fixture,
    _single_stress,
)

STATES = (TernaryState.NEGATIVE, TernaryState.NEUTRAL, TernaryState.POSITIVE)
CASES = (
    (0.900, 1, 2, 0, 0.9161573349021892),
    (0.988, 0, 0, 0, None),
    (1.000, 0, 0, 0, None),
    (1.003, 0, 0, 0, None),
    (1.006, 0, 0, 0, None),
    (1.012, 1, 0, 4, 1.0099110449564852),
)


def _inputs(state=TernaryState.NEUTRAL, *, pending=False, transform=None):
    initial, resources = _fixture(initial=state, transform=transform)
    if pending:
        assert state is TernaryState.NEUTRAL
        execution = TernaryExecutionVector(states=tuple(
            TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE)
            for _ in initial.ternary_execution.states
        ))
        initial = replace(initial, ternary_execution=execution)
    reference = _single_stress(initial, resources).evaluation
    return initial, resources, reference


def _scan(source, target, **overrides):
    _, resources, reference = source
    args = dict(cutoff=CUTOFF, target_linear_scale=target)
    args.update(overrides)
    return locate_flibe_rank_two_cutoff_transitions(
        resources["model"], reference, **args,
    )


def _channels(result):
    return (result.reference_energy.total_energy,
            result.tensor_energy.total_energy, result.energy.total_energy)


@pytest.fixture(scope="module")
def matrix():
    return {
        (state, target): _scan(_inputs(state), target)
        for state in STATES for target, *_ in CASES
    }


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("target,count,added,removed,critical", CASES)
def test_crossing_count_direction_and_target_graph(
    matrix, state, target, count, added, removed, critical,
):
    scan = matrix[state, target]
    assert isinstance(scan, FLiBeRankTwoCutoffTransitionScan)
    assert scan.crossing_count == count
    assert scan.directed_edges_added == added
    assert scan.directed_edges_removed == removed
    assert scan.target_linear_scale == target
    assert scan.reference.execution.retained_states == (state,) * 7
    assert scan.target_graph == build_cutoff_graph(
        scale_periodic_configuration(scan.reference.configuration.configuration, target),
        CUTOFF,
    )
    assert set(scan.target_graph.edges) == (
        (set(scan.reference.graph.edges)
         - {edge for event in scan.crossings for edge in event.removed_edges})
        | {edge for event in scan.crossings for edge in event.added_edges}
    )
    if critical is None:
        assert scan.crossings == ()
        assert scan.localized_energy_jumps == (0.0, 0.0, 0.0)
    else:
        crossing = scan.crossings[0]
        assert isinstance(crossing, FLiBeRankTwoCutoffCrossing)
        assert crossing.linear_scale == pytest.approx(critical, rel=1e-12)
        assert crossing.direction is (
            FLiBeCutoffSweepDirection.COMPRESSION if target < 1.0
            else FLiBeCutoffSweepDirection.EXPANSION
        )
        assert crossing.graph_before != crossing.graph_after
        assert crossing.energy_jump[2] != pytest.approx(0.0, abs=1e-6)


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("target", (0.900, 1.012))
def test_analytic_distances_and_reciprocal_edge_inventory(matrix, state, target):
    scan = matrix[state, target]
    initial = scan.reference.configuration.configuration
    event = scan.crossings[0]
    observed = event.added_edges or event.removed_edges
    expected_pairs = {(0, 6), (6, 0)} if target < 1.0 else {
        (3, 5), (5, 3), (5, 6), (6, 5),
    }
    assert {(edge.source, edge.receiver) for edge in observed} == expected_pairs
    assert all(edge.image == (0, 0, 0) for edge in observed)
    for edge in observed:
        independent_distance = dist(
            initial.positions[edge.source], initial.positions[edge.receiver],
        )
        assert event.linear_scale == pytest.approx(
            CUTOFF / independent_distance, rel=2e-13,
        )
    assert event.boundary_configuration == scale_periodic_configuration(
        initial, event.linear_scale,
    )
    assert event.probe_before_scale != event.probe_after_scale
    assert event.graph_before == build_cutoff_graph(
        scale_periodic_configuration(initial, event.probe_before_scale), CUTOFF,
    )
    assert event.graph_after == build_cutoff_graph(
        scale_periodic_configuration(initial, event.probe_after_scale), CUTOFF,
    )


@pytest.mark.parametrize("state", STATES)
@pytest.mark.parametrize("target", (0.900, 1.012))
def test_independent_boundary_energies_and_channel_partition(matrix, state, target):
    scan = matrix[state, target]
    _, resources, reference = _inputs(state)
    event = scan.crossings[0]
    model = resources["model"].rank_two_model
    before = model.evaluate(
        event.boundary_configuration, event.graph_before,
        reference.resonance_features, reference.execution,
    )
    after = model.evaluate(
        event.boundary_configuration, event.graph_after,
        reference.resonance_features, reference.execution,
    )
    assert before == event.energy_before
    assert after == event.energy_after
    assert before.layer.previous == after.layer.previous == reference.resonance_features
    expected = tuple(b - a for a, b in zip(
        _channels(before), _channels(after), strict=True,
    ))
    assert event.energy_jump == pytest.approx(expected, abs=2e-12)
    assert expected[2] == pytest.approx(fsum(expected[:2]), abs=2e-12)
    assert scan.localized_energy_jumps == pytest.approx(expected, abs=2e-12)
    assert all(isfinite(value) for value in expected)
    final_geometry = scale_periodic_configuration(
        reference.configuration.configuration, target,
    )
    end_frozen = model.evaluate(
        final_geometry, reference.graph, reference.resonance_features,
        reference.execution,
    )
    end_refreshed = model.evaluate(
        final_geometry, scan.target_graph, reference.resonance_features,
        reference.execution,
    )
    endpoint_jump = end_refreshed.energy.total_energy - end_frozen.energy.total_energy
    assert endpoint_jump != pytest.approx(expected[2], abs=1e-4)


@pytest.mark.parametrize("target", (0.900, 1.012))
@pytest.mark.parametrize("probe", (1e-5, 1e-6, 1e-8))
def test_probe_refinement_preserves_critical_geometry_and_energy(target, probe):
    source = _inputs()
    standard = _scan(source, target)
    refined = _scan(source, target, probe_relative_width=probe)
    assert refined.crossing_count == standard.crossing_count == 1
    a, b = standard.crossings[0], refined.crossings[0]
    assert refined.probe_relative_width == probe
    assert b.linear_scale == a.linear_scale
    assert b.boundary_configuration == a.boundary_configuration
    assert b.added_edges == a.added_edges
    assert b.removed_edges == a.removed_edges
    assert b.energy_jump == pytest.approx(a.energy_jump, abs=2e-12)


@pytest.mark.parametrize("target", (0.900, 1.012))
def test_neutral_pending_target_does_not_change_cutoff_events(target):
    plain = _scan(_inputs(), target)
    pending = _scan(_inputs(pending=True), target)
    assert not plain.reference.execution.has_pending_targets
    assert pending.reference.execution.has_pending_targets
    assert pending.reference.execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in pending.reference.execution.states)
    assert pending.target_graph == plain.target_graph
    assert pending.directed_edges_added == plain.directed_edges_added
    assert pending.directed_edges_removed == plain.directed_edges_removed
    assert pending.crossings[0].linear_scale == plain.crossings[0].linear_scale
    assert pending.crossings[0].energy_jump == pytest.approx(
        plain.crossings[0].energy_jump, abs=2e-12,
    )
    assert pending.reference.resonance.resonance_state == plain.reference.resonance.resonance_state


@pytest.mark.parametrize("target", (0.900, 1.012))
@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (1.0, -2.0, 0.5)),
    (REFLECTION, (-0.75, 0.25, 1.0)),
))
def test_e3_crossing_scale_and_energy_invariance(target, matrix, translation):
    reference = _scan(_inputs(), target)
    transformed = _scan(_inputs(transform=E3Transformation(matrix, translation)), target)
    a, b = reference.crossings[0], transformed.crossings[0]
    assert b.linear_scale == pytest.approx(a.linear_scale, rel=2e-12)
    assert set(b.added_edges) == set(a.added_edges)
    assert set(b.removed_edges) == set(a.removed_edges)
    assert b.energy_jump == pytest.approx(a.energy_jump, rel=2e-10, abs=2e-9)
    for position, changed in zip(
        a.boundary_configuration.positions, b.boundary_configuration.positions,
        strict=True,
    ):
        expected = tuple(
            sum(matrix[i][j] * position[j] for j in range(3))
            + b.linear_scale * translation[i]
            for i in range(3)
        )
        assert changed == pytest.approx(expected, rel=1e-12, abs=2e-12)


def test_exact_replay_with_identical_parameters():
    source = _inputs()
    first = _scan(source, 0.900)
    second = _scan(source, 0.900)
    assert first == second
    assert first.crossings[0].energy_before == second.crossings[0].energy_before
    assert first.crossings[0].energy_after == second.crossings[0].energy_after


@pytest.mark.parametrize("key,value,error", (
    ("cutoff", 0.0, ValueError),
    ("cutoff", 1.5, ValueError),
    ("cutoff", True, TypeError),
    ("cutoff", float("inf"), ValueError),
    ("target_linear_scale", -0.1, ValueError),
    ("target_linear_scale", False, TypeError),
    ("target_linear_scale", float("nan"), ValueError),
    ("probe_relative_width", 0.0, ValueError),
    ("probe_relative_width", 0.001, ValueError),
    ("probe_relative_width", True, TypeError),
))
def test_invalid_cutoff_scan_parameters_are_rejected(key, value, error):
    source = _inputs()
    options = dict(cutoff=CUTOFF, target_linear_scale=0.900)
    options[key] = value
    with pytest.raises(error):
        locate_flibe_rank_two_cutoff_transitions(
            source[1]["model"], source[2], **options,
        )


@pytest.mark.parametrize("key", ("model", "reference"))
def test_untyped_model_and_reference_are_rejected(key):
    source = _inputs()
    args = dict(model=source[1]["model"], reference=source[2])
    args[key] = None
    with pytest.raises(TypeError):
        locate_flibe_rank_two_cutoff_transitions(
            **args, cutoff=CUTOFF, target_linear_scale=0.900,
        )


def test_crossing_and_scan_reject_corrupted_boundaries():
    scan = _scan(_inputs(), 0.900)
    event = scan.crossings[0]
    with pytest.raises(ValueError):
        replace(scan, crossings=())
    with pytest.raises(ValueError):
        replace(scan, target_graph=scan.reference.graph)
    with pytest.raises(ValueError):
        replace(event, added_edges=())
    with pytest.raises(ValueError):
        replace(event, probe_before_scale=event.probe_after_scale)
    with pytest.raises(ValueError):
        replace(event, direction=FLiBeCutoffSweepDirection.EXPANSION)
    with pytest.raises(ValueError):
        replace(event, energy_before=event.energy_after)
