"""Retained balanced ternary execution state for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

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
    """Result of one committed ternary execution step."""

    previous: TernaryExecutionState
    route: TernaryRoute
    current: TernaryExecutionState


def execute_ternary_step(
    state: TernaryExecutionState,
    requested_target: TernaryState | None = None,
) -> TernaryExecutionStep:
    """Execute exactly one committed balanced ternary transition leg."""

    if not isinstance(state, TernaryExecutionState):
        raise TypeError(
            "state must be a TernaryExecutionState instance."
        )

    if state.pending_target is not None:
        if requested_target is not None:
            requested = validate_ternary_state(requested_target)

            if requested is not state.pending_target:
                raise ValueError(
                    "A new requested target cannot replace an existing "
                    "pending target."
                )

        route = route_pending_target(
            state.retained_state,
            state.pending_target,
        )
    else:
        if requested_target is None:
            raise ValueError(
                "requested_target is required when no target is pending."
            )

        requested = validate_ternary_state(requested_target)

        route = route_ternary_target(
            state.retained_state,
            requested,
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
