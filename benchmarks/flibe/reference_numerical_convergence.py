"""Structured numerical-convergence benchmark for the FLiBe TR-EIP force path."""

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
from tr_eif.flibe.resonance_descriptor import build_flibe_resonance_descriptor
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.tr_eip import FLiBeTREIPModel
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import ResonanceState
from tr_eif.ternary import TernaryExecutionVector, TernaryState


BENCHMARK_ID = "tr-eif.flibe.reference-numerical-convergence.v1"
PROVENANCE = "BENCHMARK"
SOURCE_ID = "BENCHMARK:flibe-reference-numerical-convergence-v1"

CUTOFF = 1.6
REFERENCE_STEP = 1.0e-7

CONVERGENCE_STEPS = (
    1.0e-2,
    5.0e-3,
    2.5e-3,
    1.25e-3,
)

MINIMUM_ERROR_REDUCTION_RATIO = 3.5
FINAL_ERROR_TOLERANCE = 2.0e-6


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


def _force_components(
    step: float,
    configuration: FLiBeConfiguration,
    model: FLiBeTREIPModel,
    graph,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
) -> tuple[tuple[float, float, float], ...]:
    """Evaluate the fixed-graph force estimate for one differentiation step."""

    return ConservativeForceEvaluator(
        differentiation=CoordinateDifferentiation(
            step=step,
        )
    ).evaluate(
        model=model.energy_model,
        configuration=configuration.configuration,
        graph=graph,
        features=features,
        execution=execution,
    ).forces


def _max_component_error(
    actual: tuple[tuple[float, float, float], ...],
    reference: tuple[tuple[float, float, float], ...],
) -> float:
    """Return the maximum absolute Cartesian force-component error."""

    return max(
        abs(actual_component - reference_component)
        for actual_vector, reference_vector in zip(
            actual,
            reference,
            strict=True,
        )
        for actual_component, reference_component in zip(
            actual_vector,
            reference_vector,
            strict=True,
        )
    )


def run_benchmark() -> dict[str, object]:
    """Run the structured FLiBe force-gradient convergence benchmark."""

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

    conditioned_features = (
        tr_eip_result.resonance_conditioned_features
    )

    reference_forces = _force_components(
        REFERENCE_STEP,
        configuration,
        model,
        graph,
        conditioned_features,
        execution,
    )

    errors: list[float] = []
    step_reports: list[dict[str, float]] = []

    for step in CONVERGENCE_STEPS:
        forces = _force_components(
            step,
            configuration,
            model,
            graph,
            conditioned_features,
            execution,
        )

        error = _max_component_error(
            forces,
            reference_forces,
        )

        errors.append(error)

        step_reports.append(
            {
                "step": step,
                "max_force_component_error": error,
