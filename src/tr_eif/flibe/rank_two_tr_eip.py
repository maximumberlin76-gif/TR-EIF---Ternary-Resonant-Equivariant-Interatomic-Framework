"""Typed rank-two TR-EIP specialization of the TR-EIF interatomic energy layer.

The FLiBe domain record retains the atomic configuration, graph-relative
coordination, thermodynamic context, and continuous resonance descriptor.
The established FLiBe TR-EIP model supplies resonance-augmented scalar/vector
features and their retained-ternary-conditioned energy. A rank-two E(3)
energy model extends the same reference model with Cartesian tensor channels.

Both energy paths use the identical reference-model instance. Their scalar/
vector layer outputs and energy contributions are required to match exactly.
Forces are coordinate derivatives of the resulting complete energy, with the
input resonance, tensor features, interaction graph, and retained ternary
execution held fixed over each differentiation stencil.
"""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy.differentiation import CoordinateDifferentiation
from tr_eif.energy.force import ForceState
from tr_eif.energy.rank_two_model import (
    RankTwoConservativeEnergyModel,
    RankTwoConservativeEnergyResult,
    RankTwoConservativeForceEvaluator,
)
from tr_eif.energy.state import EnergyState
from tr_eif.equivariant.rank_two import ScalarVectorTensorFeatures
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .configuration import FLiBeConfiguration
from .resonance_descriptor import FLiBeResonanceDescriptor
from .tr_eip import FLiBeTREIPModel, FLiBeTREIPResult


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPResult:
    """Domain-specific reference energy and tensor-extended energy evidence."""

    reference_result: FLiBeTREIPResult
    augmented_result: RankTwoConservativeEnergyResult
    input_features: ScalarVectorTensorFeatures
    resonance_features: ScalarVectorTensorFeatures

    def __post_init__(self) -> None:
        if not isinstance(self.reference_result, FLiBeTREIPResult):
            raise TypeError("reference_result must be FLiBeTREIPResult.")
        if not isinstance(self.augmented_result, RankTwoConservativeEnergyResult):
            raise TypeError("augmented_result must be RankTwoConservativeEnergyResult.")
        if not isinstance(self.input_features, ScalarVectorTensorFeatures):
            raise TypeError("input_features must be ScalarVectorTensorFeatures.")
        if not isinstance(self.resonance_features, ScalarVectorTensorFeatures):
            raise TypeError("resonance_features must be ScalarVectorTensorFeatures.")

        reference = self.reference_result
        combined = self.augmented_result

        if reference.input_features != self.input_features.base:
            raise ValueError(
                "TR-EIP input features differ from the registered base channels."
            )
        if reference.resonance_conditioned_features != self.resonance_features.base:
            raise ValueError("resonance-augmented scalar/vector channels differ.")
        if self.resonance_features.rank_two != self.input_features.rank_two:
            raise ValueError(
                "rank-two channels must retain their input values across resonance augmentation."
            )
        if combined.layer.previous != self.resonance_features:
            raise ValueError(
                "rank-two energy input differs from resonance-augmented features."
            )
        if combined.layer.base_layer != reference.energy_result.layer_result:
            raise ValueError(
                "scalar/vector equivariant layer outputs differ between the two models."
            )
        if combined.reference_energy != reference.energy_result.energy:
            raise ValueError(
                "TR-EIP reference energy differs from the tensor-extended reference contribution."
            )
        if combined.energy.atom_count != reference.configuration.atom_count:
            raise ValueError("energy and FLiBe configuration atom counts differ.")

    @property
    def configuration(self) -> FLiBeConfiguration:
        return self.reference_result.configuration

    @property
    def graph(self) -> InteractionGraph:
        return self.reference_result.graph

    @property
    def resonance(self) -> FLiBeResonanceDescriptor:
        return self.reference_result.resonance

    @property
    def execution(self) -> TernaryExecutionVector:
        return self.reference_result.execution

    @property
    def energy(self) -> EnergyState:
        """Return scalar/vector and rank-two atomic energies summed together."""
        return self.augmented_result.energy

    @property
    def tensor_energy(self) -> EnergyState:
        """Return the separately registered rank-two invariant contribution."""
        return self.augmented_result.tensor_energy

    @property
    def reference_energy(self) -> EnergyState:
        """Return the legacy scalar/vector TR-EIP energy contribution."""
        return self.reference_result.energy_result.energy


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPForceResult:
    """Full-energy force evidence with its registered differentiation policy."""

    evaluation: FLiBeRankTwoTREIPResult
    forces: ForceState
    differentiation: CoordinateDifferentiation

    def __post_init__(self) -> None:
        if not isinstance(self.evaluation, FLiBeRankTwoTREIPResult):
            raise TypeError("evaluation must be FLiBeRankTwoTREIPResult.")
        if not isinstance(self.forces, ForceState):
            raise TypeError("forces must be ForceState.")
        if not isinstance(self.differentiation, CoordinateDifferentiation):
            raise TypeError("differentiation must be CoordinateDifferentiation.")
        if self.forces.atom_count != self.evaluation.configuration.atom_count:
            raise ValueError("force and FLiBe configuration atom counts differ.")


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPModel:
    """Bind one FLiBe TR-EIP reference to a rank-two conservative extension."""

    tr_eip_model: FLiBeTREIPModel
    rank_two_model: RankTwoConservativeEnergyModel

    def __post_init__(self) -> None:
        if not isinstance(self.tr_eip_model, FLiBeTREIPModel):
            raise TypeError("tr_eip_model must be FLiBeTREIPModel.")
        if not isinstance(self.rank_two_model, RankTwoConservativeEnergyModel):
            raise TypeError("rank_two_model must be RankTwoConservativeEnergyModel.")
        if self.rank_two_model.reference_model is not self.tr_eip_model.energy_model:
            raise ValueError(
                "TR-EIP and rank-two extension must share one ReferenceEnergyModel instance."
            )

    def evaluate(
        self,
        configuration: FLiBeConfiguration,
        graph: InteractionGraph,
        features: ScalarVectorTensorFeatures,
        resonance: FLiBeResonanceDescriptor,
        execution: TernaryExecutionVector,
    ) -> FLiBeRankTwoTREIPResult:
        """Evaluate reference and rank-two contributions at one retained state."""
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

        configuration.composition()

        if (
            graph.node_count != configuration.atom_count
            or features.node_count != configuration.atom_count
            or execution.node_count != configuration.atom_count
        ):
            raise ValueError(
                "graph, feature, execution and FLiBe atom counts differ."
            )
        if resonance.configuration != configuration:
            raise ValueError(
                "resonance and energy evaluation configurations differ."
            )

        reference = self.tr_eip_model.evaluate(
            configuration, graph, features.base, resonance, execution,
        )

        augmented = ScalarVectorTensorFeatures(
            base=reference.resonance_conditioned_features,
            rank_two=features.rank_two,
        )

        combined = self.rank_two_model.evaluate(
            configuration.configuration,
            graph,
            augmented,
            execution,
        )

        return FLiBeRankTwoTREIPResult(
            reference_result=reference,
            augmented_result=combined,
            input_features=features,
            resonance_features=augmented,
        )

    def evaluate_forces(
        self,
        configuration: FLiBeConfiguration,
        graph: InteractionGraph,
        features: ScalarVectorTensorFeatures,
        resonance: FLiBeResonanceDescriptor,
        execution: TernaryExecutionVector,
        force_evaluator: RankTwoConservativeForceEvaluator,
    ) -> FLiBeRankTwoTREIPForceResult:
        """Differentiate the complete E(3)-invariant energy at a frozen state."""
        if not isinstance(force_evaluator, RankTwoConservativeForceEvaluator):
            raise TypeError(
                "force_evaluator must be RankTwoConservativeForceEvaluator."
            )

        evaluation = self.evaluate(
            configuration, graph, features, resonance, execution,
        )

        forces = force_evaluator.evaluate(
            self.rank_two_model,
            configuration.configuration,
            graph,
            evaluation.resonance_features,
            execution,
        )

        return FLiBeRankTwoTREIPForceResult(
            evaluation=evaluation,
            forces=forces,
            differentiation=force_evaluator.differentiation,
        )
