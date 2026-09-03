"""Deterministic trace serialization for TR-EIF."""

from __future__ import annotations

from typing import Any

from .sequence import TraceSequence
from .trace import TraceRecord


def trace_record_to_mapping(
    record: TraceRecord,
) -> dict[str, Any]:
    """Convert one trace record to a deterministic serializable mapping."""

    if not isinstance(record, TraceRecord):
        raise TypeError(
            "record must be a TraceRecord instance."
        )

    ternary_nodes = tuple(
        {
            "retained_state": int(state.retained_state),
            "pending_target": (
                None
                if state.pending_target is None
                else int(state.pending_target)
            ),
        }
        for state in record.ternary_execution.states
    )

    energy = None
    if record.energy is not None:
        energy = {
            "atomic_energies": record.energy.atomic_energies,
            "total_energy": record.energy.total_energy,
        }

    forces = None
    if record.forces is not None:
        forces = {
            "forces": record.forces.forces,
        }

    stress = None
    if record.stress is not None:
        stress = {
            "tensor": record.stress.tensor,
        }

    return {
        "step": record.step,
        "time": record.time,
        "node_count": record.node_count,
        "ternary_execution": ternary_nodes,
        "energy": energy,
        "forces": forces,
        "stress": stress,
    }


def trace_sequence_to_mapping(
    sequence: TraceSequence,
) -> dict[str, Any]:
    """Convert an ordered trace sequence to a serializable mapping."""

    if not isinstance(sequence, TraceSequence):
        raise TypeError(
            "sequence must be a TraceSequence instance."
        )

    return {
        "format": "tr_eif.trace",
        "version": 1,
        "record_count": sequence.record_count,
        "node_count": sequence.node_count,
        "records": tuple(
            trace_record_to_mapping(record)
            for record in sequence.records
        ),
    }
