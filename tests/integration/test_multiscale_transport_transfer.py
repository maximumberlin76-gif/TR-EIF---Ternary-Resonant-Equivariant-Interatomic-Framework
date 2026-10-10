"""Integration tests for the TR-EIF transport-coefficient transfer contract."""

from __future__ import annotations

import pytest

from tr_eif.multiscale.transport_transfer import (
    TransportCoefficient,
    TransportCoefficientTransferRecord,
    TransportTransferContext,
    evaluate_transport_coefficient_transfer,
)


def _source() -> TransportCoefficient:
    """Construct one deterministic source-scale transport coefficient."""

    return TransportCoefficient(
        coefficient_id="thermal_conductivity",
        value=2.5,
        unit="W/(m*K)",
        scale_id="atomistic",
        state_domain_id="state-a",
        source_id="source-a",
    )


def _context() -> TransportTransferContext:
    """Construct one deterministic explicit transfer context."""

    return TransportTransferContext(
        target_scale_id="mesoscale",
        mapping_id="mapping-a",
        normalization_id="normalization-a",
        assumptions_id="assumptions-a",
    )


def _target() -> TransportCoefficient:
    """Construct one deterministic target-scale transport coefficient."""

    return TransportCoefficient(
        coefficient_id="thermal_conductivity",
        value=1.75,
        unit="W/(m*K)",
        scale_id="mesoscale",
        state_domain_id="state-b",
        source_id="source-b",
    )


def test_transport_coefficient_normalizes_identifiers_and_value() -> None:
    """Coefficient construction must normalize identifiers and real values."""

    coefficient = TransportCoefficient(
        coefficient_id="  thermal_conductivity ",
        value=2,
        unit=" W/(m*K) ",
        scale_id=" atomistic ",
        state_domain_id=" state-a ",
        source_id=" source-a ",
    )

    assert coefficient.coefficient_id == "thermal_conductivity"
    assert coefficient.value == 2.0
    assert isinstance(coefficient.value, float)
    assert coefficient.unit == "W/(m*K)"
    assert coefficient.scale_id == "atomistic"
    assert coefficient.state_domain_id == "state-a"
    assert coefficient.source_id == "source-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "coefficient_id",
        "unit",
        "scale_id",
        "state_domain_id",
        "source_id",
    ),
)
def test_transport_coefficient_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every coefficient identifier field must use the string contract."""

    arguments: dict[str, object] = {
        "coefficient_id": "thermal_conductivity",
        "value": 2.5,
        "unit": "W/(m*K)",
        "scale_id": "atomistic",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        TransportCoefficient(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "coefficient_id",
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
def test_transport_coefficient_identifiers_must_not_be_empty(
    field_name: str,
    value: str,
) -> None:
    """Every coefficient identifier must remain nonempty after normalization."""

    arguments = {
        "coefficient_id": "thermal_conductivity",
        "value": 2.5,
        "unit": "W/(m*K)",
        "scale_id": "atomistic",
        "state_domain_id": "state-a",
        "source_id": "source-a",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        TransportCoefficient(**arguments)


@pytest.mark.parametrize(
    ("value", "exception"),
    (
        (float("inf"), ValueError),
        (float("-inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("2.5", TypeError),
    ),
)
def test_transport_coefficient_value_must_be_finite_real(
    value: object,
    exception: type[Exception],
) -> None:
    """Coefficient values must remain finite real scalars."""

    with pytest.raises(exception):
        TransportCoefficient(
            coefficient_id="thermal_conductivity",
            value=value,  # type: ignore[arg-type]
            unit="W/(m*K)",
            scale_id="atomistic",
            state_domain_id="state-a",
            source_id="source-a",
        )


def test_transport_coefficient_contract_does_not_impose_sign_restriction() -> None:
    """The generic transfer contract must not invent coefficient sign rules."""

    coefficient = TransportCoefficient(
        coefficient_id="signed_reference",
        value=-1.5,
        unit="arbitrary-unit",
        scale_id="scale-a",
        state_domain_id="state-a",
        source_id="source-a",
    )

    assert coefficient.value == -1.5


def test_transfer_context_normalizes_identifiers() -> None:
    """Transfer context identifiers must normalize surrounding whitespace."""

    context = TransportTransferContext(
        target_scale_id=" mesoscale ",
        mapping_id=" mapping-a ",
        normalization_id=" normalization-a ",
        assumptions_id=" assumptions-a ",
    )

    assert context.target_scale_id == "mesoscale"
    assert context.mapping_id == "mapping-a"
    assert context.normalization_id == "normalization-a"
    assert context.assumptions_id == "assumptions-a"


@pytest.mark.parametrize(
    "field_name",
    (
        "target_scale_id",
        "mapping_id",
        "normalization_id",
        "assumptions_id",
    ),
)
def test_transfer_context_identifiers_must_be_strings(
    field_name: str,
) -> None:
    """Every transfer-context identifier must use the string contract."""

    arguments: dict[str, object] = {
        "target_scale_id": "mesoscale",
        "mapping_id": "mapping-a",
        "normalization_id": "normalization-a",
        "assumptions_id": "assumptions-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        TransportTransferContext(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "target_scale_id",
        "mapping_id",
        "normalization_id",
        "assumptions_id",
    ),
)
def test_transfer_context_identifiers_must_not_be_empty(
    field_name: str,
) -> None:
    """Every transfer-context identifier must remain nonempty."""

    arguments = {
        "target_scale_id": "mesoscale",
        "mapping_id": "mapping-a",
        "normalization_id": "normalization-a",
        "assumptions_id": "assumptions-a",
    }
    arguments[field_name] = "   "

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        TransportTransferContext(**arguments)


def test_transfer_record_binds_source_target_and_context() -> None:
    """A transfer record must retain all three explicit contract objects."""

    source = _source()
    target = _target()
    context = _context()

    record = TransportCoefficientTransferRecord(
        source=source,
        target=target,
        context=context,
    )

    assert record.source is source
    assert record.target is target
    assert record.context is context


def test_transfer_record_requires_source_coefficient() -> None:
    """The source field must use TransportCoefficient."""

    with pytest.raises(
        TypeError,
        match="source must be a TransportCoefficient instance",
    ):
        TransportCoefficientTransferRecord(
            source=None,  # type: ignore[arg-type]
            target=_target(),
            context=_context(),
        )


def test_transfer_record_requires_target_coefficient() -> None:
    """The target field must use TransportCoefficient."""

    with pytest.raises(
        TypeError,
        match="target must be a TransportCoefficient instance",
    ):
        TransportCoefficientTransferRecord(
            source=_source(),
            target=None,  # type: ignore[arg-type]
            context=_context(),
        )


def test_transfer_record_requires_transfer_context() -> None:
    """The context field must use TransportTransferContext."""

    with pytest.raises(
        TypeError,
        match="context must be a TransportTransferContext instance",
    ):
        TransportCoefficientTransferRecord(
            source=_source(),
            target=_target(),
            context=None,  # type: ignore[arg-type]
        )


def test_target_coefficient_id_must_match_source() -> None:
    """A transfer cannot silently change the identity of the coefficient."""

    target = TransportCoefficient(
        coefficient_id="diffusivity",
        value=1.75,
        unit="m^2/s",
        scale_id="mesoscale",
        state_domain_id="state-b",
        source_id="source-b",
    )

    with pytest.raises(
        ValueError,
        match="target coefficient_id must match source coefficient_id",
    ):
        TransportCoefficientTransferRecord(
            source=_source(),
            target=target,
            context=_context(),
        )


def test_target_scale_must_match_transfer_context() -> None:
    """The target coefficient must be bound to the declared destination scale."""

    target = TransportCoefficient(
        coefficient_id="thermal_conductivity",
        value=1.75,
        unit="W/(m*K)",
        scale_id="continuum",
        state_domain_id="state-b",
        source_id="source-b",
    )

    with pytest.raises(
        ValueError,
        match="target scale_id must match context target_scale_id",
    ):
        TransportCoefficientTransferRecord(
            source=_source(),
            target=target,
            context=_context(),
        )


def test_transfer_record_does_not_require_equal_units() -> None:
    """Unit transformation remains explicit provider responsibility."""

    target = TransportCoefficient(
        coefficient_id="thermal_conductivity",
        value=17.5,
        unit="provider-unit",
        scale_id="mesoscale",
        state_domain_id="state-b",
        source_id="source-b",
    )

    record = TransportCoefficientTransferRecord(
        source=_source(),
        target=target,
        context=_context(),
    )

    assert record.source.unit == "W/(m*K)"
    assert record.target.unit == "provider-unit"


def test_transfer_record_does_not_require_equal_state_domains() -> None:
    """State-domain mapping remains explicit rather than silently constrained."""

    record = TransportCoefficientTransferRecord(
        source=_source(),
        target=_target(),
        context=_context(),
    )

    assert record.source.state_domain_id == "state-a"
    assert record.target.state_domain_id == "state-b"


def test_evaluator_receives_source_and_context_explicitly() -> None:
    """Evaluation must pass all declared transfer inputs to the provider."""

    source = _source()
    context = _context()
    observed: list[object] = []

    def evaluator(
        candidate_source: TransportCoefficient,
        candidate_context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        observed.extend(
            (candidate_source, candidate_context)
        )
        return TransportCoefficientTransferRecord(
            source=candidate_source,
            target=_target(),
            context=candidate_context,
        )

    result = evaluate_transport_coefficient_transfer(
        source,
        context,
        evaluator,
    )

    assert observed == [source, context]
    assert result.source is source
    assert result.context is context
    assert result.target == _target()


def test_evaluator_result_source_must_match_input() -> None:
    """A provider cannot replace the explicit source coefficient."""

    source = _source()
    context = _context()

    different_source = TransportCoefficient(
        coefficient_id="thermal_conductivity",
        value=9.0,
        unit="W/(m*K)",
        scale_id="atomistic",
        state_domain_id="state-a",
        source_id="different-source",
    )

    def evaluator(
        candidate_source: TransportCoefficient,
        candidate_context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        del candidate_source
        return TransportCoefficientTransferRecord(
            source=different_source,
            target=_target(),
            context=candidate_context,
        )

    with pytest.raises(
        ValueError,
        match="transport-transfer result source must match input source",
    ):
        evaluate_transport_coefficient_transfer(
            source,
            context,
            evaluator,
        )


def test_evaluator_result_context_must_match_input() -> None:
    """A provider cannot replace the explicit mapping context."""

    source = _source()
    context = _context()

    different_context = TransportTransferContext(
        target_scale_id="mesoscale",
        mapping_id="mapping-b",
        normalization_id="normalization-a",
        assumptions_id="assumptions-a",
    )

    def evaluator(
        candidate_source: TransportCoefficient,
        candidate_context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        del candidate_context
        return TransportCoefficientTransferRecord(
            source=candidate_source,
            target=_target(),
            context=different_context,
        )

    with pytest.raises(
        ValueError,
        match="transport-transfer result context must match input context",
    ):
        evaluate_transport_coefficient_transfer(
            source,
            context,
            evaluator,
        )


def test_evaluator_must_return_transfer_record() -> None:
    """Provider output must satisfy the typed transfer-record boundary."""

    def evaluator(
        source: TransportCoefficient,
        context: TransportTransferContext,
    ) -> object:
        del source, context
        return {"value": 1.75}

    with pytest.raises(
        TypeError,
        match=(
            "evaluator must return a "
            "TransportCoefficientTransferRecord instance"
        ),
    ):
        evaluate_transport_coefficient_transfer(
            _source(),
            _context(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluator_must_be_callable() -> None:
    """Transport transfer evaluation must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_transport_coefficient_transfer(
            _source(),
            _context(),
            None,  # type: ignore[arg-type]
        )


def test_evaluation_requires_transport_coefficient_source() -> None:
    """Evaluation source must satisfy the typed coefficient boundary."""

    def evaluator(
        source: TransportCoefficient,
        context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        raise AssertionError(
            "evaluator must not be called for invalid source input"
        )

    with pytest.raises(
        TypeError,
        match="source must be a TransportCoefficient instance",
    ):
        evaluate_transport_coefficient_transfer(
            None,  # type: ignore[arg-type]
            _context(),
            evaluator,
        )


def test_evaluation_requires_transport_transfer_context() -> None:
    """Evaluation context must satisfy the typed transfer boundary."""

    def evaluator(
        source: TransportCoefficient,
        context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        raise AssertionError(
            "evaluator must not be called for invalid context input"
        )

    with pytest.raises(
        TypeError,
        match="context must be a TransportTransferContext instance",
    ):
        evaluate_transport_coefficient_transfer(
            _source(),
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated transfer evaluation must preserve provider determinism."""

    source = _source()
    context = _context()

    def evaluator(
        candidate_source: TransportCoefficient,
        candidate_context: TransportTransferContext,
    ) -> TransportCoefficientTransferRecord:
        return TransportCoefficientTransferRecord(
            source=candidate_source,
            target=_target(),
            context=candidate_context,
        )

    first = evaluate_transport_coefficient_transfer(
        source,
        context,
        evaluator,
    )
    second = evaluate_transport_coefficient_transfer(
        source,
        context,
        evaluator,
    )

    assert first == second
