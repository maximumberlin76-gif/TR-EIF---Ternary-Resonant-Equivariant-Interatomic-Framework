
"""Scheduled FLiBe rank-two TR-EIP pressure-coupled MD trajectories.

Each interval advances independently selected resonance and ternary events,
then one full-energy velocity-Verlet mechanical step. The resulting rank-two
cell-strain stress and mass-weighted kinetic pressure drive an isotropic
barostat. Every post-barostat configuration becomes the next interval's input.

The trajectory retains all pre-event, post-event, post-mechanical and
post-barostat energy/stress evidence, with independent mechanical, resonance
and ternary clocks and pending destinations. The supplied thermodynamic
coordinate is held fixed across this explicitly scheduled trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite

from tr_eif.energy.rank_two_model import RankTwoConservativeForceEvaluator
from tr_eif.energy.rank_two_stress import RankTwoConservativeStressEvaluator
from tr_eif.equivariant.rank_two import ScalarVectorTensorFeatures
from tr_eif.md.coupled_execution import CoupledMolecularDynamicsState
from tr_eif.resonance import PhaseDynamicsParameters
from tr_eif.ternary import TernaryExecutionGuard

from .coupled_rank_two_tr_eip_md import execute_flibe_rank_two_tr_eip_coupled_md_step
from .rank_two_tr_eip import FLiBeRankTwoTREIPModel
from .rank_two_tr_eip_kinetic_barostat import (
    FLiBeRankTwoTREIPKineticBarostatStep,
    apply_flibe_rank_two_tr_eip_kinetic_barostat,
)
from .rank_two_tr_eip_stress import evaluate_flibe_rank_two_tr_eip_md_stresses
from .ternary_interpretation import FLiBeTernaryInterpretation
from .thermodynamic_state import FLiBeThermodynamicState
from .trajectory_pressure import FLiBeVelocityFrame
from .units import FLiBeUnit, ParameterProvenance, PhysicalParameter


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureCoupledInterval:
    """One mechanical interval with independently selected event clocks."""

    mechanical_time_step: float
    phase_parameters: PhaseDynamicsParameters | None = None
    phase_time_step: float | None = None
    ternary_event: bool = False
    guards: tuple[TernaryExecutionGuard, ...] | None = None

    def __post_init__(self) -> None:
        _positive(self.mechanical_time_step, "mechanical_time_step")
        if self.phase_time_step is None:
            if self.phase_parameters is not None:
                raise ValueError("phase_parameters require phase_time_step.")
        else:
            _positive(self.phase_time_step, "phase_time_step")
            if not isinstance(self.phase_parameters, PhaseDynamicsParameters):
                raise TypeError("phase_parameters are required for a phase interval.")
        if not isinstance(self.ternary_event, bool):
            raise TypeError("ternary_event must be bool.")
        if self.guards is not None:
            if not isinstance(self.guards, tuple) or not all(
                isinstance(guard, TernaryExecutionGuard) for guard in self.guards
            ):
                raise TypeError("guards must be a tuple of TernaryExecutionGuard.")
            if not self.ternary_event:
                raise ValueError("guards require a scheduled ternary event.")


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureCoupledTrajectory:
    """Immutable pressure-coupled record with exact state-chain continuity."""

    initial: CoupledMolecularDynamicsState
    schedule: tuple[FLiBeRankTwoTREIPPressureCoupledInterval, ...]
    steps: tuple[FLiBeRankTwoTREIPKineticBarostatStep, ...]
    thermodynamic_state: FLiBeThermodynamicState
    target_pressure: PhysicalParameter
    velocity_frame: FLiBeVelocityFrame

    def __post_init__(self) -> None:
        if not isinstance(self.initial, CoupledMolecularDynamicsState):
            raise TypeError("initial must be CoupledMolecularDynamicsState.")
        if not isinstance(self.thermodynamic_state, FLiBeThermodynamicState):
            raise TypeError("thermodynamic_state must be FLiBeThermodynamicState.")
        if not isinstance(self.target_pressure, PhysicalParameter):
            raise TypeError("target_pressure must be PhysicalParameter.")
        if self.target_pressure.unit is not FLiBeUnit.PASCAL:
            raise ValueError("target_pressure must use Pa.")
        if not isinstance(self.velocity_frame, FLiBeVelocityFrame):
            raise TypeError("velocity_frame must be FLiBeVelocityFrame.")
        if not isinstance(self.schedule, tuple) or not isinstance(self.steps, tuple):
            raise TypeError("schedule and steps must be tuples.")
        if not self.schedule or len(self.schedule) != len(self.steps):
            raise ValueError("schedule and steps must have equal positive length.")

        previous = self.initial
        first_units = None
        for index, (interval, step) in enumerate(zip(self.schedule, self.steps, strict=True)):
            if not isinstance(interval, FLiBeRankTwoTREIPPressureCoupledInterval):
                raise TypeError(f"schedule[{index}] must be FLiBeRankTwoTREIPPressureCoupledInterval.")
            if not isinstance(step, FLiBeRankTwoTREIPKineticBarostatStep):
                raise TypeError(f"steps[{index}] must be FLiBeRankTwoTREIPKineticBarostatStep.")
            record = step.barostat
            coupled = record.stress_trace.coupled
            if coupled.coupled_step.previous != previous:
                raise ValueError(f"steps[{index}] does not follow the previous post-barostat state.")
            if coupled.thermodynamic_state != self.thermodynamic_state:
                raise ValueError(f"steps[{index}] thermodynamic coordinates differ.")
            if record.target_pressure != self.target_pressure:
                raise ValueError(f"steps[{index}] target pressure differs.")
            if step.pressure.velocity_frame is not self.velocity_frame:
                raise ValueError(f"steps[{index}] velocity frame differs.")
            if not isclose(record.mechanical_time_step, interval.mechanical_time_step,
                           rel_tol=1e-12, abs_tol=1e-15):
                raise ValueError(f"steps[{index}] mechanical time interval differs.")
            current = record.current
            if (current.md_state.step != previous.md_state.step + 1
                    or current.md_state.time <= previous.md_state.time):
                raise ValueError(f"steps[{index}] mechanical clock is discontinuous.")
            phase_increment = int(interval.phase_time_step is not None)
            if (current.resonance_step_count != previous.resonance_step_count + phase_increment
                    or current.resonance_time != previous.resonance_time
                    + (interval.phase_time_step or 0.0)):
                raise ValueError(f"steps[{index}] resonance clock differs from schedule.")
            if current.ternary_event_count != previous.ternary_event_count + int(interval.ternary_event):
                raise ValueError(f"steps[{index}] ternary event clock differs from schedule.")
            if (current.md_state.configuration.species != self.initial.md_state.configuration.species
                    or current.md_state.masses != self.initial.md_state.masses):
                raise ValueError(f"steps[{index}] species or mass inventory changed.")
            if (record.after_barostat.evaluation.configuration.configuration
                    != current.md_state.configuration):
                raise ValueError(f"steps[{index}] post-barostat energy geometry differs.")
            if (record.after_barostat.evaluation.execution != current.ternary_execution
                    or record.after_barostat.evaluation.resonance.resonance_state
                    != current.resonance_state):
                raise ValueError(f"steps[{index}] post-barostat state differs.")
            current_units = (
                step.pressure.mass_unit_to_kg,
                step.pressure.coordinate_unit_to_meter,
                step.pressure.time_unit_to_second,
                step.pressure.potential_stress_unit_to_pascal,
            )
            if first_units is None:
                first_units = current_units
            elif current_units != first_units:
                raise ValueError(f"steps[{index}] SI conversion factors changed.")
            previous = current

    @property
    def interval_count(self) -> int:
        """Number of completed mechanical and pressure-coupling intervals."""
        return len(self.steps)

    @property
    def final(self) -> CoupledMolecularDynamicsState:
        """Committed state after the final barostat boundary."""
        return self.steps[-1].barostat.current

    @property
    def states(self) -> tuple[CoupledMolecularDynamicsState, ...]:
        """Initial state followed by each pressure-scaled end state."""
        return (self.initial, *(step.barostat.current for step in self.steps))

    @property
    def prebarostat_pressures_pa(self) -> tuple[float, ...]:
        """Signed mechanical-boundary pressures that drove the barostat."""
        return tuple(step.pressure.total_pressure.value for step in self.steps)

    @property
    def volume_ratios(self) -> tuple[float, ...]:
        """Affine volume ratios applied at successive barostat boundaries."""
        return tuple(step.barostat.volume_ratio for step in self.steps)

    @property
    def cell_volumes_m3(self) -> tuple[float, ...]:
        """Initial volume and each pressure-scaled volume in SI units."""
        volumes = [self.steps[0].pressure.cell_volume_m3]
        volumes.extend(
            step.pressure.cell_volume_m3 * step.barostat.volume_ratio
            for step in self.steps
        )
        return tuple(volumes)

    @property
    def densities_kg_m3(self) -> tuple[float, ...]:
        """Mass-conserving densities for the initial and scaled states."""
        mass_kg = sum(self.initial.md_state.masses) * self.steps[0].pressure.mass_unit_to_kg
        return tuple(mass_kg / volume for volume in self.cell_volumes_m3)


def run_flibe_rank_two_tr_eip_pressure_coupled_trajectory(
    initial: CoupledMolecularDynamicsState,
    *,
    schedule: tuple[FLiBeRankTwoTREIPPressureCoupledInterval, ...],
    model: FLiBeRankTwoTREIPModel,
    force_evaluator: RankTwoConservativeForceEvaluator,
    stress_evaluator: RankTwoConservativeStressEvaluator,
    features: ScalarVectorTensorFeatures,
    thermodynamic_state: FLiBeThermodynamicState,
    interpretation: FLiBeTernaryInterpretation,
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
) -> FLiBeRankTwoTREIPPressureCoupledTrajectory:
    """Run deterministic multirate rank-two MD with an isotropic pressure boundary.

    Each interval uses one mechanical step, any scheduled phase/ternary events,
    the complete rank-two strain stress and a kinetic pressure calculated from
    the resulting velocities. The pressure update rescales the cell and atomic
    positions before the next interval. The physical thermodynamic coordinate
    is supplied independently and remains unchanged during this run.
    """
    if not isinstance(initial, CoupledMolecularDynamicsState):
        raise TypeError("initial must be CoupledMolecularDynamicsState.")
    if not isinstance(schedule, tuple) or not schedule:
        raise ValueError("schedule must be a nonempty tuple.")
    if not all(isinstance(item, FLiBeRankTwoTREIPPressureCoupledInterval) for item in schedule):
        raise TypeError("schedule must contain FLiBeRankTwoTREIPPressureCoupledInterval.")
    if not isinstance(target_pressure, PhysicalParameter):
        raise TypeError("target_pressure must be PhysicalParameter.")
    if target_pressure.unit is not FLiBeUnit.PASCAL:
        raise ValueError("target_pressure must be expressed in Pa.")

    current = initial
    completed: list[FLiBeRankTwoTREIPKineticBarostatStep] = []
    for interval in schedule:
        coupled = execute_flibe_rank_two_tr_eip_coupled_md_step(
            current,
            model=model,
            force_evaluator=force_evaluator,
            features=features,
            thermodynamic_state=thermodynamic_state,
            interpretation=interpretation,
            cutoff=cutoff,
            phase_parameters=interval.phase_parameters,
            phase_time_step=interval.phase_time_step,
            ternary_event=interval.ternary_event,
            guards=interval.guards,
            mechanical_time_step=interval.mechanical_time_step,
        )
        trace = evaluate_flibe_rank_two_tr_eip_md_stresses(
            coupled, model, stress_evaluator,
        )
        pressure_step = apply_flibe_rank_two_tr_eip_kinetic_barostat(
            trace, model, stress_evaluator,
            cutoff=cutoff,
            target_pressure=target_pressure,
            mass_unit_to_kg=mass_unit_to_kg,
            coordinate_unit_to_meter=coordinate_unit_to_meter,
            time_unit_to_second=time_unit_to_second,
            potential_stress_unit_to_pascal=potential_stress_unit_to_pascal,
            velocity_frame=velocity_frame,
            compressibility_per_pascal=compressibility_per_pascal,
            coupling_time=coupling_time,
            provenance=provenance,
            source=source,
        )
        completed.append(pressure_step)
        current = pressure_step.barostat.current

    return FLiBeRankTwoTREIPPressureCoupledTrajectory(
        initial=initial,
        schedule=schedule,
        steps=tuple(completed),
        thermodynamic_state=thermodynamic_state,
        target_pressure=target_pressure,
        velocity_frame=velocity_frame,
    )
