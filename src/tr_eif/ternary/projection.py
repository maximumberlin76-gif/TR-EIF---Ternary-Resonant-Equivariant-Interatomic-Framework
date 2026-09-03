"""Resonance-descriptor projection for ternary target generation in TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from tr_eif.resonance import ResonanceDescriptor, ResonanceState, resonance_descriptor

from .state import TernaryState
from .target import TernaryTargetThresholds, ternary_target_from_scalar


@dataclass(frozen=True, slots=True)
class ResonanceProjection:
    """Linear projection from a resonance descriptor to one scalar coordinate."""

    phase_order_weight: float
    frequency_spread_weight: float
    bias: float = 0.0

    def __post_init__(self) -> None:
        for field_name, value in (
            ("phase_order_weight", self.phase_order_weight),
            ("frequency_spread_weight", self.frequency_spread_weight),
            ("bias", self.bias),
        ):
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise TypeError(f"{field_name} must be a real number.")

            if not isfinite(value):
                raise ValueError(f"{field_name} must be finite.")

            object.__setattr__(self, field_name, float(value))

        if (
            self.phase_order_weight == 0.0
            and self.frequency_spread_weight == 0.0
        ):
            raise ValueError(
                "At least one resonance projection weight must be nonzero."
            )

    def project(self, descriptor: ResonanceDescriptor) -> float:
        """Project one continuous resonance descriptor to a scalar coordinate."""

        if not isinstance(descriptor, ResonanceDescriptor):
            raise TypeError(
                "descriptor must be a ResonanceDescriptor instance."
            )

        return (
            self.phase_order_weight * descriptor.phase_order
            + self.frequency_spread_weight * descriptor.frequency_spread
            + self.bias
        )


def ternary_target_from_descriptor(
    descriptor: ResonanceDescriptor,
    projection: ResonanceProjection,
    thresholds: TernaryTargetThresholds,
) -> TernaryState:
    """Generate a requested ternary target from a resonance descriptor."""

    if not isinstance(projection, ResonanceProjection):
        raise TypeError(
            "projection must be a ResonanceProjection instance."
        )

    scalar = projection.project(descriptor)

    return ternary_target_from_scalar(
        scalar,
        thresholds,
    )


def ternary_target_from_resonance_state(
    state: ResonanceState,
    projection: ResonanceProjection,
    thresholds: TernaryTargetThresholds,
) -> TernaryState:
    """Generate a requested ternary target from a continuous resonance state."""

    if not isinstance(state, ResonanceState):
        raise TypeError("state must be a ResonanceState instance.")

    descriptor = resonance_descriptor(state)

    return ternary_target_from_descriptor(
        descriptor,
        projection,
        thresholds,
    )
