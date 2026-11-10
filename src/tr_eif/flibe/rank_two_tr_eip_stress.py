
"""Typed rank-two cell-strain stress at FLiBe TR-EIP and MD boundaries.

The FLiBe TR-EIP reference and rank-two extension share one interatomic
energy functional. Homogeneous strain differentiates its scalar/vector and
tensor contributions at a fixed interaction graph, resonance descriptor,
feature state, and committed balanced-ternary execution. Source coordination
and thermodynamic coordinates remain attached to each boundary evaluation.

The three observations of a completed multirate MD step use the recorded
pre-event, post-event, and post-mechanical states. Potential pressure is
computed from the strain-derived stress trace; the supplied thermodynamic
pressure remains an independent physical-state coordinate.
"""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy.rank_two_stress import (
    RankTwoConservativeStressEvaluator,
    RankTwoConservativeStressResult,
)
from tr_eif.equivariant.rank_two import ScalarVectorTensorFeatures
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .configuration import FLiBeConfiguration
from .coupled_rank_two_tr_eip_md import FLiBeRankTwoTREIPMDCoupledStep
from .rank_two_tr_eip import FLiBeRankTwoTREIPModel, FLiBeRankTwoTREIPResult
from .resonance_descriptor import FLiBeResonanceDescriptor


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPStressResult:
    """One FLiBe domain energy and its complete cell-strain stress evidence."""

    evaluation: FLiBeRankTwoTREIPResult
    stress: RankTwoConservativeStressResult

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation, FLiBeRankTwoTREIPResult):
            raise TypeError("evaluation must be FLiBeRankTwoTREIPResult.")
        if not isinstance(self.stress, RankTwoConservativeStressResult):
            raise TypeError("stress must be RankTwoConservativeStressResult.")
        if self.evaluation.configuration.configuration.cell is None:
            raise ValueError("FLiBe stress requires a simulation cell.")
        if self.stress.reference_evaluation != self.evaluation.augmented_result:
            raise ValueError("stress and FLiBe TR-EIP full-energy evaluations differ.")
        if self.stress.reference_evaluation.layer.previous != self.evaluation.resonance_features:
            raise ValueError("stress and FLiBe resonance-conditioned features differ.")
        if self.stress.reference_evaluation.reference_energy != self.evaluation.reference_energy:
            raise ValueError("stress and FLiBe reference energies differ.")
        if self.stress.reference_evaluation.tensor_energy != self.evaluation.tensor_energy:
            raise ValueError("stress and FLiBe rank-two energies differ.")

    @property
    def potential_pressure(self) -> float:
        """Return the potential pressure inferred from the full strain stress."""
        return self.stress.potential_pressure


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPMDStressTrace:
    """Strain stresses at all three boundaries of a completed hybrid MD step."""

    coupled: FLiBeRankTwoTREIPMDCoupledStep
    before_events: FLiBeRankTwoTREIPStressResult
    after_events: FLiBeRankTwoTREIPStressResult
    after_mechanics: FLiBeRankTwoTREIPStressResult

    def __post_init__(self) -> None:
        if not isinstance(self.coupled, FLiBeRankTwoTREIPMDCoupledStep):
            raise TypeError("coupled must be FLiBeRankTwoTREIPMDCoupledStep.")
        for name in ("before_events", "after_events", "after_mechanics"):
            record = getattr(self, name)
            if not isinstance(record, FLiBeRankTwoTREIPStressResult):
                raise TypeError(f"{name} must be FLiBeRankTwoTREIPStressResult.")
            if record.evaluation != getattr(self.coupled, name):
                raise ValueError(f"{name} stress differs from the coupled TR-EIP boundary.")
            if (record.evaluation.resonance.thermodynamic_state
                    != self.coupled.thermodynamic_state):
                raise ValueError(f"{name} thermodynamic context differs.")
        if (self.before_events.stress.reference_volume
                != self.after_events.stress.reference_volume):
            raise ValueError("phase and ternary events must retain reference cell volume.")
        if self.coupled.coupled_step.event_update is None:
            if self.before_events != self.after_events:
                raise ValueError("event-free boundary must retain its stress evidence.")
        if self.coupled.coupled_step.mechanical_update is None:
            if self.after_events != self.after_mechanics:
                raise ValueError("mechanics-free boundary must retain its stress evidence.")

    @property
    def potential_pressures(self) -> tuple[float, float, float]:
        """Ordered strain-derived potential pressures across the three boundaries."""
        return (
            self.before_events.potential_pressure,
            self.after_events.potential_pressure,
            self.after_mechanics.potential_pressure,
        )

    @property
    def event_pressure_change(self) -> float:
        """Potential-pressure change due to phase and ternary events at fixed cell."""
        return self.after_events.potential_pressure - self.before_events.potential_pressure

    @property
    def mechanical_pressure_change(self) -> float:
        """Potential-pressure change across the coordinate integration interval."""
        return self.after_mechanics.potential_pressure - self.after_events.potential_pressure


def _validate_model_and_evaluator(
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
) -> None:
    if not isinstance(model, FLiBeRankTwoTREIPModel):
        raise TypeError("model must be FLiBeRankTwoTREIPModel.")
    if not isinstance(stress_evaluator, RankTwoConservativeStressEvaluator):
        raise TypeError("stress_evaluator must be RankTwoConservativeStressEvaluator.")


def _stress_for_evaluation(
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    evaluation: FLiBeRankTwoTREIPResult,
) -> FLiBeRankTwoTREIPStressResult:
    if not isinstance(evaluation, FLiBeRankTwoTREIPResult):
        raise TypeError("evaluation must be FLiBeRankTwoTREIPResult.")
    configuration = evaluation.configuration
    if configuration.configuration.cell is None:
        raise ValueError("FLiBe rank-two stress requires a simulation cell.")
    if configuration.configuration.periodic != (True, True, True):
        raise ValueError("FLiBe periodic stress requires three periodic cell axes.")

    # Re-evaluation binds the recorded domain result to this exact model.
    checked = model.evaluate(
        configuration,
        evaluation.graph,
        evaluation.input_features,
        evaluation.resonance,
        evaluation.execution,
    )
    if checked != evaluation:
        raise ValueError("recorded FLiBe TR-EIP evaluation differs from the supplied model.")

    stress = stress_evaluator.evaluate(
        model.rank_two_model,
        configuration.configuration,
        evaluation.graph,
        evaluation.resonance_features,
        evaluation.execution,
    )
    return FLiBeRankTwoTREIPStressResult(evaluation=evaluation, stress=stress)


def evaluate_flibe_rank_two_tr_eip_stress(
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    configuration: FLiBeConfiguration,
    graph: InteractionGraph,
    features: ScalarVectorTensorFeatures,
    resonance: FLiBeResonanceDescriptor,
    execution: TernaryExecutionVector,
) -> FLiBeRankTwoTREIPStressResult:
    """Evaluate the typed FLiBe TR-EIP energy and its full periodic stress."""
    _validate_model_and_evaluator(model, stress_evaluator)
    if not isinstance(configuration, FLiBeConfiguration):
        raise TypeError("configuration must be FLiBeConfiguration.")
    if not isinstance(graph, InteractionGraph):
        raise TypeError("graph must be InteractionGraph.")
    if not isinstance(features, ScalarVectorTensorFeatures):
        raise TypeError("features must be ScalarVectorTensorFeatures.")
    if not isinstance(resonance, FLiBeResonanceDescriptor):
        raise TypeError("resonance must be FLiBeResonanceDescriptor.")
    if not isinstance(execution, TernaryExecutionVector):
        raise TypeError("execution must be TernaryExecutionVector.")

    evaluation = model.evaluate(configuration, graph, features, resonance, execution)
    return _stress_for_evaluation(model, stress_evaluator, evaluation)


def evaluate_flibe_rank_two_tr_eip_md_stresses(
    coupled: FLiBeRankTwoTREIPMDCoupledStep,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
) -> FLiBeRankTwoTREIPMDStressTrace:
    """Evaluate three domain-aligned rank-two stresses from a completed MD step."""
    if not isinstance(coupled, FLiBeRankTwoTREIPMDCoupledStep):
        raise TypeError("coupled must be FLiBeRankTwoTREIPMDCoupledStep.")
    _validate_model_and_evaluator(model, stress_evaluator)

    before = _stress_for_evaluation(model, stress_evaluator, coupled.before_events)
    after_event = (
        before if coupled.coupled_step.event_update is None else
        _stress_for_evaluation(model, stress_evaluator, coupled.after_events)
    )
    after_mechanics = (
        after_event if coupled.coupled_step.mechanical_update is None else
        _stress_for_evaluation(model, stress_evaluator, coupled.after_mechanics)
    )

    return FLiBeRankTwoTREIPMDStressTrace(
        coupled=coupled,
        before_events=before,
        after_events=after_event,
        after_mechanics=after_mechanics,
    )
