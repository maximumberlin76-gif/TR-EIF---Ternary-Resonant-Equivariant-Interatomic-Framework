"""Structured correctness benchmark for the FLiBe TR-EIP reference path."""

from __future__ import annotations

import json
from math import isclose, pi

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import LinearInvariantEnergyFunctional, ReferenceEnergyModel
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
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.reference-correctness.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-correctness-v1"
ABSOLUTE_TOLERANCE = 1.0e-12

EXPECTED_ATOMIC_ENERGIES = (
    1.2705309214957103,
    2.3853292080184136,
    2.6890312438179187,
    2.279365350241249,
    2.7361160326533533,
    2.461711066814251,
    2.5294802950816706,
)

EXPECTED_TOTAL_ENERGY = 16.351564118122567


def _configuration() -> FLiBeConfiguration:
    """Construct the fixed FLiBe correctness benchmark configuration."""

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
                vectors=(
                    (
                        1.0,
                        0.1 * index,
                        -0.05 * index,
                    ),
                ),
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


def _close(
    actual: float,
    expected: float,
) -> bool:
    """Compare one benchmark scalar against its pinned reference value."""

    return isclose(
        actual,
        expected,
        rel_tol=0.0,
        abs_tol=ABSOLUTE_TOLERANCE,
    )


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe TR-EIP correctness benchmark."""

    configuration = _configuration()

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=1.6,
    )

    resonance = build_flibe_resonance_descriptor(
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

    execution = _execution()

    result = _model().evaluate(
        configuration=configuration,
        graph=graph,
        features=_features(),
        resonance=resonance,
        execution=execution,
    )

    composition = configuration.composition()

    atomic_energies = (
        result.energy_result.energy.atomic_energies
    )

    retained_states = tuple(
        state.value
        for state in execution.retained_states
    )

    checks = {
        "atom_count": (
            configuration.atom_count == 7
        ),
        "graph_node_count": (
            graph.node_count == 7
        ),
        "graph_edge_count": (
            graph.edge_count == 38
        ),
        "lif_fraction": _close(
            composition.lif_fraction,
            2.0 / 3.0,
        ),
        "bef2_fraction": _close(
            composition.bef2_fraction,
            1.0 / 3.0,
        ),
        "phase_order": _close(
            resonance.phase_order,
            1.0 / 7.0,
        ),
        "frequency_spread": _close(
            resonance.frequency_spread,
            0.2,
        ),
        "retained_ternary_state": (
            retained_states
            == (-1, 0, 1, 0, -1, 1, 0)
        ),
        "scalar_channel_count": (
            result.resonance_conditioned_features.scalar_channel_count
            == 3
        ),
        "vector_channel_count": (
            result.resonance_conditioned_features.vector_channel_count
            == 1
        ),
        "atomic_energies": (
            len(atomic_energies)
            == len(EXPECTED_ATOMIC_ENERGIES)
            and all(
                _close(
                    actual,
                    expected,
                )
                for actual, expected in zip(
                    atomic_energies,
                    EXPECTED_ATOMIC_ENERGIES,
                    strict=True,
                )
            )
        ),
        "total_energy": _close(
            result.energy_result.energy.total_energy,
            EXPECTED_TOTAL_ENERGY,
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
        "absolute_tolerance": ABSOLUTE_TOLERANCE,
        "checks": checks,
        "observed": {
            "atom_count": configuration.atom_count,
            "graph_node_count": graph.node_count,
            "graph_edge_count": graph.edge_count,
            "composition": {
                "lif_fraction": composition.lif_fraction,
                "bef2_fraction": composition.bef2_fraction,
            },
            "resonance_coordinate": list(
                resonance.coordinate
            ),
            "retained_ternary_state": list(
                retained_states
            ),
            "scalar_channel_count": (
                result.resonance_conditioned_features.scalar_channel_count
            ),
            "vector_channel_count": (
                result.resonance_conditioned_features.vector_channel_count
            ),
            "atomic_energies": list(
                atomic_energies
            ),
            "total_energy": (
                result.energy_result.energy.total_energy
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
