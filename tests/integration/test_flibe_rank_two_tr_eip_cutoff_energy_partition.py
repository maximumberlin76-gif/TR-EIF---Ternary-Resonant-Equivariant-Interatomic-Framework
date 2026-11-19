
"""Integration qualification of FLiBe rank-two cutoff energy partitioning.

Independently reconstruct affine and graph-event energy changes for the
reference and rank-two channels, distinguish edge addition from removal,
and check frozen resonance features, retained ternary states, active-neutral
pending routes, E(3) covariance and rejection of inconsistent records.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.equivariant import E3Transformation
from tr_eif.flibe.rank_two_tr_eip_cutoff_energy_partition import (
    FLiBeRankTwoTREIPCutoffEnergyPartition,
    evaluate_flibe_rank_two_cutoff_energy_partition,
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


SCALES = (
    (0.900, 2, 0),
    (0.988, 0, 0),
    (1.000, 0, 0),
    (1.006, 0, 0),
    (1.012, 0, 4),
)
STATES = (
    TernaryState.NEGATIVE,
    TernaryState.NEUTRAL,
    TernaryState.POSITIVE,
)


def _channels(result):
    return (
        result.reference_energy.total_energy,
        result.tensor_energy.total_energy,
        result.energy.total_energy,
    )


def _pressures(stress):
    return (
        -sum(stress.reference_stress.tensor[a][a] for a in range(3)) / 3.0,
        -sum(stress.tensor_stress.tensor[a][a] for a in range(3)) / 3.0,
        -sum(stress.total_stress.tensor[a][a] for a in range(3)) / 3.0,
    )


def _matrix_transform(tensor, rotation):
    return tuple(tuple(
        sum(rotation[i][a] * tensor[a][b] * rotation[j][b]
            for a in range(3) for b in range(3))
        for j in range(3)) for i in range(3))


def _source(retained, *, pending=False, transform=None):
    initial, resources = _fixture(initial=retained, transform=transform)
    if pending:
        assert retained is TernaryState.NEUTRAL
        execution = TernaryExecutionVector(states=tuple(
            TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE)
            for _ in initial.ternary_execution.states
        ))
        initial = replace(initial, ternary_execution=execution)
    reference = _single_stress(initial, resources)
    return initial, resources, reference.evaluation


def _partition(source, scale):
    _, resources, reference = source
    return evaluate_flibe_rank_two_cutoff_energy_partition(
        resources["model"], resources["stress_evaluator"], reference,
        cutoff=CUTOFF, linear_scale=scale,
    )


@pytest.fixture(scope="module")
def cases():
    results = {}
    for state in STATES:
        source = _source(state)
        for scale, _, _ in SCALES:
            results[(state, scale)] = _partition(source, scale)
    return results


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale,added,removed", SCALES)
def test_cutoff_edge_delta_and_frozen_execution(cases, retained, scale, added, removed):
    partition = cases[(retained, scale)]
    assert isinstance(partition, FLiBeRankTwoTREIPCutoffEnergyPartition)
    assert partition.linear_scale == scale
    assert partition.cutoff == CUTOFF
    assert partition.graph_before == partition.reference.graph
    assert partition.graph_after == build_cutoff_graph(
        partition.scaled_configuration, CUTOFF,
    )
    assert partition.scaled_configuration == scale_periodic_configuration(
        partition.reference.configuration.configuration, scale,
    )
    assert partition.graph_before.node_count == partition.graph_after.node_count == 7
    assert len(partition.added_edges) == added
    assert len(partition.removed_edges) == removed
    assert partition.has_graph_event is (added + removed > 0)
    assert partition.graph_after.edge_count == (
        partition.graph_before.edge_count + added - removed
    )
    assert set(partition.added_edges) == (
        set(partition.graph_after.edges) - set(partition.graph_before.edges)
    )
    assert set(partition.removed_edges) == (
        set(partition.graph_before.edges) - set(partition.graph_after.edges)
    )
    assert partition.reference.execution.retained_states == (retained,) * 7
    assert partition.frozen_energy.layer.previous == partition.reference.resonance_features
    assert partition.refreshed_energy.layer.previous == partition.reference.resonance_features
    assert partition.stress_frozen_after.reference_evaluation == partition.frozen_energy
    assert partition.stress_refreshed_after.reference_evaluation == partition.refreshed_energy
    assert partition.stress_frozen_after.reference_volume == pytest.approx(
        partition.stress_before.reference_volume * scale**3, rel=1e-12,
    )
    assert partition.stress_refreshed_after.reference_volume == pytest.approx(
        partition.stress_frozen_after.reference_volume, rel=1e-12,
    )
    if not partition.has_graph_event:
        assert partition.graph_event_energy_change == (0.0, 0.0, 0.0)
        assert partition.stress_frozen_after == partition.stress_refreshed_after


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale,added,removed", SCALES)
def test_independent_energy_partition_and_pressure_work(cases, retained, scale, added, removed):
    partition = cases[(retained, scale)]
    start = _channels(partition.reference.augmented_result)
    frozen = _channels(partition.frozen_energy)
    refreshed = _channels(partition.refreshed_energy)
    first_pressure = _pressures(partition.stress_before)
    second_pressure = _pressures(partition.stress_frozen_after)
    delta_volume = partition.stress_frozen_after.reference_volume - partition.stress_before.reference_volume

    for index in range(3):
        affine = frozen[index] - start[index]
        event = refreshed[index] - frozen[index]
        total = refreshed[index] - start[index]
        work = -0.5 * (first_pressure[index] + second_pressure[index]) * delta_volume
        assert partition.affine_energy_change[index] == pytest.approx(affine, abs=1e-12)
        assert partition.graph_event_energy_change[index] == pytest.approx(event, abs=1e-12)
        assert partition.total_energy_change[index] == pytest.approx(total, abs=1e-12)
        assert partition.frozen_graph_pressure_work[index] == pytest.approx(work, abs=1e-12)
        assert partition.frozen_graph_quadrature_residual[index] == pytest.approx(
            affine - work, abs=1e-12,
        )
        assert partition.full_pressure_work_residual[index] == pytest.approx(
            total - work, abs=1e-12,
        )
        assert partition.full_pressure_work_residual[index] == pytest.approx(
            fsum((partition.frozen_graph_quadrature_residual[index], event)), abs=1e-12,
        )
    for triple in (
        partition.affine_energy_change,
        partition.graph_event_energy_change,
        partition.total_energy_change,
        partition.frozen_graph_pressure_work,
        partition.frozen_graph_quadrature_residual,
        partition.full_pressure_work_residual,
    ):
        assert all(isfinite(value) for value in triple)
        assert triple[2] == pytest.approx(fsum(triple[:2]), abs=1e-9)
    if scale == 1.0:
        assert partition.volume_change == 0.0
        assert partition.affine_energy_change == (0.0, 0.0, 0.0)
        assert partition.frozen_graph_pressure_work == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("scale", (0.9, 1.012))
def test_active_neutral_pending_does_not_change_energy_or_graph_event(scale):
    bare = _partition(_source(TernaryState.NEUTRAL), scale)
    pending = _partition(_source(TernaryState.NEUTRAL, pending=True), scale)
    assert bare.reference.execution.retained_states == pending.reference.execution.retained_states
    assert not bare.reference.execution.has_pending_targets
    assert pending.reference.execution.has_pending_targets
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in pending.reference.execution.states)
    assert bare.graph_before == pending.graph_before
    assert bare.graph_after == pending.graph_after
    assert bare.affine_energy_change == pytest.approx(pending.affine_energy_change, abs=1e-12)
    assert bare.graph_event_energy_change == pytest.approx(
        pending.graph_event_energy_change, abs=1e-12,
    )
    assert bare.total_energy_change == pytest.approx(pending.total_energy_change, abs=1e-12)
    assert bare.frozen_graph_pressure_work == pytest.approx(
        pending.frozen_graph_pressure_work, abs=1e-12,
    )
    assert bare.stress_before.total_stress == pending.stress_before.total_stress
    assert bare.stress_refreshed_after.total_stress == pending.stress_refreshed_after.total_stress


@pytest.mark.parametrize("scale", (0.9, 1.012))
@pytest.mark.parametrize("matrix", (ROTATION, REFLECTION))
def test_e3_energy_invariance_and_stress_covariance(scale, matrix):
    original = _partition(_source(TernaryState.NEUTRAL), scale)
    transformed = _partition(_source(
        TernaryState.NEUTRAL, transform=E3Transformation(matrix)
    ), scale)
    assert transformed.has_graph_event == original.has_graph_event
    assert transformed.graph_after.edge_count == original.graph_after.edge_count
    assert transformed.reference.execution == original.reference.execution
    assert transformed.volume_change == pytest.approx(original.volume_change, rel=1e-10, abs=1e-11)
    for name in (
        "affine_energy_change", "graph_event_energy_change", "total_energy_change",
        "frozen_graph_pressure_work", "frozen_graph_quadrature_residual",
        "full_pressure_work_residual",
    ):
        assert getattr(transformed, name) == pytest.approx(
            getattr(original, name), rel=5e-4, abs=4e-5,
        )
    for field in ("stress_before", "stress_frozen_after", "stress_refreshed_after"):
        left = getattr(original, field)
        right = getattr(transformed, field)
        for channel in ("reference_stress", "tensor_stress", "total_stress"):
            expected = _matrix_transform(getattr(left, channel).tensor, matrix)
            for actual_row, expected_row in zip(getattr(right, channel).tensor, expected, strict=True):
                assert actual_row == pytest.approx(expected_row, rel=5e-4, abs=4e-5)


def test_deterministic_replay_and_graph_event_identity():
    source = _source(TernaryState.NEUTRAL)
    first = _partition(source, 1.012)
    second = _partition(source, 1.012)
    assert first == second
    assert first.has_graph_event
    assert first.removed_edges
    assert not first.added_edges
    assert first.refreshed_energy != first.frozen_energy


@pytest.mark.parametrize("parameter,value,error", (
    ("linear_scale", 0.0, ValueError),
    ("linear_scale", -1.0, ValueError),
    ("linear_scale", float("nan"), ValueError),
    ("linear_scale", True, TypeError),
    ("cutoff", 0.0, ValueError),
    ("cutoff", float("inf"), ValueError),
    ("cutoff", False, TypeError),
    ("cutoff", 1.5, ValueError),
))
def test_invalid_cutoff_and_scale_rejected(parameter, value, error):
    state, resources, reference = _source(TernaryState.NEUTRAL)
    options = dict(cutoff=CUTOFF, linear_scale=1.012)
    options[parameter] = value
    with pytest.raises(error):
        evaluate_flibe_rank_two_cutoff_energy_partition(
            resources["model"], resources["stress_evaluator"], reference, **options,
        )


@pytest.mark.parametrize("which", ("model", "stress_evaluator", "reference"))
def test_untyped_inputs_rejected(which):
    _, resources, reference = _source(TernaryState.NEUTRAL)
    inputs = dict(model=resources["model"],
                  stress_evaluator=resources["stress_evaluator"], reference=reference)
    inputs[which] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_energy_partition(
            **inputs, cutoff=CUTOFF, linear_scale=1.012,
        )


@pytest.mark.parametrize("field", (
    "scaled_configuration", "graph_after", "graph_before",
    "frozen_energy", "refreshed_energy", "stress_frozen_after",
    "stress_refreshed_after", "stress_before",
))
def test_corrupted_partition_boundaries_rejected(field):
    result = _partition(_source(TernaryState.NEUTRAL), 1.012)
    substitutions = {
        "scaled_configuration": result.reference.configuration.configuration,
        "graph_after": result.graph_before,
        "graph_before": result.graph_after,
        "frozen_energy": result.refreshed_energy,
        "refreshed_energy": result.frozen_energy,
        "stress_frozen_after": result.stress_before,
        "stress_refreshed_after": result.stress_before,
        "stress_before": result.stress_refreshed_after,
    }
    with pytest.raises(ValueError):
        replace(result, **{field: substitutions[field]})
