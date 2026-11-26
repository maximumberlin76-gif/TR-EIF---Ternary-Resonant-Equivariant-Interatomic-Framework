
"""Executable TR-EIF resonance, ternary, equivariant-energy and MD chain.

The reference fixture runs separate phase, ternary, and mechanical clocks.
A requested opposite polarity executes through retained active neutral with
an explicitly held pending target. E(3) transformed inputs are propagated
through the same schedule and compared on energy and Cartesian observables.
"""

from __future__ import annotations

import json
from math import isclose, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    E3Transformation,
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.md.coupled_execution import (
    CoupledMolecularDynamicsState,
    execute_coupled_md_step,
)
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
    is_direct_opposite_transition,
)


EXAMPLE_ID = "tr-eif.hybrid-resonance-ternary-interatomic-md.v1"
POSITIONS = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0))
VELOCITIES = ((0.0, 0.01, 0.0), (-0.01, 0.0, 0.0), (0.0, 0.0, 0.01))
MASSES = (1.0, 2.0, 3.0)
CUTOFF = 1.6
MECHANICAL_TIME_STEP = 1.0e-4
PHASE_TIME_STEP = 0.2


TRANSFORMATION = E3Transformation(
    matrix=((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
    translation=(2.0, -3.0, 1.0),
)


def _fixture(transformation: E3Transformation | None = None):
    """Initialize the same hybrid state in either Cartesian reference frame."""
    positions = POSITIONS
    velocities = VELOCITIES
    if transformation is not None:
        positions = tuple(transformation.transform_position(p) for p in positions)
        velocities = tuple(transformation.transform_vector(v) for v in velocities)

    state = CoupledMolecularDynamicsState(
        md_state=MolecularDynamicsState(
            configuration=AtomicConfiguration(
                species=("A", "B", "C"), positions=positions,
            ),
            velocities=velocities,
            masses=MASSES,
            step=0,
            time=0.0,
        ),
        resonance_state=ResonanceState(
            phases=(0.0, 0.15, 0.3),
            frequencies=(0.1, -0.1, 0.2),
        ),
        ternary_execution=TernaryExecutionVector.from_retained_states(
            (TernaryState.NEGATIVE,) * 3,
        ),
    )

    features = NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(float(index + 1),),
            vectors=((0.2, -0.1, 0.05),),
        )
        for index in range(3)
    ))
    if transformation is not None:
        features = transformation.transform_feature_vector(features)

    model = ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=1.0),
        conditioning=TernaryConditioning(
            negative_scale=0.5,
            neutral_scale=1.2,
            positive_scale=1.7,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(0.3, 0.4, 0.7), bias=0.1,
        ),
    )
    return state, dict(
        model=model,
        force_evaluator=ConservativeForceEvaluator(
            differentiation=CoordinateDifferentiation(step=1.0e-5),
        ),
        base_features=features,
        cutoff=CUTOFF,
    )


def _execute(transformation: E3Transformation | None = None):
    """Advance three mechanical intervals and three guarded ternary events."""
    state, common = _fixture(transformation)
    projection = ResonanceProjection(
        phase_order_weight=1.0,
        frequency_spread_weight=-0.1,
    )
    thresholds = TernaryTargetThresholds(negative=-0.3, positive=0.5)
    event = dict(ternary_event=True, projection=projection, thresholds=thresholds)

    entry = execute_coupled_md_step(
        state,
        **common,
        **event,
        phase_parameters=PhaseDynamicsParameters(
            coupling=(0.2,) * 3, phase_lag=(0.1,) * 3,
        ),
        phase_time_step=PHASE_TIME_STEP,
        guards=(TernaryExecutionGuard.neutral_entry_only(),) * 3,
        mechanical_time_step=MECHANICAL_TIME_STEP,
    )
    held = execute_coupled_md_step(
        entry.current,
        **common,
        **event,
        guards=(TernaryExecutionGuard.hold(),) * 3,
        mechanical_time_step=MECHANICAL_TIME_STEP,
    )
    exit_step = execute_coupled_md_step(
        held.current,
        **common,
        **event,
        guards=(TernaryExecutionGuard.neutral_exit_only(),) * 3,
        mechanical_time_step=MECHANICAL_TIME_STEP,
    )
    return state, (entry, held, exit_step)


def _all_commits_are_neutral_mediated(steps) -> bool:
    for step in steps:
        assert step.ternary_update is not None
        for node in step.ternary_update.execution.node_steps:
            if node.route is None:
                continue
            transition = node.route.transition
            if is_direct_opposite_transition(transition.source, transition.target):
                return False
    return True


def _frame_consistency(reference, transformed) -> bool:
    """Compare E(3)-invariant energy and transformed positions/velocities."""
    for a, b in zip(reference, transformed, strict=True):
        if a.current.ternary_execution != b.current.ternary_execution:
            return False
        for energy_a, energy_b in (
            (a.energy_before_events, b.energy_before_events),
            (a.energy_after_events, b.energy_after_events),
            (a.energy_after_mechanics, b.energy_after_mechanics),
        ):
            if not isclose(energy_a.total_energy, energy_b.total_energy,
                           rel_tol=1.0e-10, abs_tol=1.0e-10):
                return False
        md_a = a.current.md_state
        md_b = b.current.md_state
        for position_a, position_b in zip(
            md_a.configuration.positions, md_b.configuration.positions, strict=True,
        ):
            expected = TRANSFORMATION.transform_position(position_a)
            if not all(isclose(v, w, rel_tol=1.0e-9, abs_tol=1.0e-9)
                       for v, w in zip(expected, position_b, strict=True)):
                return False
        for velocity_a, velocity_b in zip(
            md_a.velocities, md_b.velocities, strict=True,
        ):
            expected = TRANSFORMATION.transform_vector(velocity_a)
            if not all(isclose(v, w, rel_tol=1.0e-8, abs_tol=1.0e-8)
                       for v, w in zip(expected, velocity_b, strict=True)):
                return False
    return True


def run_example() -> dict[str, object]:
    """Produce an ordered hybrid trace and its executable invariant results."""
    initial, steps = _execute()
    _, rotated_steps = _execute(TRANSFORMATION)
    entry, held, exit_step = steps
    neutral = (TernaryState.NEUTRAL,) * 3
    positive = (TernaryState.POSITIVE,) * 3
    final = exit_step.current

    checks = {
        "opposite_request_is_explicit": all(
            step.requested_target is TernaryState.POSITIVE for step in steps
        ),
        "active_neutral_entry": (
            entry.current.ternary_execution.retained_states == neutral
            and entry.ternary_update.committed_count == 3
        ),
        "pending_retained_after_entry": all(
            node.pending_target is TernaryState.POSITIVE
            for node in entry.current.ternary_execution.states
        ),
        "neutral_hold_is_active_state_retention": (
            held.current.ternary_execution == entry.current.ternary_execution
            and held.ternary_update.committed_count == 0
        ),
        "separate_neutral_exit": (
            final.ternary_execution.retained_states == positive
            and not final.ternary_execution.has_pending_targets
            and exit_step.ternary_update.committed_count == 3
        ),
        "no_direct_opposite_commits": _all_commits_are_neutral_mediated(steps),
        "mechanical_clock": (
            final.md_state.step == initial.md_state.step + 3
            and isclose(final.md_state.time, 3.0 * MECHANICAL_TIME_STEP)
        ),
        "resonance_clock": (
            final.resonance_step_count == 1
            and isclose(final.resonance_time, PHASE_TIME_STEP)
            and all(step.current.resonance_state == entry.current.resonance_state
                    for step in (held, exit_step))
        ),
        "ternary_event_clock": final.ternary_event_count == 3,
        "energy_boundary_finite": all(
            isfinite(value)
            for step in steps
            for value in (
                step.energy_before_events.total_energy,
                step.energy_after_events.total_energy,
                step.energy_after_mechanics.total_energy,
            )
        ),
        "e3_energy_and_cartesian_covariance": _frame_consistency(steps, rotated_steps),
    }

    records = tuple({
        "interval": index + 1,
        "mechanical_step": step.current.md_state.step,
        "mechanical_time": step.current.md_state.time,
        "resonance_step_count": step.current.resonance_step_count,
        "resonance_time": step.current.resonance_time,
        "ternary_event_count": step.current.ternary_event_count,
        "requested_target": int(step.requested_target),
        "retained_states": tuple(
            int(state) for state in step.current.ternary_execution.retained_states
        ),
        "pending_targets": tuple(
            None if state.pending_target is None else int(state.pending_target)
            for state in step.current.ternary_execution.states
        ),
        "committed_ternary_legs": step.ternary_update.committed_count,
        "phase_order": step.descriptor.phase_order,
        "frequency_spread": step.descriptor.frequency_spread,
        "energy_before_events": step.energy_before_events.total_energy,
        "energy_after_events": step.energy_after_events.total_energy,
        "energy_after_mechanics": step.energy_after_mechanics.total_energy,
        "event_potential_energy_change": step.event_potential_energy_change,
        "mechanical_potential_energy_change": (
            step.mechanical_potential_energy_change
        ),
    } for index, step in enumerate(steps))

    return {
        "example_id": EXAMPLE_ID,
        "model": "ReferenceEnergyModel",
        "geometry": "three-node-nonperiodic-analytic-fixture",
        "operator_order": "phase -> ternary request -> retained execution -> mechanics",
        "initial_retained_states": tuple(
            int(value) for value in initial.ternary_execution.retained_states
        ),
        "records": records,
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


def main() -> None:
    result = run_example()
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
