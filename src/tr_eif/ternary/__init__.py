"""Balanced ternary state and transition semantics for TR-EIF."""

from .routing import (
    TernaryRoute,
    route_pending_target,
    route_ternary_target,
)
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
    "TernaryRoute",
    "TernaryState",
    "TernaryTransition",
    "TernaryVector",
    "is_committed_transition_allowed",
    "is_direct_opposite_transition",
    "route_pending_target",
    "route_ternary_target",
    "validate_ternary_state",
    "validate_ternary_vector",
]
