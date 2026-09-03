"""Force-driven velocity-Verlet execution for TR-EIF molecular dynamics."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import (
    ConservativeForceEvaluator,
    ForceState,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.graph import (
    InteractionGraph,
    build_cutoff_graph,
)
from tr_eif.ternary import TernaryExecutionVector

from .dynamics import accelerations_from_forces
from .integrator import (
    velocity_verlet_positions,
    velocity_verlet_velocities,
)
from .state import MolecularDynamicsState


def _validate_positive_finite(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one positive finite scalar."""

    if not isinstance(value, (int, float)) or isinstance(
        value,
        bool,
    ):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    normalized = float(value)

    if normalized <= 0.0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return normalized


@dataclass(frozen=True, slots=True)
class MolecularDynamicsStepResult:
    """Result of one force-driven velocity-Verlet MD step."""

    previous: MolecularDynamicsState
    current: MolecularDynamicsState
    graph_before: InteractionGraph
    graph_after: InteractionGraph
    forces_before: ForceState
    forces_after: ForceState

    def __post_init__(self) -> None:
        if not isinstance(
            self.previous,
            MolecularDynamicsState,
        ):
            raise TypeError(
                "previous must be a MolecularDynamicsState instance."
            )

        if not isinstance(
            self.current,
            MolecularDynamicsState,
        ):
            raise TypeError(
                "current must be a MolecularDynamicsState instance."
            )

        if not isinstance(
            self.graph_before,
            InteractionGraph,
        ):
            raise TypeError(
                "graph_before must be an InteractionGraph instance."
            )

        if not isinstance(
            self.graph_after,
            InteractionGraph,
        ):
            raise TypeError(
                "graph_after must be an InteractionGraph instance."
            )

        if not isinstance(self.forces_before, ForceState):
            raise TypeError(
                "forces_before must be a ForceState instance."
            )

        if not isinstance(self.forces_after, ForceState):
            raise TypeError(
                "forces_after must be a ForceState instance."
            )

        atom_count = self.previous.atom_count

        if self.current.atom_count != atom_count:
            raise ValueError(
                "current atom count must match previous atom count."
            )

        if self.graph_before.node_count != atom_count:
            raise ValueError(
                "graph_before node count must match MD atom count."
            )

        if self.graph_after.node_count != atom_count:
            raise ValueError(
                "graph_after node count must match MD atom count."
            )

        if self.forces_before.atom_count != atom_count:
            raise ValueError(
                "forces_before atom count must match MD atom count."
            )

        if self.forces_after.atom_count != atom_count:
            raise ValueError(
                "forces_after atom count must match MD atom count."
            )

        if self.current.step != self.previous.step + 1:
            raise ValueError(
                "current step must equal previous step plus one."
            )

        if self.current.time <= self.previous.time:
            raise ValueError(
                "current time must be greater than previous time."
            )


def velocity_verlet_step(
    state: MolecularDynamicsState,
    model: ReferenceEnergyModel,
    force_evaluator: ConservativeForceEvaluator,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
    cutoff: float,
    time_step: float,
) -> MolecularDynamicsStepResult:
    """Execute one force-driven velocity-Verlet molecular-dynamics step."""

    if not isinstance(state, MolecularDynamicsState):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    if not isinstance(model, ReferenceEnergyModel):
        raise TypeError(
            "model must be a ReferenceEnergyModel instance."
        )

    if not isinstance(
        force_evaluator,
        ConservativeForceEvaluator,
    ):
        raise TypeError(
            "force_evaluator must be a "
            "ConservativeForceEvaluator instance."
        )

    if not isinstance(features, NodeFeatureVector):
        raise TypeError(
            "features must be a NodeFeatureVector instance."
        )

    if not isinstance(execution, TernaryExecutionVector):
        raise TypeError(
            "execution must be a TernaryExecutionVector instance."
        )

    atom_count = state.atom_count

    if features.node_count != atom_count:
        raise ValueError(
            "feature node count must match MD atom count."
        )

    if execution.node_count != atom_count:
        raise ValueError(
            "ternary execution node count must match MD atom count."
        )

    validated_cutoff = _validate_positive_finite(
        cutoff,
        field_name="cutoff",
    )

    dt = _validate_positive_finite(
        time_step,
        field_name="time_step",
    )

    graph_before = build_cutoff_graph(
        configuration=state.configuration,
        cutoff=validated_cutoff,
    )

    forces_before = force_evaluator.evaluate(
        model=model,
        configuration=state.configuration,
        graph=graph_before,
        features=features,
        execution=execution,
    )

    accelerations_before = accelerations_from_forces(
        forces=forces_before,
        masses=state.masses,
    )

    positions_after = velocity_verlet_positions(
        positions=state.configuration.positions,
        velocities=state.velocities,
        accelerations=accelerations_before,
        time_step=dt,
    )

    configuration_after = AtomicConfiguration(
        species=state.configuration.species,
        positions=positions_after,
        cell=state.configuration.cell,
        periodic=state.configuration.periodic,
    )

    graph_after = build_cutoff_graph(
        configuration=configuration_after,
        cutoff=validated_cutoff,
    )

    forces_after = force_evaluator.evaluate(
        model=model,
        configuration=configuration_after,
        graph=graph_after,
        features=features,
        execution=execution,
    )

    accelerations_after = accelerations_from_forces(
        forces=forces_after,
        masses=state.masses,
    )

    velocities_after = velocity_verlet_velocities(
        velocities=state.velocities,
        accelerations_before=accelerations_before,
        accelerations_after=accelerations_after,
        time_step=dt,
    )

    current = MolecularDynamicsState(
        configuration=configuration_after,
        velocities=velocities_after,
        masses=state.masses,
        step=state.step + 1,
        time=state.time + dt,
    )

    return MolecularDynamicsStepResult(
        previous=state,
        current=current,
        graph_before=graph_before,
        graph_after=graph_after,
        forces_before=forces_before,
        forces_after=forces_after,
    )
