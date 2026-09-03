"""Coordinate-dependent reference energy model for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant import (
    ConditionedEquivariantLayerResult,
    NodeFeatureVector,
    RadialMessageOperator,
    TernaryConditioning,
    conditioned_equivariant_layer_step,
)
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .functional import LinearInvariantEnergyFunctional
from .state import EnergyState


@dataclass(frozen=True, slots=True)
class EnergyModelResult:
    """Result of one reference coordinate-dependent energy evaluation."""

    layer_result: ConditionedEquivariantLayerResult
    energy: EnergyState

    def __post_init__(self) -> None:
        if not isinstance(
            self.layer_result,
            ConditionedEquivariantLayerResult,
        ):
            raise TypeError(
                "layer_result must be a "
                "ConditionedEquivariantLayerResult instance."
            )

        if not isinstance(self.energy, EnergyState):
            raise TypeError(
                "energy must be an EnergyState instance."
            )

        if self.energy.atom_count != self.layer_result.current.node_count:
            raise ValueError(
                "energy atom count must match layer-result node count."
            )


@dataclass(frozen=True, slots=True)
class ReferenceEnergyModel:
    """Reference conditioned equivariant scalar-energy model."""

    message_operator: RadialMessageOperator
    conditioning: TernaryConditioning
    energy_functional: LinearInvariantEnergyFunctional

    def __post_init__(self) -> None:
        if not isinstance(
            self.message_operator,
            RadialMessageOperator,
        ):
            raise TypeError(
                "message_operator must be a "
                "RadialMessageOperator instance."
            )

        if not isinstance(
            self.conditioning,
            TernaryConditioning,
        ):
            raise TypeError(
                "conditioning must be a TernaryConditioning instance."
            )

        if not isinstance(
            self.energy_functional,
            LinearInvariantEnergyFunctional,
        ):
            raise TypeError(
                "energy_functional must be a "
                "LinearInvariantEnergyFunctional instance."
            )

    def evaluate(
        self,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: NodeFeatureVector,
        execution: TernaryExecutionVector,
    ) -> EnergyModelResult:
        """Evaluate the reference scalar energy for one configuration."""

        if not isinstance(configuration, AtomicConfiguration):
            raise TypeError(
                "configuration must be an AtomicConfiguration instance."
            )

        if not isinstance(graph, InteractionGraph):
            raise TypeError(
                "graph must be an InteractionGraph instance."
            )

        if not isinstance(features, NodeFeatureVector):
            raise TypeError(
                "features must be a NodeFeatureVector instance."
            )

        if not isinstance(execution, TernaryExecutionVector):
            raise TypeError(
                "execution must be a TernaryExecutionVector instance."
            )

        if graph.node_count != configuration.atom_count:
            raise ValueError(
                "graph node count must match configuration atom count."
            )

        if features.node_count != configuration.atom_count:
            raise ValueError(
                "feature node count must match configuration atom count."
            )

        if execution.node_count != configuration.atom_count:
            raise ValueError(
                "ternary execution node count must match "
                "configuration atom count."
            )

        layer_result = conditioned_equivariant_layer_step(
            configuration=configuration,
            graph=graph,
            features=features,
            execution=execution,
            conditioning=self.conditioning,
            operator=self.message_operator,
        )

        energy = self.energy_functional.evaluate(
            layer_result.current
        )

        return EnergyModelResult(
            layer_result=layer_result,
            energy=energy,
        )
