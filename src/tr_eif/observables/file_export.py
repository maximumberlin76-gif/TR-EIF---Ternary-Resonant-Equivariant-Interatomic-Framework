"""File export for canonical TR-EIF observable traces."""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import TypeAlias

from .json_export import trace_sequence_to_json_bytes
from .sequence import TraceSequence

PathInput: TypeAlias = str | PathLike[str]


def write_trace_sequence_json(
    sequence: TraceSequence,
    path: PathInput,
) -> int:
    """Write canonical trace JSON bytes and return the byte count."""

    if not isinstance(sequence, TraceSequence):
        raise TypeError(
            "sequence must be a TraceSequence instance."
        )

    if not isinstance(path, (str, PathLike)):
        raise TypeError(
            "path must be a string or path-like object."
        )

    destination = Path(path)
    payload = trace_sequence_to_json_bytes(sequence)

    with destination.open("wb") as stream:
        written = stream.write(payload)

    if written != len(payload):
        raise OSError(
            "trace export did not write the complete canonical payload."
        )

    return written
