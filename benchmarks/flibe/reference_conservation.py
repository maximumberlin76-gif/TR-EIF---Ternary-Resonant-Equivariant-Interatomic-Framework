"""Structured conservation benchmark for the FLiBe TR-EIP MD reference path."""

from __future__ import annotations

import json
from math import isfinite, pi

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    CoordinateDifferentiation,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.mass import FLiBeMassParameters, configuration_masses
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import run_velocity_verlet_trajectory
from tr_eif.md.trajectory_observables import evaluate_trajectory_energy
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.reference-conservation.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-conservation-v1"

CUTOFF = 1.6
TIME_STEP = 1.0e-3
STEP_COUNT = 5
ENERGY_DRIFT_ABSOLUTE_TOLERANCE = 1.0e-9
ENERGY_IDENTITY_ABSOLUTE_TOLERANCE = 1.0e-15


def _configuration() -> FLiBeConfiguration:
    """Construct the fixed non-collinear FLiBe benchmark configuration."""

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=(
                "Li",
                "Li",
                "Be",
                "F",
                "F",
                "F",
                "F",
            ),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.4, 0.9, 0.2),
                (0.2, 0.3, 1.0),
                (1.1, 0.7, 0.8),
                (1.7, 0.2, 0.5),
                (0.8, 1.5, 0.4),
            ),
        )
    )


def _features() -> NodeFeatureVector:
    """Construct the fixed scalar-plus-vector benchmark features."""

    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(
                scalars=(0.5 + 0.25 * index,),
                vectors=((1.0, 0.1 * index, -0.05 * index),),
            )
            for index in range(7)
        )
    )


def _execution() -> TernaryExecutionVector:
    """Construct the fixed retained balanced-ternary benchmark state."""

    return TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEGATIVE,
            TernaryState.NEUTRAL,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
            TernaryState.NEGATIVE,
            TernaryState.POSITIVE,
            TernaryState.NEUTRAL,
        )
    )


def _resonance_state() -> ResonanceState:
    """Construct the fixed continuous resonance benchmark state."""

    return ResonanceState(
        phases=(
            0.0,
            0.25 * pi,
            0.5 * pi,
            0.75 * pi,
            pi,
            1.25 * pi,
            1.5 * pi,
        ),
        frequencies=(
            -0.3,
            -0.2,
            -0.1,
            0.0,
            0.1,
            0.2,
            0.3,
        ),
    )


def _model() -> FLiBeTREIPModel:
    """Construct the fixed FLiBe TR-EIP benchmark realization."""

    return FLiBeTREIPModel(
        energy_model=ReferenceEnergyModel(
            message_operator=RadialMessageOperator(
                distance_scale=1.1,
            ),
            conditioning=TernaryConditioning(
                negative_scale=0.5,
                neutral_scale=1.25,
                positive_scale=1.5,
            ),
            energy_functional=LinearInvariantEnergyFunctional(
                weights=(0.4, 0.7, -0.3),
                bias=0.1,
            ),
        ),
        provenance=ParameterProvenance.BENCHMARK,
        source=SOURCE_ID,
    )


def _force_evaluator() -> ConservativeForceEvaluator:
    """Construct the fixed central-difference conservative-force evaluator."""

    return ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    )


def _initial_state(
    configuration: FLiBeConfiguration,
) -> MolecularDynamicsState:
    """Construct the fixed FLiBe MD benchmark initial state."""

    masses = configuration_masses(
        configuration,
        FLiBeMassParameters(
            lithium=1.0,
            beryllium=2.0,
            fluorine=3.0,
        ),
    )

    velocities = tuple(
        (
            1.0e-3 * (index + 1),
            -5.0e-4 * index,
            2.5e-4 * (index % 3),
        )
        for index in range(configuration.atom_count)
    )

    return MolecularDynamicsState(
        configuration=configuration.configuration,
        velocities=velocities,
        masses=masses,
    )


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe TR-EIP conservation benchmark."""

    configuration = _configuration()

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

    model = _model()
    execution = _execution()

    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(
            configuration,
            graph,
        ),
        thermodynamic_state=FLiBeThermodynamicState(
            temperature=1000.0,
            pressure=0.0,
        ),
        resonance_state=_resonance_state(),
        provenance=ParameterProvenance.BENCHMARK,
        source=SOURCE_ID,
    )

    tr_eip_result = model.evaluate(
        configuration=configuration,
        graph=graph,
        features=_features(),
        resonance=descriptor,
        execution=execution,
    )

    trajectory = run_velocity_verlet_trajectory(
        initial_state=_initial_state(configuration),
        model=model.energy_model,
        force_evaluator=_force_evaluator(),
        features=tr_eip_result.resonance_conditioned_features,
        execution=execution,
        cutoff=CUTOFF,
        time_step=TIME_STEP,
        step_count=STEP_COUNT,
    )

    energy = evaluate_trajectory_energy(
        trajectory=trajectory,
        model=model.energy_model,
        features=tr_eip_result.resonance_conditioned_features,
        execution=execution,
        cutoff=CUTOFF,
    )

    initial_total = energy.initial.total_energy
    final_total = energy.final.total_energy

    signed_drifts = tuple(
        total - initial_total
        for total in energy.total_energies
    )

    absolute_drifts = tuple(
        abs(value)
        for value in signed_drifts
    )

    max_absolute_drift = max(
        absolute_drifts
    )

    final_signed_drift = (
        final_total
        - initial_total
    )

    finite_components = all(
        isfinite(value)
        for sequence in (
            energy.kinetic_energies,
            energy.potential_energies,
            energy.total_energies,
        )
        for value in sequence
    )

    energy_identity = all(
        abs(
            state.total_energy
            - (
                state.kinetic.total_kinetic_energy
                + state.potential.total_energy
            )
        )
        <= ENERGY_IDENTITY_ABSOLUTE_TOLERANCE
        for state in energy.energies
    )

    retained_states = tuple(
        state.value
        for state in execution.retained_states
    )

    checks = {
        "atom_count_preserved": (
            trajectory.atom_count
            == configuration.atom_count
            == 7
        ),
        "state_count": (
            energy.state_count
            == STEP_COUNT + 1
        ),
        "step_count": (
            trajectory.step_count
            == STEP_COUNT
        ),
        "finite_energy_components": (
            finite_components
        ),
        "kinetic_plus_potential_identity": (
            energy_identity
        ),
        "total_energy_drift_bounded": (
            max_absolute_drift
            <= ENERGY_DRIFT_ABSOLUTE_TOLERANCE
        ),
        "resonance_coordinate_fixed": (
            descriptor.coordinate
            == tr_eip_result.resonance.coordinate
        ),
        "retained_ternary_state_preserved": (
            retained_states
            == (-1, 0, 1, 0, -1, 1, 0)
        ),
        "no_pending_ternary_targets": (
            execution.has_pending_targets is False
        ),
    }

    status = (
        "PASS"
        if all(checks.values())
        else "FAIL"
    )

    return {
        "benchmark_id": BENCHMARK_ID,
        "provenance": PROVENANCE,
        "status": status,
        "energy_drift_absolute_tolerance": (
            ENERGY_DRIFT_ABSOLUTE_TOLERANCE
        ),
        "energy_identity_absolute_tolerance": (
            ENERGY_IDENTITY_ABSOLUTE_TOLERANCE
        ),
        "checks": checks,
        "observed": {
            "atom_count": (
                trajectory.atom_count
            ),
            "step_count": (
                trajectory.step_count
            ),
            "state_count": (
                energy.state_count
            ),
            "time_step": (
                TIME_STEP
            ),
            "initial_total_energy": (
                initial_total
            ),
            "final_total_energy": (
                final_total
            ),
            "final_signed_energy_drift": (
                final_signed_drift
            ),
            "max_absolute_energy_drift": (
                max_absolute_drift
            ),
            "kinetic_energies": list(
                energy.kinetic_energies
            ),
            "potential_energies": list(
                energy.potential_energies
            ),
            "total_energies": list(
                energy.total_energies
            ),
            "resonance_coordinate": list(
                descriptor.coordinate
            ),
            "retained_ternary_state": list(
                retained_states
            ),
        },
    }


def main() -> None:
    """Run the benchmark and emit deterministic structured JSON."""

    report = run_benchmark()

    print(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
    )

    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
