
"""Cutoff-aware pressure-volume accounting for FLiBe rank-two TR-EIP MD.

Each completed isotropic barostat step has a continuous affine deformation on
its pre-barostat graph followed by a cutoff-graph refresh at the same final
geometry. This operator reconciles the pressure-volume ledger with the
independent reference/rank-two graph energy partition. It records frozen-graph
pressure work, finite-step quadrature residual and discrete graph-event energy
separately while preserving all scheduled resonance and ternary boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_cutoff_energy_partition import (
    FLiBeRankTwoTREIPCutoffEnergyPartition,
    evaluate_flibe_rank_two_cutoff_energy_partition,
)
from .rank_two_tr_eip_pressure_volume_work import (
    FLiBeRankTwoTREIPPressureVolumeWorkInterval,
    FLiBeRankTwoTREIPPressureVolumeWorkLedger,
)


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _close(actual: float, expected: float, name: str, *, absolute: float = 0.0) -> None:
    if not isfinite(actual) or not isfinite(expected) or not isclose(
        actual, expected, rel_tol=1e-9, abs_tol=absolute,
    ):
        raise ValueError(f"{name} differs from its recorded boundary.")


def _channels(values: tuple[float, float, float], energy_factor: float) -> tuple[float, float, float]:
    return tuple(value * energy_factor for value in values)


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPCutoffPressureWorkInterval:
    """One model-resolved graph event joined to its original barostat work."""

    index: int
    partition: FLiBeRankTwoTREIPCutoffEnergyPartition
    pressure_work: FLiBeRankTwoTREIPPressureVolumeWorkInterval
    energy_unit_to_joule: float
    coordinate_unit_to_meter: float
    potential_stress_unit_to_pascal: float

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise TypeError("index must be an integer.")
        if self.index < 0:
            raise ValueError("index must be nonnegative.")
        if not isinstance(self.partition, FLiBeRankTwoTREIPCutoffEnergyPartition):
            raise TypeError("partition must be FLiBeRankTwoTREIPCutoffEnergyPartition.")
        if not isinstance(self.pressure_work, FLiBeRankTwoTREIPPressureVolumeWorkInterval):
            raise TypeError("pressure_work must be FLiBeRankTwoTREIPPressureVolumeWorkInterval.")
        energy_factor = _positive(self.energy_unit_to_joule, "energy_unit_to_joule")
        length_factor = _positive(self.coordinate_unit_to_meter, "coordinate_unit_to_meter")
        stress_factor = _positive(self.potential_stress_unit_to_pascal, "potential_stress_unit_to_pascal")
        if self.index != self.pressure_work.interval_index:
            raise ValueError("interval index differs from the source pressure work.")
        _close(energy_factor / length_factor**3, stress_factor, "SI stress conversion")

        p = self.partition
        source = self.pressure_work
        _close(p.stress_before.reference_volume * length_factor**3,
               source.volume_before_m3, "pre-barostat volume")
        _close(p.stress_frozen_after.reference_volume * length_factor**3,
               source.volume_after_m3, "post-barostat volume")
        _close(p.volume_change * length_factor**3, source.volume_change_m3,
               "affine volume change", absolute=1e-45)
        _close(p.stress_before.potential_pressure * stress_factor,
               source.potential_pressure_before_pa, "initial potential pressure", absolute=1e-6)
        _close(p.stress_refreshed_after.potential_pressure * stress_factor,
               source.potential_pressure_after_pa, "refreshed potential pressure", absolute=1e-6)
        _close(self.affine_energy_change_j[2] + self.graph_event_energy_change_j[2],
               source.affine_potential_change_j, "complete barostat energy", absolute=1e-28)
        _close(self.original_pressure_work_j, source.trapezoidal_potential_work_j,
               "original trapezoidal pressure work", absolute=1e-28)
        _close(self.total_pressure_work_residual_j,
               fsum((self.frozen_graph_quadrature_residual_j,
                     self.graph_event_energy_change_j[2])),
               "cutoff-aware residual decomposition", absolute=1e-28)

    @property
    def has_graph_event(self) -> bool:
        return self.partition.has_graph_event

    @property
    def affine_energy_change_j(self) -> tuple[float, float, float]:
        """Reference, rank-two and total deformation energy in joules."""
        return _channels(self.partition.affine_energy_change, self.energy_unit_to_joule)

    @property
    def graph_event_energy_change_j(self) -> tuple[float, float, float]:
        """Reference, rank-two and total topology-update increment in joules."""
        return _channels(self.partition.graph_event_energy_change, self.energy_unit_to_joule)

    @property
    def total_energy_change_j(self) -> tuple[float, float, float]:
        """Total affine plus graph-event potential energy in joules."""
        return _channels(self.partition.total_energy_change, self.energy_unit_to_joule)

    @property
    def frozen_graph_pressure_work_j(self) -> tuple[float, float, float]:
        """Three pressure-work channels evaluated before the graph is refreshed."""
        return _channels(self.partition.frozen_graph_pressure_work, self.energy_unit_to_joule)

    @property
    def frozen_graph_quadrature_residual_j(self) -> float:
        """Smooth-branch energy minus frozen-graph pressure quadrature."""
        return self.partition.frozen_graph_quadrature_residual[2] * self.energy_unit_to_joule

    @property
    def total_pressure_work_residual_j(self) -> float:
        """Complete potential energy minus frozen-graph work; includes graph jump."""
        return self.partition.full_pressure_work_residual[2] * self.energy_unit_to_joule

    @property
    def original_pressure_work_j(self) -> float:
        """Legacy quadrature using pressure after the graph refresh."""
        before = self.pressure_work.potential_pressure_before_pa
        after = self.pressure_work.potential_pressure_after_pa
        return -0.5 * fsum((before, after)) * self.pressure_work.volume_change_m3


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPCutoffPressureWorkLedger:
    """Cutoff-aware work across the unmodified pressure-coupled MD trajectory."""

    source: FLiBeRankTwoTREIPPressureVolumeWorkLedger
    intervals: tuple[FLiBeRankTwoTREIPCutoffPressureWorkInterval, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, FLiBeRankTwoTREIPPressureVolumeWorkLedger):
            raise TypeError("source must be FLiBeRankTwoTREIPPressureVolumeWorkLedger.")
        if not isinstance(self.intervals, tuple) or len(self.intervals) != len(self.source.intervals):
            raise ValueError("cutoff intervals must align with all source intervals.")
        trajectory = self.source.observables.trajectory
        for index, (item, original, step) in enumerate(zip(
            self.intervals, self.source.intervals, trajectory.steps, strict=True,
        )):
            if not isinstance(item, FLiBeRankTwoTREIPCutoffPressureWorkInterval):
                raise TypeError("intervals must contain typed cutoff pressure work records.")
            if item.index != index or item.pressure_work != original:
                raise ValueError("cutoff work interval ordering or source differs.")
            partition = item.partition
            if partition.reference != step.barostat.stress_trace.coupled.after_mechanics:
                raise ValueError("cutoff partition must originate at the mechanical boundary.")
            if partition.graph_after != step.barostat.after_barostat.evaluation.graph:
                raise ValueError("cutoff graph differs from post-barostat evaluation.")
            if partition.refreshed_energy != step.barostat.after_barostat.evaluation.augmented_result:
                raise ValueError("refreshed energy differs from post-barostat evaluation.")
            if partition.stress_before != step.barostat.stress_trace.after_mechanics.stress:
                raise ValueError("pre-barostat stress differs from the partition.")
            if partition.stress_refreshed_after != step.barostat.after_barostat.stress:
                raise ValueError("post-barostat stress differs from the partition.")
            _close(item.partition.linear_scale, step.barostat.linear_scale,
                   "barostat linear scale")
            _close(item.energy_unit_to_joule, self.source.observables.energy_unit_to_joule,
                   "energy unit conversion")
            _close(item.coordinate_unit_to_meter, step.pressure.coordinate_unit_to_meter,
                   "coordinate unit conversion")
            _close(item.potential_stress_unit_to_pascal,
                   step.barostat.potential_stress_unit_to_pascal,
                   "stress unit conversion")
        _close(self.total_affine_energy_change_j + self.total_graph_event_energy_change_j,
               self.source.affine_potential_change_j,
               "cumulative barostat potential energy", absolute=1e-27)

    @property
    def graph_event_count(self) -> int:
        return sum(item.has_graph_event for item in self.intervals)

    @property
    def directed_edges_added(self) -> int:
        return sum(len(item.partition.added_edges) for item in self.intervals)

    @property
    def directed_edges_removed(self) -> int:
        return sum(len(item.partition.removed_edges) for item in self.intervals)

    @property
    def total_affine_energy_change_j(self) -> float:
        return fsum(item.affine_energy_change_j[2] for item in self.intervals)

    @property
    def total_graph_event_energy_change_j(self) -> float:
        return fsum(item.graph_event_energy_change_j[2] for item in self.intervals)

    @property
    def frozen_graph_pressure_work_j(self) -> float:
        return fsum(item.frozen_graph_pressure_work_j[2] for item in self.intervals)

    @property
    def frozen_graph_quadrature_residual_j(self) -> float:
        return fsum(item.frozen_graph_quadrature_residual_j for item in self.intervals)

    @property
    def total_pressure_work_residual_j(self) -> float:
        return fsum(item.total_pressure_work_residual_j for item in self.intervals)


def evaluate_flibe_rank_two_cutoff_pressure_work(
    source: FLiBeRankTwoTREIPPressureVolumeWorkLedger,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    cutoff: float,
) -> FLiBeRankTwoTREIPCutoffPressureWorkLedger:
    """Reconcile each recorded barostat update with its frozen-graph energy path.

    All quantities in the existing trajectory and pressure-volume work ledger
    remain unchanged. Reference and rank-two affine work is computed against
    the original mechanical graph; refreshed-graph energy is counted as a
    distinct event at the final cell geometry.
    """
    if not isinstance(source, FLiBeRankTwoTREIPPressureVolumeWorkLedger):
        raise TypeError("source must be FLiBeRankTwoTREIPPressureVolumeWorkLedger.")
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError("stress_evaluator must be RankTwoConservativeStressEvaluator.")
    checked_cutoff = _positive(cutoff, "cutoff")
    entries = []
    for index, (original, step) in enumerate(zip(
        source.intervals, source.observables.trajectory.steps, strict=True,
    )):
        partition = evaluate_flibe_rank_two_cutoff_energy_partition(
            model,
            stress_evaluator,
            step.barostat.stress_trace.coupled.after_mechanics,
            cutoff=checked_cutoff,
            linear_scale=step.barostat.linear_scale,
        )
        entries.append(FLiBeRankTwoTREIPCutoffPressureWorkInterval(
            index=index,
            partition=partition,
            pressure_work=original,
            energy_unit_to_joule=source.observables.energy_unit_to_joule,
            coordinate_unit_to_meter=step.pressure.coordinate_unit_to_meter,
            potential_stress_unit_to_pascal=step.barostat.potential_stress_unit_to_pascal,
        ))
    return FLiBeRankTwoTREIPCutoffPressureWorkLedger(
        source=source, intervals=tuple(entries),
    )
