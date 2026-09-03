"""Resonance-state representations and dynamics for TR-EIF."""

from .dynamics import PhaseDerivativeVector, phase_derivatives
from .integrator import euler_step
from .order import phase_order_parameter, state_phase_order
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
    "euler_step",
    "phase_derivatives",
    "phase_order_parameter",
    "state_phase_order",
    "wrap_phase",
    "wrap_phases",
]
