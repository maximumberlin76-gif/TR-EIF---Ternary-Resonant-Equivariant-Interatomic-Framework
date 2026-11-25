"""Registered-source density correspondence for FLiBe rank-two TR-EIP MD.

Project selected post-barostat MD observations onto the existing FLiBe density
and physical-state coordinate contracts. Mean instantaneous density, kinetic
temperature, and observed hydrostatic pressure are calculated from the same
selected frames; the independent barostat pressure target is retained only
in the source trajectory.

Source records retain their original provenance, uncertainties and optional
coordinates. The registered comparison operator reports a density residual
only when the declared physical-state coordinates are all matched.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose, isfinite

from .configuration import FLiBeConfiguration
from .rank_two_tr_eip_pressure_coupled_observables import (
    FLiBeRankTwoTREIPPressureCoupledObservables,
)
from .registered_density_cross_model import (
    FLiBeDensityObservableMapping,
    FLiBeRegisteredDensityComparison,
    compare_flibe_registered_density_records,
)
from .registered_density_sources import FLiBeRegisteredDensityRecord
from .trajectory_density import FLiBeDensitySample, FLiBeTrajectoryDensity
from .trajectory_state_correspondence import (
    FLiBePressureCoordinate,
    FLiBePressureRole,
    FLiBeTrajectoryStateCoordinates,
)
from .units import ParameterProvenance


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be nonempty and trimmed.")
    return value


def _selection(value: int, name: str, *, allow_zero: bool) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < (0 if allow_zero else 1):
        raise ValueError(f"{name} lies outside its permitted index range.")
    return value


@dataclass(frozen=True, slots=True)
class FLiBeRankTwoRegisteredDensityCorrespondence:
    """Source-resolved comparison with an explicit post-barostat sample window."""

    observables: FLiBeRankTwoTREIPPressureCoupledObservables
    selected_interval_indices: tuple[int, ...]
    model_coordinates: FLiBeTrajectoryStateCoordinates
    signed_post_barostat_pressures_pa: tuple[float, ...]
    comparison: FLiBeRegisteredDensityComparison

    def __post_init__(self) -> None:
        if not isinstance(
            self.observables, FLiBeRankTwoTREIPPressureCoupledObservables
        ):
            raise TypeError(
                "observables must be FLiBeRankTwoTREIPPressureCoupledObservables."
            )
        if not isinstance(self.model_coordinates, FLiBeTrajectoryStateCoordinates):
            raise TypeError(
                "model_coordinates must be FLiBeTrajectoryStateCoordinates."
            )
        if not isinstance(self.comparison, FLiBeRegisteredDensityComparison):
            raise TypeError(
                "comparison must be FLiBeRegisteredDensityComparison."
            )
        if self.comparison.model != self.model_coordinates:
            raise ValueError("comparison and selected MD coordinates differ.")

        indices = self.selected_interval_indices
        if (
            not isinstance(indices, tuple)
            or not indices
            or any(
                isinstance(i, bool) or not isinstance(i, int)
                for i in indices
            )
        ):
            raise ValueError(
                "selected_interval_indices must contain integer indices."
            )
        if indices != tuple(sorted(set(indices))):
            raise ValueError(
                "selected_interval_indices must be strictly increasing."
            )
        if indices[-1] >= len(self.observables.samples) or indices[0] < 0:
            raise ValueError(
                "selected interval lies outside the MD record."
            )

        if not isinstance(self.signed_post_barostat_pressures_pa, tuple):
            raise TypeError(
                "signed_post_barostat_pressures_pa must be a tuple."
            )
        if len(indices) != len(self.signed_post_barostat_pressures_pa):
            raise ValueError(
                "pressure count must match selected MD intervals."
            )

        density_samples = self.model_coordinates.density_trace.samples
        temperatures = self.model_coordinates.kinetic_temperature_k

        if len(density_samples) != len(indices) or len(temperatures) != len(indices):
            raise ValueError(
                "density and kinetic temperature samples must align."
            )

        source = self.observables
        for position, i in enumerate(indices):
            original = source.samples[i]
            density = density_samples[position]
            pressure = self.signed_post_barostat_pressures_pa[position]

            if (
                not isfinite(pressure)
                or pressure != original.total_pressure_pa
                or density.state_index != i + 1
                or density.md_step != original.md_step
                or density.cell_volume_m3 != original.volume_m3
                or density.density_kg_m3 != original.density_kg_m3
                or temperatures[position] != original.kinetic_temperature_k
            ):
                raise ValueError(
                    "registered comparison samples differ from MD observations."
                )

            state = source.trajectory.steps[i].barostat.current.md_state
            if density.md_time != state.time:
                raise ValueError(
                    "native mechanical time differs from the selected MD state."
                )

        pressure_coordinate = self.model_coordinates.pressure
        mean_pressure = self.mean_signed_pressure_pa

        if mean_pressure >= 0.0:
            if (
                pressure_coordinate is None
                or pressure_coordinate.role is not FLiBePressureRole.OBSERVED
                or not isclose(
                    pressure_coordinate.pressure_pa,
                    mean_pressure,
                    rel_tol=1e-12,
                    abs_tol=1e-8,
                )
            ):
                raise ValueError(
                    "model pressure must be the observed post-barostat mean."
                )
        elif pressure_coordinate is not None:
            raise ValueError(
                "signed negative pressure must retain its separate coordinate."
            )

    @property
    def mean_signed_pressure_pa(self) -> float:
        """Arithmetic mean of selected post-barostat total hydrostatic pressures."""
        return fsum(self.signed_post_barostat_pressures_pa) / len(
            self.signed_post_barostat_pressures_pa
        )

    @property
    def matched_source_count(self) -> int:
        return self.comparison.matched_count

    @property
    def unmatched_source_count(self) -> int:
        return self.comparison.unmatched_count


def compare_flibe_rank_two_registered_density(
    observables: FLiBeRankTwoTREIPPressureCoupledObservables,
    records: tuple[FLiBeRegisteredDensityRecord, ...],
    *,
    model_id: str,
    trajectory_id: str,
    physical_state_id: str,
    physical_state_method_id: str,
    observed_pressure_method_id: str,
    mapping: FLiBeDensityObservableMapping,
    provenance: ParameterProvenance,
    temperature_tolerance_k: float,
    pressure_tolerance_pa: float,
    first_interval_index: int = 0,
    stride: int = 1,
) -> FLiBeRankTwoRegisteredDensityCorrespondence:
    """Compare selected rank-two MD frames against one registered source table.

    Source coordinates and matching tolerances are supplied explicitly.
    Negative signed pressure remains in the source pressure series and has no
    nonnegative FLiBePressureCoordinate representation. It is not replaced by
    the target barostat pressure. Comparison rows preserve such missing axes.
    """
    if not isinstance(
        observables, FLiBeRankTwoTREIPPressureCoupledObservables
    ):
        raise TypeError(
            "observables must be FLiBeRankTwoTREIPPressureCoupledObservables."
        )
    if not isinstance(mapping, FLiBeDensityObservableMapping):
        raise TypeError(
            "mapping must be FLiBeDensityObservableMapping."
        )
    if not isinstance(provenance, ParameterProvenance):
        raise TypeError("provenance must be ParameterProvenance.")
    if not isinstance(records, tuple) or not records:
        raise ValueError("records must be a nonempty tuple.")
    if not all(
        isinstance(record, FLiBeRegisteredDensityRecord)
        for record in records
    ):
        raise TypeError(
            "records must contain FLiBeRegisteredDensityRecord instances."
        )
    if len({record.dataset_id for record in records}) != 1:
        raise ValueError(
            "one comparison must use one registered dataset identity."
        )
    if len({record.source_file_sha256 for record in records}) != 1:
        raise ValueError(
            "one comparison must use one registered source fingerprint."
        )

    model_id = _identifier(model_id, "model_id")
    trajectory_id = _identifier(trajectory_id, "trajectory_id")
    physical_state_id = _identifier(physical_state_id, "physical_state_id")
    physical_state_method_id = _identifier(
        physical_state_method_id, "physical_state_method_id"
    )
    observed_pressure_method_id = _identifier(
        observed_pressure_method_id,
        "observed_pressure_method_id",
    )

    first = _selection(
        first_interval_index, "first_interval_index", allow_zero=True
    )
    step = _selection(stride, "stride", allow_zero=False)
    count = len(observables.samples)

    if first >= count:
        raise ValueError(
            "first_interval_index must select an existing MD interval."
        )

    indices = tuple(range(first, count, step))
    chosen = tuple(observables.samples[i] for i in indices)
    trace = observables.trajectory

    first_pressure = trace.steps[indices[0]].pressure
    mass_factor = first_pressure.mass_unit_to_kg
    length_factor = first_pressure.coordinate_unit_to_meter
    time_factor = first_pressure.time_unit_to_second

    initial = trace.initial.md_state
    total_mass_kg = fsum(initial.masses) * mass_factor

    if not isfinite(total_mass_kg) or total_mass_kg <= 0.0:
        raise ValueError(
            "total cell mass in SI must be finite and positive."
        )

    density_samples = []

    for index, sample in zip(indices, chosen, strict=True):
        current = trace.steps[index].barostat.current.md_state

        if current.configuration.species != initial.configuration.species:
            raise ValueError(
                "FLiBe species ordering changed across MD samples."
            )
        if current.masses != initial.masses:
            raise ValueError(
                "MD mass inventory changed across samples."
            )
        if current.configuration.periodic != (True, True, True):
            raise ValueError(
                "registered density requires a fully periodic MD cell."
            )

        density_expected = total_mass_kg / sample.volume_m3
        if not isclose(
            sample.density_kg_m3,
            density_expected,
            rel_tol=1e-11,
        ):
            raise ValueError(
                "density differs from the mass and post-barostat volume."
            )

        density_samples.append(
            FLiBeDensitySample(
                state_index=index + 1,
                md_step=current.step,
                md_time=current.time,
                cell_volume_m3=sample.volume_m3,
                density_kg_m3=sample.density_kg_m3,
            )
        )

    density = FLiBeTrajectoryDensity(
        model_id=model_id,
        trajectory_id=trajectory_id,
        provenance=provenance,
        composition=FLiBeConfiguration(
            initial.configuration
        ).composition(),
        atom_count=initial.atom_count,
        total_mass_kg=total_mass_kg,
        mass_unit_to_kg=mass_factor,
        coordinate_unit_to_meter=length_factor,
        samples=tuple(density_samples),
    )

    pressures = tuple(
        sample.total_pressure_pa for sample in chosen
    )
    signed_mean = fsum(pressures) / len(pressures)

    observed_pressure = (
        FLiBePressureCoordinate(
            pressure_pa=signed_mean,
            role=FLiBePressureRole.OBSERVED,
            method_id=observed_pressure_method_id,
            source_id=trajectory_id,
            provenance=provenance,
        )
        if signed_mean >= 0.0
        else None
    )

    coordinates = FLiBeTrajectoryStateCoordinates(
        density_trace=density,
        kinetic_temperature_k=tuple(
            sample.kinetic_temperature_k
            for sample in chosen
        ),
        degrees_of_freedom=observables.degrees_of_freedom,
        time_unit_to_second=time_factor,
        physical_state_id=physical_state_id,
        physical_state_method_id=physical_state_method_id,
        pressure=observed_pressure,
    )

    comparison = compare_flibe_registered_density_records(
        coordinates,
        records,
        mapping=mapping,
        temperature_tolerance_k=temperature_tolerance_k,
        pressure_tolerance_pa=pressure_tolerance_pa,
    )

    return FLiBeRankTwoRegisteredDensityCorrespondence(
        observables=observables,
        selected_interval_indices=indices,
        model_coordinates=coordinates,
        signed_post_barostat_pressures_pa=pressures,
        comparison=comparison,
    )
