"""Balanced ternary state representation for TR-EIF."""

from __future__ import annotations

from enum import IntEnum
from typing import TypeAlias


class TernaryState(IntEnum):
    """Balanced ternary semantic state."""

    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


TernaryVector: TypeAlias = tuple[TernaryState, ...]


def validate_ternary_state(value: object) -> TernaryState:
    """Validate and return one balanced ternary semantic state."""

    if isinstance(value, bool):
        raise TypeError("ternary state must not be a boolean value.")

    if isinstance(value, TernaryState):
        return value

    if not isinstance(value, int):
        raise TypeError("ternary state must be an integer or TernaryState.")

    try:
        return TernaryState(value)
    except ValueError as error:
        raise ValueError("ternary state must be one of -1, 0, or 1.") from error


def validate_ternary_vector(
    values: tuple[object, ...],
) -> TernaryVector:
    """Validate a nonempty balanced ternary state vector."""

    if not isinstance(values, tuple):
        raise TypeError("ternary state vector must be a tuple.")

    if len(values) == 0:
        raise ValueError("ternary state vector must not be empty.")

    return tuple(validate_ternary_state(value) for value in values)
