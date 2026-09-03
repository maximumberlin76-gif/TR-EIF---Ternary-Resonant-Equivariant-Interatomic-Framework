"""Resonance-state representations and dynamics for TR-EIF."""

from .dynamics import PhaseDerivativeVector, phase_derivatives
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
    "PhaseDerivativeVector",
    "PhaseDynamicsParameters",
    "PhaseLagVector",
    "PhaseVector",
    "ResonanceState",
    "phase_derivatives",
    "wrap_phase",
    "wrap_phases",
]
