"""Conservative Cartesian forces for stationary FLiBe finite-cluster polarization.

The source-parameter finite-cluster energy is the sum of the ionic pair
potential and the stationary induced-fluoride-dipole functional. At the
stationary dipoles the coordinate derivative follows the envelope theorem:

    F_i = -partial_R_i [E_pair(R) + U_pol(R, mu)] at mu=mu*(R).

The self-polarization term is constant in R at fixed dipoles. The
charge-dipole and dipole-dipole terms are differentiated analytically,
including the registered charge-field damping derivative. Output forces
are in hartree per input Cartesian coordinate unit, consistent with the
existing finite-cluster pair-force contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, fsum, isclose, isfinite, sqrt

from tr_eif.energy import ForceState

from .charge import configuration_formal_charges
from .configuration import FLiBeConfiguration
from .finite_cluster_polarization import (
    FLiBeFiniteClusterPolarizationModel,
    FLiBeFiniteClusterPolarizationResult,
)
from .species import FLiBeSpecies


Vector3 = tuple[float, float, float]
FORCE_FUNCTIONAL_ID = "flibe.finite_cluster.stationary_polarization_forces.v1"


def _dot(a: Vector3, b: Vector3) -> float:
    return fsum(a[axis] * b[axis] for axis in range(3))


def _damping_and_derivative(radius: float, beta: float, c: float) -> tuple[float, float]:
    """Compute source charge-field damping g(r) and dg/dr in bohr units.

    g(r) = 1 - c exp(-beta*r) sum((beta*r)**k/k!, k=0..4).
    dg/dr = c beta exp(-beta*r) (beta*r)**4/4!.
    """
    z = beta * radius
    if not isfinite(z) or z <= 0.0:
        raise ValueError("charge-dipole damping argument must be finite and positive.")
    if z >= 100.0:
        return 1.0, 0.0
    exponential = exp(-z)
    polynomial = 1.0 + z * (1.0 + z * (0.5 + z * (1.0 / 6.0 + z / 24.0)))
    damping = 1.0 - c * exponential * polynomial
    derivative = c * beta * exponential * z**4 / 24.0
    if not isfinite(damping) or not isfinite(derivative):
        raise ValueError("charge-dipole damping and derivative must be finite.")
    return damping, derivative


@dataclass(frozen=True, slots=True)
class FLiBeFiniteClusterPolarizationForceResult:
    """Variational polarization and total forces for one stationary state."""

    polarization_result: FLiBeFiniteClusterPolarizationResult
    polarization_forces: ForceState
    total_forces: ForceState
    functional_id: str = FORCE_FUNCTIONAL_ID

    def __post_init__(self) -> None:
        if not isinstance(self.polarization_result, FLiBeFiniteClusterPolarizationResult):
            raise TypeError("polarization_result must be FLiBeFiniteClusterPolarizationResult.")
        if not isinstance(self.polarization_forces, ForceState):
            raise TypeError("polarization_forces must be ForceState.")
        if not isinstance(self.total_forces, ForceState):
            raise TypeError("total_forces must be ForceState.")
        if self.functional_id != FORCE_FUNCTIONAL_ID:
            raise ValueError("force functional identity differs.")
        number = self.polarization_result.configuration.atom_count
        if self.polarization_forces.atom_count != number or self.total_forces.atom_count != number:
            raise ValueError("force cardinality must equal atomic configuration cardinality.")
        pair = self.polarization_result.pair_result.forces.forces
        for atom in range(number):
            for axis in range(3):
                expected = fsum((pair[atom][axis], self.polarization_forces.forces[atom][axis]))
                if not isclose(
                    self.total_forces.forces[atom][axis], expected,
                    rel_tol=1.0e-12, abs_tol=1.0e-12,
                ):
                    raise ValueError("total forces must sum pair and polarization contributions.")

    @property
    def configuration(self) -> FLiBeConfiguration:
        """Return the evaluated FLiBe configuration."""
        return self.polarization_result.configuration

    @property
    def total_energy_hartree(self) -> float:
        """Return the potential energy associated with the total forces."""
        return self.polarization_result.total_energy_hartree


def evaluate_flibe_finite_cluster_polarization_forces(
    model: FLiBeFiniteClusterPolarizationModel,
    configuration: FLiBeConfiguration,
) -> FLiBeFiniteClusterPolarizationForceResult:
    """Evaluate the stationary total-energy gradient in Cartesian coordinates.

    Every charge-field term contributes equal and opposite Cartesian forces
    to its fluoride receiver and charge source. Every fluoride-dipole pair
    contributes equal and opposite forces once. Dipoles are solved by the
    existing stationary model, then held stationary under differentiation.
    """
    if not isinstance(model, FLiBeFiniteClusterPolarizationModel):
        raise TypeError("model must be FLiBeFiniteClusterPolarizationModel.")
    if not isinstance(configuration, FLiBeConfiguration):
        raise TypeError("configuration must be FLiBeConfiguration.")

    result = model.evaluate(configuration)
    factor = model.coordinate_unit_to_bohr
    positions = tuple(
        tuple(float(x) * factor for x in point)
        for point in configuration.configuration.positions
    )
    charges = configuration_formal_charges(configuration)
    species = configuration.species
    dipoles = result.induced_dipoles_e_bohr
    fluoride = result.polarizable_indices
    damping_by_source = {
        item.species_pair[0]: (item.b_inverse_bohr, item.c_dimensionless)
        for item in model.parameters.charge_dipole_damping
    }
    forces = [[0.0, 0.0, 0.0] for _ in range(configuration.atom_count)]

    for i in fluoride:
        mu = dipoles[i]
        for j in range(configuration.atom_count):
            if i == j:
                continue
            delta = tuple(positions[i][a] - positions[j][a] for a in range(3))
            r2 = _dot(delta, delta)
            if not isfinite(r2) or r2 <= 0.0:
                raise ValueError("charge-field pair distance must be finite and positive.")
            r = sqrt(r2)
            damping, derivative = (1.0, 0.0)
            if species[j] in damping_by_source:
                beta, c = damping_by_source[species[j]]
                damping, derivative = _damping_and_derivative(r, beta, c)
            inv_r3 = 1.0 / (r2 * r)
            coeff_mu = charges[j] * damping * inv_r3
            coeff_delta = charges[j] * _dot(mu, delta) * (
                derivative / (r2 * r2) - 3.0 * damping * inv_r3 / r2
            )
            for axis in range(3):
                contribution = factor * (coeff_mu * mu[axis] + coeff_delta * delta[axis])
                forces[i][axis] += contribution
                forces[j][axis] -= contribution

    for local_i, i in enumerate(fluoride):
        mu_i = dipoles[i]
        for j in fluoride[local_i + 1:]:
            mu_j = dipoles[j]
            delta = tuple(positions[i][a] - positions[j][a] for a in range(3))
            r2 = _dot(delta, delta)
            if not isfinite(r2) or r2 <= 0.0:
                raise ValueError("dipole pair distance must be finite and positive.")
            r = sqrt(r2)
            inv_r5 = 1.0 / (r2 * r2 * r)
            inv_r7 = inv_r5 / r2
            a = _dot(mu_i, delta)
            b = _dot(mu_j, delta)
            c = _dot(mu_i, mu_j)
            for axis in range(3):
                contribution = factor * (
                    3.0 * inv_r5 * (c * delta[axis] + b * mu_i[axis] + a * mu_j[axis])
                    - 15.0 * a * b * inv_r7 * delta[axis]
                )
                forces[i][axis] += contribution
                forces[j][axis] -= contribution

    if any(not isfinite(value) for row in forces for value in row):
        raise ValueError("polarization forces must contain finite Cartesian components.")
    polarization_forces = ForceState(forces=tuple(tuple(row) for row in forces))
    pair_forces = result.pair_result.forces.forces
    total_forces = ForceState(forces=tuple(
        tuple(fsum((pair_forces[i][axis], forces[i][axis])) for axis in range(3))
        for i in range(configuration.atom_count)
    ))
    return FLiBeFiniteClusterPolarizationForceResult(
        polarization_result=result,
        polarization_forces=polarization_forces,
        total_forces=total_forces,
    )
