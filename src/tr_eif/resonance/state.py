"""Typed continuous resonance-state representation for TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi
from typing import TypeAlias

PhaseVector: TypeAlias = tuple[float, ...]
FrequencyVector: TypeAlias = tuple[float, ...]

_TWO_PI = 2.0 * pi


def _validate_finite_vector(
    value: tuple[float, ...],
    *,
    field_name: str,
) -> None:
    if len(value) == 0:
        raise ValueError(f"{field_name} must not be empty.")

    if not all(isfinite(component) for component in value):
        raise ValueError(f"{field_name} must contain only finite values.")


def wrap_phase(phase: float) -> float:
    """Wrap one finite phase angle into the interval [0, 2π)."""

    if not isinstance(phase, (int, float)) or isinstance(phase, bool):
        raise TypeError("phase must be a real number.")

    if not isfinite(phase):
        raise ValueError("phase must be finite.")

    return float(phase) % _TWO_PI


def wrap_phases(phases: PhaseVector) -> PhaseVector:
    """Wrap a nonempty phase vector into the interval [0, 2π)."""

    _validate_finite_vector(phases, field_name="phases")

    return tuple(wrap_phase(phase) for phase in phases)


@dataclass(frozen=True, slots=True)
class ResonanceState:
    """Immutable continuous oscillator state for one TR-EIF layer."""

    phases: PhaseVector
    frequencies: FrequencyVector

    def __post_init__(self) -> None:
        _validate_finite_vector(self.phases, field_name="phases")
        _validate_finite_vector(self.frequencies, field_name="frequencies")

        if len(self.phases) != len(self.frequencies):
            raise ValueError(
                "phases and frequencies must contain the same number of entries."
            )

        object.__setattr__(self, "phases", wrap_phases(self.phases))

    @property
    def oscillator_count(self) -> int:
        """Return the number of oscillators represented by the state."""

        return len(self.phases)
