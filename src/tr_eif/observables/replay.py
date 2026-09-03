"""Deterministic replay comparison for TR-EIF observable traces."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from .json_export import trace_sequence_to_json_bytes
from .sequence import TraceSequence


@dataclass(frozen=True, slots=True)
class ReplayComparison:
    """Immutable result of canonical trace replay comparison."""

    reference_digest: str
    candidate_digest: str
    byte_identical: bool
    reference_size: int
    candidate_size: int

    def __post_init__(self) -> None:
        for field_name, digest in (
            ("reference_digest", self.reference_digest),
            ("candidate_digest", self.candidate_digest),
        ):
            if not isinstance(digest, str):
                raise TypeError(
                    f"{field_name} must be a string."
                )

            if len(digest) != 64:
                raise ValueError(
                    f"{field_name} must be a SHA-256 hexadecimal digest."
                )

            try:
                int(digest, 16)
            except ValueError as error:
                raise ValueError(
                    f"{field_name} must be a SHA-256 hexadecimal digest."
                ) from error

        if not isinstance(self.byte_identical, bool):
            raise TypeError(
                "byte_identical must be a boolean."
            )

        for field_name, size in (
            ("reference_size", self.reference_size),
            ("candidate_size", self.candidate_size),
        ):
            if not isinstance(size, int) or isinstance(size, bool):
                raise TypeError(
                    f"{field_name} must be an integer."
                )

            if size < 0:
                raise ValueError(
                    f"{field_name} must be nonnegative."
                )


def compare_trace_replay(
    reference: TraceSequence,
    candidate: TraceSequence,
) -> ReplayComparison:
    """Compare two trace sequences by their canonical serialized bytes."""

    if not isinstance(reference, TraceSequence):
        raise TypeError(
            "reference must be a TraceSequence instance."
        )

    if not isinstance(candidate, TraceSequence):
        raise TypeError(
            "candidate must be a TraceSequence instance."
        )

    reference_bytes = trace_sequence_to_json_bytes(reference)
    candidate_bytes = trace_sequence_to_json_bytes(candidate)

    return ReplayComparison(
        reference_digest=sha256(reference_bytes).hexdigest(),
        candidate_digest=sha256(candidate_bytes).hexdigest(),
        byte_identical=reference_bytes == candidate_bytes,
        reference_size=len(reference_bytes),
        candidate_size=len(candidate_bytes),
    )
