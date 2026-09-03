"""Qualification tests for TR-EIF energy consistency."""

import pytest

from tr_eif.energy import (
    EnergyState,
    LinearInvariantEnergyFunctional,
)
from tr_eif.equivariant import (
    NodeFeatures,
    NodeFeatureVector,
)


def test_total_energy_equals_sum_of_atomic_energies() -> None:
    """Total energy must equal the deterministic sum of atomic terms."""

    atomic_energies = (
        -1.25,
        0.50,
        2.75,
        -0.75,
    )

    state = EnergyState.from_atomic_energies(atomic_energies)

    assert state.atomic_energies == atomic_energies
    assert state.total_energy == pytest.approx(
        sum(atomic_energies)
    )


def test_linear_functional_matches_scalar_channel_definition() -> None:
    """Linear invariant energy must follow its scalar-channel equation."""

    features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0, 2.0),
                vectors=((10.0, 20.0, 30.0),),
            ),
            NodeFeatures(
                scalars=(-1.0, 0.5),
                vectors=((-4.0, 5.0, 6.0),),
            ),
        )
    )

    functional = LinearInvariantEnergyFunctional(
        weights=(2.0, -0.5),
        bias=0.25,
    )

    state = functional.evaluate(features)

    expected_first = 0.25 + 2.0 * 1.0 - 0.5 * 2.0
    expected_second = 0.25 + 2.0 * -1.0 - 0.5 * 0.5

    assert state.atomic_energies == pytest.approx(
        (
            expected_first,
            expected_second,
        )
    )

    assert state.total_energy == pytest.approx(
        expected_first + expected_second
    )


def test_vector_channels_do_not_directly_change_linear_energy() -> None:
    """Vector channels must not enter the scalar energy functional directly."""

    first_features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0, -2.0),
                vectors=((1.0, 0.0, 0.0),),
            ),
            NodeFeatures(
                scalars=(0.5, 3.0),
                vectors=((0.0, 1.0, 0.0),),
            ),
        )
    )

    second_features = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(1.0, -2.0),
                vectors=((100.0, -50.0, 25.0),),
            ),
            NodeFeatures(
                scalars=(0.5, 3.0),
                vectors=((-8.0, 7.0, 6.0),),
            ),
        )
    )

    functional = LinearInvariantEnergyFunctional(
        weights=(0.75, -1.25),
        bias=-0.5,
    )

    first = functional.evaluate(first_features)
    second = functional.evaluate(second_features)

    assert first.atomic_energies == second.atomic_energies
    assert first.total_energy == second.total_energy


def test_energy_is_invariant_to_polar_vector_sign_change() -> None:
    """Changing only polar-vector channels must preserve direct energy."""

    positive_vectors = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(2.0,),
                vectors=((1.0, 2.0, 3.0),),
            ),
        )
    )

    reversed_vectors = NodeFeatureVector(
        nodes=(
            NodeFeatures(
                scalars=(2.0,),
                vectors=((-1.0, -2.0, -3.0),),
            ),
        )
    )

    functional = LinearInvariantEnergyFunctional(
        weights=(1.5,),
        bias=0.125,
    )

    first = functional.evaluate(positive_vectors)
    second = functional.evaluate(reversed_vectors)

    assert first.atomic_energies == second.atomic_energies
    assert first.total_energy == second.total_energy
