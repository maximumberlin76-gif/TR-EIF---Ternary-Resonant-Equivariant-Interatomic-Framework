"""Qualification tests for the TR-EIF observable trace schema contract."""

from tr_eif.energy import EnergyState, ForceState, StressState
from tr_eif.observables import (
    TraceRecord,
    TraceSequence,
    trace_record_to_mapping,
    trace_sequence_to_mapping,
)
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)


def _make_execution_vector() -> TernaryExecutionVector:
    """Construct a trace fixture containing all retained ternary states."""

    return TernaryExecutionVector(
        states=(
            TernaryExecutionState(
                retained_state=TernaryState.NEGATIVE,
            ),
            TernaryExecutionState(
                retained_state=TernaryState.NEUTRAL,
                pending_target=TernaryState.POSITIVE,
            ),
            TernaryExecutionState(
                retained_state=TernaryState.POSITIVE,
            ),
        )
    )


def test_trace_sequence_declares_format_and_version() -> None:
    """Serialized trace sequences must declare their format contract."""

    sequence = TraceSequence(
        records=(
            TraceRecord(
                step=0,
                time=0.0,
                ternary_execution=_make_execution_vector(),
            ),
        )
    )

    mapping = trace_sequence_to_mapping(sequence)

    assert mapping["format"] == "tr_eif.trace"
    assert mapping["version"] == 1
    assert mapping["record_count"] == 1
    assert mapping["node_count"] == 3


def test_retained_state_and_pending_target_are_separate_fields() -> None:
    """Active neutral and pending target must remain distinct in traces."""

    record = TraceRecord(
        step=4,
        time=1.25,
        ternary_execution=_make_execution_vector(),
    )

    mapping = trace_record_to_mapping(record)
    execution = mapping["ternary_execution"]

    assert execution[0]["retained_state"] == -1
    assert execution[0]["pending_target"] is None

    assert execution[1]["retained_state"] == 0
    assert execution[1]["pending_target"] == 1

    assert execution[2]["retained_state"] == 1
    assert execution[2]["pending_target"] is None


def test_missing_observables_are_serialized_as_null_values() -> None:
    """Missing observables must remain distinct from ternary neutral."""

    record = TraceRecord(
        step=0,
        time=0.0,
        ternary_execution=_make_execution_vector(),
    )

    mapping = trace_record_to_mapping(record)

    assert mapping["energy"] is None
    assert mapping["forces"] is None
    assert mapping["stress"] is None

    assert mapping["ternary_execution"][1]["retained_state"] == 0


def test_present_observables_preserve_structural_fields() -> None:
    """Present observables must retain their explicit trace structure."""

    record = TraceRecord(
        step=2,
        time=0.5,
        ternary_execution=_make_execution_vector(),
        energy=EnergyState.from_atomic_energies(
            (-1.0, 0.25, 0.75)
        ),
        forces=ForceState(
            forces=(
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (-1.0, 0.0, 0.0),
            )
        ),
        stress=StressState(
            tensor=(
                (1.0, 0.0, 0.0),
                (0.0, 2.0, 0.0),
                (0.0, 0.0, 3.0),
            )
        ),
    )

    mapping = trace_record_to_mapping(record)

    assert mapping["step"] == 2
    assert mapping["time"] == 0.5
    assert mapping["node_count"] == 3

    assert mapping["energy"] is not None
    assert mapping["energy"]["atomic_energies"] == (
        -1.0,
        0.25,
        0.75,
    )
    assert mapping["energy"]["total_energy"] == 0.0

    assert mapping["forces"] is not None
    assert mapping["forces"]["forces"] == (
        (1.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
    )

    assert mapping["stress"] is not None
    assert mapping["stress"]["tensor"] == (
        (1.0, 0.0, 0.0),
        (0.0, 2.0, 0.0),
        (0.0, 0.0, 3.0),
    )


def test_sequence_preserves_record_order() -> None:
    """Trace serialization must preserve chronological record order."""

    execution = _make_execution_vector()

    sequence = TraceSequence(
        records=(
            TraceRecord(
                step=2,
                time=0.25,
                ternary_execution=execution,
            ),
            TraceRecord(
                step=5,
                time=0.75,
                ternary_execution=execution,
            ),
            TraceRecord(
                step=9,
                time=1.5,
                ternary_execution=execution,
            ),
        )
    )

    mapping = trace_sequence_to_mapping(sequence)

    assert tuple(
        record["step"]
        for record in mapping["records"]
    ) == (
        2,
        5,
        9,
    )

    assert tuple(
        record["time"]
        for record in mapping["records"]
    ) == (
        0.25,
        0.75,
        1.5,
    )
