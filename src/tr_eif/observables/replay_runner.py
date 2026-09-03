"""Deterministic replay execution boundary for TR-EIF."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .replay import ReplayComparison, compare_trace_replay
from .sequence import TraceSequence

TraceProducer = Callable[[], TraceSequence]


@dataclass(frozen=True, slots=True)
class ReplayRun:
    """Result of two executions of one deterministic trace producer."""

    reference: TraceSequence
    candidate: TraceSequence
    comparison: ReplayComparison

    def __post_init__(self) -> None:
        if not isinstance(self.reference, TraceSequence):
            raise TypeError(
                "reference must be a TraceSequence instance."
            )

        if not isinstance(self.candidate, TraceSequence):
            raise TypeError(
                "candidate must be a TraceSequence instance."
            )

        if not isinstance(self.comparison, ReplayComparison):
            raise TypeError(
                "comparison must be a ReplayComparison instance."
            )


def run_deterministic_replay(
    producer: TraceProducer,
) -> ReplayRun:
    """Execute one trace producer twice and compare canonical outputs."""

    if not callable(producer):
        raise TypeError("producer must be callable.")

    reference = producer()

    if not isinstance(reference, TraceSequence):
        raise TypeError(
            "producer must return a TraceSequence instance."
        )

    candidate = producer()

    if not isinstance(candidate, TraceSequence):
        raise TypeError(
            "producer must return a TraceSequence instance."
        )

    comparison = compare_trace_replay(
        reference=reference,
        candidate=candidate,
    )

    return ReplayRun(
        reference=reference,
        candidate=candidate,
        comparison=comparison,
    )
