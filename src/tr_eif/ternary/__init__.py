"""Balanced ternary state and transition semantics for TR-EIF."""

from .execution import (
    TernaryExecutionState,
    TernaryExecutionStep,
    execute_ternary_step,
)
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
from .target import (
    TernaryTargetThresholds,
    ternary_target_from_scalar,
)
from .transition import (
    TernaryTransition,
    is_committed_transition_allowed,
    is_direct_opposite_transition,
)

__all__ = [
    "TernaryExecutionState",
    "TernaryExecutionStep",
    "TernaryRoute",
    "TernaryState",
    "TernaryTargetThresholds",
    "TernaryTransition",
    "TernaryVector",
    "execute_ternary_step",
    "is_committed_transition_allowed",
    "is_direct_opposite_transition",
    "route_pending_target",
    "route_ternary_target",
    "ternary_target_from_scalar",
    "validate_ternary_state",
    "validate_ternary_vector",
]
