"""Integration tests for the TR-EIF engineering-boundary contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.continuum_closure import (
    ContinuumClosureRecord,
    ContinuumClosureVariable,
)
from tr_eif.multiscale.engineering_boundary import (
    EngineeringBoundaryCondition,
    EngineeringBoundaryContext,
    EngineeringBoundaryRecord,
    evaluate_engineering_boundaries,
)
from tr_eif.multiscale.mesoscale_closure import (
    MesoscaleClosureRecord,
    MesoscaleClosureVariable,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.state import CoarseScaleState


def _coarse_state() -> CoarseScaleState:
    """Construct a deterministic coarse-scale state."""

    return CoarseScaleState(
        partition=MultiscalePartition(
            fine_to_coarse=(0, 0, 1, 1),
        ),
        positions=(
            (0.5, 0.0, 0.0),
            (2.5, 0.0, 0.0),
        ),
        masses=(2.0, 4.0),
    )


def _mesoscale() -> MesoscaleClosureRecord:
    """Construct a deterministic mesoscale closure."""

    return MesoscaleClosureRecord(
        state=_coarse_state(),
        closure_id="mesoscale-a",
        source_id="source-m",
        closure_variables=(
            MesoscaleClosureVariable(
                name="flux",
                values=(1.0, -1.0),
            ),
        ),
    )


def _continuum() -> ContinuumClosureRecord:
    """Construct a deterministic continuum closure."""

    return ContinuumClosureRecord(
        mesoscale=_mesoscale(),
        closure_id="continuum-a",
        source_id="source-c",
        continuum_variables=(
            ContinuumClosureVariable(
                name="field_a",
                values=(1.0, 2.0),
            ),
        ),
    )


def _context() -> EngineeringBoundaryContext:
    """Construct one explicit engineering-boundary context."""

    return EngineeringBoundaryContext(
        engineering_model_id="engineering-model-a",
        geometry_id="geometry-a",
        mapping_id="mapping-a",
        assumptions_id="assumptions-a",
    )


def _conditions() -> tuple[EngineeringBoundaryCondition, ...]:
    """Construct canonical deterministic engineering boundary conditions."""

    return (
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field_a",
            condition_id="condition-a",
            values=(1.0, 2.0),
            unit="unit-a",
            source_id="source-a",
        ),
        EngineeringBoundaryCondition(
            boundary_id="boundary-b",
            variable_id="field_b",
            condition_id="condition-b",
            values=(-1.0,),
            unit="unit-b",
            source_id="source-b",
        ),
    )


def test_boundary_condition_normalizes_identifiers_and_values() -> None:
    """Boundary construction must normalize identifiers and numeric values."""

    condition = EngineeringBoundaryCondition(
        boundary_id=" boundary-a ",
        variable_id=" field-a ",
        condition_id=" condition-a ",
        values=(1, -2.5),
        unit=" unit-a ",
        source_id=" source-a ",
    )

    assert condition.boundary_id == "boundary-a"
    assert condition.variable_id == "field-a"
    assert condition.condition_id == "condition-a"
    assert condition.values == (1.0, -2.5)
    assert condition.unit == "unit-a"
    assert condition.source_id == "source-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "boundary_id",
        "variable_id",
        "condition_id",
        "unit",
        "source_id",
    ),
)
def test_boundary_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every boundary identifier field must use the string contract."""

    arguments: dict[str, object] = {
        "boundary_id": "boundary-a",
        "variable_id": "field-a",
        "condition_id": "condition-a",
        "values": (1.0,),
        "unit": "unit-a",
        "source_id": "source-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        EngineeringBoundaryCondition(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "boundary_id",
        "variable_id",
        "condition_id",
        "unit",
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
def test_boundary_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    """Every boundary identifier must remain nonempty after normalization."""

    arguments = {
        "boundary_id": "boundary-a",
        "variable_id": "field-a",
        "condition_id": "condition-a",
        "values": (1.0,),
        "unit": "unit-a",
        "source_id": "source-a",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        EngineeringBoundaryCondition(**arguments)


def test_boundary_values_must_be_tuple() -> None:
    """Boundary values must preserve immutable tuple semantics."""

    with pytest.raises(
        TypeError,
        match="values must be a tuple",
    ):
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field-a",
            condition_id="condition-a",
            values=[1.0],  # type: ignore[arg-type]
            unit="unit-a",
            source_id="source-a",
        )


def test_boundary_values_must_not_be_empty() -> None:
    """One boundary condition must carry at least one explicit value."""

    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field-a",
            condition_id="condition-a",
            values=(),
            unit="unit-a",
            source_id="source-a",
        )


@pytest.mark.parametrize(
    ("value", "exception"),
    (
        (True, TypeError),
        ("1.0", TypeError),
        (float("inf"), ValueError),
        (float("-inf"), ValueError),
        (float("nan"), ValueError),
    ),
)
def test_boundary_values_must_be_finite_reals(
    value: object,
    exception: type[Exception],
) -> None:
    """Boundary values must be finite real scalars."""

    with pytest.raises(exception):
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field-a",
            condition_id="condition-a",
            values=(value,),  # type: ignore[arg-type]
            unit="unit-a",
            source_id="source-a",
        )


def test_boundary_contract_does_not_infer_condition_type() -> None:
    """Condition identifiers remain caller-defined rather than enumerated."""

    condition = EngineeringBoundaryCondition(
        boundary_id="surface-a",
        variable_id="field-a",
        condition_id="provider-defined-condition",
        values=(1.0,),
        unit="unit-a",
        source_id="source-a",
    )

    assert condition.condition_id == "provider-defined-condition"


def test_context_normalizes_identifiers() -> None:
    """Engineering context identifiers must normalize surrounding whitespace."""

    context = EngineeringBoundaryContext(
        engineering_model_id=" model-a ",
        geometry_id=" geometry-a ",
        mapping_id=" mapping-a ",
        assumptions_id=" assumptions-a ",
    )

    assert context.engineering_model_id == "model-a"
    assert context.geometry_id == "geometry-a"
    assert context.mapping_id == "mapping-a"
    assert context.assumptions_id == "assumptions-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "engineering_model_id",
        "geometry_id",
        "mapping_id",
        "assumptions_id",
    ),
)
def test_context_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every engineering-context identifier must use the string contract."""

    arguments: dict[str, object] = {
        "engineering_model_id": "model-a",
        "geometry_id": "geometry-a",
        "mapping_id": "mapping-a",
        "assumptions_id": "assumptions-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        EngineeringBoundaryContext(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "engineering_model_id",
        "geometry_id",
        "mapping_id",
        "assumptions_id",
    ),
)
def test_context_identifiers_must_not_be_empty(
    field_name: str,
) -> None:
    """Every engineering-context identifier must remain nonempty."""

    arguments = {
        "engineering_model_id": "model-a",
        "geometry_id": "geometry-a",
        "mapping_id": "mapping-a",
        "assumptions_id": "assumptions-a",
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        EngineeringBoundaryContext(**arguments)


def test_boundary_record_binds_continuum_conditions_and_context() -> None:
    """A record must retain all explicit engineering-boundary inputs."""

    continuum = _continuum()
    conditions = _conditions()
    context = _context()

    record = EngineeringBoundaryRecord(
        continuum=continuum,
        conditions=conditions,
        context=context,
    )

    assert record.continuum is continuum
    assert record.conditions is conditions
    assert record.context is context
    assert record.condition_count == 2


def test_record_requires_continuum_closure() -> None:
    """Engineering records must bind to a typed continuum closure."""

    with pytest.raises(
        TypeError,
        match="continuum must be a ContinuumClosureRecord instance",
    ):
        EngineeringBoundaryRecord(
            continuum=None,  # type: ignore[arg-type]
            conditions=_conditions(),
            context=_context(),
        )


def test_record_requires_boundary_context() -> None:
    """Engineering records must bind to the typed context."""

    with pytest.raises(
        TypeError,
        match="context must be an EngineeringBoundaryContext instance",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=_conditions(),
            context=None,  # type: ignore[arg-type]
        )


def test_condition_collection_must_be_tuple() -> None:
    """Boundary collections must preserve immutable tuple semantics."""

    with pytest.raises(
        TypeError,
        match="conditions must be a tuple",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=list(_conditions()),  # type: ignore[arg-type]
            context=_context(),
        )


def test_condition_collection_must_not_be_empty() -> None:
    """Engineering records must contain at least one explicit condition."""

    with pytest.raises(
        ValueError,
        match="conditions must not be empty",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=(),
            context=_context(),
        )


def test_condition_collection_rejects_wrong_element_type() -> None:
    """Every boundary collection entry must use the typed condition."""

    with pytest.raises(
        TypeError,
        match=r"conditions\[0\] must be an EngineeringBoundaryCondition instance",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=(None,),  # type: ignore[arg-type]
            context=_context(),
        )


def test_condition_collection_rejects_duplicate_boundary_identity() -> None:
    """Boundary identity triples must remain unique."""

    duplicate = (
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field-a",
            condition_id="condition-a",
            values=(1.0,),
            unit="unit-a",
            source_id="source-a",
        ),
        EngineeringBoundaryCondition(
            boundary_id="boundary-a",
            variable_id="field-a",
            condition_id="condition-a",
            values=(2.0,),
            unit="different-unit",
            source_id="source-b",
        ),
    )

    with pytest.raises(
        ValueError,
        match="conditions must not contain duplicate boundary identities",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=duplicate,
            context=_context(),
        )


def test_condition_collection_requires_canonical_order() -> None:
    """Boundary collections must use deterministic canonical ordering."""

    with pytest.raises(
        ValueError,
        match="conditions must use canonical boundary ordering",
    ):
        EngineeringBoundaryRecord(
            continuum=_continuum(),
            conditions=tuple(reversed(_conditions())),
            context=_context(),
        )


def test_evaluator_receives_continuum_and_context_explicitly() -> None:
    """Evaluation must pass the complete engineering-boundary inputs."""

    continuum = _continuum()
    context = _context()
    observed: list[object] = []

    def evaluator(
        candidate_continuum: ContinuumClosureRecord,
        candidate_context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        observed.extend(
            (candidate_continuum, candidate_context)
        )
        return EngineeringBoundaryRecord(
            continuum=candidate_continuum,
            conditions=_conditions(),
            context=candidate_context,
        )

    result = evaluate_engineering_boundaries(
        continuum,
        context,
        evaluator,
    )

    assert observed == [continuum, context]
    assert result.continuum is continuum
    assert result.context is context
    assert result.conditions == _conditions()


def test_evaluator_result_continuum_must_match_input() -> None:
    """A provider cannot substitute another continuum closure."""

    continuum = _continuum()
    context = _context()

    different_continuum = ContinuumClosureRecord(
        mesoscale=continuum.mesoscale,
        closure_id="continuum-b",
        source_id="source-c",
        continuum_variables=continuum.continuum_variables,
    )

    def evaluator(
        candidate_continuum: ContinuumClosureRecord,
        candidate_context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        del candidate_continuum
        return EngineeringBoundaryRecord(
            continuum=different_continuum,
            conditions=_conditions(),
            context=candidate_context,
        )

    with pytest.raises(
        ValueError,
        match="engineering-boundary result continuum must match input continuum",
    ):
        evaluate_engineering_boundaries(
            continuum,
            context,
            evaluator,
        )


def test_evaluator_result_context_must_match_input() -> None:
    """A provider cannot replace the explicit engineering context."""

    continuum = _continuum()
    context = _context()

    different_context = EngineeringBoundaryContext(
        engineering_model_id="engineering-model-b",
        geometry_id="geometry-a",
        mapping_id="mapping-a",
        assumptions_id="assumptions-a",
    )

    def evaluator(
        candidate_continuum: ContinuumClosureRecord,
        candidate_context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        del candidate_context
        return EngineeringBoundaryRecord(
            continuum=candidate_continuum,
            conditions=_conditions(),
            context=different_context,
        )

    with pytest.raises(
        ValueError,
        match="engineering-boundary result context must match input context",
    ):
        evaluate_engineering_boundaries(
            continuum,
            context,
            evaluator,
        )


def test_evaluator_must_return_boundary_record() -> None:
    """Provider output must satisfy the typed boundary-record contract."""

    def evaluator(
        continuum: ContinuumClosureRecord,
        context: EngineeringBoundaryContext,
    ) -> object:
        del continuum, context
        return {"boundary": 1.0}

    with pytest.raises(
        TypeError,
        match="evaluator must return an EngineeringBoundaryRecord instance",
    ):
        evaluate_engineering_boundaries(
            _continuum(),
            _context(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    """Engineering-boundary evaluation must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_engineering_boundaries(
            _continuum(),
            _context(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_continuum_closure() -> None:
    """Evaluation input must satisfy the typed continuum boundary."""

    def evaluator(
        continuum: ContinuumClosureRecord,
        context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        raise AssertionError(
            "evaluator must not be called for invalid continuum input"
        )

    with pytest.raises(
        TypeError,
        match="continuum must be a ContinuumClosureRecord instance",
    ):
        evaluate_engineering_boundaries(
            None,  # type: ignore[arg-type]
            _context(),
            evaluator,
        )


def test_evaluation_requires_boundary_context() -> None:
    """Evaluation context must satisfy the typed engineering boundary."""

    def evaluator(
        continuum: ContinuumClosureRecord,
        context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        raise AssertionError(
            "evaluator must not be called for invalid context input"
        )

    with pytest.raises(
        TypeError,
        match="context must be an EngineeringBoundaryContext instance",
    ):
        evaluate_engineering_boundaries(
            _continuum(),
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated explicit evaluation must preserve provider determinism."""

    continuum = _continuum()
    context = _context()

    def evaluator(
        candidate_continuum: ContinuumClosureRecord,
        candidate_context: EngineeringBoundaryContext,
    ) -> EngineeringBoundaryRecord:
        return EngineeringBoundaryRecord(
            continuum=candidate_continuum,
            conditions=_conditions(),
            context=candidate_context,
        )

    first = evaluate_engineering_boundaries(
        continuum,
        context,
        evaluator,
    )
    second = evaluate_engineering_boundaries(
        continuum,
        context,
        evaluator,
    )

    assert first == second
