"""Continuous-to-ternary target mapping for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .state import TernaryState


def _validate_scalar(value: float, *, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a real number.")

    if not isfinite(value):
        raise ValueError(f"{field_name} must be finite.")

    return float(value)


@dataclass(frozen=True, slots=True)
class TernaryTargetThresholds:
    """Ordered thresholds for scalar continuous-to-ternary target mapping."""

    negative: float
    positive: float

    def __post_init__(self) -> None:
        negative = _validate_scalar(
            self.negative,
            field_name="negative",
        )
        positive = _validate_scalar(
            self.positive,
            field_name="positive",
        )

        if negative >= positive:
            raise ValueError(
                "negative threshold must be strictly less than "
                "positive threshold."
            )

        object.__setattr__(self, "negative", negative)
        object.__setattr__(self, "positive", positive)


def ternary_target_from_scalar(
    value: float,
    thresholds: TernaryTargetThresholds,
) -> TernaryState:
    """Map one continuous scalar to a requested balanced ternary target."""

    scalar = _validate_scalar(value, field_name="value")

    if not isinstance(thresholds, TernaryTargetThresholds):
        raise TypeError(
            "thresholds must be a TernaryTargetThresholds instance."
        )

    if scalar < thresholds.negative:
        return TernaryState.NEGATIVE

    if scalar > thresholds.positive:
        return TernaryState.POSITIVE

    return TernaryState.NEUTRAL
