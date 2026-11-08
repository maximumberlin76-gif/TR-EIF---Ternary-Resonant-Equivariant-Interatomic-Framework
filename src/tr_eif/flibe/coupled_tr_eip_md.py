
"""FLiBe TR-EIP energy correspondence across scheduled TR-EIF MD boundaries.

The shared reference energy model couples continuous resonance channels,
retained balanced-ternary conditioning, E(3)-equivariant representations,
and coordinate-derived forces during molecular-dynamics integration.

FLiBe coordination and thermodynamic coordinates remain explicitly typed
context for each TR-EIP evaluation. The same model and retained execution
are evaluated at three boundaries: before scheduled events, after resonance
and ternary events, and after a mechanical velocity-Verlet step.

The supplied thermodynamic context is retained for this one scheduled call;
the independently scheduled physical-state estimator determines its updates.
"""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy import ConservativeForceEvaluator
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.graph import InteractionGraph, build_cutoff_graph
from tr_eif.md.coupled_execution import (
    CoupledMolecularDynamicsState,
    CoupledMolecularDynamicsStep,
    execute_coupled_md_step,
)
from tr_eif.resonance import PhaseDynamicsParameters, ResonanceState
from tr_eif.ternary import TernaryExecutionGuard, TernaryExecutionVector

from .configuration import FLiBeConfiguration
from .coordination import build_flibe_coordination_state
from .resonance_descriptor import build_flibe_resonance_descriptor
from .ternary_interpretation import FLiBeTernaryInterpretation
from .thermodynamic_state import FLiBeThermodynamicState
from .tr_eip import FLiBeTREIPModel, FLiBeTREIPResult


@dataclass(frozen=True, slots=True)
class FLiBeTREIPMDCoupledStep:
    """Three source-aligned FLiBe TR-EIP energy evaluations and one MD step."""

    coupled_step: CoupledMolecularDynamicsStep
    thermodynamic_state: FLiBeThermodynamicState
    interpretation: FLiBeTernaryInterpretation
    before_events: FLiBeTREIPResult
    after_events: FLiBeTREIPResult
    after_mechanics: FLiBeTREIPResult

    def __post_init__(self) -> None:
        if not isinstance(self.coupled_step, CoupledMolecularDynamicsStep):
            raise TypeError("coupled_step must be CoupledMolecularDynamicsStep.")
        if not isinstance(self.thermodynamic_state, FLiBeThermodynamicState):
            raise TypeError("thermodynamic_state must be FLiBeThermodynamicState.")
        if not isinstance(self.interpretation, FLiBeTernaryInterpretation):
            raise TypeError("interpretation must be FLiBeTernaryInterpretation.")
        for name in ("before_events", "after_events", "after_mechanics"):
            if not isinstance(getattr(self, name), FLiBeTREIPResult):
                raise TypeError(f"{name} must be FLiBeTREIPResult.")

        step = self.coupled_step
        initial = step.previous
        final = step.current

        if (self.before_events.configuration.configuration
                != initial.md_state.configuration):
            raise ValueError("initial FLiBe configuration differs from scheduled MD state.")
        if (self.after_events.configuration.configuration
                != initial.md_state.configuration):
            raise ValueError("event energy must use the premechanical configuration.")
        if (self.after_mechanics.configuration.configuration
                != final.md_state.configuration):
            raise ValueError("final FLiBe configuration differs from scheduled MD state.")
        if self.before_events.execution != initial.ternary_execution:
            raise ValueError("initial TR-EIP retained execution differs.")
        if (self.after_events.execution != final.ternary_execution
                or self.after_mechanics.execution != final.ternary_execution):
            raise ValueError("TR-EIP execution differs from committed ternary state.")
        if self.before_events.resonance.resonance_state != initial.resonance_state:
            raise ValueError("initial TR-EIP resonance differs.")
        if (self.after_events.resonance.resonance_state != final.resonance_state
                or self.after_mechanics.resonance.resonance_state != final.resonance_state):
            raise ValueError("TR-EIP resonance differs from propagated oscillator state.")
        for name in ("before_events", "after_events", "after_mechanics"):
            if (getattr(self, name).resonance.thermodynamic_state
                    != self.thermodynamic_state):
                raise ValueError("FLiBe thermodynamic context differs across boundaries.")

        for observed, expected in (
            (self.before_events.energy_result.energy, step.energy_before_events),
            (self.after_events.energy_result.energy, step.energy_after_events),
            (self.after_mechanics.energy_result.energy, step.energy_after_mechanics),
        ):
            if observed != expected:
                raise ValueError("TR-EIP and coupled MD energy boundaries differ.")

        if step.ternary_update is not None:
            request = self.interpretation.target_from_descriptor(
                self.after_events.resonance.descriptor
            )
            if request is not step.requested_target:
                raise ValueError("FLiBe ternary request differs from scheduled projection.")

    @property
    def current(self) -> CoupledMolecularDynamicsState:
        """Return the updated mechanical, resonance and retained ternary state."""
        return self.coupled_step.current

    @property
    def event_potential_energy_change(self) -> float:
        """Return the fixed-geometry energy change from scheduled events."""
        return self.coupled_step.event_potential_energy_change

    @property
    def mechanical_potential_energy_change(self) -> float:
        """Return the subsequent coordinate-driven potential-energy change."""
        return self.coupled_step.mechanical_potential_energy_change


def _evaluate_flibe_boundary(
    model: FLiBeTREIPModel,
    *,
    configuration: FLiBeConfiguration,
    graph: InteractionGraph,
    features: NodeFeatureVector,
    resonance_state: ResonanceState,
    execution: TernaryExecutionVector,
    thermodynamic_state: FLiBeThermodynamicState,
) -> FLiBeTREIPResult:
    descriptor = build_flibe_resonance_descriptor(
        configuration=configuration,
        coordination=build_flibe_coordination_state(configuration, graph),
        thermodynamic_state=thermodynamic_state,
        resonance_state=resonance_state,
        provenance=model.provenance,
        source=model.source,
    )
    return model.evaluate(configuration, graph, features, descriptor, execution)


def execute_flibe_tr_eip_coupled_md_step(
    state: CoupledMolecularDynamicsState,
    *,
    model: FLiBeTREIPModel,
    force_evaluator: ConservativeForceEvaluator,
    base_features: NodeFeatureVector,
    thermodynamic_state: FLiBeThermodynamicState,
    interpretation: FLiBeTernaryInterpretation,
    cutoff: float,
    phase_parameters: PhaseDynamicsParameters | None = None,
    phase_time_step: float | None = None,
    ternary_event: bool = False,
    guards: tuple[TernaryExecutionGuard, ...] | None = None,
    mechanical_time_step: float | None = None,
) -> FLiBeTREIPMDCoupledStep:
    """Evaluate TR-EIP at each boundary of one explicit hybrid MD schedule.

    A scheduled ternary event uses the supplied FLiBe interpretation to
    generate a requested target, while the underlying vector executor
    resolves retained states and pending destinations. The force evaluator
    uses the same reference energy functional and frozen within-step
    resonance/ternary features as the corresponding TR-EIP evaluations.
    """
    if not isinstance(state, CoupledMolecularDynamicsState):
        raise TypeError("state must be CoupledMolecularDynamicsState.")
    if not isinstance(model, FLiBeTREIPModel):
        raise TypeError("model must be FLiBeTREIPModel.")
    if not isinstance(force_evaluator, ConservativeForceEvaluator):
        raise TypeError("force_evaluator must be ConservativeForceEvaluator.")
    if not isinstance(base_features, NodeFeatureVector):
        raise TypeError("base_features must be NodeFeatureVector.")
    if not isinstance(thermodynamic_state, FLiBeThermodynamicState):
        raise TypeError("thermodynamic_state must be FLiBeThermodynamicState.")
    if not isinstance(interpretation, FLiBeTernaryInterpretation):
        raise TypeError("interpretation must be FLiBeTernaryInterpretation.")

    before_configuration = FLiBeConfiguration(state.md_state.configuration)
    before_configuration.composition()

    if base_features.node_count != before_configuration.atom_count:
        raise ValueError("FLiBe feature and atom counts differ.")

    coupled = execute_coupled_md_step(
        state,
        model=model.energy_model,
        force_evaluator=force_evaluator,
        base_features=base_features,
        cutoff=cutoff,
        phase_parameters=phase_parameters,
        phase_time_step=phase_time_step,
        ternary_event=ternary_event,
        projection=interpretation.projection if ternary_event else None,
        thresholds=interpretation.thresholds if ternary_event else None,
        guards=guards,
        mechanical_time_step=mechanical_time_step,
    )

    before_graph = build_cutoff_graph(before_configuration.configuration, cutoff)

    before = _evaluate_flibe_boundary(
        model,
        configuration=before_configuration,
        graph=before_graph,
        features=base_features,
        resonance_state=state.resonance_state,
        execution=state.ternary_execution,
        thermodynamic_state=thermodynamic_state,
    )

    event = _evaluate_flibe_boundary(
        model,
        configuration=before_configuration,
        graph=before_graph,
        features=base_features,
        resonance_state=coupled.current.resonance_state,
        execution=coupled.current.ternary_execution,
        thermodynamic_state=thermodynamic_state,
    )

    final_configuration = FLiBeConfiguration(coupled.current.md_state.configuration)
    final_configuration.composition()
    final_graph = build_cutoff_graph(final_configuration.configuration, cutoff)

    mechanical = _evaluate_flibe_boundary(
        model,
        configuration=final_configuration,
        graph=final_graph,
        features=base_features,
        resonance_state=coupled.current.resonance_state,
        execution=coupled.current.ternary_execution,
        thermodynamic_state=thermodynamic_state,
    )

    return FLiBeTREIPMDCoupledStep(
        coupled_step=coupled,
        thermodynamic_state=thermodynamic_state,
        interpretation=interpretation,
        before_events=before,
        after_events=event,
        after_mechanics=mechanical,
    )
