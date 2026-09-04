"""Invariant tests for the TR-EIF FLiBe graph-relative coordination contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import (
    FLiBeAtomCoordination,
    FLiBeCoordinationState,
    build_flibe_coordination_state,
)
from tr_eif.flibe.species import FLiBeSpecies
from tr_eif.graph import InteractionEdge, InteractionGraph


def _configuration(
    species: tuple[str, ...] = ("Li", "Be", "F", "F"),
) -> FLiBeConfiguration:
    """Build one finite FLiBe-domain configuration."""

    positions = tuple(
        (float(index), 0.0, 0.0)
        for index in range(len(species))
    )

    return FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=species,
            positions=positions,
        )
    )


def _reference_graph() -> InteractionGraph:
    """Build one deterministic directed interaction graph."""

    return InteractionGraph(
        node_count=4,
        edges=(
            InteractionEdge(source=0, receiver=1),
            InteractionEdge(source=2, receiver=1),
            InteractionEdge(source=3, receiver=1),
            InteractionEdge(source=1, receiver=0),
            InteractionEdge(source=2, receiver=0),
            InteractionEdge(source=0, receiver=2),
            InteractionEdge(source=1, receiver=2),
            InteractionEdge(source=0, receiver=3),
        ),
    )


def _atom(
    atom_index: int = 0,
    species: FLiBeSpecies = FLiBeSpecies.LITHIUM,
    lithium_neighbors: int = 1,
    beryllium_neighbors: int = 2,
    fluorine_neighbors: int = 3,
) -> FLiBeAtomCoordination:
    """Build one deterministic coordination record."""

    return FLiBeAtomCoordination(
        atom_index=atom_index,
        species=species,
        lithium_neighbors=lithium_neighbors,
        beryllium_neighbors=beryllium_neighbors,
        fluorine_neighbors=fluorine_neighbors,
    )


def test_atom_coordination_preserves_fields() -> None:
    """A valid atom coordination record must preserve all supplied fields."""

    atom = _atom()

    assert atom.atom_index == 0
    assert atom.species is FLiBeSpecies.LITHIUM
    assert atom.lithium_neighbors == 1
    assert atom.beryllium_neighbors == 2
    assert atom.fluorine_neighbors == 3


@pytest.mark.parametrize(
    "invalid_index",
    (True, False, 1.0, "0", None, (), []),
)
def test_atom_index_requires_integer(
    invalid_index,
) -> None:
    """Atom index must be a non-Boolean integer."""

    with pytest.raises(
        TypeError,
        match="atom_index must be an integer",
    ):
        _atom(atom_index=invalid_index)


@pytest.mark.parametrize(
    "invalid_index",
    (-1, -2, -100),
)
def test_atom_index_rejects_negative_values(
    invalid_index: int,
) -> None:
    """Atom index must be nonnegative."""

    with pytest.raises(
        ValueError,
        match="atom_index must be nonnegative",
    ):
        _atom(atom_index=invalid_index)


@pytest.mark.parametrize(
    "invalid_species",
    ("Li", "Be", "F", None, True, 0, ()),
)
def test_atom_coordination_requires_flibe_species(
    invalid_species,
) -> None:
    """Atom species must use the canonical FLiBeSpecies enum."""

    with pytest.raises(
        TypeError,
        match="species must be an FLiBeSpecies",
    ):
        _atom(species=invalid_species)


@pytest.mark.parametrize(
    "field_name",
    (
        "lithium_neighbors",
        "beryllium_neighbors",
        "fluorine_neighbors",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (True, False, 1.0, "1", None, (), []),
)
def test_neighbor_counts_require_integers(
    field_name: str,
    invalid_value,
) -> None:
    """Every species-resolved coordination count must be an integer."""

    values = {
        "atom_index": 0,
        "species": FLiBeSpecies.LITHIUM,
        "lithium_neighbors": 1,
        "beryllium_neighbors": 2,
        "fluorine_neighbors": 3,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be an integer",
    ):
        FLiBeAtomCoordination(**values)


@pytest.mark.parametrize(
    "field_name",
    (
        "lithium_neighbors",
        "beryllium_neighbors",
        "fluorine_neighbors",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (-1, -2, -100),
)
def test_neighbor_counts_reject_negative_values(
    field_name: str,
    invalid_value: int,
) -> None:
    """Every species-resolved coordination count must be nonnegative."""

    values = {
        "atom_index": 0,
        "species": FLiBeSpecies.LITHIUM,
        "lithium_neighbors": 1,
        "beryllium_neighbors": 2,
        "fluorine_neighbors": 3,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be nonnegative",
    ):
        FLiBeAtomCoordination(**values)


def test_zero_neighbor_counts_are_allowed() -> None:
    """An atom may have zero incoming graph-neighbor records."""

    atom = _atom(
        lithium_neighbors=0,
        beryllium_neighbors=0,
        fluorine_neighbors=0,
    )

    assert atom.total_neighbors == 0


def test_total_neighbors_equals_species_sum() -> None:
    """Total coordination must equal the sum of all species-resolved counts."""

    atom = _atom(
        lithium_neighbors=4,
        beryllium_neighbors=5,
        fluorine_neighbors=6,
    )

    assert atom.total_neighbors == 15


def test_species_coordination_uses_canonical_order() -> None:
    """Species-resolved output must use canonical Li, Be, F ordering."""

    atom = _atom(
        lithium_neighbors=4,
        beryllium_neighbors=5,
        fluorine_neighbors=6,
    )

    assert atom.species_coordination == (
        (FLiBeSpecies.LITHIUM, 4),
        (FLiBeSpecies.BERYLLIUM, 5),
        (FLiBeSpecies.FLUORINE, 6),
    )


def test_atom_coordination_is_frozen() -> None:
    """Atom coordination records must be immutable."""

    atom = _atom()

    with pytest.raises(FrozenInstanceError):
        atom.lithium_neighbors = 9


def test_coordination_state_preserves_atom_tuple() -> None:
    """Coordination state must preserve a valid contiguous atom tuple."""

    atoms = (
        _atom(atom_index=0),
        _atom(atom_index=1, species=FLiBeSpecies.BERYLLIUM),
    )

    state = FLiBeCoordinationState(atoms=atoms)

    assert state.atoms == atoms
    assert state.atom_count == 2


@pytest.mark.parametrize(
    "invalid_atoms",
    (None, [], {}, "atoms", 1),
)
def test_coordination_state_requires_tuple(
    invalid_atoms,
) -> None:
    """Coordination-state atom records must be supplied as a tuple."""

    with pytest.raises(
        TypeError,
        match="atoms must be a tuple",
    ):
        FLiBeCoordinationState(atoms=invalid_atoms)


def test_coordination_state_rejects_empty_tuple() -> None:
    """Coordination state must contain at least one atom record."""

    with pytest.raises(
        ValueError,
        match="atoms must not be empty",
    ):
        FLiBeCoordinationState(atoms=())


@pytest.mark.parametrize(
    "invalid_atom",
    (None, True, 1, "atom", ()),
)
def test_coordination_state_requires_atom_coordination_records(
    invalid_atom,
) -> None:
    """Every coordination-state element must be an FLiBeAtomCoordination."""

    with pytest.raises(
        TypeError,
        match=r"atoms\[0\] must be an FLiBeAtomCoordination",
    ):
        FLiBeCoordinationState(atoms=(invalid_atom,))


def test_coordination_state_requires_zero_based_contiguous_order() -> None:
    """Stored atom indices must follow zero-based contiguous ordering."""

    atoms = (
        _atom(atom_index=0),
        _atom(atom_index=2, species=FLiBeSpecies.BERYLLIUM),
    )

    with pytest.raises(
        ValueError,
        match="atom coordination records must use contiguous configuration ordering",
    ):
        FLiBeCoordinationState(atoms=atoms)


def test_coordination_state_rejects_nonzero_start_index() -> None:
    """A standalone coordination state must start at atom index zero."""

    with pytest.raises(
        ValueError,
        match="atom coordination records must use contiguous configuration ordering",
    ):
        FLiBeCoordinationState(
            atoms=(
                _atom(atom_index=1),
            )
        )


def test_total_neighbor_records_sums_all_atom_records() -> None:
    """State-level neighbor total must sum all incoming coordination records."""

    state = FLiBeCoordinationState(
        atoms=(
            _atom(
                atom_index=0,
                lithium_neighbors=1,
                beryllium_neighbors=0,
                fluorine_neighbors=2,
            ),
            _atom(
                atom_index=1,
                species=FLiBeSpecies.BERYLLIUM,
                lithium_neighbors=3,
                beryllium_neighbors=4,
                fluorine_neighbors=0,
            ),
        )
    )

    assert state.total_neighbor_records == 10


def test_coordination_state_is_frozen() -> None:
    """Coordination-state records must be immutable."""

    state = FLiBeCoordinationState(
        atoms=(
            _atom(atom_index=0),
        )
    )

    with pytest.raises(FrozenInstanceError):
        state.atoms = ()


@pytest.mark.parametrize(
    "invalid_configuration",
    (None, True, False, 1, 1.0, (), {}),
)
def test_builder_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Coordination construction must require an FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match="configuration must be an FLiBeConfiguration",
    ):
        build_flibe_coordination_state(
            invalid_configuration,
            _reference_graph(),
        )


@pytest.mark.parametrize(
    "invalid_graph",
    (None, True, False, 1, 1.0, (), {}),
)
def test_builder_requires_interaction_graph(
    invalid_graph,
) -> None:
    """Coordination construction must require an InteractionGraph."""

    with pytest.raises(
        TypeError,
        match="graph must be an InteractionGraph",
    ):
        build_flibe_coordination_state(
            _configuration(),
            invalid_graph,
        )


def test_builder_requires_matching_graph_node_count() -> None:
    """Graph and FLiBe configuration must represent the same atom count."""

    graph = InteractionGraph(
        node_count=3,
        edges=(),
    )

    with pytest.raises(
        ValueError,
        match="graph node_count must match FLiBe configuration atom_count",
    ):
        build_flibe_coordination_state(
            _configuration(),
            graph,
        )


def test_reference_graph_produces_expected_species_counts() -> None:
    """Incoming directed edges must be counted by source species."""

    state = build_flibe_coordination_state(
        _configuration(),
        _reference_graph(),
    )

    assert state.atoms == (
        FLiBeAtomCoordination(
            atom_index=0,
            species=FLiBeSpecies.LITHIUM,
            lithium_neighbors=0,
            beryllium_neighbors=1,
            fluorine_neighbors=1,
        ),
        FLiBeAtomCoordination(
            atom_index=1,
            species=FLiBeSpecies.BERYLLIUM,
            lithium_neighbors=1,
            beryllium_neighbors=0,
            fluorine_neighbors=2,
        ),
        FLiBeAtomCoordination(
            atom_index=2,
            species=FLiBeSpecies.FLUORINE,
            lithium_neighbors=1,
            beryllium_neighbors=1,
            fluorine_neighbors=0,
        ),
        FLiBeAtomCoordination(
            atom_index=3,
            species=FLiBeSpecies.FLUORINE,
            lithium_neighbors=1,
            beryllium_neighbors=0,
            fluorine_neighbors=0,
        ),
    )


def test_builder_preserves_receiver_species_identity() -> None:
    """Each output atom record must preserve configuration species identity."""

    configuration = _configuration()
    state = build_flibe_coordination_state(
        configuration,
        _reference_graph(),
    )

    assert tuple(atom.species for atom in state.atoms) == configuration.species


def test_builder_preserves_configuration_atom_order() -> None:
    """Output records must follow exact configuration atom ordering."""

    state = build_flibe_coordination_state(
        _configuration(),
        _reference_graph(),
    )

    assert tuple(atom.atom_index for atom in state.atoms) == (0, 1, 2, 3)


def test_builder_atom_count_matches_configuration() -> None:
    """Built coordination state must contain one record per configuration atom."""

    configuration = _configuration()
    state = build_flibe_coordination_state(
        configuration,
        _reference_graph(),
    )

    assert state.atom_count == configuration.atom_count


def test_total_neighbor_records_matches_graph_edge_count() -> None:
    """Every non-self directed graph edge must contribute one neighbor record."""

    graph = _reference_graph()
    state = build_flibe_coordination_state(
        _configuration(),
        graph,
    )

    assert state.total_neighbor_records == graph.edge_count


def test_empty_edge_graph_produces_zero_coordination() -> None:
    """A valid graph with no edges must produce zero coordination for every atom."""

    configuration = _configuration()
    graph = InteractionGraph(
        node_count=configuration.atom_count,
        edges=(),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    assert all(atom.total_neighbors == 0 for atom in state.atoms)
    assert state.total_neighbor_records == 0


def test_single_directed_edge_is_not_implicitly_symmetrized() -> None:
    """Directed graph coordination must not invent the reverse interaction edge."""

    configuration = _configuration(("Li", "F"))
    graph = InteractionGraph(
        node_count=2,
        edges=(
            InteractionEdge(source=0, receiver=1),
        ),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    assert state.atoms[0].total_neighbors == 0
    assert state.atoms[1].lithium_neighbors == 1
    assert state.atoms[1].total_neighbors == 1


def test_neighbor_species_is_taken_from_edge_source() -> None:
    """Species-resolved coordination must classify the incoming edge source."""

    configuration = _configuration(("Be", "F"))
    graph = InteractionGraph(
        node_count=2,
        edges=(
            InteractionEdge(source=0, receiver=1),
        ),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    receiver = state.atoms[1]

    assert receiver.lithium_neighbors == 0
    assert receiver.beryllium_neighbors == 1
    assert receiver.fluorine_neighbors == 0


def test_edge_order_does_not_change_coordination_counts() -> None:
    """Coordination counts must depend on edge records, not their tuple order."""

    configuration = _configuration()
    first_graph = _reference_graph()
    second_graph = InteractionGraph(
        node_count=first_graph.node_count,
        edges=tuple(reversed(first_graph.edges)),
    )

    first = build_flibe_coordination_state(
        configuration,
        first_graph,
    )
    second = build_flibe_coordination_state(
        configuration,
        second_graph,
    )

    assert first == second


def test_periodic_image_edges_are_counted_as_distinct_graph_records() -> None:
    """Distinct periodic image records must contribute separately to coordination."""

    configuration = _configuration(("Li", "F"))
    graph = InteractionGraph(
        node_count=2,
        edges=(
            InteractionEdge(
                source=0,
                receiver=1,
                image=(0, 0, 0),
            ),
            InteractionEdge(
                source=0,
                receiver=1,
                image=(1, 0, 0),
            ),
        ),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    assert state.atoms[1].lithium_neighbors == 2
    assert state.atoms[1].total_neighbors == 2
    assert state.total_neighbor_records == graph.edge_count


def test_builder_rejects_self_neighbor_edge() -> None:
    """FLiBe coordination must reject graph records whose source equals receiver."""

    configuration = _configuration(("Li", "F"))
    graph = InteractionGraph(
        node_count=2,
        edges=(
            InteractionEdge(source=0, receiver=0),
        ),
    )

    with pytest.raises(
        ValueError,
        match="FLiBe coordination does not admit self-neighbor edges",
    ):
        build_flibe_coordination_state(
            configuration,
            graph,
        )


def test_builder_rejects_self_edge_even_with_valid_other_edges() -> None:
    """Presence of other valid edges must not mask a self-neighbor record."""

    configuration = _configuration(("Li", "Be", "F"))
    graph = InteractionGraph(
        node_count=3,
        edges=(
            InteractionEdge(source=0, receiver=1),
            InteractionEdge(source=2, receiver=2),
            InteractionEdge(source=1, receiver=0),
        ),
    )

    with pytest.raises(
        ValueError,
        match="FLiBe coordination does not admit self-neighbor edges",
    ):
        build_flibe_coordination_state(
            configuration,
            graph,
        )


def test_coordination_is_graph_relative_not_distance_derived() -> None:
    """Supplied graph records, not Cartesian separation, define this state."""

    configuration = FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=("Li", "F"),
            positions=(
                (0.0, 0.0, 0.0),
                (1.0e9, 0.0, 0.0),
            ),
        )
    )
    graph = InteractionGraph(
        node_count=2,
        edges=(
            InteractionEdge(source=0, receiver=1),
        ),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    assert state.atoms[1].lithium_neighbors == 1


def test_different_graphs_define_different_coordination_states() -> None:
    """The same FLiBe configuration may have distinct graph-relative states."""

    configuration = _configuration(("Li", "Be", "F"))

    first_graph = InteractionGraph(
        node_count=3,
        edges=(
            InteractionEdge(source=0, receiver=2),
        ),
    )
    second_graph = InteractionGraph(
        node_count=3,
        edges=(
            InteractionEdge(source=1, receiver=2),
        ),
    )

    first = build_flibe_coordination_state(
        configuration,
        first_graph,
    )
    second = build_flibe_coordination_state(
        configuration,
        second_graph,
    )

    assert first != second
    assert first.atoms[2].lithium_neighbors == 1
    assert first.atoms[2].beryllium_neighbors == 0
    assert second.atoms[2].lithium_neighbors == 0
    assert second.atoms[2].beryllium_neighbors == 1


def test_coordination_does_not_require_flibe_formula_stoichiometry() -> None:
    """Graph coordination must remain separate from formula-unit stoichiometry."""

    configuration = _configuration(("Li", "Li", "Li"))
    graph = InteractionGraph(
        node_count=3,
        edges=(
            InteractionEdge(source=0, receiver=1),
            InteractionEdge(source=1, receiver=2),
        ),
    )

    state = build_flibe_coordination_state(
        configuration,
        graph,
    )

    assert state.total_neighbor_records == 2
    assert state.atoms[1].lithium_neighbors == 1
    assert state.atoms[2].lithium_neighbors == 1


def test_numeric_neighbor_count_has_no_ternary_state_semantics() -> None:
    """A coordination count equal to one must remain an integer graph count."""

    state = build_flibe_coordination_state(
        _configuration(("Li", "F")),
        InteractionGraph(
            node_count=2,
            edges=(
                InteractionEdge(source=0, receiver=1),
            ),
        ),
    )

    count = state.atoms[1].lithium_neighbors

    assert count == 1
    assert type(count) is int
