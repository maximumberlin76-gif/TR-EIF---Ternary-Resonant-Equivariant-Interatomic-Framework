"""Invariant tests for the TR-EIF FLiBe configuration contract."""

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.flibe.composition import (
    FLiBeComposition,
    eutectic_flibe_composition,
)
from tr_eif.flibe.configuration import (
    FLiBeConfiguration,
    flibe_species_counts,
    validate_flibe_configuration,
)
from tr_eif.flibe.species import FLiBeSpecies


def _configuration(
    species: tuple[str, ...],
) -> AtomicConfiguration:
    """Build a finite nonperiodic configuration for species tests."""

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

    return AtomicConfiguration(
        species=species,
        positions=positions,
    )


def _reference_configuration() -> AtomicConfiguration:
    """Build one exact 2 LiF : 1 BeF2 atomic configuration."""

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


def test_configuration_wraps_atomic_configuration() -> None:
    """FLiBe wrapper must retain the original atomic configuration."""

    configuration = _reference_configuration()

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert wrapped.configuration is configuration


def test_configuration_reports_atom_count() -> None:
    """Atom count must equal the underlying species cardinality."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert wrapped.atom_count == 7


def test_configuration_species_are_canonicalized() -> None:
    """Underlying symbols must map to canonical FLiBe species."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert wrapped.species == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.FLUORINE,
    )


def test_species_order_matches_atomic_configuration_order() -> None:
    """FLiBe canonicalization must preserve atom ordering."""

    configuration = _configuration(
        (
            "F",
            "Li",
            "Be",
            "F",
        )
    )

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert wrapped.species == (
        FLiBeSpecies.FLUORINE,
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_species_counts_use_canonical_order() -> None:
    """Species counts must be returned in Li, Be, F order."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert wrapped.species_counts == (
        (
            FLiBeSpecies.LITHIUM,
            2,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            1,
        ),
        (
            FLiBeSpecies.FLUORINE,
            4,
        ),
    )


def test_species_counts_include_zero_counts() -> None:
    """Canonical counts must retain absent supported species as zero."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            (
                "Li",
                "F",
            )
        )
    )

    assert wrapped.species_counts == (
        (
            FLiBeSpecies.LITHIUM,
            1,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            0,
        ),
        (
            FLiBeSpecies.FLUORINE,
            1,
        ),
    )


def test_atomic_fractions_use_canonical_order() -> None:
    """Atomic fractions must use canonical Li, Be, F order."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert tuple(
        species
        for species, _ in wrapped.atomic_fractions
    ) == (
        FLiBeSpecies.LITHIUM,
        FLiBeSpecies.BERYLLIUM,
        FLiBeSpecies.FLUORINE,
    )


def test_reference_atomic_fractions_match_two_one_four_ratio() -> None:
    """Reference configuration must yield atomic fractions 2/7, 1/7, 4/7."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    fractions = dict(
        wrapped.atomic_fractions
    )

    assert fractions[
        FLiBeSpecies.LITHIUM
    ] == pytest.approx(
        2.0 / 7.0
    )

    assert fractions[
        FLiBeSpecies.BERYLLIUM
    ] == pytest.approx(
        1.0 / 7.0
    )

    assert fractions[
        FLiBeSpecies.FLUORINE
    ] == pytest.approx(
        4.0 / 7.0
    )


def test_atomic_fractions_sum_to_one() -> None:
    """Discrete atomic fractions must form a normalized composition."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert sum(
        fraction
        for _, fraction in wrapped.atomic_fractions
    ) == pytest.approx(
        1.0
    )


def test_reference_configuration_implies_reference_composition() -> None:
    """Two Li, one Be, and four F atoms must imply 2 LiF : 1 BeF2."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    composition = wrapped.composition()

    assert composition == eutectic_flibe_composition()


def test_composition_is_normalized_from_discrete_counts() -> None:
    """Discrete formula-unit counts must produce normalized composition."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            (
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
            )
        )
    )

    composition = wrapped.composition()

    assert composition.lif_fraction == pytest.approx(
        3.0 / 5.0
    )
    assert composition.bef2_fraction == pytest.approx(
        2.0 / 5.0
    )


def test_pure_lif_configuration_is_supported() -> None:
    """A stoichiometric LiF-only endpoint must be representable."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            (
                "Li",
                "Li",
                "F",
                "F",
            )
        )
    )

    assert wrapped.composition() == FLiBeComposition(
        lif_fraction=1.0,
        bef2_fraction=0.0,
    )


def test_pure_bef2_configuration_is_supported() -> None:
    """A stoichiometric BeF2-only endpoint must be representable."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            (
                "Be",
                "Be",
                "F",
                "F",
                "F",
                "F",
            )
        )
    )

    assert wrapped.composition() == FLiBeComposition(
        lif_fraction=0.0,
        bef2_fraction=1.0,
    )


def test_scaled_stoichiometric_configuration_preserves_composition() -> None:
    """Integer replication of stoichiometry must preserve composition."""

    first = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    second = FLiBeConfiguration(
        configuration=_configuration(
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
    )

    assert second.composition() == first.composition()


@pytest.mark.parametrize(
    "species",
    (
        (
            "Li",
            "Be",
            "F",
        ),
        (
            "Li",
            "Li",
            "Be",
            "F",
            "F",
            "F",
        ),
        (
            "Li",
            "F",
            "F",
        ),
        (
            "Be",
            "F",
        ),
        (
            "F",
            "F",
        ),
    ),
)
def test_nonstoichiometric_configuration_rejected_by_composition(
    species: tuple[str, ...],
) -> None:
    """Composition extraction must reject invalid LiF-BeF2 stoichiometry."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            species
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "FLiBe configuration does not satisfy "
            "LiF-BeF2 fluorine stoichiometry"
        ),
    ):
        wrapped.composition()


def test_fluorine_only_configuration_has_no_formula_units() -> None:
    """Fluorine-only input must not define an LiF-BeF2 composition."""

    wrapped = FLiBeConfiguration(
        configuration=_configuration(
            (
                "F",
                "F",
                "F",
            )
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "FLiBe configuration does not satisfy "
            "LiF-BeF2 fluorine stoichiometry"
        ),
    ):
        wrapped.composition()


@pytest.mark.parametrize(
    "unsupported_symbol",
    (
        "Na",
        "K",
        "O",
        "H",
        "Cl",
        "li",
        "be",
        "f",
        "Li ",
    ),
)
def test_wrapper_rejects_unsupported_species(
    unsupported_symbol: str,
) -> None:
    """FLiBe configuration must contain only canonical Li, Be, F symbols."""

    configuration = _configuration(
        (
            "Li",
            unsupported_symbol,
            "F",
        )
    )

    with pytest.raises(
        ValueError,
        match="unsupported FLiBe species symbol",
    ):
        FLiBeConfiguration(
            configuration=configuration
        )


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
def test_wrapper_requires_atomic_configuration(
    invalid_configuration,
) -> None:
    """FLiBe wrapper must require an AtomicConfiguration instance."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "AtomicConfiguration"
        ),
    ):
        FLiBeConfiguration(
            configuration=invalid_configuration
        )


def test_validate_configuration_returns_wrapper() -> None:
    """Validation helper must construct an FLiBe configuration wrapper."""

    configuration = _reference_configuration()

    wrapped = validate_flibe_configuration(
        configuration
    )

    assert isinstance(
        wrapped,
        FLiBeConfiguration,
    )
    assert wrapped.configuration is configuration


def test_validate_configuration_rejects_non_atomic_input() -> None:
    """Validation helper must preserve the wrapper type boundary."""

    with pytest.raises(
        TypeError,
        match=(
            "configuration must be an "
            "AtomicConfiguration"
        ),
    ):
        validate_flibe_configuration(
            None
        )


def test_species_count_helper_matches_wrapper_counts() -> None:
    """Species-count helper must reproduce canonical wrapper counts."""

    configuration = _reference_configuration()

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert flibe_species_counts(
        configuration
    ) == wrapped.species_counts


def test_species_count_helper_preserves_zero_count_species() -> None:
    """Species-count helper must retain canonical zero-count entries."""

    configuration = _configuration(
        (
            "Be",
            "F",
            "F",
        )
    )

    assert flibe_species_counts(
        configuration
    ) == (
        (
            FLiBeSpecies.LITHIUM,
            0,
        ),
        (
            FLiBeSpecies.BERYLLIUM,
            1,
        ),
        (
            FLiBeSpecies.FLUORINE,
            2,
        ),
    )


def test_exact_composition_match_returns_true() -> None:
    """Exact discrete and requested compositions must match at zero tolerance."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert wrapped.matches_composition(
        eutectic_flibe_composition()
    )


def test_exact_composition_mismatch_returns_false() -> None:
    """Different valid compositions must not match at zero tolerance."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    requested = FLiBeComposition(
        lif_fraction=3.0,
        bef2_fraction=1.0,
    )

    assert not wrapped.matches_composition(
        requested
    )


def test_composition_match_accepts_difference_within_tolerance() -> None:
    """Absolute tolerance must permit bounded fraction differences."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    requested = FLiBeComposition(
        lif_fraction=0.67,
        bef2_fraction=0.33,
    )

    assert wrapped.matches_composition(
        requested,
        absolute_tolerance=0.004,
    )


def test_composition_match_rejects_difference_above_tolerance() -> None:
    """Fraction difference above absolute tolerance must reject the match."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    requested = FLiBeComposition(
        lif_fraction=0.67,
        bef2_fraction=0.33,
    )

    assert not wrapped.matches_composition(
        requested,
        absolute_tolerance=0.003,
    )


def test_zero_tolerance_requires_exact_normalized_values() -> None:
    """Zero tolerance must retain exact normalized-fraction comparison."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    exact = FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )

    nearby = FLiBeComposition(
        lif_fraction=2.000001,
        bef2_fraction=1.0,
    )

    assert wrapped.matches_composition(
        exact,
        absolute_tolerance=0.0,
    )

    assert not wrapped.matches_composition(
        nearby,
        absolute_tolerance=0.0,
    )


def test_integer_tolerance_is_normalized_and_accepted() -> None:
    """A nonnegative integer tolerance must satisfy the numeric contract."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert wrapped.matches_composition(
        FLiBeComposition(
            lif_fraction=1.0,
            bef2_fraction=0.0,
        ),
        absolute_tolerance=1,
    )


@pytest.mark.parametrize(
    "invalid_composition",
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
def test_composition_match_requires_flibe_composition(
    invalid_composition,
) -> None:
    """Composition matching must require an FLiBeComposition instance."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    with pytest.raises(
        TypeError,
        match=(
            "composition must be an "
            "FLiBeComposition"
        ),
    ):
        wrapped.matches_composition(
            invalid_composition
        )


@pytest.mark.parametrize(
    "invalid_tolerance",
    (
        True,
        False,
        "0.1",
        None,
        (),
        [],
    ),
)
def test_composition_match_rejects_non_real_or_boolean_tolerance(
    invalid_tolerance,
) -> None:
    """Absolute tolerance must be a real non-Boolean number."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    with pytest.raises(
        TypeError,
        match=(
            "absolute_tolerance must be a real "
            "non-Boolean number"
        ),
    ):
        wrapped.matches_composition(
            eutectic_flibe_composition(),
            absolute_tolerance=invalid_tolerance,
        )


@pytest.mark.parametrize(
    "invalid_tolerance",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_composition_match_rejects_nonfinite_tolerance(
    invalid_tolerance: float,
) -> None:
    """Absolute tolerance must be finite."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    with pytest.raises(
        ValueError,
        match="absolute_tolerance must be finite",
    ):
        wrapped.matches_composition(
            eutectic_flibe_composition(),
            absolute_tolerance=invalid_tolerance,
        )


@pytest.mark.parametrize(
    "invalid_tolerance",
    (
        -1.0,
        -0.1,
        -1.0e-12,
    ),
)
def test_composition_match_rejects_negative_tolerance(
    invalid_tolerance: float,
) -> None:
    """Absolute tolerance must be nonnegative."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    with pytest.raises(
        ValueError,
        match=(
            "absolute_tolerance must be "
            "nonnegative"
        ),
    ):
        wrapped.matches_composition(
            eutectic_flibe_composition(),
            absolute_tolerance=invalid_tolerance,
        )


def test_composition_matching_does_not_modify_configuration() -> None:
    """Composition comparison must not mutate the underlying configuration."""

    configuration = _reference_configuration()

    original_species = configuration.species
    original_positions = configuration.positions

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    wrapped.matches_composition(
        eutectic_flibe_composition()
    )

    assert configuration.species == original_species
    assert configuration.positions == original_positions


def test_composition_extraction_does_not_modify_configuration() -> None:
    """Composition extraction must leave atomic data unchanged."""

    configuration = _reference_configuration()

    original_species = configuration.species
    original_positions = configuration.positions

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    wrapped.composition()

    assert configuration.species == original_species
    assert configuration.positions == original_positions


def test_configuration_geometry_is_preserved_exactly() -> None:
    """FLiBe wrapping must not transform atomic positions."""

    configuration = AtomicConfiguration(
        species=(
            "Li",
            "Be",
            "F",
            "F",
            "F",
        ),
        positions=(
            (
                0.25,
                -1.0,
                3.5,
            ),
            (
                2.0,
                4.0,
                -0.5,
            ),
            (
                1.0,
                1.0,
                1.0,
            ),
            (
                -2.0,
                3.0,
                5.0,
            ),
            (
                7.0,
                -4.0,
                2.0,
            ),
        ),
    )

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert (
        wrapped.configuration.positions
        == configuration.positions
    )


def test_periodic_metadata_is_preserved() -> None:
    """FLiBe wrapping must preserve periodic configuration metadata."""

    configuration = AtomicConfiguration(
        species=(
            "Li",
            "F",
        ),
        positions=(
            (
                0.0,
                0.0,
                0.0,
            ),
            (
                1.0,
                1.0,
                1.0,
            ),
        ),
        cell=(
            (
                10.0,
                0.0,
                0.0,
            ),
            (
                0.0,
                10.0,
                0.0,
            ),
            (
                0.0,
                0.0,
                10.0,
            ),
        ),
        periodic=(
            True,
            True,
            True,
        ),
    )

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert wrapped.configuration.cell == configuration.cell
    assert (
        wrapped.configuration.periodic
        == configuration.periodic
    )


def test_configuration_contract_does_not_require_periodicity() -> None:
    """FLiBe domain validation must accept nonperiodic configurations."""

    configuration = _reference_configuration()

    wrapped = FLiBeConfiguration(
        configuration=configuration
    )

    assert wrapped.configuration.periodic == (
        False,
        False,
        False,
    )


def test_species_count_total_equals_atom_count() -> None:
    """Canonical species counts must account for every atom exactly once."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    assert sum(
        count
        for _, count in wrapped.species_counts
    ) == wrapped.atom_count


def test_atomic_fraction_counts_are_derived_from_same_species_state() -> None:
    """Fractions and counts must describe the same discrete species state."""

    wrapped = FLiBeConfiguration(
        configuration=_reference_configuration()
    )

    counts = dict(
        wrapped.species_counts
    )
    fractions = dict(
        wrapped.atomic_fractions
    )

    for species in FLiBeSpecies:
        assert fractions[
            species
        ] == pytest.approx(
            counts[species]
            / wrapped.atom_count
        )
