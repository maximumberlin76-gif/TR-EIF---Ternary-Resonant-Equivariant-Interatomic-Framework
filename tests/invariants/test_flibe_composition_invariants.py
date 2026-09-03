"""Invariant tests for the TR-EIF FLiBe composition model."""

import math

import pytest

from tr_eif.flibe.composition import (
    FLiBeComposition,
    eutectic_flibe_composition,
)


def test_composition_normalizes_formula_unit_fractions() -> None:
    """Formula-unit fractions must be normalized to unit total."""

    composition = FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )

    assert composition.lif_fraction == pytest.approx(
        2.0 / 3.0
    )
    assert composition.bef2_fraction == pytest.approx(
        1.0 / 3.0
    )


def test_normalized_formula_unit_fractions_sum_to_one() -> None:
    """Normalized LiF and BeF2 fractions must sum to one."""

    composition = FLiBeComposition(
        lif_fraction=7.0,
        bef2_fraction=3.0,
    )

    assert sum(
        composition.formula_unit_fractions
    ) == pytest.approx(1.0)


def test_already_normalized_composition_is_preserved() -> None:
    """Unit-total input retains the same normalized fractions."""

    composition = FLiBeComposition(
        lif_fraction=0.75,
        bef2_fraction=0.25,
    )

    assert composition.formula_unit_fractions == pytest.approx(
        (
            0.75,
            0.25,
        )
    )


def test_uniform_formula_unit_scaling_preserves_composition() -> None:
    """Uniform positive scaling of inputs must not change composition."""

    first = FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )

    second = FLiBeComposition(
        lif_fraction=20.0,
        bef2_fraction=10.0,
    )

    assert (
        first.formula_unit_fractions
        == pytest.approx(
            second.formula_unit_fractions
        )
    )


def test_pure_lif_endpoint_is_supported() -> None:
    """The LiF endpoint is a valid binary-domain composition."""

    composition = FLiBeComposition(
        lif_fraction=1.0,
        bef2_fraction=0.0,
    )

    assert composition.formula_unit_fractions == (
        1.0,
        0.0,
    )

    assert composition.atomic_fractions == (
        ("Li", 0.5),
        ("Be", 0.0),
        ("F", 0.5),
    )


def test_pure_bef2_endpoint_is_supported() -> None:
    """The BeF2 endpoint is a valid binary-domain composition."""

    composition = FLiBeComposition(
        lif_fraction=0.0,
        bef2_fraction=1.0,
    )

    assert composition.formula_unit_fractions == (
        0.0,
        1.0,
    )

    assert composition.atomic_fractions == (
        ("Li", 0.0),
        ("Be", 1.0 / 3.0),
        ("F", 2.0 / 3.0),
    )


def test_atomic_fractions_sum_to_one() -> None:
    """Li, Be, and F atomic fractions must form a normalized composition."""

    composition = FLiBeComposition(
        lif_fraction=5.0,
        bef2_fraction=4.0,
    )

    assert sum(
        fraction
        for _, fraction in composition.atomic_fractions
    ) == pytest.approx(1.0)


def test_atomic_fraction_species_order_is_canonical() -> None:
    """Atomic fractions must use the canonical Li, Be, F order."""

    composition = FLiBeComposition(
        lif_fraction=2.0,
        bef2_fraction=1.0,
    )

    assert tuple(
        species
        for species, _ in composition.atomic_fractions
    ) == (
        "Li",
        "Be",
        "F",
    )


def test_reference_composition_has_two_to_one_formula_unit_ratio() -> None:
    """Reference FLiBe must represent the 2 LiF : 1 BeF2 ratio."""

    composition = eutectic_flibe_composition()

    assert composition.lif_fraction == pytest.approx(
        2.0 / 3.0
    )
    assert composition.bef2_fraction == pytest.approx(
        1.0 / 3.0
    )

    assert (
        composition.lif_fraction
        / composition.bef2_fraction
    ) == pytest.approx(2.0)


def test_reference_atomic_fractions_match_two_one_four_ratio() -> None:
    """Reference composition must produce Li : Be : F = 2 : 1 : 4."""

    composition = eutectic_flibe_composition()

    fractions = dict(
        composition.atomic_fractions
    )

    assert fractions["Li"] == pytest.approx(
        2.0 / 7.0
    )
    assert fractions["Be"] == pytest.approx(
        1.0 / 7.0
    )
    assert fractions["F"] == pytest.approx(
        4.0 / 7.0
    )


def test_reference_atomic_amounts_match_two_one_four_ratio() -> None:
    """Three reference formula units must yield Li2BeF4 amounts."""

    composition = eutectic_flibe_composition()

    amounts = dict(
        composition.atomic_amounts(
            total_formula_units=3.0
        )
    )

    assert amounts == pytest.approx(
        {
            "Li": 2.0,
            "Be": 1.0,
            "F": 4.0,
        }
    )


def test_formula_unit_amounts_scale_normalized_composition() -> None:
    """Formula-unit amounts must scale normalized fractions linearly."""

    composition = FLiBeComposition(
        lif_fraction=3.0,
        bef2_fraction=2.0,
    )

    amounts = composition.formula_unit_amounts(
        total_formula_units=10.0
    )

    assert amounts == pytest.approx(
        (
            6.0,
            4.0,
        )
    )


def test_formula_unit_amounts_sum_to_requested_total() -> None:
    """Scaled formula-unit amounts must preserve the requested total."""

    composition = FLiBeComposition(
        lif_fraction=7.0,
        bef2_fraction=5.0,
    )

    amounts = composition.formula_unit_amounts(
        total_formula_units=19.0
    )

    assert sum(amounts) == pytest.approx(
        19.0
    )


def test_default_formula_unit_amount_is_one() -> None:
    """Default formula-unit amount must reproduce normalized fractions."""

    composition = FLiBeComposition(
        lif_fraction=4.0,
        bef2_fraction=1.0,
    )

    assert composition.formula_unit_amounts() == pytest.approx(
        composition.formula_unit_fractions
    )


def test_atomic_amounts_follow_formula_stoichiometry() -> None:
    """Atomic amounts must follow LiF and BeF2 stoichiometry."""

    composition = FLiBeComposition(
        lif_fraction=3.0,
        bef2_fraction=2.0,
    )

    formula_amounts = composition.formula_unit_amounts(
        total_formula_units=10.0
    )

    lif_amount, bef2_amount = formula_amounts

    atomic = dict(
        composition.atomic_amounts(
            total_formula_units=10.0
        )
    )

    assert atomic["Li"] == pytest.approx(
        lif_amount
    )
    assert atomic["Be"] == pytest.approx(
        bef2_amount
    )
    assert atomic["F"] == pytest.approx(
        lif_amount + 2.0 * bef2_amount
    )


def test_atomic_amount_species_order_is_canonical() -> None:
    """Atomic amounts must use the canonical Li, Be, F order."""

    composition = eutectic_flibe_composition()

    assert tuple(
        species
        for species, _ in composition.atomic_amounts()
    ) == (
        "Li",
        "Be",
        "F",
    )


def test_atomic_amounts_scale_linearly_with_formula_units() -> None:
    """Atomic amounts must scale linearly with formula-unit amount."""

    composition = eutectic_flibe_composition()

    first = dict(
        composition.atomic_amounts(
            total_formula_units=3.0
        )
    )

    second = dict(
        composition.atomic_amounts(
            total_formula_units=15.0
        )
    )

    for species in (
        "Li",
        "Be",
        "F",
    ):
        assert second[species] == pytest.approx(
            5.0 * first[species]
        )


def test_atomic_fractions_match_normalized_atomic_amounts() -> None:
    """Atomic fractions must equal normalized stoichiometric amounts."""

    composition = FLiBeComposition(
        lif_fraction=7.0,
        bef2_fraction=4.0,
    )

    amounts = dict(
        composition.atomic_amounts(
            total_formula_units=11.0
        )
    )

    total_atoms = sum(
        amounts.values()
    )

    fractions = dict(
        composition.atomic_fractions
    )

    for species in (
        "Li",
        "Be",
        "F",
    ):
        assert fractions[species] == pytest.approx(
            amounts[species] / total_atoms
        )


def test_lithium_fraction_matches_atomic_fraction_record() -> None:
    """Lithium property must agree with the atomic composition record."""

    composition = FLiBeComposition(
        lif_fraction=8.0,
        bef2_fraction=3.0,
    )

    assert composition.lithium_fraction == pytest.approx(
        dict(composition.atomic_fractions)["Li"]
    )


def test_beryllium_fraction_matches_atomic_fraction_record() -> None:
    """Beryllium property must agree with the atomic composition record."""

    composition = FLiBeComposition(
        lif_fraction=8.0,
        bef2_fraction=3.0,
    )

    assert composition.beryllium_fraction == pytest.approx(
        dict(composition.atomic_fractions)["Be"]
    )


def test_fluorine_fraction_matches_atomic_fraction_record() -> None:
    """Fluorine property must agree with the atomic composition record."""

    composition = FLiBeComposition(
        lif_fraction=8.0,
        bef2_fraction=3.0,
    )

    assert composition.fluorine_fraction == pytest.approx(
        dict(composition.atomic_fractions)["F"]
    )


@pytest.mark.parametrize(
    "field_name",
    (
        "lif_fraction",
        "bef2_fraction",
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
def test_composition_fraction_rejects_non_real_or_boolean_values(
    field_name: str,
    invalid_value,
) -> None:
    """Formula-unit fraction inputs require real non-Boolean values."""

    values = {
        "lif_fraction": 2.0,
        "bef2_fraction": 1.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        TypeError,
        match=(
            rf"{field_name} must be a real "
            "non-Boolean number"
        ),
    ):
        FLiBeComposition(
            **values
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "lif_fraction",
        "bef2_fraction",
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
def test_composition_fraction_rejects_nonfinite_values(
    field_name: str,
    invalid_value: float,
) -> None:
    """Formula-unit fractions must be finite."""

    values = {
        "lif_fraction": 2.0,
        "bef2_fraction": 1.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be finite",
    ):
        FLiBeComposition(
            **values
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "lif_fraction",
        "bef2_fraction",
    ),
)
@pytest.mark.parametrize(
    "invalid_value",
    (
        -1.0,
        -0.5,
        -1.0e-12,
    ),
)
def test_composition_fraction_rejects_negative_values(
    field_name: str,
    invalid_value: float,
) -> None:
    """Formula-unit fractions must be nonnegative."""

    values = {
        "lif_fraction": 2.0,
        "bef2_fraction": 1.0,
    }

    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be nonnegative",
    ):
        FLiBeComposition(
            **values
        )


def test_zero_total_composition_is_rejected() -> None:
    """At least one formula-unit component must have positive amount."""

    with pytest.raises(
        ValueError,
        match=(
            "FLiBe composition must contain a positive "
            "total formula-unit fraction"
        ),
    ):
        FLiBeComposition(
            lif_fraction=0.0,
            bef2_fraction=0.0,
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        True,
        False,
        "1.0",
        None,
        (),
    ),
)
def test_formula_unit_amount_rejects_non_real_or_boolean_values(
    invalid_total,
) -> None:
    """Formula-unit scaling requires a real non-Boolean value."""

    composition = eutectic_flibe_composition()

    with pytest.raises(
        TypeError,
        match=(
            "total_formula_units must be a real "
            "non-Boolean number"
        ),
    ):
        composition.formula_unit_amounts(
            invalid_total
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_formula_unit_amount_rejects_nonfinite_values(
    invalid_total: float,
) -> None:
    """Formula-unit scaling amount must be finite."""

    composition = eutectic_flibe_composition()

    with pytest.raises(
        ValueError,
        match="total_formula_units must be finite",
    ):
        composition.formula_unit_amounts(
            invalid_total
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        0.0,
        -1.0,
        -1.0e-12,
    ),
)
def test_formula_unit_amount_rejects_nonpositive_values(
    invalid_total: float,
) -> None:
    """Formula-unit scaling amount must be strictly positive."""

    composition = eutectic_flibe_composition()

    with pytest.raises(
        ValueError,
        match="total_formula_units must be positive",
    ):
        composition.formula_unit_amounts(
            invalid_total
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        True,
        False,
        "3.0",
        None,
    ),
)
def test_atomic_amounts_propagate_total_type_validation(
    invalid_total,
) -> None:
    """Atomic amount construction must preserve scaling type validation."""

    composition = eutectic_flibe_composition()

    with pytest.raises(TypeError):
        composition.atomic_amounts(
            invalid_total
        )


@pytest.mark.parametrize(
    "invalid_total",
    (
        0.0,
        -1.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_atomic_amounts_propagate_total_value_validation(
    invalid_total: float,
) -> None:
    """Atomic amount construction must preserve scaling value validation."""

    composition = eutectic_flibe_composition()

    with pytest.raises(ValueError):
        composition.atomic_amounts(
            invalid_total
        )


def test_integer_fraction_inputs_are_normalized_to_float() -> None:
    """Integer composition inputs must produce canonical float fractions."""

    composition = FLiBeComposition(
        lif_fraction=2,
        bef2_fraction=1,
    )

    assert isinstance(
        composition.lif_fraction,
        float,
    )
    assert isinstance(
        composition.bef2_fraction,
        float,
    )


def test_integer_formula_unit_amount_produces_float_amounts() -> None:
    """Integer scaling input must produce floating-point amounts."""

    composition = eutectic_flibe_composition()

    formula_amounts = composition.formula_unit_amounts(
        3
    )

    atomic_amounts = composition.atomic_amounts(
        3
    )

    assert all(
        isinstance(value, float)
        for value in formula_amounts
    )

    assert all(
        isinstance(value, float)
        for _, value in atomic_amounts
    )


def test_reference_constructor_returns_new_equal_compositions() -> None:
    """Reference constructor calls must return equal immutable values."""

    first = eutectic_flibe_composition()
    second = eutectic_flibe_composition()

    assert first == second
    assert first is not second


def test_reference_composition_values_are_finite() -> None:
    """All reference composition fractions and amounts must be finite."""

    composition = eutectic_flibe_composition()

    values = (
        composition.lif_fraction,
        composition.bef2_fraction,
        composition.lithium_fraction,
        composition.beryllium_fraction,
        composition.fluorine_fraction,
    )

    assert all(
        math.isfinite(value)
        for value in values
    )
