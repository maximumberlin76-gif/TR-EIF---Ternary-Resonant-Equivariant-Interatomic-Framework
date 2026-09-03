"""Canonical JSON export for TR-EIF observable traces."""

from __future__ import annotations

import json

from .sequence import TraceSequence
from .serialization import trace_sequence_to_mapping


def trace_sequence_to_json(
    sequence: TraceSequence,
) -> str:
    """Return the canonical JSON representation of a trace sequence."""

    if not isinstance(sequence, TraceSequence):
        raise TypeError(
            "sequence must be a TraceSequence instance."
        )

    mapping = trace_sequence_to_mapping(sequence)

    return json.dumps(
        mapping,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def trace_sequence_to_json_bytes(
    sequence: TraceSequence,
) -> bytes:
    """Return canonical UTF-8 JSON bytes for a trace sequence."""

    return trace_sequence_to_json(sequence).encode("utf-8")
