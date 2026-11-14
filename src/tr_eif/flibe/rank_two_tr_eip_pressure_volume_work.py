"""Pressure-volume and energy accounting for FLiBe rank-two coupled MD.

Each completed interval registers its event-energy, mechanical-energy and
isotropic-cell contributions separately. The target-pressure energy coordinate
is E + P_target*V, with a fixed target pressure across the trajectory.

A trapezoidal integral of the configurational hydrostatic pressure estimates
potential-energy change over the affine volume update. Its signed difference
from the evaluated energy change is retained as a quadrature diagnostic.
Pressure is sampled at both the pre-barostat and post-barostat boundaries;
resonance, ternary, and mechanical execution remain in the source trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from .rank_two_tr_eip_pressure_coupled_observables import (
    FLiBeRankTwoTREIPPressureCoupledObservables,
    _kinetic_energy_j,
)


def _finite(value: float, label: str, *, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{label} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or (positive and number <= 0.0):
        raise ValueError(f"{label} must be finite and satisfy its sign constraint.")
    return number


def _near(a: float, b: float, label: str, *, absolute: float = 1e-33) -> None:
    if not isclose(a, b, rel_tol=1e-9, abs_tol=absolute):
        raise ValueError(f"{label} differs from its source energy or volume identity.")


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureVolumeWorkInterval:
    """Two pressure boundaries and the separated energy ledger for one interval."""

    interval_index: int
    volume_before_m3: float
    volume_after_m3: float
    volume_change_m3: float
    potential_pressure_before_pa: float
    potential_pressure_after_pa: float
    target_pressure_pa: float
    total_energy_before_j: float
    total_energy_after_j: float
    event_potential_change_j: float
    mechanical_total_change_j: float
    affine_potential_change_j: float
    net_total_energy_change_j: float
    trapezoidal_potential_work_j: float
    pressure_quadrature_residual_j: float
    target_pressure_volume_term_j: float
    target_pressure_energy_change_j: float

    def __post_init__(self) -> None:
        if isinstance(self.interval_index, bool) or not isinstance(self.interval_index, int):
            raise TypeError("interval_index must be an integer.")
        if self.interval_index < 0:
            raise ValueError("interval_index must be nonnegative.")
        for name in (
            "volume_before_m3", "volume_after_m3", "volume_change_m3",
            "potential_pressure_before_pa", "potential_pressure_after_pa",
            "target_pressure_pa", "total_energy_before_j", "total_energy_after_j",
            "event_potential_change_j", "mechanical_total_change_j",
            "affine_potential_change_j", "net_total_energy_change_j",
            "trapezoidal_potential_work_j", "pressure_quadrature_residual_j",
            "target_pressure_volume_term_j", "target_pressure_energy_change_j",
        ):
            _finite(getattr(self, name), name, positive=name in (
                "volume_before_m3", "volume_after_m3",
            ))

        change = self.volume_after_m3 - self.volume_before_m3
        _near(self.volume_change_m3, change, "volume_change_m3", absolute=1e-48)
        _near(
            self.net_total_energy_change_j,
            self.total_energy_after_j - self.total_energy_before_j,
            "net_total_energy_change_j",
        )
        _near(
            self.net_total_energy_change_j,
            fsum((self.event_potential_change_j,
                  self.mechanical_total_change_j,
                  self.affine_potential_change_j)),
            "energy partition",
        )
        trapezoid = -0.5 * (
            self.potential_pressure_before_pa + self.potential_pressure_after_pa
        ) * change
        _near(self.trapezoidal_potential_work_j, trapezoid,
              "trapezoidal_potential_work_j")
        _near(self.pressure_quadrature_residual_j,
              self.affine_potential_change_j - trapezoid,
              "pressure_quadrature_residual_j")
        target_term = self.target_pressure_pa * change
        _near(self.target_pressure_volume_term_j, target_term,
              "target_pressure_volume_term_j")
        _near(self.target_pressure_energy_change_j,
              fsum((self.net_total_energy_change_j, target_term)),
              "target_pressure_energy_change_j")

    @property
    def potential_work_estimate_j(self) -> float:
        """Trapezoidal -integral(P_configurational dV) over the affine cell update."""
        return self.trapezoidal_potential_work_j

    @property
    def target_energy_before_j(self) -> float:
        """Mechanical total energy plus target pressure times pre-update volume."""
        return fsum((self.total_energy_before_j,
                     self.target_pressure_pa * self.volume_before_m3))

    @property
    def target_energy_after_j(self) -> float:
        """Mechanical total energy plus target pressure times scaled volume."""
        return fsum((self.total_energy_after_j,
                     self.target_pressure_pa * self.volume_after_m3))


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureVolumeWorkLedger:
    """Aligned affine pressure-volume diagnostics across an MD trajectory."""

    observables: FLiBeRankTwoTREIPPressureCoupledObservables
    intervals: tuple[FLiBeRankTwoTREIPPressureVolumeWorkInterval, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.observables, FLiBeRankTwoTREIPPressureCoupledObservables):
            raise TypeError("observables must be FLiBeRankTwoTREIPPressureCoupledObservables.")
        if not isinstance(self.intervals, tuple) or len(self.intervals) != len(
            self.observables.samples
        ):
            raise ValueError("interval count must match the observables.")
        trajectory = self.observables.trajectory
        target = trajectory.target_pressure.value
        previous_total: float | None = None
        for index, (interval, sample, step) in enumerate(zip(
            self.intervals, self.observables.samples, trajectory.steps, strict=True
        )):
            if not isinstance(interval, FLiBeRankTwoTREIPPressureVolumeWorkInterval):
                raise TypeError("intervals must contain typed pressure-volume records.")
            if interval.interval_index != index:
                raise ValueError("pressure-volume interval indices must be ordered.")
            _near(interval.volume_before_m3, trajectory.cell_volumes_m3[index],
                  "pre-barostat volume", absolute=0.0)
            _near(interval.volume_after_m3, sample.volume_m3,
                  "post-barostat volume", absolute=0.0)
            _near(interval.volume_before_m3, step.pressure.cell_volume_m3,
                  "pre-barostat pressure volume", absolute=0.0)
            _near(interval.target_pressure_pa, target,
                  "target pressure", absolute=1e-6)
            _near(interval.potential_pressure_before_pa,
                  step.barostat.potential_pressure_pa,
                  "pre-barostat configurational pressure", absolute=1e-6)
            _near(interval.potential_pressure_after_pa,
                  sample.configurational_pressure_pa,
                  "post-barostat configurational pressure", absolute=1e-6)
            for field, expected in (
                ("total_energy_after_j", sample.total_energy_j),
                ("event_potential_change_j", sample.event_potential_energy_change_j),
                ("mechanical_total_change_j", sample.mechanical_total_energy_change_j),
                ("affine_potential_change_j", sample.barostat_potential_energy_change_j),
                ("net_total_energy_change_j", sample.net_total_energy_change_j),
            ):
                _near(getattr(interval, field), expected, field)
            if previous_total is not None:
                _near(interval.total_energy_before_j, previous_total,
                      "inter-interval total-energy continuity")
            previous_total = interval.total_energy_after_j
        _near(self.total_energy_change_j,
              self.final_total_energy_j - self.initial_total_energy_j,
              "trajectory total-energy change")
        _near(self.total_volume_change_m3,
              self.final_volume_m3 - self.initial_volume_m3,
              "trajectory total-volume change", absolute=1e-48)
        _near(self.target_pressure_volume_term_j,
              target * self.total_volume_change_m3,
              "cumulative target pressure-volume contribution")
        _near(self.target_pressure_energy_change_j,
              fsum((self.total_energy_change_j, self.target_pressure_volume_term_j)),
              "cumulative target-pressure energy change")

    @property
    def initial_total_energy_j(self) -> float:
        return self.intervals[0].total_energy_before_j

    @property
    def final_total_energy_j(self) -> float:
        return self.intervals[-1].total_energy_after_j

    @property
    def initial_volume_m3(self) -> float:
        return self.intervals[0].volume_before_m3

    @property
    def final_volume_m3(self) -> float:
        return self.intervals[-1].volume_after_m3

    @property
    def total_volume_change_m3(self) -> float:
        return fsum(interval.volume_change_m3 for interval in self.intervals)

    @property
    def total_energy_change_j(self) -> float:
        return fsum(interval.net_total_energy_change_j for interval in self.intervals)

    @property
    def event_potential_change_j(self) -> float:
        return fsum(interval.event_potential_change_j for interval in self.intervals)

    @property
    def mechanical_total_change_j(self) -> float:
        return fsum(interval.mechanical_total_change_j for interval in self.intervals)

    @property
    def affine_potential_change_j(self) -> float:
        return fsum(interval.affine_potential_change_j for interval in self.intervals)

    @property
    def target_pressure_volume_term_j(self) -> float:
        return fsum(interval.target_pressure_volume_term_j for interval in self.intervals)

    @property
    def target_pressure_energy_change_j(self) -> float:
        return fsum(interval.target_pressure_energy_change_j for interval in self.intervals)

    @property
    def pressure_quadrature_residual_j(self) -> float:
        return fsum(interval.pressure_quadrature_residual_j for interval in self.intervals)


def evaluate_flibe_rank_two_tr_eip_pressure_volume_work(
    observables: FLiBeRankTwoTREIPPressureCoupledObservables,
) -> FLiBeRankTwoTREIPPressureVolumeWorkLedger:
    """Register affine pressure-volume terms and cumulative energy accounting.

    The fixed target-pressure coordinate is E + P_target*V. The trapezoidal
    configurational estimate uses both cell boundary stresses; the difference
    from the measured potential-energy change is registered as a finite-step
    quadrature diagnostic under the declared target-pressure schedule.
    """
    if not isinstance(observables, FLiBeRankTwoTREIPPressureCoupledObservables):
        raise TypeError("observables must be FLiBeRankTwoTREIPPressureCoupledObservables.")
    trajectory = observables.trajectory
    target = trajectory.target_pressure.value
    energy_factor = observables.energy_unit_to_joule
    frame = trajectory.velocity_frame
    intervals: list[FLiBeRankTwoTREIPPressureVolumeWorkInterval] = []
    for index, (sample, step) in enumerate(zip(
        observables.samples, trajectory.steps, strict=True
    )):
        source = step.barostat.stress_trace.coupled
        previous_md = source.coupled_step.previous.md_state
        pressure = step.pressure
        kinetic_before = _kinetic_energy_j(
            previous_md, frame, pressure.mass_unit_to_kg,
            pressure.coordinate_unit_to_meter, pressure.time_unit_to_second,
        )
        potential_before = source.before_events.energy.total_energy * energy_factor
        total_before = fsum((potential_before, kinetic_before))
        total_after = sample.total_energy_j
        delta_volume = sample.volume_m3 - pressure.cell_volume_m3
        pre_pressure = step.barostat.potential_pressure_pa
        post_pressure = sample.configurational_pressure_pa
        trapezoid = -0.5 * fsum((pre_pressure, post_pressure)) * delta_volume
        affine_energy = sample.barostat_potential_energy_change_j
        target_term = target * delta_volume
        intervals.append(FLiBeRankTwoTREIPPressureVolumeWorkInterval(
            interval_index=index,
            volume_before_m3=pressure.cell_volume_m3,
            volume_after_m3=sample.volume_m3,
            volume_change_m3=delta_volume,
            potential_pressure_before_pa=pre_pressure,
            potential_pressure_after_pa=post_pressure,
            target_pressure_pa=target,
            total_energy_before_j=total_before,
            total_energy_after_j=total_after,
            event_potential_change_j=sample.event_potential_energy_change_j,
            mechanical_total_change_j=sample.mechanical_total_energy_change_j,
            affine_potential_change_j=affine_energy,
            net_total_energy_change_j=sample.net_total_energy_change_j,
            trapezoidal_potential_work_j=trapezoid,
            pressure_quadrature_residual_j=affine_energy - trapezoid,
            target_pressure_volume_term_j=target_term,
            target_pressure_energy_change_j=fsum((
                sample.net_total_energy_change_j, target_term,
            )),
        ))
    return FLiBeRankTwoTREIPPressureVolumeWorkLedger(
        observables=observables, intervals=tuple(intervals),
    )
