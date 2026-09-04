"""Integration tests for the TR-EIF mesoscale closure contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.mesoscale_closure import (
    MesoscaleClosureRecord,
    MesoscaleClosureVariable,
    evaluate_mesoscale_closure,
)
from tr_eif.multiscale.partition import MultiscalePartition
from tr_eif.multiscale.state import CoarseScaleState


def _state() -> CoarseScaleState:
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


def _closure_variables() -> tuple[MesoscaleClosureVariable, ...]:
    """Return canonical deterministic closure output variables."""

    return (
        MesoscaleClosureVariable(
            name="flux",
            values=(1.0, -1.0),
        ),
        MesoscaleClosureVariable(
            name="source",
            values=(0.25, 0.5),
        ),
    )


def _auxiliary_variables() -> tuple[MesoscaleClosureVariable, ...]:
    """Return canonical deterministic auxiliary variables."""

    return (
        MesoscaleClosureVariable(
            name="history",
            values=(0.1, 0.2),
        ),
        MesoscaleClosureVariable(
            name="temperature_input",
            values=(10.0, 20.0),
        ),
    )


def test_closure_variable_normalizes_name_and_numeric_values() -> None:
    """Closure variables must normalize whitespace and accepted numerics."""

    variable = MesoscaleClosureVariable(
        name="  flux  ",
        values=(1, -2.5),
    )

    assert variable.name == "flux"
    assert variable.values == (1.0, -2.5)


@pytest.mark.parametrize(
    "name",
    (
        "",
        "   ",
        "\t\n",
    ),
)
def test_closure_variable_name_must_not_be_empty(name: str) -> None:
    """Variable names must remain nonempty after normalization."""

    with pytest.raises(
        ValueError,
        match="name must not be empty or whitespace",
    ):
        MesoscaleClosureVariable(
            name=name,
            values=(1.0,),
        )


def test_closure_variable_name_must_be_string() -> None:
    """Variable names must satisfy the explicit string contract."""

    with pytest.raises(
        TypeError,
        match="name must be a string",
    ):
        MesoscaleClosureVariable(
            name=1,  # type: ignore[arg-type]
            values=(1.0,),
        )


def test_closure_variable_values_must_be_tuple() -> None:
    """Closure values must use the immutable tuple representation."""

    with pytest.raises(
        TypeError,
        match="values must be a tuple",
    ):
        MesoscaleClosureVariable(
            name="flux",
            values=[1.0],  # type: ignore[arg-type]
        )


def test_closure_variable_values_must_not_be_empty() -> None:
    """One closure variable must contain at least one finite value."""

    with pytest.raises(
        ValueError,
        match="values must not be empty",
    ):
        MesoscaleClosureVariable(
            name="flux",
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
def test_closure_variable_values_must_be_finite_reals(
    value: object,
    exception: type[Exception],
) -> None:
    """Closure values must not encode invalid or nonfinite numeric states."""

    with pytest.raises(exception):
        MesoscaleClosureVariable(
            name="flux",
            values=(value,),  # type: ignore[arg-type]
        )


def test_minimal_closure_record() -> None:
    """A closure record must bind explicit output variables to a coarse state."""

    state = _state()
    variables = _closure_variables()

    record = MesoscaleClosureRecord(
        state=state,
        closure_id="closure-a",
        source_id="source-a",
        closure_variables=variables,
    )

    assert record.state is state
    assert record.closure_id == "closure-a"
    assert record.source_id == "source-a"
    assert record.closure_variables == variables
    assert record.auxiliary_variables == ()
    assert record.variable_count == 2


def test_record_identifiers_are_trimmed() -> None:
    """Closure and source identifiers must normalize surrounding whitespace."""

    record = MesoscaleClosureRecord(
        state=_state(),
        closure_id="  closure-a ",
        source_id="\tsource-a\n",
        closure_variables=_closure_variables(),
    )

    assert record.closure_id == "closure-a"
    assert record.source_id == "source-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_id",
        "source_id",
    ),
)
def test_record_identifier_must_be_string(field_name: str) -> None:
    """Closure provenance identifiers must use explicit strings."""

    arguments: dict[str, object] = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        MesoscaleClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_id",
        "source_id",
    ),
)
def test_record_identifier_must_not_be_empty(field_name: str) -> None:
    """Closure provenance identifiers must remain nonempty."""

    arguments = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        MesoscaleClosureRecord(**arguments)


def test_record_requires_coarse_scale_state() -> None:
    """Mesoscale closure records must bind to CoarseScaleState."""

    with pytest.raises(
        TypeError,
        match="state must be a CoarseScaleState instance",
    ):
        MesoscaleClosureRecord(
            state=None,  # type: ignore[arg-type]
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
        )


def test_closure_variables_must_not_be_empty() -> None:
    """A closure record must expose at least one closure-output variable."""

    with pytest.raises(
        ValueError,
        match="closure_variables must not be empty",
    ):
        MesoscaleClosureRecord(
            state=_state(),
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=(),
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_must_be_tuples(field_name: str) -> None:
    """Closure-variable collections must preserve immutable tuple semantics."""

    arguments: dict[str, object] = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = list(_closure_variables())

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a tuple",
    ):
        MesoscaleClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_reject_wrong_element_type(
    field_name: str,
) -> None:
    """Every collection entry must be a typed closure variable."""

    arguments: dict[str, object] = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = (None,)

    with pytest.raises(
        TypeError,
        match=rf"{field_name}\[0\] must be a MesoscaleClosureVariable instance",
    ):
        MesoscaleClosureRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_reject_duplicate_names(field_name: str) -> None:
    """Variable names must be unique within each deterministic collection."""

    duplicate = (
        MesoscaleClosureVariable(
            name="flux",
            values=(1.0,),
        ),
        MesoscaleClosureVariable(
            name="flux",
            values=(2.0,),
        ),
    )

    arguments = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = duplicate

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not contain duplicate variable names",
    ):
        MesoscaleClosureRecord(**arguments)


@pytest.mark.parametrize(
    "field_name",
    (
        "closure_variables",
        "auxiliary_variables",
    ),
)
def test_variable_collections_require_canonical_name_order(
    field_name: str,
) -> None:
    """Deterministic closure collections must use ascending name ordering."""

    unsorted = tuple(
        reversed(_closure_variables())
    )

    arguments = {
        "state": _state(),
        "closure_id": "closure-a",
        "source_id": "source-a",
        "closure_variables": _closure_variables(),
        "auxiliary_variables": (),
    }
    arguments[field_name] = unsorted

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must use canonical name ordering",
    ):
        MesoscaleClosureRecord(**arguments)


def test_variable_lookup_returns_exact_closure_variable() -> None:
    """Named lookup must return the normalized explicit closure output."""

    record = MesoscaleClosureRecord(
        state=_state(),
        closure_id="closure-a",
        source_id="source-a",
        closure_variables=_closure_variables(),
    )

    variable = record.variable("  flux  ")

    assert variable is record.closure_variables[0]
    assert variable.values == (1.0, -1.0)


def test_variable_lookup_rejects_missing_name() -> None:
    """Lookup must not synthesize a closure variable that is not present."""

    record = MesoscaleClosureRecord(
        state=_state(),
        closure_id="closure-a",
        source_id="source-a",
        closure_variables=_closure_variables(),
    )

    with pytest.raises(
        KeyError,
        match="closure variable 'missing' is not present",
    ):
        record.variable("missing")


def test_evaluator_receives_state_and_auxiliary_variables_explicitly() -> None:
    """Evaluation must pass all result-affecting closure inputs explicitly."""

    state = _state()
    auxiliary = _auxiliary_variables()
    observed: list[object] = []

    def evaluator(
        candidate: CoarseScaleState,
        candidate_auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        observed.extend(
            (candidate, candidate_auxiliary)
        )
        return MesoscaleClosureRecord(
            state=candidate,
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
            auxiliary_variables=candidate_auxiliary,
        )

    result = evaluate_mesoscale_closure(
        state,
        evaluator,
        auxiliary,
    )

    assert observed == [state, auxiliary]
    assert result.state is state
    assert result.auxiliary_variables is auxiliary


def test_evaluator_result_state_must_match_input() -> None:
    """A provider cannot return closure output for another coarse state."""

    state = _state()
    different = CoarseScaleState(
        partition=state.partition,
        positions=(
            (0.75, 0.0, 0.0),
            (2.5, 0.0, 0.0),
        ),
        masses=state.masses,
    )

    def evaluator(
        candidate: CoarseScaleState,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        del candidate
        return MesoscaleClosureRecord(
            state=different,
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
            auxiliary_variables=auxiliary,
        )

    with pytest.raises(
        ValueError,
        match="mesoscale-closure result state must match input state",
    ):
        evaluate_mesoscale_closure(
            state,
            evaluator,
        )


def test_evaluator_result_auxiliary_variables_must_match_input() -> None:
    """A provider cannot replace explicit auxiliary result-affecting state."""

    state = _state()
    auxiliary = _auxiliary_variables()

    def evaluator(
        candidate: CoarseScaleState,
        candidate_auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        del candidate_auxiliary
        return MesoscaleClosureRecord(
            state=candidate,
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
            auxiliary_variables=(),
        )

    with pytest.raises(
        ValueError,
        match=(
            "mesoscale-closure result auxiliary variables "
            "must match input"
        ),
    ):
        evaluate_mesoscale_closure(
            state,
            evaluator,
            auxiliary,
        )


def test_evaluator_must_return_closure_record() -> None:
    """Provider output must satisfy the typed mesoscale closure boundary."""

    def evaluator(
        state: CoarseScaleState,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> object:
        del state, auxiliary
        return {"flux": (1.0,)}

    with pytest.raises(
        TypeError,
        match="evaluator must return a MesoscaleClosureRecord instance",
    ):
        evaluate_mesoscale_closure(
            _state(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    """Mesoscale closure evaluation must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_mesoscale_closure(
            _state(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_coarse_scale_state() -> None:
    """Closure evaluation input must satisfy the typed coarse-state boundary."""

    def evaluator(
        state: CoarseScaleState,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        raise AssertionError(
            "evaluator must not be called for invalid state input"
        )

    with pytest.raises(
        TypeError,
        match="state must be a CoarseScaleState instance",
    ):
        evaluate_mesoscale_closure(
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_validates_auxiliary_collection_before_provider() -> None:
    """Invalid auxiliary collections must fail before provider invocation."""

    called = False

    def evaluator(
        state: CoarseScaleState,
        auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        nonlocal called
        called = True
        return MesoscaleClosureRecord(
            state=state,
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
            auxiliary_variables=auxiliary,
        )

    with pytest.raises(
        ValueError,
        match="auxiliary_variables must use canonical name ordering",
    ):
        evaluate_mesoscale_closure(
            _state(),
            evaluator,
            tuple(reversed(_auxiliary_variables())),
        )

    assert called is False


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated explicit closure evaluation must preserve provider determinism."""

    state = _state()
    auxiliary = _auxiliary_variables()

    def evaluator(
        candidate: CoarseScaleState,
        candidate_auxiliary: tuple[MesoscaleClosureVariable, ...],
    ) -> MesoscaleClosureRecord:
        return MesoscaleClosureRecord(
            state=candidate,
            closure_id="closure-a",
            source_id="source-a",
            closure_variables=_closure_variables(),
            auxiliary_variables=candidate_auxiliary,
        )

    first = evaluate_mesoscale_closure(
        state,
        evaluator,
        auxiliary,
    )
    second = evaluate_mesoscale_closure(
        state,
        evaluator,
        auxiliary,
    )

    assert first == second
