"""Integration tests for the TR-EIF continuum closure contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.continuum_closure import (
    ContinuumClosureRecord,
    ContinuumClosureVariable,
    evaluate_continuum_closure,
)
from tr_eif.multiscale.mesoscale_closure import (
    MesoscaleClosureRecord,
    MesoscaleClosureVariable,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.state import CoarseScaleState


def _coarse_state() -> CoarseScaleState:
    """Construct a deterministic two-entity coarse-scale state."""

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
    """Construct one explicit mesoscale closure input."""

    return MesoscaleClosureRecord(
        state=_coarse_state(),
        closure_id="mesoscale-a",
        source_id="source-m",
        closure_variables=(
            MesoscaleClosureVariable(
                name="flux",
                values=(1.0, -1.0),
            ),
            MesoscaleClosureVariable(
                name="source",
                values=(0.25, 0.5),
            ),
        ),
    )


def _continuum_variables() -> tuple[ContinuumClosureVariable, ...]:
    """Return canonical deterministic continuum closure variables."""

    return (
        ContinuumClosureVariable(
            name="field_a",
            values=(1.0, 2.0),
        ),
        ContinuumClosureVariable(
            name="field_b",
            values=(-0.5, 0.75),
        ),
    )


def _auxiliary_variables() -> tuple[ContinuumClosureVariable, ...]:
    """Return canonical deterministic continuum auxiliary variables."""

    return (
        ContinuumClosureVariable(
            name="boundary_input",
            values=(3.0, 4.0),
        ),
        ContinuumClosureVariable(
            name="history_input",
            values=(0.1, 0.2),
        ),
    )


def test_continuum_variable_normalizes_name_and_numeric_values() -> None:
    """Continuum variables must normalize whitespace and accepted numerics."""

    variable = ContinuumClosureVariable(
        name="  field_a  ",
        values=(1, -2.5),
    )

    assert variable.name == "field_a"
    assert variable.values == (1.0, -2.5)


@pytest.mark.parametrize(
    "name",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_continuum_variable_name_must_not_be_empty(name: str) -> None:
    """Variable names must remain nonempty after normalization."""

    with pytest.raises(
        ValueError,
        match="name must not be empty or whitespace",
    ):
        ContinuumClosureVariable(
            name=name,
            values=(1.0,),
        )


def test_continuum_variable_name_must_be_string() -> None:
    """Variable names must satisfy the explicit string contract."""

    with pytest.raises(
        TypeError,
        match="name must be a string",
    ):
        ContinuumClosureVariable(
            name=1,  # type: ignore[arg-type]
            values=(1.0,),
        )


def test_continuum_variable_values_must_be_tuple() -> None:
    """Continuum values must use the immutable tuple representation."""

    with pytest.raises(
        TypeError,
        match="values must be a tuple",
    ):
        ContinuumClosureVariable(
            name="field_a",
            values=[1.0],  # type: ignore[arg-type]
        )


def test_continuum_variable_values_must_not_be_empty() -> None:
    """One continuum variable must contain at least one finite value."""

    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        ContinuumClosureVariable(
            name="field_a",
            values=(),
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
def test_continuum_variable_values_must_be_finite_reals(
    value: object,
    exception: type[Exception],
) -> None:
    """Continuum values must not encode invalid or nonfinite numeric states."""

    with pytest.raises(exception):
        ContinuumClosureVariable(
            name="field_a",
            values=(value,),  # type: ignore[arg-type]
        )


def test_minimal_continuum_closure_record() -> None:
    """A continuum record must bind explicit outputs to one mesoscale input."""

    mesoscale = _mesoscale()
    variables = _continuum_variables()

    record = ContinuumClosureRecord(
        mesoscale=mesoscale,
        closure_id="continuum-a",
        source_id="source-c",
        continuum_variables=variables,
    )

    assert record.mesoscale is mesoscale
    assert record.closure_id == "continuum-a"
    assert record.source_id == "source-c"
    assert record.continuum_variables == variables
    assert record.auxiliary_variables == ()
    assert record.variable_count == 2


def test_record_identifiers_are_trimmed() -> None:
    """Closure and source identifiers must normalize surrounding whitespace."""

    record = ContinuumClosureRecord(
        mesoscale=_mesoscale(),
        closure_id="  continuum-a ",
        source_id="\tsource-c\n",
        continuum_variables=_continuum_variables(),
    )

    assert record.closure_id == "continuum-a"
    assert record.source_id == "source-c"


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_id",
        "source_id",
    ),
)
def test_record_identifier_must_be_string(field_name: str) -> None:
    """Continuum provenance identifiers must use explicit strings."""

    arguments: dict[str, object] = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        ContinuumClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_id",
        "source_id",
    ),
)
def test_record_identifier_must_not_be_empty(field_name: str) -> None:
    """Continuum provenance identifiers must remain nonempty."""

    arguments = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        ContinuumClosureRecord(**arguments)


def test_record_requires_mesoscale_closure_record() -> None:
    """Continuum closure records must bind to MesoscaleClosureRecord."""

    with pytest.raises(
        TypeError,
        match="mesoscale must be a MesoscaleClosureRecord instance",
    ):
        ContinuumClosureRecord(
            mesoscale=None,  # type: ignore[arg-type]
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
        )


def test_continuum_variables_must_not_be_empty() -> None:
    """A continuum closure record must expose at least one output variable."""

    with pytest.raises(
        ValueError,
        match="continuum_variables must not be empty",
    ):
        ContinuumClosureRecord(
            mesoscale=_mesoscale(),
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=(),
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "continuum_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_must_be_tuples(field_name: str) -> None:
    """Continuum-variable collections must preserve immutable tuple semantics."""

    arguments: dict[str, object] = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = list(_continuum_variables())

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a tuple",
    ):
        ContinuumClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "continuum_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_reject_wrong_element_type(
    field_name: str,
) -> None:
    """Every collection entry must be a typed continuum closure variable."""

    arguments: dict[str, object] = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = (None,)

    with pytest.raises(
        TypeError,
        match=rf"{field_name}\[0\] must be a ContinuumClosureVariable instance",
    ):
        ContinuumClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "continuum_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_reject_duplicate_names(field_name: str) -> None:
    """Variable names must be unique within each deterministic collection."""

    duplicate = (
        ContinuumClosureVariable(
            name="field_a",
            values=(1.0,),
        ),
        ContinuumClosureVariable(
            name="field_a",
            values=(2.0,),
        ),
    )

    arguments = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = duplicate

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not contain duplicate variable names",
    ):
        ContinuumClosureRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "continuum_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_require_canonical_name_order(
    field_name: str,
) -> None:
    """Deterministic continuum collections must use ascending name ordering."""

    unsorted = tuple(
        reversed(_continuum_variables())
    )

    arguments = {
        "mesoscale": _mesoscale(),
        "closure_id": "continuum-a",
        "source_id": "source-c",
        "continuum_variables": _continuum_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = unsorted

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must use canonical name ordering",
    ):
        ContinuumClosureRecord(**arguments)


def test_variable_lookup_returns_exact_continuum_variable() -> None:
    """Named lookup must return the normalized explicit continuum output."""

    record = ContinuumClosureRecord(
        mesoscale=_mesoscale(),
        closure_id="continuum-a",
        source_id="source-c",
        continuum_variables=_continuum_variables(),
    )

    variable = record.variable("  field_a  ")

    assert variable is record.continuum_variables[0]
    assert variable.values == (1.0, 2.0)


def test_variable_lookup_rejects_missing_name() -> None:
    """Lookup must not synthesize a continuum variable that is not present."""

    record = ContinuumClosureRecord(
        mesoscale=_mesoscale(),
        closure_id="continuum-a",
        source_id="source-c",
        continuum_variables=_continuum_variables(),
    )

    with pytest.raises(
        KeyError,
        match="continuum variable 'missing' is not present",
    ):
        record.variable("missing")


def test_evaluator_receives_mesoscale_and_auxiliary_variables_explicitly() -> None:
    """Evaluation must pass all result-affecting continuum inputs explicitly."""

    mesoscale = _mesoscale()
    auxiliary = _auxiliary_variables()
    observed: list[object] = []

    def evaluator(
        candidate: MesoscaleClosureRecord,
        candidate_auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        observed.extend(
            (candidate, candidate_auxiliary)
        )
        return ContinuumClosureRecord(
            mesoscale=candidate,
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
            auxiliary_variables=candidate_auxiliary,
        )

    result = evaluate_continuum_closure(
        mesoscale,
        evaluator,
        auxiliary,
    )

    assert observed == [mesoscale, auxiliary]
    assert result.mesoscale is mesoscale
    assert result.auxiliary_variables is auxiliary


def test_evaluator_result_mesoscale_must_match_input() -> None:
    """A provider cannot return continuum output for another mesoscale input."""

    mesoscale = _mesoscale()
    different = MesoscaleClosureRecord(
        state=mesoscale.state,
        closure_id="mesoscale-b",
        source_id="source-m",
        closure_variables=mesoscale.closure_variables,
    )

    def evaluator(
        candidate: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        del candidate
        return ContinuumClosureRecord(
            mesoscale=different,
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
            auxiliary_variables=auxiliary,
        )

    with pytest.raises(
        ValueError,
        match="continuum-closure result mesoscale input must match input",
    ):
        evaluate_continuum_closure(
            mesoscale,
            evaluator,
        )


def test_evaluator_result_auxiliary_variables_must_match_input() -> None:
    """A provider cannot replace explicit continuum auxiliary input state."""

    mesoscale = _mesoscale()
    auxiliary = _auxiliary_variables()

    def evaluator(
        candidate: MesoscaleClosureRecord,
        candidate_auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        del candidate_auxiliary
        return ContinuumClosureRecord(
            mesoscale=candidate,
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
            auxiliary_variables=(),
        )

    with pytest.raises(
        ValueError,
        match=(
            "continuum-closure result auxiliary variables "
            "must match input"
        ),
    ):
        evaluate_continuum_closure(
            mesoscale,
            evaluator,
            auxiliary,
        )


def test_evaluator_must_return_continuum_closure_record() -> None:
    """Provider output must satisfy the typed continuum closure boundary."""

    def evaluator(
        mesoscale: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> object:
        del mesoscale, auxiliary
        return {"field_a": (1.0,)}

    with pytest.raises(
        TypeError,
        match="evaluator must return a ContinuumClosureRecord instance",
    ):
        evaluate_continuum_closure(
            _mesoscale(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    """Continuum closure evaluation must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_continuum_closure(
            _mesoscale(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_mesoscale_closure_record() -> None:
    """Closure evaluation input must satisfy the typed mesoscale boundary."""

    def evaluator(
        mesoscale: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        raise AssertionError(
            "evaluator must not be called for invalid mesoscale input"
        )

    with pytest.raises(
        TypeError,
        match="mesoscale must be a MesoscaleClosureRecord instance",
    ):
        evaluate_continuum_closure(
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_validates_auxiliary_collection_before_provider() -> None:
    """Invalid auxiliary collections must fail before provider invocation."""

    called = False

    def evaluator(
        mesoscale: MesoscaleClosureRecord,
        auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        nonlocal called
        called = True
        return ContinuumClosureRecord(
            mesoscale=mesoscale,
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
            auxiliary_variables=auxiliary,
        )

    with pytest.raises(
        ValueError,
        match="auxiliary_variables must use canonical name ordering",
    ):
        evaluate_continuum_closure(
            _mesoscale(),
            evaluator,
            tuple(reversed(_auxiliary_variables())),
        )

    assert called is False


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated explicit continuum evaluation must preserve provider determinism."""

    mesoscale = _mesoscale()
    auxiliary = _auxiliary_variables()

    def evaluator(
        candidate: MesoscaleClosureRecord,
        candidate_auxiliary: tuple[ContinuumClosureVariable, ...],
    ) -> ContinuumClosureRecord:
        return ContinuumClosureRecord(
            mesoscale=candidate,
            closure_id="continuum-a",
            source_id="source-c",
            continuum_variables=_continuum_variables(),
            auxiliary_variables=candidate_auxiliary,
        )

    first = evaluate_continuum_closure(
        mesoscale,
        evaluator,
        auxiliary,
    )
    second = evaluate_continuum_closure(
        mesoscale,
        evaluator,
        auxiliary,
    )

    assert first == second
