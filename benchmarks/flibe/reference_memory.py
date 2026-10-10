"""Structured memory-use benchmark for the FLiBe TR-EIP reference path."""

from __future__ import annotations

import gc
import json
from math import pi
import tracemalloc

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


BENCHMARK_ID = "tr-eif.flibe.reference-memory.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-memory-v1"

CUTOFF = 1.6
REPLICA_SPACING = 10.0
REPLICA_COUNTS = (1, 2, 4, 8)

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


def _configuration(
    replica_count: int,
) -> FLiBeConfiguration:
    """Construct isolated translated copies of the FLiBe benchmark fixture."""

    species: list[str] = []
    positions: list[tuple[float, float, float]] = []

    for replica_index in range(replica_count):
        offset = (
            REPLICA_SPACING
            * replica_index
        )

        species.extend(
            _BASE_SPECIES
        )

        positions.extend(
            (
                x + offset,
                y,
                z,
            )
            for x, y, z in _BASE_POSITIONS
        )

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=tuple(species),
            positions=tuple(positions),
        )
    )


def _features(
    replica_count: int,
) -> NodeFeatureVector:
    """Repeat the fixed scalar-plus-vector feature pattern."""

    nodes: list[NodeFeatures] = []

    for _ in range(replica_count):
        nodes.extend(
            NodeFeatures(
                scalars=(
                    0.5
                    + 0.25 * index,
                ),
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

    return NodeFeatureVector(
        nodes=tuple(nodes)
    )


def _resonance_state(
    replica_count: int,
) -> ResonanceState:
    """Repeat the fixed continuous resonance pattern."""

    return ResonanceState(
        phases=(
            _BASE_PHASES
            * replica_count
        ),
        frequencies=(
            _BASE_FREQUENCIES
            * replica_count
        ),
    )


def _execution(
    replica_count: int,
) -> TernaryExecutionVector:
    """Repeat the fixed retained balanced-ternary state."""

    return TernaryExecutionVector.from_retained_states(
        _BASE_TERNARY_STATES
        * replica_count
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
                weights=(
                    0.4,
                    0.7,
                    -0.3,
                ),
                bias=0.1,
            ),
        ),
        provenance=ParameterProvenance.BENCHMARK,
        source=SOURCE_ID,
    )


def _measure(
    replica_count: int,
) -> dict[str, object]:
    """Measure traced Python allocations for one complete TR-EIP evaluation."""

    gc.collect()

    tracemalloc.start()

    try:
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

        current_bytes, peak_bytes = (
            tracemalloc.get_traced_memory()
        )

        atom_count = (
            configuration.atom_count
        )

        return {
            "replica_count": (
                replica_count
            ),
            "atom_count": (
                atom_count
            ),
            "graph_edge_count": (
                graph.edge_count
            ),
            "current_traced_bytes": (
                current_bytes
            ),
            "peak_traced_bytes": (
                peak_bytes
            ),
            "peak_bytes_per_atom": (
                peak_bytes
                / float(atom_count)
            ),
            "total_energy": (
                result
                .energy_result
                .energy
                .total_energy
            ),
            "resonance_coordinate": list(
                descriptor.coordinate
            ),
            "ternary_node_count": (
                execution.node_count
            ),
        }

    finally:
        tracemalloc.stop()


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe TR-EIP memory-use benchmark."""

    samples = tuple(
        _measure(
            replica_count
        )
        for replica_count in REPLICA_COUNTS
    )

    checks = {
        "replica_sequence": (
            tuple(
                sample[
                    "replica_count"
                ]
                for sample in samples
            )
            == REPLICA_COUNTS
        ),
        "atom_count_linear": all(
            sample[
                "atom_count"
            ]
            == (
                7
                * sample[
                    "replica_count"
                ]
            )
            for sample in samples
        ),
        "memory_measurements_positive": all(
            sample[
                "current_traced_bytes"
            ] >= 0
            and sample[
                "peak_traced_bytes"
            ] > 0
            for sample in samples
        ),
        "peak_not_below_current": all(
            sample[
                "peak_traced_bytes"
            ]
            >= sample[
                "current_traced_bytes"
            ]
            for sample in samples
        ),
        "peak_per_atom_positive": all(
            sample[
                "peak_bytes_per_atom"
            ] > 0.0
            for sample in samples
        ),
        "ternary_node_count_matches_atoms": all(
            sample[
                "ternary_node_count"
            ]
            == sample[
                "atom_count"
            ]
            for sample in samples
        ),
        "resonance_coordinate_defined": all(
            len(
                sample[
                    "resonance_coordinate"
                ]
            )
            == 2
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
        "benchmark_id": (
            BENCHMARK_ID
        ),
        "provenance": (
            PROVENANCE
        ),
        "status": (
            status
        ),
        "measurement": {
            "allocator": (
                "python-tracemalloc"
            ),
            "scope": (
                "traced Python allocations during one "
                "complete FLiBe TR-EIP evaluation"
            ),
            "absolute_memory_limit": None,
        },
        "checks": (
            checks
        ),
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
    """Run the benchmark and emit structured JSON."""

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
