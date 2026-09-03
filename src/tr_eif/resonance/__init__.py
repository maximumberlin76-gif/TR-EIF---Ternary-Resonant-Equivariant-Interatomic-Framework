"""Resonance-state representations and dynamics for TR-EIF."""

from .parameters import (
    CouplingVector,
    PhaseDynamicsParameters,
    PhaseLagVector,
)
from .state import (
    FrequencyVector,
    PhaseVector,
    ResonanceState,
    wrap_phase,
    wrap_phases,
)

__all__ = [
    "CouplingVector",
    "FrequencyVector",
    "PhaseDynamicsParameters",
    "PhaseLagVector",
    "PhaseVector",
    "ResonanceState",
    "wrap_phase",
    "wrap_phases",
]
