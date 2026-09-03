"""Energy observables for TR-EIF molecular-dynamics trajectories."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy import ReferenceEnergyModel
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.graph import build_cutoff_graph
from tr_eif.ternary import TernaryExecutionVector

from .observables import (
    MolecularDynamicsEnergyState,
    molecular_dynamics_energy,
)
from .trajectory import MolecularDynamicsTrajectory


@dataclass(frozen=True, slots=True)
class MolecularDynamicsTrajectoryEnergy:
    """Ordered energy observations for one MD trajectory."""

    energies: tuple[MolecularDynamicsEnergyState, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.energies, tuple):
            raise TypeError(
                "energies must be a tuple."
            )

        if len(self.energies) == 0:
            raise ValueError(
                "energies must not be empty."
            )

        for index, energy in enumerate(self.energies):
            if not isinstance(
                energy,
                MolecularDynamicsEnergyState,
            ):
                raise TypeError(
                    f"energies[{index}] must be a "
                    "MolecularDynamicsEnergyState instance."
                )

        atom_count = self.energies[0].atom_count

        for energy in self.energies[1:]:
            if energy.atom_count != atom_count:
                raise ValueError(
                    "all trajectory energy states must have "
                    "the same atom count."
                )

    @property
    def state_count(self) -> int:
        """Return the number of observed trajectory states."""

        return len(self.energies)

    @property
    def atom_count(self) -> int:
        """Return the common atom count."""

        return self.energies[0].atom_count

    @property
    def initial(self) -> MolecularDynamicsEnergyState:
        """Return the initial trajectory energy state."""

        return self.energies[0]

    @property
    def final(self) -> MolecularDynamicsEnergyState:
        """Return the final trajectory energy state."""

        return self.energies[-1]

    @property
    def total_energies(self) -> tuple[float, ...]:
        """Return ordered total MD energies."""

        return tuple(
            energy.total_energy
            for energy in self.energies
        )

    @property
    def kinetic_energies(self) -> tuple[float, ...]:
        """Return ordered total kinetic energies."""

        return tuple(
            energy.kinetic.total_kinetic_energy
            for energy in self.energies
        )

    @property
    def potential_energies(self) -> tuple[float, ...]:
        """Return ordered total potential energies."""

        return tuple(
            energy.potential.total_energy
            for energy in self.energies
        )


def evaluate_trajectory_energy(
    trajectory: MolecularDynamicsTrajectory,
    model: ReferenceEnergyModel,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
    cutoff: float,
) -> MolecularDynamicsTrajectoryEnergy:
    """Evaluate kinetic, potential, and total energy along an MD trajectory."""

    if not isinstance(
        trajectory,
        MolecularDynamicsTrajectory,
    ):
        raise TypeError(
            "trajectory must be a MolecularDynamicsTrajectory instance."
        )

    if not isinstance(
        model,
        ReferenceEnergyModel,
    ):
        raise TypeError(
            "model must be a ReferenceEnergyModel instance."
        )

    if not isinstance(
        features,
        NodeFeatureVector,
    ):
        raise TypeError(
            "features must be a NodeFeatureVector instance."
        )

    if not isinstance(
        execution,
        TernaryExecutionVector,
    ):
        raise TypeError(
            "execution must be a TernaryExecutionVector instance."
        )

    if features.node_count != trajectory.atom_count:
        raise ValueError(
            "feature node count must match trajectory atom count."
        )

    if execution.node_count != trajectory.atom_count:
        raise ValueError(
            "ternary execution node count must match "
            "trajectory atom count."
        )

    observed: list[MolecularDynamicsEnergyState] = []

    for state in trajectory.states:
        graph = build_cutoff_graph(
            configuration=state.configuration,
            cutoff=cutoff,
        )

        potential = model.evaluate(
            configuration=state.configuration,
            features=features,
            execution=execution,
            graph=graph,
        )

        observed.append(
            molecular_dynamics_energy(
                state=state,
                potential=potential,
            )
        )

    return MolecularDynamicsTrajectoryEnergy(
        energies=tuple(observed),
    )
