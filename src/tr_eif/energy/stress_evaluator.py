"""Energy-derived stress evaluation for TR-EIF reference energy models."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.configuration import AtomicConfiguration
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.graph import InteractionGraph
from tr_eif.ternary import TernaryExecutionVector

from .model import ReferenceEnergyModel
from .strain import CellStrainDifferentiation
from .stress import StressState


def _determinant_3x3(
    matrix: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ],
) -> float:
    """Return the determinant of a 3x3 matrix."""

    return (
        matrix[0][0]
        * (
            matrix[1][1] * matrix[2][2]
            - matrix[1][2] * matrix[2][1]
        )
        - matrix[0][1]
        * (
            matrix[1][0] * matrix[2][2]
            - matrix[1][2] * matrix[2][0]
        )
        + matrix[0][2]
        * (
            matrix[1][0] * matrix[2][1]
            - matrix[1][1] * matrix[2][0]
        )
    )


def _left_transform_vector(
    matrix: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ],
    vector: tuple[float, float, float],
) -> tuple[float, float, float]:
    """Apply a Cartesian linear transformation to one vector."""

    return (
        matrix[0][0] * vector[0]
        + matrix[0][1] * vector[1]
        + matrix[0][2] * vector[2],
        matrix[1][0] * vector[0]
        + matrix[1][1] * vector[1]
        + matrix[1][2] * vector[2],
        matrix[2][0] * vector[0]
        + matrix[2][1] * vector[1]
        + matrix[2][2] * vector[2],
    )


def _strain_matrix(
    component_a: int,
    component_b: int,
    strain: float,
) -> tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]:
    """Return I plus one symmetric infinitesimal strain component."""

    matrix = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]

    if component_a == component_b:
        matrix[component_a][component_b] += strain
    else:
        half_strain = 0.5 * strain
        matrix[component_a][component_b] += half_strain
        matrix[component_b][component_a] += half_strain

    return (
        (matrix[0][0], matrix[0][1], matrix[0][2]),
        (matrix[1][0], matrix[1][1], matrix[1][2]),
        (matrix[2][0], matrix[2][1], matrix[2][2]),
    )


def _strain_configuration(
    configuration: AtomicConfiguration,
    component_a: int,
    component_b: int,
    strain: float,
) -> AtomicConfiguration:
    """Apply one homogeneous Cartesian strain to cell and positions."""

    if configuration.cell is None:
        raise ValueError(
            "stress evaluation requires a configuration with a cell."
        )

    if component_a not in (0, 1, 2) or component_b not in (0, 1, 2):
        raise IndexError(
            "strain component indices must be 0, 1, or 2."
        )

    transformation = _strain_matrix(
        component_a,
        component_b,
        strain,
    )

    positions = tuple(
        _left_transform_vector(
            transformation,
            position,
        )
        for position in configuration.positions
    )

    cell = tuple(
        _left_transform_vector(
            transformation,
            cell_vector,
        )
        for cell_vector in configuration.cell
    )

    return AtomicConfiguration(
        species=configuration.species,
        positions=positions,
        cell=cell,
        periodic=configuration.periodic,
    )


@dataclass(frozen=True, slots=True)
class ConservativeStressEvaluator:
    """Central-difference stress evaluator with fixed graph topology."""

    differentiation: CellStrainDifferentiation

    def __post_init__(self) -> None:
        if not isinstance(
            self.differentiation,
            CellStrainDifferentiation,
        ):
            raise TypeError(
                "differentiation must be a "
                "CellStrainDifferentiation instance."
            )

    def evaluate(
        self,
        model: ReferenceEnergyModel,
        configuration: AtomicConfiguration,
        graph: InteractionGraph,
        features: NodeFeatureVector,
        execution: TernaryExecutionVector,
    ) -> StressState:
        """Evaluate symmetric stress from homogeneous energy derivatives."""

        if not isinstance(model, ReferenceEnergyModel):
            raise TypeError(
                "model must be a ReferenceEnergyModel instance."
            )

        if not isinstance(configuration, AtomicConfiguration):
            raise TypeError(
                "configuration must be an AtomicConfiguration instance."
            )

        if configuration.cell is None:
            raise ValueError(
                "stress evaluation requires a configuration with a cell."
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

        reference_volume = abs(
            _determinant_3x3(configuration.cell)
        )

        if reference_volume == 0.0:
            raise ValueError(
                "stress evaluation requires nonzero cell volume."
            )

        step = self.differentiation.step
        inverse_span = self.differentiation.inverse_central_span

        tensor = [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
        ]

        for component_a in range(3):
            for component_b in range(component_a, 3):
                plus_configuration = _strain_configuration(
                    configuration=configuration,
                    component_a=component_a,
                    component_b=component_b,
                    strain=step,
                )

                minus_configuration = _strain_configuration(
                    configuration=configuration,
                    component_a=component_a,
                    component_b=component_b,
                    strain=-step,
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

                energy_derivative = (
                    plus_energy - minus_energy
                ) * inverse_span

                stress_component = (
                    energy_derivative / reference_volume
                )

                tensor[component_a][component_b] = stress_component
                tensor[component_b][component_a] = stress_component

        return StressState(
            tensor=(
                (
                    tensor[0][0],
                    tensor[0][1],
                    tensor[0][2],
                ),
                (
                    tensor[1][0],
                    tensor[1][1],
                    tensor[1][2],
                ),
                (
                    tensor[2][0],
                    tensor[2][1],
                    tensor[2][2],
                ),
            )
        )
