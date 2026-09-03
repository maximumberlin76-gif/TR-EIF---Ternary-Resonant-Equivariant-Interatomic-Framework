"""Energy observables for TR-EIF molecular dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.energy import EnergyState

from .state import MolecularDynamicsState


AtomicKineticEnergies: TypeAlias = tuple[float, ...]


def _validate_finite_energy(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one finite scalar energy value."""

    if not isinstance(value, (int, float)) or isinstance(
        value,
        bool,
    ):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    return float(value)


@dataclass(frozen=True, slots=True)
class KineticEnergyState:
    """Immutable per-atom and total molecular-dynamics kinetic energy."""

    atomic_kinetic_energies: AtomicKineticEnergies
    total_kinetic_energy: float

    def __post_init__(self) -> None:
        if not isinstance(
            self.atomic_kinetic_energies,
            tuple,
        ):
            raise TypeError(
                "atomic_kinetic_energies must be a tuple."
            )

        if len(self.atomic_kinetic_energies) == 0:
            raise ValueError(
                "atomic_kinetic_energies must not be empty."
            )

        validated = tuple(
            _validate_finite_energy(
                value,
                field_name=(
                    f"atomic_kinetic_energies[{index}]"
                ),
            )
            for index, value in enumerate(
                self.atomic_kinetic_energies
            )
        )

        for index, value in enumerate(validated):
            if value < 0.0:
                raise ValueError(
                    "atomic_kinetic_energies"
                    f"[{index}] must be nonnegative."
                )

        total = _validate_finite_energy(
            self.total_kinetic_energy,
            field_name="total_kinetic_energy",
        )

        if total < 0.0:
            raise ValueError(
                "total_kinetic_energy must be nonnegative."
            )

        expected_total = sum(validated)

        if total != expected_total:
            raise ValueError(
                "total_kinetic_energy must equal the sum "
                "of atomic kinetic energies."
            )

        object.__setattr__(
            self,
            "atomic_kinetic_energies",
            validated,
        )

        object.__setattr__(
            self,
            "total_kinetic_energy",
            total,
        )

    @classmethod
    def from_atomic_kinetic_energies(
        cls,
        atomic_kinetic_energies: AtomicKineticEnergies,
    ) -> KineticEnergyState:
        """Construct kinetic energy from atomic contributions."""

        if not isinstance(
            atomic_kinetic_energies,
            tuple,
        ):
            raise TypeError(
                "atomic_kinetic_energies must be a tuple."
            )

        if len(atomic_kinetic_energies) == 0:
            raise ValueError(
                "atomic_kinetic_energies must not be empty."
            )

        validated = tuple(
            _validate_finite_energy(
                value,
                field_name=(
                    f"atomic_kinetic_energies[{index}]"
                ),
            )
            for index, value in enumerate(
                atomic_kinetic_energies
            )
        )

        for index, value in enumerate(validated):
            if value < 0.0:
                raise ValueError(
                    "atomic_kinetic_energies"
                    f"[{index}] must be nonnegative."
                )

        return cls(
            atomic_kinetic_energies=validated,
            total_kinetic_energy=sum(validated),
        )

    @property
    def atom_count(self) -> int:
        """Return the number of atomic kinetic-energy contributions."""

        return len(self.atomic_kinetic_energies)


@dataclass(frozen=True, slots=True)
class MolecularDynamicsEnergyState:
    """Combined kinetic and potential energy for one MD state."""

    kinetic: KineticEnergyState
    potential: EnergyState
    total_energy: float

    def __post_init__(self) -> None:
        if not isinstance(
            self.kinetic,
            KineticEnergyState,
        ):
            raise TypeError(
                "kinetic must be a KineticEnergyState instance."
            )

        if not isinstance(
            self.potential,
            EnergyState,
        ):
            raise TypeError(
                "potential must be an EnergyState instance."
            )

        if self.kinetic.atom_count != self.potential.atom_count:
            raise ValueError(
                "kinetic and potential atom counts must match."
            )

        total = _validate_finite_energy(
            self.total_energy,
            field_name="total_energy",
        )

        expected_total = (
            self.kinetic.total_kinetic_energy
            + self.potential.total_energy
        )

        if total != expected_total:
            raise ValueError(
                "total_energy must equal kinetic plus "
                "potential energy."
            )

        object.__setattr__(
            self,
            "total_energy",
            total,
        )

    @classmethod
    def combine(
        cls,
        kinetic: KineticEnergyState,
        potential: EnergyState,
    ) -> MolecularDynamicsEnergyState:
        """Combine kinetic and potential energy states."""

        if not isinstance(
            kinetic,
            KineticEnergyState,
        ):
            raise TypeError(
                "kinetic must be a KineticEnergyState instance."
            )

        if not isinstance(
            potential,
            EnergyState,
        ):
            raise TypeError(
                "potential must be an EnergyState instance."
            )

        return cls(
            kinetic=kinetic,
            potential=potential,
            total_energy=(
                kinetic.total_kinetic_energy
                + potential.total_energy
            ),
        )

    @property
    def atom_count(self) -> int:
        """Return the common energy-state atom count."""

        return self.kinetic.atom_count


def kinetic_energy(
    state: MolecularDynamicsState,
) -> KineticEnergyState:
    """Evaluate per-atom and total kinetic energy for one MD state."""

    if not isinstance(
        state,
        MolecularDynamicsState,
    ):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    atomic_kinetic_energies = tuple(
        0.5
        * mass
        * (
            velocity[0] * velocity[0]
            + velocity[1] * velocity[1]
            + velocity[2] * velocity[2]
        )
        for mass, velocity in zip(
            state.masses,
            state.velocities,
            strict=True,
        )
    )

    return KineticEnergyState.from_atomic_kinetic_energies(
        atomic_kinetic_energies
    )


def molecular_dynamics_energy(
    state: MolecularDynamicsState,
    potential: EnergyState,
) -> MolecularDynamicsEnergyState:
    """Combine an MD state's kinetic energy with potential energy."""

    if not isinstance(
        state,
        MolecularDynamicsState,
    ):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    if not isinstance(
        potential,
        EnergyState,
    ):
        raise TypeError(
            "potential must be an EnergyState instance."
        )

    if potential.atom_count != state.atom_count:
        raise ValueError(
            "potential atom count must match MD state atom count."
        )

    kinetic = kinetic_energy(state)

    return MolecularDynamicsEnergyState.combine(
        kinetic=kinetic,
        potential=potential,
    )
