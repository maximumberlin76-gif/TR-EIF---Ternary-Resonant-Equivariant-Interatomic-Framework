"""Retained balanced ternary execution state for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .guard import TernaryExecutionGuard
from .routing import TernaryRoute, route_pending_target, route_ternary_target
from .state import TernaryState, validate_ternary_state


@dataclass(frozen=True, slots=True)
class TernaryExecutionState:
    """Retained ternary state with an optional pending final target."""

    retained_state: TernaryState
    pending_target: TernaryState | None = None

    def __post_init__(self) -> None:
        retained = validate_ternary_state(self.retained_state)
        object.__setattr__(self, "retained_state", retained)

        if self.pending_target is None:
            return

        pending = validate_ternary_state(self.pending_target)

        if retained is not TernaryState.NEUTRAL:
            raise ValueError(
                "A pending target requires retained active neutral."
            )

        if pending is TernaryState.NEUTRAL:
            raise ValueError(
                "pending_target must not encode active neutral."
            )

        object.__setattr__(self, "pending_target", pending)

    @property
    def has_pending_target(self) -> bool:
        """Return whether a final target remains pending."""

        return self.pending_target is not None


@dataclass(frozen=True, slots=True)
class TernaryExecutionStep:
    """Result of one ternary execution attempt."""

    previous: TernaryExecutionState
    route: TernaryRoute | None
    current: TernaryExecutionState

    @property
    def committed(self) -> bool:
        """Return whether this execution attempt committed a transition leg."""

        return self.route is not None


def execute_ternary_step(
    state: TernaryExecutionState,
    requested_target: TernaryState | None = None,
    guard: TernaryExecutionGuard | None = None,
) -> TernaryExecutionStep:
    """Attempt one guarded balanced ternary execution step."""

    if not isinstance(state, TernaryExecutionState):
        raise TypeError(
            "state must be a TernaryExecutionState instance."
        )

    if guard is None:
        execution_guard = TernaryExecutionGuard.unrestricted()
    elif isinstance(guard, TernaryExecutionGuard):
        execution_guard = guard
    else:
        raise TypeError(
            "guard must be a TernaryExecutionGuard instance or None."
        )

    if state.pending_target is not None:
        if requested_target is not None:
            requested = validate_ternary_state(requested_target)

            if requested is not state.pending_target:
                raise ValueError(
                    "A new requested target cannot replace an existing "
                    "pending target."
                )

        if not execution_guard.allow_neutral_exit:
            return TernaryExecutionStep(
                previous=state,
                route=None,
                current=state,
            )

        route = route_pending_target(
            state.retained_state,
            state.pending_target,
        )

        current = TernaryExecutionState(
            retained_state=route.executed_state,
            pending_target=route.pending_target,
        )

        return TernaryExecutionStep(
            previous=state,
            route=route,
            current=current,
        )

    if requested_target is None:
        raise ValueError(
            "requested_target is required when no target is pending."
        )

    requested = validate_ternary_state(requested_target)

    route = route_ternary_target(
        state.retained_state,
        requested,
    )

    if (
        route.transition.enters_neutral
        and not execution_guard.allow_neutral_entry
    ):
        return TernaryExecutionStep(
            previous=state,
            route=None,
            current=state,
        )

    if (
        route.transition.leaves_neutral
        and not execution_guard.allow_neutral_exit
    ):
        return TernaryExecutionStep(
            previous=state,
            route=None,
            current=state,
        )

    current = TernaryExecutionState(
        retained_state=route.executed_state,
        pending_target=route.pending_target,
    )

    return TernaryExecutionStep(
        previous=state,
        route=route,
        current=current,
    )
