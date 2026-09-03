"""Balanced ternary state and transition semantics for TR-EIF."""

from .state import (
    TernaryState,
    TernaryVector,
    validate_ternary_state,
    validate_ternary_vector,
)
from .transition import (
    TernaryTransition,
    is_committed_transition_allowed,
    is_direct_opposite_transition,
)

__all__ = [
    "TernaryState",
    "TernaryTransition",
    "TernaryVector",
    "is_committed_transition_allowed",
    "is_direct_opposite_transition",
    "validate_ternary_state",
    "validate_ternary_vector",
]
