"""Qualification tests for deterministic TR-EIF trace file export."""

from pathlib import Path

import pytest

from tr_eif.energy import EnergyState, ForceState, StressState
from tr_eif.observables import (
    TraceRecord,
    TraceSequence,
    trace_sequence_to_json_bytes,
    write_trace_sequence_json,
)
from tr_eif.ternary import (
    TernaryExecutionState,
    TernaryExecutionVector,
    TernaryState,
)


def _make_trace_sequence() -> TraceSequence:
    """Construct a deterministic observable trace fixture."""

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

    return TraceSequence(
        records=(
            TraceRecord(
                step=0,
                time=0.0,
                ternary_execution=execution,
                energy=energy,
                forces=forces,
                stress=stress,
            ),
            TraceRecord(
                step=1,
                time=0.25,
                ternary_execution=execution,
                energy=energy,
                forces=forces,
                stress=stress,
            ),
        )
    )


def test_file_export_matches_canonical_json_bytes(
    tmp_path: Path,
) -> None:
    """File export must contain the exact canonical in-memory payload."""

    sequence = _make_trace_sequence()
    expected = trace_sequence_to_json_bytes(sequence)

    destination = tmp_path / "trace.json"

    written = write_trace_sequence_json(
        sequence,
        destination,
    )

    actual = destination.read_bytes()

    assert written == len(expected)
    assert actual == expected


def test_repeated_file_export_is_byte_identical(
    tmp_path: Path,
) -> None:
    """Repeated exports of one trace must remain byte-identical."""

    sequence = _make_trace_sequence()

    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"

    first_count = write_trace_sequence_json(
        sequence,
        first_path,
    )
    second_count = write_trace_sequence_json(
        sequence,
        second_path,
    )

    first_payload = first_path.read_bytes()
    second_payload = second_path.read_bytes()

    assert first_count == second_count
    assert first_payload == second_payload


def test_reexport_overwrites_with_complete_canonical_payload(
    tmp_path: Path,
) -> None:
    """Existing file contents must be replaced by the canonical payload."""

    sequence = _make_trace_sequence()
    expected = trace_sequence_to_json_bytes(sequence)

    destination = tmp_path / "trace.json"

    destination.write_bytes(
        b"noncanonical-existing-data-that-must-not-remain"
    )

    written = write_trace_sequence_json(
        sequence,
        destination,
    )

    assert written == len(expected)
    assert destination.read_bytes() == expected


def test_string_and_pathlike_destinations_export_same_bytes(
    tmp_path: Path,
) -> None:
    """String and Path destinations must preserve identical payloads."""

    sequence = _make_trace_sequence()

    path_destination = tmp_path / "path-destination.json"
    string_destination = tmp_path / "string-destination.json"

    write_trace_sequence_json(
        sequence,
        path_destination,
    )

    write_trace_sequence_json(
        sequence,
        str(string_destination),
    )

    assert (
        path_destination.read_bytes()
        == string_destination.read_bytes()
    )


def test_file_export_rejects_non_trace_sequence(
    tmp_path: Path,
) -> None:
    """Exporter must reject values outside the TraceSequence contract."""

    destination = tmp_path / "trace.json"

    with pytest.raises(
        TypeError,
        match="sequence must be a TraceSequence instance",
    ):
        write_trace_sequence_json(
            object(),
            destination,
        )

    assert not destination.exists()


@pytest.mark.parametrize(
    "invalid_path",
    (
        1,
        1.0,
        None,
        True,
    ),
)
def test_file_export_rejects_non_path_input(
    invalid_path,
) -> None:
    """Exporter must reject values outside the path-input contract."""

    sequence = _make_trace_sequence()

    with pytest.raises(
        TypeError,
        match="path must be a string or path-like object",
    ):
        write_trace_sequence_json(
            sequence,
            invalid_path,
        )
