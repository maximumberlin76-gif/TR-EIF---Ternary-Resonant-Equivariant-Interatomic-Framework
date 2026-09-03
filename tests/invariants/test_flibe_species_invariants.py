"""Invariant tests for the TR-EIF FLiBe species contract."""

import pytest

from tr_eif.flibe.species import (
    FLIBE_SPECIES,
    FLiBeSpecies,
    flibe_species_from_symbol,
    flibe_species_symbols,
    is_flibe_species_symbol,
    validate_flibe_species_sequence,
)


def test_species_enum_contains_exact_flibe_species() -> None:
    """FLiBe species enumeration must contain exactly Li, Be, and F."""

    assert tuple(
        species.value
        for species in FLiBeSpecies
    ) == (
        "Li",
        "Be",
        "F",
    )


def test_canonical_species_tuple_has_expected_order() -> None:
    """Canonical FLiBe species order must be Li, Be, F."""

    assert FLIBE_SPECIES == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_canonical_species_tuple_contains_all_enum_members() -> None:
    """Canonical tuple must contain every FLiBe species exactly once."""

    assert FLIBE_SPECIES == tuple(
        FLiBeSpecies
    )

    assert len(
        set(FLIBE_SPECIES)
    ) == len(
        FLIBE_SPECIES
    )


def test_lithium_symbol_is_exact() -> None:
    """Lithium species must use the exact chemical symbol Li."""

    assert FLiBeSpecies.LITHIUM.value == "Li"


def test_beryllium_symbol_is_exact() -> None:
    """Beryllium species must use the exact chemical symbol Be."""

    assert FLiBeSpecies.BERYLLIUM.value == "Be"


def test_fluorine_symbol_is_exact() -> None:
    """Fluorine species must use the exact chemical symbol F."""

    assert FLiBeSpecies.FLUORINE.value == "F"


def test_species_symbols_returns_canonical_order() -> None:
    """Symbol helper must return Li, Be, F in canonical order."""

    assert flibe_species_symbols() == (
        "Li",
        "Be",
        "F",
    )


def test_species_symbols_returns_tuple() -> None:
    """Canonical species symbols must use immutable tuple storage."""

    symbols = flibe_species_symbols()

    assert isinstance(
        symbols,
        tuple,
    )


@pytest.mark.parametrize(
    ("symbol", "expected"),
    (
        (
            "Li",
            FLiBeSpecies.LITHIUM,
        ),
        (
            "Be",
            FLiBeSpecies.BERYLLIUM,
        ),
        (
            "F",
            FLiBeSpecies.FLUORINE,
        ),
    ),
)
def test_species_from_symbol_returns_canonical_enum(
    symbol: str,
    expected: FLiBeSpecies,
) -> None:
    """Each supported symbol must map to its canonical enum member."""

    assert flibe_species_from_symbol(
        symbol
    ) is expected


@pytest.mark.parametrize(
    "invalid_symbol",
    (
        "li",
        "LI",
        "be",
        "BE",
        "f",
        "Fl",
        "Na",
        "K",
        "O",
        "H",
        "",
        " ",
        "Li ",
        " Li",
        "Be ",
        "F ",
    ),
)
def test_species_from_symbol_rejects_noncanonical_symbols(
    invalid_symbol: str,
) -> None:
    """Symbol conversion must reject unsupported or altered strings."""

    with pytest.raises(
        ValueError,
        match="unsupported FLiBe species symbol",
    ):
        flibe_species_from_symbol(
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
def test_species_from_symbol_rejects_non_string_values(
    invalid_symbol,
) -> None:
    """Symbol conversion must require a string."""

    with pytest.raises(
        TypeError,
        match="symbol must be a string",
    ):
        flibe_species_from_symbol(
            invalid_symbol
        )


@pytest.mark.parametrize(
    "symbol",
    (
        "Li",
        "Be",
        "F",
    ),
)
def test_species_symbol_predicate_accepts_supported_symbols(
    symbol: str,
) -> None:
    """Species predicate must accept every canonical FLiBe symbol."""

    assert is_flibe_species_symbol(
        symbol
    )


@pytest.mark.parametrize(
    "symbol",
    (
        "li",
        "LI",
        "be",
        "BE",
        "f",
        "Na",
        "",
        " ",
        "Li ",
    ),
)
def test_species_symbol_predicate_rejects_other_strings(
    symbol: str,
) -> None:
    """Species predicate must reject noncanonical strings."""

    assert not is_flibe_species_symbol(
        symbol
    )


@pytest.mark.parametrize(
    "value",
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
def test_species_symbol_predicate_returns_false_for_non_strings(
    value,
) -> None:
    """Species predicate must return False for non-string objects."""

    assert not is_flibe_species_symbol(
        value
    )


def test_validate_species_sequence_accepts_single_species() -> None:
    """A nonempty sequence may contain one supported species."""

    assert validate_flibe_species_sequence(
        ("Li",)
    ) == (
        FLiBeSpecies.LITHIUM,
    )


def test_validate_species_sequence_accepts_canonical_triplet() -> None:
    """Canonical Li, Be, F input must map to canonical enum members."""

    assert validate_flibe_species_sequence(
        (
            "Li",
            "Be",
            "F",
        )
    ) == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_validate_species_sequence_preserves_input_order() -> None:
    """Canonicalization must preserve the supplied sequence order."""

    assert validate_flibe_species_sequence(
        (
            "F",
            "Li",
            "Be",
            "F",
        )
    ) == (
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_validate_species_sequence_preserves_multiplicity() -> None:
    """Canonicalization must preserve repeated species entries."""

    result = validate_flibe_species_sequence(
        (
            "Li",
            "Li",
            "F",
            "F",
            "F",
        )
    )

    assert result.count(
        FLiBeSpecies.LITHIUM
    ) == 2

    assert result.count(
        FLiBeSpecies.FLUORINE
    ) == 3


def test_validate_species_sequence_returns_tuple() -> None:
    """Canonicalized species sequence must be immutable tuple data."""

    result = validate_flibe_species_sequence(
        (
            "Li",
            "Be",
        )
    )

    assert isinstance(
        result,
        tuple,
    )


def test_validate_species_sequence_rejects_empty_tuple() -> None:
    """Species sequence must contain at least one entry."""

    with pytest.raises(
        ValueError,
        match="species must not be empty",
    ):
        validate_flibe_species_sequence(
            ()
        )


@pytest.mark.parametrize(
    "invalid_sequence",
    (
        ["Li", "Be", "F"],
        {"Li", "Be", "F"},
        "Li",
        None,
        1,
        True,
    ),
)
def test_validate_species_sequence_requires_tuple(
    invalid_sequence,
) -> None:
    """Species sequence container must be exactly a tuple."""

    with pytest.raises(
        TypeError,
        match="species must be a tuple",
    ):
        validate_flibe_species_sequence(
            invalid_sequence
        )


@pytest.mark.parametrize(
    "invalid_symbol",
    (
        "Na",
        "li",
        "",
        "Li ",
    ),
)
def test_validate_species_sequence_rejects_unsupported_member(
    invalid_symbol: str,
) -> None:
    """Every sequence member must be a canonical FLiBe symbol."""

    with pytest.raises(
        ValueError,
        match="unsupported FLiBe species symbol",
    ):
        validate_flibe_species_sequence(
            (
                "Li",
                invalid_symbol,
                "F",
            )
        )


@pytest.mark.parametrize(
    "invalid_member",
    (
        None,
        True,
        False,
        1,
        1.0,
        (),
    ),
)
def test_validate_species_sequence_rejects_non_string_member(
    invalid_member,
) -> None:
    """Every sequence member must satisfy the symbol string contract."""

    with pytest.raises(
        TypeError,
        match="symbol must be a string",
    ):
        validate_flibe_species_sequence(
            (
                "Li",
                invalid_member,
                "F",
            )
        )


def test_enum_members_are_string_compatible() -> None:
    """FLiBe species enum members must retain string-enum semantics."""

    assert isinstance(
        FLiBeSpecies.LITHIUM,
        str,
    )
    assert isinstance(
        FLiBeSpecies.BERYLLIUM,
        str,
    )
    assert isinstance(
        FLiBeSpecies.FLUORINE,
        str,
    )


def test_enum_construction_from_supported_symbols_is_exact() -> None:
    """Direct enum construction must reproduce canonical members."""

    assert FLiBeSpecies(
        "Li"
    ) is FLiBeSpecies.LITHIUM

    assert FLiBeSpecies(
        "Be"
    ) is FLiBeSpecies.BERYLLIUM

    assert FLiBeSpecies(
        "F"
    ) is FLiBeSpecies.FLUORINE


def test_species_helpers_do_not_normalize_case() -> None:
    """Species helpers must not silently normalize symbol case."""

    canonical = (
        "Li",
        "Be",
        "F",
    )

    altered = tuple(
        symbol.lower()
        for symbol in canonical
    )

    assert altered != canonical

    assert all(
        not is_flibe_species_symbol(
            symbol
        )
        for symbol in altered
    )


def test_species_helpers_do_not_strip_whitespace() -> None:
    """Species helpers must not silently strip symbol whitespace."""

    assert not is_flibe_species_symbol(
        " Li"
    )
    assert not is_flibe_species_symbol(
        "Li "
    )
    assert not is_flibe_species_symbol(
        "\tLi"
    )
    assert not is_flibe_species_symbol(
        "Li\n"
    )
