
"""Explicit multirate coupling of resonance, ternary execution, and atomistic MD.

A coupling call selects phase integration, one ternary event, a mechanical
velocity-Verlet step, or any ordered combination of these operations.
Scheduled operations occur in the order phase -> request -> retained-state
execution -> mechanics. The phase and mechanical clocks evolve separately.

Resonance phase order and frequency spread become two invariant scalar
feature channels. The retained ternary state conditions the equivariant
reference energy model and its coordinate-derived forces. Between scheduler
events, the corresponding variables remain retained. Potential-energy
changes caused by a phase or ternary event are recorded separately from
those produced by a mechanical step.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.energy import (
    ConservativeForceEvaluator,
    EnergyState,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import NodeFeatures, NodeFeatureVector
from tr_eif.graph import build_cutoff_graph
from tr_eif.resonance import (
    PhaseDynamicsParameters,
    ResonanceDescriptor,
    ResonanceState,
    resonance_descriptor,
)
from tr_eif.ternary import (
    ResonanceProjection,
    TernaryExecutionGuard,
    TernaryExecutionVector,
    TernaryState,
    TernaryTargetThresholds,
    TernaryVector,
    ternary_target_from_descriptor,
)

from .execution import MolecularDynamicsStepResult, velocity_verlet_step
from .resonance_propagation import (
    MolecularDynamicsResonanceStep,
    propagate_md_resonance_state,
)
from .state import MolecularDynamicsState
from .ternary_propagation import (
    MolecularDynamicsTernaryStep,
    propagate_md_ternary_state,
)


def _positive_real(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _nonnegative_real(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number.")
    number = float(value)
    if not isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative.")
    return number


def _nonnegative_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < 0:
        raise ValueError(f"{name} must be nonnegative.")
    return value


@dataclass(frozen=True, slots=True)
class CoupledMolecularDynamicsState:
    """Mechanical, continuous-phase, and retained-ternary state with clocks."""

    md_state: MolecularDynamicsState
    resonance_state: ResonanceState
    ternary_execution: TernaryExecutionVector
    resonance_time: float = 0.0
    resonance_step_count: int = 0
    ternary_event_count: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.md_state, MolecularDynamicsState):
            raise TypeError("md_state must be MolecularDynamicsState.")
        if not isinstance(self.resonance_state, ResonanceState):
            raise TypeError("resonance_state must be ResonanceState.")
        if not isinstance(self.ternary_execution, TernaryExecutionVector):
            raise TypeError("ternary_execution must be TernaryExecutionVector.")
        nodes = self.md_state.atom_count
        if (self.resonance_state.oscillator_count != nodes
                or self.ternary_execution.node_count != nodes):
            raise ValueError("MD atom, resonance oscillator, and ternary node counts differ.")
        object.__setattr__(self, "resonance_time", _nonnegative_real(
            self.resonance_time, "resonance_time"
        ))
        _nonnegative_int(self.resonance_step_count, "resonance_step_count")
        _nonnegative_int(self.ternary_event_count, "ternary_event_count")


def append_md_resonance_features(
    features: NodeFeatureVector,
    descriptor: ResonanceDescriptor,
) -> NodeFeatureVector:
    """Append invariant phase-order and frequency-spread scalars in fixed order."""
    if not isinstance(features, NodeFeatureVector):
        raise TypeError("features must be NodeFeatureVector.")
    if not isinstance(descriptor, ResonanceDescriptor):
        raise TypeError("descriptor must be ResonanceDescriptor.")
    return NodeFeatureVector(nodes=tuple(
        NodeFeatures(
            scalars=(*node.scalars, descriptor.phase_order, descriptor.frequency_spread),
            vectors=node.vectors,
        ) for node in features.nodes
    ))


@dataclass(frozen=True, slots=True)
class CoupledMolecularDynamicsStep:
    """One scheduled hybrid update with separately measured energy boundaries."""

    previous: CoupledMolecularDynamicsState
    current: CoupledMolecularDynamicsState
    resonance_update: MolecularDynamicsResonanceStep | None
    ternary_update: MolecularDynamicsTernaryStep | None
    mechanical_update: MolecularDynamicsStepResult | None
    descriptor: ResonanceDescriptor
    requested_target: TernaryState | None
    requested_targets: TernaryVector | None
    energy_before_events: EnergyState
    energy_after_events: EnergyState
    energy_after_mechanics: EnergyState

    def __post_init__(self) -> None:
        if not isinstance(self.previous, CoupledMolecularDynamicsState):
            raise TypeError("previous must be CoupledMolecularDynamicsState.")
        if not isinstance(self.current, CoupledMolecularDynamicsState):
            raise TypeError("current must be CoupledMolecularDynamicsState.")
        if not isinstance(self.descriptor, ResonanceDescriptor):
            raise TypeError("descriptor must be ResonanceDescriptor.")
        for name in ("energy_before_events", "energy_after_events", "energy_after_mechanics"):
            if not isinstance(getattr(self, name), EnergyState):
                raise TypeError(f"{name} must be EnergyState.")
        if self.resonance_update is None:
            if (self.previous.resonance_state != self.current.resonance_state
                    or self.previous.resonance_time != self.current.resonance_time
                    or self.previous.resonance_step_count != self.current.resonance_step_count):
                raise ValueError("resonance changed outside its scheduled update.")
        else:
            if (self.resonance_update.md_state != self.previous.md_state
                    or self.resonance_update.previous != self.previous.resonance_state
                    or self.resonance_update.current != self.current.resonance_state
                    or self.current.resonance_step_count != self.previous.resonance_step_count + 1):
                raise ValueError("resonance update is not aligned with the hybrid state.")
        if self.ternary_update is None:
            if (self.previous.ternary_execution != self.current.ternary_execution
                    or self.previous.ternary_event_count != self.current.ternary_event_count
                    or self.requested_target is not None or self.requested_targets is not None):
                raise ValueError("ternary state changed outside its scheduled event.")
        else:
            if (self.ternary_update.md_state != self.previous.md_state
                    or self.ternary_update.previous != self.previous.ternary_execution
                    or self.ternary_update.current != self.current.ternary_execution
                    or self.ternary_update.requested_targets != self.requested_targets
                    or self.requested_target is None
                    or self.current.ternary_event_count != self.previous.ternary_event_count + 1):
                raise ValueError("ternary event is not aligned with the hybrid state.")
        if self.mechanical_update is None:
            if self.current.md_state != self.previous.md_state:
                raise ValueError("MD state changed outside its mechanical step.")
            if self.energy_after_mechanics != self.energy_after_events:
                raise ValueError("mechanics-free event changed its post-event energy.")
        else:
            if (self.mechanical_update.previous != self.previous.md_state
                    or self.mechanical_update.current != self.current.md_state):
                raise ValueError("mechanical step is not aligned with the hybrid state.")

    @property
    def event_potential_energy_change(self) -> float:
        """Potential-energy jump from phase and retained-state events at fixed geometry."""
        return (self.energy_after_events.total_energy
                - self.energy_before_events.total_energy)

    @property
    def mechanical_potential_energy_change(self) -> float:
        """Potential-energy change from the coordinate integration interval."""
        return (self.energy_after_mechanics.total_energy
                - self.energy_after_events.total_energy)


def execute_coupled_md_step(
    state: CoupledMolecularDynamicsState,
    *,
    model: ReferenceEnergyModel,
    force_evaluator: ConservativeForceEvaluator,
    base_features: NodeFeatureVector,
    cutoff: float,
    phase_parameters: PhaseDynamicsParameters | None = None,
    phase_time_step: float | None = None,
    ternary_event: bool = False,
    projection: ResonanceProjection | None = None,
    thresholds: TernaryTargetThresholds | None = None,
    guards: tuple[TernaryExecutionGuard, ...] | None = None,
    mechanical_time_step: float | None = None,
) -> CoupledMolecularDynamicsStep:
    """Execute the selected phase, ternary, and mechanical clocks in that order.

    A ternary event samples the current resonance descriptor, projects it to
    one requested target, and applies that target to nodes without a pending
    route. Nodes with pending destinations retain their earlier requests.
    Exactly one guarded route leg can commit per node per event.

    Each mechanical step freezes the most recent resonance-derived features
    and retained ternary execution across its two force evaluations. Distinct
    phase and mechanical time increments preserve independent clock semantics.
    """
    if not isinstance(state, CoupledMolecularDynamicsState):
        raise TypeError("state must be CoupledMolecularDynamicsState.")
    if not isinstance(model, ReferenceEnergyModel):
        raise TypeError("model must be ReferenceEnergyModel.")
    if not isinstance(force_evaluator, ConservativeForceEvaluator):
        raise TypeError("force_evaluator must be ConservativeForceEvaluator.")
    if not isinstance(base_features, NodeFeatureVector):
        raise TypeError("base_features must be NodeFeatureVector.")
    if base_features.node_count != state.md_state.atom_count:
        raise ValueError("feature node count must match MD atom count.")
    if not isinstance(ternary_event, bool):
        raise TypeError("ternary_event must be a bool.")
    if model.energy_functional.scalar_channel_count != base_features.scalar_channel_count + 2:
        raise ValueError("energy weights must match base scalar channels plus two resonance channels.")
    validated_cutoff = _positive_real(cutoff, "cutoff")
    if phase_time_step is None:
        if phase_parameters is not None:
            raise ValueError("phase_parameters require a scheduled phase_time_step.")
    else:
        _positive_real(phase_time_step, "phase_time_step")
        if not isinstance(phase_parameters, PhaseDynamicsParameters):
            raise TypeError("phase_parameters must be supplied for a phase step.")
    if mechanical_time_step is not None:
        _positive_real(mechanical_time_step, "mechanical_time_step")
    if ternary_event:
        if not isinstance(projection, ResonanceProjection):
            raise TypeError("projection is required for a ternary event.")
        if not isinstance(thresholds, TernaryTargetThresholds):
            raise TypeError("thresholds are required for a ternary event.")
    elif any(value is not None for value in (projection, thresholds, guards)):
        raise ValueError("projection, thresholds and guards require a ternary event.")
    if phase_time_step is None and not ternary_event and mechanical_time_step is None:
        raise ValueError("at least one scheduler operation must be requested.")

    start_graph = build_cutoff_graph(state.md_state.configuration, validated_cutoff)
    descriptor_before = resonance_descriptor(state.resonance_state)
    initial_features = append_md_resonance_features(base_features, descriptor_before)
    before_energy = model.evaluate(
        state.md_state.configuration, start_graph, initial_features,
        state.ternary_execution,
    ).energy

    phase_update = None
    new_resonance = state.resonance_state
    if phase_time_step is not None:
        assert phase_parameters is not None
        phase_update = propagate_md_resonance_state(
            state.md_state, new_resonance, phase_parameters,
            validated_cutoff, phase_time_step,
        )
        new_resonance = phase_update.current
    descriptor = resonance_descriptor(new_resonance)
    features = append_md_resonance_features(base_features, descriptor)

    ternary_update = None
    request = None
    targets = None
    new_execution = state.ternary_execution
    if ternary_event:
        assert projection is not None and thresholds is not None
        request = ternary_target_from_descriptor(descriptor, projection, thresholds)
        targets = tuple(
            node.pending_target if node.pending_target is not None else request
            for node in new_execution.states
        )
        ternary_update = propagate_md_ternary_state(
            state.md_state, new_execution, requested_targets=targets, guards=guards,
        )
        new_execution = ternary_update.current

    event_energy = model.evaluate(
        state.md_state.configuration, start_graph, features, new_execution,
    ).energy
    mechanical_update = None
    new_md_state = state.md_state
    if mechanical_time_step is not None:
        mechanical_update = velocity_verlet_step(
            state=new_md_state,
            model=model,
            force_evaluator=force_evaluator,
            features=features,
            execution=new_execution,
            cutoff=validated_cutoff,
            time_step=mechanical_time_step,
        )
        new_md_state = mechanical_update.current
        final_graph = mechanical_update.graph_after
        final_energy = model.evaluate(
            new_md_state.configuration, final_graph, features, new_execution,
        ).energy
    else:
        final_energy = event_energy

    updated = CoupledMolecularDynamicsState(
        md_state=new_md_state,
        resonance_state=new_resonance,
        ternary_execution=new_execution,
        resonance_time=state.resonance_time + (phase_time_step or 0.0),
        resonance_step_count=state.resonance_step_count + (phase_time_step is not None),
        ternary_event_count=state.ternary_event_count + ternary_event,
    )
    return CoupledMolecularDynamicsStep(
        previous=state,
        current=updated,
        resonance_update=phase_update,
        ternary_update=ternary_update,
        mechanical_update=mechanical_update,
        descriptor=descriptor,
        requested_target=request,
        requested_targets=targets,
        energy_before_events=before_energy,
        energy_after_events=event_energy,
        energy_after_mechanics=final_energy,
    )
