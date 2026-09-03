"""Invariant tests for the TR-EIF FLiBe formal-charge contract."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.charge import (
    FLIBE_FORMAL_CHARGES,
    FormalChargeState,
    build_formal_charge_state,
    configuration_formal_charges,
    formal_charge,
    formal_charge_from_symbol,
    is_formally_neutral,
    total_formal_charge,
)
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.species import FLiBeSpecies


def _configuration(
    species: tuple[str, ...],
) -> FLiBeConfiguration:
    """Build one finite FLiBe-domain atomic configuration."""

    positions = tuple(
        (
            float(index),
            0.0,
            0.0,
        )
        for index in range(
            len(species)
        )
    )

    atomic = AtomicConfiguration(
        species=species,
        positions=positions,
    )

    return FLiBeConfiguration(
        configuration=atomic
    )


def _reference_configuration() -> FLiBeConfiguration:
    """Build one exact 2 LiF : 1 BeF2 configuration."""

    return _configuration(
        (
            "Li",
            "Li",
            "Be",
            "F",
            "F",
            "F",
            "F",
        )
    )


def test_formal_charge_table_has_canonical_species_order() -> None:
    """Formal-charge table must use canonical Li, Be, F order."""

    assert tuple(
        species
        for species, _ in FLIBE_FORMAL_CHARGES
    ) == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_formal_charge_table_contains_exact_assignments() -> None:
    """Formal-charge table must contain the defined integer assignments."""

    assert FLIBE_FORMAL_CHARGES == (
        (
            FLiBeSpecies.LITHIUM,
            1,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            2,
        ),
        (
            FLiBeSpecies.FLUORINE,
            -1,
        ),
    )


def test_formal_charge_table_contains_each_species_once() -> None:
    """Every canonical FLiBe species must have one charge assignment."""

    species = tuple(
        item
        for item, _ in FLIBE_FORMAL_CHARGES
    )

    assert len(
        species
    ) == len(
        set(species)
    )

    assert set(
        species
    ) == set(
        FLiBeSpecies
    )


@pytest.mark.parametrize(
    ("species", "expected"),
    (
        (
            FLiBeSpecies.LITHIUM,
            1,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            2,
        ),
        (
            FLiBeSpecies.FLUORINE,
            -1,
        ),
    ),
)
def test_formal_charge_returns_species_assignment(
    species: FLiBeSpecies,
    expected: int,
) -> None:
    """Canonical species must map to their formal ionic charges."""

    assert formal_charge(
        species
    ) == expected


@pytest.mark.parametrize(
    "invalid_species",
    (
        "Li",
        "Be",
        "F",
        None,
        True,
        False,
        1,
        -1,
        0,
        (),
    ),
)
def test_formal_charge_requires_flibe_species(
    invalid_species,
) -> None:
    """Enum-level charge lookup must require FLiBeSpecies."""

    with pytest.raises(
        TypeError,
        match="species must be an FLiBeSpecies",
    ):
        formal_charge(
            invalid_species
        )


@pytest.mark.parametrize(
    ("symbol", "expected"),
    (
        (
            "Li",
            1,
        ),
        (
            "Be",
            2,
        ),
        (
            "F",
            -1,
        ),
    ),
)
def test_formal_charge_from_symbol_returns_assignment(
    symbol: str,
    expected: int,
) -> None:
    """Canonical symbols must map to their formal charges."""

    assert formal_charge_from_symbol(
        symbol
    ) == expected


@pytest.mark.parametrize(
    "invalid_symbol",
    (
        "li",
        "LI",
        "be",
        "BE",
        "f",
        "Na",
        "K",
        "",
        " ",
        "Li ",
        " Be",
    ),
)
def test_formal_charge_from_symbol_rejects_unsupported_symbols(
    invalid_symbol: str,
) -> None:
    """Symbol charge lookup must reject noncanonical symbols."""

    with pytest.raises(
        ValueError,
        match="unsupported FLiBe species symbol",
    ):
        formal_charge_from_symbol(
            invalid_symbol
        )


@pytest.mark.parametrize(
    "invalid_symbol",
    (
        None,
        True,
        False,
        1,
        1.0,
        (),
        [],
        {},
    ),
)
def test_formal_charge_from_symbol_requires_string(
    invalid_symbol,
) -> None:
    """Symbol charge lookup must require a string."""

    with pytest.raises(
        TypeError,
        match="symbol must be a string",
    ):
        formal_charge_from_symbol(
            invalid_symbol
        )


def test_configuration_charges_preserve_atom_order() -> None:
    """Per-atom formal charges must follow configuration atom order."""

    configuration = _configuration(
        (
            "F",
            "Li",
            "Be",
            "F",
            "Li",
        )
    )

    assert configuration_formal_charges(
        configuration
    ) == (
        -1,
        1,
        2,
        -1,
        1,
    )


def test_reference_configuration_charges_are_exact() -> None:
    """Reference 2 LiF : 1 BeF2 configuration must have exact charges."""

    configuration = _reference_configuration()

    assert configuration_formal_charges(
        configuration
    ) == (
        1,
        1,
        2,
        -1,
        -1,
        -1,
        -1,
    )


def test_pure_lif_configuration_is_formally_neutral() -> None:
    """Stoichiometric LiF must have zero total formal charge."""

    configuration = _configuration(
        (
            "Li",
            "Li",
            "F",
            "F",
        )
    )

    assert total_formal_charge(
        configuration
    ) == 0

    assert is_formally_neutral(
        configuration
    )


def test_pure_bef2_configuration_is_formally_neutral() -> None:
    """Stoichiometric BeF2 must have zero total formal charge."""

    configuration = _configuration(
        (
            "Be",
            "Be",
            "F",
            "F",
            "F",
            "F",
        )
    )

    assert total_formal_charge(
        configuration
    ) == 0

    assert is_formally_neutral(
        configuration
    )


def test_reference_configuration_is_formally_neutral() -> None:
    """Reference 2 LiF : 1 BeF2 configuration must be formally neutral."""

    configuration = _reference_configuration()

    assert total_formal_charge(
        configuration
    ) == 0

    assert is_formally_neutral(
        configuration
    )


def test_scaled_reference_configuration_remains_neutral() -> None:
    """Integer replication of reference stoichiometry preserves neutrality."""

    configuration = _configuration(
        (
            "Li",
            "Li",
            "Li",
            "Li",
            "Be",
            "Be",
            "F",
            "F",
            "F",
            "F",
            "F",
            "F",
            "F",
            "F",
        )
    )

    assert total_formal_charge(
        configuration
    ) == 0

    assert is_formally_neutral(
        configuration
    )


def test_nonstoichiometric_supported_species_can_have_positive_charge() -> None:
    """Supported species alone do not imply formal neutrality."""

    configuration = _configuration(
        (
            "Li",
            "Be",
            "F",
        )
    )

    assert total_formal_charge(
        configuration
    ) == 2

    assert not is_formally_neutral(
        configuration
    )


def test_nonstoichiometric_supported_species_can_have_negative_charge() -> None:
    """Excess fluorine can produce a negative formal-charge total."""

    configuration = _configuration(
        (
            "Li",
            "F",
            "F",
        )
    )

    assert total_formal_charge(
        configuration
    ) == -1

    assert not is_formally_neutral(
        configuration
    )


@pytest.mark.parametrize(
    "invalid_configuration",
    (
        None,
        True,
        False,
        1,
        (),
        {},
    ),
)
def test_configuration_formal_charges_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Per-atom charge construction requires FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        configuration_formal_charges(
            invalid_configuration
        )


@pytest.mark.parametrize(
    "invalid_configuration",
    (
        None,
        True,
        False,
        1,
        (),
        {},
    ),
)
def test_total_formal_charge_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Total charge evaluation requires FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        total_formal_charge(
            invalid_configuration
        )


@pytest.mark.parametrize(
    "invalid_configuration",
    (
        None,
        True,
        False,
        1,
        (),
        {},
    ),
)
def test_formal_neutrality_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Formal-neutrality evaluation requires FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        is_formally_neutral(
            invalid_configuration
        )


def test_formal_charge_state_accepts_consistent_state() -> None:
    """FormalChargeState must retain a consistent charge tuple and total."""

    state = FormalChargeState(
        charges=(
            1,
            2,
            -1,
            -1,
            -1,
            -1,
        ),
        total_charge=-1,
    )

    assert state.charges == (
        1,
        2,
        -1,
        -1,
        -1,
        -1,
    )

    assert state.total_charge == -1


def test_formal_charge_state_neutral_property_is_true_at_zero_total() -> None:
    """Zero total formal charge must set is_neutral to True."""

    state = FormalChargeState(
        charges=(
            1,
            -1,
        ),
        total_charge=0,
    )

    assert state.is_neutral


def test_formal_charge_state_neutral_property_is_false_for_positive_total() -> None:
    """Positive total formal charge must not be classified as neutral."""

    state = FormalChargeState(
        charges=(
            1,
            1,
            -1,
        ),
        total_charge=1,
    )

    assert not state.is_neutral


def test_formal_charge_state_neutral_property_is_false_for_negative_total() -> None:
    """Negative total formal charge must not be classified as neutral."""

    state = FormalChargeState(
        charges=(
            1,
            -1,
            -1,
        ),
        total_charge=-1,
    )

    assert not state.is_neutral


def test_formal_charge_state_rejects_empty_charge_tuple() -> None:
    """Formal-charge state must contain at least one per-atom charge."""

    with pytest.raises(
        ValueError,
        match="charges must not be empty",
    ):
        FormalChargeState(
            charges=(),
            total_charge=0,
        )


@pytest.mark.parametrize(
    "invalid_charges",
    (
        [1, -1],
        {1, -1},
        "1",
        None,
        1,
    ),
)
def test_formal_charge_state_requires_charge_tuple(
    invalid_charges,
) -> None:
    """Formal-charge state charges must use immutable tuple storage."""

    with pytest.raises(
        TypeError,
        match="charges must be a tuple",
    ):
        FormalChargeState(
            charges=invalid_charges,
            total_charge=0,
        )


@pytest.mark.parametrize(
    "invalid_charge",
    (
        True,
        False,
        1.0,
        -1.0,
        0.0,
        "1",
        None,
        (),
    ),
)
def test_formal_charge_state_rejects_noninteger_charge_member(
    invalid_charge,
) -> None:
    """Every per-atom formal charge must be a non-Boolean integer."""

    with pytest.raises(
        TypeError,
        match=(
            "charge must be a "
            "non-Boolean integer"
        ),
    ):
        FormalChargeState(
            charges=(
                1,
                invalid_charge,
                -1,
            ),
            total_charge=0,
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        True,
        False,
        0.0,
        1.0,
        "0",
        None,
        (),
    ),
)
def test_formal_charge_state_rejects_noninteger_total(
    invalid_total,
) -> None:
    """Total formal charge must be a non-Boolean integer."""

    with pytest.raises(
        TypeError,
        match=(
            "total_charge must be a "
            "non-Boolean integer"
        ),
    ):
        FormalChargeState(
            charges=(
                1,
                -1,
            ),
            total_charge=invalid_total,
        )


def test_formal_charge_state_rejects_inconsistent_total() -> None:
    """Stored total must equal the sum of per-atom formal charges."""

    with pytest.raises(
        ValueError,
        match=(
            "total_charge must equal "
            "the sum of charges"
        ),
    ):
        FormalChargeState(
            charges=(
                1,
                2,
                -1,
            ),
            total_charge=0,
        )


def test_build_formal_charge_state_matches_configuration() -> None:
    """State builder must reproduce configuration charges and total."""

    configuration = _reference_configuration()

    state = build_formal_charge_state(
        configuration
    )

    assert state.charges == configuration_formal_charges(
        configuration
    )

    assert state.total_charge == total_formal_charge(
        configuration
    )


def test_reference_built_charge_state_is_neutral() -> None:
    """Reference configuration builder result must be formally neutral."""

    state = build_formal_charge_state(
        _reference_configuration()
    )

    assert state.total_charge == 0
    assert state.is_neutral


def test_nonstoichiometric_built_charge_state_preserves_nonzero_total() -> None:
    """State builder must not force unsupported neutrality."""

    state = build_formal_charge_state(
        _configuration(
            (
                "Li",
                "Be",
                "F",
            )
        )
    )

    assert state.total_charge == 2
    assert not state.is_neutral


@pytest.mark.parametrize(
    "invalid_configuration",
    (
        None,
        True,
        False,
        1,
        (),
        {},
    ),
)
def test_build_formal_charge_state_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Formal-charge state builder requires FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        build_formal_charge_state(
            invalid_configuration
        )


def test_formal_neutrality_identity_matches_stoichiometry() -> None:
    """LiF-BeF2 stoichiometry must satisfy the formal-charge identity."""

    configuration = _reference_configuration()

    counts = dict(
        configuration.species_counts
    )

    lithium_count = counts[
        FLiBeSpecies.LITHIUM
    ]
    beryllium_count = counts[
        FLiBeSpecies.BERYLLIUM
    ]
    fluorine_count = counts[
        FLiBeSpecies.FLUORINE
    ]

    assert fluorine_count == (
        lithium_count
        + 2 * beryllium_count
    )

    assert (
        lithium_count
        + 2 * beryllium_count
        - fluorine_count
    ) == 0

    assert total_formal_charge(
        configuration
    ) == 0


def test_formal_charge_zero_is_numeric_charge_total() -> None:
    """Formal neutrality is represented only by zero charge sum."""

    state = build_formal_charge_state(
        _reference_configuration()
    )

    assert isinstance(
        state.total_charge,
        int,
    )
    assert state.total_charge == 0


def test_per_atom_charge_values_are_integer_charge_data() -> None:
    """Per-atom formal charges must remain integer charge data."""

    charges = configuration_formal_charges(
        _reference_configuration()
    )

    assert all(
        isinstance(
            charge,
            int,
        )
        and not isinstance(
            charge,
            bool,
        )
        for charge in charges
    )
