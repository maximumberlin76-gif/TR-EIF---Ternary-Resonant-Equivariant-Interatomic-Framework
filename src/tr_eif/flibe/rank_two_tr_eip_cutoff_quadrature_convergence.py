"""Convergence qualification for FLiBe rank-two cutoff-path quadrature ledgers.

Fixed-graph pressure-work errors are examined at segment, MD-interval, and
trajectory levels for reference, rank-two, and total energy channels. Cutoff
energy jumps retain their analytic boundary values at every refinement level.

The qualification uses criteria declared by its caller: a finest-grid error
limit, a minimum resolved halving ratio, a roundoff floor, and a required
number of resolved refinement pairs. Unresolved numerical order and numerical
failure remain separate from balanced-ternary execution states.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isfinite, log2

from .rank_two_tr_eip_cutoff_path_quadrature_ledger import (
    FLiBeRankTwoCutoffPathQuadratureLedger,
)


CHANNEL_NAMES = ("reference", "rank_two", "total")


class FLiBeCutoffConvergenceScope(str, Enum):
    SEGMENT = "SEGMENT"
    INTERVAL = "INTERVAL"
    TRAJECTORY = "TRAJECTORY"


class FLiBeCutoffConvergenceStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INCONCLUSIVE = "INCONCLUSIVE"


def _finite_number(value: float, name: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result < minimum:
        raise ValueError(f"{name} must be finite and at least {minimum}.")
    return result


@dataclass(frozen=True, slots=True)
class FLiBeCutoffConvergenceCriterion:
    """Predeclared error and observed-order requirements in SI energy units."""

    finest_error_limit_j: float
    minimum_error_ratio: float
    roundoff_floor_j: float
    required_resolved_pairs: int

    def __post_init__(self) -> None:
        limit = _finite_number(self.finest_error_limit_j, "finest_error_limit_j")
        ratio = _finite_number(self.minimum_error_ratio, "minimum_error_ratio")
        floor = _finite_number(self.roundoff_floor_j, "roundoff_floor_j")
        if limit <= 0.0 or ratio <= 1.0 or floor >= limit:
            raise ValueError("Require positive error limit, ratio above one, and floor below limit.")
        if (isinstance(self.required_resolved_pairs, bool)
                or not isinstance(self.required_resolved_pairs, int)):
            raise TypeError("required_resolved_pairs must be an integer.")
        if self.required_resolved_pairs < 1:
            raise ValueError("required_resolved_pairs must be positive.")


@dataclass(frozen=True, slots=True)
class FLiBeCutoffConvergenceSeries:
    """Absolute quadrature error sequence for one declared scope and channel."""

    scope: FLiBeCutoffConvergenceScope
    channel: str
    interval_index: int | None
    segment_index: int | None
    errors_j: tuple[float, ...]
    criterion: FLiBeCutoffConvergenceCriterion

    def __post_init__(self) -> None:
        if not isinstance(self.scope, FLiBeCutoffConvergenceScope):
            raise TypeError("scope must be FLiBeCutoffConvergenceScope.")
        if self.channel not in CHANNEL_NAMES:
            raise ValueError("channel must be reference, rank_two, or total.")
        if not isinstance(self.criterion, FLiBeCutoffConvergenceCriterion):
            raise TypeError("criterion must be FLiBeCutoffConvergenceCriterion.")
        if not isinstance(self.errors_j, tuple) or len(self.errors_j) < 2:
            raise ValueError("errors_j must contain at least two refinement levels.")
        for value in self.errors_j:
            _finite_number(value, "quadrature error")
        for field in ("interval_index", "segment_index"):
            value = getattr(self, field)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value < 0
            ):
                raise ValueError(f"{field} must be a nonnegative integer or None.")
        if self.scope is FLiBeCutoffConvergenceScope.SEGMENT:
            if self.interval_index is None or self.segment_index is None:
                raise ValueError("segment scope requires interval and segment indices.")
        elif self.scope is FLiBeCutoffConvergenceScope.INTERVAL:
            if self.interval_index is None or self.segment_index is not None:
                raise ValueError("interval scope requires only the interval index.")
        elif self.interval_index is not None or self.segment_index is not None:
            raise ValueError("trajectory scope does not use interval or segment indices.")

    @property
    def refinement_ratios(self) -> tuple[float | None, ...]:
        """Only ratios above the declared roundoff floor are interpreted."""
        floor = self.criterion.roundoff_floor_j
        ratios = []
        for previous, current in zip(self.errors_j, self.errors_j[1:]):
            if previous <= floor or current <= floor:
                ratios.append(None)
                continue
            ratio = previous / current
            ratios.append(ratio if isfinite(ratio) else None)
        return tuple(ratios)

    @property
    def observed_orders(self) -> tuple[float | None, ...]:
        """Observed log2 error ratios for successive subdivision doublings."""
        return tuple(log2(ratio) if ratio is not None else None
                     for ratio in self.refinement_ratios)

    @property
    def resolved_pair_count(self) -> int:
        return sum(ratio is not None for ratio in self.refinement_ratios)

    @property
    def finest_error_met(self) -> bool:
        return self.errors_j[-1] <= self.criterion.finest_error_limit_j

    @property
    def status(self) -> FLiBeCutoffConvergenceStatus:
        """Require both finite error tolerance and resolved refinement order."""
        if not self.finest_error_met:
            return FLiBeCutoffConvergenceStatus.FAIL
        ratios = tuple(ratio for ratio in self.refinement_ratios if ratio is not None)
        if any(ratio < self.criterion.minimum_error_ratio for ratio in ratios):
            return FLiBeCutoffConvergenceStatus.FAIL
        if len(ratios) < self.criterion.required_resolved_pairs:
            return FLiBeCutoffConvergenceStatus.INCONCLUSIVE
        return FLiBeCutoffConvergenceStatus.PASS


@dataclass(frozen=True, slots=True)
class FLiBeCutoffQuadratureConvergenceQualification:
    """Fixed-criterion convergence evidence at three nested computational scopes."""

    source: FLiBeRankTwoCutoffPathQuadratureLedger
    criterion: FLiBeCutoffConvergenceCriterion
    segment_series: tuple[FLiBeCutoffConvergenceSeries, ...]
    interval_series: tuple[FLiBeCutoffConvergenceSeries, ...]
    trajectory_series: tuple[FLiBeCutoffConvergenceSeries, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, FLiBeRankTwoCutoffPathQuadratureLedger):
            raise TypeError("source must be FLiBeRankTwoCutoffPathQuadratureLedger.")
        if not isinstance(self.criterion, FLiBeCutoffConvergenceCriterion):
            raise TypeError("criterion must be FLiBeCutoffConvergenceCriterion.")
        expected_segments = sum(len(interval.source.path.segments)
                                for interval in self.source.intervals)
        for name, count, scope in (
            ("segment_series", 3 * expected_segments, FLiBeCutoffConvergenceScope.SEGMENT),
            ("interval_series", 3 * len(self.source.intervals), FLiBeCutoffConvergenceScope.INTERVAL),
            ("trajectory_series", 3, FLiBeCutoffConvergenceScope.TRAJECTORY),
        ):
            series = getattr(self, name)
            if not isinstance(series, tuple) or len(series) != count:
                raise ValueError(f"{name} count differs from source levels.")
            if any(not isinstance(item, FLiBeCutoffConvergenceSeries)
                   or item.scope is not scope or item.criterion != self.criterion
                   or len(item.errors_j) != len(self.source.levels) for item in series):
                raise ValueError(f"{name} has mismatched typed convergence records.")
        expected_segments = tuple(
            (i, j, channel)
            for i, item in enumerate(self.source.intervals)
            for j in range(len(item.source.path.segments))
            for channel in CHANNEL_NAMES
        )
        observed_segments = tuple(
            (item.interval_index, item.segment_index, item.channel)
            for item in self.segment_series
        )
        if observed_segments != expected_segments:
            raise ValueError("segment convergence records differ from source order.")
        expected_intervals = tuple(
            (i, channel)
            for i in range(len(self.source.intervals))
            for channel in CHANNEL_NAMES
        )
        observed_intervals = tuple(
            (item.interval_index, item.channel)
            for item in self.interval_series
        )
        if observed_intervals != expected_intervals:
            raise ValueError("interval convergence records differ from source order.")
        if tuple(item.channel for item in self.trajectory_series) != CHANNEL_NAMES:
            raise ValueError("trajectory channels must use canonical order.")
        jump = self.source.levels[0].localized_graph_energy_j
        for level in self.source.levels[1:]:
            if level.localized_graph_energy_j != jump:
                raise ValueError("localized graph energy changed during refinement.")

    @property
    def status(self) -> FLiBeCutoffConvergenceStatus:
        """Fine-grid trajectory accuracy and all local convergence must qualify."""
        local = (*self.segment_series, *self.interval_series)
        if (any(item.status is FLiBeCutoffConvergenceStatus.FAIL for item in local)
                or any(not item.finest_error_met for item in self.trajectory_series)):
            return FLiBeCutoffConvergenceStatus.FAIL
        if any(item.status is FLiBeCutoffConvergenceStatus.INCONCLUSIVE for item in local):
            return FLiBeCutoffConvergenceStatus.INCONCLUSIVE
        return FLiBeCutoffConvergenceStatus.PASS

    @property
    def cancellation_flags(self) -> tuple[bool, bool, bool]:
        """Detect when summed interval errors mask the sum of local magnitudes."""
        final_index = len(self.source.levels) - 1
        limit = self.criterion.finest_error_limit_j
        return tuple(
            abs(self.source.levels[final_index].quadrature_residual_j[k]) <= limit
            and fsum(abs(interval.levels[final_index].quadrature_residual_j[k])
                     for interval in self.source.intervals) > limit
            for k in range(3)
        )

    @property
    def localized_cutoff_energy_j(self) -> tuple[float, float, float]:
        """Analytic graph-jump energies independent of quadrature subdivision."""
        return self.source.levels[0].localized_graph_energy_j


def evaluate_flibe_rank_two_cutoff_quadrature_convergence(
    source: FLiBeRankTwoCutoffPathQuadratureLedger,
    criterion: FLiBeCutoffConvergenceCriterion,
) -> FLiBeCutoffQuadratureConvergenceQualification:
    """Apply a predeclared numerical contract to an immutable quadrature ledger.

    Segment errors compare exact fixed-graph energy differences with sampled
    smooth pressure work. Interval and trajectory errors use their recorded
    signed quadrature residuals. The cutoff-jump contribution is unchanged by
    refinement and is not treated as a smooth quadrature error.
    """
    if not isinstance(source, FLiBeRankTwoCutoffPathQuadratureLedger):
        raise TypeError("source must be FLiBeRankTwoCutoffPathQuadratureLedger.")
    if not isinstance(criterion, FLiBeCutoffConvergenceCriterion):
        raise TypeError("criterion must be FLiBeCutoffConvergenceCriterion.")
    if len(source.levels) < criterion.required_resolved_pairs + 1:
        raise ValueError("source has fewer levels than the required refinement pairs.")

    def series(scope, channel, interval, segment, errors):
        return FLiBeCutoffConvergenceSeries(
            scope=scope, channel=channel, interval_index=interval,
            segment_index=segment, errors_j=tuple(errors), criterion=criterion,
        )

    segments = []
    intervals = []
    for i, item in enumerate(source.intervals):
        factor = item.source.original.energy_unit_to_joule
        for j, segment in enumerate(item.source.path.segments):
            for k, channel in enumerate(CHANNEL_NAMES):
                exact = segment.potential_energy_change[k]
                errors = tuple(
                    abs((exact - level.segment_pressure_work[j][k]) * factor)
                    for level in item.quadrature.levels
                )
                segments.append(series(
                    FLiBeCutoffConvergenceScope.SEGMENT, channel, i, j, errors,
                ))
        for k, channel in enumerate(CHANNEL_NAMES):
            errors = tuple(abs(level.quadrature_residual_j[k])
                           for level in item.levels)
            intervals.append(series(
                FLiBeCutoffConvergenceScope.INTERVAL, channel, i, None, errors,
            ))
    trajectories = tuple(
        series(
            FLiBeCutoffConvergenceScope.TRAJECTORY, channel, None, None,
            (abs(level.quadrature_residual_j[k]) for level in source.levels),
        )
        for k, channel in enumerate(CHANNEL_NAMES)
    )
    return FLiBeCutoffQuadratureConvergenceQualification(
        source=source, criterion=criterion,
        segment_series=tuple(segments), interval_series=tuple(intervals),
        trajectory_series=trajectories,
    )
