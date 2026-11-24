
"""Integration qualification of FLiBe rank-two cutoff quadrature convergence.

Check predeclared convergence decisions, finest-grid accuracy, roundoff
resolution, and independent segment/interval/trajectory error sequences.
Reconstruct all three energy channels from the recorded MD quadrature ledger;
keep cutoff energy jumps and retained balanced-ternary execution unchanged.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite, log2

import pytest

from tr_eif.flibe.rank_two_tr_eip_cutoff_quadrature_convergence import (
    CHANNEL_NAMES,
    FLiBeCutoffConvergenceCriterion,
    FLiBeCutoffConvergenceScope,
    FLiBeCutoffConvergenceSeries,
    FLiBeCutoffConvergenceStatus,
    FLiBeCutoffQuadratureConvergenceQualification,
    evaluate_flibe_rank_two_cutoff_quadrature_convergence,
)
from tr_eif.ternary import TernaryState

# Register every transitive fixture explicitly for full-suite and single-file pytest.
from test_flibe_rank_two_tr_eip_pressure_coupled_trajectory import (
    prepared_trajectory as prepared_trajectory,
)
from test_flibe_rank_two_tr_eip_pressure_volume_work import (
    qualified_work as qualified_work,
)
from test_flibe_rank_two_tr_eip_cutoff_pressure_work import (
    aligned as aligned,
    graph_event_cases as graph_event_cases,
)
from test_flibe_rank_two_tr_eip_cutoff_path_pressure_ledger import (
    completed_path_ledger as completed_path_ledger,
    forced_path_ledgers as forced_path_ledgers,
)
from test_flibe_rank_two_tr_eip_cutoff_path_quadrature_ledger import (
    event_quadratures as event_quadratures,
    multistep_quadrature as multistep_quadrature,
)


CRITERION = FLiBeCutoffConvergenceCriterion(
    finest_error_limit_j=1.0e-19,
    minimum_error_ratio=1.1,
    roundoff_floor_j=1.0e-33,
    required_resolved_pairs=1,
)


def _series(
    errors,
    *,
    criterion=CRITERION,
    scope=FLiBeCutoffConvergenceScope.TRAJECTORY,
    channel="total",
    interval=None,
    segment=None,
):
    return FLiBeCutoffConvergenceSeries(
        scope=scope,
        channel=channel,
        interval_index=interval,
        segment_index=segment,
        errors_j=tuple(errors),
        criterion=criterion,
    )


@pytest.fixture(scope="module")
def qualified_baseline(multistep_quadrature):
    trajectory, source, ledger = multistep_quadrature
    return trajectory, source, ledger, evaluate_flibe_rank_two_cutoff_quadrature_convergence(
        ledger, CRITERION,
    )


@pytest.fixture(scope="module")
def qualified_events(event_quadratures):
    return {
        scale: (trajectory, source, ledger,
                evaluate_flibe_rank_two_cutoff_quadrature_convergence(ledger, CRITERION))
        for scale, (trajectory, source, ledger) in event_quadratures.items()
    }


@pytest.mark.parametrize("field,value,error", (
    ("finest_error_limit_j", 0.0, ValueError),
    ("finest_error_limit_j", True, TypeError),
    ("finest_error_limit_j", float("nan"), ValueError),
    ("finest_error_limit_j", float("inf"), ValueError),
    ("minimum_error_ratio", 1.0, ValueError),
    ("minimum_error_ratio", -1.0, ValueError),
    ("minimum_error_ratio", False, TypeError),
    ("roundoff_floor_j", -1.0, ValueError),
    ("roundoff_floor_j", 1.0e-19, ValueError),
    ("required_resolved_pairs", 0, ValueError),
    ("required_resolved_pairs", True, TypeError),
    ("required_resolved_pairs", 1.5, TypeError),
))
def test_criterion_rejects_invalid_parameters(field, value, error):
    with pytest.raises(error):
        replace(CRITERION, **{field: value})


@pytest.mark.parametrize("errors,limit,ratio,floor,pairs,expected", (
    ((8.0, 2.0, 0.5, 0.125), 0.2, 3.0, 0.001, 2,
     FLiBeCutoffConvergenceStatus.PASS),
    ((8.0, 4.0, 2.0, 1.0), 2.0, 3.0, 0.001, 2,
     FLiBeCutoffConvergenceStatus.FAIL),
    ((8.0, 2.0, 0.5, 0.125), 0.1, 3.0, 0.001, 2,
     FLiBeCutoffConvergenceStatus.FAIL),
    ((1e-12, 1e-12, 1e-12, 1e-12), 1e-9, 3.0, 1e-11, 2,
     FLiBeCutoffConvergenceStatus.INCONCLUSIVE),
    ((8e-9, 2e-9, 2e-12, 1e-12), 1e-10, 3.0, 1e-11, 1,
     FLiBeCutoffConvergenceStatus.PASS),
    ((8.0, 2.0, 1.5, 0.25), 0.3, 3.0, 0.001, 2,
     FLiBeCutoffConvergenceStatus.FAIL),
))
def test_predeclared_status_uses_accuracy_order_and_roundoff(
    errors, limit, ratio, floor, pairs, expected,
):
    criterion = FLiBeCutoffConvergenceCriterion(limit, ratio, floor, pairs)
    record = _series(errors, criterion=criterion)
    assert record.status is expected
    assert record.finest_error_met is (errors[-1] <= limit)
    assert record.resolved_pair_count == sum(r is not None for r in record.refinement_ratios)
    for observed, refinement_ratio in zip(record.observed_orders, record.refinement_ratios):
        if refinement_ratio is None:
            assert observed is None
        else:
            assert observed == pytest.approx(log2(refinement_ratio), rel=1e-13)


def test_second_order_synthetic_reference_has_exact_observed_order():
    criterion = FLiBeCutoffConvergenceCriterion(0.2, 3.0, 0.001, 3)
    result = _series((8.0, 2.0, 0.5, 0.125), criterion=criterion)
    assert result.refinement_ratios == (4.0, 4.0, 4.0)
    assert result.observed_orders == (2.0, 2.0, 2.0)
    assert result.resolved_pair_count == 3
    assert result.status is FLiBeCutoffConvergenceStatus.PASS


def test_roundoff_limited_exact_zero_is_not_execution_neutral():
    criterion = FLiBeCutoffConvergenceCriterion(1e-9, 3.0, 1e-12, 2)
    series = _series((0.0, 0.0, 0.0, 0.0), criterion=criterion)
    assert series.refinement_ratios == (None, None, None)
    assert series.observed_orders == (None, None, None)
    assert series.status is FLiBeCutoffConvergenceStatus.INCONCLUSIVE
    assert series.status not in tuple(TernaryState)


@pytest.mark.parametrize("scope,interval,segment", (
    (FLiBeCutoffConvergenceScope.SEGMENT, 0, 1),
    (FLiBeCutoffConvergenceScope.INTERVAL, 0, None),
    (FLiBeCutoffConvergenceScope.TRAJECTORY, None, None),
))
def test_explicit_scope_identity(scope, interval, segment):
    item = _series((4.0, 1.0), scope=scope, interval=interval, segment=segment)
    assert item.scope is scope
    assert item.interval_index == interval
    assert item.segment_index == segment


@pytest.mark.parametrize("field,value,error", (
    ("scope", "SEGMENT", TypeError),
    ("channel", "temperature", ValueError),
    ("interval_index", -1, ValueError),
    ("interval_index", True, ValueError),
    ("errors_j", (), ValueError),
    ("errors_j", [4.0, 1.0], ValueError),
    ("errors_j", (4.0, float("nan")), ValueError),
    ("errors_j", (4.0, -1.0), ValueError),
    ("errors_j", (4.0, True), TypeError),
    ("criterion", None, TypeError),
))
def test_series_rejects_invalid_inputs(field, value, error):
    with pytest.raises(error):
        replace(_series((4.0, 1.0)), **{field: value})


def test_scope_requires_correct_index_domain():
    with pytest.raises(ValueError):
        _series((4.0, 1.0), scope=FLiBeCutoffConvergenceScope.SEGMENT,
                interval=0, segment=None)
    with pytest.raises(ValueError):
        _series((4.0, 1.0), scope=FLiBeCutoffConvergenceScope.INTERVAL,
                interval=0, segment=1)
    with pytest.raises(ValueError):
        _series((4.0, 1.0), scope=FLiBeCutoffConvergenceScope.TRAJECTORY,
                interval=0)


def test_real_three_interval_series_have_canonical_scope_and_order(qualified_baseline):
    trajectory, source, ledger, result = qualified_baseline
    assert isinstance(result, FLiBeCutoffQuadratureConvergenceQualification)
    assert result.source == ledger
    assert result.criterion == CRITERION
    assert len(result.segment_series) == 3 * sum(
        len(item.source.path.segments) for item in ledger.intervals
    )
    assert len(result.interval_series) == 3 * trajectory.interval_count
    assert len(result.trajectory_series) == 3
    assert tuple(s.channel for s in result.trajectory_series) == CHANNEL_NAMES
    expected_segments = tuple(
        (index, segment, channel)
        for index, item in enumerate(ledger.intervals)
        for segment in range(len(item.source.path.segments))
        for channel in CHANNEL_NAMES
    )
    assert tuple((s.interval_index, s.segment_index, s.channel)
                 for s in result.segment_series) == expected_segments
    assert tuple((s.interval_index, s.channel) for s in result.interval_series) == tuple(
        (index, channel) for index in range(trajectory.interval_count)
        for channel in CHANNEL_NAMES
    )
    assert all(len(s.errors_j) == len(ledger.levels)
               for s in (*result.segment_series, *result.interval_series,
                         *result.trajectory_series))
    assert source == ledger.source


@pytest.mark.parametrize("channel_index", (0, 1, 2))
def test_independent_segment_si_error_reconstruction(qualified_baseline, channel_index):
    _, _, ledger, result = qualified_baseline
    channel_name = CHANNEL_NAMES[channel_index]
    records = tuple(s for s in result.segment_series if s.channel == channel_name)
    expected_records = []
    for index, interval in enumerate(ledger.intervals):
        factor = interval.source.original.energy_unit_to_joule
        for segment_index, segment in enumerate(interval.source.path.segments):
            exact = segment.potential_energy_change[channel_index]
            errors = tuple(
                abs((exact - level.segment_pressure_work[segment_index][channel_index])
                    * factor)
                for level in interval.quadrature.levels
            )
            expected_records.append((index, segment_index, errors))
    for observed, (index, segment_index, expected) in zip(records, expected_records,
                                                          strict=True):
        assert observed.scope is FLiBeCutoffConvergenceScope.SEGMENT
        assert observed.interval_index == index
        assert observed.segment_index == segment_index
        assert observed.errors_j == pytest.approx(expected, rel=1e-12, abs=1e-35)


@pytest.mark.parametrize("channel_index", (0, 1, 2))
def test_independent_interval_and_trajectory_residuals(qualified_baseline, channel_index):
    _, _, ledger, result = qualified_baseline
    for i, interval in enumerate(ledger.intervals):
        observed = next(s for s in result.interval_series
                        if s.interval_index == i and s.channel == CHANNEL_NAMES[channel_index])
        expected = tuple(abs(level.quadrature_residual_j[channel_index])
                         for level in interval.levels)
        assert observed.errors_j == expected
        assert observed.scope is FLiBeCutoffConvergenceScope.INTERVAL
    trajectory = result.trajectory_series[channel_index]
    assert trajectory.scope is FLiBeCutoffConvergenceScope.TRAJECTORY
    assert trajectory.errors_j == tuple(abs(level.quadrature_residual_j[channel_index])
                                        for level in ledger.levels)


@pytest.mark.parametrize("scale,crossings,added,removed", (
    (0.900, 1, 2, 0),
    (1.012, 2, 0, 4),
))
def test_event_series_keep_localized_cutoff_jumps(qualified_events, scale,
                                                    crossings, added, removed):
    trajectory, path_source, ledger, qualified = qualified_events[scale]
    assert trajectory.interval_count == 1
    assert qualified.source == ledger
    assert ledger.crossing_count == crossings
    assert path_source.directed_edges_added == added
    assert path_source.directed_edges_removed == removed
    assert len(qualified.segment_series) == 3 * (crossings + 1)
    assert len(qualified.interval_series) == 3
    assert len(qualified.trajectory_series) == 3
    baseline_jump = ledger.levels[0].localized_graph_energy_j
    assert abs(baseline_jump[2]) > 0.0
    assert qualified.localized_cutoff_energy_j == baseline_jump
    assert all(level.localized_graph_energy_j == baseline_jump for level in ledger.levels)
    assert all(isfinite(error) for item in (*qualified.segment_series,
                                           *qualified.interval_series,
                                           *qualified.trajectory_series)
               for error in item.errors_j)
    assert all(item.status in tuple(FLiBeCutoffConvergenceStatus)
               for item in (*qualified.segment_series, *qualified.interval_series,
                            *qualified.trajectory_series))


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_event_qualification_does_not_change_execution(qualified_events, scale):
    trajectory, path_source, ledger, qualified = qualified_events[scale]
    previous, current = trajectory.states
    assert previous.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert current.ternary_execution.has_pending_targets
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in current.ternary_execution.states)
    assert current.ternary_event_count == previous.ternary_event_count + 1
    assert current.resonance_step_count == previous.resonance_step_count + 1
    assert current.md_state.step == previous.md_state.step + 1
    assert qualified.source is ledger
    assert ledger.source is path_source
    assert ledger.intervals[0].source.path.scan.reference.execution == (
        current.ternary_execution
    )


def test_trajectory_cancellation_is_calculated_from_signed_intervals(qualified_baseline):
    _, _, ledger, qualified = qualified_baseline
    finest = len(ledger.levels) - 1
    expected = tuple(
        abs(ledger.levels[finest].quadrature_residual_j[k]) <= CRITERION.finest_error_limit_j
        and fsum(abs(item.levels[finest].quadrature_residual_j[k])
                 for item in ledger.intervals) > CRITERION.finest_error_limit_j
        for k in range(3)
    )
    assert qualified.cancellation_flags == expected
    assert len(qualified.cancellation_flags) == 3


def test_local_failure_cannot_be_hidden_by_good_total(qualified_baseline):
    _, _, ledger, source = qualified_baseline
    failed_local = replace(source.interval_series[0], errors_j=(1e-8, 1e-8, 1e-8, 1e-8))
    guarded = replace(source, interval_series=(failed_local, *source.interval_series[1:]))
    assert failed_local.status is FLiBeCutoffConvergenceStatus.FAIL
    assert guarded.status is FLiBeCutoffConvergenceStatus.FAIL
    assert guarded.source is ledger
    assert guarded.trajectory_series == source.trajectory_series


def test_trajectory_accuracy_is_required_independently_of_local_ratios(qualified_baseline):
    _, _, _, source = qualified_baseline
    failing = replace(source.trajectory_series[2], errors_j=(1e-18,) * 4)
    guarded = replace(source, trajectory_series=(*source.trajectory_series[:2], failing))
    assert not failing.finest_error_met
    assert guarded.status is FLiBeCutoffConvergenceStatus.FAIL


def test_deterministic_qualification_without_resampling(qualified_baseline):
    _, _, ledger, result = qualified_baseline
    assert evaluate_flibe_rank_two_cutoff_quadrature_convergence(ledger, CRITERION) == result
    assert result.status in tuple(FLiBeCutoffConvergenceStatus)


@pytest.mark.parametrize("field", ("source", "criterion"))
def test_operator_rejects_untyped_inputs(qualified_baseline, field):
    _, _, ledger, _ = qualified_baseline
    kwargs = dict(source=ledger, criterion=CRITERION)
    kwargs[field] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_quadrature_convergence(**kwargs)


def test_required_refinement_pairs_cannot_exceed_source_levels(qualified_baseline):
    _, _, ledger, _ = qualified_baseline
    criterion = replace(CRITERION, required_resolved_pairs=4)
    with pytest.raises(ValueError, match="fewer levels"):
        evaluate_flibe_rank_two_cutoff_quadrature_convergence(ledger, criterion)


@pytest.mark.parametrize("field,error", (
    ("segment_series", ValueError),
    ("interval_series", ValueError),
    ("trajectory_series", ValueError),
    ("source", TypeError),
    ("criterion", TypeError),
))
def test_qualification_rejects_missing_record_domains(qualified_baseline, field, error):
    record = qualified_baseline[-1]
    value = None if field in ("source", "criterion") else ()
    with pytest.raises(error):
        replace(record, **{field: value})


def test_qualification_rejects_reordered_and_mismatched_channels(qualified_baseline):
    record = qualified_baseline[-1]
    with pytest.raises(ValueError):
        replace(record, segment_series=tuple(reversed(record.segment_series)))
    with pytest.raises(ValueError):
        replace(record, interval_series=tuple(reversed(record.interval_series)))
    with pytest.raises(ValueError):
        replace(record, trajectory_series=tuple(reversed(record.trajectory_series)))
    with pytest.raises(ValueError):
        replace(record, segment_series=(None, *record.segment_series[1:]))
    with pytest.raises(ValueError):
        replace(record, trajectory_series=(
            replace(record.trajectory_series[0], channel="rank_two"),
            *record.trajectory_series[1:],
        ))
