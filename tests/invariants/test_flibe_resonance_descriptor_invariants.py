"""Invariant tests for the TR-EIF FLiBe resonance descriptor contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.coordination import (
    FLiBeAtomCoordination,
    FLiBeCoordinationState,
)
from tr_eif.flibe.resonance_descriptor import (
    FLiBeResonanceDescriptor,
    build_flibe_resonance_descriptor,
)
from tr_eif.flibe.species import FLiBeSpecies
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.resonance import ResonanceState, resonance_descriptor


def _configuration(
    *,
    offset: float = 0.0,
) -> FLiBeConfiguration:
    """Construct one exact 2 LiF : 1 BeF2 test-fixture configuration."""

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
            positions=tuple(
                (
                    float(index) + offset,
                    0.0,
                    0.0,
                )
                for index in range(7)
            ),
        )
    )


def _coordination(
    *,
    offset: int = 0,
) -> FLiBeCoordinationState:
    """Construct graph-relative coordination with canonical species ordering."""

    species = (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
    )

    return FLiBeCoordinationState(
        atoms=tuple(
            FLiBeAtomCoordination(
                atom_index=index,
                species=atom_species,
                lithium_neighbors=offset + index,
                beryllium_neighbors=offset + (index % 2),
                fluorine_neighbors=offset + (index % 3),
            )
            for index, atom_species in enumerate(species)
        )
    )


def _thermodynamic_state(
    *,
    temperature: float = 1000.0,
    pressure: float = 0.0,
) -> FLiBeThermodynamicState:
    """Construct one explicit thermodynamic test fixture."""

    return FLiBeThermodynamicState(
        temperature=temperature,
        pressure=pressure,
    )


def _resonance_state() -> ResonanceState:
    """Construct one deterministic seven-oscillator continuous state."""

    return ResonanceState(
        phases=(
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ),
        frequencies=(
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
        ),
    )


def _descriptor(
    *,
    configuration: FLiBeConfiguration | None = None,
    coordination: FLiBeCoordinationState | None = None,
    thermodynamic_state: FLiBeThermodynamicState | None = None,
    resonance_state: ResonanceState | None = None,
    provenance: ParameterProvenance = ParameterProvenance.TEST_FIXTURE,
    source: str | None = None,
) -> FLiBeResonanceDescriptor:
    """Construct one deterministic FLiBe resonance descriptor record."""

    return FLiBeResonanceDescriptor(
        configuration=(
            _configuration()
            if configuration is None
            else configuration
        ),
        coordination=(
            _coordination()
            if coordination is None
            else coordination
        ),
        thermodynamic_state=(
            _thermodynamic_state()
            if thermodynamic_state is None
            else thermodynamic_state
        ),
        resonance_state=(
            _resonance_state()
            if resonance_state is None
            else resonance_state
        ),
        provenance=provenance,
        source=source,
    )


def test_descriptor_matches_base_resonance_descriptor() -> None:
    """FLiBe context must not replace the base continuous descriptor."""

    state = _resonance_state()
    record = _descriptor(
        resonance_state=state,
    )

    assert record.descriptor == resonance_descriptor(state)


def test_known_continuous_coordinate_is_preserved() -> None:
    """The FLiBe wrapper must preserve the base resonance coordinate exactly."""

    record = _descriptor()

    assert record.phase_order == pytest.approx(1.0)
    assert record.frequency_spread == pytest.approx(2.0)
    assert record.coordinate == pytest.approx((1.0, 2.0))


def test_exact_flibe_composition_is_exposed_without_descriptor_mixing() -> None:
    """Composition metadata must remain explicit and outside the coordinate."""

    record = _descriptor()

    assert record.composition.lif_fraction == pytest.approx(
        2.0 / 3.0
    )
    assert record.composition.bef2_fraction == pytest.approx(
        1.0 / 3.0
    )
    assert len(record.coordinate) == 2


def test_thermodynamic_state_does_not_modify_resonance_coordinate() -> None:
    """Temperature and pressure must not become hidden oscillator variables."""

    first = _descriptor(
        thermodynamic_state=_thermodynamic_state(
            temperature=900.0,
            pressure=0.0,
        )
    )
    second = _descriptor(
        thermodynamic_state=_thermodynamic_state(
            temperature=1500.0,
            pressure=5.0,
        )
    )

    assert first.coordinate == second.coordinate


def test_coordination_values_do_not_modify_resonance_coordinate() -> None:
    """Graph-relative coordination must remain context, not hidden phase input."""

    first = _descriptor(
        coordination=_coordination(offset=0)
    )
    second = _descriptor(
        coordination=_coordination(offset=20)
    )

    assert first.coordinate == second.coordinate


def test_atomic_positions_do_not_modify_resonance_coordinate() -> None:
    """Geometry changes alone must not silently rewrite resonance state."""

    first = _descriptor(
        configuration=_configuration(offset=0.0)
    )
    second = _descriptor(
        configuration=_configuration(offset=100.0)
    )

    assert first.coordinate == second.coordinate


def test_builder_matches_direct_record_construction() -> None:
    """The public builder must preserve direct record semantics."""

    configuration = _configuration()
    coordination = _coordination()
    thermodynamic_state = _thermodynamic_state()
    resonance_state = _resonance_state()

    direct = FLiBeResonanceDescriptor(
        configuration=configuration,
        coordination=coordination,
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    built = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=coordination,
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert built == direct


def test_context_objects_are_retained_explicitly() -> None:
    """The record must retain the exact supplied FLiBe and resonance objects."""

    configuration = _configuration()
    coordination = _coordination()
    thermodynamic_state = _thermodynamic_state()
    resonance_state = _resonance_state()

    record = _descriptor(
        configuration=configuration,
        coordination=coordination,
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
    )

    assert record.configuration is configuration
    assert record.coordination is coordination
    assert record.thermodynamic_state is thermodynamic_state
    assert record.resonance_state is resonance_state


def test_provenance_and_source_are_retained() -> None:
    """Descriptor provenance must remain explicit metadata."""

    record = _descriptor(
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert record.provenance is ParameterProvenance.DERIVED
    assert record.source == "derived-record"


@pytest.mark.parametrize(
    "provenance",
    (
        ParameterProvenance.DERIVED,
        ParameterProvenance.CALIBRATED,
        ParameterProvenance.AUTHOR_DEFINED,
        ParameterProvenance.BENCHMARK,
        ParameterProvenance.TEST_FIXTURE,
        ParameterProvenance.REQUIRES_SOURCE,
        ParameterProvenance.REQUIRES_TEST,
    ),
)
def test_nonprimary_provenance_allows_missing_source(
    provenance: ParameterProvenance,
) -> None:
    """Non-primary descriptor records may omit direct source metadata."""

    record = _descriptor(
        provenance=provenance,
    )

    assert record.source is None


def test_primary_source_provenance_requires_source() -> None:
    """PRIMARY_SOURCE descriptors must retain an explicit source anchor."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        _descriptor(
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_source_provenance_accepts_source() -> None:
    """PRIMARY_SOURCE descriptors are valid with explicit source metadata."""

    record = _descriptor(
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="FLIBE-PRIMARY-TEST",
    )

    assert record.source == "FLIBE-PRIMARY-TEST"


@pytest.mark.parametrize(
    ("source", "error", "message"),
    (
        (
            "",
            ValueError,
            "source must not be empty",
        ),
        (
            " source",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            "source ",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            True,
            TypeError,
            "source must be a string or None",
        ),
        (
            1,
            TypeError,
            "source must be a string or None",
        ),
        (
            (),
            TypeError,
            "source must be a string or None",
        ),
    ),
)
def test_invalid_source_metadata_is_rejected(
    source: object,
    error: type[Exception],
    message: str,
) -> None:
    """Descriptor source metadata must satisfy the provenance contract."""

    with pytest.raises(
        error,
        match=message,
    ):
        _descriptor(
            source=source,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("field_name", "value", "message"),
    (
        (
            "configuration",
            None,
            "configuration must be an FLiBeConfiguration",
        ),
        (
            "coordination",
            None,
            "coordination must be an FLiBeCoordinationState",
        ),
        (
            "thermodynamic_state",
            None,
            "thermodynamic_state must be an FLiBeThermodynamicState",
        ),
        (
            "resonance_state",
            None,
            "resonance_state must be a ResonanceState",
        ),
        (
            "provenance",
            "TEST_FIXTURE",
            "provenance must be a ParameterProvenance",
        ),
    ),
)
def test_descriptor_requires_typed_context_fields(
    field_name: str,
    value: object,
    message: str,
) -> None:
    """Every descriptor boundary must retain its declared domain type."""

    arguments: dict[str, object] = {
        "configuration": _configuration(),
        "coordination": _coordination(),
        "thermodynamic_state": _thermodynamic_state(),
        "resonance_state": _resonance_state(),
        "provenance": ParameterProvenance.TEST_FIXTURE,
    }

    arguments[field_name] = value

    with pytest.raises(
        TypeError,
        match=message,
    ):
        FLiBeResonanceDescriptor(
            **arguments
        )  # type: ignore[arg-type]


def test_coordination_atom_count_must_match_configuration() -> None:
    """Coordination state cardinality must match the FLiBe configuration."""

    truncated = FLiBeCoordinationState(
        atoms=_coordination().atoms[:-1]
    )

    with pytest.raises(
        ValueError,
        match=(
            "coordination atom count must match "
            "configuration atom count"
        ),
    ):
        _descriptor(
            coordination=truncated,
        )


def test_resonance_oscillator_count_must_match_configuration() -> None:
    """The executable FLiBe descriptor requires one oscillator per atom."""

    resonance_state = ResonanceState(
        phases=(
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ),
        frequencies=(
            0.0,
            1.0,
            2.0,
            3.0,
            4.0,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "resonance oscillator count must match "
            "configuration atom count"
        ),
    ):
        _descriptor(
            resonance_state=resonance_state,
        )


def test_coordination_species_order_must_match_configuration() -> None:
    """Graph coordination records must preserve atomic species ordering."""

    atoms = list(
        _coordination().atoms
    )

    atoms[0] = FLiBeAtomCoordination(
        atom_index=0,
        species=FLiBeSpecies.FLUORINE,
        lithium_neighbors=0,
        beryllium_neighbors=0,
        fluorine_neighbors=0,
    )

    mismatched = FLiBeCoordinationState(
        atoms=tuple(atoms)
    )

    with pytest.raises(
        ValueError,
        match=(
            "coordination species ordering must match "
            "configuration species"
        ),
    ):
        _descriptor(
            coordination=mismatched,
        )


def test_invalid_flibe_stoichiometry_is_rejected() -> None:
    """Descriptor construction must preserve the FLiBe composition invariant."""

    configuration = FLiBeConfiguration(
        configuration=AtomicConfiguration(
            species=(
                "Li",
                "Li",
                "Be",
                "F",
                "F",
                "F",
            ),
            positions=tuple(
                (
                    float(index),
                    0.0,
                    0.0,
                )
                for index in range(6)
            ),
        )
    )

    coordination = FLiBeCoordinationState(
        atoms=(
            FLiBeAtomCoordination(
                atom_index=0,
                species=FLiBeSpecies.LITHIUM,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
            FLiBeAtomCoordination(
                atom_index=1,
                species=FLiBeSpecies.LITHIUM,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
            FLiBeAtomCoordination(
                atom_index=2,
                species=FLiBeSpecies.BERYLLIUM,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
            FLiBeAtomCoordination(
                atom_index=3,
                species=FLiBeSpecies.FLUORINE,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
            FLiBeAtomCoordination(
                atom_index=4,
                species=FLiBeSpecies.FLUORINE,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
            FLiBeAtomCoordination(
                atom_index=5,
                species=FLiBeSpecies.FLUORINE,
                lithium_neighbors=0,
                beryllium_neighbors=0,
                fluorine_neighbors=0,
            ),
        )
    )

    resonance_state = ResonanceState(
        phases=(
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ),
        frequencies=(
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "does not satisfy LiF-BeF2 "
            "fluorine stoichiometry"
        ),
    ):
        _descriptor(
            configuration=configuration,
            coordination=coordination,
            resonance_state=resonance_state,
        )


def test_descriptor_record_is_frozen() -> None:
    """Validated FLiBe resonance descriptor records must be immutable."""

    record = _descriptor()

    with pytest.raises(FrozenInstanceError):
        record.source = "replacement"  # type: ignore[misc]


def test_descriptor_is_deterministic() -> None:
    """Identical explicit inputs must reproduce the same FLiBe descriptor."""

    first = _descriptor()
    second = _descriptor()

    assert first == second
    assert first.coordinate == second.coordinate
