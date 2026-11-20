
"""Integration qualification of piecewise FLiBe rank-two cutoff path work.

Independently reconstruct fixed-graph potential-energy changes and pressure
quadratures between analytically located cutoff events. Graph replacements
are measured at common boundary geometry; the three energy channels retain
continuous resonance features and committed ternary execution throughout.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.equivariant import E3Transformation
from tr_eif.flibe.rank_two_tr_eip_cutoff_path_work import (
    FLiBeRankTwoCutoffPathSegment,
    FLiBeRankTwoCutoffPathWork,
    evaluate_flibe_rank_two_cutoff_path_work,
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
SWEEPS = (
    (0.900, 1, 2, 0),
    (0.988, 0, 0, 0),
    (1.000, 0, 0, 0),
    (1.006, 0, 0, 0),
    (1.012, 1, 0, 4),
)


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


def _evaluate(source, scale):
    _, resources, reference = source
    return evaluate_flibe_rank_two_cutoff_path_work(
        resources["model"], resources["stress_evaluator"], reference,
        cutoff=CUTOFF, target_linear_scale=scale,
    )


def _energy(result):
    return (
        result.reference_energy.total_energy,
        result.tensor_energy.total_energy,
        result.energy.total_energy,
    )


def _pressure(stress):
    return (
        -sum(stress.reference_stress.tensor[i][i] for i in range(3)) / 3.0,
        -sum(stress.tensor_stress.tensor[i][i] for i in range(3)) / 3.0,
        -sum(stress.total_stress.tensor[i][i] for i in range(3)) / 3.0,
    )


def _assert_channels(actual, expected, *, absolute=2e-9):
    assert len(actual) == len(expected) == 3
    for value, reference in zip(actual, expected, strict=True):
        assert isfinite(value)
        assert value == pytest.approx(reference, rel=2e-8, abs=absolute)
    assert actual[2] == pytest.approx(fsum(actual[:2]), rel=2e-8, abs=absolute)


@pytest.fixture(scope="module")
def cases():
    return {
        (state, scale): _evaluate(_source(state), scale)
        for state in STATES for scale, *_ in SWEEPS
    }


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale,crossings,added,removed", SWEEPS)
def test_segment_chain_and_cutoff_inventory(cases, retained, scale, crossings, added, removed):
    result = cases[retained, scale]
    assert isinstance(result, FLiBeRankTwoCutoffPathWork)
    assert result.scan.target_linear_scale == scale
    assert result.scan.reference.execution.retained_states == (retained,) * 7
    assert len(result.segments) == crossings + 1
    assert result.scan.crossing_count == crossings
    assert result.scan.directed_edges_added == added
    assert result.scan.directed_edges_removed == removed
    assert result.segments[0].initial_linear_scale == 1.0
    assert result.segments[-1].final_linear_scale == scale
    assert result.segments[0].graph == result.scan.reference.graph
    assert result.segments[-1].graph == result.scan.target_graph
    for index, segment in enumerate(result.segments):
        assert isinstance(segment, FLiBeRankTwoCutoffPathSegment)
        assert segment.index == index
        assert segment.initial_stress.reference_evaluation.layer.previous == (
            result.scan.reference.resonance_features
        )
        assert segment.final_stress.reference_evaluation.layer.previous == (
            result.scan.reference.resonance_features
        )
        midpoint = (segment.initial_linear_scale + segment.final_linear_scale) / 2
        geometry = scale_periodic_configuration(
            result.scan.reference.configuration.configuration, midpoint,
        )
        assert segment.graph == build_cutoff_graph(geometry, CUTOFF)
        if index < crossings:
            event = result.scan.crossings[index]
            assert segment.final_linear_scale == event.linear_scale
            assert segment.graph == event.graph_before
            assert segment.final_stress.reference_evaluation == event.energy_before
            following = result.segments[index + 1]
            assert following.initial_linear_scale == event.linear_scale
            assert following.graph == event.graph_after
            assert following.initial_stress.reference_evaluation == event.energy_after
    if crossings == 0:
        assert result.localized_graph_energy_change == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("retained", STATES)
@pytest.mark.parametrize("scale,crossings,added,removed", SWEEPS)
def test_independent_segment_quadrature_and_energy_partition(
    cases, retained, scale, crossings, added, removed,
):
    result = cases[retained, scale]
    independent_smooth = []
    independent_work = []
    independent_residual = []
    for segment in result.segments:
        initial_energy = _energy(segment.initial_stress.reference_evaluation)
        final_energy = _energy(segment.final_stress.reference_evaluation)
        before_pressure = _pressure(segment.initial_stress)
        after_pressure = _pressure(segment.final_stress)
        delta_volume = (
            segment.final_stress.reference_volume
            - segment.initial_stress.reference_volume
        )
        energy = tuple(b - a for a, b in zip(
            initial_energy, final_energy, strict=True
        ))
        work = tuple(
            -0.5 * (p0 + p1) * delta_volume
            for p0, p1 in zip(before_pressure, after_pressure, strict=True)
        )
        residual = tuple(a - b for a, b in zip(energy, work, strict=True))
        _assert_channels(segment.potential_energy_change, energy)
        _assert_channels(segment.trapezoidal_pressure_work, work)
        _assert_channels(segment.quadrature_residual, residual)
        independent_smooth.append(energy)
        independent_work.append(work)
        independent_residual.append(residual)

    smooth = tuple(fsum(values[i] for values in independent_smooth) for i in range(3))
    work = tuple(fsum(values[i] for values in independent_work) for i in range(3))
    residual = tuple(fsum(values[i] for values in independent_residual) for i in range(3))
    jumps = tuple(fsum(e.energy_jump[i] for e in result.scan.crossings) for i in range(3))
    start = _energy(result.scan.reference.augmented_result)
    end = _energy(result.segments[-1].final_stress.reference_evaluation)
    total = tuple(b - a for a, b in zip(start, end, strict=True))
    _assert_channels(result.smooth_energy_change, smooth)
    _assert_channels(result.trapezoidal_pressure_work, work)
    _assert_channels(result.smooth_quadrature_residual, residual)
    _assert_channels(result.localized_graph_energy_change, jumps)
    _assert_channels(result.total_energy_change, total)
    _assert_channels(result.total_pressure_work_residual,
                     tuple(t - w for t, w in zip(total, work, strict=True)))
    _assert_channels(total, tuple(s + j for s, j in zip(smooth, jumps, strict=True)))
    _assert_channels(result.total_pressure_work_residual,
                     tuple(r + j for r, j in zip(residual, jumps, strict=True)))
    assert result.volume_change == pytest.approx(
        result.segments[-1].final_stress.reference_volume
        - result.segments[0].initial_stress.reference_volume, abs=1e-10,
    )


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_nonzero_localized_jump_is_distinct_from_endpoint_graph_replacement(scale):
    source = _source()
    result = _evaluate(source, scale)
    assert result.scan.crossing_count == 1
    event = result.scan.crossings[0]
    assert any(abs(value) > 1e-8 for value in event.energy_jump)
    initial = result.scan.reference
    _, resources, _ = source
    final_geometry = scale_periodic_configuration(
        initial.configuration.configuration, scale
    )
    frozen = resources["model"].rank_two_model.evaluate(
        final_geometry, initial.graph, initial.resonance_features, initial.execution,
    )
    refreshed = resources["model"].rank_two_model.evaluate(
        final_geometry, result.scan.target_graph, initial.resonance_features,
        initial.execution,
    )
    endpoint_jump = refreshed.energy.total_energy - frozen.energy.total_energy
    assert event.energy_jump[2] != pytest.approx(endpoint_jump, abs=1e-4)
    assert result.total_energy_change[2] == pytest.approx(
        refreshed.energy.total_energy - initial.energy.total_energy, abs=1e-8,
    )


@pytest.mark.parametrize("scale", (0.900, 1.012))
def test_active_neutral_pending_route_does_not_alter_cutoff_energy_path(scale):
    neutral = _evaluate(_source(), scale)
    pending = _evaluate(_source(pending=True), scale)
    assert not neutral.scan.reference.execution.has_pending_targets
    assert pending.scan.reference.execution.has_pending_targets
    assert pending.scan.reference.execution.retained_states == (
        TernaryState.NEUTRAL,
    ) * 7
    assert all(x.pending_target is TernaryState.POSITIVE
               for x in pending.scan.reference.execution.states)
    assert pending.scan.target_graph == neutral.scan.target_graph
    assert tuple(e.linear_scale for e in pending.scan.crossings) == (
        tuple(e.linear_scale for e in neutral.scan.crossings)
    )
    for field in (
        "smooth_energy_change", "localized_graph_energy_change", "total_energy_change",
        "trapezoidal_pressure_work", "smooth_quadrature_residual",
        "total_pressure_work_residual",
    ):
        _assert_channels(getattr(pending, field), getattr(neutral, field))


@pytest.mark.parametrize("scale", (0.900, 1.012))
@pytest.mark.parametrize("matrix,translation", (
    (ROTATION, (0.0, 0.0, 0.0)),
    (REFLECTION, (1.0, -2.0, 0.5)),
))
def test_e3_scalar_energy_and_cutoff_path_work_invariance(scale, matrix, translation):
    baseline = _evaluate(_source(), scale)
    transformed = _evaluate(
        _source(transform=E3Transformation(matrix, translation)), scale
    )
    assert transformed.scan.crossing_count == baseline.scan.crossing_count
    assert transformed.scan.target_graph.edge_count == (
        baseline.scan.target_graph.edge_count
    )
    assert transformed.scan.reference.execution == baseline.scan.reference.execution
    for original, changed in zip(
        baseline.scan.crossings, transformed.scan.crossings, strict=True
    ):
        assert changed.linear_scale == pytest.approx(original.linear_scale, rel=2e-12)
        _assert_channels(changed.energy_jump, original.energy_jump, absolute=3e-7)
    for field in (
        "smooth_energy_change", "localized_graph_energy_change", "total_energy_change",
        "trapezoidal_pressure_work", "smooth_quadrature_residual",
        "total_pressure_work_residual",
    ):
        _assert_channels(
            getattr(transformed, field), getattr(baseline, field), absolute=3e-6
        )
    assert transformed.volume_change == pytest.approx(
        baseline.volume_change, rel=2e-12
    )


def test_deterministic_replay():
    source = _source()
    first = _evaluate(source, 0.900)
    second = _evaluate(source, 0.900)
    assert first == second
    assert first.segments[0].final_stress == second.segments[0].final_stress


@pytest.mark.parametrize("name,bad,error", (
    ("cutoff", 0.0, ValueError),
    ("cutoff", True, TypeError),
    ("cutoff", 1.5, ValueError),
    ("target_linear_scale", 0.0, ValueError),
    ("target_linear_scale", float("nan"), ValueError),
    ("target_linear_scale", False, TypeError),
    ("probe_relative_width", 0.001, ValueError),
    ("probe_relative_width", -1e-7, ValueError),
))
def test_invalid_scan_parameters_are_rejected(name, bad, error):
    _, resources, reference = _source()
    kwargs = dict(cutoff=CUTOFF, target_linear_scale=0.900)
    kwargs[name] = bad
    with pytest.raises(error):
        evaluate_flibe_rank_two_cutoff_path_work(
            resources["model"], resources["stress_evaluator"], reference, **kwargs,
        )


@pytest.mark.parametrize("field", ("model", "stress_evaluator", "reference"))
def test_untyped_sources_are_rejected(field):
    _, resources, reference = _source()
    kwargs = dict(
        model=resources["model"],
        stress_evaluator=resources["stress_evaluator"],
        reference=reference,
        cutoff=CUTOFF,
        target_linear_scale=0.900,
    )
    kwargs[field] = None
    with pytest.raises(TypeError):
        evaluate_flibe_rank_two_cutoff_path_work(**kwargs)


def test_inconsistent_segment_and_path_records_are_rejected():
    original = _evaluate(_source(), 0.900)
    initial, final = original.segments
    with pytest.raises(ValueError):
        replace(original, segments=(initial,))
    with pytest.raises(ValueError):
        replace(original, segments=tuple(reversed(original.segments)))
    with pytest.raises(TypeError):
        replace(original, segments=(None, final))
    with pytest.raises(ValueError):
        replace(original, segments=(replace(initial, index=1), final))
    with pytest.raises(ValueError):
        replace(initial, final_stress=initial.initial_stress)
    with pytest.raises(ValueError):
        replace(initial, initial_linear_scale=1.1)
    with pytest.raises(ValueError):
        replace(original, scan=_evaluate(_source(), 1.012).scan)
