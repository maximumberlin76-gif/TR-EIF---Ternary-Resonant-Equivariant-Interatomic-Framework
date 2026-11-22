
"""Refined cutoff-path pressure work over a scheduled FLiBe rank-two MD ledger.

The input trajectory keeps its mechanical, resonance, and ternary event clocks.
Each barostat interval is integrated on its fixed-graph affine segments at
successively finer equal-volume subdivisions. Localized cutoff jumps remain
at their analytic transition geometries and do not depend on subdivision.

The output preserves reference scalar/vector, rank-two, and total potential
energy channels in joules, with separate work, jump, and quadrature residual.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_cutoff_path_pressure_ledger import (
    FLiBeRankTwoCutoffPathPressureInterval,
    FLiBeRankTwoCutoffPathPressureLedger,
)
from .rank_two_tr_eip_cutoff_path_quadrature import (
    FLiBeRankTwoCutoffPathQuadrature,
    evaluate_flibe_rank_two_cutoff_path_quadrature,
)


Channels = tuple[float, float, float]


def _scale(values: Channels, factor: float) -> Channels:
    return tuple(value * factor for value in values)


def _add(left: Channels, right: Channels) -> Channels:
    return tuple(fsum((a, b)) for a, b in zip(left, right, strict=True))


def _sum_channels(values: tuple[Channels, ...]) -> Channels:
    return tuple(fsum(row[i] for row in values) for i in range(3))


def _close(actual: float, expected: float, field: str) -> None:
    if not isfinite(actual) or not isfinite(expected) or not isclose(
        actual, expected, rel_tol=1e-9, abs_tol=1e-28,
    ):
        raise ValueError(f"{field} differs from the recorded energy boundary.")


def _matching(actual: Channels, expected: Channels, field: str) -> None:
    for i, (left, right) in enumerate(zip(actual, expected, strict=True)):
        _close(left, right, f"{field}[{i}]")


def _channels(values: Channels, field: str) -> None:
    if not isinstance(values, tuple) or len(values) != 3:
        raise TypeError(f"{field} must contain three energy channels.")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not isfinite(v)
           for v in values):
        raise ValueError(f"{field} must contain finite real values.")
    _close(values[2], fsum(values[:2]), f"{field} channel sum")


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffQuadratureWorkLevel:
    """One subdivision level of an interval or an aggregated MD trajectory."""

    subdivisions_per_segment: int
    smooth_pressure_work_j: Channels
    localized_graph_energy_j: Channels
    reconstructed_potential_change_j: Channels
    exact_potential_change_j: Channels
    quadrature_residual_j: Channels

    def __post_init__(self) -> None:
        n = self.subdivisions_per_segment
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("subdivisions_per_segment must be an integer.")
        if n < 1 or n > 64 or n & (n - 1):
            raise ValueError("subdivisions_per_segment must be a power of two in [1, 64].")
        for name in (
            "smooth_pressure_work_j", "localized_graph_energy_j",
            "reconstructed_potential_change_j", "exact_potential_change_j",
            "quadrature_residual_j",
        ):
            _channels(getattr(self, name), name)
        _matching(
            self.reconstructed_potential_change_j,
            _add(self.smooth_pressure_work_j, self.localized_graph_energy_j),
            "refined pressure-work reconstruction",
        )
        _matching(
            self.exact_potential_change_j,
            _add(self.reconstructed_potential_change_j, self.quadrature_residual_j),
            "refined energy identity",
        )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffQuadratureWorkInterval:
    """Refinement evidence for one unchanged source barostat interval."""

    source: FLiBeRankTwoCutoffPathPressureInterval
    quadrature: FLiBeRankTwoCutoffPathQuadrature
    levels: tuple[FLiBeRankTwoCutoffQuadratureWorkLevel, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, FLiBeRankTwoCutoffPathPressureInterval):
            raise TypeError("source must be a cutoff path pressure interval.")
        if not isinstance(self.quadrature, FLiBeRankTwoCutoffPathQuadrature):
            raise TypeError("quadrature must be FLiBeRankTwoCutoffPathQuadrature.")
        if self.quadrature.path != self.source.path:
            raise ValueError("quadrature must use the source interval's cutoff path.")
        if not isinstance(self.levels, tuple) or len(self.levels) != len(self.quadrature.levels):
            raise ValueError("interval levels must align with all quadrature levels.")
        factor = self.source.original.energy_unit_to_joule
        if isinstance(factor, bool) or not isinstance(factor, (int, float)) or not isfinite(factor) or factor <= 0.0:
            raise ValueError("energy conversion must be finite and positive.")
        for index, (level, original) in enumerate(zip(self.levels, self.quadrature.levels, strict=True)):
            if not isinstance(level, FLiBeRankTwoCutoffQuadratureWorkLevel):
                raise TypeError("levels must contain typed refinement records.")
            if level.subdivisions_per_segment != original.subdivisions_per_segment:
                raise ValueError("subdivision levels differ from source quadrature.")
            for name, expected in (
                ("smooth_pressure_work_j", _scale(original.smooth_pressure_work, factor)),
                ("localized_graph_energy_j", self.source.localized_graph_energy_change_j),
                ("reconstructed_potential_change_j", _scale(original.estimated_total_energy_change, factor)),
                ("exact_potential_change_j", self.source.total_energy_change_j),
                ("quadrature_residual_j", _scale(original.total_quadrature_residual, factor)),
            ):
                _matching(getattr(level, name), expected, f"levels[{index}].{name}")
        _matching(self.levels[0].smooth_pressure_work_j,
                  self.source.smooth_pressure_work_j, "one-subdivision pressure work")

    @property
    def crossing_count(self) -> int:
        return self.source.crossing_count

    @property
    def subdivisions(self) -> tuple[int, ...]:
        return tuple(level.subdivisions_per_segment for level in self.levels)


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathQuadratureLedger:
    """SI quadrature convergence across the original multi-rate MD trajectory."""

    source: FLiBeRankTwoCutoffPathPressureLedger
    intervals: tuple[FLiBeRankTwoCutoffQuadratureWorkInterval, ...]
    levels: tuple[FLiBeRankTwoCutoffQuadratureWorkLevel, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, FLiBeRankTwoCutoffPathPressureLedger):
            raise TypeError("source must be FLiBeRankTwoCutoffPathPressureLedger.")
        if not isinstance(self.intervals, tuple) or len(self.intervals) != len(self.source.intervals):
            raise ValueError("quadrature intervals must match the source MD intervals.")
        if not isinstance(self.levels, tuple) or not self.levels:
            raise ValueError("ledger must contain at least one refinement level.")
        if any(not isinstance(level, FLiBeRankTwoCutoffQuadratureWorkLevel)
               for level in self.levels):
            raise TypeError("levels must contain typed refinement records.")
        counts = tuple(level.subdivisions_per_segment for level in self.levels)
        if counts[0] != 1 or any(b != 2 * a for a, b in zip(counts, counts[1:])):
            raise ValueError("ledger subdivisions must begin at 1 and double.")
        for index, (item, source) in enumerate(zip(self.intervals, self.source.intervals, strict=True)):
            if not isinstance(item, FLiBeRankTwoCutoffQuadratureWorkInterval):
                raise TypeError("intervals must contain typed quadrature work intervals.")
            if item.source != source or item.subdivisions != counts:
                raise ValueError(f"interval {index} source or refinements differ.")
        for index, level in enumerate(self.levels):
            if not isinstance(level, FLiBeRankTwoCutoffQuadratureWorkLevel):
                raise TypeError("levels must contain typed refinement records.")
            for name in (
                "smooth_pressure_work_j", "localized_graph_energy_j",
                "reconstructed_potential_change_j", "exact_potential_change_j",
                "quadrature_residual_j",
            ):
                expected = _sum_channels(tuple(getattr(item.levels[index], name) for item in self.intervals))
                _matching(getattr(level, name), expected, f"ledger levels[{index}].{name}")
            _matching(level.exact_potential_change_j,
                      self.source.total_energy_change_j, "cumulative potential energy")
            _matching(level.localized_graph_energy_j,
                      self.source.localized_graph_energy_change_j, "localized cutoff energy")

    @property
    def subdivisions(self) -> tuple[int, ...]:
        return tuple(level.subdivisions_per_segment for level in self.levels)

    @property
    def total_absolute_residuals_j(self) -> tuple[float, ...]:
        return tuple(abs(level.quadrature_residual_j[2]) for level in self.levels)

    @property
    def refinement_error_ratios(self) -> tuple[float | None, ...]:
        errors = self.total_absolute_residuals_j
        return tuple(a / b if b != 0.0 else None
                     for a, b in zip(errors, errors[1:]))

    @property
    def crossing_count(self) -> int:
        return sum(item.crossing_count for item in self.intervals)


def evaluate_flibe_rank_two_cutoff_path_quadrature_ledger(
    source: FLiBeRankTwoCutoffPathPressureLedger,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    subdivision_counts: tuple[int, ...] = (1, 2, 4, 8),
) -> FLiBeRankTwoCutoffPathQuadratureLedger:
    """Accumulate fixed-graph quadrature while retaining localized cutoff jumps.

    Each source interval supplies its analytic cutoff path, retained ternary
    execution, and existing phase/mechanical event records. Refinement changes
    only the pressure-integration grid. Report residuals without post-hoc
    modification of the acceptance criteria.
    """
    if not isinstance(source, FLiBeRankTwoCutoffPathPressureLedger):
        raise TypeError("source must be FLiBeRankTwoCutoffPathPressureLedger.")
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError("stress_evaluator must be RankTwoConservativeStressEvaluator.")

    intervals: list[FLiBeRankTwoCutoffQuadratureWorkInterval] = []
    for item in source.intervals:
        quadrature = evaluate_flibe_rank_two_cutoff_path_quadrature(
            item.path, model, stress_evaluator,
            subdivision_counts=subdivision_counts,
        )
        factor = item.original.energy_unit_to_joule
        records = tuple(
            FLiBeRankTwoCutoffQuadratureWorkLevel(
                subdivisions_per_segment=level.subdivisions_per_segment,
                smooth_pressure_work_j=_scale(level.smooth_pressure_work, factor),
                localized_graph_energy_j=item.localized_graph_energy_change_j,
                reconstructed_potential_change_j=_scale(level.estimated_total_energy_change, factor),
                exact_potential_change_j=item.total_energy_change_j,
                quadrature_residual_j=_scale(level.total_quadrature_residual, factor),
            ) for level in quadrature.levels
        )
        intervals.append(FLiBeRankTwoCutoffQuadratureWorkInterval(
            source=item, quadrature=quadrature, levels=records,
        ))

    result_levels = tuple(
        FLiBeRankTwoCutoffQuadratureWorkLevel(
            subdivisions_per_segment=n,
            smooth_pressure_work_j=_sum_channels(tuple(item.levels[index].smooth_pressure_work_j for item in intervals)),
            localized_graph_energy_j=_sum_channels(tuple(item.levels[index].localized_graph_energy_j for item in intervals)),
            reconstructed_potential_change_j=_sum_channels(tuple(item.levels[index].reconstructed_potential_change_j for item in intervals)),
            exact_potential_change_j=_sum_channels(tuple(item.levels[index].exact_potential_change_j for item in intervals)),
            quadrature_residual_j=_sum_channels(tuple(item.levels[index].quadrature_residual_j for item in intervals)),
        )
        for index, n in enumerate(subdivision_counts)
    )
    return FLiBeRankTwoCutoffPathQuadratureLedger(
        source=source, intervals=tuple(intervals), levels=result_levels,
    )
