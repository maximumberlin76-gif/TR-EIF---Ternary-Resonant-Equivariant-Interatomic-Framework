
"""Affine-cell energy partition at a FLiBe rank-two cutoff-graph boundary.

A homogeneous cell update changes positions, lattice vectors and possibly the
set of cutoff-selected interaction edges. The full potential-energy change is
resolved into (1) deformation on the original graph and (2) graph replacement
at exactly the same final geometry. The first term has a frozen-graph
pressure-volume quadrature; the second is a separately recorded graph-event
energy increment. Reference scalar/vector and rank-two contributions are
resolved by the same operation and the original resonance-conditioned
features and retained balanced-ternary execution are held fixed.

A cutoff-selected graph edge is a numerical interaction, not a chemical bond.
Graph refresh is independent of the continuous resonance and ternary clocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy.rank_two_model import RankTwoConservativeEnergyResult
from tr_eif.energy.rank_two_stress import (
    RankTwoConservativeStressEvaluator,
    RankTwoConservativeStressResult,
)
from tr_eif.graph import InteractionEdge, InteractionGraph, build_cutoff_graph
from tr_eif.md.barostat import scale_periodic_configuration

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel, FLiBeRankTwoTREIPResult


def _positive(value: float, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{label} must be finite and positive.")
    return number


def _energy_channels(
    result: RankTwoConservativeEnergyResult,
) -> tuple[float, float, float]:
    return (
        result.reference_energy.total_energy,
        result.tensor_energy.total_energy,
        result.energy.total_energy,
    )


def _stress_channels(
    result: RankTwoConservativeStressResult,
) -> tuple[float, float, float]:
    return (
        -result.reference_stress.trace / 3.0,
        -result.tensor_stress.trace / 3.0,
        result.potential_pressure,
    )


def _difference(
    after: tuple[float, ...],
    before: tuple[float, ...],
) -> tuple[float, ...]:
    return tuple(
        a - b for a, b in zip(after, before, strict=True)
    )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPCutoffEnergyPartition:
    """Frozen-feature energy and stress records on both sides of graph refresh."""

    reference: FLiBeRankTwoTREIPResult
    cutoff: float
    linear_scale: float
    scaled_configuration: AtomicConfiguration
    graph_before: InteractionGraph
    graph_after: InteractionGraph
    frozen_energy: RankTwoConservativeEnergyResult
    refreshed_energy: RankTwoConservativeEnergyResult
    stress_before: RankTwoConservativeStressResult
    stress_frozen_after: RankTwoConservativeStressResult
    stress_refreshed_after: RankTwoConservativeStressResult

    def __post_init__(self) -> None:
        if not isinstance(self.reference, FLiBeRankTwoTREIPResult):
            raise TypeError("reference must be FLiBeRankTwoTREIPResult.")

        _positive(self.cutoff, "cutoff")
        scale = _positive(self.linear_scale, "linear_scale")
        initial = self.reference.configuration.configuration

        if initial.cell is None or initial.periodic != (True, True, True):
            raise ValueError(
                "cutoff energy partition requires a fully periodic cell."
            )

        if not isinstance(self.scaled_configuration, AtomicConfiguration):
            raise TypeError(
                "scaled_configuration must be AtomicConfiguration."
            )

        if self.scaled_configuration != scale_periodic_configuration(
            initial, scale
        ):
            raise ValueError(
                "scaled_configuration differs from affine cell scaling."
            )

        if not isinstance(self.graph_before, InteractionGraph) or not isinstance(
            self.graph_after, InteractionGraph
        ):
            raise TypeError("graph boundaries must be InteractionGraph.")

        if self.graph_before != self.reference.graph:
            raise ValueError(
                "reference and pre-deformation graphs differ."
            )

        if self.graph_before != build_cutoff_graph(initial, self.cutoff):
            raise ValueError(
                "graph_before differs from the declared cutoff."
            )

        if self.graph_after != build_cutoff_graph(
            self.scaled_configuration, self.cutoff
        ):
            raise ValueError(
                "graph_after differs from the declared cutoff."
            )

        for name in ("frozen_energy", "refreshed_energy"):
            if not isinstance(
                getattr(self, name), RankTwoConservativeEnergyResult
            ):
                raise TypeError(
                    f"{name} must be RankTwoConservativeEnergyResult."
                )

        for name in (
            "stress_before",
            "stress_frozen_after",
            "stress_refreshed_after",
        ):
            if not isinstance(
                getattr(self, name), RankTwoConservativeStressResult
            ):
                raise TypeError(
                    f"{name} must be RankTwoConservativeStressResult."
                )

        initial_energy = self.reference.augmented_result

        if self.stress_before.reference_evaluation != initial_energy:
            raise ValueError(
                "initial stress and TR-EIP energy differ."
            )

        if self.stress_frozen_after.reference_evaluation != self.frozen_energy:
            raise ValueError(
                "frozen-graph stress and energy differ."
            )

        if self.stress_refreshed_after.reference_evaluation != self.refreshed_energy:
            raise ValueError(
                "refreshed-graph stress and energy differ."
            )

        for initial_result, result in (
            (initial_energy, self.frozen_energy),
            (initial_energy, self.refreshed_energy),
        ):
            if initial_result.layer.previous != result.layer.previous:
                raise ValueError(
                    "resonance-conditioned and tensor features changed."
                )

        initial_volume = self.stress_before.reference_volume
        final_volume = self.stress_frozen_after.reference_volume

        if not isclose(
            final_volume,
            initial_volume * scale**3,
            rel_tol=1e-11,
            abs_tol=0.0,
        ):
            raise ValueError(
                "affine volume ratio differs from cubic linear scaling."
            )

        if not isclose(
            final_volume,
            self.stress_refreshed_after.reference_volume,
            rel_tol=1e-12,
            abs_tol=0.0,
        ):
            raise ValueError(
                "graph refresh changed the final geometry volume."
            )

        for actual, expected in zip(
            self.total_energy_change,
            (
                fsum((a, b))
                for a, b in zip(
                    self.affine_energy_change,
                    self.graph_event_energy_change,
                    strict=True,
                )
            ),
            strict=True,
        ):
            if not isclose(
                actual, expected, rel_tol=1e-10, abs_tol=1e-10
            ):
                raise ValueError(
                    "affine and graph-event energy channels do not sum."
                )

    @property
    def added_edges(self) -> tuple[InteractionEdge, ...]:
        """Directed cutoff edges present only after deformation."""
        previous = set(self.graph_before.edges)
        return tuple(
            edge for edge in self.graph_after.edges
            if edge not in previous
        )

    @property
    def removed_edges(self) -> tuple[InteractionEdge, ...]:
        """Directed cutoff edges present only before deformation."""
        following = set(self.graph_after.edges)
        return tuple(
            edge for edge in self.graph_before.edges
            if edge not in following
        )

    @property
    def has_graph_event(self) -> bool:
        return self.graph_before != self.graph_after

    @property
    def volume_change(self) -> float:
        return (
            self.stress_frozen_after.reference_volume
            - self.stress_before.reference_volume
        )

    @property
    def affine_energy_change(self) -> tuple[float, float, float]:
        """Reference, rank-two and total energy change on the original graph."""
        return _difference(
            _energy_channels(self.frozen_energy),
            _energy_channels(self.reference.augmented_result),
        )

    @property
    def graph_event_energy_change(self) -> tuple[float, float, float]:
        """Energy difference due solely to graph replacement at fixed geometry."""
        return _difference(
            _energy_channels(self.refreshed_energy),
            _energy_channels(self.frozen_energy),
        )

    @property
    def total_energy_change(self) -> tuple[float, float, float]:
        """Reference, rank-two and total energy change including graph refresh."""
        return _difference(
            _energy_channels(self.refreshed_energy),
            _energy_channels(self.reference.augmented_result),
        )

    @property
    def frozen_graph_pressure_work(self) -> tuple[float, float, float]:
        """Trapezoidal -P dV estimate on the fixed-graph deformation branch."""
        before = _stress_channels(self.stress_before)
        after = _stress_channels(self.stress_frozen_after)

        return tuple(
            -0.5 * fsum((p0, p1)) * self.volume_change
            for p0, p1 in zip(before, after, strict=True)
        )

    @property
    def frozen_graph_quadrature_residual(self) -> tuple[float, float, float]:
        """Finite-step affine-energy minus the frozen-graph pressure-work estimate."""
        return _difference(
            self.affine_energy_change,
            self.frozen_graph_pressure_work,
        )

    @property
    def full_pressure_work_residual(self) -> tuple[float, float, float]:
        """Total energy change minus frozen-graph work, including graph-event jump."""
        return _difference(
            self.total_energy_change,
            self.frozen_graph_pressure_work,
        )


def evaluate_flibe_rank_two_cutoff_energy_partition(
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    reference: FLiBeRankTwoTREIPResult,
    *,
    cutoff: float,
    linear_scale: float,
) -> FLiBeRankTwoTREIPCutoffEnergyPartition:
    """Measure an affine energy change and a subsequent discrete graph update.

    The original graph, continuous resonance feature inputs, rank-two channels
    and retained ternary execution are unchanged over the affine branch.
    Rebuilding the radial cutoff graph at the same final geometry isolates the
    graph-event increment. Pressure quadrature is evaluated only on the
    frozen-graph branch. Descriptor or ternary updates require separate events.
    """
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")

    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError(
            "stress_evaluator must be RankTwoConservativeStressEvaluator."
        )

    if not isinstance(reference, FLiBeRankTwoTREIPResult):
        raise TypeError("reference must be FLiBeRankTwoTREIPResult.")

    checked_cutoff = _positive(cutoff, "cutoff")
    checked_scale = _positive(linear_scale, "linear_scale")
    initial = reference.configuration.configuration

    if initial.periodic != (True, True, True) or initial.cell is None:
        raise ValueError(
            "cutoff transition requires a fully periodic cell."
        )

    if build_cutoff_graph(initial, checked_cutoff) != reference.graph:
        raise ValueError(
            "cutoff does not reproduce the reference interaction graph."
        )

    # Bind the reference energy to the model, descriptor and retained state.
    if model.evaluate(
        reference.configuration,
        reference.graph,
        reference.input_features,
        reference.resonance,
        reference.execution,
    ) != reference:
        raise ValueError(
            "reference TR-EIP evaluation differs from the supplied model."
        )

    scaled = scale_periodic_configuration(initial, checked_scale)
    updated_graph = build_cutoff_graph(scaled, checked_cutoff)
    energy_model = model.rank_two_model
    features = reference.resonance_features
    execution = reference.execution

    frozen_energy = energy_model.evaluate(
        scaled, reference.graph, features, execution
    )
    refreshed_energy = energy_model.evaluate(
        scaled, updated_graph, features, execution
    )

    before_stress = stress_evaluator.evaluate(
        energy_model, initial, reference.graph, features, execution
    )
    frozen_stress = stress_evaluator.evaluate(
        energy_model, scaled, reference.graph, features, execution
    )
    refreshed_stress = (
        frozen_stress
        if updated_graph == reference.graph
        else stress_evaluator.evaluate(
            energy_model, scaled, updated_graph, features, execution
        )
    )

    return FLiBeRankTwoTREIPCutoffEnergyPartition(
        reference=reference,
        cutoff=checked_cutoff,
        linear_scale=checked_scale,
        scaled_configuration=scaled,
        graph_before=reference.graph,
        graph_after=updated_graph,
        frozen_energy=frozen_energy,
        refreshed_energy=refreshed_energy,
        stress_before=before_stress,
        stress_frozen_after=frozen_stress,
        stress_refreshed_after=refreshed_stress,
    )
