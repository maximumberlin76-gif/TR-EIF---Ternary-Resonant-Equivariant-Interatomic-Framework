"""Balanced ternary state and transition semantics for TR-EIF."""

from .state import (
    TernaryState,
    TernaryVector,
    validate_ternary_state,
    validate_ternary_vector,
)

__all__ = [
    "TernaryState",
    "TernaryVector",
    "validate_ternary_state",
    "validate_ternary_vector",
]
