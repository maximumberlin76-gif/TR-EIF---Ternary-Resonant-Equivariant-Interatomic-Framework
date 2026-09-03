"""Qualification tests for deterministic TR-EIF trace replay."""

from tr_eif.energy import EnergyState, ForceState, StressState
from tr_eif.observables import (
    TraceRecord,
    TraceSequence,
    compare_trace_replay,
    run_deterministic_replay,
    trace_sequence_to_json_bytes,
)
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)


def _make_trace_sequence() -> TraceSequence:
    """Construct one deterministic reference trace sequence."""

    execution = TernaryExecutionVector(
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

    energy = EnergyState.from_atomic_energies(
        (
            -1.25,
            0.50,
            0.75,
        )
    )

    forces = ForceState(
        forces=(
            (1.0, 0.0, -1.0),
            (0.0, 0.5, 0.0),
            (-1.0, 0.0, 1.0),
        )
    )

    stress = StressState(
        tensor=(
            (1.0, 0.1, 0.2),
            (0.1, 2.0, 0.3),
            (0.2, 0.3, 3.0),
        )
    )

    first = TraceRecord(
        step=0,
        time=0.0,
        ternary_execution=execution,
        energy=energy,
        forces=forces,
        stress=stress,
    )

    second = TraceRecord(
        step=1,
        time=0.25,
        ternary_execution=execution,
        energy=energy,
        forces=forces,
        stress=stress,
    )

    return TraceSequence(
        records=(
            first,
            second,
        )
    )


def test_repeated_serialization_is_byte_identical() -> None:
    """Repeated canonical serialization must produce identical bytes."""

    sequence = _make_trace_sequence()

    first = trace_sequence_to_json_bytes(sequence)
    second = trace_sequence_to_json_bytes(sequence)

    assert first == second


def test_equal_trace_sequences_have_identical_replay_payloads() -> None:
    """Equivalent trace construction must produce identical replay bytes."""

    reference = _make_trace_sequence()
    candidate = _make_trace_sequence()

    comparison = compare_trace_replay(
        reference=reference,
        candidate=candidate,
    )

    assert comparison.byte_identical
    assert comparison.reference_digest == comparison.candidate_digest
    assert comparison.reference_size == comparison.candidate_size


def test_replay_runner_executes_producer_twice() -> None:
    """Replay runner must compare two independently produced traces."""

    call_count = 0

    def producer() -> TraceSequence:
        nonlocal call_count
        call_count += 1
        return _make_trace_sequence()

    result = run_deterministic_replay(producer)

    assert call_count == 2
    assert result.comparison.byte_identical
    assert (
        result.comparison.reference_digest
        == result.comparison.candidate_digest
    )


def test_changed_trace_is_not_byte_identical() -> None:
    """A changed observable value must change canonical replay bytes."""

    reference = _make_trace_sequence()

    execution = reference.last.ternary_execution

    changed_record = TraceRecord(
        step=1,
        time=0.5,
        ternary_execution=execution,
        energy=reference.last.energy,
        forces=reference.last.forces,
        stress=reference.last.stress,
    )

    candidate = TraceSequence(
        records=(
            reference.first,
            changed_record,
        )
    )

    comparison = compare_trace_replay(
        reference=reference,
        candidate=candidate,
    )

    assert not comparison.byte_identical
    assert comparison.reference_digest != comparison.candidate_digest
