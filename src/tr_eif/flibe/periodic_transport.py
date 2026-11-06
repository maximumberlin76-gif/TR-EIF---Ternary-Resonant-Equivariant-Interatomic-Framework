
"""Species-resolved transport time series for periodic polarizable FLiBe MD.

The FLiBe periodic velocity-Verlet integrator retains continuous Cartesian
positions across lattice crossings. This operator independently verifies each
position and velocity update against the recorded forces before treating the
stored coordinates as an unwrapped trajectory.

For species s, the single-origin observables are

    MSD_s(t) = mean_i |[r_i(t) - r_i(0)] - Delta_R_frame(t)|**2
    VACF_s(t) = mean_i u_i(0) dot u_i(t),

where the frame is the laboratory frame or the mass-weighted center-of-mass
frame. The observations retain their finite-time coordinates and SI units.
A diffusion fit requires a separately declared time window and sampling rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isclose, isfinite

from .periodic_polarizable_md import FLiBePeriodicMDRun

_SPECIES = ("Li", "Be", "F")


class FLiBeTransportFrame(str, Enum):
    """Cartesian reference frame of a species-resolved transport series."""

    LABORATORY = "LABORATORY"
    CENTER_OF_MASS = "CENTER_OF_MASS"


def _identifier(value: str, label: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{label} must be a string.")
    if not value or not value.strip() or value != value.strip():
        raise ValueError(f"{label} must be a nonempty trimmed identifier.")
    return value


def _finite(value: float, label: str, *, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or (nonnegative and result < 0.0):
        raise ValueError(f"{label} must be finite and satisfy its sign contract.")
    return result


def _series(values: tuple[float, ...], label: str, *, nonnegative: bool) -> tuple[float, ...]:
    if not isinstance(values, tuple) or not values:
        raise TypeError(f"{label} must be a nonempty tuple.")
    return tuple(
        _finite(value, f"{label}[{index}]", nonnegative=nonnegative)
        for index, value in enumerate(values)
    )


@dataclass(frozen=True, slots=True)
class FLiBeSpeciesTransportSeries:
    """Single-time-origin MSD and VACF of one chemical species, in SI units."""

    species: str
    atom_count: int
    mean_squared_displacement_m2: tuple[float, ...]
    velocity_autocorrelation_m2_per_s2: tuple[float, ...]

    def __post_init__(self) -> None:
        if self.species not in _SPECIES:
            raise ValueError("species must be Li, Be, or F.")
        if (
            not isinstance(self.atom_count, int)
            or isinstance(self.atom_count, bool)
            or self.atom_count <= 0
        ):
            raise ValueError("atom_count must be a positive integer.")
        msd = _series(
            self.mean_squared_displacement_m2,
            "mean_squared_displacement_m2",
            nonnegative=True,
        )
        vacf = _series(
            self.velocity_autocorrelation_m2_per_s2,
            "velocity_autocorrelation_m2_per_s2",
            nonnegative=False,
        )
        if len(msd) != len(vacf):
            raise ValueError("MSD and VACF sample counts must agree.")
        if msd[0] != 0.0:
            raise ValueError("initial MSD must equal zero.")
        if vacf[0] < 0.0:
            raise ValueError("initial VACF must be nonnegative.")
        object.__setattr__(self, "mean_squared_displacement_m2", msd)
        object.__setattr__(self, "velocity_autocorrelation_m2_per_s2", vacf)


@dataclass(frozen=True, slots=True)
class FLiBePeriodicTransportResult:
    """Immutable species transport evidence with frame and source identity."""

    trajectory_id: str
    model_id: str
    source_file_sha256: str
    source_doi: str
    units_source_id: str
    frame: FLiBeTransportFrame
    times_s: tuple[float, ...]
    species_series: tuple[FLiBeSpeciesTransportSeries, ...]

    def __post_init__(self) -> None:
        for label in (
            "trajectory_id", "model_id", "source_doi", "units_source_id"
        ):
            _identifier(getattr(self, label), label)
        digest = self.source_file_sha256
        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
        ):
            raise ValueError("source_file_sha256 must be a lowercase SHA-256 digest.")
        if not isinstance(self.frame, FLiBeTransportFrame):
            raise TypeError("frame must be FLiBeTransportFrame.")
        times = _series(self.times_s, "times_s", nonnegative=True)
        if len(times) < 2 or times[0] != 0.0:
            raise ValueError("time series must start at zero and contain two states.")
        if any(current <= previous for previous, current in zip(times, times[1:])):
            raise ValueError("times_s must be strictly increasing.")
        if (
            not isinstance(self.species_series, tuple)
            or not all(
                isinstance(item, FLiBeSpeciesTransportSeries)
                for item in self.species_series
            )
            or tuple(item.species for item in self.species_series) != _SPECIES
        ):
            raise ValueError("species_series must contain Li, Be, F in that order.")
        if any(len(item.mean_squared_displacement_m2) != len(times)
               for item in self.species_series):
            raise ValueError("all species series must align with times_s.")
        object.__setattr__(self, "times_s", times)

    @property
    def atom_count(self) -> int:
        """Total number of atoms participating in the transport observation."""
        return sum(item.atom_count for item in self.species_series)

    @property
    def sample_count(self) -> int:
        """Number of aligned trajectory states."""
        return len(self.times_s)

    def for_species(self, symbol: str) -> FLiBeSpeciesTransportSeries:
        """Select the Li, Be, or F observation by its chemical identity."""
        for item in self.species_series:
            if item.species == symbol:
                return item
        raise ValueError("species must be Li, Be, or F.")


def _validate_unwrapped_verlet(
    run: FLiBePeriodicMDRun,
    position_tolerance_code: float,
    velocity_tolerance_code: float,
) -> None:
    """Verify continuous fixed-cell Verlet states directly from recorded forces."""

    states = run.trajectory.states
    initial = states[0].configuration
    if initial.cell is None or initial.periodic != (True, True, True):
        raise ValueError("FLiBe periodic transport requires a three-axis periodic cell.")
    if any(
        state.configuration.species != initial.species
        or state.configuration.cell != initial.cell
        or state.configuration.periodic != initial.periodic
        or state.masses != states[0].masses
        for state in states
    ):
        raise ValueError("transport requires fixed cell, species, and masses.")
    scale = run.units.acceleration_factor
    for step in run.trajectory.steps:
        before = step.previous
        after = step.current
        dt = after.time - before.time
        if not isfinite(dt) or dt <= 0.0:
            raise ValueError("time increments must be positive and finite.")
        for index, mass in enumerate(before.masses):
            for axis in range(3):
                acceleration_before = scale * step.forces_before.forces[index][axis] / mass
                acceleration_after = scale * step.forces_after.forces[index][axis] / mass
                measured_displacement = (
                    after.configuration.positions[index][axis]
                    - before.configuration.positions[index][axis]
                )
                verlet_displacement = (
                    before.velocities[index][axis] * dt
                    + 0.5 * acceleration_before * dt * dt
                )
                measured_velocity_change = (
                    after.velocities[index][axis] - before.velocities[index][axis]
                )
                verlet_velocity_change = (
                    0.5 * (acceleration_before + acceleration_after) * dt
                )
                if not isclose(
                    measured_displacement,
                    verlet_displacement,
                    rel_tol=1.0e-12,
                    abs_tol=position_tolerance_code,
                ):
                    raise ValueError("trajectory position increment violates unwrapped Verlet.")
                if not isclose(
                    measured_velocity_change,
                    verlet_velocity_change,
                    rel_tol=1.0e-12,
                    abs_tol=velocity_tolerance_code,
                ):
                    raise ValueError("trajectory velocity increment violates Verlet.")


def _mass_weighted_vector(
    vectors: tuple[tuple[float, float, float], ...],
    masses: tuple[float, ...],
) -> tuple[float, float, float]:
    total_mass = fsum(masses)
    return tuple(
        fsum(mass * vector[axis] for mass, vector in zip(masses, vectors, strict=True))
        / total_mass
        for axis in range(3)
    )  # type: ignore[return-value]


def evaluate_flibe_periodic_transport(
    run: FLiBePeriodicMDRun,
    *,
    trajectory_id: str,
    frame: FLiBeTransportFrame = FLiBeTransportFrame.CENTER_OF_MASS,
    position_tolerance_code: float = 1.0e-10,
    velocity_tolerance_code: float = 1.0e-10,
) -> FLiBePeriodicTransportResult:
    """Evaluate single-origin MSD and VACF from verified unwrapped FLiBe MD.

    The laboratory frame retains net translation. The center-of-mass frame
    subtracts mass-weighted displacement from the initial state and the
    instantaneous mass-weighted velocity from each state's velocities.
    Recorded coordinates use the fixed-cell, continuous-Verlet convention.
    """

    if not isinstance(run, FLiBePeriodicMDRun):
        raise TypeError("run must be FLiBePeriodicMDRun.")
    _identifier(trajectory_id, "trajectory_id")
    if not isinstance(frame, FLiBeTransportFrame):
        raise TypeError("frame must be FLiBeTransportFrame.")
    for label, value in (
        ("position_tolerance_code", position_tolerance_code),
        ("velocity_tolerance_code", velocity_tolerance_code),
    ):
        _finite(value, label, nonnegative=True)

    _validate_unwrapped_verlet(run, position_tolerance_code, velocity_tolerance_code)
    states = run.trajectory.states
    species = states[0].configuration.species
    masses = states[0].masses
    indices = {
        symbol: tuple(index for index, name in enumerate(species) if name == symbol)
        for symbol in _SPECIES
    }
    if any(not members for members in indices.values()) or sum(
        len(members) for members in indices.values()
    ) != len(species):
        raise ValueError("the periodic FLiBe trajectory must contain Li, Be, and F.")

    initial_positions = states[0].configuration.positions
    initial_velocities = states[0].velocities
    center_velocity_initial = _mass_weighted_vector(initial_velocities, masses)
    code_length = run.units.coordinate_unit_to_meter
    code_speed = code_length / run.units.time_unit_to_second
    time_factor = run.units.time_unit_to_second
    time_origin = states[0].time

    msd = {symbol: [] for symbol in _SPECIES}
    vacf = {symbol: [] for symbol in _SPECIES}
    times = []
    for state in states:
        seconds = _finite(
            (state.time - time_origin) * time_factor,
            "elapsed_time_s", nonnegative=True,
        )
        times.append(seconds)
        displacement = tuple(
            tuple(current[axis] - initial[axis] for axis in range(3))
            for current, initial in zip(
                state.configuration.positions, initial_positions, strict=True
            )
        )
        center_displacement = (
            _mass_weighted_vector(displacement, masses)
            if frame is FLiBeTransportFrame.CENTER_OF_MASS
            else (0.0, 0.0, 0.0)
        )
        center_velocity = (
            _mass_weighted_vector(state.velocities, masses)
            if frame is FLiBeTransportFrame.CENTER_OF_MASS
            else (0.0, 0.0, 0.0)
        )
        initial_center_velocity = (
            center_velocity_initial
            if frame is FLiBeTransportFrame.CENTER_OF_MASS
            else (0.0, 0.0, 0.0)
        )
        for symbol, members in indices.items():
            displacement_mean = fsum(
                fsum(
                    (displacement[index][axis] - center_displacement[axis]) ** 2
                    for axis in range(3)
                )
                for index in members
            ) / len(members)
            velocity_correlation = fsum(
                fsum(
                    (initial_velocities[index][axis] - initial_center_velocity[axis])
                    * (state.velocities[index][axis] - center_velocity[axis])
                    for axis in range(3)
                )
                for index in members
            ) / len(members)
            msd[symbol].append(_finite(
                displacement_mean * code_length**2,
                f"{symbol} MSD", nonnegative=True,
            ))
            vacf[symbol].append(_finite(
                velocity_correlation * code_speed**2,
                f"{symbol} VACF",
            ))

    return FLiBePeriodicTransportResult(
        trajectory_id=trajectory_id,
        model_id=run.model_id,
        source_file_sha256=run.source_file_sha256,
        source_doi=run.evaluations[0].source_doi,
        units_source_id=run.units.source_id,
        frame=frame,
        times_s=tuple(times),
        species_series=tuple(
            FLiBeSpeciesTransportSeries(
                species=symbol,
                atom_count=len(indices[symbol]),
                mean_squared_displacement_m2=tuple(msd[symbol]),
                velocity_autocorrelation_m2_per_s2=tuple(vacf[symbol]),
            )
            for symbol in _SPECIES
        ),
    )
