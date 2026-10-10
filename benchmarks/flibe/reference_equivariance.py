"""Structured E(3) equivariance benchmark for the FLiBe TR-EIP reference path."""

from __future__ import annotations

import json
from math import isclose, pi

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
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import build_flibe_coordination_state
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.reference-equivariance.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-equivariance-v1"

CUTOFF = 1.6

ENERGY_ABSOLUTE_TOLERANCE = 1.0e-12
FORCE_ABSOLUTE_TOLERANCE = 1.0e-7


TRANSFORMATIONS = (
    (
        "translation",
        E3Transformation(
            matrix=(
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(4.0, -3.0, 2.0),
        ),
    ),
    (
        "rotation_z_90",
        E3Transformation(
            matrix=(
                (0.0, -1.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(1.0, 2.0, -4.0),
        ),
    ),
    (
        "reflection_x",
        E3Transformation(
            matrix=(
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
            translation=(-2.0, 3.0, 1.0),
        ),
    ),
    (
        "cyclic_axis_rotation",
        E3Transformation(
            matrix=(
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
                (1.0, 0.0, 0.0),
            ),
            translation=(2.0, -1.0, 3.0),
        ),
    ),
)


def _configuration() -> FLiBeConfiguration:
    """Construct the fixed non-collinear FLiBe benchmark geometry."""

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


def _transform_configuration(
    configuration: FLiBeConfiguration,
    transformation: E3Transformation,
) -> FLiBeConfiguration:
    """Apply one E(3) transformation to FLiBe Cartesian geometry."""

    base = configuration.configuration

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=base.species,
            positions=tuple(
                transformation.transform_position(position)
                for position in base.positions
            ),
            periodic=base.periodic,
        )
    )


def _descriptor(
    configuration: FLiBeConfiguration,
):
    """Bind the fixed resonance state to one benchmark geometry."""

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

    return build_flibe_resonance_descriptor(
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


def _evaluate(
    configuration: FLiBeConfiguration,
    features: NodeFeatureVector,
):
    """Evaluate scalar energy and conservative forces in one E(3) frame."""

    graph = build_cutoff_graph(
        configuration.configuration,
        cutoff=CUTOFF,
    )

    model = _model()
    execution = _execution()
    descriptor = _descriptor(
        configuration
    )

    result = model.evaluate(
        configuration=configuration,
        graph=graph,
        features=features,
        resonance=descriptor,
        execution=execution,
    )

    forces = ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=1.0e-6,
        )
    ).evaluate(
        model=model.energy_model,
        configuration=configuration.configuration,
        graph=graph,
        features=result.resonance_conditioned_features,
        execution=execution,
    ).forces

    return (
        graph,
        descriptor,
        result,
        forces,
    )


def _vector_max_absolute_error(
    actual: tuple[
        tuple[float, float, float],
        ...,
    ],
    expected: tuple[
        tuple[float, float, float],
        ...,
    ],
) -> float:
    """Return the maximum Cartesian component error."""

    return max(
        abs(
            actual_component
            - expected_component
        )
        for actual_vector, expected_vector in zip(
            actual,
            expected,
            strict=True,
        )
        for actual_component, expected_component in zip(
            actual_vector,
            expected_vector,
            strict=True,
        )
    )


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe E(3) equivariance benchmark."""

    configuration = _configuration()
    features = _features()

    (
        reference_graph,
        reference_descriptor,
        reference_result,
        reference_forces,
    ) = _evaluate(
        configuration,
        features,
    )

    reference_energy = (
        reference_result
        .energy_result
        .energy
        .total_energy
    )

    transformation_reports: list[
        dict[str, object]
    ] = []

    for transformation_id, transformation in TRANSFORMATIONS:
        transformed_configuration = _transform_configuration(
            configuration,
            transformation,
        )

        transformed_features = (
            transformation
            .transform_feature_vector(
                features
            )
        )

        (
            graph,
            descriptor,
            result,
            forces,
        ) = _evaluate(
            transformed_configuration,
            transformed_features,
        )

        transformed_energy = (
            result
            .energy_result
            .energy
            .total_energy
        )

        energy_error = abs(
            transformed_energy
            - reference_energy
        )

        expected_forces = tuple(
            transformation.transform_vector(
                force
            )
            for force in reference_forces
        )

        force_error = (
            _vector_max_absolute_error(
                forces,
                expected_forces,
            )
        )

        resonance_coordinate_match = all(
            isclose(
                actual,
                expected,
                rel_tol=0.0,
                abs_tol=(
                    ENERGY_ABSOLUTE_TOLERANCE
                ),
            )
            for actual, expected in zip(
                descriptor.coordinate,
                reference_descriptor.coordinate,
                strict=True,
            )
        )

        checks = {
            "graph_edge_count_preserved": (
                graph.edge_count
                == reference_graph.edge_count
            ),
            "resonance_coordinate_preserved": (
                resonance_coordinate_match
            ),
            "energy_invariant": (
                energy_error
                <= ENERGY_ABSOLUTE_TOLERANCE
            ),
            "forces_equivariant": (
                force_error
                <= FORCE_ABSOLUTE_TOLERANCE
            ),
        }

        transformation_reports.append(
            {
                "transformation_id": (
                    transformation_id
                ),
                "status": (
                    "PASS"
                    if all(
                        checks.values()
                    )
                    else "FAIL"
                ),
                "checks": checks,
                "observed": {
                    "energy_absolute_error": (
                        energy_error
                    ),
                    "force_max_absolute_error": (
                        force_error
                    ),
                    "graph_edge_count": (
                        graph.edge_count
                    ),
                    "resonance_coordinate": list(
                        descriptor.coordinate
                    ),
                },
            }
        )

    status = (
        "PASS"
        if all(
            report["status"] == "PASS"
            for report
            in transformation_reports
        )
        else "FAIL"
    )

    return {
        "benchmark_id": BENCHMARK_ID,
        "provenance": PROVENANCE,
        "status": status,
        "energy_absolute_tolerance": (
            ENERGY_ABSOLUTE_TOLERANCE
        ),
        "force_absolute_tolerance": (
            FORCE_ABSOLUTE_TOLERANCE
        ),
        "reference": {
            "total_energy": (
                reference_energy
            ),
            "graph_edge_count": (
                reference_graph.edge_count
            ),
            "resonance_coordinate": list(
                reference_descriptor.coordinate
            ),
        },
        "transformations": (
            transformation_reports
        ),
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
