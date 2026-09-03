"""Conservative force evaluation for TR-EIF reference energy models."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .differentiation import CoordinateDifferentiation
from .force import ForceState
from .model import ReferenceEnergyModel


def _perturb_configuration(
    configuration: AtomicConfiguration,
    atom_index: int,
    component_index: int,
    delta: float,
) -> AtomicConfiguration:
    """Return a configuration with one Cartesian component perturbed."""

    if not 0 <= atom_index < configuration.atom_count:
        raise IndexError("atom_index is outside the configuration.")

    if component_index not in (0, 1, 2):
        raise IndexError("component_index must be 0, 1, or 2.")

    positions = list(configuration.positions)
    position = list(positions[atom_index])
    position[component_index] += delta

    positions[atom_index] = (
        position[0],
        position[1],
        position[2],
    )

    return AtomicConfiguration(
        species=configuration.species,
        positions=tuple(positions),
        cell=configuration.cell,
        periodic=configuration.periodic,
    )


@dataclass(frozen=True, slots=True)
class ConservativeForceEvaluator:
    """Central-difference force evaluator with fixed graph topology."""

    differentiation: CoordinateDifferentiation

    def __post_init__(self) -> None:
        if not isinstance(
            self.differentiation,
            CoordinateDifferentiation,
        ):
            raise TypeError(
                "differentiation must be a "
                "CoordinateDifferentiation instance."
            )

    def evaluate(
        self,
        model: ReferenceEnergyModel,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: NodeFeatureVector,
        execution: TernaryExecutionVector,
    ) -> ForceState:
        """Evaluate forces as negative fixed-graph energy derivatives."""

        if not isinstance(model, ReferenceEnergyModel):
            raise TypeError(
                "model must be a ReferenceEnergyModel instance."
            )

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

        step = self.differentiation.step
        inverse_span = self.differentiation.inverse_central_span

        forces = []

        for atom_index in range(configuration.atom_count):
            components = []

            for component_index in range(3):
                plus_configuration = _perturb_configuration(
                    configuration=configuration,
                    atom_index=atom_index,
                    component_index=component_index,
                    delta=step,
                )

                minus_configuration = _perturb_configuration(
                    configuration=configuration,
                    atom_index=atom_index,
                    component_index=component_index,
                    delta=-step,
                )

                plus_energy = model.evaluate(
                    configuration=plus_configuration,
                    graph=graph,
                    features=features,
                    execution=execution,
                ).energy.total_energy

                minus_energy = model.evaluate(
                    configuration=minus_configuration,
                    graph=graph,
                    features=features,
                    execution=execution,
                ).energy.total_energy

                derivative = (
                    plus_energy - minus_energy
                ) * inverse_span

                components.append(-derivative)

            forces.append(
                (
                    components[0],
                    components[1],
                    components[2],
                )
            )

        return ForceState(
            forces=tuple(forces)
        )
