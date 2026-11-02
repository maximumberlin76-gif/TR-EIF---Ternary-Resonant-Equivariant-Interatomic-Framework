"""Combined periodic FLiBe fixed-charge energy and Cartesian forces.

The periodic energy is the sum of the three-dimensional neutral Ewald
Coulomb functional and the registered Born-Mayer/Tang-Toennies short-range
functional:

    E = E_ewald_real + E_ewald_reciprocal + E_ewald_self
        + E_short_range_cross + E_short_range_self_images.

The Ewald component supplies the formal-charge Coulomb interaction exactly
once. The short-range component supplies Born-Mayer and damped C6/C8 terms.
Induced-dipole polarization retains its separate energy and force interface.
Both operators share the atomic configuration and the Cartesian unit-to-bohr
conversion. Energy is in hartree; forces are in hartree per input length unit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose

from tr_eif.energy import EnergyState, ForceState

from .configuration import FLiBeConfiguration
from .periodic_coulomb_ewald import FLiBePeriodicEwaldModel, FLiBePeriodicEwaldResult
from .periodic_short_range import FLiBePeriodicShortRangeModel, FLiBePeriodicShortRangeResult


PERIODIC_FIXED_CHARGE_FUNCTIONAL_ID = "flibe.periodic.fixed_charge_ewald_born_mayer_tt.v1"


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


@dataclass(frozen=True, slots=True)
class FLiBePeriodicFixedChargeResult:
    """Five-term periodic energy decomposition and combined conservative forces."""

    configuration: FLiBeConfiguration
    model_id: str
    ewald_result: FLiBePeriodicEwaldResult
    short_range_result: FLiBePeriodicShortRangeResult
    energy: EnergyState
    forces: ForceState
    functional_id: str = PERIODIC_FIXED_CHARGE_FUNCTIONAL_ID

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        _identifier(self.model_id, "model_id")
        if self.functional_id != PERIODIC_FIXED_CHARGE_FUNCTIONAL_ID:
            raise ValueError("periodic fixed-charge functional identity differs.")
        if not isinstance(self.ewald_result, FLiBePeriodicEwaldResult):
            raise TypeError("ewald_result must be FLiBePeriodicEwaldResult.")
        if not isinstance(self.short_range_result, FLiBePeriodicShortRangeResult):
            raise TypeError("short_range_result must be FLiBePeriodicShortRangeResult.")
        if (
            self.ewald_result.configuration != self.configuration
            or self.short_range_result.configuration != self.configuration
        ):
            raise ValueError("component results must use the same atomic configuration.")
        if (
            self.ewald_result.parameters.coordinate_unit_to_bohr
            != self.short_range_result.coordinate_unit_to_bohr
        ):
            raise ValueError("component coordinate-to-bohr conversions must agree.")
        if not isinstance(self.energy, EnergyState):
            raise TypeError("energy must be EnergyState.")
        if not isinstance(self.forces, ForceState):
            raise TypeError("forces must be ForceState.")
        count = self.configuration.atom_count
        if self.energy.atom_count != count or self.forces.atom_count != count:
            raise ValueError("combined energy and force cardinalities must match atom count.")

        ewald = self.ewald_result
        short_range = self.short_range_result
        expected_total = fsum((ewald.energy.total_energy, short_range.energy.total_energy))
        if not isclose(self.energy.total_energy, expected_total, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("combined energy must equal Ewald plus short-range energy.")
        if not isclose(
            self.energy.total_energy, fsum(self.energy.atomic_energies),
            rel_tol=1e-12, abs_tol=1e-12,
        ):
            raise ValueError("combined atomic energy partition must equal total energy.")
        for index in range(count):
            expected_atom = fsum((
                ewald.energy.atomic_energies[index],
                short_range.energy.atomic_energies[index],
            ))
            if not isclose(self.energy.atomic_energies[index], expected_atom,
                           rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError("combined atomic energy must equal component energies.")
            for axis in range(3):
                expected_force = fsum((
                    ewald.forces.forces[index][axis],
                    short_range.forces.forces[index][axis],
                ))
                if not isclose(self.forces.forces[index][axis], expected_force,
                               rel_tol=1e-12, abs_tol=1e-12):
                    raise ValueError("combined forces must equal component forces.")

    @property
    def coordinate_unit_to_bohr(self) -> float:
        """Return the shared input-coordinate conversion to bohr."""
        return self.ewald_result.parameters.coordinate_unit_to_bohr

    @property
    def source_doi(self) -> str:
        """Return the registered short-range parameter publication DOI."""
        return self.short_range_result.source_doi

    @property
    def source_file_sha256(self) -> str:
        """Return the registered short-range parameter-file fingerprint."""
        return self.short_range_result.source_file_sha256

    @property
    def energy_components_hartree(self) -> tuple[tuple[str, float], ...]:
        """Return the five independently retained energy terms in stable order."""
        ewald = self.ewald_result
        short_range = self.short_range_result
        return (
            ("ewald_real", ewald.real_energy_hartree),
            ("ewald_reciprocal", ewald.reciprocal_energy_hartree),
            ("ewald_self", ewald.self_energy_hartree),
            ("short_range_cross_atom", short_range.cross_atom_energy_hartree),
            ("short_range_self_image", short_range.self_image_energy_hartree),
        )


@dataclass(frozen=True, slots=True)
class FLiBePeriodicFixedChargeModel:
    """Compose compatible periodic Ewald and source-parameter short-range models."""

    model_id: str
    ewald_model: FLiBePeriodicEwaldModel
    short_range_model: FLiBePeriodicShortRangeModel

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")
        if not isinstance(self.ewald_model, FLiBePeriodicEwaldModel):
            raise TypeError("ewald_model must be FLiBePeriodicEwaldModel.")
        if not isinstance(self.short_range_model, FLiBePeriodicShortRangeModel):
            raise TypeError("short_range_model must be FLiBePeriodicShortRangeModel.")
        if (
            self.ewald_model.parameters.coordinate_unit_to_bohr
            != self.short_range_model.coordinate_unit_to_bohr
        ):
            raise ValueError("Ewald and short-range coordinate-to-bohr conversions must agree.")

    def evaluate(self, configuration: FLiBeConfiguration) -> FLiBePeriodicFixedChargeResult:
        """Add Ewald and short-range energies and forces on one periodic state."""
        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError("configuration must be FLiBeConfiguration.")
        atomic = configuration.configuration
        if atomic.periodic != (True, True, True) or atomic.cell is None:
            raise ValueError("periodic fixed-charge evaluation requires three periodic axes and a cell.")
        configuration.composition()

        ewald = self.ewald_model.evaluate(configuration)
        short_range = self.short_range_model.evaluate(configuration)
        count = configuration.atom_count
        atomic_energies = tuple(fsum((
            ewald.energy.atomic_energies[index],
            short_range.energy.atomic_energies[index],
        )) for index in range(count))
        total_energy = fsum((ewald.energy.total_energy, short_range.energy.total_energy))
        forces = tuple(tuple(fsum((
            ewald.forces.forces[index][axis],
            short_range.forces.forces[index][axis],
        )) for axis in range(3)) for index in range(count))
        return FLiBePeriodicFixedChargeResult(
            configuration=configuration,
            model_id=self.model_id,
            ewald_result=ewald,
            short_range_result=short_range,
            energy=EnergyState(atomic_energies, total_energy),
            forces=ForceState(forces),
        )
