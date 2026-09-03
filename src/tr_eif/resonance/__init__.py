"""Resonance-state representations and dynamics for TR-EIF."""

from .classification import ResonanceRegion, classify_resonance_region
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
from .window import (
    ResonanceCoordinate,
    ResonanceSpace,
    ResonanceWindow,
)

__all__ = [
    "CouplingVector",
    "FrequencyVector",
    "PhaseDerivativeVector",
    "PhaseDynamicsParameters",
    "PhaseLagVector",
    "PhaseVector",
    "ResonanceCoordinate",
    "ResonanceRegion",
    "ResonanceSpace",
    "ResonanceState",
    "ResonanceWindow",
    "classify_resonance_region",
    "euler_step",
    "phase_derivatives",
    "phase_order_parameter",
    "state_phase_order",
    "wrap_phase",
    "wrap_phases",
]
