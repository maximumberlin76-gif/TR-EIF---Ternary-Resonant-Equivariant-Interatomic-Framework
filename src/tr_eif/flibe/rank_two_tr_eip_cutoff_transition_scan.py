
"""Locate isotropic FLiBe rank-two cutoff crossings and their energy jumps.

For a uniform scaling of atomic positions and periodic cell vectors, the
minimum-image distance of each atom pair scales by the same positive factor.
A pair crosses the radial cutoff at scale = cutoff / reference_distance.

Each crossing records the directed graph change and evaluates both graph
branches at one identical boundary geometry with frozen resonance-conditioned
features and retained balanced-ternary execution. Crossing energies are
separate from finite-interval affine deformation work.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isclose, isfinite, sqrt

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy.rank_two_model import RankTwoConservativeEnergyResult
from tr_eif.geometry import minimum_image
from tr_eif.graph import InteractionEdge, InteractionGraph, build_cutoff_graph
from tr_eif.md.barostat import scale_periodic_configuration

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel, FLiBeRankTwoTREIPResult


class FLiBeCutoffSweepDirection(str, Enum):
    """Monotone direction of the isotropic linear cell-scale sweep."""

    COMPRESSION = "COMPRESSION"
    EXPANSION = "EXPANSION"


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _energy_channels(value: RankTwoConservativeEnergyResult) -> tuple[float, float, float]:
    return (
        value.reference_energy.total_energy,
        value.tensor_energy.total_energy,
        value.energy.total_energy,
    )


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffCrossing:
    """Graph replacement and full-energy jump at one critical linear scale."""

    linear_scale: float
    direction: FLiBeCutoffSweepDirection
    probe_before_scale: float
    probe_after_scale: float
    boundary_configuration: AtomicConfiguration
    graph_before: InteractionGraph
    graph_after: InteractionGraph
    energy_before: RankTwoConservativeEnergyResult
    energy_after: RankTwoConservativeEnergyResult
    added_edges: tuple[InteractionEdge, ...]
    removed_edges: tuple[InteractionEdge, ...]

    def __post_init__(self) -> None:
        center = _positive(self.linear_scale, "linear_scale")
        first = _positive(self.probe_before_scale, "probe_before_scale")
        last = _positive(self.probe_after_scale, "probe_after_scale")
        if not isinstance(self.direction, FLiBeCutoffSweepDirection):
            raise TypeError("direction must be FLiBeCutoffSweepDirection.")
        if self.direction is FLiBeCutoffSweepDirection.COMPRESSION:
            if not first > center > last:
                raise ValueError("compression probes must surround the crossing in descending order.")
        elif not first < center < last:
            raise ValueError("expansion probes must surround the crossing in ascending order.")
        if not isinstance(self.boundary_configuration, AtomicConfiguration):
            raise TypeError("boundary_configuration must be AtomicConfiguration.")
        if not isinstance(self.graph_before, InteractionGraph) or not isinstance(
            self.graph_after, InteractionGraph
        ):
            raise TypeError("crossing graphs must be InteractionGraph.")
        if self.graph_before.node_count != self.boundary_configuration.atom_count or (
            self.graph_after.node_count != self.boundary_configuration.atom_count
        ):
            raise ValueError("graph and boundary atom counts differ.")
        if not isinstance(self.energy_before, RankTwoConservativeEnergyResult) or not isinstance(
            self.energy_after, RankTwoConservativeEnergyResult
        ):
            raise TypeError("crossing energies must be RankTwoConservativeEnergyResult.")
        if self.energy_before.layer.previous != self.energy_after.layer.previous:
            raise ValueError("continuous resonance-conditioned features changed at the graph event.")
        before_messages = tuple(msg.edge for msg in self.energy_before.layer.tensor_messages)
        after_messages = tuple(msg.edge for msg in self.energy_after.layer.tensor_messages)
        if (len(before_messages) != self.graph_before.edge_count
                or set(before_messages) != set(self.graph_before.edges)
                or len(after_messages) != self.graph_after.edge_count
                or set(after_messages) != set(self.graph_after.edges)):
            raise ValueError("crossing energy messages differ from the corresponding graph.")
        added = tuple(e for e in self.graph_after.edges if e not in set(self.graph_before.edges))
        removed = tuple(e for e in self.graph_before.edges if e not in set(self.graph_after.edges))
        if self.added_edges != added or self.removed_edges != removed:
            raise ValueError("crossing edge inventory differs from its graphs.")
        if self.direction is FLiBeCutoffSweepDirection.COMPRESSION:
            if not added or removed:
                raise ValueError("compression must add cutoff edges at a crossing.")
        elif not removed or added:
            raise ValueError("expansion must remove cutoff edges at a crossing.")
        if not isclose(
            self.energy_jump[2], fsum(self.energy_jump[:2]), rel_tol=1e-10, abs_tol=1e-10,
        ):
            raise ValueError("reference and rank-two energy jumps must sum to total.")

    @property
    def energy_jump(self) -> tuple[float, float, float]:
        """Reference, rank-two and total energy difference at fixed geometry."""
        before, after = _energy_channels(self.energy_before), _energy_channels(self.energy_after)
        return tuple(b - a for a, b in zip(before, after, strict=True))


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoCutoffTransitionScan:
    """Ordered crossings along one monotone isotropic cell-scale interval."""

    reference: FLiBeRankTwoTREIPResult
    cutoff: float
    target_linear_scale: float
    target_graph: InteractionGraph
    probe_relative_width: float
    crossings: tuple[FLiBeRankTwoCutoffCrossing, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.reference, FLiBeRankTwoTREIPResult):
            raise TypeError("reference must be FLiBeRankTwoTREIPResult.")
        cutoff = _positive(self.cutoff, "cutoff")
        target = _positive(self.target_linear_scale, "target_linear_scale")
        probe = _positive(self.probe_relative_width, "probe_relative_width")
        if probe >= 0.001:
            raise ValueError("probe_relative_width must be smaller than 0.001.")
        initial = self.reference.configuration.configuration
        if initial.cell is None or initial.periodic != (True, True, True):
            raise ValueError("transition scan requires a fully periodic three-dimensional cell.")
        if build_cutoff_graph(initial, cutoff) != self.reference.graph:
            raise ValueError("reference graph differs from the declared cutoff.")
        final = scale_periodic_configuration(initial, target)
        if not isinstance(self.target_graph, InteractionGraph) or self.target_graph != build_cutoff_graph(
            final, cutoff
        ):
            raise ValueError("target graph differs from the scaled configuration.")
        if not isinstance(self.crossings, tuple) or not all(
            isinstance(item, FLiBeRankTwoCutoffCrossing) for item in self.crossings
        ):
            raise TypeError("crossings must contain typed cutoff events.")
        direction = (
            FLiBeCutoffSweepDirection.COMPRESSION if target < 1.0
            else FLiBeCutoffSweepDirection.EXPANSION
        )
        ordered = [item.linear_scale for item in self.crossings]
        if ordered != sorted(ordered, reverse=target < 1.0) or len(set(ordered)) != len(ordered):
            raise ValueError("crossings must be strictly ordered along the scale sweep.")
        for item in self.crossings:
            if item.direction is not direction or not min(1.0, target) - 1e-12 <= (
                item.linear_scale
            ) <= max(1.0, target) + 1e-12:
                raise ValueError("crossing direction or scale lies outside the declared interval.")
            if item.boundary_configuration != scale_periodic_configuration(
                initial, item.linear_scale
            ):
                raise ValueError("crossing geometry differs from its analytic scale.")
            if item.energy_before.layer.previous != self.reference.resonance_features:
                raise ValueError("crossing features differ from the reference resonance state.")
            expected_before = item.linear_scale * (
                1.0 + probe if target < 1.0 else 1.0 - probe
            )
            expected_after = item.linear_scale * (
                1.0 - probe if target < 1.0 else 1.0 + probe
            )
            if (item.probe_before_scale != expected_before
                    or item.probe_after_scale != expected_after):
                raise ValueError("crossing probe scales differ from the declared width.")
            if item.graph_before != build_cutoff_graph(
                scale_periodic_configuration(initial, item.probe_before_scale), cutoff
            ) or item.graph_after != build_cutoff_graph(
                scale_periodic_configuration(initial, item.probe_after_scale), cutoff
            ):
                raise ValueError("crossing graph probes differ from their declared scales.")
        expected_added = set(self.target_graph.edges) - set(self.reference.graph.edges)
        expected_removed = set(self.reference.graph.edges) - set(self.target_graph.edges)
        observed_added = [edge for item in self.crossings for edge in item.added_edges]
        observed_removed = [edge for item in self.crossings for edge in item.removed_edges]
        if len(observed_added) != len(set(observed_added)) or len(observed_removed) != len(
            set(observed_removed)
        ) or set(observed_added) != expected_added or set(observed_removed) != expected_removed:
            raise ValueError("crossing edge inventories do not reconstruct the target graph.")

    @property
    def crossing_count(self) -> int:
        return len(self.crossings)

    @property
    def directed_edges_added(self) -> int:
        return sum(len(item.added_edges) for item in self.crossings)

    @property
    def directed_edges_removed(self) -> int:
        return sum(len(item.removed_edges) for item in self.crossings)

    @property
    def localized_energy_jumps(self) -> tuple[float, float, float]:
        """Sum of jumps evaluated at individual crossing geometries (model units)."""
        return tuple(fsum(item.energy_jump[k] for item in self.crossings) for k in range(3))


def locate_flibe_rank_two_cutoff_transitions(
    model: FLiBeRankTwoTREIPModel,
    reference: FLiBeRankTwoTREIPResult,
    *,
    cutoff: float,
    target_linear_scale: float,
    probe_relative_width: float = 1e-7,
) -> FLiBeRankTwoCutoffTransitionScan:
    """Locate each changed pair's analytic cutoff scale and measure its energy jump.

    Both graph-branch energies are evaluated at the same critical geometry.
    Cutoff membership uses the repository's deterministic minimum-image and
    directed-edge conventions. A fixed relative probe brackets each crossing.
    """
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(reference, FLiBeRankTwoTREIPResult):
        raise TypeError("reference must be FLiBeRankTwoTREIPResult.")
    cutoff = _positive(cutoff, "cutoff")
    target = _positive(target_linear_scale, "target_linear_scale")
    probe = _positive(probe_relative_width, "probe_relative_width")
    if probe >= 0.001:
        raise ValueError("probe_relative_width must be smaller than 0.001.")
    initial = reference.configuration.configuration
    if initial.cell is None or initial.periodic != (True, True, True):
        raise ValueError("transition scan requires a fully periodic three-dimensional cell.")
    if build_cutoff_graph(initial, cutoff) != reference.graph:
        raise ValueError("reference graph differs from the declared cutoff.")
    if model.evaluate(
        reference.configuration, reference.graph, reference.input_features,
        reference.resonance, reference.execution,
    ) != reference:
        raise ValueError("reference energy differs from the supplied rank-two TR-EIP model.")
    final_graph = build_cutoff_graph(scale_periodic_configuration(initial, target), cutoff)
    start_edges = set(reference.graph.edges)
    final_edges = set(final_graph.edges)
    changed = tuple(edge for edge in (*reference.graph.edges, *final_graph.edges)
                    if (edge in start_edges) != (edge in final_edges))
    critical = []
    for edge in changed:
        displacement, image = minimum_image(
            initial.positions[edge.source], initial.positions[edge.receiver],
            initial.cell, initial.periodic,
        )
        if image != edge.image:
            raise ValueError("minimum-image convention changed across isotropic scaling.")
        distance = sqrt(fsum(component * component for component in displacement))
        if not isfinite(distance) or distance <= 0.0:
            raise ValueError("crossing pairs require positive finite reference distance.")
        scale = cutoff / distance
        if not min(1.0, target) - 1e-12 <= scale <= max(1.0, target) + 1e-12:
            raise ValueError("analytic cutoff scale is outside the requested sweep.")
        critical.append((scale, edge))
    critical.sort(key=lambda record: record[0], reverse=target < 1.0)
    grouped: list[list[tuple[float, InteractionEdge]]] = []
    for record in critical:
        if not grouped or not isclose(record[0], grouped[-1][0][0], rel_tol=1e-12, abs_tol=1e-12):
            grouped.append([record])
        else:
            grouped[-1].append(record)
    direction = (
        FLiBeCutoffSweepDirection.COMPRESSION if target < 1.0
        else FLiBeCutoffSweepDirection.EXPANSION
    )
    crossings = []
    for group in grouped:
        center = group[0][0]
        before_scale = center * (1.0 + probe if target < 1.0 else 1.0 - probe)
        after_scale = center * (1.0 - probe if target < 1.0 else 1.0 + probe)
        if before_scale <= 0.0 or after_scale <= 0.0:
            raise ValueError("cutoff probe scales must remain positive.")
        first_graph = build_cutoff_graph(scale_periodic_configuration(initial, before_scale), cutoff)
        second_graph = build_cutoff_graph(scale_periodic_configuration(initial, after_scale), cutoff)
        first_set, second_set = set(first_graph.edges), set(second_graph.edges)
        added = tuple(edge for edge in second_graph.edges if edge not in first_set)
        removed = tuple(edge for edge in first_graph.edges if edge not in second_set)
        listed = {edge for _, edge in group}
        if set((*added, *removed)) != listed:
            raise ValueError("probe width encompasses a different cutoff event grouping.")
        if not first_graph.edges or not second_graph.edges:
            raise ValueError("rank-two crossing energy requires nonempty graphs on both sides.")
        at_boundary = scale_periodic_configuration(initial, center)
        energy_before = model.rank_two_model.evaluate(
            at_boundary, first_graph, reference.resonance_features, reference.execution,
        )
        energy_after = model.rank_two_model.evaluate(
            at_boundary, second_graph, reference.resonance_features, reference.execution,
        )
        crossings.append(FLiBeRankTwoCutoffCrossing(
            linear_scale=center,
            direction=direction,
            probe_before_scale=before_scale,
            probe_after_scale=after_scale,
            boundary_configuration=at_boundary,
            graph_before=first_graph,
            graph_after=second_graph,
            energy_before=energy_before,
            energy_after=energy_after,
            added_edges=added,
            removed_edges=removed,
        ))
    return FLiBeRankTwoCutoffTransitionScan(
        reference=reference,
        cutoff=cutoff,
        target_linear_scale=target,
        target_graph=final_graph,
        probe_relative_width=probe,
        crossings=tuple(crossings),
    )
