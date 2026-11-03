"""Combined periodic FLiBe fixed-charge and stationary-polarization energy.

The complete fixed-cell potential combines three explicitly evaluated terms:

    E_total = E_Ewald_Coulomb + E_Born_Mayer_C6_C8 + U_polarization.

The first two terms come from FLiBePeriodicFixedChargeModel; the stationary
induced-fluoride-dipole contribution comes from FLiBePeriodicPolarizationModel
and its conservative-force evaluator. Each term retains its source and
numerical Ewald settings. Cartesian forces use hartree per input length unit.

Stationarity provides a fluoride-site allocation of the polarization energy:

    U_i = -0.5 * mu_i dot E_i^charge.

This site allocation is combined with the registered fixed-charge atomic
energy partition, and its sum is checked against the complete scalar energy.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isclose

from tr_eif.energy import EnergyState, ForceState

from .configuration import FLiBeConfiguration
from .periodic_fixed_charge import (
    FLiBePeriodicFixedChargeModel,
    FLiBePeriodicFixedChargeResult,
)
from .periodic_polarization import FLiBePeriodicPolarizationModel
from .periodic_polarization_forces import (
    FLiBePeriodicPolarizationForceResult,
    evaluate_flibe_periodic_polarization_forces,
)


POLARIZABLE_PERIODIC_FUNCTIONAL_ID = (
    "flibe.periodic.fixed_charge_stationary_polarization.v1"
)


def _identifier(value: str, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be a nonempty trimmed string.")
    return value


def _site_polarization_energies(
    polarization: FLiBePeriodicPolarizationForceResult,
) -> tuple[float, ...]:
    """Allocate stationary polarization energy to its fluoride dipole sites."""

    state = polarization.polarization_result

    return tuple(
        -0.5 * fsum(mu[k] * field[k] for k in range(3))
        for mu, field in zip(
            state.induced_dipoles_e_bohr,
            state.charge_fields_atomic,
            strict=True,
        )
    )


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizableResult:
    """Eight-term periodic energy and conservative-force composition."""

    configuration: FLiBeConfiguration
    model_id: str
    fixed_charge_result: FLiBePeriodicFixedChargeResult
    polarization_force_result: FLiBePeriodicPolarizationForceResult
    energy: EnergyState
    forces: ForceState
    polarization_atomic_energies_hartree: tuple[float, ...]
    functional_id: str = POLARIZABLE_PERIODIC_FUNCTIONAL_ID

    def __post_init__(self) -> None:
        if not isinstance(self.configuration, FLiBeConfiguration):
            raise TypeError(
                "configuration must be FLiBeConfiguration."
            )

        _identifier(self.model_id, "model_id")

        if self.functional_id != POLARIZABLE_PERIODIC_FUNCTIONAL_ID:
            raise ValueError(
                "periodic polarizable functional identity differs."
            )

        if not isinstance(
            self.fixed_charge_result,
            FLiBePeriodicFixedChargeResult,
        ):
            raise TypeError(
                "fixed_charge_result must be FLiBePeriodicFixedChargeResult."
            )

        if not isinstance(
            self.polarization_force_result,
            FLiBePeriodicPolarizationForceResult,
        ):
            raise TypeError(
                "polarization_force_result must be "
                "FLiBePeriodicPolarizationForceResult."
            )

        fixed = self.fixed_charge_result
        polarization = self.polarization_force_result.polarization_result

        if (
            fixed.configuration != self.configuration
            or polarization.configuration != self.configuration
        ):
            raise ValueError(
                "component results must share the exact atomic configuration."
            )

        if fixed.ewald_result.parameters != polarization.ewald_parameters:
            raise ValueError(
                "component Ewald parameters must agree."
            )

        if (
            fixed.source_doi != polarization.source_doi
            or fixed.source_file_sha256 != polarization.source_file_sha256
        ):
            raise ValueError(
                "component coefficient source identities must agree."
            )

        if not isinstance(self.energy, EnergyState):
            raise TypeError("energy must be EnergyState.")

        if not isinstance(self.forces, ForceState):
            raise TypeError("forces must be ForceState.")

        n = self.configuration.atom_count

        if self.energy.atom_count != n or self.forces.atom_count != n:
            raise ValueError(
                "energy and force cardinalities must match atom count."
            )

        if (
            not isinstance(self.polarization_atomic_energies_hartree, tuple)
            or len(self.polarization_atomic_energies_hartree) != n
        ):
            raise ValueError(
                "polarization atomic energies must match atom count."
            )

        expected_atomic = _site_polarization_energies(
            self.polarization_force_result
        )

        for actual, expected in zip(
            self.polarization_atomic_energies_hartree,
            expected_atomic,
            strict=True,
        ):
            if not isclose(
                actual,
                expected,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ):
                raise ValueError(
                    "polarization atomic energies must follow stationary dipoles."
                )

        pol_energy = polarization.polarization_energy_hartree

        dipole_magnitude_sum = fsum(
            abs(component)
            for mu in polarization.induced_dipoles_e_bohr
            for component in mu
        )

        stationary_tol = (
            1e-12 * max(1.0, abs(pol_energy))
            + 0.5
            * polarization.max_stationarity_residual_atomic
            * dipole_magnitude_sum
        )

        if not isclose(
            fsum(expected_atomic),
            pol_energy,
            rel_tol=0.0,
            abs_tol=stationary_tol,
        ):
            raise ValueError(
                "stationary site energies must sum to polarization energy."
            )

        total = fsum((
            fixed.energy.total_energy,
            pol_energy,
        ))

        if not isclose(
            self.energy.total_energy,
            total,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            raise ValueError(
                "total energy must sum fixed charge and polarization."
            )

        if not isclose(
            fsum(self.energy.atomic_energies),
            total,
            rel_tol=0.0,
            abs_tol=stationary_tol,
        ):
            raise ValueError(
                "atomic energy partition must sum to total energy."
            )

        pol_forces = self.polarization_force_result.polarization_forces.forces

        for i in range(n):
            expected_energy = fsum((
                fixed.energy.atomic_energies[i],
                expected_atomic[i],
            ))

            if not isclose(
                self.energy.atomic_energies[i],
                expected_energy,
                rel_tol=1e-12,
                abs_tol=1e-12,
            ):
                raise ValueError(
                    "atomic energy must sum both model contributions."
                )

            for axis in range(3):
                expected_force = fsum((
                    fixed.forces.forces[i][axis],
                    pol_forces[i][axis],
                ))

                if not isclose(
                    self.forces.forces[i][axis],
                    expected_force,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ):
                    raise ValueError(
                        "total Cartesian forces must sum both model contributions."
                    )

        if not isclose(
            fsum(value for _, value in self.energy_components_hartree),
            total,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            raise ValueError(
                "eight energy components must sum to total energy."
            )

    @property
    def energy_components_hartree(self) -> tuple[tuple[str, float], ...]:
        """Return five fixed-charge and three stationary-polarization terms."""

        p = self.polarization_force_result.polarization_result

        return self.fixed_charge_result.energy_components_hartree + (
            ("polarization_self", p.self_energy_hartree),
            ("polarization_charge_dipole", p.charge_dipole_energy_hartree),
            ("polarization_dipole_dipole", p.dipole_dipole_energy_hartree),
        )

    @property
    def source_doi(self) -> str:
        """Return the registered interatomic-coefficient source DOI."""

        return self.fixed_charge_result.source_doi

    @property
    def source_file_sha256(self) -> str:
        """Return the registered parameter-file SHA-256 fingerprint."""

        return self.fixed_charge_result.source_file_sha256

    @property
    def coordinate_unit_to_bohr(self) -> float:
        """Return the common input-coordinate conversion to bohr."""

        return self.fixed_charge_result.coordinate_unit_to_bohr

    @property
    def max_stationarity_residual_atomic(self) -> float:
        """Return the solved fluoride-dipole stationarity residual."""

        return (
            self.polarization_force_result
            .polarization_result
            .max_stationarity_residual_atomic
        )


@dataclass(frozen=True, slots=True)
class FLiBePeriodicPolarizableModel:
    """Compose source-aligned periodic fixed charge and stationary polarization."""

    model_id: str
    fixed_charge_model: FLiBePeriodicFixedChargeModel
    polarization_model: FLiBePeriodicPolarizationModel

    def __post_init__(self) -> None:
        _identifier(self.model_id, "model_id")

        if not isinstance(
            self.fixed_charge_model,
            FLiBePeriodicFixedChargeModel,
        ):
            raise TypeError(
                "fixed_charge_model must be FLiBePeriodicFixedChargeModel."
            )

        if not isinstance(
            self.polarization_model,
            FLiBePeriodicPolarizationModel,
        ):
            raise TypeError(
                "polarization_model must be FLiBePeriodicPolarizationModel."
            )

        if (
            self.fixed_charge_model.ewald_model.parameters
            != self.polarization_model.ewald_parameters
        ):
            raise ValueError(
                "fixed-charge and polarization Ewald parameters must agree."
            )

        if (
            self.fixed_charge_model.short_range_model.parameters
            != self.polarization_model.parameters
        ):
            raise ValueError(
                "fixed-charge and polarization coefficient tables must agree."
            )

    def evaluate(
        self,
        configuration: FLiBeConfiguration,
    ) -> FLiBePeriodicPolarizableResult:
        """Evaluate and combine energy and conservative forces at a common state."""

        if not isinstance(configuration, FLiBeConfiguration):
            raise TypeError(
                "configuration must be FLiBeConfiguration."
            )

        atomic = configuration.configuration

        if atomic.periodic != (True, True, True) or atomic.cell is None:
            raise ValueError(
                "periodic polarizable evaluation requires three periodic axes and a cell."
            )

        configuration.composition()

        fixed = self.fixed_charge_model.evaluate(configuration)

        polarized = evaluate_flibe_periodic_polarization_forces(
            self.polarization_model,
            configuration,
        )

        pol_energy = (
            polarized.polarization_result.polarization_energy_hartree
        )

        atomic_pol = _site_polarization_energies(polarized)

        energies = tuple(
            fsum((base, addition))
            for base, addition in zip(
                fixed.energy.atomic_energies,
                atomic_pol,
                strict=True,
            )
        )

        forces = tuple(
            tuple(
                fsum((
                    fixed.forces.forces[i][axis],
                    polarized.polarization_forces.forces[i][axis],
                ))
                for axis in range(3)
            )
            for i in range(configuration.atom_count)
        )

        return FLiBePeriodicPolarizableResult(
            configuration=configuration,
            model_id=self.model_id,
            fixed_charge_result=fixed,
            polarization_force_result=polarized,
            polarization_atomic_energies_hartree=atomic_pol,
            energy=EnergyState(
                energies,
                fsum((
                    fixed.energy.total_energy,
                    pol_energy,
                )),
            ),
            forces=ForceState(forces),
        )
