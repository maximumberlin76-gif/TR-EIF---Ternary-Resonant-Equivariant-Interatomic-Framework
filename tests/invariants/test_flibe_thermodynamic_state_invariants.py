"""Invariant tests for the TR-EIF FLiBe thermodynamic-state contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.thermodynamic_state import (
    FLiBeThermodynamicState,
)


def _state() -> FLiBeThermodynamicState:
    """Return one deterministic test-only thermodynamic state."""

    return FLiBeThermodynamicState(
        temperature=2.0,
        pressure=3.0,
    )


def test_state_preserves_valid_values() -> None:
    """Valid finite thermodynamic parameters must be retained."""

    state = _state()

    assert state.temperature == 2.0
    assert state.pressure == 3.0


def test_integer_inputs_are_normalized_to_float() -> None:
    """Integer thermodynamic inputs must become floating-point values."""

    state = FLiBeThermodynamicState(
        temperature=2,
        pressure=3,
    )

    assert isinstance(
        state.temperature,
        float,
    )
    assert isinstance(
        state.pressure,
        float,
    )

    assert state.temperature == 2.0
    assert state.pressure == 3.0


def test_positive_fractional_temperature_is_allowed() -> None:
    """Any finite strictly positive temperature parameter is valid."""

    state = FLiBeThermodynamicState(
        temperature=0.125,
        pressure=1.0,
    )

    assert state.temperature == 0.125


def test_zero_pressure_is_allowed() -> None:
    """The structural pressure contract includes zero."""

    state = FLiBeThermodynamicState(
        temperature=1.0,
        pressure=0.0,
    )

    assert state.pressure == 0.0


def test_positive_pressure_is_allowed() -> None:
    """Any finite positive pressure parameter is valid."""

    state = FLiBeThermodynamicState(
        temperature=1.0,
        pressure=0.125,
    )

    assert state.pressure == 0.125


@pytest.mark.parametrize(
    "invalid_temperature",
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
def test_temperature_rejects_non_real_or_boolean_values(
    invalid_temperature,
) -> None:
    """Temperature must be a real non-Boolean number."""

    with pytest.raises(
        TypeError,
        match=(
            "temperature must be a real "
            "non-Boolean number"
        ),
    ):
        FLiBeThermodynamicState(
            temperature=invalid_temperature,
            pressure=1.0,
        )


@pytest.mark.parametrize(
    "invalid_temperature",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_temperature_rejects_nonfinite_values(
    invalid_temperature: float,
) -> None:
    """Temperature must be finite."""

    with pytest.raises(
        ValueError,
        match="temperature must be finite",
    ):
        FLiBeThermodynamicState(
            temperature=invalid_temperature,
            pressure=1.0,
        )


@pytest.mark.parametrize(
    "invalid_temperature",
    (
        0.0,
        -1.0,
        -0.125,
        -1.0e-12,
    ),
)
def test_temperature_rejects_nonpositive_values(
    invalid_temperature: float,
) -> None:
    """Temperature must be strictly positive."""

    with pytest.raises(
        ValueError,
        match="temperature must be positive",
    ):
        FLiBeThermodynamicState(
            temperature=invalid_temperature,
            pressure=1.0,
        )


@pytest.mark.parametrize(
    "invalid_pressure",
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
def test_pressure_rejects_non_real_or_boolean_values(
    invalid_pressure,
) -> None:
    """Pressure must be a real non-Boolean number."""

    with pytest.raises(
        TypeError,
        match=(
            "pressure must be a real "
            "non-Boolean number"
        ),
    ):
        FLiBeThermodynamicState(
            temperature=1.0,
            pressure=invalid_pressure,
        )


@pytest.mark.parametrize(
    "invalid_pressure",
    (
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_pressure_rejects_nonfinite_values(
    invalid_pressure: float,
) -> None:
    """Pressure must be finite."""

    with pytest.raises(
        ValueError,
        match="pressure must be finite",
    ):
        FLiBeThermodynamicState(
            temperature=1.0,
            pressure=invalid_pressure,
        )


@pytest.mark.parametrize(
    "invalid_pressure",
    (
        -1.0,
        -0.125,
        -1.0e-12,
    ),
)
def test_pressure_rejects_negative_values(
    invalid_pressure: float,
) -> None:
    """Pressure must be nonnegative."""

    with pytest.raises(
        ValueError,
        match="pressure must be nonnegative",
    ):
        FLiBeThermodynamicState(
            temperature=1.0,
            pressure=invalid_pressure,
        )


def test_with_temperature_replaces_only_temperature() -> None:
    """Temperature replacement must preserve pressure exactly."""

    original = _state()

    replaced = original.with_temperature(
        7.0
    )

    assert replaced.temperature == 7.0
    assert replaced.pressure == original.pressure


def test_with_temperature_returns_new_state() -> None:
    """Temperature replacement must not mutate the original state."""

    original = _state()

    replaced = original.with_temperature(
        7.0
    )

    assert replaced is not original
    assert original.temperature == 2.0
    assert original.pressure == 3.0


def test_with_temperature_applies_temperature_validation() -> None:
    """Temperature replacement must preserve constructor validation."""

    state = _state()

    with pytest.raises(
        ValueError,
        match="temperature must be positive",
    ):
        state.with_temperature(
            0.0
        )


def test_with_temperature_applies_type_validation() -> None:
    """Temperature replacement must reject invalid types."""

    state = _state()

    with pytest.raises(
        TypeError,
        match=(
            "temperature must be a real "
            "non-Boolean number"
        ),
    ):
        state.with_temperature(
            True
        )


def test_with_pressure_replaces_only_pressure() -> None:
    """Pressure replacement must preserve temperature exactly."""

    original = _state()

    replaced = original.with_pressure(
        7.0
    )

    assert replaced.temperature == original.temperature
    assert replaced.pressure == 7.0


def test_with_pressure_returns_new_state() -> None:
    """Pressure replacement must not mutate the original state."""

    original = _state()

    replaced = original.with_pressure(
        7.0
    )

    assert replaced is not original
    assert original.temperature == 2.0
    assert original.pressure == 3.0


def test_with_pressure_accepts_zero() -> None:
    """Pressure replacement must preserve the P >= 0 boundary."""

    state = _state()

    replaced = state.with_pressure(
        0.0
    )

    assert replaced.pressure == 0.0


def test_with_pressure_applies_pressure_validation() -> None:
    """Pressure replacement must reject negative values."""

    state = _state()

    with pytest.raises(
        ValueError,
        match="pressure must be nonnegative",
    ):
        state.with_pressure(
            -1.0
        )


def test_with_pressure_applies_type_validation() -> None:
    """Pressure replacement must reject invalid types."""

    state = _state()

    with pytest.raises(
        TypeError,
        match=(
            "pressure must be a real "
            "non-Boolean number"
        ),
    ):
        state.with_pressure(
            False
        )


def test_state_is_frozen() -> None:
    """Thermodynamic state must be immutable after construction."""

    state = _state()

    with pytest.raises(
        FrozenInstanceError
    ):
        state.temperature = 9.0


def test_equal_states_compare_equal() -> None:
    """Equal thermodynamic parameters must define equal states."""

    first = FLiBeThermodynamicState(
        temperature=2.0,
        pressure=3.0,
    )

    second = FLiBeThermodynamicState(
        temperature=2,
        pressure=3,
    )

    assert first == second


def test_temperature_change_changes_state_equality() -> None:
    """Different temperature parameters must define different states."""

    first = _state()

    second = first.with_temperature(
        4.0
    )

    assert first != second


def test_pressure_change_changes_state_equality() -> None:
    """Different pressure parameters must define different states."""

    first = _state()

    second = first.with_pressure(
        4.0
    )

    assert first != second


def test_replacement_chain_preserves_validation() -> None:
    """Sequential replacements must produce a valid independent state."""

    original = _state()

    replaced = (
        original
        .with_temperature(5.0)
        .with_pressure(8.0)
    )

    assert replaced == FLiBeThermodynamicState(
        temperature=5.0,
        pressure=8.0,
    )

    assert original == FLiBeThermodynamicState(
        temperature=2.0,
        pressure=3.0,
    )


def test_state_contract_does_not_impose_temperature_upper_bound() -> None:
    """Structural contract must not invent an unsourced upper bound."""

    state = FLiBeThermodynamicState(
        temperature=1.0e100,
        pressure=1.0,
    )

    assert state.temperature == 1.0e100


def test_state_contract_does_not_impose_pressure_upper_bound() -> None:
    """Structural contract must not invent an unsourced pressure bound."""

    state = FLiBeThermodynamicState(
        temperature=1.0,
        pressure=1.0e100,
    )

    assert state.pressure == 1.0e100


def test_temperature_and_pressure_are_independent_parameters() -> None:
    """Structural validation must not impose an unsourced T-P relation."""

    state = FLiBeThermodynamicState(
        temperature=17.0,
        pressure=23.0,
    )

    assert state.temperature == 17.0
    assert state.pressure == 23.0


def test_zero_pressure_does_not_change_temperature_contract() -> None:
    """Zero pressure must not alter independent temperature validation."""

    state = FLiBeThermodynamicState(
        temperature=4.0,
        pressure=0.0,
    )

    assert state.temperature == 4.0
    assert state.pressure == 0.0


def test_test_fixture_values_have_no_embedded_unit_conversion() -> None:
    """Stored parameters must remain exactly the supplied numeric values."""

    state = FLiBeThermodynamicState(
        temperature=11.25,
        pressure=7.75,
    )

    assert state.temperature == 11.25
    assert state.pressure == 7.75
