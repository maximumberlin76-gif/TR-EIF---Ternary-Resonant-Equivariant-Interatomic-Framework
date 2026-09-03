"""Vector retained balanced ternary execution for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .execution import (
    TernaryExecutionState,
    TernaryExecutionStep,
    execute_ternary_step,
)
from .guard import TernaryExecutionGuard
from .state import TernaryVector, validate_ternary_vector


@dataclass(frozen=True, slots=True)
class TernaryExecutionVector:
    """Immutable retained ternary execution state for multiple nodes."""

    states: tuple[TernaryExecutionState, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.states, tuple):
            raise TypeError("states must be a tuple.")

        if len(self.states) == 0:
            raise ValueError("states must not be empty.")

        for index, state in enumerate(self.states):
            if not isinstance(state, TernaryExecutionState):
                raise TypeError(
                    f"states[{index}] must be a TernaryExecutionState instance."
                )

    @classmethod
    def from_retained_states(
        cls,
        retained_states: tuple[object, ...],
    ) -> TernaryExecutionVector:
        """Construct an execution vector without pending targets."""

        validated = validate_ternary_vector(retained_states)

        return cls(
            states=tuple(
                TernaryExecutionState(retained_state=state)
                for state in validated
            )
        )

    @property
    def node_count(self) -> int:
        """Return the number of ternary execution nodes."""

        return len(self.states)

    @property
    def retained_states(self) -> TernaryVector:
        """Return the retained balanced ternary state vector."""

        return tuple(state.retained_state for state in self.states)

    @property
    def has_pending_targets(self) -> bool:
        """Return whether at least one node has a pending target."""

        return any(state.has_pending_target for state in self.states)


@dataclass(frozen=True, slots=True)
class TernaryVectorExecutionStep:
    """Result of one execution attempt across multiple nodes."""

    previous: TernaryExecutionVector
    node_steps: tuple[TernaryExecutionStep, ...]
    current: TernaryExecutionVector

    def __post_init__(self) -> None:
        if len(self.node_steps) != self.previous.node_count:
            raise ValueError(
                "node_steps must match the execution-vector node count."
            )

        if self.current.node_count != self.previous.node_count:
            raise ValueError(
                "current and previous execution vectors must have "
                "the same node count."
            )

    @property
    def committed_count(self) -> int:
        """Return the number of nodes that committed a transition leg."""

        return sum(step.committed for step in self.node_steps)

    @property
    def held_count(self) -> int:
        """Return the number of nodes held by execution eligibility."""

        return self.previous.node_count - self.committed_count


def execute_ternary_vector_step(
    state: TernaryExecutionVector,
    requested_targets: TernaryVector | None = None,
    guards: tuple[TernaryExecutionGuard, ...] | None = None,
) -> TernaryVectorExecutionStep:
    """Attempt one guarded ternary execution step for every node."""

    if not isinstance(state, TernaryExecutionVector):
        raise TypeError(
            "state must be a TernaryExecutionVector instance."
        )

    if requested_targets is None:
        if not state.has_pending_targets:
            raise ValueError(
                "requested_targets are required when no targets are pending."
            )

        targets: TernaryVector | None = None
    else:
        targets = validate_ternary_vector(requested_targets)

        if len(targets) != state.node_count:
            raise ValueError(
                "requested_targets must match the execution-vector node count."
            )

    if guards is None:
        execution_guards = tuple(
            TernaryExecutionGuard.unrestricted()
            for _ in range(state.node_count)
        )
    else:
        if not isinstance(guards, tuple):
            raise TypeError("guards must be a tuple or None.")

        if len(guards) != state.node_count:
            raise ValueError(
                "guards must match the execution-vector node count."
            )

        for index, guard in enumerate(guards):
            if not isinstance(guard, TernaryExecutionGuard):
                raise TypeError(
                    f"guards[{index}] must be a "
                    "TernaryExecutionGuard instance."
                )

        execution_guards = guards

    node_steps: list[TernaryExecutionStep] = []

    for index, node_state in enumerate(state.states):
        if node_state.has_pending_target:
            requested = None if targets is None else targets[index]
        else:
            if targets is None:
                raise ValueError(
                    "Every node without a pending target requires "
                    "a requested target."
                )

            requested = targets[index]

        node_step = execute_ternary_step(
            node_state,
            requested,
            execution_guards[index],
        )
        node_steps.append(node_step)

    current = TernaryExecutionVector(
        states=tuple(step.current for step in node_steps)
    )

    return TernaryVectorExecutionStep(
        previous=state,
        node_steps=tuple(node_steps),
        current=current,
    )
