"""Conservation-layer tests for TR-EIF molecular-dynamics energy observables."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import EnergyState
from tr_eif.md.observables import (
    KineticEnergyState,
    MolecularDynamicsEnergyState,
    kinetic_energy,
    molecular_dynamics_energy,
)
from tr_eif.md.state import MolecularDynamicsState


def _make_state() -> MolecularDynamicsState:
    """Construct a deterministic molecular-dynamics state."""

    return MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=("A", "B"),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
        ),
        velocities=(
            (2.0, 0.0, 0.0),
            (0.0, 3.0, 0.0),
        ),
        masses=(
            2.0,
            4.0,
        ),
        step=0,
        time=0.0,
    )


def test_kinetic_energy_matches_classical_definition() -> None:
    """Per-atom kinetic energy must equal 0.5 * m * |v|^2."""

    result = kinetic_energy(_make_state())

    assert result.atomic_kinetic_energies == (
        pytest.approx(4.0),
        pytest.approx(18.0),
    )
    assert result.total_kinetic_energy == pytest.approx(22.0)


def test_zero_velocity_has_zero_kinetic_energy() -> None:
    """Zero velocity must produce zero kinetic energy."""

    state = MolecularDynamicsState(
        configuration=AtomicConfiguration(
            species=("A",),
            positions=((0.0, 0.0, 0.0),),
        ),
        velocities=((0.0, 0.0, 0.0),),
        masses=(5.0,),
    )

    result = kinetic_energy(state)

    assert result.atomic_kinetic_energies == (0.0,)
    assert result.total_kinetic_energy == 0.0


def test_kinetic_energy_state_requires_exact_total() -> None:
    """Stored total kinetic energy must equal atomic contributions."""

    with pytest.raises(
        ValueError,
        match="total_kinetic_energy must equal",
    ):
        KineticEnergyState(
            atomic_kinetic_energies=(
                1.0,
                2.0,
            ),
            total_kinetic_energy=4.0,
        )


def test_kinetic_energy_state_rejects_negative_atomic_energy() -> None:
    """Atomic kinetic-energy contributions must be nonnegative."""

    with pytest.raises(
        ValueError,
        match="must be nonnegative",
    ):
        KineticEnergyState.from_atomic_kinetic_energies(
            (
                1.0,
                -1.0,
            )
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_kinetic_energy_state_rejects_nonfinite_values(
    invalid_value: float,
) -> None:
    """Kinetic-energy state must reject nonfinite values."""

    with pytest.raises(ValueError):
        KineticEnergyState.from_atomic_kinetic_energies(
            (
                invalid_value,
            )
        )


def test_molecular_dynamics_energy_combines_kinetic_and_potential() -> None:
    """Total MD energy must equal kinetic plus potential energy."""

    state = _make_state()

    potential = EnergyState.from_atomic_energies(
        (
            0.25,
            0.75,
        )
    )

    result = molecular_dynamics_energy(
        state=state,
        potential=potential,
    )

    assert result.kinetic.total_kinetic_energy == pytest.approx(22.0)
    assert result.potential.total_energy == pytest.approx(1.0)
    assert result.total_energy == pytest.approx(23.0)


def test_negative_potential_energy_is_supported() -> None:
    """Potential energy may be negative while total accounting remains exact."""

    state = _make_state()

    potential = EnergyState.from_atomic_energies(
        (
            -10.0,
            -15.0,
        )
    )

    result = molecular_dynamics_energy(
        state=state,
        potential=potential,
    )

    assert result.kinetic.total_kinetic_energy == pytest.approx(22.0)
    assert result.potential.total_energy == pytest.approx(-25.0)
    assert result.total_energy == pytest.approx(-3.0)


def test_molecular_dynamics_energy_requires_matching_atom_count() -> None:
    """Potential and MD state atom counts must match."""

    state = _make_state()

    potential = EnergyState.from_atomic_energies(
        (
            1.0,
        )
    )

    with pytest.raises(
        ValueError,
        match="potential atom count must match",
    ):
        molecular_dynamics_energy(
            state=state,
            potential=potential,
        )


def test_combined_energy_state_requires_exact_total() -> None:
    """Stored total MD energy must equal kinetic plus potential."""

    kinetic = KineticEnergyState.from_atomic_kinetic_energies(
        (
            4.0,
            18.0,
        )
    )

    potential = EnergyState.from_atomic_energies(
        (
            0.25,
            0.75,
        )
    )

    with pytest.raises(
        ValueError,
        match="total_energy must equal kinetic plus",
    ):
        MolecularDynamicsEnergyState(
            kinetic=kinetic,
            potential=potential,
            total_energy=24.0,
        )


def test_combined_energy_state_requires_matching_atom_count() -> None:
    """Kinetic and potential energy states must refer to the same atom count."""

    kinetic = KineticEnergyState.from_atomic_kinetic_energies(
        (
            4.0,
            18.0,
        )
    )

    potential = EnergyState.from_atomic_energies(
        (
            1.0,
        )
    )

    with pytest.raises(
        ValueError,
        match="kinetic and potential atom counts must match",
    ):
        MolecularDynamicsEnergyState.combine(
            kinetic=kinetic,
            potential=potential,
        )


def test_kinetic_energy_atom_count_matches_md_state() -> None:
    """Kinetic-energy state atom count must match the source MD state."""

    state = _make_state()
    result = kinetic_energy(state)

    assert result.atom_count == state.atom_count


def test_molecular_dynamics_energy_atom_count_matches_md_state() -> None:
    """Combined energy state must preserve the MD atom count."""

    state = _make_state()

    potential = EnergyState.from_atomic_energies(
        (
            0.25,
            0.75,
        )
    )

    result = molecular_dynamics_energy(
        state=state,
        potential=potential,
    )

    assert result.atom_count == state.atom_count
