"""Parameters for continuous phase dynamics in TR-EIF."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import TypeAlias

CouplingVector: TypeAlias = tuple[float, ...]
PhaseLagVector: TypeAlias = tuple[float, ...]


def _validate_finite_vector(
    value: tuple[float, ...],
    *,
    field_name: str,
) -> None:
    if len(value) == 0:
        raise ValueError(f"{field_name} must not be empty.")

    if not all(isfinite(component) for component in value):
        raise ValueError(f"{field_name} must contain only finite values.")


@dataclass(frozen=True, slots=True)
class PhaseDynamicsParameters:
    """Immutable parameters for graph-coupled phase dynamics."""

    coupling: CouplingVector
    phase_lag: PhaseLagVector

    def __post_init__(self) -> None:
        _validate_finite_vector(self.coupling, field_name="coupling")
        _validate_finite_vector(self.phase_lag, field_name="phase_lag")

        if len(self.coupling) != len(self.phase_lag):
            raise ValueError(
                "coupling and phase_lag must contain the same number of entries."
            )

        if any(value < 0.0 for value in self.coupling):
            raise ValueError("coupling values must be non-negative.")

    @property
    def oscillator_count(self) -> int:
        """Return the number of receiving-oscillator parameter entries."""

        return len(self.coupling)

    def validate_oscillator_count(self, oscillator_count: int) -> None:
        """Validate compatibility with a continuous oscillator state."""

        if not isinstance(oscillator_count, int) or isinstance(
            oscillator_count,
            bool,
        ):
            raise TypeError("oscillator_count must be an integer.")

        if oscillator_count <= 0:
            raise ValueError("oscillator_count must be positive.")

        if oscillator_count != self.oscillator_count:
            raise ValueError(
                "oscillator_count does not match the parameter-vector size."
            )
