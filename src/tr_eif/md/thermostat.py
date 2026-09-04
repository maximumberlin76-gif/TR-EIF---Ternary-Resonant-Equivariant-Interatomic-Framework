"""Deterministic velocity-rescaling thermostat primitives for TR-EIF MD."""

from __future__ import annotations

from math import isfinite, sqrt

from tr_eif.md.observables import kinetic_energy
from tr_eif.md.state import MolecularDynamicsState


def _validate_positive_finite(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one positive finite real scalar."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    normalized = float(value)

    if normalized <= 0.0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return normalized


def _validate_nonnegative_finite(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one nonnegative finite real scalar."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    normalized = float(value)

    if normalized < 0.0:
        raise ValueError(
            f"{field_name} must be nonnegative."
        )

    return normalized


def _validate_degrees_of_freedom(
    state: MolecularDynamicsState,
    degrees_of_freedom: int,
) -> int:
    """Validate the declared translational degrees of freedom."""

    if not isinstance(degrees_of_freedom, int) or isinstance(
        degrees_of_freedom,
        bool,
    ):
        raise TypeError(
            "degrees_of_freedom must be an integer."
        )

    maximum = 3 * state.atom_count

    if degrees_of_freedom <= 0:
        raise ValueError(
            "degrees_of_freedom must be greater than zero."
        )

    if degrees_of_freedom > maximum:
        raise ValueError(
            "degrees_of_freedom must not exceed "
            "three times the atom count."
        )

    return degrees_of_freedom


def kinetic_temperature(
    state: MolecularDynamicsState,
    degrees_of_freedom: int,
    boltzmann_constant: float,
) -> float:
    """Evaluate kinetic temperature under an explicit MD unit convention.

    The relation used is

        T = 2 K / (f k_B)

    where K is total kinetic energy, f is the explicitly declared number
    of translational degrees of freedom, and k_B is supplied in units
    consistent with the MD energy and temperature units.

    This thermodynamic kinetic-temperature estimator is separate from any
    classifier, optimization, resonance, or ternary temperature parameter.
    """

    if not isinstance(state, MolecularDynamicsState):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    dof = _validate_degrees_of_freedom(
        state,
        degrees_of_freedom,
    )
    k_b = _validate_positive_finite(
        boltzmann_constant,
        field_name="boltzmann_constant",
    )

    kinetic = kinetic_energy(state)

    temperature = (
        2.0
        * kinetic.total_kinetic_energy
        / (float(dof) * k_b)
    )

    if not isfinite(temperature):
        raise ValueError(
            "Computed kinetic temperature must be finite."
        )

    return temperature


def velocity_rescaling_factor(
    current_temperature: float,
    target_temperature: float,
) -> float:
    """Return the deterministic global velocity-rescaling factor."""

    current = _validate_nonnegative_finite(
        current_temperature,
        field_name="current_temperature",
    )
    target = _validate_nonnegative_finite(
        target_temperature,
        field_name="target_temperature",
    )

    if current == 0.0:
        if target == 0.0:
            return 1.0

        raise ValueError(
            "A positive target temperature cannot be reached by "
            "deterministic velocity rescaling from zero kinetic temperature."
        )

    factor = sqrt(target / current)

    if not isfinite(factor):
        raise ValueError(
            "Velocity-rescaling factor must be finite."
        )

    return factor


def rescale_velocities(
    state: MolecularDynamicsState,
    scale: float,
) -> MolecularDynamicsState:
    """Return an MD state with every Cartesian velocity globally rescaled."""

    if not isinstance(state, MolecularDynamicsState):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    normalized_scale = _validate_nonnegative_finite(
        scale,
        field_name="scale",
    )

    velocities = tuple(
        (
            normalized_scale * velocity[0],
            normalized_scale * velocity[1],
            normalized_scale * velocity[2],
        )
        for velocity in state.velocities
    )

    return MolecularDynamicsState(
        configuration=state.configuration,
        velocities=velocities,
        masses=state.masses,
        step=state.step,
        time=state.time,
    )


def rescale_to_kinetic_temperature(
    state: MolecularDynamicsState,
    target_temperature: float,
    degrees_of_freedom: int,
    boltzmann_constant: float,
) -> MolecularDynamicsState:
    """Apply deterministic global velocity rescaling to a target temperature.

    The operation changes velocities only. Atomic configuration, masses,
    simulation step, and simulation time are retained unchanged.

    No stochastic velocity generation is performed. A state with zero
    kinetic temperature therefore cannot be rescaled to a positive target
    temperature by this operator.
    """

    if not isinstance(state, MolecularDynamicsState):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    target = _validate_nonnegative_finite(
        target_temperature,
        field_name="target_temperature",
    )

    current = kinetic_temperature(
        state,
        degrees_of_freedom,
        boltzmann_constant,
    )

    scale = velocity_rescaling_factor(
        current,
        target,
    )

    return rescale_velocities(
        state,
        scale,
    )
