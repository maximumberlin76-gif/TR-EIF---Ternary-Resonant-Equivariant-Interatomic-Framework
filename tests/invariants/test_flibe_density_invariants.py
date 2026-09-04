"""Invariant tests for the TR-EIF FLiBe mass-density contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.density import (
    ConstantFLiBeDensity,
    FLiBeDensityModel,
    evaluate_density,
)
from tr_eif.flibe.thermodynamic_state import FLiBeThermodynamicState
from tr_eif.flibe.units import (
    FLiBeUnit,
    ParameterProvenance,
    PhysicalParameter,
    temperature_parameter,
)


def _state(
    temperature: float = 2.0,
    pressure: float = 3.0,
) -> FLiBeThermodynamicState:
    """Return one deterministic test-only thermodynamic state."""

    return FLiBeThermodynamicState(
        temperature=temperature,
        pressure=pressure,
    )


def _model() -> FLiBeDensityModel:
    """Return one deterministic state-dependent test density model."""

    return FLiBeDensityModel(
        evaluator=lambda state: state.temperature + state.pressure,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _constant_model() -> ConstantFLiBeDensity:
    """Return one deterministic constant test density model."""

    return ConstantFLiBeDensity(
        density=5.0,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def test_density_model_preserves_metadata() -> None:
    """Model construction must retain evaluator, provenance, and source."""

    evaluator = lambda state: state.temperature
    model = FLiBeDensityModel(
        evaluator=evaluator,
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert model.evaluator is evaluator
    assert model.provenance is ParameterProvenance.DERIVED
    assert model.source == "derived-record"


def test_density_model_allows_missing_non_primary_source() -> None:
    """Non-primary provenance may omit direct source metadata."""

    assert _model().source is None


@pytest.mark.parametrize(
    "invalid_evaluator",
    (None, True, False, 1, 1.0, "evaluator", (), {}),
)
def test_density_model_requires_callable_evaluator(
    invalid_evaluator,
) -> None:
    """Density-model evaluator must be callable."""

    with pytest.raises(TypeError, match="evaluator must be callable"):
        FLiBeDensityModel(
            evaluator=invalid_evaluator,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_provenance",
    ("TEST_FIXTURE", None, True, 1, ()),
)
def test_density_model_requires_provenance_enum(
    invalid_provenance,
) -> None:
    """Density-model provenance must use ParameterProvenance."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        FLiBeDensityModel(
            evaluator=lambda state: 1.0,
            provenance=invalid_provenance,
        )


def test_density_model_primary_source_requires_source() -> None:
    """PRIMARY_SOURCE density models must carry source metadata."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        FLiBeDensityModel(
            evaluator=lambda state: 1.0,
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_density_model_primary_source_accepts_source() -> None:
    """PRIMARY_SOURCE density models must accept source metadata."""

    model = FLiBeDensityModel(
        evaluator=lambda state: 1.0,
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert model.source == "primary-record"


@pytest.mark.parametrize(
    ("source", "error", "message"),
    (
        ("", ValueError, "source must not be empty"),
        (" source", ValueError, "source must not contain leading or trailing whitespace"),
        ("source ", ValueError, "source must not contain leading or trailing whitespace"),
        ("\tsource", ValueError, "source must not contain leading or trailing whitespace"),
        ("source\n", ValueError, "source must not contain leading or trailing whitespace"),
        (True, TypeError, "source must be a string or None"),
        (1, TypeError, "source must be a string or None"),
        (1.0, TypeError, "source must be a string or None"),
        ((), TypeError, "source must be a string or None"),
    ),
)
def test_density_model_rejects_invalid_source_metadata(
    source,
    error,
    message: str,
) -> None:
    """Density-model source metadata must satisfy the units-layer contract."""

    with pytest.raises(error, match=message):
        FLiBeDensityModel(
            evaluator=lambda state: 1.0,
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


def test_density_model_evaluates_explicit_state_once() -> None:
    """Evaluation must pass the supplied state to the evaluator exactly once."""

    state = _state()
    observed = []

    def evaluator(received: FLiBeThermodynamicState) -> float:
        observed.append(received)
        return received.temperature + received.pressure

    result = FLiBeDensityModel(
        evaluator=evaluator,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(state)

    assert observed == [state]
    assert observed[0] is state
    assert result.value == 5.0


def test_density_model_returns_explicit_density_parameter() -> None:
    """Evaluation must return value, density unit, provenance, and source."""

    result = FLiBeDensityModel(
        evaluator=lambda state: 8,
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    ).evaluate(_state())

    assert result == PhysicalParameter(
        value=8.0,
        unit=FLiBeUnit.KILOGRAM_PER_CUBIC_METER,
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )
    assert isinstance(result.value, float)


@pytest.mark.parametrize(
    "invalid_value",
    (True, False, "1.0", None, (), [], {}),
)
def test_density_model_rejects_non_real_or_boolean_result(
    invalid_value,
) -> None:
    """Density evaluator output must be a real non-Boolean number."""

    model = FLiBeDensityModel(
        evaluator=lambda state: invalid_value,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        TypeError,
        match="density must be a real non-Boolean number",
    ):
        model.evaluate(_state())


@pytest.mark.parametrize(
    "invalid_value",
    (float("nan"), float("inf"), float("-inf")),
)
def test_density_model_rejects_nonfinite_result(
    invalid_value: float,
) -> None:
    """Density evaluator output must be finite."""

    model = FLiBeDensityModel(
        evaluator=lambda state: invalid_value,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(ValueError, match="density must be finite"):
        model.evaluate(_state())


@pytest.mark.parametrize(
    "invalid_value",
    (0.0, -1.0, -0.125, -1.0e-12),
)
def test_density_model_rejects_nonpositive_result(
    invalid_value: float,
) -> None:
    """Density evaluator output must be strictly positive."""

    model = FLiBeDensityModel(
        evaluator=lambda state: invalid_value,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(ValueError, match="density must be positive"):
        model.evaluate(_state())


@pytest.mark.parametrize(
    "invalid_state",
    (None, True, False, 1, 1.0, (), {}),
)
def test_density_model_requires_thermodynamic_state(
    invalid_state,
) -> None:
    """Density-model evaluation must require FLiBeThermodynamicState."""

    with pytest.raises(
        TypeError,
        match="state must be an FLiBeThermodynamicState",
    ):
        _model().evaluate(invalid_state)


def test_density_model_is_frozen() -> None:
    """Density-model records must be immutable after construction."""

    model = _model()

    with pytest.raises(FrozenInstanceError):
        model.source = "replacement"


def test_constant_density_preserves_and_normalizes_value() -> None:
    """Constant-density construction must normalize a valid integer value."""

    model = ConstantFLiBeDensity(
        density=7,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert model.density == 7.0
    assert isinstance(model.density, float)


@pytest.mark.parametrize(
    "invalid_density",
    (True, False, "1.0", None, (), [], {}),
)
def test_constant_density_rejects_non_real_or_boolean_values(
    invalid_density,
) -> None:
    """Constant density must be a real non-Boolean number."""

    with pytest.raises(
        TypeError,
        match="density must be a real non-Boolean number",
    ):
        ConstantFLiBeDensity(
            density=invalid_density,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_density",
    (float("nan"), float("inf"), float("-inf")),
)
def test_constant_density_rejects_nonfinite_values(
    invalid_density: float,
) -> None:
    """Constant density must be finite."""

    with pytest.raises(ValueError, match="density must be finite"):
        ConstantFLiBeDensity(
            density=invalid_density,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_density",
    (0.0, -1.0, -0.125, -1.0e-12),
)
def test_constant_density_rejects_nonpositive_values(
    invalid_density: float,
) -> None:
    """Constant density must be strictly positive."""

    with pytest.raises(ValueError, match="density must be positive"):
        ConstantFLiBeDensity(
            density=invalid_density,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


def test_constant_density_primary_source_requires_source() -> None:
    """PRIMARY_SOURCE constant models must carry source metadata."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        ConstantFLiBeDensity(
            density=1.0,
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_constant_density_preserves_source() -> None:
    """Constant-density model must preserve explicit source metadata."""

    model = ConstantFLiBeDensity(
        density=1.0,
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert model.source == "primary-record"


def test_constant_density_is_independent_of_state_values() -> None:
    """Constant-density model must return one value for all valid states."""

    model = _constant_model()
    first = model.evaluate(_state(1.0, 0.0))
    second = model.evaluate(_state(9.0, 8.0))

    assert first.value == 5.0
    assert second.value == 5.0
    assert first.unit is FLiBeUnit.KILOGRAM_PER_CUBIC_METER
    assert second.unit is FLiBeUnit.KILOGRAM_PER_CUBIC_METER


@pytest.mark.parametrize(
    "invalid_state",
    (None, True, False, 1, 1.0, (), {}),
)
def test_constant_density_requires_thermodynamic_state(
    invalid_state,
) -> None:
    """Constant-density evaluation must still require a valid state type."""

    with pytest.raises(
        TypeError,
        match="state must be an FLiBeThermodynamicState",
    ):
        _constant_model().evaluate(invalid_state)


def test_constant_density_is_frozen() -> None:
    """Constant-density model records must be immutable."""

    model = _constant_model()

    with pytest.raises(FrozenInstanceError):
        model.density = 9.0


@pytest.mark.parametrize(
    "model",
    (
        FLiBeDensityModel(
            evaluator=lambda state: 6.0,
            provenance=ParameterProvenance.TEST_FIXTURE,
        ),
        ConstantFLiBeDensity(
            density=6.0,
            provenance=ParameterProvenance.TEST_FIXTURE,
        ),
    ),
)
def test_evaluate_density_accepts_supported_models(model) -> None:
    """Public density evaluation must accept both supported model classes."""

    result = evaluate_density(model, _state())

    assert result.value == 6.0
    assert result.unit is FLiBeUnit.KILOGRAM_PER_CUBIC_METER


@pytest.mark.parametrize(
    "invalid_model",
    (None, True, False, 1, 1.0, (), {}, lambda state: 1.0),
)
def test_evaluate_density_rejects_unsupported_models(
    invalid_model,
) -> None:
    """Public density evaluation must reject unsupported model objects."""

    with pytest.raises(
        TypeError,
        match="model must be an FLiBeDensityModel or ConstantFLiBeDensity",
    ):
        evaluate_density(invalid_model, _state())


def test_evaluate_density_propagates_state_validation() -> None:
    """Public density evaluation must preserve state-type validation."""

    with pytest.raises(
        TypeError,
        match="state must be an FLiBeThermodynamicState",
    ):
        evaluate_density(_model(), None)


def test_evaluate_density_rejects_wrong_output_unit() -> None:
    """Public evaluation must reject a supported model returning another unit."""

    class WrongUnitDensityModel(FLiBeDensityModel):
        def evaluate(
            self,
            state: FLiBeThermodynamicState,
        ) -> PhysicalParameter:
            if not isinstance(state, FLiBeThermodynamicState):
                raise TypeError(
                    "state must be an FLiBeThermodynamicState."
                )

            return temperature_parameter(
                1.0,
                ParameterProvenance.TEST_FIXTURE,
            )

    model = WrongUnitDensityModel(
        evaluator=lambda state: 1.0,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        ValueError,
        match=r"density model must return kg/m\^3",
    ):
        evaluate_density(model, _state())


def test_state_dependence_is_defined_only_by_supplied_evaluator() -> None:
    """The density contract must not inject an empirical T-P relation."""

    model = FLiBeDensityModel(
        evaluator=lambda state: (
            100.0
            - state.temperature
            + 2.0 * state.pressure
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert model.evaluate(_state(25.0, 0.0)).value == 75.0
    assert model.evaluate(_state(25.0, 4.0)).value == 83.0


def test_density_value_has_no_ternary_state_semantics() -> None:
    """Numeric density values must remain distinct from ternary state labels."""

    result = ConstantFLiBeDensity(
        density=1.0,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(_state())

    assert result.value == 1.0
    assert result.unit is FLiBeUnit.KILOGRAM_PER_CUBIC_METER
