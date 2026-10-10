"""Integration tests for the TR-EIF uncertainty-propagation contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.uncertainty_propagation import (
    UncertaintyMeasure,
    UncertaintyPropagationContext,
    UncertaintyPropagationRecord,
    evaluate_uncertainty_propagation,
)


def _source_measures() -> tuple[UncertaintyMeasure, ...]:
    """Construct canonical deterministic source uncertainty measures."""

    return (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.2,
            unit="eV",
            representation_id="standard_deviation",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        ),
        UncertaintyMeasure(
            quantity_id="force",
            value=0.1,
            unit="eV/angstrom",
            representation_id="standard_deviation",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        ),
    )


def _context() -> UncertaintyPropagationContext:
    """Construct one explicit deterministic propagation context."""

    return UncertaintyPropagationContext(
        target_scale_id="mesoscale",
        propagation_id="propagation-a",
        assumptions_id="assumptions-a",
        correlation_id="correlation-a",
        normalization_id="normalization-a",
    )


def _target_measures() -> tuple[UncertaintyMeasure, ...]:
    """Construct canonical deterministic target uncertainty measures."""

    return (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.15,
            unit="eV",
            representation_id="standard_deviation",
            scale_id="mesoscale",
            state_domain_id="state-b",
            source_id="source-b",
        ),
        UncertaintyMeasure(
            quantity_id="force",
            value=0.08,
            unit="eV/angstrom",
            representation_id="standard_deviation",
            scale_id="mesoscale",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )


def test_uncertainty_measure_normalizes_identifiers_and_value() -> None:
    """Measure construction must normalize identifiers and accepted numerics."""

    measure = UncertaintyMeasure(
        quantity_id=" energy ",
        value=1,
        unit=" eV ",
        representation_id=" standard_deviation ",
        scale_id=" atomistic ",
        state_domain_id=" state-a ",
        source_id=" source-a ",
    )

    assert measure.quantity_id == "energy"
    assert measure.value == 1.0
    assert isinstance(measure.value, float)
    assert measure.unit == "eV"
    assert measure.representation_id == "standard_deviation"
    assert measure.scale_id == "atomistic"
    assert measure.state_domain_id == "state-a"
    assert measure.source_id == "source-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "quantity_id",
        "unit",
        "representation_id",
        "scale_id",
        "state_domain_id",
        "source_id",
    ),
)
def test_uncertainty_measure_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every measure identifier field must use the string contract."""

    arguments: dict[str, object] = {
        "quantity_id": "energy",
        "value": 0.2,
        "unit": "eV",
        "representation_id": "standard_deviation",
        "scale_id": "atomistic",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        UncertaintyMeasure(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "quantity_id",
        "unit",
        "representation_id",
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
def test_uncertainty_measure_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    """Every measure identifier must remain nonempty after normalization."""

    arguments = {
        "quantity_id": "energy",
        "value": 0.2,
        "unit": "eV",
        "representation_id": "standard_deviation",
        "scale_id": "atomistic",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        UncertaintyMeasure(**arguments)


@pytest.mark.parametrize(
    ("value", "exception"),
    (
        (-1.0, ValueError),
        (float("inf"), ValueError),
        (float("-inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("0.2", TypeError),
    ),
)
def test_uncertainty_value_must_be_nonnegative_finite_real(
    value: object,
    exception: type[Exception],
) -> None:
    """Uncertainty magnitudes must be nonnegative finite real values."""

    with pytest.raises(exception):
        UncertaintyMeasure(
            quantity_id="energy",
            value=value,  # type: ignore[arg-type]
            unit="eV",
            representation_id="standard_deviation",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        )


def test_zero_uncertainty_value_is_allowed() -> None:
    """The generic contract must permit an explicitly supplied zero magnitude."""

    measure = UncertaintyMeasure(
        quantity_id="energy",
        value=0.0,
        unit="eV",
        representation_id="standard_deviation",
        scale_id="atomistic",
        state_domain_id="state-a",
        source_id="source-a",
    )

    assert measure.value == 0.0


def test_propagation_context_normalizes_identifiers() -> None:
    """Propagation context identifiers must normalize surrounding whitespace."""

    context = UncertaintyPropagationContext(
        target_scale_id=" mesoscale ",
        propagation_id=" propagation-a ",
        assumptions_id=" assumptions-a ",
        correlation_id=" correlation-a ",
        normalization_id=" normalization-a ",
    )

    assert context.target_scale_id == "mesoscale"
    assert context.propagation_id == "propagation-a"
    assert context.assumptions_id == "assumptions-a"
    assert context.correlation_id == "correlation-a"
    assert context.normalization_id == "normalization-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "target_scale_id",
        "propagation_id",
        "assumptions_id",
        "correlation_id",
        "normalization_id",
    ),
)
def test_propagation_context_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every propagation-context identifier must use the string contract."""

    arguments: dict[str, object] = {
        "target_scale_id": "mesoscale",
        "propagation_id": "propagation-a",
        "assumptions_id": "assumptions-a",
        "correlation_id": "correlation-a",
        "normalization_id": "normalization-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        UncertaintyPropagationContext(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "target_scale_id",
        "propagation_id",
        "assumptions_id",
        "correlation_id",
        "normalization_id",
    ),
)
def test_propagation_context_identifiers_must_not_be_empty(
    field_name: str,
) -> None:
    """Every propagation-context identifier must remain nonempty."""

    arguments = {
        "target_scale_id": "mesoscale",
        "propagation_id": "propagation-a",
        "assumptions_id": "assumptions-a",
        "correlation_id": "correlation-a",
        "normalization_id": "normalization-a",
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        UncertaintyPropagationContext(**arguments)


def test_propagation_record_binds_explicit_inputs() -> None:
    """A propagation record must retain source, target, and context explicitly."""

    source = _source_measures()
    target = _target_measures()
    context = _context()

    record = UncertaintyPropagationRecord(
        source_measures=source,
        target_measures=target,
        context=context,
    )

    assert record.source_measures is source
    assert record.target_measures is target
    assert record.context is context


@pytest.mark.parametrize(
    "field_name",
    (
        "source_measures",
        "target_measures",
    ),
)
def test_measure_collections_must_be_tuples(
    field_name: str,
) -> None:
    """Uncertainty collections must preserve immutable tuple semantics."""

    arguments: dict[str, object] = {
        "source_measures": _source_measures(),
        "target_measures": _target_measures(),
        "context": _context(),
    }
    arguments[field_name] = list(arguments[field_name])  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a tuple",
    ):
        UncertaintyPropagationRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "source_measures",
        "target_measures",
    ),
)
def test_measure_collections_must_not_be_empty(
    field_name: str,
) -> None:
    """Source and target uncertainty collections must remain explicit."""

    arguments = {
        "source_measures": _source_measures(),
        "target_measures": _target_measures(),
        "context": _context(),
    }
    arguments[field_name] = ()

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty",
    ):
        UncertaintyPropagationRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_measures",
        "target_measures",
    ),
)
def test_measure_collections_reject_wrong_element_type(
    field_name: str,
) -> None:
    """Every collection entry must use the typed uncertainty measure."""

    arguments = {
        "source_measures": _source_measures(),
        "target_measures": _target_measures(),
        "context": _context(),
    }
    arguments[field_name] = (None,)

    with pytest.raises(
        TypeError,
        match=rf"{field_name}\[0\] must be an UncertaintyMeasure instance",
    ):
        UncertaintyPropagationRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_measures",
        "target_measures",
    ),
)
def test_measure_collections_reject_duplicate_uncertainty_identity(
    field_name: str,
) -> None:
    """Canonical measure identity must not be duplicated within a collection."""

    duplicate = (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.1,
            unit="eV",
            representation_id="standard_deviation",
            scale_id="mesoscale",
            state_domain_id="state-a",
            source_id="source-a",
        ),
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.2,
            unit="different-unit",
            representation_id="standard_deviation",
            scale_id="mesoscale",
            state_domain_id="state-b",
            source_id="source-a",
        ),
    )

    arguments = {
        "source_measures": _source_measures(),
        "target_measures": _target_measures(),
        "context": _context(),
    }
    arguments[field_name] = duplicate

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not contain duplicate uncertainty identities",
    ):
        UncertaintyPropagationRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_measures",
        "target_measures",
    ),
)
def test_measure_collections_require_canonical_order(
    field_name: str,
) -> None:
    """Uncertainty collections must use deterministic canonical ordering."""

    arguments = {
        "source_measures": _source_measures(),
        "target_measures": _target_measures(),
        "context": _context(),
    }
    arguments[field_name] = tuple(reversed(arguments[field_name]))

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must use canonical uncertainty ordering",
    ):
        UncertaintyPropagationRecord(**arguments)


def test_record_requires_propagation_context() -> None:
    """Propagation records must bind to the typed explicit context."""

    with pytest.raises(
        TypeError,
        match="context must be an UncertaintyPropagationContext instance",
    ):
        UncertaintyPropagationRecord(
            source_measures=_source_measures(),
            target_measures=_target_measures(),
            context=None,  # type: ignore[arg-type]
        )


def test_every_target_measure_must_use_declared_target_scale() -> None:
    """Target measures must be bound to the destination scale in context."""

    invalid_target = (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.15,
            unit="eV",
            representation_id="standard_deviation",
            scale_id="continuum",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )

    with pytest.raises(
        ValueError,
        match=r"target_measures\[0\] scale_id must match context target_scale_id",
    ):
        UncertaintyPropagationRecord(
            source_measures=_source_measures(),
            target_measures=invalid_target,
            context=_context(),
        )


def test_contract_does_not_require_source_and_target_representation_match() -> None:
    """Representation conversion remains explicit provider responsibility."""

    target = (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.0225,
            unit="eV^2",
            representation_id="variance",
            scale_id="mesoscale",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )

    record = UncertaintyPropagationRecord(
        source_measures=_source_measures(),
        target_measures=target,
        context=_context(),
    )

    assert record.source_measures[0].representation_id == "standard_deviation"
    assert record.target_measures[0].representation_id == "variance"


def test_contract_does_not_require_source_and_target_units_match() -> None:
    """Unit conversion remains explicit rather than inferred by the contract."""

    target = (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.015,
            unit="provider-unit",
            representation_id="standard_deviation",
            scale_id="mesoscale",
            state_domain_id="state-b",
            source_id="source-b",
        ),
    )

    record = UncertaintyPropagationRecord(
        source_measures=_source_measures(),
        target_measures=target,
        context=_context(),
    )

    assert record.target_measures[0].unit == "provider-unit"


def test_evaluator_receives_source_and_context_explicitly() -> None:
    """Evaluation must pass the complete declared propagation inputs."""

    source = _source_measures()
    context = _context()
    observed: list[object] = []

    def evaluator(
        candidate_source: tuple[UncertaintyMeasure, ...],
        candidate_context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        observed.extend((candidate_source, candidate_context))
        return UncertaintyPropagationRecord(
            source_measures=candidate_source,
            target_measures=_target_measures(),
            context=candidate_context,
        )

    result = evaluate_uncertainty_propagation(
        source,
        context,
        evaluator,
    )

    assert observed == [source, context]
    assert result.source_measures is source
    assert result.context is context
    assert result.target_measures == _target_measures()


def test_evaluator_result_source_measures_must_match_input() -> None:
    """A provider cannot replace the explicit source uncertainty collection."""

    source = _source_measures()
    context = _context()

    different_source = (
        UncertaintyMeasure(
            quantity_id="energy",
            value=0.3,
            unit="eV",
            representation_id="standard_deviation",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="different-source",
        ),
    )

    def evaluator(
        candidate_source: tuple[UncertaintyMeasure, ...],
        candidate_context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        del candidate_source

        return UncertaintyPropagationRecord(
            source_measures=different_source,
            target_measures=_target_measures(),
            context=candidate_context,
        )

    with pytest.raises(
        ValueError,
        match="result source measures must match input",
    ):
        evaluate_uncertainty_propagation(
            source,
            context,
            evaluator,
        )


def test_evaluator_result_context_must_match_input() -> None:
    """A provider cannot replace the explicit propagation assumptions."""

    source = _source_measures()
    context = _context()

    different_context = UncertaintyPropagationContext(
        target_scale_id="mesoscale",
        propagation_id="propagation-b",
        assumptions_id="assumptions-a",
        correlation_id="correlation-a",
        normalization_id="normalization-a",
    )

    def evaluator(
        candidate_source: tuple[UncertaintyMeasure, ...],
        candidate_context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        del candidate_context

        return UncertaintyPropagationRecord(
            source_measures=candidate_source,
            target_measures=_target_measures(),
            context=different_context,
        )

    with pytest.raises(
        ValueError,
        match="result context must match input context",
    ):
        evaluate_uncertainty_propagation(
            source,
            context,
            evaluator,
        )


def test_evaluator_must_return_propagation_record() -> None:
    """Provider output must satisfy the typed propagation-record boundary."""

    def evaluator(
        source: tuple[UncertaintyMeasure, ...],
        context: UncertaintyPropagationContext,
    ) -> object:
        del source, context
        return {"uncertainty": 0.1}

    with pytest.raises(
        TypeError,
        match="evaluator must return an UncertaintyPropagationRecord instance",
    ):
        evaluate_uncertainty_propagation(
            _source_measures(),
            _context(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    """Uncertainty propagation must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_uncertainty_propagation(
            _source_measures(),
            _context(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_propagation_context() -> None:
    """Evaluation context must satisfy the typed propagation boundary."""

    def evaluator(
        source: tuple[UncertaintyMeasure, ...],
        context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        raise AssertionError(
            "evaluator must not be called for invalid context input"
        )

    with pytest.raises(
        TypeError,
        match="context must be an UncertaintyPropagationContext instance",
    ):
        evaluate_uncertainty_propagation(
            _source_measures(),
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_validates_source_collection_before_provider() -> None:
    """Invalid source collections must fail before provider invocation."""

    called = False

    def evaluator(
        source: tuple[UncertaintyMeasure, ...],
        context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        nonlocal called
        called = True

        return UncertaintyPropagationRecord(
            source_measures=source,
            target_measures=_target_measures(),
            context=context,
        )

    with pytest.raises(
        ValueError,
        match="source_measures must use canonical uncertainty ordering",
    ):
        evaluate_uncertainty_propagation(
            tuple(reversed(_source_measures())),
            _context(),
            evaluator,
        )

    assert called is False


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated explicit propagation must preserve provider determinism."""

    source = _source_measures()
    context = _context()

    def evaluator(
        candidate_source: tuple[UncertaintyMeasure, ...],
        candidate_context: UncertaintyPropagationContext,
    ) -> UncertaintyPropagationRecord:
        return UncertaintyPropagationRecord(
            source_measures=candidate_source,
            target_measures=_target_measures(),
            context=candidate_context,
        )

    first = evaluate_uncertainty_propagation(
        source,
        context,
        evaluator,
    )
    second = evaluate_uncertainty_propagation(
        source,
        context,
        evaluator,
    )

    assert first == second
