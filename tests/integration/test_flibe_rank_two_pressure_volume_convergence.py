
"""Numerical pressure-volume convergence for FLiBe rank-two TR-EIP energy.

For one fixed interaction graph, resonance-conditioned feature state and
retained ternary execution, compare the complete energy change under an
isotropic affine cell deformation with a trapezoidal -integral(P dV).
Discretization is refined by a factor of two; numerical thresholds are fixed
for the declared scale interval before each evaluated test scenario. An
additional cutoff-graph check identifies an affine deformation that changes
the neighbor set; that topology event is kept separate from the fixed-graph
quadrature relation.
"""

from __future__ import annotations

from dataclasses import replace
from math import fsum, isfinite

import pytest

from tr_eif.graph import build_cutoff_graph
from tr_eif.md.barostat import scale_periodic_configuration
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)

from test_flibe_rank_two_tr_eip_stress import CUTOFF, _fixture, _single_stress


SCALES = (0.012, 0.006, 0.003)
STRAIN_STEP = 0.0002
ROUTES = (
    TernaryState.NEGATIVE,
    TernaryState.NEUTRAL,
    TernaryState.POSITIVE,
)


def _case(retained: TernaryState, *, pending: bool = False):
    state, resources = _fixture(initial=retained)
    if pending:
        assert retained is TernaryState.NEUTRAL
        execution = TernaryExecutionVector(states=tuple(
            TernaryExecutionState(TernaryState.NEUTRAL, TernaryState.POSITIVE)
            for _ in state.ternary_execution.states
        ))
        state = replace(state, ternary_execution=execution)
    reference = _single_stress(state, resources)
    return state, resources, reference


def _evaluate(case, scale: float):
    state, resources, baseline = case
    initial = state.md_state.configuration
    deformed = scale_periodic_configuration(initial, scale)
    graph = baseline.evaluation.graph
    # Cell-strain differentiation retains the reference graph exactly.
    # Rebuilding neighbors is a separately classified operator boundary.
    assert graph.node_count == deformed.atom_count
    record = resources["stress_evaluator"].evaluate(
        resources["model"].rank_two_model,
        deformed, graph, baseline.evaluation.resonance_features,
        state.ternary_execution,
    )
    assert record.reference_evaluation.layer.previous == baseline.evaluation.resonance_features
    return record


def _energy_and_pressure(record, channel):
    energy = record.reference_evaluation
    if channel == "reference":
        total = energy.reference_energy.total_energy
        pressure = -record.reference_stress.trace / 3.0
    elif channel == "rank_two":
        total = energy.tensor_energy.total_energy
        pressure = -record.tensor_stress.trace / 3.0
    else:
        total = energy.energy.total_energy
        pressure = record.potential_pressure
    return total, pressure


def _quadrature_error(case, increment, channel="total"):
    baseline = case[2].stress
    terminal = _evaluate(case, 1.0 + increment)
    initial_energy, initial_pressure = _energy_and_pressure(baseline, channel)
    final_energy, final_pressure = _energy_and_pressure(terminal, channel)
    delta_volume = terminal.reference_volume - baseline.reference_volume
    exact_energy_difference = final_energy - initial_energy
    trapezoid = -0.5 * fsum((initial_pressure, final_pressure)) * delta_volume
    assert isfinite(exact_energy_difference) and isfinite(trapezoid)
    if increment:
        assert delta_volume * increment > 0.0
    return exact_energy_difference - trapezoid, exact_energy_difference, trapezoid


@pytest.mark.parametrize("retained", ROUTES)
@pytest.mark.parametrize("direction", (-1.0, 1.0))
def test_pressure_volume_quadrature_refines_at_third_order(retained, direction):
    """Trapezoid residual decreases faster than quadratic refinement."""
    case = _case(retained)
    residuals = [
        abs(_quadrature_error(case, direction * size)[0])
        for size in SCALES
    ]
    assert all(isfinite(value) for value in residuals)
    # Smooth U(V): trapezoid error is O(delta_V^3); allow numerical stress noise.
    assert residuals[1] < residuals[0] / 3.0
    assert residuals[2] < residuals[1] / 3.0


@pytest.mark.parametrize("retained", ROUTES)
@pytest.mark.parametrize("direction", (-1.0, 1.0))
def test_reference_and_rank_two_pressure_work_partition(retained, direction):
    case = _case(retained)
    increment = direction * SCALES[1]
    total = _quadrature_error(case, increment, "total")
    reference = _quadrature_error(case, increment, "reference")
    tensor = _quadrature_error(case, increment, "rank_two")
    for index in range(3):
        assert total[index] == pytest.approx(
            fsum((reference[index], tensor[index])), rel=1e-9, abs=2e-9,
        )


@pytest.mark.parametrize("retained", ROUTES)
def test_isotropic_energy_derivative_matches_configurational_pressure(retained):
    case = _case(retained)
    base = case[2].stress
    above = _evaluate(case, 1.0 + STRAIN_STEP)
    below = _evaluate(case, 1.0 - STRAIN_STEP)
    for channel in ("reference", "rank_two", "total"):
        upper_energy = _energy_and_pressure(above, channel)[0]
        lower_energy = _energy_and_pressure(below, channel)[0]
        volume_change = above.reference_volume - below.reference_volume
        derivative = (upper_energy - lower_energy) / volume_change
        pressure = _energy_and_pressure(base, channel)[1]
        assert derivative == pytest.approx(-pressure, rel=2e-4, abs=5e-5)


def test_pending_destination_does_not_change_neutral_pressure_volume_response():
    retained = _case(TernaryState.NEUTRAL)
    pending = _case(TernaryState.NEUTRAL, pending=True)
    assert retained[0].ternary_execution.retained_states == pending[0].ternary_execution.retained_states
    assert not retained[0].ternary_execution.has_pending_targets
    assert pending[0].ternary_execution.has_pending_targets
    for factor in (1.0, 1.0 + SCALES[0], 1.0 - SCALES[0]):
        neutral_stress = _evaluate(retained, factor)
        pending_stress = _evaluate(pending, factor)
        assert neutral_stress.reference_evaluation.energy == pending_stress.reference_evaluation.energy
        assert neutral_stress.total_stress == pending_stress.total_stress
        assert neutral_stress.potential_pressure == pending_stress.potential_pressure
    for direction in (-1.0, 1.0):
        for amount in SCALES:
            assert _quadrature_error(retained, direction * amount) == pytest.approx(
                _quadrature_error(pending, direction * amount), abs=1e-10,
            )


@pytest.mark.parametrize("retained", ROUTES)
def test_unscaled_cell_has_zero_pressure_volume_work(retained):
    case = _case(retained)
    record = _evaluate(case, 1.0)
    assert record.reference_volume == case[2].stress.reference_volume
    assert record.reference_evaluation == case[2].stress.reference_evaluation
    assert record.potential_pressure == case[2].stress.potential_pressure
    assert _quadrature_error(case, 0.0) == (0.0, 0.0, 0.0)


@pytest.mark.parametrize("scale,expected_change", (
    (1.003, False),
    (1.006, False),
    (1.012, True),
    (0.988, False),
))
def test_neighbor_graph_changes_are_classified_outside_frozen_strain_branch(
    scale, expected_change,
):
    """Record whether the physical cutoff graph changes under affine scaling."""
    state, resources, reference = _case(TernaryState.NEUTRAL)
    initial_graph = reference.evaluation.graph
    changed_geometry = scale_periodic_configuration(state.md_state.configuration, scale)
    refreshed_graph = build_cutoff_graph(changed_geometry, CUTOFF)
    did_change = refreshed_graph != initial_graph
    assert did_change is expected_change
    frozen_result = _evaluate((state, resources, reference), scale)
    assert frozen_result.reference_evaluation.layer.previous == reference.evaluation.resonance_features
    if did_change:
        # The refreshed cutoff graph is a distinct model input.
        refreshed_energy = resources["model"].rank_two_model.evaluate(
            changed_geometry,
            refreshed_graph,
            reference.evaluation.resonance_features,
            state.ternary_execution,
        )
        assert refreshed_graph.node_count == initial_graph.node_count
        assert refreshed_energy != frozen_result.reference_evaluation
        assert len(refreshed_graph.edges) != len(initial_graph.edges)
    else:
        assert refreshed_graph == initial_graph
