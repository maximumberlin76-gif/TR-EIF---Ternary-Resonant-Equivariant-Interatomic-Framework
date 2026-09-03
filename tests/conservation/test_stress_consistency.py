"""Qualification tests for TR-EIF conservative stress evaluation."""

import math

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    CellStrainDifferentiation,
    ConservativeStressEvaluator,
    LinearInvariantEnergyFunctional,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
)
from tr_eif.graph import build_cutoff_graph
from tr_eif.ternary import (
    TernaryExecutionVector,
    TernaryState,
)


def _make_periodic_reference_system() -> tuple[
    AtomicConfiguration,
    NodeFeatureVector,
    TernaryExecutionVector,
]:
    """Construct a periodic two-atom stress reference system."""

    configuration = AtomicConfiguration(
        species=("A", "A"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
        cell=(
            (4.0, 0.0, 0.0),
            (0.0, 4.0, 0.0),
            (0.0, 0.0, 4.0),
        ),
        periodic=(True, True, True),
    )

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0,),
            ),
            NodeFeatures(
                scalars=(1.0,),
            ),
        )
    )

    execution = TernaryExecutionVector.from_retained_states(
        (
            TernaryState.NEUTRAL,
            TernaryState.NEUTRAL,
        )
    )

    return configuration, features, execution


def _make_reference_energy_model() -> ReferenceEnergyModel:
    """Construct the radial scalar reference energy model."""

    return ReferenceEnergyModel(
        message_operator=RadialMessageOperator(
            distance_scale=1.0,
        ),
        conditioning=TernaryConditioning(
            negative_scale=1.0,
            neutral_scale=1.0,
            positive_scale=1.0,
        ),
        energy_functional=LinearInvariantEnergyFunctional(
            weights=(1.0,),
            bias=0.0,
        ),
    )


def _evaluate_reference_stress():
    configuration, features, execution = (
        _make_periodic_reference_system()
    )

    graph = build_cutoff_graph(
        configuration=configuration,
        cutoff=2.0,
    )

    evaluator = ConservativeStressEvaluator(
        differentiation=CellStrainDifferentiation(
            step=1.0e-6,
        )
    )

    return evaluator.evaluate(
        model=_make_reference_energy_model(),
        configuration=configuration,
        graph=graph,
        features=features,
        execution=execution,
    )


def test_conservative_stress_is_finite() -> None:
    """Every evaluated stress component must be finite."""

    stress_state = _evaluate_reference_stress()

    for row in stress_state.tensor:
        for value in row:
            assert math.isfinite(value)


def test_conservative_stress_is_symmetric() -> None:
    """Symmetric strain differentiation must produce symmetric stress."""

    stress_state = _evaluate_reference_stress()

    assert stress_state.is_symmetric

    for row in range(3):
        for column in range(3):
            assert stress_state.tensor[row][column] == pytest.approx(
                stress_state.tensor[column][row],
                abs=1.0e-12,
            )


def test_axial_pair_has_zero_shear_stress() -> None:
    """An x-aligned reference pair must have zero shear components."""

    stress_state = _evaluate_reference_stress()

    shear_components = (
        stress_state.tensor[0][1],
        stress_state.tensor[0][2],
        stress_state.tensor[1][0],
        stress_state.tensor[1][2],
        stress_state.tensor[2][0],
        stress_state.tensor[2][1],
    )

    for value in shear_components:
        assert value == pytest.approx(
            0.0,
            abs=1.0e-8,
        )


def test_axial_pair_has_only_x_normal_stress() -> None:
    """The reference pair must not generate y or z normal stress."""

    stress_state = _evaluate_reference_stress()

    assert stress_state.tensor[0][0] != pytest.approx(
        0.0,
        abs=1.0e-8,
    )

    assert stress_state.tensor[1][1] == pytest.approx(
        0.0,
        abs=1.0e-8,
    )

    assert stress_state.tensor[2][2] == pytest.approx(
        0.0,
        abs=1.0e-8,
    )
