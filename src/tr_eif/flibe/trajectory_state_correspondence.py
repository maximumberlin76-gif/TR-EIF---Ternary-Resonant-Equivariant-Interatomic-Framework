"""FLiBe MD density state coordinates and reference correspondence."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import fsum, isclose, isfinite

from tr_eif.md.thermostat import kinetic_temperature
from tr_eif.md.trajectory import MolecularDynamicsTrajectory

from .composition import FLiBeComposition
from .configuration import FLiBeConfiguration
from .reference_comparison import FLiBeEvidenceKind, FLiBeReferenceObservable
from .trajectory_density import FLiBeTrajectoryDensity
from .units import ParameterProvenance


# Exact defining value in the SI (BIPM SI Brochure).
BOLTZMANN_CONSTANT_J_PER_K = 1.380649e-23


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


def _name(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _cell_volume(cell: tuple[tuple[float, float, float], ...]) -> float:
    """Calculate the absolute determinant of three cell vectors."""

    a, b, c = cell
    return abs(
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


class FLiBePressureRole(str, Enum):
    """Origin of a numerical pressure coordinate."""

    OBSERVED = "OBSERVED"
    CONTROL_TARGET = "CONTROL_TARGET"


@dataclass(frozen=True, slots=True)
class FLiBePressureCoordinate:
    """Pressure in pascal with an explicit observation or control role."""

    pressure_pa: float
    role: FLiBePressureRole
    method_id: str
    source_id: str
    provenance: ParameterProvenance

    def __post_init__(self) -> None:
        _nonnegative(self.pressure_pa, "pressure_pa")
        if not isinstance(self.role, FLiBePressureRole):
            raise TypeError("role must be a FLiBePressureRole.")
        _name(self.method_id, "method_id")
        _name(self.source_id, "source_id")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be a ParameterProvenance.")


@dataclass(frozen=True, slots=True)
class FLiBeTrajectoryStateCoordinates:
    """Sample-aligned kinetic temperatures and optional pressure evidence.

    Kinetic temperatures are computed from trajectory velocities and masses
    using the SI conversion of the declared MD mass, length and time units.
    Pressure evidence has a separate observable or control origin.
    """

    density_trace: FLiBeTrajectoryDensity
    kinetic_temperature_k: tuple[float, ...]
    degrees_of_freedom: int
    time_unit_to_second: float
    physical_state_id: str
    physical_state_method_id: str
    pressure: FLiBePressureCoordinate | None

    def __post_init__(self) -> None:
        if not isinstance(self.density_trace, FLiBeTrajectoryDensity):
            raise TypeError("density_trace must be a FLiBeTrajectoryDensity.")
        if not isinstance(self.kinetic_temperature_k, tuple):
            raise TypeError("kinetic_temperature_k must be a tuple.")
        if len(self.kinetic_temperature_k) != self.density_trace.sample_count:
            raise ValueError("temperature and density sample counts must agree.")
        for temperature in self.kinetic_temperature_k:
            _nonnegative(temperature, "kinetic temperature")
        if (
            isinstance(self.degrees_of_freedom, bool)
            or not isinstance(self.degrees_of_freedom, int)
            or not 0 < self.degrees_of_freedom <= 3 * self.density_trace.atom_count
        ):
            raise ValueError("degrees_of_freedom must be in 1..3*atom_count.")
        _positive(self.time_unit_to_second, "time_unit_to_second")
        _name(self.physical_state_id, "physical_state_id")
        _name(self.physical_state_method_id, "physical_state_method_id")
        if self.pressure is not None and not isinstance(
            self.pressure, FLiBePressureCoordinate
        ):
            raise TypeError("pressure must be FLiBePressureCoordinate or None.")

    @property
    def mean_kinetic_temperature_k(self) -> float:
        """Return the arithmetic mean over selected density sampling states."""

        return fsum(self.kinetic_temperature_k) / len(self.kinetic_temperature_k)


def evaluate_flibe_trajectory_state_coordinates(
    trajectory: MolecularDynamicsTrajectory,
    density_trace: FLiBeTrajectoryDensity,
    *,
    degrees_of_freedom: int,
    time_unit_to_second: float,
    physical_state_id: str,
    physical_state_method_id: str,
    pressure: FLiBePressureCoordinate | None = None,
) -> FLiBeTrajectoryStateCoordinates:
    """Evaluate sample-aligned MD kinetic temperature in kelvin.

    MD energy units are derived from the trajectory-density mass and length
    factors and the explicitly supplied time factor. The Boltzmann constant
    is converted to those energy units before calling the MD estimator.
    """

    if not isinstance(trajectory, MolecularDynamicsTrajectory):
        raise TypeError("trajectory must be a MolecularDynamicsTrajectory.")
    if not isinstance(density_trace, FLiBeTrajectoryDensity):
        raise TypeError("density_trace must be a FLiBeTrajectoryDensity.")
    time_factor = _positive(time_unit_to_second, "time_unit_to_second")
    if (
        isinstance(degrees_of_freedom, bool)
        or not isinstance(degrees_of_freedom, int)
        or not 0 < degrees_of_freedom <= 3 * density_trace.atom_count
    ):
        raise ValueError("degrees_of_freedom must be in 1..3*atom_count.")

    velocity_factor = density_trace.coordinate_unit_to_meter / time_factor
    energy_factor = density_trace.mass_unit_to_kg * velocity_factor**2
    k_b_md = BOLTZMANN_CONSTANT_J_PER_K / _positive(
        energy_factor, "MD energy unit in joules"
    )
    _positive(k_b_md, "Boltzmann constant in MD energy units")

    states = trajectory.states
    if states[0].atom_count != density_trace.atom_count:
        raise ValueError("trajectory and density atom counts must agree.")
    temperatures: list[float] = []
    for sample in density_trace.samples:
        if sample.state_index >= len(states):
            raise ValueError("density state index exceeds trajectory length.")
        state = states[sample.state_index]
        if state.step != sample.md_step or state.time != sample.md_time:
            raise ValueError("density and trajectory step/time coordinates differ.")
        if FLiBeConfiguration(state.configuration).composition() != density_trace.composition:
            raise ValueError("density and trajectory compositions differ.")
        mass_kg = fsum(state.masses) * density_trace.mass_unit_to_kg
        if not isclose(mass_kg, density_trace.total_mass_kg, rel_tol=1e-12):
            raise ValueError("density and trajectory mass inventories differ.")
        if state.configuration.periodic != (True, True, True):
            raise ValueError("sampled trajectory state requires three periodic axes.")
        if state.configuration.cell is None:
            raise ValueError("sampled trajectory state requires a periodic cell.")
        volume_m3 = _cell_volume(state.configuration.cell) * (
            density_trace.coordinate_unit_to_meter**3
        )
        if not isfinite(volume_m3) or not isclose(
            volume_m3, sample.cell_volume_m3, rel_tol=1e-12
        ):
            raise ValueError("density and trajectory cell volumes differ.")
        temperatures.append(kinetic_temperature(state, degrees_of_freedom, k_b_md))

    return FLiBeTrajectoryStateCoordinates(
        density_trace=density_trace,
        kinetic_temperature_k=tuple(temperatures),
        degrees_of_freedom=degrees_of_freedom,
        time_unit_to_second=time_factor,
        physical_state_id=physical_state_id,
        physical_state_method_id=physical_state_method_id,
        pressure=pressure,
    )


@dataclass(frozen=True, slots=True)
class FLiBeDensitySourceCoordinates:
    """Density and reported state coordinates from one identified source.

    Optional pressure and physical-state coordinates preserve source-table
    availability independently of the numeric density and temperature.
    """

    density_kg_m3: float
    composition: FLiBeComposition
    temperature_k: float
    pressure_pa: float | None
    physical_state_id: str | None
    normalization_id: str
    evidence_kind: FLiBeEvidenceKind
    source_id: str
    method_id: str
    provenance: ParameterProvenance
    density_standard_uncertainty_kg_m3: float | None = None
    temperature_standard_uncertainty_k: float | None = None
    pressure_standard_uncertainty_pa: float | None = None
    bef2_fraction_standard_uncertainty: float | None = None

    def __post_init__(self) -> None:
        _positive(self.density_kg_m3, "density_kg_m3")
        if not isinstance(self.composition, FLiBeComposition):
            raise TypeError("composition must be a FLiBeComposition.")
        _positive(self.temperature_k, "temperature_k")
        if self.pressure_pa is not None:
            _nonnegative(self.pressure_pa, "pressure_pa")
        if self.physical_state_id is not None:
            _name(self.physical_state_id, "physical_state_id")
        _name(self.normalization_id, "normalization_id")
        if not isinstance(self.evidence_kind, FLiBeEvidenceKind):
            raise TypeError("evidence_kind must be a FLiBeEvidenceKind.")
        _name(self.source_id, "source_id")
        _name(self.method_id, "method_id")
        if not isinstance(self.provenance, ParameterProvenance):
            raise TypeError("provenance must be a ParameterProvenance.")
        for name in (
            "density_standard_uncertainty_kg_m3",
            "temperature_standard_uncertainty_k",
            "pressure_standard_uncertainty_pa",
            "bef2_fraction_standard_uncertainty",
        ):
            value = getattr(self, name)
            if value is not None:
                _nonnegative(value, name)
        if (
            self.bef2_fraction_standard_uncertainty is not None
            and self.bef2_fraction_standard_uncertainty > 1.0
        ):
            raise ValueError("BeF2 fraction uncertainty must not exceed one.")


def flibe_density_source_from_observable(
    observable: FLiBeReferenceObservable,
) -> FLiBeDensitySourceCoordinates:
    """Project an existing typed scalar density observable onto state axes."""

    if not isinstance(observable, FLiBeReferenceObservable):
        raise TypeError("observable must be a FLiBeReferenceObservable.")
    if observable.observable_id != "mass_density":
        raise ValueError("observable must describe mass_density.")
    if observable.value_unit != "kg/m^3":
        raise ValueError("density unit must be kg/m^3.")
    if observable.sample_count != 1 or observable.axis is not None:
        raise ValueError("observable must contain one scalar density.")
    return FLiBeDensitySourceCoordinates(
        density_kg_m3=observable.values[0],
        composition=observable.composition,
        temperature_k=observable.thermodynamic_state.temperature,
        pressure_pa=observable.thermodynamic_state.pressure,
        physical_state_id=observable.physical_state_id,
        normalization_id=observable.normalization_id,
        evidence_kind=observable.evidence_kind,
        source_id=observable.source_id,
        method_id=observable.method_id,
        provenance=observable.provenance,
    )


@dataclass(frozen=True, slots=True)
class FLiBeDensityStateCorrespondence:
    """Numerical coordinate match between a density trajectory and source."""

    model: FLiBeTrajectoryStateCoordinates
    reference: FLiBeDensitySourceCoordinates
    temperature_tolerance_k: float
    pressure_tolerance_pa: float
    composition_match: bool
    temperature_match: bool
    pressure_match: bool
    physical_state_match: bool
    normalization_match: bool

    @property
    def coordinate_match(self) -> bool:
        """Return conjunction of the declared physical-state coordinates."""

        return all((
            self.composition_match,
            self.temperature_match,
            self.pressure_match,
            self.physical_state_match,
            self.normalization_match,
        ))

    @property
    def temperature_difference_k(self) -> float:
        """Return model mean kinetic temperature minus reported temperature."""

        return (
            self.model.mean_kinetic_temperature_k
            - self.reference.temperature_k
        )

    @property
    def pressure_difference_pa(self) -> float | None:
        """Return observed model pressure minus reported pressure when present."""

        pressure = self.model.pressure
        if pressure is None or pressure.role is not FLiBePressureRole.OBSERVED:
            return None
        if self.reference.pressure_pa is None:
            return None
        return pressure.pressure_pa - self.reference.pressure_pa

    @property
    def density_residual_kg_m3(self) -> float:
        """Return density residual for fully matched coordinate records."""

        if not self.coordinate_match:
            raise ValueError("Density residual requires matched state coordinates.")
        return self.model.density_trace.mean_density_kg_m3 - self.reference.density_kg_m3


def compare_flibe_density_state_coordinates(
    model: FLiBeTrajectoryStateCoordinates,
    reference: FLiBeDensitySourceCoordinates | FLiBeReferenceObservable,
    *,
    temperature_tolerance_k: float = 0.0,
    pressure_tolerance_pa: float = 0.0,
    normalization_id: str,
) -> FLiBeDensityStateCorrespondence:
    """Apply predeclared temperature and pressure coordinate tolerances.

    Pressure comparison requires an observed model pressure coordinate;
    a controlled pressure target retains its separate operational role.
    Exact composition and physical-state identities are checked independently.
    """

    if not isinstance(model, FLiBeTrajectoryStateCoordinates):
        raise TypeError("model must be FLiBeTrajectoryStateCoordinates.")
    if isinstance(reference, FLiBeReferenceObservable):
        source = flibe_density_source_from_observable(reference)
    elif isinstance(reference, FLiBeDensitySourceCoordinates):
        source = reference
    else:
        raise TypeError("reference must be a typed FLiBe density source.")
    t_tol = _nonnegative(temperature_tolerance_k, "temperature_tolerance_k")
    p_tol = _nonnegative(pressure_tolerance_pa, "pressure_tolerance_pa")
    normalization = _name(normalization_id, "normalization_id")

    pressure = model.pressure
    return FLiBeDensityStateCorrespondence(
        model=model,
        reference=source,
        temperature_tolerance_k=t_tol,
        pressure_tolerance_pa=p_tol,
        composition_match=model.density_trace.composition == source.composition,
        temperature_match=(
            abs(model.mean_kinetic_temperature_k - source.temperature_k)
            <= t_tol
        ),
        pressure_match=(
            pressure is not None
            and pressure.role is FLiBePressureRole.OBSERVED
            and source.pressure_pa is not None
            and abs(pressure.pressure_pa - source.pressure_pa) <= p_tol
        ),
        physical_state_match=(
            source.physical_state_id is not None
            and model.physical_state_id == source.physical_state_id
        ),
        normalization_match=normalization == source.normalization_id,
    )
