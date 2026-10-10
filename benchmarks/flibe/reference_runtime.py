"""Structured runtime benchmark for the FLiBe TR-EIP reference path."""

from __future__ import annotations

import json
from math import isfinite, pi
from statistics import median
from time import perf_counter_ns

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


BENCHMARK_ID = "tr-eif.flibe.reference-runtime.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-runtime-v1"

CUTOFF = 1.6
REPLICA_SPACING = 10.0
REPLICA_COUNTS = (1, 2, 4, 8)

WARMUP_RUNS = 2
MEASUREMENT_RUNS = 9

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
    """Construct isolated translated FLiBe benchmark replicas."""

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
    """Repeat the fixed scalar-plus-vector node-feature pattern."""

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


def _evaluate(
    replica_count: int,
) -> tuple[int, int, float]:
    """Execute one complete FLiBe TR-EIP benchmark evaluation."""

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

    return (
        configuration.atom_count,
        graph.edge_count,
        result.energy_result.energy.total_energy,
    )


def _measure(
    replica_count: int,
) -> dict[str, object]:
    """Measure repeated complete TR-EIP evaluations for one system size."""

    for _ in range(WARMUP_RUNS):
        _evaluate(
            replica_count
        )

    durations_ns: list[int] = []

    reference_atom_count: int | None = None
    reference_edge_count: int | None = None
    reference_energy: float | None = None

    for _ in range(MEASUREMENT_RUNS):
        start_ns = perf_counter_ns()

        (
            atom_count,
            edge_count,
            total_energy,
        ) = _evaluate(
            replica_count
        )

        end_ns = perf_counter_ns()

        durations_ns.append(
            end_ns - start_ns
        )

        if reference_atom_count is None:
            reference_atom_count = atom_count
            reference_edge_count = edge_count
            reference_energy = total_energy
        else:
            if atom_count != reference_atom_count:
                raise RuntimeError(
                    "atom count changed between runtime measurements."
                )

            if edge_count != reference_edge_count:
                raise RuntimeError(
                    "graph edge count changed between runtime measurements."
                )

            if total_energy != reference_energy:
                raise RuntimeError(
                    "total energy changed between runtime measurements."
                )

    if reference_atom_count is None:
        raise RuntimeError(
            "runtime benchmark produced no measurements."
        )

    if reference_edge_count is None:
        raise RuntimeError(
            "runtime benchmark produced no graph measurement."
        )

    if reference_energy is None:
        raise RuntimeError(
            "runtime benchmark produced no energy measurement."
        )

    median_ns = float(
        median(
            durations_ns
        )
    )

    minimum_ns = min(
        durations_ns
    )

    maximum_ns = max(
        durations_ns
    )

    return {
        "replica_count": (
            replica_count
        ),
        "atom_count": (
            reference_atom_count
        ),
        "graph_edge_count": (
            reference_edge_count
        ),
        "measurement_count": (
            len(durations_ns)
        ),
        "durations_ns": (
            durations_ns
        ),
        "minimum_runtime_ns": (
            minimum_ns
        ),
        "median_runtime_ns": (
            median_ns
        ),
        "maximum_runtime_ns": (
            maximum_ns
        ),
        "median_runtime_ns_per_atom": (
            median_ns
            / float(
                reference_atom_count
            )
        ),
        "total_energy": (
            reference_energy
        ),
    }


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe TR-EIP runtime benchmark."""

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
        "measurement_count": all(
            sample[
                "measurement_count"
            ]
            == MEASUREMENT_RUNS
            for sample in samples
        ),
        "positive_runtime": all(
            sample[
                "minimum_runtime_ns"
            ] > 0
            and sample[
                "median_runtime_ns"
            ] > 0.0
            and sample[
                "maximum_runtime_ns"
            ] > 0
            for sample in samples
        ),
        "runtime_ordering_valid": all(
            sample[
                "minimum_runtime_ns"
            ]
            <= sample[
                "median_runtime_ns"
            ]
            <= sample[
                "maximum_runtime_ns"
            ]
            for sample in samples
        ),
        "runtime_per_atom_finite": all(
            isfinite(
                sample[
                    "median_runtime_ns_per_atom"
                ]
            )
            and sample[
                "median_runtime_ns_per_atom"
            ] > 0.0
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
            "clock": (
                "time.perf_counter_ns"
            ),
            "scope": (
                "one complete FLiBe TR-EIP evaluation"
            ),
            "warmup_runs": (
                WARMUP_RUNS
            ),
            "measurement_runs": (
                MEASUREMENT_RUNS
            ),
            "absolute_runtime_limit": None,
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
