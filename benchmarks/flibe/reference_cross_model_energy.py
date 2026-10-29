"""Matched FLiBe energy comparison: reference baseline and resonance-conditioned TR-EIP."""

from __future__ import annotations

import json
from math import cos, fsum, isclose, pi, sin, sqrt

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
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import (
    FLiBeTREIPModel,
    append_flibe_resonance_channels,
)
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.reference-cross-model-energy.v1"
REFERENCE_STATE_ID = "FLIBE-7-ATOM-ANALYTIC-FIXTURE"
BASELINE_MODEL_ID = "REFERENCE-ONE-CHANNEL"
CONDITIONED_MODEL_ID = "TR-EIP-RESONANCE-THREE-CHANNEL"
ENERGY_UNIT_ID = "model-native-energy"
ABSOLUTE_TOLERANCE = 1.0e-10
FORCE_ABSOLUTE_TOLERANCE = 2.0e-6
FORCE_DIFFERENCE_STEP = 1.0e-6
CUTOFF = 1.6
DISTANCE_SCALE = 1.1
BIAS = 0.1
BASE_WEIGHT = 0.4
PHASE_WEIGHT = 0.7
SPREAD_WEIGHT = -0.3

SPECIES = ("Li", "Li", "Be", "F", "F", "F", "F")
POSITIONS = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0),
    (1.1, 0.7, 0.8),
    (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)
PHASES = tuple(index * pi / 4.0 for index in range(7))
FREQUENCIES = (-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3)
RETAINED_STATES = (
    TernaryState.NEGATIVE,
    TernaryState.NEUTRAL,
    TernaryState.POSITIVE,
    TernaryState.NEUTRAL,
    TernaryState.NEGATIVE,
    TernaryState.POSITIVE,
    TernaryState.NEUTRAL,
)
CONDITIONING_FACTORS = (0.5, 1.25, 1.5, 1.25, 0.5, 1.5, 1.25)


def _configuration(positions=POSITIONS) -> FLiBeConfiguration:
    return FLiBeConfiguration(
        configuration=AtomicConfiguration(species=SPECIES, positions=positions)
    )


def _features(rotated: bool = False) -> NodeFeatureVector:
    return NodeFeatureVector(
        nodes=tuple(
            NodeFeatures(
                scalars=(0.5 + 0.25 * index,),
                vectors=(
                    (
                        -(0.1 * index) if rotated else 1.0,
                        1.0 if rotated else 0.1 * index,
                        -0.05 * index,
                    ),
                ),
            )
            for index in range(len(SPECIES))
        )
    )


def _common_model(scalar_weights: tuple[float, ...]) -> ReferenceEnergyModel:
    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(distance_scale=DISTANCE_SCALE),
        conditioning=TernaryConditioning(
            negative_scale=0.5, neutral_scale=1.25, positive_scale=1.5
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=scalar_weights, bias=BIAS
        ),
    )


def _evaluate_pair(configuration: FLiBeConfiguration, features: NodeFeatureVector):
    graph = build_cutoff_graph(configuration.configuration, cutoff=CUTOFF)
    oscillator = ResonanceState(phases=PHASES, frequencies=FREQUENCIES)
    resonance = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=FLiBeThermodynamicState(
            temperature=1000.0, pressure=0.0
        ),
        resonance_state=oscillator,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )
    execution = TernaryExecutionVector.from_retained_states(RETAINED_STATES)
    baseline_model = _common_model((BASE_WEIGHT,))
    conditioned_model = _common_model((BASE_WEIGHT, PHASE_WEIGHT, SPREAD_WEIGHT))
    baseline = baseline_model.evaluate(
        configuration.configuration, graph, features, execution
    ).energy
    tr_eip_result = FLiBeTREIPModel(
        energy_model=conditioned_model,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(
        configuration=configuration,
        graph=graph,
        features=features,
        resonance=resonance,
        execution=execution,
    )
    evaluator = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(step=FORCE_DIFFERENCE_STEP)
    )
    baseline_forces = evaluator.evaluate(
        baseline_model, configuration.configuration, graph, features, execution
    ).forces
    conditioned_forces = evaluator.evaluate(
        conditioned_model, configuration.configuration, graph,
        tr_eip_result.resonance_conditioned_features, execution,
    ).forces
    return (
        baseline, tr_eip_result.energy_result.energy, graph, resonance,
        baseline_forces, conditioned_forces,
    )


def _independent_analytic_energies() -> tuple[tuple[float, ...], tuple[float, ...], int]:
    """Evaluate the declared radial and linear equations directly from inputs."""
    count = len(POSITIONS)
    phase_order = sqrt(fsum(cos(t) for t in PHASES) ** 2
                       + fsum(sin(t) for t in PHASES) ** 2) / count
    mean_frequency = fsum(FREQUENCIES) / count
    spread = sqrt(fsum((w - mean_frequency) ** 2 for w in FREQUENCIES) / count)
    resonance_increment = PHASE_WEIGHT * phase_order + SPREAD_WEIGHT * spread
    baseline: list[float] = []
    conditioned: list[float] = []
    edge_count = 0
    for receiver in range(count):
        scalar = CONDITIONING_FACTORS[receiver] * (0.5 + 0.25 * receiver)
        multiplier = CONDITIONING_FACTORS[receiver]
        xj, yj, zj = POSITIONS[receiver]
        for source in range(count):
            if source == receiver:
                continue
            xi, yi, zi = POSITIONS[source]
            squared = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            if squared <= CUTOFF ** 2:
                edge_count += 1
                radial = 1.0 / (1.0 + squared / (DISTANCE_SCALE ** 2))
                scalar += radial * CONDITIONING_FACTORS[source] * (0.5 + 0.25 * source)
                multiplier += radial * CONDITIONING_FACTORS[source]
        base = BASE_WEIGHT * scalar + BIAS
        baseline.append(base)
        conditioned.append(base + resonance_increment * multiplier)
    return tuple(baseline), tuple(conditioned), edge_count


def _independent_analytic_forces(
    phase_order: float, spread: float
) -> tuple[tuple[tuple[float, float, float], ...], ...]:
    """Derive pairwise fixed-graph forces from radial-energy gradients."""
    increment = PHASE_WEIGHT * phase_order + SPREAD_WEIGHT * spread
    outputs = []
    for extra in (0.0, increment):
        coefficients = tuple(
            CONDITIONING_FACTORS[index]
            * (BASE_WEIGHT * (0.5 + 0.25 * index) + extra)
            for index in range(len(SPECIES))
        )
        forces = [[0.0, 0.0, 0.0] for _ in SPECIES]
        for source in range(len(SPECIES)):
            for receiver in range(source + 1, len(SPECIES)):
                delta = tuple(
                    POSITIONS[source][axis] - POSITIONS[receiver][axis]
                    for axis in range(3)
                )
                distance_squared = fsum(component ** 2 for component in delta)
                if distance_squared > CUTOFF ** 2:
                    continue
                reduced = 1.0 + distance_squared / (DISTANCE_SCALE ** 2)
                coefficient = (
                    2.0 * (coefficients[source] + coefficients[receiver])
                    / (DISTANCE_SCALE ** 2 * reduced ** 2)
                )
                for axis in range(3):
                    increment_force = coefficient * delta[axis]
                    forces[source][axis] += increment_force
                    forces[receiver][axis] -= increment_force
        outputs.append(tuple(tuple(row) for row in forces))
    return tuple(outputs)


def _force_matches(actual, expected) -> bool:
    return len(actual) == len(expected) and all(
        all(isclose(a, e, rel_tol=0.0, abs_tol=FORCE_ABSOLUTE_TOLERANCE)
            for a, e in zip(a_row, e_row, strict=True))
        for a_row, e_row in zip(actual, expected, strict=True)
    )


def _rotate_vector(vector):
    return (-vector[1], vector[0], vector[2])


def _matches(actual: tuple[float, ...], expected: tuple[float, ...]) -> bool:
    return len(actual) == len(expected) and all(
        isclose(a, e, rel_tol=0.0, abs_tol=ABSOLUTE_TOLERANCE)
        for a, e in zip(actual, expected, strict=True)
    )


def _rotate_translate(position):
    x, y, z = position
    return (-y + 3.0, x - 2.0, z + 1.25)


def run_benchmark() -> dict[str, object]:
    """Execute both configured energy models on the same FLiBe fixture state."""
    configuration = _configuration()
    features = _features()
    (
        baseline, conditioned, graph, descriptor, baseline_forces, conditioned_forces,
    ) = _evaluate_pair(configuration, features)
    expected_baseline, expected_conditioned, expected_edges = _independent_analytic_energies()

    replay_base, replay_conditioned, _, _, replay_bf, replay_cf = _evaluate_pair(
        configuration, features
    )
    rotated_positions = tuple(_rotate_translate(r) for r in POSITIONS)
    (
        rotated_base, rotated_conditioned, rotated_graph, _, rotated_bf, rotated_cf,
    ) = _evaluate_pair(_configuration(rotated_positions), _features(rotated=True))
    difference = conditioned.total_energy - baseline.total_energy
    expected_difference = fsum(expected_conditioned) - fsum(expected_baseline)
    expected_bf, expected_cf = _independent_analytic_forces(
        phase_order=sqrt(fsum(cos(t) for t in PHASES) ** 2 +
                         fsum(sin(t) for t in PHASES) ** 2) / len(PHASES),
        spread=sqrt(fsum((w - fsum(FREQUENCIES)/len(FREQUENCIES)) ** 2
                          for w in FREQUENCIES) / len(FREQUENCIES)),
    )

    checks = {
        "exact_composition": configuration.composition().formula_unit_fractions
        == (2.0 / 3.0, 1.0 / 3.0),
        "directed_graph": graph.edge_count == expected_edges == rotated_graph.edge_count,
        "retained_ternary_alphabet": tuple(state.value for state in RETAINED_STATES)
        == (-1, 0, 1, 0, -1, 1, 0),
        "baseline_analytical_energy": _matches(baseline.atomic_energies, expected_baseline),
        "tr_eip_analytical_energy": _matches(conditioned.atomic_energies, expected_conditioned),
        "total_baseline_sum": isclose(baseline.total_energy, fsum(expected_baseline), rel_tol=0.0, abs_tol=ABSOLUTE_TOLERANCE),
        "total_tr_eip_sum": isclose(conditioned.total_energy, fsum(expected_conditioned), rel_tol=0.0, abs_tol=ABSOLUTE_TOLERANCE),
        "signed_model_delta": isclose(difference, expected_difference, rel_tol=0.0, abs_tol=ABSOLUTE_TOLERANCE),
        "baseline_replay": baseline == replay_base,
        "tr_eip_replay": conditioned == replay_conditioned,
        "baseline_e3_invariance": _matches(baseline.atomic_energies, rotated_base.atomic_energies),
        "tr_eip_e3_invariance": _matches(conditioned.atomic_energies, rotated_conditioned.atomic_energies),
        "baseline_analytical_forces": _force_matches(baseline_forces, expected_bf),
        "tr_eip_analytical_forces": _force_matches(conditioned_forces, expected_cf),
        "baseline_force_replay": baseline_forces == replay_bf,
        "tr_eip_force_replay": conditioned_forces == replay_cf,
        "baseline_e3_force_covariance": _force_matches(
            rotated_bf, tuple(_rotate_vector(force) for force in baseline_forces)
        ),
        "tr_eip_e3_force_covariance": _force_matches(
            rotated_cf, tuple(_rotate_vector(force) for force in conditioned_forces)
        ),
        "baseline_net_force_balance": all(abs(fsum(force[a] for force in baseline_forces))
                                          <= FORCE_ABSOLUTE_TOLERANCE for a in range(3)),
        "tr_eip_net_force_balance": all(abs(fsum(force[a] for force in conditioned_forces))
                                        <= FORCE_ABSOLUTE_TOLERANCE for a in range(3)),
    }
    return {
        "benchmark_id": BENCHMARK_ID,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "comparison_kind": "reference_baseline_vs_resonance_conditioned_tr_eip",
        "reference_state_id": REFERENCE_STATE_ID,
        "provenance": "TEST_FIXTURE",
        "declared_fixture_state": {
            "composition": {"lif_fraction": 2.0 / 3.0, "bef2_fraction": 1.0 / 3.0},
            "temperature_k": 1000.0,
            "pressure_pa": 0.0,
            "atom_count": len(SPECIES),
            "directed_edge_count": graph.edge_count,
            "retained_execution": [state.value for state in RETAINED_STATES],
            "resonance": {"phase_order": descriptor.phase_order, "frequency_spread": descriptor.frequency_spread},
        },
        "numeric_contract": {
            "energy_absolute_tolerance": ABSOLUTE_TOLERANCE,
            "force_absolute_tolerance": FORCE_ABSOLUTE_TOLERANCE,
            "force_derivative_step": FORCE_DIFFERENCE_STEP,
            "energy_unit": ENERGY_UNIT_ID,
            "force_unit": "model-native-energy-per-coordinate",
        },
        "models": {
            BASELINE_MODEL_ID: {
                "type": "ReferenceEnergyModel",
                "base_scalar_weights": [BASE_WEIGHT],
                "atomic_energy": list(baseline.atomic_energies),
                "total_energy": baseline.total_energy,
                "cartesian_forces": [list(v) for v in baseline_forces],
            },
            CONDITIONED_MODEL_ID: {
                "type": "FLiBeTREIPModel",
                "base_and_resonance_weights": [BASE_WEIGHT, PHASE_WEIGHT, SPREAD_WEIGHT],
                "atomic_energy": list(conditioned.atomic_energies),
                "total_energy": conditioned.total_energy,
                "cartesian_forces": [list(v) for v in conditioned_forces],
            },
        },
        "signed_energy_difference": difference,
        "analytical_energy_difference": expected_difference,
        "checks": checks,
    }


if __name__ == "__main__":
    result = run_benchmark()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
