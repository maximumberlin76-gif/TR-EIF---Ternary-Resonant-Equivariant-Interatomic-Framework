"""Deterministic isotropic pressure-coupling primitives for TR-EIF MD."""

from __future__ import annotations

from math import isfinite

from tr_eif.configuration import AtomicConfiguration, Cell3x3, Vector3
from tr_eif.md.state import MolecularDynamicsState


def _validate_finite_real(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one finite real scalar."""

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(
            f"{field_name} must be a real number."
        )

    if not isfinite(value):
        raise ValueError(
            f"{field_name} must be finite."
        )

    return float(value)


def _validate_positive_finite(
    value: float,
    *,
    field_name: str,
) -> float:
    """Validate and normalize one positive finite real scalar."""

    normalized = _validate_finite_real(
        value,
        field_name=field_name,
    )

    if normalized <= 0.0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return normalized


def _scale_vector(
    vector: Vector3,
    scale: float,
) -> Vector3:
    """Return one Cartesian vector under isotropic affine scaling."""

    return (
        scale * vector[0],
        scale * vector[1],
        scale * vector[2],
    )


def isotropic_barostat_scale(
    current_pressure: float,
    target_pressure: float,
    compressibility: float,
    time_step: float,
    coupling_time: float,
) -> float:
    """Return the isotropic linear scale for one pressure-coupling update.

    The pressure-coupling relation used by this reference operator is

        s^3 = 1 - (dt / tau_p) * beta * (P_target - P_current)

    where beta is the explicitly supplied compressibility, dt is the MD
    time step, and tau_p is the explicitly supplied pressure-coupling time.

    Pressure and compressibility units must be mutually consistent.
    This module does not supply a pressure estimator, material
    compressibility, target pressure, or coupling time.
    """

    current = _validate_finite_real(
        current_pressure,
        field_name="current_pressure",
    )
    target = _validate_finite_real(
        target_pressure,
        field_name="target_pressure",
    )
    beta = _validate_positive_finite(
        compressibility,
        field_name="compressibility",
    )
    dt = _validate_positive_finite(
        time_step,
        field_name="time_step",
    )
    tau = _validate_positive_finite(
        coupling_time,
        field_name="coupling_time",
    )

    volume_scale = (
        1.0
        - (dt / tau)
        * beta
        * (target - current)
    )

    if not isfinite(volume_scale):
        raise ValueError(
            "Computed isotropic volume scale must be finite."
        )

    if volume_scale <= 0.0:
        raise ValueError(
            "Computed isotropic volume scale must be greater than zero."
        )

    linear_scale = volume_scale ** (1.0 / 3.0)

    if not isfinite(linear_scale) or linear_scale <= 0.0:
        raise ValueError(
            "Computed isotropic linear scale must be finite and positive."
        )

    return linear_scale


def scale_periodic_configuration(
    configuration: AtomicConfiguration,
    linear_scale: float,
) -> AtomicConfiguration:
    """Apply isotropic affine scaling to a fully periodic 3D configuration.

    Cartesian positions and all three lattice vectors are multiplied by
    the same positive factor. Fractional atomic coordinates are therefore
    retained.
    """

    if not isinstance(
        configuration,
        AtomicConfiguration,
    ):
        raise TypeError(
            "configuration must be an AtomicConfiguration instance."
        )

    if configuration.cell is None:
        raise ValueError(
            "Isotropic barostat scaling requires a simulation cell."
        )

    if configuration.periodic != (True, True, True):
        raise ValueError(
            "Isotropic barostat scaling requires all three periodic axes."
        )

    scale = _validate_positive_finite(
        linear_scale,
        field_name="linear_scale",
    )

    scaled_positions = tuple(
        _scale_vector(
            position,
            scale,
        )
        for position in configuration.positions
    )

    scaled_cell: Cell3x3 = (
        _scale_vector(
            configuration.cell[0],
            scale,
        ),
        _scale_vector(
            configuration.cell[1],
            scale,
        ),
        _scale_vector(
            configuration.cell[2],
            scale,
        ),
    )

    return AtomicConfiguration(
        species=configuration.species,
        positions=scaled_positions,
        cell=scaled_cell,
        periodic=configuration.periodic,
    )


def apply_isotropic_barostat(
    state: MolecularDynamicsState,
    current_pressure: float,
    target_pressure: float,
    compressibility: float,
    time_step: float,
    coupling_time: float,
) -> MolecularDynamicsState:
    """Apply one deterministic isotropic pressure-coupling update.

    The operator rescales the simulation cell and Cartesian positions only.
    Velocities, masses, MD step, and MD time are retained.

    Integration order relative to force evaluation, velocity updates,
    neighbor-list rebuilding, and pressure evaluation remains explicit at
    the caller level.
    """

    if not isinstance(
        state,
        MolecularDynamicsState,
    ):
        raise TypeError(
            "state must be a MolecularDynamicsState instance."
        )

    scale = isotropic_barostat_scale(
        current_pressure=current_pressure,
        target_pressure=target_pressure,
        compressibility=compressibility,
        time_step=time_step,
        coupling_time=coupling_time,
    )

    configuration = scale_periodic_configuration(
        state.configuration,
        scale,
    )

    return MolecularDynamicsState(
        configuration=configuration,
        velocities=state.velocities,
        masses=state.masses,
        step=state.step,
        time=state.time,
    )
