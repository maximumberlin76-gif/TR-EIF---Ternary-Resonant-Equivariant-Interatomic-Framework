"""Balanced ternary state and transition semantics for TR-EIF."""

from .execution import (
    TernaryExecutionState,
    TernaryExecutionStep,
    execute_ternary_step,
)
from .projection import (
    ResonanceProjection,
    ternary_target_from_descriptor,
    ternary_target_from_resonance_state,
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
from .vector_execution import (
    TernaryExecutionVector,
    TernaryVectorExecutionStep,
    execute_ternary_vector_step,
)

__all__ = [
    "ResonanceProjection",
    "TernaryExecutionState",
    "TernaryExecutionStep",
    "TernaryExecutionVector",
    "TernaryRoute",
    "TernaryState",
    "TernaryTargetThresholds",
    "TernaryTransition",
    "TernaryVector",
    "TernaryVectorExecutionStep",
    "execute_ternary_step",
    "execute_ternary_vector_step",
    "is_committed_transition_allowed",
    "is_direct_opposite_transition",
    "route_pending_target",
    "route_ternary_target",
    "ternary_target_from_descriptor",
    "ternary_target_from_resonance_state",
    "ternary_target_from_scalar",
    "validate_ternary_state",
    "validate_ternary_vector",
]
