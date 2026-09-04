"""Invariant tests for the TR-EIF FLiBe resonance-parameterization contract."""

from dataclasses import FrozenInstanceError

import pytest

from tr_eif.flibe.coordination import (
    FLiBeAtomCoordination,
    FLiBeCoordinationState,
)
from tr_eif.flibe.resonance_parameterization import (
    ConstantFLiBeResonanceParameters,
    FLiBeResonanceParameterization,
    evaluate_resonance_parameters,
)
from tr_eif.flibe.species import FLiBeSpecies
from tr_eif.flibe.units import ParameterProvenance
from tr_eif.resonance import PhaseDynamicsParameters


def _coordination() -> FLiBeCoordinationState:
    """Return one deterministic three-atom coordination state."""

    return FLiBeCoordinationState(
        atoms=(
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
                fluorine_neighbors=1,
            ),
            FLiBeAtomCoordination(
                atom_index=2,
                species=FLiBeSpecies.FLUORINE,
                lithium_neighbors=1,
                beryllium_neighbors=1,
                fluorine_neighbors=0,
            ),
        )
    )


def _parameters(
    coupling: tuple[float, ...] = (0.2, 0.3, 0.4),
    phase_lag: tuple[float, ...] = (0.1, 0.2, 0.3),
) -> PhaseDynamicsParameters:
    """Return deterministic test-only phase-dynamics parameters."""

    return PhaseDynamicsParameters(
        coupling=coupling,
        phase_lag=phase_lag,
    )


def _parameterization() -> FLiBeResonanceParameterization:
    """Return one deterministic coordination-dependent test parameterization."""

    return FLiBeResonanceParameterization(
        evaluator=lambda coordination: _parameters(
            coupling=tuple(
                float(atom.total_neighbors)
                for atom in coordination.atoms
            ),
            phase_lag=tuple(
                0.1 * float(atom.atom_index + 1)
                for atom in coordination.atoms
            ),
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def _constant_parameterization() -> ConstantFLiBeResonanceParameters:
    """Return one deterministic fixed test parameterization."""

    return ConstantFLiBeResonanceParameters(
        parameters=_parameters(),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )


def test_parameterization_preserves_evaluator() -> None:
    """Dynamic parameterization must retain the supplied evaluator."""

    evaluator = lambda coordination: _parameters()

    model = FLiBeResonanceParameterization(
        evaluator=evaluator,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    assert model.evaluator is evaluator


def test_parameterization_preserves_provenance_and_source() -> None:
    """Dynamic parameterization must retain provenance metadata exactly."""

    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: _parameters(),
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert model.provenance is ParameterProvenance.DERIVED
    assert model.source == "derived-record"


@pytest.mark.parametrize(
    "invalid_evaluator",
    (None, True, False, 1, 1.0, "evaluator", (), [], {}),
)
def test_parameterization_requires_callable_evaluator(
    invalid_evaluator,
) -> None:
    """Dynamic resonance parameterization must require a callable evaluator."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        FLiBeResonanceParameterization(
            evaluator=invalid_evaluator,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_provenance",
    (
        "TEST_FIXTURE",
        "PRIMARY_SOURCE",
        None,
        True,
        False,
        1,
        (),
    ),
)
def test_parameterization_requires_provenance_enum(
    invalid_provenance,
) -> None:
    """Dynamic parameterization provenance must use ParameterProvenance."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        FLiBeResonanceParameterization(
            evaluator=lambda coordination: _parameters(),
            provenance=invalid_provenance,
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
def test_non_primary_parameterization_allows_missing_source(
    provenance: ParameterProvenance,
) -> None:
    """Non-primary provenance classes may omit direct source metadata."""

    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: _parameters(),
        provenance=provenance,
    )

    assert model.source is None


def test_primary_parameterization_requires_source() -> None:
    """PRIMARY_SOURCE dynamic parameterization must carry source metadata."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        FLiBeResonanceParameterization(
            evaluator=lambda coordination: _parameters(),
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_parameterization_accepts_source() -> None:
    """PRIMARY_SOURCE dynamic parameterization must accept explicit metadata."""

    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: _parameters(),
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert model.source == "primary-record"


@pytest.mark.parametrize(
    ("source", "error", "message"),
    (
        ("", ValueError, "source must not be empty"),
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
            "\tsource",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (
            "source\n",
            ValueError,
            "source must not contain leading or trailing whitespace",
        ),
        (True, TypeError, "source must be a string or None"),
        (False, TypeError, "source must be a string or None"),
        (1, TypeError, "source must be a string or None"),
        (1.0, TypeError, "source must be a string or None"),
        ((), TypeError, "source must be a string or None"),
        ([], TypeError, "source must be a string or None"),
    ),
)
def test_parameterization_rejects_invalid_source_metadata(
    source,
    error,
    message: str,
) -> None:
    """Dynamic parameterization source metadata must satisfy its contract."""

    with pytest.raises(error, match=message):
        FLiBeResonanceParameterization(
            evaluator=lambda coordination: _parameters(),
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


def test_parameterization_evaluator_receives_supplied_coordination_once() -> None:
    """Evaluation must pass the supplied coordination state exactly once."""

    coordination = _coordination()
    observed: list[FLiBeCoordinationState] = []

    def evaluator(
        received: FLiBeCoordinationState,
    ) -> PhaseDynamicsParameters:
        observed.append(received)
        return _parameters()

    result = FLiBeResonanceParameterization(
        evaluator=evaluator,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(coordination)

    assert observed == [coordination]
    assert observed[0] is coordination
    assert result == _parameters()


def test_parameterization_returns_evaluator_parameters_unchanged() -> None:
    """Validated evaluator output must be returned without hidden rewriting."""

    expected = _parameters(
        coupling=(0.7, 0.8, 0.9),
        phase_lag=(-0.4, 0.0, 0.4),
    )

    result = FLiBeResonanceParameterization(
        evaluator=lambda coordination: expected,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(_coordination())

    assert result is expected


@pytest.mark.parametrize(
    "invalid_result",
    (
        None,
        True,
        False,
        1,
        1.0,
        "parameters",
        (),
        [],
        {},
    ),
)
def test_parameterization_requires_phase_dynamics_result(
    invalid_result,
) -> None:
    """Dynamic evaluator must return PhaseDynamicsParameters."""

    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: invalid_result,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        TypeError,
        match="evaluator must return PhaseDynamicsParameters",
    ):
        model.evaluate(_coordination())


@pytest.mark.parametrize(
    "oscillator_count",
    (1, 2, 4, 5),
)
def test_parameterization_rejects_parameter_count_mismatch(
    oscillator_count: int,
) -> None:
    """Parameter-vector size must match the FLiBe coordination atom count."""

    parameters = PhaseDynamicsParameters(
        coupling=tuple(0.5 for _ in range(oscillator_count)),
        phase_lag=tuple(0.1 for _ in range(oscillator_count)),
    )

    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: parameters,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        ValueError,
        match="oscillator_count does not match the parameter-vector size",
    ):
        model.evaluate(_coordination())


def test_parameterization_accepts_exact_atom_count() -> None:
    """Parameter-vector size equal to atom count must pass validation."""

    coordination = _coordination()
    parameters = _parameters()

    assert parameters.oscillator_count == coordination.atom_count

    result = FLiBeResonanceParameterization(
        evaluator=lambda received: parameters,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(coordination)

    assert result is parameters


@pytest.mark.parametrize(
    "invalid_coordination",
    (None, True, False, 1, 1.0, "coordination", (), [], {}),
)
def test_parameterization_requires_coordination_state(
    invalid_coordination,
) -> None:
    """Dynamic parameterization must require FLiBeCoordinationState input."""

    with pytest.raises(
        TypeError,
        match="coordination must be an FLiBeCoordinationState",
    ):
        _parameterization().evaluate(invalid_coordination)


def test_parameterization_is_frozen() -> None:
    """Dynamic resonance-parameterization records must be immutable."""

    model = _parameterization()

    with pytest.raises(FrozenInstanceError):
        model.source = "replacement"


def test_evaluator_explicitly_controls_coordination_dependence() -> None:
    """Coordination affects phase parameters only through the supplied evaluator."""

    coordination = _coordination()

    first = FLiBeResonanceParameterization(
        evaluator=lambda state: PhaseDynamicsParameters(
            coupling=tuple(
                float(atom.lithium_neighbors)
                for atom in state.atoms
            ),
            phase_lag=(0.0, 0.0, 0.0),
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(coordination)

    second = FLiBeResonanceParameterization(
        evaluator=lambda state: PhaseDynamicsParameters(
            coupling=tuple(
                float(atom.fluorine_neighbors)
                for atom in state.atoms
            ),
            phase_lag=(0.0, 0.0, 0.0),
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(coordination)

    assert first.coupling == (0.0, 1.0, 1.0)
    assert second.coupling == (1.0, 1.0, 0.0)
    assert first != second


def test_coordination_counts_are_not_automatically_copied_to_parameters() -> None:
    """The contract must not impose a hidden coordination-to-coupling formula."""

    expected = _parameters(
        coupling=(9.0, 8.0, 7.0),
        phase_lag=(0.6, 0.5, 0.4),
    )

    result = FLiBeResonanceParameterization(
        evaluator=lambda coordination: expected,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(_coordination())

    assert result is expected


def test_constant_parameterization_preserves_fields() -> None:
    """Constant parameterization must preserve parameters and metadata."""

    parameters = _parameters()
    model = ConstantFLiBeResonanceParameters(
        parameters=parameters,
        provenance=ParameterProvenance.DERIVED,
        source="derived-record",
    )

    assert model.parameters is parameters
    assert model.provenance is ParameterProvenance.DERIVED
    assert model.source == "derived-record"


@pytest.mark.parametrize(
    "invalid_parameters",
    (None, True, False, 1, 1.0, "parameters", (), [], {}),
)
def test_constant_parameterization_requires_phase_parameters(
    invalid_parameters,
) -> None:
    """Constant parameterization must require PhaseDynamicsParameters."""

    with pytest.raises(
        TypeError,
        match="parameters must be PhaseDynamicsParameters",
    ):
        ConstantFLiBeResonanceParameters(
            parameters=invalid_parameters,
            provenance=ParameterProvenance.TEST_FIXTURE,
        )


@pytest.mark.parametrize(
    "invalid_provenance",
    (
        "TEST_FIXTURE",
        "PRIMARY_SOURCE",
        None,
        True,
        False,
        1,
        (),
    ),
)
def test_constant_parameterization_requires_provenance_enum(
    invalid_provenance,
) -> None:
    """Constant parameterization provenance must use ParameterProvenance."""

    with pytest.raises(
        TypeError,
        match="provenance must be a ParameterProvenance",
    ):
        ConstantFLiBeResonanceParameters(
            parameters=_parameters(),
            provenance=invalid_provenance,
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
def test_non_primary_constant_parameterization_allows_missing_source(
    provenance: ParameterProvenance,
) -> None:
    """Non-primary fixed parameter sets may omit direct source metadata."""

    model = ConstantFLiBeResonanceParameters(
        parameters=_parameters(),
        provenance=provenance,
    )

    assert model.source is None


def test_primary_constant_parameterization_requires_source() -> None:
    """PRIMARY_SOURCE fixed parameter sets must carry source metadata."""

    with pytest.raises(
        ValueError,
        match="PRIMARY_SOURCE provenance requires source",
    ):
        ConstantFLiBeResonanceParameters(
            parameters=_parameters(),
            provenance=ParameterProvenance.PRIMARY_SOURCE,
        )


def test_primary_constant_parameterization_accepts_source() -> None:
    """PRIMARY_SOURCE fixed parameter sets must accept source metadata."""

    model = ConstantFLiBeResonanceParameters(
        parameters=_parameters(),
        provenance=ParameterProvenance.PRIMARY_SOURCE,
        source="primary-record",
    )

    assert model.source == "primary-record"


@pytest.mark.parametrize(
    ("source", "error", "message"),
    (
        ("", ValueError, "source must not be empty"),
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
        (True, TypeError, "source must be a string or None"),
        (1, TypeError, "source must be a string or None"),
        ((), TypeError, "source must be a string or None"),
    ),
)
def test_constant_parameterization_rejects_invalid_source_metadata(
    source,
    error,
    message: str,
) -> None:
    """Constant parameterization source metadata must satisfy its contract."""

    with pytest.raises(error, match=message):
        ConstantFLiBeResonanceParameters(
            parameters=_parameters(),
            provenance=ParameterProvenance.DERIVED,
            source=source,
        )


def test_constant_parameterization_returns_same_parameter_object() -> None:
    """Fixed parameterization must return its stored parameter object."""

    model = _constant_parameterization()
    result = model.evaluate(_coordination())

    assert result is model.parameters


@pytest.mark.parametrize(
    "invalid_coordination",
    (None, True, False, 1, 1.0, "coordination", (), [], {}),
)
def test_constant_parameterization_requires_coordination_state(
    invalid_coordination,
) -> None:
    """Fixed parameterization must require FLiBeCoordinationState input."""

    with pytest.raises(
        TypeError,
        match="coordination must be an FLiBeCoordinationState",
    ):
        _constant_parameterization().evaluate(invalid_coordination)


@pytest.mark.parametrize(
    "oscillator_count",
    (1, 2, 4, 5),
)
def test_constant_parameterization_rejects_atom_count_mismatch(
    oscillator_count: int,
) -> None:
    """Fixed phase-parameter vectors must match the coordination atom count."""

    model = ConstantFLiBeResonanceParameters(
        parameters=PhaseDynamicsParameters(
            coupling=tuple(0.5 for _ in range(oscillator_count)),
            phase_lag=tuple(0.1 for _ in range(oscillator_count)),
        ),
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    with pytest.raises(
        ValueError,
        match="oscillator_count does not match the parameter-vector size",
    ):
        model.evaluate(_coordination())


def test_constant_parameterization_is_frozen() -> None:
    """Constant resonance-parameterization records must be immutable."""

    model = _constant_parameterization()

    with pytest.raises(FrozenInstanceError):
        model.source = "replacement"


def test_constant_parameterization_does_not_depend_on_coordination_values() -> None:
    """Fixed parameters depend on atom-count compatibility, not coordination values."""

    first = _coordination()
    second = FLiBeCoordinationState(
        atoms=(
            FLiBeAtomCoordination(
                atom_index=0,
                species=FLiBeSpecies.LITHIUM,
                lithium_neighbors=9,
                beryllium_neighbors=8,
                fluorine_neighbors=7,
            ),
            FLiBeAtomCoordination(
                atom_index=1,
                species=FLiBeSpecies.BERYLLIUM,
                lithium_neighbors=6,
                beryllium_neighbors=5,
                fluorine_neighbors=4,
            ),
            FLiBeAtomCoordination(
                atom_index=2,
                species=FLiBeSpecies.FLUORINE,
                lithium_neighbors=3,
                beryllium_neighbors=2,
                fluorine_neighbors=1,
            ),
        )
    )

    model = _constant_parameterization()

    assert model.evaluate(first) is model.parameters
    assert model.evaluate(second) is model.parameters


@pytest.mark.parametrize(
    "model",
    (
        FLiBeResonanceParameterization(
            evaluator=lambda coordination: _parameters(),
            provenance=ParameterProvenance.TEST_FIXTURE,
        ),
        ConstantFLiBeResonanceParameters(
            parameters=_parameters(),
            provenance=ParameterProvenance.TEST_FIXTURE,
        ),
    ),
)
def test_public_evaluator_accepts_supported_models(model) -> None:
    """Public evaluation boundary must accept both supported model classes."""

    result = evaluate_resonance_parameters(
        model,
        _coordination(),
    )

    assert isinstance(result, PhaseDynamicsParameters)
    assert result.oscillator_count == 3


@pytest.mark.parametrize(
    "invalid_model",
    (
        None,
        True,
        False,
        1,
        1.0,
        "model",
        (),
        [],
        {},
        lambda coordination: _parameters(),
    ),
)
def test_public_evaluator_rejects_unsupported_models(
    invalid_model,
) -> None:
    """Public resonance evaluation must reject unsupported model objects."""

    with pytest.raises(
        TypeError,
        match=(
            "model must be an FLiBeResonanceParameterization "
            "or ConstantFLiBeResonanceParameters"
        ),
    ):
        evaluate_resonance_parameters(
            invalid_model,
            _coordination(),
        )


@pytest.mark.parametrize(
    "invalid_coordination",
    (None, True, False, 1, 1.0, "coordination", (), [], {}),
)
def test_public_evaluator_preserves_coordination_validation(
    invalid_coordination,
) -> None:
    """Public evaluation must preserve coordination-state type validation."""

    with pytest.raises(
        TypeError,
        match="coordination must be an FLiBeCoordinationState",
    ):
        evaluate_resonance_parameters(
            _parameterization(),
            invalid_coordination,
        )


def test_public_evaluator_preserves_dynamic_result_identity() -> None:
    """Public evaluation must not wrap or replace valid phase parameters."""

    expected = _parameters()
    model = FLiBeResonanceParameterization(
        evaluator=lambda coordination: expected,
        provenance=ParameterProvenance.TEST_FIXTURE,
    )

    result = evaluate_resonance_parameters(
        model,
        _coordination(),
    )

    assert result is expected


def test_phase_lag_sign_is_not_given_ternary_semantics() -> None:
    """Numeric phase-lag signs must remain continuous phase parameters."""

    parameters = _parameters(
        coupling=(1.0, 1.0, 1.0),
        phase_lag=(-1.0, 0.0, 1.0),
    )

    result = ConstantFLiBeResonanceParameters(
        parameters=parameters,
        provenance=ParameterProvenance.TEST_FIXTURE,
    ).evaluate(_coordination())

    assert result.phase_lag == (-1.0, 0.0, 1.0)
    assert all(type(value) is float for value in result.phase_lag)


def test_parameterization_returns_phase_parameters_not_coordination_state() -> None:
    """Coordination input and continuous phase-parameter output remain distinct."""

    result = _parameterization().evaluate(_coordination())

    assert isinstance(result, PhaseDynamicsParameters)
    assert not isinstance(result, FLiBeCoordinationState)


def test_parameterization_does_not_construct_oscillator_state() -> None:
    """The parameterization boundary returns parameters rather than phase state."""

    result = evaluate_resonance_parameters(
        _parameterization(),
        _coordination(),
    )

    assert hasattr(result, "coupling")
    assert hasattr(result, "phase_lag")
    assert not hasattr(result, "phases")
    assert not hasattr(result, "frequencies")
