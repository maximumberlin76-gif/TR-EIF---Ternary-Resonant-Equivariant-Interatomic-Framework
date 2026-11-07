"""Fixed-cell Cartesian structural relaxation of periodic polarizable FLiBe.

The periodic model resolves stationary fluoride dipoles at each trial geometry.
Atomic positions follow projected conservative forces with Armijo backtracking.
The projection removes a uniform translational step while preserving relative
coordinates. A step is accepted only when the complete relaxed-dipole energy
satisfies the directional-decrease criterion. The cell and species stay fixed.

Force and displacement thresholds are expressed in hartree/bohr and bohr;
conversion uses the model's declared bohr-per-input-coordinate factor.
The returned stop reason records force convergence, iteration exhaustion,
or line-search exhaustion separately.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isfinite, sqrt

from tr_eif.configuration import AtomicConfiguration

from .configuration import FLiBeConfiguration
from .periodic_polarizable import (
    FLiBePeriodicPolarizableModel,
    FLiBePeriodicPolarizableResult,
)


def _positive_real(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _positive_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be positive.")
    return value


@dataclass(frozen=True, slots=True)
class FLiBeStructuralRelaxationSettings:
    """Predeclared fixed-cell minimization controls and numerical limits."""

    maximum_iterations: int = 24
    maximum_trials_per_iteration: int = 16
    force_tolerance_hartree_per_bohr: float = 1.0e-5
    maximum_atom_displacement_bohr: float = 0.08
    minimum_atom_displacement_bohr: float = 1.0e-10
    backtrack_factor: float = 0.5
    armijo_fraction: float = 1.0e-4

    def __post_init__(self) -> None:
        _positive_int(self.maximum_iterations, "maximum_iterations")
        _positive_int(self.maximum_trials_per_iteration, "maximum_trials_per_iteration")
        for name in (
            "force_tolerance_hartree_per_bohr",
            "maximum_atom_displacement_bohr",
            "minimum_atom_displacement_bohr",
            "backtrack_factor",
            "armijo_fraction",
        ):
            object.__setattr__(self, name, _positive_real(getattr(self, name), name))
        if self.minimum_atom_displacement_bohr >= self.maximum_atom_displacement_bohr:
            raise ValueError("minimum displacement must be below maximum displacement.")
        if self.backtrack_factor >= 1.0 or self.armijo_fraction >= 1.0:
            raise ValueError("backtrack_factor and armijo_fraction must be below one.")


class FLiBeRelaxationStopReason(str, Enum):
    """Termination conditions for atomic-coordinate minimization."""

    FORCE_TOLERANCE = "FORCE_TOLERANCE"
    MAXIMUM_ITERATIONS = "MAXIMUM_ITERATIONS"
    LINE_SEARCH_EXHAUSTED = "LINE_SEARCH_EXHAUSTED"


@dataclass(frozen=True, slots=True)
class FLiBeStructuralRelaxationStep:
    """One accepted atomic update and its source-aligned energy evidence."""

    iteration: int
    line_search_trials: int
    maximum_atom_displacement_bohr: float
    energy_before_hartree: float
    energy_after_hartree: float
    maximum_force_after_hartree_per_bohr: float
    dipole_stationarity_after_atomic: float

    def __post_init__(self) -> None:
        _positive_int(self.iteration, "iteration")
        _positive_int(self.line_search_trials, "line_search_trials")
        _positive_real(self.maximum_atom_displacement_bohr, "maximum_atom_displacement_bohr")
        if not (isfinite(self.energy_before_hartree) and isfinite(self.energy_after_hartree)):
            raise ValueError("energies must be finite.")
        if not self.energy_after_hartree < self.energy_before_hartree:
            raise ValueError("accepted geometry must decrease total energy.")
        for name in ("maximum_force_after_hartree_per_bohr", "dipole_stationarity_after_atomic"):
            value = getattr(self, name)
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative.")


@dataclass(frozen=True, slots=True)
class FLiBeStructuralRelaxationResult:
    """Fixed-cell relaxation record with terminal structure and convergence state."""

    model_id: str
    source_doi: str
    source_file_sha256: str
    settings: FLiBeStructuralRelaxationSettings
    initial_configuration: FLiBeConfiguration
    final_configuration: FLiBeConfiguration
    initial_energy_hartree: float
    final_energy_hartree: float
    initial_maximum_force_hartree_per_bohr: float
    final_maximum_force_hartree_per_bohr: float
    final_dipole_stationarity_atomic: float
    steps: tuple[FLiBeStructuralRelaxationStep, ...]
    stop_reason: FLiBeRelaxationStopReason

    def __post_init__(self) -> None:
        if not isinstance(self.settings, FLiBeStructuralRelaxationSettings):
            raise TypeError("settings must be FLiBeStructuralRelaxationSettings.")
        if self.initial_configuration.configuration.cell != self.final_configuration.configuration.cell:
            raise ValueError("fixed-cell minimization must preserve the cell.")
        if self.initial_configuration.species != self.final_configuration.species:
            raise ValueError("fixed-cell minimization must preserve species.")
        if not (isfinite(self.initial_energy_hartree) and isfinite(self.final_energy_hartree)):
            raise ValueError("initial and final energies must be finite.")
        for name in (
            "initial_maximum_force_hartree_per_bohr",
            "final_maximum_force_hartree_per_bohr",
            "final_dipole_stationarity_atomic",
        ):
            value = getattr(self, name)
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative.")
        if self.final_energy_hartree > self.initial_energy_hartree + 1.0e-13:
            raise ValueError("final energy must not exceed initial energy.")
        if not isinstance(self.steps, tuple) or len(self.steps) > self.settings.maximum_iterations:
            raise ValueError("step records must fit the declared iteration limit.")
        previous_energy = self.initial_energy_hartree
        for index, step in enumerate(self.steps, start=1):
            if not isinstance(step, FLiBeStructuralRelaxationStep) or step.iteration != index:
                raise ValueError("relaxation steps must be consecutive and typed.")
            if step.line_search_trials > self.settings.maximum_trials_per_iteration:
                raise ValueError("line search exceeded the declared trial budget.")
            if step.maximum_atom_displacement_bohr > self.settings.maximum_atom_displacement_bohr * (1.0 + 1.0e-12):
                raise ValueError("accepted displacement exceeded the declared maximum.")
            if step.energy_before_hartree != previous_energy:
                raise ValueError("relaxation energy record is discontinuous.")
            previous_energy = step.energy_after_hartree
        if previous_energy != self.final_energy_hartree:
            raise ValueError("final energy differs from the accepted step history.")
        if not isinstance(self.stop_reason, FLiBeRelaxationStopReason):
            raise TypeError("stop_reason must be FLiBeRelaxationStopReason.")
        if self.stop_reason is FLiBeRelaxationStopReason.FORCE_TOLERANCE and (
            self.final_maximum_force_hartree_per_bohr
            > self.settings.force_tolerance_hartree_per_bohr
        ):
            raise ValueError("force-tolerance termination requires a bounded final force.")

    @property
    def converged(self) -> bool:
        """True exactly when the declared force threshold was reached."""
        return self.stop_reason is FLiBeRelaxationStopReason.FORCE_TOLERANCE

    @property
    def accepted_steps(self) -> int:
        """Number of accepted Cartesian relaxation steps."""
        return len(self.steps)


def _maximum_force_hartree_per_bohr(
    observation: FLiBePeriodicPolarizableResult,
) -> float:
    factor = observation.coordinate_unit_to_bohr
    return max(
        sqrt(fsum(component * component for component in force)) / factor
        for force in observation.forces.forces
    )


def _projected_forces(
    observation: FLiBePeriodicPolarizableResult,
) -> tuple[tuple[float, float, float], ...]:
    forces = observation.forces.forces
    n = len(forces)
    mean = tuple(fsum(force[axis] for force in forces) / n for axis in range(3))
    return tuple(
        tuple(force[axis] - mean[axis] for axis in range(3))
        for force in forces
    )


def relax_flibe_periodic_structure(
    configuration: FLiBeConfiguration,
    model: FLiBePeriodicPolarizableModel,
    *,
    settings: FLiBeStructuralRelaxationSettings | None = None,
) -> FLiBeStructuralRelaxationResult:
    """Minimize the source-registered stationary-dipole potential at fixed cell.

    Each steepest-descent direction is the Cartesian force with its uniform
    translational component removed. The Armijo condition compares a trial
    energy with the previous energy minus a fraction of the directional
    derivative. Numerical line-search exhaustion is reported explicitly.
    """
    if not isinstance(configuration, FLiBeConfiguration):
        raise TypeError("configuration must be FLiBeConfiguration.")
    if not isinstance(model, FLiBePeriodicPolarizableModel):
        raise TypeError("model must be FLiBePeriodicPolarizableModel.")
    if settings is None:
        settings = FLiBeStructuralRelaxationSettings()
    if not isinstance(settings, FLiBeStructuralRelaxationSettings):
        raise TypeError("settings must be FLiBeStructuralRelaxationSettings.")
    atomic = configuration.configuration
    if atomic.cell is None or atomic.periodic != (True, True, True):
        raise ValueError("relaxation requires a fully periodic fixed cell.")
    configuration.composition()

    observation = model.evaluate(configuration)
    initial = observation
    conversion = _positive_real(observation.coordinate_unit_to_bohr, "coordinate_unit_to_bohr")
    accepted: list[FLiBeStructuralRelaxationStep] = []
    termination = FLiBeRelaxationStopReason.MAXIMUM_ITERATIONS

    for iteration in range(1, settings.maximum_iterations + 1):
        maximum_force = _maximum_force_hartree_per_bohr(observation)
        if maximum_force <= settings.force_tolerance_hartree_per_bohr:
            termination = FLiBeRelaxationStopReason.FORCE_TOLERANCE
            break
        direction = _projected_forces(observation)
        maximum_direction = max(
            sqrt(fsum(component * component for component in vector))
            for vector in direction
        )
        slope = fsum(component * component for vector in direction for component in vector)
        if maximum_direction == 0.0 or slope == 0.0:
            termination = FLiBeRelaxationStopReason.LINE_SEARCH_EXHAUSTED
            break
        step_size = settings.maximum_atom_displacement_bohr / (conversion * maximum_direction)
        previous_energy = observation.energy.total_energy
        found: tuple[FLiBeConfiguration, FLiBePeriodicPolarizableResult, int, float] | None = None
        for trial in range(1, settings.maximum_trials_per_iteration + 1):
            displacement = step_size * maximum_direction * conversion
            if displacement < settings.minimum_atom_displacement_bohr:
                break
            trial_positions = tuple(
                tuple(pos[axis] + step_size * vector[axis] for axis in range(3))
                for pos, vector in zip(atomic.positions, direction, strict=True)
            )
            trial_atomic = AtomicConfiguration(
                species=atomic.species,
                positions=trial_positions,
                cell=atomic.cell,
                periodic=atomic.periodic,
            )
            trial_configuration = FLiBeConfiguration(trial_atomic)
            trial_observation = model.evaluate(trial_configuration)
            if trial_observation.source_file_sha256 != initial.source_file_sha256:
                raise ValueError("relaxation source fingerprint changed during evaluation.")
            threshold = previous_energy - settings.armijo_fraction * step_size * slope
            if (
                trial_observation.energy.total_energy < previous_energy
                and trial_observation.energy.total_energy <= threshold
            ):
                found = (trial_configuration, trial_observation, trial, displacement)
                break
            step_size *= settings.backtrack_factor
        if found is None:
            termination = FLiBeRelaxationStopReason.LINE_SEARCH_EXHAUSTED
            break
        configuration, observation, trial_count, displacement = found
        atomic = configuration.configuration
        accepted.append(FLiBeStructuralRelaxationStep(
            iteration=iteration,
            line_search_trials=trial_count,
            maximum_atom_displacement_bohr=displacement,
            energy_before_hartree=previous_energy,
            energy_after_hartree=observation.energy.total_energy,
            maximum_force_after_hartree_per_bohr=_maximum_force_hartree_per_bohr(observation),
            dipole_stationarity_after_atomic=observation.max_stationarity_residual_atomic,
        ))
    else:
        if _maximum_force_hartree_per_bohr(observation) <= settings.force_tolerance_hartree_per_bohr:
            termination = FLiBeRelaxationStopReason.FORCE_TOLERANCE

    return FLiBeStructuralRelaxationResult(
        model_id=model.model_id,
        source_doi=initial.source_doi,
        source_file_sha256=initial.source_file_sha256,
        settings=settings,
        initial_configuration=initial.configuration,
        final_configuration=configuration,
        initial_energy_hartree=initial.energy.total_energy,
        final_energy_hartree=observation.energy.total_energy,
        initial_maximum_force_hartree_per_bohr=_maximum_force_hartree_per_bohr(initial),
        final_maximum_force_hartree_per_bohr=_maximum_force_hartree_per_bohr(observation),
        final_dipole_stationarity_atomic=observation.max_stationarity_residual_atomic,
        steps=tuple(accepted),
        stop_reason=termination,
    )
