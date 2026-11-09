
"""FLiBe rank-two TR-EIP correspondence across multirate TR-EIF MD events.

The generic scheduler advances the continuous resonance, balanced ternary,
and mechanical clocks. The FLiBe TR-EIP specialization evaluates the same
rank-two conservative energy at the pre-event, post-event, and post-mechanical
boundaries with explicit graph-relative and thermodynamic context.

Retained ternary states condition the E(3) scalar, vector, and rank-two
representations. Pending targets remain distinct from committed states.
The supplied thermodynamic state is held fixed during this scheduled call;
its update belongs to an independently declared physical-state schedule.
"""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy.rank_two_model import RankTwoConservativeForceEvaluator
from tr_eif.equivariant.rank_two import ScalarVectorTensorFeatures
from tr_eif.graph import InteractionGraph, build_cutoff_graph
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState
from tr_eif.md.rank_two_coupled_execution import (
    RankTwoCoupledMolecularDynamicsStep,
    execute_rank_two_coupled_md_step,
)
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import TernaryExecutionGuard, TernaryExecutionVector

from .configuration import FLiBeConfiguration
from .coordination import build_flibe_coordination_state
from .rank_two_tr_eip import FLiBeRankTwoTREIPModel, FLiBeRankTwoTREIPResult
from .resonance_descriptor import build_flibe_resonance_descriptor
from .ternary_interpretation import FLiBeTernaryInterpretation
from .thermodynamic_state import FLiBeThermodynamicState


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPMDCoupledStep:
    """FLiBe domain evaluations aligned to one multirate rank-two MD step."""

    coupled_step: RankTwoCoupledMolecularDynamicsStep
    thermodynamic_state: FLiBeThermodynamicState
    interpretation: FLiBeTernaryInterpretation
    before_events: FLiBeRankTwoTREIPResult
    after_events: FLiBeRankTwoTREIPResult
    after_mechanics: FLiBeRankTwoTREIPResult

    def __post_init__(self) -> None:
        if not isinstance(self.coupled_step, RankTwoCoupledMolecularDynamicsStep):
            raise TypeError("coupled_step must be RankTwoCoupledMolecularDynamicsStep.")
        if not isinstance(self.thermodynamic_state, FLiBeThermodynamicState):
            raise TypeError("thermodynamic_state must be FLiBeThermodynamicState.")
        if not isinstance(self.interpretation, FLiBeTernaryInterpretation):
            raise TypeError("interpretation must be FLiBeTernaryInterpretation.")
        for name in ("before_events", "after_events", "after_mechanics"):
            if not isinstance(getattr(self, name), FLiBeRankTwoTREIPResult):
                raise TypeError(f"{name} must be FLiBeRankTwoTREIPResult.")

        step = self.coupled_step
        before = step.previous
        after = step.current
        boundaries = (
            ("before_events", before.md_state, before.resonance_state,
             before.ternary_execution, step.energy_before_events),
            ("after_events", before.md_state, after.resonance_state,
             after.ternary_execution, step.energy_after_events),
            ("after_mechanics", after.md_state, after.resonance_state,
             after.ternary_execution, step.energy_after_mechanics),
        )
        for name, md_state, resonance, retained, energy in boundaries:
            observed = getattr(self, name)
            if observed.configuration.configuration != md_state.configuration:
                raise ValueError(f"{name} atomic configuration differs from MD state.")
            if observed.resonance.resonance_state != resonance:
                raise ValueError(f"{name} continuous resonance state differs.")
            if observed.execution != retained:
                raise ValueError(f"{name} retained ternary execution differs.")
            if observed.resonance.thermodynamic_state != self.thermodynamic_state:
                raise ValueError(f"{name} thermodynamic context differs.")
            if observed.augmented_result != energy:
                raise ValueError(f"{name} complete rank-two energy differs from MD.")

        if step.event_update is None:
            if self.before_events != self.after_events:
                raise ValueError("event-free FLiBe evaluation changed at fixed geometry.")
        elif step.event_update.ternary_update is not None:
            requested = self.interpretation.target_from_descriptor(
                self.after_events.resonance.descriptor
            )
            if requested is not step.requested_target:
                raise ValueError("FLiBe ternary request differs from the MD projection.")

        mechanics = step.mechanical_update
        if mechanics is None:
            if self.after_events != self.after_mechanics:
                raise ValueError("mechanics-free FLiBe evaluation changed.")
        else:
            if self.after_events.graph != mechanics.graph_before:
                raise ValueError("event FLiBe graph differs from mechanical input graph.")
            if self.after_mechanics.graph != mechanics.graph_after:
                raise ValueError("final FLiBe graph differs from mechanical output graph.")
            if (mechanics.forces_before.atom_count != before.md_state.atom_count
                    or mechanics.forces_after.atom_count != after.md_state.atom_count):
                raise ValueError("mechanical force and FLiBe atom counts differ.")

    @property
    def current(self) -> CoupledMolecularDynamicsState:
        """Return the updated mechanical, resonance, and retained ternary state."""
        return self.coupled_step.current

    @property
    def event_potential_energy_change(self) -> float:
        """Full-energy change at the fixed-geometry phase/ternary boundary."""
        return self.coupled_step.event_potential_energy_change

    @property
    def mechanical_potential_energy_change(self) -> float:
        """Full-energy change across the coordinate integration interval."""
        return self.coupled_step.mechanical_potential_energy_change


def _evaluate_flibe_boundary(
    model: FLiBeRankTwoTREIPModel,
    configuration: FLiBeConfiguration,
    graph: InteractionGraph,
    features: ScalarVectorTensorFeatures,
    resonance_state: ResonanceState,
    execution: TernaryExecutionVector,
    thermodynamic_state: FLiBeThermodynamicState,
) -> FLiBeRankTwoTREIPResult:
    """Evaluate a complete TR-EIP energy with registered FLiBe context."""
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
        provenance=model.tr_eip_model.provenance,
        source=model.tr_eip_model.source,
    )
    return model.evaluate(configuration, graph, features, descriptor, execution)


def execute_flibe_rank_two_tr_eip_coupled_md_step(
    state: CoupledMolecularDynamicsState,
    *,
    model: FLiBeRankTwoTREIPModel,
    force_evaluator: RankTwoConservativeForceEvaluator,
    features: ScalarVectorTensorFeatures,
    thermodynamic_state: FLiBeThermodynamicState,
    interpretation: FLiBeTernaryInterpretation,
    cutoff: float,
    phase_parameters: PhaseDynamicsParameters | None = None,
    phase_time_step: float | None = None,
    ternary_event: bool = False,
    guards: tuple[TernaryExecutionGuard, ...] | None = None,
    mechanical_time_step: float | None = None,
) -> FLiBeRankTwoTREIPMDCoupledStep:
    """Advance selected TR-EIF clocks and bind three FLiBe TR-EIP energies.

    The generic rank-two executor determines scheduler order and applies the
    complete-energy forces to mechanics. The FLiBe layer records identical
    energy boundaries using typed species, coordination, resonance, and
    thermodynamic context; the projected request remains separate from the
    retained ternary state and any pending destination.
    """
    if not isinstance(state, CoupledMolecularDynamicsState):
        raise TypeError("state must be CoupledMolecularDynamicsState.")
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(force_evaluator, RankTwoConservativeForceEvaluator):
        raise TypeError("force_evaluator must be RankTwoConservativeForceEvaluator.")
    if not isinstance(features, ScalarVectorTensorFeatures):
        raise TypeError("features must be ScalarVectorTensorFeatures.")
    if not isinstance(thermodynamic_state, FLiBeThermodynamicState):
        raise TypeError("thermodynamic_state must be FLiBeThermodynamicState.")
    if not isinstance(interpretation, FLiBeTernaryInterpretation):
        raise TypeError("interpretation must be FLiBeTernaryInterpretation.")

    initial = FLiBeConfiguration(state.md_state.configuration)
    initial.composition()
    if features.node_count != initial.atom_count:
        raise ValueError("FLiBe feature and atom counts differ.")

    step = execute_rank_two_coupled_md_step(
        state,
        model=model.rank_two_model,
        force_evaluator=force_evaluator,
        features=features,
        cutoff=cutoff,
        phase_parameters=phase_parameters,
        phase_time_step=phase_time_step,
        ternary_event=ternary_event,
        projection=interpretation.projection if ternary_event else None,
        thresholds=interpretation.thresholds if ternary_event else None,
        guards=guards,
        mechanical_time_step=mechanical_time_step,
    )

    initial_graph = build_cutoff_graph(initial.configuration, cutoff)
    before = _evaluate_flibe_boundary(
        model, initial, initial_graph, features, state.resonance_state,
        state.ternary_execution, thermodynamic_state,
    )
    if step.event_update is None:
        after_events = before
    else:
        after_events = _evaluate_flibe_boundary(
            model, initial, initial_graph, features, step.current.resonance_state,
            step.current.ternary_execution, thermodynamic_state,
        )
    if step.mechanical_update is None:
        after_mechanics = after_events
    else:
        final_configuration = FLiBeConfiguration(step.current.md_state.configuration)
        final_configuration.composition()
        after_mechanics = _evaluate_flibe_boundary(
            model, final_configuration, step.mechanical_update.graph_after,
            features, step.current.resonance_state, step.current.ternary_execution,
            thermodynamic_state,
        )
    return FLiBeRankTwoTREIPMDCoupledStep(
        coupled_step=step,
        thermodynamic_state=thermodynamic_state,
        interpretation=interpretation,
        before_events=before,
        after_events=after_events,
        after_mechanics=after_mechanics,
    )
