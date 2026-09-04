"""Invariant tests for the TR-EIF FLiBe units and provenance contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.units import (
    FLiBeUnit,
    ParameterProvenance,
    PhysicalParameter,
    atomic_mass_parameter,
    density_parameter,
    pressure_parameter,
    temperature_parameter,
)


def test_unit_enum_contains_exact_supported_units() -> None:
    """FLiBe unit enumeration must contain the exact supported units."""

    assert tuple(
        unit.value
        for unit in FLiBeUnit
    ) == (
        "K",
        "Pa",
        "u",
        "kg/m^3",
    )


def test_unit_enum_contains_no_duplicate_values() -> None:
    """Every canonical unit identifier must occur exactly once."""

    values = tuple(
        unit.value
        for unit in FLiBeUnit
    )

    assert len(values) == len(set(values))


def test_provenance_enum_contains_exact_classes() -> None:
    """Parameter provenance must reproduce the TR-EIF provenance classes."""

    assert tuple(
        provenance.value
        for provenance in ParameterProvenance
    ) == (
        "PRIMARY_SOURCE",
        "DERIVED",
        "CALIBRATED",
        "AUTHOR_DEFINED",
        "BENCHMARK",
        "TEST_FIXTURE",
        "REQUIRES_SOURCE",
        "REQUIRES_TEST",
    )


def test_provenance_enum_contains_no_duplicate_values() -> None:
    """Every provenance identifier must occur exactly once."""

    values = tuple(
        provenance.value
        for provenance in ParameterProvenance
    )

    assert len(values) == len(set(values))


@pytest.mark.parametrize(
    "unit",
    tuple(FLiBeUnit),
)
def test_unit_members_are_string_compatible(
    unit: FLiBeUnit,
) -> None:
    """Canonical units must retain string-enum semantics."""

    assert isinstance(
        unit,
        str,
    )


@pytest.mark.parametrize(
    "provenance",
    tuple(ParameterProvenance),
)
def test_provenance_members_are_string_compatible(
    provenance: ParameterProvenance,
) -> None:
    """Provenance classes must retain string-enum semantics."""

    assert isinstance(
        provenance,
        str,
    )


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
def test_non_primary_provenance_allows_missing_source(
    provenance: ParameterProvenance,
) -> None:
    """Non-primary provenance classes may omit direct source metadata."""

    parameter = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=provenance,
    )

    assert parameter.source is None


def test_primary_source_requires_source_metadata() -> None:
    """PRIMARY_SOURCE provenance must carry explicit source metadata."""

    with pytest.raises(
        ValueError,
        match=(
            "PRIMARY_SOURCE provenance "
            "requires source"
        ),
    ):
        PhysicalParameter(
            value=1.0,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_source_accepts_nonempty_source() -> None:
    """PRIMARY_SOURCE provenance must accept explicit source metadata."""

    parameter = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="reference-record",
    )

    assert parameter.source == "reference-record"


def test_source_metadata_is_preserved_exactly() -> None:
    """Valid source metadata must not be silently rewritten."""

    parameter = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.PASCAL,
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert parameter.source == "derived-record"


def test_empty_source_is_rejected() -> None:
    """Explicit source metadata must not be empty."""

    with pytest.raises(
        ValueError,
        match="source must not be empty",
    ):
        PhysicalParameter(
            value=1.0,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.DERIVED,
            source="",
        )


@pytest.mark.parametrize(
    "source",
    (
        " source",
        "source ",
        "\tsource",
        "source\n",
    ),
)
def test_source_rejects_boundary_whitespace(
    source: str,
) -> None:
    """Source metadata must not contain boundary whitespace."""

    with pytest.raises(
        ValueError,
        match=(
            "source must not contain leading "
            "or trailing whitespace"
        ),
    ):
        PhysicalParameter(
            value=1.0,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


@pytest.mark.parametrize(
    "source",
    (
        True,
        False,
        1,
        1.0,
        (),
        [],
        {},
    ),
)
def test_source_requires_string_or_none(
    source,
) -> None:
    """Source metadata must be a string or None."""

    with pytest.raises(
        TypeError,
        match=(
            "source must be a string or None"
        ),
    ):
        PhysicalParameter(
            value=1.0,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


def test_parameter_preserves_valid_value() -> None:
    """Finite physical-parameter values must be retained."""

    parameter = PhysicalParameter(
        value=7.25,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 7.25


def test_integer_parameter_value_is_normalized_to_float() -> None:
    """Integer physical-parameter values must become floats."""

    parameter = PhysicalParameter(
        value=7,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 7.0
    assert isinstance(
        parameter.value,
        float,
    )


@pytest.mark.parametrize(
    "value",
    (
        -7.0,
        -0.25,
        0.0,
        0.25,
        7.0,
    ),
)
def test_generic_parameter_accepts_any_finite_real_value(
    value: float,
) -> None:
    """Generic unit boundary must not invent sign restrictions."""

    parameter = PhysicalParameter(
        value=value,
        unit=FLiBeUnit.PASCAL,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == value


@pytest.mark.parametrize(
    "invalid_value",
    (
        True,
        False,
        "1.0",
        None,
        (),
        [],
        {},
    ),
)
def test_parameter_rejects_non_real_or_boolean_values(
    invalid_value,
) -> None:
    """Physical-parameter value must be a real non-Boolean number."""

    with pytest.raises(
        TypeError,
        match=(
            "value must be a real "
            "non-Boolean number"
        ),
    ):
        PhysicalParameter(
            value=invalid_value,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_value",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_parameter_rejects_nonfinite_values(
    invalid_value: float,
) -> None:
    """Physical-parameter value must be finite."""

    with pytest.raises(
        ValueError,
        match="value must be finite",
    ):
        PhysicalParameter(
            value=invalid_value,
            unit=FLiBeUnit.KELVIN,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_unit",
    (
        "K",
        "Pa",
        "u",
        "kg/m^3",
        None,
        True,
        1,
        (),
    ),
)
def test_parameter_requires_unit_enum(
    invalid_unit,
) -> None:
    """Physical parameters must use explicit FLiBeUnit members."""

    with pytest.raises(
        TypeError,
        match="unit must be an FLiBeUnit",
    ):
        PhysicalParameter(
            value=1.0,
            unit=invalid_unit,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_provenance",
    (
        "PRIMARY_SOURCE",
        "DERIVED",
        "TEST_FIXTURE",
        None,
        True,
        1,
        (),
    ),
)
def test_parameter_requires_provenance_enum(
    invalid_provenance,
) -> None:
    """Physical parameters must use explicit provenance enum members."""

    with pytest.raises(
        TypeError,
        match=(
            "provenance must be a "
            "ParameterProvenance"
        ),
    ):
        PhysicalParameter(
            value=1.0,
            unit=FLiBeUnit.KELVIN,
            provenance=invalid_provenance,
        )


def test_physical_parameter_is_frozen() -> None:
    """Physical parameter records must be immutable."""

    parameter = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        FrozenInstanceError
    ):
        parameter.value = 2.0


def test_equal_parameters_compare_equal() -> None:
    """Equal value, unit, provenance, and source define equal records."""

    first = PhysicalParameter(
        value=4,
        unit=FLiBeUnit.PASCAL,
        provenance=ParameterProvenance.DERIVED,
        source="record",
    )

    second = PhysicalParameter(
        value=4.0,
        unit=FLiBeUnit.PASCAL,
        provenance=ParameterProvenance.DERIVED,
        source="record",
    )

    assert first == second


def test_different_units_define_different_parameters() -> None:
    """Equal numeric values with different units must remain distinct."""

    first = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    second = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.PASCAL,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert first != second


def test_different_provenance_defines_different_parameters() -> None:
    """Equal value and unit with different provenance remain distinct."""

    first = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.DERIVED,
    )

    second = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert first != second


def test_temperature_constructor_assigns_kelvin() -> None:
    """Temperature constructor must assign the Kelvin unit explicitly."""

    parameter = temperature_parameter(
        2.0,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 2.0
    assert parameter.unit is FLiBeUnit.KELVIN
    assert (
        parameter.provenance
        is ParameterProvenance.TEST_FIXTURE
    )


def test_pressure_constructor_assigns_pascal() -> None:
    """Pressure constructor must assign the Pascal unit explicitly."""

    parameter = pressure_parameter(
        3.0,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 3.0
    assert parameter.unit is FLiBeUnit.PASCAL


def test_atomic_mass_constructor_assigns_atomic_mass_unit() -> None:
    """Atomic-mass constructor must assign unified atomic mass units."""

    parameter = atomic_mass_parameter(
        5.0,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 5.0
    assert (
        parameter.unit
        is FLiBeUnit.ATOMIC_MASS_UNIT
    )


def test_density_constructor_assigns_density_unit() -> None:
    """Density constructor must assign kg/m^3 explicitly."""

    parameter = density_parameter(
        7.0,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 7.0
    assert (
        parameter.unit
        is FLiBeUnit.KILOGRAM_PER_CUBIC_METER
    )


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_preserve_provenance(
    constructor,
) -> None:
    """Typed constructors must preserve explicit provenance."""

    parameter = constructor(
        1.0,
        ParameterProvenance.AUTHOR_DEFINED,
    )

    assert (
        parameter.provenance
        is ParameterProvenance.AUTHOR_DEFINED
    )


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_preserve_source(
    constructor,
) -> None:
    """Typed constructors must preserve explicit source metadata."""

    parameter = constructor(
        1.0,
        ParameterProvenance.DERIVED,
        source="source-record",
    )

    assert parameter.source == "source-record"


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_enforce_primary_source_requirement(
    constructor,
) -> None:
    """Typed constructors must preserve PRIMARY_SOURCE validation."""

    with pytest.raises(
        ValueError,
        match=(
            "PRIMARY_SOURCE provenance "
            "requires source"
        ),
    ):
        constructor(
            1.0,
            ParameterProvenance.PRIMARY_SOURCE,
        )


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_accept_primary_source_metadata(
    constructor,
) -> None:
    """Typed constructors must accept sourced PRIMARY_SOURCE records."""

    parameter = constructor(
        1.0,
        ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert (
        parameter.provenance
        is ParameterProvenance.PRIMARY_SOURCE
    )
    assert parameter.source == "primary-record"


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_reject_nonfinite_values(
    constructor,
) -> None:
    """Typed constructors must preserve finite-value validation."""

    with pytest.raises(
        ValueError,
        match="value must be finite",
    ):
        constructor(
            float("nan"),
            ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "constructor",
    (
        temperature_parameter,
        pressure_parameter,
        atomic_mass_parameter,
        density_parameter,
    ),
)
def test_typed_constructors_normalize_integer_values(
    constructor,
) -> None:
    """Typed constructors must normalize integer values to floats."""

    parameter = constructor(
        4,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 4.0
    assert isinstance(
        parameter.value,
        float,
    )


def test_parameter_record_does_not_convert_units() -> None:
    """Unit attachment must not silently transform the numeric value."""

    parameter = PhysicalParameter(
        value=123.456,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == 123.456


def test_same_value_can_exist_in_distinct_unit_domains() -> None:
    """Unit semantics must remain explicit even for equal numeric values."""

    value = 9.0

    parameters = (
        temperature_parameter(
            value,
            ParameterProvenance.TEST_FIXTURE,
        ),
        pressure_parameter(
            value,
            ParameterProvenance.TEST_FIXTURE,
        ),
        atomic_mass_parameter(
            value,
            ParameterProvenance.TEST_FIXTURE,
        ),
        density_parameter(
            value,
            ParameterProvenance.TEST_FIXTURE,
        ),
    )

    assert tuple(
        parameter.value
        for parameter in parameters
    ) == (
        9.0,
        9.0,
        9.0,
        9.0,
    )

    assert len(
        {
            parameter.unit
            for parameter in parameters
        }
    ) == 4


def test_requires_source_is_not_primary_source() -> None:
    """REQUIRES_SOURCE must remain distinct from PRIMARY_SOURCE."""

    assert (
        ParameterProvenance.REQUIRES_SOURCE
        is not ParameterProvenance.PRIMARY_SOURCE
    )

    parameter = PhysicalParameter(
        value=1.0,
        unit=FLiBeUnit.KELVIN,
        provenance=ParameterProvenance.REQUIRES_SOURCE,
    )

    assert parameter.source is None


def test_requires_test_is_distinct_from_test_fixture() -> None:
    """REQUIRES_TEST must remain distinct from TEST_FIXTURE."""

    assert (
        ParameterProvenance.REQUIRES_TEST
        is not ParameterProvenance.TEST_FIXTURE
    )


def test_units_and_provenance_do_not_imply_physical_validity() -> None:
    """Metadata attachment alone must not create domain-validity claims."""

    parameter = temperature_parameter(
        -5.0,
        ParameterProvenance.TEST_FIXTURE,
    )

    assert parameter.value == -5.0
    assert parameter.unit is FLiBeUnit.KELVIN
