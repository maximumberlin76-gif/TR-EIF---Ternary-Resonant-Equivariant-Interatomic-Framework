
"""Refined pressure-volume quadrature on FLiBe rank-two cutoff paths.

The analytic cutoff scan defines graph-constant affine intervals and
localized graph-replacement energy jumps. Composite trapezoidal integration
samples configurational pressure at equal-volume subdivisions within each
fixed-graph interval. The localized graph jumps are carried unchanged at
their critical geometries throughout quadrature refinement.

Reference scalar/vector, rank-two and total-energy channels are reported
separately. Continuous resonance features and retained balanced-ternary
execution stay fixed across all pressure samples of an affine path.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import (
    RankTwoConservativeStressEvaluator,
    RankTwoConservativeStressResult,
)
from tr_eif.md.barostat import scale_periodic_configuration

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_cutoff_path_work import (
    FLiBeRankTwoCutoffPathWork,
    FLiBeRankTwoCutoffPathSegment,
)


Channels = tuple[float, float, float]


def _sum_channels(rows: tuple[Channels, ...]) -> Channels:
    return tuple(
        fsum(row[channel] for row in rows)
        for channel in range(3)
    )


def _difference(after: Channels, before: Channels) -> Channels:
    return tuple(
        a - b for a, b in zip(after, before, strict=True)
    )


def _pressure(stress: RankTwoConservativeStressResult) -> Channels:
    return (
        -stress.reference_stress.trace / 3.0,
        -stress.tensor_stress.trace / 3.0,
        stress.potential_pressure,
    )


def _channel_identity(values: Channels, name: str) -> None:
    if not isinstance(values, tuple) or len(values) != 3:
        raise TypeError(
            f"{name} must contain three energy channels."
        )
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not isfinite(value)
        for value in values
    ):
        raise ValueError(
            f"{name} must contain finite real values."
        )
    if not isclose(
        values[2], fsum(values[:2]),
        rel_tol=1e-9, abs_tol=1e-8,
    ):
        raise ValueError(
            f"{name} must sum the reference and rank-two channels."
        )


def _validate_refinements(counts: tuple[int, ...]) -> None:
    if not isinstance(counts, tuple) or not counts:
        raise ValueError(
            "subdivision_counts must be a nonempty tuple."
        )
    if any(
        isinstance(n, bool) or not isinstance(n, int)
        for n in counts
    ):
        raise TypeError(
            "subdivision counts must be integers."
        )
    if counts[0] != 1 or any(
        n != 2 * previous
        for previous, n in zip(counts, counts[1:], strict=False)
    ):
        raise ValueError(
            "subdivision_counts must start at 1 and double each level."
        )
    if counts[-1] > 64:
        raise ValueError(
            "subdivision count must not exceed 64 per segment."
        )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffQuadratureLevel:
    """Composite fixed-graph -P dV estimate for one spatial refinement."""

    path: FLiBeRankTwoCutoffPathWork
    subdivisions_per_segment: int
    segment_pressure_work: tuple[Channels, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.path, FLiBeRankTwoCutoffPathWork):
            raise TypeError(
                "path must be FLiBeRankTwoCutoffPathWork."
            )
        if (
            isinstance(self.subdivisions_per_segment, bool)
            or not isinstance(self.subdivisions_per_segment, int)
        ):
            raise TypeError(
                "subdivisions_per_segment must be an integer."
            )
        if not 1 <= self.subdivisions_per_segment <= 64:
            raise ValueError(
                "subdivisions_per_segment must be in [1, 64]."
            )
        if not isinstance(self.segment_pressure_work, tuple) or len(
            self.segment_pressure_work
        ) != len(self.path.segments):
            raise ValueError(
                "segment_pressure_work must align with all path segments."
            )
        for index, values in enumerate(self.segment_pressure_work):
            _channel_identity(
                values, f"segment_pressure_work[{index}]"
            )
        for name in (
            "smooth_pressure_work",
            "smooth_quadrature_residual",
            "estimated_total_energy_change",
            "total_quadrature_residual",
        ):
            _channel_identity(getattr(self, name), name)
        for total, smooth in zip(
            self.total_quadrature_residual,
            self.smooth_quadrature_residual,
            strict=True,
        ):
            if not isclose(
                total, smooth, rel_tol=1e-9, abs_tol=1e-8
            ):
                raise ValueError(
                    "localized graph energy must remain unchanged by refinement."
                )
        if self.subdivisions_per_segment == 1:
            for actual, expected in zip(
                self.smooth_pressure_work,
                self.path.trapezoidal_pressure_work,
                strict=True,
            ):
                if not isclose(
                    actual, expected, rel_tol=1e-9, abs_tol=1e-8
                ):
                    raise ValueError(
                        "one-subdivision work must match the path endpoint rule."
                    )

    @property
    def smooth_pressure_work(self) -> Channels:
        return _sum_channels(self.segment_pressure_work)

    @property
    def smooth_quadrature_residual(self) -> Channels:
        """Full fixed-graph energy increments minus numerical -P dV work."""
        return _difference(
            self.path.smooth_energy_change,
            self.smooth_pressure_work,
        )

    @property
    def estimated_total_energy_change(self) -> Channels:
        """Refined smooth pressure work plus unchanged cutoff energy jumps."""
        return tuple(
            fsum((smooth, jump))
            for smooth, jump in zip(
                self.smooth_pressure_work,
                self.path.localized_graph_energy_change,
                strict=True,
            )
        )

    @property
    def total_quadrature_residual(self) -> Channels:
        """Actual final minus initial energy, less the reconstructed estimate."""
        return _difference(
            self.path.total_energy_change,
            self.estimated_total_energy_change,
        )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathQuadrature:
    """Nested fixed-graph pressure quadratures with exact graph-event accounting."""

    path: FLiBeRankTwoCutoffPathWork
    levels: tuple[FLiBeRankTwoCutoffQuadratureLevel, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.path, FLiBeRankTwoCutoffPathWork):
            raise TypeError(
                "path must be FLiBeRankTwoCutoffPathWork."
            )
        if not isinstance(self.levels, tuple) or not self.levels:
            raise ValueError(
                "levels must be a nonempty tuple."
            )
        if any(
            not isinstance(level, FLiBeRankTwoCutoffQuadratureLevel)
            for level in self.levels
        ):
            raise TypeError(
                "levels must contain typed quadrature records."
            )
        _validate_refinements(
            tuple(
                level.subdivisions_per_segment
                for level in self.levels
            )
        )
        for level in self.levels:
            if level.path != self.path:
                raise ValueError(
                    "refinement levels must use the same cutoff path."
                )

    @property
    def subdivisions(self) -> tuple[int, ...]:
        return tuple(
            level.subdivisions_per_segment
            for level in self.levels
        )

    @property
    def total_energy_change(self) -> Channels:
        return self.path.total_energy_change

    @property
    def localized_graph_energy_change(self) -> Channels:
        return self.path.localized_graph_energy_change

    @property
    def signed_total_residuals(self) -> tuple[Channels, ...]:
        return tuple(
            level.total_quadrature_residual
            for level in self.levels
        )

    @property
    def total_absolute_residuals(self) -> tuple[float, ...]:
        """Absolute total-energy-channel quadrature errors by refinement."""
        return tuple(
            abs(level.total_quadrature_residual[2])
            for level in self.levels
        )

    @property
    def refinement_error_ratios(self) -> tuple[float | None, ...]:
        """Previous absolute total-channel error divided by the next one."""
        errors = self.total_absolute_residuals
        return tuple(
            errors[index - 1] / errors[index]
            if errors[index] != 0.0 else None
            for index in range(1, len(errors))
        )


def evaluate_flibe_rank_two_cutoff_path_quadrature(
    path: FLiBeRankTwoCutoffPathWork,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    subdivision_counts: tuple[int, ...] = (1, 2, 4, 8),
) -> FLiBeRankTwoCutoffPathQuadrature:
    """Refine fixed-graph pressure integration with equal-volume subintervals.

    Sampled volumes are equally spaced between segment endpoint volumes;
    linear scales are reconstructed by the cubic root of interpolated scale
    cubes. At a cutoff crossing, the graph jumps are taken directly from the
    analytic transition scan. The computed error is reported at every level
    without imposing an observed-error-dependent acceptance threshold.
    """
    if not isinstance(path, FLiBeRankTwoCutoffPathWork):
        raise TypeError(
            "path must be FLiBeRankTwoCutoffPathWork."
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
    _validate_refinements(subdivision_counts)

    reference = path.scan.reference
    if model.evaluate(
        reference.configuration,
        reference.graph,
        reference.input_features,
        reference.resonance,
        reference.execution,
    ) != reference:
        raise ValueError(
            "path reference differs from the declared rank-two model."
        )
    if any(
        segment.initial_stress.differentiation
        != stress_evaluator.differentiation
        or segment.final_stress.differentiation
        != stress_evaluator.differentiation
        for segment in path.segments
    ):
        raise ValueError(
            "refinement evaluator differs from the path stress method."
        )

    original_configuration = reference.configuration.configuration
    features = reference.resonance_features
    execution = reference.execution
    cache: dict[
        tuple[int, Fraction], RankTwoConservativeStressResult
    ] = {}

    def sample(
        segment: FLiBeRankTwoCutoffPathSegment,
        portion: Fraction,
    ):
        if portion == 0:
            return segment.initial_stress
        if portion == 1:
            return segment.final_stress

        key = (segment.index, portion)
        if key not in cache:
            t = float(portion)
            scale_cube = fsum((
                (1.0 - t) * segment.initial_linear_scale**3,
                t * segment.final_linear_scale**3,
            ))
            if not isfinite(scale_cube) or scale_cube <= 0.0:
                raise ValueError(
                    "subdivided cell scale must be finite and positive."
                )
            scale = scale_cube ** (1.0 / 3.0)
            geometry = scale_periodic_configuration(
                original_configuration, scale
            )
            record = stress_evaluator.evaluate(
                model.rank_two_model,
                geometry,
                segment.graph,
                features,
                execution,
            )
            if record.reference_evaluation.layer.previous != features:
                raise ValueError(
                    "quadrature changed the frozen resonance features."
                )
            cache[key] = record
        return cache[key]

    levels: list[FLiBeRankTwoCutoffQuadratureLevel] = []

    for subdivisions in subdivision_counts:
        segment_works: list[Channels] = []

        for segment in path.segments:
            nodes = tuple(
                sample(segment, Fraction(index, subdivisions))
                for index in range(subdivisions + 1)
            )
            intervals = tuple(
                tuple(
                    -0.5 * fsum((left, right))
                    * (b.reference_volume - a.reference_volume)
                    for left, right in zip(
                        _pressure(a), _pressure(b), strict=True
                    )
                )
                for a, b in zip(nodes, nodes[1:])
            )
            segment_works.append(_sum_channels(intervals))

        levels.append(
            FLiBeRankTwoCutoffQuadratureLevel(
                path=path,
                subdivisions_per_segment=subdivisions,
                segment_pressure_work=tuple(segment_works),
            )
        )

    return FLiBeRankTwoCutoffPathQuadrature(
        path=path,
        levels=tuple(levels),
    )
