"""Resonance-state representations and dynamics for TR-EIF."""

from .classification import ResonanceRegion, classify_resonance_region
from .descriptor import (
    ResonanceDescriptor,
    frequency_spread,
    resonance_coordinate,
    resonance_descriptor,
)
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
    "ResonanceDescriptor",
    "ResonanceRegion",
    "ResonanceSpace",
    "ResonanceState",
    "ResonanceWindow",
    "classify_resonance_region",
    "euler_step",
    "frequency_spread",
    "phase_derivatives",
    "phase_order_parameter",
    "resonance_coordinate",
    "resonance_descriptor",
    "state_phase_order",
    "wrap_phase",
    "wrap_phases",
]
