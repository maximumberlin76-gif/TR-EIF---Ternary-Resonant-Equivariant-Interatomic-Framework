
"""Piecewise pressure-volume accounting across FLiBe rank-two cutoff events.

The isotropic cell sweep is divided at analytically located graph changes.
Within each segment the directed graph, resonance-conditioned features and
retained ternary execution are fixed. At each crossing, the energy change
is evaluated on both graph branches at one common cell geometry.

The energy difference across the entire sweep is the sum of smooth-segment
energy changes and localized graph-event jumps. Separate trapezoidal -P dV
estimates and quadrature residuals are recorded for the smooth segments.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import (
    RankTwoConservativeStressEvaluator,
    RankTwoConservativeStressResult,
)
from tr_eif.graph import InteractionGraph
from tr_eif.md.barostat import scale_periodic_configuration

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel, FLiBeRankTwoTREIPResult
from .rank_two_tr_eip_cutoff_transition_scan import (
    FLiBeRankTwoCutoffTransitionScan,
    locate_flibe_rank_two_cutoff_transitions,
)


def _triple_difference(after: tuple[float, ...], before: tuple[float, ...]) -> tuple[float, float, float]:
    return tuple(right - left for left, right in zip(before, after, strict=True))


def _energy(stress: RankTwoConservativeStressResult) -> tuple[float, float, float]:
    value = stress.reference_evaluation
    return (value.reference_energy.total_energy,
            value.tensor_energy.total_energy, value.energy.total_energy)


def _pressure(stress: RankTwoConservativeStressResult) -> tuple[float, float, float]:
    return (-stress.reference_stress.trace / 3.0,
            -stress.tensor_stress.trace / 3.0,
            stress.potential_pressure)


def _sum_channels(rows: tuple[tuple[float, float, float], ...]) -> tuple[float, float, float]:
    return tuple(fsum(row[index] for row in rows) for index in range(3))


def _assert_close(actual: float, expected: float, name: str) -> None:
    if not (isfinite(actual) and isfinite(expected) and
            isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-9)):
        raise ValueError(f"{name} differs from its energy/geometry boundary.")


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathSegment:
    """One continuous affine interval evaluated on a fixed interaction graph."""

    index: int
    initial_linear_scale: float
    final_linear_scale: float
    graph: InteractionGraph
    initial_stress: RankTwoConservativeStressResult
    final_stress: RankTwoConservativeStressResult

    def __post_init__(self) -> None:
        if isinstance(self.index, bool) or not isinstance(self.index, int):
            raise TypeError("index must be an integer.")
        if self.index < 0:
            raise ValueError("index must be nonnegative.")
        for name in ("initial_linear_scale", "final_linear_scale"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a real number.")
            if not isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive.")
        if not isinstance(self.graph, InteractionGraph):
            raise TypeError("graph must be InteractionGraph.")
        for name in ("initial_stress", "final_stress"):
            value = getattr(self, name)
            if not isinstance(value, RankTwoConservativeStressResult):
                raise TypeError(f"{name} must be RankTwoConservativeStressResult.")
            edges = tuple(message.edge for message in value.reference_evaluation.layer.tensor_messages)
            if len(edges) != self.graph.edge_count or set(edges) != set(self.graph.edges):
                raise ValueError(f"{name} must use this segment's graph.")
        if (self.initial_stress.reference_evaluation.layer.previous
                != self.final_stress.reference_evaluation.layer.previous):
            raise ValueError("resonance-conditioned features changed within the segment.")
        _assert_close(
            self.final_stress.reference_volume,
            self.initial_stress.reference_volume *
            (self.final_linear_scale / self.initial_linear_scale) ** 3,
            "affine segment volume",
        )
        for label, values in (
            ("energy", self.potential_energy_change),
            ("pressure work", self.trapezoidal_pressure_work),
            ("quadrature residual", self.quadrature_residual),
        ):
            _assert_close(values[2], fsum(values[:2]), label + " channel partition")

    @property
    def volume_change(self) -> float:
        return self.final_stress.reference_volume - self.initial_stress.reference_volume

    @property
    def potential_energy_change(self) -> tuple[float, float, float]:
        """Reference, rank-two and full energy change on this single graph."""
        return _triple_difference(_energy(self.final_stress), _energy(self.initial_stress))

    @property
    def trapezoidal_pressure_work(self) -> tuple[float, float, float]:
        """Three -P dV estimates using this segment's endpoint stresses."""
        first, last = _pressure(self.initial_stress), _pressure(self.final_stress)
        return tuple(-0.5 * fsum((a, b)) * self.volume_change
                     for a, b in zip(first, last, strict=True))

    @property
    def quadrature_residual(self) -> tuple[float, float, float]:
        """Exact segment energy difference minus trapezoidal -P dV work."""
        return _triple_difference(self.potential_energy_change, self.trapezoidal_pressure_work)


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffPathWork:
    """Ordered constant-graph segments and localized event energies of one sweep."""

    scan: FLiBeRankTwoCutoffTransitionScan
    segments: tuple[FLiBeRankTwoCutoffPathSegment, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.scan, FLiBeRankTwoCutoffTransitionScan):
            raise TypeError("scan must be FLiBeRankTwoCutoffTransitionScan.")
        if not isinstance(self.segments, tuple) or len(self.segments) != self.scan.crossing_count + 1:
            raise ValueError("one constant-graph segment is required between every crossing.")
        expected_scale = 1.0
        expected_graph = self.scan.reference.graph
        expected_energy = self.scan.reference.augmented_result
        expected_features = self.scan.reference.resonance_features
        for index, segment in enumerate(self.segments):
            if not isinstance(segment, FLiBeRankTwoCutoffPathSegment):
                raise TypeError("segments must contain FLiBeRankTwoCutoffPathSegment.")
            if segment.index != index:
                raise ValueError("segment indices must follow crossing order.")
            end_scale = (self.scan.crossings[index].linear_scale
                         if index < self.scan.crossing_count
                         else self.scan.target_linear_scale)
            if (segment.initial_linear_scale != expected_scale
                    or segment.final_linear_scale != end_scale
                    or segment.graph != expected_graph):
                raise ValueError("segment scale or graph differs from its cutoff crossing.")
            if segment.initial_stress.reference_evaluation != expected_energy:
                raise ValueError("segment initial energy differs from its preceding boundary.")
            if segment.initial_stress.reference_evaluation.layer.previous != expected_features:
                raise ValueError("continuous resonance features changed between segments.")
            if index < self.scan.crossing_count:
                crossing = self.scan.crossings[index]
                if (segment.graph != crossing.graph_before or
                        segment.final_stress.reference_evaluation != crossing.energy_before):
                    raise ValueError("segment terminal energy differs from crossing pre-event energy.")
                expected_scale = crossing.linear_scale
                expected_graph = crossing.graph_after
                expected_energy = crossing.energy_after
            else:
                if segment.graph != self.scan.target_graph:
                    raise ValueError("final segment graph differs from the target graph.")
        for actual, expected in zip(
            self.total_energy_change,
            _sum_channels((self.smooth_energy_change, self.localized_graph_energy_change)),
            strict=True,
        ):
            _assert_close(actual, expected, "total piecewise energy")
        for actual, expected in zip(
            self.total_pressure_work_residual,
            _sum_channels((self.smooth_quadrature_residual, self.localized_graph_energy_change)),
            strict=True,
        ):
            _assert_close(actual, expected, "piecewise pressure-work residual")

    @property
    def smooth_energy_change(self) -> tuple[float, float, float]:
        return _sum_channels(tuple(segment.potential_energy_change for segment in self.segments))

    @property
    def localized_graph_energy_change(self) -> tuple[float, float, float]:
        """Energy jumps evaluated at their own analytic cutoff scales."""
        return self.scan.localized_energy_jumps

    @property
    def total_energy_change(self) -> tuple[float, float, float]:
        """Full energy at target geometry minus the original full energy."""
        return _triple_difference(
            _energy(self.segments[-1].final_stress),
            _energy(self.segments[0].initial_stress),
        )

    @property
    def trapezoidal_pressure_work(self) -> tuple[float, float, float]:
        return _sum_channels(tuple(segment.trapezoidal_pressure_work for segment in self.segments))

    @property
    def smooth_quadrature_residual(self) -> tuple[float, float, float]:
        return _sum_channels(tuple(segment.quadrature_residual for segment in self.segments))

    @property
    def total_pressure_work_residual(self) -> tuple[float, float, float]:
        """Final energy difference minus piecewise smooth-work approximation."""
        return _triple_difference(self.total_energy_change, self.trapezoidal_pressure_work)

    @property
    def volume_change(self) -> float:
        return self.segments[-1].final_stress.reference_volume - self.segments[0].initial_stress.reference_volume


def evaluate_flibe_rank_two_cutoff_path_work(
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    reference: FLiBeRankTwoTREIPResult,
    *,
    cutoff: float,
    target_linear_scale: float,
    probe_relative_width: float = 1e-7,
) -> FLiBeRankTwoCutoffPathWork:
    """Reconstruct the full cutoff-aware energy balance along an affine sweep.

    Each smooth segment is differentiated on one graph; crossing energy jumps
    use their respective common-geometry evaluations from the analytic scan.
    The original descriptor, rank-two features and retained execution stay
    fixed throughout this numerical path.
    """
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError("stress_evaluator must be RankTwoConservativeStressEvaluator.")
    scan = locate_flibe_rank_two_cutoff_transitions(
        model, reference, cutoff=cutoff, target_linear_scale=target_linear_scale,
        probe_relative_width=probe_relative_width,
    )
    initial = scan.reference.configuration.configuration
    features = scan.reference.resonance_features
    execution = scan.reference.execution

    def stress_at(scale: float, graph: InteractionGraph) -> RankTwoConservativeStressResult:
        geometry = scale_periodic_configuration(initial, scale)
        return stress_evaluator.evaluate(model.rank_two_model, geometry, graph, features, execution)

    graph = scan.reference.graph
    start_scale = 1.0
    segments = []
    endpoints = tuple((*scan.crossings, None))
    for index, crossing in enumerate(endpoints):
        last_scale = crossing.linear_scale if crossing is not None else scan.target_linear_scale
        segments.append(FLiBeRankTwoCutoffPathSegment(
            index=index,
            initial_linear_scale=start_scale,
            final_linear_scale=last_scale,
            graph=graph,
            initial_stress=stress_at(start_scale, graph),
            final_stress=stress_at(last_scale, graph),
        ))
        if crossing is not None:
            if crossing.graph_before != graph:
                raise ValueError("analytic crossing sequence and active graph differ.")
            graph = crossing.graph_after
            start_scale = crossing.linear_scale
    return FLiBeRankTwoCutoffPathWork(scan=scan, segments=tuple(segments))
