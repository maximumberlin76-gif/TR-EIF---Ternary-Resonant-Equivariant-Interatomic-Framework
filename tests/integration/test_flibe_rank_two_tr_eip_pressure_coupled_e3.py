"""E(3) qualification of the FLiBe rank-two pressure-coupled MD pipeline.

Compare complete trajectories under rotations, reflection and translation.
The full conservative stress must transform as a Cartesian tensor; energy,
kinetic and configurational pressure, volume, density and pressure-volume work
must retain their scalar values. An affine barostat also scales the initial
translation, so positions are compared in the corresponding moving origin.
"""

from __future__ import annotations

import pytest

from tr_eif.equivariant import E3Transformation
from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_observables import (
    evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_coupled_trajectory import (
    run_flibe_rank_two_tr_eip_pressure_coupled_trajectory,
)
from tr_eif.flibe.rank_two_tr_eip_pressure_volume_work import (
    evaluate_flibe_rank_two_tr_eip_pressure_volume_work,
)
from tr_eif.ternary import TernaryState

from test_flibe_rank_two_tr_eip_stress import _fixture
from test_flibe_rank_two_tr_eip_pressure_coupled_trajectory import (
    LENGTH_TO_M,
    STRESS_TO_PA,
    prepared_trajectory,
)

ENERGY_TO_JOULE = STRESS_TO_PA * LENGTH_TO_M**3
DEGREES_OF_FREEDOM = 18
E3_CASES = (
    (
        "quarter_turn",
        E3Transformation(
            ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
            (1.25, -0.75, 0.5),
        ),
    ),
    (
        "reflection",
        E3Transformation(
            ((-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            (-0.5, 1.25, 0.75),
        ),
    ),
    (
        "translation",
        E3Transformation(
            ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)),
            (1.0, -2.0, 0.5),
        ),
    ),
)


def _tensor_transform(tensor, matrix):
    """Construct R sigma R^T independently of the model's tensor utilities."""
    return tuple(
        tuple(sum(matrix[a][i] * tensor[i][j] * matrix[b][j]
                  for i in range(3) for j in range(3)) for b in range(3))
        for a in range(3)
    )


def _isclose(actual, expected, *, relative=4e-4, absolute=0.0):
    assert actual == pytest.approx(expected, rel=relative, abs=absolute)


@pytest.fixture(scope="module")
def e3_pipeline(prepared_trajectory):
    baseline, options = prepared_trajectory
    baseline_observables = evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables(
        baseline, energy_unit_to_joule=ENERGY_TO_JOULE,
        degrees_of_freedom=DEGREES_OF_FREEDOM,
    )
    baseline_work = evaluate_flibe_rank_two_tr_eip_pressure_volume_work(
        baseline_observables
    )
    transformed = {}
    for label, transformation in E3_CASES:
        initial, resources = _fixture(transform=transformation)
        # Keep the same target, units, schedule and physical-state coordinates.
        parameters = {**options, **resources}
        trajectory = run_flibe_rank_two_tr_eip_pressure_coupled_trajectory(
            initial, **parameters
        )
        observables = evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables(
            trajectory, energy_unit_to_joule=ENERGY_TO_JOULE,
            degrees_of_freedom=DEGREES_OF_FREEDOM,
        )
        work = evaluate_flibe_rank_two_tr_eip_pressure_volume_work(observables)
        transformed[label] = (transformation, trajectory, observables, work)
    return baseline, baseline_observables, baseline_work, transformed


@pytest.mark.parametrize("case", (name for name, _ in E3_CASES))
def test_scalar_pressure_volume_and_density_are_e3_invariant(e3_pipeline, case):
    reference, reference_observables, _, transformed = e3_pipeline
    _, changed, observations, _ = transformed[case]
    assert changed.interval_count == reference.interval_count == 3
    assert changed.schedule == reference.schedule
    assert changed.target_pressure == reference.target_pressure
    assert changed.thermodynamic_state == reference.thermodynamic_state
    assert changed.velocity_frame is reference.velocity_frame
    for left, right in zip(reference.steps, changed.steps, strict=True):
        _isclose(right.pressure.total_pressure.value, left.pressure.total_pressure.value,
                 absolute=1e4)
        _isclose(right.pressure.kinetic_pressure.value,
                 left.pressure.kinetic_pressure.value, absolute=1e4)
        _isclose(right.barostat.current_pressure_pa, left.barostat.current_pressure_pa,
                 absolute=1e4)
        _isclose(right.barostat.linear_scale, left.barostat.linear_scale, relative=1e-5)
        _isclose(right.barostat.volume_ratio, left.barostat.volume_ratio, relative=1e-5)
        _isclose(right.barostat.after_barostat_potential_pressure_pa,
                 left.barostat.after_barostat_potential_pressure_pa, absolute=1e4)
    for left, right in zip(reference_observables.samples, observations.samples, strict=True):
        for name, absolute in (
            ("volume_m3", 1e-35),
            ("density_kg_m3", 1e-4),
            ("kinetic_energy_j", 1e-26),
            ("kinetic_temperature_k", 1e-6),
            ("kinetic_pressure_pa", 1e4),
            ("configurational_pressure_pa", 1e4),
            ("total_pressure_pa", 1e4),
            ("target_pressure_residual_pa", 1e4),
            ("reference_energy_j", 1e-26),
            ("rank_two_energy_j", 1e-26),
            ("event_potential_energy_change_j", 1e-26),
            ("mechanical_total_energy_change_j", 1e-26),
            ("barostat_potential_energy_change_j", 1e-26),
            ("net_total_energy_change_j", 1e-26),
        ):
            _isclose(getattr(right, name), getattr(left, name), absolute=absolute)


@pytest.mark.parametrize("case", (name for name, _ in E3_CASES))
def test_four_stress_boundaries_transform_as_second_rank_tensors(e3_pipeline, case):
    reference, _, _, transformed = e3_pipeline
    transformation, changed, _, _ = transformed[case]
    for base, moved in zip(reference.steps, changed.steps, strict=True):
        a = base.barostat.stress_trace
        b = moved.barostat.stress_trace
        for first, second in (
            (a.before_events, b.before_events),
            (a.after_events, b.after_events),
            (a.after_mechanics, b.after_mechanics),
            (base.barostat.after_barostat, moved.barostat.after_barostat),
        ):
            for name in ("reference_stress", "tensor_stress", "total_stress"):
                expected = _tensor_transform(
                    getattr(first.stress, name).tensor, transformation.matrix,
                )
                observed = getattr(second.stress, name).tensor
                for actual_row, expected_row in zip(observed, expected, strict=True):
                    assert actual_row == pytest.approx(expected_row, rel=4e-4, abs=4e-6)
            _isclose(second.potential_pressure, first.potential_pressure,
                     absolute=4e-6)
            _isclose(second.evaluation.energy.total_energy,
                     first.evaluation.energy.total_energy, absolute=1e-8)
            assert second.evaluation.execution == first.evaluation.execution


@pytest.mark.parametrize("case", (name for name, _ in E3_CASES))
def test_geometry_velocities_and_active_neutral_route_are_equivariant(e3_pipeline, case):
    reference, _, _, transformed = e3_pipeline
    transformation, changed, _, _ = transformed[case]
    scale_product = 1.0
    for index, (original, moved) in enumerate(zip(reference.states, changed.states, strict=True)):
        if index:
            scale_product *= reference.steps[index - 1].barostat.linear_scale
        source = original.md_state
        result = moved.md_state
        assert result.step == source.step
        assert result.time == source.time
        assert result.masses == source.masses
        assert result.configuration.species == source.configuration.species
        assert result.configuration.periodic == source.configuration.periodic
        assert moved.ternary_execution == original.ternary_execution
        assert moved.ternary_event_count == original.ternary_event_count
        assert moved.resonance_step_count == original.resonance_step_count
        _isclose(moved.resonance_time, original.resonance_time, absolute=1e-12)
        assert moved.resonance_state.phases == pytest.approx(
            original.resonance_state.phases, rel=1e-12, abs=1e-12,
        )
        assert moved.resonance_state.frequencies == pytest.approx(
            original.resonance_state.frequencies, rel=1e-12, abs=1e-12,
        )
        for left, right in zip(source.configuration.cell, result.configuration.cell, strict=True):
            assert right == pytest.approx(transformation.transform_vector(left),
                                          rel=4e-4, abs=3e-5)
        for left, right in zip(source.velocities, result.velocities, strict=True):
            assert right == pytest.approx(transformation.transform_vector(left),
                                          rel=4e-4, abs=3e-7)
        for left, right in zip(source.configuration.positions,
                               result.configuration.positions, strict=True):
            rotated = transformation.transform_vector(left)
            expected = tuple(rotated[a] + scale_product * transformation.translation[a]
                             for a in range(3))
            assert right == pytest.approx(expected, rel=4e-4, abs=3e-5)
    assert reference.states[0].ternary_execution.retained_states == (TernaryState.NEGATIVE,) * 7
    assert reference.states[1].ternary_execution.retained_states == (TernaryState.NEUTRAL,) * 7
    assert reference.states[1].ternary_execution.has_pending_targets
    assert reference.states[2].ternary_execution.retained_states == (TernaryState.POSITIVE,) * 7
    assert not reference.states[2].ternary_execution.has_pending_targets


@pytest.mark.parametrize("case", (name for name, _ in E3_CASES))
def test_pressure_volume_work_ledger_is_e3_invariant(e3_pipeline, case):
    _, _, reference, transformed = e3_pipeline
    _, _, _, changed = transformed[case]
    for left, right in zip(reference.intervals, changed.intervals, strict=True):
        for name, absolute in (
            ("volume_before_m3", 1e-35),
            ("volume_after_m3", 1e-35),
            ("volume_change_m3", 1e-35),
            ("potential_pressure_before_pa", 1e4),
            ("potential_pressure_after_pa", 1e4),
            ("total_energy_before_j", 1e-26),
            ("total_energy_after_j", 1e-26),
            ("event_potential_change_j", 1e-26),
            ("mechanical_total_change_j", 1e-26),
            ("affine_potential_change_j", 1e-26),
            ("net_total_energy_change_j", 1e-26),
            ("trapezoidal_potential_work_j", 1e-26),
            ("pressure_quadrature_residual_j", 1e-26),
            ("target_pressure_volume_term_j", 1e-26),
            ("target_pressure_energy_change_j", 1e-26),
        ):
            _isclose(getattr(right, name), getattr(left, name), absolute=absolute)
    for name in (
        "total_volume_change_m3", "total_energy_change_j", "event_potential_change_j",
        "mechanical_total_change_j", "affine_potential_change_j",
        "target_pressure_volume_term_j", "target_pressure_energy_change_j",
        "pressure_quadrature_residual_j",
    ):
        _isclose(getattr(changed, name), getattr(reference, name), absolute=1e-26)
