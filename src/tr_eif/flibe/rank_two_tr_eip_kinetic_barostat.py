"""Kinetic pressure closure for FLiBe rank-two TR-EIP MD barostat steps.

Combine post-mechanical velocities, masses and cell volume with the complete
rank-two strain stress. All SI conversion factors are explicit and the
velocity frame is recorded. Phase, ternary and mechanical states are read
from the completed coupled step and retained by the barostat interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
from tr_eif.md.state import MolecularDynamicsState

from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_barostat import (
    FLiBeRankTwoTREIPBarostatStep,
    apply_flibe_rank_two_tr_eip_barostat,
)
from .rank_two_tr_eip_stress import FLiBeRankTwoTREIPMDStressTrace
from .trajectory_pressure import FLiBeVelocityFrame, Tensor3
from .units import (
    FLiBeUnit,
    ParameterProvenance,
    PhysicalParameter,
    pressure_parameter,
)


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _volume(cell: Tensor3) -> float:
    a, b, c = cell
    volume = abs(fsum((
        a[0] * (b[1] * c[2] - b[2] * c[1]),
        a[1] * (b[2] * c[0] - b[0] * c[2]),
        a[2] * (b[0] * c[1] - b[1] * c[0]),
    )))
    if not isfinite(volume) or volume <= 0.0:
        raise ValueError("periodic cell volume must be finite and positive.")
    return volume


def _trace(tensor: Tensor3) -> float:
    return fsum(tensor[axis][axis] for axis in range(3)) / 3.0


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureClosure:
    """SI pressure tensor and hydrostatic reduction at the MD mechanical boundary."""

    stress_trace: FLiBeRankTwoTREIPMDStressTrace
    velocity_frame: FLiBeVelocityFrame
    mass_unit_to_kg: float
    coordinate_unit_to_meter: float
    time_unit_to_second: float
    potential_stress_unit_to_pascal: float
    cell_volume_m3: float
    kinetic_tensor_pa: Tensor3
    configurational_tensor_pa: Tensor3
    pressure_tensor_pa: Tensor3
    kinetic_pressure: PhysicalParameter
    total_pressure: PhysicalParameter

    def __post_init__(self) -> None:
        if not isinstance(self.stress_trace, FLiBeRankTwoTREIPMDStressTrace):
            raise TypeError("stress_trace must be a FLiBeRankTwoTREIPMDStressTrace.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
        for name in (
            "mass_unit_to_kg", "coordinate_unit_to_meter", "time_unit_to_second",
            "potential_stress_unit_to_pascal", "cell_volume_m3",
        ):
            _positive(getattr(self, name), name)
        for name in (
            "kinetic_tensor_pa", "configurational_tensor_pa", "pressure_tensor_pa"
        ):
            tensor = getattr(self, name)
            if not isinstance(tensor, tuple) or len(tensor) != 3:
                raise ValueError(f"{name} must be a 3x3 tensor.")
            if any(not isinstance(row, tuple) or len(row) != 3 or any(
                isinstance(value, bool) or not isinstance(value, (int, float))
                or not isfinite(value) for value in row
            ) for row in tensor):
                raise ValueError(f"{name} must have finite real components.")
        for name in ("kinetic_pressure", "total_pressure"):
            pressure = getattr(self, name)
            if not isinstance(pressure, PhysicalParameter):
                raise TypeError(f"{name} must be a PhysicalParameter.")
            if pressure.unit is not FLiBeUnit.PASCAL:
                raise ValueError(f"{name} must use pascal.")
        if self.kinetic_pressure.value < 0.0:
            raise ValueError("kinetic_pressure must be nonnegative.")
        if not isclose(_trace(self.kinetic_tensor_pa), self.kinetic_pressure.value,
                       rel_tol=1e-12, abs_tol=1e-10):
            raise ValueError("kinetic pressure must equal one-third of the kinetic trace.")
        if not isclose(_trace(self.pressure_tensor_pa), self.total_pressure.value,
                       rel_tol=1e-12, abs_tol=1e-10):
            raise ValueError("total pressure must equal one-third of the total trace.")
        for a in range(3):
            for b in range(3):
                combined = fsum((self.kinetic_tensor_pa[a][b],
                                 self.configurational_tensor_pa[a][b]))
                if not isclose(self.pressure_tensor_pa[a][b], combined,
                               rel_tol=1e-12, abs_tol=1e-10):
                    raise ValueError("pressure tensor must sum kinetic and configurational terms.")

    @property
    def potential_pressure_pa(self) -> float:
        """Configurational hydrostatic pressure in pascal."""
        return _trace(self.configurational_tensor_pa)


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPKineticBarostatStep:
    """Pressure reconstruction and the resulting coupled barostat step."""

    pressure: FLiBeRankTwoTREIPPressureClosure
    barostat: FLiBeRankTwoTREIPBarostatStep

    def __post_init__(self) -> None:
        if not isinstance(self.pressure, FLiBeRankTwoTREIPPressureClosure):
            raise TypeError("pressure must be a FLiBeRankTwoTREIPPressureClosure.")
        if not isinstance(self.barostat, FLiBeRankTwoTREIPBarostatStep):
            raise TypeError("barostat must be a FLiBeRankTwoTREIPBarostatStep.")
        if self.barostat.stress_trace != self.pressure.stress_trace:
            raise ValueError("barostat and kinetic pressure source traces must agree.")
        if self.barostat.kinetic_pressure != self.pressure.kinetic_pressure:
            raise ValueError("barostat and derived kinetic pressures must agree.")
        if not isclose(self.barostat.current_pressure_pa, self.pressure.total_pressure.value,
                       rel_tol=1e-12, abs_tol=1e-9):
            raise ValueError("barostat current pressure must match the kinetic closure.")


def evaluate_flibe_rank_two_tr_eip_pressure(
    stress_trace: FLiBeRankTwoTREIPMDStressTrace,
    *,
    mass_unit_to_kg: float,
    coordinate_unit_to_meter: float,
    time_unit_to_second: float,
    potential_stress_unit_to_pascal: float,
    velocity_frame: FLiBeVelocityFrame,
    provenance: ParameterProvenance,
    source: str | None = None,
) -> FLiBeRankTwoTREIPPressureClosure:
    """Calculate kinetic and complete configurational pressure from a completed MD state.

    The input velocity unit is coordinate_unit/time_unit. CENTER_OF_MASS
    removes the mass-weighted translational velocity, while LABORATORY uses
    the velocities as stored in the mechanical state. The energy-derived
    stress sigma=(1/V)dE/deformation contributes -sigma to the pressure tensor.
    The signed scalar total pressure is Tr(Pi)/3.
    """
    if not isinstance(stress_trace, FLiBeRankTwoTREIPMDStressTrace):
        raise TypeError("stress_trace must be a FLiBeRankTwoTREIPMDStressTrace.")
    mass_factor = _positive(mass_unit_to_kg, "mass_unit_to_kg")
    length_factor = _positive(coordinate_unit_to_meter, "coordinate_unit_to_meter")
    time_factor = _positive(time_unit_to_second, "time_unit_to_second")
    stress_factor = _positive(potential_stress_unit_to_pascal,
                              "potential_stress_unit_to_pascal")
    if not isinstance(velocity_frame, FLiBeVelocityFrame):
        raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
    if not isinstance(provenance, ParameterProvenance):
        raise TypeError("provenance must be a ParameterProvenance.")

    state: MolecularDynamicsState = stress_trace.coupled.current.md_state
    configuration = state.configuration
    if configuration.periodic != (True, True, True) or configuration.cell is None:
        raise ValueError("pressure requires a fully periodic three-dimensional cell.")
    if stress_trace.after_mechanics.evaluation.configuration.configuration != configuration:
        raise ValueError("mechanical stress and kinetic state geometries must agree.")
    if (stress_trace.after_mechanics.evaluation.execution
            != stress_trace.coupled.current.ternary_execution):
        raise ValueError("stress and mechanical retained execution must agree.")

    volume_m3 = _volume(configuration.cell) * length_factor**3
    if not isfinite(volume_m3) or volume_m3 <= 0.0:
        raise ValueError("SI cell volume must be finite and positive.")
    mass_total = fsum(state.masses)
    center = tuple(
        fsum(mass * velocity[a] for mass, velocity in zip(
            state.masses, state.velocities, strict=True,
        )) / mass_total for a in range(3)
    ) if velocity_frame is FLiBeVelocityFrame.CENTER_OF_MASS else (0.0, 0.0, 0.0)
    velocity_factor = length_factor / time_factor
    kinetic: Tensor3 = tuple(
        tuple(
            fsum(mass * (velocity[a] - center[a]) * (velocity[b] - center[b])
                 for mass, velocity in zip(state.masses, state.velocities, strict=True))
            * mass_factor * velocity_factor**2 / volume_m3
            for b in range(3)
        ) for a in range(3)
    )  # type: ignore[assignment]
    sigma = stress_trace.after_mechanics.stress.total_stress.tensor
    configurational: Tensor3 = tuple(
        tuple(-sigma[a][b] * stress_factor for b in range(3))
        for a in range(3)
    )  # type: ignore[assignment]
    total: Tensor3 = tuple(
        tuple(fsum((kinetic[a][b], configurational[a][b])) for b in range(3))
        for a in range(3)
    )  # type: ignore[assignment]
    kinetic_scalar = _trace(kinetic)
    total_scalar = _trace(total)
    if not isfinite(kinetic_scalar) or not isfinite(total_scalar):
        raise ValueError("computed pressure must be finite.")
    return FLiBeRankTwoTREIPPressureClosure(
        stress_trace=stress_trace,
        velocity_frame=velocity_frame,
        mass_unit_to_kg=mass_factor,
        coordinate_unit_to_meter=length_factor,
        time_unit_to_second=time_factor,
        potential_stress_unit_to_pascal=stress_factor,
        cell_volume_m3=volume_m3,
        kinetic_tensor_pa=kinetic,
        configurational_tensor_pa=configurational,
        pressure_tensor_pa=total,
        kinetic_pressure=pressure_parameter(kinetic_scalar, provenance, source=source),
        total_pressure=pressure_parameter(total_scalar, provenance, source=source),
    )


def apply_flibe_rank_two_tr_eip_kinetic_barostat(
    stress_trace: FLiBeRankTwoTREIPMDStressTrace,
    model: FLiBeRankTwoTREIPModel,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    *,
    cutoff: float,
    target_pressure: PhysicalParameter,
    mass_unit_to_kg: float,
    coordinate_unit_to_meter: float,
    time_unit_to_second: float,
    potential_stress_unit_to_pascal: float,
    velocity_frame: FLiBeVelocityFrame,
    compressibility_per_pascal: float,
    coupling_time: float,
    provenance: ParameterProvenance,
    source: str | None = None,
) -> FLiBeRankTwoTREIPKineticBarostatStep:
    """Derive kinetic pressure from the MD state, then apply the strain barostat."""
    pressure = evaluate_flibe_rank_two_tr_eip_pressure(
        stress_trace,
        mass_unit_to_kg=mass_unit_to_kg,
        coordinate_unit_to_meter=coordinate_unit_to_meter,
        time_unit_to_second=time_unit_to_second,
        potential_stress_unit_to_pascal=potential_stress_unit_to_pascal,
        velocity_frame=velocity_frame,
        provenance=provenance,
        source=source,
    )
    barostat = apply_flibe_rank_two_tr_eip_barostat(
        stress_trace, model, stress_evaluator,
        cutoff=cutoff,
        target_pressure=target_pressure,
        kinetic_pressure=pressure.kinetic_pressure,
        potential_stress_unit_to_pascal=potential_stress_unit_to_pascal,
        compressibility_per_pascal=compressibility_per_pascal,
        coupling_time=coupling_time,
    )
    return FLiBeRankTwoTREIPKineticBarostatStep(pressure=pressure, barostat=barostat)
