"""Active-neutral routing for balanced ternary transitions in TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .state import TernaryState, validate_ternary_state
from .transition import TernaryTransition, is_direct_opposite_transition


@dataclass(frozen=True, slots=True)
class TernaryRoute:
    """One executable ternary leg with an optional pending final target."""

    transition: TernaryTransition
    pending_target: TernaryState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.transition, TernaryTransition):
            raise TypeError(
                "transition must be a TernaryTransition instance."
            )

        if self.pending_target is not None:
            pending_state = validate_ternary_state(self.pending_target)

            if self.transition.target is not TernaryState.NEUTRAL:
                raise ValueError(
                    "A pending target requires the current transition "
                    "to terminate in active neutral."
                )

            if pending_state is TernaryState.NEUTRAL:
                raise ValueError(
                    "pending_target must not encode active neutral."
                )

            if self.transition.source is TernaryState.NEUTRAL:
                raise ValueError(
                    "A pending target cannot be introduced by a transition "
                    "that already starts in active neutral."
                )

            if pending_state is self.transition.source:
                raise ValueError(
                    "pending_target must be opposite to the pre-neutral state."
                )

            object.__setattr__(
                self,
                "pending_target",
                pending_state,
            )

    @property
    def executed_state(self) -> TernaryState:
        """Return the state produced by the current committed leg."""

        return self.transition.target

    @property
    def has_pending_target(self) -> bool:
        """Return whether a later transition target remains pending."""

        return self.pending_target is not None


def route_ternary_target(
    retained_state: TernaryState,
    requested_target: TernaryState,
) -> TernaryRoute:
    """Route a requested target into one admissible committed transition leg."""

    retained = validate_ternary_state(retained_state)
    requested = validate_ternary_state(requested_target)

    if is_direct_opposite_transition(retained, requested):
        return TernaryRoute(
            transition=TernaryTransition(
                source=retained,
                target=TernaryState.NEUTRAL,
            ),
            pending_target=requested,
        )

    return TernaryRoute(
        transition=TernaryTransition(
            source=retained,
            target=requested,
        )
    )


def route_pending_target(
    retained_state: TernaryState,
    pending_target: TernaryState,
) -> TernaryRoute:
    """Route an existing pending target from active neutral."""

    retained = validate_ternary_state(retained_state)
    pending = validate_ternary_state(pending_target)

    if retained is not TernaryState.NEUTRAL:
        raise ValueError(
            "A pending target can execute only from active neutral."
        )

    if pending is TernaryState.NEUTRAL:
        raise ValueError(
            "pending_target must not encode active neutral."
        )

    return TernaryRoute(
        transition=TernaryTransition(
            source=retained,
            target=pending,
        )
    )
