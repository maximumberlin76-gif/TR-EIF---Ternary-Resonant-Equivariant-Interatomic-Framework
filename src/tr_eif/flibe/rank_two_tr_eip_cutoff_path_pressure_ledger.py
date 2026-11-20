"""Piecewise cutoff-aware pressure work for FLiBe rank-two TR-EIP MD.

Reconcile the existing multi-interval barostat ledger with the analytically
localized cutoff path. Within each interval, homogeneous cell deformation is
partitioned into fixed-graph segments and individual graph-replacement events.
The exact full-energy difference is compared with the endpoint graph partition;
the smooth-work quadrature and localized graph jumps remain separate records.

Continuous resonance features and retained balanced-ternary execution are
frozen along each affine path. The source MD, resonance and ternary schedules,
kinetic pressure, thermodynamic coordinates and SI conversions are preserved.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_cutoff_path_work import (
    FLiBeRankTwoCutoffPathWork,
    evaluate_flibe_rank_two_cutoff_path_work,
)
from .rank_two_tr_eip_cutoff_pressure_work import (
    FLiBeRankTwoTREIPCutoffPressureWorkInterval,
    FLiBeRankTwoTREIPCutoffPressureWorkLedger,
)


def _close(
    actual: float,
    expected: float,
    name: str,
    *,
    absolute: float = 1e-30,
) -> None:
    if not isfinite(actual) or not isfinite(expected) or not isclose(
        actual, expected, rel_tol=1e-9, abs_tol=absolute,
    ):
        raise ValueError(
            f"{name} differs from the recorded energy boundary."
        )


def _to_joule(
    values: tuple[float, float, float],
    factor: float,
) -> tuple[float, float, float]:
    return tuple(value * factor for value in values)


def _sum_channels(
    intervals: tuple[FLiBeRankTwoCutoffPathPressureInterval, ...],
    attribute: str,
) -> tuple[float, float, float]:
    return tuple(
        fsum(getattr(item, attribute)[k] for item in intervals)
        for k in range(3)
    )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathPressureInterval:
    """One barostat interval resolved into smooth paths and cutoff jumps."""

    index: int
    original: FLiBeRankTwoTREIPCutoffPressureWorkInterval
    path: FLiBeRankTwoCutoffPathWork

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise TypeError("index must be an integer.")
        if self.index < 0:
            raise ValueError("index must be nonnegative.")
        if not isinstance(
            self.original, FLiBeRankTwoTREIPCutoffPressureWorkInterval
        ):
            raise TypeError(
                "original must be FLiBeRankTwoTREIPCutoffPressureWorkInterval."
            )
        if not isinstance(self.path, FLiBeRankTwoCutoffPathWork):
            raise TypeError("path must be FLiBeRankTwoCutoffPathWork.")
        if self.index != self.original.index:
            raise ValueError(
                "path interval index differs from cutoff ledger index."
            )

        partition = self.original.partition
        scan = self.path.scan

        if scan.reference != partition.reference:
            raise ValueError(
                "path and endpoint partition have different input states."
            )
        if (
            scan.cutoff != partition.cutoff
            or scan.target_linear_scale != partition.linear_scale
        ):
            raise ValueError(
                "path and endpoint partition have different cutoff or cell scale."
            )
        if scan.target_graph != partition.graph_after:
            raise ValueError(
                "path and endpoint partition have different final graphs."
            )
        if self.path.segments[0].initial_stress != partition.stress_before:
            raise ValueError(
                "path and endpoint partition have different initial stresses."
            )
        if (
            self.path.segments[-1].final_stress
            != partition.stress_refreshed_after
        ):
            raise ValueError(
                "path and endpoint partition have different final stresses."
            )

        added = {
            edge
            for event in scan.crossings
            for edge in event.added_edges
        }
        removed = {
            edge
            for event in scan.crossings
            for edge in event.removed_edges
        }

        if (
            added != set(partition.added_edges)
            or removed != set(partition.removed_edges)
        ):
            raise ValueError(
                "localized cutoff events differ from the endpoint edge inventory."
            )
        if (scan.crossing_count > 0) != partition.has_graph_event:
            raise ValueError(
                "localized and endpoint graph-event classifications differ."
            )

        factor = self.original.energy_unit_to_joule
        length = self.original.coordinate_unit_to_meter

        if (
            isinstance(factor, bool)
            or not isinstance(factor, (float, int))
            or not isfinite(factor)
            or factor <= 0.0
        ):
            raise ValueError(
                "energy conversion must be finite and positive."
            )
        if not isfinite(length) or length <= 0.0:
            raise ValueError(
                "length conversion must be finite and positive."
            )

        _close(
            self.path.volume_change * length**3,
            self.original.pressure_work.volume_change_m3,
            "path volume change",
            absolute=1e-45,
        )

        for channel in range(3):
            _close(
                self.total_energy_change_j[channel],
                self.original.total_energy_change_j[channel],
                "complete pressure-volume energy",
                absolute=1e-29,
            )
            _close(
                self.total_energy_change_j[channel],
                fsum((
                    self.smooth_energy_change_j[channel],
                    self.localized_graph_energy_change_j[channel],
                )),
                "piecewise energy partition",
                absolute=1e-29,
            )
            _close(
                self.total_pressure_work_residual_j[channel],
                fsum((
                    self.smooth_quadrature_residual_j[channel],
                    self.localized_graph_energy_change_j[channel],
                )),
                "piecewise pressure-work residual",
                absolute=1e-29,
            )
            _close(
                self.localized_minus_endpoint_jump_j[channel],
                self.original.affine_energy_change_j[channel]
                - self.smooth_energy_change_j[channel],
                "smooth and endpoint graph partition reconciliation",
                absolute=1e-29,
            )

    @property
    def crossing_count(self) -> int:
        return self.path.scan.crossing_count

    @property
    def smooth_segment_count(self) -> int:
        return len(self.path.segments)

    @property
    def smooth_energy_change_j(self) -> tuple[float, float, float]:
        """Reference, rank-two and total fixed-graph energy changes in joules."""
        return _to_joule(
            self.path.smooth_energy_change,
            self.original.energy_unit_to_joule,
        )

    @property
    def localized_graph_energy_change_j(
        self,
    ) -> tuple[float, float, float]:
        """Energy jumps evaluated at their respective critical geometries."""
        return _to_joule(
            self.path.localized_graph_energy_change,
            self.original.energy_unit_to_joule,
        )

    @property
    def total_energy_change_j(self) -> tuple[float, float, float]:
        return _to_joule(
            self.path.total_energy_change,
            self.original.energy_unit_to_joule,
        )

    @property
    def smooth_pressure_work_j(self) -> tuple[float, float, float]:
        """Sum of trapezoidal -P dV estimates for fixed-graph segments."""
        return _to_joule(
            self.path.trapezoidal_pressure_work,
            self.original.energy_unit_to_joule,
        )

    @property
    def smooth_quadrature_residual_j(
        self,
    ) -> tuple[float, float, float]:
        return _to_joule(
            self.path.smooth_quadrature_residual,
            self.original.energy_unit_to_joule,
        )

    @property
    def total_pressure_work_residual_j(
        self,
    ) -> tuple[float, float, float]:
        """Complete energy change minus the piecewise smooth-work estimate."""
        return _to_joule(
            self.path.total_pressure_work_residual,
            self.original.energy_unit_to_joule,
        )

    @property
    def localized_minus_endpoint_jump_j(
        self,
    ) -> tuple[float, float, float]:
        """Difference between crossing-local and endpoint graph-event conventions."""
        return tuple(
            a - b
            for a, b in zip(
                self.localized_graph_energy_change_j,
                self.original.graph_event_energy_change_j,
                strict=True,
            )
        )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathPressureLedger:
    """Piecewise cutoff work reconciled with the original multi-step MD ledger."""

    source: FLiBeRankTwoTREIPCutoffPressureWorkLedger
    intervals: tuple[FLiBeRankTwoCutoffPathPressureInterval, ...]

    def __post_init__(self) -> None:
        if not isinstance(
            self.source, FLiBeRankTwoTREIPCutoffPressureWorkLedger
        ):
            raise TypeError(
                "source must be FLiBeRankTwoTREIPCutoffPressureWorkLedger."
            )
        if (
            not isinstance(self.intervals, tuple)
            or len(self.intervals) != len(self.source.intervals)
        ):
            raise ValueError(
                "path intervals must align with the cutoff pressure-work ledger."
            )

        for index, (record, original) in enumerate(
            zip(self.intervals, self.source.intervals, strict=True)
        ):
            if not isinstance(
                record, FLiBeRankTwoCutoffPathPressureInterval
            ):
                raise TypeError(
                    "intervals must contain typed piecewise work records."
                )
            if record.index != index or record.original != original:
                raise ValueError(
                    "piecewise work interval order or source differs."
                )

        event_intervals = sum(
            int(item.crossing_count > 0)
            for item in self.intervals
        )
        if event_intervals != self.source.graph_event_count:
            raise ValueError(
                "localized and endpoint graph-event interval counts differ."
            )
        if (
            self.directed_edges_added != self.source.directed_edges_added
            or self.directed_edges_removed
            != self.source.directed_edges_removed
        ):
            raise ValueError(
                "localized and endpoint directed-edge inventories differ."
            )

        _close(
            self.total_energy_change_j[2],
            self.source.source.affine_potential_change_j,
            "cumulative potential energy",
            absolute=1e-28,
        )

        for channel in range(3):
            _close(
                self.total_energy_change_j[channel],
                fsum((
                    self.smooth_energy_change_j[channel],
                    self.localized_graph_energy_change_j[channel],
                )),
                "cumulative piecewise energy",
                absolute=1e-28,
            )
            _close(
                self.total_pressure_work_residual_j[channel],
                fsum((
                    self.smooth_quadrature_residual_j[channel],
                    self.localized_graph_energy_change_j[channel],
                )),
                "cumulative pressure-work residual",
                absolute=1e-28,
            )

    @property
    def crossing_count(self) -> int:
        return sum(
            item.crossing_count for item in self.intervals
        )

    @property
    def smooth_segment_count(self) -> int:
        return sum(
            item.smooth_segment_count for item in self.intervals
        )

    @property
    def directed_edges_added(self) -> int:
        return sum(
            item.path.scan.directed_edges_added
            for item in self.intervals
        )

    @property
    def directed_edges_removed(self) -> int:
        return sum(
            item.path.scan.directed_edges_removed
            for item in self.intervals
        )

    @property
    def smooth_energy_change_j(self) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "smooth_energy_change_j"
        )

    @property
    def localized_graph_energy_change_j(
        self,
    ) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "localized_graph_energy_change_j"
        )

    @property
    def total_energy_change_j(self) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "total_energy_change_j"
        )

    @property
    def smooth_pressure_work_j(self) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "smooth_pressure_work_j"
        )

    @property
    def smooth_quadrature_residual_j(
        self,
    ) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "smooth_quadrature_residual_j"
        )

    @property
    def total_pressure_work_residual_j(
        self,
    ) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "total_pressure_work_residual_j"
        )

    @property
    def localized_minus_endpoint_jump_j(
        self,
    ) -> tuple[float, float, float]:
        return _sum_channels(
            self.intervals, "localized_minus_endpoint_jump_j"
        )


def evaluate_flibe_rank_two_cutoff_path_pressure_ledger(
    source: FLiBeRankTwoTREIPCutoffPressureWorkLedger,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    cutoff: float,
    probe_relative_width: float = 1e-7,
) -> FLiBeRankTwoCutoffPathPressureLedger:
    """Resolve every recorded pressure-coupled cell update into its cutoff path.

    The source trajectory and its event, mechanical and barostat records are
    retained unchanged. Each graph jump is recorded at its critical scale,
    while the original endpoint graph-jump convention remains accessible.
    """
    if not isinstance(
        source, FLiBeRankTwoTREIPCutoffPressureWorkLedger
    ):
        raise TypeError(
            "source must be FLiBeRankTwoTREIPCutoffPressureWorkLedger."
        )
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError(
            "model must be FLiBeRankTwoTREIPModel."
        )
    if not isinstance(
        stress_evaluator, RankTwoConservativeStressEvaluator
    ):
        raise TypeError(
            "stress_evaluator must be RankTwoConservativeStressEvaluator."
        )
    if isinstance(cutoff, bool) or not isinstance(
        cutoff, (int, float)
    ):
        raise TypeError(
            "cutoff must be a real non-Boolean number."
        )
    if not isfinite(cutoff) or cutoff <= 0.0:
        raise ValueError(
            "cutoff must be finite and positive."
        )

    entries: list[FLiBeRankTwoCutoffPathPressureInterval] = []

    for index, original in enumerate(source.intervals):
        path = evaluate_flibe_rank_two_cutoff_path_work(
            model,
            stress_evaluator,
            original.partition.reference,
            cutoff=cutoff,
            target_linear_scale=original.partition.linear_scale,
            probe_relative_width=probe_relative_width,
        )
        entries.append(
            FLiBeRankTwoCutoffPathPressureInterval(
                index=index,
                original=original,
                path=path,
            )
        )

    return FLiBeRankTwoCutoffPathPressureLedger(
        source=source,
        intervals=tuple(entries),
    )
