"""Balanced ternary transition semantics for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass

from .state import TernaryState, validate_ternary_state


def is_direct_opposite_transition(
    source: TernaryState,
    target: TernaryState,
) -> bool:
    """Return whether a transition directly crosses between opposite states."""

    source_state = validate_ternary_state(source)
    target_state = validate_ternary_state(target)

    return (
        source_state is TernaryState.NEGATIVE
        and target_state is TernaryState.POSITIVE
    ) or (
        source_state is TernaryState.POSITIVE
        and target_state is TernaryState.NEGATIVE
    )


def is_committed_transition_allowed(
    source: TernaryState,
    target: TernaryState,
) -> bool:
    """Return whether one committed ternary transition leg is allowed."""

    source_state = validate_ternary_state(source)
    target_state = validate_ternary_state(target)

    return not is_direct_opposite_transition(
        source_state,
        target_state,
    )


@dataclass(frozen=True, slots=True)
class TernaryTransition:
    """One validated committed balanced ternary transition leg."""

    source: TernaryState
    target: TernaryState

    def __post_init__(self) -> None:
        source_state = validate_ternary_state(self.source)
        target_state = validate_ternary_state(self.target)

        if not is_committed_transition_allowed(
            source_state,
            target_state,
        ):
            raise ValueError(
                "Direct committed transitions between opposite ternary "
                "states are forbidden."
            )

        object.__setattr__(self, "source", source_state)
        object.__setattr__(self, "target", target_state)

    @property
    def changes_state(self) -> bool:
        """Return whether the committed leg changes the retained state."""

        return self.source is not self.target

    @property
    def enters_neutral(self) -> bool:
        """Return whether the committed leg enters active neutral."""

        return (
            self.source is not TernaryState.NEUTRAL
            and self.target is TernaryState.NEUTRAL
        )

    @property
    def leaves_neutral(self) -> bool:
        """Return whether the committed leg leaves active neutral."""

        return (
            self.source is TernaryState.NEUTRAL
            and self.target is not TernaryState.NEUTRAL
        )
