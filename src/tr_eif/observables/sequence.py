"""Ordered observable trace sequences for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .trace import TraceRecord


@dataclass(frozen=True, slots=True)
class TraceSequence:
    """Immutable ordered sequence of TR-EIF trace records."""

    records: tuple[TraceRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple):
            raise TypeError("records must be a tuple.")

        if len(self.records) == 0:
            raise ValueError("records must not be empty.")

        for index, record in enumerate(self.records):
            if not isinstance(record, TraceRecord):
                raise TypeError(
                    f"records[{index}] must be a TraceRecord instance."
                )

        node_count = self.records[0].node_count

        for index, record in enumerate(
            self.records[1:],
            start=1,
        ):
            previous = self.records[index - 1]

            if record.node_count != node_count:
                raise ValueError(
                    "all trace records must have the same node count."
                )

            if record.step <= previous.step:
                raise ValueError(
                    "trace record steps must be strictly increasing."
                )

            if record.time < previous.time:
                raise ValueError(
                    "trace record times must be nondecreasing."
                )

    @property
    def record_count(self) -> int:
        """Return the number of trace records."""

        return len(self.records)

    @property
    def node_count(self) -> int:
        """Return the common number of nodes."""

        return self.records[0].node_count

    @property
    def first(self) -> TraceRecord:
        """Return the first trace record."""

        return self.records[0]

    @property
    def last(self) -> TraceRecord:
        """Return the last trace record."""

        return self.records[-1]
