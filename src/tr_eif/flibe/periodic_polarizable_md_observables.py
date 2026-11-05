"""State-aligned density, temperature, and pressure for periodic polarizable FLiBe MD.

A selected NVE trajectory is evaluated without changing its mechanical states.
Mass density uses each periodic cell volume. Potential strain stress is evaluated
at the identical saved configuration, including relaxed fluoride dipoles. The
pressure tensor combines the kinetic momentum flux in the declared velocity
frame with minus the energy-derived potential stress:

    P_ab = (1/V) sum_i m_i c_ia c_ib - (1/V) dE/d(epsilon_ab).

The homogeneous-strain derivative follows the existing symmetric shear
convention. The same velocity frame defines kinetic temperature and pressure.
Potential stress is converted from hartree/bohr**3 to pascal using the MD
run's explicitly declared SI factors. Signed pressure values are retained.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite

from tr_eif.energy import CellStrainDifferentiation

from .configuration import FLiBeConfiguration
from .periodic_polarizable import FLiBePeriodicPolarizableModel
from .periodic_polarizable_md import FLiBePeriodicMDRun
from .periodic_polarizable_stress import (
    FLiBePeriodicPolarizableStressResult,
    evaluate_flibe_periodic_polarizable_stress,
)
from .trajectory_density import (
    FLiBeTrajectoryDensity,
    evaluate_flibe_trajectory_density,
)
from .trajectory_frame_thermodynamics import (
    FLiBeFrameThermodynamicState,
    evaluate_flibe_frame_thermodynamics,
)
from .trajectory_pressure import (
    FLiBePotentialStressSample,
    FLiBeTrajectoryPressure,
    FLiBeVelocityFrame,
    evaluate_flibe_trajectory_pressure,
)
from .units import ParameterProvenance


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


@dataclass(frozen=True, slots=True)
class FLiBePeriodicMDObservables:
    """Aligned MD, density, relaxed strain stress, and frame thermal records."""

    md_run: FLiBePeriodicMDRun
    density_trace: FLiBeTrajectoryDensity
    stress_results: tuple[FLiBePeriodicPolarizableStressResult, ...]
    pressure_trace: FLiBeTrajectoryPressure
    frame_thermodynamics: FLiBeFrameThermodynamicState
    differentiation: CellStrainDifferentiation
    stress_method_id: str
    source_id: str
    provenance: ParameterProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.md_run, FLiBePeriodicMDRun):
            raise TypeError("md_run must be FLiBePeriodicMDRun.")
        if not isinstance(self.density_trace, FLiBeTrajectoryDensity):
            raise TypeError("density_trace must be FLiBeTrajectoryDensity.")
        if not isinstance(self.pressure_trace, FLiBeTrajectoryPressure):
            raise TypeError("pressure_trace must be FLiBeTrajectoryPressure.")
        if not isinstance(self.frame_thermodynamics, FLiBeFrameThermodynamicState):
            raise TypeError("frame_thermodynamics must be FLiBeFrameThermodynamicState.")
        if not isinstance(self.differentiation, CellStrainDifferentiation):
            raise TypeError("differentiation must be CellStrainDifferentiation.")
        _identifier(self.stress_method_id, "stress_method_id")
        _identifier(self.source_id, "source_id")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        if self.density_trace.model_id != self.md_run.model_id:
            raise ValueError("density model identity must match the MD model.")
        if self.density_trace.provenance != self.provenance:
            raise ValueError("density and observables provenance must agree.")
        if self.pressure_trace.density_trace != self.density_trace:
            raise ValueError("pressure must reference the selected density trace.")
        if self.frame_thermodynamics.pressure_trace != self.pressure_trace:
            raise ValueError("thermal samples must reference the selected pressure trace.")
        if self.pressure_trace.velocity_frame is not self.frame_thermodynamics.velocity_frame:
            raise ValueError("thermal and pressure velocity frames must agree.")
        if self.pressure_trace.time_unit_to_second != self.md_run.units.time_unit_to_second:
            raise ValueError("pressure time units must match the MD run.")
        if (
            self.density_trace.mass_unit_to_kg != self.md_run.units.mass_unit_to_kg
            or self.density_trace.coordinate_unit_to_meter != self.md_run.units.coordinate_unit_to_meter
        ):
            raise ValueError("density SI units must match the MD run.")
        if (
            self.pressure_trace.provenance != self.provenance
            or self.pressure_trace.stress_method_id != self.stress_method_id
            or self.pressure_trace.source_id != self.source_id
        ):
            raise ValueError("pressure provenance identifiers must match observables.")
        if (
            not isinstance(self.stress_results, tuple)
            or len(self.stress_results) != self.density_trace.sample_count
        ):
            raise ValueError("relaxed stress count must match selected MD samples.")
        states = self.md_run.trajectory.states
        for sampled, stress in zip(self.density_trace.samples, self.stress_results, strict=True):
            if not isinstance(stress, FLiBePeriodicPolarizableStressResult):
                raise TypeError("stress_results must contain FLiBePeriodicPolarizableStressResult.")
            if stress.differentiation != self.differentiation:
                raise ValueError("all stress samples must use the declared differentiation.")
            if stress.configuration.configuration != states[sampled.state_index].configuration:
                raise ValueError("relaxed stress must use the selected MD configuration.")
            if stress.reference != self.md_run.evaluations[sampled.state_index]:
                raise ValueError("stress reference energy must match the saved MD potential.")
            if stress.source_file_sha256 != self.md_run.source_file_sha256:
                raise ValueError("stress source fingerprint must match the MD run.")
        expected_unit = self.md_run.units.hartree_to_joule / self.md_run.units.bohr_to_meter**3
        if not isfinite(expected_unit) or not isclose(
            self.pressure_trace.potential_stress_unit_to_pascal, expected_unit,
            rel_tol=1e-12, abs_tol=0.0,
        ):
            raise ValueError("potential stress SI conversion must match the MD units.")
        for sample, stress in zip(self.pressure_trace.samples, self.stress_results, strict=True):
            for a in range(3):
                for b in range(3):
                    expected = -stress.total_stress.tensor[a][b] * expected_unit
                    if not isclose(sample.configurational_tensor_pa[a][b], expected,
                                   rel_tol=1e-12, abs_tol=1e-7):
                        raise ValueError("configurational pressure must equal minus relaxed strain stress.")

    @property
    def mean_density_kg_m3(self) -> float:
        """Arithmetic mean of the selected instantaneous cell densities."""
        return self.density_trace.mean_density_kg_m3

    @property
    def mean_kinetic_temperature_k(self) -> float:
        """Selected-frame mean kinetic temperature in kelvin."""
        return self.frame_thermodynamics.mean_kinetic_temperature_k

    @property
    def signed_mean_pressure_pa(self) -> float:
        """Signed mean of full instantaneous pressure, in pascal."""
        return self.pressure_trace.mean_pressure_pa

    @property
    def source_file_sha256(self) -> str:
        """Fingerprint of the interatomic coefficients used by the MD run."""
        return self.md_run.source_file_sha256


def evaluate_flibe_periodic_md_observables(
    md_run: FLiBePeriodicMDRun,
    model: FLiBePeriodicPolarizableModel,
    differentiation: CellStrainDifferentiation,
    *,
    trajectory_id: str,
    velocity_frame: FLiBeVelocityFrame,
    degrees_of_freedom: int,
    physical_state_id: str,
    physical_state_method_id: str,
    stress_method_id: str,
    source_id: str,
    provenance: ParameterProvenance,
    first_state_index: int = 0,
    stride: int = 1,
) -> FLiBePeriodicMDObservables:
    """Evaluate aligned density, stress, pressure, and temperature observations.

    Stress is recalculated by symmetric homogeneous strain and stationary
    dipole relaxation at every selected frame. Physical-state identification
    is an explicit caller declaration. Pressure retains its signed value;
    the existing state-coordinate conversion applies its own pressure-domain
    contract only when a source comparison is subsequently requested.
    """
    if not isinstance(md_run, FLiBePeriodicMDRun):
        raise TypeError("md_run must be FLiBePeriodicMDRun.")
    if not isinstance(model, FLiBePeriodicPolarizableModel):
        raise TypeError("model must be FLiBePeriodicPolarizableModel.")
    if not isinstance(differentiation, CellStrainDifferentiation):
        raise TypeError("differentiation must be CellStrainDifferentiation.")
    if not isinstance(velocity_frame, FLiBeVelocityFrame):
        raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
    if not isinstance(provenance, ParameterProvenance):
        raise TypeError("provenance must be ParameterProvenance.")
    for name, value in (
        ("trajectory_id", trajectory_id),
        ("physical_state_id", physical_state_id),
        ("physical_state_method_id", physical_state_method_id),
        ("stress_method_id", stress_method_id),
        ("source_id", source_id),
    ):
        _identifier(value, name)
    if model.model_id != md_run.model_id:
        raise ValueError("MD run and observable model identifiers must agree.")
    md_run.units.check_model(model)
    if model.fixed_charge_model.short_range_model.parameters.source_file_sha256 != md_run.source_file_sha256:
        raise ValueError("model source fingerprint must match the MD run.")
    density = evaluate_flibe_trajectory_density(
        md_run.trajectory,
        md_run.mass_parameters,
        model_id=md_run.model_id,
        trajectory_id=trajectory_id,
        provenance=provenance,
        mass_unit_to_kg=md_run.units.mass_unit_to_kg,
        coordinate_unit_to_meter=md_run.units.coordinate_unit_to_meter,
        first_state_index=first_state_index,
        stride=stride,
    )
    stress_results = tuple(
        evaluate_flibe_periodic_polarizable_stress(
            model,
            FLiBeConfiguration(md_run.trajectory.states[sample.state_index].configuration),
            differentiation,
        )
        for sample in density.samples
    )
    stress_samples = tuple(
        FLiBePotentialStressSample(
            state_index=sample.state_index,
            md_step=sample.md_step,
            md_time=sample.md_time,
            stress=stress.total_stress,
        )
        for sample, stress in zip(density.samples, stress_results, strict=True)
    )
    stress_factor = md_run.units.hartree_to_joule / md_run.units.bohr_to_meter**3
    if not isfinite(stress_factor) or stress_factor <= 0.0:
        raise ValueError("potential stress conversion must be finite and positive.")
    pressure = evaluate_flibe_trajectory_pressure(
        md_run.trajectory,
        density,
        stress_samples,
        time_unit_to_second=md_run.units.time_unit_to_second,
        potential_stress_unit_to_pascal=stress_factor,
        velocity_frame=velocity_frame,
        stress_method_id=stress_method_id,
        source_id=source_id,
        provenance=provenance,
    )
    frame = evaluate_flibe_frame_thermodynamics(
        md_run.trajectory,
        pressure,
        degrees_of_freedom=degrees_of_freedom,
        physical_state_id=physical_state_id,
        physical_state_method_id=physical_state_method_id,
    )
    return FLiBePeriodicMDObservables(
        md_run=md_run,
        density_trace=density,
        stress_results=stress_results,
        pressure_trace=pressure,
        frame_thermodynamics=frame,
        differentiation=differentiation,
        stress_method_id=stress_method_id,
        source_id=source_id,
        provenance=provenance,
    )
