"""Velocity-Verlet dynamics for the periodic polarizable FLiBe potential.

Mechanical states use the existing TR-EIF MolecularDynamicsState and
MolecularDynamicsTrajectory contracts. At each force evaluation, the
periodic potential independently solves its stationary fluoride dipoles.

The unit conversion from potential forces to mechanical acceleration is

    a_code = (F_hartree/code_length / m_code)
             * (hartree_to_joule * time_unit_to_second**2)
             / (mass_unit_to_kg * coordinate_unit_to_meter**2).

The trajectory stores the complete energy and force observations for every
mechanical state. A geometric cutoff graph is retained for trajectory
interoperability; periodic electrostatics and polarization are evaluated
by the potential's own lattice operators. Resonance and ternary events
retain their separately scheduled execution contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from tr_eif.configuration import AtomicConfiguration
from tr_eif.energy import ForceState
from tr_eif.graph import build_cutoff_graph
from tr_eif.md.dynamics import accelerations_from_forces
from tr_eif.md.execution import MolecularDynamicsStepResult
from tr_eif.md.integrator import velocity_verlet_positions, velocity_verlet_velocities
from tr_eif.md.state import MolecularDynamicsState
from tr_eif.md.trajectory import MolecularDynamicsTrajectory

from .configuration import FLiBeConfiguration
from .mass import FLiBeMassParameters, configuration_masses
from .periodic_polarizable import FLiBePeriodicPolarizableModel, FLiBePeriodicPolarizableResult
from .units import ParameterProvenance


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    result = float(value)
    if not isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return result


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or not value.strip() or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


@dataclass(frozen=True, slots=True)
class FLiBePeriodicMDUnits:
    """Explicit conversion of MD mass, length, time and potential units."""

    mass_unit_to_kg: float
    coordinate_unit_to_meter: float
    time_unit_to_second: float
    bohr_to_meter: float
    hartree_to_joule: float
    provenance: ParameterProvenance
    source_id: str

    def __post_init__(self) -> None:
        for name in (
            "mass_unit_to_kg",
            "coordinate_unit_to_meter",
            "time_unit_to_second",
            "bohr_to_meter",
            "hartree_to_joule",
        ):
            object.__setattr__(self, name, _positive(getattr(self, name), name))
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be ParameterProvenance.")
        _identifier(self.source_id, "source_id")
        _positive(self.acceleration_factor, "acceleration_factor")
        _positive(self.kinetic_energy_factor, "kinetic_energy_factor")

    @property
    def acceleration_factor(self) -> float:
        """Convert potential force divided by MD mass to code acceleration."""
        return (
            self.hartree_to_joule * self.time_unit_to_second**2
            / (self.mass_unit_to_kg * self.coordinate_unit_to_meter**2)
        )

    @property
    def kinetic_energy_factor(self) -> float:
        """Convert one MD mass-velocity-squared unit to hartree."""
        return (
            self.mass_unit_to_kg
            * (self.coordinate_unit_to_meter / self.time_unit_to_second)**2
            / self.hartree_to_joule
        )

    def check_model(self, model: FLiBePeriodicPolarizableModel) -> None:
        """Require agreement between bohr and SI coordinate conversion."""
        if not isinstance(model, FLiBePeriodicPolarizableModel):
            raise TypeError("model must be FLiBePeriodicPolarizableModel.")
        declared = model.fixed_charge_model.ewald_model.parameters.coordinate_unit_to_bohr
        if not isclose(
            declared * self.bohr_to_meter,
            self.coordinate_unit_to_meter,
            rel_tol=1.0e-12,
            abs_tol=0.0,
        ):
            raise ValueError("model and MD coordinate-unit conversions must agree.")

    def kinetic_energy_hartree(self, state: MolecularDynamicsState) -> float:
        """Compute the laboratory-frame kinetic energy of one MD state."""
        if not isinstance(state, MolecularDynamicsState):
            raise TypeError("state must be MolecularDynamicsState.")
        twice_kinetic = fsum(
            mass * fsum(component * component for component in velocity)
            for mass, velocity in zip(state.masses, state.velocities, strict=True)
        )
        kinetic = 0.5 * twice_kinetic * self.kinetic_energy_factor
        if not isfinite(kinetic) or kinetic < 0.0:
            raise ValueError("kinetic energy must be finite and nonnegative.")
        return kinetic


@dataclass(frozen=True, slots=True)
class FLiBePeriodicMDRun:
    """Periodic MD trajectory and state-aligned full-potential observations."""

    model_id: str
    trajectory: MolecularDynamicsTrajectory
    evaluations: tuple[FLiBePeriodicPolarizableResult, ...]
    kinetic_energies_hartree: tuple[float, ...]
    total_energies_hartree: tuple[float, ...]
    units: FLiBePeriodicMDUnits
    mass_parameters: FLiBeMassParameters
    neighbor_cutoff: float

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        if not isinstance(self.trajectory, MolecularDynamicsTrajectory):
            raise TypeError("trajectory must be MolecularDynamicsTrajectory.")
        if not isinstance(self.units, FLiBePeriodicMDUnits):
            raise TypeError("units must be FLiBePeriodicMDUnits.")
        if not isinstance(self.mass_parameters, FLiBeMassParameters):
            raise TypeError("mass_parameters must be FLiBeMassParameters.")
        _positive(self.neighbor_cutoff, "neighbor_cutoff")
        states = self.trajectory.states
        if any(
            not isinstance(item, tuple) or len(item) != len(states)
            for item in (self.evaluations, self.kinetic_energies_hartree, self.total_energies_hartree)
        ):
            raise ValueError("potential and kinetic observations must align with MD states.")
        if not all(isinstance(value, FLiBePeriodicPolarizableResult) for value in self.evaluations):
            raise TypeError("evaluations must contain FLiBePeriodicPolarizableResult.")
        first_source = self.evaluations[0].source_file_sha256
        for index, (state, evaluated, kinetic, total) in enumerate(zip(
            states, self.evaluations, self.kinetic_energies_hartree,
            self.total_energies_hartree, strict=True,
        )):
            if evaluated.model_id != self.model_id:
                raise ValueError("all potential evaluations must use the declared model identifier.")
            if evaluated.configuration.configuration != state.configuration:
                raise ValueError("potential evaluation and MD configuration must agree.")
            if evaluated.source_file_sha256 != first_source:
                raise ValueError("all potential evaluations must use one source fingerprint.")
            if state.masses != configuration_masses(FLiBeConfiguration(state.configuration), self.mass_parameters):
                raise ValueError("MD mass inventory must match the declared FLiBe masses.")
            if not isclose(kinetic, self.units.kinetic_energy_hartree(state), rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError("kinetic energy must match each MD state.")
            if not isclose(total, kinetic + evaluated.energy.total_energy, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError("total energy must equal kinetic plus full potential energy.")
            if index < self.trajectory.step_count:
                if self.trajectory.steps[index].forces_before != evaluated.forces:
                    raise ValueError("step starting force must agree with the full potential.")
                if self.trajectory.steps[index].forces_after != self.evaluations[index + 1].forces:
                    raise ValueError("step ending force must agree with the full potential.")

    @property
    def maximum_absolute_energy_change_hartree(self) -> float:
        """Return the largest absolute total-energy change from the initial state."""
        initial = self.total_energies_hartree[0]
        return max(abs(value - initial) for value in self.total_energies_hartree)

    @property
    def source_file_sha256(self) -> str:
        return self.evaluations[0].source_file_sha256


def run_flibe_periodic_velocity_verlet(
    initial_state: MolecularDynamicsState,
    model: FLiBePeriodicPolarizableModel,
    mass_parameters: FLiBeMassParameters,
    units: FLiBePeriodicMDUnits,
    *,
    time_step: float,
    step_count: int,
    neighbor_cutoff: float,
) -> FLiBePeriodicMDRun:
    """Integrate mechanical motion with reoptimized dipoles at every force step.

    The neighbor graph is a trajectory geometry record, independent of the
    periodic Coulomb, short-range, and polarization force calculations.
    Cell vectors remain fixed throughout this NVE velocity-Verlet trajectory.
    """
    if not isinstance(initial_state, MolecularDynamicsState):
        raise TypeError("initial_state must be MolecularDynamicsState.")
    if not isinstance(model, FLiBePeriodicPolarizableModel):
        raise TypeError("model must be FLiBePeriodicPolarizableModel.")
    if not isinstance(mass_parameters, FLiBeMassParameters):
        raise TypeError("mass_parameters must be FLiBeMassParameters.")
    if not isinstance(units, FLiBePeriodicMDUnits):
        raise TypeError("units must be FLiBePeriodicMDUnits.")
    dt = _positive(time_step, "time_step")
    cutoff = _positive(neighbor_cutoff, "neighbor_cutoff")
    if isinstance(step_count, bool) or not isinstance(step_count, int):
        raise TypeError("step_count must be an integer.")
    if step_count <= 0:
        raise ValueError("step_count must be positive.")
    if initial_state.configuration.periodic != (True, True, True) or initial_state.configuration.cell is None:
        raise ValueError("periodic FLiBe MD requires three periodic axes and a cell.")
    flibe = FLiBeConfiguration(initial_state.configuration)
    flibe.composition()
    if initial_state.masses != configuration_masses(flibe, mass_parameters):
        raise ValueError("initial MD masses must equal declared FLiBe species masses.")
    units.check_model(model)

    current = initial_state
    evaluated = model.evaluate(flibe)
    graph = build_cutoff_graph(current.configuration, cutoff)
    results: list[MolecularDynamicsStepResult] = []
    observations = [evaluated]
    kinetic_energies = [units.kinetic_energy_hartree(current)]
    scale = units.acceleration_factor

    for _ in range(step_count):
        scaled_before = ForceState(tuple(
            tuple(scale * component for component in row)
            for row in evaluated.forces.forces
        ))
        acceleration_before = accelerations_from_forces(scaled_before, current.masses)
        positions_after = velocity_verlet_positions(
            current.configuration.positions, current.velocities,
            acceleration_before, dt,
        )
        updated_configuration = AtomicConfiguration(
            species=current.configuration.species,
            positions=positions_after,
            cell=current.configuration.cell,
            periodic=current.configuration.periodic,
        )
        evaluated_after = model.evaluate(FLiBeConfiguration(updated_configuration))
        scaled_after = ForceState(tuple(
            tuple(scale * component for component in row)
            for row in evaluated_after.forces.forces
        ))
        acceleration_after = accelerations_from_forces(scaled_after, current.masses)
        velocities_after = velocity_verlet_velocities(
            current.velocities, acceleration_before, acceleration_after, dt,
        )
        following = MolecularDynamicsState(
            configuration=updated_configuration,
            velocities=velocities_after,
            masses=current.masses,
            step=current.step + 1,
            time=current.time + dt,
        )
        following_graph = build_cutoff_graph(updated_configuration, cutoff)
        results.append(MolecularDynamicsStepResult(
            previous=current, current=following,
            graph_before=graph, graph_after=following_graph,
            forces_before=evaluated.forces, forces_after=evaluated_after.forces,
        ))
        observations.append(evaluated_after)
        kinetic_energies.append(units.kinetic_energy_hartree(following))
        current, evaluated, graph = following, evaluated_after, following_graph

    return FLiBePeriodicMDRun(
        model_id=model.model_id,
        trajectory=MolecularDynamicsTrajectory(steps=tuple(results)),
        evaluations=tuple(observations),
        kinetic_energies_hartree=tuple(kinetic_energies),
        total_energies_hartree=tuple(
            fsum((kinetic, observation.energy.total_energy))
            for kinetic, observation in zip(kinetic_energies, observations, strict=True)
        ),
        units=units,
        mass_parameters=mass_parameters,
        neighbor_cutoff=cutoff,
    )
