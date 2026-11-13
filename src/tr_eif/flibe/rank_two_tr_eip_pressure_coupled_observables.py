"""Frame-aligned observables for FLiBe rank-two pressure-coupled MD.

Evaluate post-barostat density, kinetic temperature, signed pressure and the
reference/rank-two energy channels. Each interval separately registers the
fixed-geometry phase/ternary potential-energy change, mechanical total-energy
change and affine-cell potential-energy change. The pressure that drives the
barostat remains distinct from the pressure measured on its scaled output.

Energy, length, mass, time and stress units are explicitly reconciled with SI.
The supplied thermodynamic coordinates, resonance clocks, retained ternary
states and pending destinations remain associated with their source records.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.md.state import MolecularDynamicsState
from tr_eif.ternary import TernaryState

from .rank_two_tr_eip_pressure_coupled_trajectory import (
    FLiBeRankTwoTREIPPressureCoupledTrajectory,
)
from .trajectory_pressure import FLiBeVelocityFrame
from .trajectory_state_correspondence import BOLTZMANN_CONSTANT_J_PER_K


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return result


def _finite(value: float, name: str, *, nonnegative: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or (nonnegative and result < 0.0):
        raise ValueError(f"{name} must be finite and satisfy its sign constraint.")
    return result


def _kinetic_energy_j(
    state: MolecularDynamicsState,
    frame: FLiBeVelocityFrame,
    mass_unit_to_kg: float,
    coordinate_unit_to_meter: float,
    time_unit_to_second: float,
) -> float:
    """Mass-weighted kinetic energy using the declared velocity reference frame."""
    masses = state.masses
    velocities = state.velocities
    total_mass = fsum(masses)
    origin = (
        tuple(
            fsum(mass * velocity[axis] for mass, velocity in zip(
                masses, velocities, strict=True
            )) / total_mass
            for axis in range(3)
        )
        if frame is FLiBeVelocityFrame.CENTER_OF_MASS else (0.0, 0.0, 0.0)
    )
    squared = fsum(
        mass * fsum((velocity[axis] - origin[axis]) ** 2 for axis in range(3))
        for mass, velocity in zip(masses, velocities, strict=True)
    )
    energy = 0.5 * squared * mass_unit_to_kg * (
        coordinate_unit_to_meter / time_unit_to_second
    ) ** 2
    return _finite(energy, "kinetic_energy_j", nonnegative=True)


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureCoupledSample:
    """One post-barostat frame and three separately evaluated energy changes."""

    interval_index: int
    md_step: int
    md_time_s: float
    resonance_time: float
    resonance_step_count: int
    ternary_event_count: int
    retained_states: tuple[TernaryState, ...]
    pending_target_count: int
    volume_m3: float
    density_kg_m3: float
    kinetic_energy_j: float
    kinetic_temperature_k: float
    kinetic_pressure_pa: float
    configurational_pressure_pa: float
    total_pressure_pa: float
    target_pressure_residual_pa: float
    reference_energy_j: float
    rank_two_energy_j: float
    event_potential_energy_change_j: float
    mechanical_total_energy_change_j: float
    barostat_potential_energy_change_j: float
    net_total_energy_change_j: float

    def __post_init__(self) -> None:
        for name in (
            "interval_index", "md_step", "resonance_step_count",
            "ternary_event_count", "pending_target_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer.")
            if value < 0:
                raise ValueError(f"{name} must be nonnegative.")
        if not isinstance(self.retained_states, tuple) or not self.retained_states:
            raise ValueError("retained_states must be a nonempty tuple.")
        if any(not isinstance(state, TernaryState) for state in self.retained_states):
            raise TypeError("retained_states must contain TernaryState entries.")
        if self.pending_target_count > len(self.retained_states):
            raise ValueError("pending_target_count exceeds node count.")
        for name in ("md_time_s", "resonance_time", "kinetic_energy_j",
                     "kinetic_temperature_k", "kinetic_pressure_pa"):
            _finite(getattr(self, name), name, nonnegative=True)
        for name in ("volume_m3", "density_kg_m3"):
            _positive(getattr(self, name), name)
        for name in (
            "configurational_pressure_pa", "total_pressure_pa",
            "target_pressure_residual_pa", "reference_energy_j", "rank_two_energy_j",
            "event_potential_energy_change_j", "mechanical_total_energy_change_j",
            "barostat_potential_energy_change_j", "net_total_energy_change_j",
        ):
            _finite(getattr(self, name), name)
        if not isclose(
            self.total_pressure_pa,
            fsum((self.kinetic_pressure_pa, self.configurational_pressure_pa)),
            rel_tol=1e-12, abs_tol=1e-6,
        ):
            raise ValueError("post-barostat pressure components differ.")
        if not isclose(
            self.net_total_energy_change_j,
            fsum((self.event_potential_energy_change_j,
                  self.mechanical_total_energy_change_j,
                  self.barostat_potential_energy_change_j)),
            rel_tol=1e-10, abs_tol=1e-25,
        ):
            raise ValueError("energy-change decomposition differs.")

    @property
    def potential_energy_j(self) -> float:
        """Complete post-barostat conservative potential energy in joule."""
        return fsum((self.reference_energy_j, self.rank_two_energy_j))

    @property
    def total_energy_j(self) -> float:
        """Post-barostat kinetic plus conservative potential energy in joule."""
        return fsum((self.kinetic_energy_j, self.potential_energy_j))


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoTREIPPressureCoupledObservables:
    """State-aligned SI observables and interval-separated energy diagnostics."""

    trajectory: FLiBeRankTwoTREIPPressureCoupledTrajectory
    degrees_of_freedom: int
    energy_unit_to_joule: float
    samples: tuple[FLiBeRankTwoTREIPPressureCoupledSample, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.trajectory, FLiBeRankTwoTREIPPressureCoupledTrajectory):
            raise TypeError("trajectory must be FLiBeRankTwoTREIPPressureCoupledTrajectory.")
        if isinstance(self.degrees_of_freedom, bool) or not isinstance(
            self.degrees_of_freedom, int
        ) or not 1 <= self.degrees_of_freedom <= 3 * self.trajectory.initial.md_state.atom_count:
            raise ValueError("degrees_of_freedom must be within the atomic Cartesian domain.")
        _positive(self.energy_unit_to_joule, "energy_unit_to_joule")
        if not isinstance(self.samples, tuple) or len(self.samples) != self.trajectory.interval_count:
            raise ValueError("samples must align with every completed interval.")
        for index, (sample, step) in enumerate(zip(
            self.samples, self.trajectory.steps, strict=True
        )):
            if not isinstance(sample, FLiBeRankTwoTREIPPressureCoupledSample):
                raise TypeError("samples must contain FLiBeRankTwoTREIPPressureCoupledSample.")
            current = step.barostat.current
            pending_count = sum(
                node.pending_target is not None
                for node in current.ternary_execution.states
            )
            if (
                sample.interval_index != index
                or sample.md_step != current.md_state.step
                or sample.resonance_time != current.resonance_time
                or sample.resonance_step_count != current.resonance_step_count
                or sample.ternary_event_count != current.ternary_event_count
                or sample.retained_states != current.ternary_execution.retained_states
                or sample.pending_target_count != pending_count
            ):
                raise ValueError(f"samples[{index}] execution identities differ.")
            expected_time_s = current.md_state.time * step.pressure.time_unit_to_second
            if not isclose(sample.md_time_s, expected_time_s, rel_tol=1e-12, abs_tol=0.0):
                raise ValueError(f"samples[{index}] mechanical time differs.")
            if not isclose(sample.kinetic_pressure_pa,
                           2.0 * sample.kinetic_energy_j / (3.0 * sample.volume_m3),
                           rel_tol=1e-12, abs_tol=1e-6):
                raise ValueError(f"samples[{index}] kinetic pressure differs.")
            if not isclose(sample.kinetic_temperature_k,
                           2.0 * sample.kinetic_energy_j /
                           (self.degrees_of_freedom * BOLTZMANN_CONSTANT_J_PER_K),
                           rel_tol=1e-12, abs_tol=1e-8):
                raise ValueError(f"samples[{index}] kinetic temperature differs.")
            if not isclose(sample.configurational_pressure_pa,
                           step.barostat.after_barostat_potential_pressure_pa,
                           rel_tol=1e-12, abs_tol=1e-6):
                raise ValueError(f"samples[{index}] stress pressure differs.")
            if not isclose(sample.potential_energy_j,
                           step.barostat.after_barostat.evaluation.energy.total_energy
                           * self.energy_unit_to_joule, rel_tol=1e-12, abs_tol=1e-30):
                raise ValueError(f"samples[{index}] complete potential energy differs.")
            if not isclose(sample.volume_m3, self.trajectory.cell_volumes_m3[index + 1],
                           rel_tol=1e-12):
                raise ValueError(f"samples[{index}] cell volume differs.")
            if not isclose(sample.density_kg_m3, self.trajectory.densities_kg_m3[index + 1],
                           rel_tol=1e-12):
                raise ValueError(f"samples[{index}] mass density differs.")
            if not isclose(sample.total_pressure_pa - self.trajectory.target_pressure.value,
                           sample.target_pressure_residual_pa, rel_tol=1e-12, abs_tol=1e-6):
                raise ValueError(f"samples[{index}] pressure residual differs.")

    @property
    def post_barostat_pressures_pa(self) -> tuple[float, ...]:
        """Instantaneous signed pressures on the updated cells."""
        return tuple(sample.total_pressure_pa for sample in self.samples)

    @property
    def kinetic_temperatures_k(self) -> tuple[float, ...]:
        return tuple(sample.kinetic_temperature_k for sample in self.samples)

    @property
    def total_energy_changes_j(self) -> tuple[float, ...]:
        return tuple(sample.net_total_energy_change_j for sample in self.samples)


def evaluate_flibe_rank_two_tr_eip_pressure_coupled_observables(
    trajectory: FLiBeRankTwoTREIPPressureCoupledTrajectory,
    *,
    energy_unit_to_joule: float,
    degrees_of_freedom: int,
) -> FLiBeRankTwoTREIPPressureCoupledObservables:
    """Evaluate each completed interval in SI with separated energy boundaries.

    The energy-to-SI and cell-length conversions must reproduce the declared
    cell-strain stress-to-Pa factor. The kinetic temperature uses an explicitly
    supplied mechanical degree-of-freedom count. The output registers the
    instantaneous signed pressure after scaling; the input pressure used by
    the barostat remains in each interval's original pressure-closure record.
    """
    if not isinstance(trajectory, FLiBeRankTwoTREIPPressureCoupledTrajectory):
        raise TypeError("trajectory must be FLiBeRankTwoTREIPPressureCoupledTrajectory.")
    energy_factor = _positive(energy_unit_to_joule, "energy_unit_to_joule")
    if isinstance(degrees_of_freedom, bool) or not isinstance(degrees_of_freedom, int):
        raise TypeError("degrees_of_freedom must be an integer.")
    if not 1 <= degrees_of_freedom <= 3 * trajectory.initial.md_state.atom_count:
        raise ValueError("degrees_of_freedom exceeds the Cartesian atomic domain.")

    samples: list[FLiBeRankTwoTREIPPressureCoupledSample] = []
    for index, step in enumerate(trajectory.steps):
        p = step.pressure
        b = step.barostat
        length_factor = p.coordinate_unit_to_meter
        expected_stress_factor = energy_factor / length_factor**3
        if not isfinite(expected_stress_factor) or not isclose(
            expected_stress_factor, p.potential_stress_unit_to_pascal,
            rel_tol=1e-11,
        ):
            raise ValueError("energy, length and potential-stress SI factors differ.")

        coupled = b.stress_trace.coupled
        before = coupled.coupled_step.previous.md_state
        after_mechanics = coupled.coupled_step.current.md_state
        after_barostat = b.current.md_state
        factors = (p.mass_unit_to_kg, p.coordinate_unit_to_meter, p.time_unit_to_second)
        energy_initial = _kinetic_energy_j(before, trajectory.velocity_frame, *factors)
        energy_final = _kinetic_energy_j(after_mechanics, trajectory.velocity_frame, *factors)
        energy_scaled = _kinetic_energy_j(after_barostat, trajectory.velocity_frame, *factors)
        if not isclose(energy_final, energy_scaled, rel_tol=1e-12, abs_tol=1e-30):
            raise ValueError("barostat changed kinetic energy under the fixed-velocity rule.")
        pressure_from_kinetics = 2.0 * energy_final / (3.0 * p.cell_volume_m3)
        if not isclose(pressure_from_kinetics, p.kinetic_pressure.value,
                       rel_tol=1e-10, abs_tol=1e-6):
            raise ValueError("kinetic pressure and post-mechanical velocities differ.")

        volume_after = p.cell_volume_m3 * b.volume_ratio
        if not isfinite(volume_after) or volume_after <= 0.0:
            raise ValueError("post-barostat SI cell volume must be finite and positive.")
        mass_kg = fsum(after_barostat.masses) * p.mass_unit_to_kg
        density_after = mass_kg / volume_after
        kinetic_pressure_after = 2.0 * energy_scaled / (3.0 * volume_after)
        potential_pressure_after = b.after_barostat_potential_pressure_pa
        pressure_after = fsum((kinetic_pressure_after, potential_pressure_after))
        temperature = 2.0 * energy_scaled / (
            degrees_of_freedom * BOLTZMANN_CONSTANT_J_PER_K
        )

        u_initial = coupled.before_events.energy.total_energy
        u_events = coupled.after_events.energy.total_energy
        u_mechanics = coupled.after_mechanics.energy.total_energy
        u_scaled = b.after_barostat.evaluation.energy.total_energy
        event_change = (u_events - u_initial) * energy_factor
        mechanical_change = fsum((
            (u_mechanics - u_events) * energy_factor,
            energy_final - energy_initial,
        ))
        scaling_change = (u_scaled - u_mechanics) * energy_factor
        net_change = fsum((
            (u_scaled - u_initial) * energy_factor,
            energy_scaled - energy_initial,
        ))
        current = b.current
        samples.append(FLiBeRankTwoTREIPPressureCoupledSample(
            interval_index=index,
            md_step=current.md_state.step,
            md_time_s=current.md_state.time * p.time_unit_to_second,
            resonance_time=current.resonance_time,
            resonance_step_count=current.resonance_step_count,
            ternary_event_count=current.ternary_event_count,
            retained_states=current.ternary_execution.retained_states,
            pending_target_count=sum(
                node.pending_target is not None
                for node in current.ternary_execution.states
            ),
            volume_m3=volume_after,
            density_kg_m3=density_after,
            kinetic_energy_j=energy_scaled,
            kinetic_temperature_k=temperature,
            kinetic_pressure_pa=kinetic_pressure_after,
            configurational_pressure_pa=potential_pressure_after,
            total_pressure_pa=pressure_after,
            target_pressure_residual_pa=pressure_after - trajectory.target_pressure.value,
            reference_energy_j=(
                b.after_barostat.evaluation.reference_energy.total_energy * energy_factor
            ),
            rank_two_energy_j=(
                b.after_barostat.evaluation.tensor_energy.total_energy * energy_factor
            ),
            event_potential_energy_change_j=event_change,
            mechanical_total_energy_change_j=mechanical_change,
            barostat_potential_energy_change_j=scaling_change,
            net_total_energy_change_j=net_change,
        ))
    return FLiBeRankTwoTREIPPressureCoupledObservables(
        trajectory=trajectory,
        degrees_of_freedom=degrees_of_freedom,
        energy_unit_to_joule=energy_factor,
        samples=tuple(samples),
    )
