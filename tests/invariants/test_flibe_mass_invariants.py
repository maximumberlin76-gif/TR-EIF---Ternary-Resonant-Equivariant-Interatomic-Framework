"""Invariant tests for the TR-EIF FLiBe atomic-mass contract."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.configuration import FLiBeConfiguration
from tr_eif.flibe.mass import (
    FLiBeMassParameters,
    configuration_masses,
    total_configuration_mass,
)
from tr_eif.flibe.species import FLiBeSpecies


def _parameters() -> FLiBeMassParameters:
    """Return deterministic test-only mass parameters."""

    return FLiBeMassParameters(
        lithium=2.0,
        beryllium=3.0,
        fluorine=5.0,
    )


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
        for index in range(len(species))
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


def test_mass_parameters_preserve_values() -> None:
    """Validated mass parameters must retain supplied finite values."""

    parameters = _parameters()

    assert parameters.lithium == 2.0
    assert parameters.beryllium == 3.0
    assert parameters.fluorine == 5.0


def test_mass_parameters_normalize_integer_inputs_to_float() -> None:
    """Integer mass inputs must be normalized to floating-point values."""

    parameters = FLiBeMassParameters(
        lithium=2,
        beryllium=3,
        fluorine=5,
    )

    assert isinstance(parameters.lithium, float)
    assert isinstance(parameters.beryllium, float)
    assert isinstance(parameters.fluorine, float)

    assert parameters == FLiBeMassParameters(
        lithium=2.0,
        beryllium=3.0,
        fluorine=5.0,
    )


def test_species_masses_use_canonical_order() -> None:
    """Species masses must use canonical Li, Be, F order."""

    parameters = _parameters()

    assert tuple(
        species
        for species, _ in parameters.species_masses
    ) == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_species_masses_contain_exact_parameter_values() -> None:
    """Canonical species mapping must retain all supplied masses."""

    parameters = _parameters()

    assert parameters.species_masses == (
        (
            FLiBeSpecies.LITHIUM,
            2.0,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            3.0,
        ),
        (
            FLiBeSpecies.FLUORINE,
            5.0,
        ),
    )


def test_species_masses_contains_each_species_once() -> None:
    """Each FLiBe species must occur once in the mass mapping."""

    parameters = _parameters()

    species = tuple(
        item
        for item, _ in parameters.species_masses
    )

    assert len(species) == len(set(species))
    assert set(species) == set(FLiBeSpecies)


@pytest.mark.parametrize(
    ("species", "expected"),
    (
        (
            FLiBeSpecies.LITHIUM,
            2.0,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            3.0,
        ),
        (
            FLiBeSpecies.FLUORINE,
            5.0,
        ),
    ),
)
def test_mass_for_species_returns_exact_parameter(
    species: FLiBeSpecies,
    expected: float,
) -> None:
    """Canonical species lookup must return its configured mass."""

    assert _parameters().mass_for_species(
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
def test_mass_for_species_requires_flibe_species(
    invalid_species,
) -> None:
    """Enum-level mass lookup must require FLiBeSpecies."""

    with pytest.raises(
        TypeError,
        match="species must be an FLiBeSpecies",
    ):
        _parameters().mass_for_species(
            invalid_species
        )


@pytest.mark.parametrize(
    ("symbol", "expected"),
    (
        (
            "Li",
            2.0,
        ),
        (
            "Be",
            3.0,
        ),
        (
            "F",
            5.0,
        ),
    ),
)
def test_mass_for_symbol_returns_exact_parameter(
    symbol: str,
    expected: float,
) -> None:
    """Canonical symbols must map to configured masses."""

    assert _parameters().mass_for_symbol(
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
def test_mass_for_symbol_rejects_unsupported_symbols(
    invalid_symbol: str,
) -> None:
    """Symbol lookup must reject unsupported or altered symbols."""

    with pytest.raises(
        ValueError,
        match="unsupported FLiBe species symbol",
    ):
        _parameters().mass_for_symbol(
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
def test_mass_for_symbol_requires_string(
    invalid_symbol,
) -> None:
    """Symbol-level mass lookup must require a string."""

    with pytest.raises(
        TypeError,
        match="symbol must be a string",
    ):
        _parameters().mass_for_symbol(
            invalid_symbol
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "lithium",
        "beryllium",
        "fluorine",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        True,
        False,
        "1.0",
        None,
        (),
    ),
)
def test_mass_parameters_reject_non_real_or_boolean_values(
    field_name: str,
    invalid_value,
) -> None:
    """Every mass parameter must be a real non-Boolean number."""

    values = {
        "lithium": 2.0,
        "beryllium": 3.0,
        "fluorine": 5.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        TypeError,
        match=(
            rf"{field_name} must be a real "
            "non-Boolean number"
        ),
    ):
        FLiBeMassParameters(
            **values
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "lithium",
        "beryllium",
        "fluorine",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_mass_parameters_reject_nonfinite_values(
    field_name: str,
    invalid_value: float,
) -> None:
    """Every mass parameter must be finite."""

    values = {
        "lithium": 2.0,
        "beryllium": 3.0,
        "fluorine": 5.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be finite",
    ):
        FLiBeMassParameters(
            **values
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "lithium",
        "beryllium",
        "fluorine",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        0.0,
        -1.0,
        -1.0e-12,
    ),
)
def test_mass_parameters_reject_nonpositive_values(
    field_name: str,
    invalid_value: float,
) -> None:
    """Every mass parameter must be strictly positive."""

    values = {
        "lithium": 2.0,
        "beryllium": 3.0,
        "fluorine": 5.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be positive",
    ):
        FLiBeMassParameters(
            **values
        )


def test_configuration_masses_preserve_atom_order() -> None:
    """Per-atom masses must follow atomic species ordering exactly."""

    configuration = _configuration(
        (
            "F",
            "Li",
            "Be",
            "F",
            "Li",
        )
    )

    assert configuration_masses(
        configuration,
        _parameters(),
    ) == (
        5.0,
        2.0,
        3.0,
        5.0,
        2.0,
    )


def test_reference_configuration_masses_are_exact() -> None:
    """Reference composition must map every atom to its species mass."""

    masses = configuration_masses(
        _reference_configuration(),
        _parameters(),
    )

    assert masses == (
        2.0,
        2.0,
        3.0,
        5.0,
        5.0,
        5.0,
        5.0,
    )


def test_configuration_mass_count_equals_atom_count() -> None:
    """Mass mapping must produce exactly one mass for every atom."""

    configuration = _reference_configuration()

    masses = configuration_masses(
        configuration,
        _parameters(),
    )

    assert len(masses) == configuration.atom_count


def test_configuration_masses_are_positive() -> None:
    """Every mapped per-atom mass must remain positive."""

    masses = configuration_masses(
        _reference_configuration(),
        _parameters(),
    )

    assert all(
        mass > 0.0
        for mass in masses
    )


def test_configuration_masses_are_float_values() -> None:
    """Per-atom mass mapping must expose normalized float values."""

    masses = configuration_masses(
        _reference_configuration(),
        _parameters(),
    )

    assert all(
        isinstance(mass, float)
        for mass in masses
    )


def test_total_configuration_mass_matches_per_atom_sum() -> None:
    """Total configuration mass must equal the explicit per-atom sum."""

    configuration = _reference_configuration()
    parameters = _parameters()

    masses = configuration_masses(
        configuration,
        parameters,
    )

    assert total_configuration_mass(
        configuration,
        parameters,
    ) == pytest.approx(
        sum(masses)
    )


def test_reference_total_mass_matches_species_counts() -> None:
    """Total mass must equal the count-weighted species-mass sum."""

    configuration = _reference_configuration()
    parameters = _parameters()

    expected = (
        2 * parameters.lithium
        + parameters.beryllium
        + 4 * parameters.fluorine
    )

    assert total_configuration_mass(
        configuration,
        parameters,
    ) == pytest.approx(
        expected
    )


def test_pure_lif_total_mass_matches_species_counts() -> None:
    """LiF endpoint mass must be determined by Li and F counts."""

    configuration = _configuration(
        (
            "Li",
            "Li",
            "F",
            "F",
        )
    )

    parameters = _parameters()

    expected = (
        2 * parameters.lithium
        + 2 * parameters.fluorine
    )

    assert total_configuration_mass(
        configuration,
        parameters,
    ) == pytest.approx(
        expected
    )


def test_pure_bef2_total_mass_matches_species_counts() -> None:
    """BeF2 endpoint mass must be determined by Be and F counts."""

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

    parameters = _parameters()

    expected = (
        2 * parameters.beryllium
        + 4 * parameters.fluorine
    )

    assert total_configuration_mass(
        configuration,
        parameters,
    ) == pytest.approx(
        expected
    )


def test_uniform_parameter_scaling_scales_per_atom_masses() -> None:
    """Uniform positive scaling must scale every mapped mass equally."""

    configuration = _reference_configuration()

    first = FLiBeMassParameters(
        lithium=2.0,
        beryllium=3.0,
        fluorine=5.0,
    )

    second = FLiBeMassParameters(
        lithium=14.0,
        beryllium=21.0,
        fluorine=35.0,
    )

    first_masses = configuration_masses(
        configuration,
        first,
    )

    second_masses = configuration_masses(
        configuration,
        second,
    )

    assert second_masses == pytest.approx(
        tuple(
            7.0 * mass
            for mass in first_masses
        )
    )


def test_uniform_parameter_scaling_scales_total_mass() -> None:
    """Uniform positive scaling must scale total mass by the same factor."""

    configuration = _reference_configuration()

    first = FLiBeMassParameters(
        lithium=2.0,
        beryllium=3.0,
        fluorine=5.0,
    )

    second = FLiBeMassParameters(
        lithium=8.0,
        beryllium=12.0,
        fluorine=20.0,
    )

    assert total_configuration_mass(
        configuration,
        second,
    ) == pytest.approx(
        4.0
        * total_configuration_mass(
            configuration,
            first,
        )
    )


def test_mass_mapping_does_not_modify_configuration() -> None:
    """Mass lookup must leave the wrapped atomic configuration unchanged."""

    configuration = _reference_configuration()

    original_species = configuration.configuration.species
    original_positions = configuration.configuration.positions

    configuration_masses(
        configuration,
        _parameters(),
    )

    assert (
        configuration.configuration.species
        == original_species
    )
    assert (
        configuration.configuration.positions
        == original_positions
    )


def test_mass_mapping_does_not_modify_parameters() -> None:
    """Per-atom mapping must not mutate species mass parameters."""

    parameters = _parameters()

    original = parameters.species_masses

    configuration_masses(
        _reference_configuration(),
        parameters,
    )

    assert parameters.species_masses == original


@pytest.mark.parametrize(
    "invalid_configuration",
    (
        None,
        True,
        False,
        1,
        1.0,
        (),
        {},
    ),
)
def test_configuration_masses_requires_flibe_configuration(
    invalid_configuration,
) -> None:
    """Mass mapping must require an FLiBeConfiguration."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        configuration_masses(
            invalid_configuration,
            _parameters(),
        )


@pytest.mark.parametrize(
    "invalid_parameters",
    (
        None,
        True,
        False,
        1,
        1.0,
        (),
        {},
    ),
)
def test_configuration_masses_requires_mass_parameters(
    invalid_parameters,
) -> None:
    """Mass mapping must require FLiBeMassParameters."""

    with pytest.raises(
        TypeError,
        match=(
            "parameters must be an "
            "FLiBeMassParameters"
        ),
    ):
        configuration_masses(
            _reference_configuration(),
            invalid_parameters,
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
def test_total_mass_propagates_configuration_validation(
    invalid_configuration,
) -> None:
    """Total mass evaluation must preserve configuration type validation."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "FLiBeConfiguration"
        ),
    ):
        total_configuration_mass(
            invalid_configuration,
            _parameters(),
        )


@pytest.mark.parametrize(
    "invalid_parameters",
    (
        None,
        True,
        False,
        1,
        (),
        {},
    ),
)
def test_total_mass_propagates_parameter_validation(
    invalid_parameters,
) -> None:
    """Total mass evaluation must preserve parameter type validation."""

    with pytest.raises(
        TypeError,
        match=(
            "parameters must be an "
            "FLiBeMassParameters"
        ),
    ):
        total_configuration_mass(
            _reference_configuration(),
            invalid_parameters,
        )


def test_mass_contract_accepts_fractional_positive_values() -> None:
    """Mass parameters may contain arbitrary positive finite test values."""

    parameters = FLiBeMassParameters(
        lithium=0.25,
        beryllium=1.5,
        fluorine=9.75,
    )

    assert parameters.species_masses == (
        (
            FLiBeSpecies.LITHIUM,
            0.25,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            1.5,
        ),
        (
            FLiBeSpecies.FLUORINE,
            9.75,
        ),
    )


def test_mass_contract_does_not_require_species_mass_ordering() -> None:
    """The contract imposes positivity, not relative species-mass ordering."""

    parameters = FLiBeMassParameters(
        lithium=7.0,
        beryllium=2.0,
        fluorine=1.0,
    )

    assert parameters.lithium > parameters.beryllium
    assert parameters.beryllium > parameters.fluorine


def test_equal_species_mass_parameters_are_allowed() -> None:
    """The structural mass contract permits equal positive parameters."""

    parameters = FLiBeMassParameters(
        lithium=3.0,
        beryllium=3.0,
        fluorine=3.0,
    )

    masses = configuration_masses(
        _reference_configuration(),
        parameters,
    )

    assert masses == (
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
        3.0,
    )


def test_total_mass_is_positive_for_valid_configuration() -> None:
    """Positive per-species parameters must produce positive total mass."""

    assert total_configuration_mass(
        _reference_configuration(),
        _parameters(),
    ) > 0.0
