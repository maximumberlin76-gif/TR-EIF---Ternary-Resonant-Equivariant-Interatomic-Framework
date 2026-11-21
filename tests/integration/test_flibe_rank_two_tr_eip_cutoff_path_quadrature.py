
"""Integration qualification of refined FLiBe rank-two cutoff-path quadrature.

Independently reconstruct equal-volume pressure integration on frozen-graph
segments and preserve energy jumps at analytically localized cutoff scales.
Check reference, rank-two and total-energy channels, active-neutral pending
execution, E(3) invariance, deterministic replay and numerical refinement.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.energy import CellStrainDifferentiation
from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
from tr_eif.equivariant import E3Transformation
from tr_eif.flibe.rank_two_tr_eip_cutoff_path_quadrature import (
    FLiBeRankTwoCutoffPathQuadrature,
    FLiBeRankTwoCutoffQuadratureLevel,
    evaluate_flibe_rank_two_cutoff_path_quadrature,
)
from tr_eif.flibe.rank_two_tr_eip_cutoff_path_work import (
    evaluate_flibe_rank_two_cutoff_path_work,
)
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
SCALES = (0.900, 1.000, 1.006, 1.012)
SUBDIVISIONS = (1, 2, 4, 8)
CHANNELS = range(3)


def _source(retained=TernaryState.NEUTRAL, *, pending=False, transform=None):
    initial, resources = _fixture(initial=retained, transform=transform)
    if pending:
        assert retained is TernaryState.NEUTRAL
        execution = TernaryExecutionVector(states=tuple(
            TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE)
            for _ in initial.ternary_execution.states
        ))
        initial = replace(initial, ternary_execution=execution)
    return initial, resources, _single_stress(initial, resources).evaluation


def _compute(source, scale, *, counts=SUBDIVISIONS):
    _, resources, reference = source
    path = evaluate_flibe_rank_two_cutoff_path_work(
        resources["model"], resources["stress_evaluator"], reference,
        cutoff=CUTOFF, target_linear_scale=scale,
    )
    result = evaluate_flibe_rank_two_cutoff_path_quadrature(
        path, resources["model"], resources["stress_evaluator"],
        subdivision_counts=counts,
    )
    return path, result


def _channel_equal(actual, expected, *, relative=2e-8, absolute=3e-8):
    assert len(actual) == len(expected) == 3
    for value, target in zip(actual, expected, strict=True):
        assert isfinite(value)
        assert value == pytest.approx(target, rel=relative, abs=absolute)
    assert actual[2] == pytest.approx(fsum(actual[:2]), rel=relative, abs=absolute)


def _pressure(stress):
    return (
        -sum(stress.reference_stress.tensor[axis][axis] for axis in range(3)) / 3.0,
        -sum(stress.tensor_stress.tensor[axis][axis] for axis in range(3)) / 3.0,
        -sum(stress.total_stress.tensor[axis][axis] for axis in range(3)) / 3.0,
    )


@pytest.fixture(scope="module")
def qualified_matrix():
    matrix = {}
    for retained in STATES:
        source = _source(retained)
        for scale in SCALES:
            matrix[retained, scale] = (source, *_compute(source, scale))
    return matrix


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale", SCALES)
def test_all_levels_preserve_cutoff_and_three_energy_channels(qualified_matrix, retained, scale):
    source, path, output = qualified_matrix[retained, scale]
    assert isinstance(output, FLiBeRankTwoCutoffPathQuadrature)
    assert output.path == path
    assert output.subdivisions == SUBDIVISIONS
    assert output.total_energy_change == path.total_energy_change
    assert output.localized_graph_energy_change == path.localized_graph_energy_change
    assert path.scan.reference == source[2]
    assert path.scan.reference.execution.retained_states == (retained,) * 7
    assert len(output.levels) == len(SUBDIVISIONS)
    assert len(output.signed_total_residuals) == len(SUBDIVISIONS)
    assert len(output.total_absolute_residuals) == len(SUBDIVISIONS)
    assert len(output.refinement_error_ratios) == len(SUBDIVISIONS) - 1
    for level, subdivisions in zip(output.levels, SUBDIVISIONS, strict=True):
        assert isinstance(level, FLiBeRankTwoCutoffQuadratureLevel)
        assert level.path == path
        assert level.subdivisions_per_segment == subdivisions
        assert len(level.segment_pressure_work) == len(path.segments)
        for value in level.segment_pressure_work:
            _channel_equal(value, value)
        _channel_equal(level.smooth_pressure_work, tuple(
            fsum(item[channel] for item in level.segment_pressure_work)
            for channel in CHANNELS
        ))
        _channel_equal(level.smooth_quadrature_residual, tuple(
            path.smooth_energy_change[channel] - level.smooth_pressure_work[channel]
            for channel in CHANNELS
        ))
        _channel_equal(level.estimated_total_energy_change, tuple(
            fsum((level.smooth_pressure_work[channel], path.localized_graph_energy_change[channel]))
            for channel in CHANNELS
        ))
        _channel_equal(level.total_quadrature_residual, tuple(
            path.total_energy_change[channel] - level.estimated_total_energy_change[channel]
            for channel in CHANNELS
        ))
        _channel_equal(level.total_quadrature_residual, level.smooth_quadrature_residual)
    _channel_equal(output.levels[0].smooth_pressure_work, path.trapezoidal_pressure_work)


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale", (0.900, 1.006, 1.012))
def test_error_refinement_is_second_order(qualified_matrix, retained, scale):
    _, path, result = qualified_matrix[retained, scale]
    error = result.total_absolute_residuals
    assert path.scan.crossing_count == int(scale != 1.006)
    assert all(isfinite(value) and value > 0.0 for value in error)
    assert all(left > right for left, right in zip(error, error[1:], strict=False))
    for ratio in result.refinement_error_ratios:
        assert ratio is not None
        # Predeclared bound around the composite trapezoidal 4x refinement.
        assert 3.25 < ratio < 4.75


def test_zero_deformation_has_zero_work_and_zero_errors(qualified_matrix):
    _, path, output = qualified_matrix[TernaryState.NEUTRAL, 1.000]
    assert path.scan.crossings == ()
    assert path.total_energy_change == (0.0, 0.0, 0.0)
    assert output.total_absolute_residuals == (0.0,) * len(SUBDIVISIONS)
    assert output.refinement_error_ratios == (None,) * (len(SUBDIVISIONS) - 1)
    for level in output.levels:
        assert level.smooth_pressure_work == (0.0, 0.0, 0.0)
        assert level.total_quadrature_residual == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("scale,added,removed", (
    (0.900, 2, 0),
    (1.012, 0, 4),
))
def test_localized_cutoff_jumps_do_not_change_with_refinement(qualified_matrix, scale, added, removed):
    _, path, output = qualified_matrix[TernaryState.NEUTRAL, scale]
    assert path.scan.crossing_count == 1
    assert path.scan.directed_edges_added == added
    assert path.scan.directed_edges_removed == removed
    assert abs(path.localized_graph_energy_change[2]) > 1e-5
    for level in output.levels:
        _channel_equal(level.estimated_total_energy_change, tuple(
            fsum((level.smooth_pressure_work[k], path.localized_graph_energy_change[k]))
            for k in CHANNELS
        ))
    assert output.localized_graph_energy_change == path.scan.localized_energy_jumps


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_independent_equal_volume_composite_quadrature(qualified_matrix, scale):
    source, path, output = qualified_matrix[TernaryState.NEUTRAL, scale]
    _, resources, reference = source
    subdivisions = 4
    independent = []
    for segment in path.segments:
        samples = []
        for index in range(subdivisions + 1):
            if index == 0:
                stress = segment.initial_stress
            elif index == subdivisions:
                stress = segment.final_stress
            else:
                fraction = index / subdivisions
                scale_cube = (
                    (1.0 - fraction) * segment.initial_linear_scale**3
                    + fraction * segment.final_linear_scale**3
                )
                geometry = scale_periodic_configuration(
                    reference.configuration.configuration, scale_cube ** (1.0 / 3.0),
                )
                stress = resources["stress_evaluator"].evaluate(
                    resources["model"].rank_two_model,
                    geometry, segment.graph,
                    reference.resonance_features, reference.execution,
                )
                assert stress.reference_evaluation.layer.previous == reference.resonance_features
            samples.append(stress)
        channel_work = []
        for channel in CHANNELS:
            work = fsum(
                -0.5 * (_pressure(a)[channel] + _pressure(b)[channel])
                * (b.reference_volume - a.reference_volume)
                for a, b in zip(samples, samples[1:], strict=False)
            )
            channel_work.append(work)
        independent.append(tuple(channel_work))
    for actual, expected in zip(
        output.levels[2].segment_pressure_work, independent, strict=True,
    ):
        _channel_equal(actual, expected, relative=5e-8, absolute=5e-7)
    _channel_equal(output.levels[2].smooth_pressure_work, tuple(
        fsum(item[channel] for item in independent) for channel in CHANNELS
    ), relative=5e-8, absolute=5e-7)


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_pending_target_does_not_change_neutral_quadrature(qualified_matrix, scale):
    _, plain_path, plain = qualified_matrix[TernaryState.NEUTRAL, scale]
    pending_path, pending = _compute(_source(pending=True), scale)
    assert not plain_path.scan.reference.execution.has_pending_targets
    assert pending_path.scan.reference.execution.has_pending_targets
    assert pending_path.scan.reference.execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert all(item.pending_target is TernaryState.POSITIVE
               for item in pending_path.scan.reference.execution.states)
    _channel_equal(pending_path.localized_graph_energy_change,
                   plain_path.localized_graph_energy_change)
    for before, after in zip(plain.levels, pending.levels, strict=True):
        _channel_equal(after.smooth_pressure_work, before.smooth_pressure_work)
        _channel_equal(after.total_quadrature_residual, before.total_quadrature_residual)
    assert pending.subdivisions == plain.subdivisions


@pytest.mark.parametrize("scale", (0.900, 1.012))
@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (1.0, -2.0, 0.5)),
    (REFLECTION, (-0.5, 0.75, 1.0)),
))
def test_e3_scalar_quadrature_and_cutoff_invariance(qualified_matrix, scale, matrix, translation):
    _, reference_path, reference = qualified_matrix[TernaryState.NEUTRAL, scale]
    moved_path, moved = _compute(_source(
        transform=E3Transformation(matrix, translation)
    ), scale)
    assert moved_path.scan.crossing_count == reference_path.scan.crossing_count
    assert moved_path.scan.directed_edges_added == reference_path.scan.directed_edges_added
    assert moved_path.scan.directed_edges_removed == reference_path.scan.directed_edges_removed
    _channel_equal(moved_path.localized_graph_energy_change,
                   reference_path.localized_graph_energy_change,
                   relative=5e-4, absolute=5e-5)
    for before, after in zip(reference.levels, moved.levels, strict=True):
        _channel_equal(after.smooth_pressure_work, before.smooth_pressure_work,
                       relative=5e-4, absolute=5e-5)
        _channel_equal(after.total_quadrature_residual, before.total_quadrature_residual,
                       relative=5e-3, absolute=5e-5)


def test_deterministic_replay_and_single_level(qualified_matrix):
    source, path, output = qualified_matrix[TernaryState.NEUTRAL, 1.012]
    assert _compute(source, 1.012)[1] == output
    _, resources, _ = source
    single = evaluate_flibe_rank_two_cutoff_path_quadrature(
        path, resources["model"], resources["stress_evaluator"],
        subdivision_counts=(1,),
    )
    assert single.subdivisions == (1,)
    assert single.refinement_error_ratios == ()
    assert single.levels[0] == output.levels[0]


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
def test_invalid_refinement_schedules_are_rejected(qualified_matrix, value, error):
    source, path, _ = qualified_matrix[TernaryState.NEUTRAL, 1.006]
    _, resources, _ = source
    with pytest.raises(error):
        evaluate_flibe_rank_two_cutoff_path_quadrature(
            path, resources["model"], resources["stress_evaluator"],
            subdivision_counts=value,
        )


@pytest.mark.parametrize("field", ("path", "model", "stress_evaluator"))
def test_untyped_operator_inputs_are_rejected(qualified_matrix, field):
    source, path, _ = qualified_matrix[TernaryState.NEUTRAL, 1.006]
    _, resources, _ = source
    args = dict(path=path, model=resources["model"],
                stress_evaluator=resources["stress_evaluator"])
    args[field] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_path_quadrature(**args)


def test_differentiation_method_mismatch_is_rejected(qualified_matrix):
    source, path, _ = qualified_matrix[TernaryState.NEUTRAL, 1.006]
    _, resources, _ = source
    changed = RankTwoConservativeStressEvaluator(CellStrainDifferentiation(step=2e-6))
    with pytest.raises(ValueError, match="stress method"):
        evaluate_flibe_rank_two_cutoff_path_quadrature(
            path, resources["model"], changed,
        )


@pytest.mark.parametrize("value,error", (
    (-1, ValueError),
    (0, ValueError),
    (65, ValueError),
    (True, TypeError),
    (1.5, TypeError),
))
def test_quadrature_level_rejects_invalid_subdivisions(qualified_matrix, value, error):
    level = qualified_matrix[TernaryState.NEUTRAL, 1.012][2].levels[0]
    with pytest.raises(error):
        replace(level, subdivisions_per_segment=value)


def test_quadrature_level_rejects_corrupted_segment_energies(qualified_matrix):
    level = qualified_matrix[TernaryState.NEUTRAL, 1.012][2].levels[0]
    with pytest.raises(ValueError):
        replace(level, segment_pressure_work=())
    with pytest.raises(ValueError):
        replace(level, segment_pressure_work=((1.0, 2.0, 9.0), *level.segment_pressure_work[1:]))
    with pytest.raises(TypeError):
        replace(level, segment_pressure_work=(None, *level.segment_pressure_work[1:]))


def test_quadrature_result_rejects_broken_level_order(qualified_matrix):
    original = qualified_matrix[TernaryState.NEUTRAL, 1.012][2]
    other_path = qualified_matrix[TernaryState.NEUTRAL, 0.900][1]
    with pytest.raises(ValueError):
        replace(original, levels=())
    with pytest.raises(ValueError):
        replace(original, levels=tuple(reversed(original.levels)))
    with pytest.raises(ValueError):
        replace(original, levels=(original.levels[0], original.levels[0]))
    with pytest.raises(TypeError):
        replace(original, levels=(None, *original.levels[1:]))
    with pytest.raises(ValueError):
        replace(original, path=other_path)
