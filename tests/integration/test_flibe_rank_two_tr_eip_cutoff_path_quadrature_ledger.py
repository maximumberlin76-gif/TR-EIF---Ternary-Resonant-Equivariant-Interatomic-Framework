
"""Integration qualification of FLiBe rank-two cutoff quadrature ledgers.

Reconstruct SI pressure work and energy changes across multirate MD intervals.
Keep smooth fixed-graph work, localized graph jumps, and quadrature residuals
separate at every refinement level. Verify the three energy channels, active
neutral pending routes, unchanged execution clocks, and deterministic replay.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.flibe.rank_two_tr_eip_cutoff_path_quadrature_ledger import (
    FLiBeRankTwoCutoffPathQuadratureLedger,
    FLiBeRankTwoCutoffQuadratureWorkInterval,
    FLiBeRankTwoCutoffQuadratureWorkLevel,
    evaluate_flibe_rank_two_cutoff_path_quadrature_ledger,
)
from tr_eif.ternary import TernaryState

# Register the complete fixture dependency graph in this test module.
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
from test_flibe_rank_two_tr_eip_stress import _fixture


COUNTS = (1, 2, 4, 8)
CHANNELS = range(3)
ENERGY_ABS = 2.0e-27


def _close_channels(actual, expected, *, absolute=ENERGY_ABS):
    assert len(actual) == len(expected) == 3
    for value, target in zip(actual, expected, strict=True):
        assert isfinite(value)
        assert value == pytest.approx(target, rel=2.0e-9, abs=absolute)
    assert actual[2] == pytest.approx(fsum(actual[:2]), rel=2.0e-9, abs=absolute)


def _evaluate(source, counts=COUNTS):
    _, resources = _fixture()
    return evaluate_flibe_rank_two_cutoff_path_quadrature_ledger(
        source,
        resources["model"],
        resources["stress_evaluator"],
        subdivision_counts=counts,
    )


@pytest.fixture(scope="module")
def multistep_quadrature(completed_path_ledger):
    trajectory, _, _, _, source = completed_path_ledger
    return trajectory, source, _evaluate(source)


@pytest.fixture(scope="module")
def event_quadratures(forced_path_ledgers):
    return {
        scale: (trajectory, path_source, _evaluate(path_source))
        for scale, (trajectory, _, _, path_source) in forced_path_ledgers.items()
    }


def test_three_interval_alignment_and_source_identity(multistep_quadrature):
    trajectory, source, result = multistep_quadrature
    assert isinstance(result, FLiBeRankTwoCutoffPathQuadratureLedger)
    assert result.source == source
    assert result.subdivisions == COUNTS
    assert len(result.intervals) == trajectory.interval_count == 3
    assert len(result.levels) == len(COUNTS)
    assert result.crossing_count == source.crossing_count
    for index, (original, recorded) in enumerate(zip(
        source.intervals, result.intervals, strict=True,
    )):
        assert isinstance(recorded, FLiBeRankTwoCutoffQuadratureWorkInterval)
        assert recorded.source == original
        assert recorded.quadrature.path == original.path
        assert recorded.subdivisions == COUNTS
        assert len(recorded.levels) == len(COUNTS)
        assert original.index == index


@pytest.mark.parametrize("index", (0, 1, 2))
def test_independent_si_channels_for_each_md_interval(multistep_quadrature, index):
    _, source, result = multistep_quadrature
    original = source.intervals[index]
    recorded = result.intervals[index]
    factor = original.original.energy_unit_to_joule
    for level, numerical in zip(recorded.levels, recorded.quadrature.levels, strict=True):
        assert isinstance(level, FLiBeRankTwoCutoffQuadratureWorkLevel)
        assert level.subdivisions_per_segment == numerical.subdivisions_per_segment
        _close_channels(level.smooth_pressure_work_j, tuple(
            value * factor for value in numerical.smooth_pressure_work
        ))
        _close_channels(level.localized_graph_energy_j,
                        original.localized_graph_energy_change_j)
        _close_channels(level.reconstructed_potential_change_j, tuple(
            value * factor for value in numerical.estimated_total_energy_change
        ))
        _close_channels(level.exact_potential_change_j, original.total_energy_change_j)
        _close_channels(level.quadrature_residual_j, tuple(
            value * factor for value in numerical.total_quadrature_residual
        ))
        _close_channels(level.reconstructed_potential_change_j, tuple(
            fsum((w, jump))
            for w, jump in zip(level.smooth_pressure_work_j,
                               level.localized_graph_energy_j, strict=True)
        ))
        _close_channels(level.exact_potential_change_j, tuple(
            fsum((computed, error))
            for computed, error in zip(level.reconstructed_potential_change_j,
                                       level.quadrature_residual_j, strict=True)
        ))
    _close_channels(recorded.levels[0].smooth_pressure_work_j,
                    original.smooth_pressure_work_j)


@pytest.mark.parametrize("level_index", (0, 1, 2, 3))
def test_cumulative_refinement_matches_independent_interval_sums(
    multistep_quadrature, level_index,
):
    _, source, result = multistep_quadrature
    level = result.levels[level_index]
    assert level.subdivisions_per_segment == COUNTS[level_index]
    for field in (
        "smooth_pressure_work_j",
        "localized_graph_energy_j",
        "reconstructed_potential_change_j",
        "exact_potential_change_j",
        "quadrature_residual_j",
    ):
        expected = tuple(
            fsum(getattr(item.levels[level_index], field)[channel]
                 for item in result.intervals)
            for channel in CHANNELS
        )
        _close_channels(getattr(level, field), expected)
    _close_channels(level.exact_potential_change_j, source.total_energy_change_j)
    _close_channels(level.localized_graph_energy_j,
                    source.localized_graph_energy_change_j)
    _close_channels(level.reconstructed_potential_change_j, tuple(
        fsum((a, b)) for a, b in zip(
            level.smooth_pressure_work_j, level.localized_graph_energy_j,
            strict=True,
        )
    ))
    _close_channels(level.quadrature_residual_j, tuple(
        a - b for a, b in zip(
            level.exact_potential_change_j,
            level.reconstructed_potential_change_j,
            strict=True,
        )
    ))


def test_no_cutoff_event_preserves_zero_jump_at_every_level(multistep_quadrature):
    trajectory, source, result = multistep_quadrature
    assert source.crossing_count == result.crossing_count == 0
    assert result.levels[0].localized_graph_energy_j == (0.0, 0.0, 0.0)
    for level in result.levels:
        assert level.localized_graph_energy_j == (0.0, 0.0, 0.0)
        _close_channels(level.reconstructed_potential_change_j,
                        level.smooth_pressure_work_j)
    assert result.total_absolute_residuals_j == tuple(
        abs(level.quadrature_residual_j[2]) for level in result.levels
    )
    assert len(result.refinement_error_ratios) == len(COUNTS) - 1
    assert result.source.source.source.observables.trajectory == trajectory


@pytest.mark.parametrize("scale,crossings,added,removed", (
    (0.900, 1, 2, 0),
    (1.012, 2, 0, 4),
))
def test_localized_graph_jumps_and_refinement_are_separate(
    event_quadratures, scale, crossings, added, removed,
):
    trajectory, source, result = event_quadratures[scale]
    assert trajectory.interval_count == 1
    assert source.source.graph_event_count == 1
    assert result.crossing_count == crossings
    assert result.source.directed_edges_added == added
    assert result.source.directed_edges_removed == removed
    assert len(result.intervals) == 1
    item = result.intervals[0]
    assert item.crossing_count == crossings
    assert len(item.quadrature.path.segments) == crossings + 1
    assert item.quadrature.path.scan.directed_edges_added == added
    assert item.quadrature.path.scan.directed_edges_removed == removed
    assert abs(item.source.localized_graph_energy_change_j[2]) > ENERGY_ABS
    for level in result.levels:
        _close_channels(level.localized_graph_energy_j,
                        item.source.localized_graph_energy_change_j)
        _close_channels(level.exact_potential_change_j,
                        item.source.total_energy_change_j)
        _close_channels(level.reconstructed_potential_change_j, tuple(
            fsum((w, jump)) for w, jump in zip(
                level.smooth_pressure_work_j, level.localized_graph_energy_j,
                strict=True,
            )
        ))
        _close_channels(level.quadrature_residual_j, tuple(
            exact - reconstructed for exact, reconstructed in zip(
                level.exact_potential_change_j,
                level.reconstructed_potential_change_j, strict=True,
            )
        ))
    assert result.total_absolute_residuals_j[-1] < result.total_absolute_residuals_j[0]


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_event_quadrature_preserves_active_neutral_pending_and_clocks(
    event_quadratures, scale,
):
    trajectory, source, result = event_quadratures[scale]
    previous, current = trajectory.states
    assert previous.ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert current.ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert current.ternary_execution.has_pending_targets
    assert all(node.pending_target is TernaryState.POSITIVE
               for node in current.ternary_execution.states)
    assert current.ternary_event_count == previous.ternary_event_count + 1
    assert current.resonance_step_count == previous.resonance_step_count + 1
    assert current.md_state.step == previous.md_state.step + 1
    assert current.md_state.masses == previous.md_state.masses
    assert result.source == source
    assert source.intervals[0].path.scan.reference.execution == current.ternary_execution
    assert source.intervals[0].path.scan.reference.resonance.resonance_state == (
        current.resonance_state
    )


def test_deterministic_replay_and_single_refinement(multistep_quadrature):
    _, source, original = multistep_quadrature
    assert _evaluate(source) == original
    single = _evaluate(source, counts=(1,))
    assert single.subdivisions == (1,)
    assert single.refinement_error_ratios == ()
    assert single.levels[0] == original.levels[0]


@pytest.mark.parametrize("value,error", (
    ((), ValueError),
    ([], ValueError),
    (None, ValueError),
    ((2, 4), ValueError),
    ((1, 3), ValueError),
    ((1, 2, 2), ValueError),
    ((1, True), TypeError),
    ((1, 2.0), TypeError),
    ((1, 2, 4, 8, 16, 32, 64, 128), ValueError),
))
def test_invalid_subdivision_schedules_are_rejected(multistep_quadrature, value, error):
    _, source, _ = multistep_quadrature
    with pytest.raises(error):
        _evaluate(source, counts=value)


@pytest.mark.parametrize("name", ("source", "model", "stress_evaluator"))
def test_operator_rejects_untyped_inputs(multistep_quadrature, name):
    _, source, _ = multistep_quadrature
    _, resources = _fixture()
    arguments = dict(source=source, model=resources["model"],
                     stress_evaluator=resources["stress_evaluator"])
    arguments[name] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_path_quadrature_ledger(**arguments)


@pytest.mark.parametrize("field,bad,error", (
    ("subdivisions_per_segment", 0, ValueError),
    ("subdivisions_per_segment", 3, ValueError),
    ("subdivisions_per_segment", True, TypeError),
    ("smooth_pressure_work_j", (0.0, 0.0, 1.0), ValueError),
    ("localized_graph_energy_j", (0.0, 0.0, float("nan")), ValueError),
))
def test_quadrature_level_rejects_inconsistent_fields(
    multistep_quadrature, field, bad, error,
):
    level = multistep_quadrature[-1].levels[0]
    with pytest.raises(error):
        replace(level, **{field: bad})


def test_interval_rejects_disconnected_sources_and_levels(
    multistep_quadrature, event_quadratures,
):
    result = multistep_quadrature[-1]
    item = result.intervals[0]
    other = event_quadratures[0.900][-1].intervals[0]
    with pytest.raises(ValueError):
        replace(item, levels=())
    with pytest.raises(ValueError):
        replace(item, levels=tuple(reversed(item.levels)))
    with pytest.raises(TypeError):
        replace(item, levels=(None, *item.levels[1:]))
    with pytest.raises(ValueError):
        replace(item, source=other.source)
    with pytest.raises(ValueError):
        replace(item, quadrature=other.quadrature)


def test_ledger_rejects_disconnected_sources_and_refinements(
    multistep_quadrature, event_quadratures,
):
    result = multistep_quadrature[-1]
    other = event_quadratures[1.012][-1]
    with pytest.raises(ValueError):
        replace(result, levels=())
    with pytest.raises(ValueError):
        replace(result, levels=tuple(reversed(result.levels)))
    with pytest.raises(ValueError):
        replace(result, intervals=result.intervals[:-1])
    with pytest.raises(ValueError):
        replace(result, intervals=tuple(reversed(result.intervals)))
    with pytest.raises(TypeError):
        replace(result, intervals=(None, *result.intervals[1:]))
    with pytest.raises(TypeError):
        replace(result, source=None)
    with pytest.raises(ValueError):
        replace(result, source=other.source)
