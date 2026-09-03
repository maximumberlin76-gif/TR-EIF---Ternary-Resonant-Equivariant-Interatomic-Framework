"""Multi-step molecular-dynamics trajectory execution for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from tr_eif.energy import (
    ConservativeForceEvaluator,
    ReferenceEnergyModel,
)
from tr_eif.equivariant import NodeFeatureVector
from tr_eif.ternary import TernaryExecutionVector

from .execution import (
    MolecularDynamicsStepResult,
    velocity_verlet_step,
)
from .state import MolecularDynamicsState


@dataclass(frozen=True, slots=True)
class MolecularDynamicsTrajectory:
    """Immutable ordered sequence of molecular-dynamics step results."""

    steps: tuple[MolecularDynamicsStepResult, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple):
            raise TypeError(
                "steps must be a tuple."
            )

        if len(self.steps) == 0:
            raise ValueError(
                "steps must not be empty."
            )

        for index, step in enumerate(self.steps):
            if not isinstance(
                step,
                MolecularDynamicsStepResult,
            ):
                raise TypeError(
                    f"steps[{index}] must be a "
                    "MolecularDynamicsStepResult instance."
                )

        atom_count = self.steps[0].previous.atom_count

        for index, step in enumerate(self.steps):
            if step.previous.atom_count != atom_count:
                raise ValueError(
                    "all trajectory steps must have "
                    "the same atom count."
                )

            if step.current.atom_count != atom_count:
                raise ValueError(
                    "all trajectory steps must have "
                    "the same atom count."
                )

            if index == 0:
                continue

            previous_step = self.steps[index - 1]

            if step.previous != previous_step.current:
                raise ValueError(
                    "each trajectory step must begin from "
                    "the preceding current state."
                )

    @property
    def step_count(self) -> int:
        """Return the number of executed molecular-dynamics steps."""

        return len(self.steps)

    @property
    def atom_count(self) -> int:
        """Return the common trajectory atom count."""

        return self.steps[0].previous.atom_count

    @property
    def initial(self) -> MolecularDynamicsState:
        """Return the initial molecular-dynamics state."""

        return self.steps[0].previous

    @property
    def final(self) -> MolecularDynamicsState:
        """Return the final molecular-dynamics state."""

        return self.steps[-1].current

    @property
    def states(self) -> tuple[MolecularDynamicsState, ...]:
        """Return the complete ordered state sequence."""

        return (
            self.initial,
            *(
                step.current
                for step in self.steps
            ),
        )


def run_velocity_verlet_trajectory(
    initial_state: MolecularDynamicsState,
    model: ReferenceEnergyModel,
    force_evaluator: ConservativeForceEvaluator,
    features: NodeFeatureVector,
    execution: TernaryExecutionVector,
    cutoff: float,
    time_step: float,
    step_count: int,
) -> MolecularDynamicsTrajectory:
    """Execute a deterministic multi-step velocity-Verlet trajectory."""

    if not isinstance(
        initial_state,
        MolecularDynamicsState,
    ):
        raise TypeError(
            "initial_state must be a MolecularDynamicsState instance."
        )

    if not isinstance(step_count, int) or isinstance(
        step_count,
        bool,
    ):
        raise TypeError(
            "step_count must be an integer."
        )

    if step_count <= 0:
        raise ValueError(
            "step_count must be greater than zero."
        )

    current_state = initial_state
    completed_steps: list[MolecularDynamicsStepResult] = []

    for _ in range(step_count):
        result = velocity_verlet_step(
            state=current_state,
            model=model,
            force_evaluator=force_evaluator,
            features=features,
            execution=execution,
            cutoff=cutoff,
            time_step=time_step,
        )

        completed_steps.append(result)
        current_state = result.current

    return MolecularDynamicsTrajectory(
        steps=tuple(completed_steps),
    )
