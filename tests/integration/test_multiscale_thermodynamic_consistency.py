"""Integration tests for the TR-EIF thermodynamic-consistency contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.thermodynamic_consistency import (
    ThermodynamicConsistencyContext,
    ThermodynamicConsistencyRecord,
    ThermodynamicVariable,
    evaluate_thermodynamic_consistency,
)


def _source_variables() -> tuple[ThermodynamicVariable, ...]:
    return (
        ThermodynamicVariable(
            variable_id="energy_density",
            value=5.0,
            unit="J/m^3",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        ),
        ThermodynamicVariable(
            variable_id="pressure",
            value=2.0,
            unit="Pa",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        ),
    )


def _target_variables() -> tuple[ThermodynamicVariable, ...]:
    return (
        ThermodynamicVariable(
            variable_id="energy_density",
            value=5.0,
            unit="J/m^3",
            scale_id="continuum",
            state_domain_id="state-b",
            source_id="source-b",
        ),
        ThermodynamicVariable(
            variable_id="pressure",
            value=2.0,
            unit="Pa",
            scale_id="continuum",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )


def _context() -> ThermodynamicConsistencyContext:
    return ThermodynamicConsistencyContext(
        relation_id="relation-a",
        model_id="model-a",
        assumptions_id="assumptions-a",
        normalization_id="normalization-a",
    )


def test_thermodynamic_variable_normalizes_identifiers_and_value() -> None:
    variable = ThermodynamicVariable(
        variable_id="  pressure ",
        value=2,
        unit=" Pa ",
        scale_id=" continuum ",
        state_domain_id=" state-a ",
        source_id=" source-a ",
    )

    assert variable.variable_id == "pressure"
    assert variable.value == 2.0
    assert isinstance(variable.value, float)
    assert variable.unit == "Pa"
    assert variable.scale_id == "continuum"
    assert variable.state_domain_id == "state-a"
    assert variable.source_id == "source-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "variable_id",
        "unit",
        "scale_id",
        "state_domain_id",
        "source_id",
    ),
)
def test_thermodynamic_variable_identifiers_must_be_strings(
    field_name: str,
) -> None:
    arguments: dict[str, object] = {
        "variable_id": "pressure",
        "value": 2.0,
        "unit": "Pa",
        "scale_id": "continuum",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        ThermodynamicVariable(
            **arguments
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "variable_id",
        "unit",
        "scale_id",
        "state_domain_id",
        "source_id",
    ),
)
@pytest.mark.parametrize(
    "value",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_thermodynamic_variable_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    arguments = {
        "variable_id": "pressure",
        "value": 2.0,
        "unit": "Pa",
        "scale_id": "continuum",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        ThermodynamicVariable(**arguments)


@pytest.mark.parametrize(
    ("value", "exception"),
    (
        (float("inf"), ValueError),
        (float("-inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("2.0", TypeError),
    ),
)
def test_thermodynamic_variable_value_must_be_finite_real(
    value: object,
    exception: type[Exception],
) -> None:
    with pytest.raises(exception):
        ThermodynamicVariable(
            variable_id="pressure",
            value=value,  # type: ignore[arg-type]
            unit="Pa",
            scale_id="continuum",
            state_domain_id="state-a",
            source_id="source-a",
        )


def test_thermodynamic_variable_contract_does_not_impose_sign_restriction(
) -> None:
    variable = ThermodynamicVariable(
        variable_id="signed_reference",
        value=-3.0,
        unit="arbitrary-unit",
        scale_id="scale-a",
        state_domain_id="state-a",
        source_id="source-a",
    )

    assert variable.value == -3.0


def test_context_normalizes_identifiers() -> None:
    context = ThermodynamicConsistencyContext(
        relation_id=" relation-a ",
        model_id=" model-a ",
        assumptions_id=" assumptions-a ",
        normalization_id=" normalization-a ",
    )

    assert context.relation_id == "relation-a"
    assert context.model_id == "model-a"
    assert context.assumptions_id == "assumptions-a"
    assert context.normalization_id == "normalization-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "relation_id",
        "model_id",
        "assumptions_id",
        "normalization_id",
    ),
)
def test_context_identifiers_must_be_strings(
    field_name: str,
) -> None:
    arguments: dict[str, object] = {
        "relation_id": "relation-a",
        "model_id": "model-a",
        "assumptions_id": "assumptions-a",
        "normalization_id": "normalization-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        ThermodynamicConsistencyContext(
            **arguments
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "relation_id",
        "model_id",
        "assumptions_id",
        "normalization_id",
    ),
)
def test_context_identifiers_must_not_be_empty(
    field_name: str,
) -> None:
    arguments = {
        "relation_id": "relation-a",
        "model_id": "model-a",
        "assumptions_id": "assumptions-a",
        "normalization_id": "normalization-a",
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        ThermodynamicConsistencyContext(**arguments)


def test_record_binds_explicit_inputs_and_validation_status() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()

    record = ThermodynamicConsistencyRecord(
        source_variables=source,
        target_variables=target,
        context=context,
        is_consistent=True,
        validation_id="validation-a",
    )

    assert record.source_variables is source
    assert record.target_variables is target
    assert record.context is context
    assert record.is_consistent is True
    assert record.validation_id == "validation-a"


@pytest.mark.parametrize(
    "status",
    (
        True,
        False,
    ),
)
def test_validation_status_is_explicit_boolean(
    status: bool,
) -> None:
    record = ThermodynamicConsistencyRecord(
        source_variables=_source_variables(),
        target_variables=_target_variables(),
        context=_context(),
        is_consistent=status,
        validation_id="validation-a",
    )

    assert record.is_consistent is status


@pytest.mark.parametrize(
    "status",
    (
        0,
        1,
        -1,
        None,
        "true",
    ),
)
def test_validation_status_does_not_accept_ternary_or_untyped_values(
    status: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="is_consistent must be a Boolean validation status",
    ):
        ThermodynamicConsistencyRecord(
            source_variables=_source_variables(),
            target_variables=_target_variables(),
            context=_context(),
            is_consistent=status,  # type: ignore[arg-type]
            validation_id="validation-a",
        )


def test_record_requires_context_type() -> None:
    with pytest.raises(
        TypeError,
        match=(
            "context must be a "
            "ThermodynamicConsistencyContext instance"
        ),
    ):
        ThermodynamicConsistencyRecord(
            source_variables=_source_variables(),
            target_variables=_target_variables(),
            context=None,  # type: ignore[arg-type]
            is_consistent=True,
            validation_id="validation-a",
        )


def test_validation_id_is_trimmed() -> None:
    record = ThermodynamicConsistencyRecord(
        source_variables=_source_variables(),
        target_variables=_target_variables(),
        context=_context(),
        is_consistent=True,
        validation_id="  validation-a ",
    )

    assert record.validation_id == "validation-a"


@pytest.mark.parametrize(
    "value",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_validation_id_must_not_be_empty(
    value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="validation_id must not be empty or whitespace",
    ):
        ThermodynamicConsistencyRecord(
            source_variables=_source_variables(),
            target_variables=_target_variables(),
            context=_context(),
            is_consistent=True,
            validation_id=value,
        )


def test_validation_id_must_be_string() -> None:
    with pytest.raises(
        TypeError,
        match="validation_id must be a string",
    ):
        ThermodynamicConsistencyRecord(
            source_variables=_source_variables(),
            target_variables=_target_variables(),
            context=_context(),
            is_consistent=True,
            validation_id=1,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "source_variables",
        "target_variables",
    ),
)
def test_variable_collections_must_be_tuples(
    field_name: str,
) -> None:
    arguments: dict[str, object] = {
        "source_variables": _source_variables(),
        "target_variables": _target_variables(),
        "context": _context(),
        "is_consistent": True,
        "validation_id": "validation-a",
    }
    arguments[field_name] = list(
        arguments[field_name]  # type: ignore[arg-type]
    )

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a tuple",
    ):
        ThermodynamicConsistencyRecord(
            **arguments
        )  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "source_variables",
        "target_variables",
    ),
)
def test_variable_collections_must_not_be_empty(
    field_name: str,
) -> None:
    arguments = {
        "source_variables": _source_variables(),
        "target_variables": _target_variables(),
        "context": _context(),
        "is_consistent": True,
        "validation_id": "validation-a",
    }
    arguments[field_name] = ()

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty",
    ):
        ThermodynamicConsistencyRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_variables",
        "target_variables",
    ),
)
def test_variable_collections_reject_wrong_element_type(
    field_name: str,
) -> None:
    arguments = {
        "source_variables": _source_variables(),
        "target_variables": _target_variables(),
        "context": _context(),
        "is_consistent": True,
        "validation_id": "validation-a",
    }
    arguments[field_name] = (None,)

    with pytest.raises(
        TypeError,
        match=(
            rf"{field_name}\[0\] must be a "
            "ThermodynamicVariable instance"
        ),
    ):
        ThermodynamicConsistencyRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_variables",
        "target_variables",
    ),
)
def test_variable_collections_reject_duplicate_scale_variable_pairs(
    field_name: str,
) -> None:
    duplicate = (
        ThermodynamicVariable(
            variable_id="pressure",
            value=1.0,
            unit="Pa",
            scale_id="continuum",
            state_domain_id="state-a",
            source_id="source-a",
        ),
        ThermodynamicVariable(
            variable_id="pressure",
            value=2.0,
            unit="Pa",
            scale_id="continuum",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )

    arguments = {
        "source_variables": _source_variables(),
        "target_variables": _target_variables(),
        "context": _context(),
        "is_consistent": True,
        "validation_id": "validation-a",
    }
    arguments[field_name] = duplicate

    with pytest.raises(
        ValueError,
        match=(
            rf"{field_name} must not contain duplicate "
            "scale_id/variable_id pairs"
        ),
    ):
        ThermodynamicConsistencyRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_variables",
        "target_variables",
    ),
)
def test_variable_collections_require_canonical_scale_name_order(
    field_name: str,
) -> None:
    arguments = {
        "source_variables": _source_variables(),
        "target_variables": _target_variables(),
        "context": _context(),
        "is_consistent": True,
        "validation_id": "validation-a",
    }
    arguments[field_name] = tuple(
        reversed(arguments[field_name])
    )

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must use canonical scale/name ordering",
    ):
        ThermodynamicConsistencyRecord(**arguments)


def test_evaluator_receives_all_explicit_inputs() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()
    observed: list[object] = []

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        observed.extend(
            (
                candidate_source,
                candidate_target,
                candidate_context,
            )
        )

        return ThermodynamicConsistencyRecord(
            source_variables=candidate_source,
            target_variables=candidate_target,
            context=candidate_context,
            is_consistent=True,
            validation_id="validation-a",
        )

    result = evaluate_thermodynamic_consistency(
        source,
        target,
        context,
        evaluator,
    )

    assert observed == [
        source,
        target,
        context,
    ]
    assert result.source_variables is source
    assert result.target_variables is target
    assert result.context is context


def test_evaluator_result_source_variables_must_match_input() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()

    different_source = (
        ThermodynamicVariable(
            variable_id="pressure",
            value=3.0,
            unit="Pa",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="different-source",
        ),
    )

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        del candidate_source

        return ThermodynamicConsistencyRecord(
            source_variables=different_source,
            target_variables=candidate_target,
            context=candidate_context,
            is_consistent=False,
            validation_id="validation-a",
        )

    with pytest.raises(
        ValueError,
        match="result source variables must match input",
    ):
        evaluate_thermodynamic_consistency(
            source,
            target,
            context,
            evaluator,
        )


def test_evaluator_result_target_variables_must_match_input() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()

    different_target = (
        ThermodynamicVariable(
            variable_id="pressure",
            value=4.0,
            unit="Pa",
            scale_id="continuum",
            state_domain_id="state-c",
            source_id="different-source",
        ),
    )

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        del candidate_target

        return ThermodynamicConsistencyRecord(
            source_variables=candidate_source,
            target_variables=different_target,
            context=candidate_context,
            is_consistent=False,
            validation_id="validation-a",
        )

    with pytest.raises(
        ValueError,
        match="result target variables must match input",
    ):
        evaluate_thermodynamic_consistency(
            source,
            target,
            context,
            evaluator,
        )


def test_evaluator_result_context_must_match_input() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()

    different_context = ThermodynamicConsistencyContext(
        relation_id="relation-b",
        model_id="model-a",
        assumptions_id="assumptions-a",
        normalization_id="normalization-a",
    )

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        del candidate_context

        return ThermodynamicConsistencyRecord(
            source_variables=candidate_source,
            target_variables=candidate_target,
            context=different_context,
            is_consistent=False,
            validation_id="validation-a",
        )

    with pytest.raises(
        ValueError,
        match="result context must match input context",
    ):
        evaluate_thermodynamic_consistency(
            source,
            target,
            context,
            evaluator,
        )


def test_evaluator_must_return_consistency_record() -> None:
    def evaluator(
        source: tuple[ThermodynamicVariable, ...],
        target: tuple[ThermodynamicVariable, ...],
        context: ThermodynamicConsistencyContext,
    ) -> object:
        del source, target, context
        return {
            "is_consistent": True,
        }

    with pytest.raises(
        TypeError,
        match=(
            "evaluator must return a "
            "ThermodynamicConsistencyRecord instance"
        ),
    ):
        evaluate_thermodynamic_consistency(
            _source_variables(),
            _target_variables(),
            _context(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_thermodynamic_consistency(
            _source_variables(),
            _target_variables(),
            _context(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_context_type() -> None:
    def evaluator(
        source: tuple[ThermodynamicVariable, ...],
        target: tuple[ThermodynamicVariable, ...],
        context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        raise AssertionError(
            "evaluator must not be called for invalid context input"
        )

    with pytest.raises(
        TypeError,
        match=(
            "context must be a "
            "ThermodynamicConsistencyContext instance"
        ),
    ):
        evaluate_thermodynamic_consistency(
            _source_variables(),
            _target_variables(),
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    source = _source_variables()
    target = _target_variables()
    context = _context()

    def evaluator(
        candidate_source: tuple[ThermodynamicVariable, ...],
        candidate_target: tuple[ThermodynamicVariable, ...],
        candidate_context: ThermodynamicConsistencyContext,
    ) -> ThermodynamicConsistencyRecord:
        return ThermodynamicConsistencyRecord(
            source_variables=candidate_source,
            target_variables=candidate_target,
            context=candidate_context,
            is_consistent=True,
            validation_id="validation-a",
        )

    first = evaluate_thermodynamic_consistency(
        source,
        target,
        context,
        evaluator,
    )
    second = evaluate_thermodynamic_consistency(
        source,
        target,
        context,
        evaluator,
    )

    assert first == second
