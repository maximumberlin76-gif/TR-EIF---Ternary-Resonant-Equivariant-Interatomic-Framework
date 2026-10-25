"""Mass-density observations and direct-reference comparisons for FLiBe MD."""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite

from tr_eif.md.trajectory import MolecularDynamicsTrajectory

from .composition import FLiBeComposition
from .configuration import FLiBeConfiguration
from .mass import FLiBeMassParameters, configuration_masses
from .reference_comparison import FLiBeEvidenceKind, FLiBeReferenceObservable
from .thermodynamic_state import FLiBeThermodynamicState
from .units import ParameterProvenance


def _positive_real(value: float, name: str) -> float:
    """Normalize one finite positive physical conversion factor."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real non-Boolean number.")
    number = float(value)
    if not isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive.")
    return number


def _identifier(value: str, name: str) -> str:
    """Validate one stable, nonempty provenance identifier."""

    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value.strip() or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _volume_in_coordinate_units(cell: tuple[tuple[float, float, float], ...]) -> float:
    """Return the absolute determinant of a three-vector periodic cell."""

    a, b, c = cell
    determinant = (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )
    volume = abs(determinant)
    if not isfinite(volume) or volume <= 0.0:
        raise ValueError("periodic cell volume must be finite and positive.")
    return volume


@dataclass(frozen=True, slots=True)
class FLiBeDensitySample:
    """One indexed density observation from a periodic FLiBe MD state."""

    state_index: int
    md_step: int
    md_time: float
    cell_volume_m3: float
    density_kg_m3: float

    def __post_init__(self) -> None:
        if (
            isinstance(self.state_index, bool)
            or not isinstance(self.state_index, int)
            or self.state_index < 0
        ):
            raise ValueError("state_index must be a nonnegative integer.")
        if (
            isinstance(self.md_step, bool)
            or not isinstance(self.md_step, int)
            or self.md_step < 0
        ):
            raise ValueError("md_step must be a nonnegative integer.")
        if not isinstance(self.md_time, (int, float)) or isinstance(self.md_time, bool):
            raise TypeError("md_time must be a real non-Boolean number.")
        if not isfinite(self.md_time) or self.md_time < 0.0:
            raise ValueError("md_time must be finite and nonnegative.")
        _positive_real(self.cell_volume_m3, "cell_volume_m3")
        _positive_real(self.density_kg_m3, "density_kg_m3")


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryDensity:
    """Ordered density series with explicit unit factors and run identity.

    Each sample is calculated using the instantaneous simulation-cell volume:

        rho[n] = M_cell / abs(det(cell[n])) / coordinate_unit_to_meter**3

    where M_cell is the fixed configuration mass expressed in kilograms.
    Arithmetic mean density and mass divided by mean volume are separate
    observables for trajectories with variable cell volume.
    """

    model_id: str
    trajectory_id: str
    provenance: ParameterProvenance
    composition: FLiBeComposition
    atom_count: int
    total_mass_kg: float
    mass_unit_to_kg: float
    coordinate_unit_to_meter: float
    samples: tuple[FLiBeDensitySample, ...]

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        _identifier(self.trajectory_id, "trajectory_id")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be a ParameterProvenance.")
        if not isinstance(self.composition, FLiBeComposition):
            raise TypeError("composition must be an FLiBeComposition.")
        if (
            isinstance(self.atom_count, bool)
            or not isinstance(self.atom_count, int)
            or self.atom_count <= 0
        ):
            raise ValueError("atom_count must be a positive integer.")
        _positive_real(self.total_mass_kg, "total_mass_kg")
        _positive_real(self.mass_unit_to_kg, "mass_unit_to_kg")
        _positive_real(self.coordinate_unit_to_meter, "coordinate_unit_to_meter")
        if not isinstance(self.samples, tuple) or not self.samples:
            raise ValueError("samples must be a nonempty tuple.")
        previous_index = -1
        for sample in self.samples:
            if not isinstance(sample, FLiBeDensitySample):
                raise TypeError("samples must contain FLiBeDensitySample values.")
            if sample.state_index <= previous_index:
                raise ValueError("density sample state indices must increase.")
            previous_index = sample.state_index

    @property
    def sample_count(self) -> int:
        """Return the number of selected MD state samples."""

        return len(self.samples)

    @property
    def mean_density_kg_m3(self) -> float:
        """Return the arithmetic mean of instantaneous cell densities."""

        return fsum(sample.density_kg_m3 for sample in self.samples) / self.sample_count

    @property
    def mean_cell_volume_m3(self) -> float:
        """Return the arithmetic mean of instantaneous cell volumes."""

        return fsum(sample.cell_volume_m3 for sample in self.samples) / self.sample_count

    @property
    def density_at_mean_volume_kg_m3(self) -> float:
        """Return total mass divided by mean instantaneous cell volume."""

        return self.total_mass_kg / self.mean_cell_volume_m3


def evaluate_flibe_trajectory_density(
    trajectory: MolecularDynamicsTrajectory,
    mass_parameters: FLiBeMassParameters,
    *,
    model_id: str,
    trajectory_id: str,
    provenance: ParameterProvenance,
    mass_unit_to_kg: float,
    coordinate_unit_to_meter: float,
    first_state_index: int = 0,
    stride: int = 1,
) -> FLiBeTrajectoryDensity:
    """Compute density samples from an existing FLiBe MD trajectory.

    Atomic masses are checked against ``FLiBeMassParameters`` in the same
    numerical mass unit as the MD state. Explicit SI factors are supplied
    for that mass unit and the configuration's Cartesian coordinate unit.
    Every trajectory state retains the initial ordered species and mass
    inventory. The selected state interval is recorded by sample indices.

    The resulting density series is available for an independently defined
    thermodynamic-state correspondence and reference comparison.
    """

    if not isinstance(trajectory, MolecularDynamicsTrajectory):
        raise TypeError("trajectory must be a MolecularDynamicsTrajectory.")
    if not isinstance(mass_parameters, FLiBeMassParameters):
        raise TypeError("mass_parameters must be an FLiBeMassParameters.")
    if not isinstance(provenance, ParameterProvenance):
        raise TypeError("provenance must be a ParameterProvenance.")

    validated_model_id = _identifier(model_id, "model_id")
    validated_trajectory_id = _identifier(trajectory_id, "trajectory_id")
    mass_factor = _positive_real(mass_unit_to_kg, "mass_unit_to_kg")
    coordinate_factor = _positive_real(
        coordinate_unit_to_meter, "coordinate_unit_to_meter"
    )

    if isinstance(first_state_index, bool) or not isinstance(first_state_index, int):
        raise TypeError("first_state_index must be an integer.")
    if isinstance(stride, bool) or not isinstance(stride, int):
        raise TypeError("stride must be an integer.")
    if stride <= 0:
        raise ValueError("stride must be positive.")

    states = trajectory.states
    if not 0 <= first_state_index < len(states):
        raise ValueError("first_state_index must select an existing MD state.")

    first = states[0]
    flibe = FLiBeConfiguration(configuration=first.configuration)
    composition = flibe.composition()
    expected_masses = configuration_masses(flibe, mass_parameters)
    if first.masses != expected_masses:
        raise ValueError("MD masses must match declared FLiBe species masses.")

    total_mass_kg = fsum(expected_masses) * mass_factor
    if not isfinite(total_mass_kg) or total_mass_kg <= 0.0:
        raise ValueError("converted total mass must be finite and positive.")

    samples: list[FLiBeDensitySample] = []

    for state_index, state in enumerate(states):
        if state.configuration.species != first.configuration.species:
            raise ValueError("ordered FLiBe species must remain invariant across MD states.")
        if state.masses != expected_masses:
            raise ValueError("FLiBe mass inventory must remain invariant across MD states.")
        if state.configuration.periodic != (True, True, True):
            raise ValueError("density sampling requires three periodic cell axes.")
        if state.configuration.cell is None:
            raise ValueError("density sampling requires an explicit periodic cell.")

        volume = _volume_in_coordinate_units(state.configuration.cell)
        volume_m3 = volume * coordinate_factor**3
        if not isfinite(volume_m3) or volume_m3 <= 0.0:
            raise ValueError("converted cell volume must be finite and positive.")

        if state_index < first_state_index or (state_index - first_state_index) % stride:
            continue

        density = total_mass_kg / volume_m3
        if not isfinite(density) or density <= 0.0:
            raise ValueError("calculated density must be finite and positive.")

        samples.append(
            FLiBeDensitySample(
                state_index=state_index,
                md_step=state.step,
                md_time=state.time,
                cell_volume_m3=volume_m3,
                density_kg_m3=density,
            )
        )

    return FLiBeTrajectoryDensity(
        model_id=validated_model_id,
        trajectory_id=validated_trajectory_id,
        provenance=provenance,
        composition=composition,
        atom_count=flibe.atom_count,
        total_mass_kg=total_mass_kg,
        mass_unit_to_kg=mass_factor,
        coordinate_unit_to_meter=coordinate_factor,
        samples=tuple(samples),
    )


@dataclass(frozen=True, slots=True)
class FLiBeDensityReferenceComparison:
    """Direct density comparison under equal declared material-state coordinates."""

    model_trace: FLiBeTrajectoryDensity
    reference: FLiBeReferenceObservable
    thermodynamic_state: FLiBeThermodynamicState
    physical_state_id: str
    normalization_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.model_trace, FLiBeTrajectoryDensity):
            raise TypeError("model_trace must be an FLiBeTrajectoryDensity.")
        if not isinstance(self.reference, FLiBeReferenceObservable):
            raise TypeError("reference must be an FLiBeReferenceObservable.")
        if not isinstance(self.thermodynamic_state, FLiBeThermodynamicState):
            raise TypeError("thermodynamic_state must be an FLiBeThermodynamicState.")
        _identifier(self.physical_state_id, "physical_state_id")
        _identifier(self.normalization_id, "normalization_id")

        if self.reference.evidence_kind not in (
            FLiBeEvidenceKind.EXPERIMENTAL,
            FLiBeEvidenceKind.FIRST_PRINCIPLES,
        ):
            raise ValueError("reference must carry a supported physical evidence kind.")
        if self.reference.observable_id != "mass_density":
            raise ValueError("reference observable must be mass_density.")
        if self.reference.value_unit != "kg/m^3":
            raise ValueError("reference density unit must be kg/m^3.")
        if self.reference.sample_count != 1 or self.reference.axis is not None:
            raise ValueError("reference must contain one scalar density observation.")
        if self.reference.values[0] <= 0.0:
            raise ValueError("reference density must be positive.")
        if self.reference.composition != self.model_trace.composition:
            raise ValueError("reference and model formula-unit compositions must match.")
        if self.reference.thermodynamic_state != self.thermodynamic_state:
            raise ValueError("reference and model thermodynamic coordinates must match.")
        if self.reference.physical_state_id != self.physical_state_id:
            raise ValueError("reference and model physical state identifiers must match.")
        if self.reference.normalization_id != self.normalization_id:
            raise ValueError("reference and model density normalization must match.")

    @property
    def residual_kg_m3(self) -> float:
        """Return arithmetic mean model density minus reference density."""

        return self.model_trace.mean_density_kg_m3 - self.reference.values[0]

    @property
    def absolute_residual_kg_m3(self) -> float:
        """Return the absolute value of the signed density residual."""

        return abs(self.residual_kg_m3)

    @property
    def relative_residual(self) -> float:
        """Return signed residual normalized by positive reference density."""

        return self.residual_kg_m3 / self.reference.values[0]


def compare_flibe_trajectory_density_to_reference(
    model_trace: FLiBeTrajectoryDensity,
    reference: FLiBeReferenceObservable,
    *,
    thermodynamic_state: FLiBeThermodynamicState,
    physical_state_id: str,
    normalization_id: str,
) -> FLiBeDensityReferenceComparison:
    """Compare model-derived mean density with one matched source observation.

    Required coordinates are composition, temperature, pressure, physical
    state, density unit and normalization. Source evidence remains identified
    as EXPERIMENTAL or FIRST_PRINCIPLES. State conversions and temperature
    interpolation are separate operations upstream of this direct comparison.
    """

    return FLiBeDensityReferenceComparison(
        model_trace=model_trace,
        reference=reference,
        thermodynamic_state=thermodynamic_state,
        physical_state_id=physical_state_id,
        normalization_id=normalization_id,
    )
