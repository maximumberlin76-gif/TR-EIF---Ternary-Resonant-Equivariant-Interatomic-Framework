"""Frame-consistent kinetic temperature and pressure coordinates for FLiBe MD."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.md.trajectory import MolecularDynamicsTrajectory

from .configuration import FLiBeConfiguration
from .trajectory_pressure import FLiBeTrajectoryPressure, FLiBeVelocityFrame
from .trajectory_state_correspondence import (
    BOLTZMANN_CONSTANT_J_PER_K,
    FLiBeTrajectoryStateCoordinates,
)


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return result


def _nonnegative(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative.")
    return result


def _cell_volume(cell: tuple[tuple[float, float, float], ...]) -> float:
    a, b, c = cell
    return abs(
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


@dataclass(frozen=True, slots=True)
class FLiBeFrameThermalSample:
    """Kinetic quantities for one MD frame in an explicitly selected velocity frame."""

    state_index: int
    md_step: int
    md_time: float
    velocity_origin_m_s: tuple[float, float, float]
    kinetic_energy_j: float
    kinetic_temperature_k: float
    kinetic_pressure_pa: float

    def __post_init__(self) -> None:
        for name in ("state_index", "md_step"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer.")
        _nonnegative(self.md_time, "md_time")
        if not isinstance(self.velocity_origin_m_s, tuple) or len(self.velocity_origin_m_s) != 3:
            raise ValueError("velocity_origin_m_s must contain three components.")
        for component in self.velocity_origin_m_s:
            if isinstance(component, bool) or not isinstance(component, (int, float)) or not isfinite(component):
                raise ValueError("velocity_origin_m_s must contain finite real components.")
        _nonnegative(self.kinetic_energy_j, "kinetic_energy_j")
        _nonnegative(self.kinetic_temperature_k, "kinetic_temperature_k")
        _nonnegative(self.kinetic_pressure_pa, "kinetic_pressure_pa")


@dataclass(frozen=True, slots=True)
class FLiBeFrameThermodynamicState:
    """Aligned pressure and temperature trace with preserved velocity-frame identity."""

    pressure_trace: FLiBeTrajectoryPressure
    degrees_of_freedom: int
    physical_state_id: str
    physical_state_method_id: str
    samples: tuple[FLiBeFrameThermalSample, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.pressure_trace, FLiBeTrajectoryPressure):
            raise TypeError("pressure_trace must be an FLiBeTrajectoryPressure.")
        maximum = 3 * self.pressure_trace.density_trace.atom_count
        if self.pressure_trace.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS:
            maximum -= 3
        if (
            isinstance(self.degrees_of_freedom, bool)
            or not isinstance(self.degrees_of_freedom, int)
            or not 0 < self.degrees_of_freedom <= maximum
        ):
            raise ValueError("degrees_of_freedom must fit the selected velocity frame.")
        _identifier(self.physical_state_id, "physical_state_id")
        _identifier(self.physical_state_method_id, "physical_state_method_id")
        if not isinstance(self.samples, tuple) or len(self.samples) != len(self.pressure_trace.samples):
            raise ValueError("thermal and pressure sample counts must agree.")
        for thermal, pressure in zip(self.samples, self.pressure_trace.samples, strict=True):
            if not isinstance(thermal, FLiBeFrameThermalSample):
                raise TypeError("samples must contain FLiBeFrameThermalSample values.")
            if (thermal.state_index, thermal.md_step, thermal.md_time) != (
                pressure.state_index, pressure.md_step, pressure.md_time
            ):
                raise ValueError("thermal and pressure state identities must agree.")
            expected_temperature = 2.0 * thermal.kinetic_energy_j / (
                self.degrees_of_freedom * BOLTZMANN_CONSTANT_J_PER_K
            )
            expected_pressure = 2.0 * thermal.kinetic_energy_j / (
                3.0 * pressure.cell_volume_m3
            )
            if not isclose(thermal.kinetic_temperature_k, expected_temperature, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError("thermal sample energy and temperature must agree.")
            if not isclose(thermal.kinetic_pressure_pa, expected_pressure, rel_tol=1e-12, abs_tol=1e-8):
                raise ValueError("thermal sample energy and kinetic pressure must agree.")
            recorded_pressure = fsum(pressure.kinetic_tensor_pa[i][i] for i in range(3)) / 3.0
            if not isclose(thermal.kinetic_pressure_pa, recorded_pressure, rel_tol=1e-12, abs_tol=1e-8):
                raise ValueError("thermal sample and pressure tensor trace must agree.")

    @property
    def velocity_frame(self) -> FLiBeVelocityFrame:
        """Return the exact frame used for pressure and kinetic temperature."""
        return self.pressure_trace.velocity_frame

    @property
    def mean_kinetic_temperature_k(self) -> float:
        """Arithmetic mean of sampled kinetic temperatures."""
        return fsum(sample.kinetic_temperature_k for sample in self.samples) / len(self.samples)

    def to_state_coordinates(self) -> FLiBeTrajectoryStateCoordinates:
        """Build density-comparison coordinates for a nonnegative mean pressure.

        The enclosing FLiBeFrameThermodynamicState retains the velocity-frame
        provenance. A negative signed pressure is preserved in pressure_trace
        and handled by the existing pressure-coordinate domain check.
        """
        return FLiBeTrajectoryStateCoordinates(
            density_trace=self.pressure_trace.density_trace,
            kinetic_temperature_k=tuple(sample.kinetic_temperature_k for sample in self.samples),
            degrees_of_freedom=self.degrees_of_freedom,
            time_unit_to_second=self.pressure_trace.time_unit_to_second,
            physical_state_id=self.physical_state_id,
            physical_state_method_id=self.physical_state_method_id,
            pressure=self.pressure_trace.to_observed_pressure_coordinate(),
        )


def evaluate_flibe_frame_thermodynamics(
    trajectory: MolecularDynamicsTrajectory,
    pressure_trace: FLiBeTrajectoryPressure,
    *,
    degrees_of_freedom: int,
    physical_state_id: str,
    physical_state_method_id: str,
) -> FLiBeFrameThermodynamicState:
    """Evaluate kinetic temperatures in the frame of a computed pressure trace.

    LABORATORY uses original velocities; CENTER_OF_MASS subtracts each
    frame's mass-weighted velocity. The supplied degrees of freedom account
    for removed translation and any additional explicitly modeled constraints.
    The kinetic identity Tr(P_kin)/3 = f k_B T/(3 V) is checked per frame.
    """
    if not isinstance(trajectory, MolecularDynamicsTrajectory):
        raise TypeError("trajectory must be a MolecularDynamicsTrajectory.")
    if not isinstance(pressure_trace, FLiBeTrajectoryPressure):
        raise TypeError("pressure_trace must be an FLiBeTrajectoryPressure.")
    _identifier(physical_state_id, "physical_state_id")
    _identifier(physical_state_method_id, "physical_state_method_id")

    density_trace = pressure_trace.density_trace
    maximum = 3 * density_trace.atom_count
    if pressure_trace.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS:
        maximum -= 3
    if (
        isinstance(degrees_of_freedom, bool)
        or not isinstance(degrees_of_freedom, int)
        or not 0 < degrees_of_freedom <= maximum
    ):
        raise ValueError("degrees_of_freedom must fit the selected velocity frame.")
    if trajectory.atom_count != density_trace.atom_count:
        raise ValueError("trajectory and pressure atom counts must agree.")

    initial = trajectory.initial
    if FLiBeConfiguration(initial.configuration).composition() != density_trace.composition:
        raise ValueError("trajectory and density compositions must agree.")
    mass_factor = density_trace.mass_unit_to_kg
    velocity_factor = density_trace.coordinate_unit_to_meter / pressure_trace.time_unit_to_second
    _positive(velocity_factor, "velocity conversion factor")
    energy_factor = _positive(mass_factor * velocity_factor**2, "MD energy unit in joules")
    initial_mass_kg = fsum(initial.masses) * mass_factor
    if not isclose(initial_mass_kg, density_trace.total_mass_kg, rel_tol=1e-12):
        raise ValueError("trajectory and density mass inventories must agree.")

    states = trajectory.states
    results: list[FLiBeFrameThermalSample] = []
    for density, pressure in zip(density_trace.samples, pressure_trace.samples, strict=True):
        if density.state_index >= len(states):
            raise ValueError("density sample index exceeds trajectory length.")
        state = states[density.state_index]
        if (state.step, state.time) != (density.md_step, density.md_time):
            raise ValueError("thermal and trajectory state identities must agree.")
        if state.configuration.species != initial.configuration.species or state.masses != initial.masses:
            raise ValueError("ordered species and atomic masses must remain invariant.")
        if state.configuration.periodic != (True, True, True) or state.configuration.cell is None:
            raise ValueError("thermal sampling requires three periodic cell axes.")
        volume_m3 = _cell_volume(state.configuration.cell) * density_trace.coordinate_unit_to_meter**3
        if not isfinite(volume_m3) or volume_m3 <= 0.0 or not isclose(
            volume_m3, density.cell_volume_m3, rel_tol=1e-12
        ):
            raise ValueError("thermal and density cell volumes must agree.")
        mass_total = fsum(state.masses)
        if pressure_trace.velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS:
            origin = tuple(
                fsum(mass * velocity[axis] for mass, velocity in zip(
                    state.masses, state.velocities, strict=True
                )) / mass_total
                for axis in range(3)
            )
        else:
            origin = (0.0, 0.0, 0.0)

        components = tuple(
            tuple(velocity[axis] - origin[axis] for axis in range(3))
            for velocity in state.velocities
        )
        twice_kinetic_md = fsum(
            mass * fsum(component * component for component in velocity)
            for mass, velocity in zip(state.masses, components, strict=True)
        )
        twice_kinetic_j = twice_kinetic_md * energy_factor
        if not isfinite(twice_kinetic_j) or twice_kinetic_j < 0.0:
            raise ValueError("kinetic energy must be finite and nonnegative.")
        temperature = twice_kinetic_j / (degrees_of_freedom * BOLTZMANN_CONSTANT_J_PER_K)
        if not isfinite(temperature) or temperature < 0.0:
            raise ValueError("kinetic temperature must be finite and nonnegative.")

        kinetic_tensor_factor = energy_factor / volume_m3
        for axis_a in range(3):
            for axis_b in range(3):
                expected = fsum(
                    mass * velocity[axis_a] * velocity[axis_b]
                    for mass, velocity in zip(state.masses, components, strict=True)
                ) * kinetic_tensor_factor
                if not isfinite(expected) or not isclose(
                    expected, pressure.kinetic_tensor_pa[axis_a][axis_b],
                    rel_tol=1e-12, abs_tol=1e-8
                ):
                    raise ValueError("kinetic pressure tensor and velocity frame differ.")

        kinetic_pressure = twice_kinetic_j / (3.0 * volume_m3)
        recorded_pressure = fsum(pressure.kinetic_tensor_pa[i][i] for i in range(3)) / 3.0
        if not isfinite(kinetic_pressure) or not isclose(
            kinetic_pressure, recorded_pressure, rel_tol=1e-12, abs_tol=1e-8
        ):
            raise ValueError("kinetic temperature and pressure trace relation differs.")

        results.append(FLiBeFrameThermalSample(
            state_index=density.state_index,
            md_step=density.md_step,
            md_time=density.md_time,
            velocity_origin_m_s=tuple(value * velocity_factor for value in origin),
            kinetic_energy_j=0.5 * twice_kinetic_j,
            kinetic_temperature_k=temperature,
            kinetic_pressure_pa=kinetic_pressure,
        ))

    return FLiBeFrameThermodynamicState(
        pressure_trace=pressure_trace,
        degrees_of_freedom=degrees_of_freedom,
        physical_state_id=physical_state_id,
        physical_state_method_id=physical_state_method_id,
        samples=tuple(results),
    )
