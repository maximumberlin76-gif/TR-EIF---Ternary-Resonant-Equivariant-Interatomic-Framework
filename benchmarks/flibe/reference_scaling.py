"""Structured size-scaling benchmark for the FLiBe TR-EIP reference path."""

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


BENCHMARK_ID = "tr-eif.flibe.reference-scaling.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-scaling-v1"

CUTOFF = 1.6
REPLICA_SPACING = 10.0
REPLICA_COUNTS = (1, 2, 4, 8)
ABSOLUTE_TOLERANCE = 1.0e-11

_BASE_SPECIES = (
    "Li",
    "Li",
    "Be",
    "F",
    "F",
    "F",
    "F",
)

_BASE_POSITIONS = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.4, 0.9, 0.2),
    (0.2, 0.3, 1.0),
    (1.1, 0.7, 0.8),
    (1.7, 0.2, 0.5),
    (0.8, 1.5, 0.4),
)

_BASE_PHASES = (
    0.0,
    0.25 * pi,
    0.5 * pi,
    0.75 * pi,
    pi,
    1.25 * pi,
    1.5 * pi,
)

_BASE_FREQUENCIES = (
    -0.3,
    -0.2,
    -0.1,
    0.0,
    0.1,
    0.2,
    0.3,
)

_BASE_TERNARY_STATES = (
    TernaryState.NEGATIVE,
    TernaryState.NEUTRAL,
    TernaryState.POSITIVE,
    TernaryState.NEUTRAL,
    TernaryState.NEGATIVE,
    TernaryState.POSITIVE,
    TernaryState.NEUTRAL,
)


def _configuration(replica_count: int) -> FLiBeConfiguration:
    """Construct isolated translated copies of the fixed FLiBe fixture."""

    species: list[str] = []
    positions: list[tuple[float, float, float]] = []

    for replica_index in range(replica_count):
        offset = REPLICA_SPACING * replica_index

        species.extend(_BASE_SPECIES)
        positions.extend(
            (x + offset, y, z)
            for x, y, z in _BASE_POSITIONS
        )

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=tuple(species),
            positions=tuple(positions),
        )
    )


def _features(replica_count: int) -> NodeFeatureVector:
    """Repeat the fixed per-formula-unit benchmark feature pattern."""

    nodes: list[NodeFeatures] = []

    for _ in range(replica_count):
        nodes.extend(
            NodeFeatures(
                scalars=(0.5 + 0.25 * index,),
                vectors=((1.0, 0.1 * index, -0.05 * index),),
            )
            for index in range(7)
        )

    return NodeFeatureVector(
        nodes=tuple(nodes)
    )


def _resonance_state(replica_count: int) -> ResonanceState:
    """Repeat the fixed continuous resonance pattern without phase mixing."""

    return ResonanceState(
        phases=_BASE_PHASES * replica_count,
        frequencies=_BASE_FREQUENCIES * replica_count,
    )


def _execution(replica_count: int) -> TernaryExecutionVector:
    """Repeat the fixed retained balanced-ternary execution pattern."""

    return TernaryExecutionVector.from_retained_states(
        _BASE_TERNARY_STATES * replica_count
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


def _evaluate(
    replica_count: int,
) -> dict[str, object]:
    """Evaluate one benchmark size without cross-replica interactions."""

    configuration = _configuration(
        replica_count
    )

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

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
        resonance_state=_resonance_state(
            replica_count
        ),
        provenance=ParameterProvenance.BENCHMARK,
        source=SOURCE_ID,
    )

    execution = _execution(
        replica_count
    )

    result = _model().evaluate(
        configuration=configuration,
        graph=graph,
        features=_features(
            replica_count
        ),
        resonance=descriptor,
        execution=execution,
    )

    composition = configuration.composition()

    return {
        "replica_count": replica_count,
        "atom_count": configuration.atom_count,
        "graph_edge_count": graph.edge_count,
        "atomic_energy_count": (
            result.energy_result.energy.atom_count
        ),
        "total_energy": (
            result.energy_result.energy.total_energy
        ),
        "energy_per_replica": (
            result.energy_result.energy.total_energy
            / float(replica_count)
        ),
        "lif_fraction": (
            composition.lif_fraction
        ),
        "bef2_fraction": (
            composition.bef2_fraction
        ),
        "resonance_coordinate": list(
            descriptor.coordinate
        ),
        "ternary_node_count": (
            execution.node_count
        ),
        "scalar_channel_count": (
            result
            .resonance_conditioned_features
            .scalar_channel_count
        ),
        "vector_channel_count": (
            result
            .resonance_conditioned_features
            .vector_channel_count
        ),
    }


def _close(
    actual: float,
    expected: float,
) -> bool:
    """Compare one scaling benchmark scalar."""

    return isclose(
        actual,
        expected,
        rel_tol=0.0,
        abs_tol=ABSOLUTE_TOLERANCE,
    )


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe TR-EIP size-scaling benchmark."""

    samples = tuple(
        _evaluate(
            replica_count
        )
        for replica_count in REPLICA_COUNTS
    )

    baseline = samples[0]

    baseline_atoms = baseline[
        "atom_count"
    ]
    baseline_edges = baseline[
        "graph_edge_count"
    ]
    baseline_energy = baseline[
        "total_energy"
    ]
    baseline_coordinate = baseline[
        "resonance_coordinate"
    ]

    assert isinstance(
        baseline_atoms,
        int,
    )
    assert isinstance(
        baseline_edges,
        int,
    )
    assert isinstance(
        baseline_energy,
        float,
    )
    assert isinstance(
        baseline_coordinate,
        list,
    )

    checks = {
        "atom_count_linear": all(
            sample["atom_count"]
            == baseline_atoms
            * sample["replica_count"]
            for sample in samples
        ),
        "graph_edge_count_linear": all(
            sample["graph_edge_count"]
            == baseline_edges
            * sample["replica_count"]
            for sample in samples
        ),
        "atomic_energy_count_linear": all(
            sample["atomic_energy_count"]
            == sample["atom_count"]
            for sample in samples
        ),
        "total_energy_extensive": all(
            _close(
                sample["total_energy"],
                baseline_energy
                * sample["replica_count"],
            )
            for sample in samples
        ),
        "energy_per_replica_constant": all(
            _close(
                sample["energy_per_replica"],
                baseline_energy,
            )
            for sample in samples
        ),
        "composition_preserved": all(
            _close(
                sample["lif_fraction"],
                2.0 / 3.0,
            )
            and _close(
                sample["bef2_fraction"],
                1.0 / 3.0,
            )
            for sample in samples
        ),
        "resonance_coordinate_preserved": all(
            sample["resonance_coordinate"]
            == baseline_coordinate
            for sample in samples
        ),
        "ternary_node_count_linear": all(
            sample["ternary_node_count"]
            == sample["atom_count"]
            for sample in samples
        ),
        "feature_channel_width_preserved": all(
            sample["scalar_channel_count"] == 3
            and sample["vector_channel_count"] == 1
            for sample in samples
        ),
    }

    status = (
        "PASS"
        if all(
            checks.values()
        )
        else "FAIL"
    )

    return {
        "benchmark_id": BENCHMARK_ID,
        "provenance": PROVENANCE,
        "status": status,
        "absolute_tolerance": (
            ABSOLUTE_TOLERANCE
        ),
        "replica_spacing": (
            REPLICA_SPACING
        ),
        "checks": checks,
        "observed": {
            "replica_counts": list(
                REPLICA_COUNTS
            ),
            "samples": list(
                samples
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
