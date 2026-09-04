"""Graph-relative coordination contract for the TR-EIF FLiBe domain layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from tr_eif.graph import InteractionGraph

from .configuration import FLiBeConfiguration
from .species import FLiBeSpecies


SpeciesCoordination: TypeAlias = tuple[
    tuple[FLiBeSpecies, int],
    ...,
]


def _validate_count(
    value: int,
    name: str,
) -> int:
    """Validate one nonnegative coordination count."""

    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(
            f"{name} must be an integer."
        )

    if value < 0:
        raise ValueError(
            f"{name} must be nonnegative."
        )

    return value


@dataclass(frozen=True)
class FLiBeAtomCoordination:
    """Species-resolved graph coordination for one FLiBe atom."""

    atom_index: int
    species: FLiBeSpecies
    lithium_neighbors: int
    beryllium_neighbors: int
    fluorine_neighbors: int

    def __post_init__(self) -> None:
        """Validate atom identity and all graph-relative neighbor counts."""

        _validate_count(
            self.atom_index,
            "atom_index",
        )

        if not isinstance(
            self.species,
            FLiBeSpecies,
        ):
            raise TypeError(
                "species must be an FLiBeSpecies."
            )

        object.__setattr__(
            self,
            "lithium_neighbors",
            _validate_count(
                self.lithium_neighbors,
                "lithium_neighbors",
            ),
        )
        object.__setattr__(
            self,
            "beryllium_neighbors",
            _validate_count(
                self.beryllium_neighbors,
                "beryllium_neighbors",
            ),
        )
        object.__setattr__(
            self,
            "fluorine_neighbors",
            _validate_count(
                self.fluorine_neighbors,
                "fluorine_neighbors",
            ),
        )

    @property
    def total_neighbors(self) -> int:
        """Return the total number of incoming graph-neighbor records."""

        return (
            self.lithium_neighbors
            + self.beryllium_neighbors
            + self.fluorine_neighbors
        )

    @property
    def species_coordination(
        self,
    ) -> SpeciesCoordination:
        """Return neighbor counts in canonical Li, Be, F order."""

        return (
            (
                FLiBeSpecies.LITHIUM,
                self.lithium_neighbors,
            ),
            (
                FLiBeSpecies.BERYLLIUM,
                self.beryllium_neighbors,
            ),
            (
                FLiBeSpecies.FLUORINE,
                self.fluorine_neighbors,
            ),
        )


@dataclass(frozen=True)
class FLiBeCoordinationState:
    """Graph-relative coordination state for one FLiBe configuration."""

    atoms: tuple[FLiBeAtomCoordination, ...]

    def __post_init__(self) -> None:
        """Validate atom records and contiguous configuration ordering."""

        if not isinstance(
            self.atoms,
            tuple,
        ):
            raise TypeError(
                "atoms must be a tuple."
            )

        if not self.atoms:
            raise ValueError(
                "atoms must not be empty."
            )

        for index, atom in enumerate(
            self.atoms
        ):
            if not isinstance(
                atom,
                FLiBeAtomCoordination,
            ):
                raise TypeError(
                    f"atoms[{index}] must be an "
                    "FLiBeAtomCoordination."
                )

            if atom.atom_index != index:
                raise ValueError(
                    "atom coordination records must use "
                    "contiguous configuration ordering."
                )

    @property
    def atom_count(self) -> int:
        """Return the number of represented atoms."""

        return len(
            self.atoms
        )

    @property
    def total_neighbor_records(self) -> int:
        """Return the total number of incoming directed graph records."""

        return sum(
            atom.total_neighbors
            for atom in self.atoms
        )


def build_flibe_coordination_state(
    configuration: FLiBeConfiguration,
    graph: InteractionGraph,
) -> FLiBeCoordinationState:
    """Build species-resolved coordination from a supplied interaction graph."""

    if not isinstance(
        configuration,
        FLiBeConfiguration,
    ):
        raise TypeError(
            "configuration must be an FLiBeConfiguration."
        )

    if not isinstance(
        graph,
        InteractionGraph,
    ):
        raise TypeError(
            "graph must be an InteractionGraph."
        )

    if graph.node_count != configuration.atom_count:
        raise ValueError(
            "graph node_count must match FLiBe configuration atom_count."
        )

    species = configuration.species
    atoms: list[FLiBeAtomCoordination] = []

    for receiver in range(
        graph.node_count
    ):
        counts = {
            FLiBeSpecies.LITHIUM: 0,
            FLiBeSpecies.BERYLLIUM: 0,
            FLiBeSpecies.FLUORINE: 0,
        }

        for edge in graph.incoming_edges(
            receiver
        ):
            if edge.source == receiver:
                raise ValueError(
                    "FLiBe coordination does not admit self-neighbor edges."
                )

            counts[
                species[edge.source]
            ] += 1

        atoms.append(
            FLiBeAtomCoordination(
                atom_index=receiver,
                species=species[receiver],
                lithium_neighbors=counts[
                    FLiBeSpecies.LITHIUM
                ],
                beryllium_neighbors=counts[
                    FLiBeSpecies.BERYLLIUM
                ],
                fluorine_neighbors=counts[
                    FLiBeSpecies.FLUORINE
                ],
            )
        )

    return FLiBeCoordinationState(
        atoms=tuple(
            atoms
        )
    )
