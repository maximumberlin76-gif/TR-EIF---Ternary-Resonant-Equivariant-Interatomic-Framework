"""Deterministic Verlet-style neighbor-list primitives for TR-EIF MD."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

from tr_eif.configuration import AtomicConfiguration, Vector3
from tr_eif.geometry import displacement, minimum_image, squared_distance
from tr_eif.graph import (
    ImageIndex,
    InteractionEdge,
    InteractionGraph,
    build_cutoff_graph,
)

NeighborPair: TypeAlias = tuple[int, int]


def _validate_real(
    value: float,
    *,
    field_name: str,
    positive: bool,
) -> float:
    """Validate and normalize one finite real-valued neighbor-list parameter."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a real number.")

    if not isfinite(value):
        raise ValueError(f"{field_name} must be finite.")

    normalized = float(value)

    if positive:
        if normalized <= 0.0:
            raise ValueError(f"{field_name} must be greater than zero.")
    elif normalized < 0.0:
        raise ValueError(f"{field_name} must be nonnegative.")

    return normalized


def _validate_configuration(configuration: AtomicConfiguration) -> None:
    """Validate one atomic-configuration argument."""

    if not isinstance(configuration, AtomicConfiguration):
        raise TypeError(
            "configuration must be an AtomicConfiguration instance."
        )


def _current_displacement(
    configuration: AtomicConfiguration,
    source: int,
    receiver: int,
) -> tuple[Vector3, ImageIndex]:
    """Return the current directed displacement and periodic image index."""

    source_position = configuration.positions[source]
    receiver_position = configuration.positions[receiver]

    if configuration.is_periodic:
        if configuration.cell is None:
            raise ValueError(
                "Periodic configuration requires a simulation cell."
            )

        return minimum_image(
            source_position,
            receiver_position,
            configuration.cell,
            configuration.periodic,
        )

    return displacement(source_position, receiver_position), (0, 0, 0)


@dataclass(frozen=True, slots=True)
class NeighborList:
    """Immutable Verlet-style neighbor-list snapshot for one configuration."""

    interaction_cutoff: float
    skin: float
    reference_configuration: AtomicConfiguration
    candidate_pairs: tuple[NeighborPair, ...]

    def __post_init__(self) -> None:
        interaction_cutoff = _validate_real(
            self.interaction_cutoff,
            field_name="interaction_cutoff",
            positive=True,
        )
        skin = _validate_real(
            self.skin,
            field_name="skin",
            positive=False,
        )
        _validate_configuration(self.reference_configuration)

        search_cutoff = interaction_cutoff + skin

        if not isfinite(search_cutoff):
            raise ValueError(
                "interaction_cutoff + skin must be finite."
            )

        if not isinstance(self.candidate_pairs, tuple):
            raise TypeError(
                "candidate_pairs must be a tuple."
            )

        validated_pairs: list[NeighborPair] = []
        atom_count = self.reference_configuration.atom_count

        for index, pair in enumerate(self.candidate_pairs):
            if not isinstance(pair, tuple):
                raise TypeError(
                    f"candidate_pairs[{index}] must be a tuple."
                )

            if len(pair) != 2:
                raise ValueError(
                    f"candidate_pairs[{index}] "
                    "must contain exactly two indices."
                )

            source, receiver = pair

            if not isinstance(source, int) or isinstance(source, bool):
                raise TypeError(
                    f"candidate_pairs[{index}][0] "
                    "must be an integer."
                )

            if not isinstance(receiver, int) or isinstance(receiver, bool):
                raise TypeError(
                    f"candidate_pairs[{index}][1] "
                    "must be an integer."
                )

            if source < 0 or receiver < 0:
                raise ValueError(
                    f"candidate_pairs[{index}] "
                    "indices must be nonnegative."
                )

            if source >= receiver:
                raise ValueError(
                    f"candidate_pairs[{index}] "
                    "must satisfy source < receiver."
                )

            if receiver >= atom_count:
                raise ValueError(
                    f"candidate_pairs[{index}] "
                    "is outside the atom index range."
                )

            validated_pairs.append(
                (source, receiver)
            )

        normalized_pairs = tuple(validated_pairs)

        if len(set(normalized_pairs)) != len(normalized_pairs):
            raise ValueError(
                "candidate_pairs must not contain duplicates."
            )

        if normalized_pairs != tuple(sorted(normalized_pairs)):
            raise ValueError(
                "candidate_pairs must be in canonical sorted order."
            )

        object.__setattr__(
            self,
            "interaction_cutoff",
            interaction_cutoff,
        )
        object.__setattr__(
            self,
            "skin",
            skin,
        )

    @property
    def search_cutoff(self) -> float:
        """Return the candidate-search cutoff used for this neighbor list."""

        return self.interaction_cutoff + self.skin

    @property
    def candidate_pair_count(self) -> int:
        """Return the number of unordered candidate atom pairs."""

        return len(self.candidate_pairs)


def build_neighbor_list(
    configuration: AtomicConfiguration,
    interaction_cutoff: float,
    skin: float,
) -> NeighborList:
    """Build a deterministic neighbor-list snapshot from a search cutoff."""

    _validate_configuration(configuration)

    normalized_cutoff = _validate_real(
        interaction_cutoff,
        field_name="interaction_cutoff",
        positive=True,
    )
    normalized_skin = _validate_real(
        skin,
        field_name="skin",
        positive=False,
    )

    search_cutoff = normalized_cutoff + normalized_skin

    if not isfinite(search_cutoff):
        raise ValueError(
            "interaction_cutoff + skin must be finite."
        )

    search_graph = build_cutoff_graph(
        configuration,
        search_cutoff,
    )

    candidate_pairs = tuple(
        (edge.source, edge.receiver)
        for edge in search_graph.edges
        if edge.source < edge.receiver
    )

    return NeighborList(
        interaction_cutoff=normalized_cutoff,
        skin=normalized_skin,
        reference_configuration=configuration,
        candidate_pairs=candidate_pairs,
    )


def neighbor_list_requires_rebuild(
    neighbor_list: NeighborList,
    configuration: AtomicConfiguration,
) -> bool:
    """Return whether the current configuration invalidates the snapshot."""

    if not isinstance(neighbor_list, NeighborList):
        raise TypeError(
            "neighbor_list must be a NeighborList instance."
        )

    _validate_configuration(configuration)

    reference = neighbor_list.reference_configuration

    if configuration.atom_count != reference.atom_count:
        return True

    if configuration.species != reference.species:
        return True

    if configuration.periodic != reference.periodic:
        return True

    if configuration.cell != reference.cell:
        return True

    threshold_squared = (
        0.5 * neighbor_list.skin
    ) ** 2

    for reference_position, current_position in zip(
        reference.positions,
        configuration.positions,
        strict=True,
    ):
        if reference.is_periodic:
            if reference.cell is None:
                raise ValueError(
                    "Periodic reference configuration "
                    "requires a simulation cell."
                )

            delta, _ = minimum_image(
                reference_position,
                current_position,
                reference.cell,
                reference.periodic,
            )
        else:
            delta = displacement(
                reference_position,
                current_position,
            )

        displacement_squared = squared_distance(
            (0.0, 0.0, 0.0),
            delta,
        )

        if displacement_squared > threshold_squared:
            return True

    return False


def interaction_graph_from_neighbor_list(
    neighbor_list: NeighborList,
    configuration: AtomicConfiguration,
) -> InteractionGraph:
    """Evaluate the current cutoff graph from a valid neighbor-list snapshot."""

    if not isinstance(neighbor_list, NeighborList):
        raise TypeError(
            "neighbor_list must be a NeighborList instance."
        )

    _validate_configuration(configuration)

    if neighbor_list_requires_rebuild(
        neighbor_list,
        configuration,
    ):
        raise ValueError(
            "Neighbor list must be rebuilt before "
            "evaluating this configuration."
        )

    cutoff_squared = (
        neighbor_list.interaction_cutoff ** 2
    )
    edges: list[InteractionEdge] = []

    for source, receiver in neighbor_list.candidate_pairs:
        forward_delta, forward_image = _current_displacement(
            configuration,
            source,
            receiver,
        )

        if squared_distance(
            (0.0, 0.0, 0.0),
            forward_delta,
        ) > cutoff_squared:
            continue

        _, reverse_image = _current_displacement(
            configuration,
            receiver,
            source,
        )

        edges.append(
            InteractionEdge(
                source=source,
                receiver=receiver,
                image=forward_image,
            )
        )
        edges.append(
            InteractionEdge(
                source=receiver,
                receiver=source,
                image=reverse_image,
            )
        )

    edges.sort(
        key=lambda edge: (
            edge.source,
            edge.receiver,
            edge.image,
        )
    )

    return InteractionGraph(
        node_count=configuration.atom_count,
        edges=tuple(edges),
    )
