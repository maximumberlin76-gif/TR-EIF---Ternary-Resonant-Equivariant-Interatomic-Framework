"""Frame-resolved pressure tensors from FLiBe MD and energy-derived stress."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isclose, isfinite
from typing import TypeAlias

from tr_eif.energy.stress import StressState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory

from .trajectory_density import FLiBeTrajectoryDensity
from .trajectory_state_correspondence import (
    FLiBePressureCoordinate,
    FLiBePressureRole,
)
from .units import ParameterProvenance


Tensor3: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


class FLiBeVelocityFrame(str, Enum):
    """Velocity convention in the kinetic pressure tensor."""

    CENTER_OF_MASS = "CENTER_OF_MASS"
    LABORATORY = "LABORATORY"


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _tensor(tensor: Tensor3, name: str) -> Tensor3:
    if not isinstance(tensor, tuple) or len(tensor) != 3:
        raise ValueError(f"{name} must have three tensor rows.")
    for row in tensor:
        if not isinstance(row, tuple) or len(row) != 3:
            raise ValueError(f"{name} must have three components per row.")
        if any(isinstance(x, bool) or not isinstance(x, (int, float))
               or not isfinite(x) for x in row):
            raise ValueError(f"{name} must contain finite real components.")
    return tensor


def _cell_volume(cell: Tensor3) -> float:
    a, b, c = cell
    return abs(
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


@dataclass(frozen=True, slots=True)
class FLiBePotentialStressSample:
    """Energy–strain stress evaluated for an identified MD state.

    StressState uses the existing convention sigma_ab = (1/V) dE/deps_ab.
    Its numeric unit is declared by potential_stress_unit_to_pascal in the
    pressure evaluation; the energy and strain differentiation procedure
    remains associated with the supplied stress_method_id and source_id.
    """

    state_index: int
    md_step: int
    md_time: float
    stress: StressState

    def __post_init__(self) -> None:
        for name in ("state_index", "md_step"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer.")
        if isinstance(self.md_time, bool) or not isinstance(self.md_time, (int, float)):
            raise TypeError("md_time must be a real non-Boolean number.")
        if not isfinite(self.md_time) or self.md_time < 0.0:
            raise ValueError("md_time must be finite and nonnegative.")
        if not isinstance(self.stress, StressState):
            raise TypeError("stress must be a StressState.")
        if not self.stress.is_symmetric:
            raise ValueError("energy-derived stress must be symmetric.")


@dataclass(frozen=True, slots=True)
class FLiBePressureSample:
    """Kinetic, configurational, and total pressure tensors in pascal."""

    state_index: int
    md_step: int
    md_time: float
    cell_volume_m3: float
    kinetic_tensor_pa: Tensor3
    configurational_tensor_pa: Tensor3
    pressure_tensor_pa: Tensor3
    scalar_pressure_pa: float

    def __post_init__(self) -> None:
        for name in ("state_index", "md_step"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer.")
        if isinstance(self.md_time, bool) or not isinstance(self.md_time, (int, float)):
            raise TypeError("md_time must be a real non-Boolean number.")
        if not isfinite(self.md_time) or self.md_time < 0.0:
            raise ValueError("md_time must be finite and nonnegative.")
        _positive(self.cell_volume_m3, "cell_volume_m3")
        for name in ("kinetic_tensor_pa", "configurational_tensor_pa", "pressure_tensor_pa"):
            _tensor(getattr(self, name), name)
        if not isinstance(self.scalar_pressure_pa, (int, float)) or isinstance(
            self.scalar_pressure_pa, bool
        ) or not isfinite(self.scalar_pressure_pa):
            raise ValueError("scalar_pressure_pa must be finite.")
        trace = fsum(self.pressure_tensor_pa[a][a] for a in range(3)) / 3.0
        if not isclose(trace, self.scalar_pressure_pa, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("scalar pressure must equal one-third tensor trace.")


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryPressure:
    """Sample-aligned MD pressure results with explicit frame and provenance."""

    density_trace: FLiBeTrajectoryDensity
    velocity_frame: FLiBeVelocityFrame
    time_unit_to_second: float
    potential_stress_unit_to_pascal: float
    stress_method_id: str
    source_id: str
    provenance: ParameterProvenance
    samples: tuple[FLiBePressureSample, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.density_trace, FLiBeTrajectoryDensity):
            raise TypeError("density_trace must be a FLiBeTrajectoryDensity.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be a FLiBeVelocityFrame.")
        _positive(self.time_unit_to_second, "time_unit_to_second")
        _positive(self.potential_stress_unit_to_pascal, "potential_stress_unit_to_pascal")
        _identifier(self.stress_method_id, "stress_method_id")
        _identifier(self.source_id, "source_id")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be a ParameterProvenance.")
        if not isinstance(self.samples, tuple) or len(self.samples) != self.density_trace.sample_count:
            raise ValueError("pressure and density sample counts must agree.")
        for pressure, density in zip(self.samples, self.density_trace.samples, strict=True):
            if not isinstance(pressure, FLiBePressureSample):
                raise TypeError("samples must contain FLiBePressureSample values.")
            if (pressure.state_index, pressure.md_step, pressure.md_time) != (
                density.state_index, density.md_step, density.md_time
            ):
                raise ValueError("pressure and density sample identities must agree.")
            if not isclose(pressure.cell_volume_m3, density.cell_volume_m3, rel_tol=1e-12):
                raise ValueError("pressure and density cell volumes must agree.")

    @property
    def mean_pressure_pa(self) -> float:
        """Arithmetic mean of instantaneous signed scalar pressures."""

        return fsum(sample.scalar_pressure_pa for sample in self.samples) / len(self.samples)

    @property
    def mean_pressure_tensor_pa(self) -> Tensor3:
        """Arithmetic mean of the instantaneous Cartesian pressure tensors."""

        n = len(self.samples)
        return tuple(
            tuple(fsum(sample.pressure_tensor_pa[a][b] for sample in self.samples) / n
                  for b in range(3))
            for a in range(3)
        )  # type: ignore[return-value]

    def to_observed_pressure_coordinate(self) -> FLiBePressureCoordinate:
        """Bind computed nonnegative mean pressure to the existing state contract."""

        pressure = self.mean_pressure_pa
        if pressure < 0.0:
            raise ValueError("the thermodynamic pressure coordinate requires nonnegative pressure.")
        return FLiBePressureCoordinate(
            pressure_pa=pressure,
            role=FLiBePressureRole.OBSERVED,
            method_id=self.stress_method_id,
            source_id=self.source_id,
            provenance=self.provenance,
        )


def evaluate_flibe_trajectory_pressure(
    trajectory: MolecularDynamicsTrajectory,
    density_trace: FLiBeTrajectoryDensity,
    potential_stresses: tuple[FLiBePotentialStressSample, ...],
    *,
    time_unit_to_second: float,
    potential_stress_unit_to_pascal: float,
    velocity_frame: FLiBeVelocityFrame,
    stress_method_id: str,
    source_id: str,
    provenance: ParameterProvenance,
) -> FLiBeTrajectoryPressure:
    """Combine MD kinetic momentum flux with energy–strain stress.

    The Cartesian pressure tensor convention is

        Pi_ab = (1/V) sum_i m_i c_i,a c_i,b - sigma_potential,ab,

    with peculiar velocities c_i = v_i - v_COM for CENTER_OF_MASS and
    c_i = v_i for LABORATORY. Scalar pressure is Tr(Pi)/3.

    StressState contains the existing potential stress dE/dstrain/V,
    which is converted to pascal using potential_stress_unit_to_pascal.
    Atomic masses, velocities, volume and time use the conversion factors
    in density_trace and time_unit_to_second. Negative signed pressures
    remain in the output and retain their numeric values.
    """

    if not isinstance(trajectory, MolecularDynamicsTrajectory):
        raise TypeError("trajectory must be a MolecularDynamicsTrajectory.")
    if not isinstance(density_trace, FLiBeTrajectoryDensity):
        raise TypeError("density_trace must be a FLiBeTrajectoryDensity.")
    if not isinstance(potential_stresses, tuple):
        raise TypeError("potential_stresses must be a tuple.")
    if len(potential_stresses) != density_trace.sample_count:
        raise ValueError("stress and density sample counts must agree.")
    t_factor = _positive(time_unit_to_second, "time_unit_to_second")
    stress_factor = _positive(potential_stress_unit_to_pascal, "potential_stress_unit_to_pascal")
    if not isinstance(velocity_frame, FLiBeVelocityFrame):
        raise TypeError("velocity_frame must be a FLiBeVelocityFrame.")
    _identifier(stress_method_id, "stress_method_id")
    _identifier(source_id, "source_id")
    if not isinstance(provenance, ParameterProvenance):
        raise TypeError("provenance must be a ParameterProvenance.")
    if trajectory.atom_count != density_trace.atom_count:
        raise ValueError("trajectory and density atom counts must agree.")
    initial = trajectory.initial
    if not isclose(
        fsum(initial.masses) * density_trace.mass_unit_to_kg,
        density_trace.total_mass_kg, rel_tol=1e-12,
    ):
        raise ValueError("trajectory and density mass inventories must agree.")

    velocity_to_si = density_trace.coordinate_unit_to_meter / t_factor
    mass_factor = density_trace.mass_unit_to_kg
    states = trajectory.states
    results: list[FLiBePressureSample] = []

    for density, stress_sample in zip(density_trace.samples, potential_stresses, strict=True):
        if not isinstance(stress_sample, FLiBePotentialStressSample):
            raise TypeError("potential_stresses must contain FLiBePotentialStressSample values.")
        if density.state_index >= len(states):
            raise ValueError("density state index exceeds trajectory length.")
        state = states[density.state_index]
        identity = (density.state_index, state.step, state.time)
        if identity != (stress_sample.state_index, stress_sample.md_step, stress_sample.md_time):
            raise ValueError("stress and trajectory state identities must agree.")
        if (density.md_step, density.md_time) != (state.step, state.time):
            raise ValueError("density and trajectory state identities must agree.")
        if state.configuration.species != initial.configuration.species or state.masses != initial.masses:
            raise ValueError("ordered species and atomic masses must remain invariant.")
        if state.configuration.periodic != (True, True, True) or state.configuration.cell is None:
            raise ValueError("pressure requires a fully periodic three-dimensional cell.")
        volume = _cell_volume(state.configuration.cell) * density_trace.coordinate_unit_to_meter**3
        if not isfinite(volume) or volume <= 0.0 or not isclose(
            volume, density.cell_volume_m3, rel_tol=1e-12,
        ):
            raise ValueError("pressure and density cell volumes must agree.")
        if not isclose(density.density_kg_m3, density_trace.total_mass_kg / volume, rel_tol=1e-12):
            raise ValueError("density sample must match the sampled cell mass and volume.")

        mass_total = fsum(state.masses)
        v_com = tuple(
            fsum(mass * v[a] for mass, v in zip(state.masses, state.velocities, strict=True))
            / mass_total for a in range(3)
        ) if velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS else (0.0, 0.0, 0.0)
        tensor_kinetic = tuple(
            tuple(
                fsum(
                    mass * (velocity[a] - v_com[a]) * (velocity[b] - v_com[b])
                    for mass, velocity in zip(state.masses, state.velocities, strict=True)
                ) * mass_factor * velocity_to_si**2 / volume
                for b in range(3)
            ) for a in range(3)
        )
        tensor_conf = tuple(
            tuple(-stress_sample.stress.tensor[a][b] * stress_factor for b in range(3))
            for a in range(3)
        )
        tensor_total = tuple(
            tuple(tensor_kinetic[a][b] + tensor_conf[a][b] for b in range(3))
            for a in range(3)
        )
        scalar = fsum(tensor_total[a][a] for a in range(3)) / 3.0
        results.append(FLiBePressureSample(
            state_index=density.state_index,
            md_step=density.md_step,
            md_time=density.md_time,
            cell_volume_m3=volume,
            kinetic_tensor_pa=tensor_kinetic,
            configurational_tensor_pa=tensor_conf,
            pressure_tensor_pa=tensor_total,
            scalar_pressure_pa=scalar,
        ))

    return FLiBeTrajectoryPressure(
        density_trace=density_trace,
        velocity_frame=velocity_frame,
        time_unit_to_second=t_factor,
        potential_stress_unit_to_pascal=stress_factor,
        stress_method_id=stress_method_id,
        source_id=source_id,
        provenance=provenance,
        samples=tuple(results),
    )
