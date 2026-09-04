"""Integration tests for the TR-EIF electronic-reference contract."""

from __future__ import annotations

import pytest

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState, StressState
from tr_eif.multiscale.electronic_reference import (
    ElectronicReferenceRecord,
    evaluate_electronic_reference,
)


def _configuration() -> AtomicConfiguration:
    """Construct a deterministic two-atom reference configuration."""

    return AtomicConfiguration(
        species=("Li", "F"),
        positions=(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
        ),
    )


def _forces() -> ForceState:
    """Construct deterministic reference forces for two atoms."""

    return ForceState(
        forces=(
            (1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
        )
    )


def _stress() -> StressState:
    """Construct one deterministic Cartesian reference stress tensor."""

    return StressState(
        tensor=(
            (1.0, 0.1, 0.2),
            (0.1, 2.0, 0.3),
            (0.2, 0.3, 3.0),
        )
    )


def test_minimal_electronic_reference_record() -> None:
    """Energy-only references must preserve the explicit configuration binding."""

    configuration = _configuration()

    record = ElectronicReferenceRecord(
        configuration=configuration,
        total_energy=-12.5,
        source_id="reference-set-001",
        method_id="method-001",
    )

    assert record.configuration is configuration
    assert record.total_energy == -12.5
    assert record.source_id == "reference-set-001"
    assert record.method_id == "method-001"
    assert record.atom_count == 2
    assert record.has_forces is False
    assert record.has_stress is False


def test_reference_record_accepts_explicit_forces_and_stress() -> None:
    """Optional force and stress references must remain explicit observables."""

    forces = _forces()
    stress = _stress()

    record = ElectronicReferenceRecord(
        configuration=_configuration(),
        total_energy=-3.0,
        source_id="source-a",
        method_id="method-a",
        forces=forces,
        stress=stress,
    )

    assert record.forces is forces
    assert record.stress is stress
    assert record.has_forces is True
    assert record.has_stress is True


def test_reference_identifiers_are_trimmed() -> None:
    """External-reference identifiers must normalize surrounding whitespace."""

    record = ElectronicReferenceRecord(
        configuration=_configuration(),
        total_energy=0.0,
        source_id="  source-a  ",
        method_id="\tmethod-a\n",
    )

    assert record.source_id == "source-a"
    assert record.method_id == "method-a"


def test_total_energy_is_normalized_to_float() -> None:
    """Accepted integral energy input must normalize to the scalar float contract."""

    record = ElectronicReferenceRecord(
        configuration=_configuration(),
        total_energy=-7,
        source_id="source-a",
        method_id="method-a",
    )

    assert record.total_energy == -7.0
    assert isinstance(record.total_energy, float)


def test_force_atom_count_must_match_configuration() -> None:
    """Force references must contain one Cartesian vector per configured atom."""

    with pytest.raises(
        ValueError,
        match="force atom count must match configuration atom count",
    ):
        ElectronicReferenceRecord(
            configuration=_configuration(),
            total_energy=0.0,
            source_id="source-a",
            method_id="method-a",
            forces=ForceState(
                forces=((0.0, 0.0, 0.0),)
            ),
        )


@pytest.mark.parametrize(
    ("value", "exception"),
    (
        (float("inf"), ValueError),
        (float("-inf"), ValueError),
        (float("nan"), ValueError),
        (True, TypeError),
        ("0.0", TypeError),
    ),
)
def test_total_energy_validation(
    value: object,
    exception: type[Exception],
) -> None:
    """Reference total energy must be a finite real scalar."""

    with pytest.raises(exception):
        ElectronicReferenceRecord(
            configuration=_configuration(),
            total_energy=value,  # type: ignore[arg-type]
            source_id="source-a",
            method_id="method-a",
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "source_id",
        "method_id",
    ),
)
def test_identifier_must_be_string(field_name: str) -> None:
    """Provenance identifiers must use the declared string representation."""

    arguments: dict[str, object] = {
        "configuration": _configuration(),
        "total_energy": 0.0,
        "source_id": "source-a",
        "method_id": "method-a",
    }
    arguments[field_name] = 1

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a string",
    ):
        ElectronicReferenceRecord(**arguments)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "field_name",
    (
        "source_id",
        "method_id",
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
def test_identifier_must_not_be_empty_or_whitespace(
    field_name: str,
    value: str,
) -> None:
    """Provenance identifiers must remain nonempty after normalization."""

    arguments = {
        "configuration": _configuration(),
        "total_energy": 0.0,
        "source_id": "source-a",
        "method_id": "method-a",
    }
    arguments[field_name] = value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must not be empty or whitespace",
    ):
        ElectronicReferenceRecord(**arguments)


def test_force_reference_requires_force_state_or_none() -> None:
    """The force field must not accept an untyped force container."""

    with pytest.raises(
        TypeError,
        match="forces must be a ForceState instance or None",
    ):
        ElectronicReferenceRecord(
            configuration=_configuration(),
            total_energy=0.0,
            source_id="source-a",
            method_id="method-a",
            forces=((0.0, 0.0, 0.0),),  # type: ignore[arg-type]
        )


def test_stress_reference_requires_stress_state_or_none() -> None:
    """The stress field must not accept an untyped tensor container."""

    with pytest.raises(
        TypeError,
        match="stress must be a StressState instance or None",
    ):
        ElectronicReferenceRecord(
            configuration=_configuration(),
            total_energy=0.0,
            source_id="source-a",
            method_id="method-a",
            stress=(  # type: ignore[arg-type]
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
        )


def test_record_requires_atomic_configuration() -> None:
    """Electronic references must bind to the typed atomic configuration."""

    with pytest.raises(
        TypeError,
        match="configuration must be an AtomicConfiguration instance",
    ):
        ElectronicReferenceRecord(
            configuration=None,  # type: ignore[arg-type]
            total_energy=0.0,
            source_id="source-a",
            method_id="method-a",
        )


def test_evaluator_receives_input_configuration_and_returns_record() -> None:
    """The evaluation boundary must delegate to the explicit external provider."""

    configuration = _configuration()
    observed: list[AtomicConfiguration] = []

    def evaluator(
        candidate: AtomicConfiguration,
    ) -> ElectronicReferenceRecord:
        observed.append(candidate)
        return ElectronicReferenceRecord(
            configuration=candidate,
            total_energy=-4.0,
            source_id="source-a",
            method_id="method-a",
            forces=_forces(),
            stress=_stress(),
        )

    result = evaluate_electronic_reference(
        configuration,
        evaluator,
    )

    assert observed == [configuration]
    assert observed[0] is configuration
    assert result.configuration is configuration
    assert result.total_energy == -4.0
    assert result.has_forces is True
    assert result.has_stress is True


def test_evaluator_result_must_match_input_configuration() -> None:
    """An external provider cannot return observables for another configuration."""

    configuration = _configuration()
    different = AtomicConfiguration(
        species=("Li", "F"),
        positions=(
            (0.0, 0.0, 0.0),
            (2.0, 0.0, 0.0),
        ),
    )

    def evaluator(
        candidate: AtomicConfiguration,
    ) -> ElectronicReferenceRecord:
        del candidate
        return ElectronicReferenceRecord(
            configuration=different,
            total_energy=0.0,
            source_id="source-a",
            method_id="method-a",
        )

    with pytest.raises(
        ValueError,
        match=(
            "electronic-reference result configuration "
            "must match input configuration"
        ),
    ):
        evaluate_electronic_reference(
            configuration,
            evaluator,
        )


def test_evaluator_must_return_reference_record() -> None:
    """The external provider return type must remain explicit and typed."""

    def evaluator(
        configuration: AtomicConfiguration,
    ) -> object:
        del configuration
        return {"total_energy": 0.0}

    with pytest.raises(
        TypeError,
        match="evaluator must return an ElectronicReferenceRecord instance",
    ):
        evaluate_electronic_reference(
            _configuration(),
            evaluator,  # type: ignore[arg-type]
        )


def test_evaluate_requires_callable_provider() -> None:
    """The electronic-reference boundary must reject non-callable providers."""

    with pytest.raises(
        TypeError,
        match="evaluator must be callable",
    ):
        evaluate_electronic_reference(
            _configuration(),
            None,  # type: ignore[arg-type]
        )


def test_evaluate_requires_atomic_configuration() -> None:
    """Evaluation input must satisfy the typed configuration boundary."""

    def evaluator(
        configuration: AtomicConfiguration,
    ) -> ElectronicReferenceRecord:
        raise AssertionError(
            "evaluator must not be called for invalid configuration input"
        )

    with pytest.raises(
        TypeError,
        match="configuration must be an AtomicConfiguration instance",
    ):
        evaluate_electronic_reference(
            None,  # type: ignore[arg-type]
            evaluator,
        )


def test_evaluation_is_deterministic_for_deterministic_provider() -> None:
    """Repeated evaluation must preserve a deterministic provider result."""

    configuration = _configuration()

    def evaluator(
        candidate: AtomicConfiguration,
    ) -> ElectronicReferenceRecord:
        return ElectronicReferenceRecord(
            configuration=candidate,
            total_energy=-1.25,
            source_id="source-a",
            method_id="method-a",
            forces=_forces(),
        )

    first = evaluate_electronic_reference(
        configuration,
        evaluator,
    )
    second = evaluate_electronic_reference(
        configuration,
        evaluator,
    )

    assert first == second
