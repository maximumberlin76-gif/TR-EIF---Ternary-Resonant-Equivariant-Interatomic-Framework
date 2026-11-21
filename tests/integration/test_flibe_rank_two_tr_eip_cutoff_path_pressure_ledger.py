
"""Integration qualification of FLiBe rank-two piecewise cutoff MD work.

Reconstruct continuous fixed-graph energy changes and localized cutoff jumps
across scheduled pressure-coupled MD intervals. Compare the path reconstruction
with the established endpoint ledger while retaining separate graph-event,
mechanical, resonance and balanced-ternary execution boundaries.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.flibe.rank_two_tr_eip_cutoff_path_pressure_ledger import (
    FLiBeRankTwoCutoffPathPressureInterval,
    FLiBeRankTwoCutoffPathPressureLedger,
    evaluate_flibe_rank_two_cutoff_path_pressure_ledger,
)
from tr_eif.flibe.rank_two_tr_eip_cutoff_transition_scan import (
    FLiBeCutoffSweepDirection,
)
from tr_eif.ternary import TernaryState

from test_flibe_rank_two_tr_eip_cutoff_pressure_work import (
    aligned,
    graph_event_cases,
)
from test_flibe_rank_two_tr_eip_pressure_coupled_trajectory import (
    prepared_trajectory as prepared_trajectory,
)
from test_flibe_rank_two_tr_eip_pressure_volume_work import (
    qualified_work as qualified_work,
)
from test_flibe_rank_two_tr_eip_stress import CUTOFF, _fixture


ENERGY_ABS = 2.0e-27
CHANNELS = (0, 1, 2)


def _assert_channels(actual, expected, *, absolute=ENERGY_ABS):
    assert len(actual) == len(expected) == 3
    for observed, reference in zip(actual, expected, strict=True):
        assert isfinite(observed)
        assert observed == pytest.approx(reference, rel=2.0e-9, abs=absolute)
    assert actual[2] == pytest.approx(fsum(actual[:2]), rel=2.0e-9, abs=absolute)


def _evaluate(source):
    _, resources = _fixture()
    return evaluate_flibe_rank_two_cutoff_path_pressure_ledger(
        source,
        resources["model"],
        resources["stress_evaluator"],
        cutoff=CUTOFF,
    )


@pytest.fixture(scope="module")
def completed_path_ledger(aligned):
    trajectory, observables, original, cutoff = aligned
    return trajectory, observables, original, cutoff, _evaluate(cutoff)


@pytest.fixture(scope="module")
def forced_path_ledgers(graph_event_cases):
    return {
        scale: (trajectory, original, cutoff, _evaluate(cutoff))
        for scale, (trajectory, original, cutoff) in graph_event_cases.items()
    }


def test_multistep_ledger_identity_and_state_order(completed_path_ledger):
    trajectory, observables, original, cutoff, result = completed_path_ledger
    assert isinstance(result, FLiBeRankTwoCutoffPathPressureLedger)
    assert result.source == cutoff
    assert result.source.source == original
    assert result.source.source.observables == observables
    assert len(result.intervals) == trajectory.interval_count == 3
    assert tuple(item.index for item in result.intervals) == (0, 1, 2)
    assert all(isinstance(item, FLiBeRankTwoCutoffPathPressureInterval)
               for item in result.intervals)
    assert result.crossing_count == sum(item.crossing_count for item in result.intervals)
    assert result.smooth_segment_count == trajectory.interval_count + result.crossing_count
    assert result.directed_edges_added == cutoff.directed_edges_added
    assert result.directed_edges_removed == cutoff.directed_edges_removed
    assert result.crossing_count >= cutoff.graph_event_count


@pytest.mark.parametrize("index", (0, 1, 2))
def test_interval_reconstructs_source_energy_and_geometry(completed_path_ledger, index):
    trajectory, _, original, cutoff, result = completed_path_ledger
    item = result.intervals[index]
    source = cutoff.intervals[index]
    step = trajectory.steps[index].barostat
    assert item.original == source
    assert item.path.scan.reference == source.partition.reference
    assert item.path.scan.target_linear_scale == step.linear_scale
    assert item.path.scan.target_graph == source.partition.graph_after
    assert item.path.segments[0].initial_stress == source.partition.stress_before
    assert item.path.segments[-1].final_stress == source.partition.stress_refreshed_after
    assert item.smooth_segment_count == item.crossing_count + 1
    assert item.path.scan.reference.execution == step.current.ternary_execution
    assert item.path.scan.reference.resonance.resonance_state == step.current.resonance_state
    for segment in item.path.segments:
        assert segment.initial_stress.reference_evaluation.layer.previous == (
            item.path.scan.reference.resonance_features
        )
        assert segment.final_stress.reference_evaluation.layer.previous == (
            item.path.scan.reference.resonance_features
        )
    assert item.path.volume_change * source.coordinate_unit_to_meter**3 == pytest.approx(
        original.intervals[index].volume_change_m3, rel=2e-11, abs=1e-42,
    )
    _assert_channels(item.total_energy_change_j, source.total_energy_change_j)
    assert item.total_energy_change_j[2] == pytest.approx(
        original.intervals[index].affine_potential_change_j, rel=2e-9, abs=ENERGY_ABS,
    )


@pytest.mark.parametrize("index", (0, 1, 2))
def test_independent_energy_and_pressure_work_decomposition(completed_path_ledger, index):
    _, _, _, _, ledger = completed_path_ledger
    item = ledger.intervals[index]
    factor = item.original.energy_unit_to_joule
    segments = item.path.segments
    crossings = item.path.scan.crossings
    smooth = tuple(fsum(segment.potential_energy_change[k] for segment in segments) * factor
                   for k in CHANNELS)
    smooth_work = tuple(fsum(segment.trapezoidal_pressure_work[k] for segment in segments) * factor
                        for k in CHANNELS)
    jumps = tuple(fsum(crossing.energy_jump[k] for crossing in crossings) * factor
                  for k in CHANNELS)
    total = tuple(a + b for a, b in zip(smooth, jumps, strict=True))
    residual = tuple(a - b for a, b in zip(smooth, smooth_work, strict=True))
    _assert_channels(item.smooth_energy_change_j, smooth)
    _assert_channels(item.localized_graph_energy_change_j, jumps)
    _assert_channels(item.total_energy_change_j, total)
    _assert_channels(item.smooth_pressure_work_j, smooth_work)
    _assert_channels(item.smooth_quadrature_residual_j, residual)
    _assert_channels(item.total_pressure_work_residual_j,
                     tuple(a + b for a, b in zip(residual, jumps, strict=True)))
    _assert_channels(item.localized_minus_endpoint_jump_j, tuple(
        a - b for a, b in zip(jumps, item.original.graph_event_energy_change_j, strict=True)
    ))
    _assert_channels(item.original.affine_energy_change_j, tuple(
        a + d for a, d in zip(smooth, item.localized_minus_endpoint_jump_j, strict=True)
    ))


def test_baseline_three_step_schedule_has_no_cutoff_crossing(completed_path_ledger):
    trajectory, _, _, _, ledger = completed_path_ledger
    assert ledger.crossing_count == 0
    assert ledger.smooth_segment_count == trajectory.interval_count
    assert ledger.directed_edges_added == 0
    assert ledger.directed_edges_removed == 0
    assert ledger.localized_graph_energy_change_j == (0.0, 0.0, 0.0)
    assert ledger.localized_minus_endpoint_jump_j == (0.0, 0.0, 0.0)
    for item in ledger.intervals:
        assert item.crossing_count == 0
        assert item.path.scan.crossings == ()
        assert item.smooth_segment_count == 1
        _assert_channels(item.smooth_energy_change_j, item.total_energy_change_j)
        _assert_channels(item.smooth_quadrature_residual_j,
                         item.total_pressure_work_residual_j)


@pytest.mark.parametrize("scale,added,removed,direction", (
    (0.900, 2, 0, FLiBeCutoffSweepDirection.COMPRESSION),
    (1.012, 0, 4, FLiBeCutoffSweepDirection.EXPANSION),
))
def test_forced_cutoff_events_localized_at_critical_scales(
    forced_path_ledgers, scale, added, removed, direction,
):
    trajectory, _, source, ledger = forced_path_ledgers[scale]
    assert trajectory.interval_count == 1
    assert ledger.crossing_count == source.graph_event_count == 1
    assert ledger.smooth_segment_count == 2
    assert ledger.directed_edges_added == added
    assert ledger.directed_edges_removed == removed
    item = ledger.intervals[0]
    assert item.original.has_graph_event
    assert item.crossing_count == 1
    assert item.path.scan.crossings[0].direction is direction
    assert item.path.segments[0].graph == item.path.scan.crossings[0].graph_before
    assert item.path.segments[1].graph == item.path.scan.crossings[0].graph_after
    _assert_channels(item.total_energy_change_j, item.original.total_energy_change_j)
    _assert_channels(item.total_energy_change_j, tuple(
        a + b for a, b in zip(
            item.smooth_energy_change_j, item.localized_graph_energy_change_j,
            strict=True,
        )
    ))
    assert abs(item.localized_graph_energy_change_j[2]) > ENERGY_ABS
    assert abs(item.localized_minus_endpoint_jump_j[2]) > ENERGY_ABS
    assert item.path.scan.crossings[0].linear_scale != scale
    assert item.path.segments[-1].final_linear_scale == pytest.approx(scale, rel=1e-10)


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_graph_event_keeps_pending_active_neutral_and_independent_clocks(
    forced_path_ledgers, scale,
):
    trajectory, original, _, result = forced_path_ledgers[scale]
    first, current = trajectory.states
    assert first.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert current.ternary_execution.has_pending_targets
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in current.ternary_execution.states)
    assert current.ternary_event_count == first.ternary_event_count + 1
    assert current.resonance_step_count == first.resonance_step_count + 1
    assert current.md_state.step == first.md_state.step + 1
    assert current.md_state.masses == first.md_state.masses
    assert result.intervals[0].path.scan.reference.execution == current.ternary_execution
    assert result.intervals[0].path.scan.reference.resonance.resonance_state == current.resonance_state
    assert result.source.source == original


def test_cumulative_signed_energy_work_and_endpoint_reconciliation(completed_path_ledger):
    _, _, original, cutoff, ledger = completed_path_ledger
    fields = (
        "smooth_energy_change_j", "localized_graph_energy_change_j",
        "total_energy_change_j", "smooth_pressure_work_j",
        "smooth_quadrature_residual_j", "total_pressure_work_residual_j",
        "localized_minus_endpoint_jump_j",
    )
    for field in fields:
        _assert_channels(getattr(ledger, field), tuple(
            fsum(getattr(item, field)[k] for item in ledger.intervals)
            for k in CHANNELS
        ))
    _assert_channels(ledger.total_energy_change_j, tuple(
        a + b for a, b in zip(
            ledger.smooth_energy_change_j, ledger.localized_graph_energy_change_j,
            strict=True,
        )
    ))
    _assert_channels(ledger.total_pressure_work_residual_j, tuple(
        a + b for a, b in zip(
            ledger.smooth_quadrature_residual_j, ledger.localized_graph_energy_change_j,
            strict=True,
        )
    ))
    assert ledger.total_energy_change_j[2] == pytest.approx(
        original.affine_potential_change_j, rel=2e-9, abs=ENERGY_ABS,
    )
    assert ledger.crossing_count == sum(item.crossing_count for item in ledger.intervals)
    assert ledger.directed_edges_added == cutoff.directed_edges_added
    assert ledger.directed_edges_removed == cutoff.directed_edges_removed


def test_deterministic_replay_for_cutoff_event(forced_path_ledgers):
    _, _, original, first = forced_path_ledgers[1.012]
    assert _evaluate(original) == first
    assert first.localized_graph_energy_change_j == _evaluate(original).localized_graph_energy_change_j


@pytest.mark.parametrize("field,bad,error", (
    ("index", -1, ValueError),
    ("index", True, TypeError),
    ("index", 1, ValueError),
    ("path", None, TypeError),
    ("original", None, TypeError),
))
def test_interval_rejects_invalid_fields(completed_path_ledger, field, bad, error):
    item = completed_path_ledger[-1].intervals[0]
    with pytest.raises(error):
        replace(item, **{field: bad})


@pytest.mark.parametrize("wrong", ("different_path", "different_source"))
def test_interval_rejects_mismatched_graph_or_source(forced_path_ledgers, wrong):
    compression = forced_path_ledgers[0.900][-1].intervals[0]
    expansion = forced_path_ledgers[1.012][-1].intervals[0]
    changed = {"different_path": {"path": expansion.path},
               "different_source": {"original": expansion.original}}[wrong]
    with pytest.raises(ValueError):
        replace(compression, **changed)


def test_ledger_rejects_inconsistent_order_and_source(completed_path_ledger, forced_path_ledgers):
    ledger = completed_path_ledger[-1]
    with pytest.raises(ValueError):
        replace(ledger, intervals=ledger.intervals[:-1])
    with pytest.raises(ValueError):
        replace(ledger, intervals=tuple(reversed(ledger.intervals)))
    with pytest.raises(ValueError):
        replace(ledger, intervals=(ledger.intervals[0],) * len(ledger.intervals))
    with pytest.raises(TypeError):
        replace(ledger, intervals=(None, *ledger.intervals[1:]))
    with pytest.raises(TypeError):
        replace(ledger, source=None)
    with pytest.raises(ValueError):
        replace(ledger, source=forced_path_ledgers[0.900][-1].source)


@pytest.mark.parametrize("field", ("source", "model", "stress_evaluator"))
def test_operator_rejects_untyped_inputs(completed_path_ledger, field):
    source = completed_path_ledger[3]
    _, resources = _fixture()
    parameters = dict(
        source=source, model=resources["model"],
        stress_evaluator=resources["stress_evaluator"], cutoff=CUTOFF,
    )
    parameters[field] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_path_pressure_ledger(**parameters)


@pytest.mark.parametrize("field,value,error", (
    ("cutoff", 0.0, ValueError),
    ("cutoff", -1.0, ValueError),
    ("cutoff", 1.5, ValueError),
    ("cutoff", True, TypeError),
    ("cutoff", float("nan"), ValueError),
    ("cutoff", float("inf"), ValueError),
    ("probe_relative_width", 0.0, ValueError),
    ("probe_relative_width", 0.001, ValueError),
    ("probe_relative_width", True, TypeError),
))
def test_invalid_operator_cutoff_and_probe_rejected(
    completed_path_ledger, field, value, error,
):
    source = completed_path_ledger[3]
    _, resources = _fixture()
    arguments = dict(
        source=source, model=resources["model"],
        stress_evaluator=resources["stress_evaluator"],
        cutoff=CUTOFF, probe_relative_width=1e-7,
    )
    arguments[field] = value
    with pytest.raises(error):
        evaluate_flibe_rank_two_cutoff_path_pressure_ledger(**arguments)
